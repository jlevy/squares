"""Exact constructions for the self-test and the controls (review L83, clean room).

Centre-line closing: square b moves by t * (c_a - c_b). On each of the pair's four
axes both projection gaps are linear in t, so the margin is the maximum of eight
linear functions, convex in t, positive at t = 0 and negative at t = 1 (centres
coincide). Its one root in (0, 1) is max(-a_k / b_k) over the slopes b_k < 0.
"""

from __future__ import annotations

from fractions import Fraction

Pt = tuple[Fraction, Fraction]


def pq(x: Fraction) -> tuple[int, int]:
    return (x.numerator, x.denominator)


def to_pq(pts: list[Pt]):
    return [(pq(x), pq(y)) for x, y in pts]


def from_pq(corners) -> list[Pt]:
    return [(Fraction(*x), Fraction(*y)) for x, y in corners]


def pyth(m: int, k: int) -> Pt:
    """A rational unit vector ((m^2 - k^2), 2mk) / (m^2 + k^2)."""
    d = m * m + k * k
    return (Fraction(m * m - k * k, d), Fraction(2 * m * k, d))


def make_square(cx: Fraction, cy: Fraction, u: Pt, sense: int = 1, start: int = 0) -> list[Pt]:
    ux, uy = u
    vx, vy = (-uy, ux) if sense == 1 else (uy, -ux)
    p0 = (cx - ux / 2 - vx / 2, cy - uy / 2 - vy / 2)
    pts = [p0, (p0[0] + ux, p0[1] + uy), (p0[0] + ux + vx, p0[1] + uy + vy), (p0[0] + vx, p0[1] + vy)]
    return pts[start:] + pts[:start]


def centre(pts: list[Pt]) -> Pt:
    return ((pts[0][0] + pts[2][0]) / 2, (pts[0][1] + pts[2][1]) / 2)


def translate(pts: list[Pt], dx: Fraction, dy: Fraction) -> list[Pt]:
    return [(x + dx, y + dy) for x, y in pts]


def _axes(pts: list[Pt]) -> list[Pt]:
    ux, uy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
    return [(ux, uy), (-uy, ux)]


def _proj(pts: list[Pt], a: Pt) -> list[Fraction]:
    return [x * a[0] + y * a[1] for x, y in pts]


def closing_parameter(a: list[Pt], b: list[Pt]) -> Fraction:
    """t at which b, moved by t * (c_a - c_b), first touches a."""
    ca, cb = centre(a), centre(b)
    d = (ca[0] - cb[0], ca[1] - cb[1])
    best = Fraction(0)
    for axis in _axes(a) + _axes(b):
        pa, pb = _proj(a, axis), _proj(b, axis)
        s = d[0] * axis[0] + d[1] * axis[1]
        lines = [(min(pb) - max(pa), s), (min(pa) - max(pb), -s)]
        for a0, b0 in lines:
            if b0 < 0:
                best = max(best, -a0 / b0)
    return best


def close_pair(a: list[Pt], b: list[Pt], extra: Fraction = Fraction(0)) -> list[Pt]:
    """b moved along the centre line to contact with a, plus `extra` of the parameter."""
    t = closing_parameter(a, b) + extra
    ca, cb = centre(a), centre(b)
    return translate(b, t * (ca[0] - cb[0]), t * (ca[1] - cb[1]))


def reflect_h(pts: list[Pt]) -> list[Pt]:
    """Each square reflected in its own horizontal centre line, corner order kept."""
    cy = centre(pts)[1]
    return [(x, 2 * cy - y) for x, y in pts]


def scale_about_centre(pts: list[Pt], f: Fraction) -> list[Pt]:
    cx, cy = centre(pts)
    return [(cx + f * (x - cx), cy + f * (y - cy)) for x, y in pts]
