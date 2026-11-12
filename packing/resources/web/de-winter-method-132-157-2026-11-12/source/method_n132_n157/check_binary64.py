"""Check a packing in binary64 with a separating-axis test over all pairs of squares.

Usage:
  python check_binary64.py nN_exact.json

Reads the exact rational file, converts every number to binary64 and reports the least clearance to the walls and the
least separation over all pairs. This check shares no code with verify_exact.py. It is a plausibility check in rounded
arithmetic and it proves nothing by itself."""
import sys, json, itertools
from fractions import Fraction
import numpy as np

d = json.load(open(sys.argv[1]))
S = float(Fraction(d['side']))
Q = np.array([[float(Fraction(v)) for v in q] for q in d['squares']])       # centre x, centre y, cos, sin
n = len(Q)
off = np.array([[0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5], [0.5, -0.5]])
C = np.empty((n, 4, 2))
for i, (x, y, c, s) in enumerate(Q):
    C[i, :, 0] = x + off[:, 0] * c - off[:, 1] * s
    C[i, :, 1] = y + off[:, 0] * s + off[:, 1] * c
wall = min(C.min(), S - C.max())
worst = np.inf; pair = None
for i, j in itertools.combinations(range(n), 2):
    if (Q[i, 0] - Q[j, 0]) ** 2 + (Q[i, 1] - Q[j, 1]) ** 2 >= 2.0000001: continue
    best = -np.inf
    for a, b in ((i, j), (j, i)):
        c, s = Q[a, 2], Q[a, 3]
        for ax, ay in ((c, s), (-s, c)):
            centre = Q[a, 0] * ax + Q[a, 1] * ay
            p = C[b, :, 0] * ax + C[b, :, 1] * ay
            best = max(best, p.min() - centre - 0.5, centre - 0.5 - p.max())
    if best < worst: worst, pair = best, (i + 1, j + 1)
print('n = %d, side %.15f' % (n, S))
print('least clearance to a wall: %.3e' % wall)
print('least separation over all pairs: %.3e (squares %d and %d)' % ((worst,) + pair))
print('PASS' if wall > -1e-12 and worst > -1e-12 else 'FAIL', '(tolerance 1e-12)')
