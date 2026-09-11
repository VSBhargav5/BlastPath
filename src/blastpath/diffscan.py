"""Turn a unified diff or a file list into changed paths."""

from __future__ import annotations

from pathlib import Path


def files_from_diff(text: str) -> list[str]:
    found: list[str] = []
    for line in text.splitlines():
        if line.startswith("+++ "):
            rest = line[4:].strip()
            if rest == "/dev/null":
                continue
            if rest.startswith("a/") or rest.startswith("b/"):
                rest = rest[2:]
            found.append(rest)
    return list(dict.fromkeys(found))


def files_from_paths(paths: list[str], root: Path) -> list[str]:
    out = []
    root = root.resolve()
    for p in paths:
        path = Path(p)
        if not path.is_absolute():
            path = root / path
        if path.exists() and path.suffix == ".py":
            try:
                out.append(str(path.resolve().relative_to(root)))
            except ValueError:
                out.append(str(path))
    return out
