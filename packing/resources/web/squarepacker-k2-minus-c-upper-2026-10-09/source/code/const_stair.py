# const_stair.py -- interval-arithmetic certification of the constants of the band-end corollary (Section 7.2 of the
# paper) and of the proof of the main theorem (Section 7.3).
# Phi(x), x = b^{-1/3}, is the sum T1..T7 of the band-end corollary; each term is a product of non-negative,
# non-decreasing functions of x on (0, x0], so sup_{b >= 10^4} Phi = Phi(x0) with x0 = 10^{-4/3}.  As a check that
# does not use this monotonicity, Phi is also bounded on [0, x0] by a subdivision into 4000 intervals.
# Usage: python code/const_stair.py [out.json]        (needs mpmath; about 10 seconds)
import json, sys
from mpmath import iv
iv.dps = 40

KAPPA = iv.mpf(3) / 4
DBAR = iv.mpf('3.000001')           # delta = m - g0 <= Delta + 1 <= 3.000001
A = 2 * DBAR                        # A = 6.000002
RHO = iv.mpf('2.000001')            # Delta = w mu <= 2.000001, b mu <= 2.000001


def Phi(x):
    x = iv.mpf(x)
    p = KAPPA - iv.mpf('5e-8') * x ** 2
    theta = (x + iv.sqrt(x ** 2 + A * KAPPA)) / (2 * p) + x ** 2 / 16
    tb = x * theta                                  # bound for the tilt parameter t
    ta = 2 * tb / (1 - tb ** 2)                     # bound for tan(alpha)
    se = (1 + tb ** 2) / (1 - tb ** 2)              # bound for sec(alpha)
    T1 = 2 * theta
    T2 = 2 * x * theta ** 2
    T3 = RHO * (x ** 2 * se + (KAPPA + iv.mpf('5.000001') * x ** 2) * ta)
    T4 = (KAPPA + iv.mpf('4.000001') * x ** 2) * (1 + ta / 2)
    om = x ** 2 * se + (KAPPA + iv.mpf('4.000001') * x ** 2) * ta
    T5 = (1 + RHO * x * om) * om
    T6 = (KAPPA + 2 * x ** 2) * (1 + ta / 2)
    T7 = iv.mpf('4.000001') * ta * x ** 2 * (1 + RHO * x ** 3 * iv.mpf('4.000001') * ta)
    tot = T1 + T2 + T3 + T4 + T5 + T6 + T7
    return dict(tbar=tb, tan_bar=ta, T1=T1, T2=T2, T3=T3, T4=T4, T5=T5, T6=T6, T7=T7, Phi=tot)


def hi(v): return float(v.b)


def xb(b0):
    x = iv.mpf(1) / iv.mpf(b0) ** (iv.mpf(1) / 3)      # an interval enclosing b0^{-1/3}
    return iv.mpf([x.a, x.b])


if __name__ == '__main__':
    out, ok = {}, {}
    for b0 in (10 ** 4, 10 ** 5, 10 ** 6, 10 ** 8):
        out['b0=%d' % b0] = {k: hi(v) for k, v in Phi(xb(b0)).items()}
    out['limit x->0'] = {k: hi(v) for k, v in Phi(iv.mpf(0)).items()}
    x0 = xb(10 ** 4)
    r = Phi(x0)
    ok['Phi(x0) <= 5.0163'] = hi(r['Phi']) <= 5.0163
    ok['tbar(x0) <= 0.0672'] = hi(r['tbar']) <= 0.0672
    ok['tan_bar(x0) <= 0.1349'] = hi(r['tan_bar']) <= 0.1349
    # subdivision of [0, x0] into 4000 intervals (no monotonicity used)
    n, sup = 4000, 0.0
    for i in range(n):
        lo = x0.a * i / n; up = x0.b * (i + 1) / n
        sup = max(sup, hi(Phi(iv.mpf([lo, up]))['Phi']))
    out['sup of Phi on [0, x0] by subdivision'] = sup
    ok['subdivision sup <= 5.03'] = sup <= 5.03
    CE = iv.mpf('5.03')
    Cp = iv.mpf(20) / 3 * (iv.mpf(3) / 2) ** (iv.mpf(2) / 5) * CE ** (iv.mpf(3) / 5)
    Cs = iv.mpf(8) / 3 * CE * iv.mpf(10) ** (iv.mpf(-4) / 3)
    k0 = (2 * CE / 3) * iv.mpf(10) ** (iv.mpf(20) / 3)
    lam = iv.mpf('8.001') * (2 * CE / 3) * iv.mpf(10) ** (iv.mpf(-16) / 3) + iv.mpf('4.1e-4')
    out['theorem'] = dict(CE=5.03, coefficient=[float(Cp.a), float(Cp.b)], constant=[float(Cs.a), float(Cs.b)],
                          k0_needed=[float(k0.a), float(k0.b)], lambda_hi=hi(lam),
                          limit_coefficient=hi(iv.mpf(20) / 3 * (iv.mpf(3) / 2) ** (iv.mpf(2) / 5)
                                               * Phi(iv.mpf(0))['Phi'] ** (iv.mpf(3) / 5)))
    ok['coefficient <= 20.6675'] = hi(Cp) <= 20.6675
    ok['constant <= 0.6226'] = hi(Cs) <= 0.6226
    ok['(2 C_E/3) 10^(20/3) <= 1.6e7'] = hi(k0) <= 1.6e7
    ok['lambda < 0.001'] = hi(lam) < 0.001
    out['checks'] = ok
    print(json.dumps(out, indent=1))
    print('ALL CHECKS:', all(ok.values()))
    if len(sys.argv) > 1:
        json.dump(out, open(sys.argv[1], 'w'), indent=1)
