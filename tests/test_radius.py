from pathlib import Path

from blastpath.diffscan import files_from_diff
from blastpath.graph import CodeGraph
from blastpath.parse import parse_repo
from blastpath.radius import analyze
from blastpath.report import format_markdown


def test_diff_files():
    text = Path(__file__).resolve().parents[1].joinpath("examples/sample.diff").read_text()
    assert files_from_diff(text) == ["examples/sample_pkg/db.py"]


def test_radius_includes_callers():
    root = Path(__file__).resolve().parents[1]
    g = CodeGraph(*parse_repo(root))
    report = analyze(g, ["examples/sample_pkg/db.py"], hops=4, root=root)
    assert report.changed_files
    assert "BlastPath" in format_markdown(report)
