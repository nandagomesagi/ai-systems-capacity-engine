from __future__ import annotations

from typing import Iterable, List, Optional

from .models import CapacityInput, CapacityResult, ControlStatus, DomainCapacity


def _known_domains(domains: Iterable[DomainCapacity]) -> List[DomainCapacity]:
    return [domain for domain in domains if domain.is_known()]


def _minimum_domain(domains: Iterable[DomainCapacity]) -> Optional[DomainCapacity]:
    known = _known_domains(domains)
    if not known:
        return None
    return min(known, key=lambda item: item.supported_capacity_mw)


def find_binding_constraint(domains: Iterable[DomainCapacity]) -> Optional[str]:
    """Return the minimum known domain.

    This helper is intentionally evidence-agnostic. `evaluate_capacity` decides
    whether the result is final or only provisional when unknown domains exist.
    """
    minimum = _minimum_domain(domains)
    return minimum.domain if minimum else None


def _collect_unresolved_controls(controls: Iterable[ControlStatus]) -> List[str]:
    unresolved: List[str] = []
    for control in controls:
        if control.required and control.satisfied is not True:
            unresolved.append(control.control)
    return unresolved


def evaluate_capacity(model_input: CapacityInput) -> CapacityResult:
    known = _known_domains(model_input.domains)
    unknown_domains = sorted(
        domain.domain for domain in model_input.domains if not domain.is_known()
    )
    all_domains_known = not unknown_domains

    provisional_minimum = _minimum_domain(known)
    provisional_capacity_mw = (
        provisional_minimum.supported_capacity_mw if provisional_minimum else None
    )
    provisional_binding_constraint = (
        provisional_minimum.domain if provisional_minimum else None
    )

    # A numeric deployable capacity is only reported when every required domain
    # is known. This prevents an unknown domain from being silently treated as
    # non-binding and creating false precision.
    deployable_capacity_mw = provisional_capacity_mw if all_domains_known else None
    binding_constraint = provisional_binding_constraint if all_domains_known else None

    architecture_gaps = {}
    evidence_refs = set()

    for domain in model_input.domains:
        evidence_refs.update(domain.evidence_refs)
        if not domain.is_known():
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
        target_date=model_input.target_date,
        deployable_capacity_mw=deployable_capacity_mw,
        provisional_capacity_mw=provisional_capacity_mw,
        binding_constraint=binding_constraint,
        provisional_binding_constraint=provisional_binding_constraint,
        architecture_gaps_mw=architecture_gaps,
        unknown_domains=unknown_domains,
        unresolved_controls=sorted(unresolved_controls),
        evidence_refs=sorted(evidence_refs),
        complete=complete,
    )
