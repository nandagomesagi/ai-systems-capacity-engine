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

    def is_known(self) -> bool:
        return self.supported_capacity_mw is not None


@dataclass(frozen=True)
class ControlStatus:
    control: str
    required: bool
    satisfied: Optional[bool]
    evidence_refs: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class CapacityInput:
    location: str
    target_capacity_mw: float
    target_date: date
    domains: List[DomainCapacity]
    cyber_controls: List[ControlStatus] = field(default_factory=list)
    governance_controls: List[ControlStatus] = field(default_factory=list)


@dataclass(frozen=True)
class CapacityResult:
    location: str
    target_capacity_mw: float
    deployable_capacity_mw: Optional[float]
    binding_constraint: Optional[str]
    architecture_gaps_mw: Dict[str, Optional[float]]
    unresolved_controls: List[str]
    evidence_refs: List[str]
    complete: bool
