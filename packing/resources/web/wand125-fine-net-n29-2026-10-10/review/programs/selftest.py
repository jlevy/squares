"""Self-tests of fine_net_exact on synthetic data (review think-1lri).

1. Partition: tile a box containing the core by a random grid of rectangles; the
   clipped areas sum to B^2 exactly, at six net directions of the 2,073-node net.
2. Axis: capture with (c, s) = (1, 0) equals the product-of-overlaps formula.
3. Quarter turn (lemma C1): for a D4-averaged measure, the capture at centre p
   equals the capture at p turned by pi/2 about (L/2, L/2); a reflection does not
   preserve it at an oblique angle (so the test can fail).
4. Directions: c^2 + s^2 = 1 exactly; rho(0) = 1/2; tan(pi/8) bracketed.
5. D4: the eight images of a rectangle are closed under the generators.
6. The strict number reader refuses non-canonical spellings Fraction() accepts.
7. A seeded wrong clip (an edge moved) makes test 1 fail.

Run: python3 -I selftest.py   (prints PASS lines; exits 1 on any failure)
"""

import random
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fine_net_exact as fx  # noqa: E402

rng = random.Random(20261104 + 29)
failures = 0


def check(name, ok):
    global failures
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        failures += 1


B = F(4999, 5000)
h = B / 2
D = F(1, 5002)
L = F(291, 50)


def grid_partition(x0, x1, y0, y1, k):
    xs = sorted({x0, x1, *(x0 + (x1 - x0) * F(rng.randrange(1, 10**6), 10**6) for _ in range(k))})
    ys = sorted({y0, y1, *(y0 + (y1 - y0) * F(rng.randrange(1, 10**6), 10**6) for _ in range(k))})
    return [(xs[i], ys[j], xs[i + 1], ys[j + 1]) for i in range(len(xs) - 1) for j in range(len(ys) - 1)]


# 1. partition
ok = True
for r in (0, 1, 777, 1500, 2071, 2072):
    c, s = fx.direction(D, r)
    px = F(3) + F(rng.randrange(10**6), 10**7)
    py = F(2) + F(rng.randrange(10**6), 10**7)
    poly = fx.core_polygon(px, py, c, s, h)
    tiles = grid_partition(px - 1, px + 1, py - 1, py + 1, 7)
    tot = sum(fx.clip_area(poly, *t) for t in tiles)
    ok &= tot == B * B
check("partition of the core's neighbourhood sums to B^2 at r in {0,1,777,1500,2071,2072}", ok)

# 2. axis
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
    px = F(rng.randrange(500, 5320), 1000)
    py = F(rng.randrange(500, 5320), 1000)
    ok &= fx.capture(ims, px, py, F(1), F(0), h) == fx.axis_capture(ims, px, py, h)
check("axis capture equals the product of overlaps at 10 centres", ok)

# 3. quarter turn, and a reflection as its negative control
ok = True
differs = False
for r in (1, 900, 2072):
    c, s = fx.direction(D, r)
    for _ in range(3):
        px = F(rng.randrange(800, 5000), 1000)
        py = F(rng.randrange(800, 5000), 1000)
        a = fx.capture(ims, px, py, c, s, h)
        b = fx.capture(ims, L - py, px, c, s, h)  # (x, y) -> (L - y, x)
        ok &= a == b
        differs |= a != fx.capture(ims, py, px, c, s, h)  # reflection in y = x
check("capture is invariant under the quarter turn about the centre (lemma C1)", ok)
check("a reflection in y = x changes an oblique capture (C1 uses no reflection)", differs)

# 4. directions and rho
ok = all(sum(v * v for v in fx.direction(D, r)) == 1 for r in range(0, 2073, 37))
check("c^2 + s^2 = 1 exactly at every 37th node", ok)
ok = fx.rho(F(0)) == F(1, 2)
lo, hi = F(41421356, 10**8), F(41421357, 10**8)
ok &= lo * lo + 2 * lo - 1 < 0 < hi * hi + 2 * hi - 1
check("rho(0) = 1/2 and tan(pi/8) bracketed by its polynomial", ok)

# 5. D4 closure
ok = True
for _ in range(20):
    x1 = F(rng.randrange(0, 4000), 1000)
    y1 = F(rng.randrange(0, 4000), 1000)
    x2 = x1 + F(rng.randrange(1, 1000), 1000)
    y2 = y1 + F(rng.randrange(1, 1000), 1000)
    orbit = set(fx.d4_images(L, x1, y1, x2, y2))
    for a1, b1, a2, b2 in list(orbit):
        ok &= (b1, a1, b2, a2) in orbit  # swap
        ok &= (L - a2, b1, L - a1, b2) in orbit  # x -> L - x
        ok &= (a1, L - b2, a2, L - b1) in orbit  # y -> L - y
check("the eight images are closed under the three generators of D4", ok)

# 6. strict reader
bad = ["1e-3", " 5.82", "5.82 ", "1_000", "-1", "+1", ".5", "5.", "01", "1/0", "0x10", "1/-2", "nan"]
refused = 0
for text in bad:
    try:
        fx.rational(text)
    except (ValueError, TypeError, ZeroDivisionError):
        refused += 1
good = ["0", "5.82", "291/50", "1/5002", "2899999/100000", "0.9998"]
accepted = all(fx.rational(t) == F(t) for t in good)
check(f"strict reader refuses {refused} of {len(bad)} non-canonical spellings and reads the canonical ones", refused == len(bad) and accepted)

# 7. seeded wrong clip
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
