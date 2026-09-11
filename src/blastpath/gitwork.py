"""Changed files from the working tree or a git range."""

from __future__ import annotations

import subprocess
from pathlib import Path


class GitError(RuntimeError):
    pass


def _run(root: Path, *args: str) -> str:
    try:
        proc = subprocess.run(
            ["git", *args],
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise GitError("git is not on PATH") from exc
    if proc.returncode != 0:
        raise GitError(proc.stderr.strip() or "git command failed")
    return proc.stdout


def changed_files(root: Path, *, against: str = "HEAD", unstaged: bool = True) -> list[str]:
    """Python files changed vs `against`, plus unstaged by default."""
    names: list[str] = []
    out = _run(root, "diff", "--name-only", "--diff-filter=ACMR", against)
    names.extend(out.splitlines())
    if unstaged:
        out = _run(root, "diff", "--name-only", "--diff-filter=ACMR")
        names.extend(out.splitlines())
        out = _run(root, "ls-files", "--others", "--exclude-standard")
        names.extend(out.splitlines())
    py = [n for n in names if n.endswith(".py")]
    return list(dict.fromkeys(py))
