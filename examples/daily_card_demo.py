"""Render a public-safe Bridget daily card as SVG.

The private system can generate chat-friendly daily summaries from live data.
This demo uses mock data and standard-library SVG output so it can run in the
public overview repo with no image dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path
import textwrap


OUTPUT_PATH = Path(__file__).with_name("daily_card_demo.svg")


@dataclass(frozen=True)
class CardMetric:
    label: str
    value: str


@dataclass(frozen=True)
class DailyCard:
    date: str
    day_label: str
    final_call: str
    score: int | None
    confidence: str
    metrics: tuple[CardMetric, ...]
    signal: str
    nudge: str
    uncertainty: str


CALL_COLORS = {
    "Push": "#047857",
    "Maintain": "#2563eb",
    "Modify": "#b45309",
    "Rest": "#be123c",
}


def _text(x: int, y: int, value: str, size: int = 18, fill: str = "#0f172a", weight: str = "400") -> str:
    return (
        f'<text x="{x}" y="{y}" font-family="Inter, Arial, sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}">{escape(value)}</text>'
    )


def _wrapped_text(x: int, y: int, value: str, width: int, size: int = 18, fill: str = "#0f172a") -> list[str]:
    lines: list[str] = []
    for index, line in enumerate(textwrap.wrap(value, width=width)):
        lines.append(_text(x, y + index * (size + 8), line, size=size, fill=fill))
    return lines


def render_svg(card: DailyCard) -> str:
    color = CALL_COLORS.get(card.final_call, CALL_COLORS["Modify"])
    score = "--" if card.score is None else str(card.score)
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="900" height="1200" viewBox="0 0 900 1200">',
        '<rect width="900" height="1200" fill="#f8fafc"/>',
        '<rect x="40" y="40" width="820" height="1120" rx="32" fill="#ffffff" stroke="#e2e8f0"/>',
        _text(80, 105, "Bridget daily card", 22, "#64748b", "600"),
        _text(80, 152, f"{card.day_label} - {card.date}", 34, "#0f172a", "700"),
        '<rect x="80" y="210" width="740" height="210" rx="26" fill="#f1f5f9"/>',
        _text(115, 295, card.final_call, 76, color, "800"),
        _text(118, 372, f"{score}/100", 52, "#0f172a", "700"),
        '<rect x="592" y="330" width="190" height="48" rx="18" fill="#e2e8f0"/>',
        _text(616, 362, f"{card.confidence} confidence", 20, "#334155", "600"),
    ]

    x_positions = [80, 470]
    y = 480
    for index, metric in enumerate(card.metrics):
        x = x_positions[index % 2]
        row_y = y + (index // 2) * 100
        parts.extend(
            [
                f'<rect x="{x}" y="{row_y}" width="350" height="76" rx="16" fill="#f8fafc" stroke="#e2e8f0"/>',
                _text(x + 24, row_y + 30, metric.label.upper(), 15, "#64748b", "700"),
                _text(x + 24, row_y + 58, metric.value, 25, "#0f172a", "700"),
            ]
        )

    y = 690
    parts.append(_text(80, y, "Signal", 17, "#64748b", "700"))
    parts.extend(_wrapped_text(80, y + 42, card.signal, 58, 26))
    y += 170
    parts.append(_text(80, y, "Nudge", 17, "#64748b", "700"))
    parts.extend(_wrapped_text(80, y + 42, card.nudge, 58, 26))
    if card.uncertainty:
        parts.append('<rect x="80" y="1010" width="740" height="90" rx="18" fill="#fffbeb"/>')
        parts.extend(_wrapped_text(110, 1050, card.uncertainty, 58, 20, "#92400e"))
    parts.append("</svg>")
    return "\n".join(parts)


def sample_card() -> DailyCard:
    return DailyCard(
        date="2026-06-17",
        day_label="Wednesday",
        final_call="Modify",
        score=68,
        confidence="Medium",
        metrics=(
            CardMetric("Sleep", "7.4h"),
            CardMetric("HRV", "78ms"),
            CardMetric("RHR", "53bpm"),
            CardMetric("Energy", "7/10"),
        ),
        signal="Sleep duration is usable, but recent training load keeps the morning call flexible.",
        nudge="Start with the planned session, then let the first working set decide intensity.",
        uncertainty="This is mock data. In the private system, sync uncertainty is shown when health data is incomplete.",
    )


def main() -> None:
    OUTPUT_PATH.write_text(render_svg(sample_card()) + "\n")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
