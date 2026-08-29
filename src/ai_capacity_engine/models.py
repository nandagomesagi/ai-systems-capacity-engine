from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Dict, List, Optional


class EpistemicState(str, Enum):
    OBSERVED = "OBSERVED"
    DERIVED = "DERIVED"
    ASSUMED = "ASSUMED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class DomainCapacity:
    domain: str
    supported_capacity_mw: Optional[float]
    epistemic_state: EpistemicState
    evidence_refs: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.domain.strip():
            raise ValueError("domain must not be empty")
        if self.supported_capacity_mw is not None and self.supported_capacity_mw < 0:
            raise ValueError("supported_capacity_mw must be >= 0")
        if self.epistemic_state is EpistemicState.UNKNOWN and self.supported_capacity_mw is not None:
            raise ValueError("UNKNOWN domain capacity must not contain a numeric value")
        if self.epistemic_state is not EpistemicState.UNKNOWN and self.supported_capacity_mw is None:
            raise ValueError("known epistemic states require a numeric capacity")

    def is_known(self) -> bool:
        return self.supported_capacity_mw is not None and self.epistemic_state is not EpistemicState.UNKNOWN


@dataclass(frozen=True)
class ControlStatus:
    control: str
    required: bool
    satisfied: Optional[bool]
    evidence_refs: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.control.strip():
            raise ValueError("control must not be empty")


@dataclass(frozen=True)
class CapacityInput:
    location: str
    target_capacity_mw: float
    target_date: date
    domains: List[DomainCapacity]
    cyber_controls: List[ControlStatus] = field(default_factory=list)
    governance_controls: List[ControlStatus] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.location.strip():
            raise ValueError("location must not be empty")
        if self.target_capacity_mw <= 0:
            raise ValueError("target_capacity_mw must be > 0")
        if not self.domains:
            raise ValueError("at least one capacity domain is required")


@dataclass(frozen=True)
class CapacityResult:
    location: str
    target_capacity_mw: float
    target_date: date
    deployable_capacity_mw: Optional[float]
    provisional_capacity_mw: Optional[float]
    binding_constraint: Optional[str]
    provisional_binding_constraint: Optional[str]
    architecture_gaps_mw: Dict[str, Optional[float]]
    unknown_domains: List[str]
    unresolved_controls: List[str]
    evidence_refs: List[str]
    complete: bool
