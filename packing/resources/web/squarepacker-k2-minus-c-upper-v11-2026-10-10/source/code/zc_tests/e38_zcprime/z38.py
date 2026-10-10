# z38.py -- construction of the paper (end region with chained wall fillers), exact rationals.
#   zfill(...)   : the chain filler ZC of a canonical wall region Z(h0, sig, L) (wall filler section of the paper)
#   build(...)   : the end packing E38 of Reg(y) (section 3): shifted stair + aligned cut + 3 walls filled by ZC
# Number type: fractions.Fraction (local) or gmpy2.mpq (AWS; set NUM='mpq').
import sys, math, bisect, os
NUM = os.environ.get('NUM', 'frac')
if NUM == 'mpq':
    import gmpy2
    def F(a, b=1): return gmpy2.mpq(a, b)
else:
    from fractions import Fraction
    def F(a, b=1): return Fraction(a, b)

def fl(q): return int(q.numerator // q.denominator)
def cl(q): return -fl(-q)
def frac(q): return q - fl(q)

GRID = 2 ** 48          # grid for start offsets phi
QW = 2 ** 40            # tilt grid of the wall fillers and of the cut

def tilt(t):
    ca = (1 - t * t) / (1 + t * t); sa = 2 * t / (1 + t * t)
    return ca, sa, sa / ca, 1 / ca, 1 - ca

def ta_of(t): return 2 * t / (1 - t * t)

def t_grid_ceil(ta_target, Q):
    tf = ta_target / (1 + math.sqrt(1 + ta_target * ta_target))
    return max(1, math.ceil(tf * Q))

def largest_u_with_ta_le(target, Q, uhi):
    """largest integer u <= uhi with ta(u/Q) <= target (exact); returns 0 if none >0."""
    tgf = float(target)
    if tgf <= 0: return 0
    u = min(uhi, int(tgf / (1 + math.sqrt(1 + tgf * tgf)) * Q) + 2)
    while u > 0 and ta_of(F(u, Q)) > target: u -= 1
    while u + 1 <= uhi and ta_of(F(u + 1, Q)) <= target: u += 1
    return u

# ----------------------------------------------------------------------------------------------------------
def zfill(h0, sig, L, u0, Q=QW, nmin=1):
    """Chain filler of Z = {0<=x<=L, 0<=y<=h0+sig x}. Returns dict with blocks, cols, runs, checks."""
    h = lambda x: h0 + sig * x
    N0 = fl(h0) - 1
    blocks = []; info = dict(N0=N0, fail=None)
    if N0 >= 2 and L > 0:
        u = u0; t = F(u, Q); ca, sa, ta, se, e = tilt(t)
        Fb = fl(h0 - N0 * ca - sa)
        if Fb >= 0:
            M = Fb + N0; s = M * ta
            while True:
                if s + se > L: break
                cols = []; i = 0; reason = None
                while True:
                    c = s + i * se
                    if c + se > L: reason = 'L'; break
                    gam = h(c - M * ta)
                    Jf = fl((gam - M * ca - sa) / e)
                    if Jf > M - nmin: reason = 'sat'; break
                    cols.append((c, Jf, M - Jf)); i += 1
                if not cols:
                    info['fail'] = 'empty block'; break
                P = len(cols); cP = s + P * se
                blk = dict(u=u, t=t, ca=ca, sa=sa, ta=ta, se=se, e=e, s=s, M=M, Fb=Fb, cols=cols, P=P, cP=cP,
                           reason=reason, Js=[cc[1] for cc in cols])
                blocks.append(blk)
                if reason == 'L': break
                # ---- next tilt (aligned): largest grid t' with ta(t') <= ta - kappa, kappa = e^2/sig
                kap = e * e / sig
                u2 = largest_u_with_ta_le(ta - kap, Q, u)
                if u2 <= 0: info['fail'] = 'tilt collapse'; break
                t2 = F(u2, Q); ca2, sa2, ta2, se2, e2 = tilt(t2)
                kp = ta - ta2; eta = kp - kap
                J0 = cols[0][1]; JL = cols[-1][1]; Js = blk['Js']
                phi = F(0)
                if JL > J0:
                    A = (h(s - M * ta) - M * ca - sa) / e; B = e / (sig * se)
                    p = bisect.bisect_right(Js, J0)
                    theta = p - B * (J0 + 1 - A)
                    psi = cP - ta2 - (s + p * se) + J0 * kp
                    phi0 = frac(-(psi + theta * (se - 1) - (se - 1)))
                    phi = F(cl(phi0 * GRID), GRID)
                    blk['eps'] = (se - 1) + (JL - J0) * eta + F(1, GRID)
                    blk['theta0'] = theta
                else:
                    blk['eps'] = F(0)
                blk['eta'] = eta; blk['kap'] = kap; blk['phi'] = phi
                s2 = cP + phi
                Fb2 = fl((h0 + sig * s2 - N0 * (ca2 + sig * ta2) - sa2) / (1 + sig * ta2))
                if Fb2 < Fb: info['fail'] = 'F decreasing'; break
                M2 = Fb2 + N0
                if s2 < M2 * ta2: info['fail'] = 'x<0'; break
                u, t, ca, sa, ta, se, e, s, M, Fb = u2, t2, ca2, sa2, ta2, se2, e2, s2, M2, Fb2
        else:
            info['fail'] = 'F0<0'
    # ---- runs (rows), generic: stretch between consecutive blocking blocks
    runs = []; stretches = []
    jtop = fl(h(L))
    for j in range(0, jtop):
        left = F(0); lkind = ('start', -1)
        for bi, blk in enumerate(blocks):
            if blk['cols'][0][1] <= j:
                right = blk['s'] - (j + 1) * blk['ta']
                stretches.append((j, left, right, lkind, ('blk', bi)))
                p = bisect.bisect_right(blk['Js'], j)
                left = (blk['s'] + p * blk['se']) - j * blk['ta']
                lkind = ('slab', bi, p)
        stretches.append((j, left, L, lkind, ('end', -1)))
    for (j, left, right, lk, rk) in stretches:
        # [v3-C] rule (Z4') of the paper, version 1.1 (construction ZC'): a* = max(a, 0, (j + 1 - h0)/sig)
        a_ = max(left, F(0), (j + 1 - h0) / sig) if sig > 0 else max(left, F(0))
        ln = right - a_
        if ln >= 1 and j + 1 <= h(a_):
            runs.append((j, a_, fl(ln)))
    cols = []
    for blk in blocks:
        for (c, J, n) in blk['cols']: cols.append((c, J, n, blk['ca'], blk['sa'], blk['ta']))
    info.update(nblocks=len(blocks), ncols=len(cols), nruns=len(runs), nstretch=len(stretches))
    return dict(blocks=blocks, cols=cols, runs=runs, stretches=stretches, info=info, h0=h0, sig=sig, L=L, u0=u0, Q=Q)

def zpolys(Z):
    out = []
    for (c, J, n, ca, sa, ta) in Z['cols']:
        px, py = c - J * ta, F(J)
        out.append([(px, py), (px + ca, py + sa), (px + ca - n * sa, py + sa + n * ca), (px - n * sa, py + n * ca)])
    for (j, a, Ln) in Z['runs']:
        out.append([(a, F(j)), (a + Ln, F(j)), (a + Ln, F(j + 1)), (a, F(j + 1))])
    return out

def zV(Z): return sum(c[2] for c in Z['cols']) + sum(r[2] for r in Z['runs'])

def zchecks(Z):
    """internal facts used in the proof of Lemma W (exact)."""
    h0, sig, L = Z['h0'], Z['sig'], Z['L']; h = lambda x: h0 + sig * x
    bl = Z['blocks']; out = dict(ok=True, notes=[])
    def bad(msg):
        out['ok'] = False; out['notes'].append(msg)
    for k, blk in enumerate(bl):
        ta, se, e, ca, sa, M = blk['ta'], blk['se'], blk['e'], blk['ca'], blk['sa'], blk['M']
        Js = blk['Js']
        if any(Js[i] > Js[i + 1] for i in range(len(Js) - 1)): bad('J not monotone %d' % k)
        if Js[0] < blk['Fb']: bad('J0<Fb %d' % k)
        if Js[-1] > M - 1: bad('JL>M-1')
        if blk['s'] < M * ta: bad('s<M ta %d' % k)
        for (c, J, n) in blk['cols']:
            gp = h(c - M * ta) - (J + n * ca + sa)
            if not (0 <= gp < e): bad('gap %d' % k); break
        if k + 1 < len(bl):
            nb = bl[k + 1]
            if not (nb['ta'] <= ta): bad('tilt not nonincreasing')
            if nb['s'] < blk['cP']: bad("s' < cP")
            if nb['cols'][0][1] > Js[-1]: bad('next J0 > JL at %d' % k)
            if nb['Fb'] < blk['Fb']: bad('Fb decreasing')
            if blk['eps'] >= 1: bad('eps>=1')
    # residuals of aligned closings
    maxres = F(0); nal = 0
    for (j, left, right, lk, rk) in Z['stretches']:
        if lk[0] == 'slab' and rk[0] == 'blk' and rk[1] == lk[1] + 1:
            blk = bl[lk[1]]
            if lk[2] < blk['P'] and j >= blk['Js'][0]:
                ln = right - left; r = frac(ln); nal += 1
                if ln < 0 or r > blk['eps']: bad('residual j=%d blk=%d r=%s' % (j, lk[1], float(r)))
                maxres = max(maxres, r)
    out['aligned'] = nal; out['maxres'] = float(maxres)
    return out

def zarea(Z): return Z['L'] * Z['h0'] + Z['sig'] * Z['L'] ** 2 / 2

# ----------------------------------------------------------------------------------------------------------
def band(b):
    tt = F(b, b * b - 1)
    c = (1 - tt * tt) / (1 + tt * tt); s = 2 * tt / (1 + tt * tt)
    return dict(c=c, s=s, W=b * c + s, T=s / c, d=1 / c, h=b * s + c)

def build(b, y, cD=F(3), cR=F(3), aw=2.0, Qmain=None):
    """End packing E38 of Reg(y). D = floor(cD m^{3/4}), DR = floor(cR m^{3/4}); wall tilt ta_w ~ aw*sqrt(sig)."""
    Bd = band(b); W, T, sb = Bd['W'], Bd['T'], Bd['s']; y = F(y) if not hasattr(y, 'numerator') else y
    g = lambda X: y + (X - sb) * T
    G0 = g(F(0)); G = g(W)
    m = fl(G) + 1
    m34 = m ** 0.75
    D = int(math.floor(float(cD) * m34)); DR = int(math.floor(float(cR) * m34))
    gD = g(F(D))
    Q = Qmain or (1 << max(4, (16 * b - 1).bit_length()))
    Dd = m + gD; dl = m - gD
    Ft = lambda t: Dd * t * t - 2 * t - dl
    u = math.ceil((1 + math.sqrt(1 + float(Dd) * float(dl))) / float(Dd) * Q)
    while Ft(F(u, Q)) < 0: u += 1
    while u > 0 and Ft(F(u - 1, Q)) >= 0: u -= 1
    t = F(u, Q); ca, sa, ta, se, e = tilt(t)
    c0 = D + m * ta
    cols = []; i = 0
    while True:
        ci = c0 + i * se
        if ci + se > W - DR: break
        gam = g(F(D) + i * se)                       # = g(c_i - m ta)
        J = fl((gam - m * ca - sa) / e)
        cols.append((ci, J, m - J)); i += 1
    N = len(cols); cN = c0 + N * se; Js = [cc[1] for cc in cols]
    JL = Js[-1]; J0 = Js[0]
    # cut line X + Y tau = l0
    kapm = e * e / T
    uc = largest_u_with_ta_le(ta - kapm, QW, 10 ** 30)
    tc = F(uc, QW); cac, sac, tau, sec, ec = tilt(tc)
    kp = ta - tau; eta = kp - kapm
    cmin = cols[-1][0]
    phi = F(0); eps_m = F(0)
    if JL > J0:
        A = (gD - m * ca - sa) / e; Bm = e / (T * se)
        p = bisect.bisect_right(Js, J0); theta = p - Bm * (J0 + 1 - A)
        psi = cmin - tau - (c0 + p * se) + J0 * kp
        phi0 = frac(-(psi + theta * (se - 1) - (se - 1)))
        phi = F(cl(phi0 * GRID), GRID)
        eps_m = (se - 1) + (JL - J0) * eta + F(1, GRID)
    l0 = cmin + phi
    mrows = []; mstretch = []
    for j in range(0, JL):
        p = bisect.bisect_right(Js, j)
        a = c0 + p * se - j * ta
        r = l0 - (j + 1) * tau
        mstretch.append((j, a, r, p))
        if r - a >= 1: mrows.append((j, a, fl(r - a)))
    # wall regions (canonical) and maps
    walls = {}
    def wall(name, h0, sig, L, mp):
        ta_w = aw * math.sqrt(float(sig))
        u0 = t_grid_ceil(ta_w, QW)
        Z = zfill(h0, sig, L, u0) if L > 0 else dict(blocks=[], cols=[], runs=[], stretches=[], info=dict(nblocks=0), h0=h0, sig=sig, L=L)
        walls[name] = (Z, mp)
    walls_def = []
    wall('left', c0 - G0 * ta, ta, G0, lambda x, yy: (yy, G0 - x))
    wall('lowright', W - l0, tau, F(JL), lambda x, yy: (W - yy, x))
    Yu = (G0 + T * cN) / (1 + T * ta)
    wall('upright', W - cN + JL * ta, ta, Yu - JL, lambda x, yy: (W - yy, JL + x))
    return dict(b=b, y=y, Bd=Bd, g=g, G0=G0, G=G, m=m, D=D, DR=DR, gD=gD, Q=Q, t=t, ca=ca, sa=sa, ta=ta, se=se, e=e,
                c0=c0, cols=cols, N=N, cN=cN, Js=Js, JL=JL, J0=J0, tau=tau, kapm=kapm, eta=eta, l0=l0, phi=phi,
                eps_m=eps_m, mrows=mrows, mstretch=mstretch, walls=walls, Yu=Yu, aw=aw, cD=cD, cR=cR)

def polys(C):
    out = []
    ca, sa, ta = C['ca'], C['sa'], C['ta']
    for (ci, J, n) in C['cols']:
        px, py = ci - J * ta, F(J)
        out.append([(px, py), (px + ca, py + sa), (px + ca - n * sa, py + sa + n * ca), (px - n * sa, py + n * ca)])
    for (j, a, Ln) in C['mrows']:
        out.append([(a, F(j)), (a + Ln, F(j)), (a + Ln, F(j + 1)), (a, F(j + 1))])
    for name, (Z, mp) in C['walls'].items():
        for V in zpolys(Z):
            out.append([mp(x, yy) for (x, yy) in V])
    return out

def V_total(C):
    return (sum(c[2] for c in C['cols']) + sum(r[2] for r in C['mrows'])
            + sum(zV(Z) for (Z, mp) in C['walls'].values()))

def area_reg(C):
    Bd = C['Bd']; W, T, s = Bd['W'], Bd['T'], Bd['s']
    return C['y'] * W + T * (W * W / 2 - s * W)

# ---- Lemma W bound B_W and hypotheses (W1)-(W4), evaluated in floats from the actual inputs (comparison only)
def bw_bound(h0, sig, L, u0, Q=QW, Qphi=GRID, mu=0.65):
    h0, sig, L = float(h0), float(sig), float(L)
    t0 = u0 / Q; ta0 = 2 * t0 / (1 - t0 * t0); s0 = math.sqrt(1 + ta0 * ta0); ca0 = 1 / s0
    e0 = ta0 * ta0 / (s0 * (s0 + 1)); tm = mu * ta0; sm = math.sqrt(1 + tm * tm); emin = tm * tm / (sm * (sm + 1))
    N0 = math.floor(h0) - 1; g = 2.1 / Q; hL = h0 + sig * L
    Mmax = hL + N0 * e0
    Lam = (emin * N0 - 1 - sig * ta0) / sig
    if Lam <= 0: return dict(ok=False, why='Lam<=0')
    Kb = L / Lam
    W1 = Lam - N0 * ta0
    W2 = (1 - mu) * ta0 - ((e0 / N0) * (L + Kb * (1 + sig * ta0) / sig) + Kb * g)
    W3 = N0 * ca0 - (sig * s0 / emin + ta0 + sig * (2 + s0 + Mmax * ta0) + (1 + sig * ta0) / emin)
    epsb = (s0 - 1) + N0 * g + 1 / Qphi
    W4 = 1 - epsb
    ccol = ta0 + s0 * e0 + s0 * sig * (s0 + N0 * e0 * ta0)
    hT = 1 + sig * s0 / emin + ta0 + sig * (1 + s0 + Mmax * ta0)
    wT = 1 + (hL + 1) * (e0 * e0 / sig + g)
    w0 = (1 + N0 * e0) * ta0; we = 1 + s0 + (hL + N0 * e0) * ta0
    terms = dict(col=L * ccol, closed=Kb * (N0 - 1) * (epsb + ta0), unal=Kb * ((1 + sig * ta0) / emin) * (1 + ta0),
                 trans=Kb * hT * wT, start=math.floor(h0) * (1 + ta0 / 2) + w0 * (1 + sig * w0),
                 end=hL * (1 + ta0 / 2) + we * (4 + 2 * sig * we))
    B = sum(terms.values())
    return dict(ok=(W1 > 0 and W2 > 0 and W3 > 0 and W4 > 0), W1=W1, W2=W2, W3=W3, W4=W4, B=B, Kbar=Kb, terms=terms)
