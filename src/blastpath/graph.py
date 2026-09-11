"""In-memory directed graph."""

from __future__ import annotations

from collections import defaultdict

from .models import Edge, Node, NodeKind


class CodeGraph:
    def __init__(self, nodes: list[Node] | None = None, edges: list[Edge] | None = None):
        self.nodes: dict[str, Node] = {}
        self.out: dict[str, list[Edge]] = defaultdict(list)
        self.inn: dict[str, list[Edge]] = defaultdict(list)
        for n in nodes or []:
            self.add_node(n)
        for e in edges or []:
            self.add_edge(e)

    def add_node(self, node: Node) -> None:
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge) -> None:
        self.out[edge.src].append(edge)
        self.inn[edge.dst].append(edge)
        if edge.src not in self.nodes:
            self.nodes[edge.src] = Node(id=edge.src, kind=NodeKind.MODULE, name=edge.src, file="")
        if edge.dst not in self.nodes:
            self.nodes[edge.dst] = Node(id=edge.dst, kind=NodeKind.MODULE, name=edge.dst, file="")

    def neighbors(self, node_id: str, *, reverse: bool = False) -> list[Edge]:
        return list(self.inn[node_id] if reverse else self.out[node_id])

    def degree(self, node_id: str) -> int:
        return len(self.out[node_id]) + len(self.inn[node_id])
