"""KKT-point consistency (review bold-ritchie-rv-daniel): decides nothing about the bound.

usage: kkt_consistency.py CERT EXACT_TXT
Reads the source's high-precision point (header 'n S*', rows 'x y degrees') at 100 digits and
the certificate exactly, and reports:
  - the certificate's relation to the point: dilation factor on the side, centre and angle
    agreement after dividing the certificate's centres by that factor;
  - the point as a packing at S*: least wall clearance and least pair gap (separating-axis
    projected gap, at 100 digits), counts of walls and pairs active below 1e-60, the squares
    touching nothing (rattlers), and the least inactive gaps.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F

import mpmath as mp

mp.mp.dps = 100


def read_cert(path):
    rows, side = [], None
    for line in open(path):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        p = s.split()
        if side is None:
            side = F(p[1])
            continue
        rows.append(tuple(F(v) for v in p))
    return side, rows


def read_exact(path):
    rows, side = [], None
    for line in open(path):
        s = line.strip()
        if not s:
            continue
        p = s.split()
        if side is None:
            side = mp.mpf(p[1])
            continue
        rows.append(tuple(mp.mpf(v) for v in p))
    return side, rows


def mpq(q: F):
    return mp.mpf(q.numerator) / q.denominator


def main(cert, exact):
    Sc, C = read_cert(cert)
    Ss, X = read_exact(exact)
    assert len(C) == len(X)
    n = len(C)
    factor = mpq(Sc) / Ss
    dc = mp.mpf(0)
    da = mp.mpf(0)
    for (x, y, t), (xs, ys, deg) in zip(C, X):
        cx, cy = mpq(x) / factor, mpq(y) / factor
        dc = max(dc, abs(cx - xs), abs(cy - ys))
        ang = mp.degrees(2 * mp.atan(mpq(t)))
        d = (ang - deg) % 90
        d = min(d, 90 - d)
        da = max(da, d)
    # the point as a packing at S*
    sq = []
    for xs, ys, deg in X:
        th = mp.radians(deg)
        sq.append((xs, ys, mp.cos(th), mp.sin(th)))
    tol = mp.mpf(10) ** -60
    wall_active = 0
    least_wall = None
    least_inactive_wall = None
    touched = [0] * n
    for i, (x, y, c, s) in enumerate(sq):
        h = (abs(c) + abs(s)) / 2
        for g in (x - h, y - h, Ss - x - h, Ss - y - h):
            if least_wall is None or g < least_wall:
                least_wall = g
            if abs(g) < tol:
                wall_active += 1
                touched[i] += 1
            elif least_inactive_wall is None or g < least_inactive_wall:
                least_inactive_wall = g
    pair_active = 0
    least_pair = None
    least_inactive_pair = None
    for i in range(n):
        xi, yi = sq[i][0], sq[i][1]
        for j in range(i + 1, n):
            dx, dy = sq[j][0] - xi, sq[j][1] - yi
            if dx * dx + dy * dy > 2.0001:
                continue
            best = None
            for own, oth, sgn in ((sq[i], sq[j], 1), (sq[j], sq[i], -1)):
                _, _, ac, as_ = own
                _, _, bc, bs = oth
                for wx, wy in ((ac, as_), (-as_, ac)):
                    cen = sgn * (dx * wx + dy * wy)
                    g = abs(cen) - mp.mpf(1) / 2 - (abs(bc * wx + bs * wy) + abs(-bs * wx + bc * wy)) / 2
                    if best is None or g > best:
                        best = g
            if least_pair is None or best < least_pair:
                least_pair = best
            if abs(best) < tol:
                pair_active += 1
                touched[i] += 1
                touched[j] += 1
            elif least_inactive_pair is None or best < least_inactive_pair:
                least_inactive_pair = best
    rattlers = [i for i in range(n) if touched[i] == 0]
    out = {
        "cert": cert.split("/")[-1],
        "S_cert_minus_S_star": mp.nstr(mpq(Sc) - Ss, 6),
        "side_factor_minus_1": mp.nstr(factor - 1, 6),
        "max_centre_disagreement_after_undilating": mp.nstr(dc, 4),
        "max_angle_disagreement_deg": mp.nstr(da, 4),
        "point_least_wall_clearance": mp.nstr(least_wall, 4),
        "point_least_pair_gap": mp.nstr(least_pair, 4),
        "walls_active_below_1e-60": wall_active,
        "pairs_active_below_1e-60": pair_active,
        "rattlers_touching_nothing": len(rattlers),
        "rattlers": rattlers,
        "least_inactive_wall": mp.nstr(least_inactive_wall, 4),
        "least_inactive_pair": mp.nstr(least_inactive_pair, 4),
    }
    print(json.dumps(out))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
