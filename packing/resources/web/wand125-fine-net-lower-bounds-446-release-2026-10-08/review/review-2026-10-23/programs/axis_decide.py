"""Decide the axis direction (net index 0) of each certificate completely, independently.

At index 0 the core is the axis-parallel square of side B, and its capture is

    F(x, y) = sum_k rho_k * o_k(x) * p_k(y),
    o_k(x) = |[x - h, x + h] cap [x1_k, x2_k]|,  p_k(y) likewise,  h = B/2,

over the expanded rectangles k. Each o_k is continuous and affine between consecutive
points of {x1_k - h, x1_k + h, x2_k - h, x2_k + h}. On every cell of the grid E x E, with
E the union of those events inside the per-bin quadrant [L/2, L - 1/2] and its two ends,
F is a sum of products of an affine function of x and one of y, hence bilinear, and a
bilinear function on a rectangle takes its least value at a corner. So the least capture
over the closed quadrant is the least value over the grid's vertices (the quarter turn
reduces the whole per-bin domain [1/2, L - 1/2]^2 to this quadrant).

Every coordinate here is an exact rational whose denominator divides Q = 10^17 (checked),
so o_k and p_k at the events are computed exactly as int64 multiples of 1/Q. The vertex
values are one matrix product, evaluated in binary64 with a rigorous a priori bound: all
terms are nonnegative, inputs are rounded at most once (relative 2^-53) and densities are
rounded down, so the true value is at least the computed one divided by
(1 + gamma_K)(1 + u)^3, gamma_K = K u / (1 - K u), u = 2^-53, in any summation order. The
comparison with the threshold 1 is then made in exact rationals. The 64 smallest vertices
are also evaluated exactly (Python fractions) as a check on the float pass.

    OPENBLAS_NUM_THREADS=1 python3 -I axis_decide.py --packet PACKET --out OUT.json
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from t233lib import CERTS, exact_capture, expand, read_candidate  # noqa: E402

Q = 10**17  # every coordinate's denominator divides it (checked); 6 Q < 2^63
U = Fraction(1, 2**53)


def scaled(x: Fraction) -> int:
    v = x * Q
    if v.denominator != 1:
        msg = f"coordinate {x} does not have a denominator dividing 10^17"
        raise ArithmeticError(msg)
    return v.numerator


def overlaps(lo: np.ndarray, hi: np.ndarray, centres: np.ndarray, half: int) -> np.ndarray:
    """Exact int64 lengths |[c - half, c + half] cap [lo, hi]| for every (rect, centre)."""
    a = np.maximum(centres[None, :] - half, lo[:, None])
    b = np.minimum(centres[None, :] + half, hi[:, None])
    return np.maximum(b - a, 0)


def decide(packet: Path, n: int, scale: Fraction = Fraction(1)) -> dict:
    """Decide index 0; ``scale`` multiplies every mass (1 for the certificate itself)."""
    cand = read_candidate(packet, n)
    meas = expand(cand)
    if scale != 1:  # a control: the same measure with every mass scaled
        meas.density = [d * scale for d in meas.density]
        meas.mass = [m * scale for m in meas.mass]
    h = cand.B / 2
    lo_dom = cand.L / 2
    hi_dom = cand.L - Fraction(1, 2)  # rho(a_0) = rho(0) = 1/2
    H = scaled(h)
    x1 = np.array([scaled(r.x1) for r in meas.rects], dtype=np.int64)
    x2 = np.array([scaled(r.x2) for r in meas.rects], dtype=np.int64)
    y1 = np.array([scaled(r.y1) for r in meas.rects], dtype=np.int64)
    y2 = np.array([scaled(r.y2) for r in meas.rects], dtype=np.int64)
    lo_s, hi_s = scaled(lo_dom), scaled(hi_dom)

    def events(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        pts = np.concatenate([a - H, a + H, b - H, b + H, np.array([lo_s, hi_s])])
        pts = pts[(pts >= lo_s) & (pts <= hi_s)]
        return np.unique(pts)

    ex = events(x1, x2)
    ey = events(y1, y2)
    # densities rounded down to binary64, and the exact ones for the recheck
    rho_exact = meas.density
    rho_dn = np.array([float(r) for r in rho_exact], dtype=np.float64)
    for k, r in enumerate(rho_exact):
        if Fraction(rho_dn[k]) > r:
            rho_dn[k] = np.nextafter(rho_dn[k], 0.0)
    kcount = len(rho_exact)
    p_int = overlaps(y1, y2, ey, H)  # K x |Ey|, exact
    p_f = p_int.astype(np.float64)
    best = math.inf
    best_ij = (-1, -1)
    smallest: list[tuple[float, int, int]] = []
    chunk = 256
    for start in range(0, len(ex), chunk):
        cols = ex[start : start + chunk]
        o_int = overlaps(x1, x2, cols, H)  # K x c, exact
        w = o_int.astype(np.float64) * rho_dn[:, None]
        vals = w.T @ p_f  # c x |Ey|
        flat = np.argpartition(vals, 63, axis=None)[:64] if vals.size > 64 else np.arange(vals.size)
        for idx in flat:
            i, j = divmod(int(idx), vals.shape[1])
            smallest.append((float(vals[i, j]), start + i, j))
        m = float(vals.min())
        if m < best:
            i, j = np.unravel_index(int(vals.argmin()), vals.shape)
            best = m
            best_ij = (start + int(i), int(j))
        smallest = sorted(smallest)[:64]
    gamma = kcount * U / (1 - kcount * U)
    factor = (1 + gamma) * (1 + U) ** 3
    lower = Fraction(best) / factor / (Q * Q)  # rigorous lower bound on min F
    decided = lower >= 1
    # exact recheck at the 64 smallest vertices (fractions, integers exact)
    exact_vals = []
    for _v, i, j in smallest:
        xi, yj = int(ex[i]), int(ey[j])
        acc = Fraction(0)
        oi = overlaps(x1, x2, np.array([xi]), H)[:, 0]
        pj = overlaps(y1, y2, np.array([yj]), H)[:, 0]
        nz = np.flatnonzero((oi > 0) & (pj > 0))
        for k in nz:
            acc += rho_exact[k] * int(oi[k]) * int(pj[k])
        exact_vals.append((acc / (Q * Q), Fraction(xi, Q), Fraction(yj, Q)))
    exact_min = min(exact_vals, key=lambda t: t[0])
    # an independent cross-check of one vertex by the clipping geometry
    geo, _i, _b = exact_capture(meas, exact_min[1], exact_min[2], Fraction(1), Fraction(0), h)
    return {
        "certificate": cand.name,
        "domain": [str(lo_dom), str(hi_dom)],
        "x_events": len(ex),
        "y_events": len(ey),
        "vertices": len(ex) * len(ey),
        "expanded_rectangles": kcount,
        "float_min_scaled": best,
        "float_min": best / (Q * Q),
        "rigorous_lower_bound": float(lower),
        "rigorous_lower_bound_exact": f"{lower.numerator}/{lower.denominator}",
        "decided_at_least_1": decided,
        "argmin_vertex": [str(Fraction(int(ex[best_ij[0]]), Q)), str(Fraction(int(ey[best_ij[1]]), Q))],
        "exact_min_over_64_smallest": float(exact_min[0]),
        "exact_min_vertex": [str(exact_min[1]), str(exact_min[2])],
        "clipping_geometry_agrees_at_that_vertex": geo == exact_min[0],
        "gamma_K": float(gamma),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--only", type=int, action="append")
    args = ap.parse_args()
    t0 = time.perf_counter()
    out: dict[str, object] = {"kind": "t233-review-axis-decision/v1", "cases": {}}
    ok = True
    for n in CERTS:
        if args.only and n not in args.only:
            continue
        c0 = resource.getrusage(resource.RUSAGE_SELF)
        res = decide(args.packet, n)
        c1 = resource.getrusage(resource.RUSAGE_SELF)
        res["cpu_seconds"] = round(c1.ru_utime + c1.ru_stime - c0.ru_utime - c0.ru_stime, 3)
        ok = ok and res["decided_at_least_1"] and res["clipping_geometry_agrees_at_that_vertex"]
        out["cases"][str(n)] = res
        print(n, "decided" if res["decided_at_least_1"] else "NOT DECIDED", res["x_events"],
              res["vertices"], res["rigorous_lower_bound"], res["exact_min_over_64_smallest"],
              res["exact_min_vertex"], "cpu", res["cpu_seconds"], flush=True)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["verdict"] = "AXIS_DIRECTION_DECIDED" if ok else "AXIS_DIRECTION_NOT_DECIDED"
    out["cpu_seconds"] = round(usage.ru_utime + usage.ru_stime, 3)
    out["wall_seconds"] = round(time.perf_counter() - t0, 3)
    args.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(out["verdict"], "cpu", out["cpu_seconds"])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
