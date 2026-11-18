"""Decide net index r = 0 (the axis direction) of a format M certificate completely.

Lane r108-1118, blind review of jlevy/squares#1018. At angle 0 the capture of the core of
half-side h centred at (x, y) is F(x, y) = sum_k d_k o_k(x) p_k(y), where
o_k(x) = |[x - h, x + h] n [x0_k, x1_k]| is continuous and affine between consecutive
points of {x0_k - h, x0_k + h, x1_k - h, x1_k + h}, and likewise p_k. On every cell of the
grid of all such points in the quadrant [L/2, U_0]^2 (U_0 = L - w(0) = L - 1/2), together
with the quadrant's ends, F is bilinear, so its least value on the closed quadrant is at a
grid vertex. The events are computed and sorted exactly (Fractions). The vertex values are
one float64 matrix product of nonnegative terms, and each is bounded below rigorously:

    F >= Fc / ((1 + u)(1 + g)) - E (Sx_i + Sy_j) / ((1 - u)(1 - g)),

where Fc is the computed value, u = 2^-53, g = (K + 3) u covers the products and the sum
in any order, E bounds the error of every computed overlap (inputs rounded to nearest, two
sums, a min, a max and a difference), and Sx_i, Sy_j are the computed sums of the rounded
densities times the overlaps at that vertex's abscissa and ordinate. The program uses the
weaker Fc (1 - 3g) - E (Sx_i + Sy_j)(1 + 3g) - 1e-15. The 64 smallest vertices are then
evaluated exactly.

Verdicts: AXIS_DIRECTION_DECIDED when every vertex's lower bound is at least the threshold;
REFUSED_EXACT when an exact vertex value is below it; otherwise UNDECIDED.

Imports nothing from jlevy/squares or the source.

Usage: python -I rv1018_axis.py --measure M.json.gz [--factor 99/100] [--runs RUNS.json]
         --out OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_common as cm  # noqa: E402

U53 = 2.0**-53


def overlaps(ev: np.ndarray, lo: np.ndarray, hi: np.ndarray, hf: float) -> np.ndarray:
    out = np.empty((len(ev), len(lo)))
    for i0 in range(0, len(ev), 512):
        e = ev[i0 : i0 + 512, None]
        o = np.minimum(e + hf, hi[None, :]) - np.maximum(e - hf, lo[None, :])
        np.maximum(o, 0.0, out=out[i0 : i0 + 512])
    return out


def decide_axis(meas: dict, factor: Fraction, threshold: Fraction = Fraction(1)) -> dict:
    t0 = time.process_time()
    side, step = meas["L"], meas["step"]
    h = meas["B"] / 2
    rects = cm.expand(meas["rows"], side)
    lo, hi = side / 2, cm.domain_upper(0, step, side)
    xe, ye = {lo, hi}, {lo, hi}
    for x0, y0, x1, y1, _m, _g in rects:
        for v in (x0 - h, x0 + h, x1 - h, x1 + h):
            if lo <= v <= hi:
                xe.add(v)
        for v in (y0 - h, y0 + h, y1 - h, y1 + h):
            if lo <= v <= hi:
                ye.add(v)
    X, Y = sorted(xe), sorted(ye)
    xs = np.array([float(v) for v in X])
    ys = np.array([float(v) for v in Y])
    K = len(rects)
    x0f = np.array([float(r[0]) for r in rects])
    y0f = np.array([float(r[1]) for r in rects])
    x1f = np.array([float(r[2]) for r in rects])
    y1f = np.array([float(r[3]) for r in rects])
    df = np.array([float(r[5] * factor) for r in rects])
    hf = float(h)
    xmax = max(float(side) + 1.0, float(np.max(np.abs(np.concatenate([x0f, x1f, y0f, y1f])))))
    E = 128.0 * U53 * xmax
    g = (K + 3) * U53
    Ox = overlaps(xs, x0f, x1f, hf)
    Oyd = overlaps(ys, y0f, y1f, hf)
    Oyd *= df[None, :]
    Sx = Ox @ df
    Sy = Oyd.sum(axis=1)
    best_lb = np.inf
    best_lb_at = None
    cand: list[tuple[float, int, int]] = []
    chunk = 256
    for i0 in range(0, len(xs), chunk):
        Fc = Ox[i0 : i0 + chunk] @ Oyd.T
        lb = Fc * (1 - 3 * g) - E * (Sx[i0 : i0 + chunk, None] + Sy[None, :]) * (1 + 3 * g) - 1e-15
        k = int(np.argmin(lb))
        if lb.flat[k] < best_lb:
            best_lb = float(lb.flat[k])
            best_lb_at = (i0 + k // lb.shape[1], k % lb.shape[1])
        take = min(64, Fc.size)
        idx = np.argpartition(Fc, take - 1, axis=None)[:take]
        for f in idx:
            cand.append((float(Fc.flat[f]), i0 + int(f) // Fc.shape[1], int(f) % Fc.shape[1]))
        cand.sort()
        del cand[64:]
    rq = cm.to_mpq_rects(rects, factor)
    hq = cm._q(h)
    exact = []
    for fc, i, j in cand:
        val = cm.capture_exact_axis(rq, hq, cm._q(X[i]), cm._q(Y[j]))
        exact.append((val, i, j, fc))
    exact.sort(key=lambda t: t[0])
    least_val, li, lj, lfc = exact[0]
    thr = cm._q(threshold)
    if Fraction(best_lb) >= threshold:
        verdict = "AXIS_DIRECTION_DECIDED"
    elif least_val < thr:
        verdict = "REFUSED_EXACT"
    else:
        verdict = "UNDECIDED"
    return {
        "verdict": verdict,
        "factor": str(factor),
        "threshold": str(threshold),
        "x_events": len(X),
        "y_events": len(Y),
        "vertices": len(X) * len(Y),
        "expanded_rectangles": K,
        "overlap_error_E": E,
        "gamma": g,
        "max_Sx": float(Sx.max()),
        "max_Sy": float(Sy.max()),
        "rigorous_least_capture": best_lb,
        "rigorous_least_at": [str(X[best_lb_at[0]]), str(Y[best_lb_at[1]])],
        "least_exact_vertex_value": cm.mpq_to_float_str(least_val, 20),
        "least_exact_vertex_value_fraction_digits": len(str(least_val.denominator)),
        "least_exact_vertex": [str(X[li]), str(Y[lj])],
        "least_exact_vertex_float": [float(X[li]), float(Y[lj])],
        "float_estimate_there": lfc,
        "smallest_vertices_evaluated_exactly": len(exact),
        "cpu_seconds": round(time.process_time() - t0, 2),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", required=True)
    ap.add_argument("--factor", default="1")
    ap.add_argument("--runs")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    meas = cm.read_measure(args.measure)
    factor = Fraction(args.factor)
    res = decide_axis(meas, factor)
    res["program"] = "rv1018_axis.py"
    res["measure_json_sha256"] = meas["json_sha256"]
    if args.runs:
        runs = json.loads(Path(args.runs).read_text())
        ax = next(t for t in runs["directions"] if t["r"] == 0)
        rects_q = cm.to_mpq_rects(cm.expand(meas["rows"], meas["L"]), factor)
        argmin = [Fraction(v) for v in ax["argmin"]]
        at = cm.capture_exact_axis(rects_q, cm._q(meas["B"] / 2), cm._q(argmin[0]), cm._q(argmin[1]))
        logged = Fraction(float(ax["bound"]))
        res["source_axis"] = {
            "x_events": ax["x_events"],
            "y_events": ax["y_events"],
            "vertices": ax["vertices"],
            "argmin": ax["argmin"],
            "logged_bound": ax["bound"],
            "events_agree": [ax["x_events"], ax["y_events"]] == [res["x_events"], res["y_events"]],
            "exact_capture_at_argmin": cm.mpq_to_float_str(at, 20),
            "exact_minus_logged_bound": float(Fraction(at.numerator, at.denominator) - logged),
            "argmin_is_least_exact_vertex": [str(v) for v in argmin] == res["least_exact_vertex"]
            or [str(v) for v in argmin[::-1]] == res["least_exact_vertex"],
        }
    Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    print(res["verdict"], "rigorous least", res["rigorous_least_capture"], "exact least",
          res["least_exact_vertex_value"], "cpu", res["cpu_seconds"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
