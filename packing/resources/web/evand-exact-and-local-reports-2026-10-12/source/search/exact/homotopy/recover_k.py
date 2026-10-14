"""Recover a rational polynomial f = D * P * Q when k roots are missing from the refined root set.

    ../env.sh python3 recover_k.py BITS K1,K2,.. OUT_PREFIX work/n29_ref_*.txt

P = prod (x - S_j) over the known roots (conjugates added back, as in reconstruct.py); Q is monic of degree K, unknown.
The top K+1 coefficients a_0..a_K of f (integers) determine D*Q, hence every other coefficient of f, linearly:
f[N-i] = sum_l M[i][l] a_l.  LLL finds integers a making the next M coefficients integral too; then all coefficients
are checked for integrality, and the roots of Q are the missing roots.  Works while about (K+1) * log10|a| is below
digits * M / (M + K + 1).
"""
import json, math, sys, time
sys.set_int_max_str_digits(0)
import flint
from flint import acb, arb, acb_poly, fmpz_mat, fmpz_poly, arb_poly

bits, Ks, outp = int(sys.argv[1]), [int(x) for x in sys.argv[2].split(',')], sys.argv[3]
files = sys.argv[4:]
flint.ctx.prec = bits + 64
digits = int(bits * math.log10(2))
roots = []
for fn in files:
    for l in open(fn):
        f = l.split()
        col = int(__import__('os').environ.get('COL', '0'))
        s = acb(arb(f[2 + 2 * col]), arb(f[3 + 2 * col]))
        if max(abs(float(x)) for x in f[5::2]) < 1e-30:
            roots.append(acb(s.real))
        else:
            roots += [s, s.conjugate()]
t0 = time.time()
P = acb_poly.from_roots(roots)
n0 = P.degree()
p = [P[i].real for i in range(n0 + 1)]                       # real parts; imaginary parts are rounding noise
print(f'{n0} known roots; product in {time.time() - t0:.0f} s', flush=True)


def dist(c):                                                   # log10 distance of an arb midpoint to the nearest integer
    m, e = c.mid().man_exp()
    m, e = int(m), int(e)
    v = m << e if e >= 0 else (m + (1 << (-e - 1))) >> -e
    d = abs(c - v).mid()
    return float(d.log()) / math.log(10) if d != 0 else -1e9


def solve(K):
    M = int(__import__("os").environ.get("MM", max(12, 2 * K)))
    N = n0 + K


    def coeffs(a):
        """f[N-i] for i = 0..K+M given the top coefficients a (arb or ints)."""
        g = [None] * (K + 1)                                       # g[K-i] = (D*Q) coefficient
        for i in range(K + 1):
            v = arb(a[i])
            for j in range(i):
                v -= p[n0 - (i - j)] * g[K - j]
            g[K - i] = v
        res = []
        for i in range(K + M + 21):
            v = arb(0)
            for j in range(0, min(i, K) + 1):
                if n0 - (i - j) >= 0:
                    v += p[n0 - (i - j)] * g[K - j]
            res.append(v)
        return res, g


    cols = []                                                     # cols[l] = f[N-i] for i = K+1..K+M, from a = e_l
    for l in range(K + 1):
        e = [0] * (K + 1); e[l] = 1
        cols.append(coeffs(e)[0][K + 1:])
    size = max(float(abs(c.mid()).log()) / math.log(10) if c.mid() != 0 else 0 for col in cols for c in col)
    C = 10 ** max(1, int(digits - max(0, size) - 30))
    print(f'linear map entries up to 1e{size:.0f}; lattice scale 1e{len(str(C)) - 1}', flush=True)


    def rnd(x):                                                    # round(arb * C) to an int
        m, e = (x * C).mid().man_exp()
        m, e = int(m), int(e)
        return m << e if e >= 0 else m >> -e


    rows = []
    for l in range(K + 1):
        rows.append([1 if j == l else 0 for j in range(K + 1)] + [rnd(c) for c in cols[l][:M]])
    for j in range(M):
        rows.append([0] * (K + 1) + [C if jj == j else 0 for jj in range(M)])
    t0 = time.time()
    B = fmpz_mat(rows).lll()
    print(f'LLL {B.nrows()}x{B.ncols()} in {time.time() - t0:.0f} s', flush=True)
    best = None
    for r in range(B.nrows()):
        a = [int(B[r, j]) for j in range(K + 1)]
        if a[0] == 0:
            continue
        if a[0] < 0:
            a = [-x for x in a]
        fc, g = coeffs(a)
        sz = max(len(str(abs(x))) for x in a)
        ex = max(dist(c) for c in fc[K + M + 1:])                 # coefficients not used by the lattice
        if __import__("os").environ.get("DEBUG"): print(f"  row {r}: |a| {sz} digits, a0 {len(str(a[0]))} digits; log10 dist to Z of f[N-{K+1}..]: {[round(dist(c)) for c in fc[K + 1:]]}", flush=True)
        if __import__("os").environ.get("DEBUG") and sz < 5000: print("    a =", a, "\n    D*Q coeffs (desc) ~", [float(x.mid()) for x in g[::-1]], "\n    Q roots ~", [complex(float(z.real.mid()), float(z.imag.mid())) for z in acb_poly([acb(x) for x in g]).roots()], flush=True)
        if best is None or ex < best[1]:
            best = (a, ex, g, sz)
    a, ex, g, sz = best
    print(f'K={K}: best row: top coefficients up to {sz} digits; held-out coefficients 1e{ex:.0f} from integers', flush=True)
    if ex > -100:
        return False
    # full polynomial: f = P * (D*Q); check all coefficients are integers
    G = acb_poly([acb(x) for x in g])
    F = P * G
    ints, err = [], -1e9
    for i in range(N + 1):
        c = F[i].real
        m, e = c.mid().man_exp()
        m, e = int(m), int(e)
        v = m << e if e >= 0 else (m + (1 << (-e - 1))) >> -e                 # nearest integer
        ints.append(v)
        d = abs(c - v)
        err = max(err, float(d.mid().log()) / math.log(10) if d.mid() != 0 else -1e9)
    print(f'K={K}: leading coefficient {len(str(a[0]))} digits; height {max(len(str(abs(x))) for x in ints)} digits; '
          f'max distance to integers 1e{err:.0f}', flush=True)
    q = acb_poly([acb(x) for x in g])
    missing = [str(complex(float(z.real.mid()), float(z.imag.mid()))) for z in q.roots()] if K > 0 else []
    print('missing roots:', missing, flush=True)
    json.dump({'K': K, 'int_err_log10': err, 'missing': missing, 'coeffs_ascending': [str(c) for c in ints]}, open(f'{outp}_k{K}.json', 'w'))
    return err < -100

for K in Ks:
    t0 = time.time()
    ok = solve(K)
    print(f'K={K}: {"RECOVERED" if ok else "no"} ({time.time() - t0:.0f} s)', flush=True)
    if ok:
        break
