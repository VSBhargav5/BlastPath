from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .diffscan import files_from_diff, files_from_paths
from .god import god_nodes
from .graph import CodeGraph
from .html import format_html
from .parse import parse_repo
from .paths import shortest_path
from .radius import analyze
from .report import format_markdown

app = typer.Typer(help="BlastPath – what breaks if this change lands", no_args_is_help=True)
console = Console()


def _graph(root: Path) -> CodeGraph:
    nodes, edges = parse_repo(root)
    return CodeGraph(nodes, edges)


@app.command("build")
def build_cmd(root: Path = typer.Argument(Path(".")), json_out: Optional[Path] = typer.Option(None, "--json")):
    g = _graph(root)
    console.print(f"[green]Nodes[/green] {len(g.nodes)}  [green]Edges[/green] {sum(len(v) for v in g.out.values())}")
    if json_out:
        payload = {"nodes": [n.model_dump() for n in g.nodes.values()], "edges": [e.model_dump() for edges in g.out.values() for e in edges]}
        json_out.write_text(json.dumps(payload, indent=2) + "\n")
        console.print(f"[green]Wrote[/green] {json_out}")


@app.command("gods")
def gods_cmd(root: Path = typer.Argument(Path(".")), top: int = typer.Option(10, "--top")):
    table = Table(title="God nodes")
    table.add_column("Symbol")
    table.add_column("Degree", justify="right")
    for name, deg in god_nodes(_graph(root), top=top):
        table.add_row(name, str(deg))
    console.print(table)


@app.command("path")
def path_cmd(src: str, dst: str, root: Path = typer.Option(Path("."), "--root")):
    hops = shortest_path(_graph(root), src, dst)
    if not hops:
        console.print("[yellow]No path[/yellow]")
        raise typer.Exit(1)
    for h in hops:
        console.print(f"{h.src} -{h.kind}-> {h.dst}  [{h.provenance.value}] {h.file or ''}:{h.line or ''}")


@app.command("radius")
def radius_cmd(
    root: Path = typer.Argument(Path(".")),
    files: list[str] = typer.Option([], "--file", "-f"),
    diff: Optional[Path] = typer.Option(None, "--diff"),
    hops: int = typer.Option(2, "--hops", "-n"),
    format: str = typer.Option("rich", "--format"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
):
    changed: list[str] = []
    if diff:
        changed.extend(files_from_diff(diff.read_text(encoding="utf-8", errors="replace")))
    if files:
        changed.extend(files_from_paths(files, root))
    changed = list(dict.fromkeys(changed))
    if not changed:
        console.print("[red]Pass --file or --diff[/red]")
        raise typer.Exit(1)
    report = analyze(_graph(root), changed, hops=hops, root=root)
    fmt = format.lower()
    mapping = {"md": format_markdown, "html": format_html, "json": lambda r: r.model_dump_json(indent=2) + "\n"}
    if fmt == "rich":
        content = None
    elif fmt in mapping:
        content = mapping[fmt](report)
    else:
        console.print("[red]format must be rich, md, html, or json[/red]")
        raise typer.Exit(1)
    if content is not None:
        if output:
            output.write_text(content, encoding="utf-8")
            console.print(f"[green]Wrote[/green] {output}")
        else:
            console.print(content, highlight=False)
        return
    tone = "red" if report.risk >= 60 else "yellow" if report.risk >= 30 else "green"
    console.print(Panel.fit(
        f"[bold]BlastPath[/bold]  ·  risk {report.risk}/100\nChanged {len(report.changed_files)}  ·  radius {len(report.radius_nodes)}  ·  must-read {len(report.must_read)}  ·  god hits {len(report.god_hits)}",
        border_style=tone,
    ))
    table = Table(title="Must-read")
    table.add_column("File")
    for f in report.must_read:
        table.add_row(f)
    console.print(table)


def main() -> None:
    app()
