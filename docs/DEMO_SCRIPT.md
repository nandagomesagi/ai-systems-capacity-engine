# WebMCP Challenge Demo Script

Target length: **2:20–2:40**. The official challenge requires a public demo video under 3 minutes with audio.

## Recording setup

- Open the production app: `https://intelligence.businessaifuture.com`
- Use ChatGPT's in-app browser or Chrome 149+ with WebMCP enabled.
- Confirm the page shows `API: ok` and `WebMCP: 8 tools` before recording.
- Keep the page and agent interaction visible whenever practical.
- Do not prefill unsupported capacity values as facts.
- Validate all eight tools before recording; the video itself only needs the clearest subset of calls.

## Judge takeaway

The demo should make two ideas obvious without explanation after the video ends:

1. WebMCP lets the agent operate the same decision surface the human sees.
2. The engine preserves the difference between evidence, assumptions and unknowns even when an agent is operating it.

## 0:00–0:15 — Hook

### Screen

Show the top of the workbench with the default Northern Virginia / Loudoun County scenario.

### Narration

> AI infrastructure announcements are not deployable capacity. This workbench lets a human and an AI agent test what has to exist first, what remains unknown, and what can actually be supported by a target date.

Point briefly to:

- `Architecture Before Amplification`
- `Limits Before Scale`
- final deployable capacity = `UNKNOWN`

## 0:15–0:35 — Agent reads the live page

### Prompt

> Read the current scenario state and tell me the target and which required domains are still unknown.

### Expected WebMCP tool

`get-scenario-state`

### What to show

The agent reads the same live scenario visible on the page. No manual copying of dashboard values is required.

## 0:35–1:00 — Agent changes shared state

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

## 1:00–1:25 — No false precision

### Prompt

> Evaluate the current capacity scenario.

### Expected WebMCP tool

`evaluate-capacity`

### Narration

> The agent can change the scenario, but it cannot erase uncertainty. Grid is now an explicit assumption, while the other required domains remain unknown, so the engine withholds a final deployable-capacity number.

Show:

- `Final deployable capacity: UNKNOWN`
- provisional value if present;
- unresolved domain chips;
- `Model state: INCOMPLETE`

## 1:25–1:50 — Evidence with limitations

### Prompt

> Retrieve the evidence record ev-pjm-firehouse-load-request-2026 and explain its limitation.

### Expected WebMCP tool

`get-evidence-record`

### Narration

> Evidence is not just a link. The record retains publisher, geography, claim and limitations. A customer load request cannot be silently converted into regional available capacity.

## 1:50–2:12 — Dependency graph

### Prompt

> Trace the dependencies for firehouse-grid-delivery.

### Expected WebMCP tool

`trace-project-dependencies`

Show the dependency chain and evidence reference.

### Narration

> The same primary source can support a dependency relationship without supporting a regional-capacity claim.

## 2:12–2:30 — Critical path refuses fabrication

### Prompt

> Calculate the critical path for firehouse-grid-delivery.

### Expected WebMCP tool

`calculate-critical-path`

### Narration

> Required component lead times are not fully supported by the evidence, so the system returns incomplete timing instead of fabricating a duration.

Show:

- total duration `UNKNOWN`;
- incomplete state;
- unknown lead-time nodes.

## 2:30–2:40 — Close

### Screen

Return to the workbench headline and shared state.

### Narration

> Humans and agents can test scale together without confusing facts, assumptions and unknowns. Architecture Before Amplification. Limits Before Scale.

## Recording rules

- Do not exceed 3 minutes.
- Include audible narration.
- Keep the opening hook under 15 seconds.
- Do not explain implementation details that the screen can prove visually.
- Do not speed through tool calls so quickly that page mutations are invisible.
- If a tool call fails, restart the recording rather than hiding the failure with editing.
- Do not claim end-to-end WebMCP validation until all eight tools have been discovered and invoked successfully in the recording environment.
