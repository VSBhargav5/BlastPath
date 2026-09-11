from blastpath.ignore import is_ignored, load_patterns


def test_default_skips_venv():
    pats = load_patterns(__import__("pathlib").Path("."))
    assert is_ignored(".venv/lib/x.py", pats)
    assert is_ignored("src/foo.py", pats) is False
