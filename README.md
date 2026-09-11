# BlastPath

**What breaks if this change lands?**

Graphify maps a *repo*. BlastPath maps a *change*.  
Same contract — **the answer is a path, not a vibe** — different job.

A PR touches `db.py`. Reviewers still grep. BlastPath walks inbound edges and writes a paste-ready radius: must-read files, god-node hits, risk 0–100.

Not a 36-language indexer. Python-first, local, no account, no embeddings.

**Current version: 0.1.0**

---

## Why this instead of Graphify

| | Graphify | BlastPath |
|--|----------|-----------|
| Unit | Whole codebase | A **diff / changed files** |
| Question | What is this repo? | What does **this PR** touch? |
| Artifact | City map | Construction-site map |
| v0.1 languages | 36 | Python (honest, deep) |

---

## Quick start

```bash
git clone https://github.com/VSBhargav5/BlastPath.git
cd BlastPath
pip install -e ".[dev]"
pytest -q

python -m blastpath radius . --diff examples/sample.diff --hops 4 --format md -o radius.md
python -m blastpath gods examples
```

---

## CLI

```bash
python -m blastpath build [root] [--json graph.json]
python -m blastpath gods [root]
python -m blastpath path SRC DST --root .
python -m blastpath radius [root] --file a.py --diff change.diff --hops 2 --format rich|md|html|json
```

---

## Tech

Python 3.11+ · stdlib `ast` · Pydantic · Typer · Rich

## License

MIT
