from pathlib import Path

from blastpath.graph import CodeGraph
from blastpath.parse import parse_repo
from blastpath.stats import graph_stats


def test_stats_nonzero():
    g = CodeGraph(*parse_repo(Path(__file__).resolve().parents[1] / "examples"))
    s = graph_stats(g)
    assert s["nodes"] > 0
    assert s["edges"] > 0
