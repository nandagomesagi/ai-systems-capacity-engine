# WebMCP Challenge Submission Draft

## Project

**AI Systems Capacity Engine**

## One-line description

A shared human-agent constraint workbench that tests whether a target amount of AI infrastructure can actually be supported, identifies what is still unknown, traces required infrastructure dependencies, and preserves the evidence behind each claim.

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

The data also comes from different geographic boundaries and evidence states. A utility-system forecast is not automatically local available capacity. An issued permit is not an operational data center. A project load request is not regional headroom.

The project therefore asks:

> Given a target AI scale, what architecture is required, what limits deployment, and what can be supported by the target date?

## What the MVP does

The first demonstration focuses on Northern Virginia, with Loudoun County as the core project geography.

A human or agent can:

1. set a target capacity and date;
2. inspect which required domains are still unknown;
3. enter explicit scenario assumptions without confusing them with observed facts;
4. run the same constraint engine;
5. inspect provisional and final capacity states;
6. inspect architecture gaps;
7. retrieve primary-source evidence records;
8. trace a verified grid dependency example;
9. ask for a critical path and receive `UNKNOWN` rather than a fabricated duration when lead times are not supported by evidence.

## Why WebMCP matters

WebMCP is not attached as a decorative API layer. The agent works on the same live scenario state that the human sees.

For example, an agent can change a target from 5,000 MW to 3,500 MW, set a hypothetical grid-support assumption, run the model, and the visible page updates immediately. The human can see exactly what changed and can distinguish agent-entered assumptions from source-backed observations.

This makes the page a collaborative decision surface instead of a dashboard that an agent merely reads.

## Current WebMCP tools

```text
get-scenario-state
set-scenario-target
set-domain-assumption
clear-domain-assumption
evaluate-capacity
get-evidence-record
trace-project-dependencies
calculate-project-critical-path
```

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

The MVP includes the PJM/Dominion Firehouse 230 kV delivery example in Loudoun County. The primary record verifies a large data-center customer load request and required delivery/interconnection architecture.

The project uses that evidence to demonstrate dependency tracing while explicitly refusing to reinterpret the project request as regional available capacity.

## Demo script

### Scene 1 — Start from uncertainty

Open the workbench. Required domains are `UNKNOWN`; final deployable capacity is withheld.

### Scene 2 — Agent inspects live state

Ask the agent to read the current target and list unresolved domains through `get-scenario-state`.

### Scene 3 — Agent changes the same page the human sees

Ask the agent to change the target capacity/date. The visible form changes.

### Scene 4 — Explicit assumptions

Ask the agent to set a hypothetical supported capacity for selected domains. Each input is visibly labeled `ASSUMED`.

### Scene 5 — Constraint evaluation

Ask the agent to evaluate the scenario. If required domains remain unknown, the engine withholds a final capacity value and may show only a provisional known minimum.

### Scene 6 — Evidence

Ask for a primary-source record. The tool returns publisher, geography, claim, limitations, and source URL.

### Scene 7 — Dependency graph

Ask the agent to trace `firehouse-grid-delivery`. Show the same dependency state in the page.

### Scene 8 — No false critical path

Ask for the project critical path. The engine returns an incomplete timing state because required component lead times are not supported by the ingested evidence.

End on:

> Architecture Before Amplification. Limits Before Scale.

## What is deliberately not claimed

The MVP does not claim:

- exact unused Loudoun County grid headroom;
- exact water-supported AI capacity without a compatible quantified source;
- a national AI-capacity ranking;
- an AGI arrival date;
- a synthetic ethics or readiness score;
- investment advice.

The point of the MVP is to prove a source-aware constraint architecture that can expand without discarding uncertainty.

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

The MVP is the first auditable cell of that larger system.
