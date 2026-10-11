"""Independent re-derivation of Table 1 of the paper and of the numbers quoted in its text.

Written from the statements of the paper only (Proposition 6.1, Lemma 4.4, Section 2.1), not from check_table_iv.py
or check_table_exact.py. Exact rational arithmetic (fractions.Fraction); roots are bracketed by integer roots at 10^-30
relative precision; cos(betabar) >= 1 - betabar^2/2. Every quantity that must be bounded above is bounded above.
Usage: python check_table_exact2.py  (standard library only; prints its results).
"""
from fractions import Fraction as F
from math import isqrt
import math

P = 10 ** 30  # scaling for integer roots


def icbrt(n):
    lo, hi = 0, 1
    while hi ** 3 <= n:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** 3 <= n:
            lo = mid
        else:
            hi = mid
    return lo


def sqrt_bounds(k):  # k a positive Fraction with integer value here
    n = k * P * P
    assert n.denominator == 1
    s = isqrt(n.numerator)
    return F(s, P), F(s + 1, P)


def cbrt_bounds(k):
    n = k * P ** 3
    assert n.denominator == 1
    s = icbrt(n.numerator)
    return F(s, P), F(s + 1, P)


d = F(1, 10 ** 5)
bb = F(15, 10 ** 7)
CONST = {
    9: dict(A=F('10.6067'), Ap=F('10.6068'), S=F('56.2501'), CM=F('318.20'), CG=F('56.2501'), CE=F('754.8')),
    13: dict(A=F('12.7476'), Ap=F('12.7476'), S=F('81.2502'), CM=F('459.7'), CG=F('81.26'), CE=F('1090.3')),
}


def consts(K):
    c = dict(CONST[K])
    cos_lo = 1 - bb * bb / 2
    c['B1'] = (c['A'] / 2 + 2 * bb) / cos_lo            # upper bound for B1
    c['B1lo'] = (c['A'] / 2 + 2 * bb)                   # lower bound (cos <= 1)
    c['L1'] = (1 + c['S'] * d * d) / d + (c['CM'] + c['CE'] + c['CG']) * d + 4 * c['B1']
    return c


def fl(x, n=12):
    return f"{float(x):.{n}g}"


def case(no, K, p, cc, b, ka, kb, tau0, tau1, nu0):
    c = consts(K)
    cc, b, ka, tau0, tau1, nu0 = (F(x) for x in (cc, b, ka, tau0, tau1, nu0))
    kb = None if kb is None else F(kb)
    if p == 2:
        s_lo, s_up = sqrt_bounds(ka)
        W_up = cc * s_up
        beta_up = b / s_lo                      # b k^{-1/2}
    else:
        r_lo, r_up = cbrt_bounds(ka)
        W_up = cc * r_up
        beta_up = b / (r_lo * r_lo)             # b k^{-2/3}
    ok = []
    ok.append(('params', d < tau1 < tau0 < F(1, 2) and 0 < nu0 < F(1, 2) and ka >= 14))
    ok.append(('(i) beta<=bb', beta_up <= bb))
    ok.append(('(i) tau0-1.0001beta>tau1', tau0 - F('1.0001') * beta_up > tau1))
    E_up = F('0.50001') * beta_up * (c['A'] + beta_up / d) * W_up
    ok.append(('(ii) E<1-nu0', E_up < 1 - nu0))
    inv_theta = max(1 / bb, c['B1'] * W_up / (2 * tau1))
    L_up = c['Ap'] * W_up * inv_theta + c['L1'] * W_up + 4 * d
    R_up = W_up / nu0 + c['A'] * cc * ka / (2 * b) + beta_up * (ka / 2) * L_up / (1 - nu0 - E_up)
    lhs = (1 - 2 * tau0) * (ka - 6)
    ok.append(('(iii) lhs>R+', lhs > R_up))
    marg = None
    if p == 2:
        sb_lo, sb_up = sqrt_bounds(kb)
        W1_lo = 2 * tau1 / (c['B1'] * bb)
        ok.append(('(iv) c sqrt(kb)<=W1', cc * sb_up <= W1_lo))
        marg = (cc * sb_up, W1_lo)
    allok = all(v for _, v in ok)
    print(f"case {no} K={K} p=1/{p}: {'OK' if allok else 'FAIL'}  "
          f"lhs/ka={fl(lhs / ka, 11)}  R+/ka<={fl(R_up / ka, 11)}  beta(ka)<={fl(beta_up, 4)}  E<={fl(E_up, 4)}"
          f"  branch={'2nd' if c['B1'] * W_up / (2 * tau1) > 1 / bb else '1st'}")
    if marg:
        print(f"         (iv): c*sqrt(kb) <= {fl(marg[0], 10)}, W1 >= {fl(marg[1], 10)}, rel.margin {fl(marg[1] / marg[0] - 1, 4)}")
    for name, v in ok:
        if not v:
            print('         FAILED:', name)
    return allok, lhs / ka, R_up / ka


def Rplus_over_k_float(K, p, cc, b, k, tau0, tau1, nu0):
    """floating-point R+(k)/k for the monotonicity sanity check"""
    c = {kk: float(v) for kk, v in consts(K).items()}
    dd, B = 1e-5, 1.5e-6
    W = cc * k ** (1 / p)
    beta = b * k ** (1 / p - 1)
    E = 0.50001 * beta * (c['A'] + beta / dd) * W
    L = c['Ap'] * W * max(1 / B, c['B1'] * W / (2 * tau1)) + c['L1'] * W + 4 * dd
    return (W / nu0 + c['A'] * W / (2 * beta) + beta * (k / 2) * L / (1 - nu0 - E)) / k


if __name__ == '__main__':
    for K in (9, 13):
        c = consts(K)
        print(f"K={K}: B1 in [{fl(c['B1lo'], 13)}, {fl(c['B1'], 13)}]  L1 <= {fl(c['L1'], 13)}")
    print()
    CASES = [
        (1, 9, 2, '1e-4', '1.2e-3', '1e8', '2.5e15', '0.0205', '0.02', '0.001'),
        (2, 9, 2, '7e-5', '1.2e-3', '2.5e15', '3.5e17', '0.1675', '0.167', '0.001'),
        (3, 9, 3, '0.06', '1', '3.5e17', None, '0.1675', '0.167', '0.01'),
        (4, 9, 3, '0.0625', '1', '1e21', None, '0.1668', '0.1667', '0.005'),
        (5, 13, 2, '8.5e-5', '1.2e-3', '1e8', '2.4e15', '0.0205', '0.02', '0.001'),
        (6, 13, 2, '6e-5', '1.2e-3', '2.4e15', '3.39e17', '0.1675', '0.167', '0.001'),
        (7, 13, 3, '0.05', '1', '3.39e17', None, '0.1675', '0.167', '0.01'),
        (8, 13, 3, '0.052', '1', '1e21', None, '0.1668', '0.1667', '0.005'),
    ]
    TABLE = {1: ('0.95899994', '0.87266009'), 2: ('0.66499999', '0.61085501'), 3: ('0.66499999', '0.62871651'),
             4: ('0.66639999', '0.66296281'), 5: ('0.95899994', '0.89044495'), 6: ('0.66499999', '0.62854332'),
             7: ('0.66499999', '0.63009391'), 8: ('0.66639999', '0.66284161')}
    allok = True
    for args in CASES:
        ok, l, r = case(*args)
        allok &= ok
        tl, tr = TABLE[args[0]]
        print(f"         table: left>={tl} (true lhs/ka {'>=' if l >= F(tl) else '<'} it), "
              f"R+/ka<={tr} (my upper bound {'<=' if r <= F(tr) else '>'} it)")
    print('ALL CASES OK' if allok else 'SOME CASE FAILED')

    # monotonicity sanity check of R+(k)/k (floating point, log-spaced sample)
    print('\nmonotonicity sample of R+(k)/k (floating point):')
    for (no, K, p, cc, b, ka, kb, t0, t1, n0) in CASES:
        ka_f = float(ka)
        kb_f = float(kb) if kb else ka_f * 1e30
        ks = [ka_f * (kb_f / ka_f) ** (i / 400) for i in range(401)]
        vals = [Rplus_over_k_float(K, p, float(cc), float(b), k, float(t0), float(t1), float(n0)) for k in ks]
        inc = max(vals[i + 1] - vals[i] for i in range(400))
        lhsk = [(1 - 2 * float(t0)) * (k - 6) / k for k in ks]
        print(f"  case {no}: max increase of R+/k over sample = {inc:.3e}; min(lhs/k - R+/k) = "
              f"{min(a - r for a, r in zip(lhsk, vals)):.6f}")

    # liminf constants
    print()
    for K, target in ((9, F('0.062853')), (13, F('0.052297'))):
        c = consts(K)
        cube = F(4, 27) / (c['A'] * c['Ap'] * c['B1'])
        print(f"K={K}: cbar_inf^3 >= {fl(cube, 12)}, cbar_inf >= {fl(float(cube) ** (1 / 3), 10)}; "
              f"claim cbar_inf > {target}: {cube > target ** 3}")

    # numbers in the introduction
    print()
    print('k with 7e-5 sqrt(k) = 0.1 k^(1/4):', (0.1 / 7e-5) ** 4, ' (paper: 4.17e12)')
    print('k with 0.06 k^(1/3) = 0.1 k^(1/4):', (F(5, 3)) ** 12, '=', float(F(5, 3) ** 12), ' (paper: 460)')
    s_lo, s_up = sqrt_bounds(F(462 * 10 ** 10))
    print('1e-4 sqrt(4.62e12) in [', fl(s_lo / 10 ** 4), ',', fl(s_up / 10 ** 4), '] (paper: > 214.9)')
    print('0.1 (4.62e12)^(1/4) =', 0.1 * 4.62e12 ** 0.25, '-> ceil', math.ceil(0.1 * 4.62e12 ** 0.25), ' (paper/[Q]: 147)')
    print('1e-4 sqrt(9e8) =', 1e-4 * math.sqrt(9e8), ' (paper: new from 9e8, W>=4)')
    print('analytic: 8.5e-5 sqrt(k) > 3 from k >', (3 / 8.5e-5) ** 2)
    # Lemma 2.1 (C5)
    th = bb
    print('2^-1/4 < 0.8409:', F(8409, 10000) ** 4 > F(1, 2))
    w0_up = F('0.50001') * th * th * (1 + F('1.0001')) + d + F('1.0001') * F(8409, 10000) * th + F(10) ** -12
    print('Lemma 2.1 (C5): w0 <=', fl(w0_up), ' < 1.13e-5:', w0_up < F('1.13e-5'))
