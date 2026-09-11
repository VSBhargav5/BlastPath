"""Shortest path between two nodes."""

from __future__ import annotations

from collections import deque

from .graph import CodeGraph
from .models import PathHop


def shortest_path(graph: CodeGraph, src: str, dst: str, *, max_hops: int = 8) -> list[PathHop]:
    if src == dst:
        return []
    prev: dict[str, tuple[str, object]] = {}
    q = deque([src])
    seen = {src}
    found = False
    while q:
        cur = q.popleft()
        for edge in graph.neighbors(cur, reverse=False):
            nxt = edge.dst
            if nxt in seen:
                continue
            seen.add(nxt)
            prev[nxt] = (cur, edge)
            if nxt == dst:
                found = True
                q.clear()
                break
            q.append(nxt)
        if found:
            break
        if len(seen) > 5000:
            break
    if dst not in prev:
        return []
    hops: list[PathHop] = []
    cur = dst
    guard = 0
    while cur != src and guard < max_hops:
        parent, edge = prev[cur]
        hops.append(
            PathHop(
                src=edge.src,
                dst=edge.dst,
                kind=edge.kind,
                provenance=edge.provenance,
                file=edge.file,
                line=edge.line,
            )
        )
        cur = parent
        guard += 1
    hops.reverse()
    return hops
