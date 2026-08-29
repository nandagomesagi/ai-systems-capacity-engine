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
- [ ] Add machine-readable project inventory for the demo geography
- [ ] Add grid/transmission dependency records beyond the first seed project
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

Status: **CONTRACT DEFINED**

- [x] Define tool contract
- [ ] Implement `evaluate_capacity`
- [ ] Implement `find_binding_constraint`
- [ ] Implement `trace_dependency`
- [ ] Implement `calculate_architecture_gap`
- [ ] Implement `calculate_critical_path`
- [ ] Implement `verify_evidence`
- [ ] Expose tools from a live web application
- [ ] Verify agent discovery and invocation

## Phase 4 — Challenge demo

- [ ] Build one scenario editor: target MW + target date
- [ ] Show known vs unknown domains explicitly
- [ ] Show binding/provisional constraint
- [ ] Show architecture gaps
- [ ] Show evidence drawer for each output
- [ ] Demonstrate one dependency chain
- [ ] Record demo video
- [ ] Publish live app

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
