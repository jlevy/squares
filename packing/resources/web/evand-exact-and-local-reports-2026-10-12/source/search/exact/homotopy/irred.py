"""Irreducibility of an integer polynomial by factorisation degree patterns modulo primes (rigorous: a factorisation
over Z of degrees (d, n-d) would give, mod every good prime, a sub-multiset of factor degrees summing to d).

    ../env.sh python3 irred.py POLY.json NPRIMES
"""
import json, sys, time
sys.set_int_max_str_digits(0)
import flint
from flint import nmod_poly, fmpz
c = [int(x) for x in json.load(open(sys.argv[1]))['coeffs_ascending']]
n = len(c) - 1
from math import gcd
g = 0
for x in c:
    g = gcd(g, x)
print(f'degree {n}; content {g}', flush=True)
possible = None
p = 2 ** 61
good = 0
while good < int(sys.argv[2]):
    p += 1
    while not fmpz(p).is_prime():
        p += 1
    if c[-1] % p == 0:
        continue
    fp = nmod_poly(c, p)
    if fp.gcd(fp.derivative()).degree() > 0:
        print(f'p={p}: not squarefree mod p, skipped', flush=True)
        continue
    t0 = time.time()
    degs = sorted(f.degree() for f, e in fp.factor()[1])
    sums = 1
    for d in degs:
        sums |= sums << d
    possible = sums if possible is None else possible & sums
    good += 1
    cand = [d for d in range(1, n) if possible >> d & 1]
    print(f'p={p}: {len(degs)} factors, degrees {degs[:12]}{"..." if len(degs) > 12 else ""} ({time.time() - t0:.0f} s); '
          f'possible proper factor degrees left: {len(cand)}', flush=True)
print('IRREDUCIBLE over Q' if not cand and g == 1 else f'not proven: {cand[:20]}')
