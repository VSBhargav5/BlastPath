"""Honor .blastpathignore plus default junk dirs."""

from __future__ import annotations

from fnmatch import fnmatch
from pathlib import Path

DEFAULTS = [
    ".git/",
    ".venv/",
    "venv/",
    "__pycache__/",
    "node_modules/",
    ".tox/",
    "dist/",
    "build/",
    "*.egg-info/",
]


def load_patterns(root: Path) -> list[str]:
    extra: list[str] = []
    path = root / ".blastpathignore"
    if path.exists():
        extra = [ln.strip() for ln in path.read_text().splitlines() if ln.strip() and not ln.startswith("#")]
    return DEFAULTS + extra


def is_ignored(rel: str, patterns: list[str]) -> bool:
    rel = rel.replace("\\", "/").lstrip("./")
    for pat in patterns:
        p = pat.rstrip("/")
        if pat.endswith("/"):
            if rel.startswith(p + "/") or rel == p:
                return True
        if fnmatch(rel, pat) or fnmatch(rel.split("/")[-1], pat):
            return True
    return False
