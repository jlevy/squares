"""Independent high-precision feasibility check of the upper construction at the exact root (UPPER premise).
For every one of the 136 pairs: the best separating-axis gap max over the 8 options of
n.(c_t - c_o) - 1/2 - h_t(n); for every square: the four wall clearances. Interval arithmetic (mpmath iv,
120 digits) on the Krawczyk-verified root box of radius 1e-100: reports the least upper end (should be >= 0 up to
~1e-95 for exact contacts) and how many pairs/walls are strict (lower end > 0) vs zero-to-precision."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import iv, mp
import geom, rows as R
iv.dps = 120
geo = R.Geo()
side = geo.side
sq = list(range(1, 18))
def axes(lab):
    u = geo.axes[lab - 1]; return (u, (-u[1], u[0]))
def support(lab, n):
    u, v = axes(lab)
    return (abs(R.dot(n, u)) + abs(R.dot(n, v)))/2
strict_pairs = zero_pairs = bad_pairs = 0
worst = None
for i in sq:
    for j in sq:
        if j <= i: continue
        best = None
        for o, t in ((i, j), (j, i)):
            for a in axes(o):
                for s in (1, -1):
                    n = (s*a[0], s*a[1])
                    d = (geo.pts[t-1][0] - geo.pts[o-1][0], geo.pts[t-1][1] - geo.pts[o-1][1])
                    g = R.dot(n, d) - iv.mpf(1)/2 - support(t, n)
                    if best is None or g.b > best.b:
                        best = g
        if best.a > 0: strict_pairs += 1
        elif best.b > -iv.mpf(10)**-90: zero_pairs += 1
        else: bad_pairs += 1
        if worst is None or best.b < worst[0].b: worst = (best, i, j)
strict_w = zero_w = bad_w = 0
for i in sq:
    h = support(i, (iv.mpf(1), iv.mpf(0))); hy = support(i, (iv.mpf(0), iv.mpf(1)))
    for g in (geo.pts[i-1][0] - h, side - geo.pts[i-1][0] - h, geo.pts[i-1][1] - hy, side - geo.pts[i-1][1] - hy):
        if g.a > 0: strict_w += 1
        elif g.b > -iv.mpf(10)**-90: zero_w += 1
        else: bad_w += 1
print('pairs: strict', strict_pairs, 'zero-to-1e-90', zero_pairs, 'overlapping', bad_pairs)
print('walls: strict', strict_w, 'zero-to-1e-90', zero_w, 'outside', bad_w)
print('least pair best-gap upper end', mp.nstr(mp.mpf(worst[0].b), 5), 'pair', worst[1:])
