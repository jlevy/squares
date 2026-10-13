"""COARSE_LOOSE_CAPACITY quartic (PROOF.md P066): p(u) = (1-w) + (1-2H)u + 4u^2 + (-1-2H)u^3 + (1+w)u^4 > 0 on [0,1].
Exact check with SymPy: count real roots in [0,1] (Sturm) and the exact minimum value on [0,1]."""
import sympy as sp
u = sp.symbols('u')
for name, w, H in (('k3', sp.Rational(529, 750), sp.Rational(2821531, 2000000)),
                   ('k15', sp.Rational(3427, 5000), sp.Rational(2859531, 2000000))):
    p = sp.Poly((1-w) + (1-2*H)*u + 4*u**2 + (-1-2*H)*u**3 + (1+w)*u**4, u)
    nroots = p.count_roots(0, 1)
    crit = [r for r in sp.Poly(p.diff(u), u).real_roots() if 0 <= r <= 1]
    vals = [p.eval(0), p.eval(1)] + [p.eval(sp.nsimplify(r)) if r.is_rational else sp.N(p.as_expr().subs(u, r), 30) for r in crit]
    print(name, 'roots in [0,1]:', nroots, ' min over endpoints/critical points ~', min(sp.N(v, 20) for v in vals))
