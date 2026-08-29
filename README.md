# AI Systems Capacity Engine

Constraint-based model for AI infrastructure capacity, strategic dependencies, cyber resilience, governance, and time-to-deploy.

**Live app:** https://intelligence.businessaifuture.com

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/nandagomesagi/ai-systems-capacity-engine)

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

## WebMCP Challenge materials

- `docs/CHALLENGE_SUBMISSION.md` — submission copy
- `docs/DEMO_SCRIPT.md` — sub-3-minute demo plan
- `docs/TESTING_INSTRUCTIONS.md` — judge/tester prompts and expected behavior
- `docs/WEBMCP_AUDIT.md` — conformance hardening and validation boundary
- `docs/SUBMISSION_CHECKLIST.md` — remaining submission gates

## Deploy

A repository-root `render.yaml` defines the challenge web service. The Deploy to Render button above opens the Blueprint for this repository. Deployment uses the tested `main` branch, a pinned Python 3.11 runtime, Uvicorn, and `/api/health` as the health-check path.

Production custom domain:

```text
https://intelligence.businessaifuture.com
```

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

Use ChatGPT's in-app browser or a WebMCP-enabled compatible Chrome build to test agent discovery and invocation. The normal browser interface still works when WebMCP is unavailable.

## Tests

```bash
pytest -q
```

CI also parses the browser JavaScript as ES modules and runs WebMCP contract guards.

## Repository map

```text
data/northern-virginia/   source-aware MVP datasets and dependency graph seeds
docs/                     model, architecture, evidence, charter, roadmap and challenge material
src/ai_capacity_engine/   Python constraint and dependency engines
webapp/                   human + WebMCP shared-state workbench
webmcp/                   agent tool contracts
tests/                    model, evidence, API, dependency and WebMCP contract tests
```

## License

The repository code and documentation are licensed under the **Apache License 2.0**. See `LICENSE` and `NOTICE`.

Apache-2.0 was selected to keep the challenge repository genuinely open source while preserving explicit patent terms and keeping project/brand identifiers outside the software-license grant except for customary attribution.

## Status

**MODEL MVP v0.1 + WebMCP workbench deployed.**

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
