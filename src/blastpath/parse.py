"""Python AST → modules, functions, classes, imports, calls."""

from __future__ import annotations

import ast
from pathlib import Path

from .models import Edge, Node, NodeKind, Provenance

SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".tox", "dist", "build"}


def iter_py_files(root: Path) -> list[Path]:
    root = root.resolve()
    files = [p for p in root.rglob("*.py") if not any(part in SKIP_DIRS for part in p.parts)]
    return sorted(files)


def module_id(root: Path, file: Path) -> str:
    rel = file.resolve().relative_to(root.resolve())
    return ".".join(rel.with_suffix("").parts)


def parse_file(root: Path, file: Path) -> tuple[list[Node], list[Edge]]:
    text = file.read_text(encoding="utf-8", errors="replace")
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [], []
    rel = str(file.resolve().relative_to(root.resolve()))
    mid = module_id(root, file)
    nodes: list[Node] = [Node(id=mid, kind=NodeKind.MODULE, name=file.stem, file=rel, line=1, qualname=mid)]
    edges: list[Edge] = []
    defined: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            nid = f"{mid}.{node.name}"
            nodes.append(Node(id=nid, kind=NodeKind.FUNCTION, name=node.name, file=rel, line=node.lineno, qualname=nid))
            defined[node.name] = nid
            edges.append(Edge(src=mid, dst=nid, kind="defines", file=rel, line=node.lineno))
        elif isinstance(node, ast.ClassDef):
            cid = f"{mid}.{node.name}"
            nodes.append(Node(id=cid, kind=NodeKind.CLASS, name=node.name, file=rel, line=node.lineno, qualname=cid))
            defined[node.name] = cid
            edges.append(Edge(src=mid, dst=cid, kind="defines", file=rel, line=node.lineno))
            for item in node.body:
                if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef):
                    nid = f"{cid}.{item.name}"
                    nodes.append(Node(id=nid, kind=NodeKind.FUNCTION, name=item.name, file=rel, line=item.lineno, qualname=nid))
                    defined[item.name] = nid
                    edges.append(Edge(src=cid, dst=nid, kind="defines", file=rel, line=item.lineno))
    imports: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                imports[name] = alias.name
                edges.append(Edge(src=mid, dst=alias.name, kind="imports", provenance=Provenance.EXTRACTED, file=rel, line=node.lineno))
        elif isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                local = alias.asname or alias.name
                target = f"{node.module}.{alias.name}"
                imports[local] = target
                edges.append(Edge(src=mid, dst=target, kind="imports", provenance=Provenance.EXTRACTED, file=rel, line=node.lineno))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = None
        if isinstance(node.func, ast.Name):
            name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            name = node.func.attr
        if not name:
            continue
        dst = defined.get(name) or imports.get(name) or name
        prov = Provenance.EXTRACTED if name in defined or name in imports else Provenance.AMBIGUOUS
        edges.append(Edge(src=mid, dst=dst, kind="calls", provenance=prov, file=rel, line=getattr(node, "lineno", 1)))
    return nodes, edges


def parse_repo(root: Path) -> tuple[list[Node], list[Edge]]:
    nodes: list[Node] = []
    edges: list[Edge] = []
    for file in iter_py_files(root):
        n, e = parse_file(root, file)
        nodes.extend(n)
        edges.extend(e)
    return nodes, edges
