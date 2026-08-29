from datetime import date

import pytest

from ai_capacity_engine.io import apply_scenario_assumptions, capacity_input_from_dict
from ai_capacity_engine.models import EpistemicState


BASE = {
    "location": "Northern Virginia",
    "target_capacity_mw": 5000,
    "target_date": "2030-12-31",
    "domains": [
        {
            "domain": "power",
            "supported_capacity_mw": None,
            "epistemic_state": "UNKNOWN",
            "evidence_refs": ["context-only"],
        },
        {
            "domain": "grid",
            "supported_capacity_mw": None,
            "epistemic_state": "UNKNOWN",
            "evidence_refs": [],
        },
    ],
}


def test_assumption_is_explicit_and_drops_evidence_refs():
    payload = apply_scenario_assumptions(
        BASE,
        target_capacity_mw=4500,
        target_date=date(2031, 6, 30),
        domain_assumptions={"power": 4200},
    )

    power = payload["domains"][0]
    assert power["supported_capacity_mw"] == 4200
    assert power["epistemic_state"] == "ASSUMED"
    assert power["evidence_refs"] == []

    model_input = capacity_input_from_dict(payload)
    assert model_input.domains[0].epistemic_state is EpistemicState.ASSUMED
    assert model_input.domains[1].epistemic_state is EpistemicState.UNKNOWN


def test_none_override_restores_unknown():
    base = {
        **BASE,
        "domains": [
            {
                "domain": "power",
                "supported_capacity_mw": 4000,
                "epistemic_state": "DERIVED",
                "evidence_refs": ["ev-power"],
            }
        ],
    }
    payload = apply_scenario_assumptions(
        base,
        target_capacity_mw=5000,
        target_date=date(2030, 12, 31),
        domain_assumptions={"power": None},
    )
    power = payload["domains"][0]
    assert power["supported_capacity_mw"] is None
    assert power["epistemic_state"] == "UNKNOWN"
    assert power["evidence_refs"] == []


def test_unknown_assumption_domain_is_rejected():
    with pytest.raises(ValueError, match="Unknown domain assumptions"):
        apply_scenario_assumptions(
            BASE,
            target_capacity_mw=5000,
            target_date=date(2030, 12, 31),
            domain_assumptions={"imaginary": 10},
        )
