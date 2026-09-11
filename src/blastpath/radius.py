"""Compute blast radius for a set of changed files."""

from __future__ import annotations

from pathlib import Path

from .god import god_nodes
from .graph import CodeGraph
from .models import BlastReport
from .parse import module_id
from .risk import risk_score
from .walk import blast_radius


def symbols_in_files(graph: CodeGraph, rel_files: list[str]) -> list[str]:
    files = set(rel_files)
    return [nid for nid, node in graph.nodes.items() if node.file in files]


def analyze(graph: CodeGraph, changed_files: list[str], *, hops: int = 2, root: Path | None = None) -> BlastReport:
    seeds = symbols_in_files(graph, changed_files)
    if not seeds and root is not None:
        for rel in changed_files:
            path = root / rel
            if path.exists():
                seeds.append(module_id(root, path))
    radius, _edges = blast_radius(graph, seeds, hops=hops, reverse=True)
    gods = {n for n, _d in god_nodes(graph)}
    god_hits = sorted(n for n in radius if n in gods)
    must_read = sorted({graph.nodes[n].file for n in radius if n in graph.nodes and graph.nodes[n].file})
    report = BlastReport(
        changed_files=changed_files,
        changed_symbols=sorted(seeds),
        radius_nodes=sorted(radius),
        must_read=must_read,
        god_hits=god_hits,
        hops=hops,
        risk=0,
    )
    report.risk = risk_score(report, graph)
    return report
