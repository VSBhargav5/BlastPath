from pathlib import Path

from blastpath.god import god_nodes
from blastpath.graph import CodeGraph
from blastpath.parse import parse_repo
from blastpath.paths import shortest_path


def test_gods_and_path():
    root = Path(__file__).resolve().parents[1]
    g = CodeGraph(*parse_repo(root / "examples"))
    assert god_nodes(g, min_degree=1)
    srcs = [n for n in g.nodes if n.endswith("api")]
    dsts = [n for n in g.nodes if n.endswith("db") or n.endswith("DatabasePool")]
    if srcs and dsts:
        assert isinstance(shortest_path(g, srcs[0], dsts[0]), list)
