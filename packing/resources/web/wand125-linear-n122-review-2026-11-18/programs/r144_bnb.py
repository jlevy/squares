"""Decide sampled net nodes completely, by branch and bound on boxes of centres.

Usage: r144_bnb.py --bundle BUNDLE_DIR --angles 37,108 [--factor P/Q] [--grid 32]
                   [--max-nodes N] --out OUT.json

At node j the core Q(c) is the closed square of side B = 2b centred at c with sides along
u = (cos, sin), v = (-sin, cos). In the core's frame, U = u.p and V = v.p, Q(c) is the
axis-parallel square |U - u.c| <= b, |V - v.c| <= b. For a box of centres
[x0, x1] x [y0, y1] (cos, sin >= 0), the intersection of all Q(c) is the trimmed core
  T = [cos x1 + sin y1 - b, cos x0 + sin y0 + b] x [-sin x0 + cos y1 - b, -sin x1 + cos y0 + b]
in (U, V), and mu(T) <= mu(Q(c)) for every c in the box, since mu >= 0. A box is
discharged when a rigorous lower bound on mu(T) is at least gamma = 1; otherwise it is
halved across its longer side. The quadrant [L/2, L/2 + E_j]^2 suffices: the rotation by
pi/2 about the centre of K preserves mu and the angle class, and maps the quadrant onto
the other three.

Rigour. Image coordinates (U, V) are computed exactly and rounded to nearest; the box's
T is computed in binary64 and shrunk by delta = 1e-13 on every side, which exceeds the
absolute error of every quantity compared (below 2e-14 for numbers below 16). A point
counts only if it is inside the shrunk T by the binary64 comparison; a segment counts
the parameter interval that Liang-Barsky computes against the shrunk T, which lies
inside the exact interval against T because each bound's error is below delta/|d|. A
rectangle counts its full mass only when its four corners are inside the shrunk T, and
otherwise, if it may meet T, its exact share by rational clipping against the exact T.
Masses are rounded down. The sum of k nonnegative terms is divided by (1 + 2e-12)
(k u < 1e-12 is asserted), so a discharged box truly has mu(T) >= 1.

A box that is not discharged is also tested at its centre: if a binary64 estimate of the
capture there (rectangles at full mass) is below 1 - 1e-9, the capture is computed
exactly at that centre, and a value below 1 refutes the node (AXIS witnesses are exact).

Verdicts per node: NODE_DECIDED (every box discharged), NODE_REFUTED (an exact witness
below 1), NODE_UNDECIDED (a box below 1e-10 undischarged, or the node budget spent).
Written for this review; imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from r144_common import angle_data, expand_images, frac_str, load_candidate, rat, round_down, round_up  # noqa: E402
from r144_exact import Measure, _clip_halfplane, _shoelace, capture_a  # noqa: E402

DELTA = 1e-13
SUMFAC = 1.0 + 2e-12
MIN_SIDE = 1e-10


def prepare(cand: dict, j: int, factor: F):
    L, B = cand["L"], cand["B"]
    ang = angle_data(j, cand["step"], L, B)
    c, s, b = ang["cos"], ang["sin"], ang["b"]
    if not (c >= 0 and s >= 0):
        raise SystemExit("node outside [0, pi/2]")
    imgs = expand_images(cand["primitives"], L, factor)
    P, S, R = [], [], []
    for kind, g, m, _i, _g in imgs:
        mf = round_down(m)
        if kind == "point":
            x, y = g
            P.append((float(c * x + s * y), float(-s * x + c * y), mf, float(x), float(y)))
        elif kind == "segment":
            x0, y0, x1, y1 = g
            ua, va = c * x0 + s * y0, -s * x0 + c * y0
            ub, vb = c * x1 + s * y1, -s * x1 + c * y1
            S.append((float(ua), float(va), float(ub - ua), float(vb - va), mf, float(min(x0, x1)), float(max(x0, x1)), float(min(y0, y1)), float(max(y0, y1)), (ub - ua) == 0, (vb - va) == 0))
        else:
            x0, y0, x1, y1 = g
            corners = [(c * x + s * y, -s * x + c * y) for (x, y) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]
            R.append({"poly": corners, "area": (x1 - x0) * (y1 - y0), "m": m, "mf": mf, "bbox": (float(x0), float(x1), float(y0), float(y1)), "cu": [float(p[0]) for p in corners], "cv": [float(p[1]) for p in corners]})
    arr = lambda rows, k: np.array([r[k] for r in rows], dtype=np.float64)  # noqa: E731
    pts = {k: arr(P, i) for i, k in enumerate(("u", "v", "m", "x", "y"))}
    segs = {k: arr(S, i) for i, k in enumerate(("au", "av", "du", "dv", "m", "xlo", "xhi", "ylo", "yhi"))}
    segs["du0"] = np.array([r[9] for r in S], dtype=bool)
    segs["dv0"] = np.array([r[10] for r in S], dtype=bool)
    return ang, pts, segs, R, imgs


class Node:
    def __init__(self, cand, j, factor, grid, max_nodes):
        self.cand = cand
        self.j = j
        self.factor = factor
        self.ang, self.pts, self.segs, self.rects, _ = prepare(cand, j, factor)
        self.cf, self.sf, self.bf = float(self.ang["cos"]), float(self.ang["sin"]), float(self.ang["b"])
        self.Rext = float(self.ang["b"] * (self.ang["cos"] + self.ang["sin"])) + 1e-9
        L = cand["L"]
        self.lo = round_down(L / 2)
        self.hi = round_up(L / 2 + self.ang["E"])
        self.grid = grid
        self.max_nodes = max_nodes
        self.meas = Measure(cand["primitives"], L, factor)
        self.stats = {"nodes": 0, "discharged": 0, "max_depth": 0, "rect_exact": 0, "centre_checks_exact": 0, "least_margin": math.inf, "least_margin_box": None, "max_terms": 0}
        self.witness = None
        self.undischarged = []

    def candidates(self, x0, x1, y0, y1):
        r = self.Rext
        p, s = self.pts, self.segs
        pm = (p["x"] >= x0 - r) & (p["x"] <= x1 + r) & (p["y"] >= y0 - r) & (p["y"] <= y1 + r)
        sm = (s["xhi"] >= x0 - r) & (s["xlo"] <= x1 + r) & (s["yhi"] >= y0 - r) & (s["ylo"] <= y1 + r)
        rm = [k for k, R in enumerate(self.rects) if R["bbox"][1] >= x0 - r and R["bbox"][0] <= x1 + r and R["bbox"][3] >= y0 - r and R["bbox"][2] <= y1 + r]
        return np.nonzero(pm)[0], np.nonzero(sm)[0], rm

    def bounds(self, B, pi, si, ri, centre=False):
        """B: (N, 4) boxes x0, x1, y0, y1. Returns rigorous lower bounds of mu(T), or the
        binary64 estimate at the centres (with rectangles at full mass) when centre."""
        cf, sf, bf = self.cf, self.sf, self.bf
        x0, x1, y0, y1 = B[:, 0:1], B[:, 1:2], B[:, 2:3], B[:, 3:4]
        if centre:
            cx = 0.5 * (x0 + x1)
            cy = 0.5 * (y0 + y1)
            uc = cf * cx + sf * cy
            vc = -sf * cx + cf * cy
            U0, U1, V0, V1 = uc - bf, uc + bf, vc - bf, vc + bf
        else:
            U0 = cf * x1 + sf * y1 - bf + DELTA
            U1 = cf * x0 + sf * y0 + bf - DELTA
            V0 = -sf * x0 + cf * y1 - bf + DELTA
            V1 = -sf * x1 + cf * y0 + bf - DELTA
        total = np.zeros(B.shape[0])
        nterms = np.zeros(B.shape[0])
        if len(pi):
            pu = self.pts["u"][pi][None, :]
            pv = self.pts["v"][pi][None, :]
            ins = (pu >= U0) & (pu <= U1) & (pv >= V0) & (pv <= V1)
            total += ins.astype(np.float64) @ self.pts["m"][pi]
            nterms += ins.sum(axis=1)
        if len(si):
            s = self.segs
            au, av, du, dv = s["au"][si][None, :], s["av"][si][None, :], s["du"][si][None, :], s["dv"][si][None, :]
            du0, dv0 = s["du0"][si][None, :], s["dv0"][si][None, :]
            with np.errstate(divide="ignore", invalid="ignore"):
                a1 = (U0 - au) / du
                a2 = (U1 - au) / du
                b1 = (V0 - av) / dv
                b2 = (V1 - av) / dv
            # bounds chosen by the sign of the direction, so that an inverted slab
            # (U0 > U1, a box too wide for any trimmed core) stays empty
            ulo = np.where(du0, np.where((au >= U0) & (au <= U1), -np.inf, np.inf), np.where(du > 0, a1, a2))
            uhi = np.where(du0, np.where((au >= U0) & (au <= U1), np.inf, -np.inf), np.where(du > 0, a2, a1))
            vlo = np.where(dv0, np.where((av >= V0) & (av <= V1), -np.inf, np.inf), np.where(dv > 0, b1, b2))
            vhi = np.where(dv0, np.where((av >= V0) & (av <= V1), np.inf, -np.inf), np.where(dv > 0, b2, b1))
            s0 = np.maximum(np.maximum(ulo, vlo), 0.0)
            s1 = np.minimum(np.minimum(uhi, vhi), 1.0)
            fr = np.maximum(s1 - s0, 0.0)
            total += fr @ s["m"][si]
            nterms += (fr > 0).sum(axis=1)
        for k in ri:
            R = self.rects[k]
            cu = np.array(R["cu"])[None, :]
            cv = np.array(R["cv"])[None, :]
            if centre:
                meets = (cu.max() >= U0[:, 0] - 1e-9) & (cu.min() <= U1[:, 0] + 1e-9) & (cv.max() >= V0[:, 0] - 1e-9) & (cv.min() <= V1[:, 0] + 1e-9)
                total += np.where(meets, R["mf"], 0.0)
                continue
            inside = ((cu >= U0) & (cu <= U1) & (cv >= V0) & (cv <= V1)).all(axis=1)
            total += np.where(inside, R["mf"], 0.0)
            nterms += inside
            maybe = (~inside) & (cu.max() >= U0[:, 0] - 1e-9) & (cu.min() <= U1[:, 0] + 1e-9) & (cv.max() >= V0[:, 0] - 1e-9) & (cv.min() <= V1[:, 0] + 1e-9)
            for n in np.nonzero(maybe)[0]:
                self.stats["rect_exact"] += 1
                q = self.rect_exact(R, B[n])
                if q > 0:
                    total[n] += round_down(q)
                    nterms[n] += 1
        if not centre:
            self.stats["max_terms"] = max(self.stats["max_terms"], int(nterms.max()) if len(nterms) else 0)
        return total

    def rect_exact(self, R, box) -> F:
        c, s, b = self.ang["cos"], self.ang["sin"], self.ang["b"]
        x0, x1, y0, y1 = (F(float(v)) for v in box)
        u0 = c * x1 + s * y1 - b
        u1 = c * x0 + s * y0 + b
        v0 = -s * x0 + c * y1 - b
        v1 = -s * x1 + c * y0 + b
        if u0 > u1 or v0 > v1:
            return F(0)
        poly = list(R["poly"])
        for a, bb, cc in ((1, 0, u1), (-1, 0, -u0), (0, 1, v1), (0, -1, -v0)):
            poly = _clip_halfplane(poly, F(a), F(bb), cc)
            if not poly:
                return F(0)
        if len(poly) < 3:
            return F(0)
        return R["m"] * _shoelace(poly) / R["area"]

    def run_cell(self, x0, x1, y0, y1, depth0):
        pi, si, ri = self.candidates(x0, x1, y0, y1)
        boxes = np.array([[x0, x1, y0, y1]])
        depth = depth0
        CH = max(1, int(1_500_000 // max(1, len(pi) + len(si))))
        while len(boxes):
            if self.stats["nodes"] >= self.max_nodes:
                self.undischarged.append({"reason": "node budget"})
                return False
            nxt = []
            for k0 in range(0, len(boxes), CH):
                Bc = boxes[k0 : k0 + CH]
                self.stats["nodes"] += len(Bc)
                lb = self.bounds(Bc, pi, si, ri)
                ok = lb >= SUMFAC
                if ok.any():
                    marg = lb[ok] / SUMFAC - 1.0
                    i = int(np.argmin(marg))
                    if marg[i] < self.stats["least_margin"]:
                        self.stats["least_margin"] = float(marg[i])
                        self.stats["least_margin_box"] = [float(v) for v in Bc[ok][i]]
                self.stats["discharged"] += int(ok.sum())
                bad = Bc[~ok]
                if not len(bad):
                    continue
                est = self.bounds(bad, pi, si, ri, centre=True)
                for n in np.nonzero(est < 1.0 - 1e-9)[0]:
                    self.stats["centre_checks_exact"] += 1
                    bx = bad[n]
                    cx = (F(float(bx[0])) + F(float(bx[1]))) / 2
                    cy = (F(float(bx[2])) + F(float(bx[3]))) / 2
                    q = capture_a(self.meas, self.ang, cx, cy)
                    if q < 1:
                        self.witness = {"x": frac_str(cx), "y": frac_str(cy), "capture": frac_str(q), "capture_float": float(q)}
                        return False
                w = bad[:, 1] - bad[:, 0]
                h = bad[:, 3] - bad[:, 2]
                tiny = np.maximum(w, h) < MIN_SIDE
                if tiny.any():
                    for bx in bad[tiny][:5]:
                        self.undischarged.append({"box": [float(v) for v in bx], "reason": "below minimum side"})
                    return False
                splitx = w >= h
                mx = 0.5 * (bad[:, 0] + bad[:, 1])
                my = 0.5 * (bad[:, 2] + bad[:, 3])
                A = bad.copy()
                Bb = bad.copy()
                A[splitx, 1] = mx[splitx]
                Bb[splitx, 0] = mx[splitx]
                A[~splitx, 3] = my[~splitx]
                Bb[~splitx, 2] = my[~splitx]
                nxt.append(A)
                nxt.append(Bb)
            boxes = np.concatenate(nxt) if nxt else np.zeros((0, 4))
            if len(boxes):
                depth += 1
                self.stats["max_depth"] = max(self.stats["max_depth"], depth)
        return True

    def run(self):
        t0 = time.process_time()
        G = self.grid
        xs = np.linspace(self.lo, self.hi, G + 1)
        xs[0], xs[-1] = self.lo, self.hi
        ok = True
        for i in range(G):
            for k in range(G):
                if not self.run_cell(xs[i], xs[i + 1], xs[k], xs[k + 1], 2 * int(math.log2(G))):
                    ok = False
                    break
            if not ok:
                break
        assert self.stats["max_terms"] * 2**-53 < 1e-12
        if self.witness:
            verdict = "NODE_REFUTED"
        elif ok:
            verdict = "NODE_DECIDED"
        else:
            verdict = "NODE_UNDECIDED"
        st = dict(self.stats)
        st["least_margin"] = None if st["least_margin"] == math.inf else st["least_margin"]
        return {
            "j": self.j,
            "t": frac_str(self.ang["t"]),
            "verdict": verdict,
            "quadrant": [self.lo, self.hi],
            "grid": G,
            "stats": st,
            "witness": self.witness,
            "undischarged": self.undischarged[:5],
            "cpu_seconds": round(time.process_time() - t0, 2),
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--angles", required=True)
    ap.add_argument("--factor", default="1")
    ap.add_argument("--grid", type=int, default=32)
    ap.add_argument("--max-nodes", type=int, default=20_000_000)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cand = load_candidate(open(os.path.join(a.bundle, "candidate.json"), "rb").read())
    factor = rat(a.factor)
    out = {"program": "r144_bnb.py", "factor": frac_str(factor), "delta": DELTA, "sum_factor": SUMFAC, "nodes": []}
    for j in [int(x) for x in a.angles.split(",")]:
        if j == 0:
            print("node 0 is decided by r144_axis.py; skipped")
            continue
        r = Node(cand, j, factor, a.grid, a.max_nodes).run()
        out["nodes"].append(r)
        print(r["verdict"], f"node {j}", f"boxes {r['stats']['nodes']}", f"least margin {r['stats']['least_margin']}", f"witness {r['witness']}", f"cpu {r['cpu_seconds']} s", flush=True)
        with open(a.out, "w") as f:
            json.dump(out, f, indent=1)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
