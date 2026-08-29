# WebMCP Challenge Demo Script

Target length: **2:30–2:50**. The official challenge requires a public demo video under 3 minutes with audio.

## Recording setup

- Open the production app: `https://intelligence.businessaifuture.com`
- Use ChatGPT's in-app browser or Chrome 149+ with WebMCP enabled.
- Confirm the page shows `API: ok` and `WebMCP: 8 tools` before recording.
- Keep the page and agent interaction visible whenever practical.
- Do not prefill unsupported capacity values as facts.

## 0:00–0:20 — Problem and product

### Screen

Show the top of the workbench with the default Northern Virginia / Loudoun County scenario.

### Narration

> AI infrastructure plans are often summarized as a target number and a date. But announced capacity is not the same as deployable capacity. This workbench asks what architecture has to exist first, what remains unknown, and what can actually be supported by the target date.

Point briefly to:

- `Architecture Before Amplification`
- `Limits Before Scale`
- final deployable capacity = `UNKNOWN`

## 0:20–0:40 — Agent reads the live page

### Prompt

> Read the current scenario state and tell me the target and which required domains are still unknown.

### Expected WebMCP tool

`get-scenario-state`

### What to show

The agent reads the same live scenario visible on the page. No manual copying of dashboard values is required.

## 0:40–1:05 — Agent changes shared state

### Prompt

> Change the target to 6000 MW by 2030-12-31.

### Expected WebMCP tool

`set-scenario-target`

### What to show

The target input on the webpage changes to `6000` and the page re-evaluates.

Then prompt:

> Assume grid can support 3200 MW.

Expected tool: `set-domain-assumption`

Show that:

- the visible grid input changes;
- the domain is labeled `ASSUMED`;
- the activity log records the agent action.

## 1:05–1:30 — No false precision

### Prompt

> Evaluate the current capacity scenario.

### Expected WebMCP tool

`evaluate-capacity`

### Narration

> Grid now has an explicit scenario assumption, but the other required domains remain unknown. The engine therefore refuses to publish a final deployable-capacity number. It can show a provisional known minimum without pretending that the scenario is complete.

Show:

- `Final deployable capacity: UNKNOWN`
- provisional value if present;
- unresolved domain chips;
- `Model state: INCOMPLETE`

## 1:30–1:55 — Evidence with limitations

### Prompt

> Retrieve the evidence record ev-pjm-firehouse-load-request-2026 and explain its limitation.

### Expected WebMCP tool

`get-evidence-record`

### Narration

> Evidence is not just a URL. The record retains publisher, geography, claim, epistemic state, and limitations. A customer load request cannot be silently converted into regional available capacity.

## 1:55–2:20 — Dependency graph

### Prompt

> Trace the dependencies for firehouse-grid-delivery.

### Expected WebMCP tool

`trace-project-dependencies`

Show the dependency chain and evidence reference.

### Narration

> The same source can support a dependency relationship without supporting a regional-capacity claim.

## 2:20–2:40 — Critical path refuses fabrication

### Prompt

> Calculate the critical path for firehouse-grid-delivery.

### Expected WebMCP tool

`calculate-critical-path`

### Narration

> The source does not provide defensible lead times for every required component, so the system returns an incomplete timing state instead of fabricating a duration.

Show:

- total duration `UNKNOWN`;
- incomplete state;
- unknown lead-time nodes.

## 2:40–2:50 — Close

### Screen

Return to the workbench headline and shared state.

### Narration

> Humans and agents can test scale together while keeping facts, assumptions, dependencies, and unknowns separate. Architecture Before Amplification. Limits Before Scale.

## Recording rules

- Do not exceed 3 minutes.
- Include audible narration.
- Do not speed through tool calls so quickly that page mutations are invisible.
- If a tool call fails, restart the recording rather than hiding the failure with editing.
- Do not claim end-to-end WebMCP validation until the eight tools have been discovered in the recording environment.
