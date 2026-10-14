"""Tie the record to the polynomial: tau(sigma) lies in the Krawczyk box of t*, for a root sigma of p near S(t*).

    ../env.sh python3 link.py SYSTEM.jl POLY.json KRAWCZYK.json S_DIGITS_FILE PARAM_t1.json ... PARAM_t5.json

1. I = S0 +- 10^-1000 (S0 from the 40k-digit refined root): p changes sign on I (exact signs via ball arithmetic), so
   I contains a root sigma of p; p' has no zero on I.
2. tau_i(I) = g_i(I) / (den_i p'(I)) is inside the box X = tstar +- r where Krawczyk proved F has exactly one zero t*.
Given the identities F_k(tau) = 0 and Sn(tau) = x Sd(tau) mod p (verify_mod.py), tau(sigma) is a zero of F in X, so
tau(sigma) = t*, and Sd(t*) != 0 (checked on X) gives S(t*) = Sn(t*)/Sd(t*) = sigma: S(t*) is a root of p.
"""
import json, re, sys
sys.set_int_max_str_digits(0)
import flint
from flint import arb, arb_poly, fmpz_poly
import sympy as sp

flint.ctx.prec = int(__import__('os').environ.get('PREC', 140000))
src = open(sys.argv[1]).read()
pc = [int(c) for c in json.load(open(sys.argv[2]))['coeffs_ascending']]
kr = json.load(open(sys.argv[3]))
assert kr['certified']
S0 = arb(open(sys.argv[4]).read().split()[0])
r = arb(kr['radius'])
tstar = [arb(x) for x in kr['tstar']]
p = fmpz_poly(pc)
dp = p.derivative()
eps = arb(__import__('os').environ.get('EPS', '1e-38000'))
lo, hi = arb(S0.mid()) - eps, arb(S0.mid()) + eps
plo, phi = arb_poly(pc)(lo), arb_poly(pc)(hi)
sc = (plo > 0 and phi < 0) or (plo < 0 and phi > 0)
print(f'p(S0 - eps) {"+" if plo > 0 else "-" if plo < 0 else "?"}, p(S0 + eps) {"+" if phi > 0 else "-" if phi < 0 else "?"}: '
      f'sign change {sc}')
I = arb(S0.mid(), eps)
dpI = arb_poly([int(c) for c in dp.coeffs()])(I)
print(f'p\'(I) excludes 0: {not dpI.contains(0)}')
ok = sc and not dpI.contains(0)
for i, fn in enumerate(sys.argv[5:10]):
    g = json.load(open(fn))['g'][0]
    num = arb_poly([int(c) for c in g['num_ascending']])
    tau = num(I) / (int(g['den']) * dpI)
    d = (tau - tstar[i]).abs_upper()
    inside = d < r
    ok &= bool(inside)
    print(f't{g["coord"]}: tau(I) = {tau.str(30)}; |tau - tstar| <= {float(d):.3e} < {float(r):.0e}: {inside}')
names = re.search(r'@var (.*)', src).group(1).split()
syms = sp.symbols(names)
Sd = sp.Poly(sp.sympify(re.search(r'^Sd = (.*)$', src, re.M).group(1).replace('^', '**'), locals=dict(zip(names, syms))), *syms)
X = [arb(t.mid(), r) for t in tstar]
v = arb(0)
for m, c in Sd.terms():
    w = arb(int(c.p)) / int(c.q)
    for xi, e in zip(X, m):
        w *= xi ** e
    v += w
print(f'Sd(X) excludes 0: {not v.contains(0)}')
ok &= not v.contains(0)
print('LINKED: S(t*) is a root of p' if ok else 'NOT LINKED')
