"""Tiny CODEOWNERS matcher for must-read files."""

from __future__ import annotations

from pathlib import Path


def parse_codeowners(text: str) -> list[tuple[str, list[str]]]:
    rules: list[tuple[str, list[str]]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        rules.append((parts[0], parts[1:]))
    return rules


def load_codeowners(root: Path) -> list[tuple[str, list[str]]]:
    for rel in ("CODEOWNERS", ".github/CODEOWNERS", "docs/CODEOWNERS"):
        path = root / rel
        if path.exists():
            return parse_codeowners(path.read_text(encoding="utf-8", errors="replace"))
    return []


def _match(pattern: str, file: str) -> bool:
    file = file.lstrip("./")
    pattern = pattern.lstrip("/")
    if pattern.endswith("/*"):
        prefix = pattern[:-2]
        return file.startswith(prefix.rstrip("/") + "/") or file.startswith(prefix)
    if pattern.endswith("/"):
        return file.startswith(pattern)
    if "*" in pattern:
        from fnmatch import fnmatch

        return fnmatch(file, pattern) or fnmatch(file.split("/")[-1], pattern)
    return file == pattern or file.startswith(pattern.rstrip("/") + "/")


def owners_for(file: str, rules: list[tuple[str, list[str]]]) -> list[str]:
    hits: list[str] = []
    for pattern, owners in rules:
        if _match(pattern, file):
            hits = owners
    return hits


def owners_for_files(files: list[str], rules: list[tuple[str, list[str]]]) -> dict[str, list[str]]:
    return {f: owners_for(f, rules) for f in files}
