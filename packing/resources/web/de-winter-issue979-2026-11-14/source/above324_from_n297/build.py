"""n = 332 and n = 409 from the n = 297 packing plus rows of axis-aligned squares. Exact rational arithmetic."""
import json
from fractions import Fraction as F
d = json.load(open('../n297/n297_exact.json'))
S = F(d['side']); base = [tuple(F(v) for v in q) for q in d['squares']]
H = F(1, 2)
def up(x, y): return (F(x) + H, F(y) + H, F(1), F(0))       # axis-aligned square with lower left corner (x, y)
def write(n, side, sq):
    assert len(sq) == n
    json.dump({"n": n, "side": str(side), "square_size": "1", "format": "each square: [center_x, center_y, cos, sin] as exact rationals; (cos, sin) is the unit direction of one edge", "squares": [[str(v) for v in q] for q in sq]}, open('n%d_exact.json' % n, 'w'), indent=0)
# 332: side S + 1, 297 packing moved by (1, 1), 18 squares along the bottom, 17 along the left wall
sq = [(x + 1, y + 1, c, s) for x, y, c, s in base] + [up(i, 0) for i in range(18)] + [up(0, 1 + i) for i in range(17)]
write(332, S + 1, sq)
# 409: side S + 3, 297 packing moved by (3, 3); arms of 3 x 17 squares against the far walls; 10 squares in the corner
T = S + 3; sq = [(x + 3, y + 3, c, s) for x, y, c, s in base]
sq += [up(T - 1 - i, j) for i in range(17) for j in range(3)] + [up(j, T - 1 - i) for i in range(17) for j in range(3)]
a = F(272, 100); t = F(408, 985); c45 = (1 - t * t) / (1 + t * t); s45 = 2 * t / (1 + t * t)
sq += [up(0, 0), up(a - 1, 0), up(0, a - 1), up(a - 1, a - 1), (a / 2, a / 2, c45, s45)]      # five squares in a square of side 2.72
sq += [up(a, 0), up(a, 1), up(a, 2), up(0, a), up(1, a)]
write(409, T, sq)
print('332 side %.13f, 409 side %.13f' % (float(S + 1), float(T)))
