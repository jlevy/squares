"""Exact-rational interval re-derivation of Table 1 of the paper, written independently of check_table_iv.py.

Part 1 checks that the rounded constants of Section 2.1 are upper bounds of the exact ones; Part 2 checks conditions
(i)-(iv) of Proposition 6.1 for the eight cases of Table 1; Part 3 is a floating-point sanity sweep (not part of the
proof) and computes c_infinity.

Arithmetic: closed intervals with fractions.Fraction endpoints. Irrational inputs are enclosed rigorously:
  * x^(1/q) for rational x>0: integer q-th roots of scaled integers (lo^q <= x <= hi^q exactly checked);
  * cos, sin of small rational x (0 <= x <= 1e-3): alternating Taylor bounds
        1 - x^2/2 <= cos x <= 1 - x^2/2 + x^4/24,   x - x^3/6 <= sin x <= x;
  * pi: 3.14159265358979323 < pi < 3.14159265358979324 (known digits).
Theorem 5.1 of the paper:  (1-2 t0)(k-6) <= W/n0 + A W/(2 b) + b (k/2-1) Ltot/(1-n0-E*),
   Ltot = A' W max(1/bb, B1 W/(2 t1)) + L1 W + 4 d,  E* = 0.50001 b (A + b/d) W,  b = line threshold beta.
Usage: python check_table_exact.py  (Part 3 needs mpmath). Writes check_table_exact.out.txt.
"""
from fractions import Fraction as Fr
import math
import sys

OUT = []


def say(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    OUT.append(s)


class Iv:
    """closed interval [lo, hi] of rationals"""

    def __init__(self, lo, hi=None):
        lo = Fr(lo)
        hi = lo if hi is None else Fr(hi)
        assert lo <= hi, (lo, hi)
        self.lo, self.hi = lo, hi

    @staticmethod
    def c(x):
        return x if isinstance(x, Iv) else Iv(x)

    def __add__(self, o):
        o = Iv.c(o); return Iv(self.lo + o.lo, self.hi + o.hi)
    __radd__ = __add__

    def __sub__(self, o):
        o = Iv.c(o); return Iv(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, o):
        return Iv.c(o) - self

    def __mul__(self, o):
        o = Iv.c(o)
        p = [self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi]
        return Iv(min(p), max(p))
    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Iv.c(o)
        assert o.lo > 0 or o.hi < 0, 'division by interval containing 0'
        return self * Iv(1 / o.hi, 1 / o.lo)

    def __rtruediv__(self, o):
        return Iv.c(o) / self

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def f(self, n=10):
        return '[%s, %s]' % (fmt(self.lo, n), fmt(self.hi, n))


def imax(a, b):
    a, b = Iv.c(a), Iv.c(b)
    return Iv(max(a.lo, b.lo), max(a.hi, b.hi))


def fmt(x, n=10):
    return '%.*g' % (n, float(x)) if abs(float(x)) < 1e300 else str(x)


def iroot(n, q):
    """floor(n^(1/q)) for integer n >= 0"""
    if n < 2:
        return n
    # start from a guaranteed over-estimate, then integer Newton decreases monotonically to floor(n^(1/q))
    x = 1 << ((n.bit_length() + q - 1) // q)
    while x ** q <= n:
        x <<= 1
    while True:
        y = ((q - 1) * x + n // x ** (q - 1)) // q
        if y >= x:
            break
        x = y
    while x ** q > n:          # safety (at most a step)
        x -= 1
    while (x + 1) ** q <= n:   # safety (at most a step)
        x += 1
    return x


def root(x, q, digits=45):
    """rigorous enclosure of x^(1/q), x rational > 0"""
    x = Fr(x)
    M = 10 ** digits
    n = (x.numerator * M ** q) // x.denominator
    m = iroot(n, q)
    lo, hi = Fr(m, M), Fr(m + 1, M)
    assert lo ** q <= x <= hi ** q
    return Iv(lo, hi)


def cos_small(x):
    x = Fr(x); assert 0 <= x <= Fr(1, 1000)
    return Iv(1 - x * x / 2, 1 - x * x / 2 + x ** 4 / 24)


def sin_small(x):
    x = Fr(x); assert 0 <= x <= Fr(1, 1000)
    return Iv(x - x ** 3 / 6, x)


PI = Iv(Fr('3.14159265358979323'), Fr('3.14159265358979324'))
D = Fr('1e-5')        # delta
BB = Fr('1.5e-6')     # beta-bar

# ---------------------------------------------------------------------------------------------------------
# Part 1: the imported constants (rounded values used in the paper) are upper bounds of the exact ones.
# ---------------------------------------------------------------------------------------------------------
ROUND = {9: dict(A='10.6067', Ap='10.6068', S='56.2501', CM='318.20', CG='56.2501', CE='754.8'),
         13: dict(A='12.7476', Ap='12.7476', S='81.2502', CM='459.7', CG='81.26', CE='1090.3')}
EXACT = {}
allok = True
say('== Part 1: exact constants vs. the rounded-up values of Section 2.1 of the paper ==')
for K in (9, 13):
    A = 4 * root(Fr(K) / Fr('0.32'), 2) / (2 - Fr('3e-6'))                  # [R] 4.13 / [Q] Rem. 2.2
    Ap = A / cos_small(BB) + Fr('1e-8')                                       # [Q] Def. 3.4, Thm 8.3
    S = Iv((1 + Fr('1e-11')) * Fr(4 * K) / (Fr('0.32') * (2 - Fr('3e-6'))))   # [Q] Thm 7.1 S_K (exact)
    # [Q] Thm 7.1(M): 4/cos(pi/4+a) S_K, a <= bb; cos(pi/4+a) = (cos a - sin a)/sqrt2 is decreasing in a
    cpa = (cos_small(BB) - sin_small(BB)) / root(2, 2)
    CM = 4 / cpa * S
    CG = S / cos_small(BB)                                                    # [Q] Thm 7.1(G)
    # [Q] Prop 5.10: c_E = 41.933 must dominate 40/((pi/4)(2-pi/4)) and 40 tan(pi/4+bb)/((pi/4-bb)(2-pi/4+bb))
    r1 = 40 / ((PI / 4) * (2 - PI / 4))
    tanb = sin_small(BB) / cos_small(BB)
    r2 = 40 * ((1 + tanb) / (1 - tanb)) / ((PI / 4 - BB) * (2 - PI / 4 + BB))
    cE = Fr('41.933')
    CE = 2 * cE * K
    EXACT[K] = dict(A=A, Ap=Ap, S=S, CM=CM, CG=CG, CE=CE)
    R = {k: Fr(v) for k, v in ROUND[K].items()}
    checks = [('A', A.hi < R['A']), ("A'", Ap.hi < R['Ap']), ('S_K', S.hi <= R['S']), ('C_M', CM.hi <= R['CM']),
              ('C_G', CG.hi <= R['CG']), ('c_E ratio 1', r1.hi <= cE), ('c_E ratio 2', r2.hi <= cE),
              ('C_E', CE <= R['CE'])]
    for name, ok in checks:
        allok &= ok
    say(f'[K={K}] A in {A.f(12)}  A\' in {Ap.f(12)}  S_K in {S.f(12)}')
    say(f'       C_M <= {fmt(CM.hi, 10)} (used {ROUND[K]["CM"]}),  C_G <= {fmt(CG.hi, 10)} (used {ROUND[K]["CG"]}),'
        f'  ratios {fmt(r1.hi, 9)}, {fmt(r2.hi, 9)} <= 41.933,  C_E = {fmt(CE, 9)} (used {ROUND[K]["CE"]})')
    say('       all upper bounds OK' if all(ok for _, ok in checks) else '       FAILED: ' + str(checks))


def derived(K):
    R = {k: Fr(v) for k, v in ROUND[K].items()}
    B1 = (R['A'] / 2 + 2 * BB) / cos_small(BB)
    L1 = (1 + R['S'] * D * D) / D + (R['CM'] + R['CE'] + R['CG']) * D + 4 * B1
    return R, B1, L1


for K in (9, 13):
    R, B1, L1 = derived(K)
    say(f'[K={K}] B1 in {B1.f(13)}  L1 in {L1.f(13)}')
    allok &= B1.hi <= (Fr('5.3033531') if K == 9 else Fr('6.3738031'))
    allok &= L1.hi <= (Fr('100021.23') if K == 9 else Fr('100025.52'))

# ---------------------------------------------------------------------------------------------------------
# Part 2: the 8 cases of Table 1, evaluated at k = ka with rigorous rational intervals.
# ---------------------------------------------------------------------------------------------------------
CASES = [  # K, p, c, b, ka, kb, tau0, tau1, nu0
    (9, 2, '1.0e-4', '1.2e-3', '1e8', '2.5e15', '0.0205', '0.02', '0.001'),
    (9, 2, '7.0e-5', '1.2e-3', '2.5e15', '3.5e17', '0.1675', '0.167', '0.001'),
    (9, 3, '0.06', '1.0', '3.5e17', None, '0.1675', '0.167', '0.01'),
    (9, 3, '0.0625', '1.0', '1e21', None, '0.1668', '0.1667', '0.005'),
    (13, 2, '8.5e-5', '1.2e-3', '1e8', '2.4e15', '0.0205', '0.02', '0.001'),
    (13, 2, '6.0e-5', '1.2e-3', '2.4e15', '3.39e17', '0.1675', '0.167', '0.001'),
    (13, 3, '0.05', '1.0', '3.39e17', None, '0.1675', '0.167', '0.01'),
    (13, 3, '0.052', '1.0', '1e21', None, '0.1668', '0.1667', '0.005'),
]


def evaluate(K, q, c, b, k, t0, t1, n0):
    """returns dict of intervals at integer/rational k; q = 2 (p=1/2) or 3 (p=1/3)."""
    R, B1, L1 = derived(K)
    A, Ap = R['A'], R['Ap']
    kp = root(k, q)                 # k^p
    W = c * kp
    beta = b * kp / k               # b k^(p-1)
    Es = Fr('0.50001') * beta * (A + beta / D) * W
    mx = imax(Iv(1 / BB), B1 * W / (2 * t1))
    Ltot = Ap * W * mx + L1 * W + 4 * D
    rhs = W / n0 + A * W / (2 * beta) + beta * (Fr(k) / 2) * Ltot / (1 - n0 - Es)
    rhs_exact_h = W / n0 + A * W / (2 * beta) + beta * (Fr(k) / 2 - 1) * Ltot / (1 - n0 - Es)
    lhs = Iv((1 - 2 * t0) * (Fr(k) - 6))
    return dict(W=W, beta=beta, Es=Es, mx=mx, Ltot=Ltot, rhs=rhs, rhs_h=rhs_exact_h, lhs=lhs, B1=B1)


say('')
say('== Part 2: the 8 cases of Table 1 at k = ka (exact rational intervals) ==')
res = []
for (K, q, c, b, ka, kb, t0, t1, n0) in CASES:
    c, b, t0, t1, n0 = map(Fr, (c, b, t0, t1, n0))
    ka_ = Fr(ka)
    assert ka_.denominator == 1
    v = evaluate(K, q, c, b, ka_, t0, t1, n0)
    par = D < t1 < t0 < Fr(1, 2) and 0 < n0 < Fr(1, 2)
    okb = v['beta'].hi <= BB
    okq = (t0 - Fr('1.0001') * v['beta']).lo > t1
    oke = v['Es'].hi < 1 - n0
    okm = v['lhs'].lo > v['rhs'].hi
    okbr = True
    brs = ''
    if q == 2:
        W1 = 2 * t1 / (v['B1'] * BB)
        top = c * root(Fr(kb), 2)
        okbr = top.hi <= W1.lo
        brs = f'  branch: c*sqrt(kb) <= {fmt(top.hi, 9)} vs W1 >= {fmt(W1.lo, 9)} (slack {fmt(W1.lo - top.hi, 4)})'
    ok = par and okb and okq and oke and okm and okbr and ka_ >= 14
    res.append(ok)
    marg = (v['lhs'].lo - v['rhs'].hi) / ka_
    say(f"{'PASS' if ok else 'FAIL'} K={K} p=1/{q} W > {fmt(c, 6)} k^(1/{q}) on [{ka}, {kb or 'inf'}]"
        f"  (t0={t0}, t1={t1}, n0={n0}, b={fmt(b, 4)})")
    say(f"     LHS/k >= {fmt(v['lhs'].lo / ka_, 9)}, RHS+/k <= {fmt(v['rhs'].hi / ka_, 9)}, margin/k >= {fmt(marg, 6)}"
        f" (rel {fmt(marg / (v['lhs'].lo / ka_), 4)}); beta={fmt(v['beta'].hi, 5)}, E*<={fmt(v['Es'].hi, 4)},"
        f" W={fmt(v['W'].lo, 8)}, theta-branch max={'1/bb' if v['mx'].lo == 1 / BB else 'B1W/2t1'}{brs}")
say('PART 2: ALL 8 PASS' if all(res) else 'PART 2: SOME FAILED')
allok &= all(res)

# ---------------------------------------------------------------------------------------------------------
# Part 3: sanity (not a proof) -- monotonicity of RHS+(k)/k and positivity of the margin on a log grid,
# and the limit of RHS+/k for p=1/3; also c_infinity.
# ---------------------------------------------------------------------------------------------------------
from mpmath import mp, mpf, log10, cbrt, sqrt, cos
mp.dps = 50


def rhs_over_k(K, q, c, b, k, t0, t1, n0):
    R, B1, L1 = derived(K)
    A, Ap, B1, L1 = mpf(R['A']), mpf(R['Ap']), mpf(B1.hi), mpf(L1.hi)
    k = mpf(k); kp = k ** (mpf(1) / q)
    W = c * kp; beta = b * kp / k
    Es = mpf('0.50001') * beta * (A + beta / mpf(D)) * W
    mx = max(1 / mpf(BB), B1 * W / (2 * t1))
    Ltot = Ap * W * mx + L1 * W + 4 * mpf(D)
    rhs = W / n0 + A * W / (2 * beta) + beta * (k / 2) * Ltot / (1 - n0 - Es)
    return rhs / k, (1 - 2 * t0) * (1 - 6 / k), Es


say('')
say('== Part 3: sanity sweeps (floating point, 50 digits; not part of the proof) ==')
for (K, q, c, b, ka, kb, t0, t1, n0) in CASES:
    c, b, t0, t1, n0 = map(mpf, (c, b, t0, t1, n0))
    lo = float(log10(mpf(ka)))
    hi = float(log10(mpf(kb))) if kb else 40.0
    prev = None
    mono = True
    worst = mpf(10)
    for i in range(0, 401):
        e = lo + (hi - lo) * i / 400
        r, l, Es = rhs_over_k(K, q, c, b, mpf(10) ** e, t0, t1, n0)
        if prev is not None and r > prev * (1 + mpf('1e-30')):
            mono = False
        prev = r
        worst = min(worst, l - r)
    lim = ''
    if q == 3:
        R, B1, L1 = derived(K)
        A, Ap, B1f = mpf(R['A']), mpf(R['Ap']), mpf(B1.hi)
        limv = A * c / (2 * b) + b * c * c * Ap * B1f / (4 * t1 * (1 - n0))
        lim = f', RHS+/k -> {mp.nstr(limv, 8)} vs LHS/k -> {mp.nstr(1 - 2 * t0, 6)}'
    say(f'K={K} p=1/{q} c={mp.nstr(c, 4)}: RHS+/k non-increasing on grid: {mono}; min(LHS/k-RHS+/k) on grid = '
        f'{mp.nstr(worst, 6)}{lim}')

for K in (9, 13):
    R, B1, L1 = derived(K)
    Ar, Apr, B1r = mpf(R['A']), mpf(R['Ap']), mpf(B1.hi)
    Ae = 4 * sqrt(mpf(K) / mpf('0.32')) / (2 - mpf('3e-6'))
    Ape = Ae / cos(mpf('1.5e-6')) + mpf('1e-8')
    B1e = (Ae / 2 + 2 * mpf('1.5e-6')) / cos(mpf('1.5e-6'))
    cinf_r = cbrt((mpf(4) / 27) / (Ar * Apr * B1r))
    cinf_e = cbrt((mpf(4) / 27) / (Ae * Ape * B1e))
    cinf_0 = cbrt((mpf(4) / 27) / (Ae * Ape * Ae / 2))     # theta -> 0 limit of B1
    say(f'[K={K}] c_inf with rounded A,A\',B1: {mp.nstr(cinf_r, 10)};  exact: {mp.nstr(cinf_e, 10)};'
        f'  exact with B1 -> A/2: {mp.nstr(cinf_0, 10)}')

say('')
say('OVERALL: ' + ('OK' if allok else 'SOMETHING FAILED'))
with open(__file__.replace('.py', '.out.txt'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(OUT) + '\n')
sys.exit(0 if allok else 1)
