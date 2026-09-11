from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .bands import risk_band
from .diffscan import files_from_diff, files_from_paths
from .gitwork import GitError, changed_files
from .god import god_nodes
from .graph import CodeGraph
from .html import format_html
from .owners import load_codeowners, owners_for_files
from .parse import parse_repo
from .paths import shortest_path
from .radius import analyze
from .report import format_markdown
from .snapshot import compare_graphs, load_snapshot, save_snapshot

app = typer.Typer(help="BlastPath – what breaks if this change lands", no_args_is_help=True)
console = Console()


def _graph(root: Path) -> CodeGraph:
    nodes, edges = parse_repo(root)
    return CodeGraph(nodes, edges)


def _emit_report(report, root: Path, fmt: str, output: Optional[Path]) -> None:
    rules = load_codeowners(root)
    owners = owners_for_files(report.must_read, rules) if rules else {}
    fmt = fmt.lower()
    if fmt == "md":
        content = format_markdown(report, owners=owners or None)
    elif fmt == "html":
        content = format_html(report)
    elif fmt == "json":
        payload = report.model_dump()
        payload["band"] = risk_band(report.risk)
        payload["owners"] = owners
        content = json.dumps(payload, indent=2) + "\n"
    elif fmt == "rich":
        content = None
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
    band = risk_band(report.risk)
    tone = "red" if report.risk >= 60 else "yellow" if report.risk >= 30 else "green"
    console.print(Panel.fit(
        f"[bold]BlastPath[/bold]  ·  risk {report.risk}/100 ({band})\n"
        f"Changed {len(report.changed_files)}  ·  radius {len(report.radius_nodes)}  ·  "
        f"must-read {len(report.must_read)}  ·  god hits {len(report.god_hits)}",
        border_style=tone,
    ))
    table = Table(title="Must-read")
    table.add_column("File")
    table.add_column("Owners")
    for f in report.must_read:
        table.add_row(f, ", ".join(owners.get(f, [])))
    console.print(table)


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
    git: bool = typer.Option(False, "--git", help="Use git changed files vs HEAD"),
    against: str = typer.Option("HEAD", "--against"),
    hops: int = typer.Option(2, "--hops", "-n"),
    format: str = typer.Option("rich", "--format"),
    output: Optional[Path] = typer.Option(None, "--output", "-o"),
):
    changed: list[str] = []
    if git:
        try:
            changed.extend(changed_files(root, against=against))
        except GitError as exc:
            console.print(f"[red]{exc}[/red]")
            raise typer.Exit(1)
    if diff:
        changed.extend(files_from_diff(diff.read_text(encoding="utf-8", errors="replace")))
    if files:
        changed.extend(files_from_paths(files, root))
    changed = list(dict.fromkeys(changed))
    if not changed:
        console.print("[red]Pass --file, --diff, or --git[/red]")
        raise typer.Exit(1)
    report = analyze(_graph(root), changed, hops=hops, root=root)
    _emit_report(report, root, format, output)


@app.command("snapshot")
def snapshot_cmd(
    root: Path = typer.Argument(Path(".")),
    output: Path = typer.Option(Path("blast-out/snapshot.json"), "--output", "-o"),
):
    save_snapshot(_graph(root), output)
    console.print(f"[green]Wrote[/green] {output}")


@app.command("compare")
def compare_cmd(old: Path, new: Path):
    delta = compare_graphs(load_snapshot(old), load_snapshot(new))
    console.print(json.dumps(delta, indent=2))


def main() -> None:
    app()
