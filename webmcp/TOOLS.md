# WebMCP Tool Contract — Workbench MVP

WebMCP is the agent interface to the same live scenario state used by the human-facing workbench. It is not a separate backend product.

The implementation follows the current imperative WebMCP API using `document.modelContext.registerTool(...)`. A compatibility fallback to the deprecated `navigator.modelContext` location is retained for earlier implementations. Tool registration is owned by an `AbortController`; aborting its signal unregisters the page tools.

The public service requests an origin-keyed agent cluster with `Origin-Agent-Cluster: ?1` and explicitly limits the `tools` Permissions Policy to `self`, matching the browser security requirements for WebMCP registration.

## Shared-state tools

### `get-scenario-state`
Returns the target, current domain assumptions, unknown domains, and latest engine result visible on the page.

Annotation: read-only.

### `set-scenario-target`

```json
{
  "target_capacity_mw": 5000,
  "target_date": "2030-12-31"
}
```

Changes the live human-visible target and immediately re-runs the engine.

### `set-domain-assumption`

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
Runs the current live scenario and updates the visible result. Final deployable capacity is withheld whenever a required domain remains unknown.

## Evidence and dependency tools

### `get-evidence-record`
Returns the source-aware record for one `evidence_id`, including publisher, geography, claim, limitations, and URL.

Annotation: read-only; output is marked as containing externally sourced/untrusted content for agent-safety purposes.

### `trace-project-dependencies`

```json
{
  "graph_id": "firehouse-grid-delivery"
}
```

Returns the verified dependency closure for the Firehouse 230 kV customer-load example and its evidence references.

Annotation: read-only; externally sourced content.

### `calculate-critical-path`

```json
{
  "graph_id": "firehouse-grid-delivery"
}
```

Returns the critical-path state. A numeric duration is withheld when required component lead times are unknown.

Annotation: read-only; externally sourced content.

## Conformance rules

- Tool names stay within the current browser recommendation of 30 characters where practical.
- Every tool has an explicit JSON input schema; no-argument tools use an empty object schema.
- Schemas reject undeclared properties with `additionalProperties: false`.
- Tool `execute` callbacks return native JavaScript values. The WebMCP layer serializes those values for the agent; the app does not wrap them in a separate MCP `content` envelope.
- Async WebMCP calls propagate the execution `AbortSignal` into network requests so user/agent cancellation can stop work.
- Registration failures are surfaced separately from ordinary API startup failures.
- The page retains the registration `AbortController` for the document lifetime.

## Human-agent interaction rule

Mutating WebMCP tools must update the same DOM state the human sees. Agent actions are recorded in the page activity log so the user can inspect what changed.

Read-only dependency tools use the same project graph displayed in the human interface.

## Epistemic rules

- Do not infer missing values silently.
- Return `UNKNOWN` when required evidence is insufficient.
- Separate facts from scenario assumptions.
- Never attach primary-source evidence to a user- or agent-entered assumption.
- Every derived factual output must be traceable to evidence and documented calculations.
- A customer load request is not regional available capacity.
- An issued permit is not equivalent to operational capacity.

## Deferred tool

`verify-claim` remains deferred until every supported claim type has an end-to-end evidence-resolution path in the live application.
