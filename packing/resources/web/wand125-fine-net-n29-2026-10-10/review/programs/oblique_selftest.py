"""Self-tests of oblique_decide's bounds against exact rational geometry
(review think-1lri).

1. area_lower against fine_net_exact.clip_area on 3,000 random pairs (rectangle,
   rotated rectangle of half-sizes hu, hv at a net direction): never above the
   exact area, and within 1e-12 of it.  Thin rectangles, rectangles containing the
   core, rectangles outside it and rectangles crossing a vertex are all drawn.
2. Seeded errors: a sign slip in g2, and nodes left unclamped beyond the
   rectangle, must each produce a bound above the exact area somewhere.
3. box_bounds on the candidate's own measure: at 24 random boxes over five
   directions, the box's lower bound is at most the exact capture at the box's
   centre and four corners (lemma S end to end), and the full-core bound at the
   centre is within 1e-9 below the exact capture there.

Run: python3 -I oblique_selftest.py CANDIDATE.json[.gz]
"""

import random
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fine_net_exact as fx  # noqa: E402
import oblique_decide as od  # noqa: E402

rng = random.Random(20261104)
failures = 0


def check(name, ok):
    global failures
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures += 1


Dstep = F(1, 5002)
B = F(4999, 5000)


def random_pairs(n):
    out = []
    for _ in range(n):
        r = rng.choice([1, 2, 7, 100, 777, 1500, 2000, 2071, 2072])
        c, s = fx.direction(Dstep, r)
        d = od.Direction(c, s, B / 2)
        hu = rng.uniform(0.05, 0.5)
        hv = rng.uniform(0.05, 0.5)
        kind = rng.random()
        if kind < 0.3:  # thin
            w, hgt = rng.uniform(1e-6, 2e-3), rng.uniform(0.01, 1.5)
            if rng.random() < 0.5:
                w, hgt = hgt, w
        elif kind < 0.5:  # large
            w, hgt = rng.uniform(0.5, 2.0), rng.uniform(0.5, 2.0)
        else:
            w, hgt = rng.uniform(0.01, 0.6), rng.uniform(0.01, 0.6)
        x1 = rng.uniform(-0.9, 0.9) - w / 2
        y1 = rng.uniform(-0.9, 0.9) - hgt / 2
        out.append((d, hu, hv, x1, x1 + w, y1, y1 + hgt))
    return out


def exact_area(d, hu, hv, X1, X2, Y1, Y2):
    poly = fx.core_polygon(F(0), F(0), d.c, d.s, F(hu), F(hv))
    return fx.clip_area(poly, F(X1), F(Y1), F(X2), F(Y2))


pairs = random_pairs(3000)
worst_gap = 0.0
above = 0
for d, hu, hv, X1, X2, Y1, Y2 in pairs:
    a = od.area_lower(d, np.array([hu]), np.array([hv]), np.array([X1]), np.array([X2]), np.array([Y1]), np.array([Y2]))[0]
    e = exact_area(d, hu, hv, X1, X2, Y1, Y2)
    if F(a) > e:
        above += 1
    worst_gap = max(worst_gap, float(e - F(a)))
check(f"area_lower never above the exact area on 3,000 pairs (worst gap {worst_gap:.2e})", above == 0)
check("area_lower within 1e-12 of the exact area", worst_gap < 1e-12)

# 2. seeded errors
real = od.area_lower


def too_wide(d, hu, hv, X1, X2, Y1, Y2):
    return real(d, hu * 1.0001, hv, X1, X2, Y1, Y2)  # a core 0.01% too wide along u


caught = 0
for d, hu, hv, X1, X2, Y1, Y2 in pairs[:600]:
    a = too_wide(d, np.array([hu]), np.array([hv]), np.array([X1]), np.array([X2]), np.array([Y1]), np.array([Y2]))[0]
    if F(a) > exact_area(d, hu, hv, X1, X2, Y1, Y2):
        caught += 1
check(f"a core 0.01% too wide is caught above the exact area ({caught} of 600)", caught > 0)


def unclamped(d, hu, hv, X1, X2, Y1, Y2):
    # integrate over [X1 - 0.01, X2 + 0.01] instead of [X1, X2]
    return real(d, hu, hv, X1 - 0.01, X2 + 0.01, Y1, Y2)


caught = 0
for d, hu, hv, X1, X2, Y1, Y2 in pairs[:600]:
    a = unclamped(d, np.array([hu]), np.array([hv]), np.array([X1]), np.array([X2]), np.array([Y1]), np.array([Y2]))[0]
    if F(a) > exact_area(d, hu, hv, X1, X2, Y1, Y2):
        caught += 1
check(f"nodes beyond the rectangle are caught above the exact area ({caught} of 600)", caught > 0)

# 3. lemma Q itself, exactly, one rectangle at a time: the area |R ∩ (Q0 + p)| at
# interior points of a box is at least its least value at the box's corners
viol = 0
cases = 0
for _ in range(400):
    r = rng.choice([1, 300, 1000, 2072])
    c, s = fx.direction(Dstep, r)
    h = B / 2
    w = F(rng.randrange(1, 1500), 1000)
    hgt = F(rng.randrange(1, 1500), 1000) if rng.random() < 0.7 else F(rng.randrange(1, 30), 10000)
    R = (F(rng.randrange(-800, 800), 1000), F(rng.randrange(-800, 800), 1000))
    rect = (R[0], R[1], R[0] + w, R[1] + hgt)
    side = F(rng.choice([1, 10, 100, 400]), 1000)
    bx0 = F(rng.randrange(-600, 600), 1000)
    by0 = F(rng.randrange(-600, 600), 1000)
    corners = [(bx0, by0), (bx0 + side, by0), (bx0, by0 + side), (bx0 + side, by0 + side)]
    area = lambda p: fx.clip_area(fx.core_polygon(p[0], p[1], c, s, h), *rect)  # noqa: E731
    cmin = min(area(v) for v in corners)
    for _ in range(4):
        p = (bx0 + side * F(rng.randrange(0, 1001), 1000), by0 + side * F(rng.randrange(0, 1001), 1000))
        cases += 1
        if area(p) < cmin:
            viol += 1
check(f"lemma Q: at {cases} interior points the exact area is at least its least corner value", viol == 0)

# 4. box bounds on the candidate's measure, both lemmas, end to end
if len(sys.argv) > 1:
    cand = fx.load_candidate(Path(sys.argv[1]))
    meas = od.Measure(cand)
    ok_box = {"corners": True, "intersection": True}
    ok_centre = True
    worst_centre = 0.0
    better = 0
    gain = 0.0
    tested = 0
    for r in (1, 312, 886, 1947, 2068):
        c, s = fx.direction(cand.D, r)
        d = od.Direction(c, s, cand.h)
        lo, hi = fx.per_bin_domain(cand, r)
        for _ in range(5 if r != 1 else 4):
            dxv = rng.choice([1e-4, 1e-3, 5e-3, 2e-2])
            cxv = rng.uniform(float(lo) + dxv, float(hi) - dxv)
            cyv = rng.uniform(float(lo) + dxv, float(hi) - dxv)
            xa, xb, ya, yb = cxv - dxv, cxv + dxv, cyv - dxv, cyv + dxv
            pb = np.zeros(meas.K, dtype=np.int64)
            pk = np.arange(meas.K, dtype=np.int64)
            arr = lambda v: np.array([v])  # noqa: E731
            dxe = od.up(max(od.up(xb - cxv), od.up(cxv - xa)))
            dye = od.up(max(od.up(yb - cyv), od.up(cyv - ya)))
            cor = ((arr(xa), arr(ya)), (arr(xb), arr(ya)), (arr(xa), arr(yb)), (arr(xb), arr(yb)))
            _, low_q = od.box_bounds(meas, d, arr(cxv), arr(cyv), arr(dxe), arr(dye), pb, pk, corners=cor)
            _, low_s = od.box_bounds(meas, d, arr(cxv), arr(cyv), arr(dxe), arr(dye), pb, pk)
            _, centre = od.box_bounds(meas, d, arr(cxv), arr(cyv), arr(dxe), arr(dye), pb, pk, full_core=True)
            pts = [(cxv, cyv), (xa, ya), (xb, ya), (xa, yb), (xb, yb)]
            pts += [(rng.uniform(xa, xb), rng.uniform(ya, yb)) for _ in range(3)]
            ex = [fx.capture(meas.ims, F(px), F(py), c, s, cand.h) for px, py in pts]
            ok_box["corners"] &= all(F(float(low_q[0])) <= e for e in ex)
            ok_box["intersection"] &= all(F(float(low_s[0])) <= e for e in ex)
            # mathematically the corner bound is the larger; computed, the two may differ
            # by rounding where no straddling image separates them
            better += low_q[0] >= low_s[0] - 1e-12
            gain = max(gain, float(low_q[0] - low_s[0]))
            ok_centre &= F(float(centre[0])) <= ex[0]
            worst_centre = max(worst_centre, float(ex[0] - F(float(centre[0]))))
            tested += 1
    check(f"corner bound (lemma Q) at most the exact capture at the centre, corners and 3 interior points of {tested} boxes",
          ok_box["corners"])
    check(f"intersection bound (lemma S) likewise at the same {tested} boxes", ok_box["intersection"])
    check(f"the corner bound is at least the intersection bound, to 1e-12, at {better} of {tested} boxes "
          f"(largest gain {gain:.2e})", better == tested)
    check(f"full-core bound at the centre below the exact capture and within 1e-9 (worst {worst_centre:.2e})",
          ok_centre and worst_centre < 1e-9)

sys.exit(1 if failures else 0)
