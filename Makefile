.PHONY: test radius snapshot

test:
	PYTHONPATH=src pytest -q

radius:
	PYTHONPATH=src python -m blastpath radius . --diff examples/sample.diff --hops 4 --format md -o radius.md

snapshot:
	PYTHONPATH=src python -m blastpath snapshot . -o blast-out/snapshot.json
