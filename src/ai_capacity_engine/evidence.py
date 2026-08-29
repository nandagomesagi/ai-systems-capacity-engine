from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    publisher: str
    source_type: str
    geography: str
    geography_type: str
    domains: List[str]
    epistemic_state: str
    claim: str
    use_in_engine: str
    limitations: str
    url: str
    numeric_value: Optional[float] = None
    numeric_values: Optional[List[Dict[str, Any]]] = None

    @property
    def has_numeric_observation(self) -> bool:
        return self.numeric_value is not None or bool(self.numeric_values)


def _require_text(record: Mapping[str, Any], field: str) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Evidence record requires non-empty '{field}'.")
    return value.strip()


def _parse_record(raw: Mapping[str, Any]) -> EvidenceRecord:
    domains = raw.get("domains")
    if not isinstance(domains, list) or not domains or not all(
        isinstance(item, str) and item.strip() for item in domains
    ):
        raise ValueError("Evidence record requires a non-empty string list 'domains'.")

    numeric_values = raw.get("numeric_values")
    if numeric_values is not None and not isinstance(numeric_values, list):
        raise ValueError("'numeric_values' must be a list when supplied.")

    record = EvidenceRecord(
        evidence_id=_require_text(raw, "evidence_id"),
        publisher=_require_text(raw, "publisher"),
        source_type=_require_text(raw, "source_type"),
        geography=_require_text(raw, "geography"),
        geography_type=_require_text(raw, "geography_type"),
        domains=[item.strip() for item in domains],
        epistemic_state=_require_text(raw, "epistemic_state"),
        claim=_require_text(raw, "claim"),
        use_in_engine=_require_text(raw, "use_in_engine"),
        limitations=_require_text(raw, "limitations"),
        url=_require_text(raw, "url"),
        numeric_value=raw.get("numeric_value"),
        numeric_values=numeric_values,
    )

    if record.has_numeric_observation and not record.geography:
        raise ValueError(
            f"Numeric evidence '{record.evidence_id}' must have explicit geography."
        )

    return record


def load_evidence_registry(path: str | Path) -> Dict[str, EvidenceRecord]:
    """Load and validate the source-aware evidence registry.

    Duplicate evidence IDs are rejected because silent overwrites would corrupt
    provenance. Numeric observations are only accepted with explicit geography.
    """
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("Evidence registry must contain a 'records' list.")

    index: Dict[str, EvidenceRecord] = {}
    for raw in records:
        if not isinstance(raw, dict):
            raise ValueError("Each evidence record must be an object.")
        record = _parse_record(raw)
        if record.evidence_id in index:
            raise ValueError(f"Duplicate evidence_id: {record.evidence_id}")
        index[record.evidence_id] = record

    return index


def validate_evidence_references(
    evidence_refs: Iterable[str],
    registry: Mapping[str, EvidenceRecord],
) -> None:
    missing = sorted(set(evidence_refs) - set(registry))
    if missing:
        raise ValueError(f"Unknown evidence references: {', '.join(missing)}")
