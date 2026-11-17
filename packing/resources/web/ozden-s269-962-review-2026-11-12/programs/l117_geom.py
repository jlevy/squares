"""Lane L117: exact geometry for the self-test and the controls. Decides nothing.

Clean-room code for the stage 4 review of jlevy/squares#962. A unit square is its centre
c and a rational unit vector u = (cos, sin), with w = u turned a quarter
counterclockwise. Its half-width along a unit vector a is (|a.u| + |a.w|) / 2, so the
closed-form gap of two squares along a is |a.(c_Q - c_P)| less both half-widths, and
the closed-form margin is the largest such gap over the four edge normals. This formula
is independent of method A, which projects corners.

Closing Q toward P along their centre line moves Q by -t d, d = c_Q - c_P. Each gap is
then |a.d| (1 - t) - h_a, so contact is at t* = 1 - min_a h_a / |a.d|, and past it by
eps the margin is -eps times the least |a.d| over the binding axes.
"""

from __future__ import annotations

from fractions import Fraction as F

Pt = tuple[F, F]


def pyth(m: int, k: int) -> tuple[F, F]:
    """A rational unit vector from a Pythagorean triple (m > k > 0)."""
    h = m * m + k * k
    return F(m * m - k * k, h), F(2 * m * k, h)


def square(cx: F, cy: F, u: tuple[F, F], ccw: bool = True, start: int = 0) -> list[Pt]:
    """Corners of the unit square with centre (cx, cy) and edge direction u."""
    ux, uy = u
    wx, wy = -uy, ux
    p0 = (cx - (ux + wx) / 2, cy - (uy + wy) / 2)
    pts = [p0, (p0[0] + ux, p0[1] + uy), (p0[0] + ux + wx, p0[1] + uy + wy), (p0[0] + wx, p0[1] + wy)]
    if not ccw:
        pts = [pts[0], pts[3], pts[2], pts[1]]
    return pts[start:] + pts[:start]


def to_rat(pts: list[Pt]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    return [((x.numerator, x.denominator), (y.numerator, y.denominator)) for x, y in pts]


def from_rat(corners: list[tuple[tuple[int, int], tuple[int, int]]]) -> list[Pt]:
    return [(F(x[0], x[1]), F(y[0], y[1])) for x, y in corners]


def pose(pts: list[Pt]) -> tuple[Pt, Pt, Pt]:
    """Centre and the two edge vectors at corner 0 of a unit square given by corners."""
    p0, p1, p2, p3 = pts
    c = ((p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2)
    return c, (p1[0] - p0[0], p1[1] - p0[1]), (p3[0] - p0[0], p3[1] - p0[1])


def _dot(a: Pt, b: Pt) -> F:
    return a[0] * b[0] + a[1] * b[1]


def axes_terms(P: list[Pt], Q: list[Pt]) -> list[tuple[F, F]]:
    """For each of the four normals a: (|a.d|, h_a), d = c_Q - c_P."""
    cP, uP, wP = pose(P)
    cQ, uQ, wQ = pose(Q)
    d = (cQ[0] - cP[0], cQ[1] - cP[1])
    out = []
    for a in (uP, wP, uQ, wQ):
        h = (abs(_dot(a, uP)) + abs(_dot(a, wP)) + abs(_dot(a, uQ)) + abs(_dot(a, wQ))) / 2
        out.append((abs(_dot(a, d)), h))
    return out


def closed_margin(P: list[Pt], Q: list[Pt]) -> F:
    return max(ad - h for ad, h in axes_terms(P, Q))


def closing(P: list[Pt], Q: list[Pt], eps_margin: F) -> tuple[F, F, F, int]:
    """(t*, t_past, |d|^2 t*^2, binding axes) closing Q toward P; margin -eps_margin past."""
    terms = axes_terms(P, Q)
    ratios = [(h / ad) for ad, h in terms if ad > 0]
    rmin = min(ratios)
    t_star = 1 - rmin
    binding = [ad for ad, h in terms if ad > 0 and h / ad == rmin]
    rate = min(binding)
    t_past = t_star + eps_margin / rate
    cP, _, _ = pose(P)
    cQ, _, _ = pose(Q)
    d = (cQ[0] - cP[0], cQ[1] - cP[1])
    return t_star, t_past, _dot(d, d) * t_star * t_star, len(binding)


def moved(Q: list[Pt], P: list[Pt], t: F) -> list[Pt]:
    """Q translated by -t (c_Q - c_P)."""
    cP, _, _ = pose(P)
    cQ, _, _ = pose(Q)
    dx, dy = cQ[0] - cP[0], cQ[1] - cP[1]
    return [(x - t * dx, y - t * dy) for x, y in Q]


def margin_at(P: list[Pt], Q: list[Pt], t: F) -> F:
    return closed_margin(P, moved(Q, P, t))


def shift(Q: list[Pt], dx: F, dy: F) -> list[Pt]:
    return [(x + dx, y + dy) for x, y in Q]
