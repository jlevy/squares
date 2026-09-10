"""Synthetic controls for the exact two-escape sixth-site screen."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from typing import cast

import pytest

import devtools.wall_owner_sixth_site_screen as screen
from cases.n11_five_dot_cover.independent_union import (
    Direction,
    FrozenInput,
    full_direction_manifest,
)
from devtools.owner_footprints import ANGLE_LIMIT, CORE_SIDE, OUTER_SIDE, Polygon
from devtools.wall_owner_containment import CLASS_IDS, WallClass, WallInput
from devtools.wall_owner_selected_cover import (
    DirectionResult,
    SelectedCoverEvidence,
    SelectedEscape,
    select_four_footprints,
)
from devtools.wall_owner_six_dot_cover import SixDotCoverResult, result_document

F = Fraction
SOURCE = "a" * 40


def _rectangle(x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction) -> Polygon:
    return ((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def _source() -> FrozenInput:
    directions = tuple(item.direction for item in full_direction_manifest(ANGLE_LIMIT, 180))
    patch = _rectangle(F(0), F(0), F(1, 10), F(1, 10))
    return FrozenInput(
        "endpoint.json",
        SOURCE,
        screen.RETAINED_ENDPOINT_BLOB,
        OUTER_SIDE,
        CORE_SIDE,
        ANGLE_LIMIT,
        180,
        (patch,) * 4,
        (
            (F(73, 75), F(187, 90)),
            (F(793, 450), F(43, 15)),
            (F(48, 25), F(48, 25)),
            (F(187, 90), F(73, 75)),
            (F(43, 15), F(793, 450)),
        ),
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
    return WallInput("wall.json", SOURCE, "wall-blob", "constructor", classes)


def _selected(
    source: FrozenInput, wall: WallInput, centre: tuple[Fraction, Fraction]
) -> SelectedCoverEvidence:
    direction = DirectionResult(0, source.directions[0].label, F(1), F(1, 2), F(1, 2), 41)
    return SelectedCoverEvidence(
        "selected.json",
        SOURCE,
        "selected-blob",
        "selected-source",
        direction,
        SelectedEscape(0, source.directions[0].label, centre),
        select_four_footprints(source, wall),
    )


def _six_dot(
    source: FrozenInput, centre: tuple[Fraction, Fraction]
) -> screen.SixDotEscapeEvidence:
    return screen.SixDotEscapeEvidence(
        "six.json",
        SOURCE,
        "six-blob",
        SOURCE,
        DirectionResult(0, source.directions[0].label, F(1), F(1, 2), F(1, 2), 42),
        SelectedEscape(0, source.directions[0].label, centre),
    )


def _disable_replays(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        screen, "replay_selected_cover_evidence", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(screen, "replay_six_dot_escape", lambda *_args, **_kwargs: None)


@pytest.mark.parametrize(
    ("offset", "dimension", "vertex_count"),
    [
        ((F(1, 4), F(0)), 2, 4),
        ((CORE_SIDE, F(0)), 1, 2),
        ((CORE_SIDE, CORE_SIDE), 0, 1),
    ],
)
def test_nonempty_intersections_preserve_area_segment_and_point(
    monkeypatch: pytest.MonkeyPatch,
    offset: tuple[Fraction, Fraction],
    dimension: int,
    vertex_count: int,
) -> None:
    source, wall = _source(), _wall()
    first_centre = (F(3, 2), F(3, 2))
    second_centre = (first_centre[0] + offset[0], first_centre[1] + offset[1])
    selected = _selected(source, wall, first_centre)
    _disable_replays(monkeypatch)
    result = screen.run_sixth_site_screen(
        source, wall, selected, _six_dot(source, second_centre)
    )
    assert result.status == "complete"
    assert result.outcome == "nonempty"
    assert result.dimension == dimension
    assert result.intersection is not None
    assert len(result.intersection) == vertex_count
    assert result.candidate is not None
    assert result.first_core is not None
    assert result.second_core is not None
    assert screen.point_in_closed_convex_polygon(result.candidate, result.first_core)
    assert screen.point_in_closed_convex_polygon(result.candidate, result.second_core)
    assert result.separator is None


def test_separated_cores_require_independent_positive_sat(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    selected = _selected(source, wall, (F(1), F(1)))
    _disable_replays(monkeypatch)
    result = screen.run_sixth_site_screen(
        source, wall, selected, _six_dot(source, (F(3), F(3)))
    )
    assert result.status == "complete"
    assert result.outcome == "empty"
    assert result.intersection == ()
    assert result.candidate is None
    assert result.separator is not None
    assert result.separator.gap > 0


def test_replays_use_original_d_then_augmented_d6(monkeypatch: pytest.MonkeyPatch) -> None:
    source, wall = _source(), _wall()
    selected = _selected(source, wall, (F(3, 2), F(3, 2)))
    six_dot = _six_dot(source, (F(7, 4), F(3, 2)))
    calls: list[tuple[str, int]] = []

    def original(
        evidence: SelectedCoverEvidence, *, source: FrozenInput, deadline: float
    ) -> None:
        assert evidence is selected
        assert deadline > 0
        calls.append(("exp149", len(source.dots)))

    def augmented(escape: SelectedEscape, received: FrozenInput, *, deadline: float) -> None:
        assert escape is six_dot.escape
        assert received.dots == (*source.dots, selected.escape.centre)
        assert deadline > 0
        calls.append(("exp151", len(received.dots)))

    monkeypatch.setattr(screen, "replay_selected_cover_evidence", original)
    monkeypatch.setattr(screen, "replay_six_dot_escape", augmented)
    result = screen.run_sixth_site_screen(source, wall, selected, six_dot)
    assert result.status == "complete"
    assert calls == [("exp149", 5), ("exp151", 6)]


def test_distinct_oblique_escape_direction_builds_an_eight_vertex_intersection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    oblique = Direction("owner-001", F(3, 5), F(4, 5))
    source = replace(source, directions=(source.directions[0], oblique, *source.directions[2:]))
    centre = (F(2), F(2))
    selected = _selected(source, wall, centre)
    six_dot = screen.SixDotEscapeEvidence(
        "six.json",
        SOURCE,
        "six-blob",
        SOURCE,
        DirectionResult(1, oblique.label, F(1), F(1, 2), F(1, 2), 42),
        SelectedEscape(1, oblique.label, centre),
    )
    _disable_replays(monkeypatch)
    result = screen.run_sixth_site_screen(source, wall, selected, six_dot)
    assert result.status == "complete"
    assert result.outcome == "nonempty"
    assert result.intersection is not None
    assert len(result.intersection) == 8
    assert result.candidate == centre


def test_deadline_during_replay_is_partial(monkeypatch: pytest.MonkeyPatch) -> None:
    source, wall = _source(), _wall()
    selected = _selected(source, wall, (F(3, 2), F(3, 2)))
    monkeypatch.setattr(
        screen, "replay_selected_cover_evidence", lambda *_args, **_kwargs: None
    )

    def expire(*_args: object, **_kwargs: object) -> None:
        raise screen.DeadlineError("synthetic replay deadline")

    monkeypatch.setattr(screen, "replay_six_dot_escape", expire)
    result = screen.run_sixth_site_screen(
        source, wall, selected, _six_dot(source, (F(2), F(2)))
    )
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert result.first_core is None
    assert result.error == "synthetic replay deadline"


def test_deadline_after_geometry_retains_the_exact_intersection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    selected = _selected(source, wall, (F(3, 2), F(3, 2)))
    _disable_replays(monkeypatch)
    calls = 0

    def clock() -> float:
        nonlocal calls
        calls += 1
        return 0.0 if calls == 1 else 2.0

    monkeypatch.setattr(screen.time, "perf_counter", clock)
    result = screen.run_sixth_site_screen(
        source,
        wall,
        selected,
        _six_dot(source, (F(7, 4), F(3, 2))),
        deadline_seconds=1,
    )
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert result.first_core is not None
    assert result.second_core is not None
    assert result.intersection
    assert result.candidate is not None
    assert result.error == "sixth-site screen deadline reached after geometry"


def test_six_dot_receipt_parser_binds_sites_sources_and_first_deficit() -> None:
    source, wall = _source(), _wall()
    selected = _selected(source, wall, (F(3, 2), F(3, 2)))
    augmented = screen.augment_with_selected_escape(source, wall, selected)
    rows = tuple(
        DirectionResult(
            index,
            source.directions[index].label,
            F(1),
            F(1) if index < 6 else F(3, 4),
            F(0) if index < 6 else F(1, 4),
            45 if index < 6 else 42,
        )
        for index in range(7)
    )
    escape = SelectedEscape(6, source.directions[6].label, (F(5, 2), F(5, 2)))
    result = SixDotCoverResult(
        "complete",
        "uncovered",
        rows,
        escape,
        augmented.footprints,
        augmented.dots,
        1.0,
    )
    document = result_document(
        result,
        source=source,
        wall=wall,
        selected=selected,
        implementation_revision=SOURCE,
        process_seconds=2.0,
    )
    parsed = screen.parse_six_dot_escape_evidence(
        document,
        source_path="six.json",
        git_commit="receipt-commit",
        git_blob="six-blob",
        expected_source=SOURCE,
        source=source,
        wall=wall,
        selected=selected,
    )
    assert parsed.escape == escape
    assert parsed.direction == rows[-1]
    changed_sites = dict(cast(dict[str, object], document["sites"]))
    changed_sites["added"] = ["0", "0"]
    changed = dict(document)
    changed["sites"] = changed_sites
    with pytest.raises(screen.SixthSiteScreenError, match="changes the six fixed sites"):
        screen.parse_six_dot_escape_evidence(
            changed,
            source_path="six.json",
            git_commit="receipt-commit",
            git_blob="six-blob",
            expected_source=SOURCE,
            source=source,
            wall=wall,
            selected=selected,
        )


def test_result_receipt_retains_canonical_candidate_and_sources(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    selected = _selected(source, wall, (F(3, 2), F(3, 2)))
    six_dot = _six_dot(source, (F(7, 4), F(3, 2)))
    _disable_replays(monkeypatch)
    result = screen.run_sixth_site_screen(source, wall, selected, six_dot)
    document = screen.result_document(
        result,
        source=source,
        wall=wall,
        selected=selected,
        six_dot=six_dot,
        implementation_revision="screen-source",
        process_seconds=1.0,
    )
    intersection = document["intersection"]
    assert isinstance(intersection, dict)
    assert intersection["dimension"] == 2
    assert result.candidate is not None
    assert intersection["canonical_site"] == [
        str(result.candidate[0]),
        str(result.candidate[1]),
    ]
    sources = document["sources"]
    assert isinstance(sources, dict)
    assert sources["six_dot_cover"] == {
        "path": "six.json",
        "git_commit": SOURCE,
        "git_blob": "six-blob",
        "implementation_revision": SOURCE,
    }
