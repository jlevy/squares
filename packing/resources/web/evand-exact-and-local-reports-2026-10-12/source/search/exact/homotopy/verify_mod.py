"""Check the parametrization identities modulo random primes.

    ../env.sh python3 verify_mod.py SYSTEM.jl POLY.json PARAM_t1.json ... PARAM_t5.json NPRIMES SEED

With tau_i = g_i(x) / (den_i p'(x)) in Q[x]/(p): F_k(tau) = 0 for every k, and Sn(tau) - x Sd(tau) = 0.
Each is checked in F_q[x]/(p mod q) for NPRIMES random 62-bit primes q (q not dividing lc(p) or any den_i, p squarefree
mod q).  A false identity is a nonzero element of Q[x]/(p); it reduces to 0 mod q only for primes dividing one fixed
nonzero integer, so random q expose it with overwhelming probability (Monte Carlo, not a deterministic proof).
"""
import json, random, re, sys, time
sys.set_int_max_str_digits(0)
import sympy as sp
from flint import nmod_poly, fmpz

src = open(sys.argv[1]).read()
pc = [int(c) for c in json.load(open(sys.argv[2]))['coeffs_ascending']]
G = {}
for fn in sys.argv[3:8]:
    for g in json.load(open(fn))['g']:
        G[g['coord']] = (int(g['den']), [int(c) for c in g['num_ascending']])
nprimes, seed = int(sys.argv[8]), int(sys.argv[9])
names = re.search(r'@var (.*)', src).group(1).split()
syms = sp.symbols(names)
loc = dict(zip(names, syms))


def jl2sp(s):
    s = re.sub(r'big\((\d+)\)//(\d+)', r'Rational(\1, \2)', s).replace('^', '**')
    return sp.sympify(s, locals={**loc, 'Rational': sp.Rational})


fblock = src.split('F = [', 1)[1].split('\n]', 1)[0]
Fexpr = [jl2sp(x.strip().rstrip(',')) for x in fblock.strip().split('\n') if x.strip()]
Sn = jl2sp(re.search(r'^Sn = (.*)$', src, re.M).group(1))
Sd = jl2sp(re.search(r'^Sd = (.*)$', src, re.M).group(1))


def terms(e):
    P = sp.Poly(sp.expand(e), *syms)
    return [(m, int(c.p), int(c.q)) for m, c in P.terms()]


FT = [terms(f) for f in Fexpr]
ST, DT = terms(Sn), terms(Sd)
maxe = [max(max(m[i] for m, _, _ in T) for T in FT + [ST, DT]) for i in range(len(syms))]
print(f'{len(FT)} polynomials, {sum(len(T) for T in FT)} terms; max degree per variable {maxe}', flush=True)
rng = random.Random(seed)
passed = 0
while passed < nprimes:
    q = rng.randrange(2 ** 61, 2 ** 62) | 1
    while not fmpz(q).is_prime():
        q = rng.randrange(2 ** 61, 2 ** 62) | 1
    if pc[-1] % q == 0 or any(d % q == 0 for d, _ in G.values()):
        continue
    t0 = time.time()
    P = nmod_poly(pc, q)
    dP = P.derivative()
    g, u, _ = dP.xgcd(P)              # u p' + v p = g
    if g.degree() != 0:
        print(f'q={q}: p not squarefree mod q, skipped', flush=True)
        continue
    u = u * pow(int(g[0]), -1, q) % P   # u = 1/p' mod p
    tau = []
    for i in range(len(syms)):
        d, num = G[i + 1]
        tau.append(nmod_poly(num, q) * u * pow(d % q, -1, q) % P)
    pw = []
    for i in range(len(syms)):
        L = [nmod_poly([1], q)]
        for e in range(maxe[i]):
            L.append(L[-1] * tau[i] % P)
        pw.append(L)

    def ev(T):
        acc = nmod_poly([0], q)
        for m, a, b in T:
            v = nmod_poly([a * pow(b, -1, q) % q], q)
            for i, e in enumerate(m):
                if e:
                    v = v * pw[i][e] % P
            acc += v
        return acc % P
    zeros = [ev(T).is_zero() for T in FT]
    x = nmod_poly([0, 1], q)
    sid = (ev(ST) - x * ev(DT)) % P
    ok = all(zeros) and sid.is_zero()
    passed += ok
    print(f'q={q}: F_k(tau) = 0: {zeros}; Sn - x Sd = 0: {sid.is_zero()} ({time.time() - t0:.1f} s)', flush=True)
    if not ok:
        print('IDENTITY FAILS mod q'); sys.exit(1)
print(f'all identities hold modulo {passed} random 62-bit primes')
