#!/usr/bin/env python3
"""The vertex test without the combinations (a prototype).

`kmirror.vertOkK` tests every combination of the segments' alternatives: the sum of one term per
row, over the combination's common denominator, has Kronecker digits `>= 0`.  Here every term is
raised to the common denominator of all the rows and to a common degree (multiplying by powers of
`B = R (1 + 2^K)`, a polynomial with nonnegative coefficients in the Kronecker variable), and each
row is replaced by the coefficient-wise minimum of its terms.  If the sum of the minima has digits
`>= 0`, so has every combination's sum over that denominator, so the bound holds at every point of
the sub-bin; the cost is the number of terms, not the number of combinations.

    rowmin.py PKL [PKL ...]     prints, per root, the sub-bins with combinations and how many pass
"""
import pickle, sys, time
from math import gcd
from types import SimpleNamespace

import kmirror as KM
from kmirror import (Ctx, kraise_h, kconst, segCAltsK, segCOkK, capAOkK, lebRFsK, sprocK, hUps, hLos,
                     vUps, vLos, capXm, capYm, pats, tagOk, capTag, nat_sub)
import gen_exact as G


def digits(v, n, K):
    """the signed base-`2^K` digits `c_0 .. c_n` of `v = sum c_i 2^(K i)`"""
    out, base, half = [], 1 << K, 1 << (K - 1)
    for _ in range(n + 1):
        d = v % base
        if d >= half:
            d -= base
        out.append(d)
        v = (v - d) >> K
    assert v == 0, "digits overflow"
    return out


def rowmin_ok(c, sigma, rows, fixed):
    """every combination of `rows` (one term each) plus `fixed` passes, by the row minima"""
    terms = [r for row in rows for r in row] + fixed
    E = max(r.e for r in terms); I = max(r.i for r in terms)
    J = max(r.j for r in terms); Kk = max(r.k for r in terms)
    L = 1
    for r in terms:
        L = L * r.d // gcd(L, r.d)
    raised = {}
    for r in terms:
        raised[id(r)] = kraise_h(c, r, E - r.e, I - r.i, J - r.j, Kk - r.k, L // r.d)
    N = max(h[1] for h in raised.values())

    def vec(r):
        v, n, _ = raised[id(r)]
        return digits(v * c.bpow(N - n), N, c.K)

    tot = [0] * (N + 1)
    for row in rows:
        vs = [vec(r) for r in row]
        for i in range(N + 1):
            tot[i] += min(x[i] for x in vs)
    for r in fixed:
        for i, x in enumerate(vec(r)):
            tot[i] += x
    neg = not (sigma or E % 2 == 0)
    return all((-x if neg else x) >= 0 for x in tot)


def sub_rowmin(lf, sb, D, X, Y, b0):
    """`vertOkK` of a `val` sub-bin with the row minima in place of the combinations"""
    b1, sigma, _m, (_, cert) = sb
    Dn, W, R = lf.D, getattr(lf, 'W', 0), lf.R
    splits, fcs, hc, vc, lc = cert
    c = Ctx(D, X, Y, b0, b1, R)
    ok = True
    for pat in pats(len(splits)):
        rows = []
        for e, bx, l in zip(lf.chs, lf.hbx, hc):
            rows.append([t for x in l if tagOk(pat, x[1])
                         for t in segCAltsK(c, e[4], Dn, nat_sub(e[2], e[0]), hUps(Dn, e), hLos(Dn, e), bx, x[0])])
        for e, bx, l in zip(lf.cvs, lf.vbx, vc):
            rows.append([t for x in l if tagOk(pat, x[1])
                         for t in segCAltsK(c, e[4], Dn, nat_sub(e[3], e[1]), vUps(Dn, e), vLos(Dn, e), bx, x[0])])
        for r, (xs, ys) in zip(lf.crs, lc):
            rows.append([t for ax in xs if tagOk(pat, capTag(ax))
                         for ay in ys if tagOk(pat, capTag(ay)) for t in lebRFsK(c, Dn, r, ax, ay)])
        fixed = [sprocK(c, sp, b) for sp, b in zip(splits, pat)] + [kconst(-W, 1)]
        ok = ok and rowmin_ok(c, sigma, rows, fixed)
    return ok


def main(paths):
    from lemmae_mirror import detP, xP, yP   # the pair's polynomials
    for p in paths:
        d = pickle.load(open(p, 'rb'))
        t0 = time.time()
        n = npass = big = bigpass = 0
        for cd in d['leaves'].values():
            if not isinstance(cd, dict) or 'certs' not in cd:
                continue
            lf = SimpleNamespace(**cd)
            Ls = list(lf.side) + list(lf.Ls)
            for i, row in enumerate(lf.certs):
                for j, cert in enumerate(row):
                    if not isinstance(cert, list):
                        continue
                    P, Q = Ls[i], Ls[i + 1 + j]
                    b0 = lf.box[4]
                    for sb in cert:
                        if sb[3][0] == 'val':
                            k = sum(G.n_combos(lf, sb[3][1], pt) for pt in pats(len(sb[3][1][0])))
                            if k > 1:
                                ok = sub_rowmin(lf, sb, detP(P, Q), xP(P, Q), yP(P, Q), b0)
                                n += 1; npass += ok
                                if k > 64:
                                    big += 1; bigpass += ok
                        b0 = sb[0]
        print(f"{p}: sub-bins with combinations {n}, pass {npass}; with > 64: {big}, pass {bigpass}; "
              f"{time.time() - t0:.1f} s", flush=True)


if __name__ == '__main__':
    main(sys.argv[1:])
