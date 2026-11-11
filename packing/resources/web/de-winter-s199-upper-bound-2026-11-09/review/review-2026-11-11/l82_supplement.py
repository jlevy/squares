"""Added after the controls ran (S1 for #946 was mis-stated: the file has no wall contact).

S1p: #946's side lowered by 1e-319, still 5.6e-320 above the root: decided whole.
Also the largest move of a square that is not a rattler, #946 against T-282.

Usage: python -I l82_supplement.py N172_JSON T282_YAML MOVES_JSON OUT.json
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l82_check as C  # noqa: E402

pk = C.read_author_json(sys.argv[1])
t282 = C.read_witness_yaml(sys.argv[2])
rattlers = set(json.load(open(sys.argv[3]))["rattlers_946"])
S = F(*pk["side"])
r = C.decide(pk, side=S - F(1, 10**319))
q = [[F(*v) for v in s] for s in pk["squares"]]
cl = [C.wall_clearances_a(s, S) for s in pk["squares"]]
moves = []
for k, (a, b) in enumerate(zip(t282["squares"], pk["squares"]), start=1):
    if k in rattlers:
        continue
    xa, ya = F(*a[0]), F(*a[1])
    xb, yb = F(*b[0]), F(*b[1])
    moves.append((float((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5, k))
moves.sort(reverse=True)
out = {
    "S1p_verdict": r["verdict"], "S1p_outside": [r["outside_a"], r["outside_b"]],
    "least_clearance_by_wall": {w: C.sci(min(c[i] for c in cl), 6) for i, w in enumerate(("left", "bottom", "right", "top"))},
    "largest_non_rattler_moves": [[k, f"{m:.4e}"] for m, k in moves[:5]],
    "non_rattlers_moved_beyond_1e-5": sum(1 for m, _ in moves if m > 1e-5),
}
with open(sys.argv[4], "w") as fh:
    json.dump(out, fh, indent=1)
    fh.write("\n")
print(json.dumps(out, indent=1))
