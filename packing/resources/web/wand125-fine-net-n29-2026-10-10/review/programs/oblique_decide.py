"""Decide one oblique direction r >= 1 of a check2 candidate over its whole
per-bin domain, by a branch and bound written for review think-1lri that shares
no code, no lemma of the search and no arithmetic with the crate.

Claim decided: for every centre p in [rho(a_r), L - rho(a_r)]^2 the closed core
Q_r(p) (side B, angle theta_r = 2 atan(r D)) captures at least 1.  With
--domain quadrant only [L/2, L - rho(a_r)]^2 is searched, and lemma C1 (the
quarter turn about the centre) extends the verdict to the domain.

The bound (derived for this review):

  Q. (--bound corners)  For an image rectangle R (convex) and the
     core Q_0 at angle theta_r (a convex square centred at the origin),
     A(p) = |R ∩ (Q_0 + p)| has A^(1/2) concave on the convex set
     S = {p : R ∩ (Q_0 + p) is nonempty}: if a in R ∩ (Q_0 + p) and b in
     R ∩ (Q_0 + q), then la + (1-l)b lies in R ∩ (Q_0 + lp + (1-l)q), so that set
     contains l(R ∩ (Q_0 + p)) + (1-l)(R ∩ (Q_0 + q)), and the Brunn-Minkowski
     inequality in the plane gives A(lp + (1-l)q)^(1/2) >= l A(p)^(1/2) +
     (1-l) A(q)^(1/2).  So on a box C = [xa, xb] x [ya, yb] of centres, A is at least
     its least value at the four corners: if every corner lies in S, then C lies in S
     (S is convex) and a concave function's minimum over a box is at a corner; if one
     corner does not, A is 0 there and the bound is 0.  Hence every p in C has
     F(p) = sum_k g_k A_k(p) >= sum_k g_k min_corners A_k.  A rectangle that misses
     every core of the box contributes 0 and one inside every core its mass (C below);
     each other one is evaluated at the four exact corners by E and I with the core of
     half-side h rounded down (a subset of the core).  No derivative is used, and no
     lemma of the crate's search (the crate bounds a derivative, lemmas R3 to R5).
     Q is never weaker than S, but it costs four area evaluations a rectangle where S
     costs one, and on this measure S decided direction 312 in 51,001 boxes against
     Q's 49,029, at 18.8 against 62.4 CPU seconds, so S is the default.
  S. (the default, --bound intersection)  For a box of
     centres C = [cx +- dx] x [cy +- dy], the rectangle
     Q'' = {q : |u.(q - p0)| <= hu, |v.(q - p0)| <= hv},  p0 = (cx, cy),
     hu = h - (c dx + s dy), hv = h - (s dx + c dy),  u = (c, s), v = (-s, c),
     lies in Q(p) for every p in C: |u.(p - p0)| <= c dx + s dy and
     |v.(p - p0)| <= s dx + c dy, and the triangle inequality.  The density is
     nonnegative, so every p in C has F(p) >= the integral of g over Q''.
     Nothing about derivatives is used.
  E. The area |R ∩ Q''| of an axis-parallel rectangle R = [X1, X2] x [Y1, Y2] and
     a rectangle Q'' of half-sizes hu, hv along u and v centred at p0 (lemma S's, or
     for lemma Q the core at a corner, hu = hv = h rounded down), with coordinates
     relative to p0, is the integral over xi in [X1, X2] of
     max(0, eta(xi)), eta = min(Y2, f1, f2) - max(Y1, g1, g2) with
     f1 = (hu - c xi)/s, g1 = (-hu - c xi)/s, f2 = (hv + s xi)/c,
     g2 = (s xi - hv)/c.  eta is concave (a minimum of affine functions minus a
     maximum of affine functions), so for any nodes X1 <= xi_0 <= ... <= xi_m <= X2
     and lower bounds lambda_i <= eta(xi_i) the area is at least
     sum_i max(0, (xi_{i+1} - xi_i)(lambda_i + lambda_{i+1})/2).  The nodes are
     placed at the approximate breakpoints (the four vertices and the eight
     crossings with Y1 and Y2), so the sum is nearly exact; their accuracy
     affects only tightness, never validity.
  I. Every lambda_i is an interval lower end: c and s enter as binary64 enclosures
     of the exact rationals, hu and hv as binary64 values rounded down (so Q'' is
     replaced by a subset), R by its inner binary64 rectangle (a subset), and every
     operation is rounded outward by one ulp with numpy.nextafter after a correctly
     rounded IEEE operation.  The weighted sum over rectangles of nonnegative lower
     bounds is taken in any order and multiplied by (1 - 2 gamma_K), K the term
     count's bound.  A box is accepted when that number is at least 1.
  C. Classification, in binary64 with slack TAU = 1e-12 (every quantity tested is
     within 1e-14 of its exact value): a rectangle whose outer binary64 rectangle
     lies in Q'' by TAU on all four sides contributes its exact mass m/8 rounded
     down; one whose outer rectangle misses the superset square of half-sizes
     h + c dx + s dy, h + s dx + c dy by TAU along x, y, u or v meets no core of the
     box and is dropped for the box's children too; the rest go through E and I.
  X. A box that is not accepted is split across its longer side.  A box of depth at
     least 20 whose centre, by E and I with the full core, may capture below
     1 + 1e-9 has its centre's capture evaluated exactly in fractions
     (fine_net_exact.capture); a value below 1 with the centre in the domain is a
     counterexample and the direction is refuted.  A box at the depth limit is
     unresolved.  Verified means every box was accepted.

Usage: python3 -I oblique_decide.py CANDIDATE.json[.gz] R [--domain full|quadrant]
       [--bound corners|intersection] [--scale 99/100] [--max-depth 64]
       [--max-boxes N] [--out FILE]
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import sys
import time
from fractions import Fraction as F
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fine_net_exact as fx  # noqa: E402

TAU = 1e-12
U = 2.0**-53
NINF, PINF = -np.inf, np.inf


def dn(x):
    return np.nextafter(x, NINF)


def up(x):
    return np.nextafter(x, PINF)


def f_dn(q: F) -> float:
    """The largest binary64 value at most q."""
    x = float(q)
    while F(x) > q:
        x = float(np.nextafter(x, NINF))
    return x


def f_up(q: F) -> float:
    """The smallest binary64 value at least q."""
    x = float(q)
    while F(x) < q:
        x = float(np.nextafter(x, PINF))
    return x


class Direction:
    def __init__(self, c: F, s: F, h: F):
        self.c, self.s, self.h = c, s, h
        self.c_lo, self.c_hi = f_dn(c), f_up(c)
        self.s_lo, self.s_hi = f_dn(s), f_up(s)
        self.h_lo, self.h_hi = f_dn(h), f_up(h)
        self.cm, self.sm = float(c), float(s)


def half_sizes(d: Direction, dx, dy):
    """(hu'', hv'') rounded down and (hu+, hv+) rounded up, for arrays dx, dy >= 0."""
    a_hi = up(up(d.c_hi * dx) + up(d.s_hi * dy))
    b_hi = up(up(d.s_hi * dx) + up(d.c_hi * dy))
    hu = dn(d.h_lo - a_hi)
    hv = dn(d.h_lo - b_hi)
    hup = up(d.h_hi + a_hi)
    hvp = up(d.h_hi + b_hi)
    return hu, hv, hup, hvp


def area_lower(d: Direction, hu, hv, X1, X2, Y1, Y2):
    """Lower bounds of |[X1, X2] x [Y1, Y2] ∩ Q''| for arrays (coordinates relative
    to the box centre, already rounded inward: X1, Y1 up and X2, Y2 down), with
    Q'' of half-sizes hu, hv (binary64, used exactly) at the exact direction whose
    enclosures d holds.  Lemma E with the nodes clamped into [X1, X2], lemma I."""
    c, s = d.cm, d.sm
    huc, hus, hvc, hvs = hu * c, hu * s, hv * c, hv * s
    nodes = np.stack([
        X1, X2,
        huc - hvs, huc + hvs, -huc + hvs, -huc - hvs,
        (hu - s * Y2) / c, (hu - s * Y1) / c, (-hu - s * Y1) / c, (-hu - s * Y2) / c,
        (c * Y2 - hv) / s, (c * Y1 - hv) / s, (c * Y1 + hv) / s, (c * Y2 + hv) / s,
    ], axis=1)
    lo = X1[:, None]
    hi = X2[:, None]
    nodes = np.minimum(np.maximum(nodes, lo), hi)
    nodes.sort(axis=1)
    xi = nodes
    pos = xi >= 0
    cxi_hi = np.where(pos, up(d.c_hi * xi), up(d.c_lo * xi))
    cxi_lo = np.where(pos, dn(d.c_lo * xi), dn(d.c_hi * xi))
    sxi_hi = np.where(pos, up(d.s_hi * xi), up(d.s_lo * xi))
    sxi_lo = np.where(pos, dn(d.s_lo * xi), dn(d.s_hi * xi))
    huu = hu[:, None]
    hvv = hv[:, None]
    num = dn(huu - cxi_hi)
    f1 = np.where(num >= 0, dn(num / d.s_hi), dn(num / d.s_lo))
    num = up(-huu - cxi_lo)
    g1 = np.where(num >= 0, up(num / d.s_lo), up(num / d.s_hi))
    num = dn(sxi_lo + hvv)
    f2 = np.where(num >= 0, dn(num / d.c_hi), dn(num / d.c_lo))
    num = up(sxi_hi - hvv)
    g2 = np.where(num >= 0, up(num / d.c_lo), up(num / d.c_hi))
    top = np.minimum(np.minimum(Y2[:, None], f1), f2)
    bot = np.maximum(np.maximum(Y1[:, None], g1), g2)
    lam = dn(top - bot)
    w = np.maximum(dn(xi[:, 1:] - xi[:, :-1]), 0.0)
    sl = dn(lam[:, :-1] + lam[:, 1:])
    term = np.where(sl > 0, np.maximum(dn(dn(w * sl) * 0.5), 0.0), 0.0)
    acc = np.zeros(len(X1))
    for j in range(term.shape[1]):
        acc = dn(acc + term[:, j])
    acc = np.maximum(acc, 0.0)
    empty = ~(X1 < X2)
    acc[empty] = 0.0
    return acc


class Measure:
    def __init__(self, cand, scale: F = F(1)):
        self.ims = fx.images(cand, scale)
        ims = self.ims
        self.K = len(ims)
        self.X1o = np.array([f_dn(im[0]) for im in ims])
        self.Y1o = np.array([f_dn(im[1]) for im in ims])
        self.X2o = np.array([f_up(im[2]) for im in ims])
        self.Y2o = np.array([f_up(im[3]) for im in ims])
        self.X1i = np.array([f_up(im[0]) for im in ims])
        self.Y1i = np.array([f_up(im[1]) for im in ims])
        self.X2i = np.array([f_dn(im[2]) for im in ims])
        self.Y2i = np.array([f_dn(im[3]) for im in ims])
        self.G = np.array([f_dn(im[4]) for im in ims])
        self.Mass = np.array([f_dn(im[4] * (im[2] - im[0]) * (im[3] - im[1])) for im in ims])
        self.gamma = (self.K + 2) * U / (1 - (self.K + 2) * U)
        self.sum_factor = float(np.nextafter(1.0 - 2.0 * self.gamma - 4 * U, 0.0))


def box_bounds(meas: Measure, d: Direction, bx, by, bdx, bdy, pb, pk, full_core=False, corners=None):
    """For pairs (box pb, image pk): classify and return (per-pair keep mask,
    per-box lower bound).

    With corners = ((xa, ya), (xb, ya), (xa, yb), (xb, yb)), arrays per box giving
    the exact corners of the box's covering range, a straddling image contributes
    its density times the least, over the four corners v, of the lower bound of
    |R ∩ Q(v)| (lemma Q of the module docstring).  Without corners it contributes
    its capture by the intersection of the box's cores (lemma S).  With full_core,
    the core itself at the box centre is used (dx = dy = 0), which gives a lower
    bound of F at the centre."""
    if full_core:
        hu, hv, hup, hvp = half_sizes(d, np.zeros_like(bdx), np.zeros_like(bdy))
    else:
        hu, hv, hup, hvp = half_sizes(d, bdx, bdy)
    cx = bx[pb]
    cy = by[pb]
    hu_p, hv_p, hup_p, hvp_p = hu[pb], hv[pb], hup[pb], hvp[pb]
    ox1 = meas.X1o[pk] - cx
    ox2 = meas.X2o[pk] - cx
    oy1 = meas.Y1o[pk] - cy
    oy2 = meas.Y2o[pk] - cy
    c, s = d.cm, d.sm
    umin = c * ox1 + s * oy1
    umax = c * ox2 + s * oy2
    vmin = -s * ox2 + c * oy1
    vmax = -s * ox1 + c * oy2
    extx = c * hup_p + s * hvp_p
    exty = s * hup_p + c * hvp_p
    outside = ((umin > hup_p + TAU) | (umax < -hup_p - TAU) | (vmin > hvp_p + TAU) | (vmax < -hvp_p - TAU)
               | (ox1 > extx + TAU) | (ox2 < -extx - TAU) | (oy1 > exty + TAU) | (oy2 < -exty - TAU))
    valid = (hu_p > 0) & (hv_p > 0)
    inside = valid & (umin >= -hu_p + TAU) & (umax <= hu_p - TAU) & (vmin >= -hv_p + TAU) & (vmax <= hv_p - TAU) & ~outside
    boundary = valid & ~outside & ~inside
    val = np.zeros(len(pb))
    val[inside] = meas.Mass[pk[inside]]
    if corners is not None:
        # every image the box's cores may meet goes through lemma Q, which also
        # covers images whose intersection of cores is empty (hu or hv <= 0)
        boundary = ~outside & ~inside
    bidx = np.nonzero(boundary)[0]
    if len(bidx):
        kk = pk[bidx]
        if corners is None:
            X1 = up(meas.X1i[kk] - cx[bidx])
            X2 = dn(meas.X2i[kk] - cx[bidx])
            Y1 = up(meas.Y1i[kk] - cy[bidx])
            Y2 = dn(meas.Y2i[kk] - cy[bidx])
            a = area_lower(d, hu_p[bidx], hv_p[bidx], X1, X2, Y1, Y2)
        else:
            hfull = np.full(len(bidx), d.h_lo)
            a = None
            for vx_box, vy_box in corners:
                vx = vx_box[pb[bidx]]
                vy = vy_box[pb[bidx]]
                X1 = up(meas.X1i[kk] - vx)
                X2 = dn(meas.X2i[kk] - vx)
                Y1 = up(meas.Y1i[kk] - vy)
                Y2 = dn(meas.Y2i[kk] - vy)
                av = area_lower(d, hfull, hfull, X1, X2, Y1, Y2)
                a = av if a is None else np.minimum(a, av)
        val[bidx] = np.maximum(dn(meas.G[kk] * a), 0.0)
    total = np.bincount(pb, weights=val, minlength=len(bx))
    lower = np.maximum(dn(total * meas.sum_factor), 0.0)
    return ~outside, lower


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("candidate", type=Path)
    ap.add_argument("r", type=int)
    ap.add_argument("--domain", choices=["full", "quadrant"], default="full")
    ap.add_argument("--scale", default="1")
    ap.add_argument("--max-depth", type=int, default=64)
    ap.add_argument("--max-boxes", type=int, default=30_000_000)
    ap.add_argument("--max-pairs", type=int, default=250_000)
    ap.add_argument("--bound", choices=["corners", "intersection"], default="intersection")
    ap.add_argument("--split", choices=["longer", "adaptive"], default="longer")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    t0 = time.time()
    cand = fx.load_candidate(args.candidate)
    scale = F(args.scale)
    r = args.r
    if not 1 <= r <= cand.last:
        raise SystemExit("an oblique direction is 1 .. last")
    c, s = fx.direction(cand.D, r)
    d = Direction(c, s, cand.h)
    meas = Measure(cand, scale)
    lo, hi = fx.per_bin_domain(cand, r)
    a_lo = f_dn(lo if args.domain == "full" else cand.L / 2)
    a_hi = f_up(hi)
    # boxes: covering ranges [xa, xb] x [ya, yb] (binary64), the box [cx +- dx] x [cy +- dy] contains them
    stack = [(np.array([a_lo]), np.array([a_hi]), np.array([a_lo]), np.array([a_hi]), np.array([0]),
              np.zeros(meas.K, dtype=np.int64), np.arange(meas.K, dtype=np.int64))]
    boxes = accepted = 0
    least_accepted = math.inf
    least_accepted_box = None
    depth_hist: dict = {}
    exact_checks = []
    status = None
    witness = None
    least_centre_estimate = math.inf
    least_centre_at = None
    iterations = 0
    while stack and status is None:
        xa, xb, ya, yb, depth, pb, pk = stack.pop()
        # merge small chunks from the top of the stack into one batch (order only)
        parts = [(xa, xb, ya, yb, depth, pb, pk)]
        npairs = len(pk)
        while stack and npairs + len(stack[-1][6]) <= args.max_pairs:
            part = stack.pop()
            parts.append(part)
            npairs += len(part[6])
        if len(parts) > 1:
            offs = np.cumsum([0] + [len(p[0]) for p in parts[:-1]])
            xa, xb, ya, yb, depth = (np.concatenate([p[i] for p in parts]) for i in range(5))
            pb = np.concatenate([p[5] + o for p, o in zip(parts, offs)])
            pk = np.concatenate([p[6] for p in parts])
        iterations += 1
        if iterations % 200 == 0:
            print(f"  {boxes} boxes, {accepted} accepted, stack {len(stack)}, batch {len(xa)} boxes / {len(pk)} pairs",
                  file=sys.stderr, flush=True)
        nb = len(xa)
        boxes += nb
        if boxes > args.max_boxes:
            status = "UNRESOLVED_BUDGET"
            break
        cx = (xa + xb) * 0.5
        cy = (ya + yb) * 0.5
        dx = up(np.maximum(up(xb - cx), up(cx - xa)))
        dy = up(np.maximum(up(yb - cy), up(cy - ya)))
        corners = ((xa, ya), (xb, ya), (xa, yb), (xb, yb)) if args.bound == "corners" else None
        keep, lower = box_bounds(meas, d, cx, cy, dx, dy, pb, pk, corners=corners)
        ok = lower >= 1.0
        accepted += int(ok.sum())
        if ok.any():
            dvals, dcounts = np.unique(depth[ok], return_counts=True)
            for dv, dc in zip(dvals.tolist(), dcounts.tolist()):
                depth_hist[dv] = depth_hist.get(dv, 0) + dc
        if ok.any():
            m = int(np.argmin(np.where(ok, lower, np.inf)))
            if lower[m] < least_accepted:
                least_accepted = float(lower[m])
                least_accepted_box = [float(cx[m]), float(cy[m]), float(dx[m]), float(dy[m]), int(depth[m])]
        fail = np.nonzero(~ok)[0]
        if len(fail) == 0:
            continue
        # counterexample screen at deep boxes: the full core at the centre
        deep = fail[depth[fail] >= 20]
        if len(deep):
            sel = np.isin(pb, deep) & keep
            remap = -np.ones(nb, dtype=np.int64)
            remap[deep] = np.arange(len(deep))
            _, est = box_bounds(meas, d, cx[deep], cy[deep], dx[deep], dy[deep], remap[pb[sel]], pk[sel], full_core=True)
            jmin = int(np.argmin(est))
            if float(est[jmin]) < least_centre_estimate:
                least_centre_estimate = float(est[jmin])
                least_centre_at = (float(cx[deep[jmin]]), float(cy[deep[jmin]]))
            for j in np.nonzero(est < 1.0 + 1e-9)[0]:
                b = deep[j]
                px, py = F(float(cx[b])), F(float(cy[b]))
                e = fx.capture(meas.ims, px, py, c, s, cand.h)
                inside_domain = lo <= px <= hi and lo <= py <= hi
                exact_checks.append({"centre": [float(cx[b]), float(cy[b])], "exact": float(e), "in_domain": inside_domain})
                if e < 1 and inside_domain:
                    status = "REFUTED"
                    witness = {"centre": [str(px), str(py)], "exact_capture": str(e), "exact_capture_approx": float(e),
                               "depth": int(depth[b])}
                    break
            if status:
                break
        if (depth[fail] >= args.max_depth).any():
            status = "UNRESOLVED_DEPTH"
            break
        # split each failing box across its longer side, or (--split adaptive) across the
        # side whose halving at the same centre raises the box's bound more; the choice
        # is only an order of search and never accepts anything.  Children inherit the
        # parent's kept images.
        wide = (xb - xa) >= (yb - ya)
        if args.split == "adaptive":
            sel = np.isin(pb, fail) & keep
            remap = -np.ones(nb, dtype=np.int64)
            remap[fail] = np.arange(len(fail))
            _, lx = box_bounds(meas, d, cx[fail], cy[fail], dx[fail] * 0.5, dy[fail], remap[pb[sel]], pk[sel])
            _, ly = box_bounds(meas, d, cx[fail], cy[fail], dx[fail], dy[fail] * 0.5, remap[pb[sel]], pk[sel])
            choice = np.where(lx > ly, True, np.where(ly > lx, False, wide[fail]))
            wide = wide.copy()
            wide[fail] = choice
        mx = (xa + xb) * 0.5
        my = (ya + yb) * 0.5
        f = fail
        cxa = np.concatenate([xa[f], np.where(wide[f], mx[f], xa[f])])
        cxb = np.concatenate([np.where(wide[f], mx[f], xb[f]), xb[f]])
        cya = np.concatenate([ya[f], np.where(wide[f], ya[f], my[f])])
        cyb = np.concatenate([np.where(wide[f], yb[f], my[f]), yb[f]])
        cdepth = np.concatenate([depth[f], depth[f]]) + 1
        # pair lists for the children
        kept = keep & np.isin(pb, f)
        ppb, ppk = pb[kept], pk[kept]
        pos = -np.ones(nb, dtype=np.int64)
        pos[f] = np.arange(len(f))
        child_pb = np.concatenate([pos[ppb], pos[ppb] + len(f)])
        child_pk = np.concatenate([ppk, ppk])
        order = np.argsort(child_pb, kind="stable")
        child_pb, child_pk = child_pb[order], child_pk[order]
        # chunk children so that each chunk has at most max_pairs pairs
        counts = np.bincount(child_pb, minlength=2 * len(f))
        starts = np.concatenate([[0], np.cumsum(counts)])
        i = 0
        nchild = 2 * len(f)
        chunks = []
        while i < nchild:
            j = i + 1
            while j < nchild and starts[j + 1] - starts[i] <= args.max_pairs:
                j += 1
            sl = slice(starts[i], starts[j])
            chunks.append((cxa[i:j], cxb[i:j], cya[i:j], cyb[i:j], cdepth[i:j], child_pb[sl] - i, child_pk[sl]))
            i = j
        stack.extend(reversed(chunks))
    if status is None:
        status = "VERIFIED"
    least_centre = None
    if least_centre_at is not None:
        px, py = F(least_centre_at[0]), F(least_centre_at[1])
        e = fx.capture(meas.ims, px, py, c, s, cand.h)
        least_centre = {"centre": [str(px), str(py)], "estimate": least_centre_estimate, "exact": str(e),
                        "exact_approx": float(e), "estimate_le_exact": F(least_centre_estimate) <= e,
                        "in_domain": lo <= px <= hi and lo <= py <= hi}
    ru = resource.getrusage(resource.RUSAGE_SELF)
    out = {
        "candidate": str(args.candidate),
        "candidate_sha256": cand.file_sha256,
        "direction": r,
        "scale": str(scale),
        "bound": args.bound,
        "split": args.split,
        "domain": args.domain,
        "domain_exact": [str(lo), str(hi)] if args.domain == "full" else [str(cand.L / 2), str(hi)],
        "domain_searched_binary64": [a_lo, a_hi],
        "status": status,
        "boxes": boxes,
        "accepted": accepted,
        "max_depth_accepted": max(depth_hist) if depth_hist else None,
        "depth_histogram": dict(sorted(depth_hist.items())),
        "least_accepted_lower_bound": least_accepted,
        "least_accepted_box": least_accepted_box,
        "least_centre_estimate_at_depth_ge_20": least_centre_estimate,
        "least_centre_exact": least_centre,
        "exact_checks": exact_checks[:20],
        "exact_checks_count": len(exact_checks),
        "witness": witness,
        "sum_factor": meas.sum_factor,
        "cpu_seconds": ru.ru_utime + ru.ru_stime,
        "wall_seconds": time.time() - t0,
    }
    text = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0 if status in ("VERIFIED", "REFUTED") else 1


if __name__ == "__main__":
    sys.exit(main())
