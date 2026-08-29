from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
WEBMCP_SOURCE = (ROOT / "webapp" / "webmcp.js").read_text(encoding="utf-8")
INDEX_SOURCE = (ROOT / "webapp" / "index.html").read_text(encoding="utf-8")


EXPECTED_TOOLS = {
    "get-scenario-state",
    "set-scenario-target",
    "set-domain-assumption",
    "clear-domain-assumption",
    "evaluate-capacity",
    "get-evidence-record",
    "trace-project-dependencies",
    "calculate-critical-path",
}


def test_current_webmcp_entry_point_and_lifecycle_contract():
    assert "document.modelContext" in WEBMCP_SOURCE
    assert "globalThis.navigator?.modelContext" in WEBMCP_SOURCE
    assert "new AbortController()" in WEBMCP_SOURCE
    assert "registerTool(tool, registrationOptions)" in WEBMCP_SOURCE
    assert "unregisterTool(" not in WEBMCP_SOURCE
    assert "provideContext(" not in WEBMCP_SOURCE


def test_tool_names_are_distinct_and_within_recommended_budget():
    tool_names = set(re.findall(r'name:\s*"([^"]+)"', WEBMCP_SOURCE))
    assert tool_names == EXPECTED_TOOLS
    assert all(len(name) <= 30 for name in tool_names)


def test_tool_contract_has_schema_and_security_hints():
    assert WEBMCP_SOURCE.count("additionalProperties: false") >= 7
    assert WEBMCP_SOURCE.count("readOnlyHint:") == len(EXPECTED_TOOLS)
    assert WEBMCP_SOURCE.count("untrustedContentHint:") == len(EXPECTED_TOOLS)
    assert 'name: "get-evidence-record"' in WEBMCP_SOURCE
    assert "untrustedContentHint: true" in WEBMCP_SOURCE


def test_webmcp_returns_native_values_not_mcp_content_envelopes():
    assert "content: [" not in WEBMCP_SOURCE


def test_async_tools_propagate_execution_abort_signal():
    assert "{ signal } = {}" in WEBMCP_SOURCE
    assert "fetchJson(`/api/dependencies/${encodeURIComponent(graph_id)}/trace`, { signal })" in WEBMCP_SOURCE
    assert "api.evaluateScenario({ signal })" in WEBMCP_SOURCE


def test_human_visible_tool_list_matches_registered_tools():
    displayed_tools = set(re.findall(r"<span>([a-z0-9-]+)</span>", INDEX_SOURCE))
    assert EXPECTED_TOOLS.issubset(displayed_tools)
    assert "calculate-project-critical-path" not in INDEX_SOURCE


def test_judge_facing_hook_keeps_core_product_claim_precise():
    assert "AI infrastructure announcements are not deployable capacity." in INDEX_SOURCE
    assert "agent-entered values remain ASSUMED" in INDEX_SOURCE
    assert "unknowns remain UNKNOWN" in INDEX_SOURCE
