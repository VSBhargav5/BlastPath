"""Persist a graph snapshot and diff two snapshots."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .graph import CodeGraph
from .models import Edge, Node, Provenance


def graph_to_dict(graph: CodeGraph) -> dict[str, Any]:
    edges = [e.model_dump() for bucket in graph.out.values() for e in bucket]
    return {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "nodes": [n.model_dump() for n in graph.nodes.values()],
        "edges": edges,
    }


def save_snapshot(graph: CodeGraph, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph_to_dict(graph), indent=2) + "\n")


def load_snapshot(path: Path) -> CodeGraph:
    raw = json.loads(path.read_text())
    nodes = [Node.model_validate(n) for n in raw.get("nodes", [])]
    edges = []
    for e in raw.get("edges", []):
        if isinstance(e.get("provenance"), str):
            e["provenance"] = Provenance(e["provenance"])
        edges.append(Edge.model_validate(e))
    return CodeGraph(nodes, edges)


def edge_key(src: str, dst: str, kind: str) -> str:
    return f"{src}|{kind}|{dst}"


def compare_graphs(old: CodeGraph, new: CodeGraph) -> dict[str, list[str]]:
    old_n, new_n = set(old.nodes), set(new.nodes)
    old_e = {edge_key(e.src, e.dst, e.kind) for bucket in old.out.values() for e in bucket}
    new_e = {edge_key(e.src, e.dst, e.kind) for bucket in new.out.values() for e in bucket}
    return {
        "nodes_added": sorted(new_n - old_n),
        "nodes_removed": sorted(old_n - new_n),
        "edges_added": sorted(new_e - old_e),
        "edges_removed": sorted(old_e - new_e),
    }
