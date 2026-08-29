# WebMCP Tool Contract — Workbench MVP

WebMCP is the agent interface to the same live scenario state used by the human-facing workbench. It is not a separate backend product.

The implementation follows the current WebMCP imperative pattern using `document.modelContext.registerTool(...)`. A compatibility fallback to `navigator.modelContext` is retained for earlier browser implementations.

## Shared-state tools

### `get-scenario-state`

Returns the target, current domain assumptions, unknown domains, and latest engine result visible on the page.

### `set-scenario-target`

Input:

```json
{
  "target_capacity_mw": 5000,
  "target_date": "2030-12-31"
}
```

Changes the live human-visible target and immediately re-runs the engine.

### `set-domain-assumption`

Input:

```json
{
  "domain": "grid",
  "capacity_mw": 3100
}
```

The value is always classified as `ASSUMED`. It must not inherit evidence references or be represented as an observed fact.

### `clear-domain-assumption`

Restores one domain to `UNKNOWN` and re-runs the engine.

### `evaluate-capacity`

Runs the current live scenario. Final deployable capacity is withheld whenever a required domain remains unknown.

### `get-evidence-record`

Returns the source-aware record for one `evidence_id`, including publisher, geography, claim, limitations, and URL.

## Human-agent interaction rule

Mutating WebMCP tools must update the same DOM state the human sees. Agent actions are recorded in the page activity log so the user can inspect what changed.

## Epistemic rules

- Do not infer missing values silently.
- Return `UNKNOWN` when required evidence is insufficient.
- Separate facts from scenario assumptions.
- Never attach primary-source evidence to a user- or agent-entered assumption.
- Every derived factual output must be traceable to evidence and documented calculations.

## Next tools

After the dependency graph is connected to the live app:

```text
trace-dependency
calculate-critical-path
verify-claim
```

These should not be exposed until their page-visible outputs and evidence chains are implemented end-to-end.
