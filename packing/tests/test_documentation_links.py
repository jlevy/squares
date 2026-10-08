"""A local link must survive moving the checkout to the CI runner."""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import check_documentation
from devtools.check_documentation import _link_problems


def test_only_declared_cargo_outputs_are_outside_document_map(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Rustdoc licenses are generated; ordinary target-named paths stay checked."""
    generated = tmp_path / "packing/sqsearch/target/doc/static.files/SourceSerif4-LICENSE.md"
    exact_generated = tmp_path / "packing/sqverify_exact/target/doc/static.files/LICENSE.md"
    native_generated = tmp_path / "packing/n17_kernel_verify/target/doc/static.files/LICENSE.md"
    authored = tmp_path / "docs/target/README.md"
    similar = tmp_path / "packing/sqsearch/target-not-generated/README.md"
    for path in (generated, exact_generated, native_generated, authored, similar):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Document\n")
    synopsis = tmp_path / "SYNOPSIS.md"
    synopsis.write_text("# Synopsis\n")
    monkeypatch.setattr(check_documentation, "REPO", tmp_path)
    monkeypatch.setattr(check_documentation, "MAP", tmp_path / "docs/project/document-map.yaml")
    monkeypatch.setattr(check_documentation, "SYNOPSIS", synopsis)
    monkeypatch.setattr(check_documentation, "is_vendored", lambda _: False)
    monkeypatch.setattr(
        check_documentation,
        "load_map",
        lambda: {
            "documents": [],
            "collections": [],
            "exclusions": [{"pattern": "SYNOPSIS.md"}],
        },
    )
    monkeypatch.setattr(check_documentation, "expected_synopsis", lambda current, _: current)
    assert check_documentation.check() == [
        "unmapped durable document: docs/target/README.md",
        "unmapped durable document: packing/sqsearch/target-not-generated/README.md",
    ]


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


def test_a_link_quoted_in_a_fenced_code_block_is_not_checked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A quoted line of another file keeps its links as text; outside the fence they count."""
    monkeypatch.setattr(check_documentation, "REPO", tmp_path)
    report = tmp_path / "report.md"
    quoted = "| [Row](docs/elsewhere.md) | record |"
    report.write_text(f"Text.\n\n```\n{quoted}\n```\n\n~~~~text\n{quoted}\n~~~~\n")
    assert _link_problems(report) == []
    # A shorter or other fence does not close it; an unclosed fence runs to the end.
    report.write_text(f"````\n```\n{quoted}\n~~~\n{quoted}\n")
    assert _link_problems(report) == []
    report.write_text(f"```\n{quoted}\n```\n{quoted}\n")
    assert _link_problems(report) == ["report.md: dead link -> docs/elsewhere.md"]
