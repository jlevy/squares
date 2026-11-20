"""Decide net node 0 (the axis angle) completely, by a vertex argument.

Usage: r144_axis.py --bundle BUNDLE_DIR [--factor P/Q] --out OUT.json

At angle 0 the core is [X - b, X + b] x [Y - b, Y + b], b = B/2, and the capture is
F(X, Y) = sum_k w_k f_k(X) g_k(Y): a point contributes indicators in X and Y, a
horizontal segment its overlap fraction in X and an indicator in Y, a vertical segment
the reverse, a rectangle overlap fractions in both. Between consecutive breakpoints
(every image coordinate +- b inside the quadrant, and the quadrant's ends) each f_k and
g_k is affine, so F is bilinear on every cell and its least value on a closed cell, with
the one-sided limits of the indicators from inside that cell, is at a corner. Points are
counted in the closed core, so F at a cell boundary is at least either one-sided limit,
and the infimum of F over the quadrant [L/2, L - b]^2 is the least one-sided corner
value. The rotation by pi/2 about the centre of K preserves the measure and the axis
angle, and the quadrant's four images cover the centre domain [b, L - b]^2.

Coordinates are scaled by the least common denominator to exact integers below 2^53.
Corner values are binary64 matrix products of nonnegative factors: overlaps rounded to
nearest, masses rounded down; the true value is at least the computed one divided by
(1 + u)^4 (1 + gamma_k), u = 2^-53, k the number of terms, in any summation order. The
least corners are then evaluated again in exact rationals, and a witness pose inside the
least cell is evaluated with the exact evaluator.

Verdict AXIS_DECIDED (least corner value >= 1, rigorously), AXIS_REFUSED (an exact
witness below 1), or AXIS_UNDECIDED. Written for this review; imports nothing from
jlevy/squares or the source.
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

from r144_common import angle_data, expand_images, frac_str, load_candidate, rat, round_down  # noqa: E402
from r144_exact import Measure, capture_a, capture_b  # noqa: E402

U = F(1, 2**53)


def build(cand: dict, factor: F):
    L, B = cand["L"], cand["B"]
    b = B / 2
    imgs = expand_images(cand["primitives"], L, factor)
    den = math.lcm(L.denominator, b.denominator, (L / 2).denominator)
    for kind, g, m, _i, _g in imgs:
        for v in g:
            den = math.lcm(den, v.denominator)
    if den * L >= 2**52:
        raise SystemExit(f"scaled coordinates too large: {den}")
    S = lambda q: int(q * den)  # noqa: E731 (exact: den is a common denominator)
    xp, yp = [], []  # (type, a, c) type 0 indicator at a, type 1 overlap [a, c]
    w, wq = [], []
    for kind, g, m, _i, _g in imgs:
        if kind == "point":
            xp.append((0, S(g[0]), 0))
            yp.append((0, S(g[1]), 0))
        elif kind == "segment":
            x0, y0, x1, y1 = g
            if y0 == y1:
                xp.append((1, S(min(x0, x1)), S(max(x0, x1))))
                yp.append((0, S(y0), 0))
            elif x0 == x1:
                xp.append((0, S(x0), 0))
                yp.append((1, S(min(y0, y1)), S(max(y0, y1))))
            else:
                raise SystemExit("oblique segment: the axis decision does not apply")
        else:
            x0, y0, x1, y1 = g
            xp.append((1, S(x0), S(x1)))
            yp.append((1, S(y0), S(y1)))
        w.append(round_down(m))
        wq.append(m)
    return {"den": den, "b": S(b), "lo": S(L / 2), "hi": S(L - b), "xp": xp, "yp": yp, "w": np.array(w), "wq": wq, "L": L, "bq": b}


def breakpoints(prof, b, lo, hi):
    pts = {lo, hi}
    for t, a, c in prof:
        cand = (a - b, a + b) if t == 0 else (a - b, a + b, c - b, c + b)
        for v in cand:
            if lo <= v <= hi:
                pts.add(v)
    return np.array(sorted(pts), dtype=np.int64)


def profile_arrays(prof):
    t = np.array([p[0] for p in prof], dtype=np.int64)
    a = np.array([p[1] for p in prof], dtype=np.int64)
    c = np.array([p[2] for p in prof], dtype=np.int64)
    ext_lo = a.copy()
    ext_hi = np.where(t == 0, a, c)
    return t, a, c, ext_lo, ext_hi


def values(X, t, a, c, b, side):
    """f_k(X) for breakpoints X (n,) and images (k,), one-sided for indicators.
    side +1: right limit, -1: left limit. Overlaps exact integers, then one division."""
    Xc = X[:, None]
    if side > 0:
        ind = (a[None, :] - b <= Xc) & (Xc < a[None, :] + b)
    else:
        ind = (a[None, :] - b < Xc) & (Xc <= a[None, :] + b)
    ov = np.minimum(c[None, :], Xc + b) - np.maximum(a[None, :], Xc - b)
    ov = np.maximum(ov, 0)
    length = np.where(t == 1, c - a, 1)
    frac = ov.astype(np.float64) / length[None, :].astype(np.float64)
    return np.where(t[None, :] == 0, ind.astype(np.float64), frac)


def exact_corner(data, X: int, Y: int, sx: int, sy: int) -> F:
    b = data["b"]
    tot = F(0)
    for (tx, ax, cx), (ty, ay, cy), m in zip(data["xp"], data["yp"], data["wq"]):
        fx = _exact_val(tx, ax, cx, b, X, sx)
        if fx == 0:
            continue
        fy = _exact_val(ty, ay, cy, b, Y, sy)
        if fy == 0:
            continue
        tot += m * fx * fy
    return tot


def _exact_val(t, a, c, b, X, side) -> F:
    if t == 0:
        if side > 0:
            return F(1) if a - b <= X < a + b else F(0)
        return F(1) if a - b < X <= a + b else F(0)
    ov = min(c, X + b) - max(a, X - b)
    return F(max(ov, 0), c - a)


def decide(cand: dict, factor: F, BLK: int = 192) -> dict:
    t0 = time.process_time()
    data = build(cand, factor)
    b, lo, hi = data["b"], data["lo"], data["hi"]
    tx, ax, cx, xlo_e, xhi_e = profile_arrays(data["xp"])
    ty, ay, cy, ylo_e, yhi_e = profile_arrays(data["yp"])
    BX = breakpoints(data["xp"], b, lo, hi)
    BY = breakpoints(data["yp"], b, lo, hi)
    w = data["w"]
    best = []  # (value, X, Y, sx, sy)
    kmax = 0
    nbx = (len(BX) + BLK - 1) // BLK
    nby = (len(BY) + BLK - 1) // BLK
    for i in range(nbx):
        Xs = BX[i * BLK : (i + 1) * BLK]
        relx = np.nonzero((xhi_e >= Xs[0] - b) & (xlo_e <= Xs[-1] + b))[0]
        FXp = values(Xs, tx[relx], ax[relx], cx[relx], b, +1)
        FXm = values(Xs, tx[relx], ax[relx], cx[relx], b, -1)
        validx = {+1: Xs < hi, -1: Xs > lo}
        for jb in range(nby):
            Ys = BY[jb * BLK : (jb + 1) * BLK]
            sel = (yhi_e[relx] >= Ys[0] - b) & (ylo_e[relx] <= Ys[-1] + b)
            rel = relx[sel]
            if len(rel) == 0:
                for sx in (1, -1):
                    for sy in (1, -1):
                        vx = np.nonzero(validx[sx])[0]
                        vy = np.nonzero({+1: Ys < hi, -1: Ys > lo}[sy])[0]
                        if len(vx) and len(vy):
                            best.append((0.0, int(Xs[vx[0]]), int(Ys[vy[0]]), sx, sy))
                continue
            kmax = max(kmax, len(rel))
            GYp = values(Ys, ty[rel], ay[rel], cy[rel], b, +1)
            GYm = values(Ys, ty[rel], ay[rel], cy[rel], b, -1)
            wr = w[rel]
            validy = {+1: Ys < hi, -1: Ys > lo}
            for sx, FX in ((1, FXp), (-1, FXm)):
                A = FX[:, sel] * wr[None, :]
                for sy, GY in ((1, GYp), (-1, GYm)):
                    V = A @ GY.T
                    V = np.where(validx[sx][:, None] & validy[sy][None, :], V, np.inf)
                    flat = np.argsort(V, axis=None)[:4]
                    for f_ in flat:
                        r_, c_ = np.unravel_index(f_, V.shape)
                        if np.isfinite(V[r_, c_]):
                            best.append((float(V[r_, c_]), int(Xs[r_]), int(Ys[c_]), sx, sy))
        best.sort()
        best = best[:64]
    best.sort()
    k = kmax
    gam = F(k) * U / (1 - F(k) * U)
    vmin = best[0][0]
    rig = F(vmin) / ((1 + U) ** 4 * (1 + gam))
    den = data["den"]
    exact = []
    for v, X, Y, sx, sy in best[:24]:
        q = exact_corner(data, X, Y, sx, sy)
        exact.append({"value_binary64": v, "X": frac_str(F(X, den)), "Y": frac_str(F(Y, den)), "sx": sx, "sy": sy, "exact": frac_str(q), "exact_float": float(q)})
    least = min(exact, key=lambda e: F(e["exact"]))
    # witness pose inside the least cell, 1/1000 of the way to the next breakpoints
    Xv, Yv = F(least["X"]) * den, F(least["Y"]) * den
    ix = int(np.searchsorted(BX, int(Xv)))
    iy = int(np.searchsorted(BY, int(Yv)))
    nx = BX[ix + 1] if least["sx"] > 0 else BX[ix - 1]
    ny = BY[iy + 1] if least["sy"] > 0 else BY[iy - 1]
    px = F(int(Xv), den) + F(int(nx) - int(Xv), den) / 1000
    py = F(int(Yv), den) + F(int(ny) - int(Yv), den) / 1000
    meas = Measure(cand["primitives"], cand["L"], factor)
    ang = angle_data(0, cand["step"], cand["L"], cand["B"])
    wa = capture_a(meas, ang, px, py)
    wb = capture_b(meas, ang, px, py)
    if rig >= 1:
        verdict = "AXIS_DECIDED"
    elif wa < 1 and wa == wb:
        verdict = "AXIS_REFUSED"
    else:
        verdict = "AXIS_UNDECIDED"
    res = {
        "program": "r144_axis.py",
        "factor": frac_str(factor),
        "verdict": verdict,
        "scale_denominator": den,
        "breakpoints_x": int(len(BX)),
        "breakpoints_y": int(len(BY)),
        "corners": int(len(BX) * len(BY)),
        "max_terms_per_block": k,
        "least_binary64": vmin,
        "rigorous_lower_bound": f"{float(rig):.17g}",
        "rigorous_lower_bound_minus_one": float(rig - 1),
        "least_corners_exact": exact,
        "least_exact": least,
        "witness_pose": {"x": frac_str(px), "y": frac_str(py), "capture_a": frac_str(wa), "capture_b": frac_str(wb), "capture_float": float(wa), "a_equals_b": wa == wb},
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--factor", default="1")
    ap.add_argument("--block", type=int, default=192)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cand = load_candidate(open(os.path.join(a.bundle, "candidate.json"), "rb").read())
    res = decide(cand, rat(a.factor), a.block)
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print(res["verdict"], f"factor {a.factor}", f"corners {res['corners']}", f"rigorous lower {res['rigorous_lower_bound']}", f"least exact {res['least_exact']['exact_float']!r}", f"witness {res['witness_pose']['capture_float']!r}", f"cpu {res['cpu_seconds']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
