"""Target-blind controls for the fixed two-attainer obstruction wrapper."""

# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

from dataclasses import replace
from fractions import Fraction
from types import SimpleNamespace
from typing import Literal, cast

import pytest

from cases.n11_five_dot_cover.independent_union import Direction, FrozenInput
from devtools import wall_owner_two_attainer_obstruction as obstruction
from devtools.owner_footprints import Point, Polygon
from devtools.wall_owner_containment import CLASS_IDS, WallClass, WallInput
from devtools.wall_owner_selected_cover import select_four_footprints
from devtools.wall_owner_sixth_site_screen import StrictSeparator

F = Fraction
SOURCE = "a" * 40
RIGHT_DEFAULT = (F(5), F(4))
LEFT_DEFAULT = (F(2), F(4))


def _rectangle(x0: Fraction, y0: Fraction, x1: Fraction, y1: Fraction) -> Polygon:
    return ((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def _source() -> FrozenInput:
    directions = [Direction(f"axis-{index:03d}", F(1), F(0)) for index in range(361)]
    directions[obstruction.LEFT_DIRECTION] = Direction("oblique-187", F(3, 5), F(4, 5))
    patch = _rectangle(F(0), F(0), F(1, 10), F(1, 10))
    return FrozenInput(
        "endpoint.json",
        SOURCE,
        obstruction.RETAINED_ENDPOINT_BLOB,
        F(8),
        F(2),
        F(1),
        180,
        (patch,) * 4,
        ((F(1), F(7)), (F(2), F(7)), (F(3), F(7)), (F(4), F(7)), (F(5), F(7))),
        F(1),
        F(5),
        tuple(directions),
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


def _attainer(
    source: FrozenInput,
    *,
    index: int,
    extremum: Literal["u_min", "u_max"],
    vertex: Point,
    vertex_index: int,
) -> obstruction.FixedAttainer:
    direction = source.directions[index]
    return obstruction.FixedAttainer(
        index,
        direction.label,
        extremum,
        1,
        0,
        vertex_index,
        vertex,
        direction.cosine * vertex[0] + direction.sine * vertex[1],
    )


def _evidence(
    source: FrozenInput,
    *,
    right: Point = RIGHT_DEFAULT,
    left: Point = LEFT_DEFAULT,
) -> obstruction.FeasibilityEvidence:
    return obstruction.FeasibilityEvidence(
        "exp153.json",
        SOURCE,
        "exp153-blob",
        SOURCE,
        188,
        _attainer(
            source,
            index=obstruction.RIGHT_DIRECTION,
            extremum="u_max",
            vertex=right,
            vertex_index=1,
        ),
        _attainer(
            source,
            index=obstruction.LEFT_DIRECTION,
            extremum="u_min",
            vertex=left,
            vertex_index=0,
        ),
    )


def _components() -> tuple[Polygon, Polygon]:
    right = ((F(5), F(3)), (F(5), F(4)), (F(4), F(4)), (F(4), F(3)))
    u, v = (F(3, 5), F(4, 5)), (F(-4, 5), F(3, 5))
    left_seed = (F(2), F(4))
    left = (
        left_seed,
        (left_seed[0] - v[0], left_seed[1] - v[1]),
        (left_seed[0] - v[0] + u[0], left_seed[1] - v[1] + u[1]),
        (left_seed[0] + u[0], left_seed[1] + u[1]),
    )
    return right, left


def _mock_components(monkeypatch: pytest.MonkeyPatch, source: FrozenInput) -> None:
    monkeypatch.setattr(obstruction, "OUTER_SIDE", F(8))
    monkeypatch.setattr(obstruction, "CORE_SIDE", F(2))
    right, left = _components()

    def component(
        received: FrozenInput, attainer: obstruction.FixedAttainer
    ) -> tuple[Polygon, Point]:
        assert received.dots == source.dots
        assert len(received.footprints) == 4
        polygon = right if attainer.direction_index == 0 else left
        return polygon, obstruction._mean(polygon)

    monkeypatch.setattr(obstruction, "_closure_component", component)


def test_positive_oblique_pair_uses_exact_margin_rule_and_original_d(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    _mock_components(monkeypatch, source)
    replayed: list[tuple[int, int, int]] = []

    def replay(received: FrozenInput, _centre: Point, index: int) -> bool:
        replayed.append((index, len(received.dots), len(received.footprints)))
        return True

    monkeypatch.setattr(obstruction, "_strict_escape", replay)
    result = obstruction.run_two_attainer_obstruction(source, wall, _evidence(source))
    assert result.status == "complete"
    assert result.outcome == "strict-obstruction"
    assert result.closure_x_gap == F(3, 5)
    assert result.movement_bound == F(6, 5)
    assert result.perturbation_coefficient == F(1, 4)
    assert result.strict_x_gap == F(3, 10)
    assert result.separator is not None
    assert result.separator.gap > 0
    assert replayed == [(0, 5, 4), (187, 5, 4)]
    assert obstruction._x_radius(source, 187) == F(7, 5)


def test_positive_oblique_pair_passes_independent_strict_replay(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    _mock_components(monkeypatch, source)
    result = obstruction.run_two_attainer_obstruction(source, wall, _evidence(source))
    assert result.status == "complete"
    assert result.outcome == "strict-obstruction"
    assert result.right is not None
    assert result.left is not None
    assert obstruction._strict_escape(source, result.right.centre, 0)
    assert obstruction._strict_escape(source, result.left.centre, 187)


def test_positive_movement_can_use_capped_half_coefficient(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    monkeypatch.setattr(obstruction, "OUTER_SIDE", F(8))
    monkeypatch.setattr(obstruction, "CORE_SIDE", F(2))
    right = ((F(5), F(4)), (F(49, 10), F(5)), (F(24, 5), F(3)))
    left = ((F(2), F(4)), (F(21, 10), F(3)), (F(11, 5), F(5)))

    def component(
        _source: FrozenInput, attainer: obstruction.FixedAttainer
    ) -> tuple[Polygon, Point]:
        polygon = right if attainer.direction_index == 0 else left
        return polygon, obstruction._mean(polygon)

    monkeypatch.setattr(obstruction, "_closure_component", component)
    monkeypatch.setattr(obstruction, "_strict_escape", lambda *_args: True)
    result = obstruction.run_two_attainer_obstruction(source, wall, _evidence(source))
    assert result.status == "complete"
    assert result.movement_bound == F(1, 5)
    assert result.perturbation_coefficient == F(1, 2)
    assert result.strict_x_gap == F(1, 2)


def test_zero_horizontal_movement_uses_half(monkeypatch: pytest.MonkeyPatch) -> None:
    source, wall = _source(), _wall()
    evidence = _evidence(source)
    monkeypatch.setattr(obstruction, "OUTER_SIDE", F(8))
    monkeypatch.setattr(obstruction, "CORE_SIDE", F(2))

    def component(
        _source: FrozenInput, attainer: obstruction.FixedAttainer
    ) -> tuple[Polygon, Point]:
        x, y = attainer.vertex
        mean = (x, y + 1)
        return ((x, y), (x + 1, y + 1), (x, y + 2), (x - 1, y + 1)), mean

    monkeypatch.setattr(obstruction, "_closure_component", component)
    monkeypatch.setattr(obstruction, "_strict_escape", lambda *_args: True)
    result = obstruction.run_two_attainer_obstruction(source, wall, evidence)
    assert result.status == "complete"
    assert result.movement_bound == 0
    assert result.perturbation_coefficient == F(1, 2)
    assert result.strict_x_gap == result.closure_x_gap


@pytest.mark.parametrize(
    ("right_x", "expected_sign"),
    [(F(22, 5), 0), (F(4), -1)],
)
def test_nonpositive_limit_gap_stops_without_search(
    monkeypatch: pytest.MonkeyPatch, right_x: Fraction, expected_sign: int
) -> None:
    source, wall = _source(), _wall()
    monkeypatch.setattr(obstruction, "OUTER_SIDE", F(8))
    monkeypatch.setattr(obstruction, "CORE_SIDE", F(2))

    def component(
        _source: FrozenInput, attainer: obstruction.FixedAttainer
    ) -> tuple[Polygon, Point]:
        x, y = attainer.vertex
        return ((x, y), (x + 1, y), (x, y + 1)), attainer.vertex

    monkeypatch.setattr(obstruction, "_closure_component", component)
    monkeypatch.setattr(
        obstruction,
        "_strict_escape",
        lambda *_args: pytest.fail("nonpositive gap must not perturb or replay"),
    )
    result = obstruction.run_two_attainer_obstruction(
        source, wall, _evidence(source, right=(right_x, F(4)))
    )
    assert result.status == "complete"
    assert result.outcome == "no-positive-closure-x-gap"
    assert result.closure_x_gap is not None
    assert (result.closure_x_gap > 0) - (result.closure_x_gap < 0) == expected_sign
    assert result.perturbation_coefficient is None


def test_reconstructed_attainer_requires_exact_component_vertex_and_extremum(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source = replace(_source(), footprints=select_four_footprints(_source(), _wall()))
    right = ((F(4), F(3)), (F(5), F(4)), (F(4), F(5)), (F(3), F(4)))
    captured_obstacles: list[int] = []

    def decompose(_container: Polygon, obstacles: tuple[Polygon, ...]) -> SimpleNamespace:
        captured_obstacles.append(len(obstacles))
        return SimpleNamespace(components=(right,))

    monkeypatch.setattr(obstruction, "vertical_decompose", decompose)
    component, mean = obstruction._closure_component(source, _evidence(source).right)
    assert component == right
    assert mean == (F(4), F(4))
    assert captured_obstacles == [9]
    changed = replace(_evidence(source).right, vertex_index=0)
    with pytest.raises(obstruction.TwoAttainerError, match="closure vertex"):
        obstruction._closure_component(source, changed)


def test_closed_dot_and_patch_tangencies_are_rejected() -> None:
    source = _source()
    centre = (F(2), F(4))
    dot_tangent = replace(source, footprints=(), dots=((F(3), F(4)),))
    assert not obstruction._strict_escape(dot_tangent, centre, 0)
    patch_tangent = replace(
        source,
        footprints=(_rectangle(F(3), F(7, 2), F(7, 2), F(9, 2)),),
        dots=((F(7), F(7)),),
    )
    assert not obstruction._strict_escape(patch_tangent, centre, 0)


def test_pre_replay_expiry_retains_unverified_candidates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    _mock_components(monkeypatch, source)
    expired = False
    original_interpolate = obstruction._interpolate
    calls = 0

    def interpolate(start: Point, end: Point, coefficient: Fraction) -> Point:
        nonlocal calls, expired
        calls += 1
        result = original_interpolate(start, end, coefficient)
        if calls == 2:
            expired = True
        return result

    monkeypatch.setattr(obstruction, "_interpolate", interpolate)
    monkeypatch.setattr(obstruction.time, "perf_counter", lambda: 2.0 if expired else 0.0)
    monkeypatch.setattr(
        obstruction,
        "_strict_escape",
        lambda *_args: pytest.fail("expired candidate must not replay"),
    )
    result = obstruction.run_two_attainer_obstruction(
        source, wall, _evidence(source), deadline_seconds=1
    )
    assert result.status == "partial"
    assert result.right is not None
    document = obstruction.result_document(
        result,
        source=source,
        wall=wall,
        feasibility=_evidence(source),
        implementation_revision=SOURCE,
        process_seconds=2.0,
    )
    assert cast(dict[str, object], document["summary"])["strict_escape_count"] == 0
    right_record = cast(dict[str, object], document["right_witness"])
    assert right_record["strict_replay_verified"] is False
    assert "nominal total mass at least 7" in cast(str, document["claim_limit"])
    assert "separately requires proof" in cast(str, document["banking_condition"])


def test_failed_replay_is_invalid_without_claiming_strict_witnesses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    _mock_components(monkeypatch, source)
    monkeypatch.setattr(obstruction, "_strict_escape", lambda *_args: False)
    result = obstruction.run_two_attainer_obstruction(source, wall, _evidence(source))
    assert result.status == "invalid"
    assert result.outcome == "invalid"
    document = obstruction.result_document(
        result,
        source=source,
        wall=wall,
        feasibility=_evidence(source),
        implementation_revision=SOURCE,
        process_seconds=1.0,
    )
    assert cast(dict[str, object], document["summary"])["strict_escape_count"] == 0


def test_expiry_after_successful_sat_retains_geometry_without_acceptance(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    source, wall = _source(), _wall()
    _mock_components(monkeypatch, source)
    monkeypatch.setattr(obstruction, "_strict_escape", lambda *_args: True)
    expired = False
    real_separator = obstruction.strict_separator

    def expire_after_sat(first: Polygon, second: Polygon) -> StrictSeparator | None:
        nonlocal expired
        result = real_separator(first, second)
        expired = True
        return result

    monkeypatch.setattr(obstruction, "strict_separator", expire_after_sat)
    monkeypatch.setattr(obstruction.time, "perf_counter", lambda: 2.0 if expired else 0.0)
    result = obstruction.run_two_attainer_obstruction(
        source, wall, _evidence(source), deadline_seconds=1
    )
    assert result.status == "partial"
    assert result.outcome == "incomplete"
    assert result.strict_x_gap == F(3, 10)
    assert result.separator is not None


def _receipt(source: FrozenInput, wall: WallInput) -> dict[str, object]:
    selected = select_four_footprints(source, wall)
    supports: list[dict[str, object]] = []
    evidence = _evidence(source)
    for index in range(188):
        direction = source.directions[index]
        extrema: dict[str, object] = {}
        if index == 0:
            extrema["u_max"] = {
                "component_index": 0,
                "vertex_index": 1,
                "vertex": [str(value) for value in evidence.right.vertex],
                "value": str(evidence.right.value),
                "semantics": "positive-area component closure vertex",
            }
        if index == 187:
            row = {
                "component_index": 0,
                "vertex_index": 0,
                "vertex": [str(value) for value in evidence.left.vertex],
                "value": str(evidence.left.value),
                "semantics": "positive-area component closure vertex",
            }
            extrema["u_min"] = row
            v = (-direction.sine, direction.cosine)
            extrema["v_max"] = {
                **row,
                "value": str(v[0] * evidence.left.vertex[0] + v[1] * evidence.left.vertex[1]),
            }
        supports.append(
            {
                "index": index,
                "label": direction.label,
                "u": [str(direction.cosine), str(direction.sine)],
                "v": [str(-direction.sine), str(direction.cosine)],
                "component_count": 1,
                "extrema": extrema,
                "resulting_region": [] if index == 187 else [["0", "0"]],
            }
        )
    return {
        "schema": "wall-owner-sixth-site-feasibility/v1",
        "status": "complete",
        "outcome": "refute-fixed-D-plus-one-site-family",
        "claim_limit": "the explicit tuple (0,0,0,7) under fixed D plus one site only",
        "sources": {
            "implementation": {
                "git_commit": SOURCE,
                "module": "packing/devtools/wall_owner_sixth_site_feasibility.py",
            },
            "endpoint": {
                "path": source.source_path,
                "git_commit": SOURCE,
                "git_blob": source.git_blob,
            },
            "wall": {
                "path": wall.source_path,
                "git_commit": SOURCE,
                "git_blob": wall.git_blob,
                "constructor_revision": wall.constructor_revision,
            },
            "selected_cover": {
                "path": obstruction.RETAINED_SELECTED_PATH,
                "git_commit": SOURCE,
                "git_blob": obstruction.RETAINED_SELECTED_BLOB,
                "implementation_revision": obstruction.RETAINED_SELECTED_SOURCE,
            },
            "six_dot_cover": {
                "path": obstruction.RETAINED_SIX_DOT_PATH,
                "git_commit": SOURCE,
                "git_blob": obstruction.RETAINED_SIX_DOT_BLOB,
                "implementation_revision": obstruction.RETAINED_SIX_DOT_SOURCE,
            },
        },
        "settings": {
            "outer_side": str(source.outer_side),
            "core_side": str(source.core_side),
            "candidate": [0, 0, 0, 7],
            "orientation_count": 361,
            "original_dot_count": 5,
            "support_obstacle_count": len(selected) + 5,
            "confirmation_obstacle_count": len(selected) + 6,
            "max_subsets": 1023,
            "candidate_limit": 1,
        },
        "supports": supports,
        "final_region": {"dimension": None, "vertices": []},
        "canonical_site": None,
        "confirmation": [],
        "conflicting_escape": None,
        "summary": {
            "support_directions_complete": 188,
            "confirmation_directions_complete": 0,
        },
        "error": None,
    }


def test_receipt_parser_binds_source_chain_prefix_and_fixed_attainers() -> None:
    source, wall = _source(), _wall()
    document = _receipt(source, wall)
    parsed = obstruction.parse_feasibility_evidence(
        document,
        source_path="exp153.json",
        git_commit="current",
        git_blob="exp153-blob",
        expected_source=SOURCE,
        source=source,
        wall=wall,
    )
    assert parsed.right == _evidence(source).right
    assert parsed.left == _evidence(source).left
    changed = dict(document)
    changed["supports"] = cast(list[object], document["supports"])[:-1]
    with pytest.raises(obstruction.TwoAttainerError, match="complete support prefix"):
        obstruction.parse_feasibility_evidence(
            changed,
            source_path="exp153.json",
            git_commit="current",
            git_blob="exp153-blob",
            expected_source=SOURCE,
            source=source,
            wall=wall,
        )
    sources = cast(dict[str, object], document["sources"])
    implementation = cast(dict[str, object], sources["implementation"])
    changed = {
        **document,
        "sources": {
            **sources,
            "implementation": {**implementation, "git_commit": "b" * 40},
        },
    }
    with pytest.raises(obstruction.TwoAttainerError, match="authority chain"):
        obstruction.parse_feasibility_evidence(
            changed,
            source_path="exp153.json",
            git_commit="current",
            git_blob="exp153-blob",
            expected_source=SOURCE,
            source=source,
            wall=wall,
        )
