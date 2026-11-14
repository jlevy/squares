"""Lane L153 geometry helpers: builders and closed forms, deciding nothing.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

Used by the self-test (to build squares with known margins and areas) and by the plan
facts and controls (to compute closing moves). A square here is four Fractions
(cx, cy, c, s) with u = (c, s) and v = (-s, c).
"""

from __future__ import annotations

from fractions import Fraction

Pair = tuple[int, int]
Square = tuple[Pair, Pair, Pair, Pair]
FSquare = tuple[Fraction, Fraction, Fraction, Fraction]


def pyth(t: Fraction) -> tuple[Fraction, Fraction]:
    """The rational unit vector ((1 - t^2) / (1 + t^2), 2t / (1 + t^2))."""
    d = 1 + t * t
    return (1 - t * t) / d, 2 * t / d


def encode(sq: FSquare) -> Square:
    """Fractions to the reader's reduced integer pairs."""
    return tuple((f.numerator, f.denominator) for f in sq)  # type: ignore[return-value]


def decode(sq: Square) -> FSquare:
    return tuple(Fraction(p, q) for p, q in sq)  # type: ignore[return-value]


def normals(sq: FSquare) -> list[tuple[Fraction, Fraction]]:
    _, _, c, s = sq
    return [(c, s), (-s, c)]


def half_extent(sq: FSquare, w: tuple[Fraction, Fraction]) -> Fraction:
    """Half-length of the square's projection on the unit vector w."""
    _, _, c, s = sq
    return (abs(c * w[0] + s * w[1]) + abs(-s * w[0] + c * w[1])) / 2


def axes(sq_i: FSquare, sq_j: FSquare) -> list[tuple[Fraction, Fraction, str]]:
    """For each of the four normals: the centre separation d along it, the summed
    half-extents h, and a label; the gap along that normal is |d| - h."""
    out = []
    dx, dy = sq_j[0] - sq_i[0], sq_j[1] - sq_i[1]
    for owner, sq in (("i", sq_i), ("j", sq_j)):
        for k, w in enumerate(normals(sq)):
            d = dx * w[0] + dy * w[1]
            h = half_extent(sq_i, w) + half_extent(sq_j, w)
            out.append((d, h, f"{owner}{'uv'[k]}"))
    return out


def closed_form_margin(sq_i: FSquare, sq_j: FSquare) -> Fraction:
    return max(abs(d) - h for d, h, _ in axes(sq_i, sq_j))


def closing(sq_i: FSquare, sq_j: FSquare) -> dict:
    """Move j along its centre line toward i: C_j(t) = C_j + t (C_i - C_j).

    Each gap is |d| (1 - t) - h, so the margin first reaches 0 at t* = max over the
    normals of 1 - h / |d|. Returns t*, the binding normals (those reaching 0 at t*),
    their rates |d|, and every normal's gap at t*.
    """
    data = axes(sq_i, sq_j)
    times = []
    for d, h, label in data:
        if d != 0:
            times.append((1 - h / abs(d), label))
    t_star = max(t for t, _ in times)
    binding = [label for t, label in times if t == t_star]
    rates = {label: abs(d) for d, _, label in data}
    gaps_at = {label: abs(d) * (1 - t_star) - h for d, h, label in data}
    return {"t": t_star, "binding": binding, "rates": rates, "gaps_at": gaps_at}


def moved(sq_j: FSquare, sq_i: FSquare, t: Fraction) -> FSquare:
    cx, cy, c, s = sq_j
    return (cx + t * (sq_i[0] - cx), cy + t * (sq_i[1] - cy), c, s)


def vertex_on_edge(
    sq_i: FSquare,
    normal_index: int,
    sign: int,
    basis_j: tuple[Fraction, Fraction],
    tau: Fraction,
    delta: Fraction,
) -> tuple[FSquare, Fraction]:
    """Square j with basis_j, its extreme vertex toward i placed at distance delta
    beyond i's edge with outward normal n = sign * (u_i or v_i), at tangential offset
    tau from the edge's midpoint. Returns j and the factor F with overlap area
    F * delta^2 for delta < 0 (F = 1 / (2 |u_j . n| |v_j . n|)).
    """
    w = normals(sq_i)[normal_index]
    n = (sign * w[0], sign * w[1])
    t = (-n[1], n[0])
    cj, sj = basis_j
    uj = (cj, sj)
    vj = (-sj, cj)
    un = uj[0] * n[0] + uj[1] * n[1]
    vn = vj[0] * n[0] + vj[1] * n[1]
    if un == 0 or vn == 0:
        raise ValueError("an edge of j is parallel to the edge of i")
    s1 = -1 if un > 0 else 1
    s2 = -1 if vn > 0 else 1
    off = ((s1 * uj[0] + s2 * vj[0]) / 2, (s1 * uj[1] + s2 * vj[1]) / 2)
    reach = Fraction(1, 2) + delta
    px = sq_i[0] + reach * n[0] + tau * t[0]
    py = sq_i[1] + reach * n[1] + tau * t[1]
    factor = 1 / (2 * abs(un) * abs(vn))
    return (px - off[0], py - off[1], cj, sj), factor


def side_by_side(
    sq_i: FSquare, normal_index: int, sign: int, quarter_turns: int, tau: Fraction, delta: Fraction
) -> FSquare:
    """Square j turned by quarter_turns relative to i, its edge facing i's edge with
    outward normal n at distance delta, offset tau along the edge (|tau| < 1).
    Margin delta; overlap area |delta| (1 - |tau|) for delta < 0."""
    w = normals(sq_i)[normal_index]
    n = (sign * w[0], sign * w[1])
    t = (-n[1], n[0])
    c, s = sq_i[2], sq_i[3]
    for _ in range(quarter_turns % 4):
        c, s = -s, c
    reach = 1 + delta
    return (sq_i[0] + reach * n[0] + tau * t[0], sq_i[1] + reach * n[1] + tau * t[1], c, s)
