"""Direction r = 0 of #910's certificate, decided in exact integer arithmetic.

At theta = 0 the core is the axis-aligned square of side B, so for the expanded
rectangles R_k = [x1,x2] x [y1,y2] with densities rho_k,

    F(x, y) = sum_k rho_k * o(x; x1, x2) * o(y; y1, y2),  o(z; z1, z2) = |[z-h, z+h] n [z1, z2]|,

with h = B/2. Each o is continuous and piecewise affine with breakpoints z1 +- h, z2 +- h,
so on every cell of the grid E x E, where E is the set of all breakpoints inside the
quadrant [L/2, U_0] together with both ends, F is affine in x for fixed y and in y for
fixed x (bilinear), and its minimum over the closed quadrant is attained at a vertex of
E x E. By the quarter turn (lemma C1) the quadrant stands for the whole per-bin domain
[1/2, L - 1/2]^2 at r = 0 (margin rho(0) = 1/2).

The program computes F at every vertex exactly: all values are integers over the common
denominator P * Dc^2, with Dc the l.c.m. of the coordinate denominators and P that of
the densities, and each column is swept in y by exact slope updates. It reports the
exact minimum and its vertex, and the same for the 99/100 mutant (exactly 99/100 F).

Usage: axis_exact.py CERT_GZ OUT_JSON [UPPER]

With UPPER (an exact rational) the quadrant is [L/2, UPPER] instead of [L/2, U_0]; with
UPPER = L - lambda/2 it is Hosono's own axis domain, mapped by the dilation.
"""

from __future__ import annotations

import json
import sys
import time
from bisect import bisect_left
from math import lcm
from pathlib import Path

from gmpy2 import mpq, mpz

from xzcommon import direction, expand, frac_str, load_certificate


def main() -> int:
    t0 = time.process_time()
    cert = load_certificate(Path(sys.argv[1]))
    out_path = Path(sys.argv[2])
    upper = mpq(sys.argv[3]) if len(sys.argv) > 3 else None
    L, B = cert.L, cert.B
    h = B / 2
    dens = expand(cert)
    keys = list(dens)
    U = direction(cert, 0).U
    lo = L / 2
    assert U == L - mpq(1, 2)
    if upper is not None:
        assert lo < upper <= U
        U = upper

    # Events: every breakpoint of every o in [lo, U], and both ends. By the D4
    # invariance of the expanded density (premises.py) the y-events are the x-events,
    # but they are computed separately here.
    def events(axis: int) -> list[mpq]:
        ev = {lo, U}
        for k in keys:
            z1, z2 = (k[0], k[2]) if axis == 0 else (k[1], k[3])
            for e in (z1 - h, z1 + h, z2 - h, z2 + h):
                if lo <= e <= U:
                    ev.add(e)
        return sorted(ev)

    EX = events(0)
    EY = events(1)
    print(f"x events {len(EX)}, y events {len(EY)}, vertices {len(EX) * len(EY)}")

    # Common denominators.
    Dc = 1
    for v in [h, lo, U, *(c for k in keys for c in k)]:
        Dc = lcm(Dc, int(v.denominator))
    P = 1
    for d in dens.values():
        P = lcm(P, int(d.denominator))
    Dcq = mpq(Dc)
    print(f"Dc bits {Dc.bit_length()}, P bits {P.bit_length()}")

    def I(v: mpq) -> int:  # noqa: E743
        w = v * Dcq
        assert w.denominator == 1
        return int(w.numerator)

    hI = I(h)
    EYI = [I(e) for e in EY]
    loI = EYI[0]
    rhoP = [mpz(int((dens[k] * P).numerator)) for k in keys]
    for k in keys:
        assert (dens[k] * P).denominator == 1

    def overlap(zI: int, z1: int, z2: int) -> int:
        return max(0, min(zI + hI, z2) - max(zI - hI, z1))

    # Per rectangle: y-breakpoint indices in EY and slope steps (+1, -1, -1, +1).
    ybreak: list[list[tuple[int, int]]] = []
    for k in keys:
        y1, y2 = I(k[1]), I(k[3])
        lst = []
        for val, step in ((y1 - hI, 1), (y2 - hI, -1), (y1 + hI, -1), (y2 + hI, 1)):
            lst.append((val, step))
        ybreak.append(lst)
    xb = [(I(k[0]), I(k[2])) for k in keys]
    yb = [(I(k[1]), I(k[3])) for k in keys]

    nY = len(EYI)
    best = None
    best_at: tuple[int, int] | None = None
    vertices = 0
    for ix, xv in enumerate(EX):
        xI = I(xv)
        active = []
        for idx in range(len(keys)):
            ox = overlap(xI, *xb[idx])
            if ox:
                active.append((idx, rhoP[idx] * ox))
        # Initial value at y0 and slope at or below y0; steps at events above y0.
        steps = [mpz(0)] * nY
        G = mpz(0)
        sigma = mpz(0)
        for idx, a in active:
            y1, y2 = yb[idx]
            G += a * overlap(loI, y1, y2)
            for val, step in ybreak[idx]:
                if val <= loI:
                    sigma += step * a
                else:
                    j = bisect_left(EYI, val)
                    if j < nY:
                        assert EYI[j] == val
                        steps[j] += step * a
        colmin = G
        colarg = 0
        prev = loI
        for j in range(1, nY):
            yj = EYI[j]
            G += sigma * (yj - prev)
            sigma += steps[j]
            prev = yj
            if G < colmin:
                colmin, colarg = G, j
        vertices += nY
        if best is None or colmin < best:
            best, best_at = colmin, (ix, colarg)
        if ix % 500 == 0:
            print(f"  column {ix}/{len(EX)}: running min {float(mpq(best, P * Dc * Dc)):.15f}", flush=True)

    assert best is not None and best_at is not None
    Fmin = mpq(best, P * Dc * Dc)
    xa, ya = EX[best_at[0]], EY[best_at[1]]
    # Check the minimum vertex by direct evaluation.
    direct = mpq(0)
    for k, d in dens.items():
        ox = max(mpq(0), min(xa + h, k[2]) - max(xa - h, k[0]))
        oy = max(mpq(0), min(ya + h, k[3]) - max(ya - h, k[1]))
        direct += d * ox * oy
    mut = mpq(99, 100) * Fmin
    rep = {
        "r": 0,
        "x_events": len(EX),
        "y_events": len(EY),
        "vertices": vertices,
        "min_capture_exact": frac_str(Fmin),
        "min_capture_float": float(Fmin),
        "argmin": [frac_str(xa), frac_str(ya)],
        "argmin_float": [float(xa), float(ya)],
        "quadrant_upper": frac_str(U),
        "argmin_on_wall_edge": xa == U or ya == U,
        "direct_evaluation_agrees": direct == Fmin,
        "verdict": "verified" if Fmin >= 1 else "refused",
        "mutant_99_100_min_capture_exact": frac_str(mut),
        "mutant_99_100_min_capture_float": float(mut),
        "mutant_refused": mut < 1,
        "cpu_seconds": time.process_time() - t0,
    }
    for key, v in rep.items():
        print(f"{key}: {v}")
    out_path.write_text(json.dumps(rep, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
