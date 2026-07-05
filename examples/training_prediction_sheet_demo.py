"""Sanitized training-prediction-to-workout-sheet example.

The private system generates guarded next-session load predictions, then
Bridget turns those predictions into an editable workout sheet. This public
example keeps only the product behavior: preserve workout order, keep reps,
carry non-modelable loads forward, and leave space for actual training notes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionRow:
    exercise: str
    set_number: int
    set_role: str
    previous_reps: int | None
    model_recommended_weight_kg: float | None
    guarded_recommended_weight_kg: float | None
    previous_logged_weight_text: str = ""
    guardrail: str = "none"


def build_editable_workout_sheet(
    predictions: list[PredictionRow],
    exercise_order: dict[str, int],
    target_date: str,
    workout_name: str,
) -> list[dict[str, str]]:
    """Convert model output into rows a person can correct after training."""

    sorted_rows = sorted(
        predictions,
        key=lambda row: (
            exercise_order.get(row.exercise, 999),
            row.set_number,
            row.exercise,
        ),
    )
    sheet_rows: list[dict[str, str]] = []
    for row in sorted_rows:
        sheet_rows.append(
            {
                "date": target_date,
                "workout_name": workout_name,
                "exercise_order": _format_number(exercise_order.get(row.exercise)),
                "exercise": row.exercise,
                "set_number": str(row.set_number),
                "set_role": _set_role_label(row.set_role),
                "recommended_weight_kg": _recommendation_text(row),
                "recommended_reps": "" if row.previous_reps is None else str(row.previous_reps),
                "actual_weight_kg": "",
                "actual_reps": "",
                "notes": "",
                "guardrail": row.guardrail,
            }
        )
    return sheet_rows


def summarize_sheet(rows: list[dict[str, str]]) -> dict[str, object]:
    """Return the small review summary Bridget can use before sending a file."""

    guardrails = sorted(
        {row["guardrail"] for row in rows if row["guardrail"] and row["guardrail"] != "none"}
    )
    non_modelable = [
        row["exercise"]
        for row in rows
        if row["recommended_weight_kg"] and not _looks_numeric(row["recommended_weight_kg"])
    ]
    return {
        "set_count": len(rows),
        "exercise_count": len({row["exercise"] for row in rows}),
        "guardrails_applied": guardrails,
        "non_modelable_loads": tuple(dict.fromkeys(non_modelable)),
        "ready_for_bridget": bool(rows),
    }


def sample_predictions() -> list[PredictionRow]:
    return [
        PredictionRow(
            "Smith Machine Shoulder Press",
            1,
            "warmup_or_feeder",
            10,
            None,
            None,
            previous_logged_weight_text="machine weight",
        ),
        PredictionRow(
            "Smith Machine Shoulder Press",
            2,
            "working",
            10,
            7.5,
            7.5,
        ),
        PredictionRow(
            "Incline One Arm Dumbbell Front Raise",
            1,
            "warmup_or_feeder",
            10,
            8.0,
            7.5,
            guardrail="warmup_preserved",
        ),
        PredictionRow(
            "Smith Machine Incline Bench Press",
            1,
            "warmup_or_feeder",
            10,
            10.0,
            10.0,
            guardrail="warmup_preserved",
        ),
    ]


def sample_exercise_order() -> dict[str, int]:
    return {
        "Smith Machine Incline Bench Press": 1,
        "Incline One Arm Dumbbell Front Raise": 2,
        "Smith Machine Shoulder Press": 5,
    }


def _recommendation_text(row: PredictionRow) -> str:
    if row.guarded_recommended_weight_kg is not None:
        return _format_number(row.guarded_recommended_weight_kg)
    return row.previous_logged_weight_text


def _set_role_label(value: str) -> str:
    labels = {
        "warmup_or_feeder": "Warm-up/feeder",
        "working": "Working set",
        "top_set": "Top set",
    }
    return labels.get(value, value.replace("_", " ").title())


def _format_number(value: float | int | None) -> str:
    if value is None:
        return ""
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def _looks_numeric(value: str) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    return True


def main() -> None:
    rows = build_editable_workout_sheet(
        sample_predictions(),
        sample_exercise_order(),
        target_date="2026-07-05",
        workout_name="Delts",
    )
    for row in rows:
        print(row)
    print(summarize_sheet(rows))


if __name__ == "__main__":
    main()
