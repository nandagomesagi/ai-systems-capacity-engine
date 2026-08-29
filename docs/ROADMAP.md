# Implementation Roadmap

## Phase 0 — Model integrity

Status: **ACTIVE / MOSTLY COMPLETE**

- [x] Define constraint-based capacity model
- [x] Preserve `OBSERVED / DERIVED / ASSUMED / UNKNOWN`
- [x] Prevent unknown domains from producing false final capacity
- [x] Define geography boundary rules
- [x] Define evidence registry
- [x] Add source-aware project seed records
- [x] Add automated evidence-reference tests

## Phase 1 — Real Northern Virginia data

Status: **ACTIVE**

- [x] Add Dominion/PJM power-system context
- [x] Add Loudoun zoning constraint evidence
- [x] Add Loudoun Water planning evidence
- [x] Add Virginia DEQ permit registry evidence
- [x] Add Virginia SCC large-load governance context
- [x] Add first machine-readable project records for the demo geography
- [x] Add first verified grid/transmission dependency graph
- [ ] Expand project inventory for the demo geography
- [ ] Quantify water-supported capacity only when a compatible primary source supports it
- [ ] Quantify network support only when evidence is defensible
- [ ] Resolve project-level permit status into a state-transition model

## Phase 2 — Dependency and time engine

Status: **ACTIVE**

- [x] Add typed dependency nodes and edges
- [ ] Add dependency criticality
- [x] Add build-time / lead-time fields
- [ ] Add replacement-time fields
- [ ] Add redundancy / single-point-of-failure fields
- [x] Implement dependency tracing
- [x] Implement uncertainty-aware critical-path calculation
- [ ] Calculate earliest feasible calendar date only when required timing inputs are known

## Phase 3 — WebMCP MVP

Status: **IMPLEMENTATION ACTIVE**

- [x] Define tool contract
- [x] Implement shared scenario-state tool
- [x] Implement target mutation tool
- [x] Implement domain assumption / clear tools
- [x] Implement capacity evaluation tool
- [x] Implement evidence-record retrieval tool
- [x] Implement project dependency trace tool
- [x] Implement project critical-path tool
- [x] Register tools through `document.modelContext.registerTool(...)`
- [x] Connect mutating tools to the human-visible live page state
- [ ] Verify discovery and invocation in ChatGPT's WebMCP-capable browser
- [ ] Add end-to-end browser conformance test where practical

## Phase 4 — Challenge demo

Status: **ACTIVE**

- [x] Build scenario editor: target MW + target date
- [x] Show known vs unknown domains explicitly
- [x] Show binding/provisional constraint
- [x] Show architecture gaps
- [x] Show primary-source evidence registry
- [x] Demonstrate one verified dependency chain
- [x] Show why unknown lead times block a false critical-path duration
- [ ] Add evidence-detail interaction tied directly to outputs
- [ ] Publish live app
- [ ] Connect production domain
- [ ] Test WebMCP in the live deployment
- [ ] Prepare challenge description
- [ ] Record demo video
- [ ] Submit before deadline

## Phase 5 — Post-MVP expansion

- [ ] Virginia regional graph
- [ ] Build-rate model
- [ ] Cyber-resilience state model
- [ ] Strategic dependency concentration
- [ ] Semiconductor / HBM / packaging dependency layer
- [ ] US comparative capacity model
- [ ] International comparison layer
- [ ] Longitudinal forecast-vs-delivery reliability dataset

## Decision gate

Before expanding geography, the MVP must demonstrate this full chain with real evidence:

```text
TARGET
  -> REQUIREMENTS
  -> EVIDENCE
  -> DEPENDENCIES
  -> CONSTRAINT
  -> ARCHITECTURE GAP
  -> TIME
  -> DEPLOYABLE / UNKNOWN
```

If any link is not auditable, expansion pauses until it is fixed.
