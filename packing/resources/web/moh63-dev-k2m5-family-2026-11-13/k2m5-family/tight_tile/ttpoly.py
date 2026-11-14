"""Exact multivariate polynomials in (p, q, h) with Fraction coefficients, and exact rational interval arithmetic.
A polynomial is a dict {(i, j, k): Fraction} meaning sum c p^i q^j h^k.  Intervals are (lo, hi) pairs of Fractions."""
from fractions import Fraction as F

def P(c=0, e=(0, 0, 0)):
    c = F(c); return {e: c} if c != 0 else {}
def padd(*ps):
    r = {}
    for p in ps:
        for e, c in p.items():
            v = r.get(e, 0) + c
            if v == 0: r.pop(e, None)
            else: r[e] = v
    return r
def pscale(k, p): k = F(k); return {e: k*c for e, c in p.items()} if k != 0 else {}
def pmul(a, b):
    r = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            e = (e1[0]+e2[0], e1[1]+e2[1], e1[2]+e2[2]); v = r.get(e, 0) + c1*c2
            if v == 0: r.pop(e, None)
            else: r[e] = v
    return r
def pdiff_h(p): return {(i, j, k-1): c*k for (i, j, k), c in p.items() if k > 0}
def pat_h0(p): return {e: c for e, c in p.items() if e[2] == 0}
def pmindeg(ps):
    """componentwise minimal exponent over all monomials of the given (nonzero) polynomials"""
    es = [e for p in ps for e in p]
    return tuple(min(e[t] for e in es) for t in range(3))
def pdivmono(p, m): return {(e[0]-m[0], e[1]-m[1], e[2]-m[2]): c for e, c in p.items()}
def pdeg_pq(p): return max((e[0]+e[1] for e in p), default=0)
def peval(p, x, y, h=F(0)):
    return sum((c * x**e[0] * y**e[1] * h**e[2] for e, c in p.items()), F(0))

# ---- exact rational intervals ----
def imul(a, b):
    v = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]); return (min(v), max(v))
def ipow(a, n):
    if n == 0: return (F(1), F(1))
    if n % 2 == 1 or a[0] >= 0: lo, hi = a[0]**n, a[1]**n; return (min(lo, hi), max(lo, hi))
    if a[1] <= 0: return (a[1]**n, a[0]**n)
    return (F(0), max(a[0]**n, a[1]**n))
def ieval(p, X, Y, H):
    lo = hi = F(0); cache = {}
    def pw(I, n, tag):
        k = (tag, n)
        if k not in cache: cache[k] = ipow(I, n)
        return cache[k]
    for (i, j, k), c in p.items():
        t = imul(imul(pw(X, i, 'x'), pw(Y, j, 'y')), pw(H, k, 'h'))
        if c > 0: lo += c*t[0]; hi += c*t[1]
        else: lo += c*t[1]; hi += c*t[0]
    return (lo, hi)
def idiv(a, b):
    if not (b[0] > 0 or b[1] < 0): raise ArithmeticError('division by an interval containing 0')
    return imul(a, (1/b[1], 1/b[0]) if b[0] > 0 else (1/b[1], 1/b[0]))

# ---- outward-rounded float intervals (rigorous: every operation rounds lo down and hi up by one ulp) ----
import math
_dn = lambda x: math.nextafter(x, -math.inf); _up = lambda x: math.nextafter(x, math.inf)
def fcoef(c):
    """Fraction -> enclosing float interval"""
    x = float(c); return (_dn(x), _up(x)) if F(x) != c else (x, x)
def fpoly(p): return [(fcoef(c), e) for e, c in p.items()]
def fI(a): return (_dn(float(a[0])), _up(float(a[1])))      # Fraction interval -> float interval (outward)
def fmul(a, b):
    v = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1]); return (_dn(min(v)), _up(max(v)))
def fpow(a, n):
    if n == 0: return (1.0, 1.0)
    r = a
    for _ in range(n-1): r = fmul(r, a)
    if n % 2 == 0 and a[0] < 0 < a[1]: r = (0.0, r[1])
    return r
def feval(fp, X, Y, H):
    """X, Y, H float intervals; fp from fpoly.  Terms are grouped by the power of h (then of q): the coefficient
    polynomial of each h^k is enclosed first, then multiplied by H^k (fewer dependency losses; still rigorous)."""
    groups = {}
    for cc, e in fp: groups.setdefault(e[2], {}).setdefault(e[1], []).append((cc, e[0]))
    lo = hi = 0.0; cx = {}; cy = {}; ch = {}
    for k, byj in groups.items():
        clo = chi = 0.0
        for j, terms in byj.items():
            ilo = ihi = 0.0
            for (cl, cu), i in terms:
                t = fmul((cl, cu), cx.setdefault(i, fpow(X, i)))
                ilo = _dn(ilo + t[0]); ihi = _up(ihi + t[1])
            t = fmul((ilo, ihi), cy.setdefault(j, fpow(Y, j)))
            clo = _dn(clo + t[0]); chi = _up(chi + t[1])
        t = fmul((clo, chi), ch.setdefault(k, fpow(H, k)))
        lo = _dn(lo + t[0]); hi = _up(hi + t[1])
    return (lo, hi)
def fdiv(a, b):
    if not (b[0] > 0 or b[1] < 0): raise ArithmeticError('division by an interval containing 0')
    inv = (_dn(1/b[1]), _up(1/b[0]))
    return fmul(a, inv)
