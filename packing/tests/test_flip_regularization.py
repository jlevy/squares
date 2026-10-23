"""Flip regularization: the eight point maps, the rule on fixtures whose answer is known by
hand, the canonical pose's invariance on real drawings, and the exact maps' round trips in
every scalar kind.

Three unit squares in a side-2 box end with the empty cell lower right. One tilted square
in a corner cell ties at every grid and is decided by its tilt's sign. Real house
witnesses, each drawn from all eight of its poses, decide one picture; a symmetric one
keeps its published pose. Every frame the builder makes, decimal, rational or
number-field, and a binary64 one, is mapped there and back to itself exactly.
"""

from __future__ import annotations

import json
import math
from collections.abc import Callable
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import pytest

from devtools.build_known_best_atlas import frame_from_witness
from devtools.flip_regularization import (
    DESCRIPTIONS,
    IDENTITY,
    POSES,
    Decision,
    Pose,
    decide,
    decide_counts,
    decide_frame,
    frame_corners,
    grid_weights,
    image_weights,
    invariant,
    orient_frame,
    orient_polygon,
    placements,
    same_picture,
    totals,
)
from sqpack.render.model import (
    ActiveFeature,
    CheckKind,
    CheckSummary,
    ContactFeature,
    ContainerWall,
    DetectedContactFeature,
    EvidenceTier,
    PackingFrame,
    Point2,
    RigidPose,
    ScalarKind,
    ScalarSource,
    SquareGeometry,
)
from sqpack.render.numbers import scalar_from_decimal, scalar_from_float, scalar_from_fraction
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parents[1]
UNIT = ((0, 0), (1, 0), (1, 1), (0, 1))

#: The module docstring's table: each pose's composite map, with side `s`.
TABLE: dict[Pose, Callable[[Fraction, Fraction, Fraction], tuple[Fraction, Fraction]]] = {
    Pose(rotate=0, flip=False): lambda x, y, _s: (x, y),
    Pose(rotate=90, flip=False): lambda x, y, s: (s - y, x),
    Pose(rotate=180, flip=False): lambda x, y, s: (s - x, s - y),
    Pose(rotate=270, flip=False): lambda x, y, s: (y, s - x),
    Pose(rotate=0, flip=True): lambda x, y, s: (s - y, s - x),
    Pose(rotate=90, flip=True): lambda x, y, s: (s - x, y),
    Pose(rotate=180, flip=True): lambda x, y, _s: (y, x),
    Pose(rotate=270, flip=True): lambda x, y, s: (x, s - y),
}


@cache
def _frame(n: int) -> PackingFrame:
    path = ROOT / f"witnesses/known-best/n-{n:03d}.yaml"
    return frame_from_witness(load_yaml(path.read_text(encoding="utf-8"))["witness"])


def _picture(n: int) -> tuple[list[list[tuple[float, float]]], float]:
    frame = _frame(n)
    return frame_corners(frame), float(frame.container_side.projected)


def _cells(
    filled: list[tuple[int, int]], *, tilt: float = 0.0
) -> list[list[tuple[float, float]]]:
    """Unit squares centred in the given unit cells, `(column, row)` from the lower left,
    each turned `tilt` degrees about its centre."""
    cosine, sine = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    squares = []
    for column, row in filled:
        cx, cy = column + 0.5, row + 0.5
        squares.append(
            [
                (
                    cx + (x - 0.5) * cosine - (y - 0.5) * sine,
                    cy + (x - 0.5) * sine + (y - 0.5) * cosine,
                )
                for x, y in UNIT
            ]
        )
    return squares


# --------------------------------------------------------------------------- poses


def test_each_pose_is_the_composite_its_table_row_states() -> None:
    side = Fraction(7, 2)
    points = [(Fraction(1, 3), Fraction(5, 4)), (Fraction(0), Fraction(7, 2)), (side, side)]
    assert tuple(TABLE) == POSES
    for pose, composite in TABLE.items():
        for x, y in points:
            assert pose.point(x, y, side) == composite(x, y, side)


def test_each_pose_reads_as_its_description() -> None:
    side = Fraction(6)
    lines = {
        "mirror left-right": lambda t: (side / 2, t),
        "mirror top-bottom": lambda t: (t, side / 2),
        "mirror across the rising diagonal": lambda t: (t, t),
        "mirror across the falling diagonal": lambda t: (t, side - t),
    }
    for pose in POSES[4:]:
        line = lines[DESCRIPTIONS[pose]]
        for t in (Fraction(0), Fraction(1, 3), Fraction(5)):
            x, y = line(t)
            assert pose.point(x, y, side) == (x, y)
    # Where each turn sends the right wall's midpoint.
    turns = {
        "unchanged": (side, side / 2),
        "quarter turn counter-clockwise": (side / 2, side),
        "half turn": (Fraction(0), side / 2),
        "quarter turn clockwise": (side / 2, Fraction(0)),
    }
    for pose in POSES[:4]:
        assert pose.point(side, side / 2, side) == turns[DESCRIPTIONS[pose]]


def test_the_poses_are_the_eight_symmetries_and_each_has_its_inverse() -> None:
    side = Fraction(7)
    assert POSES[0] is IDENTITY
    assert IDENTITY.identity
    assert len({pose.point(Fraction(1), Fraction(2), side) for pose in POSES}) == 8
    for pose in POSES:
        x, y = pose.point(Fraction(1), Fraction(2), side)
        assert pose.inverse().point(x, y, side) == (1, 2)
        assert pose.inverse().inverse() == pose
        assert pose.identity == (pose == IDENTITY)


def test_a_pose_record_round_trips_and_is_checked() -> None:
    for pose in POSES:
        assert Pose.from_record(pose.record()) == pose
    decision = Decision(Pose(rotate=90, flip=True), "grid-4", (1.0, 0.5, 0.25, 0.0))
    assert decision.record() == {
        "rotate": 90,
        "flip": True,
        "decided_by": "grid-4",
        "quadrants": [1.0, 0.5, 0.25, 0.0],
    }
    assert Pose.from_record(decision.record()) == decision.pose
    with pytest.raises(ValueError, match="rotate must be one of"):
        Pose.from_record({"rotate": 45, "flip": False})
    with pytest.raises(TypeError, match="rotate must be an integer"):
        Pose.from_record({"rotate": True, "flip": False})
    with pytest.raises(TypeError, match="flip must be a boolean"):
        Pose.from_record({"rotate": 90, "flip": "yes"})
    with pytest.raises(ValueError, match="needs flip"):
        Pose.from_record({"rotate": 90})


def test_orient_polygon_keeps_the_winding() -> None:
    side = Fraction(3)
    square = [(Fraction(x) + Fraction(1, 2), Fraction(y) + 1) for x, y in UNIT]

    def signed_area(polygon: list[tuple[Fraction, Fraction]]) -> Fraction:
        return (
            sum(
                (
                    polygon[index - 1][0] * y - x * polygon[index - 1][1]
                    for index, (x, y) in enumerate(polygon)
                ),
                Fraction(0),
            )
            / 2
        )

    assert signed_area(square) == 1
    for pose in POSES:
        image = orient_polygon(pose, square, side)
        assert signed_area(image) == 1
        assert set(image) == {pose.point(x, y, side) for x, y in square}


# --------------------------------------------------------------------------- the rule


def test_weights_clip_each_square_to_its_cells() -> None:
    diamond = _cells([(1, 1)], tilt=45.0)
    # A unit square turned 45 degrees about the centre of a side-3 box puts a quarter of
    # itself in each quadrant. On the 3 x 3 grid each of its corners pokes a right
    # triangle of area (sqrt(2)/2 - 1/2)^2 into an edge cell, and the rest is the centre's.
    assert grid_weights(diamond, 3.0, 2) == pytest.approx((0.25 / 2.25,) * 4, abs=1e-15)
    tip = (math.sqrt(2) / 2 - 0.5) ** 2
    expected = (0.0, tip, 0.0, tip, 1 - 4 * tip, tip, 0.0, tip, 0.0)
    assert grid_weights(diamond, 3.0, 3) == pytest.approx(expected, abs=1e-15)


def test_a_poses_weights_are_its_image_weights_permuted() -> None:
    squares, side = _picture(11)
    for cells in (2, 4, 8):
        weights = grid_weights(squares, side, cells)
        for pose in POSES:
            image = [orient_polygon(pose, corners, side) for corners in squares]
            assert grid_weights(image, side, cells) == pytest.approx(
                image_weights(weights, pose, cells), abs=1e-12
            )


@pytest.mark.parametrize("empty", [(0, 0), (1, 0), (0, 1), (1, 1)])
def test_three_squares_leave_the_empty_cell_lower_right(empty: tuple[int, int]) -> None:
    filled = [cell for cell in [(0, 0), (1, 0), (0, 1), (1, 1)] if cell != empty]
    decision = decide(_cells(filled), 2.0)
    assert decision.quadrants == (1.0, 1.0, 1.0, 0.0)
    assert decision.decided_by == "quadrants"
    if empty == (1, 1):
        # A grid filled from the lower left, empty at the upper right: a clockwise
        # quarter turn and the top-bottom mirror both draw it, and the turn comes first.
        assert decision.pose == Pose(rotate=270, flip=False)


def test_the_tilt_decides_between_mirror_images_that_share_every_centre() -> None:
    side = 64.0
    for tilt, expected in ((10.0, Pose(rotate=0, flip=True)), (-10.0, IDENTITY)):
        # One square inside the upper-left cell of every grid up to 16 x 16: only the
        # identity and the falling-diagonal mirror keep it there, and the weights tie.
        square = [(x + 1.5, y + 61.5) for x, y in _cells([(0, 0)], tilt=tilt)[0]]
        decision = decide([square], side)
        assert decision.decided_by == "squares"
        assert decision.pose == expected
        assert invariant([square], side)


def test_same_picture_pairs_squares_by_centre_and_tilt_modulo_a_quarter_turn() -> None:
    picture = [(0.5, 0.5, 44.9999999999), (1.5, 0.5, 0.0)]
    assert same_picture(picture, [(1.5, 0.5, 0.0), (0.5, 0.5, -45.0)])
    assert not same_picture(picture, [(1.5, 0.5, 0.0), (0.5, 0.5, 10.0)])
    assert not same_picture(picture, [(1.5, 0.5, 0.0), (0.5, 0.50001, 45.0)])
    assert not same_picture(picture, picture[:1])
    mirrored = placements([[(x, 1 - y) for x, y in _cells([(0, 0)], tilt=10.0)[0]]])
    assert not same_picture(placements(_cells([(0, 0)], tilt=10.0)), mirrored)


@pytest.mark.parametrize("n", [4, 5, 9])
def test_a_symmetric_packing_keeps_its_published_pose(n: int) -> None:
    decision = decide(*_picture(n))
    assert decision.pose == IDENTITY
    assert decision.decided_by == "quadrants"


def test_the_decisions_the_prototype_measured() -> None:
    ten = decide_frame(_frame(10))
    assert ten.pose == IDENTITY
    assert ten.quadrants == pytest.approx((0.8607, 0.5946, 0.5946, 0.8607), abs=5e-5)
    assert decide_frame(_frame(11)).pose == Pose(rotate=180, flip=False)
    assert decide_frame(_frame(17)).pose == Pose(rotate=270, flip=True)
    assert decide_frame(_frame(62)).decided_by == "grid-8"
    assert decide_frame(_frame(254)).decided_by == "grid-16"


@pytest.mark.parametrize("n", [10, 17, 37, 62, 254])
def test_every_pose_of_a_picture_draws_the_same_picture(n: int) -> None:
    squares, side = _picture(n)
    drawn, stages = [], set()
    for pose in POSES:
        image = [orient_polygon(pose, corners, side) for corners in squares]
        decision = decide(image, side)
        stages.add(decision.decided_by)
        drawn.append(placements(orient_polygon(decision.pose, c, side) for c in image))
    assert len(stages) == 1
    assert all(same_picture(drawn[0], other) for other in drawn[1:])
    assert invariant(squares, side)
    # The canonical pose of a picture already in it is the identity.
    assert decide_frame(orient_frame(_frame(n), decide_frame(_frame(n)).pose)).pose == IDENTITY


def test_the_command_decides_drawn_pictures() -> None:
    rows = decide_counts([10, 11], workers=1, invariance=True)
    assert [(row["n"], row["rotate"], row["flip"], row["invariant"]) for row in rows] == [
        (10, 0, False, True),
        (11, 180, False, True),
    ]
    summary = totals(rows)
    assert summary["identity"] == 1
    assert summary["decided_by"]["quadrants"] == 2
    assert summary["not_invariant"] == []


# --------------------------------------------------------------------------- exact maps


class _Coefficients(tuple[Fraction, ...]):
    """A number-field scalar's power-basis coefficients, subtracted one by one."""

    def __sub__(self, other: _Coefficients) -> _Coefficients:
        return _Coefficients(a - b for a, b in zip(self, other, strict=True))


def _exact(value: ScalarSource) -> Any:
    """A scalar's exact value, whatever its kind."""
    match value.kind:
        case ScalarKind.EXACT:
            coefficients = json.loads(value.source)["coefficients"]
            return _Coefficients(Fraction(c) for c in coefficients)
        case ScalarKind.RATIONAL:
            return Fraction(value.source)
        case ScalarKind.BINARY64:
            return Fraction(float(value.source))
        case _:
            return Fraction(Decimal(value.source))


def _synthetic(
    scalar: Callable[[Any], ScalarSource], side: Any, cells: list[tuple[int, int]], **frame: Any
) -> PackingFrame:
    squares = tuple(
        SquareGeometry(
            square_id=f"square-{index:03d}",
            corners=tuple(Point2(scalar(column + x), scalar(row + y)) for x, y in UNIT),
            label=str(index),
        )
        for index, (column, row) in enumerate(cells, start=1)
    )
    return PackingFrame(container_side=scalar(side), squares=squares, **frame)


def _features_frame() -> PackingFrame:
    """A rational frame with a pose on one square, a wall contact on each wall and an
    active feature."""
    half, side = Fraction(1, 2), Fraction(5, 2)
    rational = scalar_from_fraction
    frame = _synthetic(
        lambda value: rational(Fraction(value)),
        side,
        [(0, 0), (1, 0), (0, 1)],
        evidence=EvidenceTier.CERTIFIED_UPPER_BOUND,
        check=CheckSummary(passed=True, kind=CheckKind.FORMAL, method="fixture"),
    )
    midpoints = {
        ContainerWall.LEFT: (Fraction(0), half),
        ContainerWall.RIGHT: (side, half),
        ContainerWall.BOTTOM: (half, Fraction(0)),
        ContainerWall.TOP: (half, side),
    }
    features: list[ContactFeature | DetectedContactFeature | ActiveFeature] = [
        ContactFeature(
            f"contact-{wall.value}",
            Point2(rational(x), rational(y)),
            ("square-001",),
            wall=wall,
        )
        for wall, (x, y) in midpoints.items()
    ]
    features.append(
        ActiveFeature("active-0", Point2(rational(half), rational(Fraction(3, 2))), "corner")
    )
    pose = RigidPose(Point2(rational(half), rational(half)), rational(Fraction(1, 10)))
    first = frame.squares[0]
    return PackingFrame(
        container_side=frame.container_side,
        squares=(
            SquareGeometry(first.square_id, first.corners, pose, first.label),
            *frame.squares[1:],
        ),
        evidence=frame.evidence,
        check=frame.check,
        features=tuple(sorted(features, key=lambda feature: feature.feature_id)),
    )


def _frames() -> dict[str, PackingFrame]:
    return {
        "decimal n=5": _frame(5),
        "decimal n=10": _frame(10),
        "decimal n=11": _frame(11),
        "rational corners n=3": _frame(3),
        "rational corners n=62": _frame(62),
        "number field n=51": _frame(51),
        "binary64": _synthetic(
            lambda value: scalar_from_float(float(value)), 2.5, [(0, 0), (1, 1)]
        ),
        "features": _features_frame(),
    }


def test_frames_of_every_kind_are_mapped_there_and_back_exactly() -> None:
    kinds = set()
    for name, frame in _frames().items():
        kinds.add(frame.container_side.kind)
        for pose in POSES:
            assert orient_frame(orient_frame(frame, pose), pose.inverse()) == frame, (
                name,
                pose,
            )
    assert kinds == set(ScalarKind)


def test_every_point_is_mapped_exactly_and_projected_again() -> None:
    for name, frame in _frames().items():
        side = _exact(frame.container_side)
        for pose in (Pose(rotate=90, flip=False), Pose(rotate=0, flip=True)):
            image = orient_frame(frame, pose)
            assert image.container_side == frame.container_side
            for source, oriented in zip(frame.squares, image.squares, strict=True):
                assert (oriented.square_id, oriented.label) == (source.square_id, source.label)
                expected = orient_polygon(
                    pose, [(_exact(p.x), _exact(p.y)) for p in source.corners], side
                )
                assert [(_exact(p.x), _exact(p.y)) for p in oriented.corners] == expected, name
                projected = orient_polygon(
                    pose,
                    [(p.x.projected, p.y.projected) for p in source.corners],
                    frame.container_side.projected,
                )
                with localcontext() as context:
                    context.prec = 60
                    for point, (x, y) in zip(oriented.corners, projected, strict=True):
                        assert abs(point.x.projected - x) < Decimal("1e-25"), name
                        assert abs(point.y.projected - y) < Decimal("1e-25"), name


def test_walls_poses_and_features_follow_the_map() -> None:
    frame = _features_frame()
    side = _exact(frame.container_side)
    turned = orient_frame(frame, Pose(rotate=90, flip=False))
    walls = {
        feature.feature_id: feature.wall
        for feature in turned.features
        if isinstance(feature, ContactFeature)
    }
    assert walls == {
        "contact-left": ContainerWall.BOTTOM,
        "contact-bottom": ContainerWall.RIGHT,
        "contact-right": ContainerWall.TOP,
        "contact-top": ContainerWall.LEFT,
    }
    on_wall = {
        ContainerWall.LEFT: lambda x, _y: x == 0,
        ContainerWall.RIGHT: lambda x, _y: x == side,
        ContainerWall.BOTTOM: lambda _x, y: y == 0,
        ContainerWall.TOP: lambda _x, y: y == side,
    }
    for pose in POSES:
        image = orient_frame(frame, pose)
        assert [feature.feature_id for feature in image.features] == [
            feature.feature_id for feature in frame.features
        ]
        for before, after in zip(frame.features, image.features, strict=True):
            point = after.point if isinstance(after, ActiveFeature) else after.start
            source = before.point if isinstance(before, ActiveFeature) else before.start
            assert (_exact(point.x), _exact(point.y)) == pose.point(
                _exact(source.x), _exact(source.y), side
            )
            if isinstance(after, ContactFeature) and after.wall is not None:
                assert on_wall[after.wall](_exact(point.x), _exact(point.y))
        rigid = image.squares[0].pose
        assert rigid is not None
        assert _exact(rigid.angle) == (Fraction(-1, 10) if pose.flip else Fraction(1, 10))
        assert (_exact(rigid.centre.x), _exact(rigid.centre.y)) == pose.point(
            Fraction(1, 2), Fraction(1, 2), side
        )


def test_a_map_it_cannot_make_exactly_is_refused() -> None:
    rational = _synthetic(lambda value: scalar_from_fraction(Fraction(value)), 3, [(0, 0)])
    first = rational.squares[0]
    corner = Point2(scalar_from_decimal("0.0"), first.corners[0].y)
    mixed = PackingFrame(
        container_side=rational.container_side,
        squares=(SquareGeometry(first.square_id, (corner, *first.corners[1:])),),
    )
    with pytest.raises(ValueError, match="mixed scalar kinds"):
        orient_frame(mixed, IDENTITY)

    centre = Point2(first.corners[0].x, first.corners[0].y)
    pair = DetectedContactFeature(
        "census-pair",
        centre,
        Point2(first.corners[2].x, first.corners[2].y),
        ("square-001", "square-002"),
        angle_tolerance_radians=Decimal("1e-6"),
        contact_tolerance=Decimal("2e-6"),
        residual=Decimal(0),
        normal="u-normal",
    )
    with pytest.raises(ValueError, match="normal is not mapped"):
        orient_frame(
            PackingFrame(rational.container_side, rational.squares, features=(pair,)), IDENTITY
        )

    field = _frame(51)
    square = field.squares[0]
    x = square.corners[0].x
    document = json.loads(x.source)
    document["field"] = {**document["field"], "minimal_polynomial": ["1", "0", "-3"]}
    foreign = ScalarSource(
        x.kind, json.dumps(document), x.projected, x.precision, json.dumps(document)
    )
    other = SquareGeometry(
        square.square_id, (Point2(foreign, square.corners[0].y), *square.corners[1:])
    )
    with pytest.raises(ValueError, match="different fields"):
        orient_frame(PackingFrame(field.container_side, (other,)), Pose(rotate=180, flip=False))
