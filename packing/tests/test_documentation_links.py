"""A local link must survive moving the checkout to the CI runner."""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import check_documentation
from devtools.check_documentation import _link_problems

# Exercise the link scanner directly; a whole document-map fixture would hide the case.
# pyright: reportPrivateUsage=false


def test_existing_absolute_link_is_rejected_but_relative_link_passes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(check_documentation, "REPO", tmp_path)
    target = tmp_path / "proof.md"
    target.write_text("# Proof\n")
    report = tmp_path / "report.md"
    report.write_text("[Proof](proof.md)\n")
    assert _link_problems(report) == []
    report.write_text(f"[Proof]({target.as_posix()})\n")
    problems = _link_problems(report)
    assert len(problems) == 1
    assert "absolute local link" in problems[0]
