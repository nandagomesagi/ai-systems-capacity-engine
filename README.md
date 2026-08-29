# AI Systems Capacity Engine

Constraint-based model for AI infrastructure capacity, strategic dependencies, cyber resilience, governance, and time-to-deploy.

## Core question

> Given a target AI scale, what architecture is required, what limits deployment, and what can be securely sustained by a given date?

## Design principles

- **Architecture Before Amplification** — supporting architecture must exist before scale is treated as feasible.
- **Limits Before Scale** — identify the first binding constraint before accepting expansion claims.
- **Evidence Before Assertion** — material inputs retain source, timestamp, geography, and verification state.
- **No false precision** — `OBSERVED`, `DERIVED`, `ASSUMED`, and `UNKNOWN` remain distinct.
- **Shared human-agent state** — WebMCP tools operate on the same live scenario the user sees.

## MVP — Northern Virginia / Loudoun County

The first implementation is a source-aware scenario workbench for additional AI data-center capacity in Northern Virginia, with Loudoun County as the core demonstration geography and Dominion/PJM as broader power-system context.

Required capacity domains:

```text
power
grid
water
cooling
network
permits
```

Core outputs:

```text
deployable_capacity_mw
provisional_capacity_mw
binding_constraint
provisional_binding_constraint
architecture_gaps_mw
unknown_domains
unresolved_controls
complete
```

## Constraint model

```text
DEPLOYABLE_CAPACITY = min(required domain support)
```

A final numeric result is emitted only when every required domain is known. If any domain is unknown, the engine may expose a clearly labeled provisional minimum from known domains but withholds final deployable capacity and final binding constraint.

## Evidence states

```text
OBSERVED
DERIVED
ASSUMED
UNKNOWN
```

Scenario values entered by a human or agent are always `ASSUMED` and never inherit primary-source evidence references.

## WebMCP workbench

The browser app registers tools through the current WebMCP page API (`document.modelContext.registerTool`). Mutating tools update the same inputs and results visible to the human user.

Current tools:

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

The Firehouse dependency example deliberately withholds a numeric critical-path duration because the primary source does not publish defensible component lead times.

WebMCP is an interface to the model, not the product itself.

## Run locally

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn ai_capacity_engine.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

Use a WebMCP-capable browser environment to test agent discovery and invocation. The normal browser interface still works when WebMCP is unavailable.

## Tests

```bash
pytest -q
```

CI runs the test suite on pushes to `main` and pull requests.

## Repository map

```text
data/northern-virginia/   source-aware MVP datasets and dependency graph seeds
docs/                     model, architecture, evidence, charter, roadmap
src/ai_capacity_engine/   Python constraint and dependency engines
webapp/                   human + WebMCP shared-state workbench
webmcp/                   agent tool contracts
tests/                    model, evidence, API, and dependency tests
```

## Status

**MODEL MVP v0.1 + WebMCP workbench implementation.**

The immediate objective is to validate the end-to-end chain:

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

before expanding geography or claiming national-scale capacity estimates.

---

NANDA GOMES AI® / BUSINESS AI FUTURE®
