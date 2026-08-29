# WebMCP Conformance Audit — 2026-08-29

## Scope

Audit the workbench implementation against the current WebMCP draft and Chrome implementation guidance.

Primary references:

- W3C Web Machine Learning Community Group draft: https://webmachinelearning.github.io/webmcp/
- Chrome WebMCP overview: https://developer.chrome.com/docs/ai/webmcp
- Chrome Imperative API: https://developer.chrome.com/docs/ai/webmcp/imperative-api
- Chrome WebMCP tool security: https://developer.chrome.com/docs/ai/webmcp/secure-tools
- Chrome WebMCP best practices: https://developer.chrome.com/docs/ai/webmcp/best-practices

## Findings

### 1. Entry point and registration lifecycle

Status: aligned after hardening.

The current producer API is `document.modelContext.registerTool(...)`. A fallback to the deprecated `navigator.modelContext` location is retained only for compatibility. Registration is asynchronous and uses an `AbortSignal` to own the tool lifecycle.

### 2. Origin-keyed agent cluster

Status: fixed.

WebMCP registration requires an origin-keyed agent cluster. The service now sends:

```http
Origin-Agent-Cluster: ?1
```

The service also explicitly limits the WebMCP Permissions Policy to the same origin:

```http
Permissions-Policy: camera=(), microphone=(), geolocation=(), tools=(self)
```

### 3. Tool return values

Status: fixed.

Tool callbacks now return native JavaScript values directly. WebMCP serializes the result for the caller. The previous extra MCP-style `content` wrapper was removed to keep the implementation aligned with the browser-native API and reduce agent-output overhead.

### 4. Tool annotations

Status: fixed.

Every tool now declares `readOnlyHint` and `untrustedContentHint`. Evidence/dependency tools are marked read-only and their externally sourced content is marked untrusted for agent-safety signaling.

### 5. Input schemas

Status: hardened.

All tools now have explicit object schemas. No-argument tools use an empty object schema. Declared schemas reject undeclared properties with `additionalProperties: false`. Runtime validation remains authoritative.

### 6. Cancellation

Status: fixed.

Async tool callbacks accept the WebMCP execution `AbortSignal` and propagate it into network requests. This allows user or agent cancellation to stop pending fetches.

### 7. Registration diagnostics

Status: fixed.

A browser that does not expose WebMCP remains labeled `browser unavailable`. A browser that exposes the API but rejects registration is now labeled `registration blocked`, with the error and `originAgentCluster` state recorded in the page activity log.

### 8. Tool naming

Status: hardened.

The longest tool name was shortened from `calculate-project-critical-path` to `calculate-critical-path` to remain within Chrome's current recommended 30-character tool-name budget.

## Automated guards

CI checks:

- Python tests;
- JavaScript syntax with `node --check`;
- presence of current WebMCP entry points and lifecycle primitives;
- absence of removed APIs such as `provideContext()` and `unregisterTool()`;
- exact eight-tool contract;
- tool-name length budget;
- schema hardening and security annotations;
- native return values instead of an MCP `content` envelope;
- WebMCP origin and permissions response headers.

## Remaining validation

This audit establishes source-level and CI-level conformance. It does **not** replace a real browser-agent invocation test.

Before claiming end-to-end WebMCP validation, verify in a compatible environment that:

1. all eight tools are discovered;
2. each tool can be invoked successfully;
3. mutating tools change the same visible page state;
4. read-only tools return the expected evidence/dependency data;
5. cancellation behaves correctly for pending requests;
6. `calculate-critical-path` preserves `UNKNOWN` when lead times are unsupported;
7. the agent selects the intended tool from natural-language prompts.

Browser-level validation remains explicitly pending until those checks are completed in a compatible runtime.
