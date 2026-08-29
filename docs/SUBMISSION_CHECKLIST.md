# WebMCP Challenge Submission Checklist

Official submission deadline: **September 3, 2026 at 1:00 PM Pacific Time**.

## Already complete

- [x] Working public web app
- [x] Stable custom domain: `https://intelligence.businessaifuture.com`
- [x] Public GitHub repository
- [x] FastAPI backend and human-facing workbench
- [x] Eight WebMCP tools implemented
- [x] Shared human-agent state for mutating tools
- [x] Evidence-aware constraint behavior
- [x] Dependency tracing and critical-path completeness logic
- [x] Static WebMCP conformance audit
- [x] WebMCP contract tests
- [x] JavaScript syntax checks in CI
- [x] GitHub Actions passing on `main`
- [x] Render deployment of audited WebMCP code
- [x] Final-draft submission description
- [x] Sub-3-minute demo script
- [x] Judge/tester instructions
- [x] Primary-source evidence validation pass completed on 2026-08-29
- [x] Apache License 2.0 selected and added to the repository
- [x] Project `NOTICE` added for attribution and brand/license boundary

## Blocking before submission

### 1. Real WebMCP browser validation

- [ ] Open production URL in ChatGPT's in-app browser or Chrome 149+ with WebMCP enabled
- [ ] Confirm page reports `WebMCP: 8 tools`
- [ ] Confirm all eight tools are discoverable
- [ ] Execute all eight tools at least once
- [ ] Confirm mutating tools visibly update the page
- [ ] Confirm activity log records agent mutations
- [ ] Confirm `ASSUMED` / `UNKNOWN` integrity rules survive real tool invocation
- [ ] Confirm evidence and dependency tool payloads render correctly in the agent
- [ ] Confirm `calculate-critical-path` returns incomplete/unknown timing rather than a fabricated duration

### 2. Open-source license — complete

The public repository uses **Apache License 2.0**.

- [x] License selected
- [x] `LICENSE` added to repository root
- [x] `NOTICE` added to repository root
- [ ] Confirm GitHub displays Apache-2.0 licensing metadata after merge

Rationale: Apache-2.0 is permissive and challenge-compatible, includes an explicit patent grant/termination framework, and does not grant trademark rights beyond reasonable and customary attribution.

### 3. Evidence final pass — complete

- [x] Open every primary-source URL in `data/northern-virginia/evidence.registry.json`
- [x] Confirm the referenced source pages/documents are currently resolvable through public web discovery
- [x] Confirm publisher and date/year metadata
- [x] Re-read every `claim`
- [x] Re-read every `limitations` field
- [x] Confirm no project-level value is represented as regional available capacity
- [x] Confirm no permit is represented as operational capacity
- [x] Confirm no unsupported local water/grid capacity number has been introduced

Validated source set:

- PJM 2026 Long-Term Load Forecast Supplement — Dominion data-center load adjustment context
- PJM/Dominion Firehouse 230 kV delivery project — customer-load/dependency evidence
- Dominion Energy Virginia Powering Virginia — service-territory demand context
- Loudoun County Data Center Standards & Locations Phase 1 — zoning constraint
- Loudoun Water Data Center Water Use — planning/resilience context, no inferred capacity number
- Virginia DEQ Issued Air Permits for Data Centers — regulatory milestone registry
- Virginia SCC Data Center Initiatives — GS-5 / large-load governance context

### 4. Demo video

Official format: public YouTube demo, **under 3 minutes**, with audio.

- [ ] Use a WebMCP-capable environment
- [ ] Confirm app is warm and responsive before recording
- [ ] Record according to `docs/DEMO_SCRIPT.md`
- [ ] Keep WebMCP mutations visible
- [ ] Show at least one source-aware evidence retrieval
- [ ] Show dependency trace
- [ ] Show unknown critical-path duration
- [ ] Keep final duration below 3:00
- [ ] Include audible narration
- [ ] Upload publicly to YouTube
- [ ] Test video link in signed-out/private browser

### 5. Devpost entry

- [ ] Join/register for the challenge on Devpost
- [ ] Project name: `AI Systems Capacity Engine`
- [ ] Add working live URL
- [ ] Add public repository URL
- [ ] Paste final English description from `docs/CHALLENGE_SUBMISSION.md`
- [ ] Explain why WebMCP is a strong fit
- [ ] Explain the improved human-agent experience
- [ ] Explain what human and agent can now do together
- [ ] Briefly explain WebMCP implementation
- [ ] Add public YouTube demo URL
- [ ] Add testing instructions from `docs/TESTING_INSTRUCTIONS.md`
- [ ] Complete all other required Devpost form fields
- [ ] Verify submission materials are in English or include required English translations
- [ ] Submit before the deadline

## Pre-judge production checks

- [x] Production URL loads without authentication
- [x] `/api/health` is healthy in the deployed workbench
- [x] Custom HTTPS domain is live
- [ ] Re-check source links immediately before final submission
- [ ] No console error that prevents WebMCP registration in the compatible validation browser
- [x] No stale tool name `calculate-project-critical-path` remains in the prepared public challenge docs
- [ ] Render free-tier cold start is assessed before judging; upgrade only if necessary to avoid an unacceptable demo/judge delay

## Official judging dimensions to optimize for

- usefulness
- originality
- execution
- thoughtful use of WebMCP
- quality of the human-agent experience

## Submission gate

Do not call the project challenge-ready until the remaining two operational conditions are true:

```text
REAL WEBMCP INVOCATION PASSED
+ PUBLIC <3 MINUTE DEMO VIDEO VERIFIED
= READY TO SUBMIT
```
