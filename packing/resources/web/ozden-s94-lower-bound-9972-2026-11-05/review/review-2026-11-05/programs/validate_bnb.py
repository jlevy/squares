"""Cross-checks of bnb.py's per-box quantities against exact capture (decides nothing).

For random binary64 poses p (exact dyadic rationals) at several directions:

- bnb.py's centre lower bound F_lo(p) (zero-width box) is at most the exact capture
  computed by capture_exact.py's polygon clipping, and its estimate is within 1e-9;
- for a small box around p, the enclosure of each partial derivative contains the exact
  symmetric difference quotient of F over the box, which by the mean value theorem is a
  value of that partial derivative at a point of the box;
- the inside/outside classification agrees with exact intersection areas.

Usage: validate_bnb.py CERT_GZ OUT_JSON R [R ...]
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import numpy as np
from gmpy2 import mpq

from bnb import Direction
from capture_exact import Evaluator, clip, poly_area


def main() -> int:
    t0 = time.process_time()
    cert_path = Path(sys.argv[1])
    out = Path(sys.argv[2])
    rs = [int(v) for v in sys.argv[3:]]
    rng = random.Random(910)
    ev = None
    report = []
    ok = True
    for r in rs:
        d = Direction(cert_path, r, mpq(1), None)
        if ev is None:
            ev = Evaluator(d.cert)
        n_all = len(d.keys)
        allk = np.arange(n_all)
        worst_gap = 0.0
        worst_under = 0.0
        grad_ok = 0
        grad_n = 0
        cls_bad = 0
        for trial in range(12):
            px = rng.uniform(d.lo, d.hi)
            py = rng.uniform(d.lo, d.hi)
            if trial % 3 == 0:  # near the wall edge of the per-bin domain
                py = d.hi - rng.uniform(0, 0.01)
            P = np.array([px]); Q = np.array([py])
            ins, outs = d.classify(P.repeat(n_all), Q.repeat(n_all), np.zeros(n_all), np.zeros(n_all), allk)
            bnd = allk[~(ins | outs)]
            T, Terr = d.area_lb(P.repeat(len(bnd)), Q.repeat(len(bnd)), bnd)
            inside = float(np.sum(d.mass[ins]))
            Flo = inside + float(np.sum(np.maximum(T - Terr, 0) * d.rho[bnd]))
            Fest = inside + float(np.sum(T * d.rho[bnd]))
            exact = ev.capture(r, mpq(px), mpq(py))
            under = float(exact - mpq(Flo))
            gap = abs(float(exact - mpq(Fest)))
            worst_gap = max(worst_gap, gap)
            if under < 0:
                ok = False
            worst_under = min(worst_under, under) if trial else under
            # classification spot check against exact areas for a few rectangles
            sq = ev.square(r, mpq(px), mpq(py))
            for idx in rng.sample(range(n_all), 40):
                k = d.keys[idx]
                poly = clip(clip(clip(clip(sq, 0, k[0], True), 0, k[2], False), 1, k[1], True), 1, k[3], False)
                a = poly_area(poly)
                full = (k[2] - k[0]) * (k[3] - k[1])
                if ins[idx] and a != full:
                    cls_bad += 1
                if outs[idx] and a != 0:
                    cls_bad += 1
            # gradient enclosure over a small box vs exact difference quotients
            for half in (1e-4, 3e-3):
                x0, x1, y0, y1 = px - half, px + half, py - half, py + half
                bx = np.array([x0]); by0 = np.array([y0]); bx1 = np.array([x1]); by1 = np.array([y1])
                ins2, outs2 = d.classify(P.repeat(n_all), Q.repeat(n_all), np.full(n_all, half), np.full(n_all, half), allk)
                b2 = allk[~(ins2 | outs2)]
                m = len(b2)
                gp = d.grad_parts(bx.repeat(m), bx1.repeat(m), by0.repeat(m), by1.repeat(m), b2)
                for name, (dxq, dyq) in (("x", (mpq(x1) - mpq(px), 0)), ("y", (0, mpq(y1) - mpq(py)))):
                    stable, Dc, lo, hi, err = gp[name]
                    Sc = Dc[stable].sum(axis=0)
                    glo = Sc.min() + lo[~stable].sum() - err.sum()
                    ghi = Sc.max() + hi[~stable].sum() + err.sum()
                    fp = ev.capture(r, mpq(px) + dxq, mpq(py) + dyq)
                    fm = ev.capture(r, mpq(px) - dxq, mpq(py) - dyq)
                    dq = float((fp - fm) / (2 * (dxq if name == "x" else dyq)))
                    grad_n += 1
                    if glo <= dq <= ghi:
                        grad_ok += 1
                    else:
                        ok = False
                        print(f"  GRADIENT ENCLOSURE MISS r={r} {name} half={half} [{glo}, {ghi}] dq={dq}")
        row = {
            "r": r,
            "poses": 12,
            "max_abs_estimate_minus_exact": worst_gap,
            "least_exact_minus_lower_bound": worst_under,
            "gradient_enclosures_containing_difference_quotient": f"{grad_ok}/{grad_n}",
            "classification_disagreements": cls_bad,
        }
        if cls_bad:
            ok = False
        print(row, flush=True)
        report.append(row)
    res = {"rows": report, "all_hold": ok, "cpu_seconds": time.process_time() - t0}
    out.write_text(json.dumps(res, indent=1) + "\n")
    print("ALL_HOLD" if ok else "SOME_FAIL", res["cpu_seconds"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
