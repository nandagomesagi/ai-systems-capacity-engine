# Architecture

## System flow

```text
TARGET AI SCALE
      |
      v
REQUIREMENTS
      |
      v
AVAILABLE CAPACITY
      |
      v
DEPENDENCY GRAPH
      |
      v
BINDING CONSTRAINTS
      |
      +--> CYBER CONTROLS
      +--> GOVERNANCE CONTROLS
      |
      v
ARCHITECTURE GAP
      |
      v
CRITICAL BUILD PATH
      |
      v
SECURE DEPLOYABLE CAPACITY
```

## MVP layers

### 1. Data layer
Source-aware records for Northern Virginia. No raw value is accepted without a provenance field and epistemic state.

### 2. Model layer
Typed representations for capacities, dependencies, controls, and evidence.

### 3. Constraint engine
Computes domain support, binding constraint, and architecture gaps.

### 4. Dependency engine
Traces required upstream systems and determines unresolved prerequisites.

### 5. Time layer
Uses dependency lead times to identify the critical build path and earliest feasible deployment date.

### 6. Agent interface
Exposes narrow, auditable operations to WebMCP-compatible clients.

## Initial repository layout

```text
docs/
  MODEL.md
  ARCHITECTURE.md
  EVIDENCE.md

data/
  northern-virginia/
src/
  ai_capacity_engine/
webmcp/
tests/
```

## Architecture rule

The engine must preserve the distinction between:

```text
announced != funded != permitted != powered != compute-ready != operational
```

Any future model that collapses these states into one number violates the design contract.
