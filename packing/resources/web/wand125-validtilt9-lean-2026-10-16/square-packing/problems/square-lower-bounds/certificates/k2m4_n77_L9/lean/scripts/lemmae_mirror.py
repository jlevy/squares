"""Exact mirror of the kernel computations of Lemma E (`BernsteinZ`, `RatU`, `LemmaEPoly`,
`LemmaEVert`, `LemmaELeaf`).

Every function here computes exactly what the Lean definition of the same name computes (same list
shapes, since `List.contains` compares polynomial triples syntactically).  Integers only.
"""
from math import comb, gcd


# ---------------------------------------------------------------- BernsteinZ
def padd(p, q):
    out = []
    for i in range(max(len(p), len(q))):
        if i < len(p) and i < len(q):
            out.append(p[i] + q[i])
        elif i < len(p):
            out.append(p[i])
        else:
            out.append(q[i])
    return out


def psmul(c, p):
    return [c * a for a in p]


def pmul(p, q):
    # mul [] _ = []; mul (a :: p) q = add (smul a q) (0 :: mul p q)
    if not p:
        return []
    return padd(psmul(p[0], q), [0] + pmul(p[1:], q))


def hom(U0, H, R, n, p):
    if not p:
        return []
    if len(p) == 1:
        return [p[0] * R ** n]
    return padd([p[0] * R ** n], pmul([U0, H], hom(U0, H, R, max(n - 1, 0), p[1:])))


def chooseF(n, k):
    return comb(n, k) if k <= n else 0


def gamK(n, b, i):
    return sum(chooseF(n - k, i - k) * (b[k] if k < len(b) else 0) for k in range(i + 1))


def tpoly(p, n, U0, U1, R):
    return hom(U0, U1 - U0, R, n, p)


def check(p, n, U0, U1, R):
    if len(p) > n + 1:
        return False
    t = tpoly(p, n, U0, U1, R)
    if len(t) > n + 1:
        return False
    return all(gamK(n, t, i) >= 0 for i in range(n + 1))


def checkPos(p, n, U0, U1, R):
    if not check(p, n, U0, U1, R):
        return False
    t = tpoly(p, n, U0, U1, R)
    return gamK(n, t, 0) > 0 and gamK(n, t, n) > 0


def nat_sub(a, b):
    return a - b if a > b else 0


# ---------------------------------------------------------------- RatU
Cp = [1, 0, -1]
Sp = [0, 2]
Np = [1, 0, 1]


def ppow(p, n):
    out = [1]
    for _ in range(n):
        out = pmul(p, out)
    return out


# RF = (num, e, i, j, k, d)
def rf_const(n, d):
    return ([n], 0, 0, 0, 0, d)


def raise_(D, r, a, b, c, g, m):
    num, e, i, j, k, d = r
    num2 = pmul(psmul(m, num), pmul(ppow(D, a), pmul(ppow(Cp, b), pmul(ppow(Sp, c), ppow(Np, g)))))
    return (num2, e + a, i + b, j + c, k + g, d * m)


def lcm(a, b):
    return a * b // gcd(a, b) if a and b else 0


def rf_add(D, r, s):
    e = max(r[1], s[1]); i = max(r[2], s[2]); j = max(r[3], s[3]); k = max(r[4], s[4])
    l = lcm(r[5], s[5])
    r2 = raise_(D, r, e - r[1], i - r[2], j - r[3], k - r[4], l // r[5])
    s2 = raise_(D, s, e - s[1], i - s[2], j - s[3], k - s[4], l // s[5])
    return (padd(r2[0], s2[0]), e, i, j, k, l)


def rf_mul(r, s):
    return (pmul(r[0], s[0]), r[1] + s[1], r[2] + s[2], r[3] + s[3], r[4] + s[4], r[5] * s[5])


def rf_neg(r):
    return (psmul(-1, r[0]),) + tuple(r[1:])


def checkRF(sigma, r, n, U0, U1, R):
    num = r[0] if (sigma or r[1] % 2 == 0) else psmul(-1, r[0])
    return check(num, n, U0, U1, R)


def ckRF(sigma, r, b0, b1, R):
    return checkRF(sigma, r, nat_sub(len(r[0]), 1), b0, b1, R)


# ---------------------------------------------------------------- LemmaEPoly
# PL = (a, b, k) polynomials;  SL = (P, i, j, k, d)
def addPL(P, Q):
    return (padd(P[0], Q[0]), padd(P[1], Q[1]), padd(P[2], Q[2]))


def mulPL(p, P):
    return (pmul(p, P[0]), pmul(p, P[1]), pmul(p, P[2]))


def negPL(P):
    return (psmul(-1, P[0]), psmul(-1, P[1]), psmul(-1, P[2]))


def sdenP(L):
    return pmul(ppow(Cp, L[1]), pmul(ppow(Sp, L[2]), pmul(ppow(Np, L[3]), [L[4]])))


def sl_sub(L, M):
    return (addPL(mulPL(sdenP(M), L[0]), negPL(mulPL(sdenP(L), M[0]))),
            L[1] + M[1], L[2] + M[2], L[3] + M[3], L[4] * M[4])


def sl_cst(n, d):
    return (([0], [0], [n]), 0, 0, 0, d)


def atV(L, D, X, Y):
    P = L[0]
    return (padd(padd(pmul(P[0], X), pmul(P[1], Y)), pmul(P[2], D)), 1, L[1], L[2], L[3], L[4])


def tw(Dn, p):
    return psmul(2 * Dn, p)


def hTA(Dn, Y): return ((tw(Dn, Cp), tw(Dn, Sp), padd(psmul(-Dn, Np), psmul(-2 * Y, Sp))), 1, 0, 0, 2 * Dn)
def hTB(Dn, Y): return ((tw(Dn, Sp), psmul(-1, tw(Dn, Cp)), padd(psmul(2 * Y, Cp), psmul(-Dn, Np))), 0, 1, 0, 2 * Dn)
def hTC(Dn, Y): return ((tw(Dn, Cp), tw(Dn, Sp), padd(psmul(Dn, Np), psmul(-2 * Y, Sp))), 1, 0, 0, 2 * Dn)
def hTD(Dn, Y): return ((tw(Dn, Sp), psmul(-1, tw(Dn, Cp)), padd(psmul(2 * Y, Cp), psmul(Dn, Np))), 0, 1, 0, 2 * Dn)
def vLXs(Dn, X): return ((tw(Dn, Cp), tw(Dn, Sp), padd(psmul(-Dn, Np), psmul(-2 * X, Cp))), 0, 1, 0, 2 * Dn)
def vUXs(Dn, X): return ((tw(Dn, Cp), tw(Dn, Sp), padd(psmul(Dn, Np), psmul(-2 * X, Cp))), 0, 1, 0, 2 * Dn)
def vLYs(Dn, X): return ((psmul(-1, tw(Dn, Sp)), tw(Dn, Cp), padd(psmul(2 * X, Sp), psmul(-Dn, Np))), 1, 0, 0, 2 * Dn)
def vUYs(Dn, X): return ((psmul(-1, tw(Dn, Sp)), tw(Dn, Cp), padd(psmul(2 * X, Sp), psmul(Dn, Np))), 1, 0, 0, 2 * Dn)
def capX(Dn, X0): return ((psmul(-2 * Dn, Np), [0], padd(psmul(2 * X0, Np), psmul(Dn, padd(Cp, Sp)))), 0, 0, 1, 2 * Dn)
def capY(Dn, Y0): return (([0], psmul(-2 * Dn, Np), padd(psmul(2 * Y0, Np), psmul(Dn, padd(Cp, Sp)))), 0, 0, 1, 2 * Dn)
def sSL(h): return (([0], [0], Sp), 0, 0, 1, h)
def cSL(h): return (([0], [0], Cp), 0, 0, 1, h)


# tan-mode cap lines (LemmaEPoly.tanK / tanC / tanCap / capXm / capYm); a RectM is (rect, mx, my)
def tanK(n, m): return padd(psmul(m, padd(Sp, Cp)), psmul(-n, Np))


def tanC(Dn, n, m):
    K = tanK(n, m)
    return padd(padd(psmul(2 * Dn * m * m, pmul(Sp, Cp)), psmul(-Dn, pmul(K, K))),
                padd(psmul(-(2 * Dn * n), pmul(Np, K)), psmul(Dn * m * m, pmul(Sp, Sp))))


def tanCap(Dn, n, m, P):
    mK = psmul(m, tanK(n, m))
    return ((pmul(mK, P[0]), pmul(mK, P[1]), padd(pmul(mK, P[2]), tanC(Dn, n, m))), 0, 1, 1, 2 * Dn * m * m)


def capXm(Dn, rm):
    r, mx = rm[0], rm[1]
    return capX(Dn, r[0]) if mx is None else tanCap(Dn, mx[0], mx[1], capX(Dn, r[0])[0])


def capYm(Dn, rm):
    r, my = rm[0], rm[2]
    return capY(Dn, r[1]) if my is None else tanCap(Dn, my[0], my[1], capY(Dn, r[1])[0])


def modeP(mo): return mo is None or (0 < mo[1] and mo[0] <= mo[1])


# ---------------------------------------------------------------- LemmaEVert
def hUps(Dn, e): return [sl_cst(e[2], Dn), hTC(Dn, e[1]), hTD(Dn, e[1])]
def hLos(Dn, e): return [sl_cst(e[0], Dn), hTA(Dn, e[1]), hTB(Dn, e[1])]
def vUps(Dn, e): return [sl_cst(e[3], Dn), vUXs(Dn, e[0]), vUYs(Dn, e[0])]
def vLos(Dn, e): return [sl_cst(e[1], Dn), vLXs(Dn, e[0]), vLYs(Dn, e[0])]


def signOk(sigma, D, m, b0, b1, R):
    if any(c != 0 for c in D[:m]):
        return False
    q = D[m:]
    return checkPos(q if sigma else psmul(-1, q), nat_sub(len(q), 1), b0, b1, R)


def segOkA(sigma, D, X, Y, b0, b1, R, ups, los, Ua, La):
    if not Ua or not La or not all(a < len(ups) for a in Ua) or not all(b < len(los) for b in La):
        return False
    return all(any(ckRF(sigma, atV(sl_sub(U, ups[a]), D, X, Y), b0, b1, R) for a in Ua) for U in ups) and \
        all(any(ckRF(sigma, atV(sl_sub(los[b], L), D, X, Y), b0, b1, R) for b in La) for L in los)


def segVal(D, X, Y, w, Dn, ln, ups, los, iu, il):
    return rf_mul(rf_const(w * Dn, ln), atV(sl_sub(ups[iu], los[il]), D, X, Y))


def ghOk(sigma, D, X, Y, b0, b1, R, cap, mode):
    if mode == 0:
        return ckRF(sigma, atV(sl_sub(sl_cst(0, 1), cap), D, X, Y), b0, b1, R)
    if mode == 1:
        return True
    return ckRF(sigma, atV(sl_sub(cap, sSL(1)), D, X, Y), b0, b1, R)


def ghU(D, X, Y, cap, mode):
    if mode == 0:
        return rf_const(0, 1)
    if mode == 1:
        a = atV(cap, D, X, Y)
        return rf_mul(rf_mul(a, a), (pmul(Np, Np), 0, 1, 1, 0, 2))
    return rf_mul(atV(sl_sub(cap, sSL(2)), D, X, Y), (Np, 0, 1, 0, 0, 1))


def lebVal(D, X, Y, Dn, r, mx, my):
    return rf_mul(rf_const(r[4], 1),
                  rf_add(D, rf_add(D, rf_const(1, 1), rf_neg(ghU(D, X, Y, capX(Dn, r[0]), mx))),
                         rf_neg(ghU(D, X, Y, capY(Dn, r[1]), my))))


def sumRF(D, rs):
    out = rf_const(0, 1)
    for r in reversed(rs):
        out = rf_add(D, r, out)
    return out


def segAlts(D, X, Y, w, Dn, ln, ups, los, Ua, La):
    return [segVal(D, X, Y, w, Dn, ln, ups, los, a, b) for a in Ua for b in La]


def cprod(Ls):
    out = [[]]
    for l in reversed(Ls):
        out = [[a] + c for a in l for c in out]
    return out


# SegC: ('drop',) | ('box',) | ('alt', Ua, La)
def segCAlts(D, X, Y, w, Dn, ln, ups, los, bx, sc):
    if sc[0] == 'drop':
        return [rf_const(0, 1)]
    if sc[0] == 'box':
        return segAlts(D, X, Y, w, Dn, ln, ups, los, bx[0], bx[1])
    return segAlts(D, X, Y, w, Dn, ln, ups, los, sc[1], sc[2])


def segCOk(sigma, D, X, Y, b0, b1, R, ups, los, bx, sc):
    if sc[0] == 'drop':
        return True
    if sc[0] == 'box':
        return bool(bx[0]) and bool(bx[1]) and all(a < len(ups) for a in bx[0]) and all(b < len(los) for b in bx[1])
    return segOkA(sigma, D, X, Y, b0, b1, R, ups, los, sc[1], sc[2])


def snum(sigma, r):
    return r[0] if (sigma or r[1] % 2 == 0) else psmul(-1, r[0])


def ptrim(p):
    p = list(p)
    while p and p[-1] == 0:
        p.pop()
    return p


def peqb(p, q): return ptrim(p) == ptrim(q)


def divHL(rg, fuel, rp):
    out = []
    while fuel > 0:
        fuel -= 1
        if len(rp) < len(rg) or not rp or not rg:
            break
        c = int(rp[0] / rg[0]) if False else _idiv(rp[0], rg[0])
        out.append(c)
        rg2 = rg + [0] * (len(rp) - len(rg))
        rp = [x - c * y for x, y in zip(rp, rg2)][1:]
    return out


def _idiv(a, b):
    # Lean's Int `/` is `Int.div` (T-division? no: Lean 4 `Int./` is `Int.div` = round toward zero? It is `Int.div` in core = ediv)
    q = a // b
    if b < 0 and q * b != a:
        pass
    # Lean 4 core: HDiv Int is Int.div (Euclidean `ediv`): remainder >= 0
    r = a - b * q
    if r < 0:
        q += 1 if b < 0 else -1
    return q if a - b * q >= 0 else q


def pdiv(p, g):
    tp = ptrim(p); tg = ptrim(g)
    return list(reversed(divHL(list(reversed(tg)), len(tp), list(reversed(tp)))))


def splitAt(splits, k):
    return splits[k][0] if k < len(splits) else sl_cst(0, 1)


def fcOk(sigma, D, X, Y, b0, b1, R, splits, pat, f, T):
    k, G, g1, m = f
    if not k < len(splits): return False
    if not peqb(snum(sigma, atV(splitAt(splits, k), D, X, Y)), pmul(G, g1)): return False
    if any(c != 0 for c in g1[:m]): return False
    g1d = g1[m:]
    if not checkPos(g1d, nat_sub(len(g1d), 1), b0, b1, R): return False
    sT = snum(sigma, T)
    c1 = pdiv(sT, G)
    if not peqb(sT, pmul(G, c1)): return False
    b = pat[k] if k < len(pat) else False
    return check(c1 if b else psmul(-1, c1), nat_sub(len(c1), 1), b0, b1, R)


def totOk(sigma, D, X, Y, b0, b1, R, splits, pat, fcs, T):
    return ckRF(sigma, T, b0, b1, R) or any(fcOk(sigma, D, X, Y, b0, b1, R, splits, pat, f, T) for f in fcs)


def tagOk(pat, t):
    if t is None: return True
    k, b = t
    return (pat[k] if k < len(pat) else False) == b


def pats(n):
    out = [[]]
    for _ in range(n):
        out = [[b] + p for p in out for b in (False, True)]
    return out


def sproc(D, X, Y, sp, b):
    q, nm, dm, np_, dp = sp
    if b: return rf_neg(rf_mul(rf_const(np_, dp), atV(q, D, X, Y)))
    return rf_mul(rf_const(nm, dm), atV(q, D, X, Y))


# CapA: ('zeroC',) | ('zeroT', k) | ('par',) | ('linC',) | ('linT', k)
def capTag(a):
    if a[0] == 'zeroT': return (a[1], False)
    if a[0] == 'parT': return (a[1], a[2])
    if a[0] == 'linT': return (a[1], True)
    return None


def capAOk(sigma, D, X, Y, b0, b1, R, splits, cap, a):
    if a[0] == 'zeroC': return ghOk(sigma, D, X, Y, b0, b1, R, cap, 0)
    if a[0] == 'par': return True
    if a[0] == 'parT': return a[1] < len(splits)
    if a[0] == 'linC': return ghOk(sigma, D, X, Y, b0, b1, R, cap, 2)
    if a[0] == 'zeroT': return a[1] < len(splits) and splitAt(splits, a[1]) == cap
    return a[1] < len(splits) and splitAt(splits, a[1]) == sl_sub(cap, sSL(1))


def capAU(D, X, Y, cap, a):
    return ghU(D, X, Y, cap, {'zeroC': 0, 'zeroT': 0, 'par': 1, 'parT': 1, 'linC': 2, 'linT': 2}[a[0]])


def lebRF(D, X, Y, Dn, r, ax, ay):
    return rf_mul(rf_const(r[0][4], 1), rf_add(D, rf_add(D, rf_const(1, 1), rf_neg(capAU(D, X, Y, capXm(Dn, r), ax))),
                                             rf_neg(capAU(D, X, Y, capYm(Dn, r), ay))))


# corner kinds (LemmaEVert.slAtP / mcRF / lebRFs); a RectM is (rect, mx, my, ck),
# ck = ('std',) | ('c3', xa, ya, ym, q) | ('xc', xa, ya, ym, q)
def slAtP(L, x, y, q):
    P = L[0]
    return (padd(padd(psmul(x, P[0]), psmul(y, P[1])), psmul(q, P[2])), 0, L[1], L[2], L[3], L[4] * q)


cRF = (Cp, 0, 0, 0, 1, 1)
sRF = (Sp, 0, 0, 0, 1, 1)
i2cRF = (Np, 0, 1, 0, 0, 2)


def mcRF(D, A, B, bs, al, be):
    t1 = rf_mul(rf_mul(rf_const(2, 1), cRF), rf_add(D, rf_add(D, rf_mul(A, be), rf_mul(B, al)), rf_neg(rf_mul(A, B))))
    t2 = rf_mul(sRF, rf_add(D, rf_mul(rf_mul(rf_const(2, 1), bs), be), rf_neg(rf_mul(bs, bs))))
    t3 = rf_neg(rf_mul(sRF, rf_mul(al, al)))
    return rf_mul(i2cRF, rf_add(D, rf_add(D, t1, t2), t3))


def lebRFs(D, X, Y, Dn, r, ax, ay):
    w = rf_const(r[0][4], 1)
    gx = rf_neg(capAU(D, X, Y, capXm(Dn, r), ax))
    gy = rf_neg(capAU(D, X, Y, capYm(Dn, r), ay))
    ck = r[3]
    if ck[0] == 'std':
        return [lebRF(D, X, Y, Dn, r, ax, ay)]
    _, xa, ya, ym, q = ck
    if ck[0] == 'c3':
        aL = sl_sub(capX(Dn, r[0][0]), sSL(1)); bL = capY(Dn, r[0][1])
        mc = mcRF(D, slAtP(aL, xa, ya, q), slAtP(bL, xa, ya, q), slAtP(bL, xa, ym, q),
                  atV(sl_sub(capXm(Dn, r), sSL(1)), D, X, Y), atV(capYm(Dn, r), D, X, Y))
        return [rf_mul(w, rf_add(D, rf_add(D, rf_add(D, rf_const(1, 1), gx), gy), mc)),
                rf_mul(w, rf_add(D, rf_const(1, 1), gx))]
    aL = capX(Dn, r[0][0]); bL = sl_sub(capY(Dn, r[0][1]), cSL(1))
    mc = mcRF(D, slAtP(aL, xa, ya, q), slAtP(bL, xa, ya, q), slAtP(bL, xa, ym, q),
              atV(capXm(Dn, r), D, X, Y), atV(sl_sub(capYm(Dn, r), cSL(1)), D, X, Y))
    return [rf_mul(w, rf_add(D, rf_add(D, rf_const(1, 1), gy), mc)), lebRF(D, X, Y, Dn, r, ax, ay)]


def ckOk(ck): return ck[0] == 'std' or 0 < ck[4]


def vertOk(Dn, W, sigma, D, X, Y, b0, b1, R, chs, cvs, crs, hbx, vbx, c):
    splits, fcs, hc, vc, lc = c
    if len(hbx) != len(chs) or len(vbx) != len(cvs) or len(hc) != len(chs) or len(vc) != len(cvs) or len(lc) != len(crs):
        return False
    if not all(sp[2] != 0 and sp[4] != 0 for sp in splits): return False
    for e, bx, l in zip(chs, hbx, hc):
        if not all(segCOk(sigma, D, X, Y, b0, b1, R, hUps(Dn, e), hLos(Dn, e), bx, x[0]) for x in l): return False
    for e, bx, l in zip(cvs, vbx, vc):
        if not all(segCOk(sigma, D, X, Y, b0, b1, R, vUps(Dn, e), vLos(Dn, e), bx, x[0]) for x in l): return False
    for r, (xs, ys) in zip(crs, lc):
        if not all(capAOk(sigma, D, X, Y, b0, b1, R, splits, capXm(Dn, r), a) for a in xs): return False
        if not all(capAOk(sigma, D, X, Y, b0, b1, R, splits, capYm(Dn, r), a) for a in ys): return False
    for pat in pats(len(splits)):
        if not all(any(tagOk(pat, x[1]) for x in l) for l in hc): return False
        if not all(any(tagOk(pat, x[1]) for x in l) for l in vc): return False
        if not all(any(tagOk(pat, capTag(a)) for a in xs) and any(tagOk(pat, capTag(a)) for a in ys) for xs, ys in lc): return False
        alts = []
        for e, bx, l in zip(chs, hbx, hc):
            alts.append([t for x in l if tagOk(pat, x[1])
                         for t in segCAlts(D, X, Y, e[4], Dn, nat_sub(e[2], e[0]), hUps(Dn, e), hLos(Dn, e), bx, x[0])])
        for e, bx, l in zip(cvs, vbx, vc):
            alts.append([t for x in l if tagOk(pat, x[1])
                         for t in segCAlts(D, X, Y, e[4], Dn, nat_sub(e[3], e[1]), vUps(Dn, e), vLos(Dn, e), bx, x[0])])
        for r, (xs, ys) in zip(crs, lc):
            alts.append([t for ax in xs if tagOk(pat, capTag(ax))
                         for ay in ys if tagOk(pat, capTag(ay)) for t in lebRFs(D, X, Y, Dn, r, ax, ay)])
        sps = [sproc(D, X, Y, sp, b) for sp, b in zip(splits, pat)]
        for comb in cprod(alts):
            if not totOk(sigma, D, X, Y, b0, b1, R, splits, pat, fcs, sumRF(D, comb + sps + [rf_const(-W, 1)])):
                return False
    return True


# ---------------------------------------------------------------- LemmaELeaf
def detP(P, Q): return padd(pmul(P[0], Q[1]), psmul(-1, pmul(Q[0], P[1])))
def xP(P, Q): return padd(pmul(P[1], Q[2]), psmul(-1, pmul(Q[1], P[2])))
def yP(P, Q): return padd(pmul(Q[0], P[2]), psmul(-1, pmul(P[0], Q[2])))


def sideL(Q, x0, x1, y0, y1, wx, wy):
    wall = psmul(-1, padd(Cp, Sp))
    return [(psmul(2, Np), [0], wall) if wx else ([Q], [0], [-x0]),
            ([-Q], [0], [x1]),
            ([0], psmul(2, Np), wall) if wy else ([0], [Q], [-y0]),
            ([0], [-Q], [y1])]


wallX = (psmul(2, Np), [0], psmul(-1, padd(Cp, Sp)))
wallY = ([0], psmul(2, Np), psmul(-1, padd(Cp, Sp)))


def sideE(Q, x0, x1, y0, y1, wx, wy, ex, ey):
    return sideL(Q, x0, x1, y0, y1, wx, wy) + ([wallX] if ex else []) + ([wallY] if ey else [])


def cnum(x, w): return padd(Cp, Sp) if w else [x]
def cden(Q, w): return psmul(2, Np) if w else [Q]


def cornerPoly(P, nx, dx, ny, dy):
    return padd(padd(pmul(P[0], pmul(nx, dy)), pmul(P[1], pmul(ny, dx))), pmul(P[2], pmul(dx, dy)))


def cornersOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, neg, P):
    cs = [(cnum(x0, wx), cden(Q, wx), cnum(y0, wy), cden(Q, wy)), (cnum(x0, wx), cden(Q, wx), cnum(y1, False), cden(Q, False)),
          (cnum(x1, False), cden(Q, False), cnum(y0, wy), cden(Q, wy)),
          (cnum(x1, False), cden(Q, False), cnum(y1, False), cden(Q, False))]
    for c in cs:
        p = cornerPoly(P, *c)
        if not check(psmul(-1, p) if neg else p, nat_sub(len(p), 1), U0, U1, R):
            return False
    return True


def formsSL(A, B, lo1, lo2, up1, up2):
    return [sl_sub(up1, A), sl_sub(up2, A), sl_sub(B, lo1), sl_sub(B, lo2),
            sl_sub(up1, lo1), sl_sub(up1, lo2), sl_sub(up2, lo1), sl_sub(up2, lo2)]


def hFormsSLs(Dn, e):
    return formsSL(sl_cst(e[0], Dn), sl_cst(e[2], Dn), hTA(Dn, e[1]), hTB(Dn, e[1]), hTC(Dn, e[1]), hTD(Dn, e[1]))


def vFormsSLs(Dn, e):
    return formsSL(sl_cst(e[1], Dn), sl_cst(e[3], Dn), vLXs(Dn, e[0]), vLYs(Dn, e[0]), vUXs(Dn, e[0]), vUYs(Dn, e[0]))


def lebSLs(Dn, r):
    return [capXm(Dn, r), sl_sub(capXm(Dn, r), sSL(1)), capYm(Dn, r), sl_sub(capYm(Dn, r), sSL(1))]


def tanAx(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, L, mo):
    if mo is None: return True
    n, m = mo
    return 0 < m and n <= m and \
        cornersOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, False, sl_sub(L, sSL(1))[0]) and \
        cornersOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, False, sl_sub(L, cSL(1))[0])


def ancPL(x, q, fst):
    return ([-q], [0], [x]) if fst else ([0], [-q], [x])


def ancOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, xa, ya, q):
    co = lambda neg, P: cornersOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, neg, P)
    return (co(False, ancPL(xa, q, True)) and co(False, ancPL(ya, q, False))) or \
        (co(True, ancPL(xa, q, True)) and co(True, ancPL(ya, q, False)))


def xiPL(A, B):
    return addPL(addPL(mulPL(pmul(Cp, sdenP(B)), A[0]), mulPL(pmul(Sp, sdenP(A)), B[0])),
                 ([0], [0], psmul(-1, pmul(Np, pmul(sdenP(A), sdenP(B))))))


def cornerOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, Dn, r):
    co = lambda neg, P: cornersOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, neg, P)
    ck = r[3]
    if ck[0] == 'std': return True
    _, xa, ya, ym, q = ck
    if not (0 < q and r[1] is None and r[2] is None): return False
    aL = sl_sub(capX(Dn, r[0][0]), sSL(1))
    if ck[0] == 'c3':
        return co(False, aL[0]) and co(True, sl_sub(aL, cSL(1))[0]) and \
            co(True, sl_sub(capY(Dn, r[0][1]), cSL(1))[0]) and co(True, xiPL(aL, capY(Dn, r[0][1]))) and \
            ancOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, xa, ya, q)
    return co(True, aL[0]) and co(True, sl_sub(capY(Dn, r[0][1]), cSL(1))[0]) and \
        ancOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, xa, ya, q)


def tanOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, Dn, r):
    return tanAx(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, capX(Dn, r[0][0]), r[1]) and \
        tanAx(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, capY(Dn, r[0][1]), r[2])


def widN(R, U0, U1): return nat_sub(R * R + 2 * U1 * R, U0 * U0)
def widD(R, U0): return R * R + U0 * U0


def boxDomOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, ups, los, bx):
    d0 = sl_cst(0, 1)
    g = lambda l, a: l[a] if a < len(l) else d0
    return all(any(cornersOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, False, sl_sub(U, g(ups, a))[0]) for a in bx[0]) for U in ups) and \
        all(any(cornersOk(Q, x0, x1, y0, y1, U0, U1, R, wx, wy, False, sl_sub(g(los, b), L)[0]) for b in bx[1]) for L in los)
