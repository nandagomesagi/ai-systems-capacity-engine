from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .engine import evaluate_capacity
from .io import (
    apply_scenario_assumptions,
    capacity_input_from_dict,
    capacity_result_to_dict,
)

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "northern-virginia"
WEB_DIR = ROOT / "webapp"

SCENARIO_PATH = DATA_DIR / "scenario.example.json"
EVIDENCE_PATH = DATA_DIR / "evidence.registry.json"
PROJECTS_PATH = DATA_DIR / "projects.seed.json"


class EvaluateRequest(BaseModel):
    target_capacity_mw: float = Field(gt=0)
    target_date: date
    domain_assumptions: Dict[str, Optional[float]] = Field(default_factory=dict)


app = FastAPI(
    title="AI Systems Capacity Engine",
    version="0.2.0",
    description="Evidence-aware constraint workbench for AI infrastructure capacity.",
)

app.mount("/assets", StaticFiles(directory=WEB_DIR), name="assets")


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "model": "MODEL MVP v0.1", "service": "workbench"}


@app.get("/api/default-scenario")
def default_scenario() -> dict:
    return _load_json(SCENARIO_PATH)


@app.get("/api/evidence")
def evidence_registry() -> dict:
    return _load_json(EVIDENCE_PATH)


@app.get("/api/evidence/{evidence_id}")
def evidence_record(evidence_id: str) -> dict:
    registry = _load_json(EVIDENCE_PATH)
    for record in registry.get("records", []):
        if record.get("evidence_id") == evidence_id:
            return record
    raise HTTPException(status_code=404, detail="Evidence record not found")


@app.get("/api/projects")
def projects() -> dict:
    return _load_json(PROJECTS_PATH)


@app.post("/api/evaluate")
def evaluate(request: EvaluateRequest) -> dict:
    base = _load_json(SCENARIO_PATH)
    try:
        scenario = apply_scenario_assumptions(
            base,
            target_capacity_mw=request.target_capacity_mw,
            target_date=request.target_date,
            domain_assumptions=request.domain_assumptions,
        )
        model_input = capacity_input_from_dict(scenario)
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    result = evaluate_capacity(model_input)
    payload = capacity_result_to_dict(result)
    payload["scenario_domains"] = scenario["domains"]
    payload["epistemic_notice"] = (
        "Numeric overrides supplied by the user or agent are ASSUMED, not observed facts."
    )
    return payload
