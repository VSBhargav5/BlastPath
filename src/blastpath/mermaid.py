"""Mermaid flowchart for a blast report."""

from __future__ import annotations

from .models import BlastReport


def _sid(name: str) -> str:
    out = []
    for ch in name:
        out.append(ch if ch.isalnum() else "_")
    return "n_" + "".join(out)[:80]


def format_mermaid(report: BlastReport) -> str:
    lines = ["flowchart LR"]
    seeds = set(report.changed_symbols[:30])
    radius = report.radius_nodes[:40]
    for nid in radius:
        shape = f"{{"{nid}"}}" if nid in seeds else f"[\"{nid}\"]"
        lines.append(f"  {_sid(nid)}{shape}")
    for src in report.changed_symbols[:20]:
        for dst in report.radius_nodes[:20]:
            if src != dst and src in radius and dst in radius:
                continue
    lines.append(f"  classDef seed fill:#fb7185,color:#111,stroke:#9f1239")
    return "\n".join(lines) + "\n"
