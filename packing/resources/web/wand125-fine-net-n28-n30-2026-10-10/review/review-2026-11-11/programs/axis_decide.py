"""Decides net index 0 (the axis direction) of each certificate completely.

Usage: python -I axis_decide.py --release DIR --out FILE [--factor P/Q]

At angle 0 the core is the axis-parallel square of side B, and its capture is
F(x, y) = sum_k d_k ox_k(x) oy_k(y), where ox_k(x) is the length of
[x - B/2, x + B/2] inside image k's x-range, and oy_k likewise. Each ox_k is piecewise
linear in x with breakpoints X0_k +- B/2 and X1_k +- B/2, so on every cell of the grid
of all breakpoints in the quadrant [L/2, L - 1/2] (whose ends are added), F is
bilinear, and a bilinear function on a rectangle takes its least value at a vertex.
So the least capture over the closed quadrant is the least over the grid's vertices.

Every coordinate, B/2 and the quadrant's ends are multiples of 1e-17, so each overlap is
an exact int64 multiple of 1e-17. The vertex values are one binary64 matrix product
(OX diag(d) OY^T, in row blocks) of nonnegative terms: the overlaps rounded to nearest,
the densities over 1e34 rounded down. For every summation order, with or without fused
multiply-add, the true value is at least the computed one divided by
(1 + gamma_K)(1 + 2^-53)^3, gamma_K = K u / (1 - K u), K the number of terms; the
comparison with 1 is made in fractions. The smallest vertices are evaluated again in
fractions by two methods (overlap lengths and polygon clipping).

With --factor every mass is scaled first (the 99/100 mutant): then the decision must
fail, and the least vertex is an exact witness below 1.
"""

from __future__ import annotations

import argparse
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import fnlib as F  # noqa: E402

NAMES = ("mixed_n28_L57425", "mixed_n30_L58925")
Q = 10**17
U = Fraction(1, 2**53)


def down(x: Fraction) -> float:
    """The largest binary64 value at most x (x positive and in the normal range)."""
    f = float(x)
    if Fraction(f) > x:
        f = math.nextafter(f, 0.0)
    assert Fraction(f) <= x
    return f


def events(lo: int, hi: int, a0: np.ndarray, a1: np.ndarray, h: int) -> np.ndarray:
    cand = np.concatenate([a0 - h, a0 + h, a1 - h, a1 + h])
    cand = cand[(cand > lo) & (cand < hi)]
    return np.unique(np.concatenate([cand, np.array([lo, hi], dtype=np.int64)]))


def overlaps(ev: np.ndarray, a0: np.ndarray, a1: np.ndarray, h: int) -> np.ndarray:
    """Overlap lengths (int64, units 1e-17) of [e - h, e + h] with [a0, a1], events x images."""
    lo = np.maximum(a0[None, :], ev[:, None] - h)
    hi = np.minimum(a1[None, :], ev[:, None] + h)
    return np.maximum(hi - lo, 0)


def one(name: str, cdir: Path, factor: Fraction, keep: int) -> dict:
    t0 = time.process_time()
    cert = F.read_candidate(cdir / "candidate.json.gz")
    L = cert.L
    images = F.expand(cert.rows, L)
    if factor != 1:
        images = {k: d * factor for k, d in images.items()}
    m = F.Measure(images)
    b = cert.B / 2
    lo, hi = L / 2, L - Fraction(1, 2)
    for v in (b, lo, hi):
        assert (v * Q).denominator == 1
    h, qlo, qhi = int(b * Q), int(lo * Q), int(hi * Q)
    keys = m.keys
    X0 = np.array([int(k[0] * Q) for k in keys], dtype=np.int64)
    Y0 = np.array([int(k[1] * Q) for k in keys], dtype=np.int64)
    X1 = np.array([int(k[2] * Q) for k in keys], dtype=np.int64)
    Y1 = np.array([int(k[3] * Q) for k in keys], dtype=np.int64)
    for arr, src in ((X0, 0), (Y0, 1), (X1, 2), (Y1, 3)):
        assert all(Fraction(int(a), Q) == k[src] for a, k in zip(arr, keys))
    ex = events(qlo, qhi, X0, X1, h)
    ey = events(qlo, qhi, Y0, Y1, h)
    # Images that capture nothing anywhere in the quadrant are dropped.
    rel = (X1 > qlo - h) & (X0 < qhi + h) & (Y1 > qlo - h) & (Y0 < qhi + h)
    sel = np.nonzero(rel)[0]
    K = len(sel)
    dens = np.array([down(m.dens[i] / Q**2) for i in sel], dtype=np.float64)
    OX = overlaps(ex, X0[sel], X1[sel], h)
    OY = overlaps(ey, Y0[sel], Y1[sel], h)
    assert OX.max() <= 2**62 and OY.max() <= 2**62
    A = OX.astype(np.float64) * dens[None, :]
    BT = OY.astype(np.float64).T.copy()
    best = []  # (value, i, j) of the smallest computed vertices
    gmin = math.inf
    for s in range(0, len(ex), 256):
        blk = A[s : s + 256] @ BT
        flat = np.argpartition(blk, min(keep, blk.size - 1), axis=None)[:keep]
        for f in flat:
            i, j = divmod(int(f), blk.shape[1])
            best.append((float(blk[i, j]), s + i, j))
        gmin = min(gmin, float(blk.min()))
        best = sorted(best)[:keep]
    gamma = Fraction(K, 1) * U / (1 - Fraction(K, 1) * U)
    shrink = (1 + gamma) * (1 + U) ** 3
    lower = Fraction(gmin) / shrink
    # The smallest vertices again in fractions, by two methods.
    exact = []
    for val, i, j in best:
        x, y = Fraction(int(ex[i]), Q), Fraction(int(ey[j]), Q)
        e1 = F.axis_capture(m, x, y)
        e2 = F.capture(m, 0, x, y)
        assert e1 == e2, "the two exact evaluations differ"
        assert Fraction(val) / shrink <= e1, "the float bound exceeds the exact value"
        exact.append((e1, x, y, val))
    exact.sort()
    e_min, x_min, y_min, v_min = exact[0]
    decided = lower >= 1
    return {
        "certificate": name,
        "factor": F.fstr(factor),
        "quadrant": [F.fstr(lo), F.fstr(hi)],
        "x_events": len(ex),
        "y_events": len(ey),
        "vertices": len(ex) * len(ey),
        "images_in_reach": K,
        "gamma_K_plus_rounding": float(shrink - 1),
        "least_computed_vertex": gmin,
        "rigorous_least_capture": float(lower),
        "rigorous_least_capture_exact_lower": F.fstr(lower) if len(F.fstr(lower)) < 400 else None,
        "least_vertex": [F.fstr(x_min), F.fstr(y_min)],
        "least_vertex_float": [float(x_min), float(y_min)],
        "exact_at_least_vertex": F.fstr(e_min),
        "exact_at_least_vertex_float": float(e_min),
        "computed_at_least_vertex": v_min,
        "smallest_vertices_rechecked_exactly": len(exact),
        "decision": "AXIS_VERIFIED" if decided else ("AXIS_REFUSED" if e_min < 1 else "AXIS_UNDECIDED"),
        "cpu_seconds": round(time.process_time() - t0, 1),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--factor", default="1")
    ap.add_argument("--keep", type=int, default=64)
    args = ap.parse_args()
    factor = F.rat(args.factor)
    res = {name: one(name, Path(args.release) / name, factor, args.keep) for name in NAMES}
    for name, r in res.items():
        print(name, r["decision"], r["x_events"], r["vertices"], r["rigorous_least_capture"],
              r["least_vertex"], r["cpu_seconds"])
    want = "AXIS_VERIFIED" if factor == 1 else "AXIS_REFUSED"
    status = "AXIS_DIRECTION_DECIDED" if all(r["decision"] == want for r in res.values()) else "UNEXPECTED"
    F.write_json(args.out, {"program": "axis_decide.py", "factor": args.factor, "status": status,
                            "certificates": res})
    print(status)
    return 0 if status == "AXIS_DIRECTION_DECIDED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
