"""Explain why a node sits in the graph."""

from __future__ import annotations

from .graph import CodeGraph


def explain_node(graph: CodeGraph, node_id: str) -> dict:
    node = graph.nodes.get(node_id)
    if node is None:
        return {"id": node_id, "found": False}
    incoming = graph.neighbors(node_id, reverse=True)
    outgoing = graph.neighbors(node_id, reverse=False)
    return {
        "id": node_id,
        "found": True,
        "kind": node.kind.value,
        "file": node.file,
        "line": node.line,
        "degree": graph.degree(node_id),
        "called_by": [e.src for e in incoming if e.kind in {"calls", "imports"}][:20],
        "calls": [e.dst for e in outgoing if e.kind == "calls"][:20],
        "defines": [e.dst for e in outgoing if e.kind == "defines"][:20],
    }
