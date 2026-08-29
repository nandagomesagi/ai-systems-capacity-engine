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

### 2. Open-source license

The Devpost resources require the public repository to contain an open-source license.

- [ ] Owner selects the license
- [ ] Add `LICENSE` to repository root
- [ ] Confirm repository licensing metadata is visible on GitHub

Do not select a license automatically: this affects downstream reuse rights and should be an explicit owner decision.

### 3. Evidence final pass

- [ ] Open every primary-source URL in `data/northern-virginia/evidence.registry.json`
- [ ] Confirm each URL is live and publicly accessible
- [ ] Confirm publisher and date metadata
- [ ] Re-read every `claim`
- [ ] Re-read every `limitations` field
- [ ] Confirm no project-level value is represented as regional available capacity
- [ ] Confirm no permit is represented as operational capacity
- [ ] Confirm no unsupported local water/grid capacity number has been introduced

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

- [ ] Production URL loads without authentication
- [ ] `/api/health` returns success
- [ ] Custom TLS certificate is valid
- [ ] No broken source links
- [ ] No console error that prevents WebMCP registration
- [ ] No stale tool name `calculate-project-critical-path` remains in public docs
- [ ] Render free-tier cold start is assessed before judging; upgrade only if necessary to avoid an unacceptable demo/judge delay

## Official judging dimensions to optimize for

- usefulness
- originality
- execution
- thoughtful use of WebMCP
- quality of the human-agent experience

## Submission gate

Do not call the project challenge-ready until all three conditions are true:

```text
REAL WEBMCP INVOCATION PASSED
+ OPEN-SOURCE LICENSE ADDED
+ PUBLIC <3 MINUTE DEMO VIDEO VERIFIED
= READY TO SUBMIT
```
