"""Exact captures at poses: fixed poses at every node, and a seeded search at sampled nodes.

Usage: r144_poses.py --bundle BUNDLE_DIR --search-nodes 0,1,... --out OUT.json
                     [--grid 120] [--fixed-per-node 4] [--refine 6]

Part 1, at every node j = 0..200: the exact capture (methods A and B, which must agree)
at the four corners of the quadrant [L/2, L/2 + E_j]^2 and at seeded poses in it; each is
compared with gamma = 1 and with the source's least leaf bound at that node (the
'lower' of its result.json), which no capture in the domain may undercut if the source's
leaf bounds are sound.
Part 2, at each search node: a binary64 estimate of the capture on a grid over the
quadrant (rectangles counted at full mass where they meet the core, an over-estimate),
then a compass search in binary64 from the best grid points, and the exact capture
(method A) at every end point.
Neither part decides anything: they can find a capture below 1 or below the source's
bound, and report the least exact capture found.
Written for this review; imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import sys
import time
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from r144_bnb import Node  # noqa: E402
from r144_common import angle_data, frac_str, load_candidate  # noqa: E402
from r144_exact import Measure, capture_a, capture_b  # noqa: E402


def source_lower(bundle, j):
    r = json.loads(open(os.path.join(bundle, f"net{j:03d}", "result.json")).read(), parse_float=lambda s: F(s))
    return r["lower"]


def estimate(node: Node, pts):
    """binary64 capture estimates at centres pts (N, 2)."""
    out = np.empty(len(pts))
    for k0 in range(0, len(pts), 2000):
        P = pts[k0 : k0 + 2000]
        xlo, xhi = P[:, 0].min(), P[:, 0].max()
        ylo, yhi = P[:, 1].min(), P[:, 1].max()
        pi, si, ri = node.candidates(xlo, xhi, ylo, yhi)
        Bx = np.stack([P[:, 0], P[:, 0], P[:, 1], P[:, 1]], axis=1)
        out[k0 : k0 + 2000] = node.bounds(Bx, pi, si, ri, centre=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--search-nodes", required=True)
    ap.add_argument("--grid", type=int, default=120)
    ap.add_argument("--fixed-per-node", type=int, default=4)
    ap.add_argument("--refine", type=int, default=6)
    ap.add_argument("--draw", type=int, default=0, help="add this many search nodes, drawn from the rest by a generator seeded from the candidate's SHA-256")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    t0 = time.process_time()
    raw = open(os.path.join(a.bundle, "candidate.json"), "rb").read()
    cand = load_candidate(raw)
    L = cand["L"]
    meas = Measure(cand["primitives"], L)
    seed = int(hashlib.sha256(raw).hexdigest()[:16], 16)
    rng = random.Random(seed)
    part1 = []
    disagree = 0
    below_one = []
    below_source = []
    for j in range(201):
        ang = angle_data(j, cand["step"], L, cand["B"])
        lo, hi = L / 2, L / 2 + ang["E"]
        poses = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
        for _ in range(a.fixed_per_node):
            poses.append((lo + (hi - lo) * F(rng.randrange(10**9), 10**9), lo + (hi - lo) * F(rng.randrange(10**9), 10**9)))
        sl = source_lower(a.bundle, j)
        least = None
        for x, y in poses:
            qa = capture_a(meas, ang, x, y)
            qb = capture_b(meas, ang, x, y)
            if qa != qb:
                disagree += 1
            if qa < 1:
                below_one.append({"j": j, "x": frac_str(x), "y": frac_str(y), "capture": frac_str(qa)})
            if qa < sl:
                below_source.append({"j": j, "x": frac_str(x), "y": frac_str(y), "capture": float(qa), "source_lower": float(sl)})
            if least is None or qa < least[0]:
                least = (qa, x, y)
        part1.append({"j": j, "poses": len(poses), "least": float(least[0]), "least_minus_one": float(least[0] - 1), "at": [float(least[1]), float(least[2])]})
    part2 = []
    named = [int(v) for v in a.search_nodes.split(",")]
    drawn = sorted(random.Random(seed + 1).sample([j for j in range(201) if j not in named], a.draw)) if a.draw else []
    for j in named + drawn:
        node = Node(cand, j, F(1), 1, 1)
        ang = node.ang
        lo, hi = node.lo, node.hi
        g = np.linspace(lo, hi, a.grid)
        X, Y = np.meshgrid(g, g, indexing="ij")
        P = np.stack([X.ravel(), Y.ravel()], axis=1)
        est = estimate(node, P)
        order = np.argsort(est)[: a.refine]
        ends = []
        h0 = (hi - lo) / a.grid
        for k in order:
            p = P[k].copy()
            v = est[k]
            h = h0
            while h > 1e-7:
                trial = np.array([p + [h, 0], p - [h, 0], p + [0, h], p - [0, h]])
                trial = np.clip(trial, lo, hi)
                ev = estimate(node, trial)
                i = int(np.argmin(ev))
                if ev[i] < v:
                    p, v = trial[i], ev[i]
                else:
                    h /= 2
            ends.append(p)
        sl = source_lower(a.bundle, j)
        exact = []
        for p in ends:
            q = capture_a(meas, ang, F(float(p[0])), F(float(p[1])))
            exact.append(q)
            if q < 1:
                below_one.append({"j": j, "x": float(p[0]), "y": float(p[1]), "capture": frac_str(q)})
            if q < sl:
                below_source.append({"j": j, "x": float(p[0]), "y": float(p[1]), "capture": float(q), "source_lower": float(sl)})
        i = min(range(len(exact)), key=lambda k: exact[k])
        part2.append({"j": j, "grid": a.grid, "grid_least_estimate": float(est.min()), "end_points": len(ends), "least_exact": float(exact[i]), "least_exact_minus_one": float(exact[i] - 1), "at": [float(ends[i][0]), float(ends[i][1])], "source_lower_minus_one": float(sl - 1)})
        print(f"search node {j}: least exact {float(exact[i])!r} at {ends[i]}, source lower {float(sl)!r}", flush=True)
    res = {
        "program": "r144_poses.py",
        "seed": seed,
        "search_nodes_named": named,
        "search_nodes_drawn": drawn,
        "part1_nodes": 201,
        "part1_poses": sum(r["poses"] for r in part1),
        "part1_methods_disagree": disagree,
        "part1": part1,
        "part2": part2,
        "below_one": below_one,
        "below_source_lower": below_source,
        "verdict": "NO_COUNTEREXAMPLE_FOUND" if not below_one else "COUNTEREXAMPLE",
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(res["verdict"], f"part 1: {res['part1_poses']} poses, {disagree} disagreements; below source bound: {len(below_source)}; cpu {res['cpu_seconds']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
