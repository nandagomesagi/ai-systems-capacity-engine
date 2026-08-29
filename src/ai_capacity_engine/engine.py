from __future__ import annotations

from typing import Iterable, List, Optional

from .models import CapacityInput, CapacityResult, ControlStatus, DomainCapacity


def _known_domains(domains: Iterable[DomainCapacity]) -> List[DomainCapacity]:
    return [domain for domain in domains if domain.is_known()]


def find_binding_constraint(domains: Iterable[DomainCapacity]) -> Optional[str]:
    known = _known_domains(domains)
    if not known:
        return None
    return min(known, key=lambda item: item.supported_capacity_mw).domain


def _collect_unresolved_controls(controls: Iterable[ControlStatus]) -> List[str]:
    unresolved: List[str] = []
    for control in controls:
        if control.required and control.satisfied is not True:
            unresolved.append(control.control)
    return unresolved


def evaluate_capacity(model_input: CapacityInput) -> CapacityResult:
    known = _known_domains(model_input.domains)
    all_domains_known = len(known) == len(model_input.domains) and bool(known)

    deployable_capacity_mw = (
        min(domain.supported_capacity_mw for domain in known)
        if known
        else None
    )

    binding_constraint = find_binding_constraint(model_input.domains)

    architecture_gaps = {}
    evidence_refs = set()

    for domain in model_input.domains:
        evidence_refs.update(domain.evidence_refs)
        if domain.supported_capacity_mw is None:
            architecture_gaps[domain.domain] = None
        else:
            architecture_gaps[domain.domain] = max(
                model_input.target_capacity_mw - domain.supported_capacity_mw,
                0.0,
            )

    controls = [*model_input.cyber_controls, *model_input.governance_controls]
    unresolved_controls = _collect_unresolved_controls(controls)

    for control in controls:
        evidence_refs.update(control.evidence_refs)

    complete = all_domains_known and not unresolved_controls

    return CapacityResult(
        location=model_input.location,
        target_capacity_mw=model_input.target_capacity_mw,
        deployable_capacity_mw=deployable_capacity_mw,
        binding_constraint=binding_constraint,
        architecture_gaps_mw=architecture_gaps,
        unresolved_controls=sorted(unresolved_controls),
        evidence_refs=sorted(evidence_refs),
        complete=complete,
    )
