"""Z-F: exact probe of zmx2's certified lower bound in its tightest certified leaves (review of #973, L144).

usage: python -I zmx2_leaf_probe.py BOARD OUT_JSON TIGHTFILE [TIGHTFILE ...]
A tight file (zmx2 --dump-tight, --tight 1e-3) lists certified leaves "pass box bound", the bound in units of
target = W * Lc * 2^30 with W = 2*10^12 and Lc = 1 for this board (every piece has length 1/10).  zmx2's main
property is: bound <= target * mu(Q) at every ADMISSIBLE pose Q of the leaf.  For a draw of leaves this program
evaluates mu exactly (k2m5_exact) at every admissible corner of the leaf and at two random admissible interior
poses, and requires mu >= bound / target.  Draw: 3,000 leaves uniformly (random.Random(973), a fresh stream; the
plan's single stream cannot reach this data), plus the 300 leaves of least bound (an addition to the plan).
Also an addition: for a leaf whose u range starts at 0, its four centre corners at u = u1 2^-20 and u1 2^-40.
"""
import json
import os
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from k2m5_exact import load_cover, mass, admissible  # noqa: E402

TARGET = 2 * 10 ** 12 * 2 ** 30


def main():
    board, out = sys.argv[1:3]
    leaves = []
    for f in sys.argv[3:]:
        for ln in open(f):
            t = ln.split()
            if len(t) != 3:
                continue
            if t[0] != "0":
                raise ValueError("pass 1 leaf in a D4 run")
            box = [F(v) for v in t[1].split(",")]
            leaves.append((box, int(t[2]), os.path.basename(f)))
    cv = load_cover(board)
    rng = random.Random(973)
    uni = rng.sample(range(len(leaves)), min(3000, len(leaves)))
    tight = sorted(range(len(leaves)), key=lambda i: leaves[i][1])[:300]
    t0 = time.time()
    res = dict(leaves_total=len(leaves), files=[os.path.basename(f) for f in sys.argv[3:]])
    for tag, idx in (("uniform_3000", uni), ("least_bound_300", tight)):
        evals = 0
        skipped = 0
        worst = None
        viol = []
        cat = {}                     # least mu - bound by category
        for i in idx:
            (x0, x1, y0, y1, u0, u1), bound, src = leaves[i]
            lb = F(bound, TARGET)
            pts = [(x, y, u) for x in (x0, x1) for y in (y0, y1) for u in (u0, u1)]
            if u0 == 0:
                # an addition stated before the run: the first-order regime of Lemma U, as u -> 0+
                pts += [(x, y, u1 / 2 ** e) for x in (x0, x1) for y in (y0, y1) for e in (20, 40)]
            for _ in range(2):
                for _try in range(20):
                    p = tuple(a + (b - a) * F(rng.randrange(10 ** 6 + 1), 10 ** 6) for a, b in ((x0, x1), (y0, y1), (u0, u1)))
                    if admissible(F(11), *p):
                        pts.append(p)
                        break
            for k_, p in enumerate(pts):
                if not admissible(F(11), *p):
                    skipped += 1
                    continue
                m = mass(cv, *p)
                evals += 1
                gap = m - lb
                kind = ("bound_above_1" if lb > 1 else "bound_exactly_1" if lb == 1 else "bound_below_1")
                kind += "|small_u" if (u0 == 0 and k_ >= 8 and k_ < 16) else "|corner_or_interior"
                if kind not in cat or gap < cat[kind][0]:
                    cat[kind] = (gap, [str(v) for v in p], float(m), float(lb))
                if gap < 0:
                    viol.append((src, [str(v) for v in p], float(m), float(lb)))
                if worst is None or gap < worst[0]:
                    worst = (gap, [str(v) for v in p], float(m), float(lb), src)
        res[tag] = dict(leaves=len(idx), evaluations=evals, non_admissible_points_skipped=skipped,
                        violations=len(viol), first_violations=viol[:5],
                        least_mu_minus_bound=float(worst[0]), at=worst[1], mu=worst[2], bound=worst[3], file=worst[4],
                        least_bound_in_draw=float(min(F(leaves[i][1], TARGET) for i in idx)),
                        by_category={k: dict(least_gap=float(v[0]), at=v[1], mu=v[2], bound=v[3]) for k, v in sorted(cat.items())})
    res["secs"] = round(time.time() - t0, 1)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
