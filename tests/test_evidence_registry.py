import json
from pathlib import Path

import pytest

from ai_capacity_engine.evidence import (
    load_evidence_registry,
    validate_evidence_references,
)


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_PATH = ROOT / "data" / "northern-virginia" / "evidence.registry.json"
PROJECTS_PATH = ROOT / "data" / "northern-virginia" / "projects.seed.json"


def test_evidence_registry_loads_and_preserves_geography():
    registry = load_evidence_registry(EVIDENCE_PATH)

    assert registry
    assert "ev-pjm-firehouse-load-request-2026" in registry

    for record in registry.values():
        assert record.geography
        assert record.geography_type
        assert record.url.startswith("https://")
        if record.has_numeric_observation:
            assert record.geography


def test_project_evidence_references_resolve():
    registry = load_evidence_registry(EVIDENCE_PATH)
    payload = json.loads(PROJECTS_PATH.read_text(encoding="utf-8"))

    for project in payload["projects"]:
        validate_evidence_references(project.get("evidence_refs", []), registry)


def test_unknown_evidence_reference_is_rejected():
    registry = load_evidence_registry(EVIDENCE_PATH)

    with pytest.raises(ValueError, match="Unknown evidence references"):
        validate_evidence_references(["ev-does-not-exist"], registry)
