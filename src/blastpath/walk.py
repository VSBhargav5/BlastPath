"""BFS blast radius from seed symbols."""

from __future__ import annotations

from collections import deque

from .graph import CodeGraph
from .models import Edge


def blast_radius(
    graph: CodeGraph,
    seeds: list[str],
    *,
    hops: int = 2,
    reverse: bool = True,
) -> tuple[set[str], list[Edge]]:
    """Walk inbound by default: who depends on the changed symbols."""
    seen: set[str] = set(seeds)
    frontier = deque((s, 0) for s in seeds)
    walked: list[Edge] = []
    while frontier:
        node, depth = frontier.popleft()
        if depth >= hops:
            continue
        for edge in graph.neighbors(node, reverse=reverse):
            nxt = edge.src if reverse else edge.dst
            walked.append(edge)
            if nxt not in seen:
                seen.add(nxt)
                frontier.append((nxt, depth + 1))
    return seen, walked
