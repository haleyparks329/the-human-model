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
from dashboard_data_shaping_demo import (  # noqa: E402
    ImportRun,
    body_trends,
    dashboard_payload,
    sample_body_rows,
    sample_imports,
    sample_sessions,
    signal_health,
    training_session_summary,
    weekly_volume,
)
from readiness_scoring_demo import (  # noqa: E402
    RecoveryDay,
    TrainingContext,
    calculate_readiness,
    sample_history,
)
from readiness_modeling_demo import (  # noqa: E402
    DailyFeature,
    movement_output_summary,
    report_lines,
    sample_history as modeling_sample_history,
    score_day,
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


class DashboardDataShapingDemoTests(unittest.TestCase):
    def test_body_trends_include_direction_and_delta(self):
        trends = {row["metric_name"]: row for row in body_trends(sample_body_rows())}

        self.assertEqual(trends["waist_cm"]["direction"], "down")
        self.assertEqual(trends["waist_cm"]["delta"], -0.6)
        self.assertEqual(trends["weight_kg"]["direction"], "up")

    def test_training_summary_flags_qualitative_loads(self):
        summary = training_session_summary(sample_sessions()[0])

        self.assertEqual(summary["exercise_count"], 3)
        self.assertEqual(summary["work_set_count"], 3)
        self.assertEqual(summary["volume_load"], 1390.0)
        self.assertTrue(summary["needs_review"])
        self.assertIn("chest", summary["muscle_groups"])
        self.assertIn("back", summary["muscle_groups"])
        self.assertIn("shoulders", summary["muscle_groups"])
        self.assertNotIn("triceps", summary["muscle_groups"])
        self.assertTrue(any("reps missing" in item for item in summary["review_warnings"]))

    def test_dashboard_payload_can_feed_review_surface(self):
        payload = dashboard_payload(sample_body_rows(), sample_sessions(), sample_imports())

        self.assertEqual(payload["signals"]["status"], "OK")
        self.assertIn("review", payload["daily_review_hint"])
        self.assertIn("body_trends", payload)
        self.assertIn("latest_training", payload)
        self.assertEqual(payload["weekly_volume"]["session_count"], 3)
        self.assertEqual(payload["progression_signals"][0]["exercise"], "Bench press")
        self.assertEqual(payload["progression_signals"][0]["status"], "up")

    def test_weekly_volume_groups_sessions_by_muscle(self):
        summary = weekly_volume(sample_sessions(), "2026-06-18")

        self.assertEqual(summary["work_sets"], 9)
        self.assertEqual(summary["muscle_group_counts"]["chest"], 2)

    def test_signal_health_surfaces_blocked_imports(self):
        health = signal_health(sample_imports() + [ImportRun("notion", "blocked", 0, 0)])

        self.assertEqual(health["status"], "Needs review")
        self.assertIn("notion", health["blocked_sources"])


class ReadinessModelingDemoTests(unittest.TestCase):
    def test_score_day_surfaces_quality_and_limiting_factor(self):
        target = DailyFeature("2026-06-23", 6.4, 72, 54, None, None, None, True)
        result = score_day(target, modeling_sample_history())

        self.assertEqual(result.band, "Yellow")
        self.assertEqual(result.data_quality, "Medium")
        self.assertEqual(result.limiting_factor, "hrv")
        self.assertIn("missing energy", result.model_notes)
        self.assertIn("Cautious training day", result.so_what)

    def test_report_lines_are_portfolio_readable(self):
        target = DailyFeature("2026-06-23", 7.6, 83, 52, 8, 3, 2, True)
        result = score_day(target, modeling_sample_history())
        text = "\n".join(report_lines(result))

        self.assertIn("Baseline Readiness Report", text)
        self.assertIn("Data Quality: High", text)
        self.assertIn("So What:", text)

    def test_movement_output_is_context_not_model_decision(self):
        target = DailyFeature("2026-06-23", 6.4, 72, 54, None, None, None, True, 410, 45)

        self.assertIn("45 min workout", movement_output_summary(target))


if __name__ == "__main__":
    unittest.main()
