"""Exact check that the rational seed upper-packing-certificate.json is a packing of 17 unit squares in [0, R]^2.

68 wall conditions (17 squares x 4 walls) and 136 pair separations (separating-axis test with the 8 candidate
axes), all in exact rationals. Also reports the wall clearance eps of the flush squares.
Usage: python3 -I seed_packing_check.py SRC_ROOT
"""
import json
import os
import sys
from fractions import Fraction as Fr

src = sys.argv[1]
pk = json.load(open(os.path.join(src, "upper-packing-certificate.json")))
R = Fr(pk["side"])
sq = []
for s in pk["squares"]:
    t = Fr(s["t"])
    u = ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))
    v = (-u[1], u[0])
    sq.append(((Fr(s["x"]), Fr(s["y"])), u, v))


def support(u, v, n):
    return (abs(n[0] * u[0] + n[1] * u[1]) + abs(n[0] * v[0] + n[1] * v[1])) / 2


walls_ok = 0
min_clear = None
clear_list = []
for i, (c, u, v) in enumerate(sq):
    for n, bound in (((1, 0), c[0]), ((-1, 0), R - c[0]), ((0, 1), c[1]), ((0, -1), R - c[1])):
        h = support(u, v, (Fr(n[0]), Fr(n[1])))
        clear = bound - h
        clear_list.append(clear)
        assert clear >= 0, (i, n)
        walls_ok += 1
        min_clear = clear if min_clear is None else min(min_clear, clear)
eps = Fr(323264740583067756265381186720884493986257, 625 * 10**56)
print("walls:", walls_ok, "all nonnegative; minimum clearance", min_clear, "= eps?", min_clear == eps)
print("flush wall clearances equal eps:", sum(1 for c in clear_list if c == eps), "of 68")

pairs_ok = 0
touch = 0
for i in range(17):
    for j in range(i + 1, 17):
        ci, ui, vi = sq[i]
        cj, uj, vj = sq[j]
        d = (cj[0] - ci[0], cj[1] - ci[1])
        sep = None
        for n in (ui, vi, uj, vj):
            gap = abs(n[0] * d[0] + n[1] * d[1]) - support(ui, vi, n) - support(uj, vj, n)
            if gap >= 0:
                sep = gap if sep is None else max(sep, gap)
        assert sep is not None, (i + 1, j + 1)
        pairs_ok += 1
        if sep == 0:
            touch += 1
print("pairs:", pairs_ok, "all separated; touching pairs (gap exactly 0):", touch)
print("RESULT: the rational seed is a packing of 17 unit squares in [0, %s]^2" % R)
