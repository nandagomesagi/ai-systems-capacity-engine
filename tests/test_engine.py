from datetime import date

from ai_capacity_engine.engine import evaluate_capacity
from ai_capacity_engine.models import (
    CapacityInput,
    ControlStatus,
    DomainCapacity,
    EpistemicState,
)


def test_binding_constraint_and_gap():
    model_input = CapacityInput(
        location="Northern Virginia",
        target_capacity_mw=5000,
        target_date=date(2030, 12, 31),
        domains=[
            DomainCapacity("power", 4200, EpistemicState.OBSERVED, ["ev-power"]),
            DomainCapacity("grid", 3100, EpistemicState.DERIVED, ["ev-grid"]),
            DomainCapacity("water", 4700, EpistemicState.OBSERVED, ["ev-water"]),
        ],
        cyber_controls=[
            ControlStatus("recovery", required=True, satisfied=True, evidence_refs=["ev-cyber"]),
        ],
    )

    result = evaluate_capacity(model_input)

    assert result.deployable_capacity_mw == 3100
    assert result.binding_constraint == "grid"
    assert result.architecture_gaps_mw["grid"] == 1900
    assert result.unresolved_controls == []
    assert result.complete is True


def test_unknown_capacity_preserves_uncertainty():
    model_input = CapacityInput(
        location="Northern Virginia",
        target_capacity_mw=5000,
        target_date=date(2030, 12, 31),
        domains=[
            DomainCapacity("power", 4200, EpistemicState.OBSERVED),
            DomainCapacity("water", None, EpistemicState.UNKNOWN),
        ],
        governance_controls=[
            ControlStatus("auditability", required=True, satisfied=None),
        ],
    )

    result = evaluate_capacity(model_input)

    assert result.deployable_capacity_mw == 4200
    assert result.architecture_gaps_mw["water"] is None
    assert result.unresolved_controls == ["auditability"]
    assert result.complete is False
