"""Graph summary stats for a build."""

from __future__ import annotations

from collections import Counter

from .graph import CodeGraph


def graph_stats(graph: CodeGraph) -> dict[str, int | float]:
    kinds = Counter(n.kind.value for n in graph.nodes.values())
    edge_kinds = Counter(e.kind for bucket in graph.out.values() for e in bucket)
    n_edges = sum(len(v) for v in graph.out.values())
    n_nodes = len(graph.nodes)
    return {
        "nodes": n_nodes,
        "edges": n_edges,
        "modules": kinds.get("module", 0),
        "classes": kinds.get("class", 0),
        "functions": kinds.get("function", 0),
        "calls": edge_kinds.get("calls", 0),
        "imports": edge_kinds.get("imports", 0),
        "defines": edge_kinds.get("defines", 0),
        "avg_degree": round((2 * n_edges / n_nodes) if n_nodes else 0.0, 2),
    }
