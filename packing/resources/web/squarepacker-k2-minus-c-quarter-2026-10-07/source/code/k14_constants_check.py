#!/usr/bin/env python3
"""k14_constants_check.py

Recomputes every number displayed in Sections 10-12 of the manuscript, the constants appearing in Theorems A, A13
and Corollary A and in the comparison with [R] of Section 1, and the numerical constants displayed in Sections 2-9
(one block per section), and checks each displayed value with its rounding direction.

Usage:   python k14_constants_check.py          (Python 3 with mpmath; no other packages)

Method (the conventions are those of Section 12.1 of the manuscript):
  * Every quantity is computed with mpmath at 50 significant digits (mp) and enclosed in mpmath interval
    arithmetic with outward rounding at 50 digits (iv).  Interval endpoints are converted exactly to rational
    numbers (fractions.Fraction) and compared exactly with the displayed decimal strings.
  * 'x <= v'  (upper bound, rounded up at the last displayed digit): hi(x) <= v and lo(x) > v - u,
    where u is one unit of the last displayed digit.
  * 'x >= v'  (lower bound, rounded down) and 'x = v...' (truncated decimal expansion): lo(x) >= v and
    hi(x) < v + u.
  * 'x < v'   (a chosen bound, such as A < 10.6067, not obtained by rounding at the last digit): hi(x) < v.
  * 'x < v' rounded up (Sections 2-9): hi(x) < v and lo(x) > v - u;  'x > v' rounded down: lo(x) > v and
    hi(x) < v + u.
  * exact values (such as eps*y0 = 244226.4 or 10^4*146^4 + 1): rational arithmetic; displayed values that are
    rational functions of displayed decimals (such as S_9 in Section 7) are compared in exact rational arithmetic.
  * The constraints (C0)-(C4), (C7), (Q1), (Q2) of Section 3 are checked in exact rational arithmetic (after
    raising both sides to a suitable power); (C5), (C6) and all remaining inequalities in interval arithmetic.
  * The decisive inequalities, conditions (i)-(iii) of Proposition 11.2 (Section 11.2), are checked in interval
    arithmetic.
  * A few closed forms of Section 10 are cross-checked by numerical quadrature; these are not used in any proof.
One line is printed per check.  The last line is 'ALL OK' if every check holds, and 'SOME FAILED' otherwise.
"""
import sys
import time
from fractions import Fraction
from mpmath import mp, iv, nstr

mp.dps = 50
iv.dps = 50
T0 = time.time()
TLIM = 900.0          # internal time limit in seconds
RES = []


def finish():
    nfail = RES.count(False)
    print('-' * 78)
    print('checks: %d, failed: %d, time %.1f s' % (len(RES), nfail, time.time() - T0))
    print('ALL OK' if nfail == 0 else 'SOME FAILED')
    sys.exit(0 if nfail == 0 else 1)


def check(name, ok, info=''):
    ok = bool(ok)
    RES.append(ok)
    print(('OK   ' if ok else 'FAIL ') + name + (('   [' + info + ']') if info else ''), flush=True)
    if time.time() - T0 > TLIM:
        print('FAIL internal time limit exceeded', flush=True)
        RES.append(False)
        finish()


def head(t):
    print('=' * 78)
    print(t, flush=True)


# ------------------------------------------------------------------------------------------------------------
# exact rational helpers
# ------------------------------------------------------------------------------------------------------------
def frac_raw(t):
    """exact rational value of a raw mpf tuple (sign, man, exp, bc)"""
    sign, man, exp, bc = t
    if man == 0:
        if exp != 0:
            raise ValueError('special value (inf/nan) in an interval endpoint')
        return Fraction(0)
    v = Fraction(int(man)) * (Fraction(2) ** exp if exp >= 0 else Fraction(1, 2 ** (-exp)))
    return -v if sign else v


def frac_mp(x):
    return frac_raw(x._mpf_)


def ends(X):
    """exact rational endpoints of an iv interval"""
    a, b = X._mpi_
    return frac_raw(a), frac_raw(b)


def lo(X):
    return ends(X)[0]


def hi(X):
    return ends(X)[1]


def mid(X):
    a, b = ends(X)
    m = (a + b) / 2
    return nstr(mp.mpf(m.numerator) / m.denominator, 16)


def unit_of(s):
    """one unit of the last displayed digit of the decimal string s"""
    s = s.strip().lower()
    if 'e' in s:
        m, ex = s.split('e')
        ex = int(ex)
    else:
        m, ex = s, 0
    dec = len(m.split('.')[1]) if '.' in m else 0
    return Fraction(1, 10 ** dec) * (Fraction(10) ** ex)


def plus_unit(s):
    """the decimal string one unit (of the last displayed digit) above s; s without exponent"""
    dec = len(s.split('.')[1]) if '.' in s else 0
    v = Fraction(s) + unit_of(s)
    n = v * 10 ** dec
    assert n.denominator == 1
    n = int(n)
    return str(n) if dec == 0 else '%d.%0*d' % (n // 10 ** dec, dec, n % 10 ** dec)


F = Fraction


def disp(name, kind, X, shown):
    """check a displayed value: kind 'le' (upper bound, rounded up), 'ge' (lower bound, rounded down),
    'tr' (truncated expansion, printed as v...), 'lt' (chosen strict upper bound), 'ltr' (strict upper bound,
    rounded up), 'gtr' (strict lower bound, rounded down)"""
    a, b = ends(X)
    v = F(shown)
    u = unit_of(shown)
    if kind == 'le':
        ok, sym = (b <= v and a > v - u), '<='
    elif kind == 'ge':
        ok, sym = (a >= v and b < v + u), '>='
    elif kind == 'tr':
        ok, sym = (a >= v and b < v + u), '= (truncated)'
    elif kind == 'lt':
        ok, sym = (b < v), '<'
    elif kind == 'ltr':
        ok, sym = (b < v and a > v - u), '< (rounded up)'
    elif kind == 'gtr':
        ok, sym = (a > v and b < v + u), '> (rounded down)'
    else:
        raise ValueError(kind)
    check('%s %s %s' % (name, sym, shown), ok, 'value ' + mid(X))


def qstr(q):
    return nstr(mp.mpf(q.numerator) / q.denominator, 16)


def dispq(name, kind, q, shown):
    """as disp, for an exact rational value q (a fractions.Fraction)"""
    v = F(shown)
    u = unit_of(shown)
    if kind == 'le':
        ok, sym = (q <= v and q > v - u), '<='
    elif kind == 'ge':
        ok, sym = (q >= v and q < v + u), '>='
    elif kind == 'tr':
        ok, sym = (q >= v and q < v + u), '= (truncated)'
    elif kind == 'lt':
        ok, sym = (q < v), '<'
    elif kind == 'ltr':
        ok, sym = (q < v and q > v - u), '< (rounded up)'
    elif kind == 'gtr':
        ok, sym = (q > v and q < v + u), '> (rounded down)'
    else:
        raise ValueError(kind)
    check('%s %s %s' % (name, sym, shown), ok, 'value %s, exact' % qstr(q))


def ivq(q):
    """an iv enclosure of the rational number q"""
    return iv.mpf(q.numerator) / iv.mpf(q.denominator)


# ------------------------------------------------------------------------------------------------------------
# the formulas of Section 10.2 (the same code runs in mp and in iv)
# ------------------------------------------------------------------------------------------------------------
def A_exact(C, K):
    """[R, Lemma 4.13]: A = 4 sqrt(K/Q*)/(2 - 3e-6), Q* = 0.32; K = 9 (K = 13 in Section 11.5)"""
    return 4 * C.sqrt(C.mpf(K) / C.mpf('0.32')) / (2 - C.mpf('3e-6'))


def Ap_exact(C, K):
    """Corollary cor:P6scale (Section 8): A' = A/cos(1.5e-6) + 1e-8"""
    return A_exact(C, K) / C.cos(C.mpf('1.5e-6')) + C.mpf('1e-8')


def CL_exact(C, s):
    """Corollary cor:Lambda0 (Section 7): C_Lambda = 1 + s delta^2, s = 1185.6 (1712.6 in Section 11.5)"""
    return 1 + C.mpf(s) * C.mpf('1e-5') ** 2


def pw(C, x, p, q):
    """x^(p/q) for x > 0"""
    return C.exp(C.mpf(p) / q * C.log(x))


def derive(C, par, A, Ap, CL, bw='2.0002', wallfac='1'):
    """the k-independent quantities of Section 10.2 for pi = par = (c0, c1, y0, eps, omega0)"""
    M = C.mpf
    c0, c1, y0, e, w = [M(p) for p in par]
    dl = M('1e-5')
    bwv = M(bw)
    d = {}
    d['al0'] = c0 / C.sqrt(y0)                                   # alpha(y0)
    d['be0'] = c1 * pw(C, y0, -3, 4)                              # hat beta(y0)
    d['bstar'] = c1 * pw(C, (1 - e) * y0, -3, 4)                  # b* = hat beta((1-eps) y0)
    d['C3l'] = c1 * pw(C, 1 - e, -3, 4)                           # left-hand side of (C3)
    d['C3r'] = c0 * pw(C, y0, 1, 4)                               # right-hand side of (C3)
    d['w0'] = M('0.50001') * c0 ** 2 * (1 + M('1.0001') / y0) + dl + M('1.0001') * d['bstar'] + M('1e-12')
    d['h0'] = 1 - 2 * d['w0']
    t = pw(C, 1 - e, 3, 4)
    d['invF'] = 4 * t * (1 - t) / (3 * e * (1 + bwv / (e * y0)))
    d['invFcap'] = 1 / (1 + bwv / (e * y0))
    d['Gp'] = M('1.00002') * (2 * c1 * A / C.sqrt(y0) + M(4) / 5 * c1 ** 2 / dl * pw(C, y0, -5, 4))   # Gamma
    d['B1'] = 1 / (w * pw(C, y0, 3, 4))
    d['B2'] = A / (2 * c1)
    d['B3'] = 2 * c1 / (c0 * d['invF']) * (Ap + d['al0'] * CL / dl)
    d['B'] = d['B1'] + d['B2'] + d['B3'] + d['Gp']
    d['Cw'] = 4 * c1 / (c0 * d['invF']) * M(wallfac)             # C_wall (times a factor in Section 12.6)
    d['KO'] = M('1.000001') * c0 ** 2 * d['Cw']                    # K_W
    d['Pinf'] = 8 * pw(C, M(2), -1, 4) * d['h0'] * (1 - w) * pw(C, 1 - e, 1, 4) / d['B']   # Psi_infinity(pi)
    d['par'] = (c0, c1, y0, e, w)
    return d


def at_k(C, d, k, cs):
    """k-dependent quantities: the bounds for ell(H) and Omega_W in Theorem 10.3, bar Psi(k), and the quantities in
    conditions (i)-(iii) of Proposition prop:monotone (Section 11.2)"""
    M = C.mpf
    c0, c1, y0, e, w = d['par']
    kk = M(k)
    y1 = kk / 2 - 3
    r = {}
    r['C7r'] = (1 - e) * y1
    r['LH'] = 8 * d['h0'] * (pw(C, (1 - e) * y1, 1, 4) - pw(C, y0 + 1, 1, 4))     # lower bound for ell(H), Theorem 10.3
    r['Omb'] = M('1.000001') * c0 ** 2 * (C.log(y1 / y0) + 2 / y0)                  # upper bound for Omega_W, Theorem 10.3
    r['wall'] = d['Cw'] * r['Omb']
    r['num'] = (1 - w) * r['LH'] - r['wall']
    r['Psi'] = r['num'] / d['B']
    r['k4'] = pw(C, kk, 1, 4)
    r['tgt'] = M(cs) * r['k4']
    r['D1'] = d['h0'] * (1 - w) * pw(C, 1 - e, 1, 4) / d['B'] - M(cs) / (4 * pw(C, M(2), 3, 4))
    r['iiiL'] = pw(C, y1, 1, 4) * r['D1']
    r['iiiR'] = d['KO'] / (2 * d['B'])
    r['mono'] = pw(C, y1, 1, 4) * d['h0'] * (1 - w) * pw(C, 1 - e, 1, 4) - d['KO'] / 2
    r['ratio'] = r['Psi'] / r['k4']
    r['Bcrit'] = r['num'] / r['tgt']
    return r


UPPER = {'9': ('10.6067', '10.6068', '1.0000002'),      # bar A, bar A', bar C_Lambda (Section 11.1)
         '13': ('12.7476', '12.7476', '1.0000002')}     # bar A_13, bar A'_13, bar C_Lambda^(13) (Section 11.5)


def both(par, K, k=None, cs='0.1', **kw):
    """mp and iv versions of derive/at_k with the upper bounds UPPER[K]; keyword overrides A, Ap, CL, bw, wallfac"""
    out = []
    for C in (mp, iv):
        A, Ap, CL = [C.mpf(kw.get(n, UPPER[K][i])) for i, n in enumerate(('A', 'Ap', 'CL'))]
        d = derive(C, par, A, Ap, CL, bw=kw.get('bw', '2.0002'), wallfac=kw.get('wallfac', '1'))
        r = at_k(C, d, k, cs) if k is not None else None
        out.append((d, r))
    (dm, rm), (di, ri) = out
    return dm, rm, di, ri


def constraints(tag, par, k, K):
    """(C0)-(C7), (Q1), (Q2) of Section 3 for pi = par at k (exact rational arithmetic where possible), and the
    facts of Lemma 10.2 (0 < invF < 1/(1 + b_W/(eps y0))) and B > 0"""
    c0, c1, y0, e, w = [F(p) for p in par]
    y1 = F(k) / 2 - 3
    b = F('1.5e-6')
    check(tag + ' (C0) c0,c1 > 0, y0 positive integer, 0 < eps < 1, omega0 > 0',
          c0 > 0 and c1 > 0 and y0.denominator == 1 and y0 > 0 and 0 < e < 1 and w > 0)
    check(tag + ' (C1) alpha(y0) <= 1.5e-6  [exact: c0^2 <= (1.5e-6)^2 y0]', c0 ** 2 <= b ** 2 * y0)
    check(tag + ' (C2) hat beta(y0) <= 1.5e-6  [exact: c1^4 <= (1.5e-6)^4 y0^3]', c1 ** 4 <= b ** 4 * y0 ** 3)
    check(tag + ' (C3) c1 (1-eps)^(-3/4) < c0 y0^(1/4)  [exact: c1^4 < c0^4 y0 (1-eps)^3]',
          c1 ** 4 < c0 ** 4 * y0 * (1 - e) ** 3)
    check(tag + ' (C4) omega0 < 1/2  [exact]', w < F(1, 2))
    _, _, di, _ = both(par, K)
    check(tag + ' (C5) w0 < 1/2  [interval]', hi(di['w0']) < F(1, 2), 'w0 = ' + mid(di['w0']))
    check(tag + ' (C6) delta <= cos(2 alpha(y0))/2  [interval]', lo(iv.cos(2 * di['al0']) / 2) >= F('1e-5'))
    check(tag + ' (C7) y0 + 1 <= (1-eps)(k/2-3) at k = %s  [exact]' % k, y0 + 1 <= (1 - e) * y1)
    check(tag + ' (Q1) alpha(y0) <= 1e-3  [exact]', c0 ** 2 <= F('1e-6') * y0)
    check(tag + ' (Q2) b* <= 1e-4  [exact: c1^4 <= 1e-16 ((1-eps) y0)^3]',
          c1 ** 4 <= F('1e-16') * ((1 - e) * y0) ** 3)
    check(tag + ' Lemma 10.2: 0 < invF < 1/(1+b_W/(eps y0)); B > 0  [interval]',
          lo(di['invF']) > 0 and hi(di['invF']) < lo(di['invFcap']) and lo(di['B']) > 0)


def monotone_conditions(tag, ri):
    """conditions (i)-(iii) of Proposition 11.2, in interval arithmetic"""
    check(tag + ' (i)   bar Psi(k0) >= c* k0^(1/4)  [interval]', lo(ri['Psi']) >= hi(ri['tgt']),
          'bar Psi = %s, c* k0^(1/4) = %s' % (mid(ri['Psi']), mid(ri['tgt'])))
    check(tag + ' (ii)  D1 > 0  [interval]', lo(ri['D1']) > 0, 'D1 = ' + mid(ri['D1']))
    check(tag + ' (iii) y1(k0)^(1/4) D1 >= K_W/(2 bar B)  [interval]', lo(ri['iiiL']) >= hi(ri['iiiR']),
          '%s >= %s' % (mid(ri['iiiL']), mid(ri['iiiR'])))


# ============================================================================================================
# Section 1, comparison with [R]: the condition log k > 15.22 c + 13.07 follows from the quoted bound
# W >= 1.99954 (log k - 13.06675)/30.418 of [R] (W > c as soon as log k > (30.418/1.99954) c + 13.06675)
# ============================================================================================================
head('Section 1: comparison with [R]')
dispq('Section 1, comparison with [R]: 30.418/1.99954 (coefficient of c)', 'le', F('30.418') / F('1.99954'), '15.22')
check('Section 1, comparison with [R]: 13.06675 <= 13.07, so log k > 15.22 c + 13.07 gives '
      '1.99954 (log k - 13.06675)/30.418 > c for c >= 0  [exact]', F('13.06675') <= F('13.07'))

# ============================================================================================================
# Section 2: the constants of [R] quoted in Section 2 and used in this paper
# ============================================================================================================
head('Section 2: constants quoted from [R]')
DL = F('1e-5')           # delta (Definition 3.1)
BB = F('1.5e-6')         # bar beta (Definition 3.1)
# Section 2, before [R, Lemma 4.8]: R_0(d) = sqrt((d + sqrt 2)^2 + 1/4) < 1.5001 for 0 < d <= 1e-4 (R_0 increases in d)
R0 = iv.sqrt((iv.mpf('1e-4') + iv.sqrt(iv.mpf(2))) ** 2 + iv.mpf(1) / 4)
check('Section 2, before [R, Lemma 4.8]: R_0(d) <= R_0(1e-4) = sqrt((1e-4 + sqrt 2)^2 + 1/4) < 1.5001  [interval]',
      hi(R0) < F('1.5001'), 'R_0(1e-4) = ' + mid(R0))
# Section 2, [R, Lemma 4.8(a)]: q_0 = 10, m' <= q_0 - 1 = 9, waste >= theta(2-theta)/(4 q_0) (used with 4 q_0 = 40)
check("Section 2, [R, Lemma 4.8(a)]: q_0 = 10 gives m' <= q_0 - 1 = 9 and 4 q_0 = 40  [exact]",
      10 - 1 == 9 and 4 * 10 == 40)
# Section 2, [R, Lemma 4.13] and Remark 2.2: A = 4 sqrt(K_w^*/Q_*)/(2 - 3e-6) with K_w^* = 9, Q_* = 0.32, and
# A_13 = 4 sqrt(K_w/Q_*)/(2 - 3e-6) with K_w = 13 (digits truncated, bounds rounded up)
disp('Section 2, Remark 2.2: A = 4 sqrt(9/0.32)/(2-3e-6)', 'tr', A_exact(iv, '9'), '10.60661762')
disp('Section 2, [R, Lemma 4.13] and Remark 2.2: A', 'ltr', A_exact(iv, '9'), '10.6067')
disp('Section 2, Remark 2.2: A_13 = 4 sqrt(13/0.32)/(2-3e-6)', 'tr', A_exact(iv, '13'), '12.74756790')
disp('Section 2, Remark 2.2: A_13', 'ltr', A_exact(iv, '13'), '12.7476')
# Section 2, the inequality sec x - 1 <= 0.50001 x^2 (0 <= x <= 1e-3) from the proof of [R, Lemma 4.15], with the
# proof given in Section 2: sec x - 1 <= x^2/(2 - x^2) <= x^2/(2 - 1e-6) < 0.5000003 x^2 for 0 < x <= 1e-3
check('Section 2, proof of sec x - 1 <= 0.50001 x^2: x^2 <= 1e-6 < 2, 1/(2 - 1e-6) < 0.5000003 <= 0.50001  [exact]',
      F('1e-3') ** 2 == F('1e-6') < 2 and 1 / (2 - F('1e-6')) < F('0.5000003') <= F('0.50001'),
      '1/(2 - 1e-6) = ' + qstr(1 / (2 - F('1e-6'))))
SECQ = (1 / iv.cos(iv.mpf('1e-3')) - 1) / iv.mpf('1e-3') ** 2
check('Section 2, cross-check: (sec x - 1)/x^2 < 0.5000003 at x = 1e-3, where this increasing function is largest '
      '[interval]', hi(SECQ) < F('0.5000003'), '(sec x - 1)/x^2 = ' + mid(SECQ))

# ============================================================================================================
# Section 3: parameters, constraints (C0)-(C7), (Q1), (Q2), the vectors pi*, pi*_13, and Definition 3.6
# ============================================================================================================
head('Section 3: parameters, constraints and the parameter vectors')
PI3 = {'A': ('0.3078', '0.2754', '42108000000', '5.8e-6', '1.7e-5'),     # pi*    (Section 3, display before Def. 3.2)
       'A13': ('0.3674', '0.3012', '60000000000', '5e-6', '1.4e-5')}     # pi*_13 (Section 3, display before Def. 3.2)
# Section 3, Definitions 3.1 and 3.5: V_s = [(1-eps)s - 1.0001, s + 1.0001], |V_s| = eps s + b_W, b_W = 2.0002
check('Section 3, Definition 3.5: |V_s| = (s + 1.0001) - ((1-eps)s - 1.0001) = eps s + b_W, b_W = 2 * 1.0001 = 2.0002'
      '  [exact]', 2 * F('1.0001') == F('2.0002'))
# Section 3, Lemma 3.3(a): (1/2) cos(2 alpha_max) >= (1/2)(1 - (1/2)(3e-6)^2) > 0.49 > 1e-5 >= delta; 1.5e-6 <= 1e-3
check('Section 3, Lemma 3.3(a): (1/2)(1 - (1/2)(3e-6)^2) > 0.49 > 1e-5, and 1.5e-6 <= 1e-3 ((Q1) from (C1))  [exact]',
      F(1, 2) * (1 - F(1, 2) * F('3e-6') ** 2) > F('0.49') > DL and 2 * BB == F('3e-6') and BB <= F('1e-3'))
check('Section 3, Lemma 3.3(a): (1/2) cos(3e-6) > 0.49  [interval]', lo(iv.cos(iv.mpf('3e-6')) / 2) > F('0.49'))
# Section 3, Lemma 3.3(b): eps <= 0.9963 gives (1-eps)^(3/4) >= 0.0037^(3/4) > 0.015, as 0.0037^3 = 5.0653e-8 >
# 5.0625e-8 = 0.015^4; hence b* < 1.5e-6/0.015 = 1e-4
check('Section 3, Lemma 3.3(b): 1 - 0.9963 = 0.0037, 0.0037^3 = 5.0653e-8 > 5.0625e-8 = 0.015^4, '
      '1.5e-6/0.015 = 1e-4  [exact]',
      1 - F('0.9963') == F('0.0037') and F('0.0037') ** 3 == F('5.0653e-8') > F('5.0625e-8') == F('0.015') ** 4
      and BB / F('0.015') == F('1e-4'))
# Section 3, Lemma 3.4(a) and its proof: pi* at k >= 4.62e12
c0_, c1_, y0_, e_, w_ = [F(p) for p in PI3['A']]
check('Section 3, Lemma 3.4(a): c0/bar beta = 205200 exactly, 205200^2 = 42107040000 <= y0 = 42108000000  [exact]',
      c0_ / BB == 205200 and 205200 ** 2 == 42107040000 <= y0_)
check('Section 3, Lemma 3.4(a), (C1): c0^2 = 0.09474084 <= 0.094743 = 2.25e-12 * 42108000000 = bar beta^2 y0  [exact]',
      c0_ ** 2 == F('0.09474084') <= F('0.094743') == F('2.25e-12') * y0_ and BB ** 2 == F('2.25e-12'))
check('Section 3, Lemma 3.4(a), (C2), (Q2): y0 >= 1e10, (1-eps) y0 >= 1e10, 10^7.5 > 3e7 (10^15 > 9e14), '
      '0.2754/(3e7) < 1e-8  [exact]',
      y0_ >= 10 ** 10 and (1 - e_) * y0_ >= 10 ** 10 and 10 ** 15 > 9 * 10 ** 14 and c1_ / (3 * 10 ** 7) < F('1e-8'))
check('Section 3, Lemma 3.4(a): b* < 1e-8  [exact: c1^4 < 1e-32 ((1-eps) y0)^3]',
      c1_ ** 4 < F('1e-32') * ((1 - e_) * y0_) ** 3)
check('Section 3, Lemma 3.4(a), (C3): 0.2754/(1 - 5.8e-6) < 0.2755, and 0.3078 * 10^2.5 > 97 '
      '[exact: 0.3078^2 * 10^5 > 97^2]', c1_ / (1 - e_) < F('0.2755') and c0_ ** 2 * 10 ** 5 > 97 ** 2)
check('Section 3, Lemma 3.4(a), (C5): 0.50001 c0^2 = 0.0473713674084 and 1.0001/y0 < 1e-10  [exact]',
      F('0.50001') * c0_ ** 2 == F('0.0473713674084') and F('1.0001') / y0_ < F('1e-10'))
check('Section 3, Lemma 3.4(a), (C5): w0 > 0.0473713674 + 1e-5 > 0.0473813  [exact]',
      F('0.0473713674') + DL > F('0.0473813'))
check('Section 3, Lemma 3.4(a), (C5): 0.0473713674085 (1 + 1e-10) + 1e-5 + 1.0001e-8 + 1e-12 < 0.0473814  [exact]',
      F('0.0473713674085') * (1 + F('1e-10')) + DL + F('1.0001e-8') + F('1e-12') < F('0.0473814'))
_, _, D3, _ = both(PI3['A'], '9')
check('Section 3, Lemma 3.4(a): 0.0473813 < w0 < 0.0473814  [interval]',
      lo(D3['w0']) > F('0.0473813') and hi(D3['w0']) < F('0.0473814'), 'w0 = ' + mid(D3['w0']))
check('Section 3, Lemma 3.4(a): 0.9052372 < h0 < 0.9052374  [interval; 1 - 2*0.0473814 = 0.9052372 and '
      '1 - 2*0.0473813 = 0.9052374 exactly]',
      lo(D3['h0']) > F('0.9052372') and hi(D3['h0']) < F('0.9052374') and 1 - 2 * F('0.0473814') == F('0.9052372')
      and 1 - 2 * F('0.0473813') == F('0.9052374'), 'h0 = ' + mid(D3['h0']))
check('Section 3, Lemma 3.4(a), (C7): eps <= 1e-5, 4.62e12/2 = 2.31e12, (1 - 1e-5)(2.31e12 - 3) > 2e12 > y0 + 1'
      '  [exact]', e_ <= DL and F('4.62e12') / 2 == F('2.31e12') and (1 - DL) * (F('2.31e12') - 3) > F('2e12') > y0_ + 1)
constraints('[Section 3, Lemma 3.4(a): pi*, k = 4.62e12]', PI3['A'], '4620000000000', '9')
# Section 3, Lemma 3.4(b) and its proof: pi*_13 at k >= 2.17e13
c0_, c1_, y0_, e_, w_ = [F(p) for p in PI3['A13']]
check('Section 3, Lemma 3.4(b), (C1): c0^2 = 0.3674^2 = 0.13498276 <= 0.135 = 2.25e-12 * 6e10  [exact]',
      c0_ ** 2 == F('0.13498276') <= F('0.135') == F('2.25e-12') * y0_)
check('Section 3, Lemma 3.4(b), (C2), (Q2): y0 >= 1e10, (1-eps) y0 >= 1e10, 0.3012/(3e7) < 1.1e-8  [exact]',
      y0_ >= 10 ** 10 and (1 - e_) * y0_ >= 10 ** 10 and c1_ / (3 * 10 ** 7) < F('1.1e-8'))
check('Section 3, Lemma 3.4(b), (C3): c1/(1-eps) < 0.302 < 97 < c0 y0^(1/4)  [exact: 97^4 < c0^4 y0]',
      c1_ / (1 - e_) < F('0.302') < 97 and 97 ** 4 < c0_ ** 4 * y0_)
check('Section 3, Lemma 3.4(b), (C5): 1.0001/y0 < 1e-10 and '
      '0.50001 * 0.13498276 (1 + 1e-10) + 1e-5 + 1.0001 * 1.1e-8 + 1e-12 < 0.0676  [exact]',
      F('1.0001') / y0_ < F('1e-10') and
      F('0.50001') * F('0.13498276') * (1 + F('1e-10')) + DL + F('1.0001') * F('1.1e-8') + F('1e-12') < F('0.0676'))
_, _, D3, _ = both(PI3['A13'], '13')
check('Section 3, Lemma 3.4(b): w0 < 0.0676  [interval]', hi(D3['w0']) < F('0.0676'), 'w0 = ' + mid(D3['w0']))
check('Section 3, Lemma 3.4(b), (C7): eps <= 1e-5, 2.17e13/2 = 1.085e13, (1 - 1e-5)(1.085e13 - 3) > 1e13 > y0 + 1'
      '  [exact]',
      e_ <= DL and F('2.17e13') / 2 == F('1.085e13') and (1 - DL) * (F('1.085e13') - 3) > F('1e13') > y0_ + 1)
constraints('[Section 3, Lemma 3.4(b): pi*_13, k = 2.17e13]', PI3['A13'], '21700000000000', '13')
# Section 3.2, the roles of the conditions (end of Section 3.2): (Q1) gives sec(alpha(s)) - 1 <= 0.50001 alpha(s)^2
# by the inequality of Section 2; (Q2) gives cos a + sin a <= 1 + a < 1.0001 for a < b* <= 1e-4; (C1) gives
# tan x <= 1.000001 x for 0 <= x <= alpha_max
check('Section 3.2, roles of the conditions: (Q1) gives sec(alpha) - 1 <= 0.50001 alpha^2 for alpha <= 1e-3, as '
      '(sec x - 1)/x^2 <= 0.50001 at x = 1e-3  [interval; (sec x - 1)/x^2 increases]', hi(SECQ) <= F('0.50001'),
      '(sec x - 1)/x^2 = ' + mid(SECQ))
check('Section 3.2, roles of the conditions: (Q2) gives cos a + sin a <= 1 + a < 1 + 1e-4 = 1.0001  [exact]',
      1 + F('1e-4') == F('1.0001'))
xb_ = iv.mpf('1.5e-6')
check('Section 3.2, roles of the conditions: (C1) gives tan x <= 1.000001 x on [0, 1.5e-6]  [interval; tan x/x '
      'increases]', hi(iv.sin(xb_) / iv.cos(xb_)) <= F('1.000001') * BB)
# Section 3, after Definition 3.6: A < 10.6067, A' < 10.6068, C_Lambda < 1.0000002, A_13 < 12.7476,
# A'_13 < 12.7476 and C_Lambda^(13) < 1.0000002 (rounded up). Gamma, K_W and B (Definition 3.6) have no displayed
# values in Section 3; their values at pi* and pi*_13 are displayed in Section 12.3 and checked in that block.
disp('Section 3, after Definition 3.6: A', 'ltr', A_exact(iv, '9'), '10.6067')
disp("Section 3, after Definition 3.6: A' = A/cos(bar beta) + 1e-8", 'lt', Ap_exact(iv, '9'), '10.6068')
dispq('Section 3, after Definition 3.6: C_Lambda = 1 + 1185.6 delta^2', 'ltr', 1 + F('1185.6') * DL ** 2, '1.0000002')
disp('Section 3, after Definition 3.6: A_13', 'ltr', A_exact(iv, '13'), '12.7476')
disp("Section 3, after Definition 3.6: A'_13 = A_13/cos(bar beta) + 1e-8", 'ltr', Ap_exact(iv, '13'), '12.7476')
dispq('Section 3, after Definition 3.6: C_Lambda^(13) = 1 + 1712.6 delta^2', 'ltr', 1 + F('1712.6') * DL ** 2,
      '1.0000002')

# ============================================================================================================
# Section 4: the auxiliary inequality (Lemma 4.6) and the window (Lemma 4.12)
# ============================================================================================================
head('Section 4: P1 and P2; the threshold a* of Lemma 4.6')


def h_aux(C, t):
    """h(t) = f(t) - 1.0001 t, f(t) = sin t + 1 - cos t (Lemma 4.6); 1 - cos t is written as 2 sin(t/2)^2"""
    t = C.mpf(t)
    return C.sin(t) + 2 * C.sin(t / 2) ** 2 - C.mpf('1.0001') * t


FQ = iv.sin(iv.pi / 4) + 1 - iv.cos(iv.pi / 4)
check('Section 4, Lemma 4.6(a): f(pi/4) = 1  [interval contains 1]', lo(FQ) <= 1 <= hi(FQ), 'f(pi/4) = ' + mid(FQ))
check('Section 4, Lemma 4.6(b): h(pi/4) = 1 - 1.0001 pi/4 > 1 - 1.0001 * 0.7854 = 0.21452146 > 0.2  '
      '[interval: pi/4 < 0.7854; exact]',
      hi(iv.pi / 4) < F('0.7854') and 1 - F('1.0001') * F('0.7854') == F('0.21452146') > F('0.2'))
T1, T2 = F('2.000133e-4'), F('2.000134e-4')
TAY_HI = T1 / 2 - T1 ** 2 / 6 + T1 ** 4 / 120 - F('1e-4')     # upper bound for h(t1)/t1, Lemma 4.6(c)
TAY_LO = T2 / 2 - T2 ** 2 / 6 - T2 ** 3 / 24 - F('1e-4')      # lower bound for h(t2)/t2, Lemma 4.6(c)
# both bounds are rounded towards zero: up for the negative value at t1, down for the positive value at t2
dispq('Section 4, Lemma 4.6(c): t/2 - t^2/6 + t^4/120 - 1e-4 at t1 = 2.000133e-4', 'ltr', TAY_HI, '-1.7e-11')
dispq('Section 4, Lemma 4.6(c): t/2 - t^2/6 - t^3/24 - 1e-4 at t2 = 2.000134e-4', 'gtr', TAY_LO, '3.2e-11')
H1, H2 = h_aux(iv, ivq(T1)), h_aux(iv, ivq(T2))
check('Section 4, Lemma 4.6(c), cross-check: h(t1)/t1 <= t1/2 - t1^2/6 + t1^4/120 - 1e-4 < 0 and '
      'h(t2)/t2 >= t2/2 - t2^2/6 - t2^3/24 - 1e-4 > 0  [interval]',
      hi(H1 / ivq(T1)) <= TAY_HI < 0 < TAY_LO <= lo(H2 / ivq(T2)), 'h(t1) = %s, h(t2) = %s' % (mid(H1), mid(H2)))
ASTAR = mp.findroot(lambda t: h_aux(mp, t), mp.mpf('2.0001e-4'))
AS_LO, AS_HI = ASTAR - mp.mpf('1e-35'), ASTAR + mp.mpf('1e-35')
check('Section 4, Lemma 4.6(b),(c): h < 0 just below and h > 0 just above the computed zero a*, so a* lies in an '
      'interval of width 2e-35 around it  [interval]', hi(h_aux(iv, AS_LO)) < 0 < lo(h_aux(iv, AS_HI)))
disp('Section 4, Lemma 4.6(c): a*', 'tr', iv.mpf([AS_LO, AS_HI]), '2.000133e-4')
check('Section 4, Lemma 4.6(c): f(a) <= a + a^2/2 <= 1.0001 a for 0 <= a <= 2e-4 (a/2 <= 1e-4), and 2e-4 < t1  [exact]',
      F('2e-4') / 2 == F('1e-4') and F('2e-4') < T1)
# Section 4, Lemma 4.12 (window): b_s <= 1e-4 < a* (under (Q2)); b_s <= hat beta(y0) <= 1.5e-6 < 1e-4 (under (C2));
# cos a + sin a <= 1 + a < 1.0001
check('Section 4, Lemma 4.12(a),(b),(d): 1.5e-6 < 1e-4 < t1 < a*, and 1 + 1e-4 = 1.0001  [exact]',
      BB < F('1e-4') < T1 and 1 + F('1e-4') == F('1.0001'))

# ============================================================================================================
# Section 5: end collisions (P3)
# ============================================================================================================
head('Section 5: end collisions (P3); c_E = 41.933')
check('Section 5, Lemma 5.4: cos a + sin a <= sqrt 2 < 2 = (k - h_max) - h_max  [interval]',
      hi(iv.sqrt(iv.mpf(2))) < 2)
# Section 5, Proposition 5.10, Step 1: the ratio 40 tan|Delta|/(theta(2 - theta)) is at most c_E = 41.933
R51 = 40 / ((iv.pi / 4) * (2 - iv.pi / 4))
disp('Section 5, Proposition 5.10, Step 1: 40/((pi/4)(2 - pi/4))', 'tr', R51, '41.93109')
AM = iv.mpf('1.5e-6')
R52 = 40 * (iv.sin(iv.pi / 4 + AM) / iv.cos(iv.pi / 4 + AM)) / ((iv.pi / 4 - AM) * (2 - iv.pi / 4 + AM))
disp('Section 5, Proposition 5.10, Step 1: 40 tan(pi/4 + 1.5e-6)/((pi/4 - 1.5e-6)(2 - pi/4 + 1.5e-6))', 'tr', R52,
     '41.93124')
disp('Section 5, Proposition 5.10, Step 1: the same quantity', 'le', R52, '41.9313')
check('Section 5, Proposition 5.10, Step 1: pi/2 - 2 < 0 (the denominator decreases in alpha_max), pi/4 < 1  [interval]',
      hi(iv.pi / 2 - 2) < 0 and hi(iv.pi / 4) < 1)
check('Section 5, Proposition 5.10, Step 1: both ratios are <= c_E = 41.933  [interval]',
      hi(R51) <= F('41.933') and hi(R52) <= F('41.933'))
check('Section 5, Proposition 5.10, Step 6: 18 * 41.933 = 754.794 <= 754.8 (K = 9) and 26 * 41.933 = 1090.258 <= '
      '1090.3 (K = 13)  [exact]', 18 * F('41.933') == F('754.794') <= F('754.8') and
      26 * F('41.933') == F('1090.258') <= F('1090.3'))
dispq('Section 5, Proposition 5.10: 2 c_E K delta W with K = 9, coefficient 2 * 41.933 * 9', 'le', 2 * F('41.933') * 9,
      '754.8')
dispq('Section 5, Proposition 5.10: 2 c_E K delta W with K = 13, coefficient 2 * 41.933 * 13', 'le',
      2 * F('41.933') * 13, '1090.3')

# ============================================================================================================
# Section 6: the configuration of Proposition 6.17
# ============================================================================================================
head('Section 6: the example of Proposition 6.17')
ZX = [(i + F(i + 1, 1000), i + 1 + F(i + 1, 1000)) for i in range(3)]
check('Section 6, Proposition 6.17: consecutive squares Z_i at distance 1/1000, Z_0, Z_1, Z_2 in [0, 4]^2 (b + 1 < 2), '
      '|J| = 3  [exact]',
      all(ZX[i + 1][0] - ZX[i][1] == F(1, 1000) for i in range(2)) and ZX[0][0] >= 0 and ZX[2][1] == F('3.003') <= 4
      and sum(b - a for a, b in ZX) == 3)
check('Section 6, Proposition 6.17: h_F >= 1 > b, since k/2 - 1 >= 1 for k >= 4 and s + 2 > 2  [exact]',
      F(4, 2) - 1 >= 1)

# ============================================================================================================
# Section 7: deaths, merges and gap overlap (P5); the constants S_K, C_D, C_M, C_G and C_Lambda
# ============================================================================================================
head('Section 7: P5; S_9, S_13, C_D, C_M, C_G, C_Lambda')


def S_K(K):
    """Theorem 7.1: S_K = (1 + 1e-11) 4K/(Q_*(2 - 3e-6)), Q_* = 0.32 (exact rational)"""
    return (1 + F('1e-11')) * 4 * K / (F('0.32') * (2 - F('3e-6')))


# Section 7, Remark 7.3 and Lemma 7.4: delta <= 1e-5 < 0.4999999 < (1/2) cos(3e-6) <= (1/2) cos(2 alpha_max);
# delta < cos(alpha_max)
check('Section 7, Remark 7.3: delta <= 1e-5 < 0.4999999 < (1/2) cos(3e-6) <= (1/2) cos(2 alpha_max)  [interval]',
      DL < F('0.4999999') < lo(iv.cos(iv.mpf('3e-6')) / 2))
check('Section 7, Lemma 7.4: delta <= 1e-5 < cos(1.5e-6) <= cos(alpha_max)  [interval]',
      lo(iv.cos(iv.mpf('1.5e-6'))) > DL)
# Section 7, Lemma 7.9: 4 pi (r + sqrt(2)/2)^2 <= 4 pi 0.70721^2 < 6.29 for r <= 1e-4, hence at most 6 squares
RR = iv.mpf('1e-4') + iv.sqrt(iv.mpf(2)) / 2
check('Section 7, Lemma 7.9: r + sqrt(2)/2 <= 1e-4 + sqrt(2)/2 <= 0.70721  [interval]', hi(RR) <= F('0.70721'),
      '1e-4 + sqrt(2)/2 = ' + mid(RR))
disp('Section 7, Lemma 7.9: 4 pi 0.70721^2', 'ltr', 4 * iv.pi * iv.mpf('0.70721') ** 2, '6.29')
check('Section 7, Lemma 7.9 and proof of Theorem 7.1(M): at most 6 squares (6 < 6.29 < 7), so at most 6 - 2 = 4 '
      'squares Y  [exact]', 6 < F('6.29') < 7)
# Section 7, Lemma 7.11(c): 4*9/(0.32(2-3e-6)) = 56.2500843..., 4*13/(0.32(2-3e-6)) = 81.2501218...;
# tan(theta)/(theta cos(theta)) <= 1/cos^2(3e-6) <= 1 + 1e-11 for 0 < theta <= 3e-6
dispq('Section 7, Lemma 7.11(c): 4*9/(0.32 (2-3e-6))', 'tr', 36 / (F('0.32') * (2 - F('3e-6'))), '56.2500843')
dispq('Section 7, Lemma 7.11(c): 4*13/(0.32 (2-3e-6))', 'tr', 52 / (F('0.32') * (2 - F('3e-6'))), '81.2501218')
TC = 1 / iv.cos(iv.mpf('3e-6')) ** 2
check('Section 7, Lemma 7.11(c): 1/cos^2(3e-6) <= 1 + 1e-11  [interval]', hi(TC) <= 1 + F('1e-11'),
      '1/cos^2(3e-6) - 1 = ' + mid(TC - 1))
check('Section 7, Lemma 7.11(b): theta_e < 2 alpha_max <= 3e-6 <= 1e-5 <= 1e-4, tan(3e-6) < 1  [exact, interval]',
      2 * BB == F('3e-6') <= DL <= F('1e-4') and hi(iv.sin(iv.mpf('3e-6')) / iv.cos(iv.mpf('3e-6'))) < 1)
# Section 7, Theorem 7.1 and Lemma 7.11(c): S_9 <= 56.2501, S_13 <= 81.2502 (rounded up)
dispq('Section 7, Theorem 7.1: S_9 = (1 + 1e-11) 36/(0.32 (2-3e-6))', 'le', S_K(9), '56.2501')
dispq('Section 7, Theorem 7.1: S_13 = (1 + 1e-11) 52/(0.32 (2-3e-6))', 'le', S_K(13), '81.2502')
# Section 7, Theorem 7.1(D) (C_D): C_D = 1 + 56.2501 delta^2 (K = 9), 1 + 81.26 delta^2 (K = 13)
check('Section 7, Theorem 7.1(D), C_D: 1 + S_9 delta^2 <= 1 + 56.2501 delta^2 and 1 + S_13 delta^2 <= '
      '1 + 81.26 delta^2  [exact]', S_K(9) <= F('56.2501') and S_K(13) <= F('81.26'))
# Section 7, Theorem 7.1(M) (C_M): 4/cos(pi/4 + 1.5e-6) = 5.65686273... <= 5.656863; 5.656863 * 56.2501 = 318.1991...
# <= 318.20 = C_M (K = 9); 5.656863 * 81.2502 = 459.6212... <= 459.7 = C_M (K = 13); both rounded up at the last digit
CM = 4 / iv.cos(iv.pi / 4 + iv.mpf('1.5e-6'))
disp('Section 7, proof of Theorem 7.1(M): 4/cos(pi/4 + 1.5e-6)', 'tr', CM, '5.65686273')
disp('Section 7, proof of Theorem 7.1(M): 4/cos(pi/4 + 1.5e-6)', 'le', CM, '5.656863')
dispq('Section 7, proof of Theorem 7.1(M): 5.656863 * 56.2501', 'tr', F('5.656863') * F('56.2501'), '318.1991')
dispq('Section 7, proof of Theorem 7.1(M): 5.656863 * 81.2502', 'tr', F('5.656863') * F('81.2502'), '459.6212')
check('Section 7, Theorem 7.1(M), C_M: 4/cos(pi/4 + alpha_max) S_9 <= 5.656863 * 56.2501 <= 318.20 and '
      '4/cos(pi/4 + alpha_max) S_13 <= 5.656863 * 81.2502 <= 459.7  [interval, exact]',
      hi(CM * ivq(S_K(9))) <= F('5.656863') * F('56.2501') <= F('318.20') and
      hi(CM * ivq(S_K(13))) <= F('5.656863') * F('81.2502') <= F('459.7'))
disp('Section 7, Theorem 7.1(M): C_M = 4/cos(pi/4 + 1.5e-6) S_9 (all values rounded up)', 'le', CM * ivq(S_K(9)), '318.20')
disp('Section 7, Theorem 7.1(M): C_M = 4/cos(pi/4 + 1.5e-6) S_13 (all values rounded up)', 'le', CM * ivq(S_K(13)), '459.7')
# Section 7, Theorem 7.1(G) (C_G): S_9/cos(1.5e-6) < 56.2501 = C_G (K = 9), S_13/cos(1.5e-6) < 81.2502 <= 81.26 = C_G
CG9 = ivq(S_K(9)) / iv.cos(iv.mpf('1.5e-6'))
CG13 = ivq(S_K(13)) / iv.cos(iv.mpf('1.5e-6'))
disp('Section 7, proof of Theorem 7.1(G), C_G: S_9/cos(1.5e-6)', 'ltr', CG9, '56.2501')
disp('Section 7, proof of Theorem 7.1(G): S_13/cos(1.5e-6)', 'ltr', CG13, '81.2502')
check('Section 7, Theorem 7.1(G), C_G for K = 13: 81.2502 <= 81.26  [exact]', F('81.2502') <= F('81.26'))
# Section 7, proof of Theorem 7.1(M): w_e < 3.1e-6 delta; |q - v_1|, |q - v_2| < 1.01 delta; radius 3 delta <= 3e-5
WE = iv.sin(iv.mpf('3e-6')) / iv.cos(iv.mpf('3e-6')) ** 2
TN2 = (iv.sin(iv.mpf('3e-6')) / iv.cos(iv.mpf('3e-6'))) ** 2
check('Section 7, proof of Theorem 7.1(M): w_e/delta = tan(theta)/cos(theta) <= tan(3e-6)/cos(3e-6) < 3.1e-6  '
      '[interval]', hi(WE) < F('3.1e-6'), mid(WE))
check('Section 7, proof of Theorem 7.1(M): (3.1e-6)^2 + 1 < 1.01^2 and tan(3e-6)^2 + 1 < 1.01^2  [exact, interval]',
      F('3.1e-6') ** 2 + 1 < F('1.01') ** 2 and hi(TN2 + 1) < F('1.01') ** 2)
check('Section 7, proof of Theorem 7.1(M): 2 * 1.01 delta < 3 delta and 3 delta <= 3e-5 <= 1e-4 (Lemma 7.9)  [exact]',
      2 * F('1.01') < 3 and 3 * DL == F('3e-5') <= F('1e-4'))
# Section 7, Corollary 7.2 and its proof: C_Lambda = 1 + 1185.6 delta^2 (K = 9), 1 + 1712.6 delta^2 (K = 13)
check('Section 7, proof of Corollary 7.2: 56.2501 + 318.20 + 754.8 + 56.2501 = 1185.5002 <= 1185.6  [exact]',
      F('56.2501') + F('318.20') + F('754.8') + F('56.2501') == F('1185.5002') <= F('1185.6'))
check('Section 7, proof of Corollary 7.2: 81.26 + 459.7 + 1090.3 + 81.26 = 1712.52 <= 1712.6  [exact]',
      F('81.26') + F('459.7') + F('1090.3') + F('81.26') == F('1712.52') <= F('1712.6'))
check('Section 7, Corollary 7.2: 1185.6 delta^2 <= 1.1856e-7 < 2e-7 and 1712.6 delta^2 <= 1.7126e-7 < 2e-7, '
      'so C_Lambda < 1.0000002  [exact]',
      F('1185.6') * DL ** 2 == F('1.1856e-7') < F('2e-7') and F('1712.6') * DL ** 2 == F('1.7126e-7') < F('2e-7'))

# ============================================================================================================
# Section 8: P6, the path version of [R, Lemma 4.14]; the constants A', A'_13 and the error terms
# ============================================================================================================
head("Section 8: P6; chi_e, the error terms 8.5e-10 and 1.22e-9, A' and A'_13")
BBI = iv.mpf('1.5e-6')
KAP = iv.sin(iv.pi / 4 + BBI) / iv.cos(iv.pi / 4 + BBI)
disp('Section 8, Section 8.3: |kappa_e| < tan(pi/4 + bar beta)', 'ltr', KAP, '1.00001')
CHI = iv.cos(BBI) - iv.mpf('1.00001') * BBI
disp('Section 8, Lemma 8.7: chi_e > cos(1.5e-6) - 1.00001 * 1.5e-6', 'gtr', CHI, '0.99999849')
dispq('Section 8, Lemma 8.7: 1/chi_e < 1/0.99999849', 'ltr', 1 / F('0.99999849'), '1.0000016')
dispq('Section 8, Lemma 8.7(c): the constant 1.0000016 of (c) bounds 1/chi_e < 1/0.99999849', 'ltr', 1 / F('0.99999849'),
      '1.0000016')
check('Section 8, Lemma 8.9(a): vertical extent cos a + sin a <= sqrt 2 < 2 = (k/2 + 1) - (k/2 - 1)  [interval]',
      hi(iv.sqrt(iv.mpf(2))) < 2)
check('Section 8, Lemma 8.11: 1e-5 (2 - 1e-5)/40 > 4.99e-7 > 2.4e-7 = 0.32 * 1.5e-6 * 2/4  [exact]',
      F('1e-5') * (2 - F('1e-5')) / 40 > F('4.99e-7') > F('2.4e-7') == F('0.32') * BB * 2 / 4)
check('Section 8, Lemma 8.11: theta_e <= pi/4 < 1 (x(2-x) increases on [0, 1])  [interval]', hi(iv.pi / 4) < 1)
# Section 8, proof of Theorem 8.3 (Section 8.7), Steps 3-6
check('Section 8, proof of Theorem 8.3, Step 3: 2 - bar beta = 2 - 1.5e-6 >= 2 - 3e-6; 4 * 9 = 36, 4 * 13 = 52  [exact]',
      2 - BB >= 2 - F('3e-6') and 4 * 9 == 36 and 4 * 13 == 52)
dispq('Section 8, proof of Theorem 8.3, Step 4: 36/(0.32 (2 - 1.5e-6))', 'ltr', 36 / (F('0.32') * (2 - BB)), '56.26')
dispq('Section 8, proof of Theorem 8.3, Step 4: error term 1.0000016 * 1e-5 * 1.5e-6 * 56.26', 'ltr',
      F('1.0000016') * DL * BB * F('56.26'), '8.5e-10')
SECB = 1 / iv.cos(BBI)
check('Section 8, proof of Theorem 8.3, Step 5: 1/cos(bar beta) < 1 + 1.2e-12  [interval]', hi(SECB) < 1 + F('1.2e-12'),
      '1/cos(1.5e-6) - 1 = ' + mid(SECB - 1))
disp('Section 8, proof of Theorem 8.3, Step 5: A = 4 sqrt(9/0.32)/(2-3e-6)', 'ltr', A_exact(iv, '9'), '10.6067')
check("Section 8, proof of Theorem 8.3, Step 5: A' < 10.6067 (1 + 1.2e-12) + 1e-8 < 10.60671 < 10.6068, and "
      "8.5e-10 <= 1e-8 (so A/cos(bar beta) + 8.5e-10 <= A')  [exact]",
      F('10.6067') * (1 + F('1.2e-12')) + F('1e-8') < F('10.60671') < F('10.6068') and F('8.5e-10') <= F('1e-8'))
disp("Section 8, Theorem 8.3(a) and Corollary 8.13: A' = A/cos(bar beta) + 1e-8", 'lt', Ap_exact(iv, '9'), '10.6068')
dispq('Section 8, proof of Theorem 8.3, Step 6: 52/(0.32 (2 - 1.5e-6))', 'ltr', 52 / (F('0.32') * (2 - BB)), '81.26')
dispq('Section 8, proof of Theorem 8.3, Step 6: error term 1.0000016 * 1e-5 * 1.5e-6 * 81.26', 'ltr',
      F('1.0000016') * DL * BB * F('81.26'), '1.22e-9')
disp('Section 8, proof of Theorem 8.3, Step 6: A_13 = 4 sqrt(13/0.32)/(2-3e-6)', 'ltr', A_exact(iv, '13'), '12.74757')
check("Section 8, proof of Theorem 8.3, Step 6: A'_13 < 12.74757 (1 + 1.2e-12) + 1e-8 < 12.7476, and 1.22e-9 <= 1e-8"
      "  [exact]", F('12.74757') * (1 + F('1.2e-12')) + F('1e-8') < F('12.7476') and F('1.22e-9') <= F('1e-8'))
disp('Section 8, Theorem 8.3(c): A_13', 'ltr', A_exact(iv, '13'), '12.7476')
disp("Section 8, Theorem 8.3(c) and Corollary 8.13: A'_13 = A_13/cos(bar beta) + 1e-8", 'ltr', Ap_exact(iv, '13'),
     '12.7476')

# ============================================================================================================
# Section 9: P7, the per-scale count; the window V_s
# ============================================================================================================
head('Section 9: P7; the window V_s and b_W')
check('Section 9, Section 9.1: |V_s| = eps s + b_W with b_W = 2 * 1.0001 = 2.0002  [exact]',
      2 * F('1.0001') == F('2.0002'))
check('Section 9, Lemma 9.3(c),(d): 0 < a(Z) < 1.5e-6, so cos a + sin a <= 1 + a < 1 + 1.5e-6 < 1.0001  [exact]',
      1 + BB < F('1.0001'))
check('Section 9, Lemma 9.3(e): a < 1.5e-6 < 2e-4, and a^2/2 <= 1e-4 a for 0 <= a <= 2e-4  [exact]',
      BB < F('2e-4') and F('2e-4') / 2 == F('1e-4'))
R94 = iv.mpf('1.0001') * iv.pi / 4
disp('Section 9, Remark 9.4: 1.0001 pi/4', 'tr', R94, '0.7854767')
check('Section 9, Remark 9.4: f(pi/4) = 1 > 1.0001 pi/4  [interval]', lo(FQ) > hi(R94))
check('Section 9, Remark 9.13(2): 2 (1 + 1.5e-6) - 2 = 3e-6, and b_W = 2 + 3e-6 <= 2.0002  [exact]',
      2 * (1 + BB) - 2 == F('3e-6') and 2 + F('3e-6') <= F('2.0002'))
check('Section 9, proof of Theorem 9.1, Step 5: s + 1.0001 <= k/2 - 3 + 1.0001 < k (k >= 4), and 1.0001 <= 2  [exact]',
      F(4, 2) - 3 + F('1.0001') < 4 and F('1.0001') <= 2)
check('Section 9, Remark 9.5: hypotheses of [R, Lemma 4.13] (bar beta = 1.5e-6 <= 1.5e-6) and of [R, Lemma 4.15] '
      '(delta = 1e-5 <= 1e-5, beta(y) <= 1.5e-6)  [exact]', BB <= F('1.5e-6') and DL <= F('1e-5'))

# ============================================================================================================
# Section 10: elementary facts used in the proof of Theorem 10.3
# ============================================================================================================
head('Section 10: elementary inequalities and identities')
x = iv.mpf('1.5e-6')
check('Section 10, Step 11: tan(1.5e-6) <= 1.000001 * 1.5e-6  [interval; tan x/x is increasing]',
      hi(iv.sin(x) / iv.cos(x)) <= F('1.000001') * F('1.5e-6'), 'tan(x)/x = ' + mid(iv.sin(x) / iv.cos(x) / x))
check('Lemma 10.1(b): (1/2) cos(3e-6) > 0.495 > delta = 1e-5  [interval]',
      lo(iv.cos(iv.mpf('3e-6')) / 2) > F('0.495') > F('1e-5'))


def pmul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, c in enumerate(q):
            out[i + j] += a * c
    return out


def padd(p, q, s=1):
    n = max(len(p), len(q))
    p, q = p + [0] * (n - len(p)), q + [0] * (n - len(q))
    return [a + s * c for a, c in zip(p, q)]


# 3(1 - v^4) - 4 v^3 (1 - v^3) and (v-1)^2 (4v^4 + 8v^3 + 9v^2 + 6v + 3), coefficient lists of v^0, v^1, ...
lhs = padd(pmul([3], [1, 0, 0, 0, -1]), pmul([0, 0, 0, 4], [1, 0, 0, -1]), -1)
rhs = pmul([1, -2, 1], [3, 6, 9, 8, 4])
check('Lemma 10.2: 3(1-v^4) - 4v^3(1-v^3) = 4v^6-3v^4-4v^3+3 = (v-1)^2(4v^4+8v^3+9v^2+6v+3)  [exact]',
      lhs == rhs == [3, 0, 0, -4, -3, 0, 4], str(lhs))
check('Lemma 10.5: 2 * 0.50001 = 1.00002  [exact]', 2 * F('0.50001') == F('1.00002'))

# ============================================================================================================
# Section 12.2: fixed constants (Table tab:const-fixed) and the constants of Theorems A, A13 (Section 1)
# ============================================================================================================
head('Section 12.2: fixed constants')
for K, sA, sAp, sAb, sApb, CLs, CLv in (('9', '10.6066176277', '10.6066176377', '10.6067', '10.6068', '1185.6',
                                        '1.00000011856'),
                                       ('13', '12.7475679053', '12.7475679153', '12.7476', '12.7476', '1712.6',
                                        '1.00000017126')):
    Ai, Api = A_exact(iv, K), Ap_exact(iv, K)
    disp('K=%s: A = 4 sqrt(%s/0.32)/(2-3e-6)' % (K, K), 'tr', Ai, sA)
    disp('K=%s: A' % K, 'lt', Ai, sAb)
    disp("K=%s: A' = A/cos(1.5e-6) + 1e-8" % K, 'tr', Api, sAp)
    disp("K=%s: A'" % K, 'lt', Api, sApb)
    check('K=%s: C_Lambda = 1 + %s delta^2 = %s  [exact]' % (K, CLs, CLv), 1 + F(CLs) * F('1e-5') ** 2 == F(CLv))
    check('K=%s: C_Lambda < 1.0000002  [exact]' % K, F(CLv) < F('1.0000002'))
# the sums behind C_Lambda (Sections 5 and 7) and behind C_Lambda^(13)
check('C_Lambda: 56.2501 + 318.20 + 56.2501 + 754.8 <= 1185.6  [exact]',
      F('56.2501') + F('318.20') + F('56.2501') + F('754.8') <= F('1185.6'))
check('C_Lambda^(13): 81.26 + 459.7 + 81.26 + 1090.3 <= 1712.6  [exact]',
      F('81.26') + F('459.7') + F('81.26') + F('1090.3') <= F('1712.6'))
check("A'_13 >= 4 sqrt(13/0.32)/((2-1.5e-6) cos(1.5e-6)) + 1e-8  [interval]",
      lo(Ap_exact(iv, '13')) >= hi(4 * iv.sqrt(iv.mpf(13) / iv.mpf('0.32')) /
                                   ((2 - iv.mpf('1.5e-6')) * iv.cos(iv.mpf('1.5e-6'))) + iv.mpf('1e-8')))

# the asymptotic constant (Section 11.4, the displayed formula for c_inf)
lam = F('2e-5') + F('2e-12')
check('lambda_* = 2 delta + 2e-12 = 2.0000002e-5  [exact]', lam == F('2.0000002e-5'))
check('Lemma 11.4: 5 * 1.00002 = 5.0001  [exact]', 5 * F('1.00002') == F('5.0001'))
c0opt_sq = (1 - lam) / F('5.0001')
check('Proposition 11.5: (c0opt)^2 = (1-lambda_*)/5.0001 < 0.2  [exact]', c0opt_sq < F('0.2'))
check('Proposition 11.5: 0.50001 (c0opt)^2 + delta + 1e-12 < 0.10002 < 1/2  [exact]',
      F('0.50001') * c0opt_sq + F('1e-5') + F('1e-12') < F('0.10002') < F(1, 2))
c0opt_iv = iv.sqrt((1 - iv.mpf('2e-5') - iv.mpf('2e-12')) / iv.mpf('5.0001'))
disp('c0opt = sqrt((1-lambda_*)/5.0001)', 'tr', c0opt_iv, '0.4472046513')


def cinf(C, A, Ap):
    lamC = C.mpf('2e-5') + C.mpf('2e-12')
    return 16 * pw(C, C.mpf(2), -1, 4) / (5 * C.sqrt(A * Ap)) * pw(C, 1 - lamC, 5, 4) * pw(C, C.mpf('5.0001'), -1, 4)


def cinf_first_form(C, A, Ap):
    lamC = C.mpf('2e-5') + C.mpf('2e-12')
    c0o = C.sqrt((1 - lamC) / C.mpf('5.0001'))
    h0inf = 1 - lamC - C.mpf('1.00002') * c0o ** 2
    return 4 * pw(C, C.mpf(2), -1, 4) * h0inf * C.sqrt(c0o) / C.sqrt(A * Ap)


for K, s_ex, s_up, s_th in (('9', '0.1696524112', '0.1696502940', '0.1696524'),
                            ('13', '0.1411593387', '0.1411589833', '0.1411593')):
    ce = cinf(iv, A_exact(iv, K), Ap_exact(iv, K))
    cu = cinf(iv, iv.mpf(UPPER[K][0]), iv.mpf(UPPER[K][1]))
    disp("K=%s: c_inf (exact A, A')" % K, 'tr', ce, s_ex)
    disp('K=%s: c_inf as stated in Theorem %s (Section 1)' % (K, 'A' if K == '9' else 'A13'), 'tr', ce, s_th)
    disp('K=%s: c_inf^+ (with the upper bounds of Sections 11.1 and 11.5)' % K, 'tr', cu, s_up)
    f1 = cinf_first_form(iv, A_exact(iv, K), Ap_exact(iv, K))
    check('K=%s: the two expressions for c_inf in Section 11.4 agree  [intervals overlap and have width < 1e-40]' % K,
          lo(f1) <= hi(ce) and lo(ce) <= hi(f1) and hi(ce) - lo(ce) < F('1e-40'))

# ============================================================================================================
# Section 12.3: Table tab:const-main -- Theorem A (pi*, k0 = 4.62e12) and Theorem A13 (pi_13, k0 = 2.17e13)
# ============================================================================================================
MAIN = {
    'A': dict(K='9', par=('0.3078', '0.2754', '42108000000', '5.8e-6', '1.7e-5'), k0='4620000000000', ceil=147,
              rows=[('al0', 'le', '1.4999830e-6'), ('be0', 'le', '2.9628e-9'), ('bstar', 'le', '2.9628e-9'),
                    ('C3l', 'le', '0.27541'), ('C3r', 'ge', '139.43'), ('w0', 'le', '0.04738138'),
                    ('h0', 'ge', '0.9052372592'), ('invF', 'ge', '0.99998818'), ('Gp', 'le', '2.8472e-5'),
                    ('B1', 'le', '0.00063282'), ('B2', 'le', '19.256900'), ('B3', 'le', '19.249235'),
                    ('B', 'le', '38.506796'), ('Cw', 'le', '3.5789897'), ('KO', 'le', '0.3390769'),
                    ('Pinf', 'tr', '0.1581428')],
              krows=[('C7r', 'ge', '2.3099866e12'), ('Omb', 'le', '0.37941519'), ('wall', 'le', '1.3579231'),
                     ('LH', 'ge', '5647.4855'), ('Psi', 'ge', '146.62429'), ('tgt', 'le', '146.60896'),
                     ('D1', 'ge', '0.0086429'), ('iiiL', 'ge', '10.655'), ('iiiR', 'le', '0.0044029')],
              epsy0='244226.4'),
    'A13': dict(K='13', par=('0.3674', '0.3012', '60000000000', '5e-6', '1.4e-5'), k0='21700000000000', ceil=216,
                rows=[('al0', 'le', '1.4999043e-6'), ('be0', 'le', '2.4846e-9'), ('bstar', 'le', '2.4846e-9'),
                      ('C3l', 'le', '0.30121'), ('C3r', 'ge', '181.83'), ('w0', 'le', '0.06750274'),
                      ('h0', 'ge', '0.8649945353'), ('invF', 'ge', '0.99999020'), ('Gp', 'le', '3.1351e-5'),
                      ('B1', 'le', '0.00058920'), ('B2', 'le', '21.161355'), ('B3', 'le', '21.147482'),
                      ('B', 'le', '42.309457'), ('Cw', 'le', '3.2792918'), ('KO', 'le', '0.4426483'),
                      ('Pinf', 'tr', '0.1375313')],
                krows=[('C7r', 'ge', '1.0849945e13'), ('Omb', 'le', '0.70158383'), ('wall', 'le', '2.3006981'),
                       ('LH', 'ge', '9134.3029'), ('Psi', 'ge', '215.83530'), ('tgt', 'le', '215.83156'),
                       ('D1', 'ge', '0.0055790'), ('iiiL', 'ge', '10.125'), ('iiiR', 'le', '0.0052311')],
                epsy0='300000'),
}
NAMES = {'al0': 'alpha(y0)', 'be0': 'hat beta(y0)', 'bstar': 'b*', 'C3l': '(C3) left side c1(1-eps)^(-3/4)',
         'C3r': '(C3) right side c0 y0^(1/4)', 'w0': 'w0', 'h0': 'h0', 'invF': 'invF', 'Gp': 'Gamma',
         'B1': 'term 1/(omega0 y0^(3/4)) of bar B', 'B2': 'term A/(2c1) of bar B',
         'B3': "term 2c1/(c0 invF)(A'+alpha(y0)C_Lambda/delta) of bar B", 'B': 'bar B',
         'Cw': 'C_wall = 4c1/(c0 invF)', 'KO': 'K_W', 'Pinf': 'Psi_infinity(pi) (limit of bar Psi(k)/k^(1/4))',
         'C7r': '(C7) right side (1-eps)(k0/2-3)', 'Omb': 'upper bound for Omega_W (Thm 10.3) at k0',
         'wall': 'wall term C_wall * (bound for Omega_W) at k0', 'LH': 'lower bound for ell(H) (Thm 10.3) at k0',
         'Psi': 'bar Psi(k0)', 'tgt': '0.1 k0^(1/4)', 'D1': 'D1', 'iiiL': 'y1(k0)^(1/4) D1',
         'iiiR': 'K_W/(2 bar B)'}

for th, S in MAIN.items():
    head('Section 12.3: Table tab:const-main, column Theorem %s (Sections 11.3 and 11.5)' % th)
    tag = '[Thm %s]' % th
    constraints(tag, S['par'], S['k0'], S['K'])
    check(tag + ' eps*y0 = %s  [exact]' % S['epsy0'], F(S['par'][3]) * F(S['par'][2]) == F(S['epsy0']))
    dm, rm, di, ri = both(S['par'], S['K'], k=S['k0'], cs='0.1')
    shown = {}
    for key, kind, s in S['rows']:
        disp(tag + ' ' + NAMES[key], kind, di[key], s)
        shown[key] = s
    for key, kind, s in S['krows']:
        disp(tag + ' ' + NAMES[key], kind, ri[key], s)
        shown[key] = s
    check(tag + ' the four terms of bar B add up to bar B  [interval]',
          lo(di['B1'] + di['B2'] + di['B3'] + di['Gp']) <= hi(di['B']) and
          lo(di['B']) <= hi(di['B1'] + di['B2'] + di['B3'] + di['Gp']))
    check(tag + ' (C7) from the displayed bound: y0 + 1 <= %s' % shown['C7r'], F(S['par'][2]) + 1 <= F(shown['C7r']))
    monotone_conditions(tag, ri)
    check(tag + ' (i)-(iii) read off the displayed values: %s > %s, %s > 0, %s > %s' % (
        shown['Psi'], shown['tgt'], shown['D1'], shown['iiiL'], shown['iiiR']),
        F(shown['Psi']) > F(shown['tgt']) and F(shown['D1']) > 0 and F(shown['iiiL']) > F(shown['iiiR']))
    n = S['ceil']
    check(tag + ' ceil(0.1 k0^(1/4)) = %d  [interval: %d < 0.1 k0^(1/4) <= %d]' % (n, n - 1, n),
          lo(ri['tgt']) > n - 1 and hi(ri['tgt']) <= n and F(shown['tgt']) <= n)
    check(tag + ' the 50-digit value of bar Psi(k0) agrees with the interval midpoint to 1e-30',
          abs(frac_mp(rm['Psi']) - (lo(ri['Psi']) + hi(ri['Psi'])) / 2) < F('1e-30'))

# ============================================================================================================
# Section 11.6: Corollary A (integer facts)
# ============================================================================================================
head('Section 11.6: Corollary A; numbers stated in Section 1')
check('10^4 * 146^4 + 1 = 4543718560001 < 4.62e12  [exact]', 10 ** 4 * 146 ** 4 + 1 == 4543718560001 < 4620000000000)
check('10^4 * 147^4 + 1 = 4669488810001 > 4.62e12  [exact]', 10 ** 4 * 147 ** 4 + 1 == 4669488810001 > 4620000000000)
check('10^4 * 215^4 + 1 = 21367506250001 < 2.17e13  [exact]',
      10 ** 4 * 215 ** 4 + 1 == 21367506250001 < 21700000000000)
check('10^4 * 216^4 + 1 = 21767823360001 > 2.17e13  [exact]',
      10 ** 4 * 216 ** 4 + 1 == 21767823360001 > 21700000000000)
check('(c/0.1)^4 = 10^4 c^4 for c = 0, ..., 300  [exact]',
      all((F(c) / F('0.1')) ** 4 == 10 ** 4 * c ** 4 for c in range(301)))
check('c*(k0) >= ceil(0.1 k0^(1/4)) - 1: 147 - 1 = 146 and 216 - 1 = 215', 147 - 1 == 146 and 216 - 1 == 215)
# numbers in the comparison paragraph of Section 1
check('Section 1: log(4.62e12) < 29.17  [interval]', hi(iv.log(iv.mpf('4620000000000'))) < F('29.17'),
      'log(4.62e12) = ' + mid(iv.log(iv.mpf('4620000000000'))))
check('Section 1: 1.99954/30.418 > 0.0657  [exact]', F('1.99954') / F('30.418') > F('0.0657'))

# ============================================================================================================
# Section 12.5: further thresholds (Table tab:const-pairs) and bounds at given k (Table tab:const-k)
# ============================================================================================================
PAIRS = [  # (K, c*, k0, pi, ratio bar Psi(k0)/k0^(1/4) (>=), D1 (>=), y1(k0)^(1/4) D1 (>=), K_W/(2 bar B) (<=))
    ('9', '0.12', '21700000000000', ('0.3674', '0.3009', '60000000000', '5e-6', '1.5e-5'),
     '0.1200448', '0.0067036', '12.166', '0.0062733'),
    ('9', '0.14', '201000000000000', ('0.4086', '0.3173', '74220000000', '4.7e-6', '1.5e-5'),
     '0.1400019', '0.0041135', '13.024', '0.0077586'),
    ('9', '0.15', '1180000000000000', ('0.4243', '0.3234', '80030000000', '4.6e-6', '1.4e-5'),
     '0.1500058', '0.0027026', '13.320', '0.0083679'),
    ('9', '0.16', '27700000000000000', ('0.4376', '0.3284', '85109000000', '4.5e-6', '1.4e-5'),
     '0.1600075', '0.0012500', '13.560', '0.0088999'),
    ('13', '0.12', '378000000000000', ('0.4153', '0.3203', '76670000000', '4.6e-6', '1.3e-5'),
     '0.1200086', '0.0029558', '10.959', '0.0066855'),
]
head('Section 12.5: further thresholds (c*, k0), Table tab:const-pairs')
for K, cs, k0, par, s_rat, s_d1, s_iii, s_r in PAIRS:
    tag = '[K=%s c*=%s k0=%s]' % (K, cs, k0)
    constraints(tag, par, k0, K)
    dm, rm, di, ri = both(par, K, k=k0, cs=cs)
    monotone_conditions(tag, ri)
    disp(tag + ' bar Psi(k0)/k0^(1/4)', 'ge', ri['ratio'], s_rat)
    disp(tag + ' D1', 'ge', ri['D1'], s_d1)
    disp(tag + ' y1(k0)^(1/4) D1', 'ge', ri['iiiL'], s_iii)
    disp(tag + ' K_W/(2 bar B)', 'le', ri['iiiR'], s_r)
    check(tag + ' (i)-(iii) read off the displayed values: %s >= %s, %s > 0, %s > %s' % (s_rat, cs, s_d1, s_iii, s_r),
          F(s_rat) >= F(cs) and F(s_d1) > 0 and F(s_iii) > F(s_r))
check('Section 12.5: (2065/0.16)^4 > 2.77e16 > (2064/0.16)^4  [exact]',
      (F(2065) / F('0.16')) ** 4 > F('2.77e16') > (F(2064) / F('0.16')) ** 4)

KTAB = [  # (K, log10 k, pi, bar B (<=), bar Psi(k) (>=), W >=)
    ('9', 13, ('0.3421', '0.2903', '52015000000', '5.3e-6', '1.6e-5'), '36.52537', '196.77', 197),
    ('9', 14, ('0.3993', '0.3136', '70863000000', '4.8e-6', '1.5e-5'), '33.80809', '426.16', 427),
    ('9', 16, ('0.4345', '0.3273', '83930000000', '4.5e-6', '1.4e-5'), '32.40967', '1575.76', 1576),
    ('9', 20, ('0.4457', '0.3324', '245800000000', '2.7e-6', '9.5e-6'), '31.91017', '16751.28', 16752),
    ('9', 30, ('0.4472', '0.3343', '547300000000000', '5.7e-8', '5.3e-7'), '31.72495', '5363347.52', 5363348),
    ('13', 13, ('0.3421', '0.2907', '52015000000', '5.3e-6', '1.4e-5'), '43.84613', '163.91', 164),
    ('13', 14, ('0.3993', '0.314', '70863000000', '4.8e-6', '1.3e-5'), '40.58423', '355.01', 356),
    ('13', 16, ('0.4345', '0.3276', '83930000000', '4.5e-6', '1.3e-5'), '38.90551', '1312.66', 1313),
    ('13', 20, ('0.4458', '0.3325', '192800000000', '3e-6', '9.5e-6'), '38.33686', '13948.51', 13949),
    ('13', 30, ('0.4472', '0.3343', '428700000000000', '6.4e-8', '5.3e-7'), '38.12805', '4462691.45', 4462692),
]
head('Section 12.5: lower bounds at given k, Table tab:const-k')
for K, lk, par, s_B, s_Psi, n in KTAB:
    k = '1' + '0' * lk
    tag = '[K=%s k=1e%d]' % (K, lk)
    constraints(tag, par, k, K)
    dm, rm, di, ri = both(par, K, k=k, cs='0.1')
    disp(tag + ' bar B', 'le', di['B'], s_B)
    disp(tag + ' bar Psi(k)', 'ge', ri['Psi'], s_Psi)
    check(tag + ' W >= %d, since W is an integer and bar Psi(k) >= %s > %d' % (n, s_Psi, n - 1),
          lo(ri['Psi']) > n - 1 and n - 1 < F(s_Psi) <= n)

# ============================================================================================================
# Section 12.6: sensitivity of k0 = 4.62e12 for Theorem A (pi* fixed, c* = 0.1)
# ============================================================================================================
head('Section 12.6: sensitivity of k0 = 4.62e12 (pi* fixed)')
PS = MAIN['A']['par']
K0 = MAIN['A']['k0']
dm, rm, di, ri = both(PS, '9', k=K0, cs='0.1')
disp('B_crit = [(1-omega0)(ell(H) bound) - C_wall (Omega_W bound)]/(0.1 k0^(1/4))', 'ge', ri['Bcrit'], '38.510824')
disp('relative margin (B_crit - bar B)/bar B', 'tr', (ri['Bcrit'] - di['B']) / di['B'], '1.0463e-4')
check('relative margin < 1.05e-4  [interval]', hi((ri['Bcrit'] - di['B']) / di['B']) < F('1.05e-4'))
check('(iii) is monotone in B: y1^(1/4) h0 (1-omega0)(1-eps)^(1/4) > K_W/2  [interval]', lo(ri['mono']) > 0)

SENS = [  # (description, parameter, tolerance stated in Section 12.6 (a)-(f), truncation of the largest value)
    ("(a) A' (A = 10.6067 fixed)", 'Ap', '10.60905', '10.6090514'),
    ("(b) A (A' = 10.6068 fixed)", 'A', '10.60891', '10.6089191'),
    ("(c) A, with A' = A + 1e-4", 'A_Ap', '10.60781', '10.6078176'),
    ('(d) C_Lambda', 'CL', '1.0150', '1.0150101'),
    ('(e) b_W', 'bw', '53.09', '53.0942'),
    ('(f) factor on the wall term', 'wallfac', '1.434', '1.43499'),
]
SENS_RANGE = {'Ap': ('10.6068', '11'), 'A': ('10.6067', '11'), 'A_Ap': ('10.6067', '11'), 'CL': ('1.0000002', '3'),
              'bw': ('2.0002', '1000'), 'wallfac': ('1', '10')}


def frac_to_dec(fr):
    """exact decimal string of a rational number whose denominator divides a power of 10"""
    num, den = fr.numerator, fr.denominator
    e = 0
    while (10 ** e) % den:
        e += 1
    n = num * (10 ** e // den)
    s = str(abs(n)).rjust(e + 1, '0')
    return ('-' if n < 0 else '') + (s[:-e] + '.' + s[-e:] if e > 0 else s)


def scen(key, v, k=K0, Kset='9'):
    """the quantities at pi*, k with one constant changed: A, Ap, CL, bw, wallfac, AAp (A = A' = v), or
    A_Ap (A = v, A' = v + 1e-4, computed exactly)"""
    if key == 'A_Ap':
        kw = dict(A=v, Ap=frac_to_dec(F(v) + F('1e-4')))
    elif key == 'AAp':
        kw = dict(A=v, Ap=v)
    else:
        kw = {key: v}
    return both(PS, Kset, k=k, cs='0.1', **kw)


def margin_mp(key, v, k=K0):
    """bar Psi(k) - 0.1 k^(1/4) in 50-digit arithmetic"""
    _, rmx, _, _ = scen(key, v, k=k)
    return rmx['Psi'] - rmx['tgt']


def bisect_mp(f, a, b, steps=170):
    """largest x in [a, b] with f(x) >= 0, for f decreasing with f(a) >= 0 > f(b)"""
    a, b = mp.mpf(a), mp.mpf(b)
    for _ in range(steps):
        m = (a + b) / 2
        if f(m) >= 0:
            a = m
        else:
            b = m
    return a


for desc, key, tol, tmax in SENS:
    # the threshold, recomputed by bisection in 50-digit arithmetic
    lo_s, hi_s = SENS_RANGE[key]
    xmax = bisect_mp(lambda v: margin_mp(key, nstr(v, 45)), lo_s, hi_s)
    check('%s: recomputed largest value for (i) = %s; its truncation is %s and the stated sufficient value %s is '
          'below it (rounded down)' % (desc, nstr(xmax, 15), tmax, tol),
          F(tmax) <= frac_mp(xmax) < F(tmax) + unit_of(tmax) and F(tol) <= frac_mp(xmax))
    # rigorous: (i)-(iii) at the stated value, and the bracket [tmax, tmax + unit) for the largest value
    _, _, di2, ri2 = scen(key, tol)
    check('%s = %s: conditions (i)-(iii) at k0 and the monotonicity condition of Section 12.6  [interval]'
          % (desc, tol),
          lo(ri2['Psi']) >= hi(ri2['tgt']) and lo(ri2['D1']) > 0 and lo(ri2['iiiL']) >= hi(ri2['iiiR'])
          and lo(ri2['mono']) > 0, 'bar Psi - target = ' + mid(ri2['Psi'] - ri2['tgt']))
    nxt = plus_unit(tmax)
    _, _, _, ra = scen(key, tmax)
    _, _, _, rb = scen(key, nxt)
    check('%s: (i) holds at %s and fails at %s, so the largest value lies in [%s, %s)  [interval]'
          % (desc, tmax, nxt, tmax, nxt), lo(ra['Psi']) >= hi(ra['tgt']) and hi(rb['Psi']) < lo(rb['tgt']))
# (c) in the form A = A' <= 10.60781 (covered by (c), since A' = A <= A + 1e-4); also checked directly
_, _, _, rc = scen('AAp', '10.60781')
check("(c) A = A' = 10.60781: conditions (i)-(iii) at k0  [interval]",
      lo(rc['Psi']) >= hi(rc['tgt']) and lo(rc['D1']) > 0 and lo(rc['iiiL']) >= hi(rc['iiiR']))
# C_Lambda = 2 with pi* unchanged: crossing point, rounded up to 4.845e12
_, _, _, r1 = scen('CL', '2', k='4620000000000')
check('C_Lambda = 2: condition (i) fails at k = 4.62e12  [interval]', hi(r1['Psi']) < lo(r1['tgt']),
      'bar Psi - target = ' + mid(r1['Psi'] - r1['tgt']))
check('C_Lambda = 2: (ii) and (iii) hold at k = 4.62e12, so bar Psi(k) - 0.1 k^(1/4) increases on [4.62e12, inf)'
      '  [interval]', lo(r1['D1']) > 0 and lo(r1['iiiL']) >= hi(r1['iiiR']))
_, _, _, r3 = scen('CL', '2', k='4844900000000')
check('C_Lambda = 2: condition (i) fails at k = 4.8449e12  [interval]', hi(r3['Psi']) < lo(r3['tgt']),
      'bar Psi - target = ' + mid(r3['Psi'] - r3['tgt']))
_, _, _, r2 = scen('CL', '2', k='4845000000000')
check('C_Lambda = 2: conditions (i)-(iii) hold at k0 = 4.845e12  [interval]',
      lo(r2['Psi']) >= hi(r2['tgt']) and lo(r2['D1']) > 0 and lo(r2['iiiL']) >= hi(r2['iiiR']),
      'bar Psi - target = ' + mid(r2['Psi'] - r2['tgt']))
check('C_Lambda = 2: (C7) at k = 4.845e12  [exact]', F(PS[2]) + 1 <= (1 - F(PS[3])) * (F('4845000000000') / 2 - 3))
kx = bisect_mp(lambda kk: -margin_mp('CL', '2', k=nstr(kk, 45)), '4620000000000', '4845000000000')
check('C_Lambda = 2: recomputed crossing point %s lies in (4.8449e12, 4.845e12]; displayed as 4.8449...e12 and '
      'rounded up to 4.845e12' % nstr(kx, 12), F('4844900000000') < frac_mp(kx) <= F('4845000000000'))
# Theorem A13: relative margin
S13 = MAIN['A13']
_, _, d13, r13 = both(S13['par'], '13', k=S13['k0'], cs='0.1')
disp('Theorem A13: relative margin (B_crit - bar B)/bar B', 'tr', (r13['Bcrit'] - d13['B']) / d13['B'], '1.7385e-5')

# Section 12.6 and Section 1: the least threshold k_* for the fixed parameters (pi*, resp. pi*_13)
KSTAR = [  # (theorem, parameters, K, k0, least integer k with (C7), floor(k_*), displayed truncation of k_*,
           #  truncation of k0/k_* - 1, bound for it stated in Section 1, k_* to five significant digits (Section 1))
    ('Theorem A', MAIN['A']['par'], '9', '4620000000000', 84216488464, 4616673963026, '4.616673e12', '7.20e-4', '7.3e-4',
     '4.6167e12'),
    ('Theorem A13', MAIN['A13']['par'], '13', '21700000000000', 120000600012, 21695977343082, '2.169597e13', '1.85e-4', None,
     '2.1696e13'),
]
for name, par, Kset, k0s, kc7, n, s_k, s_rel, s_rel1, s_5 in KSTAR:
    c0_, c1_, y0_, e_, w_ = [F(v) for v in par]
    check('Section 12.6, %s: the least integer k with (C7) is %d  [exact]' % (name, kc7),
          y0_ + 1 <= (1 - e_) * (F(kc7) / 2 - 3) and not (y0_ + 1 <= (1 - e_) * (F(kc7 - 1) / 2 - 3)))
    _, _, _, rc = both(par, Kset, k=str(kc7), cs='0.1')
    check('Section 12.6, %s: (ii) D_1 > 0 and (iii) hold at k = %d, so bar Psi(k) - 0.1 k^(1/4) increases wherever (C7) '
          'holds  [interval]' % (name, kc7), lo(rc['D1']) > 0 and lo(rc['iiiL']) >= hi(rc['iiiR']) and lo(rc['mono']) > 0)
    _, _, _, ra = both(par, Kset, k=str(n), cs='0.1')
    _, _, _, rb = both(par, Kset, k=str(n + 1), cs='0.1')
    check('Section 12.6, %s: condition (i) fails at k = %d and holds at k = %d, so %d < k_* <= %d  [interval]'
          % (name, n, n + 1, n, n + 1), hi(ra['Psi']) < lo(ra['tgt']) and lo(rb['Psi']) >= hi(rb['tgt']),
          'bar Psi - target at k = %d: %s' % (n + 1, mid(rb['Psi'] - rb['tgt'])))
    kx = bisect_mp(lambda kk: -(both(par, Kset, k=nstr(kk, 45), cs='0.1')[1]['Psi'] - both(par, Kset, k=nstr(kk, 45), cs='0.1')[1]['tgt']),
                   str(n), str(n + 1), steps=60)
    check('Section 12.6, %s: k_* = %s... (truncated) and %s < k_* <= %s; recomputed by bisection: %s  [exact]'
          % (name, s_k, n, n + 1, nstr(kx, 20)),
          F(s_k) <= n and n + 1 < F(s_k) + unit_of(s_k) and F(n) < frac_mp(kx) <= F(n + 1))
    lo_rel, hi_rel = F(k0s) / (n + 1) - 1, F(k0s) / n - 1          # k_* in (n, n+1]
    check('Section 12.6, %s: k0/k_* - 1 = %s... (truncated)  [exact]' % (name, s_rel),
          F(s_rel) <= lo_rel and hi_rel < F(s_rel) + unit_of(s_rel))
    if s_rel1:
        check('Section 1: k0/k_* - 1 < %s  [exact]' % s_rel1, hi_rel < F(s_rel1))
    check('Section 1 and Section 12.6, %s: k0 = %s is k_* rounded up to three significant digits  [exact]' % (name, k0s),
          F(k0s) - 10 ** (len(k0s) - 3) < n and n + 1 <= F(k0s))
    check('Section 1, %s: k_* is about %s (rounded to five significant digits)  [exact]' % (name, s_5),
          abs(F(n) - F(s_5)) <= unit_of(s_5) / 2 and abs(F(n + 1) - F(s_5)) <= unit_of(s_5) / 2)

# ============================================================================================================
# cross-checks of three closed forms of Section 10 by quadrature (not used in any proof)
# ============================================================================================================
head('Section 10: cross-checks of closed forms by quadrature (not used in the proofs)')
c0, c1, y0, e, w = [mp.mpf(p) for p in PS]
A = mp.mpf(UPPER['9'][0])
dl = mp.mpf('1e-5')
Lg = mp.log(y0)
gam = 2 * mp.mpf('0.50001') * mp.quad(lambda t: (A * c1 * mp.exp(-mp.mpf(3) / 2 * t) + c1 ** 2 / dl *
                                                 mp.exp(-mp.mpf(9) / 4 * t)) * mp.exp(t),
                                      [Lg, Lg + 10, Lg + 40, Lg + 200])
gam += 2 * mp.mpf('0.50001') * (A * c1 * 2 * mp.exp(-(Lg + 200) / 2) + c1 ** 2 / dl * mp.mpf(4) / 5 *
                                mp.exp(-mp.mpf(5) / 4 * (Lg + 200)))
check('Lemma 10.5: 1.00002 int_{y0}^inf (A c1 y^(-3/2) + c1^2/delta y^(-9/4)) dy = Gamma  (relative 1e-20)',
      abs(gam / dm['Gp'] - 1) < mp.mpf('1e-20'), 'quadrature ' + nstr(gam, 15))
y1 = mp.mpf(K0) / 2 - 3
omq = mp.quad(lambda t: 2 * (mp.exp(t) + 2) * mp.tan(c0 * mp.exp(-t / 2)) * c0 / 2 * mp.exp(-mp.mpf(3) / 2 * t)
              * mp.exp(t), [Lg, Lg + 1, mp.log(y1)])
check('Step 11: Omega_W (quadrature) <= its bound in Theorem 10.3 at pi*, k0', omq <= rm['Omb'],
      nstr(omq, 12) + ' <= ' + nstr(rm['Omb'], 12))
for yy in (y0, 10 * y0, (1 - e) * y1):
    J = mp.quad(lambda s: (1 - e) ** (mp.mpf(3) / 4) * s ** (-mp.mpf(3) / 4) / (e * s + mp.mpf('2.0002')),
                [yy, yy / (1 - e)])
    check('Step 10: (1-eps)^(3/4) int_y^(y/(1-eps)) s^(-3/4)/(eps s + b_W) ds >= invF y^(-3/4) at y = %s'
          % nstr(yy, 8), J >= dm['invF'] * yy ** (-mp.mpf(3) / 4),
          'ratio ' + nstr(J / (dm['invF'] * yy ** (-mp.mpf(3) / 4)), 12))

# ============================================================================================================
# consistency of Section 3 with Sections 11 and 12
# ============================================================================================================
head('Section 3 and Sections 11-12: the same parameter vectors')
check('Section 3: pi* and pi*_13 (display before Definition 3.2) are the vectors of Table tab:const-main (Section 12.3)',
      PI3['A'] == MAIN['A']['par'] and PI3['A13'] == MAIN['A13']['par'])

finish()
