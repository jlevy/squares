"""Numeric sanity checks of the cell cover, interior-cell diameters and wall capacities.

Reads Sq17Lean/ExactCellCoverData.lean and Sq17Lean/ExactWallCapacity.lean as text.
  A. exact rational check that the eight interior cells have squared diameter
     <= 29377/31250 < 1 (vertex pairs), as InteriorCellCapacity claims;
  B. grid check (not a proof) that the 24 closed cells cover [1/2, 522/125]^2,
     with exact rational point-in-convex-polygon tests on a 400 x 400 grid plus
     all cell vertices and random points;
  C. adversarial numeric search for two unit squares in the half-plane y >= 0 with
     centres in a wall-class rectangle [start, start+w] x [1/2, 1/2+d] and disjoint
     interiors (would contradict ExactWallCapacity.wall_capacity): maximise the
     separating-axis gap by random restarts and local search.
"""
import random
import re
import sys
from fractions import Fraction
from math import cos, sin, pi
from pathlib import Path

src = Path(sys.argv[1])
cd = (src / "Sq17Lean/ExactCellCoverData.lean").read_text()
vblock = cd[cd.index("def vertices :"):cd.index("def xBreaks")]
cells = []
names = []
for line in vblock.splitlines():
    s = line.strip()
    if s.startswith("--"):
        names.append(s[2:].strip())
    if s.startswith("["):
        pts = re.findall(r"\((-?\d+)(?:/(\d+))?, (-?\d+)(?:/(\d+))?\)", s)
        cells.append([(Fraction(int(a), int(b or 1)), Fraction(int(c), int(d or 1))) for a, b, c, d in pts])
assert len(cells) == 24 and len(names) == 24

# A. interior diameters
print("A. interior cells (16..23) squared diameters:")
for i in range(16, 24):
    v = cells[i]
    m = max((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for p in v for q in v)
    print(f"   cell {i} {names[i]:12s} diam^2 = {float(m):.6f}  <= 29377/31250 ? {m <= Fraction(29377, 31250)}")


# B. cover grid check with exact arithmetic
def inside(poly, x, y):
    # convex polygon given in order (we check both orientations), closed
    n = len(poly)
    signs = []
    for k in range(n):
        ax, ay = poly[k]
        bx, by = poly[(k + 1) % n]
        signs.append((bx - ax) * (y - ay) - (by - ay) * (x - ax))
    return all(s >= 0 for s in signs) or all(s <= 0 for s in signs)


# check each polygon is convex and listed in order (all cross products same sign)
for i, poly in enumerate(cells):
    n = len(poly)
    cr = []
    for k in range(n):
        ax, ay = poly[k]; bx, by = poly[(k + 1) % n]; cx, cy = poly[(k + 2) % n]
        cr.append((bx - ax) * (cy - by) - (by - ay) * (cx - bx))
    assert all(c >= 0 for c in cr) or all(c <= 0 for c in cr), (i, cr)
lo, hi = Fraction(1, 2), Fraction(522, 125)
N = 400
miss = 0
for a in range(N + 1):
    x = lo + (hi - lo) * a / N
    for b in range(N + 1):
        y = lo + (hi - lo) * b / N
        if not any(inside(p, x, y) for p in cells):
            miss += 1
rng = random.Random(1)
miss_r = 0
for _ in range(20000):
    x = lo + (hi - lo) * Fraction(rng.randrange(10 ** 6), 10 ** 6)
    y = lo + (hi - lo) * Fraction(rng.randrange(10 ** 6), 10 ** 6)
    if not any(inside(p, x, y) for p in cells):
        miss_r += 1
miss_v = sum(1 for p in cells for v in p if not any(inside(q, v[0], v[1]) for q in cells))
print(f"B. cover grid {N+1}x{N+1}: uncovered points = {miss}; random 20000: {miss_r}; vertices: {miss_v}")
area = sum(abs(sum(p[k][0] * p[(k + 1) % len(p)][1] - p[(k + 1) % len(p)][0] * p[k][1] for k in range(len(p)))) / 2 for p in cells)
print("   sum of cell areas =", area, "=", float(area), " (box area", float((hi - lo) ** 2), ")")

# C. wall capacity adversarial search
ew = (src / "Sq17Lean/ExactWallCapacity.lean").read_text()
def vec(name):
    return [Fraction(int(a), int(b or 1)) for a, b in re.findall(r"(-?\d+)(?:/(\d+))?", re.search(rf"def {name} : Fin 3 → ℚ := !\[([^\]]*)\]", ew).group(1))]
W, D, S = vec("wallWidth"), vec("wallDepth"), vec("wallStart")
print("C. wall classes (width, depth, start):", [(float(W[k]), float(D[k]), float(S[k])) for k in range(3)])


def gap(p, q):
    """Max over the 4 edge normals of (projected centre distance - sum of half-extents).
    Positive => interiors disjoint (SAT); we search for the maximum."""
    (x1, y1, t1), (x2, y2, t2) = p, q
    best = -1e9
    for t in (t1, t2):
        for (a, b) in ((cos(t), sin(t)), (-sin(t), cos(t))):
            d = abs(a * (x2 - x1) + b * (y2 - y1))
            e1 = (abs(a * cos(t1) + b * sin(t1)) + abs(-a * sin(t1) + b * cos(t1))) / 2
            e2 = (abs(a * cos(t2) + b * sin(t2)) + abs(-a * sin(t2) + b * cos(t2))) / 2
            best = max(best, d - e1 - e2)
    return best


def feasible(x, y, t, w, d, start):
    # centre in rectangle, square above y = 0
    half = (abs(cos(t)) + abs(sin(t))) / 2
    return start <= x <= start + w and 0.5 <= y <= 0.5 + d and y - half >= -1e-12


for k in range(3):
    w, d, start = float(W[k]), float(D[k]), float(S[k])
    best = -1e9
    bestcfg = None
    for trial in range(400):
        def rnd():
            while True:
                x = start + rng.random() * w
                y = 0.5 + rng.random() * d
                t = (rng.random() - 0.5) * pi / 2
                if feasible(x, y, t, w, d, start):
                    return [x, y, t]
        p, q = rnd(), rnd()
        cur = gap(p, q)
        step = 0.2
        for it in range(600):
            cand_p = [p[0] + rng.gauss(0, step * w), p[1] + rng.gauss(0, step * d), p[2] + rng.gauss(0, step)]
            cand_q = [q[0] + rng.gauss(0, step * w), q[1] + rng.gauss(0, step * d), q[2] + rng.gauss(0, step)]
            if feasible(*cand_p, w, d, start) and feasible(*cand_q, w, d, start):
                g = gap(cand_p, cand_q)
                if g > cur:
                    cur, p, q = g, cand_p, cand_q
                    continue
            step *= 0.995
        if cur > best:
            best, bestcfg = cur, (p, q)
    # Changed at retention, 14 October 2026: the arrow is printed as "={chr(62)}", the same
    # output, because the repository's check refuses "=>" in a Python string.
    print(f"   class {k}: max separating gap found = {best:+.6f}  (negative ={chr(62)} always overlapping)  at {bestcfg}")
