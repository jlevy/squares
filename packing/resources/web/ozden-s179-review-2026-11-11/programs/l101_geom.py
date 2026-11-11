"""Exact constructions for the self-test, the plan facts and the controls. Decides nothing.

It builds modified squares (translations, reflections, transpositions) and computes, for a
pair, the exact time at which translating one square along the line of centres brings
the pair to contact. Every outcome is decided by the two methods, not here.
"""

from __future__ import annotations

from fractions import Fraction

Pt = tuple[Fraction, Fraction]


def to_fracs(points: list) -> list[Pt]:
    return [(Fraction(*x), Fraction(*y)) for x, y in points]


def to_ints(points: list[Pt]) -> list:
    return [((x.numerator, x.denominator), (y.numerator, y.denominator)) for x, y in points]


def square_from(p0: Pt, u: Pt, sense: int = 1) -> list:
    """Corners p0, p0+u, p0+u+v, p0+v with v = sense * perp(u), as reader integers."""
    v = (-u[1] * sense, u[0] * sense)
    pts = [p0, (p0[0] + u[0], p0[1] + u[1]), (p0[0] + u[0] + v[0], p0[1] + u[1] + v[1]),
           (p0[0] + v[0], p0[1] + v[1])]
    return to_ints(pts)


def centre(points: list) -> Pt:
    p = to_fracs(points)
    return ((p[0][0] + p[2][0]) / 2, (p[0][1] + p[2][1]) / 2)


def translate(points: list, dx: Fraction, dy: Fraction) -> list:
    return to_ints([(x + dx, y + dy) for x, y in to_fracs(points)])


def reflect_horizontal(points: list) -> list:
    """Reflect in the horizontal line through the square's centre."""
    cy = centre(points)[1]
    return to_ints([(x, 2 * cy - y) for x, y in to_fracs(points)])


def transpose(points: list) -> list:
    return to_ints([(y, x) for x, y in to_fracs(points)])


def axes(points: list) -> list[Pt]:
    p = to_fracs(points)
    u = (p[1][0] - p[0][0], p[1][1] - p[0][1])
    return [u, (-u[1], u[0])]


def interval(points: list, a: Pt) -> tuple[Fraction, Fraction]:
    vals = [x * a[0] + y * a[1] for x, y in to_fracs(points)]
    return min(vals), max(vals)


def pieces(fixed: list, moving: list, w: Pt) -> list[tuple[Fraction, Fraction]]:
    """(alpha, beta): the gap along each axis is max of alpha + beta * t over its pieces."""
    out = []
    for a in axes(fixed) + axes(moving):
        s = w[0] * a[0] + w[1] * a[1]
        lo_f, hi_f = interval(fixed, a)
        lo_m, hi_m = interval(moving, a)
        out.append((lo_m - hi_f, s))
        out.append((lo_f - hi_m, -s))
    return out


def closing(fixed: list, moving: list) -> dict:
    """Translate `moving` by t * w, w = centre(fixed) - centre(moving).

    The margin is max over pieces of alpha + beta * t, convex in t, positive at 0 for an
    apart pair and negative at t = 1, where the centres coincide. Contact is first reached at T = max over beta < 0 of
    alpha / -beta. `past` is T + eps with the active pieces' least |beta| * eps = 1e-30,
    so the margin there is exactly -1e-30 if every active piece decreases.
    """
    cf, cm = centre(fixed), centre(moving)
    w = (cf[0] - cm[0], cf[1] - cm[1])
    ps = pieces(fixed, moving, w)
    t_contact = max(alpha / -beta for alpha, beta in ps if beta < 0)
    values = [alpha + beta * t_contact for alpha, beta in ps]
    active = [beta for (alpha, beta), v in zip(ps, values, strict=True) if v == 0]
    assert max(values) == 0, "contact time does not give margin 0"
    all_decreasing = all(beta < 0 for beta in active)
    least = min(-beta for beta in active) if all_decreasing else None
    eps = Fraction(1, 10**30) / least if least else None
    move = (w[0] * t_contact, w[1] * t_contact)
    return {
        "w": w,
        "t_contact": t_contact,
        "t_past": t_contact + eps if eps is not None else None,
        "active_all_decreasing": all_decreasing,
        "move_l1": abs(move[0]) + abs(move[1]),
        "move": move,
    }


def moved(points: list, w: Pt, t: Fraction) -> list:
    return translate(points, w[0] * t, w[1] * t)
