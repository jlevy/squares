"""Self-tests of fine_net_exact's clipping and capture, on synthetic data.

1. Partition: tile a box containing the core by a random grid of rectangles;
   the clipped areas sum to B^2 exactly, at several net directions.
2. Axis: capture with (c, s) = (1, 0) equals the product-of-overlaps formula.
3. Quarter turn (lemma C1): for a D4-averaged measure, the capture at centre p
   equals the capture at p turned by pi/2 about (L/2, L/2).
4. Directions: c^2 + s^2 = 1 exactly, and rho(0) = 1/2, rho(tan(pi/8)) = sqrt2/2
   bracketed.
5. Seeded wrong clip (dropping the last half-plane) makes test 1 fail.

Run: python3 -I selftest.py   (prints PASS lines; exits 1 on any failure)
"""

import random
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fine_net_exact as fx  # noqa: E402

rng = random.Random(20261104)
failures = 0


def check(name, ok):
    global failures
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures += 1


B = F(4999, 5000)
h = B / 2
D = F(1, 5002)


def grid_partition(x0, x1, y0, y1, k):
    xs = sorted({x0, x1, *(x0 + (x1 - x0) * F(rng.randrange(1, 10**6), 10**6) for _ in range(k))})
    ys = sorted({y0, y1, *(y0 + (y1 - y0) * F(rng.randrange(1, 10**6), 10**6) for _ in range(k))})
    return [(xs[i], ys[j], xs[i + 1], ys[j + 1]) for i in range(len(xs) - 1) for j in range(len(ys) - 1)]


# 1. partition
ok = True
for r in (0, 1, 777, 1500, 2072):
    c, s = fx.direction(D, r)
    px = F(3) + F(rng.randrange(10**6), 10**7)
    py = F(2) + F(rng.randrange(10**6), 10**7)
    poly = fx.core_polygon(px, py, c, s, h)
    tiles = grid_partition(px - 1, px + 1, py - 1, py + 1, 7)
    tot = sum(fx.clip_area(poly, *t) for t in tiles)
    ok &= tot == B * B
check("partition of the core's neighbourhood sums to B^2 at r in {0,1,777,1500,2072}", ok)

# 2. axis
L = F(2297, 400)
rows = []
for _ in range(40):
    x1 = F(rng.randrange(0, 5000), 1000)
    y1 = F(rng.randrange(0, 5000), 1000)
    w = F(rng.randrange(1, 700), 1000)
    hh = F(rng.randrange(1, 700), 1000)
    rows.append(((x1, y1, min(L, x1 + w), min(L, y1 + hh)), F(rng.randrange(1, 1000), 997)))


class Fake:
    pass


cand = Fake()
cand.rows = rows
cand.L = L
ims = fx.images(cand)
ok = True
for _ in range(10):
    px = F(rng.randrange(500, 5243), 1000)
    py = F(rng.randrange(500, 5243), 1000)
    ok &= fx.capture(ims, px, py, F(1), F(0), h) == fx.axis_capture(ims, px, py, h)
check("axis capture equals the product of overlaps at 10 centres", ok)

# 3. quarter turn
ok = True
for r in (1, 900, 2072):
    c, s = fx.direction(D, r)
    for _ in range(3):
        px = F(rng.randrange(800, 4900), 1000)
        py = F(rng.randrange(800, 4900), 1000)
        a = fx.capture(ims, px, py, c, s, h)
        # rotation by +pi/2 about (L/2, L/2): (x, y) -> (L - y, x)
        b = fx.capture(ims, L - py, px, c, s, h)
        ok &= a == b
check("capture is invariant under the quarter turn about the centre (lemma C1)", ok)

# 4. directions and rho
ok = all(sum(v * v for v in fx.direction(D, r)) == 1 for r in range(0, 2073, 37))
check("c^2 + s^2 = 1 exactly at every 37th node", ok)
ok = fx.rho(F(0)) == F(1, 2)
lo, hi = F(41421356, 10**8), F(41421357, 10**8)  # tan(pi/8) = sqrt2 - 1 bracketed
ok &= lo * lo + 2 * lo - 1 < 0 < hi * hi + 2 * hi - 1
ok &= fx.rho(lo) < fx.rho(hi) + F(1, 10**7)
check("rho(0) = 1/2 and tan(pi/8) bracketed by its polynomial", ok)

# 5. seeded wrong clip
real = fx.clip_area


def wrong(poly, x1, y1, x2, y2):
    return real(poly, x1, y1, x2, y2 + 1)


fx.clip_area = wrong
c, s = fx.direction(D, 500)
poly = fx.core_polygon(F(3), F(3), c, s, h)
tiles = grid_partition(F(2), F(4), F(2), F(4), 5)
tot = sum(fx.clip_area(poly, *t) for t in tiles)
fx.clip_area = real
check("a seeded wrong clip breaks the partition identity", tot != B * B)

sys.exit(1 if failures else 0)
