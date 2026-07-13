from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from .db import apply_migrations
from .health_import import import_mock_health_export
from .models import ImportRequest, ImportResultOut, require_iso_date
from .repository import get_recovery, list_import_runs, list_recovery
from .review import (
    compute_and_store_readiness,
    daily_review_for_date,
    get_or_compute_readiness,
    readiness_to_out,
    recovery_to_out,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    apply_migrations()
    yield


app = FastAPI(title="Human Model Public Readiness Slice", lifespan=lifespan)


def _validate_date(target_date: str) -> str:
    try:
        return require_iso_date(target_date)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/health")
def health() -> dict:
    return {"ok": True}


@app.post("/imports/mock-health", response_model=ImportResultOut)
def import_mock_health(payload: ImportRequest = ImportRequest()) -> ImportResultOut:
    result = import_mock_health_export(payload.fixture_names)
    if result.status == "blocked":
        raise HTTPException(status_code=404, detail=list(result.errors))
    if result.status == "error":
        raise HTTPException(status_code=422, detail=list(result.errors))
    return ImportResultOut(
        status=result.status,
        files_seen=result.files_seen,
        rows_seen=result.rows_seen,
        rows_inserted=result.rows_inserted,
        rows_updated=result.rows_updated,
        rows_unchanged=result.rows_unchanged,
        warnings=list(result.warnings),
        errors=list(result.errors),
    )


@app.get("/imports")
def imports() -> list:
    return list_import_runs()


@app.get("/recovery")
def recovery() -> list:
    return [recovery_to_out(row) for row in list_recovery()]


@app.get("/recovery/{target_date}")
def recovery_day(target_date: str):
    _validate_date(target_date)
    row = get_recovery(target_date)
    if row is None:
        raise HTTPException(status_code=404, detail="Recovery day not found")
    return recovery_to_out(row)


@app.post("/readiness/{target_date}")
def compute_readiness(target_date: str):
    _validate_date(target_date)
    try:
        return readiness_to_out(compute_and_store_readiness(target_date))
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/readiness/{target_date}")
def readiness(target_date: str):
    _validate_date(target_date)
    try:
        return readiness_to_out(get_or_compute_readiness(target_date))
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/daily-review/{target_date}")
def daily_review(target_date: str):
    _validate_date(target_date)
    try:
        return daily_review_for_date(target_date)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
