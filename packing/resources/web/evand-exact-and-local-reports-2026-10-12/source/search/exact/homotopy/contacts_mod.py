"""Independent check of the full contact system at tau (not just the eliminated consistency polynomials F).

    ../env.sh python3 contacts_mod.py SYSTEM.jl POLY.json PARAM_t1.json ... PARAM_t5.json NPRIMES SEED

The contact rows (affine in the centres and S, coefficients in Q(t)) are evaluated at tau_i = g_i/(den_i p') in
F_q[x]/(p mod q) and solved by Gaussian elimination with unit pivots.  Checked: every row is consistent (no nonzero
leftover), the centres and S are uniquely determined (a unit pivot for every unknown), and S = x (the polynomial's
variable).  Same Monte Carlo character as verify_mod.py.
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
env = dict(zip(names, syms)); env['Rational'] = sp.Rational


def D(*a):
    return {a[i]: a[i + 1] for i in range(0, len(a), 2)}


env['__D'] = D
block = src.split('rows = [', 1)[1].split('\n]', 1)[0]
rows = []
for l in block.strip().split('\n'):
    l = l.strip().rstrip(',')
    if not l:
        continue
    l = re.sub(r'big\((\d+)\)//(\d+)', r'Rational(\1, \2)', l).replace('^', '**')
    l = l.replace('Dict{String,Any}(', '__D(')
    l = re.sub(r'"(\w+)" => ', r'"\1", ', l)
    rows.append(eval(l, {'__builtins__': {}}, env))
zvars = sorted({v for r in rows for v in r[0]})
print(f'{len(rows)} rows, {len(zvars)} unknowns', flush=True)


def terms(e):
    P = sp.Poly(sp.expand(sp.sympify(e)), *syms)
    return [(m, int(c.p), int(c.q)) for m, c in P.terms()]


RT = [([(v, terms(nu), terms(de)) for v, (nu, de) in r[0].items()], terms(r[1][0]), terms(r[1][1])) for r in rows]
maxe = [max([0] + [m[i] for r in RT for T in [r[1], r[2]] + [x for _, a, b in r[0] for x in (a, b)] for m, _, _ in T])
        for i in range(len(syms))]
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
    g, u, _ = P.derivative().xgcd(P)
    if g.degree() != 0:
        continue
    u = u * pow(int(g[0]), -1, q) % P
    tau = [nmod_poly(G[i + 1][1], q) * u * pow(G[i + 1][0] % q, -1, q) % P for i in range(len(syms))]
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

    def inv(a):
        g, s, _ = a.xgcd(P)
        if g.degree() != 0:
            return None
        return s * pow(int(g[0]), -1, q) % P
    M = []                                   # each row: dict var -> R element, plus constant
    bad = False
    for ents, kn, kd in RT:
        r = {}
        for v, nu, de in ents:
            di = inv(ev(de))
            if di is None:
                bad = True; break
            r[v] = ev(nu) * di % P
        if bad:
            break
        kdi = inv(ev(kd))
        if kdi is None:
            bad = True; break
        r[None] = ev(kn) * kdi % P
        M.append({k: v for k, v in r.items() if not v.is_zero()})
    if bad:
        print(f'q={q}: a denominator is not a unit mod (p, q); skipped', flush=True)
        continue
    pivots = {}
    rest = list(range(len(M)))
    for v in zvars:
        piv = None
        for i in rest:
            if v in M[i]:
                iv = inv(M[i][v])
                if iv is not None:
                    piv = i; break
        if piv is None:
            break
        rest.remove(piv)
        R = {k: e * iv % P for k, e in M[piv].items()}
        M[piv] = R
        for i in list(rest) + list(pivots.values()):
            if v in M[i]:
                c = M[i][v]
                for k, e in R.items():
                    M[i][k] = (M[i].get(k, nmod_poly([0], q)) - c * e) % P
                M[i] = {k: e for k, e in M[i].items() if not e.is_zero()}
        pivots[v] = piv
    determined = len(pivots) == len(zvars)
    consistent = all(not M[i] for i in rest)
    # row of S: S + const = 0  ->  S = -const
    Sval = (-M[pivots['S']].get(None, nmod_poly([0], q))) % P if 'S' in pivots else None
    S_is_x = Sval is not None and (Sval - nmod_poly([0, 1], q)) % P == nmod_poly([0], q)
    ok = determined and consistent and S_is_x
    passed += ok
    print(f'q={q}: unknowns determined {determined}; {len(rest)} leftover rows consistent {consistent}; S = x {S_is_x} '
          f'({time.time() - t0:.0f} s)', flush=True)
    if not ok:
        print('CONTACT CHECK FAILS mod q'); sys.exit(1)
print(f'contact system consistent with S = x modulo {passed} random 62-bit primes')
