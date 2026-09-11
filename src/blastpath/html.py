"""Minimal self-contained HTML blast map."""

from __future__ import annotations

from html import escape

from .models import BlastReport


def format_html(report: BlastReport) -> str:
    files = "".join(f"<li><code>{escape(f)}</code></li>" for f in report.must_read) or "<li>None</li>"
    gods = "".join(f"<li><code>{escape(g)}</code></li>" for g in report.god_hits) or "<li>None</li>"
    return (
        "<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n"
        f"<title>BlastPath risk {report.risk}</title>\n"
        "<style>body{font:15px/1.45 system-ui,sans-serif;background:#0f1419;color:#e7ecf3;margin:0;padding:24px}"
        "h1{font-size:22px}.kpi{color:#9aa7b8}.risk{color:#fb7185;font-weight:700}code{color:#7dd3fc}"
        "</style></head><body>\n"
        "<h1>BlastPath · change radius</h1>\n"
        f"<p class=\"kpi\">Risk <span class=\"risk\">{report.risk}/100</span> · "
        f"hops {report.hops} · radius {len(report.radius_nodes)} · god hits {len(report.god_hits)}</p>\n"
        f"<h2>Must-read</h2><ul>{files}</ul>\n"
        f"<h2>God-node hits</h2><ul>{gods}</ul>\n"
        "</body></html>\n"
    )
