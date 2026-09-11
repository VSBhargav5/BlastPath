"""PR-ready Markdown artifact."""

from __future__ import annotations

from .bands import risk_band
from .models import BlastReport


def format_markdown(report: BlastReport, owners: dict[str, list[str]] | None = None) -> str:
    band = risk_band(report.risk)
    lines = [
        "# BlastPath · change radius",
        "",
        f"Risk **{report.risk}/100** ({band}) · hops **{report.hops}** · "
        f"changed files **{len(report.changed_files)}** · "
        f"radius **{len(report.radius_nodes)}** · "
        f"god-node hits **{len(report.god_hits)}**",
        "",
        "## Changed files",
    ]
    if report.changed_files:
        lines.extend(f"- `{f}`" for f in report.changed_files)
    else:
        lines.append("- None")
    lines += ["", "## Must-read (in radius)"]
    if report.must_read:
        for f in report.must_read:
            who = ""
            if owners and owners.get(f):
                who = " — " + ", ".join(owners[f])
            lines.append(f"- `{f}`{who}")
    else:
        lines.append("- None")
    lines += ["", "## Changed symbols"]
    if report.changed_symbols:
        lines.extend(f"- `{s}`" for s in report.changed_symbols[:40])
        extra = len(report.changed_symbols) - 40
        if extra > 0:
            lines.append(f"- …and {extra} more")
    else:
        lines.append("- None")
    lines += ["", "## God-node hits"]
    if report.god_hits:
        lines.extend(f"- `{s}`" for s in report.god_hits)
    else:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)
