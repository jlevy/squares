"""The vertex test in Kronecker form (`LemmaEK.vertOkK`, `KBern.hcheck`), mirrored exactly.

A polynomial `p` of formal degree `n` is carried as `(v, n, b)` with `v = Bⁿ p(A/B)`, `A = b0 + b1 2ᴷ`,
`B = R (1 + 2ᴷ)`, `b ≥ Σ|pᵢ|`; the sign test is one `&` with a mask.  A rational function is a `KR`:
its image, its exponents `(e, i, j, k, d)` and a thunk giving the list form (`lemmae_mirror`), which
only the common-factor certificates need.
"""
from itertools import product
from math import gcd

import lemmae_mirror as M
from lemmae_mirror import (Cp, Sp, Np, sSL, cSL, sl_cst, sl_sub, atV, capX, capY, capXm, capYm, hUps, hLos,
                           vUps, vLos, pats, tagOk, capTag, splitAt, fcOk, nat_sub, rf_const, rf_add, rf_mul,
                           rf_neg, raise_, pmul)

KK = 1024          # LemmaEK.kK


# ------------------------------------------------------------------ KBern
def hconst(c): return (c, 0, abs(c))


class Ctx:
    def __init__(self, D, X, Y, b0, b1, R, K=KK):
        self.A = b0 + b1 * 2 ** K
        self.B = R * (1 + 2 ** K)
        self.K, self.M = K, max(b0 + b1, 2 * R)
        self.D, self.X, self.Y = D, X, Y
        self._bp = {0: 1}
        self.hD, self.hX, self.hY = self.hP(D), self.hP(X), self.hP(Y)
        self.hC, self.hS, self.hN = self.hP(Cp), self.hP(Sp), self.hP(Np)
        self._pw = {}
        self._mask = {}

    def bpow(self, n):
        v = self._bp.get(n)
        if v is None:
            v = self._bp[n] = self.B ** n
        return v

    def hP(self, p):
        if not p:
            return (0, 0, 0)
        out = hconst(p[-1])
        for a in reversed(p[:-1]):
            v, n, c = out
            out = (a * self.bpow(n + 1) + self.A * v, n + 1, abs(a) + c)
        return out

    def hadd(self, p, q):
        if p[1] == q[1]:
            return (p[0] + q[0], p[1], p[2] + q[2])
        if p[1] < q[1]:
            return (p[0] * self.bpow(q[1] - p[1]) + q[0], q[1], p[2] + q[2])
        return (p[0] + q[0] * self.bpow(p[1] - q[1]), p[1], p[2] + q[2])

    def hpow(self, p, n):
        if n == 0: return hconst(1)
        out = p
        for _ in range(n - 1):
            out = hmul(p, out)
        return out

    def hpowc(self, which, n):
        key = (which, n)
        v = self._pw.get(key)
        if v is None:
            v = self._pw[key] = self.hpow({'D': self.hD, 'C': self.hC, 'S': self.hS, 'N': self.hN}[which], n)
        return v

    def mask(self, L):
        m = self._mask.get(L)
        if m is None:
            m = 0
            for _ in range(L):
                m = 2 ** (self.K - 1) + 2 ** self.K * m
            self._mask[L] = m
        return m

    def hcheck(self, neg, h):
        v = -h[0] if neg else h[0]
        return (0 < self.K and 2 * h[2] * self.M ** h[1] < 2 ** self.K and v >= 0
                and (v & self.mask(h[1] + 2)) == 0)


def hmul(p, q):
    if q[1] == 0 and q[0] == 1 and q[2] == 1: return p
    if p[1] == 0 and p[0] == 1 and p[2] == 1: return q
    return (p[0] * q[0], p[1] + q[1], p[2] * q[2])


def hsmul(c, p): return (c * p[0], p[1], abs(c) * p[2])


# ------------------------------------------------------------------ KR / KSL
class KR:
    __slots__ = ('h', 'e', 'i', 'j', 'k', 'd', '_f', '_r', '_raised')

    def __init__(self, h, e, i, j, k, d, f):
        self.h, self.e, self.i, self.j, self.k, self.d, self._f, self._r = h, e, i, j, k, d, f, None
        self._raised = None

    @property
    def r(self):
        if self._r is None:
            self._r = self._f()
        return self._r


def kRF(c, r): return KR(c.hP(r[0]), r[1], r[2], r[3], r[4], r[5], lambda: r)


def kconst(n, d): return KR(hconst(n), 0, 0, 0, 0, d, lambda: rf_const(n, d))


def kraise_h(c, r, a, b, cc, g, m):
    if a == 0 and b == 0 and cc == 0 and g == 0 and m == 1:
        return hmul(hsmul(1, r.h), hconst(1))
    key = (a, b, cc, g, m)
    if r._raised is None:
        r._raised = {}
    v = r._raised.get(key)
    if v is None:
        v = r._raised[key] = hmul(hsmul(m, r.h), hmul(c.hpowc('D', a), hmul(c.hpowc('C', b),
                                                                            hmul(c.hpowc('S', cc), c.hpowc('N', g)))))
    return v


def kadd(c, r, s):
    e, i, j, k = max(r.e, s.e), max(r.i, s.i), max(r.j, s.j), max(r.k, s.k)
    l = r.d * s.d // gcd(r.d, s.d)
    h = c.hadd(kraise_h(c, r, e - r.e, i - r.i, j - r.j, k - r.k, l // r.d),
               kraise_h(c, s, e - s.e, i - s.i, j - s.j, k - s.k, l // s.d))
    return KR(h, e, i, j, k, l, lambda: rf_add(c.D, r.r, s.r))


def kmul(r, s):
    return KR(hmul(r.h, s.h), r.e + s.e, r.i + s.i, r.j + s.j, r.k + s.k, r.d * s.d, lambda: rf_mul(r.r, s.r))


def kneg(r): return KR(hsmul(-1, r.h), r.e, r.i, r.j, r.k, r.d, lambda: rf_neg(r.r))


def ckK(c, sigma, r): return c.hcheck(not (sigma or r.e % 2 == 0), r.h)


class KSL:
    __slots__ = ('P1', 'P2', 'P3', 's')

    def __init__(self, P1, P2, P3, s):
        self.P1, self.P2, self.P3, self.s = P1, P2, P3, s


def kSL(c, L): return KSL(c.hP(L[0][0]), c.hP(L[0][1]), c.hP(L[0][2]), L)


def kden(c, L):
    s = L.s
    return hmul(c.hpowc('C', s[1]), hmul(c.hpowc('S', s[2]), hmul(c.hpowc('N', s[3]), hconst(s[4]))))


def ksub(c, L, Mx):
    dM, dL = kden(c, Mx), kden(c, L)
    return KSL(c.hadd(hmul(dM, L.P1), hsmul(-1, hmul(dL, Mx.P1))),
               c.hadd(hmul(dM, L.P2), hsmul(-1, hmul(dL, Mx.P2))),
               c.hadd(hmul(dM, L.P3), hsmul(-1, hmul(dL, Mx.P3))), sl_sub(L.s, Mx.s))


def katV(c, L):
    s = L.s
    h = c.hadd(c.hadd(hmul(L.P1, c.hX), hmul(L.P2, c.hY)), hmul(L.P3, c.hD))
    return KR(h, 1, s[1], s[2], s[3], s[4], lambda: atV(s, c.D, c.X, c.Y))


# ------------------------------------------------------------------ the vertex test
def kget(c, Ls, i): return kSL(c, Ls[i] if i < len(Ls) else sl_cst(0, 1))


def segValK(c, w, Dn, ln, ups, los, iu, il):
    return kmul(kconst(w * Dn, ln), katV(c, ksub(c, kget(c, ups, iu), kget(c, los, il))))


def ghOkK(c, sigma, cap, mode):
    if mode == 0: return ckK(c, sigma, katV(c, ksub(c, kSL(c, sl_cst(0, 1)), kSL(c, cap))))
    if mode == 1: return True
    return ckK(c, sigma, katV(c, ksub(c, kSL(c, cap), kSL(c, sSL(1)))))


def ghUK(c, cap, mode):
    if mode == 0: return kconst(0, 1)
    if mode == 1:
        return kmul(kmul(katV(c, kSL(c, cap)), katV(c, kSL(c, cap))), kRF(c, (pmul(Np, Np), 0, 1, 1, 0, 2)))
    return kmul(katV(c, ksub(c, kSL(c, cap), kSL(c, sSL(2)))), kRF(c, (Np, 0, 1, 0, 0, 1)))


def segOkAK(c, sigma, ups, los, Ua, La):
    if not Ua or not La or not all(a < len(ups) for a in Ua) or not all(b < len(los) for b in La):
        return False
    return all(any(ckK(c, sigma, katV(c, ksub(c, kSL(c, U), kget(c, ups, a)))) for a in Ua) for U in ups) and \
        all(any(ckK(c, sigma, katV(c, ksub(c, kget(c, los, b), kSL(c, L)))) for b in La) for L in los)


def segAltsK(c, w, Dn, ln, ups, los, Ua, La):
    return [segValK(c, w, Dn, ln, ups, los, a, b) for a in Ua for b in La]


def segCAltsK(c, w, Dn, ln, ups, los, bx, sc):
    if sc[0] == 'drop': return [kconst(0, 1)]
    if sc[0] == 'box': return segAltsK(c, w, Dn, ln, ups, los, bx[0], bx[1])
    return segAltsK(c, w, Dn, ln, ups, los, sc[1], sc[2])


def segCOkK(c, sigma, ups, los, bx, sc):
    if sc[0] == 'drop': return True
    if sc[0] == 'box':
        return bool(bx[0]) and bool(bx[1]) and all(a < len(ups) for a in bx[0]) and all(b < len(los) for b in bx[1])
    return segOkAK(c, sigma, ups, los, sc[1], sc[2])


def sprocK(c, sp, b):
    q, nm, dm, np_, dp = sp
    if b: return kneg(kmul(kconst(np_, dp), katV(c, kSL(c, q))))
    return kmul(kconst(nm, dm), katV(c, kSL(c, q)))


def capAOkK(c, sigma, splits, cap, a):
    if a[0] == 'zeroC': return ghOkK(c, sigma, cap, 0)
    if a[0] == 'par': return True
    if a[0] == 'parT': return a[1] < len(splits)
    if a[0] == 'linC': return ghOkK(c, sigma, cap, 2)
    if a[0] == 'zeroT': return a[1] < len(splits) and splitAt(splits, a[1]) == cap
    return a[1] < len(splits) and splitAt(splits, a[1]) == sl_sub(cap, sSL(1))


def capAUK(c, cap, a):
    return ghUK(c, cap, {'zeroC': 0, 'zeroT': 0, 'par': 1, 'parT': 1, 'linC': 2, 'linT': 2}[a[0]])


def lebRFK(c, Dn, r, ax, ay):
    return kmul(kconst(r[0][4], 1), kadd(c, kadd(c, kconst(1, 1), kneg(capAUK(c, capXm(Dn, r), ax))),
                                        kneg(capAUK(c, capYm(Dn, r), ay))))


def slAtPK(c, L, x, y, q):
    K_ = kSL(c, L)
    h = c.hadd(c.hadd(hsmul(x, K_.P1), hsmul(y, K_.P2)), hsmul(q, K_.P3))
    return KR(h, 0, L[1], L[2], L[3], L[4] * q, lambda: M.slAtP(L, x, y, q))


def mcRFK(c, A, B, bs, al, be):
    t1 = kmul(kmul(kconst(2, 1), kRF(c, M.cRF)), kadd(c, kadd(c, kmul(A, be), kmul(B, al)), kneg(kmul(A, B))))
    t2 = kmul(kRF(c, M.sRF), kadd(c, kmul(kmul(kconst(2, 1), bs), be), kneg(kmul(bs, bs))))
    t3 = kneg(kmul(kRF(c, M.sRF), kmul(al, al)))
    return kmul(kRF(c, M.i2cRF), kadd(c, kadd(c, t1, t2), t3))


def lebRFsK(c, Dn, r, ax, ay):
    w = kconst(r[0][4], 1)
    gx = kneg(capAUK(c, capXm(Dn, r), ax))
    gy = kneg(capAUK(c, capYm(Dn, r), ay))
    ck = r[3]
    if ck[0] == 'std':
        return [lebRFK(c, Dn, r, ax, ay)]
    _, xa, ya, ym, q = ck
    if ck[0] == 'c3':
        aL = sl_sub(capX(Dn, r[0][0]), sSL(1)); bL = capY(Dn, r[0][1])
        mc = mcRFK(c, slAtPK(c, aL, xa, ya, q), slAtPK(c, bL, xa, ya, q), slAtPK(c, bL, xa, ym, q),
                   katV(c, kSL(c, sl_sub(capXm(Dn, r), sSL(1)))), katV(c, kSL(c, capYm(Dn, r))))
        return [kmul(w, kadd(c, kadd(c, kadd(c, kconst(1, 1), gx), gy), mc)), kmul(w, kadd(c, kconst(1, 1), gx))]
    aL = capX(Dn, r[0][0]); bL = sl_sub(capY(Dn, r[0][1]), cSL(1))
    mc = mcRFK(c, slAtPK(c, aL, xa, ya, q), slAtPK(c, bL, xa, ya, q), slAtPK(c, bL, xa, ym, q),
               katV(c, kSL(c, capXm(Dn, r))), katV(c, kSL(c, sl_sub(capYm(Dn, r), cSL(1)))))
    return [kmul(w, kadd(c, kadd(c, kconst(1, 1), gy), mc)), lebRFK(c, Dn, r, ax, ay)]


def sumK(c, rs):
    out = kconst(0, 1)
    for r in reversed(rs):
        out = kadd(c, r, out)
    return out


def totOkK(c, sigma, b0, b1, R, splits, pat, fcs, T):
    return ckK(c, sigma, T) or any(fcOk(sigma, c.D, c.X, c.Y, b0, b1, R, splits, pat, f, T.r) for f in fcs)


def cprod(Ls):
    out = [[]]
    for l in reversed(Ls):
        out = [[a] + x for a in l for x in out]
    return out


def reordK(L):
    return [l for l in L if len(l) != 1] + [l for l in L if len(l) == 1]


def vertOkK(Dn, W, sigma, D, X, Y, b0, b1, R, chs, cvs, crs, hbx, vbx, cert, K=KK):
    """`LemmaEK.vertOkK D W σ Δ X Y b0 b1 R K chs cvs crs hbx vbx c`"""
    splits, fcs, hc, vc, lc = cert
    if len(hbx) != len(chs) or len(vbx) != len(cvs) or len(hc) != len(chs) or len(vc) != len(cvs) or len(lc) != len(crs):
        return False
    if not all(sp[2] != 0 and sp[4] != 0 for sp in splits): return False
    c = Ctx(D, X, Y, b0, b1, R, K)
    for e, bx, l in zip(chs, hbx, hc):
        if not all(segCOkK(c, sigma, hUps(Dn, e), hLos(Dn, e), bx, x[0]) for x in l): return False
    for e, bx, l in zip(cvs, vbx, vc):
        if not all(segCOkK(c, sigma, vUps(Dn, e), vLos(Dn, e), bx, x[0]) for x in l): return False
    for r, (xs, ys) in zip(crs, lc):
        if not all(capAOkK(c, sigma, splits, capXm(Dn, r), a) for a in xs): return False
        if not all(capAOkK(c, sigma, splits, capYm(Dn, r), a) for a in ys): return False
    for pat in pats(len(splits)):
        if not all(any(tagOk(pat, x[1]) for x in l) for l in hc): return False
        if not all(any(tagOk(pat, x[1]) for x in l) for l in vc): return False
        if not all(any(tagOk(pat, capTag(a)) for a in xs) and any(tagOk(pat, capTag(a)) for a in ys) for xs, ys in lc):
            return False
        alts = []
        for e, bx, l in zip(chs, hbx, hc):
            alts.append([t for x in l if tagOk(pat, x[1])
                         for t in segCAltsK(c, e[4], Dn, nat_sub(e[2], e[0]), hUps(Dn, e), hLos(Dn, e), bx, x[0])])
        for e, bx, l in zip(cvs, vbx, vc):
            alts.append([t for x in l if tagOk(pat, x[1])
                         for t in segCAltsK(c, e[4], Dn, nat_sub(e[3], e[1]), vUps(Dn, e), vLos(Dn, e), bx, x[0])])
        for r, (xs, ys) in zip(crs, lc):
            alts.append([t for ax in xs if tagOk(pat, capTag(ax))
                         for ay in ys if tagOk(pat, capTag(ay)) for t in lebRFsK(c, Dn, r, ax, ay)])
        sps = [sprocK(c, sp, b) for sp, b in zip(splits, pat)]
        # `sumK` folds from the right: the singletons (last after `reordK`) and the tail are one
        # shared suffix, the same term for every combination
        multi = [l for l in alts if len(l) != 1]
        base = sumK(c, [l[0] for l in alts if len(l) == 1] + sps + [kconst(-W, 1)])
        for comb in product(*multi):     # = cprod(multi), lazily
            T = base
            for r in reversed(comb):  # noqa: B007
                T = kadd(c, r, T)
            if not totOkK(c, sigma, b0, b1, R, splits, pat, fcs, T):
                return False
    return True
