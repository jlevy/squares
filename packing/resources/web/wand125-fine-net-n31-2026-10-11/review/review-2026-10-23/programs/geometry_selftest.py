"""Self-test of n31_geometry against a second, brute-force exact method.

Usage: python3 -I geometry_selftest.py OUTPUT.json [CASES]

For directions 0, 1, 2, 7, 296, 1036, 1777, 2071 and 2072 of the 1/5002 net, and CASES
random rectangles and rotated boxes each (seeded, so the run repeats), it compares:

- area16 with the area of the intersection computed by Sutherland-Hodgman clipping of
  the rotated box's four vertices against the rectangle, in Fractions, then the
  shoelace formula;
- chord_sigma and chord_omega with the segment clipped against the rectangle in
  Fractions along its own parametrisation.

Cases are biased toward the hard ones: rectangles 1/1000 thin, near-parallel edges at
direction 1, boxes that contain, miss or cut a rectangle, corners on edges.
Prints PASS or the first mismatch, and writes counts to OUTPUT.json.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import n31_exact as nx  # noqa: E402
import n31_geometry as ng  # noqa: E402

STEP = Fraction(1, 5002)


def clip(poly, inside, cross):
    out = []
    for k in range(len(poly)):
        p, q = poly[k], poly[(k + 1) % len(poly)]
        ip, iq = inside(p), inside(q)
        if ip:
            out.append(p)
        if ip != iq:
            out.append(cross(p, q))
    return out


def area_brute(rect, centre, half_u, half_v, cos, sin):
    x0, y0, x1, y1 = rect
    cx, cy = centre
    ux, uy, vx, vy = cos, sin, -sin, cos
    poly = [(cx + a * half_u * ux + b * half_v * vx, cy + a * half_u * uy + b * half_v * vy)
            for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]

    def along_x(bound, keep_ge):
        def inside(p):
            return p[0] >= bound if keep_ge else p[0] <= bound

        def cross(p, q):
            t = (bound - p[0]) / (q[0] - p[0])
            return (bound, p[1] + t * (q[1] - p[1]))
        return inside, cross

    def along_y(bound, keep_ge):
        def inside(p):
            return p[1] >= bound if keep_ge else p[1] <= bound

        def cross(p, q):
            t = (bound - p[1]) / (q[1] - p[1])
            return (p[0] + t * (q[0] - p[0]), bound)
        return inside, cross

    for inside, cross in (along_x(x0, True), along_x(x1, False), along_y(y0, True),
                          along_y(y1, False)):
        if not poly:
            return Fraction(0)
        poly = clip(poly, inside, cross)
    if len(poly) < 3:
        return Fraction(0)
    twice = sum(poly[k][0] * poly[(k + 1) % len(poly)][1]
                - poly[(k + 1) % len(poly)][0] * poly[k][1] for k in range(len(poly)))
    return abs(twice) / 2


def segment_in_rect(p, d, lo, hi, rect):
    """Length of {p + t d : lo <= t <= hi} inside the closed rectangle; |d| = 1."""
    x0, y0, x1, y1 = rect
    for k, (a, b) in enumerate(((x0, x1), (y0, y1))):
        pk, dk = p[k], d[k]
        if dk == 0:
            if not a <= pk <= b:
                return Fraction(0)
            continue
        ta, tb = (a - pk) / dk, (b - pk) / dk
        if ta > tb:
            ta, tb = tb, ta
        lo, hi = max(lo, ta), min(hi, tb)
    return hi - lo if hi > lo else Fraction(0)


def main() -> int:
    start = time.process_time()
    out_path = Path(sys.argv[1])
    cases = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rng = random.Random(20261023)
    grid = 10**6
    big = 2**12
    counts = {"area": 0, "chord_sigma": 0, "chord_omega": 0, "nonzero_area": 0,
              "partial_area": 0}
    for j in (0, 1, 2, 7, 296, 1036, 1777, 2071, 2072):
        if j == 0:
            c_i, s_i, e_i = 1, 0, 1
        else:
            c_i, s_i, e_i = nx.direction(j, STEP)
        cos, sin = Fraction(c_i, e_i), Fraction(s_i, e_i)
        e2 = e_i * e_i
        g = grid * big  # grid units per unit length
        norm_area = 2 * c_i * s_i * e2 if s_i else 1
        norm_chord = c_i * s_i * e_i if s_i else 1
        for _ in range(cases):
            kind = rng.random()
            x0 = Fraction(rng.randrange(0, 3 * grid), grid)
            y0 = Fraction(rng.randrange(0, 3 * grid), grid)
            if kind < 0.3:
                w, hgt = Fraction(rng.randrange(1, 2000), grid), Fraction(1, 1000)
            elif kind < 0.5:
                w, hgt = Fraction(1, 1000), Fraction(rng.randrange(1, 2 * grid), grid)
            else:
                w = Fraction(rng.randrange(1, 2 * grid), grid)
                hgt = Fraction(rng.randrange(1, 2 * grid), grid)
            rect = (x0, y0, x0 + w, y0 + hgt)
            cx = x0 + Fraction(rng.randrange(-grid, 2 * grid), grid)
            cy = y0 + Fraction(rng.randrange(-grid, 2 * grid), grid)
            if rng.random() < 0.1:
                cx, cy = x0, y0  # a corner of the rectangle at the centre
            hu = Fraction(rng.randrange(1, grid), 2 * grid)
            hv = Fraction(rng.randrange(1, grid), 2 * grid)
            # Integer version: grid coordinates, E-scaled rotated box.
            xs = [int(v * g) for v in rect]
            gx0, gy0, gx1, gy1 = xs
            corners = tuple((c_i * xx + s_i * yy, -s_i * xx + c_i * yy)
                            for xx, yy in ((gx0, gy0), (gx1, gy0), (gx0, gy1), (gx1, gy1)))
            gcx, gcy = int(cx * g), int(cy * g)
            sig0, om0 = c_i * gcx + s_i * gcy, -s_i * gcx + c_i * gcy
            # Half-sides must be E-scaled grid integers: choose them on the E-grid.
            hu_i, hv_i = int(hu * g * e_i), int(hv * g * e_i)
            hu_q, hv_q = Fraction(hu_i, g * e_i), Fraction(hv_i, g * e_i)
            got = ng.area16(corners, sig0 - hu_i, sig0 + hu_i, om0 - hv_i, om0 + hv_i,
                            c_i, s_i, e2)
            want = area_brute(rect, (cx, cy), hu_q, hv_q, cos, sin)
            if Fraction(got, norm_area * g * g) != want:
                print("MISMATCH area", j, rect, cx, cy, hu_q, hv_q, got, want)
                return 1
            counts["area"] += 1
            counts["nonzero_area"] += want > 0
            counts["partial_area"] += 0 < want < w * hgt
            # Chords along sigma = t (direction v) and omega = t (direction u).
            t_sig = sig0 + rng.randrange(-hu_i, hu_i + 1)
            got = ng.chord_sigma(t_sig, om0 - hv_i, om0 + hv_i, gx0, gx1, gy0, gy1,
                                 c_i, s_i, e2)
            # The point sigma = t_sig, omega = om0 in real coordinates:
            sig_r, om_r = Fraction(t_sig, e_i * g), Fraction(om0, e_i * g)
            base = (sig_r * cos - om_r * sin, sig_r * sin + om_r * cos)
            want = segment_in_rect(base, (-sin, cos), -hv_q, hv_q, rect)
            if Fraction(got, norm_chord * g) != want:
                print("MISMATCH chord_sigma", j, rect, got, want)
                return 1
            counts["chord_sigma"] += 1
            t_om = om0 + rng.randrange(-hv_i, hv_i + 1)
            got = ng.chord_omega(t_om, sig0 - hu_i, sig0 + hu_i, gx0, gx1, gy0, gy1,
                                 c_i, s_i, e2)
            sig_r, om_r = Fraction(sig0, e_i * g), Fraction(t_om, e_i * g)
            base = (sig_r * cos - om_r * sin, sig_r * sin + om_r * cos)
            want = segment_in_rect(base, (cos, sin), -hu_q, hu_q, rect)
            if Fraction(got, norm_chord * g) != want:
                print("MISMATCH chord_omega", j, rect, got, want)
                return 1
            counts["chord_omega"] += 1
    out = {"kind": "review-2026-10-23-n31-geometry-selftest/v1", "status": "PASS",
           "counts": counts, "cases_per_direction": cases,
           "program_sha256": nx.sha256_file(Path(__file__)),
           "geometry_sha256": nx.sha256_file(Path(ng.__file__)),
           "cpu_seconds": round(time.process_time() - start, 3)}
    out_path.write_text(json.dumps(out, indent=1) + "\n")
    print("PASS", counts, f"cpu {out['cpu_seconds']} s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
