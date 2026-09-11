"""Optional blastpath.toml / pyproject tool.blastpath settings."""

from __future__ import annotations

from pathlib import Path
from typing import Any

DEFAULTS = {"hops": 2, "min_god_degree": 4, "format": "rich"}


def load_config(root: Path) -> dict[str, Any]:
    cfg = dict(DEFAULTS)
    path = root / "blastpath.toml"
    if not path.exists():
        return cfg
    text = path.read_text(encoding="utf-8", errors="replace")
    section = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        if "=" not in line:
            continue
        key, val = [p.strip() for p in line.split("=", 1)]
        if section and section not in {"blastpath", "tool.blastpath"}:
            continue
        if val.isdigit():
            cfg[key] = int(val)
        elif val.lower() in {"true", "false"}:
            cfg[key] = val.lower() == "true"
        else:
            cfg[key] = val.strip('"')
    return cfg
