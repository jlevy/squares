"""Constructions for the self-test and the controls; decides nothing.

Lane L108, blind stage 4 review of jlevy/squares#959. Exact rationals
(fractions.Fraction) throughout. Builds rational unit squares, moves them, and computes
the exact time at which a square moving along the centre line of a pair first touches
the other, from the support widths of centrally symmetric squares. Imports neither
deciding method.
"""

from __future__ import annotations

from fractions import Fraction

FP = tuple[Fraction, Fraction]
Corners = tuple[FP, FP, FP, FP]
RawPoint = tuple[tuple[int, int], tuple[int, int]]
Raw = tuple[RawPoint, RawPoint, RawPoint, RawPoint]


def pythagorean(m: int, k: int) -> tuple[Fraction, Fraction]:
    """(cos, sin) of a rational rotation: ((m^2 - k^2), 2mk) / (m^2 + k^2)."""
    h = m * m + k * k
    return (Fraction(m * m - k * k, h), Fraction(2 * m * k, h))


def square(centre: FP, rot: tuple[Fraction, Fraction], ccw: bool = True, start: int = 0) -> Corners:
    """A unit square about `centre` turned by `rot`, listed counterclockwise (or not) from corner `start`."""
    c, s = rot
    half = Fraction(1, 2)
    local = [(-half, -half), (half, -half), (half, half), (-half, half)]
    pts = [(centre[0] + c * x - s * y, centre[1] + s * x + c * y) for x, y in local]
    if not ccw:
        pts = [pts[0], pts[3], pts[2], pts[1]]
    pts = pts[start:] + pts[:start]
    return (pts[0], pts[1], pts[2], pts[3])


def to_raw(corners: Corners) -> Raw:
    def r(v: Fraction) -> tuple[int, int]:
        return (v.numerator, v.denominator)

    return tuple((r(x), r(y)) for x, y in corners)  # type: ignore[return-value]


def from_raw(raw: Raw) -> Corners:
    return tuple((Fraction(*x), Fraction(*y)) for x, y in raw)  # type: ignore[return-value]


def translate(corners: Corners, d: FP) -> Corners:
    return tuple((x + d[0], y + d[1]) for x, y in corners)  # type: ignore[return-value]


def centre(corners: Corners) -> FP:
    return ((corners[0][0] + corners[2][0]) / 2, (corners[0][1] + corners[2][1]) / 2)


def edge_axes(corners: Corners) -> tuple[FP, FP]:
    """The two edge directions at corner 0 (unit vectors for a unit square)."""
    p0, p1, _p2, p3 = corners
    return ((p1[0] - p0[0], p1[1] - p0[1]), (p3[0] - p0[0], p3[1] - p0[1]))


def width(corners: Corners, axis: FP) -> Fraction:
    values = [axis[0] * x + axis[1] * y for x, y in corners]
    return max(values) - min(values)


def closing(fixed: Corners, moving: Corners) -> dict[str, object]:
    """Move `moving` toward `fixed` along their centre line by tau * (c_fixed - c_moving).

    On each edge axis a of the two squares, the projections are intervals centred at the
    centres' projections, so the gap is |a.D| (1 - tau) - (w_fixed(a) + w_moving(a)) / 2
    with D the centre difference. It is linear and falls as tau grows, so the pair first
    touches at tau* = max over a of 1 - h_a / |a.D|. Returns tau*, the rate |a.D| of each
    axis whose gap is 0 there, and the exact gap function's value at any tau.
    """
    cf, cm = centre(fixed), centre(moving)
    d = (cf[0] - cm[0], cf[1] - cm[1])
    axes = list(edge_axes(fixed)) + list(edge_axes(moving))
    rows: list[tuple[Fraction, Fraction]] = []  # (rate |a.D|, half-sum h_a)
    for a in axes:
        rate = abs(a[0] * d[0] + a[1] * d[1])
        h = (width(fixed, a) + width(moving, a)) / 2
        rows.append((rate, h))
    taus = [1 - h / rate for rate, h in rows if rate != 0]
    tau = max(taus)
    binding = [rate for rate, h in rows if rate != 0 and 1 - h / rate == tau]
    return {"tau": tau, "binding_rates": binding, "rows": rows, "direction": d}


def gap_at(info: dict[str, object], tau: Fraction) -> Fraction:
    """The largest axis gap at tau, from the closed form."""
    rows = info["rows"]
    assert isinstance(rows, list)
    return max(rate * (1 - tau) - h for rate, h in rows)


def moved(moving: Corners, info: dict[str, object], tau: Fraction) -> Corners:
    d = info["direction"]
    assert isinstance(d, tuple)
    return translate(moving, (tau * d[0], tau * d[1]))


def past_tau(info: dict[str, object], depth: Fraction) -> Fraction:
    """The tau at which the binding gap has fallen `depth` below contact (the slowest binding axis)."""
    rates = info["binding_rates"]
    assert isinstance(rates, list)
    tau = info["tau"]
    assert isinstance(tau, Fraction)
    return tau + depth / min(rates)


def clearances(corners: Corners, side: Fraction) -> dict[str, Fraction]:
    xs = [p[0] for p in corners]
    ys = [p[1] for p in corners]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


WALL_DIRECTION: dict[str, FP] = {
    "left": (Fraction(-1), Fraction(0)),
    "bottom": (Fraction(0), Fraction(-1)),
    "right": (Fraction(1), Fraction(0)),
    "top": (Fraction(0), Fraction(1)),
}


def to_wall(corners: Corners, wall: str, distance: Fraction) -> Corners:
    dx, dy = WALL_DIRECTION[wall]
    return translate(corners, (dx * distance, dy * distance))
