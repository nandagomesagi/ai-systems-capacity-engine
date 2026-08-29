# WebMCP Challenge Submission — Final Draft

## Project

**AI Systems Capacity Engine**

## Live app

https://intelligence.businessaifuture.com

## Public repository

https://github.com/nandagomesagi/ai-systems-capacity-engine

## One-line description

An evidence-aware human-agent workbench that tests whether a target amount of AI infrastructure can actually be supported, identifies the first unresolved constraints, traces required infrastructure dependencies, and refuses to turn missing evidence into confident-looking numbers.

## Why this is a strong fit for WebMCP

AI infrastructure planning is not a single search or a static dashboard problem. A user may need to change a target, test hypothetical domain support, compare those assumptions with source-backed facts, evaluate the resulting constraint state, inspect a project dependency chain, and then ask whether the timeline is actually supportable.

WebMCP makes that workflow collaborative. The agent operates on the same live scenario state the human sees instead of working in a separate hidden tool session.

When the agent changes a target or a domain assumption:

- the visible page changes immediately;
- the action is recorded in the activity log;
- the entered value is explicitly classified as `ASSUMED`;
- the constraint engine re-runs against the same state;
- unresolved evidence remains `UNKNOWN` rather than being silently inferred.

This turns the webpage into a shared decision surface for human and agent.

## Problem

AI infrastructure expansion is often described through announcements: gigawatts, data-center campuses, compute, capital, and target dates. Those announcements do not prove deployability.

A proposed AI load can depend on:

```text
power
-> transmission
-> substations
-> grid delivery
-> water / cooling
-> network
-> permits
-> controls
-> time
```

The evidence also comes from different geographic and operational states. A utility forecast is not automatically local available capacity. An issued permit is not an operational data center. A customer load request is not regional headroom.

The system therefore asks:

> Given a target AI scale, what architecture is required, what limits deployment, and what can be supported by the target date?

## What people and agents can do together

The first demonstration focuses on Northern Virginia, with Loudoun County as the core project geography.

A human and agent can jointly:

1. inspect the current scenario and unresolved domains;
2. change the target capacity and target date;
3. add explicit hypothetical support values for required domains;
4. restore those values to `UNKNOWN`;
5. run the evidence-aware constraint engine;
6. inspect provisional versus final capacity states and architecture gaps;
7. retrieve a source-aware evidence record with its geography and limitations;
8. trace a verified project dependency chain;
9. evaluate timing completeness without fabricating a critical-path duration.

Before WebMCP, an agent could describe what a user should type into a dashboard or operate against a separate API. Here, the agent directly updates the same browser state that the human is inspecting, while preserving provenance and epistemic state.

## How WebMCP is implemented

The page uses the imperative WebMCP API through `document.modelContext.registerTool(...)`, with a compatibility fallback to `navigator.modelContext` for earlier implementations.

Eight tools are registered:

```text
get-scenario-state
set-scenario-target
set-domain-assumption
clear-domain-assumption
evaluate-capacity
get-evidence-record
trace-project-dependencies
calculate-critical-path
```

The tool schemas reject unexpected properties. Read-only and external-content tools carry appropriate annotations. Mutating tool execution supports cancellation and updates the same DOM state used by the human-facing workbench.

The production response requests an origin-keyed agent cluster and restricts the WebMCP permissions policy to the same origin.

## Evidence and uncertainty contract

Every material value is classified as:

```text
OBSERVED
DERIVED
ASSUMED
UNKNOWN
```

Rules:

- unknown required domains block a final capacity number;
- human- or agent-entered numeric overrides are always `ASSUMED`;
- assumptions never inherit primary-source evidence references;
- project, county, utility-territory, transmission-zone, and state values are not silently mixed;
- `announced != funded != permitted != powered != compute-ready != operational`;
- unknown dependency lead times block a final critical-path duration.

## Verified dependency example

The MVP includes the PJM/Dominion Firehouse 230 kV delivery example in Loudoun County. The source record supports a customer load request and associated delivery/interconnection architecture.

The system uses that evidence to demonstrate dependency tracing while explicitly refusing to reinterpret the project request as regional available capacity.

## Demo sequence

The demo begins with all required capacity domains unresolved. Final deployable capacity is therefore withheld.

The agent then:

1. reads the live scenario;
2. changes the target;
3. sets one explicit grid assumption;
4. evaluates the scenario and shows that unknown domains still prevent a final answer;
5. retrieves a primary-source evidence record and its limitations;
6. traces the Firehouse dependency chain;
7. calculates timing completeness and returns an incomplete critical path because evidence-backed component lead times are missing.

The point is not that the model always produces a number. The point is that the human and agent can work together without erasing the boundary between evidence, assumptions, and unknowns.

## What is deliberately not claimed

The MVP does not claim:

- exact unused Loudoun County grid headroom;
- exact water-supported AI capacity without a compatible quantified source;
- a national AI-capacity ranking;
- an AGI arrival date;
- a synthetic ethics or readiness score;
- investment advice.

The MVP proves a source-aware constraint architecture that can expand without discarding uncertainty.

## Long-term direction

The long-term asset is a longitudinal dependency graph of AI expansion:

```text
projects
resources
infrastructure
capacity
constraints
dependencies
controls
build times
regulations
failures
changes
```

The future system can compare:

```text
forecast
-> required architecture
-> actual build
-> delay
-> cause
-> revised capacity state
```

The Northern Virginia MVP is the first auditable cell of that larger system.

## Closing line

**Architecture Before Amplification. Limits Before Scale.**
