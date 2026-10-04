#!/usr/bin/env python3
"""Classify the known-best atlas by each n's position relative to the perfect squares.

The atlas triangle puts row k at n = (k-1)^2+1 .. k^2, which invites reading families off
a position: k^2-1 and k^2-2 as clean grids, k^2+1 as a 45-degree style, consecutive pairs
that look alike. This census measures what each of those readings would need, one record
per n: the side against a small closed-form library, the angle profile, the axis-aligned
grid part, the D4 symmetry, and how much of each packing reappears in the next one. It
then summarizes by offset from the nearest square and by triangle row, so a family either
shows in the numbers or does not.

Descriptive only. It reads retained witnesses as projected geometry and checks nothing:
no packing, side, or optimality claim is verified or upgraded here. The 176 `exact-grid`
records are canonical row-major subsets of an integer grid, so their arrangement is a
convention and only their side is evidence.

Usage:
    uv run --frozen python -m devtools.classify_known_best_families --update
    uv run --frozen python -m devtools.classify_known_best_families --check
"""

from __future__ import annotations

import argparse
import bisect
import itertools
import json
import math
from collections import Counter
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

import mpmath as mp
from strif import atomic_output_file

from sqpack import retained_json
from sqpack.witness import materialize_witness
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "atlas/known-best/manifest.json"
OUTPUT = ROOT / "campaign/explorations/X049-families-data/family-census.json"
GENERATOR = "python -m devtools.classify_known_best_families"
CONTRACT = "packing.squares:KnownBestFamilyCensus/v1"

PROJECTION_DIGITS = 30
"""Working digits for projecting a witness to poses; every output is rounded far coarser."""

SIDE_TOLERANCE = 1e-9
TIGHT_ANGLE_RADIANS = 1e-6
TIGHT_ANGLE_DEGREES = TIGHT_ANGLE_RADIANS * 180.0 / math.pi
LOOSE_ANGLE_DEGREES = 0.5
ANGLE_BANDS: tuple[tuple[str, float], ...] = (
    ("tight", TIGHT_ANGLE_DEGREES),
    ("loose", LOOSE_ANGLE_DEGREES),
)
"""Angle tolerances in degrees: 1e-6 radians, and half a degree."""

FACE_TOLERANCE = 1e-3
LATTICE_TOLERANCE = 1e-6
SYMMETRY_BANDS: tuple[tuple[str, float, float], ...] = (
    ("tight", 1e-6, 1e-6 * 180.0 / math.pi),
    ("near", 1e-3, 1e-3 * 180.0 / math.pi),
)
"""`(name, center tolerance, angle tolerance in degrees)` for the D4 symmetry test."""

SHARED_CENTER_TOLERANCE = 1e-3
SHARED_ANGLE_DEGREES = 1e-3 * 180.0 / math.pi

CLOSED_FORM_DENOMINATORS = (1, 2, 3, 4)
CLOSED_FORM_NUMERATOR_BOUND = 8
WIDE_COEFFICIENT_NUMERATOR_BOUND = 32
WIDE_CONSTANT_DENOMINATOR_BOUND = 16
SQRT2 = math.sqrt(2.0)

SUMMARY_OFFSETS = tuple(range(-3, 4))
SUMMARY_REMAINDERS = (0, 1, 2)
QUERIED_PAIRS: tuple[tuple[int, int], ...] = ((232, 233), (264, 265), (268, 269), (301, 302))
"""Consecutive pairs the atlas owner named as sharing a pattern; reported in full."""

ROUND_DIGITS = 12
ANGLE_DIGITS = 4


@dataclass(frozen=True)
class Pose:
    """One unit square: center and orientation folded into [0, 90) degrees."""

    x: float
    y: float
    angle: float


@dataclass(frozen=True)
class Geometry:
    """A packing as the census reads it: container side and square poses."""

    n: int
    side: float
    poses: tuple[Pose, ...]


@dataclass(frozen=True)
class Transform:
    """One D4 symmetry of the container, as a signed permutation matrix about its center."""

    name: str
    xx: int
    xy: int
    yx: int
    yy: int

    @property
    def reflects(self) -> bool:
        return self.xx * self.yy - self.xy * self.yx < 0

    def apply(self, pose: Pose, side: float) -> Pose:
        half = side / 2.0
        u, v = pose.x - half, pose.y - half
        angle = fold_degrees(-pose.angle) if self.reflects else pose.angle
        return Pose(
            self.xx * u + self.xy * v + half,
            self.yx * u + self.yy * v + half,
            angle,
        )


TRANSFORMS: tuple[Transform, ...] = (
    Transform("identity", 1, 0, 0, 1),
    Transform("rot90", 0, -1, 1, 0),
    Transform("rot180", -1, 0, 0, -1),
    Transform("rot270", 0, 1, -1, 0),
    Transform("flip-x", -1, 0, 0, 1),
    Transform("flip-y", 1, 0, 0, -1),
    Transform("flip-diagonal", 0, 1, 1, 0),
    Transform("flip-antidiagonal", 0, -1, -1, 0),
)
"""Rotations counterclockwise about the container center; `flip-x` sends x to side - x."""

_ALL_ELEMENTS = frozenset(transform.name for transform in TRANSFORMS)
GROUP_NAMES: dict[frozenset[str], str] = {
    frozenset({"identity"}): "trivial",
    frozenset({"identity", "rot180"}): "C2",
    frozenset({"identity", "flip-x"}): "D1-axis",
    frozenset({"identity", "flip-y"}): "D1-axis",
    frozenset({"identity", "flip-diagonal"}): "D1-diagonal",
    frozenset({"identity", "flip-antidiagonal"}): "D1-diagonal",
    frozenset({"identity", "rot180", "flip-x", "flip-y"}): "D2-axis",
    frozenset({"identity", "rot180", "flip-diagonal", "flip-antidiagonal"}): "D2-diagonal",
    frozenset({"identity", "rot90", "rot180", "rot270"}): "C4",
    _ALL_ELEMENTS: "D4",
}

ANCHORS: tuple[tuple[str, int, int], ...] = (
    ("lower-left", 0, 0),
    ("lower-right", 1, 0),
    ("upper-left", 0, 1),
    ("upper-right", 1, 1),
)
"""Container corners, as which walls a translation keeps fixed when the side grows."""


def fold_degrees(angle: float) -> float:
    """An orientation in [0, 90) degrees, with arithmetic dust at the seam sent to 0."""
    folded = angle % 90.0
    if folded >= 90.0 or min(folded, 90.0 - folded) < 1e-12:
        return 0.0
    return folded


def angle_gap(left: float, right: float) -> float:
    """Distance between two orientations on the 90-degree circle."""
    difference = abs(left - right) % 90.0
    return min(difference, 90.0 - difference)


def is_axis_aligned(pose: Pose, tolerance: float = TIGHT_ANGLE_DEGREES) -> bool:
    return angle_gap(pose.angle, 0.0) <= tolerance


def square_indices(n: int) -> dict[str, int]:
    """Both conventions for where n sits: floor square `m^2 + r`, nearest square `k^2 + d`.

    `k = round(sqrt n)` is never a tie for an integer n, because `(m + 1/2)^2` is not an
    integer, so the nearest square is the one with the smaller `|d|`.
    """
    m = math.isqrt(n)
    r = n - m * m
    k = m if r <= m else m + 1
    ceil_sqrt = m if r == 0 else m + 1
    return {"m": m, "r": r, "k": k, "d": n - k * k, "ceil_sqrt": ceil_sqrt}


def _small_rationals(bound: int) -> list[Fraction]:
    """Distinct rationals over `CLOSED_FORM_DENOMINATORS` with |numerator| <= bound."""
    return sorted(
        {
            Fraction(numerator, denominator)
            for denominator in CLOSED_FORM_DENOMINATORS
            for numerator in range(-bound, bound + 1)
        }
    )


@cache
def closed_form_library() -> tuple[tuple[float, Fraction, Fraction], ...]:
    """Every `a + b*sqrt(2)` with `a, b` rationals of denominator <= 4, |numerator| <= 8.

    `b = 0` is the plain rationals. Sorted by value, so a match is one bisection.
    """
    rationals = _small_rationals(CLOSED_FORM_NUMERATOR_BOUND)
    forms = [(float(a) + float(b) * SQRT2, a, b) for a in rationals for b in rationals]
    return tuple(sorted(forms))


@cache
def _library_values() -> tuple[float, ...]:
    return tuple(form[0] for form in closed_form_library())


def match_closed_form(value: float) -> tuple[Fraction, Fraction] | None:
    """The small-library form within `SIDE_TOLERANCE` of `value`, closest first, else None."""
    library, values = closed_form_library(), _library_values()
    start = bisect.bisect_left(values, value - SIDE_TOLERANCE)
    stop = bisect.bisect_right(values, value + SIDE_TOLERANCE)
    candidates = sorted(library[start:stop], key=lambda form: abs(form[0] - value))
    if not candidates:
        return None
    _value, a, b = candidates[0]
    return a, b


@cache
def wide_coefficients() -> tuple[Fraction, ...]:
    """The wide tier's sqrt(2) coefficients: denominator <= 4, |numerator| <= 32."""
    return tuple(_small_rationals(WIDE_COEFFICIENT_NUMERATOR_BOUND))


def match_wide_closed_form(value: float) -> tuple[Fraction, Fraction] | None:
    """`value` as `c + b*sqrt(2)` with c of denominator <= 16 and b from the wide set.

    The wide tier exists because the small library cannot reach the large 45-degree
    blocks (n = 233 is `8 + 11/2*sqrt(2)`) or the 3-4-5 rational sides (n = 50 is 53/7).
    Closest residual first, then the smaller `|b|`, so a plain rational wins a tie.
    """
    candidates: list[tuple[float, Fraction, Fraction, Fraction]] = []
    for coefficient in wide_coefficients():
        rest = value - float(coefficient) * SQRT2
        constant = Fraction(rest).limit_denominator(WIDE_CONSTANT_DENOMINATOR_BOUND)
        residual = abs(value - (float(constant) + float(coefficient) * SQRT2))
        if residual <= SIDE_TOLERANCE:
            candidates.append((residual, abs(coefficient), coefficient, constant))
    if not candidates:
        return None
    _residual, _size, coefficient, constant = min(candidates)
    return constant, coefficient


def _expression(constant: Fraction, coefficient: Fraction) -> str:
    if coefficient == 0:
        return str(constant)
    magnitude = abs(coefficient)
    radical = "sqrt(2)" if magnitude == 1 else f"{magnitude}*sqrt(2)"
    if constant == 0:
        return radical if coefficient > 0 else f"-{radical}"
    sign = "+" if coefficient > 0 else "-"
    return f"{constant} {sign} {radical}"


def closed_form_record(side: float, m: int) -> dict[str, Any] | None:
    """The side as `m + a + b*sqrt(2)`: the small library first, then the wide tier.

    `a` and `b` are the form of `side - m`, as the small library tests it; the
    expression is the whole side. The residual is reported to three significant digits
    so a reader can see how far inside the tolerance a match sits.
    """
    small = match_closed_form(side - m)
    if small is not None:
        tier, (a, b) = "small", small
    else:
        wide = match_wide_closed_form(side)
        if wide is None:
            return None
        tier, a, b = "wide", wide[0] - m, wide[1]
    constant = a + m
    if b != 0:
        kind = "sqrt2"
    elif constant.denominator == 1:
        kind = "integer"
    else:
        kind = "rational"
    residual = abs(side - (float(constant) + float(b) * SQRT2))
    return {
        "tier": tier,
        "kind": kind,
        "a": str(a),
        "b": str(b),
        "side_expression": _expression(constant, b),
        "residual": float(f"{residual:.3g}"),
    }


class CenterIndex:
    """Square centers bucketed by unit cell, for tolerance lookups without an n^2 scan."""

    def __init__(self, poses: Sequence[Pose]) -> None:
        self.poses = poses
        self.cells: dict[tuple[int, int], list[int]] = {}
        for index, pose in enumerate(poses):
            self.cells.setdefault((math.floor(pose.x), math.floor(pose.y)), []).append(index)

    def near(self, x: float, y: float, radius: float) -> Iterator[int]:
        for cell_x in range(math.floor(x - radius), math.floor(x + radius) + 1):
            for cell_y in range(math.floor(y - radius), math.floor(y + radius) + 1):
                yield from self.cells.get((cell_x, cell_y), ())

    def match(self, pose: Pose, center_tolerance: float, angle_tolerance: float) -> int | None:
        """The square whose center is within the tolerance on each axis, at a matching angle.

        Two unit squares with disjoint interiors have centers at least 1 apart, so with any
        tolerance used here at most one square can match.
        """
        for index in self.near(pose.x, pose.y, center_tolerance):
            other = self.poses[index]
            if (
                abs(other.x - pose.x) <= center_tolerance
                and abs(other.y - pose.y) <= center_tolerance
                and angle_gap(other.angle, pose.angle) <= angle_tolerance
            ):
                return index
        return None


class _UnionFind:
    def __init__(self, size: int) -> None:
        self.parents = list(range(size))

    def find(self, item: int) -> int:
        while self.parents[item] != item:
            self.parents[item] = self.parents[self.parents[item]]
            item = self.parents[item]
        return item

    def union(self, left: int, right: int) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parents[max(left_root, right_root)] = min(left_root, right_root)

    def groups(self) -> list[list[int]]:
        grouped: dict[int, list[int]] = {}
        for item in range(len(self.parents)):
            grouped.setdefault(self.find(item), []).append(item)
        return [grouped[root] for root in sorted(grouped)]


def witness_geometry(witness: Mapping[str, Any]) -> Geometry:
    """Project a witness to poses through the project's materializer, at fixed digits.

    The trigonometry is mpmath's rather than the platform libm's, so the retained census
    does not depend on which machine regenerated it.
    """
    with mp.workdps(PROJECTION_DIGITS):
        squares, side = materialize_witness(witness, digits=PROJECTION_DIGITS)
        poses: list[Pose] = []
        for corners in squares:
            center_x = mp.fsum(x for x, _y in corners) / 4
            center_y = mp.fsum(y for _x, y in corners) / 4
            edge_x = corners[1][0] - corners[0][0]
            edge_y = corners[1][1] - corners[0][1]
            angle = float(mp.degrees(mp.atan2(edge_y, edge_x)))
            poses.append(Pose(float(center_x), float(center_y), fold_degrees(angle)))
        return Geometry(int(witness["n"]), float(side), tuple(poses))


@cache
def manifest_entries() -> dict[int, dict[str, Any]]:
    """The atlas entries keyed by n, read once per process."""
    atlas = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]
    return {int(entry["n"]): entry for entry in atlas["entries"]}


@cache
def load_geometry(n: int) -> Geometry:
    """One atlas witness, parsed and projected without schema validation.

    Schema validation is what `load_witness` adds, and it is ten of the twelve seconds a
    full load of the 324 witnesses costs; the atlas's own checks already own it.
    """
    entry = manifest_entries()[n]
    document = load_yaml((ROOT / entry["witness"]["path"]).read_text(encoding="utf-8"))
    geometry = witness_geometry(document["witness"])
    if geometry.n != n or len(geometry.poses) != n:
        raise ValueError(f"n={n}: witness holds n={geometry.n} with {len(geometry.poses)}")
    return geometry


def _angle_classes(angles: Iterable[float], tolerance: float) -> list[list[float]]:
    """Single-linkage classes on the 90-degree circle; a class across the seam is unwrapped."""
    ordered = sorted(angles)
    groups: list[list[float]] = []
    for angle in ordered:
        if groups and angle - groups[-1][-1] <= tolerance:
            groups[-1].append(angle)
        else:
            groups.append([angle])
    if len(groups) > 1 and ordered[0] + 90.0 - ordered[-1] <= tolerance:
        groups[0] = [angle - 90.0 for angle in groups.pop()] + groups[0]
    return groups


def _class_angle(members: Sequence[float]) -> float:
    mean = math.fsum(members) / len(members)
    rounded = round(mean + 90.0 if mean < 0 else mean, ANGLE_DIGITS)
    return 0.0 if rounded >= 90.0 else rounded


def angle_profile(poses: Sequence[Pose]) -> dict[str, Any]:
    """Axis-aligned, 45-degree, and other counts, and angle classes, in both bands."""
    angles = [pose.angle for pose in poses]
    profile: dict[str, Any] = {
        "axis_aligned": {},
        "forty_five": {},
        "other": {},
        "class_count": {},
    }
    for name, tolerance in ANGLE_BANDS:
        axis = sum(angle_gap(angle, 0.0) <= tolerance for angle in angles)
        diagonal = sum(angle_gap(angle, 45.0) <= tolerance for angle in angles)
        profile["axis_aligned"][name] = axis
        profile["forty_five"][name] = diagonal
        profile["other"][name] = len(angles) - axis - diagonal
        profile["class_count"][name] = len(_angle_classes(angles, tolerance))
    profile["classes_loose"] = sorted(
        (
            {"angle_degrees": _class_angle(members), "count": len(members)}
            for members in _angle_classes(angles, LOOSE_ANGLE_DEGREES)
        ),
        key=lambda item: (item["angle_degrees"], item["count"]),
    )
    return profile


def tilt_signature(profile: Mapping[str, Any]) -> list[dict[str, Any]]:
    """The loose angle classes whose mean is not within the loose band of the axes."""
    return [
        item
        for item in profile["classes_loose"]
        if angle_gap(item["angle_degrees"], 0.0) > LOOSE_ANGLE_DEGREES
    ]


def tilted_layout(poses: Sequence[Pose]) -> dict[str, Any]:
    """Where the visibly tilted squares sit: the principal axis of their centers.

    Visibly tilted means outside the loose axis band. The direction is the major axis of
    the centers' covariance in degrees on [0, 180), and elongation is the square root of
    the major-to-minor variance ratio, so a band reads as a direction with a large
    elongation, and a blob or a symmetric pair of bands as an elongation near 1.
    """
    tilted = [pose for pose in poses if not is_axis_aligned(pose, LOOSE_ANGLE_DEGREES)]
    count = len(tilted)
    if count < 2:
        return {"count": count, "principal_direction_degrees": None, "elongation": None}
    mean_x = math.fsum(pose.x for pose in tilted) / count
    mean_y = math.fsum(pose.y for pose in tilted) / count
    sxx = math.fsum((pose.x - mean_x) ** 2 for pose in tilted) / count
    syy = math.fsum((pose.y - mean_y) ** 2 for pose in tilted) / count
    sxy = math.fsum((pose.x - mean_x) * (pose.y - mean_y) for pose in tilted) / count
    with mp.workdps(PROJECTION_DIGITS):
        direction = float(mp.degrees(mp.atan2(2 * sxy, sxx - syy)) / 2) % 180.0
    spread = math.sqrt(((sxx - syy) / 2) ** 2 + sxy**2)
    major, minor = (sxx + syy) / 2 + spread, (sxx + syy) / 2 - spread
    elongation = math.sqrt(major / minor) if minor > 1e-12 else None
    return {
        "count": count,
        "principal_direction_degrees": round(direction, 2) % 180.0,
        "elongation": None if elongation is None else round(elongation, 3),
    }


def same_tilt_signature(left: Sequence[Mapping[str, Any]], right: Sequence[Any]) -> bool:
    """Both tilted, with equal class counts at angles within the loose band."""
    return (
        bool(left)
        and len(left) == len(right)
        and all(
            a["count"] == b["count"]
            and angle_gap(a["angle_degrees"], b["angle_degrees"]) <= LOOSE_ANGLE_DEGREES
            for a, b in zip(left, right, strict=True)
        )
    )


def _on_lattice(value: float) -> bool:
    return abs(value - round(value)) <= LATTICE_TOLERANCE


def _face_adjacent(left: Pose, right: Pose) -> bool:
    across_x, across_y = abs(left.x - right.x), abs(left.y - right.y)
    return (abs(across_x - 1.0) <= FACE_TOLERANCE and across_y <= FACE_TOLERANCE) or (
        abs(across_y - 1.0) <= FACE_TOLERANCE and across_x <= FACE_TOLERANCE
    )


def axis_structure(geometry: Geometry) -> dict[str, Any]:
    """The axis-aligned part: its largest face-sharing component, and corner lattices."""
    axis = [pose for pose in geometry.poses if is_axis_aligned(pose)]
    index = CenterIndex(axis)
    components = _UnionFind(len(axis))
    for left, pose in enumerate(axis):
        for right in index.near(pose.x, pose.y, 1.0 + FACE_TOLERANCE):
            if right > left and _face_adjacent(pose, axis[right]):
                components.union(left, right)
    groups = components.groups()
    largest: dict[str, Any] = {"size": 0, "rows": 0, "columns": 0, "filled_rectangle": False}
    if groups:
        biggest = max(groups, key=len)
        xs = [axis[member].x for member in biggest]
        ys = [axis[member].y for member in biggest]
        rows = round(max(ys) - min(ys)) + 1
        columns = round(max(xs) - min(xs)) + 1
        largest = {
            "size": len(biggest),
            "rows": rows,
            "columns": columns,
            "filled_rectangle": len(biggest) == rows * columns,
        }
    side = geometry.side
    corners = dict.fromkeys((name for name, _x, _y in ANCHORS), 0)
    anywhere = 0
    for pose in axis:
        on_x = (_on_lattice(pose.x - 0.5), _on_lattice(side - 0.5 - pose.x))
        on_y = (_on_lattice(pose.y - 0.5), _on_lattice(side - 0.5 - pose.y))
        hits = [name for name, at_x, at_y in ANCHORS if on_x[at_x] and on_y[at_y]]
        for name in hits:
            corners[name] += 1
        anywhere += bool(hits)
    return {
        "axis_aligned": len(axis),
        "component_count": len(groups),
        "largest_component": largest,
        "corner_lattice": {**corners, "any": anywhere, "best": max(corners.values())},
    }


def symmetry(geometry: Geometry, center_tolerance: float, angle_tolerance: float) -> dict:
    """The D4 elements that map the packing onto itself, and the subgroup's name.

    A rotation keeps a folded orientation; a reflection negates it modulo 90 degrees.
    """
    index = CenterIndex(geometry.poses)
    elements = [
        transform.name
        for transform in TRANSFORMS
        if all(
            index.match(transform.apply(pose, geometry.side), center_tolerance, angle_tolerance)
            is not None
            for pose in geometry.poses
        )
    ]
    return {
        "group": GROUP_NAMES.get(frozenset(elements), "not-a-subgroup"),
        "elements": elements,
    }


def shared_structure(current: Geometry, following: Geometry) -> dict[str, Any]:
    """How many squares of `current` reappear in `following`, under D4 and a corner anchor.

    Each D4 image of `current` is translated so one container corner stays put while the
    side changes, then matched square by square. The best `(matched, matched_tilted)` is
    reported with the first transform and anchor reaching it; `max_tilted_matched` is the
    best tilted count over all 32 alignments, which need not be the same one. Tilted here
    means outside the loose axis band. `embeds` says every square of `current` reappears:
    for consecutive n, `following` is `current` plus one square; for an L parent, the
    child is the parent plus its L.
    """
    index = CenterIndex(following.poses)
    growth = following.side - current.side
    tilted = [not is_axis_aligned(pose, LOOSE_ANGLE_DEGREES) for pose in current.poses]
    best: tuple[int, int] = (-1, -1)
    best_alignment = ("", "")
    max_tilted = 0
    for transform in TRANSFORMS:
        images = [transform.apply(pose, current.side) for pose in current.poses]
        for anchor, shift_x, shift_y in ANCHORS:
            matched = matched_tilted = 0
            for image, is_tilted in zip(images, tilted, strict=True):
                moved = Pose(
                    image.x + shift_x * growth, image.y + shift_y * growth, image.angle
                )
                if (
                    index.match(moved, SHARED_CENTER_TOLERANCE, SHARED_ANGLE_DEGREES)
                    is not None
                ):
                    matched += 1
                    matched_tilted += is_tilted
            max_tilted = max(max_tilted, matched_tilted)
            if (matched, matched_tilted) > best:
                best = (matched, matched_tilted)
                best_alignment = (transform.name, anchor)
    return {
        "matched": best[0],
        "matched_tilted": best[1],
        "tilted_in_n": sum(tilted),
        "max_tilted_matched": max_tilted,
        "fraction_of_n": round(best[0] / current.n, 6),
        "transform": best_alignment[0],
        "anchor": best_alignment[1],
        "embeds": best[0] == current.n,
    }


def _rounded(value: float) -> float:
    result = round(value, ROUND_DIGITS)
    return 0.0 if result == 0 else result


def _equal_sides(left: float, right: float) -> bool:
    return abs(left - right) <= SIDE_TOLERANCE


@cache
def manifest_sides() -> dict[int, float]:
    """Every atlas side by n, from the manifest's reported_side."""
    return {n: float(entry["reported_side"]) for n, entry in manifest_entries().items()}


def l_step(side: float) -> int:
    """Squares the L construction adds to a packing of this side: 2*floor(side) + 1.

    The L construction (DS7, section 2): if n' squares fit in side s', then
    n' + 2*floor(s') + 1 fit in s' + 1, by laying an L of unit squares along two walls.
    The floor is taken within `SIDE_TOLERANCE`, so a numerically integer side counts whole.
    """
    return 2 * math.floor(side + SIDE_TOLERANCE) + 1


def l_candidates(n: int, sides: Mapping[int, float]) -> list[int]:
    """Every smaller n' whose L construction lands on exactly n squares."""
    return [parent for parent in range(1, n) if n - parent == l_step(sides[parent])]


def l_parent(n: int, sides: Mapping[int, float]) -> int | None:
    """The n' that n is an L-extension of: n - n' = 2*floor(side(n')) + 1 and side + 1.

    At most one n' qualifies, since side(n) fixes floor(side(n')); the largest is taken
    should a tolerance edge ever admit two.
    """
    parents = [
        parent
        for parent in l_candidates(n, sides)
        if _equal_sides(sides[n] - sides[parent], 1.0)
    ]
    return max(parents) if parents else None


def l_chain(n: int, sides: Mapping[int, float]) -> tuple[int, int]:
    """`(root, length)`: follow `l_parent` down to a record that has none."""
    current, length = n, 0
    while (parent := l_parent(current, sides)) is not None:
        current, length = parent, length + 1
    return current, length


def l_bound(n: int, sides: Mapping[int, float]) -> dict[str, Any] | None:
    """The best side the L construction offers n from a smaller record, and the margin.

    The margin is `side(n') + 1 - side(n)`: zero for an L-extension, positive where the
    record beats the construction, and negative only if the atlas holds a side the
    construction would improve on.
    """
    candidates = l_candidates(n, sides)
    if not candidates:
        return None
    best = min(candidates, key=lambda parent: (sides[parent], -parent))
    return {
        "from": best,
        "side": _rounded(sides[best] + 1.0),
        "margin": _rounded(sides[best] + 1.0 - sides[n]),
    }


def entry_record(n: int, geometry_of: Callable[[int], Geometry]) -> dict[str, Any]:
    """Everything the census says about one n; reads n - 1 and n + 1 for the pair fields."""
    entries = manifest_entries()
    entry = entries[n]
    geometry = geometry_of(n)
    side_text = str(entry["reported_side"])
    side = float(side_text)
    if not _equal_sides(side, geometry.side):
        raise ValueError(f"n={n}: manifest side {side_text} disagrees with the witness")
    indices = square_indices(n)
    m = indices["m"]
    previous = geometry_of(n - 1) if n - 1 in entries else None
    following = geometry_of(n + 1) if n + 1 in entries else None
    profile = angle_profile(geometry.poses)
    tilted = n - profile["axis_aligned"]["tight"]
    shared = None
    same_signature = None
    if following is not None:
        shared = shared_structure(geometry, following)
        same_signature = same_tilt_signature(
            tilt_signature(profile), tilt_signature(angle_profile(following.poses))
        )
    sides = manifest_sides()
    parent = l_parent(n, sides)
    root, length = l_chain(n, sides)
    parent_embeds = (
        None if parent is None else shared_structure(geometry_of(parent), geometry)["embeds"]
    )
    return {
        "n": n,
        **indices,
        "side": side_text,
        "side_minus_sqrt_n": _rounded(side - math.sqrt(n)),
        "side_minus_m": _rounded(side - m),
        "integer_side": _equal_sides(side, indices["ceil_sqrt"]),
        "side_equals_previous": None if previous is None else _equal_sides(previous.side, side),
        "side_equals_next": None if following is None else _equal_sides(following.side, side),
        "closed_form": closed_form_record(side, m),
        "tilted": tilted,
        "tilted_loose": n - profile["axis_aligned"]["loose"],
        "tilted_layout": tilted_layout(geometry.poses),
        "angles": profile,
        "axis_grid": axis_structure(geometry),
        "symmetry": {
            name: symmetry(geometry, center_tolerance, angle_tolerance)
            for name, center_tolerance, angle_tolerance in SYMMETRY_BANDS
        },
        "shared_with_next": shared,
        "same_tilt_signature_as_next": same_signature,
        "l_parent": parent,
        "l_chain_root": root,
        "l_chain_length": length,
        "l_bound": l_bound(n, sides),
        "l_parent_embeds": parent_embeds,
        "source": {
            "kind": entry["source"]["kind"],
            "method": entry["witness"]["method"],
            "coordinate_provenance": entry["witness"]["coordinate_provenance"],
        },
    }


def build_records(ns: Iterable[int] | None = None) -> list[dict[str, Any]]:
    """Records for the requested n (default: the whole atlas), in ascending order."""
    selected = sorted(manifest_entries()) if ns is None else sorted(set(ns))
    return [entry_record(n, load_geometry) for n in selected]


def _closed_tier(record: Mapping[str, Any]) -> str | None:
    closed = record["closed_form"]
    return None if closed is None else closed["tier"]


def _member(record: Mapping[str, Any]) -> dict[str, Any]:
    closed = record["closed_form"]
    return {
        "n": record["n"],
        "k": record["k"],
        "d": record["d"],
        "side": record["side"],
        "integer_side": record["integer_side"],
        "tilted": record["tilted"],
        "tilted_loose": record["tilted_loose"],
        "forty_five": record["angles"]["forty_five"]["tight"],
        "closed_form": None if closed is None else closed["side_expression"],
        "closed_form_tier": _closed_tier(record),
        "symmetry": record["symmetry"]["tight"]["group"],
        "symmetry_near": record["symmetry"]["near"]["group"],
        "source_kind": record["source"]["kind"],
    }


def _family(members: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "count": len(members),
        "integer_side": sum(record["integer_side"] for record in members),
        "non_integer_n": [record["n"] for record in members if not record["integer_side"]],
        "with_tilted": sum(record["tilted"] > 0 for record in members),
        "with_tilted_loose": sum(record["tilted_loose"] > 0 for record in members),
        "with_forty_five": [
            record["n"] for record in members if record["angles"]["forty_five"]["tight"]
        ],
        "closed_form_non_integer": [
            record["n"]
            for record in members
            if record["closed_form"] is not None and not record["integer_side"]
        ],
        "symmetry_groups": _counts(record["symmetry"]["tight"]["group"] for record in members),
        "members": [_member(record) for record in members],
    }


def _row(k: int, records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Triangle row k: n = (k-1)^2+1 .. k^2, where every n has ceil(sqrt n) = k.

    Field names here are a stable interface: the asymptotics lane reads
    `grid_held_width` against the O(k^(3/5)) bound.
    """
    first, last = (k - 1) ** 2 + 1, k * k
    members = [record for record in records if first <= record["n"] <= last]
    held = [record["n"] for record in members if record["integer_side"]]
    smallest = min(held) if held else None
    small = [record for record in members if _closed_tier(record) == "small"]
    matched = [record for record in members if record["closed_form"] is not None]
    widest = max(members, key=lambda record: (record["side_minus_sqrt_n"], -record["n"]))
    mid = next((record for record in members if record["n"] == (k - 1) ** 2 + k - 1), None)
    return {
        "k": k,
        "first_n": first,
        "last_n": last,
        "count": len(members),
        "row_max_excess": widest["side_minus_sqrt_n"],
        "row_max_excess_n": widest["n"],
        "mid_row_n": None if mid is None else mid["n"],
        "mid_row_excess": None if mid is None else mid["side_minus_m"],
        "grid_held_width": len(held),
        "grid_held_smallest_n": smallest,
        "grid_held_contiguous_to_k_squared": bool(held)
        and held == list(range(min(held), last + 1)),
        "closed_form_count": len(small),
        "closed_form_non_integer_count": sum(not record["integer_side"] for record in small),
        "closed_form_any_tier_count": len(matched),
        "closed_form_any_tier_non_integer_count": sum(
            not record["integer_side"] for record in matched
        ),
        "tilted_n_count": sum(record["tilted"] > 0 for record in members),
        "tilted_loose_n_count": sum(record["tilted_loose"] > 0 for record in members),
    }


def _pair(record: Mapping[str, Any], following: Mapping[str, Any]) -> dict[str, Any]:
    shared = record["shared_with_next"]
    return {
        "n": record["n"],
        "next": following["n"],
        "sides": [record["side"], following["side"]],
        "offsets": [[record["k"], record["d"]], [following["k"], following["d"]]],
        "tilted": [record["tilted"], following["tilted"]],
        "tilted_loose": [record["tilted_loose"], following["tilted_loose"]],
        "tilted_layout": [record["tilted_layout"], following["tilted_layout"]],
        "forty_five": [
            record["angles"]["forty_five"]["tight"],
            following["angles"]["forty_five"]["tight"],
        ],
        "symmetry": [
            record["symmetry"]["tight"]["group"],
            following["symmetry"]["tight"]["group"],
        ],
        "symmetry_near": [
            record["symmetry"]["near"]["group"],
            following["symmetry"]["near"]["group"],
        ],
        "side_equal": record["side_equals_next"],
        "same_tilt_signature": record["same_tilt_signature_as_next"],
        "tilt_signatures": [
            tilt_signature(record["angles"]),
            tilt_signature(following["angles"]),
        ],
        "shared": shared,
        "l_parent": [record["l_parent"], following["l_parent"]],
        "l_chain": [
            [record["l_chain_root"], record["l_chain_length"]],
            [following["l_chain_root"], following["l_chain_length"]],
        ],
        "l_bound": [record["l_bound"], following["l_bound"]],
        "source_kinds": [record["source"]["kind"], following["source"]["kind"]],
    }


def _pairs_summary(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_n = {record["n"]: record for record in records}
    adjacent = [
        (record, by_n[record["n"] + 1]) for record in records if record["n"] + 1 in by_n
    ]
    equal = [(left, right) for left, right in adjacent if left["side_equals_next"]]
    tilted_both = [
        (left, right)
        for left, right in adjacent
        if left["tilted_loose"] and right["tilted_loose"]
    ]
    return {
        "adjacent_pairs": len(adjacent),
        "equal_side": {
            "count": len(equal),
            "integer_side": sum(left["integer_side"] for left, _right in equal),
            "integer_side_below_k_squared_minus_2": [
                left["n"]
                for left, _right in equal
                if left["integer_side"] and left["ceil_sqrt"] ** 2 - left["n"] >= 3
            ],
            "non_integer": [
                _pair(left, right) for left, right in equal if not left["integer_side"]
            ],
            "integer_side_n": [left["n"] for left, _right in equal if left["integer_side"]],
        },
        "embeds_in_next": {
            "count": sum(left["shared_with_next"]["embeds"] for left, _right in adjacent),
            "both_non_grid_n": [
                left["n"]
                for left, right in adjacent
                if left["shared_with_next"]["embeds"]
                and left["source"]["kind"] != "exact-grid"
                and right["source"]["kind"] != "exact-grid"
            ],
        },
        "both_tilted": {
            "count": len(tilted_both),
            "same_tilt_signature_n": [
                left["n"] for left, _right in tilted_both if left["same_tilt_signature_as_next"]
            ],
            "pairs": [
                {
                    "n": left["n"],
                    "tilted_loose": [left["tilted_loose"], right["tilted_loose"]],
                    "matched": left["shared_with_next"]["matched"],
                    "matched_tilted": left["shared_with_next"]["matched_tilted"],
                    "max_tilted_matched": left["shared_with_next"]["max_tilted_matched"],
                    "same_tilt_signature": left["same_tilt_signature_as_next"],
                    "side_equal": left["side_equals_next"],
                }
                for left, right in tilted_both
            ],
        },
    }


def _counts(values: Iterable[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


CONVENTIONS = {
    "triangle_row": (
        "row k holds n = (k-1)^2+1 .. k^2, every n with ceil(sqrt n) = k; `rows`, "
        "grid_held_width and the row_max/mid_row fields use it"
    ),
    "nearest_square": (
        "n = k^2 + d with k = round(sqrt n); `by_nearest_offset`, excess_table, "
        "gobel_strip_check, delta_plateau and best_known_d_max index n this way"
    ),
    "floor_square": "n = m^2 + r with m = floor(sqrt n); `by_floor_remainder` and L columns",
}
"""How each summary block indexes n, recorded once so two conventions cannot blur."""

EXCESS_OFFSETS = tuple(range(-3, 4))
EXCESS_ROWS = tuple(range(2, 18))
GOEBEL_ROWS = tuple(range(5, 18))
PLATEAU_EXCESS = 5 * SQRT2 / 2 - 3
D_MAX_ROWS = tuple(range(2, 19))
BAND_ELONGATION = 5.0
BAND_DIRECTION_TOLERANCE = 10.0


def _diagonal_band(record: Mapping[str, Any]) -> bool:
    """Whether the visibly tilted squares lie in an elongated set along a diagonal."""
    layout = record["tilted_layout"]
    elongation, direction = layout["elongation"], layout["principal_direction_degrees"]
    if direction is None or (elongation is not None and elongation < BAND_ELONGATION):
        return False
    return min(abs(direction - 45.0), abs(direction - 135.0)) <= BAND_DIRECTION_TOLERANCE


def goebel_offset(k: int) -> int:
    """d_G(k) = 3 - k + floor((k - 2) * sqrt 2), the floor taken exactly as an isqrt."""
    return 3 - k + math.isqrt(2 * (k - 2) ** 2)


def _side_minus(by_n: Mapping[int, Mapping[str, Any]], n: int, k: int) -> float | None:
    return _rounded(float(by_n[n]["side"]) - k) if n in by_n else None


def _asymptotics(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Tables the asymptotics lane reads, all in the nearest-square convention n = k^2 + d."""
    by_n = {record["n"]: record for record in records}
    plateau = [
        by_n[k * k + 1]
        for k in range(1, math.isqrt(max(by_n)) + 1)
        if k * k + 1 in by_n
        and _equal_sides(float(by_n[k * k + 1]["side"]) - k, PLATEAU_EXCESS)
    ]
    return {
        "excess_table": {
            "description": "side(k^2 + d) - k; null where k^2 + d is outside the atlas",
            "offsets": list(EXCESS_OFFSETS),
            "rows": [
                {"k": k, "excess": [_side_minus(by_n, k * k + d, k) for d in EXCESS_OFFSETS]}
                for k in EXCESS_ROWS
            ],
        },
        "gobel_strip_check": {
            "description": (
                "d_G(k) = 3 - k + floor((k - 2)*sqrt 2) and n = k^2 + d_G(k); whether "
                f"side(n) - k = 1/sqrt(2) within {SIDE_TOLERANCE}, and n's 45-degree squares"
            ),
            "rows": [
                {
                    "k": k,
                    "d_G": goebel_offset(k),
                    "n": k * k + goebel_offset(k),
                    "side_minus_k": _side_minus(by_n, k * k + goebel_offset(k), k),
                    "equals_inverse_root_two": _equal_sides(
                        float(by_n[k * k + goebel_offset(k)]["side"]) - k, SQRT2 / 2
                    ),
                    "forty_five": by_n[k * k + goebel_offset(k)]["angles"]["forty_five"][
                        "tight"
                    ],
                }
                for k in GOEBEL_ROWS
                if k * k + goebel_offset(k) in by_n
            ],
        },
        "delta_plateau": {
            "description": (
                f"k with side(k^2 + 1) - k = 5/sqrt(2) - 3 within {SIDE_TOLERANCE}, and "
                "those records' axis-aligned and 45-degree square counts at 1e-6 radians"
            ),
            "k": [record["k"] for record in plateau],
            "members": [
                {
                    "k": record["k"],
                    "n": record["n"],
                    "axis_aligned": record["angles"]["axis_aligned"]["tight"],
                    "forty_five": record["angles"]["forty_five"]["tight"],
                }
                for record in plateau
            ],
        },
        "best_known_d_max": {
            "description": (
                "the largest d >= 0 with side(k^2 - d) = k within the side tolerance, read "
                "from the atlas's best-known sides: a best-known value, not a proved one"
            ),
            "rows": [
                {
                    "k": k,
                    "d_max": max(
                        d
                        for d in range(k * k)
                        if k * k - d in by_n and _equal_sides(float(by_n[k * k - d]["side"]), k)
                    ),
                }
                for k in D_MAX_ROWS
                if k * k in by_n
            ],
        },
    }


def _l_chains(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Every chain of one or more L steps, from its root, in root order.

    A parent has at most one child, since the child is the parent plus a fixed count, so
    chains are paths rather than trees.
    """
    by_n = {record["n"]: record for record in records}
    children = {record["l_parent"]: record["n"] for record in records if record["l_parent"]}
    chains = []
    for record in records:
        if record["l_parent"] is None and record["n"] in children:
            chain = [record["n"]]
            while chain[-1] in children:
                chain.append(children[chain[-1]])
            chains.append(
                {
                    "root": chain[0],
                    "length": len(chain) - 1,
                    "n": chain,
                    "integer_side": by_n[chain[0]]["integer_side"],
                    "parent_embeds": [by_n[member]["l_parent_embeds"] for member in chain[1:]],
                }
            )
    return chains


def _l_columns(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """The left-justified triangle's columns, n = m^2 + j, and where L steps hold in them.

    A non-integer side m' + f steps to (m' + 1)^2 + j, the same column one row down; an
    integer side steps two columns right. So a break is a non-integer record whose column
    predecessor is also non-integer and is not its L parent.
    """
    columns = []
    for j in sorted({record["r"] for record in records}):
        members = [record for record in records if record["r"] == j]
        steps = list(itertools.pairwise(members))
        breaks = [
            {
                "n": member["n"],
                "predecessor": prior["n"],
                "l_bound": member["l_bound"],
            }
            for prior, member in steps
            if not member["integer_side"]
            and not prior["integer_side"]
            and member["l_parent"] != prior["n"]
        ]
        columns.append(
            {
                "j": j,
                "n": [record["n"] for record in members],
                "integer_side_n": [record["n"] for record in members if record["integer_side"]],
                "l_from_predecessor_n": [
                    member["n"] for prior, member in steps if member["l_parent"] == prior["n"]
                ],
                "breaks": breaks,
                "closed_among_non_integer": not breaks,
            }
        )
    return columns


def _l_summary(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    extensions = [record for record in records if record["l_parent"] is not None]
    non_integer = [record for record in extensions if not record["integer_side"]]
    bounded = [record for record in records if record["l_bound"] is not None]
    return {
        "extensions": len(extensions),
        "extensions_integer_side": len(extensions) - len(non_integer),
        "extensions_non_integer": len(non_integer),
        "non_integer_extension_n": [record["n"] for record in non_integer],
        "non_integer_parent_embeds": _counts(
            str(record["l_parent_embeds"]).lower() for record in non_integer
        ),
        "with_bound": len(bounded),
        "beats_bound": [
            {"n": record["n"], **record["l_bound"]}
            for record in bounded
            if record["l_bound"]["margin"] > SIDE_TOLERANCE
        ],
        "bound_violations": [
            {"n": record["n"], **record["l_bound"]}
            for record in bounded
            if record["l_bound"]["margin"] < -SIDE_TOLERANCE
        ],
        "chains": _l_chains(records),
        "columns": _l_columns(records),
    }


def _closed_form_families(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Matched sides grouped by the form of `side - m`, largest group first.

    A family in this sense is a construction that keeps its shape while the grid around
    it grows by one row and column: the same `side - m` at successive m.
    """
    groups: dict[tuple[Fraction, Fraction], list[Mapping[str, Any]]] = {}
    for record in records:
        closed = record["closed_form"]
        if closed is not None:
            key = (Fraction(closed["a"]), Fraction(closed["b"]))
            groups.setdefault(key, []).append(record)
    ordered = sorted(groups.items(), key=lambda item: (-len(item[1]), item[0]))
    return [
        {
            "side_minus_m": _expression(a, b),
            "count": len(members),
            "n": [record["n"] for record in members],
            "m": [record["m"] for record in members],
            "r": [record["r"] for record in members],
            "d": [record["d"] for record in members],
        }
        for (a, b), members in ordered
    ]


def summary(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    by_n = {record["n"]: record for record in records}
    offsets = sorted({record["d"] for record in records})
    non_grid = [record for record in records if record["source"]["kind"] != "exact-grid"]
    closed = [record for record in records if record["closed_form"] is not None]
    return {
        "conventions": CONVENTIONS,
        **_asymptotics(records),
        "records": len(records),
        "source_kinds": _counts(record["source"]["kind"] for record in records),
        "by_nearest_offset": [
            {"d": d, **_family([record for record in records if record["d"] == d])}
            for d in SUMMARY_OFFSETS
        ],
        "by_floor_remainder": [
            {"r": r, **_family([record for record in records if record["r"] == r])}
            for r in SUMMARY_REMAINDERS
        ],
        "integer_side_by_nearest_offset": [
            {
                "d": d,
                "count": sum(record["d"] == d for record in records),
                "integer_side": sum(
                    record["d"] == d and record["integer_side"] for record in records
                ),
            }
            for d in offsets
        ],
        "rows": [_row(k, records) for k in range(1, math.isqrt(max(by_n)) + 1)],
        "closed_form": {
            "matched": len(closed),
            "by_tier": _counts(record["closed_form"]["tier"] for record in closed),
            "by_kind": _counts(record["closed_form"]["kind"] for record in closed),
            "families": _closed_form_families(records),
            "non_integer": [
                {
                    "n": record["n"],
                    "d": record["d"],
                    "side": record["side"],
                    "side_expression": record["closed_form"]["side_expression"],
                    "tier": record["closed_form"]["tier"],
                    "residual": record["closed_form"]["residual"],
                    "source_kind": record["source"]["kind"],
                }
                for record in closed
                if not record["integer_side"]
            ],
        },
        "symmetry": {
            **{
                band: {
                    "all": _counts(record["symmetry"][band]["group"] for record in records),
                    "non_grid": _counts(
                        record["symmetry"][band]["group"] for record in non_grid
                    ),
                }
                for band, _center, _angle in SYMMETRY_BANDS
            },
            "tight_non_trivial_by_source_kind": {
                kind: {
                    "count": sum(record["source"]["kind"] == kind for record in records),
                    "non_trivial": sum(
                        record["source"]["kind"] == kind
                        and record["symmetry"]["tight"]["group"] != "trivial"
                        for record in records
                    ),
                }
                for kind in sorted({record["source"]["kind"] for record in records})
            },
            "tight_non_grid_by_closed_form": {
                "closed_form": _counts(
                    record["symmetry"]["tight"]["group"]
                    for record in non_grid
                    if record["closed_form"] is not None
                ),
                "no_closed_form": _counts(
                    record["symmetry"]["tight"]["group"]
                    for record in non_grid
                    if record["closed_form"] is None
                ),
            },
        },
        "diagonal_bands": {
            "description": (
                f"records whose tilted_layout elongation is at least {BAND_ELONGATION} with "
                f"a principal direction within {BAND_DIRECTION_TOLERANCE} degrees of a "
                "container diagonal"
            ),
            "n": [record["n"] for record in records if _diagonal_band(record)],
        },
        "tilted": {
            "with_tilted": sum(record["tilted"] > 0 for record in records),
            "with_tilted_loose": sum(record["tilted_loose"] > 0 for record in records),
            "with_forty_five": sum(
                record["angles"]["forty_five"]["tight"] > 0 for record in records
            ),
            "all_tilted_at_forty_five": [
                record["n"]
                for record in records
                if record["tilted"] > 0
                and record["tilted"] == record["angles"]["forty_five"]["tight"]
            ],
            "tight_loose_axis_disagreements": [
                record["n"]
                for record in records
                if record["angles"]["axis_aligned"]["tight"]
                != record["angles"]["axis_aligned"]["loose"]
            ],
        },
        "consecutive": _pairs_summary(records),
        "monotonicity_violations": [
            record["n"]
            for record in records
            if record["n"] + 1 in by_n
            and float(record["side"]) > float(by_n[record["n"] + 1]["side"]) + SIDE_TOLERANCE
        ],
        "l_construction": _l_summary(records),
        "queried_pairs": [
            _pair(by_n[left], by_n[right])
            for left, right in QUERIED_PAIRS
            if left in by_n and right in by_n
        ],
    }


def expected_document(records: Sequence[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    rows = build_records() if records is None else list(records)
    library = closed_form_library()
    return {
        "contract": CONTRACT,
        "generated_by": GENERATOR,
        "corpus": "atlas/known-best/manifest.json; every atlas entry",
        "claim_status": "exploratory-no-verdict",
        "detector": {
            "indices": (
                "m = floor(sqrt n), r = n - m^2; k = round(sqrt n), d = n - k^2 (nearest "
                "square, never tied); ceil_sqrt = ceil(sqrt n)"
            ),
            "side": (
                "the manifest's reported_side; integer_side when it equals ceil_sqrt, and "
                f"side equality between neighbours, within {SIDE_TOLERANCE}"
            ),
            "closed_form": {
                "small": {
                    "tested": "side - m against a + b*sqrt(2); b = 0 is the plain rationals",
                    "denominators": list(CLOSED_FORM_DENOMINATORS),
                    "numerator_bound": CLOSED_FORM_NUMERATOR_BOUND,
                    "library_size": len(library),
                },
                "wide": {
                    "tested": (
                        "only when the small library misses: side against c + b*sqrt(2), "
                        "c the nearest rational of bounded denominator to side - b*sqrt(2)"
                    ),
                    "coefficient_denominators": list(CLOSED_FORM_DENOMINATORS),
                    "coefficient_numerator_bound": WIDE_COEFFICIENT_NUMERATOR_BOUND,
                    "coefficient_count": len(wide_coefficients()),
                    "constant_denominator_bound": WIDE_CONSTANT_DENOMINATOR_BOUND,
                },
                "tolerance": SIDE_TOLERANCE,
            },
            "angles": (
                "orientations folded into [0, 90) degrees; axis-aligned and 45-degree "
                "counts and single-linkage angle classes at 1e-6 radians (tight) and 0.5 "
                "degrees (loose); `tilted` is n minus the tight axis-aligned count and "
                "`tilted_loose` n minus the loose one, so their difference is squares "
                "drifted off the axes by less than half a degree"
            ),
            "tilted_layout": (
                "squares outside the loose axis band: the major axis of their centers' "
                "covariance on [0, 180) degrees, and the square root of the major-to-minor "
                "variance ratio as elongation"
            ),
            "axis_grid": (
                "tight axis-aligned squares; components join squares sharing a full face "
                f"within {FACE_TOLERANCE}; a square is on a corner's lattice when its "
                f"distances to that corner's two walls are half-integers within "
                f"{LATTICE_TOLERANCE}"
            ),
            "symmetry": {
                "bands": {
                    name: {"center": center, "angle_radians": round(angle * math.pi / 180, 9)}
                    for name, center, angle in SYMMETRY_BANDS
                },
                "elements": [transform.name for transform in TRANSFORMS],
                "rule": (
                    "an element holds when every square's image has a square center within "
                    "the tolerance on each axis at a matching orientation; rotations are "
                    "counterclockwise, reflections negate orientation modulo 90 degrees"
                ),
            },
            "shared_with_next": (
                "each D4 image of n, translated so one container corner is fixed as the "
                "side changes, matched against n + 1 within "
                f"{SHARED_CENTER_TOLERANCE} and 1e-3 radians; 32 alignments, best "
                "(matched, matched_tilted) reported, tilted meaning outside the loose axis "
                "band; embeds means all n squares matched"
            ),
            "same_tilt_signature_as_next": (
                "both packings tilted, with the same non-axis loose angle classes: equal "
                "counts at angles within 0.5 degrees"
            ),
            "l_construction": {
                "step": (
                    "n' squares in side s' give n' + 2*floor(s') + 1 squares in s' + 1 (DS7 "
                    "section 2), floor taken within the side tolerance"
                ),
                "l_parent": (
                    "the n' < n with n - n' = 2*floor(side(n')) + 1 and side(n) - side(n') "
                    f"= 1 within {SIDE_TOLERANCE}, else null"
                ),
                "l_chain_root": "l_parent followed until null; l_chain_length counts steps",
                "l_bound": (
                    "over every n' < n with n - n' = 2*floor(side(n')) + 1, the smallest "
                    "side(n') + 1, its n', and margin = that bound - side(n)"
                ),
                "l_parent_embeds": (
                    "every square of the parent reappears in n under shared_with_next's "
                    "32 alignments"
                ),
                "column_break": (
                    "in the left-justified column n = m^2 + j, a non-integer record whose "
                    "non-integer column predecessor is not its l_parent"
                ),
            },
            "exact_grid_caveat": (
                "exact-grid records are canonical row-major grid subsets; their arrangement, "
                "symmetry, and sharing are a convention, and only the side is evidence"
            ),
        },
        "summary": summary(rows),
        "entries": rows,
    }


def _text(document: Mapping[str, Any]) -> str:
    return retained_json.dumps(document, sort_keys=True)


def update() -> None:
    text = _text(expected_document())
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(text, encoding="utf-8")
    print(f"family census updated: {len(manifest_entries())} records")


def json_differences(retained: Any, expected: Any, path: str = "$") -> Iterator[str]:
    """Each JSON path where the retained document and a fresh one disagree, with both values.

    A byte comparison says only that the census moved; this says where, so a failure on a
    runner nobody can reproduce on is diagnosed from its own log.
    """
    if isinstance(retained, dict) and isinstance(expected, dict):
        for key in sorted(set(retained) | set(expected)):
            if key not in retained or key not in expected:
                side = "retained" if key in retained else "fresh"
                yield f"{path}.{key}: present only in {side}"
            else:
                yield from json_differences(retained[key], expected[key], f"{path}.{key}")
    elif isinstance(retained, list) and isinstance(expected, list):
        if len(retained) != len(expected):
            yield f"{path}: retained {len(retained)} items, fresh {len(expected)}"
        for index, (left, right) in enumerate(zip(retained, expected, strict=False)):
            yield from json_differences(left, right, f"{path}[{index}]")
    elif retained != expected:
        yield f"{path}: retained {retained!r}, fresh {expected!r}"


def check() -> None:
    document = expected_document()
    expected = _text(document)
    if not OUTPUT.is_file():
        raise ValueError(f"{OUTPUT.relative_to(ROOT)} is missing")
    retained = OUTPUT.read_text(encoding="utf-8")
    if retained != expected:
        differences = list(
            itertools.islice(json_differences(json.loads(retained), json.loads(expected)), 20)
        )
        raise ValueError(
            f"{OUTPUT.relative_to(ROOT)} is stale; first differences:\n  "
            + "\n  ".join(differences or ["the bytes differ but the parsed documents agree"])
        )
    print(f"family census check passed: {len(manifest_entries())} records")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    update() if args.update else check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
