#!/usr/bin/env python3
"""Build a zero-margin pose-space tree for a MIXED cover (points + axis-parallel segments) and emit it as
Lean data for the kernel checker `Sqpack/ZMTreeM.lean` (see `lean/LADDER.md`, `notes/lean-segments.md`).

Usage (from s12/):
  python3 lean/scripts/gen_zmmtree.py COVER --n N --name NAME --outdir lean/Sqpack/NAME
          [--K 12] [--J 32] [--pitch 1/10] [--ubins 8] [--nproc 4] [--parts 4] [--depth 30]
          [--only N] [--cells i,j;...] [--census-only] [--no-thr]

The oracle is `search/zm_mixed.py` (read-only): its Lemma S intervals (`line_cond_iv`, the hull over
zeromargin's bound choices of the Bernstein intervals) and its Lemma T group selection.  Every piece of
the certificate is then rebuilt in the integer terms of the Lean leaf and re-checked by `pc_ok`, an exact
mirror of `ZMTreeM.pcOk` / `pcVal`:

* S-block (Lemma S): the line's certified core J4 rounded inward to the 1/Q grid; both ends checked with
  the mirror of `ZMTree.admAll` (all four conditions) and shrunk if needed;
* T-group (Lemma T, germ pair): J3 of both lines (three conditions each) rounded inward and checked,
  optional singular points tau, and a greedy monotone coupling of the two lines' masses (pairs
  `c <= a + u0`, `d <= b + u0`), rounded to the grid; its value is the matched mass.  By max-flow/min-cut
  on the line this is zm_mixed's min_T f(T) up to rounding.

Lemma L / L' / V and SPLIT (Lemma R) are not in the Lean leaf yet: the search uses only S and T (the
zm_mixed piece bound WITHOUT Lemma L is what a Lean leaf can certify).  Points (if any) go to the
ZMTree point leaf of `gen_zmtree.py` with the target weight W - Lp (Lemma P).

Nothing in this script is trusted: the Lean kernel re-checks every leaf (`ZMTreeM.soundM`).
"""
import argparse
import hashlib
import math
import os
import sys
import time
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'search'))
import gen_zmtree as G  # noqa: E402  (the point-leaf mirror and search; read-only use)
import zeromargin as zm  # noqa: E402
import zm_mixed as ZX  # noqa: E402
import mixed_cover as MC  # noqa: E402
import lblock as LB  # noqa: E402

sys.setrecursionlimit(100000)
BASE = G.BASE


# =============================================================================================
# exact mirror of ZMTreeM.pcOk / pcVal

def admall(ctx, kp, XS, YS, box):
    """ZMTree.admAll (the admK conjunction; ptOkK is a fast path implying it)."""
    return all(G.admk(ctx, k, XS, YS, box) for k in range(4) if k != kp)


def lx(d, K, t):
    return K if d == 0 else t


def ly(d, K, t):
    return t if d == 0 else K


def on_line(S, d, K, e):
    X0, Y0, X1, Y1, _ = e
    if d == 0:
        return X0 == X1 and X0 * S == K and Y0 < Y1
    return Y0 == Y1 and Y0 * S == K and X0 < X1


def slo(S, d, e):
    return (e[1] if d == 0 else e[0]) * S


def shi(S, d, e):
    return (e[3] if d == 0 else e[2]) * S


def kU(d):
    return 1 if d == 0 else 2


def kD(d):
    return 0 if d == 0 else 3


def lnU(Q, d, K):
    return K if d == 0 else K + Q


def lnD(Q, d, K):
    return K + Q if d == 0 else K


def sclaim(sc, cands):
    out = []
    pos = 0
    for gap, tag in sc:
        pos += gap
        if pos >= len(cands):
            return None
        out.append((cands[pos], tag))
        pos += 1
    return out


def sblk_ok(ctx, box, b):
    d, K, A, B = b
    return A <= B and admall(ctx, 4, lx(d, K, A), ly(d, K, A), box) and admall(ctx, 4, lx(d, K, B), ly(d, K, B), box)


def sval(S, b, e):
    d, K, A, B = b
    ov = min(shi(S, d, e), B) - max(slo(S, d, e), A)
    return (e[4] * max(ov, 0)) // (shi(S, d, e) - slo(S, d, e))


def piece_ok(S, d, L, lo, hi, tag, cls, j1, a, b, m):
    j = j1 - 1
    if not (0 <= j < len(cls)):
        return False
    e, t = cls[j]
    return (t == tag and on_line(S, d, L, e) and slo(S, d, e) <= a and b <= shi(S, d, e) and lo <= a and b <= hi
            and m * (shi(S, d, e) - slo(S, d, e)) <= e[4] * (b - a))


def tgrp_ends(ctx, box, g):
    d, K, Au, Bu, Ad, Bd, tu1, td1, prs = g
    Q = ctx.Q
    U, Dn = lnU(Q, d, K), lnD(Q, d, K)
    if not (Au <= Bu and Ad <= Bd):
        return False
    if not (admall(ctx, kU(d), lx(d, U, Au), ly(d, U, Au), box) and admall(ctx, kU(d), lx(d, U, Bu), ly(d, U, Bu), box)):
        return False
    if not (admall(ctx, kD(d), lx(d, Dn, Ad), ly(d, Dn, Ad), box) and admall(ctx, kD(d), lx(d, Dn, Bd), ly(d, Dn, Bd), box)):
        return False
    if tu1 and not G.admk(ctx, kU(d), lx(d, U, tu1 - 1), ly(d, U, tu1 - 1), box):
        return False
    if td1 and not G.admk(ctx, kD(d), lx(d, Dn, td1 - 1), ly(d, Dn, td1 - 1), box):
        return False
    return True


def tpr_ok(ctx, box, cls, tag, g, p):
    S, Q, R = ctx.S, ctx.Q, ctx.R
    U0 = box[4]
    d, K, Au, Bu, Ad, Bd, tu1, td1, _ = g
    ju1, a, b, jd1, c, dd, m = p
    if not (a <= b and c <= dd):
        return False
    if ju1 and not piece_ok(S, d, lnU(Q, d, K), Au, Bu, tag, cls, ju1, a, b, m):
        return False
    if jd1 and not piece_ok(S, d, lnD(Q, d, K), Ad, Bd, tag, cls, jd1, c, dd, m):
        return False
    if ju1 == 0:
        if jd1 == 0:
            return m == 0
        return td1 != 0 and dd <= td1 - 1
    if jd1 == 0:
        return tu1 != 0 and tu1 - 1 <= a
    return c * R <= a * R + U0 * Q and dd * R <= b * R + U0 * Q


def tchain(prs):
    return all(p[2] <= q[1] and p[5] <= q[4] for p, q in zip(prs, prs[1:]))


def lnums(lb):
    out = []
    for (lines, corners, lg) in lb:
        out.append(lg)
        for l in lines:
            out += [l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[9]]
            for z in (l[11], l[12], l[13]):
                for p in z:
                    out += list(p)
        for c in corners:
            for x in c:
                out += list(x)
    return out


def pc_value(ctx, box, cls, sb, tg, lb=()):
    """(ok, value): the exact mirror of pcOkX and pcValX (ZMTreeX.lean) on the decoded claims."""
    S = ctx.S
    if any(x < 0 for x in lnums(lb)):
        return False, 0
    ok, val = pc_value_st(ctx, box, cls, sb, tg)
    if not ok:
        return False, 0
    for li, B in enumerate(lb):
        tag = 2 * (len(tg) + li) + 1
        if not LB.lblk_ok(ctx, box, cls, tag, B):
            return False, 0
        val += LB.lblk_val(ctx, cls, B)
    return True, val


def pc_value_st(ctx, box, cls, sb, tg):
    """the S-block and T-group part (ZMTreeM.pcOk / pcVal)."""
    S = ctx.S
    nums = [x for b in sb for x in b] + [x for g in tg for x in g[:8]] + \
        [x for g in tg for p in g[8] for x in p] + [t for _, t in cls]
    if any(x < 0 for x in nums):          # the Lean data are natural numbers
        return False, 0
    for b in sb:
        if not sblk_ok(ctx, box, b):
            return False, 0
    val = 0
    for e, t in cls:
        if t % 2 == 0:
            s = t // 2
            if s >= len(sb) or not on_line(S, sb[s][0], sb[s][1], e):
                return False, 0
            val += sval(S, sb[s], e)
    for gi, g in enumerate(tg):
        if not tgrp_ends(ctx, box, g):
            return False, 0
        tag = 2 * gi + 1
        if not all(tpr_ok(ctx, box, cls, tag, g, p) for p in g[8]) or not tchain(g[8]):
            return False, 0
        val += sum(p[6] for p in g[8])
    return True, val


# =============================================================================================
# building the piece certificate of a box

def ceil_div(a, b):
    return -((-a) // b)


class Pieces:
    """Per-cover data: segments (normalised, sorted = the Lean list), lines, the zm_mixed Cover."""

    def __init__(self, ctx, cov, segs):
        self.ctx = ctx
        self.cov = cov                     # zm_mixed.Cover
        self.segs = segs                   # sorted normalised integer entries
        self.idx = {e: i for i, e in enumerate(segs)}
        S = ctx.S
        self.lines = {}                    # (d, K) -> list of segment indices (sorted by position)
        for i, e in enumerate(segs):
            X0, Y0, X1, Y1, w = e
            if X0 == X1:
                key = (0, X0 * S)
            elif Y0 == Y1:
                key = (1, Y0 * S)
            else:
                raise ValueError("only axis-parallel segments are supported")
            self.lines.setdefault(key, []).append(i)
        for k in self.lines:
            self.lines[k].sort(key=lambda i: slo(S, k[0], segs[i]))
        # zm_mixed's line keys
        self.zkey = {}
        for (d, K) in self.lines:
            v = F(K, ctx.Q)
            self.zkey[(d, K)] = ('V', v) if d == 0 else ('H', v)

    def seg_range(self, key):
        S = self.ctx.S
        d = key[0]
        ii = self.lines[key]
        return min(slo(S, d, self.segs[i]) for i in ii), max(shi(S, d, self.segs[i]) for i in ii)


def iv_round_in(iv, lo_def, hi_def, Q):
    """An interval of real line coordinates (Fractions or None ends) to an integer interval over Q,
    rounded inward and clipped to [lo_def, hi_def]; None if empty."""
    if iv is None:
        return None
    lo = lo_def if iv[0] is None else max(lo_def, ceil_div(iv[0].numerator * Q, iv[0].denominator))
    hi = hi_def if iv[1] is None else min(hi_def, (iv[1].numerator * Q) // iv[1].denominator)
    if lo > hi:
        return None
    return lo, hi


def certify_interval(ctx, box, kp, d, L, lo, hi, steps=48):
    """Shrink [lo, hi] until both ends pass admall(kp); returns (lo, hi) or None."""
    def ok(t):
        return admall(ctx, kp, lx(d, L, t), ly(d, L, t), box)
    if lo > hi:
        return None
    if not ok(lo):
        # the set passing is (near) convex: bisect towards hi for the first passing point
        if not ok(hi):
            mid = (lo + hi) // 2
            if not ok(mid):
                return None
            a, b = lo, mid
        else:
            a, b = lo, hi
        for _ in range(steps):
            if b - a <= 1:
                break
            c = (a + b) // 2
            if ok(c):
                b = c
            else:
                a = c
        lo = b
    if not ok(hi):
        a, b = lo, hi          # ok(lo), not ok(hi)
        for _ in range(steps):
            if b - a <= 1:
                break
            c = (a + b) // 2
            if ok(c):
                a = c
            else:
                b = c
        hi = a
    if lo > hi or not ok(lo) or not ok(hi):
        return None
    return lo, hi


def couple(up, dn, delta):
    """Greedy monotone coupling (FIFO) of up pieces [(lo, hi, rho, seg)] and down pieces with the constraint
    down position <= up position + delta (positions as Fractions over Q, rho = mass per unit).
    Returns pairs (su, a, b, sd, c, d, mass) with c <= a + delta, d <= b + delta, mass <= both masses."""
    pairs = []
    i = j = 0
    s = up[0][0] if up else None
    t = dn[0][0] if dn else None
    while i < len(up) and j < len(dn):
        ulo, uhi, ru, su = up[i]
        dlo, dhi, rd, sd = dn[j]
        if s < ulo:
            s = ulo
        if t < dlo:
            t = dlo
        if s >= uhi:
            i += 1
            continue
        if t >= dhi:
            j += 1
            continue
        if ru == 0:
            i += 1
            continue
        if rd == 0:
            j += 1
            continue
        if t > s + delta:
            # skip up mass until the down position is reachable
            s = min(t - delta, uhi)
            continue
        mu = min(ru * (uhi - s), rd * (dhi - t))
        s2 = s + mu / ru
        t2 = t + mu / rd
        if t2 <= s2 + delta:
            pairs.append((su, s, s2, sd, t, t2, mu))
            s, t = s2, t2
            continue
        # the down side would overtake: match up to the binding point, then at the down rate
        if t < s + delta:
            lam = (s + delta - t) / (1 / rd - 1 / ru)
            s2 = s + lam / ru
            t2 = t + lam / rd
            pairs.append((su, s, s2, sd, t, t2, lam))
            s, t = s2, t2
        # binding: t = s + delta, rd < ru: pair [s, s + ds] with [t, t + ds], mass rd * ds
        ds = min(uhi - s, dhi - t)
        pairs.append((su, s, s + ds, sd, t, t + ds, rd * ds))
        s, t = s + ds, t + ds
    return pairs


class Builder:
    """The piece certificate of one box: S-blocks for lines not in a germ group, T-groups for germ pairs."""

    def __init__(self, P, mchk, use_thr=True, use_lin=True):
        self.P = P
        self.mchk = mchk              # zm_mixed.MixedChecker (oracle: specs and intervals)
        self.use_thr = use_thr
        self.use_lin = use_lin

    def build(self, box):
        """returns (sc, sb, tg, value) with sc the claims as (segment index, tag), or None."""
        P, ctx = self.P, self.P.ctx
        Q, S, R = ctx.Q, ctx.S, ctx.R
        x0, x1, y0, y1, U0, U1 = box
        fb = (F(x0, Q), F(x1, Q), F(y0, Q), F(y1, Q), F(U0, R), F(U1, R))
        cx0, cx1, cy0, cy1, u0, u1 = fb
        B = zm.bin_data(u0, u1)
        zc = self.mchk.zc
        specs = zc._adm_specs(fb, B)
        h = u1 - u0
        m = self.mchk.m
        cxm, cym = float(cx0 + cx1) / 2, float(cy0 + cy1) / 2
        Rr = 0.7072 + 0.5 * math.hypot(float(cx1 - cx0), float(cy1 - cy0)) + 1e-9
        cov = P.cov

        def near(key):
            d, K = key
            v = K / Q
            lo, hi = P.seg_range(key)
            dist = abs(v - (cxm if d == 0 else cym))
            if dist > Rr:
                return False
            other = cym if d == 0 else cxm
            half = math.sqrt(max(Rr * Rr - dist * dist, 0.0))
            return not (other + half < lo / Q or other - half > hi / Q)

        ivc = {}

        def ivs(key):
            if key not in ivc:
                L = cov.lines[P.zkey[key]]
                ivc[key] = [ZX.line_cond_iv(L['P0'], L['d'], specs, c, u0, h, m) for c in range(4)]
            return ivc[key]

        def interval(key, kp):
            """the certified interval (conditions != kp) of a line, as integers over Q."""
            I = ivs(key)
            J = (None, None)
            for c in range(4):
                if c != kp:
                    J = ZX.iv_and(J, I[c])
            lo, hi = P.seg_range(key)
            r = iv_round_in(J, lo, hi, Q)
            if r is None:
                return None
            return certify_interval(ctx, box, kp, key[0], key[1], r[0], r[1])

        near_keys = [k for k in P.lines if near(k)]
        used = set()
        groups = []
        if self.use_thr:
            for d in (0, 1):
                cm = cxm if d == 0 else cym
                cands = set()
                for (dd, K) in near_keys:
                    if dd != d:
                        continue
                    fv = K / Q
                    if d == 0:
                        if abs(fv + 0.5 - cm) <= 0.3: cands.add(K)          # up line x = xi
                        if abs(fv - 0.5 - cm) <= 0.3: cands.add(K - Q)      # down line x = xi + 1
                    else:
                        if abs(fv - 0.5 - cm) <= 0.3: cands.add(K - Q)      # up line y = eta + 1
                        if abs(fv + 0.5 - cm) <= 0.3: cands.add(K)          # down line y = eta
                for K in sorted(cands):
                    ku, kd = (d, lnU(Q, d, K)), (d, lnD(Q, d, K))
                    if ku in used or kd in used or ku not in P.lines or kd not in P.lines:
                        continue
                    if ku not in near_keys or kd not in near_keys:
                        continue
                    groups.append((d, K))
                    used.add(ku); used.add(kd)
        self._ctxd = dict(fb=fb, specs=specs, B=B, ivs=ivs, interval=interval, near_keys=near_keys)
        best = None
        cands = [('T', groups)]
        if self.use_lin:
            cands += [('L', []), ('TL', groups)]
        for mode, grps in cands:
            r = self._assemble(box, mode, grps, interval, ivs, near_keys)
            if r is not None and (best is None or r[4] > best[4]):
                best = r
        return best

    def _assemble(self, box, mode, groups, interval, ivs, near_keys):
        P, ctx = self.P, self.P.ctx
        Q, S, R = ctx.Q, ctx.S, ctx.R
        used = set()
        sb, tg, claims = [], [], []    # claims: (segment index, tag)
        lbk = []
        # T-groups
        for gi, (d, K) in enumerate(groups if mode in ('T', 'TL') else []):
            r = self._group(box, d, K, interval, ivs, len(tg))
            if r is None:
                continue
            g, cl = r
            used.add((d, lnU(Q, d, K))); used.add((d, lnD(Q, d, K)))
            tag = 2 * len(tg) + 1
            tg.append(g)
            claims += [(i, tag) for i in cl]
        # the L-block (one, jointly over its lines)
        if mode in ('L', 'TL'):
            keys = [k for k in near_keys if k not in used]
            r = self._lblock(box, keys, ivs)
            if r is not None:
                lines, segi, lkeys = r
                tagL = 2 * len(tg) + 1
                claims += [(i, tagL) for i in segi]
                for k in lkeys:
                    used.add(k)
                lbk.append(lines)
        # S-blocks
        for key in near_keys:
            if key in used:
                continue
            iv = interval(key, 4)
            if iv is None:
                continue
            A, Bv = iv
            if A >= Bv:
                continue
            s = len(sb)
            segi = [i for i in P.lines[key] if min(shi(S, key[0], P.segs[i]), Bv) > max(slo(S, key[0], P.segs[i]), A)]
            if not segi:
                continue
            sb.append((key[0], key[1], A, Bv))
            claims += [(i, 2 * s) for i in segi]
        claims.sort()
        assert len(set(i for i, _ in claims)) == len(claims), "a segment in two blocks"
        # renumber the pieces' claim indices (the groups were built with segment indices)
        pos = {i: k for k, (i, _) in enumerate(claims)}
        tg2 = []
        for (d, K, Au, Bu, Ad, Bd, tu1, td1, prs) in tg:
            prs2 = [((pos[ju] + 1) if ju is not None else 0, a, b, (pos[jd] + 1) if jd is not None else 0, c, dd, mm)
                    for (ju, a, b, jd, c, dd, mm) in prs]
            tg2.append((d, K, Au, Bu, Ad, Bd, tu1, td1, prs2))
        cls = [(P.segs[i], t) for i, t in claims]
        lb2 = []
        for (lines, rest) in lbk:
            def rn(pcs):
                return [(pos[i] + 1, lo, hi) for (i, lo, hi) in pcs]
            lines2 = [l[:11] + (rn(l[11]), rn(l[12]), rn(l[13])) for l in lines]
            B = self._finish_lblock(box, cls, lines2, len(tg2) + len(lb2))
            if B is not None:
                lb2.append(B)
            else:
                # the block did not certify: its segments' claims stay, with no value (harmless)
                pass
        ok, val = pc_value(ctx, box, cls, sb, tg2, lb2)
        if not ok:
            raise AssertionError(("piece certificate rejected by the mirror", box, mode))
        return claims, sb, tg2, lb2, val

    def _lblock(self, box, keys, ivs):
        """the lines of an L-block (Lemma L data from zm_mixed.lemma_l_data, rebuilt on the grid), their
        segment indices, their keys; corners and lg are computed after the claims are numbered."""
        P, ctx = self.P, self.P.ctx
        Q, S, R = ctx.Q, ctx.S, ctx.R
        x0, x1, y0, y1, U0, U1 = box
        fb = self._ctxd['fb']
        cov = P.cov
        lines, segi, lkeys = [], [], []
        for key in sorted(keys):
            d, K = key
            zk = P.zkey[key]
            L = cov.lines[zk]
            I = ivs(key)
            lo_f, hi_f = P.seg_range(key)
            w = (lo_f / Q - 1.0, hi_f / Q + 1.0)
            dat = ZX.lemma_l_data(L, zk, I, w, fb, self.mchk.m)
            if dat is None or dat.get('vertex'):
                continue
            roles = sum(4 ** k * 1 for k in dat['up']) + sum(4 ** k * 2 for k in dat['lo'])
            if not LB.roles_ok(R, U0, U1, d, roles):
                continue
            a = (dat['a_up'].numerator * Q) // dat['a_up'].denominator
            b = ceil_div(dat['b_lo'].numerator * Q, dat['b_lo'].denominator)
            ok = False
            for _ in range(8):
                if all(G.admk(ctx, k, lx(d, K, a), ly(d, K, a), box) for k in dat['up']):
                    ok = True
                    break
                a -= 1
            if not ok:
                continue
            ok = False
            for _ in range(8):
                if all(G.admk(ctx, k, lx(d, K, b), ly(d, K, b), box) for k in dat['lo']):
                    ok = True
                    break
                b += 1
            if not ok or b > a:
                continue
            top = ((dat['a_up'] + dat['Dup']).numerator * Q) // (dat['a_up'] + dat['Dup']).denominator
            bot = ceil_div((dat['b_lo'] - dat['Dlo']).numerator * Q, (dat['b_lo'] - dat['Dlo']).denominator)
            top, bot = max(top, a), min(max(bot, 0), b)
            unt = [k for k in range(4) if k not in dat['up'] and k not in dat['lo']]

            def unt_ok(t):
                return all(G.admk(ctx, k, lx(d, K, t), ly(d, K, t), box) for k in unt)
            while top > a and not unt_ok(top):
                top = a + (top - a) // 2
            while bot < b and not unt_ok(bot):
                bot = b - (b - bot) // 2
            if not (unt_ok(top) and unt_ok(bot)):
                continue
            du, dd = top - a, b - bot
            up, core, dn = [], [], []
            for i in P.lines[key]:
                e = P.segs[i]
                s0, s1 = slo(S, d, e), shi(S, d, e)
                for (zl, zh, dst) in ((b - dd, b, dn), (b, a, core), (a, a + du, up)):
                    lo, hi = max(s0, zl), min(s1, zh)
                    if hi > lo:
                        dst.append((i, lo, hi))
            if not (up or core or dn):
                continue
            # the minorants of the two gains (fine units), steered by the chord ends at the box centre
            cxm, cym = float(fb[0] + fb[1]) / 2, float(fb[2] + fb[3]) / 2
            um = max(float(fb[4] + fb[5]) / 2, 1e-9)
            fam = 'V' if d == 0 else 'H'
            xu = (min(ZX._tk_float(fam, k, zk[1], cxm, cym, um) for k in dat['up']) - float(dat['a_up'])) * Q \
                if dat['up'] else float(du)
            xl = (float(dat['b_lo']) - max(ZX._tk_float(fam, k, zk[1], cxm, cym, um) for k in dat['lo'])) * Q \
                if dat['lo'] else float(dd)

            def rho_seg(i):
                e = P.segs[i]
                return (e[4] * Q) // (shi(S, d, e) - slo(S, d, e))
            offu = [(rho_seg(i), lo - a, hi - a) for (i, lo, hi) in up]
            offd = list(reversed([(rho_seg(i), b - hi, b - lo) for (i, lo, hi) in dn]))
            mu = LB.minorant(offu, du, xu) or (0, 0)
            md = LB.minorant(offd, dd, xl) or (0, 0)
            lines.append((d, K, a, b, du, dd, roles, mu[0], mu[1], md[0], md[1], up, core, dn))
            segi += sorted({i for z in (up, core, dn) for (i, _, _) in z})
            lkeys.append(key)
        if not lines:
            return None
        return (lines, None), sorted(set(segi)), lkeys

    def _finish_lblock(self, box, cls, lines, li):
        """corners (choices, slacks) and lg of an L-block whose pieces are numbered; None if nothing."""
        ctx = self.P.ctx
        S, Q, R = ctx.S, ctx.Q, ctx.R
        x0, x1, y0, y1, U0, U1 = box
        vm = (U0 + U1) / 2.0
        corners = []
        lgs = []

        def fval(f, v):
            return {0: 1.0, 1: 4 * R * v, 2: 2 * (R * R - v * v), 3: 4 * R * v * 2 * (R * R - v * v)}[f]
        for (cx, cy) in ((x0, y0), (x0, y1), (x1, y0), (x1, y1)):
            ch = []
            for l in lines:
                row = []
                for up in (True, False):
                    cap = LB.cap_u(S, Q, cls, l) if up else LB.cap_d(S, Q, cls, l)
                    opts = [o for o in range(5) if LB.is_opt(l, up, o)]
                    def fv(o):
                        t = LB.opt_t(ctx, l, up, cap, o, cx, cy)
                        if t[0] == 0:
                            return float(cap)
                        n = t[1]
                        return (n[0] + n[1] * vm + n[2] * vm * vm) / fval(t[0], vm)
                    best = None
                    for o in sorted(opts, key=fv):
                        sg = 0
                        okk = True
                        t1 = LB.opt_t(ctx, l, up, cap, o, cx, cy)
                        for o2 in opts:
                            if o2 == o:
                                continue
                            t2 = LB.opt_t(ctx, l, up, cap, o2, cx, cy)
                            f = LB.tor(t1[0], t2[0])
                            Pp = LB.padd(LB.term(R, f, t1), LB.pneg(LB.term(R, f, t2)))
                            rb = LB.ratio_bound(Pp, LB.cmul(f, R, 1), U0, U1, True)
                            if rb is None:
                                okk = False
                                break
                            sg = max(sg, rb)
                        if okk:
                            best = (o, sg)
                            break
                    if best is None:
                        return None
                    row += [best[0], best[1]]
                ch.append(tuple(row))
            # the main bound at this corner
            f = 0
            for l, c in zip(lines, ch):
                f = LB.tor(LB.tor(LB.opt_t(ctx, l, True, LB.cap_u(S, Q, cls, l), c[0], cx, cy)[0],
                                  LB.opt_t(ctx, l, False, LB.cap_d(S, Q, cls, l), c[2], cx, cy)[0]), f)
            Pm = (0, 0, 0, 0, 0)
            sgs = 0
            for l, c in zip(lines, ch):
                Pm = LB.padd(Pm, LB.padd(LB.term(R, f, LB.opt_t(ctx, l, True, LB.cap_u(S, Q, cls, l), c[0], cx, cy)),
                                         LB.term(R, f, LB.opt_t(ctx, l, False, LB.cap_d(S, Q, cls, l), c[2], cx, cy))))
                sgs += c[1] + c[3]
            Den = LB.cmul(f, R, 1)
            lb_ = LB.ratio_bound(LB.padd(Pm, LB.pneg(LB.cmul(f, R, sgs))), Den, U0, U1, False)
            if lb_ is None:
                return None
            lgs.append(lb_)
            corners.append(ch)
        lg = max(min(lgs), 0)
        B = (lines, corners, lg)
        tag = 2 * li + 1
        if not LB.lblk_ok(ctx, box, cls, tag, B):
            return None
        return B

    def _group(self, box, d, K, interval, ivs, gi):
        P, ctx = self.P, self.P.ctx
        Q, S, R = ctx.Q, ctx.S, ctx.R
        U0 = box[4]
        Lu, Ld = lnU(Q, d, K), lnD(Q, d, K)
        ku, kd = kU(d), kD(d)
        Ju = interval((d, Lu), ku)
        Jd = interval((d, Ld), kd)
        if Ju is None or Jd is None:
            return None
        Au, Bu = Ju
        Ad, Bd = Jd
        # tau: the singular condition's certified half-line (Lemma T's tau), one certified point
        Iu = ivs((d, Lu))[ku]
        Id = ivs((d, Ld))[kd]
        tu = td = None
        if Iu is not None and Iu[1] is None:
            tu = Au if Iu[0] is None else max(Au, ceil_div(Iu[0].numerator * Q, Iu[0].denominator))
            if not G.admk(ctx, ku, lx(d, Lu, tu), ly(d, Lu, tu), box):
                tu = None
        if Id is not None and Id[0] is None:
            td = Bd if Id[1] is None else min(Bd, (Id[1].numerator * Q) // Id[1].denominator)
            if not G.admk(ctx, kd, lx(d, Ld, td), ly(d, Ld, td), box):
                td = None
        if tu is not None and tu > Bu:
            tu = None                  # above the certified range: no solo piece can use it
        if td is not None and td < Ad:
            td = None
        # pieces (exact, over Q)
        def pieces(L, lo, hi):
            out = []
            for i in P.lines[(d, L)]:
                e = P.segs[i]
                a, b = max(slo(S, d, e), lo), min(shi(S, d, e), hi)
                if b > a:
                    out.append((F(a), F(b), F(e[4], shi(S, d, e) - slo(S, d, e)), i))
            return out
        upP = pieces(Lu, Au, Bu)
        dnP = pieces(Ld, Ad, Bd)
        if not upP or not dnP:
            return None
        solo_up, cup = [], []
        for (a, b, rho, i) in upP:
            if tu is not None and b > tu:
                solo_up.append((max(a, F(tu)), b, rho, i))
                if a < tu:
                    cup.append((a, F(tu), rho, i))
            else:
                cup.append((a, b, rho, i))
        solo_dn, cdn = [], []
        for (a, b, rho, i) in dnP:
            if td is not None and a < td:
                solo_dn.append((a, min(b, F(td)), rho, i))
                if b > td:
                    cdn.append((F(td), b, rho, i))
            else:
                cdn.append((a, b, rho, i))
        delta = F(U0 * Q, R)
        cp = couple(cup, cdn, delta)
        # round to the grid, in chain order: down solos, coupled pairs, up solos
        prs = []
        lastb, lastd = Au, Ad
        segs = P.segs

        def mass(i, a, b):
            e = segs[i]
            return (e[4] * (b - a)) // (shi(S, d, e) - slo(S, d, e))
        for (a, b, rho, i) in solo_dn:
            c2, d2 = math.ceil(a), math.floor(b)
            c2 = max(c2, lastd)
            if d2 <= c2:
                continue
            prs.append((None, lastb, lastb, i, c2, d2, mass(i, c2, d2)))
            lastd = d2
        for (su, a, b, sd, c, dd, mu) in cp:
            a2, b2 = max(math.ceil(a), lastb), math.floor(b)
            if b2 < a2:
                b2 = a2
            c2 = max(min(math.ceil(c), (a2 * R + U0 * Q) // R), lastd)
            d2 = min(math.floor(dd), (b2 * R + U0 * Q) // R)
            if d2 < c2:
                d2 = c2
            # the shift conditions after rounding
            if c2 * R > a2 * R + U0 * Q or d2 * R > b2 * R + U0 * Q:
                continue
            # the pieces must stay inside their segments
            eu, ed = segs[su], segs[sd]
            if not (slo(S, d, eu) <= a2 and b2 <= shi(S, d, eu) and slo(S, d, ed) <= c2 and d2 <= shi(S, d, ed)):
                continue
            mm = min(mass(su, a2, b2), mass(sd, c2, d2))
            if mm <= 0:
                continue
            prs.append((su, a2, b2, sd, c2, d2, mm))
            lastb, lastd = b2, d2
        for (a, b, rho, i) in solo_up:
            a2, b2 = max(math.ceil(a), lastb), math.floor(b)
            if b2 <= a2:
                continue
            prs.append((i, a2, b2, None, lastd, lastd, mass(i, a2, b2)))
            lastb = b2
        if not prs:
            return None
        used = sorted({p[0] for p in prs if p[0] is not None} | {p[3] for p in prs if p[3] is not None})
        g = (d, K, Au, Bu, Ad, Bd, (tu + 1) if tu is not None else 0, (td + 1) if td is not None else 0, prs)
        return g, used


# =============================================================================================
# the search

class MSearch:
    def __init__(self, ctx, P, mchk, max_depth=30, use_thr=True, use_lin=True, pts=(), D=1, m=1):
        self.ctx, self.P, self.mchk = ctx, P, mchk
        self.pts = list(pts)
        self.psearch = G.Search(ctx, D, ctx.W, self.pts, m) if self.pts else None
        self.builder = Builder(P, mchk, use_thr=use_thr, use_lin=use_lin)
        self.max_depth = max_depth
        self.m = mchk.m
        self.stat = dict(E=0, PIECE=0, C=0, split=0, boxes=0, maxdepth=0, UNCERT=0, T=0, Sblk=0, claims=0,
                         pairs=0, inherit=0, Lblk=0, Llines=0, leafT=0, leafL=0, ADM=0, CHAIN1=0,
                         CHAIN2=0, ptclaims=0)

    def fbox(self, box):
        Q, R = self.ctx.Q, self.ctx.R
        x0, x1, y0, y1, U0, U1 = box
        return (F(x0, Q), F(x1, Q), F(y0, Q), F(y1, Q), F(U0, R), F(U1, R))

    def point_leaf(self, box, need):
        """a ZMTree point leaf reaching `need` (units of 1/W) at every admissible pose (Lemma P: the pieces
        supply the rest), via gen_zmtree's search with the target lowered; checked by its mirror."""
        ps = self.psearch
        if ps is None or need <= 0:
            return None
        ctx2 = G.Ctx(self.ctx.S, self.ctx.Q, self.ctx.R, need, self.ctx.F)
        old_ctx, old_den = ps.ctx, ps.chk.Wden
        ps.ctx = ctx2
        ps.chk.Wden = need
        try:
            lf = ps.leaf_for(box, 0)
        finally:
            ps.ctx, ps.chk.Wden = old_ctx, old_den
        if lf is None or lf[0] == 'E':
            return None
        kind, chA, chB, emp, ents = lf
        if kind != 'ADM':
            chA, chB, emp, ents = G.optimise_leaf(need, self.pts, chA, chB, emp, ents)
        leaf = G.Leaf([], chA, chB, emp)
        prev = -1
        for k, tag in ents:
            leaf.ents.append((k - prev - 1, tag)); prev = k
        if not G.leaf_ok(ctx2, box, self.pts, leaf):
            return None
        return (kind, chA, chB, emp, ents)

    def _build(self, box, depth, parent=None):
        ctx = self.ctx
        st = self.stat
        st['boxes'] += 1
        st['maxdepth'] = max(st['maxdepth'], depth)
        us = G.clip_value(ctx, box)
        if us is not None:
            st['C'] += 1
            nb = box[:5] + (us,)
            return ('C', us, self._build(nb, depth, parent))
        if G.empty_ok(ctx, box):
            st['E'] += 1
            return ('E',)
        r = self.builder.build(box)
        best = r
        if parent is not None and (r is None or parent[4] > r[4]):
            # the parent's certificate holds on the sub-box too (re-checked by the mirror)
            cls = [(self.P.segs[i], t) for i, t in parent[0]]
            ok, val = pc_value(ctx, box, cls, parent[1], parent[2], parent[3])
            if ok and (r is None or val > r[4]):
                best = (parent[0], parent[1], parent[2], parent[3], val)
                st['inherit'] += 1
        Lp = best[4] if best is not None else 0
        if Lp < ctx.W and self.psearch is not None:
            pl = self.point_leaf(box, ctx.W - Lp)
            if pl is not None:
                if best is None:
                    best = ([], [], [], [], 0)
                st[pl[0]] += 1
                st['ptclaims'] += len(pl[4])
                if best[3]:
                    st['leafL'] += 1
                if best[2]:
                    st['leafT'] += 1
                return ('Z', best, pl)
        if best is not None and best[4] >= ctx.W:
            st['PIECE'] += 1
            st['T'] += len(best[2]); st['Sblk'] += len(best[1]); st['claims'] += len(best[0])
            st['pairs'] += sum(len(g[8]) for g in best[2])
            st['Lblk'] += len(best[3]); st['Llines'] += sum(len(B[0]) for B in best[3])
            st['leafT'] += 1 if best[2] else 0
            st['leafL'] += 1 if best[3] else 0
            return ('Z', best)
        if depth >= self.max_depth:
            st['UNCERT'] += 1
            return ('UNC', box)
        st['split'] += 1
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
        l, r2 = G.split(box, axis)
        return (axis, self._build(l, depth + 1, best), self._build(r2, depth + 1, best))


# =============================================================================================
# Lean emission

def leaf_digits_pc(claims, sb, tg, lb=(), B=BASE):
    d = [len(claims)]
    prev = -1
    for i, t in claims:
        d += [i - prev - 1, t]
        prev = i
    def big(v):
        assert 0 <= v < B ** 3, v
        return [v % B, (v // B) % B, v // (B * B)]
    d.append(len(sb))
    for (dr, K, A, Bv) in sb:
        d += [dr] + big(K) + big(A) + big(Bv)
    d.append(len(tg))
    for (dr, K, Au, Bu, Ad, Bd, tu1, td1, prs) in tg:
        d += [dr] + big(K) + big(Au) + big(Bu) + big(Ad) + big(Bd) + big(tu1) + big(td1) + [len(prs)]
        for (ju1, a, b, jd1, c, dd, mm) in prs:
            d += [ju1] + big(a) + big(b) + [jd1] + big(c) + big(dd) + big(mm)

    def big4(v):
        assert 0 <= v < B ** 4, v
        return [v % B, (v // B) % B, (v // (B * B)) % B, v // (B * B * B)]

    def sgn(v):
        return big4(v) + big4(0) if v >= 0 else big4(0) + big4(-v)
    d.append(len(lb))
    for (lines, corners, lg) in lb:
        d.append(len(lines))
        for (dr, K, a, b, du, dd, roles, sU, iU, sD, iD, up, core, dn) in lines:
            d += [dr] + big4(K) + big4(a) + big4(b) + big4(du) + big4(dd) + [roles] + big4(sU) + sgn(iU) + \
                big4(sD) + sgn(iD)
            for z in (up, core, dn):
                d.append(len(z))
                for (j1, lo, hi) in z:
                    d += [j1] + big4(lo) + big4(hi)
        for ch in corners:
            for (oU, sgU, oD, sgD) in ch:
                d += [oU] + big4(sgU) + [oD] + big4(sgD)
        d += big4(lg)
    for x in d:
        assert 0 <= x < B, x
    return d


def replay(ctx, t, box, st, out, leaves):
    B = BASE
    if t[0] == 'E':
        assert G.empty_ok(ctx, box), box
        out.append(5); st['E'] += 1
        return
    if t[0] == 'C':
        us = t[1]
        assert G.clip_ok(ctx, box, us), box
        out += [6, us % B, us // B]; st['C'] += 1
        replay(ctx, t[2], box[:5] + (us,), st, out, leaves)
        return
    if t[0] in ('XM', 'YM'):
        _, m, l, r = t
        out += [7 if t[0] == 'XM' else 8, m % B, m // B]
        ax = 0 if t[0] == 'XM' else 1
        lb = list(box); rb = list(box)
        lb[2 * ax + 1] = m; rb[2 * ax] = m
        replay(ctx, l, tuple(lb), st, out, leaves)
        replay(ctx, r, tuple(rb), st, out, leaves)
        return
    if t[0] == 'Z':
        claims, sb, tg, lb, val = t[1]
        out.append(0)
        if len(t) > 2:
            kind, chA, chB, emp, ents = t[2]
            d = [len(ents)]
            prev = -1
            for k, tag in ents:
                g = k - prev - 1; prev = k
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
            leaves.append(d)
        else:
            leaves.append([0])                     # the point part: no points claimed
        leaves.append(leaf_digits_pc(claims, sb, tg, lb))
        st['Z'] += 1
        return
    if t[0] == 'UNC':
        raise AssertionError("uncertified box in the tree")
    axis, l, r = t
    out.append(1 + axis)
    lb, rb = G.split(box, axis)
    replay(ctx, l, lb, st, out, leaves)
    replay(ctx, r, rb, st, out, leaves)


def tree_cost(t, memo):
    k = id(t)
    if k in memo:
        return memo[k]
    if t[0] == 'E':
        r = 0.2
    elif t[0] == 'Z':
        claims, sb, tg, lb, _ = t[1]
        r = (2.0 + 4.0 * len(sb) + 8.0 * len(tg) + 0.05 * len(claims) + 0.5 * sum(len(g[8]) for g in tg)
             + sum(20.0 * len(B[0]) for B in lb))
    elif t[0] == 'C':
        r = 0.1 + tree_cost(t[2], memo)
    elif t[0] in ('XM', 'YM'):
        r = 0.05 + tree_cost(t[2], memo) + tree_cost(t[3], memo)
    else:
        r = 0.05 + tree_cost(t[1], memo) + tree_cost(t[2], memo)
    memo[k] = r
    return r


def emit_stree(Sg):
    def b(lo, hi):
        if lo >= hi:
            return '.leaf'
        mid = (lo + hi) // 2
        X0, Y0, X1, Y1, w = Sg[mid]
        return f"(.node {b(lo, mid)} ({X0}, {Y0}, {X1}, {Y1}, {w}) {b(mid + 1, hi)})"
    return b(0, len(Sg))


HDR = "set_option linter.style.longLine false\n"
FUEL = 128


def emit(args, sha, s, D, W, Pts, Sg, ctx, trees, cells, Mq, M):
    name, outdir = args.name, args.outdir
    os.makedirs(outdir, exist_ok=True)
    mod = outdir.rstrip('/').replace('lean/', '', 1).replace('/', '.')
    R = ctx.R
    Um = R // 2
    half = M - M // 2
    width = half // cells
    covT = f"CovM {D} {ctx.S} {Mq} {R} {W} ptsL segsL"
    kmemo = {}
    chunks = []
    budget = args.chunk_cost

    def skel(t, box):
        if tree_cost(t, kmemo) <= budget or t[0] in ('E', 'Z'):
            chunks.append((t, box))
            return f"ok{len(chunks) - 1}"
        if t[0] == 'C':
            nb = box[:5] + (t[1],)
            return (f"(ZMTreeM.CM_cov (by norm_num) (by norm_num) (by norm_num) (by decide +kernel) "
                    f"{skel(t[2], nb)})")
        if t[0] in ('XM', 'YM'):
            _, m, l, r = t
            ax = 0 if t[0] == 'XM' else 1
            lb = list(box); rb = list(box)
            lb[2 * ax + 1] = m; rb[2 * ax] = m
            return f"(CovM.split{'XY'[ax]} {m} {skel(l, tuple(lb))} {skel(r, tuple(rb))})"
        axis, l, r = t
        lb, rb = G.split(box, axis)
        return f"(CovM.split{'XYU'[axis]} {lb[2 * axis + 1]} {skel(l, lb)} {skel(r, rb)})"

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
    if args.chunks_only:
        # measurement mode: the chunks of the searched root cells only (no Cov.lean)
        for rt in sorted(trees):
            skel(trees[rt], rt)
        del chunks[args.chunks_only:]
        proof = None
    else:
        proof = skel(gx(0, cells), root)
    ns = f"SquarePacking.{name}"
    doc = (f"/-!\n# `{name}`: the mixed cover (generated by `lean/scripts/gen_zmmtree.py`; do not edit)\n\n"
           f"From `{os.path.basename(args.cover)}`, sha256 `{sha}`:\n{len(Pts)} points `(X/{D}, Y/{D})` and {len(Sg)} segments, "
           f"masses `w/{W}`, container `[0, {Mq}/{D}]²`.\n-/\n")
    ptl = ",\n   ".join(f"({x}, {y}, {w})" for x, y, w in Pts)
    sgl = ",\n   ".join(f"({a}, {b}, {c}, {d}, {w})" for a, b, c, d, w in Sg)
    L = ["import Sqpack.ZMTreeX\n", HDR, doc, f"namespace {ns}\n", "open BoxTree ZMTreeM\n",
         "set_option maxRecDepth 100000 in",
         f"def pts : PTree :=\n  {G.emit_ptree(Pts)}\n",
         "theorem pts_nodup : pts.toList.Nodup :=\n  PTree.nodup_of_chainB _ (by decide +kernel)\n",
         f"theorem pts_d4 : d4Check {Mq} pts = true := by decide +kernel\n",
         "set_option maxRecDepth 100000 in",
         f"def segs : STree :=\n  {emit_stree(Sg)}\n",
         f"theorem segs_d4 : segD4Check {Mq} segs = true := by decide +kernel\n",
         f"theorem wsum_lt : pts.wsum + segs.wsum < {args.n} * {W} := by decide +kernel\n",
         "set_option maxRecDepth 100000 in\nset_option maxHeartbeats 0 in",
         "def ptsL : List (ℕ × ℕ × ℕ) :=\n  [" + ptl + "]\n",
         "set_option maxRecDepth 100000 in\nset_option maxHeartbeats 0 in",
         "def segsL : List SegE :=\n  [" + sgl + "]\n",
         "set_option maxRecDepth 100000 in\ntheorem pts_toList : pts.toList = ptsL := by decide +kernel\n",
         "set_option maxRecDepth 100000 in\ntheorem segs_toList : segs.toList = segsL := by decide +kernel\n",
         "theorem ptsL_nodup : ptsL.Nodup := pts_toList ▸ pts_nodup\n",
         "theorem segsL_nodup : segsL.Nodup := by\n  rw [← segs_toList]\n"
         "  have h := segs_d4\n  simp only [segD4Check, Bool.and_eq_true] at h\n"
         "  exact STree.nodup_of_chainB _ h.1\n",
         f"end {ns}\n"]
    open(f"{outdir}/Pts.lean", 'w').write("\n".join(L))
    st = dict(C=0, E=0, Z=0, digits=0)
    streams = []
    for t, box in chunks:
        out, lv = [], []
        replay(ctx, t, box, st, out, lv)
        streams.append((out, lv))
    costs = [tree_cost(t, kmemo) for t, _ in chunks]
    nparts = args.parts
    parts = [[] for _ in range(nparts)]
    loads = [0.0] * nparts
    for i in sorted(range(len(chunks)), key=lambda i: -costs[i]):
        j = min(range(nparts), key=lambda j: loads[j])
        parts[j].append(i); loads[j] += costs[i]
    for pi, idxs in enumerate(parts):
        idxs.sort()
        L = [f"import {mod}.Pts\n", HDR,
             f"/-!\n# `{name}`: mixed box-tree chunks (generated; do not edit)\n\n"
             f"Each `okI` is one kernel evaluation (`decide +kernel`) of `ZMTreeM.checkM` on one subtree.\n-/\n",
             f"namespace {ns}\n", "open BoxTree ZMTreeM\n"]
        for i in idxs:
            t, box = chunks[i]
            bx = ' '.join(map(str, box))
            out, lv = streams[i]
            code = G.encode(out, BASE)
            nd = len(out) + sum(len(x) for x in lv)
            st['digits'] += nd
            L.append(f"/-- Chunk {i}: {len(lv) // 2} `Z` leaves, {nd} base-2^20 digits. -/")
            L.append(f"def c{i} : ℕ :=\n  0x{code:x}\n")
            lits = ",\n   ".join(f"0x{G.encode(x, BASE):x}" for x in lv)
            L.append(f"def d{i} : List ℕ :=\n  [{lits}]\n")
            L.append(f"theorem ok{i} : {covT} {bx} :=\n"
                     f"  ZMTreeM.soundM {D} {ctx.S} {Mq} {R} {W} {ctx.F} ptsL segsL (by norm_num) (by norm_num) "
                     f"(by norm_num) ptsL_nodup segsL_nodup (ZMTreeM.decM {BASE} {FUEL} c{i} d{i}).1 {bx} ptsL segsL\n"
                     f"    (List.Sublist.refl _) (List.Sublist.refl _) (by decide +kernel)\n")
        L.append(f"end {ns}\n")
        open(f"{outdir}/Part{pi}.lean", 'w').write("\n".join(L))
    if proof is None:
        print(f"wrote {outdir}: {len(chunks)} chunks in {nparts} parts (chunks only), {st}", file=sys.stderr)
        return
    imports = "\n".join(f"import {mod}.Part{pi}" for pi in range(nparts))
    L = [imports + "\n", HDR,
         f"/-!\n# `{name}`: the mixed box tree covers the D4 fundamental region (generated; do not edit)\n\n"
         f"{st['Z']} `Z` leaves, {st['E']} `E` leaves, {st['C']} clips, in {len(chunks)} chunks, {nparts} files.\n-/\n",
         f"namespace {ns}\n", "open BoxTree ZMTreeM\n",
         f"theorem cov_rootL : {covT} {' '.join(map(str, root))} :=\n  {proof}\n",
         f"theorem cov_root : CovM {D} {ctx.S} {Mq} {R} {W} pts.toList segs.toList {' '.join(map(str, root))} := by\n"
         f"  rw [pts_toList, segs_toList]; exact cov_rootL\n",
         f"end {ns}\n"]
    open(f"{outdir}/Cov.lean", 'w').write("\n".join(L))
    print(f"wrote {outdir}: {len(chunks)} chunks in {nparts} parts, {st}", file=sys.stderr)


# =============================================================================================
# driver

_S = None


def _work_cell(root):
    t0 = time.process_time()
    for k in _S.stat:
        _S.stat[k] = 0

    def rec(box, n):
        if n == 1:
            return _S._build(box, 0)
        l, r = G.split(box, 2)
        return (2, rec(l, n // 2), rec(r, n // 2))
    tree = rec(root, _S.ubins)
    return root, tree, dict(_S.stat), time.process_time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cover')
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--K', type=int, default=12)
    ap.add_argument('--J', type=int, default=32)
    ap.add_argument('--pitch', default='1/10')
    ap.add_argument('--ubins', type=int, default=8)
    ap.add_argument('--nproc', type=int, default=1)
    ap.add_argument('--depth', type=int, default=30)
    ap.add_argument('--only', type=int, default=None)
    ap.add_argument('--cells', default=None, help='only these root cells, "i,j;i,j" (testing)')
    ap.add_argument('--no-thr', action='store_true')
    ap.add_argument('--no-lin', action='store_true', help='no L-blocks (Lemma L)')
    ap.add_argument('--name')
    ap.add_argument('--outdir')
    ap.add_argument('--chunk-cost', type=float, default=3000.0)
    ap.add_argument('--parts', type=int, default=1)
    ap.add_argument('--chunks-only', type=int, default=0,
                    help='measurement: emit only the first N chunks of the searched cells (no Cov.lean)')
    ap.add_argument('--save')
    ap.add_argument('--load')
    args = ap.parse_args()
    raw = open(args.cover, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    cv = MC.load(args.cover)
    MC.validate(cv)
    s = F(cv['s_num'], cv['s_den'])
    D, W = cv['D'], cv['W']
    assert not cv['polygons'], "polygons are not supported"
    Pts = sorted(tuple(p) for p in cv['points'] if p[2] > 0)
    Sg = []
    for (X0, Y0, X1, Y1, w) in cv['segments']:
        if w == 0:
            continue
        a, b = (X0, Y0), (X1, Y1)
        if b < a:
            a, b = b, a
        Sg.append((a[0], a[1], b[0], b[1], w))
    Sg.sort()
    assert len(set(e[:4] for e in Sg)) == len(Sg), "repeated segment"
    tot = sum(p[2] for p in Pts) + sum(e[4] for e in Sg)
    assert tot < args.n * W, (tot, args.n * W)
    S = 2 ** args.K
    Q = D * S
    Mq = s * D
    assert Mq.denominator == 1
    Mq = int(Mq)
    M = Mq * S
    R = 2 ** args.J
    ctx = G.Ctx(S, Q, R, W, 3 * Q // 4)
    pitch = F(args.pitch)
    cells = (s / 2) / pitch
    assert cells.denominator == 1
    cells = int(cells)
    cov = ZX.Cover(cv)
    assert cov.symmetric_d4()
    mchk = ZX.MixedChecker(cov, max_depth=args.depth, cert_mode=True)
    P = Pieces(ctx, cov, Sg)
    global _S
    if args.load:
        import pickle
        dd = pickle.load(open(args.load, 'rb'))
        trees = dd['trees']
        assert dd['sha'] == sha
    else:
        _S = MSearch(ctx, P, mchk, max_depth=args.depth, use_thr=not args.no_thr, use_lin=not args.no_lin,
                     pts=Pts, D=D, m=s)
        _S.ubins = args.ubins
        roots = G.roots_of(ctx, M, cells, args.ubins)
        if args.cells:
            want = [tuple(map(int, c.split(','))) for c in args.cells.replace('+', ';').split(';')]
            wd = (M // 2) // cells
            roots = [r for r in roots if (r[0] // wd, r[2] // wd) in want]
        if args.only:
            roots = roots[:args.only]
        t0 = time.time()
        tot = {}
        trees = {}
        cpu = 0.0
        if args.nproc > 1:
            import multiprocessing as mp
            pool = mp.get_context('fork').Pool(args.nproc)
            it = pool.imap_unordered(_work_cell, roots, chunksize=1)
        else:
            it = map(_work_cell, roots)
        for i, (root, tree, st, c) in enumerate(it):
            trees[root] = tree
            cpu += c
            for k, v in st.items():
                tot[k] = max(tot.get(k, 0), v) if k == 'maxdepth' else tot.get(k, 0) + v
            if (i + 1) % 20 == 0:
                print(f"  {i+1}/{len(roots)} cells {time.time()-t0:.0f}s {tot}", file=sys.stderr, flush=True)
        print(f"search done: {len(roots)} cells, {time.time()-t0:.0f}s wall, {cpu:.0f}s cpu; {tot}", file=sys.stderr)
        if args.save:
            import pickle
            pickle.dump(dict(trees=trees, sha=sha, stat=tot), open(args.save, 'wb'))
        if tot.get('UNCERT', 0):
            print("UNCERTIFIED boxes remain: no Lean output", file=sys.stderr)
            return 1
    if args.outdir:
        emit(args, sha, s, D, W, Pts, Sg, ctx, trees, cells, Mq, M)
    return 0


if __name__ == '__main__':
    sys.exit(main())
