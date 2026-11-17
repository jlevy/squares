"""Clean-room closure check for root 9632 (paper Theorem 10, part 3), with control M-5 (review of #973, L144).

usage: python -I closure_9632.py ZMX2_DUMP QX2_OUT QX2_UNC OUT_JSON [M-5]
The root is closed if
  (a) every box zmx2 leaves (UNCERT lines of the dump, all printed) lies in the qx2 root box that contains it:
      qx2_zm.py's D4 roots are the 1/10 cells times u bins of width 1/16, so the root of the window is
      [43/10, 44/10]^2 x [0, 1/16], which this program checks contains every zmx2 leftover box;
  (b) qx2_zm.py ran exactly one root, that one, to completion (its log says 1 root and gives a census);
  (c) no box qx2_zm.py leaves uncertified meets (closed boxes) any box zmx2 leaves.
With M-5, the first qx2 uncertified box is moved onto the first zmx2 box (its x, y and u ranges replaced by the
zmx2 box's), which must make (c) fail.
"""
import json
import re
import sys
from fractions import Fraction as F

dump, qout, qunc, out = sys.argv[1:5]
m5 = len(sys.argv) > 5 and sys.argv[5] == "M-5"
Z = [[F(t) for t in m.group(1).split(",")] for m in (re.match(r"^UNCERT \d+ pass \d+ box (\S+) ", ln) for ln in open(dump)) if m]
Q = [[F(t) for t in ln.split()] for ln in open(qunc) if ln.strip()]
if m5:
    Q[0] = list(Z[0])
root = (F(43, 10), F(44, 10), F(43, 10), F(44, 10), F(0), F(1, 16))
inside = all(root[0] <= z[0] and z[1] <= root[1] and root[2] <= z[2] and z[3] <= root[3] and root[4] <= z[4] and z[5] <= root[5] for z in Z)
txt = open(qout).read()
one_root = bool(re.search(r": 1 roots \(PARTIAL\)", txt))
finished = bool(re.search(r"^done in \d+s: boxes \d+", txt, re.M))
n_unc = int(re.search(r"UNCERT (\d+)\s*$", txt.split("leaves:")[1].split("\n")[0]).group(1))


def meet(a, b):
    return all(max(a[2 * i], b[2 * i]) <= min(a[2 * i + 1], b[2 * i + 1]) for i in range(3))


Zs = sorted(Z)
hits = 0
for q in Q:
    for z in Zs:
        if z[0] > q[1]:
            break
        if meet(q, z):
            hits += 1
gap = None
for q in Q:
    for z in Z:
        d = max(max(q[2 * i], z[2 * i]) - min(q[2 * i + 1], z[2 * i + 1]) for i in range(3))
        gap = d if gap is None or d < gap else gap
res = dict(zmx2_boxes=len(Z), zmx2_boxes_in_qx2_root=inside, qx2_one_root=one_root, qx2_finished=finished,
           qx2_uncert=len(Q), qx2_log_uncert=n_unc, meeting_pairs=hits,
           least_separation=str(gap) if not m5 else None, least_separation_float=float(gap) if gap is not None else None,
           closed=inside and one_root and finished and n_unc == len(Q) and hits == 0, mutated="M-5" if m5 else None)
json.dump(res, open(out, "w"), indent=1)
print(json.dumps(res))
