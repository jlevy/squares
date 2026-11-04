"""The paper-render comparison: what it calls a difference, and that it restores inputs."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from devtools import compare_paper_renders as tool
from devtools import render_overview

#: A tracked file no lane edits, so that HEAD's bytes are the working tree's.
STABLE = "LICENSE"


def test_a_difference_is_a_file_added_removed_or_changed(tmp_path: Path) -> None:
    first, second = tmp_path / "first", tmp_path / "second"
    for root in (first, second):
        (root / "papers").mkdir(parents=True)
        (root / "papers/same.html").write_bytes(b"same")
    (first / "papers/changed.md").write_bytes(b"one")
    (second / "papers/changed.md").write_bytes(b"two")
    (first / "papers/only-first.html").write_bytes(b"x")
    (second / "only-second.css").write_bytes(b"y")
    found = tool.differences(tool.tree_files(first), tool.tree_files(second))
    assert found == ["only-second.css", "papers/changed.md", "papers/only-first.html"]
    assert tool.differences(tool.tree_files(first), tool.tree_files(first)) == []


def _swap_and_fail(path: Path, head: bytes) -> None:
    with tool.baseline_inputs("HEAD", [STABLE]):
        assert path.read_bytes() == head
        raise RuntimeError("a render failed")


def test_the_baseline_inputs_are_swapped_in_and_restored_even_on_failure() -> None:
    path = tool.REPO / STABLE
    working = path.read_bytes()
    head = subprocess.run(
        ["git", "show", f"HEAD:{STABLE}"], cwd=tool.REPO, check=True, capture_output=True
    ).stdout
    with pytest.raises(RuntimeError, match="a render failed"):
        _swap_and_fail(path, head)
    assert path.read_bytes() == working


def test_every_paper_the_release_gate_names_has_its_own_renderer() -> None:
    named = {f"paper:{paper.slug}": paper.module for paper in render_overview.PAPERS}
    assert named == {paper: module for paper, (module, _) in tool.RENDERERS.items()}
