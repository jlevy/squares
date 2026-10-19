# cert_v3.py -- interval certification of Corollary 3E' and Theorem 4E' of the paper (version 1.1), tier by tier.
# Author's program (AI agent "v3", 2026-10-09). A generalisation of code/cert3e.py
# (version 1.0 of this repository). mpmath.iv, 120 bits. Every number written to the theorem is checked here.
#
# What is evaluated on each box (z, t/z^2) of the cover of (0, z0] x [t-range] (see the paper, proof of the Corollary on the band ends):
#   main part: (E-i) 1/10 - t, (E-ii), (E-iii), (E-iv) in the corrected form 1 - eps_m - tau;
#   three walls: (W1)-(W5), h0 >= 4, 1/10 - t0 with the exact half-angle formula t0 = ta0/(1 + se0);
#   Psi = z^3 x (bound of Lemma E with B_W of Lemma W, or of Lemma W'' when the tier uses parts B, C).
# Parts:  'A'   -> B_W of Lemma W (unchanged from version 1.0).
#         'ABC' -> B_W'' of Lemma W'' (paper, version 1.1): transition term A_T replaced by A_T' (Lemma P2) and the
#                  end-region term we(4 + 2 sig we) replaced by we + 2(1 + ta0) (Lemma P3, construction ZC').
# Usage:
#   python cert_v3.py run   --tier T [--nz NZ --nt NT --iz0 I0 --iz1 I1] [--params cy,cd,cr,aw,mu --lb0 X --parts A]
#   python cert_v3.py merge --tier T files...        (checks the slices cover [0, nz) x [0, nt) exactly once)
#   python cert_v3.py search ...                     (see opt_v3.py; uses 'run' on the whole range)
import json, sys, time, argparse
from mpmath import iv, mpf, mp
iv.prec = 120
mp.prec = 120

# ---------------------------------------------------------------- tier table of the paper (Theorem 4E' = Theorem 1.1)
# lb0: b0 = 10^lb0.  CE, C, k, a: the constants stated in the theorem (checked in 'merge').
TIERS = {}
try:
    TIERS = json.load(open('tiers_v3.json'))
except Exception:
    pass

def I(a, b=None):
    return iv.mpf([a, a]) if b is None else iv.mpf([a, b])

def frac(s):
    s = str(s)
    if '/' in s:
        p, q = s.split('/'); return I(p) / I(q)
    return I(s)

def hull(*xs):
    lo = min(LO(x) for x in xs); hi = max(HI(x) for x in xs)
    return iv.mpf([lo, hi])

def LO(x):                # exact lower endpoint (mpf) of an interval
    return mp.make_mpf(x._mpi_[0]) if hasattr(x, '_mpi_') else mpf(x)

def HI(x):                # exact upper endpoint (mpf) of an interval
    return mp.make_mpf(x._mpi_[1]) if hasattr(x, '_mpi_') else mpf(x)

def mexact(x):            # exact (man, exp) of an mpf
    x = mpf(x)
    if x == 0:
        return [0, 0]
    m, e = x.man_exp
    return [int(m), int(e)]

def mfrom(me):
    return mpf(me[0]) * mpf(2) ** me[1]

class P:
    pass

def setup(lb0, cy, cd, cr, aw, mu, parts, rel='1.03e-12'):
    p = P()
    p.lb0 = lb0; p.parts = parts
    p.MU = frac(mu); p.AW = frac(aw); p.REL = I(rel)
    p.CY = frac(cy); p.CD = frac(cd); p.CR = frac(cr)
    p.B0 = I(10) ** frac(lb0)
    p.BH_UP = p.CY ** I('-1.25')                       # bh = b z^5 < cy^{-5/4}
    p.Z0 = (p.CY ** I('-0.25')) * (p.B0 ** I('-0.2'))   # z < cy^{-1/4} b^{-1/5} <= z0
    p.z0 = HI(p.Z0)
    p.TINY = I('1e-40')
    return p

def wall(p, z, sig, h0, Ln, gq, fq):
    flag = False
    if LO(sig) <= 0:          # only if (E-iii) fails; then the box fails anyway (Eiii margin <= 0)
        sig = iv.mpf([LO(p.TINY), max(HI(sig), HI(p.TINY))]); flag = True
    sq = iv.sqrt(sig)
    ta0 = hull(p.AW * sq * (1 - p.REL), p.AW * sq * (1 + p.REL) + gq * z ** 4)   # ta0/z
    t0z = ta0 * z
    se0 = iv.sqrt(1 + t0z ** 2)
    ca0 = 1 / se0
    se0m1 = ta0 ** 2 / (se0 + 1)
    e0 = ta0 ** 2 / (se0 * (se0 + 1))
    sm = iv.sqrt(1 + (p.MU * t0z) ** 2)
    emin = (p.MU * ta0) ** 2 / (sm * (sm + 1))
    N0 = hull(h0 - 2 * z ** 3, h0 - z ** 3)
    fh = hull(h0 - z ** 3, h0)
    hL = h0 + sig * Ln * z
    Mmax = hL + N0 * e0 * z ** 2
    Lam = (emin * N0 - z - sig * ta0 * z ** 4) / sig
    Kb = Ln / Lam
    eps = se0m1 + N0 * gq + fq * z ** 3
    W1 = Lam - N0 * ta0 * z
    Dr = (e0 / N0) * (Ln + Kb * (1 + sig * ta0 * z ** 3) * z / sig) + Kb * gq * z ** 3
    W2 = (1 - p.MU) * ta0 - Dr
    W3 = N0 * ca0 - z ** 3 * (sig * se0 / emin + ta0 * z + sig * z ** 2 * (2 + se0) + sig * Mmax * ta0) \
         - z * (1 + sig * ta0 * z ** 3) / emin
    W4 = 1 - eps * z ** 2
    W5 = p.MU * ta0 - gq * z ** 4
    t0max = ta0 * z / (1 + se0)                  # t0 = tan(a0)/(1 + sec(a0)), exact half-angle formula
    h0ge4 = h0 - 4 * z ** 3
    cc = ta0 + se0 * e0 * z + se0 ** 2 * sig * z + se0 * sig * N0 * e0 * ta0 * z
    X1 = (N0 - z ** 3) * (eps * z + ta0)
    X2 = (1 + sig * ta0 * z ** 3) / emin * (1 + ta0 * z)
    hT = 1 + sig * se0 / emin + ta0 * z + sig * z ** 2 * (1 + se0) + sig * Mmax * ta0
    wT = z + (hL + z ** 3) * (e0 ** 2 / sig + gq * z ** 3)                         # wT z
    if p.parts == 'ABC':
        # Lemma P2: A_T' = (hT + 1)(1 + ta0) + (2 + sig (wT + ta0 + sig ta0)) (wT + ta0), times z^2
        X3 = (hT + 1) * (1 + ta0 * z) * z ** 2 \
             + (2 + sig * wT * z + sig * ta0 * z ** 3 + sig ** 2 * ta0 * z ** 5) * (wT * z + ta0 * z ** 3)
    else:
        X3 = hT * wT * z                                                           # A_T = hT wT, times z^2
    X = X1 + X2 + X3
    alpha = cc + X / Lam
    w0 = ta0 * z + N0 * e0 * ta0
    sigw0 = sig * z ** 2 * w0
    we = z ** 2 * (1 + se0) + hL * ta0 + N0 * e0 * ta0 * z ** 2                   # we z^2
    Rstart = fh * (1 + ta0 * z / 2) + w0 * z ** 3 * (1 + sigw0)
    Rend = hL * (1 + ta0 * z / 2)
    if p.parts == 'ABC':
        Rwe = we * z + 2 * (1 + ta0 * z) * z ** 3                                 # Lemma P3: (we + 2(1 + ta0)) z^3
    else:
        Rwe = we * z * (4 + 2 * sig * we)                                          # we (4 + 2 sig we) z^3
    R = Rstart + Rend + Rwe
    parts = dict(ccol=cc, aligned=X1 / Lam, unaligned=X2 / Lam, transition=X3 / Lam, Rstart=Rstart, Rend=Rend, Rwe=Rwe)
    return dict(W1=W1, W2=W2, W3=W3, W4=W4, W5=W5, t0max=t0max, h0ge4=h0ge4, alpha=alpha, R=R, parts=parts, flag=flag)

def bhat(p, z):
    return hull(p.BH_UP * (1 - I('5.000001') * z ** 4) ** I('1.25'), p.BH_UP)

def box(p, zl, zu, tl, tu):
    z = I(zl, zu)
    bh = bhat(p, z)
    Tb = I(2, '2.000001')
    rho = I(2, '2.000001')
    Dn = hull(p.CD - z ** 3, p.CD)
    DRn = hull(p.CR - z ** 3, p.CR)
    gq = hull(I(0), I('2.1') / (16 * bh))
    fq = hull(I(0), 1 / (16 * bh))
    tau = I(tl, tu)
    t = tau * z ** 2
    t2 = t ** 2
    ta = 2 * tau / (1 - t2)
    sa = 2 * tau / (1 + t2)
    en = 2 * tau ** 2 / (1 + t2)
    se = (1 + t2) / (1 - t2)
    sem1 = 2 * tau ** 2 / (1 - t2)
    kap = en ** 2 * bh * z / Tb
    taun = hull(ta - kap - gq * z ** 3, ta - kap)
    out = {}
    out['Ei_t'] = I('0.1') - t
    out['Eii'] = bh * (1 - I('2.1') * z ** 10 / bh ** 2) - (Dn + DRn) * z ** 2 - ta * z ** 3 - se * z ** 5
    out['Eiii'] = ta - kap - gq * z ** 3
    epsm = sem1 * z ** 4 + gq * z + fq * z ** 5
    out['Eiv'] = 1 - epsm - taun * z ** 2
    J0 = (4 * tau * z ** 2 + 2 * z ** 4) / (16 * bh * en)
    tri = bh * sa
    other = bh * en * z ** 2 + rho * (se * z ** 3 + ta * z) + J0 * (1 + ta * z ** 2) \
        + (sem1 * z ** 3 + gq + fq * z ** 4 + ta * z) \
        + Tb * hull(Dn, Dn + I('3.000001') * ta * z ** 5) ** 2 * z ** 2 / (2 * bh) \
        + Tb * (DRn + se * z ** 3 + ta * z) ** 2 * z ** 2 / bh
    ZL = wall(p, z, ta, hull(Dn, Dn + I('3.000001') * ta * z ** 5), I(1), gq, fq)
    ZLR = wall(p, z, taun, hull(DRn + sem1 * z ** 7, DRn + 2 * se * z ** 3), I(1), gq, fq)
    ZUR = wall(p, z, ta, hull(DRn, DRn + se * z ** 3 + ta * z), I(1), gq, fq)
    left = ZL['alpha'] + ZL['R']
    right = I(HI(hull(ZLR['alpha'], ZUR['alpha']))) + ZLR['R'] + ZUR['R']
    Psi = tri + other + left + right
    out['Psi'] = Psi
    for nm, Z in (('L', ZL), ('LR', ZLR), ('UR', ZUR)):
        for k in ('W1', 'W2', 'W3', 'W4', 'W5', 'h0ge4'):
            out[k + '_' + nm] = Z[k]
        out['t0_' + nm] = I('0.1') - Z['t0max']
    brk = dict(tri=HI(tri), other=HI(other), left=HI(left), right=HI(right))
    for nm, Z in (('L', ZL), ('LR', ZLR), ('UR', ZUR)):
        for k, v in Z['parts'].items():
            brk[nm + '_' + k] = HI(v)
    return out, brk

def taurange(p, zl, zu):
    z = I(zl, zu)
    bh = bhat(p, z)
    lo_ = iv.sqrt(1 - p.CD * z ** 2 / bh - I('2.1') * z ** 10 / bh ** 2)    # D_l/b <= cD z^2/bh
    c = I('3.000001')
    up = (z ** 2 + iv.sqrt(z ** 4 + c * (2 - c * z ** 4))) / (2 - c * z ** 4) + z ** 3 / (16 * bh)
    return LO(lo_), HI(up)

def params_of(A):
    if A.tier:
        T = TIERS[A.tier]
        return T['lb0'], T['cy'], T['cd'], T['cr'], T['aw'], T['mu'], T['parts']
    cy, cd, cr, aw, mu = A.params.split(',')
    return A.lb0, cy, cd, cr, aw, mu, A.parts

def run(A):
    T0 = time.time()
    lb0, cy, cd, cr, aw, mu, parts = params_of(A)
    p = setup(lb0, cy, cd, cr, aw, mu, parts, A.rel)
    NZ, NT = A.nz, A.nt
    iz0 = A.iz0; iz1 = NZ if A.iz1 < 0 else A.iz1
    mins = {}; psimax = mpf(0); worst = None; nbox = 0; fails = {}
    for iz in range(iz0, iz1):
        zl = p.z0 * iz / NZ; zu = p.z0 * (iz + 1) / NZ
        tl, tu = taurange(p, zl, zu)
        for it in range(NT):
            a = tl + (tu - tl) * it / NT; bb = tl + (tu - tl) * (it + 1) / NT
            o, brk = box(p, zl, zu, a, bb)
            nbox += 1
            for k, v in o.items():
                if k == 'Psi':
                    continue
                if k not in mins or LO(v) < mins[k]:
                    mins[k] = LO(v)
                if not (LO(v) > 0):
                    fails[k] = fails.get(k, 0) + 1
            pb = HI(o['Psi'])
            if not (pb < mpf('1e300')):
                pb = mpf('inf')
            if pb > psimax:
                psimax = pb
                worst = dict(iz=iz, it=it, z=[float(zl), float(zu)], tn=[float(a), float(bb)],
                             **{k: float(v) for k, v in brk.items()})
    res = dict(kind='slice', tier=A.tier, lb0=lb0, cy=cy, cd=cd, cr=cr, aw=aw, mu=mu, parts=parts, rel=A.rel,
               nz=NZ, nt=NT, iz0=iz0, iz1=iz1, nbox=nbox, z0=float(p.z0),
               margins_min={k: float(v) for k, v in mins.items()},
               margins_min_exact={k: mexact(v) for k, v in mins.items()},
               fails=fails, all_positive=(len(fails) == 0),
               psimax=float(psimax) if psimax < mpf('1e300') else None,
               psimax_exact=mexact(psimax) if psimax < mpf('1e300') else None,
               worst=worst, seconds=round(time.time() - T0, 1))
    return res, p

def constants(p, psimax, lb0):
    fac = (1 + I('5.000001') / p.CY * p.B0 ** I('-0.8')) ** I('0.75')
    CE = I(psimax) * p.CY ** I('0.75') * fac
    ce = HI(CE)
    cp = I('6.4') * (I(5) / 3) ** I('0.375') * I(ce) ** I('0.625')
    return dict(C_E_cert=float(ce), C_E_cert_exact=mexact(ce), Cprime=float(HI(cp)),
                k0=float(HI(I('0.6') * I(ce) * p.B0 ** I('1.6'))),
                additive=float(HI(I('2.4') * I(ce) * p.B0 ** I('-0.4'))),
                k_cross_2_5=float(HI((cp / I('20.668')) ** 40)))

def theorem_check(p, ce_cert, T):
    """checks the stated constants of the tier: C_E >= certified, C >= (32/5)(5/3)^{3/8} C_E^{5/8},
    k >= (3/5) C_E b0^{8/5}, a >= (12/5) C_E b0^{-2/5}, lambda' bound < 1 at b = b0, and y0-room for k >= k."""
    CE = frac(T['CE']); C = frac(T['C']); K = frac(T['k']); A_ = frac(T['a'])
    chk = {}
    chk['CE_stated>=cert'] = bool(LO(CE) >= ce_cert)
    cp = I('32') / 5 * (I(5) / 3) ** I('0.375') * CE ** I('0.625')
    chk['C>=Cprime(CE)'] = bool(LO(C) >= HI(cp))
    chk['k>=k0(CE)'] = bool(LO(K) >= HI(I(3) / 5 * CE * p.B0 ** I('1.6')))
    chk['a>=(12/5)CE b0^-2/5'] = bool(LO(A_) >= HI(I(12) / 5 * CE * p.B0 ** I('-0.4')))
    lam = I('8.001') * I(3) / 5 * CE * p.B0 ** I('-1.4') + I('4.1') / p.B0
    chk['lambda_bound<1'] = bool(HI(lam) < 1)
    chk['lambda_bound'] = float(HI(lam))
    # room (Theorem 4E' proof): y0 <= cy b^{4/5} + 1/4, b <= b* + 1, b^{4/5} <= b*^{4/5} + 1,
    # b*^{4/5} = (5k/(3 CE))^{1/2}; so y0 <= k^{1/2} + 1 if cy (5/(3 CE))^{1/2} <= 1 and cy <= 3/4.
    chk['room_cy_sqrt'] = bool(HI(p.CY * iv.sqrt(I(5) / (3 * CE))) <= 1 and HI(p.CY) <= LO(I('0.75')))
    chk['cross_2_5'] = float(HI((C / I('20.668')) ** 40))
    chk['k_below_cross'] = bool(HI(K) <= LO((C / I('20.668')) ** 40))
    return chk

def merge(A, files):
    S = [json.loads(open(f).read().strip().splitlines()[-1]) for f in files]
    S = [s for s in S if s.get('kind') == 'slice']
    keys = ('tier', 'lb0', 'cy', 'cd', 'cr', 'aw', 'mu', 'parts', 'rel', 'nz', 'nt')
    ref = {k: S[0][k] for k in keys}
    out = dict(kind='merged', files=[f for f in files], **ref)
    same = all(all(s[k] == ref[k] for k in keys) for s in S)
    covered = [0] * ref['nz']
    for s in S:
        for iz in range(s['iz0'], s['iz1']):
            covered[iz] += 1
    out['same_params'] = same
    out['cover_exact_once'] = all(c == 1 for c in covered)
    out['nbox'] = sum(s['nbox'] for s in S)
    out['nbox_expected'] = ref['nz'] * ref['nt']
    mins = {}
    for s in S:
        for k, v in s['margins_min_exact'].items():
            v = mfrom(v)
            if k not in mins or v < mins[k]:
                mins[k] = v
    out['margins_min'] = {k: float(v) for k, v in mins.items()}
    out['all_positive'] = all(s['all_positive'] for s in S) and all(v > 0 for v in mins.values())
    w2 = min(mins[k] for k in mins if k.startswith('W2_'))
    out['W2_min'] = float(w2)
    if any(s['psimax_exact'] is None for s in S):
        out['valid'] = False; return out
    psimax = max(mfrom(s['psimax_exact']) for s in S)
    out['Psi_sup'] = float(psimax)
    out['worst'] = max(S, key=lambda s: mfrom(s['psimax_exact']))['worst']
    p = setup(ref['lb0'], ref['cy'], ref['cd'], ref['cr'], ref['aw'], ref['mu'], ref['parts'], ref['rel'])
    c = constants(p, psimax, ref['lb0'])
    out.update(c)
    out['valid'] = bool(same and out['cover_exact_once'] and out['nbox'] == out['nbox_expected'] and out['all_positive'])
    if A.tier and A.tier in TIERS and 'CE' in TIERS[A.tier]:
        chk = theorem_check(p, mfrom(c['C_E_cert_exact']), TIERS[A.tier])
        out['theorem_check'] = chk
        out['theorem_ok'] = out['valid'] and all(v for k, v in chk.items() if isinstance(v, bool) and k != 'k_below_cross')
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['run', 'merge'])
    ap.add_argument('files', nargs='*')
    ap.add_argument('--tier', type=str, default='')
    ap.add_argument('--lb0', type=str, default='16')
    ap.add_argument('--params', type=str, default='1/12,4,4,1.5,0.65')
    ap.add_argument('--parts', type=str, default='A')
    ap.add_argument('--nz', type=int, default=160)
    ap.add_argument('--nt', type=int, default=64)
    ap.add_argument('--iz0', type=int, default=0)
    ap.add_argument('--iz1', type=int, default=-1)
    ap.add_argument('--rel', type=str, default='1.03e-12')
    ap.add_argument('--full', type=int, default=0)   # run: also print the merged constants (single full slice)
    A = ap.parse_args()
    if A.mode == 'run':
        res, p = run(A)
        if A.full and res['psimax_exact'] is not None:
            res.update(constants(p, mfrom(res['psimax_exact']), res['lb0']))
            res['W2_min'] = min(v for k, v in res['margins_min'].items() if k.startswith('W2_'))
            res['valid'] = res['all_positive'] and res['iz0'] == 0 and res['iz1'] == res['nz']
        print(json.dumps(res))
    else:
        print(json.dumps(merge(A, A.files)))

if __name__ == '__main__':
    main()
