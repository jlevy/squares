"""Which squares the re-solve moved, and whether #946's own contraction stays above the root.

Usage: python -I l82_moves.py T282_YAML N172_JSON ALGEBRA_JSON MEASURE_JSON OUT.json
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l82_check as C  # noqa: E402

t282 = C.read_witness_yaml(sys.argv[1])
c946 = C.read_author_json(sys.argv[2])
alg = json.load(open(sys.argv[3]))
mea = json.load(open(sys.argv[4]))


def degree(pk, th):
    q = pk["squares"]
    S = F(*pk["side"])
    ca = [C._corners_a(s) for s in q]
    deg = [0] * len(q)
    for i in range(len(q)):
        if min(C.wall_clearances_a(q[i], S, ca[i])) < th:
            deg[i] += 1
        for j in range(i + 1, len(q)):
            if C.pair_margin_a(q[i], q[j], ca[i], ca[j]) < th:
                deg[i] += 1
                deg[j] += 1
    return deg


d282 = degree(t282, F(1, 10**12))
d946 = degree(c946, F(1, 10**300))
rows = []
for k, (a, b) in enumerate(zip(t282["squares"], c946["squares"]), start=1):
    xa, ya, ca_, sa = (F(*v) for v in a)
    xb, yb, cb, sb = (F(*v) for v in b)
    mv = float((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5
    # turn: sine of the angle between the edge directions, reduced to a quarter turn
    cr = ca_ * sb - sa * cb
    dt = ca_ * cb + sa * sb
    turn = min(abs(float(cr)), abs(float(dt)))
    rows.append((mv, k, turn, d282[k - 1], d946[k - 1], float(xb - xa), float(yb - ya)))
rows.sort(reverse=True)
root_lo = F(alg["946_root_bracket"][0])
S946 = F(*c946["side"])
own_margin = F(mea["K_946_own"]["margin_exact"])
out = {
    "top_moves": [{"id": k, "move": f"{m:.6e}", "dx": f"{dx:.6e}", "dy": f"{dy:.6e}", "turn": f"{t:.3e}",
                   "T282_near_degree": a, "946_tight_degree": b} for m, k, t, a, b, dx, dy in rows[:12]],
    "moved_beyond": {th: sum(1 for r in rows if r[0] > float(th)) for th in ("1e-12", "1e-9", "1e-6", "1e-5")},
    "rattlers_946": [k for k in range(1, 173) if d946[k - 1] == 0],
    "rattlers_T282": [k for k in range(1, 173) if d282[k - 1] == 0],
    "contracted_946_minus_root": C.sci(S946 - own_margin - root_lo, 6),
    "contracted_946_not_below_root": S946 - own_margin >= root_lo,
}
with open(sys.argv[5], "w") as fh:
    json.dump(out, fh, indent=1)
    fh.write("\n")
print(json.dumps(out, indent=1))
