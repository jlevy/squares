"""Exact capture of a core of #910's certificate at a rational pose.

F_r(p) = sum_k rho_k |R_k n Q_r(p)|, where Q_r(p) is the closed square of side B,
centre p and angle theta_r = 2 atan(r D), whose cosine and sine are the exact rationals
(1 - t^2)/(1 + t^2) and 2t/(1 + t^2). Each |R_k n Q| is computed by clipping the
square's four exact vertices against the rectangle's four half-planes
(Sutherland-Hodgman) and the shoelace formula, all in gmpy2.mpq, so the result is
the exact rational value. A float filter discards rectangles at least 1e-6 clear of
the square's bounding box, which meet no part of it.

This is a different computation from the section integrals of bnb.py, so the two
check each other.

Usage as a program: capture_exact.py CERT_GZ R X Y [MASS_FACTOR]
(X, Y and MASS_FACTOR as exact rationals 'a/b').
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from gmpy2 import mpq

from xzcommon import Certificate, direction, expand, frac_str, load_certificate

Pt = tuple[mpq, mpq]


def clip(poly: list[Pt], axis: int, bound: mpq, keep_ge: bool) -> list[Pt]:
    """Clip a convex polygon to the half-plane coord[axis] >= bound (or <= bound)."""
    out: list[Pt] = []
    n = len(poly)
    for i in range(n):
        P = poly[i]
        Q = poly[(i + 1) % n]
        pin = P[axis] >= bound if keep_ge else P[axis] <= bound
        qin = Q[axis] >= bound if keep_ge else Q[axis] <= bound
        if pin:
            out.append(P)
        if pin != qin:
            t = (bound - P[axis]) / (Q[axis] - P[axis])
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out


def poly_area(poly: list[Pt]) -> mpq:
    n = len(poly)
    if n < 3:
        return mpq(0)
    s = mpq(0)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return abs(s) / 2


class Evaluator:
    """Exact capture for one certificate (optionally with every mass scaled)."""

    def __init__(self, cert: Certificate, mass_factor: mpq = mpq(1)) -> None:
        self.cert = cert
        self.dens = expand(cert, mass_factor)
        self.keys = list(self.dens)
        self.arr = np.array([[float(v) for v in k] for k in self.keys])
        self.h = cert.B / 2

    def square(self, r: int, px: mpq, py: mpq) -> list[Pt]:
        dr = direction(self.cert, r)
        h, c, s = self.h, dr.c, dr.s
        # u = (c, s), v = (-s, c); vertices p + h(u - v), p + h(u + v), p + h(-u + v),
        # p + h(-u - v), counterclockwise.
        return [
            (px + h * (c + s), py + h * (s - c)),
            (px + h * (c - s), py + h * (s + c)),
            (px + h * (-c - s), py + h * (c - s)),
            (px + h * (s - c), py + h * (-s - c)),
        ]

    def capture(self, r: int, px: mpq, py: mpq) -> mpq:
        sq = self.square(r, px, py)
        xs = [float(v[0]) for v in sq]
        ys = [float(v[1]) for v in sq]
        m = (
            (self.arr[:, 0] < max(xs) + 1e-6)
            & (self.arr[:, 2] > min(xs) - 1e-6)
            & (self.arr[:, 1] < max(ys) + 1e-6)
            & (self.arr[:, 3] > min(ys) - 1e-6)
        )
        total = mpq(0)
        for idx in np.nonzero(m)[0]:
            k = self.keys[int(idx)]
            x1, y1, x2, y2 = k
            poly = clip(sq, 0, x1, True)
            poly = clip(poly, 0, x2, False)
            poly = clip(poly, 1, y1, True)
            poly = clip(poly, 1, y2, False)
            a = poly_area(poly)
            if a:
                total += self.dens[k] * a
        return total

    def in_domain(self, r: int, px: mpq, py: mpq) -> dict[str, bool]:
        dr = direction(self.cert, r)
        L = self.cert.L
        in_dom = all(dr.margin <= v <= L - dr.margin for v in (px, py))
        in_quad = all(L / 2 <= v <= dr.U for v in (px, py))
        return {"in_per_bin_domain": in_dom, "in_quadrant": in_quad}


def main() -> int:
    cert = load_certificate(Path(sys.argv[1]))
    r = int(sys.argv[2])
    px, py = mpq(sys.argv[3]), mpq(sys.argv[4])
    factor = mpq(sys.argv[5]) if len(sys.argv) > 5 else mpq(1)
    ev = Evaluator(cert, factor)
    val = ev.capture(r, px, py)
    print(f"r={r} p=({frac_str(px)}, {frac_str(py)}) factor={frac_str(factor)}")
    print(f"capture = {float(val):.18f}")
    print(f"exact   = {frac_str(val)[:200]}{'...' if len(frac_str(val)) > 200 else ''}")
    print(ev.in_domain(r, px, py))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
