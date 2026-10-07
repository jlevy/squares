"""Historical layers preserve only an explicitly adopted later source report."""

from __future__ import annotations

from pathlib import Path

import pytest
from yaml import safe_dump

from devtools import source_supersession as sources


def test_a_later_selection_does_not_turn_an_earlier_draft_into_a_no_op(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    coverage = {
        "sources": [{"id": "new", "source_key": "[new]"}],
        "selected_overrides": [{"n": 2, "source_id": "new"}],
        "superseded_reports": [{"n": 2, "source_id": "old", "superseded_by": "new"}],
    }
    path = tmp_path / "coverage.yaml"
    path.write_text(safe_dump(coverage))
    monkeypatch.setattr(sources, "COVERAGE", path)
    assert sources.superseded_counts(coverage, {"old"}) == {2}
    assert sources.superseded_counts(coverage, {"new"}) == set()
    for key, expected in (("[old]", False), ("[new]", True)):
        text = (
            "---\n"
            + safe_dump({"packing": {"reported_upper_bound": {"source_key": key}}})
            + "---\nbody\n"
        )
        assert sources.preserve_selected_case(2, text, {"old"}) is expected


def test_an_unrelated_supersession_never_claims_the_selected_source() -> None:
    coverage = {
        "selected_overrides": [{"n": 2, "source_id": "other"}],
        "superseded_reports": [{"n": 2, "source_id": "old", "superseded_by": "new"}],
    }
    assert sources.superseded_counts(coverage, {"old"}) == set()


def test_coverage_updates_preserve_the_order_and_facts_of_other_imports() -> None:
    original = (
        "selected_overrides:\n"
        "  - n: 2\n    source_id: new\n    value: '2'\n"
        "  - n: 1\n    source_id: old\n    value: '3'\n"
        "superseded_reports: []\n"
    )
    rendered = (
        "selected_overrides:\n"
        "  - n: 1\n    source_id: old\n    value: '3'\n"
        "  - n: 2\n    source_id: new\n    value: '99'\n"
        "superseded_reports: []\n"
    )
    assert sources.preserve_other_coverage(original, rendered, {1}) == original
    changed = sources.preserve_other_coverage(original, rendered.replace("'3'", "'4'"), {1})
    assert "value: '4'" in changed
    assert "value: '2'" in changed
    assert "value: '99'" not in changed
