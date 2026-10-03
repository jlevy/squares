"""Exact rational polygon primitives that know nothing about any frame.

Every function here is a verbatim copy of its namesake in the frozen n11 mask-0 checker
(`packing/devtools/check_n11_optimality_field_mask0.py`, SHA-256 `75fc0238...`), with
the same arithmetic in the same order, so that a frame built from n11's cover reproduces
that checker's `Fraction` outputs bit for bit. Only the names of the error types differ.
"""

from __future__ import annotations

import math
from typing import NamedTuple

from sqpack.hull_kernel.rational import Q

type Point = tuple[Q, Q]
type Polygon = list[Point]
type Halfplane = tuple[Q, Q, Q]


class RefusalError(ValueError):
    """An input or a proof obligation failed; no claim follows from the call."""


class IncompleteError(Exception):
    """A bounded check could not finish without making a proof claim."""


class Budget(NamedTuple):
    """A monotonic-clock deadline and a work ceiling, shared by every bounded check."""

    deadline: float
    max_nodes: int


def require(condition: object, message: str) -> None:
    if not condition:
        raise RefusalError(message)


def area2(poly: Polygon) -> Q:
    """Twice the absolute area; zero for points, segments and the empty polygon."""
    if len(poly) < 3:
        return Q(0)
    return abs(
        sum(
            (p[0] * q[1] - p[1] * q[0] for p, q in zip(poly, poly[1:] + poly[:1], strict=True)),
            Q(0),
        )
    )


def clip(poly: Polygon, line: Halfplane) -> Polygon:
    """Intersect even a point or segment polygon with the closed half-plane ax+by<=c."""
    if not poly:
        return []
    a, b, c = line
    out: Polygon = []
    for p, q in zip(poly, poly[1:] + poly[:1], strict=True):
        dp = a * p[0] + b * p[1] - c
        dq = a * q[0] + b * q[1] - c
        if dp <= 0 and (not out or out[-1] != p):
            out.append(p)
        if (dp < 0 < dq) or (dq < 0 < dp):
            z = dp / (dp - dq)
            cross = (p[0] + z * (q[0] - p[0]), p[1] + z * (q[1] - p[1]))
            if not out or out[-1] != cross:
                out.append(cross)
        elif dp == 0 and dq > 0 and (not out or out[-1] != p):
            out.append(p)
        elif dq == 0 and dp > 0 and (not out or out[-1] != q):
            out.append(q)
    if len(out) > 1 and out[-1] == out[0]:
        out.pop()
    return out


def intersect(poly: Polygon, lines: list[Halfplane]) -> Polygon:
    for line in lines:
        poly = clip(poly, line)
        if not poly:
            break
    return poly


def trig(t: Q) -> tuple[Q, Q]:
    """Cosine and sine at the half-angle chart value `t = tan(theta/2)`."""
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def projection_range(
    vector: Point, c_interval: tuple[Q, Q], s_interval: tuple[Q, Q]
) -> tuple[Q, Q]:
    a, d = vector
    clo, chi = c_interval
    slo, shi = s_interval
    values = (a * clo + d * slo, a * clo + d * shi, a * chi + d * slo, a * chi + d * shi)
    return min(values), max(values)


def quadratic_nonnegative(a: Q, b: Q, c: Q, left: Q, right: Q) -> bool:
    """Whether `a + b t + c t^2 >= 0` on the closed interval, by its exact extrema."""
    probes = [left, right]
    if c > 0:
        critical = -b / (2 * c)
        if left < critical < right:
            probes.append(critical)
    return all(a + b * t + c * t * t >= 0 for t in probes)


def primitive_normal(dx: Q, dy: Q) -> Point:
    denominator = math.lcm(dx.denominator, dy.denominator)
    a, b = int(dx * denominator), int(dy * denominator)
    scale = math.gcd(abs(a), abs(b))
    require(scale > 0, "zero normal")
    a, b = a // scale, b // scale
    if a < 0 or (a == 0 and b < 0):
        a, b = -a, -b
    return Q(a), Q(b)


def box_halfplanes(center: Point, radius: Q) -> list[Halfplane]:
    x, y = center
    return [
        (Q(1), Q(0), x + radius),
        (Q(-1), Q(0), -x + radius),
        (Q(0), Q(1), y + radius),
        (Q(0), Q(-1), -y + radius),
    ]


def strictly_convex_counterclockwise(poly: Polygon) -> bool:
    """Every consecutive vertex triple turns strictly left (no repeats, no collinear)."""
    n = len(poly)
    if n < 3:
        return False
    for index in range(n):
        o, a, b = poly[index], poly[(index + 1) % n], poly[(index + 2) % n]
        if (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]) <= 0:
            return False
    return True
