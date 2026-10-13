# cert_v4.py -- interval covering for the corollary and theorem of the paper for the tiers C.
# Written 2026-10-10 by the v4 author agent (AI). Adapted from a copy of code/cert_v3/cert_v3.py (the program of
# the tiers without double dagger). NO switches: this program implements exactly the v4 statements:
#   * parts A, B, C of v3 (Lemma E, Lemmas W, P2, P3a, P3 for ZC'),
#   * Lemma T1 / Lemma W4 of v4 (sawtooth accounting of the start rows and of the final stretches), with
#       start:  floor(h0)(1/2 + ta0) + 1/(8 ta0) + w0 (1 + sig w0)
#       end:    h(L)(1/2 + ta0 + (se0 - 1)) + (Kbar + 2)/(8 beta_*) + (1/2)(2 + N0 e0 + (1 + sig ta0)/e_min)
#               + (1/2)(1 + sig L + sig we) + we + 2(1 + ta0)
#     and the new hypothesis (W6) beta_* := mu ta0 - e0^2/sig > 0,
#   * T2 (Corollary 3E'' window): y in [cy b^{4/5}, cy b^{4/5} + 2.0001] with frac(G(y)) >= 1/2, hence
#       delta <= 2.500001 (the t-range uses 2.500002) and m <= cy b^{4/5} + 4.500101 (the program uses 4.5002).
# Normalisation: the appendix of the paper with the replacements of its last appendix.
# Usage:
#   python cert_v4.py run   --lb0 X --params cy,cD,cR,awL,awLR,awUR,mu --nz NZ --nt NT --iz0 A --iz1 B  > slice.json
#   python cert_v4.py merge --stated CE,Ci,ki,ai slice1.json slice2.json ...                         > merged.json
import json, sys, time, argparse
from mpmath import iv, mpf, mp
iv.prec = 120
mp.prec = 120

WEXT_S = '4.5002'      # m <= cy b^{4/5} + WEXT   (v4: 4.500101)
CDEL_S = '2.500002'    # delta = m - g0 <= CDEL   (v4: 2.500001)
REL_S = '1.03e-12'     # eps' of (E6)


def I(a, b=None):
    return iv.mpf([a, a]) if b is None else iv.mpf([a, b])


def frac(s):
    s = str(s)
    if '/' in s:
        p, q = s.split('/'); return I(p) / I(q)
    return I(s)


def LO(x):
    return mp.make_mpf(x._mpi_[0]) if hasattr(x, '_mpi_') else mpf(x)


def HI(x):
    return mp.make_mpf(x._mpi_[1]) if hasattr(x, '_mpi_') else mpf(x)


def hull(*xs):
    return iv.mpf([min(LO(x) for x in xs), max(HI(x) for x in xs)])


class P:
    pass


def setup(lb0, params):
    p = P()
    v = params.split(',')
    assert len(v) == 7, 'params: cy,cD,cR,awL,awLR,awUR,mu'
    p.pstr = ','.join(v)
    p.lb0 = lb0
    p.CY, p.CD, p.CR = frac(v[0]), frac(v[1]), frac(v[2])
    p.AW = dict(L=frac(v[3]), LR=frac(v[4]), UR=frac(v[5]))
    p.MU = frac(v[6])
    p.REL = I(REL_S)
    p.WEXT = I(WEXT_S)
    p.CDEL = I(CDEL_S)
    p.B0 = I(10) ** frac(lb0)
    p.BH_UP = p.CY ** I('-1.25')
    p.Z0 = (p.CY ** I('-0.25')) * (p.B0 ** I('-0.2'))
    p.z0 = HI(p.Z0)          # covering of [0, z0] with z0 rounded up (covers the true z0)
    p.TINY = I('1e-40')
    return p


def wall(p, nm, z, sig, h0, Ln, gq, fq):
    """One wall Z(h0, sig, L) filled by ZC', normalised (Appendix A'.3 with the v4 terms of A''.2).
    z, sig (= zeta_n), h0 (= chi_n), Ln, gq, fq are intervals."""
    AW = p.AW[nm]; MU = p.MU
    flag = False
    if LO(sig) <= 0:
        sig = iv.mpf([LO(p.TINY), max(HI(sig), HI(p.TINY))]); flag = True
    sq = iv.sqrt(sig)
    ta0 = hull(AW * sq * (1 - p.REL), AW * sq * (1 + p.REL) + gq * z ** 4)      # a_n = ta0/z
    t0z = ta0 * z
    se0 = iv.sqrt(1 + t0z ** 2)
    ca0 = 1 / se0
    se0m1 = ta0 ** 2 / (se0 + 1)                                                # (se0 - 1)/z^2
    e0 = ta0 ** 2 / (se0 * (se0 + 1))                                           # q0n = e0/z^2
    sm = iv.sqrt(1 + (MU * t0z) ** 2)
    emin = (MU * ta0) ** 2 / (sm * (sm + 1))                                    # qmn = e_min/z^2
    N0 = hull(h0 - 2 * z ** 3, h0 - z ** 3)                                     # N0 z^3
    fh = hull(h0 - z ** 3, h0)                                                  # floor(h0) z^3
    hL = h0 + sig * Ln * z                                                      # h(L) z^3
    Mmax = hL + N0 * e0 * z ** 2                                                # Mmax z^3
    Lam = (emin * N0 - z - sig * ta0 * z ** 4) / sig                            # Lam z^3
    Kb = Ln / Lam                                                               # Kbar z
    eps = se0m1 + N0 * gq + fq * z ** 3                                         # eps/z^2
    W1 = Lam - N0 * ta0 * z
    Dr = (e0 / N0) * (Ln + Kb * (1 + sig * ta0 * z ** 3) * z / sig) + Kb * gq * z ** 3
    W2 = (1 - MU) * ta0 - Dr
    W3 = N0 * ca0 - z ** 3 * (sig * se0 / emin + ta0 * z + sig * z ** 2 * (2 + se0) + sig * Mmax * ta0) \
         - z * (1 + sig * ta0 * z ** 3) / emin
    W4 = 1 - eps * z ** 2
    W5 = MU * ta0 - gq * z ** 4
    betan = MU * ta0 - e0 ** 2 * z / sig                                        # (W6): beta_*/z
    t0max = ta0 * z / (1 + se0)                                                 # t_up (exact half-angle, Tw = ta0 z)
    h0ge4 = h0 - 4 * z ** 3
    cc = ta0 + se0 * e0 * z + se0 ** 2 * sig * z + se0 * sig * N0 * e0 * ta0 * z
    X1 = (N0 - z ** 3) * (eps * z + ta0)
    X2 = (1 + sig * ta0 * z ** 3) / emin * (1 + ta0 * z)
    hT = 1 + sig * se0 / emin + ta0 * z + sig * z ** 2 * (1 + se0) + sig * Mmax * ta0
    wT = z + (hL + z ** 3) * (e0 ** 2 / sig + gq * z ** 3)                      # w_T z
    X3 = (hT + 1) * (1 + ta0 * z) * z ** 2 \
         + (2 + sig * wT * z + sig * ta0 * z ** 3 + sig ** 2 * ta0 * z ** 5) * (wT * z + ta0 * z ** 3)   # A_T' z^2
    X = X1 + X2 + X3
    alpha = cc + X / Lam
    w0 = ta0 * z + N0 * e0 * ta0
    sigw0 = sig * z ** 2 * w0
    we = z ** 2 * (1 + se0) + hL * ta0 + N0 * e0 * ta0 * z ** 2                 # we z^2
    # v4, Lemma W4 (T1):
    Rstart = fh * (I('0.5') + ta0 * z) + z ** 2 / (8 * ta0) + w0 * z ** 3 * (1 + sigw0)
    Rend = hL * (I('0.5') + ta0 * z + se0m1 * z ** 2) \
        + (Kb * z + 2 * z ** 2) / (8 * betan) \
        + I('0.5') * (N0 * e0 * z ** 2 + 2 * z ** 3 + z * (1 + sig * ta0 * z ** 3) / emin) \
        + I('0.5') * (z ** 3 + sig * Ln * z + sig * we * z ** 3)
    Rwe = we * z + 2 * (1 + ta0 * z) * z ** 3
    R = Rstart + Rend + Rwe
    parts = dict(ccol=cc, aligned=X1 / Lam, unaligned=X2 / Lam, transition=X3 / Lam, Rstart=Rstart, Rend=Rend, Rwe=Rwe)
    out = dict(W1=W1, W2=W2, W3=W3, W4=W4, W5=W5, W6=betan, t0max=t0max, h0ge4=h0ge4, alpha=alpha, R=R, parts=parts,
               flag=flag)
    return out


def bhat(p, z):
    return hull(p.BH_UP * (1 - p.WEXT * z ** 4) ** I('1.25'), p.BH_UP)


def box(p, zl, zu, tl, tu):
    z = I(zl, zu)
    bh = bhat(p, z)
    Tb = I(2, '2.000001')
    rho = I(2, '2.000001')
    Dn = hull(p.CD - z ** 3, p.CD)
    DRn = hull(p.CR - z ** 3, p.CR)
    gq = hull(I(0), I('2.1') / (16 * bh))
    fq = hull(I(0), 1 / (16 * bh))
    tau = I(tl, tu)                        # tn = t/z^2
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
    h0L = hull(Dn, Dn + I('3.000001') * ta * z ** 5)        # delta <= 2.500001 <= 3.000001 (enclosure kept from v3)
    other = bh * en * z ** 2 + rho * (se * z ** 3 + ta * z) + J0 * (1 + ta * z ** 2) \
        + (sem1 * z ** 3 + gq + fq * z ** 4 + ta * z) \
        + Tb * h0L ** 2 * z ** 2 / (2 * bh) \
        + Tb * (DRn + se * z ** 3 + ta * z) ** 2 * z ** 2 / bh
    ZL = wall(p, 'L', z, ta, h0L, I(1), gq, fq)
    ZLR = wall(p, 'LR', z, taun, hull(DRn + sem1 * z ** 7, DRn + 2 * se * z ** 3), I(1), gq, fq)
    ZUR = wall(p, 'UR', z, ta, hull(DRn, DRn + se * z ** 3 + ta * z), I(1), gq, fq)
    left = ZL['alpha'] + ZL['R']
    right = I(HI(hull(ZLR['alpha'], ZUR['alpha']))) + ZLR['R'] + ZUR['R']
    Psi = tri + other + left + right
    out['Psi'] = Psi
    for nm, Z in (('L', ZL), ('LR', ZLR), ('UR', ZUR)):
        for k in ('W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'h0ge4'):
            out[k + '_' + nm] = Z[k]
        out['t0_' + nm] = I('0.1') - Z['t0max']
        if Z['flag']:
            out['sigpos_' + nm] = I(-1)    # sig <= 0 on the box: counted as a failure
    brk = dict(tri=HI(tri), other=HI(other), left=HI(left), right=HI(right))
    for nm, Z in (('L', ZL), ('LR', ZLR), ('UR', ZUR)):
        for k, v in Z['parts'].items():
            brk[nm + '_' + k] = HI(v)
    return out, brk


def taurange(p, zl, zu):
    z = I(zl, zu)
    bh = bhat(p, z)
    lo_ = iv.sqrt(1 - p.CD * z ** 2 / bh - I('2.1') * z ** 10 / bh ** 2)
    c = p.CDEL
    up = (z ** 2 + iv.sqrt(z ** 4 + c * (2 - c * z ** 4))) / (2 - c * z ** 4) + z ** 3 / (16 * bh)
    return LO(lo_), HI(up)


def zedges(p, NZ):
    # z-interval iz is [z0*iz/NZ, z0*(iz+1)/NZ] computed in mp (120 bits) from the same z0; adjacent intervals share
    # their endpoint exactly (the same mpf expression), so the union is [0, z0] without gaps.
    E = [p.z0 * iz / NZ for iz in range(NZ + 1)]
    E[0] = mpf(0); E[NZ] = p.z0          # exact ends: z = 0 included, top end = z0 (rounded up)
    return E


def run(A):
    T0 = time.time()
    p = setup(A.lb0, A.params)
    NZ, NT = A.nz, A.nt
    E = zedges(p, NZ)
    iz0, iz1 = A.iz0, (A.iz1 if A.iz1 >= 0 else NZ)
    mins = {}; psimax = mpf(0); worst = None; nbox = 0; fails = {}
    for iz in range(iz0, iz1):
        zl, zu = E[iz], E[iz + 1]
        tl, tu = taurange(p, zl, zu)
        for it in range(NT):
            a = tl + (tu - tl) * it / NT; bb = tl + (tu - tl) * (it + 1) / NT
            if it == NT - 1:
                bb = tu
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
                fails['Psi_nonfinite'] = fails.get('Psi_nonfinite', 0) + 1
            if pb > psimax:
                psimax = pb
                worst = dict(iz=iz, it=it, z=[float(zl), float(zu)], tn=[float(a), float(bb)],
                             **{k: float(v) for k, v in brk.items()})
    res = dict(kind='slice_v4', lb0=A.lb0, params=p.pstr, nz=NZ, nt=NT, iz0=iz0, iz1=iz1, nbox=nbox,
               z0=mp.nstr(p.z0, 40), wext=WEXT_S, cdel=CDEL_S, rel=REL_S,
               margins_min={k: mp.nstr(v, 20) for k, v in mins.items()}, fails=fails,
               all_positive=(len(fails) == 0), psimax=mp.nstr(psimax, 40) if psimax < mpf('1e300') else None,
               worst=worst, seconds=round(time.time() - T0, 1))
    return res


def merge(A):
    sl = [json.load(open(f)) for f in A.files]
    out = dict(kind='merged_v4', files=A.files, checks={})
    c = out['checks']
    keys = set((s['lb0'], s['params'], s['nz'], s['nt'], s['z0'], s['wext'], s['cdel'], s['rel']) for s in sl)
    c['same_parameters'] = (len(keys) == 1)
    lb0, params, NZ, NT, z0, wext, cdel, rel = list(keys)[0]
    cover = [0] * NZ
    for s in sl:
        for iz in range(s['iz0'], s['iz1']):
            cover[iz] += 1
    c['every_z_interval_exactly_once'] = all(x == 1 for x in cover)
    c['box_count'] = sum(s['nbox'] for s in sl)
    c['box_count_ok'] = (c['box_count'] == NZ * NT)
    c['all_margins_positive'] = all(s['all_positive'] for s in sl)
    psimax = max(mpf(s['psimax']) for s in sl)
    mins = {}
    for s in sl:
        for k, v in s['margins_min'].items():
            v = mpf(v)
            if k not in mins or v < mins[k]:
                mins[k] = v
    p = setup(lb0, params)
    c['z0_matches_params'] = (mp.nstr(p.z0, 40) == z0)
    fac = (1 + p.WEXT / p.CY * p.B0 ** I('-0.8')) ** I('0.75')
    CEc = I(psimax) * p.CY ** I('0.75') * fac
    ce = HI(CEc)
    K = I('6.4') * (I(5) / 3) ** I('0.375')
    out.update(lb0=lb0, params=params, nz=NZ, nt=NT, psimax=mp.nstr(psimax, 20), C_E_cert=mp.nstr(ce, 20),
               margins_min={k: mp.nstr(v, 12) for k, v in mins.items()},
               W2_min=mp.nstr(min(v for k, v in mins.items() if k.startswith('W2_')), 12),
               W6_min=mp.nstr(min(v for k, v in mins.items() if k.startswith('W6_')), 12),
               Cprime_from_cert=mp.nstr(HI(K * I(ce) ** I('0.625')), 12),
               const_7751277_ok=bool(HI(K) <= mpf('7.751277')))
    if A.stated:
        CE, Ci, ki, ai = [frac(x) for x in A.stated.split(',')]
        c['C_E_ge_cert'] = bool(LO(CE) >= ce)
        c['Ci_ge'] = bool(LO(Ci) >= HI(I('7.751277') * CE ** I('0.625'))) and out['const_7751277_ok']
        c['ki_ge'] = bool(LO(ki) >= HI(I('0.6') * CE * p.B0 ** I('1.6')))
        c['ai_ge'] = bool(LO(ai) >= HI(I('2.4') * CE * p.B0 ** I('-0.4')))
        lam = I('8.001') * I('0.6') * CE * p.B0 ** I('-1.4') + I('4.1') / p.B0
        c['lam_lt_1'] = bool(HI(lam) < 1)
        c['room_cy_sqrt'] = bool(HI(p.CY * (I(5) / (3 * CE)) ** I('0.5')) <= 1)
        c['room_cy'] = bool(HI(p.CY) <= mpf('0.75'))
        c['ki_ge_1e12'] = bool(LO(ki) >= mpf('1e12'))
        kx = (Ci / I('20.668')) ** 40
        out.update(stated=A.stated, lam_upper=mp.nstr(HI(lam), 6), k_x=mp.nstr(HI(kx), 6),
                   beats_2_5_from=mp.nstr(max(HI(kx), LO(ki)), 6))
    out['all_checks_true'] = all(v is True for k, v in c.items() if k != 'box_count')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['run', 'merge'])
    ap.add_argument('--lb0', type=str, default='7.3617')
    ap.add_argument('--params', type=str, default='')
    ap.add_argument('--nz', type=int, default=320)
    ap.add_argument('--nt', type=int, default=128)
    ap.add_argument('--iz0', type=int, default=0)
    ap.add_argument('--iz1', type=int, default=-1)
    ap.add_argument('--stated', type=str, default='')
    ap.add_argument('files', nargs='*')
    A = ap.parse_args()
    print(json.dumps(run(A) if A.mode == 'run' else merge(A)))


if __name__ == '__main__':
    main()
