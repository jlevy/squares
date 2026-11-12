"""Check a packing by the area of the union of its squares, computed with Shapely in binary64.

Usage:
  python check_shapely.py nN_exact.json

If no two squares overlap, the union of the n unit squares has area n. The script also reports the largest pairwise
intersection area and the bounding box of the union. It is a plausibility check in rounded arithmetic."""
import sys, json
from fractions import Fraction
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

d = json.load(open(sys.argv[1]))
S = float(Fraction(d['side'])); polys = []
for q in d['squares']:
    x, y, c, s = (float(Fraction(v)) for v in q)
    polys.append(Polygon([(x + a * c / 2 - b * s / 2, y + a * s / 2 + b * c / 2) for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]))
n = len(polys)
u = unary_union(polys)
tree = STRtree(polys); worst = 0.0
for i, p in enumerate(polys):
    for j in tree.query(p):
        if j > i: worst = max(worst, p.intersection(polys[j]).area)
x0, y0, x1, y1 = u.bounds
print('n = %d, side %.15f' % (n, S))
print('area of the union: %.10f' % u.area)
print('largest pairwise intersection area: %.3e' % worst)
print('bounding box of the union: [%.3e, %.15f] x [%.3e, %.15f]' % (x0, x1, y0, y1))
print('PASS' if abs(u.area - n) < 1e-8 and worst < 1e-10 and x0 > -1e-12 and y0 > -1e-12 and x1 < S + 1e-12 and y1 < S + 1e-12 else 'FAIL')
