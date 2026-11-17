"""Lane L186, method A: separating axes in Python integers, from the corners.

Each square's eight corner coordinates are written over one positive integer
denominator D (their least common multiple), so its corners are integer points
Q_k / D. Its edges E_k = Q_{k+1} - Q_k are integer vectors.

The square is accepted as a unit square when every edge has squared length D^2,
E_0 . E_1 = 0, E_2 = -E_0 and E_3 = -E_1: a parallelogram with two
perpendicular unit sides. The sign of cross(E_0, E_1) = +-D^2 is its listing
sense.

Its two unit normals are E_0 / D and E_1 / D, exact. On a unit normal w of
either square of a pair, each square's four corners project to an interval, and
the gap on w is how far apart the two intervals are (negative when they
overlap), an exact distance because w has length exactly 1. The pair's margin
is the greatest of its four gaps. Two convex polygons have disjoint interiors
exactly when some line parallel to an edge of one of them weakly separates them
(0 lies outside the interior of their Minkowski difference, whose edges are
parallel to theirs), so margin > 0 is apart, margin = 0 is contact with
disjoint interiors and margin < 0 is overlap.

A wall's clearance is the signed distance from the square's extreme corner to
the wall: min x, min y, S - max x, S - max y.

Nothing here filters by distance: every pair is decided.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import lcm

from l186_reader import Square


@dataclass
class SqA:
    den: int
    q: list[tuple[int, int]]
    e0: tuple[int, int]
    e1: tuple[int, int]
    unit: bool
    sense: int
    # own projections on e0 and e1, numerators over den^2
    p0: tuple[int, int]
    p1: tuple[int, int]


def prepare(sq: Square) -> SqA:
    den = 1
    for x, y in sq:
        den = lcm(den, x.denominator, y.denominator)
    q = [(int(x * den), int(y * den)) for x, y in sq]
    edges = [(q[(k + 1) % 4][0] - q[k][0], q[(k + 1) % 4][1] - q[k][1]) for k in range(4)]
    d2 = den * den
    e0, e1, e2, e3 = edges
    unit = (
        all(ex * ex + ey * ey == d2 for ex, ey in edges)
        and e0[0] * e1[0] + e0[1] * e1[1] == 0
        and e2 == (-e0[0], -e0[1])
        and e3 == (-e1[0], -e1[1])
    )
    cross = e0[0] * e1[1] - e0[1] * e1[0]
    sense = 1 if cross > 0 else (-1 if cross < 0 else 0)
    if unit and cross not in (d2, -d2):
        unit = False
    pr0 = [e0[0] * qx + e0[1] * qy for qx, qy in q]
    pr1 = [e1[0] * qx + e1[1] * qy for qx, qy in q]
    return SqA(
        den=den,
        q=q,
        e0=e0,
        e1=e1,
        unit=unit,
        sense=sense,
        p0=(min(pr0), max(pr0)),
        p1=(min(pr1), max(pr1)),
    )


def _axis_gaps(a: SqA, b: SqA) -> list[tuple[int, int]]:
    """Gaps on a's two normals, each as (numerator, denominator) over a.den^2 * b.den."""
    out: list[tuple[int, int]] = []
    denom = a.den * a.den * b.den
    for e, own in ((a.e0, a.p0), (a.e1, a.p1)):
        lo_a, hi_a = own[0] * b.den, own[1] * b.den
        pr = [(e[0] * qx + e[1] * qy) * a.den for qx, qy in b.q]
        lo_b, hi_b = min(pr), max(pr)
        out.append((max(lo_b - hi_a, lo_a - hi_b), denom))
    return out


def pair_margin(a: SqA, b: SqA) -> Fraction:
    gaps = _axis_gaps(a, b) + _axis_gaps(b, a)
    best_n, best_d = gaps[0]
    for gn, gd in gaps[1:]:
        if gn * best_d > best_n * gd:
            best_n, best_d = gn, gd
    return Fraction(best_n, best_d)


def wall_clearances(a: SqA, side: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Left, bottom, right, top clearances, exact."""
    xs = [qx for qx, _ in a.q]
    ys = [qy for _, qy in a.q]
    d = a.den
    return (
        Fraction(min(xs), d),
        Fraction(min(ys), d),
        side - Fraction(max(xs), d),
        side - Fraction(max(ys), d),
    )


def sign_class(v: Fraction) -> str:
    return "apart" if v > 0 else ("touch" if v == 0 else "overlap")
