"""Rebuild the polynomial prod (x - S_j) over the refined genuine solutions and recognise its rational coefficients.

    ../env.sh python3 reconstruct.py BITS OUT.json work/n29_ref_*.txt

Conjugate partners of the refined representatives are added back.  Coefficients of the monic product are recognised
by continued fractions (the common denominator is the leading coefficient); then all of them must be integers to a
margin far below the working precision.  Irreducibility: degree patterns of the factorisation mod small primes.
"""
import json, math, sys, time
sys.set_int_max_str_digits(0)
from fractions import Fraction
import flint
from flint import acb, arb, acb_poly, fmpz_poly, nmod_poly

bits = int(sys.argv[1]); out = sys.argv[2]; files = sys.argv[3:]
flint.ctx.prec = bits + 64
digits = int(bits * math.log10(2))
roots, nreal, worst = [], 0, -1e9
for fn in files:
    for l in open(fn):
        f = l.split()
        worst = max(worst, float(f[1]))
        col = int(__import__('os').environ.get('COL', '0'))     # 0: S; i >= 1: t_i
        s = acb(arb(f[2 + 2 * col]), arb(f[3 + 2 * col]))
        ts_im = [float(x) for x in f[5::2]]
        if max(abs(x) for x in ts_im) < 1e-30:
            roots.append(acb(s.real)); nreal += 1
        else:
            roots += [s, s.conjugate()]
print(f'{len(roots)} roots ({nreal} real); worst log10 residual {worst:.0f}; working digits {digits}', flush=True)
t0 = time.time()
P = acb_poly.from_roots(roots)
n = P.degree()
print(f'product polynomial degree {n} ({time.time() - t0:.0f} s)', flush=True)
co = [P[k] for k in range(n + 1)]
maxim = max(float(abs(c.imag).mid().log()) if c.imag != 0 else -1e9 for c in co) / math.log(10)
print(f'max log10 |imag part| of coefficients: {maxim:.0f}', flush=True)


def flog10(x):                     # log10 |x| for a nonzero Fraction, without float overflow/underflow
    x = abs(x)
    a, b = x.numerator, x.denominator
    sa, sb = max(0, a.bit_length() - 60), max(0, b.bit_length() - 60)
    return math.log10(a >> sa) - math.log10(b >> sb) + (sa - sb) * math.log10(2)


def exact(a):                       # midpoint of an arb as a Fraction
    m, e = a.mid().man_exp()
    m, e = int(m), int(e)
    return Fraction(m * 2 ** e) if e >= 0 else Fraction(m, 2 ** -e)


E = [exact(c.real) for c in co]     # monic: E[n] = 1


def lll_denominator(vals, digits, m=8):
    """Common denominator D of the top m monic coefficients by simultaneous approximation (LLL): works for
    log10 D < about (digits - size) m / (m + 1), against digits / 2 for continued fractions on one coefficient."""
    from flint import fmpz_mat
    size = max(max(0.0, flog10(v)) if v else 0.0 for v in vals)
    C = 10 ** int(digits - size - 20)
    rows = [[1] + [round(v * C) for v in vals]]
    for i in range(len(vals)):
        rows.append([0] * (i + 1) + [C] + [0] * (len(vals) - i - 1))
    B = fmpz_mat(rows).lll()
    best = None
    for i in range(B.nrows()):
        d = abs(int(B[i, 0]))
        if d == 0:
            continue
        e = max(flog10(v * d - round(v * d)) if v * d != round(v * d) else -1e9 for v in vals)
        if best is None or e < best[1]:
            best = (d, e)
    return best


t0 = time.time()
D, e0 = lll_denominator([E[k] for k in range(n - 1, n - 9, -1)], digits)
print(f'LLL common denominator of the top 8 coefficients: {len(str(D))} digits, max distance to integers 1e{e0:.0f} '
      f'({time.time() - t0:.0f} s)', flush=True)
if e0 > -40:
    D = 1
for k in range(n - 1, -1, -1):
    y = E[k] * D
    size = max(0.0, flog10(y)) if y else 0.0
    qmax = 10 ** max(1, int((digits - size - 200) / 2))
    q = y.limit_denominator(qmax)
    D *= q.denominator
ints, err = [], -1e9
for k in range(n + 1):
    y = E[k] * D
    r = round(y)
    ints.append(int(r))
    d = abs(y - r)
    err = max(err, flog10(d) if d else -1e9)
from math import gcd
g = 0
for c in ints:
    g = gcd(g, c)
ints = [c // g for c in ints]
h = max(len(str(abs(c))) for c in ints)
print(f'leading coefficient: {len(str(ints[-1]))} digits; height {h} digits; max distance to integers 1e{err:.0f}',
      flush=True)
ok = err < -(100)
f = fmpz_poly(ints)
# irreducibility via degree patterns mod p
possible = (1 << (n + 1)) - 1 if False else None
pats = []
p = 1000003
cnt = 0
while cnt < 25:
    p += 2
    while not flint.fmpz(p).is_prime():
        p += 2
    if ints[-1] % p == 0:
        continue
    fp = nmod_poly(ints, p)
    if fp.gcd(fp.derivative()).degree() > 0:
        continue
    degs = sorted(fac.degree() for fac, _ in fp.factor()[1])
    pats.append(degs)
    sums = 1
    for d in degs:
        sums |= sums << d
    possible = sums if possible is None else possible & sums
    cnt += 1
    if possible == (1 | (1 << n)):
        break
cand = [d for d in range(1, n) if possible >> d & 1]
print(f'{cnt} primes: possible proper factor degrees {cand[:20]}{"..." if len(cand) > 20 else ""}', flush=True)
json.dump({'degree': n, 'roots_real': nreal, 'height_digits': h, 'int_err_log10': err, 'recognised': ok,
           'irreducible_by_patterns': not cand, 'possible_factor_degrees': cand[:200],
           'patterns_first': pats[:3], 'coeffs_ascending': [str(c) for c in ints]}, open(out, 'w'))
print('wrote', out)
