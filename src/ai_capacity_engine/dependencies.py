from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Optional, Set, Tuple


@dataclass(frozen=True)
class DependencyNode:
    node_id: str
    label: str
    node_type: str
    lead_time_days: Optional[int] = 0
    evidence_refs: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError("node_id must be non-empty")
        if not self.label.strip():
            raise ValueError("label must be non-empty")
        if not self.node_type.strip():
            raise ValueError("node_type must be non-empty")
        if self.lead_time_days is not None and self.lead_time_days < 0:
            raise ValueError("lead_time_days must be >= 0 or None")


@dataclass(frozen=True)
class DependencyEdge:
    upstream: str
    downstream: str
    relation: str = "REQUIRES"
    evidence_refs: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class DependencyTrace:
    target_node: str
    ordered_dependencies: List[str]
    evidence_refs: List[str]


@dataclass(frozen=True)
class CriticalPathResult:
    target_node: str
    path: List[str]
    total_lead_time_days: Optional[int]
    unknown_lead_time_nodes: List[str]
    evidence_refs: List[str]
    complete: bool


def _build_maps(
    nodes: Iterable[DependencyNode],
    edges: Iterable[DependencyEdge],
) -> Tuple[Dict[str, DependencyNode], Dict[str, List[DependencyEdge]]]:
    node_map: Dict[str, DependencyNode] = {}
    for node in nodes:
        if node.node_id in node_map:
            raise ValueError(f"Duplicate dependency node: {node.node_id}")
        node_map[node.node_id] = node

    incoming: Dict[str, List[DependencyEdge]] = {node_id: [] for node_id in node_map}
    for edge in edges:
        if edge.upstream not in node_map:
            raise ValueError(f"Unknown upstream node: {edge.upstream}")
        if edge.downstream not in node_map:
            raise ValueError(f"Unknown downstream node: {edge.downstream}")
        incoming[edge.downstream].append(edge)

    return node_map, incoming


def trace_dependencies(
    nodes: Iterable[DependencyNode],
    edges: Iterable[DependencyEdge],
    target_node: str,
) -> DependencyTrace:
    node_map, incoming = _build_maps(nodes, edges)
    if target_node not in node_map:
        raise ValueError(f"Unknown target node: {target_node}")

    ordered: List[str] = []
    evidence_refs: Set[str] = set(node_map[target_node].evidence_refs)
    visiting: Set[str] = set()
    visited: Set[str] = set()

    def visit(node_id: str) -> None:
        if node_id in visiting:
            raise ValueError("Dependency graph contains a cycle")
        if node_id in visited:
            return

        visiting.add(node_id)
        for edge in incoming[node_id]:
            evidence_refs.update(edge.evidence_refs)
            visit(edge.upstream)
        visiting.remove(node_id)
        visited.add(node_id)

        evidence_refs.update(node_map[node_id].evidence_refs)
        if node_id != target_node:
            ordered.append(node_id)

    visit(target_node)

    return DependencyTrace(
        target_node=target_node,
        ordered_dependencies=ordered,
        evidence_refs=sorted(evidence_refs),
    )


def calculate_critical_path(
    nodes: Iterable[DependencyNode],
    edges: Iterable[DependencyEdge],
    target_node: str,
) -> CriticalPathResult:
    """Return the longest prerequisite path to a target.

    A final duration is only emitted if every node on the selected dependency
    closure has a known lead time. Unknown timing cannot be silently treated as
    zero because that would manufacture a false feasible date.
    """
    node_map, incoming = _build_maps(nodes, edges)
    if target_node not in node_map:
        raise ValueError(f"Unknown target node: {target_node}")

    visiting: Set[str] = set()
    memo: Dict[str, Tuple[int, List[str]]] = {}
    closure: Set[str] = set()
    evidence_refs: Set[str] = set()

    def longest_known_path(node_id: str) -> Tuple[int, List[str]]:
        if node_id in visiting:
            raise ValueError("Dependency graph contains a cycle")
        if node_id in memo:
            return memo[node_id]

        visiting.add(node_id)
        closure.add(node_id)
        node = node_map[node_id]
        evidence_refs.update(node.evidence_refs)

        best_upstream_duration = 0
        best_upstream_path: List[str] = []

        for edge in incoming[node_id]:
            evidence_refs.update(edge.evidence_refs)
            upstream_duration, upstream_path = longest_known_path(edge.upstream)
            if upstream_duration > best_upstream_duration:
                best_upstream_duration = upstream_duration
                best_upstream_path = upstream_path

        visiting.remove(node_id)

        own_duration = node.lead_time_days or 0
        result = (
            best_upstream_duration + own_duration,
            [*best_upstream_path, node_id],
        )
        memo[node_id] = result
        return result

    known_duration, path = longest_known_path(target_node)

    unknown_nodes = sorted(
        node_id for node_id in closure if node_map[node_id].lead_time_days is None
    )
    complete = not unknown_nodes

    return CriticalPathResult(
        target_node=target_node,
        path=path,
        total_lead_time_days=known_duration if complete else None,
        unknown_lead_time_nodes=unknown_nodes,
        evidence_refs=sorted(evidence_refs),
        complete=complete,
    )
