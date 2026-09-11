"""God nodes — high degree symbols everything depends on."""

from __future__ import annotations

from .graph import CodeGraph


def god_nodes(graph: CodeGraph, *, top: int = 10, min_degree: int = 4) -> list[tuple[str, int]]:
    ranked = sorted(
        ((nid, graph.degree(nid)) for nid in graph.nodes),
        key=lambda kv: kv[1],
        reverse=True,
    )
    return [(n, d) for n, d in ranked if d >= min_degree][:top]
