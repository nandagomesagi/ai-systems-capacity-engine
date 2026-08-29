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
provisional_capacity_mw
binding_constraint
provisional_binding_constraint
architecture_gaps_mw
unknown_domains
unresolved_controls
complete
evidence_refs
```

### Uncertainty rule

If any required domain is `UNKNOWN`, the tool must not return a final numeric `deployable_capacity_mw` or final `binding_constraint`. It may return a clearly labeled provisional minimum calculated only from known domains.

## find_binding_constraint

Returns the lowest supported required domain and the evidence chain supporting that determination.

If required domains remain unknown, the result must be labeled provisional.

## trace_dependency

Returns upstream dependencies for a selected node or constraint, including known project, grid, regulatory, or resource prerequisites and evidence references.

## calculate_architecture_gap

Returns the difference between target requirements and documented available capacity by domain.

Unknown capacity must produce an unknown gap, not zero.

## calculate_critical_path

Returns the dependency sequence controlling the earliest feasible deployment date.

A final feasible date must not be emitted when a required dependency has unknown lead time unless the response explicitly identifies that limitation.

## verify_evidence

Returns provenance, geography, verification state, source type, limitations, and upstream evidence for a requested claim or modeled value.

## Geographic rules

- Every numeric evidence observation must have explicit geography.
- A Dominion/PJM zone number is not automatically a Loudoun County number.
- A project load request is not regional available capacity.
- Cross-geography transformations require a documented method and must be classified as `DERIVED`.

## Interface rules

- Do not infer missing values silently.
- Return `UNKNOWN` when evidence is insufficient.
- Separate facts from scenario assumptions.
- Separate final outputs from provisional outputs.
- Every derived output must be traceable to evidence references and documented calculations.
- Preserve the distinction: `announced != funded != permitted != powered != compute-ready != operational`.
