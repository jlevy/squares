#!/usr/bin/env python3
"""Verify, in exact arithmetic, the counterexample to Lemma 1 of [Nagamochi 2005].

`T-007` rests on Nagamochi's Theorem 2, which rests on Theorem 1 (the rectangle bound
`nu(a, b) < ab - (a + 1 - ceil a) - (b + 1 - ceil b)`), which the paper proves by
summing the scores of Lemma 1: every `lambda x lambda` square `S` inside
`R = [0, a] x [0, b]`, `1 < lambda <= 1.01`, has score `sigma(S) > 1` against the
unavoidable set `U` of its Section 3. Karakus (arXiv:2609.37410, 29 September 2026)
exhibits a family of squares `K_t` at the lower-left corner of `R`, one for each
`0 < t <= 1/50` with `t < min(10(a - 3), b - 2)`, whose score after a concentric shrink
is below one; chelokot's Lean archive exhibits one such square in `[0, 4]^2`
(side `10001/10000`, score `25009470849041/25584000000000`). This tool recomputes both
from their printed coordinates with `Fraction` arithmetic and nothing floating.

The score is a measure: area density on `R* = [1, a-1] x [1, b-1]`, line density `1/2`
on four axis-parallel segments, `9/20` on the eight points of `Q` and `1/2` on the points
of `P`. Every piece of that geometry is rational for a rational square, so the score is
an exact rational and each printed value is checked as an equality, not to a tolerance.
Whether a boundary point counts is the one convention the paper leaves open; the
shrunken square decides it by having the contested point strictly outside, and both
conventions are computed.

Two further checks support the review that owns this tool
(`docs/project/reviews/review-2026-10-02-nagamochi-lemma1-karakus.md`):

- Karakus's replacement bound, Corollary 6.2: `s(N) >= 1/2 + sqrt(N - floor(sqrt N) + 1/4)`
  for every nonsquare `N >= 8`. It is compared with Theorem 2's closed form, exactly
  (the comparison reduces to `floor(sqrt N)^2 <= N`) and in decimals at named `N`.
- The two obvious local repairs of Nagamochi's measure, each of which rescues `K_t`
  and each of which an axis-parallel square at the same corner then defeats, so that
  neither is a repair. Those squares are the witnesses the review cites.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m \\
        devtools.check_nagamochi_lemma1_counterexample
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
from typing import Literal

from devtools.check_nagamochi_bounds import theorem_two

Point = tuple[Fraction, Fraction]
Polygon = tuple[Point, ...]
#: Rectangle as `(x1, y1, x2, y2, density)`.
Rectangle = tuple[Fraction, Fraction, Fraction, Fraction, Fraction]
#: Axis-parallel segment as `(p, q, density)`.
Segment = tuple[Point, Point, Fraction]
#: Weighted point as `(point, weight)`.
Weighted = tuple[Point, Fraction]

HALF = Fraction(1, 2)
NINE_TENTHS = Fraction(9, 10)
Q_WEIGHT = Fraction(9, 20)
#: The paper's technical ceiling on the enlarged side, `lambda <= 1.01`.
SIDE_CEILING = Fraction(101, 100)
#: The members of Karakus's family verified here. (4.3) admits every `t` in `(0, 1/50]`
#: below `min(10(a - 3), b - 2)`; these four are the declared finite set, the largest
#: being the paper's own worst case.
DECLARED_T = (Fraction(1, 50), Fraction(1, 100), Fraction(1, 1000), Fraction(1, 10**6))
#: Rational containers the family is checked in. `(4, 4)` is chelokot's; `(7/2, 5/2)` is
#: within `1/2` of the family's `a > 3`, `b > 2` edge; the others stand in for the
#: square containers Theorem 2 needs, whose sides are mostly irrational.
DECLARED_CONTAINERS = (
    (Fraction(4), Fraction(4)),
    (Fraction(7, 2), Fraction(5, 2)),
    (Fraction(10), Fraction(10)),
    (Fraction(33), Fraction(7)),
)
DECIMAL_DIGITS = 30


class CounterexampleError(AssertionError):
    """A printed fact about the counterexample that the exact recomputation refutes."""


def _fr(value: int | Fraction) -> Fraction:
    return Fraction(value)


# -- convex polygons ----------------------------------------------------------------


def _cross(o: Point, p: Point, q: Point) -> Fraction:
    return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])


def signed_area(polygon: Polygon) -> Fraction:
    total = Fraction(0)
    for i, (x1, y1) in enumerate(polygon):
        x2, y2 = polygon[(i + 1) % len(polygon)]
        total += x1 * y2 - x2 * y1
    return total / 2


def counterclockwise(polygon: Polygon) -> Polygon:
    """The same polygon, oriented counterclockwise."""
    if signed_area(polygon) < 0:
        return tuple(reversed(polygon))
    return polygon


def contains_point(polygon: Polygon, point: Point, *, closed: bool) -> bool:
    """Is `point` in the convex polygon: in its closure, or strictly in its interior?"""
    polygon = counterclockwise(polygon)
    for i, vertex in enumerate(polygon):
        turn = _cross(vertex, polygon[(i + 1) % len(polygon)], point)
        if turn < 0 or (not closed and turn == 0):
            return False
    return True


def clip_to_rectangle(polygon: Polygon, rectangle: Rectangle) -> Polygon:
    """Sutherland-Hodgman: the convex polygon cut down to an axis-parallel rectangle."""
    x1, y1, x2, y2, _ = rectangle
    sides = (
        (lambda p: p[0] - x1),
        (lambda p: x2 - p[0]),
        (lambda p: p[1] - y1),
        (lambda p: y2 - p[1]),
    )
    output = list(counterclockwise(polygon))
    for inside in sides:
        if not output:
            break
        current, output = output, []
        for i, p in enumerate(current):
            q = current[(i + 1) % len(current)]
            fp, fq = inside(p), inside(q)
            if fp >= 0:
                output.append(p)
            if (fp < 0 < fq) or (fq < 0 < fp):
                s = fp / (fp - fq)
                output.append((p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1])))
    return tuple(output)


def segment_length_inside(polygon: Polygon, segment: Segment, *, closed: bool) -> Fraction:
    """Length of an axis-parallel segment's part inside the convex polygon.

    Cyrus-Beck against each edge's inward half-plane. A segment lying along an edge
    has positive closed length and no interior length, which is the one place the two
    conventions give different lengths; that is why `closed` reaches down to here.
    """
    (px, py), (qx, qy), _ = segment
    if px != qx and py != qy:
        message = "only axis-parallel segments have rational lengths"
        raise ValueError(message)
    polygon = counterclockwise(polygon)
    low, high = Fraction(0), Fraction(1)
    dx, dy = qx - px, qy - py
    for i, (vx, vy) in enumerate(polygon):
        wx, wy = polygon[(i + 1) % len(polygon)]
        # Inward normal of the edge v -> w for a counterclockwise polygon.
        nx, ny = -(wy - vy), wx - vx
        a = nx * (px - vx) + ny * (py - vy)
        b = nx * dx + ny * dy
        if b == 0:
            if a < 0 or (not closed and a == 0):
                return Fraction(0)
            continue
        s = -a / b
        if b > 0:
            low = max(low, s)
        else:
            high = min(high, s)
    if high <= low:
        return Fraction(0)
    return (high - low) * (abs(dx) + abs(dy))


# -- measures -----------------------------------------------------------------------


@dataclass(frozen=True)
class Measure:
    """A finite nonnegative measure of rectangles, axis-parallel segments and points."""

    rectangles: tuple[Rectangle, ...]
    segments: tuple[Segment, ...]
    points: tuple[Weighted, ...]

    def total(self) -> Fraction:
        mass = sum(((x2 - x1) * (y2 - y1) * d for x1, y1, x2, y2, d in self.rectangles), _fr(0))
        mass += sum(
            ((abs(q[0] - p[0]) + abs(q[1] - p[1])) * d for p, q, d in self.segments), _fr(0)
        )
        return mass + sum((w for _, w in self.points), _fr(0))

    def score(self, polygon: Polygon, *, closed: bool) -> Fraction:
        """The mass the polygon captures: its closure, or its interior."""
        value = Fraction(0)
        for rectangle in self.rectangles:
            clipped = clip_to_rectangle(polygon, rectangle)
            if len(clipped) >= 3:
                value += rectangle[4] * abs(signed_area(clipped))
        for segment in self.segments:
            value += segment[2] * segment_length_inside(polygon, segment, closed=closed)
        for point, weight in self.points:
            if contains_point(polygon, point, closed=closed):
                value += weight
        return value


def _rect(x1: Fraction, y1: Fraction, x2: Fraction, y2: Fraction, d: Fraction) -> Rectangle:
    return (x1, y1, x2, y2, d)


def _seg(p: Point, q: Point, d: Fraction = HALF) -> Segment:
    return (p, q, d)


def nagamochi_measure(a: Fraction, b: Fraction) -> Measure:
    """The unavoidable set `U` of [Nagamochi 2005] Section 3, as a measure on `[0,a]x[0,b]`.

    The printed `P` writes `(i, a - 0.9)` and `(b - 0.9, j)`; Figure 1 and the point
    count `2 ceil(a) + 2 ceil(b) - 12` say `(i, b - 0.9)` and `(a - 0.9, j)`, which is
    what is built (Karakus, footnote 1, makes the same correction).
    """
    one = Fraction(1)
    e = NINE_TENTHS
    q_points = (
        (e, one),
        (a - e, one),
        (e, b - one),
        (a - e, b - one),
        (one, e),
        (one, b - e),
        (a - one, e),
        (a - one, b - e),
    )
    p_points = [(_fr(i), e) for i in range(2, math.ceil(a) - 1)]
    p_points += [(_fr(i), b - e) for i in range(2, math.ceil(a) - 1)]
    p_points += [(e, _fr(j)) for j in range(2, math.ceil(b) - 1)]
    p_points += [(a - e, _fr(j)) for j in range(2, math.ceil(b) - 1)]
    return Measure(
        rectangles=(_rect(one, one, a - one, b - one, one),),
        segments=(
            _seg((e, one), (a - e, one)),
            _seg((e, b - one), (a - e, b - one)),
            _seg((one, e), (one, b - e)),
            _seg((a - one, e), (a - one, b - e)),
        ),
        points=tuple((p, Q_WEIGHT) for p in q_points) + tuple((p, HALF) for p in p_points),
    )


def nagamochi_total(a: Fraction, b: Fraction) -> Fraction:
    """Theorem 1's right-hand side `ab - Delta(a) - Delta(b)`, `Delta(t) = t + 1 - ceil t`."""
    return a * b - (a + 1 - math.ceil(a)) - (b + 1 - math.ceil(b))


def karakus_strip_measure(a: Fraction, b: Fraction) -> Measure:
    """Karakus's strip measure (5.1): mass `ab - Delta(a)` for `a >= 2`, `b >= 3`."""
    zero, one = Fraction(0), Fraction(1)
    w = Fraction(4, 5)
    points = [(_fr(j), w) for j in range(1, math.ceil(a))]
    points += [(_fr(j), b - w) for j in range(1, math.ceil(a))]
    return Measure(
        rectangles=(_rect(zero, one, a, b - one, one),),
        segments=(_seg((zero, one), (a, one)), _seg((zero, b - one), (a, b - one))),
        points=tuple((p, HALF) for p in points),
    )


def karakus_total(a: Fraction) -> Fraction:
    return a * a - (a + 1 - math.ceil(a))


Repair = Literal["weight", "slide", "augment"]


def local_repair(a: Fraction, b: Fraction, variant: Repair) -> Measure:
    """Three candidate local repairs of `U` at its eight corner points.

    Each `Q` point of weight `9/20` sits `1/10` beyond the end of a side of `R*`, and the
    side is extended `1/10` to reach it, worth `1/20`; the pair is worth `1/2`. `K_t`
    captures the point and almost none of the extension.

    - `weight`: give the point `1/2` and drop the extensions. Total unchanged.
    - `slide`: drop the extensions and attach to each `Q` point a `1/10` segment along
      its own row or column, inward. Total unchanged.
    - `augment`: give the point `1/2` and keep the extensions (chelokot's augmented
      measure, which proves `s(k^2 - 1) = k`). Total rises by `2/5`.
    """
    base = nagamochi_measure(a, b)
    one, e, tenth = Fraction(1), NINE_TENTHS, Fraction(1, 10)
    q_points = tuple(p for p, w in base.points if w == Q_WEIGHT)
    p_points = tuple((p, w) for p, w in base.points if w == HALF)
    points = tuple((p, HALF) for p in q_points) + p_points
    if variant == "augment":
        return Measure(base.rectangles, base.segments, points)
    sides = (
        _seg((one, one), (a - one, one)),
        _seg((one, b - one), (a - one, b - one)),
        _seg((one, one), (one, b - one)),
        _seg((a - one, one), (a - one, b - one)),
    )
    if variant == "weight":
        return Measure(base.rectangles, sides, points)
    attached = []
    for x, y in q_points:
        if y in (e, b - e):  # a point on a row: slide inward along the row
            direction = one if x == one else -one
            attached.append(_seg((x, y), (x + direction * tenth, y)))
        else:  # a point on a column
            direction = one if y == one else -one
            attached.append(_seg((x, y), (x, y + direction * tenth)))
    return Measure(base.rectangles, sides + tuple(attached), base.points)


# -- squares ------------------------------------------------------------------------


def side_squared(square: Polygon) -> Fraction:
    """The common squared side, after checking the four edges make a square."""
    if len(square) != 4:
        message = "a square has four vertices"
        raise CounterexampleError(message)
    edges = [
        (square[(i + 1) % 4][0] - square[i][0], square[(i + 1) % 4][1] - square[i][1])
        for i in range(4)
    ]
    lengths = {ex * ex + ey * ey for ex, ey in edges}
    if len(lengths) != 1:
        message = f"edges differ in length: {sorted(lengths)}"
        raise CounterexampleError(message)
    for i in range(4):
        (ux, uy), (vx, vy) = edges[i], edges[(i + 1) % 4]
        if ux * vx + uy * vy != 0:
            message = f"edges {i} and {i + 1} are not perpendicular"
            raise CounterexampleError(message)
    return lengths.pop()


def centre(square: Polygon) -> Point:
    return ((square[0][0] + square[2][0]) / 2, (square[0][1] + square[2][1]) / 2)


def shrink(square: Polygon, factor: Fraction, about: Point) -> Polygon:
    return tuple(
        (about[0] + factor * (x - about[0]), about[1] + factor * (y - about[1]))
        for x, y in square
    )


def inside_container(square: Polygon, a: Fraction, b: Fraction) -> bool:
    return all(0 <= x <= a and 0 <= y <= b for x, y in square)


def karakus_contact_square(t: Fraction) -> Polygon:
    """`K_t` of Karakus (4.4): vertices `A, B, C, D` in cyclic order."""
    return (
        (2 - NINE_TENTHS * t, Fraction(0)),
        (2 + t / 10, Fraction(1)),
        (1 + t / 10, 1 + t),
        (1 - NINE_TENTHS * t, t),
    )


def shrink_factor(t: Fraction) -> Fraction:
    """A rational factor below one that keeps the shrunken side above one."""
    return 1 - t * t / 8


def chelokot_square() -> Polygon:
    """The square of chelokot's `docs/nagamochi-score-counterexample.md`, in `[0, 4]^2`."""
    lam = Fraction(10001, 10000)
    c, s = Fraction(80, 1601), Fraction(1599, 1601)
    ax, ay = Fraction(10419467, 5330000), Fraction(0)
    return (
        (ax, ay),
        (ax + lam * c, ay + lam * s),
        (ax + lam * (c - s), ay + lam * (s + c)),
        (ax - lam * s, ay + lam * c),
    )


CHELOKOT_SCORE = Fraction(25009470849041, 25584000000000)
CHELOKOT_LEAN_CEILING = Fraction(199, 200)


def axis_square(x0: Fraction, y0: Fraction, side: Fraction) -> Polygon:
    return ((x0, y0), (x0 + side, y0), (x0 + side, y0 + side), (x0, y0 + side))


# -- checks -------------------------------------------------------------------------


def _require(condition: bool, message: str) -> None:  # noqa: FBT001 -- a predicate, by design
    if not condition:
        raise CounterexampleError(message)


def check_karakus_member(t: Fraction, a: Fraction, b: Fraction) -> dict[str, Fraction]:
    """Recompute Karakus Section 4 and Appendix A for one `t` in one container.

    Returns the exact quantities, having raised on the first printed fact that fails.
    """
    _require(0 < t <= Fraction(1, 50), f"t = {t} is outside (0, 1/50]")
    _require(t < min(10 * (a - 3), b - 2), f"t = {t} violates (4.3) in [0,{a}]x[0,{b}]")
    measure = nagamochi_measure(a, b)
    one, e = Fraction(1), NINE_TENTHS
    k = karakus_contact_square(t)
    side2 = side_squared(k)
    _require(side2 == 1 + t * t, "side^2 of K_t is not 1 + t^2")
    _require(1 < side2 <= SIDE_CEILING**2, "K_t's side is outside (1, 101/100]")
    _require(inside_container(k, a, b), "K_t leaves the container")
    _require(max(x for x, _ in k) < a - 1 and max(y for _, y in k) < b - 1, "(4.1) fails")
    # Appendix A, piece by piece.
    chord_09 = segment_length_inside(k, _seg((Fraction(0), e), (a, e)), closed=True)
    _require(chord_09 == 2 - (1 - t * t), "(A.1): chord at y = 9/10 is not [1 - t^2, 2]")
    _require(contains_point(k, (one, e), closed=False), "(1, 9/10) is not interior to K_t")
    on_boundary = contains_point(k, (_fr(2), e), closed=True) and not contains_point(
        k, (_fr(2), e), closed=False
    )
    _require(on_boundary, "(2, 9/10) is not on the boundary of K_t")
    l1 = segment_length_inside(k, measure.segments[0], closed=True)
    l3 = segment_length_inside(k, measure.segments[2], closed=True)
    _require(l1 == 1 + t * t, "(A.4): |K_t ∩ L1| is not 1 + t^2")
    _require(l3 == t, "(A.5): |K_t ∩ L3| is not t")
    area = abs(signed_area(clip_to_rectangle(k, measure.rectangles[0])))
    _require(area == t * (1 + t * t) / 2, "(A.6): area in R* is not t(1 + t^2)/2")
    closed_score = measure.score(k, closed=True)
    printed = Fraction(29, 20) + t + t * t / 2 + t**3 / 2
    _require(closed_score == printed, "the contact-square score is not (A)'s polynomial")
    _require(measure.score(k, closed=False) == printed - HALF, "(4.7) fails on the interior")

    # The concentric shrink: the score counterexample proper.
    rho = shrink_factor(t)
    s = shrink(k, rho, centre(k))
    _require(1 < side_squared(s) <= SIDE_CEILING**2, "the shrunken side left (1, 101/100]")
    _require(inside_container(s, a, b), "the shrunken square leaves the container")
    _require(contains_point(s, (one, e), closed=False), "(1, 9/10) left the interior")
    _require(not contains_point(s, (_fr(2), e), closed=True), "(2, 9/10) is still in S_t")
    shrunk_closed = measure.score(s, closed=True)
    shrunk_open = measure.score(s, closed=False)
    _require(shrunk_closed < 1 and shrunk_open < 1, "the shrunken square scores >= 1")

    # The vertex shrink: the configuration Lemma 6's hypothesis excludes.
    v = shrink(k, rho, k[0])
    _require(v[1][1] < 1 < v[2][1] and v[3][1] < 1, "y = 1 does not cut B''C'' and C''D''")
    # (2, 9/10) = A + (9/10)(t, 1) and the image of B is A + rho (t, 1): the point lies in
    # the relative interior of the image of AB exactly when 9/10 < rho.
    _require(NINE_TENTHS < rho < 1, "(2, 9/10) is not in the relative interior of AB''")
    _require(contains_point(v, (one, e), closed=False), "(1, 9/10) left the vertex shrink")
    vertex_open = measure.score(v, closed=False)
    _require(vertex_open < 1, "the vertex-shrunk square's interior scores >= 1")

    # Consistency: Karakus's own measure scores both interiors above one, as his
    # Proposition 5.1 requires; the family refutes Lemma 1, not the strip measure.
    strip = karakus_strip_measure(a, b)
    _require(strip.score(s, closed=False) > 1, "the strip measure fails on S_t")
    _require(strip.score(k, closed=False) > 1, "the strip measure fails on K_t")
    return {
        "t": t,
        "side_squared": side2,
        "contact_closed": closed_score,
        "contact_without_P": closed_score - HALF,
        "shrunk_closed": shrunk_closed,
        "shrunk_interior": shrunk_open,
        "vertex_shrunk_interior": vertex_open,
        "strip_measure_interior": strip.score(s, closed=False),
    }


def check_chelokot_instance() -> dict[str, Fraction]:
    """Recompute the archive's square and its printed exact score in `[0, 4]^2`."""
    a = b = Fraction(4)
    measure = nagamochi_measure(a, b)
    s = chelokot_square()
    _require(side_squared(s) == Fraction(10001, 10000) ** 2, "side is not 10001/10000")
    _require(inside_container(s, a, b), "the square leaves [0, 4]^2")
    _require(contains_point(s, (Fraction(1), NINE_TENTHS), closed=False), "(1, 0.9) outside")
    _require(not contains_point(s, (Fraction(2), NINE_TENTHS), closed=True), "(2, 0.9) inside")
    for point, _ in measure.points:
        on = contains_point(s, point, closed=True) and not contains_point(
            s, point, closed=False
        )
        _require(not on, f"weighted point {point} lies on the boundary")
    interior = measure.score(s, closed=False)
    _require(interior == CHELOKOT_SCORE, f"score {interior} is not the printed fraction")
    _require(interior < CHELOKOT_LEAN_CEILING < 1, "the Lean ceiling 199/200 is not above it")
    return {"interior": interior, "closed": measure.score(s, closed=True)}


def check_local_repairs(a: Fraction, b: Fraction) -> dict[str, dict[str, Fraction]]:
    """The two mass-preserving local repairs each fail on an axis-parallel corner square.

    `alpha` is `[9/10, 9/10 + 101/100] x [0, 101/100]`: its left side on the column of
    `(9/10, 1)`, so that point is on its boundary; it captures `(1, 9/10)`, the whole
    of both extensions at the corner `(1, 1)`, and almost nothing else. Nagamochi's
    measure gives it `1.0191`; drop the extensions and it falls to `0.9691`, whichever
    way their mass is moved. The augmented measure passes both squares and costs `2/5`.
    """
    beta = shrink(
        karakus_contact_square(DECLARED_T[0]),
        shrink_factor(DECLARED_T[0]),
        centre(karakus_contact_square(DECLARED_T[0])),
    )
    alpha = axis_square(NINE_TENTHS, Fraction(0), SIDE_CEILING)
    _require(inside_container(alpha, a, b) and inside_container(beta, a, b), "witness outside")
    base = nagamochi_measure(a, b)
    report: dict[str, dict[str, Fraction]] = {
        "nagamochi": {
            "total": base.total(),
            "alpha": base.score(alpha, closed=False),
            "beta": base.score(beta, closed=False),
        }
    }
    _require(report["nagamochi"]["alpha"] > 1 > report["nagamochi"]["beta"], "baseline wrong")
    for variant in ("weight", "slide", "augment"):
        repaired = local_repair(a, b, variant)
        report[variant] = {
            "total": repaired.total(),
            "alpha": repaired.score(alpha, closed=False),
            "beta": repaired.score(beta, closed=False),
        }
    for variant in ("weight", "slide"):
        _require(report[variant]["total"] == base.total(), f"{variant} changed the total")
        _require(report[variant]["beta"] > 1, f"{variant} does not rescue K_t")
        _require(report[variant]["alpha"] < 1, f"{variant} is not defeated by alpha")
    _require(report["augment"]["total"] == base.total() + Fraction(2, 5), "augment total")
    _require(min(report["augment"]["alpha"], report["augment"]["beta"]) > 1, "augment fails")
    return report


# -- the replacement bound ----------------------------------------------------------


def karakus_bound(n: int) -> Decimal:
    """Corollary 6.2 of Karakus: `1/2 + sqrt(N - floor(sqrt N) + 1/4)`, nonsquare `N >= 8`."""
    k = math.isqrt(n)
    if k * k == n or n < 8:
        message = f"Corollary 6.2 is stated for nonsquare N >= 8, not N = {n}"
        raise ValueError(message)
    with localcontext() as context:
        context.prec = DECIMAL_DIGITS
        return (1 + Decimal(4 * n - 4 * k + 1).sqrt()) / 2


def karakus_at_most_nagamochi(n: int) -> tuple[bool, bool]:
    """Exactly: is Karakus's bound at most Theorem 2's closed form, and is it equal?

    With `k = floor(sqrt N)`, `u = N - k + 1/4` and `v = N - 2k + 1`:
    `1/2 + sqrt u <= 1 + sqrt v` iff `u - v - 1/4 <= sqrt v` iff `k - 1 <= sqrt v` iff
    `k^2 <= N`, strict iff `N` is not a square; and `1/2 + sqrt u <= k + 1 = ceil(sqrt N)`
    iff `N <= k^2 + 2k`, with equality iff `N = (k + 1)^2 - 1`. The closed form is the
    minimum of the two, so Karakus is below it with equality exactly at `N = m^2 - 1`.
    """
    k = math.isqrt(n)
    if k * k == n or n < 8:
        message = f"Corollary 6.2 is stated for nonsquare N >= 8, not N = {n}"
        raise ValueError(message)
    below_root = k * k <= n  # strict for nonsquare N
    below_ceiling = n <= k * k + 2 * k  # always; equality at N = (k+1)^2 - 1
    equal = n == (k + 1) * (k + 1) - 1
    return below_root and below_ceiling, equal


def karakus_above_area(n: int) -> bool:
    """Exactly: `1/2 + sqrt(N - k + 1/4) > sqrt N` iff `N > k^2`, so for every nonsquare `N`."""
    k = math.isqrt(n)
    return n > k * k


def compare_bounds(n: int) -> dict[str, Decimal | None]:
    """Area bound, Theorem 2's closed form and Corollary 6.2 at one `N`, to 30 digits."""
    with localcontext() as context:
        context.prec = DECIMAL_DIGITS
        area = Decimal(n).sqrt()
        nagamochi, _ = theorem_two(n)
        k = math.isqrt(n)
        karakus = None if (k * k == n or n < 8) else karakus_bound(n)
    return {"area": area, "nagamochi": nagamochi, "karakus": karakus}


REVIEW_N = (7, 12, 14, 23, 26, 34, 47, 82, 97)


def main() -> int:
    for a, b in DECLARED_CONTAINERS:
        for t in DECLARED_T:
            report = check_karakus_member(t, a, b)
            print(
                f"[0,{a}]x[0,{b}] t={t}: contact {report['contact_closed']} "
                f"(= 29/20 + t + t^2/2 + t^3/2), shrunk interior {report['shrunk_interior']} "
                f"= {float(report['shrunk_interior']):.6f} < 1"
            )
    chelokot = check_chelokot_instance()
    interior = chelokot["interior"]
    print(f"chelokot in [0,4]^2: interior {interior} = {float(interior):.9f}")
    repairs = check_local_repairs(Fraction(4), Fraction(4))
    for variant, values in repairs.items():
        print(
            f"{variant:>9}: total {values['total']}, alpha {float(values['alpha']):.4f}, "
            f"beta {float(values['beta']):.4f}"
        )
    for n in range(8, 401):
        if math.isqrt(n) ** 2 == n:
            continue
        below, equal = karakus_at_most_nagamochi(n)
        if not (below and karakus_above_area(n)) or equal != (
            n == (math.isqrt(n) + 1) ** 2 - 1
        ):
            print(f"N={n}: the exact comparison failed")
            return 1
    print("N in [8, 400], nonsquare: area < Karakus <= Nagamochi, equality only at N = m^2 - 1")
    for n in REVIEW_N:
        values = compare_bounds(n)
        karakus = (
            "n/a (needs N >= 8)" if values["karakus"] is None else f"{values['karakus']:.6f}"
        )
        print(
            f"N={n:>3}: area {values['area']:.6f}  Nagamochi {values['nagamochi']:.6f}  "
            f"Karakus {karakus}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
