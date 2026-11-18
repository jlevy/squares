"""Contraction to first contact, exactly (lane r127b-1118).

The owner's option D (think-b0w5) asks for a predecessor's side "once the predecessor
is itself shrunk until its squares first touch". This module measures that on a
certificate's own poses, in exact rational arithmetic:

- every centre is scaled by one factor ``lam`` (about any point: the result is defined
  up to translation), each square keeping its size and its angle;
- a pair has disjoint interiors at ``lam`` exactly when ``lam >= f``, its contact
  factor ``f = H / max_w |d . w|`` (method A's numbers), so the first contact of the
  contraction is ``lam* = max f`` over all pairs, at the pairs that attain it;
- the shrunk packing's side is the side of the smallest square box that holds it, the
  larger of its width and height at ``lam*``, each the span of ``lam * x_k +- h_k``,
  ``h_k`` the square's half-extent.

The contraction margin is the certificate's side less that shrunk side. It is the sum of
two parts, given apart: the side less the packing's own extent at scale 1 (the box's
slack), and the extent less the shrunk side (the gaps the contraction closes).

Uses method A's integer pose numbers and ``fractions.Fraction``; decides nothing about
feasibility, which ``rb127_decide`` decides and the controls K1c and K1p check on the
shrunk packing itself.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from typing import Any

import rb127_axes as A
import rb127_fmt as F

Q = tuple[int, int]


def extent(ip: list[A.IPose], lam: Fraction) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Width, height, and the least x and y reached, of the packing with centres scaled."""
    xs_lo = []
    xs_hi = []
    ys_lo = []
    ys_hi = []
    for p in ip:
        x, y = A.centre(p)
        h = A.half_extent(p)
        xs_lo.append(lam * x - h)
        xs_hi.append(lam * x + h)
        ys_lo.append(lam * y - h)
        ys_hi.append(lam * y + h)
    return max(xs_hi) - min(xs_lo), max(ys_hi) - min(ys_lo), min(xs_lo), min(ys_lo)


def factors(ip: list[A.IPose]) -> list[tuple[Fraction | None, tuple[int, int]]]:
    out = []
    for i, j in combinations(range(len(ip)), 2):
        out.append((A.contact_factor(ip[i], ip[j]), (i + 1, j + 1)))
    return out


def contraction(rows: list[tuple[Q, Q, Q, Q]], side: Q) -> dict[str, Any]:
    ip = [A.to_ipose(*r) for r in rows]
    if not all(A.is_unit(p) for p in ip):
        raise ValueError("a pose is not a unit square")
    S = Fraction(side[0], side[1])
    fs = factors(ip)
    if any(f is None for f, _ in fs):
        raise ValueError("two centres coincide")
    ranked = sorted(((f, p) for f, p in fs if f is not None), key=lambda t: (-t[0], t[1]))
    lam_star = ranked[0][0]
    binding = [p for f, p in ranked if f == lam_star]
    nxt = next((f for f, _ in ranked if f != lam_star), None)
    w1, h1, _, _ = extent(ip, Fraction(1))
    ext1 = max(w1, h1)
    out: dict[str, Any] = {
        "side": F.exact(S),
        "extent_width": F.exact(w1),
        "extent_height": F.exact(h1),
        "extent": F.exact(ext1),
        "side_less_extent": F.exact(S - ext1),
        "side_less_extent_sci": F.sci(S - ext1, 8),
        "lambda_star": F.exact(lam_star),
        "one_minus_lambda_star": F.exact(1 - lam_star),
        "one_minus_lambda_star_sci": F.sci(1 - lam_star, 8),
        "binding_pairs": [list(p) for p in binding],
        "next_factor_gap_sci": None if nxt is None else F.sci(lam_star - nxt, 8),
    }
    if lam_star > 1:
        out["feasible_at_scale_1"] = False
        out["note"] = "a pair overlaps at scale 1: no contraction margin"
        return out
    out["feasible_at_scale_1"] = True
    wc, hc, x0, y0 = extent(ip, lam_star)
    shrunk = max(wc, hc)
    margin = S - shrunk
    out.update(
        {
            "shrunk_width": F.exact(wc),
            "shrunk_height": F.exact(hc),
            "shrunk_side": F.exact(shrunk),
            "shrunk_side_ceil12": F.ceil_places(shrunk, 12),
            "shrunk_side_floor20": F.floor_places(shrunk, 20),
            "margin": F.exact(margin),
            "margin_sci": F.sci(margin, 8),
            "contraction_part": F.exact(ext1 - shrunk),
            "contraction_part_sci": F.sci(ext1 - shrunk, 8),
            "_shrunk_side": shrunk,
            "_margin": margin,
            "_lam": lam_star,
            "_x0": x0,
            "_y0": y0,
        }
    )
    return out


def shrunk_rows(rows: list[tuple[Q, Q, Q, Q]], lam: Fraction) -> tuple[list[tuple[Q, Q, Q, Q]], Q]:
    """The packing with centres scaled by ``lam``, moved into the corner of the smallest
    square box that holds it, and that box's side."""
    ip = [A.to_ipose(*r) for r in rows]
    w, h, x0, y0 = extent(ip, lam)
    side = max(w, h)
    out = []
    for r, p in zip(rows, ip, strict=True):
        x, y = A.centre(p)
        nx = lam * x - x0
        ny = lam * y - y0
        out.append(((nx.numerator, nx.denominator), (ny.numerator, ny.denominator), r[2], r[3]))
    return out, (side.numerator, side.denominator)
