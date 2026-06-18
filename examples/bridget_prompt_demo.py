"""Sanitized Bridget prompt logic example.

Bridget is the assistant layer for The Human Model. This demo shows how a
profile, prompt budget, daily state, and missing-data policy can produce
low-friction prompts without exposing private schedules or live bot code.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, time
from typing import Optional


PROMPT_KINDS = {"morning", "post_gym", "evening"}
PROMPT_MODES = {"minimal", "standard", "coachy"}


@dataclass
class BridgetProfile:
    gym_days: list[int] = field(default_factory=lambda: [0, 2, 4])
    gym_start: str = "07:00"
    gym_done_by: str = "09:00"
    quiet_after: str = "21:30"
    prompt_mode: str = "minimal"
    prompt_budgets: dict[str, int] = field(
        default_factory=lambda: {"minimal": 2, "standard": 3, "coachy": 4}
    )


@dataclass
class BridgetDayState:
    sent_prompts: list[str] = field(default_factory=list)
    ignored: bool = False
    workout_status: str = "unknown"
    notes: list[str] = field(default_factory=list)


@dataclass
class BridgetState:
    days: dict[str, BridgetDayState] = field(default_factory=dict)


@dataclass(frozen=True)
class QuickReply:
    action: str
    value: Optional[str] = None


def _parse_time(value: str) -> time:
    hour, minute = value.split(":", 1)
    return time(int(hour), int(minute))


def get_day_state(state: BridgetState, date: str) -> BridgetDayState:
    if date not in state.days:
        state.days[date] = BridgetDayState()
    return state.days[date]


def is_expected_gym_day(date: str, profile: BridgetProfile) -> bool:
    return datetime.fromisoformat(date).weekday() in profile.gym_days


def _watch_data_missing(health_row: Optional[dict]) -> bool:
    if not health_row:
        return True
    return not any(value is not None for value in health_row.values())


def should_send_prompt(
    kind: str,
    now: datetime,
    profile: BridgetProfile,
    state: BridgetState,
    health_row: Optional[dict] = None,
) -> bool:
    if kind not in PROMPT_KINDS:
        raise ValueError(f"Unknown prompt kind: {kind}")
    if profile.prompt_mode not in PROMPT_MODES:
        raise ValueError(f"Unknown prompt mode: {profile.prompt_mode}")

    date = now.date().isoformat()
    day_state = get_day_state(state, date)
    if day_state.ignored or kind in day_state.sent_prompts:
        return False
    if now.time() >= _parse_time(profile.quiet_after):
        return False
    if len(day_state.sent_prompts) >= profile.prompt_budgets[profile.prompt_mode]:
        return False

    expected_gym = is_expected_gym_day(date, profile)
    unresolved_workout = day_state.workout_status in {"unknown", "later", "trained_later"}

    if kind == "morning":
        return now.weekday() < 5 or _watch_data_missing(health_row)
    if kind == "post_gym":
        return expected_gym and unresolved_workout
    if kind == "evening":
        return expected_gym and unresolved_workout
    return False


def format_morning_prompt(date: str, profile: BridgetProfile, health_row: Optional[dict]) -> str:
    lines = ["Good morning. I hope you slept well."]
    if health_row and health_row.get("sleep_hours") is not None:
        lines.append(f"I have sleep at {health_row['sleep_hours']:.1f}h.")
    else:
        lines.append(
            "I am still waiting for health data to sync, so I am flying with partial info."
        )
        lines.append("Anything you want me to know about sleep before I make assumptions?")

    if is_expected_gym_day(date, profile):
        lines.append(f"I am assuming a normal gym window: {profile.gym_start}-{profile.gym_done_by}.")
    else:
        lines.append("I am not assuming a gym session today.")

    if _watch_data_missing(health_row):
        lines.append("Missing watch data means low confidence, not bad recovery.")
    lines.append("No need to answer if this is right.")
    lines.append("Quick replies: ok / no gym / slept 7h / sore / sick / remind me later")
    return "\n".join(lines)


def parse_quick_reply(text: str) -> Optional[QuickReply]:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    sleep_match = re.search(r"\b(?:slept\s*)?(\d+(?:\.\d+)?)\s*h(?:ours?)?\b", normalized)
    if sleep_match:
        return QuickReply("sleep_hours", sleep_match.group(1))

    replies = {
        "ok": QuickReply("ok"),
        "no gym": QuickReply("workout_status", "no_gym"),
        "later": QuickReply("workout_status", "later"),
        "remind me later": QuickReply("workout_status", "later"),
        "sore": QuickReply("note", "sore"),
        "sick": QuickReply("note", "sick"),
        "watch off": QuickReply("watch_off"),
        "ignore today": QuickReply("ignore_today"),
    }
    return replies.get(normalized)


def apply_quick_reply(reply: QuickReply, state: BridgetState, date: str) -> str:
    day_state = get_day_state(state, date)
    if reply.action == "workout_status" and reply.value:
        day_state.workout_status = reply.value
        return f"Marked workout status as {reply.value}."
    if reply.action == "ignore_today":
        day_state.ignored = True
        return "Done. I will ignore today's Bridget loop."
    if reply.action == "note" and reply.value:
        day_state.notes.append(reply.value)
        return f"Noted: {reply.value}."
    if reply.action == "sleep_hours" and reply.value:
        day_state.notes.append(f"sleep: {reply.value}h")
        return f"Using {reply.value}h sleep for today's context."
    if reply.action == "watch_off":
        day_state.notes.append("watch off")
        return "I will not overread missing watch data today."
    return "Got it."


def main() -> None:
    profile = BridgetProfile()
    state = BridgetState()
    now = datetime(2026, 6, 17, 6, 45)
    date = now.date().isoformat()
    if should_send_prompt("morning", now, profile, state, health_row=None):
        print(format_morning_prompt(date, profile, health_row=None))
    reply = parse_quick_reply("slept 7h")
    if reply:
        print(apply_quick_reply(reply, state, date))


if __name__ == "__main__":
    main()
