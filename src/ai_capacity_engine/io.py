from __future__ import annotations

from dataclasses import asdict
from datetime import date
from typing import Any, Dict, Mapping

from .models import (
    CapacityInput,
    CapacityResult,
    ControlStatus,
    DomainCapacity,
    EpistemicState,
)


def capacity_input_from_dict(payload: Mapping[str, Any]) -> CapacityInput:
    domains = [
        DomainCapacity(
            domain=str(item["domain"]),
            supported_capacity_mw=item.get("supported_capacity_mw"),
            epistemic_state=EpistemicState(str(item["epistemic_state"])),
            evidence_refs=list(item.get("evidence_refs", [])),
        )
        for item in payload["domains"]
    ]

    cyber_controls = [
        ControlStatus(
            control=str(item["control"]),
            required=bool(item.get("required", False)),
            satisfied=item.get("satisfied"),
            evidence_refs=list(item.get("evidence_refs", [])),
        )
        for item in payload.get("cyber_controls", [])
    ]

    governance_controls = [
        ControlStatus(
            control=str(item["control"]),
            required=bool(item.get("required", False)),
            satisfied=item.get("satisfied"),
            evidence_refs=list(item.get("evidence_refs", [])),
        )
        for item in payload.get("governance_controls", [])
    ]

    target_date = payload["target_date"]
    if isinstance(target_date, str):
        target_date = date.fromisoformat(target_date)

    return CapacityInput(
        location=str(payload["location"]),
        target_capacity_mw=float(payload["target_capacity_mw"]),
        target_date=target_date,
        domains=domains,
        cyber_controls=cyber_controls,
        governance_controls=governance_controls,
    )


def capacity_result_to_dict(result: CapacityResult) -> Dict[str, Any]:
    payload = asdict(result)
    payload["target_date"] = result.target_date.isoformat()
    return payload


def apply_scenario_assumptions(
    base: Mapping[str, Any],
    *,
    target_capacity_mw: float,
    target_date: date,
    domain_assumptions: Mapping[str, float | None],
) -> Dict[str, Any]:
    """Return a scenario payload with explicit user assumptions applied.

    Numeric overrides are always marked ASSUMED and never inherit evidence
    references from observed context. A None value explicitly restores UNKNOWN.
    """
    payload: Dict[str, Any] = {
        "location": base["location"],
        "target_capacity_mw": target_capacity_mw,
        "target_date": target_date.isoformat(),
        "domains": [],
        "cyber_controls": list(base.get("cyber_controls", [])),
        "governance_controls": list(base.get("governance_controls", [])),
    }

    allowed_domains = {str(item["domain"]) for item in base["domains"]}
    unknown_overrides = set(domain_assumptions) - allowed_domains
    if unknown_overrides:
        raise ValueError(
            "Unknown domain assumptions: " + ", ".join(sorted(unknown_overrides))
        )

    for item in base["domains"]:
        domain = str(item["domain"])
        record = dict(item)
        if domain in domain_assumptions:
            value = domain_assumptions[domain]
            if value is None:
                record["supported_capacity_mw"] = None
                record["epistemic_state"] = EpistemicState.UNKNOWN.value
            else:
                if value < 0:
                    raise ValueError(f"Assumption for {domain} must be >= 0")
                record["supported_capacity_mw"] = float(value)
                record["epistemic_state"] = EpistemicState.ASSUMED.value
            record["evidence_refs"] = []
        payload["domains"].append(record)

    return payload
