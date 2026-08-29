from datetime import date

import pytest

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
    assert result.provisional_capacity_mw == 3100
    assert result.binding_constraint == "grid"
    assert result.provisional_binding_constraint == "grid"
    assert result.architecture_gaps_mw["grid"] == 1900
    assert result.unknown_domains == []
    assert result.unresolved_controls == []
    assert result.complete is True


def test_unknown_capacity_does_not_create_false_deployable_number():
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

    assert result.deployable_capacity_mw is None
    assert result.binding_constraint is None
    assert result.provisional_capacity_mw == 4200
    assert result.provisional_binding_constraint == "power"
    assert result.unknown_domains == ["water"]
    assert result.architecture_gaps_mw["water"] is None
    assert result.unresolved_controls == ["auditability"]
    assert result.complete is False


def test_unknown_state_cannot_carry_numeric_capacity():
    with pytest.raises(ValueError):
        DomainCapacity("water", 1000, EpistemicState.UNKNOWN)


def test_non_unknown_state_requires_numeric_capacity():
    with pytest.raises(ValueError):
        DomainCapacity("power", None, EpistemicState.OBSERVED)


def test_target_capacity_must_be_positive():
    with pytest.raises(ValueError):
        CapacityInput(
            location="Northern Virginia",
            target_capacity_mw=0,
            target_date=date(2030, 12, 31),
            domains=[DomainCapacity("power", 100, EpistemicState.OBSERVED)],
        )
