from pathlib import Path

from blastpath.graph import CodeGraph
from blastpath.parse import parse_repo
from blastpath.snapshot import compare_graphs, load_snapshot, save_snapshot


def test_roundtrip(tmp_path: Path):
    root = Path(__file__).resolve().parents[1] / "examples"
    g = CodeGraph(*parse_repo(root))
    path = tmp_path / "snap.json"
    save_snapshot(g, path)
    loaded = load_snapshot(path)
    delta = compare_graphs(g, loaded)
    assert delta["nodes_added"] == []
    assert delta["nodes_removed"] == []
