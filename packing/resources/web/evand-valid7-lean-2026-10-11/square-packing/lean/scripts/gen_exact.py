#!/usr/bin/env python3
"""EXACT leaves (Lemma E, `LemmaELeaf.lean`): build an `ExLeaf` certificate for a pose box.

    gen_exact.py COVER S R x0 x1 y0 y1 U0 U1 [--lean NAME]

Box: centres [x0, x1] x [y0, y1] over Q = D*S, angles u in (U0/R, U1/R].  The search uses floats
only to choose; every decision is re-checked with the exact mirror `lemmae_mirror.py`, which computes
what the kernel computes.
"""
import os, sys, time, argparse
from fractions import Fraction as Fr
from lemmae_mirror import *
from kmirror import vertOkK  # the kernel's vertex test (LemmaEK.vertOkK)
import itertools
FC_MAXCOMB = 512   # combinations searched for common-factor certificates
from gen_axis import read_cover


def ev(p, u):
    s = 0.0
    for a in reversed(p):
        s = s * u + a
    return s


def lowdeg(p):
    m = 0
    while m < len(p) and p[m] == 0:
        m += 1
    return m


def svals(L, u, v):
    """float value of a scaled line at the point v and angle u"""
    P, i, j, k, d = L
    den = (1 - u * u) ** i * (2 * u) ** j * (1 + u * u) ** k * d
    return (ev(P[0], u) * v[0] + ev(P[1], u) * v[1] + ev(P[2], u)) / den


class Leaf:
    USE_TAN = True
    # mixed segments without a separating split: the chord only (zm's Lemma E: a line whose chord is
    # empty at every sample is dropped, otherwise min up - max lo); with deep bisection of the sub-bins
    MIXED_CH = os.environ.get('V7_MIXED_CH', '0') == '1'
    MAXDEPTH = int(os.environ.get('V7_MAXDEPTH', '8'))
    CAP_TAG = os.environ.get('V7_CAP_TAG', '0') == '1'
    # prefer the box-wide alternatives unless the vertex ones cut the combinations by this factor
    BOX_FACTOR = float(os.environ.get('V7_BOX_FACTOR', '1'))
    USE_CORNER = True
    ANCHOR = 'hi'

    def __init__(self, cover, S, R, x0, x1, y0, y1, U0, U1, maxdepth=None):
        side_, D, W, pts, segs, rects = cover
        self.D, self.W, self.S, self.R = D, W, S, R
        self.W0 = W          # the target of the leaf; W = W0 - credit for the vertex test
        self.cred = None
        self.Q = Q = D * S
        self.box = (x0, x1, y0, y1, U0, U1)
        self.maxdepth = maxdepth if maxdepth is not None else Leaf.MAXDEPTH
        reach = 0.7072
        cx0, cx1, cy0, cy1 = x0 / Q, x1 / Q, y0 / Q, y1 / Q
        self.chs = [e for e in segs if e[1] == e[3] and e[0] < e[2]
                    and cy0 - reach <= e[1] / D <= cy1 + reach
                    and e[2] / D >= cx0 - reach and e[0] / D <= cx1 + reach]
        self.cvs = [e for e in segs if e[0] == e[2] and e[1] < e[3]
                    and cx0 - reach <= e[0] / D <= cx1 + reach
                    and e[3] / D >= cy0 - reach and e[1] / D <= cy1 + reach]
        wN, wD = widN(R, U0, U1), widD(R, U0)
        self.crs = [r for r in rects
                    if 2 * x1 * wD + D * S * wN <= 2 * r[2] * S * wD
                    and 2 * y1 * wD + D * S * wN <= 2 * r[3] * S * wD
                    and r[0] / D <= cx1 + reach and r[1] / D <= cy1 + reach]
        # lower sides: the wall where it is above the box side on the whole bin
        def wall(x):
            w0 = (1 - (U0 / R) ** 2 + 2 * U0 / R) / (1 + (U0 / R) ** 2) / 2
            w1 = (1 - (U1 / R) ** 2 + 2 * U1 / R) / (1 + (U1 / R) ** 2) / 2
            if w1 <= x / Q: return False
            if w0 >= x / Q: return True
            return None
        self.wx, self.wy = wall(x0), wall(y0)
        # a wall crossing the box side inside the bin: keep the side and add the wall as a constraint
        self.ex, self.ey = self.wx is None, self.wy is None
        if self.ex: self.wx = False
        if self.ey: self.wy = False
        self.ok = True
        self.use_tan = Leaf.USE_TAN
        self.use_corner = Leaf.USE_CORNER
        if self.ok:
            self.crs = [self.modes(r) for r in self.crs]

    def modes(self, r):
        """the cap modes of a rectangle (QUADRANT_EXACT.md 4.4, qx2_zm.Exact.u_regime): 'tan' at
        d* = min(1, (dmin + dmax)/2) when d >= cos on the whole box, else std; re-checked by tanAx."""
        D, Q, R = self.D, self.Q, self.R
        x0, x1, y0, y1, U0, U1 = self.box
        u0, u1 = Fr(U0, R), Fr(U1, R)
        c0, s0 = (1 - u0 * u0) / (1 + u0 * u0), 2 * u0 / (1 + u0 * u0)
        if u1 * u1 + 2 * u1 - 1 <= 0:
            c1, s1 = (1 - u1 * u1) / (1 + u1 * u1), 2 * u1 / (1 + u1 * u1)
            w1 = c1 + s1
        else:
            w1 = Fr(14143, 10000)
        w0 = c0 + s0
        out = [r]
        for a, lo, hi, cap, w in ((Fr(r[0], D), Fr(x0, Q), Fr(x1, Q), capX(D, r[0]), self.wx),
                                  (Fr(r[1], D), Fr(y0, Q), Fr(y1, Q), capY(D, r[1]), self.wy)):
            mo = None
            dmax = a - lo + w1 / 2
            dmin = a - hi + w0 / 2
            if self.use_tan and dmax > 0 and dmin >= c0:
                ds = min(Fr(1), (dmin + dmax) / 2)
                cand = (ds.numerator, ds.denominator)
                if tanAx(Q, x0, x1, y0, y1, U0, U1, R, self.wx, self.wy, cap, cand):
                    mo = cand
            out.append(mo)
        out.append(('std',))
        if self.use_corner and out[1] is None and out[2] is None:
            # E'': corner3, then xcut; McCormick anchor at the low corner (2x0, 2y0)/2Q, else the high one
            ym = y0 + y1
            anchors = [(2 * x0, 2 * y0), (2 * x1, 2 * y1)]
            if Leaf.ANCHOR == 'lo': anchors.reverse()
            for kind in ('c3', 'xc'):
                for xa, ya in anchors:
                    cand = tuple(out[:3]) + ((kind, xa, ya, ym, 2 * Q),)
                    if cornerOk(Q, x0, x1, y0, y1, U0, U1, R, self.wx, self.wy, D, cand):
                        return cand
        return tuple(out)

    def pins(self):
        D, Q, R = self.D, self.Q, self.R
        x0, x1, y0, y1, U0, U1 = self.box
        Ls = []
        forms = [L for e in self.chs for L in hFormsSLs(D, e)] + \
            [L for e in self.cvs for L in vFormsSLs(D, e)] + [L for r in self.crs for L in lebSLs(D, r)]
        for L in forms:
            P = L[0]
            if P in Ls: continue
            if cornersOk(Q, x0, x1, y0, y1, U0, U1, R, self.wx, self.wy, False, P): continue
            if cornersOk(Q, x0, x1, y0, y1, U0, U1, R, self.wx, self.wy, True, P): continue
            Ls.append(P)
        self.Ls = Ls
        self.side = sideE(Q, x0, x1, y0, y1, self.wx, self.wy, self.ex, self.ey)
        import itertools
        def boxalts(ups, los):
            for k in (1, 2, 3):
                for Ua in itertools.combinations(range(3), k):
                    for kk in (1, 2, 3):
                        for La in itertools.combinations(range(3), kk):
                            if boxDomOk(Q, x0, x1, y0, y1, U0, U1, R, self.wx, self.wy, ups, los,
                                        (list(Ua), list(La))):
                                return (list(Ua), list(La))
        self.hbx = [boxalts(hUps(D, e), hLos(D, e)) for e in self.chs]
        self.vbx = [boxalts(vUps(D, e), vLos(D, e)) for e in self.cvs]
        return Ls

    # -------------------------------------------------------------- one sub-bin of a pair
    def choose(self, Dp, X, Y, b0, b1):
        """float-guided certificate at the vertex: (splits, fcs, hc, vc, lc)"""
        R = self.R
        ts = (0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0)
        us = [max(b0 / R + (b1 - b0) / R * t, 1e-9) for t in ts]
        pts = []
        for u in us:
            dv = ev(Dp, u)
            pts.append((u, (ev(X, u) / dv, ev(Y, u) / dv)))
        splits, lc = [], []
        m0 = lowdeg(Dp) if b0 == 0 else 0
        sig = ev(Dp[m0:], (b0 + b1) / 2 / R) > 0
        def qsign(q):
            return [svals(q, u, v) >= 0 for u, v in pts]
        capk = {}     # (axis, coordinate of the rectangle's side) -> split on its cap depth
        for r in self.crs:
            pair = []
            for ax, cap in (('x', capXm(self.D, r)), ('y', capYm(self.D, r))):
                ds = [svals(cap, u, v) for u, v in pts]
                ss = [2 * u / (1 + u * u) for u, _ in pts]
                if all(d <= 0 for d in ds): pair.append([('zeroC',)])
                elif all(d >= s for d, s in zip(ds, ss)): pair.append([('linC',)])
                elif all(0 <= d <= s for d, s in zip(ds, ss)): pair.append([('par',)])
                elif any(d < 0 for d in ds):
                    k = len(splits); splits.append((cap, 0, 1, 0, 1))
                    pair.append([('zeroT', k), ('parT', k, True)])
                    capk[(ax, r[0][0] if ax == 'x' else r[0][1])] = k
                else:
                    k = len(splits); splits.append((sl_sub(cap, sSL(1)), 0, 1, 0, 1))
                    pair.append([('parT', k, False), ('linT', k)])
            lc.append(tuple(pair))
        tol = 1e-9
        def pick(ups, los, bx, side=None):
            Ua, La, posl = set(), set(), []
            for u, v in pts:
                uv = [svals(L, u, v) for L in ups]; lv = [svals(L, u, v) for L in los]
                mu = min(uv); ml = max(lv)
                posl.append(mu - ml > 1e-12)
                if mu - ml > -1e-9:
                    Ua |= {i for i in range(3) if uv[i] <= mu + tol}
                    La |= {i for i in range(3) if lv[i] >= ml - tol}
            if side in capk and Leaf.CAP_TAG and ((bx[0] and bx[1]) or (Ua and La)):
                # a segment on a side of the Lebesgue rectangle whose cap is split: where the square pokes
                # past the side (cap depth >= 0) its chord pays for the cap's area, elsewhere it is dropped
                k = capk[side]
                return [(('drop',), (k, False)), (('box',) if bx[0] and bx[1] else ('alt', sorted(Ua), sorted(La)),
                                                  (k, True))]
            if not any(posl): return [(('drop',), None)]
            ch = ('box',) if len(bx[0]) * len(bx[1]) == 1 or \
                len(bx[0]) * len(bx[1]) <= Leaf.BOX_FACTOR * len(Ua) * len(La) \
                else ('alt', sorted(Ua), sorted(La))
            if ch[0] == 'alt' and not segOkA(sig, Dp, X, Y, b0, b1, R, ups, los, ch[1], ch[2]):
                # options crossing inside the sub-bin: widen by float closeness, else the box choice
                ch = ('box',)
                for wtol in (1e-6, 1e-3, 1e-2, 1e-1):
                    Ub, Lb = set(Ua), set(La)
                    for u, v in pts:
                        uv = [svals(L, u, v) for L in ups]; lv = [svals(L, u, v) for L in los]
                        Ub |= {i for i in range(3) if uv[i] <= min(uv) + wtol}
                        Lb |= {i for i in range(3) if lv[i] >= max(lv) - wtol}
                    if len(Ub) * len(Lb) >= len(bx[0]) * len(bx[1]): break
                    if segOkA(sig, Dp, X, Y, b0, b1, R, ups, los, sorted(Ub), sorted(Lb)):
                        ch = ('alt', sorted(Ub), sorted(Lb)); break
            if all(posl): return [(ch, None)]
            # mixed: tag by a split whose sign pattern matches
            for k, sp in enumerate(splits):
                sg = qsign(sp[0])
                if sg == posl: return [(('drop',), (k, False)), (ch, (k, True))]
                if [not x for x in sg] == posl: return [(('drop',), (k, True)), (ch, (k, False))]
            if Leaf.MIXED_CH:
                # the chord alone is a lower bound everywhere; where the segment only just misses
                # it is slightly negative, much less than what `drop` loses where it just meets
                return [(ch, None)]
            return [(('drop',), None), (ch, None)]
        hc = [pick(hUps(self.D, e), hLos(self.D, e), bx, ('y', e[1])) for e, bx in zip(self.chs, self.hbx)]
        vc = [pick(vUps(self.D, e), vLos(self.D, e), bx, ('x', e[0])) for e, bx in zip(self.cvs, self.vbx)]
        return [splits, [], hc, vc, lc]

    def factor_certs(self, sig, Dp, X, Y, b0, b1, cert):
        """common-factor certificates for the failing combinations (sympy gcd)"""
        import sympy
        splits, fcs, hc, vc, lc = cert
        uu = sympy.Symbol('u')
        def topoly(p): return sympy.Poly(list(reversed(p)) or [0], uu)
        def tolist(P):
            c = P.all_coeffs(); return [int(x) for x in reversed(c)]
        out = []
        for k, sp in enumerate(splits):
            sq = snum(sig, atV(sp[0], Dp, X, Y))
            Pq = topoly(sq)
            if Pq.is_zero: continue
            # gcd with a few failing totals: use the full sum with each pattern's first combination
            for pat in pats(len(splits)):
                alts = []
                for e, bx, l in zip(self.chs, self.hbx, hc):
                    alts.append([t for x in l if tagOk(pat, x[1]) for t in segCAlts(Dp, X, Y, e[4], self.D, nat_sub(e[2], e[0]), hUps(self.D, e), hLos(self.D, e), bx, x[0])])
                for e, bx, l in zip(self.cvs, self.vbx, vc):
                    alts.append([t for x in l if tagOk(pat, x[1]) for t in segCAlts(Dp, X, Y, e[4], self.D, nat_sub(e[3], e[1]), vUps(self.D, e), vLos(self.D, e), bx, x[0])])
                for r, (xs, ys) in zip(self.crs, lc):
                    alts.append([t for ax in xs if tagOk(pat, capTag(ax)) for ay in ys if tagOk(pat, capTag(ay))
                                 for t in lebRFs(Dp, X, Y, self.D, r, ax, ay)])
                sps = [sproc(Dp, X, Y, s_, b) for s_, b in zip(splits, pat)]
                nc = 1
                for l in alts: nc *= len(l)
                if nc > FC_MAXCOMB:      # too many to search (memory): the sub-bin is split instead
                    continue
                for comb in itertools.product(*alts):
                    comb = list(comb)
                    T = sumRF(Dp, comb + sps + [rf_const(-self.W, 1)])
                    if ckRF(sig, T, b0, b1, self.R): continue
                    G = sympy.gcd(topoly(snum(sig, T)), Pq)
                    if G.degree() < 1: continue
                    G = sympy.Poly(sympy.primitive(G.as_expr())[1], uu)
                    Gl = tolist(G)
                    g1P, rem = sympy.div(Pq, G)
                    if not rem.is_zero: continue
                    g1 = tolist(g1P)
                    if not all(isinstance(x, int) for x in g1): continue
                    m = 0
                    while m < len(g1) and g1[m] == 0: m += 1
                    for sgn in (1, -1):
                        gg = [sgn * x for x in g1]; GG = [sgn * x for x in Gl]
                        if checkPos(gg[m:], nat_sub(len(gg[m:]), 1), b0, b1, self.R):
                            f = (k, GG, gg, m)
                            if f not in out: out.append(f)
        return out

    def sub(self, P, Qp, b0, b1, depth):
        """certificates for [b0, b1] (list of sub-bins), or None"""
        R = self.R
        Dp = detP(P, Qp); X = xP(P, Qp); Y = yP(P, Qp)
        m = lowdeg(Dp) if b0 == 0 else 0
        q = Dp[m:]
        sig = ev(q, (b0 + b1) / 2 / R) > 0
        ok = signOk(sig, Dp, m, b0, b1, R)
        if ok:
            for k, Sd in enumerate(self.side):
                nm = atV((Sd, 0, 0, 0, 1), Dp, X, Y)[0]
                mm = lowdeg(nm) if b0 == 0 else 0
                q2 = nm[mm:]
                q2 = q2 if (not sig) else psmul(-1, q2)
                if checkPos(q2, nat_sub(len(nm[mm:]), 1), b0, b1, R):
                    self.stat['out'] += 1
                    return [(b1, sig, m, ('out', k, mm))]
            cert = self.choose(Dp, X, Y, b0, b1)
            args = (self.D, self.W, sig, Dp, X, Y, b0, b1, R, self.chs, self.cvs, self.crs, self.hbx, self.vbx)
            nc = 1
            for l, bx in list(zip(cert[2], self.hbx)) + list(zip(cert[3], self.vbx)):
                nc *= sum(len(bx[0]) * len(bx[1]) if x[0][0] == 'box' else
                          (len(x[0][1]) * len(x[0][2]) if x[0][0] == 'alt' else 1) for x in l)
            if nc > 16 and depth < self.maxdepth and b1 - b0 >= 2:
                pass
            elif vertOkK(*args, cert):
                self.stat['val'] += 1
                return [(b1, sig, m, ('val', cert))]
            if cert[0]:
                fcs = self.factor_certs(sig, Dp, X, Y, b0, b1, cert)
                if fcs:
                    cert[1] = fcs
                    if vertOkK(*args, cert):
                        self.stat['val'] += 1; self.stat['fc'] = self.stat.get('fc', 0) + 1
                        return [(b1, sig, m, ('val', cert))]
        if depth >= self.maxdepth or b1 - b0 < 2:
            return None
        mid = (b0 + b1) // 2
        a = self.sub(P, Qp, b0, mid, depth + 1)
        if a is None: return None
        b = self.sub(P, Qp, mid, b1, depth + 1)
        if b is None: return None
        self.stat['split'] += 1
        return a + b

    def run(self):
        self.stat = dict(par=0, out=0, val=0, split=0, fail=0)
        self.pins()
        allL = self.side + self.Ls
        U0, U1 = self.box[4], self.box[5]
        certs = []
        for i in range(len(allL)):
            row = []
            for j in range(i + 1, len(allL)):
                Dp = detP(allL[i], allL[j])
                if all(c == 0 for c in Dp):
                    self.stat['par'] += 1; row.append('par'); continue
                c = self.sub(allL[i], allL[j], U0, U1, 0)
                if c is None:
                    self.stat['fail'] += 1
                    return None
                row.append(c)
            certs.append(row)
        self.certs = certs
        return certs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cover'); ap.add_argument('S', type=int); ap.add_argument('R', type=int)
    ap.add_argument('box', nargs=6, type=int)
    ap.add_argument('--maxdepth', type=int, default=8)
    a = ap.parse_args()
    cov = read_cover(a.cover)
    t = time.process_time()
    lf = Leaf(cov, a.S, a.R, *a.box, maxdepth=a.maxdepth)
    if not lf.ok:
        print("wall crosses the box side within the bin"); return
    c = lf.run()
    print(f"claims {len(lf.chs)}+{len(lf.cvs)} segs, {len(lf.crs)} rects; Ls {len(lf.Ls)}; "
          f"{'OK' if c else 'FAIL'} {lf.stat} {time.process_time() - t:.1f}s")


if __name__ == '__main__':
    main()


# ---------------------------------------------------------------- Lean output
def lpoly(p):
    return "[" + ", ".join(str(c) for c in p) + "]"


def lPL(P):
    return f"({lpoly(P[0])}, {lpoly(P[1])}, {lpoly(P[2])})"


def lmode(mo):
    return "none" if mo is None else f"some ({mo[0]}, {mo[1]})"


def lck(ck):
    return "CK.std" if ck[0] == 'std' else f"(CK.{ck[0]} {ck[1]} {ck[2]} {ck[3]} {ck[4]})"


def lrm(rm):
    return f"({ltup(rm[0])}, {lmode(rm[1])}, {lmode(rm[2])}, {lck(rm[3])})"


def ltup(t):
    return "(" + ", ".join(str(x) for x in t) + ")"


def lnat(xs):
    return "[" + ", ".join(str(x) for x in xs) + "]"


def lsegc(o):
    if o[0] == 'drop': return ".drop"
    if o[0] == 'box': return ".box"
    return f"(.alt {lnat(o[1])} {lnat(o[2])})"


def ltag(t):
    return "none" if t is None else f"some ({t[0]}, {'true' if t[1] else 'false'})"


def lcapa(a):
    if a[0] in ('zeroC', 'par', 'linC'): return "." + a[0]
    if a[0] == 'parT': return f"(.parT {a[1]} {'true' if a[2] else 'false'})"
    return f"(.{a[0]} {a[1]})"


def lSL(L):
    return f"⟨{lPL(L[0])}, {L[1]}, {L[2]}, {L[3]}, {L[4]}⟩"


def lbx(b):
    return f"({lnat(b[0])}, {lnat(b[1])})"


def lvcert(c):
    splits, fcs, hc, vc, lc = c
    sp = ", ".join(f"⟨{lSL(q)}, {nm}, {dm}, {np_}, {dp}⟩" for q, nm, dm, np_, dp in splits)
    fc = ", ".join(f"⟨{k}, {lpoly(G)}, {lpoly(g1)}, {m}⟩" for k, G, g1, m in fcs)
    h = ", ".join("[" + ", ".join(f"({lsegc(x[0])}, {ltag(x[1])})" for x in l) + "]" for l in hc)
    v = ", ".join("[" + ", ".join(f"({lsegc(x[0])}, {ltag(x[1])})" for x in l) + "]" for l in vc)
    l_ = ", ".join(f"([{', '.join(lcapa(a) for a in xs)}], [{', '.join(lcapa(a) for a in ys)}])" for xs, ys in lc)
    return f"⟨[{sp}], [{fc}], [{h}], [{v}], [{l_}]⟩"


def lsub(sb):
    b1, sig, m, kind = sb
    if kind[0] == 'out':
        k = f".out {kind[1]} {kind[2]}"
    else:
        k = f"(.val {lvcert(kind[1])})"
    return f"⟨{b1}, {'true' if sig else 'false'}, {m}, {k}⟩"


def lcert(c):
    if c == 'par':
        return ".par"
    return ".bins [" + ", ".join(lsub(sb) for sb in c) + "]"


def to_lean(lf, name):
    rows = ",\n    ".join("[" + ", ".join(lcert(c) for c in row) + "]" for row in lf.certs)
    return (f"def {name} : ExLeaf where\n"
            f"  wx := {'true' if lf.wx else 'false'}\n  wy := {'true' if lf.wy else 'false'}\n"
            f"  chs := [{', '.join(ltup(e) for e in lf.chs)}]\n"
            f"  cvs := [{', '.join(ltup(e) for e in lf.cvs)}]\n"
            f"  crs := [{', '.join(lrm(r) for r in lf.crs)}]\n"
            f"  Ls := [{', '.join(lPL(P) for P in lf.Ls)}]\n"
            f"  hbx := [{', '.join(lbx(b) for b in lf.hbx)}]\n"
            f"  vbx := [{', '.join(lbx(b) for b in lf.vbx)}]\n"
            f"  certs := [\n    {rows}]\n"
            + ("  ex := true\n" if lf.ex else "") + ("  ey := true\n" if lf.ey else "")
            + lcred(getattr(lf, 'cred', None)))


def lcred(cr):
    """the `cred` field: `(rect, G, h, amt, strips)`"""
    if cr is None:
        return ""
    e, G, h, amt, strips = cr
    return (f"  cred := some ⟨{ltup(e)}, {G}, {h}, {amt},\n    [{', '.join(ltup(t) for t in strips)}]⟩\n")



SPLIT_MIN = int(os.environ.get('V7_SPLIT_MIN', '64'))   # a pair with more combinations is split
SPLIT_CHUNK = int(os.environ.get('V7_SPLIT_CHUNK', '64'))  # combinations per kernel check


def _nalts(sc, bx):
    """the number of terms of `segCAltsK` for a segment certificate"""
    if sc[0] == 'drop': return 1
    if sc[0] == 'box': return len(bx[0]) * len(bx[1])
    return len(sc[1]) * len(sc[2])


def n_combos(lf, v, pat):
    """`(vL c D chs cvs crs hbx vbx v pat).length` (`LemmaESplit.vL`)"""
    n = 1
    for bx, l in zip(lf.hbx, v[2]):
        n *= sum(_nalts(x[0], bx) for x in l if tagOk(pat, x[1]))
    for bx, l in zip(lf.vbx, v[3]):
        n *= sum(_nalts(x[0], bx) for x in l if tagOk(pat, x[1]))
    for r, (xs, ys) in zip(lf.crs, v[4]):
        k = 1 if r[3][0] == 'std' else 2
        n *= k * sum(1 for ax in xs if tagOk(pat, capTag(ax))) * sum(1 for ay in ys if tagOk(pat, capTag(ay)))
    return n


def pair_combos(lf, cert):
    if not isinstance(cert, list): return 0
    return sum(n_combos(lf, sb[3][1], p) for sb in cert if sb[3][0] == 'val' for p in pats(len(sb[3][1][0])))


def pair_split(lf, name, i, j, cert, sctx, P, U0, U1, W, D, R):
    """the pair theorem `{name}_{i}_{j}` from one kernel check per sub-bin, and per chunk of
    combinations of a heavy sub-bin (`LemmaESplit`)"""
    dk = "by decide +kernel"
    q0 = "((([0], [0], [0]) : PL), PairCert.par)"
    X = f"(({name}_Z {i}).getD {j} {q0})"
    S = f"(sbsOf {X}.2)"
    Q = f"{X}.1"
    nm = f"{name}_{i}_{j}"
    m = SPLIT_CHUNK
    out = []
    lists = f"{name}.chs {name}.cvs {name}.crs {name}.hbx {name}.vbx"
    for t, sb in enumerate(cert):
        sbT = f"({S}.getD {t} dSB)"
        b0T = f"(bAt {U0} {S} {t})"
        stmt = f"subOk {sctx} {P} {Q} {b0T} {sbT} = true"
        v = sb[3][1] if sb[3][0] == 'val' else None
        if v is None or sum(n_combos(lf, v, p) for p in pats(len(v[0]))) <= m:
            out.append(f"theorem {nm}_s{t} : {stmt} := {dk}\n")
            continue
        c, vv = f"{nm}_c{t}", f"{nm}_v{t}"
        out.append(f"def {c} : LemmaEK.Ctx := LemmaEK.mkCtx (detP {P} {Q}) (xP {P} {Q}) (yP {P} {Q}) {b0T} {sbT}.b1 {R} LemmaEK.kK\n")
        out.append(f"def {vv} : VCert := vcOf {sbT}.kind\n")
        out.append(f"theorem {nm}_s{t}_h : vHead {c} {D} {sbT}.σ {lists} {vv} = true := {dk}\n")
        ps = pats(len(v[0]))
        PA = f"(pats {vv}.splits.length)"
        Lf = lambda pt: f"(vL {c} {D} {lists} {vv} {pt})"
        Ff = lambda pt: f"(vF {c} ({W}) {sbT}.σ {b0T} {sbT}.b1 {R} {vv} {pt})"
        terms = []
        for p, pat in enumerate(ps):
            pt = f"({PA}.getD {p} [])"
            n = n_combos(lf, v, pat)
            ks = list(range(0, n, m))
            out.append(f"theorem {nm}_s{t}_p{p} : vPre {vv} {pt} = true := {dk}\n")
            for k in ks:
                out.append(f"theorem {nm}_s{t}_p{p}_k{k} : (({Lf(pt)}.drop {k}).take {m}).all {Ff(pt)} = true := {dk}\n")
            tc = f"all_drop_end {Ff(pt)} {Lf(pt)} {len(ks) * m} ({dk})"
            for k in reversed(ks):
                tc = f"all_chunk_step {Ff(pt)} {Lf(pt)} {k} {m} {nm}_s{t}_p{p}_k{k}\n      ({tc})"
            terms.append(f"and_of {nm}_s{t}_p{p} (all_of_drop_zero ({tc}))")
        G = f"(fun pat => vPre {vv} pat && {Lf('pat')}.all {Ff('pat')})"
        tp = f"all_drop_end {G} {PA} {len(ps)} ({dk})"
        for p in reversed(range(len(ps))):
            tp = f"all_drop_step {G} {PA} {p} [] ({dk})\n    ({terms[p]})\n    ({tp})"
        out.append(f"theorem {nm}_s{t} : {stmt} :=\n  subOk_of_val ({dk}) ({dk}) ({dk}) ({dk})\n"
                   f"    (vertOkK'_of {nm}_s{t}_h\n    ({tp}))\n")
    tb = f"binsOk_end {len(cert)} ({dk}) ({dk})"
    for t in reversed(range(len(cert))):
        tb = f"binsOk_step {t} ({dk}) {nm}_s{t}\n    ({tb})"
    out.append(f"theorem {nm} : {name}_p {i} {X} = true :=\n  pairOk_of_sbs ({dk})\n    ({tb})\n")
    return "\n".join(out)


def pair_subX(name, i, j, cert, sctx, P, U0):
    """`LemmaELeafX`: the pair theorem `{name}_{i}_{j}` from one kernel check per sub-bin"""
    dk = "by decide +kernel"
    q0 = "((([0], [0], [0]) : PL), PairCert.par)"
    X = f"(({name}_Z {i}).getD {j} {q0})"
    S = f"(sbsOf {X}.2)"
    nm = f"{name}_{i}_{j}"
    out = [f"theorem {nm}_s{t} : subOkX {sctx} {P} {X}.1 (bAt {U0} {S} {t}) ({S}.getD {t} dSB) = true := {dk}\n"
           for t in range(len(cert))]
    tb = f"binsOkX_end {len(cert)} ({dk}) ({dk})"
    for t in reversed(range(len(cert))):
        tb = f"binsOkX_step {t} ({dk}) {nm}_s{t}\n    ({tb})"
    out.append(f"theorem {nm} : {name}_p {i} {X} = true :=\n  pairOkX_of_sbs ({dk})\n    ({tb})\n")
    return "\n".join(out)


def to_lean_parts(lf, name, segs="tsegs", rects="trects", X=False):
    """The leaf in parts: the definitions with the head theorem, one block per row (its pair
    theorems and the row theorem), and the `exOk` theorem gluing the rows.  `X`: through
    `LemmaELeafX` (the vertex test by the rows' minima, `exOkX`)."""
    x = "X" if X else ""
    x0, x1, y0, y1, U0, U1 = lf.box
    D, S, R, Q = lf.D, lf.S, lf.R, lf.Q
    W = getattr(lf, 'W0', lf.W)
    side = f"(sideE {Q} {x0} {x1} {y0} {y1} {name}.wx {name}.wy {name}.ex {name}.ey)"
    ctx = f"{D} ({W} - credAmt {name}) {R} {U0} {U1} {side} {name}.chs {name}.cvs {name}.crs {name}.hbx {name}.vbx"
    d0 = "(([0], [0], [0]) : PL)"
    q0 = "((([0], [0], [0]) : PL), PairCert.par)"
    n = len(lf.side) + len(lf.Ls)
    dk = "by decide +kernel"
    args = f"{D} {S} {R} {W} {x0} {x1} {y0} {y1} {U0} {U1} {segs} {rects} {name}"
    defs = [to_lean(lf, name),
            f"def {name}_L : List PL := {side} ++ {name}.Ls\n",
            f"def {name}_Z (i : ℕ) : List (PL × PairCert) := ({name}_L.drop (i + 1)).zip ({name}.certs.getD i [])\n",
            f"def {name}_p (i : ℕ) : PL × PairCert → Bool := fun q => pairOk{x} {ctx} ({name}_L.getD i {d0}) q.1 q.2\n",
            f"theorem {name}_head : exHead {args} = true := {dk}\n"]
    rows = []
    for i in range(n):
        out = []
        m = len(lf.certs[i]) if i < len(lf.certs) else 0
        for j in range(m):
            cert = lf.certs[i][j]
            if X and isinstance(cert, list):
                out.append(pair_subX(name, i, j, cert,
                                     f"{D} ({W} - credAmt {name}) {R} {side} {name}.chs {name}.cvs {name}.crs "
                                     f"{name}.hbx {name}.vbx", f"({name}_L.getD {i} {d0})", U0))
                continue
            if not X and pair_combos(lf, cert) > SPLIT_MIN:
                out.append(pair_split(lf, name, i, j, cert,
                                      f"{D} ({W} - credAmt {name}) {R} {side} {name}.chs {name}.cvs {name}.crs "
                                      f"{name}.hbx {name}.vbx", f"({name}_L.getD {i} {d0})",
                                      U0, U1, f"{W} - credAmt {name}", D, R))
                continue
            out.append(f"theorem {name}_{i}_{j} : {name}_p {i} (({name}_Z {i}).getD {j} {q0}) = true := {dk}\n")
        t = f"all_drop_end ({name}_p {i}) ({name}_Z {i}) {m} ({dk})"
        for j in reversed(range(m)):
            t = f"all_drop_step ({name}_p {i}) ({name}_Z {i}) {j} {q0} ({dk}) {name}_{i}_{j}\n    ({t})"
        out.append(f"theorem {name}_r{i} : rowOk{x} {ctx} ({name}_L.getD {i} {d0}) ({name}_L.drop {i + 1}) "
                   f"({name}.certs.getD {i} []) = true :=\n  rowOk{x}_of ({dk})\n    ({t})\n")
        rows.append("\n".join(out))
    t = f"allPairsOk{x}_drop_end {name}_L ({name}.certs.drop {n}) {n} ({dk})"
    for i in reversed(range(n)):
        t = f"allPairsOk{x}_drop_step {name}_L {name}.certs {i} {d0} ({dk}) ({dk}) {name}_r{i}\n    ({t})"
    ok = f"theorem {name}_ok : exOk{x} {args} = true :=\n  exOk{x}_of {name}_head\n    ({t})\n"
    return "\n".join(defs), rows, ok


def to_lean_split(lf, name, segs="tsegs", rects="trects", rows_only=False):
    """The leaf and its `exOk` theorem in one block (see `to_lean_parts`)."""
    defs, rows, ok = to_lean_parts(lf, name, segs, rects)
    return "\n".join([defs] + rows + [ok])