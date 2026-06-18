import unittest
from datetime import datetime
from pathlib import Path
import sys

EXAMPLES_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLES_DIR))

from bridget_prompt_demo import (  # noqa: E402
    BridgetDayState,
    BridgetProfile,
    BridgetState,
    apply_quick_reply,
    format_morning_prompt,
    parse_quick_reply,
    should_send_prompt,
)
from daily_card_demo import render_svg, sample_card  # noqa: E402
from readiness_scoring_demo import (  # noqa: E402
    RecoveryDay,
    TrainingContext,
    calculate_readiness,
    sample_history,
)


class ReadinessScoringDemoTests(unittest.TestCase):
    def test_good_day_can_push_or_maintain_with_training_load(self):
        target = RecoveryDay("2026-06-17", 7.6, 83, 52, 8, 3, "Good")
        result = calculate_readiness(
            target,
            sample_history(),
            TrainingContext(trained_yesterday=True, workout_days_7d=4),
        )

        self.assertIsNotNone(result.score)
        self.assertIn(result.status, {"Push", "Maintain"})
        self.assertIn(result.confidence, {"Medium", "High"})

    def test_low_energy_forces_rest(self):
        target = RecoveryDay("2026-06-17", 7.2, 82, 52, 3, 4, "Good")
        result = calculate_readiness(target, sample_history(), TrainingContext())

        self.assertEqual(result.status, "Rest")
        self.assertIn("energy 3 or lower", result.factors)


class BridgetPromptDemoTests(unittest.TestCase):
    def test_missing_health_data_uses_uncertainty_language(self):
        text = format_morning_prompt("2026-06-17", BridgetProfile(), None)

        self.assertIn("waiting for health data to sync", text)
        self.assertIn("low confidence, not bad recovery", text)

    def test_prompt_budget_prevents_extra_prompt(self):
        profile = BridgetProfile(prompt_mode="minimal")
        state = BridgetState()
        day = state.days.setdefault("2026-06-17", BridgetDayState())
        day.sent_prompts = ["morning", "post_gym"]

        self.assertFalse(
            should_send_prompt(
                "evening",
                datetime(2026, 6, 17, 18, 0),
                profile,
                state,
            )
        )

    def test_quick_reply_updates_state(self):
        state = BridgetState()
        reply = parse_quick_reply("slept 7h")
        message = apply_quick_reply(reply, state, "2026-06-17")

        self.assertIn("7", message)
        self.assertIn("sleep: 7h", state.days["2026-06-17"].notes)


class DailyCardDemoTests(unittest.TestCase):
    def test_render_svg_contains_core_fields(self):
        svg = render_svg(sample_card())

        self.assertIn("<svg", svg)
        self.assertIn("Bridget daily card", svg)
        self.assertIn("Modify", svg)
        self.assertIn("68/100", svg)


if __name__ == "__main__":
    unittest.main()
