"""The vertex test by the rows' minima (`LemmaEKM.vertOkM`, `rowOkM`, `RowMinK.rmLoop`), mirrored.

`kmirror.vertOkK` sums every combination of the segments' alternatives; here all terms are raised
to one common denominator and degree and the digits base `2ᴷ` of the rows' minima are tested, so
the cost is the number of terms.  The fallback of `vertOkM` (the combinations, `vertOkK`) is not
tried here: a sub-bin passes only through the minima.
"""
from math import gcd

from kmirror import (KK, Ctx, KR, kconst, kraise_h, segCOkK, capAOkK, segCAltsK, lebRFsK, sprocK,
                     reordK)
from lemmae_mirror import capXm, capYm, hUps, hLos, vUps, vLos, pats, tagOk, capTag, nat_sub


def lcm(a, b): return a * b // gcd(a, b)


def balD(K, v):
    X = 2 ** K
    r = v % X
    return r if r < 2 ** (K - 1) else r - X


def rowOkM(c, sigma, rows, fx):
    ts = [r for l in rows for r in l] + fx
    E = max((r.e for r in ts), default=0)
    I = max((r.i for r in ts), default=0)
    J = max((r.j for r in ts), default=0)
    Kx = max((r.k for r in ts), default=0)
    L = 1
    for r in ts:
        if r.d == 0:
            return False
        L = lcm(L, r.d)
    rz = {id(r): kraise_h(c, r, E - r.e, I - r.i, J - r.j, Kx - r.k, L // r.d) for r in ts}
    N = max((rz[id(r)][1] for r in ts), default=0)
    eps = 1 if (sigma or E % 2 == 0) else -1
    lift = {}
    for r in ts:
        h = rz[id(r)]
        h = c.hadd(h, (0, N, 0))
        if not 2 * h[2] * c.M ** N < 2 ** c.K:
            return False
        lift[id(r)] = h[0]
    vr = [[lift[id(r)] for r in l] for l in rows]
    vf = [lift[id(r)] for r in fx]
    K = c.K
    for _ in range(N + 2):
        s = sum(min((eps * balD(K, v) for v in l), default=0) for l in vr) + sum(eps * balD(K, v) for v in vf)
        if s < 0:
            return False
        vr = [[(v - balD(K, v)) >> K for v in l] for l in vr]
        vf = [(v - balD(K, v)) >> K for v in vf]
    return True


def vertOkM(Dn, W, sigma, D, X, Y, b0, b1, R, chs, cvs, crs, hbx, vbx, cert, K=KK):
    """`LemmaEK.vertOkM` without its fallback"""
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
        if not rowOkM(c, sigma, reordK(alts), sps + [kconst(-W, 1)]):
            return False
    return True
