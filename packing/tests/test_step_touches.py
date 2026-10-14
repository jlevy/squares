"""A step's literal `touches` path names something tracked (think-mv16).

A change selects a step through its `touches`. A literal path that no longer names a file
selects nothing and says nothing: after a move, the step stops running for the moved
file's changes while every tier stays green. A glob may match nothing on purpose, so only
literal paths are held here.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from sqpack.cli.validate import STEPS

REPO = Path(__file__).resolve().parents[2]
GLOB = frozenset("*?[")


def tracked_paths() -> set[str]:
    listed = subprocess.run(
        ("git", "-C", str(REPO), "ls-files"), capture_output=True, text=True, check=False
    )
    if listed.returncode != 0:
        pytest.skip(listed.stderr.strip() or "git cannot list tracked files here")
    files = listed.stdout.split()
    directories = {
        "/".join(parts[:end])
        for parts in (f.split("/") for f in files)
        for end in range(1, len(parts))
    }
    return set(files) | directories


def test_every_literal_touches_path_names_something_tracked() -> None:
    tracked = tracked_paths()
    stale = [
        f"{step.name}: {path}"
        for step in STEPS
        for path in step.touches
        if not GLOB & set(path) and path.rstrip("/") not in tracked
    ]
    assert stale == []
