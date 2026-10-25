#!/usr/bin/env python3
"""How far #728's packing lies from the house at 303, under the box's eight symmetries.

A measurement for the review of #728 (lane c-review-728-math). It decides nothing: it
measures. The assignment code (a Hungarian algorithm with its inner loop vectorized in
numpy, and a bottleneck matching by augmenting paths) is this lane's own; --self-test
checks it against brute force on small random instances. The certificate is read with
review_728_check.py's reader; the house witness with PyYAML. No repository code runs.

For each reference packing and each of the eight symmetries of the square box (applied
to the reference in its own box), it reports: whether nearest centres pair the squares
one to one; under the assignment minimizing total squared centre displacement, the
largest, root-mean-square and mean displacement, how many squares move beyond 1e-6,
1e-3, 1e-2, 1e-1 and 0.5, and how far squares turn modulo 90 degrees; and the bottleneck
value (the least largest displacement over all one-to-one pairings). It also counts the
tilted squares of each packing at several thresholds.

Usage:
    python3 -I identity_728.py CERT --house WITNESS.yaml [--contrast NAME=CERT.gz ...] --out FILE.json
    python3 -I identity_728.py --self-test
"""

from __future__ import annotations

import argparse
import gzip
import itertools
import json
import math
import os
import random
import sys
from fractions import Fraction as F

import numpy as np
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_728_check as chk  # noqa: E402


# ------------------------------------------------------------------ assignment (own code)


def hungarian(cost: np.ndarray) -> list[int]:
    """Row i -> column ans[i] minimizing the total cost (shortest augmenting paths, O(n^3))."""
    n = cost.shape[0]
    INF = float("inf")
    u = np.zeros(n + 1)
    v = np.zeros(n + 1)
    p = np.zeros(n + 1, dtype=np.int64)  # p[j]: row matched to column j (1-based), 0 none
    way = np.zeros(n + 1, dtype=np.int64)
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = np.full(n + 1, INF)
        used = np.zeros(n + 1, dtype=bool)
        while True:
            used[j0] = True
            i0 = p[j0]
            free = ~used
            free[0] = False
            cur = np.full(n + 1, INF)
            cur[1:] = cost[i0 - 1] - u[i0] - v[1:]
            better = free & (cur < minv)
            minv[better] = cur[better]
            way[better] = j0
            cand = np.where(free, minv, INF)
            j1 = int(np.argmin(cand))
            delta = cand[j1]
            idx = np.nonzero(used)[0]
            u[p[idx]] += delta
            v[idx] -= delta
            minv[free] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    ans = [0] * n
    for j in range(1, n + 1):
        if p[j]:
            ans[p[j] - 1] = j - 1
    return ans


def perfect_matching_within(d: np.ndarray, r: float) -> bool:
    """Is there a one-to-one pairing using only entries d[i, j] <= r? (Kuhn's augmenting paths.)"""
    n = d.shape[0]
    adj = [np.nonzero(d[i] <= r)[0].tolist() for i in range(n)]
    if any(not a for a in adj):
        return False
    match_col = [-1] * n
    sys.setrecursionlimit(10000)

    def try_row(i: int, seen: list[bool]) -> bool:
        for j in adj[i]:
            if not seen[j]:
                seen[j] = True
                if match_col[j] < 0 or try_row(match_col[j], seen):
                    match_col[j] = i
                    return True
        return False

    for i in range(n):
        if not try_row(i, [False] * n):
            return False
    return True


def bottleneck(d: np.ndarray) -> float:
    vals = np.unique(d)
    lo, hi = 0, len(vals) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if perfect_matching_within(d, vals[mid]):
            hi = mid
        else:
            lo = mid + 1
    return float(vals[lo])


def self_test() -> int:
    rng = random.Random(728)
    bad = 0
    for trial in range(300):
        n = rng.randint(1, 7)
        c = np.array([[rng.random() for _ in range(n)] for _ in range(n)])
        best = min(itertools.permutations(range(n)), key=lambda p: sum(c[i, p[i]] for i in range(n)))
        got = hungarian(c)
        if abs(sum(c[i, got[i]] for i in range(n)) - sum(c[i, best[i]] for i in range(n))) > 1e-12:
            bad += 1
        bn = min(max(c[i, p[i]] for i in range(n)) for p in itertools.permutations(range(n)))
        if bottleneck(c) != bn:
            bad += 1
    print(f"assignment self-test: 300 random instances against brute force, {bad} mismatches")
    return 0 if bad == 0 else 1


# ------------------------------------------------------------------ packings


def from_cert(data: bytes) -> dict:
    cert = chk.read_certificate(data)
    sq = []
    for (xn, xd), (yn, yd), (p, q) in cert["rows"]:
        t = F(p, q)
        c, s = (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)
        sq.append((F(xn, xd), F(yn, yd), c, s))
    return {"side": F(*cert["side"]), "squares": sq}


def from_witness(path: str) -> dict:
    w = yaml.safe_load(open(path))["witness"]
    assert w["representation"] == "center-basis"
    sq = []
    for s in w["squares"]:
        x, y = (F(str(v)) for v in s["center"])
        c, sn = (F(str(v)) for v in s["basis"])
        assert c * c + sn * sn == 1
        sq.append((x, y, c, sn))
    return {"side": F(str(w["side"])), "squares": sq, "id": w["id"]}


def angle_mod90(c: float, s: float) -> float:
    """The square's orientation in degrees, reduced to (-45, 45]."""
    a = math.degrees(math.atan2(s, c)) % 90.0
    return a - 90.0 if a > 45.0 else a


def exact_axis_aligned(c: F, s: F) -> bool:
    return c == 0 or s == 0


SYMS = {
    "identity": lambda x, y, S: (x, y),
    "mirror x": lambda x, y, S: (S - x, y),
    "mirror y": lambda x, y, S: (x, S - y),
    "half turn": lambda x, y, S: (S - x, S - y),
    "transpose": lambda x, y, S: (y, x),
    "quarter turn": lambda x, y, S: (S - y, x),
    "three-quarter turn": lambda x, y, S: (y, S - x),
    "anti-transpose": lambda x, y, S: (S - y, S - x),
}
REFLECTS = {"mirror x", "mirror y", "transpose", "anti-transpose"}


def tilt_counts(pk: dict) -> dict:
    angles = [abs(angle_mod90(float(c), float(s))) for _, _, c, s in pk["squares"]]
    out = {"exactly_tilted": sum(1 for _, _, c, s in pk["squares"] if not exact_axis_aligned(c, s))}
    for thr in (1e-12, 1e-9, 1e-6, 1e-3, 1e-2, 0.1, 1.0):
        out[f"tilted_beyond_{thr:g}_deg"] = sum(1 for a in angles if a > thr)
    return out


def compare(new: dict, ref: dict, name: str) -> dict:
    A = np.array([[float(x), float(y)] for x, y, _, _ in new["squares"]])
    angA = np.array([angle_mod90(float(c), float(s)) for _, _, c, s in new["squares"]])
    S_ref = float(ref["side"])
    scale = float(new["side"] / ref["side"])
    rows = []
    for sym, f in SYMS.items():
        for scaled in (False, True):
            B = []
            angB = []
            for x, y, c, s in ref["squares"]:
                bx, by = f(float(x), float(y), S_ref)
                if scaled:
                    bx, by = bx * scale, by * scale
                B.append((bx, by))
                a = angle_mod90(float(c), float(s))
                angB.append(-a if sym in REFLECTS else a)
            B = np.array(B)
            angB = np.array(angB)
            d = np.sqrt(((A[:, None, :] - B[None, :, :]) ** 2).sum(-1))
            nearest = d.argmin(1)
            one_to_one = len(set(nearest.tolist())) == len(nearest)
            if scaled:
                rows.append({"symmetry": sym, "scaled_to_new_side": True, "nearest_one_to_one": one_to_one,
                             "_d": d})
                continue
            ass = hungarian(d**2)
            disp = np.array([d[i, ass[i]] for i in range(len(ass))])
            turn = np.array([((angA[i] - angB[ass[i]] + 45.0) % 90.0) - 45.0 for i in range(len(ass))])
            rows.append(
                {
                    "symmetry": sym,
                    "scaled_to_new_side": False,
                    "nearest_one_to_one": one_to_one,
                    "max_displacement": float(disp.max()),
                    "rms_displacement": float(math.sqrt((disp**2).mean())),
                    "mean_displacement": float(disp.mean()),
                    "sum_squared_displacement": float((disp**2).sum()),
                    "within_1e-6": int((disp <= 1e-6).sum()),
                    "beyond_1e-3": int((disp > 1e-3).sum()),
                    "beyond_1e-2": int((disp > 1e-2).sum()),
                    "beyond_0.1": int((disp > 0.1).sum()),
                    "beyond_0.5": int((disp > 0.5).sum()),
                    "largest_turn_deg": float(np.abs(turn).max()),
                    "turned_beyond_1deg": int((np.abs(turn) > 1.0).sum()),
                    "turned_beyond_0.1deg": int((np.abs(turn) > 0.1).sum()),
                    "within_1e-3": int((disp <= 1e-3).sum()),
                    "within_0.1": int((disp <= 0.1).sum()),
                    "tilt_reversed": int(
                        sum(
                            1
                            for i in range(len(ass))
                            if abs(angB[ass[i]]) > 1.0 and abs(angA[i] + angB[ass[i]]) < 1.0
                        )
                    ),
                    "tilt_reversed_largest_residual_deg": float(
                        max(
                            [abs(angA[i] + angB[ass[i]]) for i in range(len(ass))
                             if abs(angB[ass[i]]) > 1.0 and abs(angA[i] + angB[ass[i]]) < 1.0] or [0.0]
                        )
                    ),
                    "moved_beyond_0.1_bbox": [
                        [float(A[disp > 0.1][:, 0].min()), float(A[disp > 0.1][:, 1].min())],
                        [float(A[disp > 0.1][:, 0].max()), float(A[disp > 0.1][:, 1].max())],
                    ]
                    if (disp > 0.1).any()
                    else None,
                    "_d": d,
                    "_ass": ass,
                }
            )
    plain = [r for r in rows if not r["scaled_to_new_side"]]
    best = min(plain, key=lambda r: r["sum_squared_displacement"])
    for r in plain:
        r["bottleneck"] = bottleneck(r["_d"]) if r is best or r["nearest_one_to_one"] else None
    for r in rows:
        r.pop("_d", None)
        r.pop("_ass", None)
    return {"reference": name, "reference_side": str(ref["side"]), "best_symmetry": best["symmetry"], "rows": rows}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert", nargs="?")
    ap.add_argument("--house")
    ap.add_argument("--contrast", action="append", default=[])
    ap.add_argument("--out")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    new = from_cert(open(args.cert, "rb").read())
    refs = {"house (T-186, W-known-best-n303)": from_witness(args.house)}
    for item in args.contrast:
        name, path = item.split("=", 1)
        raw = gzip.open(path).read() if path.endswith(".gz") else open(path, "rb").read()
        refs[name] = from_cert(raw)
    out = {"tilts": {"#728": tilt_counts(new), **{k: tilt_counts(v) for k, v in refs.items()}}, "comparisons": []}
    for name, ref in refs.items():
        out["comparisons"].append(compare(new, ref, name))
    open(args.out, "w").write(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out["tilts"], indent=1))
    for comp in out["comparisons"]:
        print(f"against {comp['reference']}: best symmetry {comp['best_symmetry']}")
        for r in comp["rows"]:
            if r["scaled_to_new_side"]:
                continue
            print(
                f"  {r['symmetry']:18} 1:1 {str(r['nearest_one_to_one']):5} max {r['max_displacement']:.6f} rms {r['rms_displacement']:.6f} "
                f"mean {r['mean_displacement']:.6f} bneck {('%.6f' % r['bottleneck']) if r['bottleneck'] is not None else '-':>8} "
                f"<=1e-6 {r['within_1e-6']:3} >1e-3 {r['beyond_1e-3']:3} >0.1 {r['beyond_0.1']:3} >0.5 {r['beyond_0.5']:3} "
                f"turn {r['largest_turn_deg']:.4f} >1deg {r['turned_beyond_1deg']:3} reversed {r['tilt_reversed']:3}"
            )
            if r["symmetry"] == comp["best_symmetry"]:
                print(f"    best: within 1e-3 {r['within_1e-3']}, within 0.1 {r['within_0.1']}, tilt reversed {r['tilt_reversed']} "
                      f"(residual <= {r['tilt_reversed_largest_residual_deg']:.4f} deg), moved beyond 0.1 inside {r['moved_beyond_0.1_bbox']}")
        scaled = {r["symmetry"]: r["nearest_one_to_one"] for r in comp["rows"] if r["scaled_to_new_side"]}
        print("  scaled to the new side, nearest one to one:", scaled)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
