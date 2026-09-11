from pathlib import Path

from blastpath.parse import parse_repo


def test_parses_sample():
    root = Path(__file__).resolve().parents[1]
    nodes, edges = parse_repo(root / "examples")
    ids = {n.id for n in nodes}
    assert any("auth" in i for i in ids)
    assert any(e.kind == "imports" for e in edges)
