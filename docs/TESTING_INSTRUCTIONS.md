# WebMCP Testing Instructions

## Production URL

`https://intelligence.businessaifuture.com`

## Supported test environments

Use either:

- ChatGPT's in-app browser, or
- Google Chrome 149+ with WebMCP enabled through the experimental flag or origin trial.

The normal browser interface remains usable without WebMCP, but agent tool discovery will be unavailable.

## Initial checks

Before testing tools, confirm the page shows:

```text
API: ok
WebMCP: 8 tools
```

If the page shows `WebMCP: browser unavailable`, the browser does not expose the WebMCP API.

If it shows a registration failure, inspect the page activity log and browser console rather than treating it as a model failure.

## Tool tests

### 1. Read live scenario

Prompt:

> Read the current scenario state and list the target, assumptions, and unresolved domains.

Expected tool:

`get-scenario-state`

Expected behavior:

- returns the live target shown on the page;
- returns explicit assumptions only;
- unresolved required domains remain unknown.

### 2. Change target

Prompt:

> Change the target to 6000 MW by 2030-12-31.

Expected tool:

`set-scenario-target`

Expected behavior:

- target fields change on the visible page;
- engine re-runs;
- activity log records an agent action.

### 3. Set an assumption

Prompt:

> Assume grid can support 3200 MW.

Expected tool:

`set-domain-assumption`

Expected behavior:

- grid input becomes `3200`;
- grid state becomes `ASSUMED`;
- value is not labeled observed or source-backed;
- engine re-runs.

### 4. Clear an assumption

Prompt:

> Clear the grid assumption.

Expected tool:

`clear-domain-assumption`

Expected behavior:

- grid input becomes blank;
- grid returns to `UNKNOWN`;
- engine re-runs.

### 5. Evaluate current scenario

Prompt:

> Evaluate the current capacity scenario.

Expected tool:

`evaluate-capacity`

Expected behavior:

- if any required domain remains unknown, final deployable capacity is withheld;
- a provisional known minimum may be shown from known domains;
- model remains incomplete until every required domain is known.

### 6. Retrieve source-aware evidence

Prompt:

> Retrieve the evidence record ev-pjm-firehouse-load-request-2026 and explain its limitation.

Expected tool:

`get-evidence-record`

Expected behavior:

- returns publisher, source type, geography, claim, limitations and URL;
- limitation explicitly prevents treating the Firehouse customer load request as regional available capacity.

### 7. Trace project dependencies

Prompt:

> Trace the dependencies for firehouse-grid-delivery.

Expected tool:

`trace-project-dependencies`

Expected behavior:

- returns upstream dependency closure for the Firehouse example;
- includes the evidence reference;
- does not claim the dependency graph proves regional headroom.

### 8. Calculate timing completeness

Prompt:

> Calculate the critical path for firehouse-grid-delivery.

Expected tool:

`calculate-critical-path`

Expected behavior:

- total lead time is `UNKNOWN` / null when required node lead times lack evidence;
- result is incomplete;
- unknown lead-time nodes are listed rather than assigned synthetic estimates.

## Reset state after testing

The MVP is stateless on the server, but a browser session can retain temporary page state until reload.

To reset the visible workbench:

1. reload the page; or
2. clear any assumptions using `clear-domain-assumption` and restore the desired target.

## Epistemic acceptance criteria

A successful tool invocation is not enough. The following integrity rules must also hold:

- `UNKNOWN` is never silently converted into a number;
- human/agent numeric overrides remain `ASSUMED`;
- assumptions do not inherit primary-source evidence;
- geographic scopes are not silently mixed;
- a permit is not treated as operational capacity;
- a customer load request is not treated as regional capacity;
- incomplete dependency timing does not produce a fabricated critical-path duration.
