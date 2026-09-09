"""Synthetic controls for the direct exact sixth-site feasibility instrument."""

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from types import SimpleNamespace
from typing import cast

import pytest

import devtools.wall_owner_sixth_site_feasibility as feasibility
from cases.n11_five_dot_cover.independent_union import (
    Direction,
    FrozenInput,
    UnionMeasure,
    full_direction_manifest,
)
from devtools.owner_footprints import ANGLE_LIMIT, CORE_SIDE, OUTER_SIDE, Point, Polygon
from devtools.wall_owner_containment import CLASS_IDS, WallClass, WallInput
from devtools.wall_owner_selected_cover import (
    DirectionResult,
    SelectedCoverEvidence,
    SelectedEscape,
    select_four_footprints,
)
from devtools.wall_owner_sixth_site_screen import SixDotEscapeEvidence

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
        feasibility.RETAINED_ENDPOINT_BLOB,
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


def _axis_source() -> FrozenInput:
    source = _source()
    return replace(
        source,
        directions=tuple(Direction(f"axis-{index:03d}", F(1), F(0)) for index in range(361)),
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


def _selected(source: FrozenInput, wall: WallInput, centre: Point) -> SelectedCoverEvidence:
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


def _six_dot(source: FrozenInput, centre: Point) -> SixDotEscapeEvidence:
    return SixDotEscapeEvidence(
        "six.json",
        SOURCE,
        "six-blob",
        "six-source",
        DirectionResult(0, source.directions[0].label, F(1), F(1, 2), F(1, 2), 42),
        SelectedEscape(0, source.directions[0].label, centre),
    )


def _disable_authority_replays(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        feasibility, "replay_selected_cover_evidence", lambda *_args, **_kwargs: None
    )
    monkeypatch.setattr(feasibility, "replay_six_dot_escape", lambda *_args, **_kwargs: None)


def _component_around(centre: Point) -> Polygon:
    delta = F(1, 100)
    return _rectangle(
        centre[0] - delta,
        centre[1] - delta,
        centre[0] + delta,
        centre[1] + delta,
    )


def test_support_uses_all_vertices_with_correct_minimum_maximum_signs() -> None:
    h = F(1)
    direction = feasibility.Direction("axis", F(1), F(0))
    component = _rectangle(F(0), F(0), h, h / 2)
    constraints, u_min, u_max, v_min, v_max = feasibility.support_constraints(
        (component,), direction, h
    )
    assert tuple((item.name, item.a, item.b, item.bound) for item in constraints) == (
        ("u-lower", F(-1), F(0), F(0)),
        ("u-upper", F(1), F(0), h),
        ("v-lower", F(0), F(-1), h / 2),
        ("v-upper", F(0), F(1), h),
    )
    assert u_min is not None
    assert u_min.value == 0
    assert u_max is not None
    assert u_max.value == h
    assert v_min is not None
    assert v_min.value == 0
    assert v_max is not None
    assert v_max.value == h / 2


def test_oblique_support_has_identical_axis_coordinate_bounds() -> None:
    h = F(1)
    direction = feasibility.Direction("oblique", F(3, 5), F(4, 5))
    u = (direction.cosine, direction.sine)
    v = (-direction.sine, direction.cosine)

    def world(a: Fraction, b: Fraction) -> Point:
        return a * u[0] + b * v[0], a * u[1] + b * v[1]

    component = tuple(
        world(a, b) for a, b in ((F(0), F(0)), (h, F(0)), (h, h / 2), (F(0), h / 2))
    )
    constraints, *_ = feasibility.support_constraints((component,), direction, h)
    assert tuple(item.bound for item in constraints) == (F(0), h, h / 2, h)
    assert all(item.value(world(h / 2, h / 4)) <= item.bound for item in constraints)


def test_extrema_may_come_from_different_components() -> None:
    direction = feasibility.Direction("axis", F(1), F(0))
    components = (
        _rectangle(F(-3), F(0), F(-2), F(1)),
        _rectangle(F(4), F(-5), F(5), F(-4)),
    )
    _, u_min, u_max, v_min, v_max = feasibility.support_constraints(
        components, direction, F(10)
    )
    assert u_min is not None
    assert u_min.component_index == 0
    assert u_max is not None
    assert u_max.component_index == 1
    assert v_min is not None
    assert v_min.component_index == 1
    assert v_max is not None
    assert v_max.component_index == 0


def test_empty_domain_is_vacuous_and_degenerate_clips_are_retained() -> None:
    direction = feasibility.Direction("axis", F(1), F(0))
    constraints, *attainers = feasibility.support_constraints((), direction, F(1))
    assert constraints == ()
    assert attainers == [None, None, None, None]

    square = _rectangle(F(0), F(0), F(2), F(2))
    segment = feasibility.clip_constraints(
        square,
        (
            feasibility.HalfPlane("u-upper", F(1), F(0), F(1)),
            feasibility.HalfPlane("u-lower", F(-1), F(0), F(-1)),
        ),
    )
    assert set(segment) == {(F(1), F(0)), (F(1), F(2))}
    point = feasibility.clip_constraints(
        segment, (feasibility.HalfPlane("v-upper", F(0), F(1), F(0)),)
    )
    assert point == ((F(1), F(0)),)
    assert (
        feasibility.clip_constraints(
            point, (feasibility.HalfPlane("v-upper", F(0), F(1), F(-1)),)
        )
        == ()
    )


def test_empty_first_prefix_is_complete_without_confirmation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _axis_source(), _wall()
    selected = _selected(source, wall, (F(2), F(2)))
    _disable_authority_replays(monkeypatch)
    far_component = _rectangle(F(0), F(0), F(1, 100), F(1, 100))
    monkeypatch.setattr(
        feasibility,
        "vertical_decompose",
        lambda *_args: SimpleNamespace(components=(far_component,)),
    )
    monkeypatch.setattr(
        feasibility,
        "measure_direction",
        lambda *_args, **_kwargs: pytest.fail("empty support prefix must not confirm"),
    )
    result = feasibility.run_sixth_site_feasibility(
        source, wall, selected, _six_dot(source, (F(2), F(2)))
    )
    assert result.status == "complete"
    assert result.outcome == "empty"
    assert len(result.supports) == 1
    assert result.final_region == ()
    assert result.confirmation == ()


def test_full_support_candidate_visits_all_directions_and_uses_six_sites(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _axis_source(), _wall()
    first_centre = (F(2), F(2))
    second_centre = (F(9, 4), F(2))
    candidate = (F(17, 8), F(2))
    selected = _selected(source, wall, first_centre)
    _disable_authority_replays(monkeypatch)
    component = _component_around(candidate)
    obstacle_counts: list[int] = []
    dot_counts: list[int] = []
    checkpoints: list[int] = []

    def decompose(_container: Polygon, obstacles: tuple[Polygon, ...]) -> SimpleNamespace:
        obstacle_counts.append(len(obstacles))
        return SimpleNamespace(components=(component,))

    def measure(
        received: FrozenInput,
        _direction: object,
        *,
        max_subsets: int,
        deadline: float,
    ) -> UnionMeasure:
        assert max_subsets == 1023
        assert deadline > 0
        dot_counts.append(len(received.dots))
        assert received.dots == (*source.dots, candidate)
        assert received.footprints == selected.selected_footprints
        return UnionMeasure(F(1), F(1), 12)

    monkeypatch.setattr(feasibility, "vertical_decompose", decompose)
    monkeypatch.setattr(feasibility, "measure_direction", measure)
    result = feasibility.run_sixth_site_feasibility(
        source,
        wall,
        selected,
        _six_dot(source, second_centre),
        checkpoint=lambda snapshot: checkpoints.append(len(snapshot.supports)),
    )
    assert result.status == "complete"
    assert result.outcome == "covered"
    assert result.candidate == candidate
    assert len(result.supports) == 361
    assert len(result.confirmation) == 361
    assert tuple(row.index for row in result.supports) == tuple(range(361))
    assert tuple(row.label for row in result.supports) == tuple(
        direction.label for direction in source.directions
    )
    assert tuple(row.index for row in result.confirmation) == tuple(range(361))
    assert tuple(row.label for row in result.confirmation) == tuple(
        direction.label for direction in source.directions
    )
    assert obstacle_counts == [9] * 361
    assert dot_counts == [6] * 361
    assert checkpoints == list(range(1, 362))


def test_positive_confirmation_deficit_is_invalid_and_replayed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _axis_source(), _wall()
    centre = (F(2), F(2))
    selected = _selected(source, wall, centre)
    _disable_authority_replays(monkeypatch)
    component = _component_around(centre)
    monkeypatch.setattr(
        feasibility,
        "vertical_decompose",
        lambda *_args: SimpleNamespace(components=(component,)),
    )
    monkeypatch.setattr(
        feasibility,
        "measure_direction",
        lambda *_args, **_kwargs: UnionMeasure(F(3, 4), F(1), 17),
    )
    conflicting = SelectedEscape(0, source.directions[0].label, (F(3), F(3)))
    replayed: list[SelectedEscape] = []
    monkeypatch.setattr(
        feasibility, "extract_six_dot_escape", lambda *_args, **_kwargs: conflicting
    )
    monkeypatch.setattr(
        feasibility,
        "replay_six_dot_escape",
        lambda escape, *_args, **_kwargs: replayed.append(cast(SelectedEscape, escape)),
    )
    result = feasibility.run_sixth_site_feasibility(
        source, wall, selected, _six_dot(source, centre)
    )
    assert result.status == "invalid"
    assert result.outcome == "inconsistent"
    assert len(result.supports) == 361
    assert len(result.confirmation) == 1
    assert result.conflicting_escape == conflicting
    assert replayed[-1] == conflicting


def test_unreplayable_positive_deficit_retains_support_and_union_evidence(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _axis_source(), _wall()
    centre = (F(2), F(2))
    selected = _selected(source, wall, centre)
    _disable_authority_replays(monkeypatch)
    component = _component_around(centre)
    monkeypatch.setattr(
        feasibility,
        "vertical_decompose",
        lambda *_args: SimpleNamespace(components=(component,)),
    )
    monkeypatch.setattr(
        feasibility,
        "measure_direction",
        lambda *_args, **_kwargs: UnionMeasure(F(3, 4), F(1), 17),
    )

    def fail_extract(*_args: object, **_kwargs: object) -> SelectedEscape:
        raise feasibility.SixDotCoverError("synthetic missing witness")

    monkeypatch.setattr(feasibility, "extract_six_dot_escape", fail_extract)
    result = feasibility.run_sixth_site_feasibility(
        source, wall, selected, _six_dot(source, centre)
    )
    assert result.status == "invalid"
    assert result.outcome == "inconsistent"
    assert len(result.supports) == 361
    assert len(result.confirmation) == 1
    assert result.conflicting_escape is None
    assert result.error is not None
    assert "synthetic missing witness" in result.error


def test_deadline_after_decomposition_retains_only_completed_prefix(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _axis_source(), _wall()
    centre = (F(2), F(2))
    selected = _selected(source, wall, centre)
    _disable_authority_replays(monkeypatch)
    component = _component_around(centre)
    monkeypatch.setattr(
        feasibility,
        "vertical_decompose",
        lambda *_args: SimpleNamespace(components=(component,)),
    )
    values = iter((0.0, 0.0, 0.0, 0.0, 2.0, 2.0))
    monkeypatch.setattr(feasibility.time, "perf_counter", lambda: next(values, 2.0))
    result = feasibility.run_sixth_site_feasibility(
        source,
        wall,
        selected,
        _six_dot(source, centre),
        deadline_seconds=1,
    )
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert result.initial_region
    assert result.supports == ()
    assert result.error == "sixth-site feasibility deadline reached after decomposition"


def test_final_confirmation_deadline_retains_complete_support_and_union_rows(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _axis_source(), _wall()
    centre = (F(2), F(2))
    selected = _selected(source, wall, centre)
    _disable_authority_replays(monkeypatch)
    component = _component_around(centre)
    monkeypatch.setattr(
        feasibility,
        "vertical_decompose",
        lambda *_args: SimpleNamespace(components=(component,)),
    )
    expired = False
    deadlines: list[float] = []

    def clock() -> float:
        return 2.0 if expired else 0.0

    def measure(
        _source: FrozenInput,
        direction: Direction,
        *,
        max_subsets: int,
        deadline: float,
    ) -> UnionMeasure:
        nonlocal expired
        assert max_subsets == 1023
        assert direction.label == source.directions[len(deadlines)].label
        deadlines.append(deadline)
        if len(deadlines) == 361:
            expired = True
        return UnionMeasure(F(1), F(1), 12)

    monkeypatch.setattr(feasibility.time, "perf_counter", clock)
    monkeypatch.setattr(feasibility, "measure_direction", measure)
    result = feasibility.run_sixth_site_feasibility(
        source,
        wall,
        selected,
        _six_dot(source, centre),
        deadline_seconds=1,
    )
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert len(result.supports) == 361
    assert len(result.confirmation) == 361
    assert set(deadlines) == {1.0}
    assert result.error == "sixth-site feasibility deadline reached after confirmation"
