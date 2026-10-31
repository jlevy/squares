"""Distribution of near-contact gaps (SAT margin and wall clearance below 1e-9) in a certificate (think-ikku review)."""
import sys, statistics
from fractions import Fraction as F
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from rv_check import read_cert, pair_margin, extent
for p in sys.argv[1:]:
    n, S, sq = read_cert(p)
    gaps = []
    for i in range(n):
        for j in range(i + 1, n):
            dx, dy = sq[j][0] - sq[i][0], sq[j][1] - sq[i][1]
            if dx * dx + dy * dy > F(9, 4):
                continue
            m = pair_margin(sq[i], sq[j])
            if m < F(1, 10**9):
                gaps.append(float(m))
    walls = []
    for x, y, c, s in sq:
        h = extent(c, s)
        for v in (x - h, S - x - h, y - h, S - y - h):
            if v < F(1, 10**9):
                walls.append(float(v))
    q = lambda a: (min(a), statistics.median(a), max(a)) if a else None
    print(p.rsplit("/", 3)[-3][:28], n, "contacts", len(gaps), "pair gap min/med/max %.3g %.3g %.3g" % q(gaps), "| walls", len(walls), "min/med/max %.3g %.3g %.3g" % q(walls))
