# r38.py -- independent reimplementation (from the text of the proof only) of
#   ZC (wall filler, Lemma W) and E38 (end packing, Lemma E), plus a generic exact checker.
# Exact rationals: gmpy2.mpq if available, else fractions.Fraction.
import math, bisect, sys
try:
    import gmpy2
    QQ = gmpy2.mpq
    HAVE_GMP = True
except ImportError:
    from fractions import Fraction as QQ
    HAVE_GMP = False
import mpmath
mpmath.mp.prec = 200

def fl(x):
    x = QQ(x)
    return int(x.numerator) // int(x.denominator)

def ce(x):
    return -fl(-QQ(x))

def frac(x):
    return x - fl(x)

class Tilt:
    __slots__ = ('t', 'ca', 'sa', 'ta', 'se', 'e')
    def __init__(self, t):
        t = QQ(t); t2 = t * t
        self.t = t
        self.ca = (1 - t2) / (1 + t2)
        self.sa = 2 * t / (1 + t2)
        self.ta = self.sa / self.ca
        self.se = 1 / self.ca
        self.e = 1 - self.ca

def ta_of(k, Q):
    # ta at t = k/Q, exact
    return QQ(2 * k * Q, Q * Q - k * k)

def mpf_of(x):
    x = QQ(x)
    return mpmath.mpf(int(x.numerator)) / int(x.denominator)

def grid_k_for_ta(X, Q, kmax):
    """largest integer k in [0, kmax] with ta(k/Q) <= X (k=0 means none positive)."""
    X = QQ(X)
    if X <= 0:
        return 0
    Xm = mpf_of(X)
    t = Xm / (1 + mpmath.sqrt(1 + Xm * Xm))
    k = int(mpmath.floor(t * Q))
    k = min(k, kmax)
    while k > 0 and ta_of(k, Q) > X:
        k -= 1
    while k + 1 <= kmax and ta_of(k + 1, Q) <= X:
        k += 1
    return max(k, 0)

def wall_t0(sig, Qs, aw=QQ(3, 2)):
    """t0 = ceil(Qs t_tgt)/Qs with ta(t_tgt) = aw sqrt(sig) (high precision)."""
    X = mpf_of(aw) * mpmath.sqrt(mpf_of(sig))
    t = X / (1 + mpmath.sqrt(1 + X * X))
    return QQ(int(mpmath.ceil(t * Qs)), Qs)

# ---------------------------------------------------------------- ZC
class Block:
    pass

def zfill(h0, sig, L, t0, Qs, Qf, noblock=False):
    """Construction ZC on Z(h0,sig,L). Returns dict with blocks, rows, stats."""
    h0 = QQ(h0); sig = QQ(sig); L = QQ(L)
    h = lambda x: h0 + sig * x
    N0 = fl(h0) - 1
    res = {'fail': None, 'blocks': [], 'rows': [], 'N0': N0}
    blocks = res['blocks']
    if not noblock:
        kt = int(QQ(t0) * Qs)
        assert QQ(kt, Qs) == QQ(t0)
        tl = Tilt(t0)
        F = fl(h0 - N0 * tl.ca - tl.sa)
        M = F + N0
        s = M * tl.ta
        while True:
            ca, sa, ta, se, e = tl.ca, tl.sa, tl.ta, tl.se, tl.e
            if s + se > L:
                break
            B = Block(); B.k = kt; B.tl = tl; B.s = s; B.F = F; B.M = M
            Js = []
            reason = None
            g0 = h(s - M * ta)
            i = 0
            base = M * ca + sa
            while True:
                c = s + i * se
                if c + se > L:
                    reason = 'L'; break
                gam = g0 + i * sig * se   # = h(c - M ta)
                Jf = fl((gam - base) / e)
                if Jf > M - 1:
                    reason = 'sat'; break
                Js.append(Jf)
                i += 1
            P = len(Js)
            B.J = Js; B.P = P; B.reason = reason; B.cP = s + P * se; B.gamma0 = g0
            if P == 0:
                res['fail'] = 'P0'; blocks.append(B); break
            blocks.append(B)
            if reason == 'L':
                break
            if sig == 0:
                res['fail'] = 'sat_sig0'; break
            kappa = e * e / sig
            kn = grid_k_for_ta(ta - kappa, Qs, kt)
            if kn <= 0:
                res['fail'] = 'tilt'; break
            tn = Tilt(QQ(kn, Qs))
            kp = ta - tn.ta
            B.kappa = kappa; B.eta = kp - kappa
            Jlo, JL = Js[0], Js[-1]
            if JL > Jlo:
                A = (g0 - M * ca - sa) / e
                Bq = e / (sig * se)
                p = bisect.bisect_right(Js, Jlo)
                theta = p - Bq * (Jlo + 1 - A)
                psi = B.cP - tn.ta - (s + p * se) + Jlo * kp
                phi0 = frac(-(psi + theta * (se - 1) - (se - 1)))
                phi = QQ(ce(phi0 * Qf), Qf)
            else:
                phi = QQ(0)
            B.phi = phi
            sn = B.cP + phi
            Fn = fl((h0 + sig * sn - N0 * (tn.ca + sig * tn.ta) - tn.sa) / (1 + sig * tn.ta))
            Mn = Fn + N0
            # defining property of F' as a maximum (independent check of the closed form)
            ok1 = Fn + N0 * tn.ca + tn.sa <= h(sn - (Fn + N0) * tn.ta)
            ok2 = not (Fn + 1 + N0 * tn.ca + tn.sa <= h(sn - (Fn + 1 + N0) * tn.ta))
            if not (ok1 and ok2):
                res['fail'] = 'Fdef'; break
            if Fn < F or sn < Mn * tn.ta:
                res['fail'] = 'F_or_s'; break
            tl = tn; kt = kn; s = sn; F = Fn; M = Mn
    # rows
    jmax = fl(h(L))
    if h(L) == jmax:
        pass  # rows j < floor(h(L))
    rows = res['rows']
    maxres = QQ(0); minl = None; naligned = 0
    nb = len(blocks)
    for j in range(jmax):
        a = QQ(0); prevb = None
        for bi, B in enumerate(blocks):
            if B.J[0] <= j:
                r = B.s - (j + 1) * B.tl.ta
                # aligned-closing stats: left end in block bi-1 with J_lo <= j < J_L (consecutive blocks)
                if prevb is not None and prevb == bi - 1:
                    P_ = blocks[prevb]
                    if P_.J[0] <= j < P_.J[-1]:
                        l = r - a
                        naligned += 1
                        if minl is None or l < minl: minl = l
                        if frac(l) > maxres: maxres = frac(l)
                _place(rows, a, r, j, h)
                p = bisect.bisect_right(B.J, j)
                a = B.s + p * B.tl.se - j * B.tl.ta
                prevb = bi
        _place(rows, a, L, j, h)
    res['naligned'] = naligned; res['maxres'] = maxres; res['minl'] = minl
    nsq = sum(B.M * B.P - sum(B.J) for B in blocks if B.P) + sum(k for (_, _, k) in rows)
    res['nsq'] = nsq
    res['area'] = L * h0 + sig * L * L / 2
    res['U'] = res['area'] - nsq
    return res

def _place(rows, a, r, j, h):
    if r - a >= 1 and a >= 0 and j + 1 <= h(a):
        rows.append((a, j, fl(r - a)))

def zpieces(res, mapf=None):
    """yield pieces as 4 exact vertices (v0,v1 = unit side) and n"""
    for B in res['blocks']:
        tl = B.tl; ca, sa, ta, se = tl.ca, tl.sa, tl.ta, tl.se
        for i, J in enumerate(B.J):
            n = B.M - J
            c = B.s + i * se
            P = (c - J * ta, QQ(J))
            v = [P, (P[0] + ca, P[1] + sa), (P[0] + ca - n * sa, P[1] + sa + n * ca), (P[0] - n * sa, P[1] + n * ca)]
            if mapf: v = [mapf(q) for q in v]
            yield v, n
    for (a, j, k) in res['rows']:
        v = [(a, QQ(j)), (a, QQ(j + 1)), (a + k, QQ(j + 1)), (a + k, QQ(j))]
        if mapf: v = [mapf(q) for q in v]
        yield v, k

def bw_bound(h0, sig, L, t0, Qs, Qf, mu=mpmath.mpf('0.65')):
    """Hypotheses (W1)-(W5) margins and B_W, in mpmath interval arithmetic."""
    iv = mpmath.iv; iv.prec = 150
    def I(x):
        x = QQ(x); return iv.mpf(int(x.numerator)) / iv.mpf(int(x.denominator))
    tl = Tilt(t0)
    h0i, sigi, Li = I(h0), I(sig), I(L)
    N0 = fl(QQ(h0)) - 1
    ta0, se0, e0, ca0 = I(tl.ta), I(tl.se), I(tl.e), I(tl.ca)
    mu = iv.mpf('0.65')
    g = iv.mpf(21) / 10 / Qs
    hL = h0i + sigi * Li
    Mmax = hL + N0 * e0
    sm = iv.sqrt(1 + mu ** 2 * ta0 ** 2)
    emin = (mu * ta0) ** 2 / (sm * (sm + 1))
    Lam = (emin * N0 - 1 - sigi * ta0) / sigi
    Kbar = Li / Lam
    eps = (se0 - 1) + N0 * g + iv.mpf(1) / Qf
    W1 = Lam - N0 * ta0
    Dr = (e0 / N0) * (Li + Kbar * (1 + sigi * ta0) / sigi) + Kbar * g
    W2 = (1 - mu) * ta0 - Dr
    W3 = N0 * ca0 - (sigi * se0 / emin + ta0 + sigi * (2 + se0 + Mmax * ta0) + (1 + sigi * ta0) / emin)
    W4 = 1 - eps
    W5a = mu * ta0 - g
    W5b = iv.mpf('0.21') - ta0
    ccol = ta0 + se0 * e0 + se0 * sigi * (se0 + N0 * e0 * ta0)
    hT = 1 + sigi * se0 / emin + ta0 + sigi * (1 + se0 + Mmax * ta0)
    wT = 1 + (hL + 1) * (e0 ** 2 / sigi + g)
    AT = hT * wT
    w0 = (1 + N0 * e0) * ta0
    we = 1 + se0 + (hL + N0 * e0) * ta0
    fh0 = fl(QQ(h0))
    BW = (Li * ccol + Kbar * ((N0 - 1) * (eps + ta0) + ((1 + sigi * ta0) / emin) * (1 + ta0) + AT)
          + fh0 * (1 + ta0 / 2) + w0 * (1 + sigi * w0) + hL * (1 + ta0 / 2) + we * (4 + 2 * sigi * we))
    marg = {'W1': W1.a, 'W2': W2.a, 'W3': W3.a, 'W4': W4.a, 'W5a': W5a.a, 'W5b': W5b.a,
            't0<=1/10': (QQ(t0) <= QQ(1, 10)), 'h0>=4': QQ(h0) >= 4}
    ok = all((float(v) > 0) if not isinstance(v, bool) else v for v in marg.values())
    return {'BW_hi': float(BW.b), 'Kbar': float(Kbar.b), 'eps': float(eps.b),
            'margins': {k: (float(v) if not isinstance(v, bool) else v) for k, v in marg.items()}, 'hyp_ok': ok}

# ---------------------------------------------------------------- E38
def iroot4_floor(n):
    r = int(round(n ** 0.25)) if n < 2 ** 1000 else int(mpmath.floor(mpmath.root(n, 4)))
    while r ** 4 > n: r -= 1
    while (r + 1) ** 4 <= n: r += 1
    return r

def e38(b, y, Qs=2 ** 40, Qf=2 ** 48, aw=QQ(3, 2), Q=None):
    b = int(b); y = QQ(y)
    tb = QQ(b, b * b - 1)
    cth = (1 - tb * tb) / (1 + tb * tb); s = 2 * tb / (1 + tb * tb); T = s / cth
    W = b * cth + s
    g = lambda X: y + (X - s) * T
    G0 = g(0); G = g(W)
    out = {'b': b, 'y': y, 'W': W, 'T': T, 'G0': G0, 'G': G}
    m = fl(G) + 1
    D = iroot4_floor(256 * m ** 3); DR = D
    gD = g(D)
    if Q is None:
        Q = 1
        while Q < 16 * b: Q *= 2
    Dp = m + gD; dl = m - gD
    Fq = lambda t: Dp * t * t - 2 * t - dl
    tst = (1 + mpmath.sqrt(1 + mpf_of(Dp) * mpf_of(dl))) / mpf_of(Dp)
    k = int(mpmath.ceil(tst * Q))
    while Fq(QQ(k - 1, Q)) >= 0: k -= 1
    while Fq(QQ(k, Q)) < 0: k += 1
    t = QQ(k, Q); tl = Tilt(t)
    ca, sa, ta, se, e = tl.ca, tl.sa, tl.ta, tl.se, tl.e
    assert m * ca + sa <= gD
    c0 = D + m * ta
    x = (W - DR - se - c0)
    N = fl(x / se) + 1 if x >= 0 else 0
    out.update(m=m, D=D, DR=DR, gD=gD, Q=Q, t=t, ta=ta, se=se, e=e, ca=ca, sa=sa, N=N, c0=c0)
    if N < 1:
        out['fail'] = 'N0'; return out
    base = m * ca + sa
    Js = [fl((gD + i * T * se - base) / e) for i in range(N)]   # gamma_i = g(D + i se)
    J0, JL = Js[0], Js[-1]
    cN = c0 + N * se; cN1 = c0 + (N - 1) * se
    kappa_m = e * e / T
    kc = grid_k_for_ta(ta - kappa_m, Qs, Qs // 10)
    tau = ta_of(kc, Qs) if kc > 0 else QQ(0)
    kp = ta - tau
    if JL > J0:
        A = (gD - m * ca - sa) / e
        Bq = e / (T * se)
        p = bisect.bisect_right(Js, J0)
        theta = p - Bq * (J0 + 1 - A)
        psi = cN1 - tau - (c0 + p * se) + J0 * kp
        phi0 = frac(-(psi + theta * (se - 1) - (se - 1)))
        phi = QQ(ce(phi0 * Qf), Qf)
    else:
        phi = QQ(0)
    l0 = cN1 + phi
    out.update(Js=Js, J0=J0, JL=JL, cN=cN, kappa_m=kappa_m, kc=kc, tau=tau, phi=phi, l0=l0)
    rows = []
    eps_m = (se - 1) + m * QQ(21, 10) / Qs + QQ(1, Qf)
    maxres = QQ(0); minl = None
    for j in range(JL):
        p = bisect.bisect_right(Js, j)
        a = c0 + p * se - j * ta
        r = l0 - (j + 1) * tau
        l = r - a
        if j >= J0:
            if minl is None or l < minl: minl = l
            if frac(l) > maxres: maxres = frac(l)
        if l >= 1:
            rows.append((a, j, fl(l)))
    out.update(rows=rows, eps_m=eps_m, maxres_main=maxres, minl_main=minl)
    # walls
    Yu = (G0 + T * cN) / (1 + T * ta)
    walls = {}
    specs = {
        'L': (c0 - G0 * ta, ta, G0, lambda q: (q[1], G0 - q[0])),
        'LR': (W - l0, tau, QQ(JL), lambda q: (W - q[1], q[0])),
        'UR': (W - cN + JL * ta, ta, Yu - JL, lambda q: (W - q[1], JL + q[0])),
    }
    for name, (h0, sig, L, mp) in specs.items():
        if sig > 0:
            t0 = wall_t0(sig, Qs, aw)
            z = zfill(h0, sig, L, t0, Qs, Qf)
        else:
            t0 = None
            z = zfill(h0, sig, L, None, Qs, Qf, noblock=True)
        z['t0'] = t0; z['h0'] = h0; z['sig'] = sig; z['L'] = L; z['map'] = mp
        walls[name] = z
    out['walls'] = walls
    out['Yu'] = Yu
    nsq = sum(m - J for J in Js) + sum(k for (_, _, k) in rows) + sum(z['nsq'] for z in walls.values())
    area = W * (G0 + G) / 2
    out['nsq'] = nsq; out['area'] = area; out['U'] = area - nsq
    # Lemma E bound (with each U_Z replaced by its exact value and by B_W)
    rho = W * T
    h0L = c0 - G0 * ta; wR = W - cN + G * ta
    mainpart = W * sa + W * e + rho * (se + m * ta) + J0 * (1 + ta) + JL * (eps_m + ta) + T * h0L ** 2 / 2 + T * wR ** 2
    out['mainpart'] = mainpart
    return out

def e38_pieces(o):
    t = o['t']; tl = Tilt(t); ca, sa, ta, se = tl.ca, tl.sa, tl.ta, tl.se
    m = o['m']; c0 = o['c0']
    for i, J in enumerate(o['Js']):
        n = m - J; c = c0 + i * se
        P = (c - J * ta, QQ(J))
        yield ('main', [P, (P[0] + ca, P[1] + sa), (P[0] + ca - n * sa, P[1] + sa + n * ca), (P[0] - n * sa, P[1] + n * ca)], n)
    for (a, j, k) in o['rows']:
        yield ('mrow', [(a, QQ(j)), (a, QQ(j + 1)), (a + k, QQ(j + 1)), (a + k, QQ(j))], k)
    for name, z in o['walls'].items():
        for v, n in zpieces(z, z['map']):
            yield ('w' + name, v, n)
