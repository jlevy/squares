#!/usr/bin/env python3
"""Build a zero-margin pose-space box tree for a weighted point certificate and emit it as Lean data
for the kernel checker `Sqpack/ZMTree.lean` (rung 2 of the Lean ladder; see `lean/LADDER.md`).

Usage (from the repo root):
  python3 lean/scripts/gen_zmtree.py CERT --n N --name NAME --outdir lean/Sqpack/NAME
          [--K 12] [--J 32] [--pitch 1/10] [--ubins 8] [--nproc 4] [--chunk-cost 6000] [--parts 4]
          [--save trees.pkl | --load trees.pkl]

The search is `search/zeromargin.py`'s (its `run_box` recursion with `clip_bin`, EMPTY, ADM and
CHAIN on the D4 roots `[0, m/2]^2 x u in [0, 1/2]`), with zeromargin.py used read-only as an
*oracle*: its float screens and exact tests propose the leaf (the ADM witness set T is recomputed
without P1 and without inherited points, which the Lean leaf does not have), and every leaf is
re-checked by `leaf_ok` below, an exact integer mirror of `ZMTree.check`; a box whose certificate
the mirror rejects is split further (on s(13) that never happens).  Chain leaves are then pruned
(`optimise_leaf`: fewer pivots, fewer claimed entries and reasons, as long as every region still
reaches W).  The Lean kernel is the judge; nothing in this script is trusted (a wrong tree only
makes `decide` fail).

Integer semantics (mirror of `ZMTree.lean`):
* spatial scale        Q = D * S, S = 2^K; point (X, Y) of the certificate is (X*S, Y*S) / Q;
* angle parameter      u = tan(theta/2) = U / R, R = 2^J; root U in [0, R/2];
* root                 [0, M/2]^2 x [0, R/2]; `XM`/`YM` nodes cut it into (m/2)/pitch cells per axis,
                       each cell's u-range into `ubins` bins by `U` splits; below, midpoint splits.
Leaf kinds: `E` (no admissible pose), `Z` (ADM witnesses plus up to two monotone chains, CHAIN).
Node kinds: `X`, `Y`, `U` (midpoint splits), `XM`, `YM` (explicit splits), `F` (candidate
pruning), `C` (clip_bin).  Output: NAME/Pts.lean (points, `ptsL`), NAME/Part*.lean (chunks, one
`decide +kernel` each, balanced over --parts files), NAME/Cov.lean (`cov_root`, glued by
`Cov.split*` / `ZMTree.C_cov`).  Deterministic.
"""
import argparse
import hashlib
import math
import os
import sys
import time
from fractions import Fraction as F

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'search'))
import zeromargin as zm  # noqa: E402  (read-only use: Checker's float screens and exact tests)

sys.setrecursionlimit(100000)


def read_cert(path):
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    it = iter(raw.decode().split())
    snum, sden = int(next(it)), int(next(it))
    D = int(next(it)); W = int(next(it)); m = int(next(it))
    pts = [(int(next(it)), int(next(it)), int(next(it))) for _ in range(m)]
    assert next(it, None) is None, "trailing data is not supported"
    return sha, F(snum, sden), D, W, pts


# =============================================================================================
# The exact integer mirror of ZMTree.lean.  Signed pairs (p, n) of the Lean are plain Python
# ints here: every Lean test is a comparison of p - n with 0, which is what is computed.

class Ctx:
    def __init__(self, S, Q, R, W, Fr):
        self.S, self.Q, self.R, self.W, self.F = S, Q, R, W, Fr
        self.RR = R * R


def qok(a0, a1, a2, U0, U1):
    """ZMTree.qOk: max of a0 + a1 v + a2 v^2 over [U0, U1] is <= 0 (exact)."""
    if a0 + a1 * U0 + a2 * U0 * U0 > 0:
        return False
    if a0 + a1 * U1 + a2 * U1 * U1 > 0:
        return False
    if a2 < 0 and a1 + 2 * U0 * a2 > 0 and a1 + 2 * U1 * a2 < 0:
        return a1 * a1 - 4 * a0 * a2 <= 0
    return True


def bok(p, U0, U1):
    """ZMTree.bOk: the degree-4 Bernstein coefficients on [U0, U1] are all <= 0."""
    p0, p1, p2, p3, p4 = p
    H = U1 - U0
    b0 = p0 + U0 * (p1 + U0 * (p2 + U0 * (p3 + U0 * p4)))
    b1 = H * (p1 + U0 * (2 * p2 + U0 * (3 * p3 + U0 * 4 * p4)))
    b2 = H * H * (p2 + U0 * (3 * p3 + U0 * 6 * p4))
    b3 = H * H * H * (p3 + U0 * 4 * p4)
    b4 = H * H * H * H * p4
    return (b0 <= 0 and 4 * b0 + b1 <= 0 and 6 * b0 + 3 * b1 + b2 <= 0
            and 4 * b0 + 3 * b1 + 2 * b2 + b3 <= 0 and b0 + b1 + b2 + b3 + b4 <= 0)


def gq(ctx, k, A, B):
    """ZMTree.gq: R^2 Q G_k(v/R) at offsets (A, B)/Q, as a quadratic in v."""
    Q, R, RR = ctx.Q, ctx.R, ctx.RR
    if k == 0:
        return (RR * (2 * A - Q), 4 * R * B, -(2 * A + Q))
    if k == 1:
        return (RR * -(2 * A + Q), -(4 * R * B), 2 * A - Q)
    if k == 2:
        return (RR * (2 * B - Q), -(4 * R * A), -(2 * B + Q))
    return (RR * -(2 * B + Q), 4 * R * A, 2 * B - Q)


def uR(XS, c):
    return (2 * (XS - c), 0, 2 * (XS - c))


def uW(ctx, XS):
    Q = ctx.Q
    return (2 * XS - Q, -2 * Q, 2 * XS + Q)


def cpoly(ctx, k, U, V):
    """ZMTree.cpoly: Q R^4 condPoly_k(U, V)(v / R) as a quartic in v."""
    Q, R = ctx.Q, ctx.R
    U0, U1, U2 = U; V0, V1, V2 = V
    if k == 0:
        c = (U0 - Q, U1 + 2 * V0, U2 - U0 + 2 * V1 - 2 * Q, -U1 + 2 * V2, -U2 - Q)
    elif k == 1:
        c = (-U0 - Q, -U1 - 2 * V0, U0 - U2 - 2 * V1 - 2 * Q, U1 - 2 * V2, U2 - Q)
    elif k == 2:
        c = (V0 - Q, V1 - 2 * U0, V2 - V0 - 2 * U1 - 2 * Q, -V1 - 2 * U2, -V2 - Q)
    else:
        c = (-V0 - Q, 2 * U0 - V1, V0 - V2 + 2 * U1 - 2 * Q, V1 + 2 * U2, V2 - Q)
    RR = ctx.RR
    return (c[0] * RR * RR, c[1] * RR * R, c[2] * RR, c[3] * R, c[4])


def admk(ctx, k, XS, YS, box):
    """ZMTree.admK: condition k of the point holds at every admissible pose of the box."""
    x0, x1, y0, y1, U0, U1 = box
    if k == 0:
        if qok(*gq(ctx, 0, XS - x0, YS - y0), U0, U1):
            return True
        return (bok(cpoly(ctx, 0, uR(XS, x0), uW(ctx, YS)), U0, U1)
                or bok(cpoly(ctx, 0, uW(ctx, XS), uR(YS, y0)), U0, U1)
                or bok(cpoly(ctx, 0, uW(ctx, XS), uW(ctx, YS)), U0, U1))
    if k == 1:
        return qok(*gq(ctx, 1, XS - x1, YS - y1), U0, U1)
    if k == 2:
        return (qok(*gq(ctx, 2, XS - x1, YS - y0), U0, U1)
                or bok(cpoly(ctx, 2, uR(XS, x1), uW(ctx, YS)), U0, U1))
    return (qok(*gq(ctx, 3, XS - x0, YS - y1), U0, U1)
            or bok(cpoly(ctx, 3, uW(ctx, XS), uR(YS, y1)), U0, U1))


def comb(l, a, b):
    if l == 0:
        return a - b
    if l == 1:
        return a + b
    if l == 2:
        return 2 * a + b
    return a + 2 * b


def pairok(ctx, l, kp, XSp, YSp, kq, XSq, YSq, box):
    """ZMTree.pairOk: lamA(l) G_p + lamB(l) G_q <= 0 on the whole (unclipped) box."""
    x0, x1, y0, y1, U0, U1 = box
    for cx in (x0, x1):
        for cy in (y0, y1):
            g = gq(ctx, kp, XSp - cx, YSp - cy)
            h = gq(ctx, kq, XSq - cx, YSq - cy)
            if not qok(comb(l, g[0], h[0]), comb(l, g[1], h[1]), comb(l, g[2], h[2]), U0, U1):
                return False
    return True


def wge(ctx, U, K):
    """Q (R^2 + 2UR - U^2) >= 2 K (R^2 + U^2), i.e. w(U/R)/2 >= K/Q."""
    R, RR = ctx.R, ctx.RR
    return ctx.Q * (RR + 2 * U * R - U * U) >= 2 * K * (RR + U * U)


def empty_ok(ctx, box):
    """ZMTree check of an `E` leaf: x1 (or y1) is below w/2 at both ends of the bin."""
    x0, x1, y0, y1, U0, U1 = box
    if U1 > ctx.R:
        return False
    R, RR, Q = ctx.R, ctx.RR, ctx.Q

    def below(z):
        return all(2 * z * (RR + U * U) < Q * (RR + 2 * U * R - U * U) for U in (U0, U1))
    return below(x1) or below(y1)


def clip_ok(ctx, box, us):
    x0, x1, y0, y1, U0, U1 = box
    R = ctx.R
    return (U0 <= us <= U1 and wge(ctx, us, min(x1, y1))
            and (R + us) * (R + U1) < 2 * ctx.RR)


def clip_value(ctx, box):
    """The smallest grid U in [U0, U1] with w(U/R)/2 >= min(x1, y1)/Q (w is increasing on the
    bins where the clip is allowed), or None when no clip applies."""
    x0, x1, y0, y1, U0, U1 = box
    if U1 <= U0:
        return None
    K = min(x1, y1)
    if not wge(ctx, U1, K):
        return None                     # the whole bin may hold admissible poses
    if (ctx.R + U0) * (ctx.R + U1) >= 2 * ctx.RR:
        return None
    lo, hi = U0, U1                     # smallest U with wge(U): wge(hi) holds
    if wge(ctx, lo, K):
        hi = lo
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if wge(ctx, mid, K):
            hi = mid
        else:
            lo = mid
    us = hi
    if us >= U1 or not clip_ok(ctx, box, us):
        return None
    return us


class Leaf:
    """A `Z` leaf: claimed entries (index into the candidate list, tag), two chains of pivots
    (X, Y, kind) over D, and the emptiness staircase [(e_r, l_r)] for chain A x chain B.
    tag = (kp, (dA, uA, lA), (dB, uB, lB)); kp = 4: all four conditions by ADM."""
    def __init__(self, ents, chA, chB, emp):
        self.ents, self.chA, self.chB, self.emp = ents, chA, chB, emp


def capc(reason, r):
    d, uu, _ = reason
    return (0 < d <= r) or r < uu


def capt(tag, r, s):
    return tag[0] == 4 or capc(tag[1], r) or capc(tag[2], s)


def reas_ok(ctx, ch, reason, kp, XS, YS, box):
    d, uu, l = reason
    S = ctx.S
    if d != 0:
        if d > len(ch):
            return False
        qx, qy, qk = ch[d - 1]
        if not pairok(ctx, 0, kp, XS, YS, qk, qx * S, qy * S, box):
            return False
    if uu != 0:
        if uu > len(ch) or not (1 <= l <= 3):
            return False
        qx, qy, qk = ch[uu - 1]
        if not pairok(ctx, l, kp, XS, YS, qk, qx * S, qy * S, box):
            return False
    return True


def leaf_ok(ctx, box, cands, leaf, verbose=False):
    """Exact mirror of `ZMTree.check` on a `Z` leaf (cands = the candidate list at the leaf)."""
    x0, x1, y0, y1, U0, U1 = box
    if U1 > ctx.R or U0 > U1:
        return False
    S = ctx.S
    cl = []
    pos = 0
    for gap, tag in leaf.ents:
        pos += gap
        if pos >= len(cands):
            return False
        cl.append((cands[pos], tag))
        pos += 1
    for (X, Y, w), tag in cl:
        kp = tag[0]
        if kp > 4:
            return False
        XS, YS = X * S, Y * S
        for k in range(4):
            if k != kp and not admk(ctx, k, XS, YS, box):
                if verbose:
                    print("adm fail", (X, Y), k)
                return False
        if kp != 4:
            if not reas_ok(ctx, leaf.chA, tag[1], kp, XS, YS, box):
                return False
            if not reas_ok(ctx, leaf.chB, tag[2], kp, XS, YS, box):
                return False
    for ch in (leaf.chA, leaf.chB):
        for a, b in zip(ch, ch[1:]):
            if not pairok(ctx, 0, a[2], a[0] * S, a[1] * S, b[2], b[0] * S, b[1] * S, box):
                return False
    ka, kb = len(leaf.chA), len(leaf.chB)
    for r in range(ka):
        e, l = leaf.emp[r] if r < len(leaf.emp) else (0, 0)
        if e != 0:
            if e > kb or not (1 <= l <= 3):
                return False
            a = leaf.chA[r]; b = leaf.chB[e - 1]
            if not pairok(ctx, l, a[2], a[0] * S, a[1] * S, b[2], b[0] * S, b[1] * S, box):
                return False
    for r in range(ka + 1):
        er = leaf.emp[r][0] if r < len(leaf.emp) else 0
        for s in range(kb + 1):
            if r < ka and s < er:
                continue
            tot = sum(e[2] for e, t in cl if capt(t, r, s))
            if tot < ctx.W:
                return False
    return True


# =============================================================================================
# The search: zeromargin.py's run_box, with every leaf re-derived in the mirror's terms.

class Search:
    def __init__(self, ctx, D, W, pts, m):
        self.ctx, self.D, self.Wden = ctx, D, W
        self.pts = pts                                      # sorted (X, Y, w)
        self.m = F(m)
        self.chk = zm.Checker(m, [(F(X, D), F(Y, D)) for X, Y, _ in pts],
                              [F(w, W) for _, _, w in pts], use_chain=True, clip=True)
        assert self.chk.symmetric_d4()
        self.idx = {p: i for i, p in enumerate(pts)}
        self.stat = dict(E=0, ADM=0, CHAIN1=0, CHAIN2=0, C=0, split=0, zm_only=0, boxes=0,
                         maxdepth=0, claimed=0, chainpts=0, piv=0)

    def fbox(self, box):
        Q, R = self.ctx.Q, self.ctx.R
        x0, x1, y0, y1, U0, U1 = box
        return (F(x0, Q), F(x1, Q), F(y0, Q), F(y1, Q), F(U0, R), F(U1, R))

    # --- T: the points certified by ADM for the whole box (mirror test, float pre-screen)
    def t_set(self, box, fb, B):
        chk = self.chk
        specs = chk._adm_specs(fb, B)
        mask, cmasks = chk._adm_mask(specs, fb[4], fb[5], per_cond=True)
        S = self.ctx.S
        T = []
        for k in np.nonzero(mask)[0]:
            X, Y, w = self.pts[k]
            if all(admk(self.ctx, c, X * S, Y * S, box) for c in range(4)):
                T.append(int(k))
        return T, specs, cmasks

    def chain_leaf(self, box, fb, B, T, specs, cmasks):
        """cert_chain_fast of zeromargin.py with T = the mirror's ADM set (no P1, no inherited
        points); returns a Leaf or None."""
        chk = self.chk
        cx0, cx1, cy0, cy1, u0, u1 = fb
        n = len(self.pts)
        inT = np.zeros(n, dtype=bool); inT[T] = True
        cxm, cym = float((cx0 + cx1) / 2), float((cy0 + cy1) / 2)
        rad = 0.7072 + 0.5 * math.hypot(float(cx1 - cx0), float(cy1 - cy0))
        reach = (((chk.Pxf - cxm) ** 2 + (chk.Pyf - cym) ** 2) <= rad * rad) & (~inT) & (chk.Wf > 0)
        wT = int(chk.Wnum[inT].sum())
        if wT + int(chk.Wnum[reach].sum()) < chk.Wden:
            return None
        nfail = np.zeros(n, dtype=np.int8)
        for cm in cmasks:
            nfail += (~cm)
        reach &= (nfail <= 1)
        S = self.ctx.S
        cand = []
        for k in np.nonzero(reach)[0]:
            X, Y, w = self.pts[k]
            bad = None
            for c in range(4):
                if not cmasks[c][k]:
                    if bad is not None:
                        bad = -1; break
                    bad = c; continue
                if not admk(self.ctx, c, X * S, Y * S, box):
                    if bad is not None:
                        bad = -1; break
                    bad = c
            if bad is None or bad < 0:
                continue
            cand.append((int(k), bad))
        if len(cand) < 2:
            return None
        if wT + sum(int(chk.Wnum[k]) for k, _ in cand) < chk.Wden:
            return None
        nc = len(cand)
        ck = np.array([k for k, _ in cand], dtype=np.int64)
        cd = np.array([d for _, d in cand], dtype=np.int64)
        TOL = chk.FTOL
        f0, f1 = float(u0), float(u1)
        Gf = np.empty((4, nc, 3))
        ci = 0
        for cx in (cx0, cx1):
            for cy in (cy0, cy1):
                a = chk.Pxf[ck] - float(cx); b = chk.Pyf[ck] - float(cy)
                g = Gf[ci]
                g[:, 0] = np.select([cd == 0, cd == 1, cd == 2], [2 * a - 1, -2 * a - 1, 2 * b - 1], -2 * b - 1)
                g[:, 1] = np.select([cd == 0, cd == 1, cd == 2], [4 * b, -4 * b, -4 * a], 4 * a)
                g[:, 2] = np.select([cd == 0, cd == 1, cd == 2], [-2 * a - 1, 2 * a - 1, -2 * b - 1], 2 * b - 1)
                ci += 1

        def fmax(ia, wa, ib, wb):
            best = None
            for c in range(4):
                G = Gf[c]
                v = zm._quadmax_f(wa * G[ia, 0] + wb * G[ib, 0], wa * G[ia, 1] + wb * G[ib, 1],
                                  wa * G[ia, 2] + wb * G[ib, 2], f0, f1)
                best = v if best is None else np.maximum(best, v)
            return best

        ctx = self.ctx
        excache = {}

        def ex(i, l, j):
            """exact: pairOk(l, cand i, cand j) in the mirror (l = 0: G_i - G_j; 1,2,3: lambdas)"""
            key = (i, l, j)
            r = excache.get(key)
            if r is None:
                ki, di = cand[i]; kj, dj = cand[j]
                Xi, Yi, _ = self.pts[ki]; Xj, Yj, _ = self.pts[kj]
                r = excache[key] = pairok(ctx, l, di, Xi * S, Yi * S, dj, Xj * S, Yj * S, box)
            return r

        LAMS = ((1, 1.0), (2, 0.5), (3, 2.0))          # l code, float lambda (G_a + lam G_q)

        def lam_of(i, j):
            for l, _ in LAMS:
                if ex(i, l, j):
                    return l
            return 0

        yn_, yd_ = F(cym).numerator, F(cym).denominator
        xn_, xd_ = F(cxm).numerator, F(cxm).denominator
        umn, umd = ((u0 + u1) / 2).numerator, ((u0 + u1) / 2).denominator
        Lp = chk.Dp
        for d_ in (xd_, yd_):
            Lp = Lp * d_ // math.gcd(Lp, d_)
        sP, sX, sY = Lp // chk.Dp, Lp // xd_, Lp // yd_

        def pxkey(k, kd):
            A = chk.PXi[k] * sP - xn_ * sX; Bv = chk.PYi[k] * sP - yn_ * sY
            if kd == 0: g0, g1 = 2 * A - Lp, 4 * Bv
            elif kd == 1: g0, g1 = -2 * A - Lp, -4 * Bv
            elif kd == 2: g0, g1 = 2 * Bv - Lp, -4 * A
            else: g0, g1 = -2 * Bv - Lp, 4 * A
            return (g0 * umd + g1 * umn) / (Lp * umd)

        kinds = sorted({kd for _, kd in cand}, key=lambda kd: -sum(chk.Wf[k] for k, d in cand if d == kd))
        chains = []
        for kd in kinds:
            grp = [i for i in range(nc) if cand[i][1] == kd]
            if len(grp) < 2:
                continue
            grp.sort(key=lambda i: pxkey(cand[i][0], kd))
            garr = np.array(grp, dtype=np.int64); ng = len(grp)
            Mg = fmax(np.repeat(garr, ng), 1.0, np.tile(garr, ng), -1.0).reshape(ng, ng)
            ch = [grp[0]]; lastg = 0; p = 1
            while p < ng:
                nxt = np.nonzero(Mg[lastg, p:] <= TOL)[0]
                if len(nxt) == 0:
                    break
                p += int(nxt[0])
                if ex(ch[-1], 0, grp[p]):
                    ch.append(grp[p]); lastg = p
                p += 1
            chains.append(ch)
        if not chains:
            return None

        def bsearch_down(chp):
            kk = len(chp)
            lo = np.ones(nc, dtype=np.int64); hi = np.full(nc, kk + 1, dtype=np.int64)
            while True:
                act = np.nonzero(lo < hi)[0]
                if len(act) == 0:
                    break
                mid = (lo[act] + hi[act]) // 2
                q = chp[mid - 1]
                selfq = (q == act)
                v = fmax(act, 1.0, q, -1.0)
                pred = selfq | (v < -TOL)
                for t in np.nonzero(~selfq & (np.abs(v) <= TOL))[0]:
                    pred[t] = ex(int(act[t]), 0, int(q[t]))
                hi[act[pred]] = mid[pred]
                lo[act[~pred]] = mid[~pred] + 1
            for i in range(nc):
                r = int(lo[i])
                if r <= kk and not ex(i, 0, int(chp[r - 1])):
                    a_, b_ = 1, kk + 1
                    while a_ < b_:
                        m_ = (a_ + b_) // 2
                        if ex(i, 0, int(chp[m_ - 1])): b_ = m_
                        else: a_ = m_ + 1
                    lo[i] = a_
            return lo

        def bsearch_up(rowsq, chp, selfcheck):
            kk = len(chp); nr = len(rowsq)
            lo = np.zeros(nr, dtype=np.int64); hi = np.full(nr, kk, dtype=np.int64)
            while True:
                act = np.nonzero(lo < hi)[0]
                if len(act) == 0:
                    break
                mid = (lo[act] + hi[act] + 1) // 2
                q = chp[mid - 1]; ia = rowsq[act]
                notself = (q != ia) if selfcheck else np.ones(len(act), dtype=bool)
                vs = [fmax(ia, 1.0, q, lf) for _, lf in LAMS]
                yes = (vs[0] < -TOL) | (vs[1] < -TOL) | (vs[2] < -TOL)
                no = (vs[0] > TOL) & (vs[1] > TOL) & (vs[2] > TOL)
                good = notself & yes
                for t in np.nonzero(notself & ~yes & ~no)[0]:
                    good[t] = any(ex(int(ia[t]), l, int(q[t]))
                                  for (l, _), vv in zip(LAMS, vs) if abs(vv[t]) <= TOL)
                lo[act[good]] = mid[good]
                hi[act[~good]] = mid[~good] - 1
            lams = np.zeros(nr, dtype=np.int64)
            for x in range(nr):
                r = int(lo[x])
                if r > 0:
                    l = lam_of(int(rowsq[x]), int(chp[r - 1]))
                    if l == 0 or (selfcheck and int(chp[r - 1]) == int(rowsq[x])):
                        a_, b_ = 0, kk
                        while a_ < b_:
                            m_ = (a_ + b_ + 1) // 2
                            qq = int(chp[m_ - 1])
                            if (not selfcheck or qq != int(rowsq[x])) and lam_of(int(rowsq[x]), qq): a_ = m_
                            else: b_ = m_ - 1
                        lo[x] = a_
                        l = lam_of(int(rowsq[x]), int(chp[a_ - 1])) if a_ > 0 else 0
                    lams[x] = l
            return lo, lams

        allrows = np.arange(nc, dtype=np.int64)

        def analyse(ch):
            kk = len(ch); chp = np.array(ch, dtype=np.int64)
            dlo = bsearch_down(chp)
            ulo, ulam = bsearch_up(allrows, chp, True)
            dlo = np.where(dlo <= kk, dlo, 0)                # 0: no down reason
            return chp, dlo, ulo, ulam

        Wc = chk.Wnum[ck]
        need = chk.Wden - wT
        info = [analyse(ch) for ch in chains]

        def cap_mat(dlo, ulo, kk):
            r_ = np.arange(kk + 1)[:, None]
            return ((dlo[None, :] > 0) & (dlo[None, :] <= r_)) | (r_ < ulo[None, :])

        def build(chsel, empt=None, elam=None):
            """Leaf from chain(s) chsel = [i] or [i, j] (indices into chains/info)."""
            tags = {}
            for k in T:
                tags[k] = (4, (0, 0, 0), (0, 0, 0))
            reasons = [[(0, 0, 0)] * nc, [(0, 0, 0)] * nc]
            for slot, ci in enumerate(chsel):
                chp, dlo, ulo, ulam = info[ci]
                for i in range(nc):
                    reasons[slot][i] = (int(dlo[i]), int(ulo[i]), int(ulam[i]) if ulo[i] > 0 else 0)
            for i in range(nc):
                rA, rB = reasons[0][i], reasons[1][i]
                if rA[0] or rA[1] or rB[0] or rB[1]:
                    tags[cand[i][0]] = (cand[i][1], rA, rB)
            piv = []
            for ci in chsel:
                chp = info[ci][0]
                piv.append([(self.pts[cand[int(i)][0]][0], self.pts[cand[int(i)][0]][1], cand[int(i)][1])
                            for i in chp])
            chA = piv[0]; chB = piv[1] if len(piv) > 1 else []
            emp = []
            if empt is not None:
                emp = [(int(e), int(l)) for e, l in zip(empt, elam)]
            ents = sorted(tags.items())
            return chA, chB, emp, ents

        for ci, ch in enumerate(chains):
            chp, dlo, ulo, ulam = info[ci]; kk = len(ch)
            U = cap_mat(dlo, ulo, kk)
            if int((U.astype(np.int64) @ Wc).min()) >= need:
                return ('CHAIN1',) + build([ci])
        for i in range(len(chains)):
            for j in range(i + 1, len(chains)):
                chA, dA, uA, _ = info[i]; chB, dB, uB, _ = info[j]
                ka, kb = len(chA), len(chB)
                empt, elam = bsearch_up(chA, chB, False)
                MA = cap_mat(dA, uA, ka); MB = cap_mat(dB, uB, kb).astype(np.int64)
                ok = True
                sidx = np.arange(kb + 1)
                for r in range(ka + 1):
                    if r < ka:
                        live = ~((sidx < kb) & (empt[r] >= sidx + 1))
                    else:
                        live = np.ones(kb + 1, dtype=bool)
                    if not live.any():
                        continue
                    tot = np.maximum(MB[live], MA[r][None, :].astype(np.int64)) @ Wc
                    if int(tot.min()) < need:
                        ok = False; break
                if ok:
                    return ('CHAIN2',) + build([i, j], empt, elam)
        return None

    def leaf_for(self, box, depth):
        """('E',) or ('Z', kind, Leaf-as-index-tags) or None."""
        ctx = self.ctx
        if empty_ok(ctx, box):
            return ('E',)
        fb = self.fbox(box)
        B = zm.bin_data(fb[4], fb[5])
        T, specs, cmasks = self.t_set(box, fb, B)
        wT = sum(self.pts[k][2] for k in T)
        if wT >= ctx.W:
            take, need = [], ctx.W
            for k in sorted(T, key=lambda k: -self.pts[k][2]):
                if need <= 0:
                    break
                take.append(k); need -= self.pts[k][2]
            ents = sorted((k, (4, (0, 0, 0), (0, 0, 0))) for k in take)
            return ('ADM', [], [], [], ents)
        r = self.chain_leaf(box, fb, B, T, specs, cmasks)
        return r

    def _build(self, box, depth):
        ctx = self.ctx
        st = self.stat
        st['boxes'] += 1
        st['maxdepth'] = max(st['maxdepth'], depth)
        if depth > 40:
            raise RuntimeError(f"depth limit at {box}")
        us = clip_value(ctx, box)
        if us is not None:
            st['C'] += 1
            nb = box[:5] + (us,)
            return ('C', us, self._build(nb, depth))
        lf = self.leaf_for(box, depth)
        if lf is not None:
            if lf[0] == 'E':
                st['E'] += 1
                return ('E',)
            kind, chA, chB, emp, ents = lf
            if kind != 'ADM':
                chA, chB, emp, ents = optimise_leaf(ctx.W, self.pts, chA, chB, emp, ents)
            leaf = Leaf(None, chA, chB, emp)
            # mirror check against the full point list (gaps = indices here)
            leaf.ents = []
            prev = -1
            for k, tag in ents:
                leaf.ents.append((k - prev - 1, tag)); prev = k
            if leaf_ok(ctx, box, self.pts, leaf):
                st[kind] += 1
                st['claimed'] += len(ents)
                st['chainpts'] += sum(1 for _, t in ents if t[0] != 4)
                st['piv'] += len(chA) + len(chB)
                return ('Z', kind, chA, chB, emp, ents)
            st['zm_only'] += 1
        st['split'] += 1
        x0, x1, y0, y1, U0, U1 = box
        fb = self.fbox(box)
        B = zm.bin_data(fb[4], fb[5])
        dx, dy, du = fb[1] - fb[0], fb[3] - fb[2], 2 * (fb[5] - fb[4])
        m = self.m
        if (fb[4] * 2 < B['wlo'] and (fb[0] < B['whi'] / 2 or fb[1] > m - B['whi'] / 2 or
                                      fb[2] < B['whi'] / 2 or fb[3] > m - B['whi'] / 2)):
            du = du * 4
        if dx >= dy and dx >= du:
            axis = 0
        elif dy >= du:
            axis = 1
        else:
            axis = 2
        l, r = split(box, axis)
        return (axis, self._build(l, depth + 1), self._build(r, depth + 1))


def split(box, axis):
    b = list(box)
    mid = (b[2 * axis] + b[2 * axis + 1]) // 2
    l = b.copy(); r = b.copy()
    l[2 * axis + 1] = mid
    r[2 * axis] = mid
    return tuple(l), tuple(r)



# =============================================================================================
# Leaf optimisation: fewer pivots (coarser regions) and fewer claimed entries, as long as every
# region still reaches W.  Reasons are remapped by transitivity along the chain (a down reason
# moves to the next kept pivot, an up reason to the previous one, with the same lambda: the exact
# box tests are pointwise-true inequalities, so the remapped tests pass too); the mirror re-checks.

def _region_ok(W, ka, kb, w, isT, dA, uA, dB, uB, empt):
    r = np.arange(ka + 1)[:, None]; s_ = np.arange(kb + 1)[:, None]
    CA = ((dA > 0) & (dA <= r)) | (r < uA) | isT
    CB = ((dB > 0) & (dB <= s_)) | (s_ < uB)
    sidx = np.arange(kb + 1)
    for rr in range(ka + 1):
        if rr < ka:
            live = ~(sidx < empt[rr])
        else:
            live = np.ones(kb + 1, dtype=bool)
        if not live.any():
            continue
        tot = np.maximum(CB[live], CA[rr][None, :]).astype(np.int64) @ w
        if tot.min() < W:
            return False
    return True


def optimise_leaf(W, pts, chA, chB, emp, ents):
    ka0, kb0 = len(chA), len(chB)
    w = np.array([pts[k][2] for k, _ in ents], dtype=np.int64)
    isT = np.array([t[0] == 4 for _, t in ents])
    DA = np.array([t[1][0] for _, t in ents]); UA = np.array([t[1][1] for _, t in ents])
    LA = np.array([t[1][2] for _, t in ents])
    DB = np.array([t[2][0] for _, t in ents]); UB = np.array([t[2][1] for _, t in ents])
    LB = np.array([t[2][2] for _, t in ents])
    empt0 = [e for e, _ in emp] + [0] * (ka0 - len(emp))
    elam0 = [l for _, l in emp] + [0] * (ka0 - len(emp))

    def maps(keep, k0):
        """down[i] = new index of the first kept pivot >= i (0 if none); up[i] = new index of the
        last kept pivot <= i (0 if none), for original indices i = 0..k0."""
        import bisect
        down = np.zeros(k0 + 2, dtype=np.int64); up = np.zeros(k0 + 2, dtype=np.int64)
        for i in range(1, k0 + 1):
            j = bisect.bisect_left(keep, i)
            down[i] = j + 1 if j < len(keep) else 0
            up[i] = bisect.bisect_right(keep, i)
        return down, up

    def remap(kA, kB):
        dmA, umA = maps(kA, ka0); dmB, umB = maps(kB, kb0)
        dA = np.where(DA > 0, dmA[DA], 0); uA = umA[UA]
        dB = np.where(DB > 0, dmB[DB], 0); uB = umB[UB]
        empt = [int(umB[empt0[a - 1]]) if kb0 else 0 for a in kA]
        return dA, uA, dB, uB, empt

    keepA = list(range(1, ka0 + 1)); keepB = list(range(1, kb0 + 1))
    alive = np.ones(len(ents), dtype=bool)

    def ok(kA, kB, al):
        dA, uA, dB, uB, empt = remap(kA, kB)
        return _region_ok(W, len(kA), len(kB), np.where(al, w, 0), isT & al,
                          np.where(al, dA, 0), np.where(al, uA, 0), np.where(al, dB, 0),
                          np.where(al, uB, 0), empt)

    assert ok(keepA, keepB, alive)
    for which in ('A', 'B'):
        i = 0
        while True:
            keep = keepA if which == 'A' else keepB
            if i >= len(keep):
                break
            trial = keep[:i] + keep[i + 1:]
            if (ok(trial, keepB, alive) if which == 'A' else ok(keepA, trial, alive)):
                if which == 'A': keepA = trial
                else: keepB = trial
            else:
                i += 1
    dA, uA, dB, uB, empt = remap(keepA, keepB)
    # entries: drop the useless, then greedily the costly
    useful = isT | (dA > 0) | (uA > 0) | (dB > 0) | (uB > 0)
    alive &= useful
    cost = np.where(isT, 1.0, 2.0 + (dA > 0) + (uA > 0) + (dB > 0) + (uB > 0))
    order = sorted(np.nonzero(alive)[0], key=lambda i: (-cost[i] / max(1, w[i]), i))
    for i in order:
        alive[i] = False
        if not ok(keepA, keepB, alive):
            alive[i] = True
    # reasons: drop single reasons that are not needed
    for i in np.nonzero(alive & ~isT)[0]:
        for arr in (dA, uA, dB, uB):
            if arr[i] == 0:
                continue
            old = arr[i]; arr[i] = 0
            if (dA[i] == 0 and uA[i] == 0 and dB[i] == 0 and uB[i] == 0) or not _region_ok(
                    W, len(keepA), len(keepB), np.where(alive, w, 0), isT & alive,
                    np.where(alive, dA, 0), np.where(alive, uA, 0), np.where(alive, dB, 0),
                    np.where(alive, uB, 0), empt):
                arr[i] = old
    newA = [chA[j - 1] for j in keepA]; newB = [chB[j - 1] for j in keepB]
    newemp = []
    for a, e in zip(keepA, empt):
        newemp.append((int(e), int(elam0[a - 1]) if e else 0))
    if not newB:
        newemp = []
    newents = []
    for i in np.nonzero(alive)[0]:
        k, t = ents[i]
        if t[0] == 4:
            newents.append((k, t))
        else:
            ra = (int(dA[i]), int(uA[i]), int(LA[i]) if uA[i] else 0)
            rb = (int(dB[i]), int(uB[i]), int(LB[i]) if uB[i] else 0)
            newents.append((k, (t[0], ra, rb)))
    return newA, newB, newemp, newents

# =============================================================================================
# Lean emission

def near(ctx, box, cands, P):
    x0, x1, y0, y1 = box[:4]
    S, Fr = ctx.S, ctx.F
    return [i for i in cands
            if x0 <= P[i][0] * S + Fr and P[i][0] * S <= x1 + Fr
            and y0 <= P[i][1] * S + Fr and P[i][1] * S <= y1 + Fr]


def claimed(t, memo):
    k = id(t)
    if k in memo:
        return memo[k]
    if t[0] == 'E':
        r = frozenset()
    elif t[0] == 'C':
        r = claimed(t[2], memo)
    elif t[0] == 'Z':
        r = frozenset(k2 for k2, _ in t[5])
    elif t[0] in ('XM', 'YM'):
        r = claimed(t[2], memo) | claimed(t[3], memo)
    else:
        r = claimed(t[1], memo) | claimed(t[2], memo)
    memo[k] = r
    return r


def leaf_cost(t):
    """a rough kernel-cost estimate (arbitrary units ~ ms), for chunking"""
    if t[0] == 'E':
        return 0.2
    _, kind, chA, chB, emp, ents = t
    ka, kb = len(chA), len(chB)
    nT = sum(1 for _, g in ents if g[0] == 4)
    nr = sum((g[1][0] > 0) + (g[1][1] > 0) + (g[2][0] > 0) + (g[2][1] > 0) for _, g in ents if g[0] != 4)
    nc = len(ents) - nT
    return (2.0 + 0.3 * nT + 0.8 * nc + 0.6 * nr + 0.6 * (ka + kb + ka)
            + 0.002 * (ka + 1) * (kb + 1) * len(ents))


def tree_cost(t, memo):
    k = id(t)
    if k in memo:
        return memo[k]
    if t[0] in ('E', 'Z'):
        r = leaf_cost(t)
    elif t[0] == 'C':
        r = 0.1 + tree_cost(t[2], memo)
    elif t[0] in ('XM', 'YM'):
        r = 0.05 + tree_cost(t[2], memo) + tree_cost(t[3], memo)
    else:
        r = 0.05 + tree_cost(t[1], memo) + tree_cost(t[2], memo)
    memo[k] = r
    return r


BASE = 1 << 20


def replay(ctx, t, box, cands, P, fratio, st, out, leaves, cmemo):
    """Structure digits (appended to `out`) and one digit list per Z leaf (appended to `leaves`)
    of subtree `t` checked on `box` with candidate list `cands` (indices into P, increasing), in
    the format of `ZMTree.dec`; every leaf is re-checked with the mirror."""
    B = BASE
    if t[0] == 'E':
        assert empty_ok(ctx, box), box
        out.append(5); st['E'] += 1
        return
    if t[0] == 'C':
        us = t[1]
        assert clip_ok(ctx, box, us), box
        assert us < B * B
        out += [6, us % B, us // B]; st['C'] += 1
        replay(ctx, t[2], box[:5] + (us,), cands, P, fratio, st, out, leaves, cmemo)
        return
    fc = near(ctx, box, cands, P)
    if len(fc) <= fratio * len(cands) and claimed(t, cmemo) <= set(fc):
        out.append(4); st['F'] += 1
        cands = fc
    if t[0] in ('XM', 'YM'):
        _, m, l, r = t
        assert m < B * B
        out += [7 if t[0] == 'XM' else 8, m % B, m // B]
        ax = 0 if t[0] == 'XM' else 1
        lb = list(box); rb = list(box)
        lb[2 * ax + 1] = m; rb[2 * ax] = m
        replay(ctx, l, tuple(lb), cands, P, fratio, st, out, leaves, cmemo)
        replay(ctx, r, tuple(rb), cands, P, fratio, st, out, leaves, cmemo)
        return
    if t[0] == 'Z':
        _, kind, chA, chB, emp, ents = t
        pos = {k: j for j, k in enumerate(cands)}
        items = sorted((pos[k], tag) for k, tag in ents)
        leaf = Leaf([], chA, chB, emp)
        prev = -1
        for j, tag in items:
            leaf.ents.append((j - prev - 1, tag)); prev = j
        assert leaf_ok(ctx, box, [P[i] for i in cands], leaf), ("mirror rejects leaf", box)
        d = [len(leaf.ents)]
        for g, tag in leaf.ents:
            assert 8 * g + tag[0] < B
            d.append(8 * g + tag[0])
            if tag[0] < 4:
                for (dd, uu, ll) in (tag[1], tag[2]):
                    assert dd < 256 and uu < 256 and ll < 4
                    d.append(dd + 256 * uu + 65536 * ll)
        for ch in (chA, chB):
            d.append(len(ch))
            for X, Y, k in ch:
                assert X < 16384 and k < 4 and Y < B
                d += [X + 16384 * k, Y]
        d.append(len(emp))
        for e, l in emp:
            assert e < 256 and l < 4
            d.append(e + 256 * l)
        out.append(0)
        leaves.append(d)
        st['Z'] += 1
        st[kind] = st.get(kind, 0) + 1
        return
    axis, l, r = t
    out.append(1 + axis)
    lb, rb = split(box, axis)
    replay(ctx, l, lb, cands, P, fratio, st, out, leaves, cmemo)
    replay(ctx, r, rb, cands, P, fratio, st, out, leaves, cmemo)


def encode(digits, B):
    n = 0
    for d in reversed(digits):
        assert 0 <= d < B
        n = n * B + d
    return n


def emit_ptree(P):
    def b(lo, hi):
        if lo >= hi:
            return '.leaf'
        mid = (lo + hi) // 2
        x, y, w = P[mid]
        return f"(.node {b(lo, mid)} {x} {y} {w} {b(mid + 1, hi)})"
    return b(0, len(P))


HDR = "set_option linter.style.longLine false\n"
FUEL = 128


def emit(args, sha, s, D, W, P, ctx, trees, cells, ubins, Mq, M):
    name, outdir = args.name, args.outdir
    os.makedirs(outdir, exist_ok=True)
    mod = outdir.rstrip('/').replace('lean/', '', 1).replace('/', '.')
    R = ctx.R
    Um = R // 2
    half = M - M // 2
    width = half // cells
    covT = f"Cov {D} {ctx.S} {Mq} {R} {W} ptsL"
    cmemo, kmemo = {}, {}
    chunks = []          # (tree, box)
    budget = args.chunk_cost

    def skel(t, box):
        if tree_cost(t, kmemo) <= budget or t[0] in ('E', 'Z'):
            chunks.append((t, box))
            return f"ok{len(chunks) - 1}"
        if t[0] == 'C':
            nb = box[:5] + (t[1],)
            return (f"(ZMTree.C_cov (by norm_num) (by norm_num) (by norm_num) (by decide +kernel) "
                    f"{skel(t[2], nb)})")
        if t[0] in ('XM', 'YM'):
            _, m, l, r = t
            ax = 0 if t[0] == 'XM' else 1
            lb = list(box); rb = list(box)
            lb[2 * ax + 1] = m; rb[2 * ax] = m
            return f"(Cov.split{'XY'[ax]} {m} {skel(l, tuple(lb))} {skel(r, tuple(rb))})"
        axis, l, r = t
        lb, rb = split(box, axis)
        return f"(Cov.split{'XYU'[axis]} {lb[2 * axis + 1]} {skel(l, lb)} {skel(r, rb)})"

    # the whole region as one tree: the cell grid by explicit splits (x-cells, then y-cells,
    # balanced), then the cell trees
    def gx(i0, i1):
        if i1 - i0 == 1:
            return gy(i0, 0, cells)
        m = (i0 + i1) // 2
        return ('XM', m * width, gx(i0, m), gx(m, i1))

    def gy(i, j0, j1):
        if j1 - j0 == 1:
            return trees[(i * width, (i + 1) * width, j0 * width, (j0 + 1) * width, 0, Um)]
        m = (j0 + j1) // 2
        return ('YM', m * width, gy(i, j0, m), gy(i, m, j1))

    root = (0, half, 0, half, 0, Um)
    proof = skel(gx(0, cells), root)
    ns = f"SquarePacking.{name}"
    doc = (f"/-!\n# `{name}`: certificate points (generated by `lean/scripts/gen_zmtree.py`; do not edit)\n\n"
           f"From `{args.cert}`, sha256 `{sha}`:\n{len(P)} points `(X/{D}, Y/{D})` with weights `w/{W}`, "
           f"container `[0, {Mq}/{D}]²`.\n-/\n")
    L = ["import Sqpack.ZMTree\n", HDR, doc, f"namespace {ns}\n", "open BoxTree\n",
         "-- large certificates (s(32): 13,085 points) need more than the default recursion depth",
         "set_option maxRecDepth 100000 in",
         "/-- The certificate points `(X, Y, w)`, in a search tree on `(X, Y)`. -/",
         f"def pts : PTree :=\n  {emit_ptree(P)}\n",
         "theorem pts_nodup : pts.toList.Nodup :=\n  PTree.nodup_of_chainB _ (by decide +kernel)\n",
         f"theorem pts_d4 : d4Check {Mq} pts = true := by decide +kernel\n",
         f"theorem pts_wsum : pts.wsum = {sum(w for _, _, w in P)} := by decide +kernel\n",
         "-- a long list literal: elaboration needs more than the default heartbeats\n"
         "set_option maxRecDepth 100000 in\nset_option maxHeartbeats 0 in\n"
         "/-- The same entries as a list literal (the chunks use it: "
         "`pts.toList` costs a kernel evaluation per declaration). -/",
         "def ptsL : List (ℕ × ℕ × ℕ) :=\n  [" + ",\n   ".join(f"({x}, {y}, {w})" for x, y, w in P) + "]\n",
         "set_option maxRecDepth 100000 in\ntheorem pts_toList : pts.toList = ptsL := by decide +kernel\n",
         "theorem ptsL_nodup : ptsL.Nodup := pts_toList ▸ pts_nodup\n",
         f"end {ns}\n"]
    open(f"{outdir}/Pts.lean", 'w').write("\n".join(L))
    # digit streams
    st = dict(F=0, C=0, E=0, Z=0, digits=0)
    streams = []
    B = BASE
    for t, box in chunks:
        out, lv = [], []
        replay(ctx, t, box, list(range(len(P))), P, args.fratio, st, out, lv, cmemo)
        streams.append((out, lv))
    # parts, balanced by cost
    costs = [tree_cost(t, kmemo) for t, _ in chunks]
    total = sum(costs)
    nparts = args.parts
    parts = [[] for _ in range(nparts)]
    loads = [0.0] * nparts
    for i in sorted(range(len(chunks)), key=lambda i: -costs[i]):
        j = min(range(nparts), key=lambda j: loads[j])
        parts[j].append(i); loads[j] += costs[i]
    for pi, idxs in enumerate(parts):
        idxs.sort()
        L = [f"import {mod}.Pts\n", HDR,
             f"/-!\n# `{name}`: zero-margin box-tree chunks (generated; do not edit)\n\n"
             f"Each `okI` is one kernel evaluation (`decide +kernel`) of `ZMTree.check` on one subtree.\n-/\n",
             f"namespace {ns}\n", "open BoxTree ZMTree\n"]
        for i in idxs:
            t, box = chunks[i]
            bx = ' '.join(map(str, box))
            out, lv = streams[i]
            code = encode(out, B)
            nd = len(out) + sum(len(x) for x in lv)
            st['digits'] += nd
            L.append(f"/-- Chunk {i}: {len(lv)} `Z` leaves, {nd} base-2^20 digits, est. cost {costs[i]:.0f}. -/")
            L.append(f"def c{i} : ℕ :=\n  0x{code:x}\n")
            lits = ",\n   ".join(f"0x{encode(x, B):x}" for x in lv)
            L.append(f"def d{i} : List ℕ :=\n  [{lits}]\n")
            L.append(f"theorem ok{i} : {covT} {bx} :=\n"
                     f"  ZMTree.sound {D} {ctx.S} {Mq} {R} {W} {ctx.F} ptsL (by norm_num) (by norm_num) "
                     f"(by norm_num) ptsL_nodup (ZMTree.dec {B} {FUEL} c{i} d{i}).1 {bx} ptsL\n"
                     f"    (List.Sublist.refl _) (by decide +kernel)\n")
        L.append(f"end {ns}\n")
        open(f"{outdir}/Part{pi}.lean", 'w').write("\n".join(L))
    imports = "\n".join(f"import {mod}.Part{pi}" for pi in range(nparts))
    L = [imports + "\n", HDR,
         f"/-!\n# `{name}`: the zero-margin box tree covers the D4 fundamental region (generated; do not edit)\n\n"
         f"{st['Z']} `Z` leaves, {st['E']} `E` leaves, {st['C']} clips, in {len(chunks)} chunks, {nparts} files;\n"
         f"spatial scale `Q = {D}·{ctx.S}`, angle `u = U/{R}`, root `u ∈ [0, {Um}/{R}]`, "
         f"{cells}×{cells} root cells.\n-/\n",
         f"namespace {ns}\n", "open BoxTree\n",
         "/-- The box tree covers the D4 fundamental region, for the list literal `ptsL`. -/",
         f"theorem cov_rootL : {covT} {' '.join(map(str, root))} :=\n  {proof}\n",
         "/-- **The zero-margin box tree covers the D4 fundamental region** (stated for `pts.toList`). -/",
         f"theorem cov_root : Cov {D} {ctx.S} {Mq} {R} {W} pts.toList {' '.join(map(str, root))} := by\n"
         f"  rw [pts_toList]; exact cov_rootL\n",
         f"end {ns}\n"]
    open(f"{outdir}/Cov.lean", 'w').write("\n".join(L))
    print(f"wrote {outdir}: {len(chunks)} chunks in {nparts} parts, {st}, total est. cost {total:.0f}",
          file=sys.stderr)


# =============================================================================================
# driver

_SEARCH = None


def roots_of(ctx, M, pitch_cells, ubins):
    """Root cells: the D4 region [0, M/2]^2 cut into pitch_cells^2 cells; each root is a cell with
    the whole u range [0, R/2] (the ubins bins are the first levels of its tree)."""
    half = M // 2
    assert half % pitch_cells == 0
    w = half // pitch_cells
    return [(i * w, (i + 1) * w, j * w, (j + 1) * w, 0, ctx.R // 2)
            for i in range(pitch_cells) for j in range(pitch_cells)]


def ubin_tree(search, root, ubins):
    """A root cell's tree: `ubins` u-bins by midpoint U splits, each searched."""
    def rec(box, n):
        if n == 1:
            return search._build(box, 0)
        l, r = split(box, 2)
        return (2, rec(l, n // 2), rec(r, n // 2))
    return rec(root, ubins)


def _work_cell(root):
    t0 = time.process_time()
    for k in _SEARCH.stat:
        _SEARCH.stat[k] = 0
    tree = ubin_tree(_SEARCH, root, _SEARCH.ubins)
    return root, tree, dict(_SEARCH.stat), time.process_time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cert')
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--K', type=int, default=12)
    ap.add_argument('--J', type=int, default=32)
    ap.add_argument('--pitch', default='1/10')
    ap.add_argument('--ubins', type=int, default=8)
    ap.add_argument('--nproc', type=int, default=4)
    ap.add_argument('--only', type=int, default=None, help='only the first N root cells (testing)')
    ap.add_argument('--name')
    ap.add_argument('--outdir')
    ap.add_argument('--save', help='pickle the trees here')
    ap.add_argument('--load', help='load the trees from this pickle instead of searching')
    ap.add_argument('--chunk-cost', type=float, default=6000.0)
    ap.add_argument('--parts', type=int, default=4)
    ap.add_argument('--fratio', type=float, default=0.85)
    args = ap.parse_args()
    sha, s, D, W, pts = read_cert(args.cert)
    assert sum(w for _, _, w in pts) < args.n * W
    S = 2 ** args.K; Q = D * S
    Mq = s * D
    assert Mq.denominator == 1
    Mq = int(Mq); M = Mq * S
    R = 2 ** args.J
    ctx = Ctx(S, Q, R, W, 3 * Q // 4)
    pitch = F(args.pitch)
    cells = (s / 2) / pitch
    assert cells.denominator == 1
    cells = int(cells)
    global _SEARCH
    P = sorted(pts)
    if args.load:
        import pickle
        dd = pickle.load(open(args.load, 'rb'))
        trees = dd['trees']
        assert dd['sha'] == sha
    else:
        _SEARCH = Search(ctx, D, W, P, s)
        _SEARCH.ubins = args.ubins
        roots = roots_of(ctx, M, cells, args.ubins)
        if args.only:
            roots = roots[:args.only]
        t0 = time.time()
        import multiprocessing as mp
        tot = {}
        trees = {}
        cpu = 0.0
        with mp.get_context('fork').Pool(args.nproc) as pool:
            for i, (root, tree, st, c) in enumerate(pool.imap_unordered(_work_cell, roots, chunksize=1)):
                trees[root] = tree
                cpu += c
                for k, v in st.items():
                    tot[k] = max(tot.get(k, 0), v) if k == 'maxdepth' else tot.get(k, 0) + v
                if (i + 1) % 50 == 0:
                    print(f"  {i+1}/{len(roots)} cells {time.time()-t0:.0f}s", file=sys.stderr, flush=True)
        print(f"search done: {time.time()-t0:.0f}s wall, {cpu:.0f}s cpu; {tot}", file=sys.stderr)
        if args.save:
            import pickle
            pickle.dump(dict(trees=trees, sha=sha, stat=tot), open(args.save, 'wb'))
    if args.outdir:
        emit(args, sha, s, D, W, P, ctx, trees, cells, args.ubins, Mq, M)


if __name__ == '__main__':
    main()
