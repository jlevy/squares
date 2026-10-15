"""Exact arithmetic for a point, segment and rectangle measure (``point_line_rectangle_v1``).

Written for the mathematical review of 14 October 2026
(``docs/project/reviews/review-2026-10-14-wand125-fine-net-and-linear-lower-bounds.md``)
from the argument the 2 October review of the T-080 route derived and from the candidate
and input formats. It imports nothing from ``devtools`` or from the source: the eight
images, the invariance test, the rotated core, the clipping and the captures are written
here, in Python fractions, and every function is exact.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

Geometry = tuple[Fraction, ...]
Point = tuple[Fraction, Fraction]

#: The kinds in the order the source's export writes them.
KINDS = ("rectangle", "point", "segment")
SIZES = {"point": 2, "segment": 4, "rectangle": 4}
SCHEMA = "point_line_rectangle_v1"
#: The gap every certificate of this kind leaves below its count.
GAP = Fraction(1, 100000)
#: A core of side ``B < 1`` lies within this distance of its centre on each axis.
REACH = Fraction(71, 100)


def refuse_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    found: dict[str, Any] = {}
    for key, value in pairs:
        if key in found:
            msg = f"duplicate JSON key {key!r}"
            raise ValueError(msg)
        found[key] = value
    return found


def load_json(data: bytes) -> Any:
    """JSON with every decimal kept as its text, so that it reads as an exact rational."""
    return json.loads(data, parse_float=str, object_pairs_hook=refuse_duplicates)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class Measure:
    """A candidate read exactly: its orbit representatives and their weighted images."""

    n: int
    side: Fraction
    core: Fraction
    step: Fraction
    last: int
    primitives: list[tuple[str, Geometry, Fraction]]
    images: dict[str, list[tuple[Geometry, Fraction]]]
    total: Fraction


def orbit(kind: str, geometry: Geometry, side: Fraction) -> list[Geometry]:
    """The eight images of one primitive under the symmetries of ``[0, L]^2``, in the
    source's export order: the diagonal swap outermost, then the four sign choices."""
    corners = [geometry] if kind == "point" else [geometry[:2], geometry[2:]]
    images: list[Geometry] = []
    for swap in (False, True):
        for flip_x, flip_y in ((False, False), (False, True), (True, False), (True, True)):
            moved: list[Point] = []
            for x, y in corners:
                u, v = (y, x) if swap else (x, y)
                moved.append((side - u if flip_x else u, side - v if flip_y else v))
            if kind == "point":
                images.append(moved[0])
            elif kind == "rectangle":
                (a, b), (c, d) = moved
                images.append((min(a, c), min(b, d), max(a, c), max(b, d)))
            else:
                images.append((*moved[0], *moved[1]))
    return images


def read_measure(candidate: dict[str, Any]) -> Measure:
    """Read a candidate exactly, refusing what the format refuses."""
    if candidate.get("schema") != SCHEMA:
        msg = "not a point_line_rectangle_v1 measure"
        raise ValueError(msg)
    n = candidate["n"]
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        msg = "n is not a positive integer"
        raise ValueError(msg)
    side, core = Fraction(candidate["L"]), Fraction(candidate["B"])
    if not 0 < core < 1 < side:
        msg = "invalid side or core"
        raise ValueError(msg)
    net = candidate["net"]
    if (
        set(net) != {"step", "last"}
        or isinstance(net["last"], bool)
        or not isinstance(net["last"], int)
    ):
        msg = "net is not exactly {step, last} with an integer last"
        raise ValueError(msg)
    step, last = Fraction(net["step"]), int(net["last"])
    primitives: list[tuple[str, Geometry, Fraction]] = []
    images: dict[str, list[tuple[Geometry, Fraction]]] = {kind: [] for kind in KINDS}
    total = Fraction(0)
    for index, item in enumerate(candidate["primitives"]):
        if set(item) != {"kind", "geometry", "mass"}:
            msg = f"primitive {index} has other fields"
            raise ValueError(msg)
        kind = item["kind"]
        if kind not in SIZES:
            msg = f"primitive {index}: unknown kind {kind!r}"
            raise ValueError(msg)
        geometry = tuple(Fraction(value) for value in item["geometry"])
        mass = Fraction(item["mass"])
        if len(geometry) != SIZES[kind] or mass < 0:
            msg = f"primitive {index}: wrong size or negative mass"
            raise ValueError(msg)
        if not all(0 <= value <= side for value in geometry):
            msg = f"primitive {index} is outside [0, L]^2"
            raise ValueError(msg)
        if kind == "rectangle" and not (
            geometry[0] < geometry[2] and geometry[1] < geometry[3]
        ):
            msg = f"rectangle {index} is empty or reversed"
            raise ValueError(msg)
        if kind == "segment" and geometry[:2] == geometry[2:]:
            msg = f"segment {index} has length zero"
            raise ValueError(msg)
        primitives.append((kind, geometry, mass))
        total += mass
        if mass:
            images[kind].extend((image, mass / 8) for image in orbit(kind, geometry, side))
    return Measure(n, side, core, step, last, primitives, images, total)


def canonical(kind: str, geometry: Geometry) -> Geometry:
    """One spelling per set: a segment's endpoints in order, anything else as it is."""
    if kind == "segment" and geometry[2:] < geometry[:2]:
        return (*geometry[2:], *geometry[:2])
    return geometry


def moved_by(kind: str, geometry: Geometry, side: Fraction, *, swap: bool) -> Geometry:
    """The image under one generator: the diagonal swap, or the reflection ``x -> L - x``."""
    corners = [geometry] if kind == "point" else [geometry[:2], geometry[2:]]
    mapped = [(y, x) if swap else (side - x, y) for x, y in corners]
    if kind == "point":
        return mapped[0]
    if kind == "rectangle":
        (a, b), (c, d) = mapped
        return (min(a, c), min(b, d), max(a, c), max(b, d))
    return canonical(kind, (*mapped[0], *mapped[1]))


def invariant_under_d4(measure: Measure) -> dict[str, bool]:
    """Whether the weighted images, as a multiset of (kind, set, weight), are carried onto
    themselves by each generator of ``D4``: the diagonal swap and ``x -> L - x``."""
    found: Counter[tuple[str, Geometry, Fraction]] = Counter()
    for kind, rows in measure.images.items():
        for geometry, weight in rows:
            found[(kind, canonical(kind, geometry), weight)] += 1
    outcome = {}
    for name, swap in (("diagonal_swap", True), ("reflection_x", False)):
        image: Counter[tuple[str, Geometry, Fraction]] = Counter()
        for (kind, geometry, weight), count in found.items():
            image[(kind, moved_by(kind, geometry, measure.side, swap=swap), weight)] += count
        outcome[name] = image == found
    return outcome


def direction(step: Fraction, index: int) -> tuple[Fraction, Fraction]:
    t = index * step
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def half_width(measure: Measure, index: int) -> Fraction:
    """``E_r = (L - B (c_r + s_r)) / 2``: Tokoharu's centre domain is ``L/2 +- E_r``."""
    c, s = direction(measure.step, index)
    return (measure.side - measure.core * (c + s)) / 2


def net_facts(core: Fraction, step: Fraction, count: int) -> dict[str, Fraction]:
    last = step * (count - 1)
    shrink = core * (1 + step)
    return {
        "step": step,
        "count": Fraction(count),
        "endpoint": last,
        "endpoint_check": last * last + 2 * last - 1,
        "rotated_side_upper": shrink,
        "side_margin": 1 - shrink,
        "per_edge_margin": (1 - shrink) / 2,
    }


def core_polygon(
    x: Fraction, y: Fraction, c: Fraction, s: Fraction, core: Fraction
) -> list[Point]:
    h = core / 2
    ux, uy, vx, vy = c * h, s * h, -s * h, c * h
    return [
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
    ]


def clip(polygon: list[Point], axis: int, bound: Fraction, *, keep_above: bool) -> list[Point]:
    """Sutherland-Hodgman: the part of a convex polygon on one side of an axis-parallel line."""
    kept: list[Point] = []
    count = len(polygon)
    for k in range(count):
        current, following = polygon[k], polygon[(k + 1) % count]
        inside_current = (current[axis] >= bound) if keep_above else (current[axis] <= bound)
        inside_following = (
            (following[axis] >= bound) if keep_above else (following[axis] <= bound)
        )
        if inside_current:
            kept.append(current)
        if inside_current != inside_following:
            t = (bound - current[axis]) / (following[axis] - current[axis])
            kept.append(
                (
                    current[0] + t * (following[0] - current[0]),
                    current[1] + t * (following[1] - current[1]),
                )
            )
    return kept


def area(polygon: list[Point]) -> Fraction:
    total = Fraction(0)
    count = len(polygon)
    for k in range(count):
        (x0, y0), (x1, y1) = polygon[k], polygon[(k + 1) % count]
        total += x0 * y1 - x1 * y0
    return abs(total) / 2


def capture(measure: Measure, x: Fraction, y: Fraction, index: int) -> Fraction:
    """The exact mass the closed core at centre ``(x, y)`` and net angle ``index`` captures:
    a point when it lies in the closed core, a segment by the parameter length of its
    closed intersection, a rectangle by its area."""
    c, s = direction(measure.step, index)
    half = measure.core / 2
    polygon = core_polygon(x, y, c, s, measure.core)

    def local(px: Fraction, py: Fraction) -> tuple[Fraction, Fraction]:
        dx, dy = px - x, py - y
        return c * dx + s * dy, c * dy - s * dx

    total = Fraction(0)
    for (x1, y1, x2, y2), weight in measure.images["rectangle"]:
        if x1 > x + REACH or x2 < x - REACH or y1 > y + REACH or y2 < y - REACH:
            continue
        piece = clip(polygon, 0, x1, keep_above=True)
        piece = clip(piece, 0, x2, keep_above=False)
        piece = clip(piece, 1, y1, keep_above=True)
        piece = clip(piece, 1, y2, keep_above=False)
        if len(piece) >= 3:
            total += weight / ((x2 - x1) * (y2 - y1)) * area(piece)
    for (px, py), weight in measure.images["point"]:
        if abs(px - x) > REACH or abs(py - y) > REACH:
            continue
        u, v = local(px, py)
        if abs(u) <= half and abs(v) <= half:
            total += weight
    for (x0, y0, x1, y1), weight in measure.images["segment"]:
        if max(x0, x1) < x - REACH or min(x0, x1) > x + REACH:
            continue
        if max(y0, y1) < y - REACH or min(y0, y1) > y + REACH:
            continue
        start, end = local(x0, y0), local(x1, y1)
        low, high = Fraction(0), Fraction(1)
        for a, b in zip(start, end, strict=True):
            slope = b - a
            if slope == 0:
                if abs(a) > half:
                    high = Fraction(-1)
                continue
            t1, t2 = (-half - a) / slope, (half - a) / slope
            low, high = max(low, min(t1, t2)), min(high, max(t1, t2))
        if high > low:
            total += weight * (high - low)
    return total


def semantic_digest(candidate: dict[str, Any]) -> str:
    """The candidate digest by the source's rule: its seven semantic fields, canonical JSON."""
    fields = ("schema", "n", "L", "B", "primitives", "total_mass", "net")
    text = json.dumps(
        {key: candidate[key] for key in fields}, sort_keys=True, separators=(",", ":")
    )
    return sha256(text.encode())


def sqrt_bounds(value: int, digits: int) -> tuple[Fraction, Fraction]:
    """Rational bounds ``lo <= sqrt(value) <= hi`` with ``hi - lo = 10^-digits``."""
    scale = 10**digits
    root = math.isqrt(value * scale * scale)
    low = Fraction(root, scale)
    return low, (low if root * root == value * scale * scale else low + Fraction(1, scale))
