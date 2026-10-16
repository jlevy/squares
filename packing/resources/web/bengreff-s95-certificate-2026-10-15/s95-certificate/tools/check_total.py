#!/usr/bin/env python3
"""Exact checks on a "mixed 1" cover file: well-formedness, non-negative integer weights,
container [0, K]^2 with K = ceil(sqrt(N)), and total mass < N (exact rationals). Standard library only.

usage: python3 check_total.py COVER [N]
"""
import sys
from fractions import Fraction as F

path = sys.argv[1]
n = int(sys.argv[2]) if len(sys.argv) > 2 else 76
K = next(k for k in range(1, n + 1) if k * k >= n)
toks = [ln.split() for ln in open(path) if ln.strip() and not ln.startswith("#")]
assert toks[0] == ["mixed", "1"], "not a mixed-1 cover"
s_num, s_den = map(int, toks[1]); D = int(toks[2][0]); W = int(toks[3][0]); m = int(toks[4][0])
assert (s_num, s_den) == (K, 1) and D > 0 and W > 0
S = K * D
pts = [tuple(map(int, t)) for t in toks[5:5 + m]]
assert len(pts) == m and all(len(p) == 3 for p in pts)
k = int(toks[5 + m][0])
segs = [tuple(map(int, t)) for t in toks[6 + m:6 + m + k]]
assert len(segs) == k and all(len(s) == 5 for s in segs)
assert toks[6 + m + k] == ["0"] and len(toks) == 7 + m + k, "trailing data or polygons present"
for X, Y, w in pts:
    assert 0 <= X <= S and 0 <= Y <= S and w >= 0
for X0, Y0, X1, Y1, w in segs:
    assert (X0 == X1) != (Y0 == Y1), "segment not axis-parallel or degenerate"
    assert all(0 <= v <= S for v in (X0, Y0, X1, Y1)) and w >= 0
total = F(sum(w for _, _, w in pts) + sum(s[4] for s in segs), W)
print("points %d, segments %d, coordinate unit 1/%d, weight unit 1/%d" % (m, k, D, W))
print("total mass = %s = %.9f" % (total, float(total)))
assert total < n, "total is not below %d" % n
print("OK: all weights >= 0, all atoms in [0,%d]^2, total < %d" % (K, n))
