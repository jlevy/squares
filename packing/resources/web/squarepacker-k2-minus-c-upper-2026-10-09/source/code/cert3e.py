# Independent interval certification of Corollary 3E / Theorem 4E (k^{3/8} section of the paper), written from the text only.
# All quantities normalised by powers of z = m^{-1/4}; box cover of z in [0, z0] x tau = t/z^2 in [tlo, thi].
import json, sys
from mpmath import iv, mpf, mp
iv.prec = 120
mp.prec = 120

def I(a, b=None):
    return iv.mpf([a, a]) if b is None else iv.mpf([a, b])

def hull(*xs):
    lo = min(x.a for x in xs); hi = max(x.b for x in xs)
    return iv.mpf([lo, hi])

def lo(x): return x.a
def hi(x): return x.b

MU = I('0.65'); AW = I('1.5')
REL = I('1.03e-12')   # relative slack on ta(t~) (text: 1e-12 on t; d ln ta/d ln t <= 1.0203 for t <= 1/10)
B0 = I(10) ** 16
Z0 = (I(12) ** I('0.25')) * (B0 ** I('-0.2'))   # z < 12^{1/4} b^{-1/5}
z0 = mpf(hi(Z0))

def wall(z, sig, h0, Ln, gq, fq):
    """Lemma W in normalised form. sig = sig_n (sig/z^2), h0 = h0_n (h0 z^3), Ln = L z^4 (upper value used),
    gq: g = gq z^5, fq: 1/Qf = fq z^5. Returns dict of margins and normalised pieces of B_W (times z^3)."""
    sq = iv.sqrt(sig)
    ta0 = hull(AW * sq * (1 - REL), AW * sq * (1 + REL) + gq * z ** 4)    # ta0 = ta0_n z
    t0z = ta0 * z
    se0 = iv.sqrt(1 + t0z ** 2)
    ca0 = 1 / se0
    se0m1 = ta0 ** 2 / (se0 + 1)                       # (se0-1)/z^2
    e0 = ta0 ** 2 / (se0 * (se0 + 1))                   # e0/z^2
    sm = iv.sqrt(1 + (MU * t0z) ** 2)
    emin = (MU * ta0) ** 2 / (sm * (sm + 1))            # e_min/z^2
    N0 = hull(h0 - 2 * z ** 3, h0 - z ** 3)             # N0 z^3
    fh = hull(h0 - z ** 3, h0)                          # floor(h0) z^3
    hL = h0 + sig * Ln * z                              # h(L) z^3
    Mmax = hL + N0 * e0 * z ** 2                        # Mmax z^3
    Lam = (emin * N0 - z - sig * ta0 * z ** 4) / sig    # Lam z^3
    Kb = Ln / Lam                                       # Kbar z
    eps = se0m1 + N0 * gq + fq * z ** 3                 # eps / z^2
    W1 = Lam - N0 * ta0 * z
    Dr = (e0 / N0) * (Ln + Kb * (1 + sig * ta0 * z ** 3) * z / sig) + Kb * gq * z ** 3   # Dr / z
    W2 = (1 - MU) * ta0 - Dr
    W3 = N0 * ca0 - z ** 3 * (sig * se0 / emin + ta0 * z + sig * z ** 2 * (2 + se0) + sig * Mmax * ta0) \
         - z * (1 + sig * ta0 * z ** 3) / emin
    W4 = 1 - eps * z ** 2
    W5 = MU * ta0 - gq * z ** 4                         # (mu ta0 - g)/z
    t0max = ta0 * z                                     # t0 <= ta0 (t0 = ta0/(1+se0) actually smaller)
    # B_W pieces (times z^3)
    cc = ta0 + se0 * e0 * z + se0 ** 2 * sig * z + se0 * sig * N0 * e0 * ta0 * z     # c_col / z
    X1 = (N0 - z ** 3) * (eps * z + ta0)                 # (N0-1)(eps+ta0) z^2
    X2 = (1 + sig * ta0 * z ** 3) / emin * (1 + ta0 * z)
    hT = 1 + sig * se0 / emin + ta0 * z + sig * z ** 2 * (1 + se0) + sig * Mmax * ta0
    wT = z + (hL + z ** 3) * (e0 ** 2 / sig + gq * z ** 3)                       # wT z
    X = X1 + X2 + hT * wT * z                            # bracket * z^2
    alpha = cc + X / Lam                                 # coefficient of L_n: L c_col + Kbar X
    w0 = ta0 * z + N0 * e0 * ta0                         # w0
    sigw0 = sig * z ** 2 * w0
    we = z ** 2 * (1 + se0) + hL * ta0 + N0 * e0 * ta0 * z ** 2       # we z^2
    R = fh * (1 + ta0 * z / 2) + w0 * z ** 3 * (1 + sigw0) + hL * (1 + ta0 * z / 2) + we * z * (4 + 2 * sig * we)
    return dict(W1=W1, W2=W2, W3=W3, W4=W4, W5=W5, t0max=t0max, alpha=alpha, R=R, ta0=ta0, sig=sig, Lam=Lam)

def box(zl, zu, tl, tu):
    z = I(zl, zu)
    bh = hull(I(12) ** I('1.25') * (1 - I('5.000001') * z ** 4) ** I('1.25'), I(12) ** I('1.25'))
    Tb = I(2, '2.000001')
    rho = I(2, '2.000001')       # lower bound 2 - 4.2/b^2 irrelevant (only upper used)
    Wb = I(0, 1)                 # W/b <= 1 (only the upper bound is used in the terms)
    Dn = hull(4 - z ** 3, I(4))
    DRn = Dn
    gq = I(0) + I('2.1') / (16 * bh)   # g = 2.1/Q* <= 2.1/(16 b) = gq z^5
    gq = hull(I(0), gq)
    fq = hull(I(0), 1 / (16 * bh))
    tau = I(tl, tu)
    # admissible tau range check: tau must lie in [sqrt(1-4z^2/bh-2.1 z^10/bh^2), upper] -- handled by caller
    t = tau * z ** 2
    t2 = t ** 2
    ta = 2 * tau / (1 - t2)          # ta / z^2
    sa = 2 * tau / (1 + t2)          # sa / z^2
    en = 2 * tau ** 2 / (1 + t2)     # e / z^4
    se = (1 + t2) / (1 - t2)
    sem1 = 2 * tau ** 2 / (1 - t2)   # (se-1)/z^4
    kap = en ** 2 * bh * z / Tb      # kappa_m / z^2 (Tb in [2,2.000001])
    taun = hull(ta - kap - gq * z ** 3, ta - kap)   # tau_cut / z^2
    out = {}
    # (E-i): t <= 1/10
    out['Ei_t'] = I('0.1') - t
    # (E-ii): (W - D - DR - m ta - se) z^5 >= bh(1 - 2.1 z^10/bh^2) - (D+DR) z^2 - ta z^3 - se z^5
    out['Eii'] = bh * (1 - I('2.1') * z ** 10 / bh ** 2) - (Dn + DRn) * z ** 2 - ta * z ** 3 - se * z ** 5
    # (E-iii): (ta - kappa_m - ta(1/Q*)) / z^2, ta(1/Q*) <= 2.1/Q* = gq z^5
    out['Eiii'] = ta - kap - gq * z ** 3
    # (E-iv): 1 - eps_m, eps_m = (se-1) + m g + 1/Qf
    epsm = sem1 * z ** 4 + gq * z + fq * z ** 5
    out['Eiv'] = 1 - epsm
    # main terms of Lemma E (times z^3)
    J0 = (4 * tau * z ** 2 + 2 * z ** 4) / (16 * bh * en)
    tri = bh * sa                                     # W sa
    other = bh * en * z ** 2 + rho * (se * z ** 3 + ta * z) + J0 * (1 + ta * z ** 2) \
        + (sem1 * z ** 3 + gq + fq * z ** 4 + ta * z) \
        + Tb * hull(Dn, Dn + I('3.000001') * ta * z ** 5) ** 2 * z ** 2 / (2 * bh) \
        + Tb * (DRn + se * z ** 3 + ta * z) ** 2 * z ** 2 / bh
    # walls
    ZL = wall(z, ta, hull(Dn, Dn + I('3.000001') * ta * z ** 5), I(1), gq, fq)
    ZLR = wall(z, taun, hull(DRn + sem1 * z ** 7, DRn + 2 * se * z ** 3), I(1), gq, fq)
    ZUR = wall(z, ta, hull(DRn, DRn + se * z ** 3 + ta * z), I(1), gq, fq)
    left = ZL['alpha'] + ZL['R']
    right = hull(ZLR['alpha'], ZUR['alpha']).b
    right = I(right) + ZLR['R'] + ZUR['R']
    Psi = tri + other + left + right
    out['Psi'] = Psi; out['tri'] = tri; out['other'] = other; out['left'] = left; out['right'] = right
    for nm, Z in (('L', ZL), ('LR', ZLR), ('UR', ZUR)):
        for k in ('W1', 'W2', 'W3', 'W4', 'W5'):
            out[k + '_' + nm] = Z[k]
        out['t0_' + nm] = I('0.1') - Z['t0max']
        out['sig_' + nm] = Z['sig']
    return out

def taurange(zl, zu):
    z = I(zl, zu)
    bh = hull(I(12) ** I('1.25') * (1 - I('5.000001') * z ** 4) ** I('1.25'), I(12) ** I('1.25'))
    lo_ = iv.sqrt(1 - 4 * z ** 2 / bh - I('2.1') * z ** 10 / bh ** 2)
    c = I('3.000001')
    up = (z ** 2 + iv.sqrt(z ** 4 + c * (2 - c * z ** 4))) / (2 - c * z ** 4) + z ** 3 / (16 * bh)
    return lo_.a, up.b

def main(NZ=40, NT=16):
    res = {'z0': str(z0), 'NZ': NZ, 'NT': NT}
    mins = {}; psimax = mpf(0); worst = None
    for iz in range(NZ):
        zl = z0 * iz / NZ; zu = z0 * (iz + 1) / NZ
        tl, tu = taurange(zl, zu)
        for it in range(NT):
            a = tl + (tu - tl) * it / NT; bb = tl + (tu - tl) * (it + 1) / NT
            o = box(zl, zu, a, bb)
            for k, v in o.items():
                if k in ('Psi', 'tri', 'other', 'left', 'right') or k.startswith('sig_'):
                    continue
                if k not in mins or v.a < mins[k]:
                    mins[k] = v.a
            if o['Psi'].b > psimax:
                psimax = o['Psi'].b
                worst = dict(z=[str(zl), str(zu)], tau=[str(a), str(bb)],
                             tri=str(o['tri'].b), other=str(o['other'].b), left=str(o['left'].b), right=str(o['right'].b))
    res['margins_min'] = {k: str(mp.nstr(v, 8)) for k, v in mins.items()}
    res['all_positive'] = all(v > 0 for v in mins.values())
    res['Psi_sup'] = str(psimax)
    res['worst_box'] = worst
    fac = (1 + I('60.000012') * B0 ** I('-0.8')) ** I('0.75')
    CE = I(psimax) * I(12) ** I('-0.75') * fac
    res['C_E_cert'] = str(CE.b)
    res['C_E_limit_z0'] = None
    return res

if __name__ == '__main__':
    NZ = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    NT = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    r = main(NZ, NT)
    print(json.dumps(r, indent=1))
    with open(__file__.replace('cert3e.py', 'cert3e_out_%d_%d.json' % (NZ, NT)), 'w') as f:
        json.dump(r, f, indent=1)
