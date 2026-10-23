#!/usr/bin/env python3
"""Flip regularization: each drawn picture turned by one of the container's eight symmetries.

Usage, from `packing/`, after
`uv run --frozen --all-extras --group dev python -m devtools.flip_regularization`:

    [--n N ...] [--workers K] [--invariance] [--json]

Packings arrive in whatever pose their source published, so neighbouring atlas tiles
are turned and mirrored against one another. Flip regularization picks, for each drawn
picture, the symmetry that draws it in its canonical pose, decided in binary64 from where
its squares lie. It is display only: the renderers apply the pose exactly to the stored
coordinates, and no witness, view or certificate changes. The plan is
`docs/project/specs/active/plan-2026-10-23-flip-regularization.md`.

**Poses.** A `Pose` is the owner's two steps: `rotate` 0, 90, 180 or 270 degrees
counter-clockwise about the container's centre, then, if `flip`, mirror across the
diagonal from the upper-left to the lower-right corner. That mirror fixes the upper-left
and lower-right quadrants and swaps the other two, so the rotation decides which quadrant
is upper left and the flip which of its neighbours is upper right. Each of the eight
symmetries is exactly one pair, and with y up and side `s` the composites are:

    pose        point map         reads as
    (0, F)      (x, y)            unchanged
    (90, F)     (s - y, x)        quarter turn counter-clockwise
    (180, F)    (s - x, s - y)    half turn
    (270, F)    (y, s - x)        quarter turn clockwise
    (0, T)      (s - y, s - x)    mirror across the falling diagonal
    (90, T)     (s - x, y)        mirror left-right
    (180, T)    (y, x)            mirror across the rising diagonal y = x
    (270, T)    (x, s - y)        mirror top-bottom

`POSES` lists them in that order, rotations without a flip first.

**The rule** (`decide`). The owner's words, 23 October 2026: rotate so the heaviest
quadrant by filled area is upper left, then flip if necessary so that the heavier of its
two neighbours is upper right, ties broken by some further deterministic rule.

1. *Weights.* On an m x m grid over the container, a cell's weight is the area of the
   squares inside it over the cell's area, each square clipped to the cell as a convex
   polygon in binary64. Cells are read in reading order, top row first and left to
   right, so at m = 2 they are upper left, upper right, lower left, lower right.
2. *Filter.* Of the candidate poses, keep at each position in turn those whose image's
   weight there is within `TOLERANCE` of the greatest. At m = 2 this is the owner's rule.
3. *Levels.* The filter runs at m = 2, then 4, 8 and 16 (`LEVELS`) on the survivors.
4. *Final key.* Each survivor's image as its squares, each `(-cy, cx, tilt)` rounded to
   nine places and sorted (the highest square first, then the leftmost), the least kept.
   The tilt is the square's angle modulo 90 degrees in (-45, 45]; it is in the key
   because two mirror images can share every centre and differ only in its sign.
5. *Same picture.* After each stage the survivors are matched square for square; once
   they all draw the same picture, the packing having that symmetry, the stage that got
   there is `decided_by` and the first survivor in `POSES` order is the pose, so a
   symmetric packing keeps its published pose where it can. Distinct pictures surviving
   the final key raise, rather than a symmetry being assumed.

**Exact maps** (`orient_frame`). Each point is mapped in its own scalar kind: rational
by `Fraction`, decimal by `Decimal` at whatever precision keeps the difference exact,
number-field elements coefficient by coefficient with the projection recomputed, and
binary64 by float subtraction, the one kind that rounds, since the difference of two
doubles need not be one; no witness-built frame is binary64.

The command decides each count's drawn picture -- its regularized view where
`default-drawings.json` makes that the default, else its house witness -- and prints the
pose, the stage that decided it and the oriented quadrant weights, then how many counts
each stage decided. `--invariance` also decides each picture from all eight of its poses
and fails unless all eight draw the same (`invariant`). It reads and prints; it writes
nothing.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import os
from bisect import bisect_left, bisect_right
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cache, lru_cache
from pathlib import Path
from typing import Any, Protocol, Self

from sqpack.field import NumberField
from sqpack.render.model import (
    ActiveFeature,
    ContactFeature,
    ContainerWall,
    DetectedContactFeature,
    PackingFrame,
    Point2,
    RigidPose,
    ScalarKind,
    ScalarSource,
    SquareGeometry,
)
from sqpack.render.numbers import (
    scalar_from_decimal,
    scalar_from_exact,
    scalar_from_float,
    scalar_from_fraction,
)
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
GENERATOR = "python -m devtools.flip_regularization"
FORMAT = "flip-regularization-v1"
WITNESS = "packing/witnesses/known-best/n-{n:03d}.yaml"
COUNTS = range(1, 325)

ROTATIONS = (0, 90, 180, 270)
TOLERANCE = 1e-9
"""Two weights this close are equal."""
LEVELS = (2, 4, 8, 16)
STAGES = ("quadrants", "grid-4", "grid-8", "grid-16", "squares")
"""What decided a pose: the grid at each of `LEVELS`, then the final key."""
KEY_PLACES = 9
"""The final key's rounding, in decimal places."""
MATCH_TOLERANCE = 1e-6
"""Two pictures are the same when their squares pair off within this, centres in the
container's units and tilts in degrees."""


class Coordinate(Protocol):
    """What `Pose.point` needs of a coordinate: subtraction from the side."""

    def __sub__(self, other: Self, /) -> Self: ...


@dataclass(frozen=True)
class Pose:
    """One of the container's eight symmetries, as the owner's two steps."""

    rotate: int
    """0, 90, 180 or 270: degrees counter-clockwise about the container's centre."""
    flip: bool
    """Then mirror across the diagonal from the upper-left to the lower-right corner."""

    def __post_init__(self) -> None:
        if not isinstance(self.rotate, int) or isinstance(self.rotate, bool):
            raise TypeError(f"rotate must be an integer, not {self.rotate!r}")
        if self.rotate not in ROTATIONS:
            raise ValueError(f"rotate must be one of {ROTATIONS}, not {self.rotate!r}")
        if not isinstance(self.flip, bool):
            raise TypeError(f"flip must be a boolean, not {self.flip!r}")

    def point[T: Coordinate](self, x: T, y: T, side: T) -> tuple[T, T]:
        """Where `(x, y)` lands, y up with the origin lower left.

        Only `side - v` and swapping, so it maps ints, floats, `Fraction`s, `Decimal`s
        and number-field elements alike, each in its own arithmetic."""
        match self.rotate:
            case 90:
                x, y = side - y, x
            case 180:
                x, y = side - x, side - y
            case 270:
                x, y = y, side - x
            case _:
                pass
        if self.flip:
            x, y = side - y, side - x
        return x, y

    def inverse(self) -> Pose:
        """The pose that undoes this one: a flipped pose is a reflection, its own
        inverse, and a rotation's is the opposite turn."""
        return self if self.flip else Pose(rotate=(360 - self.rotate) % 360, flip=False)

    def record(self) -> dict[str, Any]:
        return {"rotate": self.rotate, "flip": self.flip}

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> Pose:
        """The pose a record states, its fields checked as a new pose's are; other fields,
        such as a `Decision`'s, are ignored."""
        missing = sorted({"rotate", "flip"} - record.keys())
        if missing:
            raise ValueError(f"a pose record needs {', '.join(missing)}")
        return cls(rotate=record["rotate"], flip=record["flip"])

    @property
    def identity(self) -> bool:
        return self.rotate == 0 and not self.flip


POSES = tuple(Pose(rotate=rotate, flip=flip) for flip in (False, True) for rotate in ROTATIONS)
IDENTITY = POSES[0]
DESCRIPTIONS = dict(
    zip(
        POSES,
        (
            "unchanged",
            "quarter turn counter-clockwise",
            "half turn",
            "quarter turn clockwise",
            "mirror across the falling diagonal",
            "mirror left-right",
            "mirror across the rising diagonal",
            "mirror top-bottom",
        ),
        strict=True,
    )
)


def orient_polygon[T: Coordinate](
    pose: Pose, corners: Iterable[tuple[T, T]], side: T
) -> list[tuple[T, T]]:
    """Map each corner; when the pose flips, reverse the corner order so the winding is
    kept."""
    mapped = [pose.point(x, y, side) for x, y in corners]
    return mapped[::-1] if pose.flip else mapped


# --------------------------------------------------------------------------- the rule

type Corners = Sequence[tuple[float, float]]
type Placement = tuple[float, float, float]
"""A square as its centre and its tilt: `(cx, cy, degrees in (-45, 45])`."""


def _half_plane(
    polygon: list[tuple[float, float]], axis: int, bound: float, *, below: bool
) -> list[tuple[float, float]]:
    """One Sutherland-Hodgman pass: the part of a convex polygon on one side of an axis
    line, `axis` 0 for x and 1 for y, on or below `bound` when `below`, else on or above.
    """
    kept: list[tuple[float, float]] = []
    if not polygon:
        return kept
    previous = polygon[-1]
    previous_in = previous[axis] <= bound if below else previous[axis] >= bound
    for current in polygon:
        current_in = current[axis] <= bound if below else current[axis] >= bound
        if current_in != previous_in:
            share = (bound - previous[axis]) / (current[axis] - previous[axis])
            other = previous[1 - axis] + share * (current[1 - axis] - previous[1 - axis])
            kept.append((bound, other) if axis == 0 else (other, bound))
        if current_in:
            kept.append(current)
        previous, previous_in = current, current_in
    return kept


def _area(polygon: Sequence[tuple[float, float]]) -> float:
    if len(polygon) < 3:
        return 0.0
    total = 0.0
    previous = polygon[-1]
    for current in polygon:
        total += previous[0] * current[1] - current[0] * previous[1]
        previous = current
    return abs(total) / 2


def _span(edges: Sequence[float], low: float, high: float) -> range:
    """The cells along one axis that `[low, high]` can reach."""
    last = len(edges) - 2
    first = min(last, max(0, bisect_right(edges, low) - 1))
    return range(first, min(last, max(0, bisect_left(edges, high) - 1)) + 1)


def grid_weights(squares: Iterable[Corners], side: float, cells: int) -> tuple[float, ...]:
    """Each cell's filled fraction on a `cells` x `cells` grid, in reading order: top row
    first, left to right. A square is clipped only against the cells its bounding box
    reaches, which keeps a 16 x 16 grid cheap."""
    edges = [side * index / cells for index in range(cells + 1)]
    areas = [0.0] * (cells * cells)
    for corners in squares:
        polygon = list(corners)
        xs = [x for x, _y in polygon]
        ys = [y for _x, y in polygon]
        rows = _span(edges, min(ys), max(ys))
        for column in _span(edges, min(xs), max(xs)):
            strip = _half_plane(polygon, 0, edges[column], below=False)
            strip = _half_plane(strip, 0, edges[column + 1], below=True)
            if len(strip) < 3:
                continue
            for row in rows:
                piece = _half_plane(strip, 1, edges[row], below=False)
                piece = _half_plane(piece, 1, edges[row + 1], below=True)
                areas[(cells - 1 - row) * cells + column] += _area(piece)
    cell = side / cells
    return tuple(area / (cell * cell) for area in areas)


@cache
def _targets(pose: Pose, cells: int) -> tuple[int, ...]:
    """Where each cell, in reading order, lands under `pose`: its centre mapped in whole
    half-cells, so the permutation is exact."""
    targets: list[int] = []
    for index in range(cells * cells):
        row, column = divmod(index, cells)
        x, y = pose.point(2 * column + 1, 2 * (cells - 1 - row) + 1, 2 * cells)
        targets.append((cells - 1 - (y - 1) // 2) * cells + (x - 1) // 2)
    return tuple(targets)


def image_weights(weights: Sequence[float], pose: Pose, cells: int) -> tuple[float, ...]:
    """The weights of the picture `pose` draws, from the source picture's own."""
    image = [0.0] * len(weights)
    for weight, target in zip(weights, _targets(pose, cells), strict=True):
        image[target] = weight
    return tuple(image)


def _strongest(candidates: list[Pose], weights: Mapping[Pose, Sequence[float]]) -> list[Pose]:
    """The candidates whose weights are lexicographically greatest, within `TOLERANCE`."""
    for position in range(len(weights[candidates[0]])):
        if len(candidates) == 1:
            break
        best = max(weights[pose][position] for pose in candidates)
        candidates = [
            pose for pose in candidates if weights[pose][position] >= best - TOLERANCE
        ]
    return candidates


def _tilt(degrees: float) -> float:
    """An angle modulo a quarter turn, in `(-45, 45]`."""
    reduced = degrees % 90.0
    return reduced - 90.0 if reduced > 45.0 else reduced


def placements(squares: Iterable[Corners]) -> list[Placement]:
    """Each square's centre and tilt, the tilt from its first edge."""
    found: list[Placement] = []
    for corners in squares:
        (x0, y0), (x1, y1) = corners[0], corners[1]
        found.append(
            (
                sum(x for x, _y in corners) / len(corners),
                sum(y for _x, y in corners) / len(corners),
                _tilt(math.degrees(math.atan2(y1 - y0, x1 - x0))),
            )
        )
    return found


def oriented_placements(
    source: Iterable[Placement], pose: Pose, side: float
) -> list[Placement]:
    """The placements of the picture `pose` draws. A turn by quarter turns keeps a tilt
    and a mirror negates it, modulo a quarter turn."""
    return [
        (*pose.point(x, y, side), _tilt(-tilt) if pose.flip else tilt) for x, y, tilt in source
    ]


def same_picture(first: Sequence[Placement], second: Sequence[Placement]) -> bool:
    """Whether two pictures pair off square for square, each pair's centres within
    `MATCH_TOLERANCE` and its tilts within it in degrees, modulo 90.

    Paired by position rather than by sorting both lists: a sort by rounded key can order
    two squares of one row differently in two images of one picture, when a centre sits
    within float noise of a rounding boundary. Unit squares that do not overlap have
    centres at least 1 apart, so a pairing within the tolerance is unique."""
    if len(first) != len(second):
        return False
    buckets: dict[tuple[int, int], list[int]] = {}
    for index, (x, y, _angle) in enumerate(second):
        buckets.setdefault((round(x), round(y)), []).append(index)
    paired: set[int] = set()
    for x, y, tilt in first:
        column, row = round(x), round(y)
        match = next(
            (
                index
                for dx in (-1, 0, 1)
                for dy in (-1, 0, 1)
                for index in buckets.get((column + dx, row + dy), ())
                if index not in paired and _paired((x, y, tilt), second[index])
            ),
            None,
        )
        if match is None:
            return False
        paired.add(match)
    return True


def _paired(left: Placement, right: Placement) -> bool:
    turn = abs(left[2] - right[2]) % 90.0
    return (
        math.dist(left[:2], right[:2]) <= MATCH_TOLERANCE
        and min(turn, 90.0 - turn) <= MATCH_TOLERANCE
    )


def _key(image: Iterable[Placement]) -> list[tuple[float, float, float]]:
    return sorted(
        (round(-y, KEY_PLACES), round(x, KEY_PLACES), round(tilt, KEY_PLACES))
        for x, y, tilt in image
    )


@dataclass(frozen=True)
class Decision:
    """The pose that draws a picture in its canonical pose, and what decided it."""

    pose: Pose
    decided_by: str
    """The first of `STAGES` after which every surviving pose drew the same picture."""
    quadrants: tuple[float, float, float, float]
    """The oriented picture's quadrant weights: upper left, upper right, lower left,
    lower right."""

    def record(self) -> dict[str, Any]:
        """The drawings record's `flip_regularization` field for this picture."""
        return {
            **self.pose.record(),
            "decided_by": self.decided_by,
            "quadrants": [round(weight, 6) for weight in self.quadrants],
        }


def decide(squares: Sequence[Sequence[tuple[float, float]]], side: float) -> Decision:
    """The canonical pose of a picture given as each square's corners, in binary64."""
    source = placements(squares)
    images: dict[Pose, list[Placement]] = {}

    def image(pose: Pose) -> list[Placement]:
        if pose not in images:
            images[pose] = oriented_placements(source, pose, side)
        return images[pose]

    def one_picture(candidates: Sequence[Pose]) -> bool:
        first = image(candidates[0])
        return all(same_picture(first, image(pose)) for pose in candidates[1:])

    candidates = list(POSES)
    quadrants: dict[Pose, tuple[float, ...]] = {}
    for cells, stage in zip(LEVELS, STAGES, strict=False):
        weights = grid_weights(squares, side, cells)
        oriented = {pose: image_weights(weights, pose, cells) for pose in candidates}
        if cells == LEVELS[0]:
            quadrants = oriented
        candidates = _strongest(candidates, oriented)
        if one_picture(candidates):
            return _decision(candidates[0], stage, quadrants)
    keys = {pose: _key(image(pose)) for pose in candidates}
    least = min(keys.values())
    candidates = [pose for pose in candidates if keys[pose] == least]
    if one_picture(candidates):
        return _decision(candidates[0], STAGES[-1], quadrants)
    names = ", ".join(f"({pose.rotate}, {pose.flip})" for pose in candidates)
    raise ValueError(f"distinct pictures survive the {STAGES[-1]!r} stage: poses {names}")


def _decision(pose: Pose, stage: str, quadrants: Mapping[Pose, Sequence[float]]) -> Decision:
    upper_left, upper_right, lower_left, lower_right = quadrants[pose]
    return Decision(pose, stage, (upper_left, upper_right, lower_left, lower_right))


def frame_corners(frame: PackingFrame) -> list[list[tuple[float, float]]]:
    """Each square's corners as binary64, from each scalar's projection."""
    return [
        [(float(point.x.projected), float(point.y.projected)) for point in square.corners]
        for square in frame.squares
    ]


def decide_frame(frame: PackingFrame) -> Decision:
    return decide(frame_corners(frame), float(frame.container_side.projected))


def invariant(squares: Sequence[Sequence[tuple[float, float]]], side: float) -> bool:
    """Whether a picture is drawn the same from each of its eight poses, which is what
    makes the pose canonical: each pose's image, decided and oriented, is one picture."""
    drawn: list[list[Placement]] = []
    for pose in POSES:
        image = [orient_polygon(pose, corners, side) for corners in squares]
        chosen = decide(image, side).pose
        drawn.append(placements(orient_polygon(chosen, corners, side) for corners in image))
    return all(same_picture(drawn[0], other) for other in drawn[1:])


# --------------------------------------------------------------------------- exact maps

KINDS = frozenset(ScalarKind)


def _decimal_text(value: Decimal) -> str:
    """Fixed point with trailing zeros dropped, as the frame builder spells a projection
    (`build_known_best_atlas._projection_text`), so a decimal picture mapped there and
    back is spelled as it was built."""
    if value.is_zero():
        return "0.0"
    text = format(value, "f")
    if "." not in text:
        return f"{text}.0"
    text = text.rstrip("0")
    return f"{text}0" if text.endswith(".") else text


def _exact_decimal(operation: Callable[[], Decimal], *operands: Decimal) -> Decimal:
    """`operation` at a precision no difference or negation of `operands` can round at,
    whatever the caller's context: the result spans both coefficients and exponents."""
    for operand in operands:
        if not operand.is_finite():
            raise ValueError("an exact map requires finite decimal coordinates")
    precision = (
        sum(
            len(operand.as_tuple().digits) + abs(int(operand.as_tuple().exponent))
            for operand in operands
        )
        + 4
    )
    with localcontext() as context:
        context.prec = max(precision, 28)
        return operation()


def _field_value(value: ScalarSource) -> tuple[dict[str, Any], list[Fraction]]:
    """A number-field scalar's declaration and power-basis coefficients, low first."""
    document = json.loads(value.exact_source or value.source)
    return document["field"], [
        Fraction(coefficient) for coefficient in document["coefficients"]
    ]


@lru_cache(maxsize=8)
def _side_fraction(source: str) -> Fraction:
    """A rational side, parsed once rather than at every point: a center-basis witness's
    rationals run to thousands of digits (n = 29's to 8,000 characters), and parsing the
    side at every point was 15 per cent of mapping its frame."""
    return Fraction(source)


@cache
def _number_field(declaration: str) -> NumberField:
    field = json.loads(declaration)
    return NumberField(
        [Fraction(value) for value in field["minimal_polynomial"]],
        tuple(Fraction(value) for value in field["isolating_interval"]),
    )


def _field_scalar(
    field: Mapping[str, Any], coefficients: Sequence[Fraction], precision: int
) -> ScalarSource:
    """A number-field scalar in the frame builder's encoding
    (`build_known_best_atlas._exact_frame_geometry`), its projection recomputed."""
    source = json.dumps(
        {"field": field, "coefficients": [str(value) for value in coefficients]},
        sort_keys=True,
        separators=(",", ":"),
    )
    number_field = _number_field(json.dumps(field, sort_keys=True, separators=(",", ":")))
    projected = number_field.decimal(number_field.element(list(coefficients)), 40)
    return scalar_from_exact(source, projected, precision=precision)


def _difference(side: ScalarSource, value: ScalarSource) -> ScalarSource:
    """`side - value`, exactly, in their shared kind; `value`'s precision is kept."""
    if side.kind is not value.kind:
        raise ValueError(f"mixed scalar kinds: {side.kind} and {value.kind}")
    match value.kind:
        case ScalarKind.RATIONAL:
            difference = _side_fraction(side.source) - Fraction(value.source)
            return scalar_from_fraction(difference, precision=value.precision)
        case ScalarKind.DECIMAL:
            bound, coordinate = Decimal(side.source), Decimal(value.source)
            result = _exact_decimal(lambda: bound - coordinate, bound, coordinate)
            return scalar_from_decimal(_decimal_text(result))
        case ScalarKind.EXACT:
            field, bound = _field_value(side)
            value_field, coordinate = _field_value(value)
            if field != value_field:
                raise ValueError("number-field scalars declare different fields")
            difference = [a - b for a, b in zip(bound, coordinate, strict=True)]
            return _field_scalar(field, difference, value.precision)
        case ScalarKind.BINARY64:
            difference = float(side.source) - float(value.source)
            return scalar_from_float(difference, precision=value.precision)
        case _:
            raise ValueError(f"unknown scalar kind {value.kind!r}")


def _negated(value: ScalarSource) -> ScalarSource:
    """`-value`, exactly, in its own kind."""
    match value.kind:
        case ScalarKind.RATIONAL:
            return scalar_from_fraction(-Fraction(value.source), precision=value.precision)
        case ScalarKind.DECIMAL:
            number = Decimal(value.source)
            return scalar_from_decimal(_decimal_text(_exact_decimal(lambda: -number, number)))
        case ScalarKind.EXACT:
            field, coefficients = _field_value(value)
            return _field_scalar(field, [-c for c in coefficients], value.precision)
        case ScalarKind.BINARY64:
            return scalar_from_float(-float(value.source), precision=value.precision)
        case _:
            raise ValueError(f"unknown scalar kind {value.kind!r}")


@dataclass(frozen=True, slots=True)
class _Exact:
    """A scalar that `Pose.point` subtracts from the side in its own kind. A coordinate
    the map only moves comes back as the same object, so its scalar is kept as it was."""

    value: ScalarSource

    def __sub__(self, other: _Exact) -> _Exact:
        return _Exact(_difference(self.value, other.value))


def _wall_images(pose: Pose) -> dict[ContainerWall, ContainerWall]:
    """Where each wall goes, found by mapping its midpoint on a side-2 container."""
    midpoints = {
        ContainerWall.LEFT: (0, 1),
        ContainerWall.RIGHT: (2, 1),
        ContainerWall.BOTTOM: (1, 0),
        ContainerWall.TOP: (1, 2),
    }
    walls = {point: wall for wall, point in midpoints.items()}
    return {wall: walls[pose.point(*point, 2)] for wall, point in midpoints.items()}


def _points(frame: PackingFrame) -> Iterable[Point2]:
    for square in frame.squares:
        yield from square.corners
        if square.pose is not None:
            yield square.pose.centre
    for feature in frame.features:
        if isinstance(feature, ActiveFeature):
            yield feature.point
        else:
            yield feature.start
            if feature.end is not None:
                yield feature.end


def orient_frame(frame: PackingFrame, pose: Pose) -> PackingFrame:
    """The frame drawn in `pose`, every point mapped exactly in its own scalar kind.

    Square ids, labels and order, and the side, evidence, check and source fields, are
    kept, so colours stay stable. A flipped pose reverses each square's corners to keep
    their winding. A square's `RigidPose`, which nothing on the atlas path sets, has its
    centre mapped and its angle kept, or negated under a flip: every reader of the angle
    takes it modulo a quarter turn (`color._square_orientation`,
    `motion.short_quarter_turn`), where a turn by quarter turns keeps it and a mirror
    negates it. Feature points are mapped, a wall goes where its midpoint does, and
    feature ids are kept, a wall's name in one included.

    Refused, with `ValueError`: a point whose kind is not the side's, an unknown kind,
    number-field scalars of different fields, and a detected pair contact, whose
    `u-normal` or `v-normal` names an axis of its census's lattice frame that a pose
    swaps or keeps according to how the census reduces the class's angle.
    """
    side = frame.container_side
    if side.kind not in KINDS:
        raise ValueError(f"unknown scalar kind {side.kind!r}")
    for point in _points(frame):
        for value in (point.x, point.y):
            if value.kind is not side.kind:
                raise ValueError(f"mixed scalar kinds: side {side.kind}, point {value.kind}")
    bound = _Exact(side)
    walls = _wall_images(pose)

    def mapped(point: Point2) -> Point2:
        x, y = pose.point(_Exact(point.x), _Exact(point.y), bound)
        return Point2(x.value, y.value)

    def square_image(square: SquareGeometry) -> SquareGeometry:
        corners = orient_polygon(
            pose, [(_Exact(point.x), _Exact(point.y)) for point in square.corners], bound
        )
        rigid = square.pose
        if rigid is not None:
            angle = _negated(rigid.angle) if pose.flip else rigid.angle
            rigid = RigidPose(mapped(rigid.centre), angle)
        return replace(
            square, corners=tuple(Point2(x.value, y.value) for x, y in corners), pose=rigid
        )

    def feature_image(
        feature: ContactFeature | DetectedContactFeature | ActiveFeature,
    ) -> ContactFeature | DetectedContactFeature | ActiveFeature:
        if isinstance(feature, ActiveFeature):
            return replace(feature, point=mapped(feature.point))
        if isinstance(feature, DetectedContactFeature) and feature.normal is not None:
            raise ValueError(
                f"{feature.feature_id}: a detected pair contact's normal is not mapped"
            )
        return replace(
            feature,
            start=mapped(feature.start),
            end=None if feature.end is None else mapped(feature.end),
            wall=None if feature.wall is None else walls[feature.wall],
        )

    return replace(
        frame,
        squares=tuple(square_image(square) for square in frame.squares),
        features=tuple(feature_image(feature) for feature in frame.features),
    )


# --------------------------------------------------------------------------- command line


def _drawn_witness(n: int, view: str | None) -> tuple[str, dict[str, Any]]:
    relative = view or WITNESS.format(n=n)
    raw = (REPO / relative).read_bytes()
    text = (gzip.decompress(raw) if relative.endswith(".gz") else raw).decode("utf-8")
    document = load_yaml(text)
    if not isinstance(document, dict) or not isinstance(document.get("witness"), dict):
        raise TypeError(f"{relative} is not a witness document")
    return relative, document["witness"]


def decide_count(unit: tuple[int, str | None, bool]) -> dict[str, Any]:
    """One count's row: its drawn picture, that picture's decision and, when asked,
    whether the picture is `invariant`."""
    # The builder and the drawings record both import this module, so they are read
    # here, when a count is decided, rather than when it is imported.
    from devtools.build_known_best_atlas import frame_from_witness  # noqa: PLC0415

    n, view, check = unit
    relative, witness = _drawn_witness(n, view)
    frame = frame_from_witness(witness)
    row = {"n": n, "drawn": relative, **decide_frame(frame).record()}
    if check:
        row["invariant"] = invariant(
            frame_corners(frame), float(frame.container_side.projected)
        )
    return row


def drawn_views() -> dict[int, str]:
    """The repository-relative view path of each count whose default picture is its
    regularized view, from the drawings record."""
    from devtools.default_drawings import regularized_defaults  # noqa: PLC0415

    return {n: str(row["view"]) for n, row in regularized_defaults().items()}


def decide_counts(
    counts: Sequence[int], *, workers: int, invariance: bool = False
) -> list[dict[str, Any]]:
    views = drawn_views()
    units = [(n, views.get(n), invariance) for n in counts]
    if workers > 1 and len(units) > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            return list(pool.map(decide_count, units, chunksize=4))
    return [decide_count(unit) for unit in units]


def totals(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    stages = Counter(row["decided_by"] for row in rows)
    poses = Counter(Pose.from_record(row) for row in rows)
    summary: dict[str, Any] = {
        "counts": len(rows),
        "decided_by": {stage: stages[stage] for stage in STAGES},
        "identity": poses[IDENTITY],
        "poses": [
            {**pose.record(), "reads_as": DESCRIPTIONS[pose], "counts": poses[pose]}
            for pose in POSES
        ],
    }
    if any("invariant" in row for row in rows):
        summary["not_invariant"] = [row["n"] for row in rows if not row["invariant"]]
    return summary


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    command.add_argument("--n", type=int, nargs="+", help="counts (default 1..324)")
    command.add_argument(
        "--workers", type=int, default=os.cpu_count() or 1, help="processes (default: CPUs)"
    )
    command.add_argument(
        "--invariance",
        action="store_true",
        help="also decide each picture from all eight poses; exit 1 unless all draw the same",
    )
    command.add_argument("--json", action="store_true", help="print the decisions as JSON")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    rows = decide_counts(
        args.n or list(COUNTS), workers=args.workers, invariance=args.invariance
    )
    summary = totals(rows)
    failed = 1 if summary.get("not_invariant") else 0
    if args.json:
        document = {"format": FORMAT, "generated_by": GENERATOR, "totals": summary}
        print(json.dumps({**document, "counts": rows}, indent=1))
        return failed
    print(f"{'n':>4} {'rotate':>6} {'flip':>5}  {'decided by':<10}  quadrants UL UR LL LR")
    for row in rows:
        weights = " ".join(f"{weight:.4f}" for weight in row["quadrants"])
        print(
            f"{row['n']:>4} {row['rotate']:>6} {'yes' if row['flip'] else 'no':>5}  "
            f"{row['decided_by']:<10}  {weights}"
        )
    stages = ", ".join(f"{stage} {count}" for stage, count in summary["decided_by"].items())
    print(f"\n{summary['counts']} counts decided by stage: {stages}")
    print(f"identity: {summary['identity']}")
    for pose in summary["poses"]:
        flip = "flip" if pose["flip"] else "no flip"
        print(f"  rotate {pose['rotate']:>3}, {flip:<7} ({pose['reads_as']}): {pose['counts']}")
    if "not_invariant" in summary:
        broken = ", ".join(str(n) for n in summary["not_invariant"]) or "none"
        print(f"drawn differently from some pose: {broken}")
    return failed


if __name__ == "__main__":
    raise SystemExit(main())
