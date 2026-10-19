"""Krawczyk certificate: F has exactly one zero t* in the box X = tstar +- r (ball arithmetic), and S(t*) in an interval.

    ../env.sh python3 krawczyk.py work/n29_system.jl RADIUS OUT.json

K(X) = m - Y F(m) + (I - Y J(X)) (X - m), m = box centre, Y ~ J(m)^-1.  K(X) inside the interior of X proves a unique
zero of F in X (Krawczyk / Moore).  All arithmetic is arb ball arithmetic (rigorous enclosures).
"""
import json, re, sys
sys.set_int_max_str_digits(0)
from fractions import Fraction
import sympy as sp
import flint
from flint import arb, arb_mat

flint.ctx.prec = 600
src = open(sys.argv[1]).read()
rad = arb(sys.argv[2])
names = re.search(r'@var (.*)', src).group(1).split()
k = len(names)
syms = sp.symbols(names)
loc = dict(zip(names, syms))


def jl2sp(s):
    s = re.sub(r'big\((\d+)\)//(\d+)', r'Rational(\1, \2)', s)
    s = s.replace('^', '**')
    return sp.sympify(s, locals={**loc, 'Rational': sp.Rational})


fblock = src.split('F = [', 1)[1].split('\n]', 1)[0]
Fexpr = [jl2sp(x.strip().rstrip(',')) for x in fblock.strip().split('\n') if x.strip()]
Sn = jl2sp(re.search(r'^Sn = (.*)$', src, re.M).group(1))
Sd = jl2sp(re.search(r'^Sd = (.*)$', src, re.M).group(1))
tstar = [arb(x) for x in re.findall(r'big"([-0-9.e]+)"', re.search(r'^tstar = (.*)$', src, re.M).group(1))]
assert len(Fexpr) == k and len(tstar) == k


def terms(e):
    P = sp.Poly(sp.expand(e), *syms)
    return [(m, Fraction(int(c.p), int(c.q))) for m, c in P.terms()]


def ev(T, x):
    s = arb(0)
    for m, c in T:
        v = arb(c.numerator) / c.denominator
        for xi, e in zip(x, m):
            if e:
                v *= xi ** e
        s += v
    return s


FT = [terms(f) for f in Fexpr]
JT = [[terms(sp.diff(f, v)) for v in syms] for f in Fexpr]
X = [arb(m, rad) for m in tstar]
mid = tstar
Fm = arb_mat([[ev(T, mid)] for T in FT])
Jm = arb_mat([[ev(T, mid) for T in row] for row in JT])
Y = arb_mat([[arb(Jm[i, j].mid()) for j in range(k)] for i in range(k)]).inv()
Y = arb_mat([[arb(Y[i, j].mid()) for j in range(k)] for i in range(k)])      # exact floating matrix
JX = arb_mat([[ev(T, X) for T in row] for row in JT])
I = arb_mat([[1 if i == j else 0 for j in range(k)] for i in range(k)])
dX = arb_mat([[X[i] - mid[i]] for i in range(k)])
K = arb_mat([[mid[i]] for i in range(k)]) - Y * Fm + (I - Y * JX) * dX
ok = True
for i in range(k):
    inside = (K[i, 0] - mid[i]).abs_upper() < rad
    ok &= bool(inside)
    print(f't{i + 1}: |K - m| <= {float((K[i, 0] - mid[i]).abs_upper()):.3e} vs radius {float(rad):.1e}: {inside}')
Sint = ev(terms(Sn), X) / ev(terms(Sd), X)
print('UNIQUE ZERO of F in X' if ok else 'NOT CERTIFIED')
print('S(t*) in', Sint.str(80))
json.dump({'certified': ok, 'radius': sys.argv[2], 'tstar': [m.str(70, radius=False) for m in mid],
           'S_mid': Sint.mid().str(70, radius=False), 'S_rad': float(Sint.rad())}, open(sys.argv[3], 'w'))
