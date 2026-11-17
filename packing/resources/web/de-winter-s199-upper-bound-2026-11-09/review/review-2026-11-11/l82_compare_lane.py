"""After the freeze: hold the import lane L78's receipts (PR #948, ded2c8df8) to this review's.

Usage: python -I l82_compare_lane.py L78_DIR N172_JSON T282_YAML MEASURE_JSON MOVES_JSON OUT.json
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l82_check as C  # noqa: E402

d, n172p, t282p, meap, movp, outp = sys.argv[1:7]
mea = json.load(open(meap))
mov = json.load(open(movp))


def lj(name):
    return json.load(open(os.path.join(d, name)))


c946 = C.read_author_json(n172p)
t282 = C.read_witness_yaml(t282p)
S946 = F(*c946["side"])
out: dict = {}

# contraction receipts
own = lj("de-winter-s172-upper-bound-2026-11-10_measure_contraction-n172-own.json")
k282 = lj("de-winter-s172-upper-bound-2026-11-10_measure_contraction-n172.json")
base = lj("de-winter-s199-upper-bound-2026-11-09_measure_contraction-n172-base.json")
k199 = lj("de-winter-s199-upper-bound-2026-11-09_measure_contraction-n199.json")
out["T282_margin_equal_exactly"] = F(k282["margin"]) == F(mea["K_T282"]["margin_exact"])
out["T284_base_margin_equal_exactly"] = F(base["margin"]) == F(mea["K_T282"]["margin_exact"])
out["T284_whole_margin_zero_both"] = F(k199["margin"]) == 0 == F(mea["K_T284_whole"]["margin_exact"])
out["946_own_side_equal"] = F(own["side"]) == S946
mine = F(mea["K_946_own"]["margin_exact"])
out["946_own_margin_lane"] = C.sci(F(own["margin"]), 10)
out["946_own_margin_mine"] = C.sci(mine, 10)
out["946_own_margin_lane_minus_mine"] = C.sci(F(own["margin"]) - mine, 6)

# recompute lambda* for #946 exactly, from the certificate's own scalars
q = [[F(*v) for v in s] for s in c946["squares"]]


def ratio(i, j):
    xi, yi, ci, si = q[i - 1]
    xj, yj, cj, sj = q[j - 1]
    dd = (xj - xi, yj - yi)
    T = (1 + abs(ci * cj + si * sj) + abs(-ci * sj + si * cj)) / 2
    ws = ((ci, si), (-si, ci), (cj, sj), (-sj, cj))
    return T / max(abs(w[0] * dd[0] + w[1] * dd[1]) for w in ws)


ratios = {(i, j): ratio(i, j) for i in range(1, 173) for j in range(i + 1, 173)}
lam_mine = max(ratios.values())
lam_lane = F(own["lambda_star"])
out["946_lambda_lane_minus_mine"] = C.sci(lam_lane - lam_mine, 6)
out["946_one_minus_lambda_mine"] = C.sci(1 - lam_mine, 10)
out["946_one_minus_lambda_lane"] = C.sci(1 - lam_lane, 10)
out["946_pair_17_20_attains_mine"] = ratios[(17, 20)] == lam_mine
out["946_lane_lambda_attained_by_a_pair"] = [list(k) for k, v in ratios.items() if v == lam_lane]
ex = [(abs(c) + abs(s)) / 2 for _, _, c, s in q]
for name, lam in (("mine", lam_mine), ("lane", lam_lane)):
    xs = [lam * x for x, _, _, _ in q]
    ys = [lam * y for _, y, _, _ in q]
    side = max(max(a + h for a, h in zip(xs, ex)) - min(a - h for a, h in zip(xs, ex)),
               max(a + h for a, h in zip(ys, ex)) - min(a - h for a, h in zip(ys, ex)))
    out[f"946_margin_from_{name}_lambda"] = C.sci(S946 - side, 10)
out["946_lane_contracted_side_minus_mine"] = C.sci(F(own["contracted_side"]) - (S946 - mine), 6)

# the 84 moved squares: do they keep their contacts?
rat = set(mov["rattlers_946"])
ca = [C._corners_a(s) for s in c946["squares"]]
cb = [C._corners_a(s) for s in t282["squares"]]
tight: dict = {}
near: dict = {}
for i in range(172):
    for j in range(i + 1, 172):
        if C.pair_margin_a(c946["squares"][i], c946["squares"][j], ca[i], ca[j]) < F(1, 10**300):
            tight.setdefault(i + 1, set()).add(j + 1)
            tight.setdefault(j + 1, set()).add(i + 1)
        if C.pair_margin_a(t282["squares"][i], t282["squares"][j], cb[i], cb[j]) < F(1, 10**12):
            near.setdefault(i + 1, set()).add(j + 1)
            near.setdefault(j + 1, set()).add(i + 1)
moved = []
for k in range(1, 173):
    xa, ya = F(*t282["squares"][k - 1][0]), F(*t282["squares"][k - 1][1])
    xb, yb = F(*c946["squares"][k - 1][0]), F(*c946["squares"][k - 1][1])
    if (xa - xb) ** 2 + (ya - yb) ** 2 > F(1, 10**18):
        moved.append(k)
nr = [k for k in moved if k not in rat]
out["moved_beyond_1e-9"] = len(moved)
out["moved_rattlers"] = len(moved) - len(nr)
out["moved_non_rattlers"] = len(nr)
out["moved_non_rattlers_with_tight_pairs"] = len([k for k in nr if tight.get(k)])
out["moved_non_rattlers_keeping_every_T282_near_pair"] = len(
    [k for k in nr if near.get(k, set()) <= tight.get(k, set())])
out["moved_non_rattlers_losing_a_near_pair"] = sorted(k for k in nr if not near.get(k, set()) <= tight.get(k, set()))
out["tight_pairs_with_a_moved_square"] = len({(min(a, b), max(a, b)) for a in nr for b in tight.get(a, ())})
with open(outp, "w") as fh:
    json.dump(out, fh, indent=1)
    fh.write("\n")
print(json.dumps(out, indent=1))
