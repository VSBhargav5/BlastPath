"""Risk score 0–100 from radius size + god-node hits."""

from __future__ import annotations

from .graph import CodeGraph
from .models import BlastReport


def risk_score(report: BlastReport, graph: CodeGraph) -> int:
    score = 0
    score += min(len(report.changed_files) * 4, 20)
    score += min(len(report.radius_nodes) * 2, 40)
    score += min(len(report.god_hits) * 12, 30)
    if any(graph.degree(n) >= 10 for n in report.changed_symbols if n in graph.nodes):
        score += 10
    return min(score, 100)
