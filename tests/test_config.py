from pathlib import Path

from blastpath.config import load_config


def test_defaults(tmp_path: Path):
    assert load_config(tmp_path)["hops"] == 2


def test_toml(tmp_path: Path):
    (tmp_path / "blastpath.toml").write_text("[blastpath]\nhops = 4\n")
    assert load_config(tmp_path)["hops"] == 4
