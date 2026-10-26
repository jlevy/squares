#!/usr/bin/env python3
"""An exact capture evaluator for Tokoharu-format rectangle densities, written for the
stage 4 review of T-046 (bead think-buaj) from the mathematics alone.

It was written from `packing/sqverify_fast/SOUNDNESS.md`'s statement of the density,

    g = sum_j w_j / (8 |R_j|) * sum_{S in D4} 1_{S(R_j)},

and the theorem's closed square Q_r(c) of side B, centre c and angle
theta_r = 2 arctan(r D). Its author did not open `sqpack.rectangle_density`, the crate's
`oracle.rs` or `exact.rs`, Tokoharu's `verify.cpp`, or the census driver's control code
before it agreed with the retained receipts; it imports nothing from this repository.

Every quantity is an exact rational. A JSON number in a candidate is its literal decimal
value; a pose taken from a receipt is the exact value of the binary64 number printed
there. The net direction's cosine and sine are rational, (1 - t^2)/(1 + t^2) and
2t/(1 + t^2) with t = r D, so the square's vertices are rational and the capture is the
exact sum of the image densities times the exact areas of the clipped polygons.
"""

from __future__ import annotations

import gzip
import json
from dataclasses import dataclass
from decimal import Decimal
from fractions import Fraction as Q
from pathlib import Path

D = Q(83, 40000)

Point = tuple[Q, Q]
Rect = tuple[Q, Q, Q, Q]


def literal(token: str) -> Q:
    """A JSON number's literal decimal value, never the nearest binary64."""
    return Q(Decimal(token))


def load(path: Path) -> dict:
    """A candidate, plain or gzip, with every JSON number exact."""
    data = path.read_bytes()
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return json.loads(data, parse_float=literal, parse_int=lambda token: Q(int(token)))


@dataclass(frozen=True)
class Density:
    """The D4 expansion of a candidate: each positive-weight row's eight images, each
    carrying w / 8 spread uniformly over its rectangle, coincident images kept apart."""

    n: int
    side: Q
    core: Q
    images: tuple[tuple[Rect, Q], ...]  # (rectangle, mass w / 8)
    mass: Q


def images_of(rect: Rect, side: Q) -> list[Rect]:
    """The eight images of [x1, x2] x [y1, y2] under the symmetries of [0, L]^2."""
    x1, y1, x2, y2 = rect
    flips = [(x1, x2), (side - x2, side - x1)]
    found: list[Rect] = []
    for a1, a2 in flips:
        for b1, b2 in ((y1, y2), (side - y2, side - y1)):
            found.append((a1, b1, a2, b2))
            found.append((b1, a1, b2, a2))
    return found


def density(raw: dict) -> Density:
    side = Q(raw["L"])
    core = Q(raw["B"])
    weights = [Q(str(w)) if not isinstance(w, Q) else w for w in raw["weights"]]
    images: list[tuple[Rect, Q]] = []
    for row, weight in zip(raw["rectangles"], weights, strict=True):
        if weight < 0:
            raise ValueError("negative weight")
        if weight == 0:
            continue
        rect = tuple(Q(value) for value in row)
        assert len(rect) == 4
        for image in images_of((rect[0], rect[1], rect[2], rect[3]), side):
            images.append((image, weight / 8))
    return Density(int(raw["n"]), side, core, tuple(images), sum(weights, Q(0)))


def rotation(r: int) -> tuple[Q, Q]:
    t = r * D
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def half_extent(core: Q, r: int) -> Q:
    """a_r = B (cos + sin) / 2: the half-width of the square's axis bounding box."""
    c, s = rotation(r)
    return core * (c + s) / 2


def square(centre: Point, core: Q, r: int) -> list[Point]:
    c, s = rotation(r)
    h = core / 2
    cx, cy = centre
    return [
        (cx + h * (c * a - s * b), cy + h * (s * a + c * b))
        for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))
    ]


def clip(polygon: list[Point], axis: int, bound: Q, keep_above: bool) -> list[Point]:
    """Sutherland-Hodgman against one axis-parallel half-plane."""
    out: list[Point] = []
    count = len(polygon)
    for index in range(count):
        p, q = polygon[index], polygon[(index + 1) % count]
        p_in = p[axis] >= bound if keep_above else p[axis] <= bound
        q_in = q[axis] >= bound if keep_above else q[axis] <= bound
        if p_in:
            out.append(p)
        if p_in != q_in:
            t = (bound - p[axis]) / (q[axis] - p[axis])
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def area(polygon: list[Point]) -> Q:
    total = Q(0)
    count = len(polygon)
    for index in range(count):
        x1, y1 = polygon[index]
        x2, y2 = polygon[(index + 1) % count]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def capture(g: Density, r: int, centre: Point) -> Q:
    """The exact mass of g in the closed square Q_r(centre) of side B."""
    corners = square(centre, g.core, r)
    c, s = rotation(r)
    h = g.core / 2
    reach = h * (c + s)
    cx, cy = centre
    left, right, low, high = cx - reach, cx + reach, cy - reach, cy + reach

    def inside(x: Q, y: Q) -> bool:
        dx, dy = x - cx, y - cy
        return abs(dx * c + dy * s) <= h and abs(-dx * s + dy * c) <= h

    total = Q(0)
    for (x1, y1, x2, y2), share in g.images:
        if x2 <= left or x1 >= right or y2 <= low or y1 >= high:
            continue
        if inside(x1, y1) and inside(x2, y1) and inside(x1, y2) and inside(x2, y2):
            total += share
            continue
        piece = corners
        for axis, bound, above in ((0, x1, True), (0, x2, False), (1, y1, True), (1, y2, False)):
            piece = clip(piece, axis, bound, above)
            if not piece:
                break
        if len(piece) >= 3:
            total += share * area(piece) / ((x2 - x1) * (y2 - y1))
    return total


def pose(values: list[float]) -> Point:
    """A receipt's binary64 pose as exact rationals."""
    return Q(values[0]), Q(values[1])
