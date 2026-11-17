"""M-3: search for a first-order-only mutant of the Tight-Tile kind (review of #973, L144).  Exact arithmetic.

usage: python -I m3_search.py BOARD OUT_JSON OUT_COVER
Tiles tried in the plan's order: (d0, y_b, sign) = (5/2, 7/2, +1), (3/2, 5/2, -1), (5/2, 9/2, -1).  On the C_u face
grid (p, q) in {-4, -15/4, ..., 4}^2 at h1 = 10^-6 (pose centre (d0 + h p, y_b + h q), u = sign h), every segment
captured at h1 but whose capture at h2 = 10^-9 is at most 2 (h2/h1) times its capture at h1 has zero limit
contribution there (it scales like h).  Removing it lowers the mass by its capture at h1.  The first tile where some
(point, segment) gives mass below 1 is used, with the most negative such value; the segment is deleted from the
board to make the mutant, and the deficit is re-computed exactly on the mutant file.
"""
import json
import os
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2m5_exact import load_cover, mass  # noqa: E402

board, out, out_cover = sys.argv[1:4]
cv = load_cover(board)
h1, h2 = F(1, 10 ** 6), F(1, 10 ** 9)
tiles = [(F(5, 2), F(7, 2), 1), (F(3, 2), F(5, 2), -1), (F(5, 2), F(9, 2), -1)]
grid = [F(k, 4) for k in range(-16, 17)]
res = dict(tried=[])
choice = None
for d0, yb, sg in tiles:
    best = None
    tight_pts = 0
    for p in grid:
        for q in grid:
            pose1 = (d0 + h1 * p, yb + h1 * q, sg * h1)
            pose2 = (d0 + h2 * p, yb + h2 * q, sg * h2)
            m1, parts1, a1, _ = mass(cv, *pose1, detail=True)
            m2, parts2, a2, _ = mass(cv, *pose2, detail=True)
            c2 = {pp[:5]: pp[5] for pp in parts2}
            if (m2 - 1) < F(1, 10 ** 7):
                tight_pts += 1
            for pp in parts1:
                key, c1 = pp[:5], pp[5]
                if c2.get(key, F(0)) <= 2 * (h2 / h1) * c1:
                    newm = m1 - c1
                    if newm < 1 and (best is None or newm < best[0]):
                        best = (newm, p, q, key, c1, m1)
    res["tried"].append(dict(tile=[str(d0), str(yb), sg], face_points=len(grid) ** 2, limit_tight_points=tight_pts,
                             found=best is not None))
    if best is not None:
        choice = (d0, yb, sg, best)
        break
if choice is None:
    res["result"] = "no first-order-only mutant found at the three tiles"
else:
    d0, yb, sg, (newm, p, q, key, c1, m1) = choice
    orient, line, s0, s1, w = key
    seg = (s0, line, s1, line) if orient == "h" else (line, s0, line, s1)
    L = open(board).read().split("\n")
    i = 0
    while not L[i].split() or L[i].startswith("#") or L[i].startswith("mixed"):
        i += 1
    n = int(L[i + 4])
    drop = None
    for j in range(n):
        t = list(map(int, L[i + 5 + j].split()))
        if t[4] == w and ((t[0], t[1], t[2], t[3]) == seg or (t[2], t[3], t[0], t[1]) == seg):
            drop = i + 5 + j
            break
    newL = L[:i] + [f"# CONTROL M-3 (L144 review): segment {seg} (tenths) weight {w}/{L[i + 2]} deleted"] + L[i:i + 4] + [str(n - 1)]
    newL += [L[k] for k in range(i + 5, i + 5 + n) if k != drop] + L[i + 5 + n:]
    open(out_cover, "w").write("\n".join(newL))
    cm = load_cover(out_cover)
    pose1 = (d0 + h1 * p, yb + h1 * q, sg * h1)
    res["result"] = dict(tile=[str(d0), str(yb), sg], face_point=[str(p), str(q)], h=str(h1),
                         segment_tenths=seg, weight=f"{w}/{L[i + 2]}", capture_at_h=float(c1),
                         mu11_minus_1=float(mass(cv, *pose1) - 1), mutant_minus_1=float(mass(cm, *pose1) - 1),
                         mutant_mass_below_1=mass(cm, *pose1) < 1,
                         mu11_limit_minus_1_at_h2=float(mass(cv, d0 + h2 * p, yb + h2 * q, sg * h2) - 1))
json.dump(res, open(out, "w"), indent=1, default=str)
print(json.dumps(res, indent=1, default=str))
