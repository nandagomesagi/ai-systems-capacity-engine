import pytest

from ai_capacity_engine.dependencies import (
    DependencyEdge,
    DependencyNode,
    calculate_critical_path,
    trace_dependencies,
)


def test_trace_and_critical_path_for_known_chain():
    nodes = [
        DependencyNode("generation", "Generation", "power", 365, ["ev-gen"]),
        DependencyNode("transmission", "Transmission", "grid", 540, ["ev-grid"]),
        DependencyNode("substation", "Substation", "grid", 300),
        DependencyNode("data_center", "Data Center", "facility", 180),
    ]
    edges = [
        DependencyEdge("generation", "transmission"),
        DependencyEdge("transmission", "substation"),
        DependencyEdge("substation", "data_center"),
    ]

    trace = trace_dependencies(nodes, edges, "data_center")
    result = calculate_critical_path(nodes, edges, "data_center")

    assert trace.ordered_dependencies == ["generation", "transmission", "substation"]
    assert result.path == ["generation", "transmission", "substation", "data_center"]
    assert result.total_lead_time_days == 1385
    assert result.complete is True
    assert result.evidence_refs == ["ev-gen", "ev-grid"]


def test_unknown_lead_time_blocks_final_duration():
    nodes = [
        DependencyNode("transmission", "Transmission", "grid", None),
        DependencyNode("substation", "Substation", "grid", 300),
    ]
    edges = [DependencyEdge("transmission", "substation")]

    result = calculate_critical_path(nodes, edges, "substation")

    assert result.total_lead_time_days is None
    assert result.unknown_lead_time_nodes == ["transmission"]
    assert result.complete is False


def test_longest_known_branch_is_selected():
    nodes = [
        DependencyNode("power", "Power", "power", 500),
        DependencyNode("fiber", "Fiber", "network", 120),
        DependencyNode("site", "Site", "facility", 100),
    ]
    edges = [
        DependencyEdge("power", "site"),
        DependencyEdge("fiber", "site"),
    ]

    result = calculate_critical_path(nodes, edges, "site")

    assert result.path == ["power", "site"]
    assert result.total_lead_time_days == 600


def test_cycle_is_rejected():
    nodes = [
        DependencyNode("a", "A", "test", 1),
        DependencyNode("b", "B", "test", 1),
    ]
    edges = [
        DependencyEdge("a", "b"),
        DependencyEdge("b", "a"),
    ]

    with pytest.raises(ValueError, match="cycle"):
        calculate_critical_path(nodes, edges, "a")
