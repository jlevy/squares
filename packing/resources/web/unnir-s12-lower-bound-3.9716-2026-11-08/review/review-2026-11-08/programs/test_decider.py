"""Differential test of decide_bins.min_capture against a brute-force enumeration.

The brute force shares no data structure with the sweep: it enumerates every
open cell of the box arrangement (consecutive distinct U breakpoints x
consecutive distinct V breakpoints, unbounded end cells included), decides
whether the open cell meets the open domain with an exact separating-axis test
on the four axes U, V, X, Y, and counts the boxes containing the cell directly.

Instances are small random point sets on a coarse grid, so that ties, shared
breakpoints and boundary-touching boxes are frequent.

Usage: python -I test_decider.py [N_CASES] [SEED]
"""

import random
import sys
from fractions import Fraction

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import decide_bins as db  # noqa: E402


def brute_min(pts, side, d, t_r, half_side, lo):
    cn, sn, Q = db.rotation_of_t(t_r)
    A = (half_side * Q * d).__floor__()
    LO = lo * d
    HI = side * d - LO
    Q2 = Q * Q
    us = [cn * x + sn * y for x, y, _ in pts]
    vs = [-sn * x + cn * y for x, y, _ in pts]
    Ub = sorted(set([u - A for u in us] + [u + A for u in us]))
    Vb = sorted(set([v - A for v in vs] + [v + A for v in vs]))
    # domain polygon vertices in (U~, V~)
    verts = [(LO, LO), (HI, LO), (HI, HI), (LO, HI)]
    dv = [(cn * X + sn * Y, -sn * X + cn * Y) for X, Y in verts]
    BIG = 10**40

    def cell_meets_domain(u0, u1, v0, v1):
        # rectangle corners (UV); projections on U, V, X, Y must overlap openly
        rc = [(u0, v0), (u1, v0), (u1, v1), (u0, v1)]

        def proj(points, f):
            vals = [f(p) for p in points]
            return min(vals), max(vals)

        axes = [
            lambda p: p[0],
            lambda p: p[1],
            lambda p: cn * p[0] - sn * p[1],   # Q^2 X
            lambda p: sn * p[0] + cn * p[1],   # Q^2 Y
        ]
        for f in axes:
            a0, a1 = proj(rc, f)
            b0, b1 = proj(dv, f)
            if not (a0 < b1 and b0 < a1):
                return False
        return True

    best = None
    ucells = [(-BIG, Ub[0])] + list(zip(Ub, Ub[1:])) + [(Ub[-1], BIG)]
    vcells = [(-BIG, Vb[0])] + list(zip(Vb, Vb[1:])) + [(Vb[-1], BIG)]
    for u0, u1 in ucells:
        for v0, v1 in vcells:
            if not cell_meets_domain(u0, u1, v0, v1):
                continue
            cap = sum(
                wt for (x, y, wt), pu, pv in zip(pts, us, vs)
                if pu - A <= u0 and u1 <= pu + A and pv - A <= v0 and v1 <= pv + A
            )
            if best is None or cap < best:
                best = cap
    return best


def main():
    n_cases = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    rng = random.Random(int(sys.argv[2]) if len(sys.argv) > 2 else 1)
    d = 40
    fails = 0
    for case in range(n_cases):
        side = Fraction(rng.randint(60, 140), d)        # 1.5 .. 3.5
        m = rng.randint(1, 18)
        grid = rng.choice([4, 8, 40])                    # coarse grids force ties
        pts = []
        for _ in range(m):
            x = rng.randint(0, int(side * d) // (d // grid)) * (d // grid)
            y = rng.randint(0, int(side * d) // (d // grid)) * (d // grid)
            pts.append((min(x, int(side * d)), min(y, int(side * d)), rng.randint(1, 5)))
        t_r = Fraction(rng.choice([0, 1, 1, 2, 3, 5]), rng.choice([7, 9, 12, 40]))
        if t_r >= 1:
            t_r = Fraction(1, 3)
        half = rng.choice([Fraction(1, 2), Fraction(2, 5), Fraction(49, 100), Fraction(1, 4)])
        lo = rng.choice([db.half_extent(t_r), Fraction(1, 2), Fraction(3, 5)])
        if 2 * lo >= side:
            continue
        got, _ = db.min_capture(pts, side, d, t_r, half, lo)
        ref = brute_min(pts, side, d, t_r, half, lo)
        if got != ref:
            fails += 1
            print("MISMATCH", case, got, ref, side, t_r, half, lo, pts)
    print(f"cases={n_cases} mismatches={fails}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
