"""Synthetic controls for the fixed D-plus-exp149 six-dot cover wrapper."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction

import pytest

import devtools.wall_owner_six_dot_cover as six_dot
from cases.n11_five_dot_cover.independent_union import (
    AuditError,
    DeadlineError,
    FrozenInput,
    UnionMeasure,
    full_direction_manifest,
    measure_direction,
)
from devtools.owner_footprints import ANGLE_LIMIT, CORE_SIDE, OUTER_SIDE, Polygon
from devtools.wall_owner_containment import CLASS_IDS, WallClass, WallInput
from devtools.wall_owner_selected_cover import (
    DirectionResult,
    SelectedCoverEvidence,
    SelectedEscape,
    select_four_footprints,
)

F = Fraction


def _rectangle(x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction) -> Polygon:
    return ((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def _source() -> FrozenInput:
    directions = tuple(item.direction for item in full_direction_manifest(ANGLE_LIMIT, 180))
    patch = _rectangle(F(0), F(0), F(1, 10), F(1, 10))
    dots = (
        (F(73, 75), F(187, 90)),
        (F(793, 450), F(43, 15)),
        (F(48, 25), F(48, 25)),
        (F(187, 90), F(73, 75)),
        (F(43, 15), F(793, 450)),
    )
    return FrozenInput(
        "endpoint.json",
        "endpoint-revision",
        six_dot.RETAINED_ENDPOINT_BLOB,
        OUTER_SIDE,
        CORE_SIDE,
        ANGLE_LIMIT,
        180,
        (patch,) * 4,
        dots,
        F(1),
        F(5),
        directions,
    )


def _wall() -> WallInput:
    classes = tuple(
        WallClass(
            class_id,
            _rectangle(F(0), F(0), F(index + 1, 100), F(1, 10)),
            "possible",
            _rectangle(F(0), F(0), F(index + 1, 100), F(1, 10)),
        )
        for index, class_id in enumerate(CLASS_IDS)
    )
    return WallInput("wall.json", "wall-revision", "wall-blob", "constructor", classes)


def _evidence(
    source: FrozenInput,
    wall: WallInput,
    *,
    centre: tuple[Fraction, Fraction] = (F(2), F(2)),
) -> SelectedCoverEvidence:
    footprints = select_four_footprints(source, wall)
    direction = DirectionResult(0, source.directions[0].label, F(1), F(1, 2), F(1, 2), 41)
    return SelectedCoverEvidence(
        "selected.json",
        "selected-receipt-commit",
        "selected-blob",
        "selected-source",
        direction,
        SelectedEscape(0, source.directions[0].label, centre),
        footprints,
    )


def test_ten_obstacle_union_requires_full_1023_guard() -> None:
    source, wall = _source(), _wall()
    augmented = six_dot.augment_with_selected_escape(source, wall, _evidence(source, wall))
    direction = augmented.directions[0]
    measure = measure_direction(augmented, direction, max_subsets=1023, deadline=None)
    assert F(0) <= measure.covered_area <= measure.container_area
    with pytest.raises(AuditError, match="subset count exceeds"):
        measure_direction(augmented, direction, max_subsets=511, deadline=None)


def test_first_deficit_uses_original_authority_and_augmented_replays(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    evidence = _evidence(source, wall)
    seen: list[tuple[str, int]] = []

    def authority(
        received: SelectedCoverEvidence, *, source: FrozenInput, deadline: float
    ) -> None:
        assert received is evidence
        assert deadline > 0
        seen.append(("authority", len(source.dots)))

    def deficit(
        received: FrozenInput, _direction: object, *, max_subsets: int, deadline: float
    ) -> UnionMeasure:
        assert max_subsets == 1023
        assert deadline > 0
        assert received.dots[:5] == source.dots
        assert received.dots[5] == evidence.escape.centre
        seen.append(("union", len(received.dots)))
        return UnionMeasure(F(0), F(1), 0)

    witness = SelectedEscape(0, source.directions[0].label, (F(3), F(3)))

    def extract(received: FrozenInput, index: int, *, deadline: float) -> SelectedEscape:
        seen.append(("extract", len(received.dots)))
        assert index == 0
        assert deadline > 0
        return witness

    def replay(escape: SelectedEscape, received: FrozenInput, *, deadline: float) -> None:
        assert escape is witness
        assert deadline > 0
        seen.append(("replay", len(received.dots)))

    monkeypatch.setattr(six_dot, "replay_selected_cover_evidence", authority)
    monkeypatch.setattr(six_dot, "measure_direction", deficit)
    monkeypatch.setattr(six_dot, "extract_six_dot_escape", extract)
    monkeypatch.setattr(six_dot, "replay_six_dot_escape", replay)
    result = six_dot.run_six_dot_cover(source, wall, evidence, deadline_seconds=30)
    assert result.status == "complete"
    assert result.outcome == "uncovered"
    assert len(result.directions) == 1
    assert seen == [
        ("authority", 5),
        ("union", 6),
        ("extract", 6),
        ("replay", 6),
    ]


def test_sixth_site_rejects_the_saved_centre_as_an_escape() -> None:
    source, wall = _source(), _wall()
    evidence = _evidence(source, wall, centre=(F(3), F(3)))
    direction = source.directions[evidence.escape.orientation_index]
    assert six_dot.strict_dot_free(
        evidence.escape.centre,
        direction,
        outer_side=source.outer_side,
        core_side=source.core_side,
        dots=source.dots,
    )
    assert all(
        six_dot.core_disjoint_from_polygon(
            evidence.escape.centre, direction, source.core_side, polygon
        )
        for polygon in evidence.selected_footprints
    )
    augmented = six_dot.augment_with_selected_escape(source, wall, evidence)
    assert not six_dot.is_strict_six_dot_escape(
        evidence.escape.centre, augmented, evidence.escape.orientation_index
    )
    with pytest.raises(six_dot.SixDotCoverError, match="strict physical replay"):
        six_dot.replay_six_dot_escape(evidence.escape, augmented, deadline=float("inf"))


def test_augmented_order_and_receipt_bind_all_sources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    evidence = _evidence(source, wall)
    monkeypatch.setattr(
        six_dot, "replay_selected_cover_evidence", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        six_dot,
        "measure_direction",
        lambda *_args, **_kwargs: UnionMeasure(F(1), F(1), 1),
    )
    result = six_dot.run_six_dot_cover(source, wall, evidence, deadline_seconds=30)
    assert result.status == "complete"
    assert result.outcome == "covered"
    assert tuple(row.index for row in result.directions) == tuple(range(361))
    assert tuple(row.label for row in result.directions) == tuple(
        direction.label for direction in source.directions
    )
    assert result.dots == (*source.dots, evidence.escape.centre)
    receipt = six_dot.result_document(
        result,
        source=source,
        wall=wall,
        selected=evidence,
        implementation_revision="six-dot-source",
        process_seconds=1.0,
    )
    assert receipt["sites"] == {
        "original": [[str(x), str(y)] for x, y in source.dots],
        "added": [str(evidence.escape.centre[0]), str(evidence.escape.centre[1])],
        "augmented": [[str(x), str(y)] for x, y in result.dots],
    }
    sources = receipt["sources"]
    assert isinstance(sources, dict)
    assert sources["selected_cover"] == {
        "path": "selected.json",
        "git_commit": "selected-receipt-commit",
        "git_blob": "selected-blob",
        "implementation_revision": "selected-source",
    }


def test_duplicate_saved_site_is_refused() -> None:
    source, wall = _source(), _wall()
    evidence = _evidence(source, wall, centre=source.dots[0])
    with pytest.raises(six_dot.SixDotCoverError, match="distinct sixth site"):
        six_dot.augment_with_selected_escape(source, wall, evidence)


def test_expiry_after_final_direction_is_partial(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    evidence = _evidence(source, wall)
    calls = 0

    def clock() -> float:
        nonlocal calls
        calls += 1
        return 0.0 if calls <= 362 else 2.0

    monkeypatch.setattr(six_dot.time, "perf_counter", clock)
    monkeypatch.setattr(
        six_dot, "replay_selected_cover_evidence", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        six_dot,
        "measure_direction",
        lambda *_args, **_kwargs: UnionMeasure(F(1), F(1), 1),
    )
    result = six_dot.run_six_dot_cover(source, wall, evidence, deadline_seconds=1)
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert len(result.directions) == 361
    assert result.error == "six-dot deadline reached after the final direction"


def test_expiry_during_escape_extraction_retains_first_deficit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    evidence = _evidence(source, wall)
    monkeypatch.setattr(
        six_dot, "replay_selected_cover_evidence", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(
        six_dot,
        "measure_direction",
        lambda *_args, **_kwargs: UnionMeasure(F(0), F(1), 1),
    )

    def expire(*_args: object, **_kwargs: object) -> SelectedEscape:
        raise DeadlineError("synthetic extraction deadline")

    monkeypatch.setattr(six_dot, "extract_six_dot_escape", expire)
    result = six_dot.run_six_dot_cover(source, wall, evidence, deadline_seconds=30)
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert len(result.directions) == 1
    assert result.directions[0].uncovered_area == F(1)
    assert result.escape is None
    assert result.error == "synthetic extraction deadline"


def test_changed_selected_footprints_are_refused() -> None:
    source, wall = _source(), _wall()
    evidence = _evidence(source, wall)
    changed = replace(evidence, selected_footprints=evidence.selected_footprints[::-1])
    with pytest.raises(six_dot.SixDotCoverError, match="changes the four wall footprints"):
        six_dot.augment_with_selected_escape(source, wall, changed)
