"""Shape-lemma parametrization from the refined roots: t_i = g_i(S) / p'(S) at every root S of p.

    ../env.sh python3 param.py BITS POLY.json OUT.json work/n29_ref133k_*.txt work/n29_q4_ref.txt

g_i = lc(p) * sum_j t_ij prod_{k != j} (x - S_k) (product tree over all roots, conjugates added back), so that
g_i(S_j) = t_ij p'(S_j).  Its coefficients are recognised as rationals (common denominator by LLL on the top ones,
then continued fractions down the list, as in reconstruct.py) and checked to be within far less than the working
precision of the recognised values.
"""
import json, math, sys, time
sys.set_int_max_str_digits(0)
from fractions import Fraction
import flint
from flint import acb, arb, acb_poly, fmpz_mat

bits, polyf, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
files = sys.argv[4:]
flint.ctx.prec = bits + 64
digits = int(bits * math.log10(2))
pc = [int(c) for c in json.load(open(polyf))['coeffs_ascending']]
lc = pc[-1]
S, T = [], []
for fn in files:
    for l in open(fn):
        f = l.split()
        s = acb(arb(f[2]), arb(f[3]))
        ts = [acb(arb(f[4 + 2 * i]), arb(f[5 + 2 * i])) for i in range((len(f) - 4) // 2)]
        if max(abs(float(x)) for x in f[3::2]) < 1e-30:            # real root: S and all t real
            S.append(acb(s.real)); T.append([acb(t.real) for t in ts])
        else:
            S += [s, s.conjugate()]; T += [ts, [t.conjugate() for t in ts]]
n = len(S)
COLS = [int(c) for c in __import__('os').environ.get('COLS', ','.join(str(i + 1) for i in range(len(T[0])))).split(',')]
T = [[row[c - 1] for c in COLS] for row in T]
k = len(COLS)
print(f'{n} roots, {k} coordinates; working digits {digits}', flush=True)
assert n == len(pc) - 1, (n, len(pc) - 1)


def tree(lo, hi):
    if hi - lo == 1:
        return acb_poly([-S[lo], 1]), [acb_poly([T[lo][i]]) for i in range(k)]
    mid = (lo + hi) // 2
    PL, NL = tree(lo, mid)
    PR, NR = tree(mid, hi)
    return PL * PR, [NL[i] * PR + NR[i] * PL for i in range(k)]


t0 = time.time()
P, N = tree(0, n)
print(f'product tree in {time.time() - t0:.0f} s', flush=True)
# sanity: lc * P should be p
dev = max(float(abs(P[j] * lc - pc[j]).mid().log()) / math.log(10) if (P[j] * lc - pc[j]).mid() != 0 else -1e9
          for j in range(0, n + 1, max(1, n // 50)))
print(f'max log10 |lc*P - p| over sampled coefficients: {dev:.0f}', flush=True)


def exact(a):
    m, e = a.mid().man_exp()
    m, e = int(m), int(e)
    return Fraction(m * 2 ** e) if e >= 0 else Fraction(m, 2 ** -e)


def flog10(x):
    x = abs(x)
    if x == 0:
        return -1e9
    a, b = x.numerator, x.denominator
    sa, sb = max(0, a.bit_length() - 60), max(0, b.bit_length() - 60)
    return math.log10(a >> sa) - math.log10(b >> sb) + (sa - sb) * math.log10(2)


def recognise(E):
    """Common denominator D with D*E[j] integral (to far below working precision) for all j, or None."""
    D = 1
    for j in range(len(E) - 1, -1, -1):
        y = E[j] * D
        size = max(0.0, flog10(y))
        qmax = 10 ** max(1, int((digits - size - 200) / 2))
        D *= y.limit_denominator(qmax).denominator
    ints, err = [], -1e9
    for e in E:
        y = e * D
        r = round(y)
        ints.append(int(r))
        err = max(err, flog10(y - r))
    return D, ints, err


res = {'degree': n, 'g': []}
for i in range(k):
    E = [exact((N[i][j] * lc).real) for j in range(n)]
    imag = max(float(abs(N[i][j].imag).mid().log()) / math.log(10) if N[i][j].imag.mid() != 0 else -1e9
               for j in range(0, n, max(1, n // 50)))
    D, ints, err = recognise(E)
    h = max(len(str(abs(c))) for c in ints)
    print(f't{COLS[i]}: g degree {n - 1}, denominator {len(str(D))} digits, numerator height {h} digits, '
          f'max distance to integers 1e{err:.0f}; max log10 |imag| {imag:.0f}', flush=True)
    res['g'].append({'coord': COLS[i], 'den': str(D), 'num_ascending': [str(c) for c in ints], 'int_err_log10': err})
json.dump(res, open(out, 'w'))
print('wrote', out)
