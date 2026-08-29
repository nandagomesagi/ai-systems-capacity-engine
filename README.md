# AI Systems Capacity Engine

Constraint-based model for AI infrastructure capacity, strategic dependencies, cyber resilience, governance, and time-to-deploy.

**Live app:** https://intelligence.businessaifuture.com

## Project status

This prototype was developed during the 2026 OpenAI WebMCP Challenge period, but it was **not submitted** after a review of the official geographic eligibility rules determined that the author was not eligible to enter from Brazil.

No claim is made that this repository was an official competition entry, finalist, winner, or award recipient.

Development continues independently as Nanda Gomes intellectual property.

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

The browser app registers tools through the WebMCP page API (`document.modelContext.registerTool`). Mutating tools update the same inputs and results visible to the human user.

Current tools:

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

The Firehouse dependency example deliberately withholds a numeric critical-path duration because the ingested primary evidence does not publish defensible component lead times.

WebMCP is an interface to the model, not the product itself.

## Protection and licensing

**Current and future revisions are proprietary. Copyright © 2026 Nanda Gomes. All rights reserved.**

No permission is granted to copy, reproduce, modify, distribute, sublicense, commercialize, or create derivative works from the current revision without prior written permission, except where required by applicable law. See `LICENSE`.

Earlier repository revisions were published under Apache License 2.0. Rights already granted for those historical Apache-2.0 revisions cannot be retroactively revoked. The current proprietary notice applies to the current revision and subsequent revisions to the extent the relevant copyright is owned by Nanda Gomes.

Project and brand identifiers are not licensed for reuse merely because source code can be viewed.

## Repository map

```text
data/northern-virginia/   source-aware MVP datasets and dependency graph seeds
docs/                     model, architecture, evidence, charter and roadmap
src/ai_capacity_engine/   Python constraint and dependency engines
webapp/                   human + WebMCP shared-state workbench
webmcp/                   agent tool contracts
tests/                    model, evidence, API, dependency and WebMCP contract tests
```

## Status

**MODEL MVP v0.1 + WebMCP workbench deployed.**

The technical objective remains to validate and evolve the chain:

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

without expanding claims beyond defensible evidence.

---

NANDA GOMES AI® / BUSINESS AI FUTURE®
