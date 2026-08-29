# WebMCP Tool Contract — MVP

WebMCP is an interface to the capacity model. It must expose narrow operations with auditable inputs and outputs.

## evaluate_capacity

Input:

```json
{
  "location": "Northern Virginia",
  "target_capacity_mw": 5000,
  "target_date": "2030-12-31"
}
```

Output fields:

```text
deployable_capacity_mw
binding_constraint
architecture_gaps_mw
unresolved_controls
complete
evidence_refs
```

## find_binding_constraint

Returns the lowest supported required domain and the evidence chain supporting that determination.

## trace_dependency

Returns upstream dependencies for a selected node or constraint.

## calculate_architecture_gap

Returns the difference between target requirements and documented available capacity by domain.

## calculate_critical_path

Returns the dependency sequence controlling the earliest feasible deployment date.

## verify_evidence

Returns provenance, verification state, and upstream evidence for a requested claim or modeled value.

## Interface rules

- Do not infer missing values silently.
- Return `UNKNOWN` when evidence is insufficient.
- Separate facts from scenario assumptions.
- Every derived output must be traceable to evidence references and documented calculations.
