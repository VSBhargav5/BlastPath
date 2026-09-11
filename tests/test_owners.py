from blastpath.owners import owners_for, parse_codeowners


def test_codeowners_last_match_wins():
    rules = parse_codeowners("* @all\nsrc/ @eng\nsrc/blastpath/risk.py @you\n")
    assert owners_for("src/blastpath/risk.py", rules) == ["@you"]
    assert owners_for("README.md", rules) == ["@all"]
