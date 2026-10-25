"""What the lift domain needs from the outside world. Any adapter that fits can replace another."""
from __future__ import annotations

from datetime import date, datetime
from typing import Iterable, Protocol


class ExerciseCatalog(Protocol):
    def key(self, exercise: dict) -> str: ...            # one identity per lift across sources
    def group(self, title: str) -> str | None: ...       # substitution group, for swaps


class SignalInterpreter(Protocol):
    """Turns the athlete's words into signals: kind (pain, easy, hard, reduce, state_hold, state_note),
    optional region, and the source reference and sentence they came from."""
    def read(self, messages: Iterable[dict]) -> list[dict]: ...


class Evidence(Protocol):
    def workouts(self, cutoff: datetime) -> list[dict]: ...           # performed sessions
    def history_only(self, cutoff: datetime) -> list[dict]: ...       # older logs: estimates, never rotation
    def messages(self, since: datetime, until: datetime) -> list[dict]: ...
    def health(self, on: date) -> list[dict]: ...
    def strength_goals(self) -> list[str]: ...


class RoutineSource(Protocol):
    def routines(self) -> list[dict]: ...


class Ledger(Protocol):
    def save_routines(self, routines: list[dict], at: datetime) -> None: ...
    def save_run(self, model_version: str, at: datetime, inputs: dict, rows: list[dict]) -> dict: ...
    def unscored(self, routine_title: str, before: datetime) -> list[dict]: ...
    def save_outcome(self, prediction: dict, workout: dict, result: tuple) -> None: ...
