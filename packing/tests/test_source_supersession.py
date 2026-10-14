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


def test_a_lane_is_held_by_a_later_layer_only_when_foreign_and_lower() -> None:
    """The shared predicate the earlier ceiling layers ask with their own ids: a lane
    citing another layer's evidence below the bound they would write is not theirs to
    write over; their own evidence, or a foreign bound above theirs, is (review A2)."""
    own = {"value": "2", "exact_form": "2", "evidence": ["E-own"]}
    held = sources.verified_lane_held_by_later_layer
    assert held(
        {"value": "1.9", "exact_form": "19/10", "evidence": ["E-later"]}, ["E-own"], own
    )
    assert held(
        {"value": "1.9", "exact_form": "19/10", "evidence": ["E-own", "E-later"]},
        ["E-own"],
        own,
    )
    assert not held(
        {"value": "1.9", "exact_form": "19/10", "evidence": ["E-own"]}, ["E-own"], own
    )
    assert not held({"value": "3", "exact_form": "3", "evidence": ["E-grid"]}, ["E-own"], own)
    assert not held({"value": "2", "exact_form": "2", "evidence": ["E-grid"]}, ["E-own"], own)


def _with_lane(n: int, lane: dict[str, object]) -> tuple[str, str]:
    """A committed record with its verified upper lane replaced, and its front matter."""
    from devtools.apply_upper_bound_packets import set_block  # noqa: PLC0415

    text = (Path(sources.COVERAGE).parent / f"n-{n:03d}.md").read_text(encoding="utf-8")
    _, front, body = text.split("---\n", 2)
    front = set_block(front, "verified_upper_bound", lane)
    return f"---\n{front}---\n{body}", front


def _later_lane(exact_form: str, value: str) -> dict[str, object]:
    return {"value": value, "exact_form": exact_form, "evidence": ["E-a-later-layer"]}


def test_the_t101_layer_leaves_a_lane_any_later_layer_holds_below_it() -> None:
    """Neither earlier layer names a later one: a lane an unnamed later layer holds at
    T-155's exact side is left alone, and one above the layer's own bound is not (A2)."""
    from devtools import apply_exact_ceilings as t101  # noqa: PLC0415
    from devtools import register_regularized_bounds as registered  # noqa: PLC0415

    row = registered.committed()[28]
    below, front = _with_lane(28, _later_lane(row["side"], row["value"]))
    assert t101.later_ceiling(28, front)
    assert t101.apply_case(28, below) == below
    _above, front = _with_lane(28, _later_lane("6", "6"))
    assert not t101.later_ceiling(28, front)


def test_the_catalogue_layer_leaves_a_lane_any_later_layer_holds_below_it() -> None:
    from devtools import catalogue_upper_bounds as catalogue  # noqa: PLC0415
    from devtools import register_regularized_bounds as registered  # noqa: PLC0415

    row = registered.committed()[83]
    below, _front = _with_lane(83, _later_lane(row["side"], row["value"]))
    assert catalogue.apply_case(83, below) == below
    above, _front = _with_lane(83, _later_lane("10", "10"))
    written = catalogue.apply_case(83, above)
    assert "E-a-later-layer" not in written.split("---\n", 2)[1]
