"""Exact evaluation of the pre-stated pose samples S1-S5 and the M-1 confirmation (review of #973, L144).

usage: python -I k2m5_samples.py BOARD CTL_RISE M1_COVER SAMPLES_JSON OUT_JSON
Every mass is exact (k2m5_exact.mass).  A sample fails if any pose has mass below 1.
"""
import json
import os
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2m5_exact import load_cover, mass, admissible  # noqa: E402


def run(cv, poses, tag):
    t = time.time()
    best = None
    below = 0
    for k, (cx, cy, u) in enumerate(poses):
        m = mass(cv, F(cx), F(cy), F(u))
        if m < 1:
            below += 1
        if best is None or m < best[0]:
            best = (m, k, (str(cx), str(cy), str(u)))
    return dict(sample=tag, poses=len(poses), below_1=below, min_mass_minus_1=float(best[0] - 1),
                min_exact=str(best[0]), argmin=best[2], secs=round(time.time() - t, 1))


def main():
    board, ctl, m1, sp, out = sys.argv[1:6]
    cv = load_cover(board)
    smp = json.load(open(sp))
    res = {}
    s1 = [tuple(p) for p in smp["S1"]]
    res["S1_admissible_all"] = all(admissible(F(11), F(a), F(b), F(c)) for a, b, c in s1)
    res["S1"] = run(cv, s1, "S1 uniform admissible")
    # S2: tight-tile neighbourhoods; also the least (mass - 1)/h per h level
    s2 = smp["S2"]
    res["S2"] = run(cv, [tuple(p[:3]) for p in s2], "S2 tight-tile base lines")
    per_h = {}
    for p in s2:
        cx, cy, u, d0, sg, yb, pp, qq, h = p
        m = mass(cv, F(cx), F(cy), F(u))
        r = (m - 1) / F(h)
        cur = per_h.get(h)
        if cur is None or r < cur[0]:
            per_h[h] = (r, (d0, sg, yb, pp, qq))
    res["S2_min_mass_minus_1_over_h"] = {h: dict(value=float(v[0]), at=v[1]) for h, v in per_h.items()}
    res["S3"] = run(cv, [tuple(p) for p in smp["S3"]], "S3 root-9632 window")
    s4pts = [tuple(pt) for _, _, pts in smp["S4"] for pt in pts]
    res["S4"] = run(cv, s4pts, f"S4 leftover-box centres and u>0 corners ({len(smp['S4'])} boxes)")
    # S5: the source's 'same limit, smaller growth' pose
    ct = load_cover(ctl)
    h = F(1, 10 ** 6)
    pose = (F(3, 2) + h, F(9, 2) + h, h)
    res["S5"] = dict(pose=[str(x) for x in pose], mu11_minus_1=float(mass(cv, *pose) - 1),
                     ctl_rise_minus_1=float(mass(ct, *pose) - 1))
    # M-1: poses of root 12096 (centre [5.4, 5.5]^2, u in [0, 1/8]) on the board and on the M-1 cover
    cm1 = load_cover(m1)
    rg = random.Random(973)
    poses = [(F(54, 10) + F(rg.randrange(10 ** 6), 10 ** 7), F(54, 10) + F(rg.randrange(10 ** 6), 10 ** 7),
              F(rg.randrange(10 ** 6), 8 * 10 ** 6)) for _ in range(50)]
    res["M1_confirm"] = dict(poses=50, board_masses={str(x) for x in (mass(cv, *p) for p in poses)},
                             m1_masses={str(x) for x in (mass(cm1, *p) for p in poses)})
    json.dump(res, open(out, "w"), indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
