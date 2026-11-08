"""Independent exact decider for angle bins of a weighted-point certificate.

Written for the L58 review of jlevy/squares issue #924 without reading either
producer checker or any jlevy/squares tool.  Inputs: the certificate text (format
in premises.py) and a list of angle bins of the half-angle-tangent net
theta_k = 2 arctan(k / N).

What a bin decision proves
--------------------------
For the closed angle interval I = [theta_lo, theta_hi] (0 <= theta_lo < theta_hi
<= 90 deg, with rational tan(theta/2)), and the container [0, s]^2:

    for every theta in I and every centre c such that the closed unit square
    S(c, theta) lies in [0, s]^2, the total weight of certificate points in
    S(c, theta) is at least W  (i.e. weight >= 1).

Method (this program's own; it is not the producer's shrink):

1. Reference angle theta_r with tan(theta_r/2) = (t_lo + t_hi)/2, an exactly
   rational rotation cos = cn/Q, sin = sn/Q.
2. h = max |theta - theta_r| over I is bounded by the rational
   H = max(2(t_r - t_lo)/(1 + t_r t_lo), 2(t_hi - t_r)/(1 + t_r t_hi))
   (arctan z <= z).  B = 1 - H^2/2 + H^4/24 + H - H^3/6 + H^5/120 is a rational
   upper bound on cos h + sin h (increasing on [0, pi/4]; Taylor bounds).
3. Core: the closed square at angle theta_r, same centre, half-side
   a <= 1/(2B) (rounded down onto the 1/(Q D) grid).  For |phi| <= h,
   |R(phi) q|_inf <= (cos h + sin h)|q|_inf <= 1/2, so the core lies in
   S(c, theta) for every theta in I; since 1/(2B) < 1/(2(cos h + sin h)) when
   h > 0, it even lies in the open unit square.
4. Centre domain: the union over theta in I of [r(theta), s - r(theta)]^2,
   r(theta) = (cos theta + sin theta)/2, which is [r_min, s - r_min]^2 with
   r_min = min(r(theta_lo), r(theta_hi)) (r is concave on [0, 90 deg]).
5. Capture of the core as a function of the centre is a sum of indicators of
   closed axis-parallel boxes in the theta_r frame.  Its minimum over the
   (compact, convex) domain equals its minimum over the open cells of the box
   arrangement that meet the domain's interior (boxes are closed, so every
   centre has a nearby open-cell centre capturing no more).  A strip sweep in U
   with an exact cell grid in V computes that minimum exactly; the counts are
   int64 numpy arrays (exact integers), every comparison is exact rational.
6. If the core minimum is below W, the bin is split in t and each half is
   decided again (to --max-depth).  An --exact-angle evaluation (H = 0, a = 1/2,
   the exact domain at that angle) computes the true minimum at one angle; a
   value below W there is a refutation, and the witness centre is re-checked
   by brute force.

Usage:
  python -I decide_bins.py CERT N_NET K [K ...] [--max-depth 8] [--exact-angles]
         [--jsonl OUT]
"""

import argparse
import bisect
import json
import math
import sys
import time
from fractions import Fraction

import numpy as np


# ---------------------------------------------------------------- certificate
def read_certificate(path):
    raw = open(path, "rb").read()
    lines = raw.decode("ascii").rstrip("\n").split("\n")
    side_num, side_den = (int(v) for v in lines[0].split())
    d = int(lines[1])
    w = int(lines[2])
    m = int(lines[3])
    pts = []
    for i in range(m):
        x, y, wt = (int(v) for v in lines[4 + i].split())
        pts.append((x, y, wt))
    assert len(lines) == 4 + m
    side = Fraction(side_num, side_den)
    return side, d, w, pts


# ---------------------------------------------------------------- rotations
def rotation_of_t(t):
    """tan(theta/2) = t  ->  (cn, sn, Q) with cos = cn/Q, sin = sn/Q exactly."""
    p, q = t.numerator, t.denominator
    return q * q - p * p, 2 * p * q, q * q + p * p


def half_extent(t):
    """r(theta) = (cos theta + sin theta)/2, valid for theta in [0, 90 deg]."""
    cn, sn, Q = rotation_of_t(t)
    assert cn >= 0 and sn >= 0
    return Fraction(cn + sn, 2 * Q)


def angle_bound(t_lo, t_r, t_hi):
    h1 = 2 * (t_r - t_lo) / (1 + t_r * t_lo)
    h2 = 2 * (t_hi - t_r) / (1 + t_r * t_hi)
    H = max(h1, h2)
    assert 0 <= H <= Fraction(1, 2)
    B = 1 - H**2 / 2 + H**4 / 24 + H - H**3 / 6 + H**5 / 120
    return H, B


# ---------------------------------------------------------------- core sweep
def min_capture(pts, side, d, t_r, half_side, lo):
    """Exact minimum, over centres c in [lo, side - lo]^2 (real units), of the
    weight of points in the closed square at angle theta_r (tan(theta_r/2) = t_r)
    centred at c with half-side `half_side` (Fraction, real units).

    Returns (min_weight, witness) where witness locates a minimising open cell.
    """
    cn, sn, Q = rotation_of_t(t_r)
    assert cn > 0 and sn >= 0
    # scaled frame: U~ = cn X + sn Y,  V~ = -sn X + cn Y, with X = D x.
    # One real unit of U is Q*D scaled units.
    A = math.floor(half_side * Q * d)          # core half-side, rounded down
    LO = lo * d                                # domain bounds in D units
    HI = side * d - LO
    assert LO < HI
    Q2 = Q * Q
    us = [cn * x + sn * y for x, y, _ in pts]
    vs = [-sn * x + cn * y for x, y, _ in pts]
    ws = [wt for _, _, wt in pts]

    # domain vertices in the scaled frame
    verts = [(LO, LO), (HI, LO), (HI, HI), (LO, HI)]
    vu = [cn * X + sn * Y for X, Y in verts]
    umin, umax = min(vu), max(vu)
    uL = cn * HI + sn * LO      # U~ of vertex (HI, LO): argmin of lower V boundary
    uU = cn * LO + sn * HI      # U~ of vertex (LO, HI): argmax of upper V boundary

    def lower(u):  # max of the lower constraints on V~ at U~ = u
        cands = [(Q2 * LO - sn * u) / cn]
        if sn:
            cands.append((cn * u - Q2 * HI) / sn)
        return max(cands)

    def upper(u):
        cands = [(Q2 * HI - sn * u) / cn]
        if sn:
            cands.append((cn * u - Q2 * LO) / sn)
        return min(cands)

    # V cell grid
    G = sorted(set([v - A for v in vs] + [v + A for v in vs]))
    gindex = {g: i for i, g in enumerate(G)}
    cover = np.zeros(len(G) + 1, dtype=np.int64)
    cell_lo = [gindex[v - A] + 1 for v in vs]
    cell_hi = [gindex[v + A] for v in vs]          # inclusive

    # U events
    opens, closes = {}, {}
    for i, u in enumerate(us):
        opens.setdefault(u - A, []).append(i)
        closes.setdefault(u + A, []).append(i)
    X = sorted(set(opens) | set(closes))

    best = None
    best_at = None
    strips = 0
    # strip boundaries: -inf, X0, X1, ..., Xn-1, +inf
    bounds = [None] + X + [None]
    for j in range(len(bounds) - 1):
        u0, u1 = bounds[j], bounds[j + 1]
        if u0 is not None:
            for i in closes.get(u0, ()):
                cover[cell_lo[i] : cell_hi[i] + 1] -= ws[i]
            for i in opens.get(u0, ()):
                cover[cell_lo[i] : cell_hi[i] + 1] += ws[i]
        # does the open strip (u0, u1) meet the open domain?
        if u1 is not None and u1 <= umin:
            continue
        if u0 is not None and u0 >= umax:
            continue
        a = umin if u0 is None or u0 < umin else u0
        b = umax if u1 is None or u1 > umax else u1
        vlo = lower(min(max(uL, a), b))
        vhi = upper(min(max(uU, a), b))
        if not vlo < vhi:
            continue
        jl = bisect.bisect_right(G, math.floor(vlo))
        jh = bisect.bisect_left(G, math.ceil(vhi))
        seg = cover[jl : jh + 1]
        k = int(seg.argmin())
        val = int(seg[k])
        strips += 1
        if best is None or val < best:
            best = val
            best_at = (a, b, jl + k, vlo, vhi)
    # sanity: every box was removed again
    assert not cover.any(), "sweep bookkeeping error"

    # witness: a rational centre in the minimising open cell and the open domain
    a, b, cell, vlo, vhi = best_at
    glo = G[cell - 1] if cell > 0 else None
    ghi = G[cell] if cell < len(G) else None
    v_lo = vlo if glo is None else max(vlo, Fraction(glo))
    v_hi = vhi if ghi is None else min(vhi, Fraction(ghi))
    witness = None
    if v_lo < v_hi:
        v = (v_lo + v_hi) / 2
        # u-interval where lower(u) < v < upper(u), intersected with (a, b)
        ulo = [Fraction(a), (sn * v + Q2 * LO) / cn]
        uhi = [Fraction(b), (sn * v + Q2 * HI) / cn]
        if sn:
            ulo.append((Q2 * LO - cn * v) / sn)
            uhi.append((Q2 * HI - cn * v) / sn)
        if max(ulo) < min(uhi):
            u = (max(ulo) + min(uhi)) / 2
            assert lower(u) < v < upper(u) and a < u < b
            witness = (u, v)
    out = {"min": best, "strips": strips, "A_scaled": A, "Q": Q}
    if witness:
        u, v = witness
        Xc = (cn * u - sn * v) / Q2
        Yc = (sn * u + cn * v) / Q2
        # brute-force recount at the witness: closed core box
        cap = 0
        for (x, y, wt), pu, pv in zip(pts, us, vs):
            if abs(pu - u) <= A and abs(pv - v) <= A:
                cap += wt
        inside = LO < Xc < HI and LO < Yc < HI
        out["witness"] = {
            "centre_float": [float(Xc / d), float(Yc / d)],
            "brute_force_capture": cap,
            "strictly_inside_domain": inside,
        }
    return best, out


# ---------------------------------------------------------------- decisions
def decide_interval(pts, side, d, w, t_lo, t_hi, depth, max_depth, log):
    t_r = (t_lo + t_hi) / 2
    H, B = angle_bound(t_lo, t_r, t_hi)
    half = 1 / (2 * B)
    lo = min(half_extent(t_lo), half_extent(t_hi))
    m, info = min_capture(pts, side, d, t_r, half, lo)
    rec = {
        "t_lo": str(t_lo), "t_hi": str(t_hi), "depth": depth,
        "H_float": float(H), "shrink_D_units": float((Fraction(1, 2) - half) * d),
        "core_min": m, "decided": m >= w,
    }
    rec.update(info)
    log.append(rec)
    if m >= w:
        return True, m
    if depth >= max_depth:
        return False, m
    tm = (t_lo + t_hi) / 2
    ok1, m1 = decide_interval(pts, side, d, w, t_lo, tm, depth + 1, max_depth, log)
    if not ok1:
        return False, m1
    ok2, m2 = decide_interval(pts, side, d, w, tm, t_hi, depth + 1, max_depth, log)
    return ok2, min(m1, m2)


def exact_angle_min(pts, side, d, t):
    lo = half_extent(t)
    return min_capture(pts, side, d, t, Fraction(1, 2), lo)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("net", type=int)
    ap.add_argument("bins", type=int, nargs="+")
    ap.add_argument("--max-depth", type=int, default=8)
    ap.add_argument("--exact-angles", action="store_true",
                    help="also compute the true minimum at t_lo, t_mid, t_hi")
    ap.add_argument("--jsonl", default=None)
    args = ap.parse_args()
    side, d, w, pts = read_certificate(args.cert)
    out = open(args.jsonl, "a") if args.jsonl else None
    for k in args.bins:
        t0 = time.process_time()
        t_lo, t_hi = Fraction(k, args.net), Fraction(k + 1, args.net)
        log = []
        ok, m = decide_interval(pts, side, d, w, t_lo, t_hi, 0, args.max_depth, log)
        rec = {
            "bin": k, "net": args.net,
            "theta_lo_deg": math.degrees(2 * math.atan(k / args.net)),
            "theta_hi_deg": math.degrees(2 * math.atan((k + 1) / args.net)),
            "decided": ok, "min_over_leaves": m, "W": w,
            "leaves": sum(1 for r in log if r["decided"]) if ok else None,
            "nodes": log,
        }
        if args.exact_angles:
            ex = {}
            for name, t in (("lo", t_lo), ("mid", (t_lo + t_hi) / 2), ("hi", t_hi)):
                mm, info = exact_angle_min(pts, side, d, t)
                ex[name] = {"min": mm, **{kk: info[kk] for kk in ("witness",) if kk in info}}
            rec["exact_angle_minima"] = ex
        rec["cpu_s"] = round(time.process_time() - t0, 2)
        line = json.dumps(rec)
        print(json.dumps({kk: rec[kk] for kk in ("bin", "decided", "min_over_leaves", "W", "leaves", "cpu_s")}
                         | ({"exact": {n: v["min"] for n, v in rec["exact_angle_minima"].items()}} if args.exact_angles else {})
                         | {"root_core_min": log[0]["core_min"], "root_witness": log[0].get("witness")}),
              flush=True)
        if out:
            out.write(line + "\n")
            out.flush()


if __name__ == "__main__":
    main()
