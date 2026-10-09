"""Independent exact check of a minpoly.py output (NAME.minpoly.json): standard library only (fractions).

Claim checked: n closed unit squares fit, with pairwise disjoint interiors, in [0, S*]^2, where
  S* = S(t*), t* a real root of f in [ta, tb] (exact sign change, or ta = tb with f(ta) = 0),
and S* is the unique root of the integer polynomial p in [Sa, Sb] (sign change, and p' has constant sign there).

Data: the number field K = Q[t]/f; per square a centre (x, y) in K (coefficient lists in t), an angle parameter u in K
(u = tan(theta'/2), |u| <= 1) and m: (c, s) = R^m ((1-u^2)/(1+u^2), 2u/(1+u^2)), R = rotation by 90 deg, so
c^2 + s^2 = 1 identically.

Every inequality g >= 0 (corner of j on the far side of a side line of i; corner inside the box) is proved either by
rational interval arithmetic over t in [ta, tb] (g > 0 there), or as an identity: the numerator of g is 0 mod f, so
g(t*) = 0 at every root of f.  Nothing here depends on how the data was produced.

Separation: for each pair, either the centres are at distance >= sqrt 2 (disjoint circumscribed discs), or some side
line of one square has all four corners of the other on its closed outer side (separating line: closed half-planes,
so the interiors are disjoint).  Inside: all four corners in [0, S]^2 (convexity).

  python3 verify_exact.py results/NAME.minpoly.json [...]
"""
import sys, json, gzip
from fractions import Fraction as F

P2 = 2 ** 400                                   # interval endpoints are rounded outward to multiples of 2^-400


def rdn(x):
    return F((x.numerator * P2) // x.denominator, P2)


def rup(x):
    return F(-((-x.numerator * P2) // x.denominator), P2)


class I:
    """Closed rational interval with outward rounding."""
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        self.lo, self.hi = F(lo), F(lo if hi is None else hi)

    def __add__(a, b):
        b = b if isinstance(b, I) else I(b)
        return I(rdn(a.lo + b.lo), rup(a.hi + b.hi))
    __radd__ = __add__

    def __neg__(a):
        return I(-a.hi, -a.lo)

    def __sub__(a, b):
        return a + (-(b if isinstance(b, I) else I(b)))

    def __rsub__(a, b):
        return I(b) - a

    def __mul__(a, b):
        b = b if isinstance(b, I) else I(b)
        p = (a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi)
        return I(rdn(min(p)), rup(max(p)))
    __rmul__ = __mul__

    def inv(a):
        assert a.lo > 0 or a.hi < 0, 'interval division by an interval containing 0'
        return I(rdn(1 / a.hi), rup(1 / a.lo))


# ---------------------------------------------------------------- Q[t] mod f, and fractions num/den over it
def padd(a, b):
    r = [F(0)] * max(len(a), len(b))
    for i, x in enumerate(a):
        r[i] += x
    for i, x in enumerate(b):
        r[i] += x
    return trim(r)


def pneg(a):
    return [-x for x in a]


def pmul(a, b):
    if not a or not b:
        return []
    r = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return trim(r)


def trim(a):
    while a and a[-1] == 0:
        a = a[:-1]
    return list(a)


def pmod(a, f):
    a = list(a)
    d = len(f) - 1
    lc = f[-1]
    while len(a) - 1 >= d and a:
        q = a[-1] / lc
        s = len(a) - 1 - d
        for i, c in enumerate(f):
            a[s + i] -= q * c
        a = trim(a)
    return a


class E:
    """Element num/den with num, den in Q[t] (reduced mod f); den is a product of factors 1 + u^2 > 0."""
    __slots__ = ('n', 'd')
    f = None

    def __init__(self, n, d=None):
        self.n, self.d = pmod(trim(n), E.f), (d if d is not None else [F(1)])

    @staticmethod
    def c(x):
        return E([F(x)])

    def __add__(a, b):
        b = b if isinstance(b, E) else E.c(b)
        if a.d == b.d:
            return E(padd(a.n, b.n), a.d)
        return E(padd(pmul(a.n, b.d), pmul(b.n, a.d)), pmod(pmul(a.d, b.d), E.f))
    __radd__ = __add__

    def __neg__(a):
        return E(pneg(a.n), a.d)

    def __sub__(a, b):
        return a + (-(b if isinstance(b, E) else E.c(b)))

    def __rsub__(a, b):
        return E.c(b) - a

    def __mul__(a, b):
        b = b if isinstance(b, E) else E.c(b)
        return E(pmul(a.n, b.n), pmod(pmul(a.d, b.d), E.f))
    __rmul__ = __mul__

    def is_zero(a):
        return not a.n


def ev_iv(p, t):
    v = I(0)
    for c in reversed(p):
        v = v * t + c
    return v


class V:
    """A value carried as an interval over t in [ta, tb], with its exact value in K computed lazily (only when the
    interval cannot decide a sign)."""
    __slots__ = ('_e', 'i')

    def __init__(self, e, i):
        self._e, self.i = e, i                 # e: an E, or a thunk returning one

    @property
    def e(self):
        if callable(self._e):
            self._e = self._e()
        return self._e

    def __add__(a, b):
        if isinstance(b, V):
            return V(lambda: a.e + b.e, a.i + b.i)
        return V(lambda: a.e + b, a.i + b)
    __radd__ = __add__

    def __neg__(a):
        return V(lambda: -a.e, -a.i)

    def __sub__(a, b):
        return a + (-b if isinstance(b, V) else -F(b))

    def __rsub__(a, b):
        return (-a) + b

    def __mul__(a, b):
        if isinstance(b, V):
            return V(lambda: a.e * b.e, a.i * b.i)
        return V(lambda: a.e * b, a.i * b)
    __rmul__ = __mul__


def nonneg(v):
    """Proof that v >= 0 at t*: 'gt' (interval > 0) or 'eq' (identity mod f), else None."""
    if v.i.lo > 0:
        return 'gt'
    if v.i.hi < 0:
        return None
    return 'eq' if v.e.is_zero() else None


def check(path, quiet=False):
    D = json.load(gzip.open(path, 'rt') if path.endswith('.gz') else open(path))
    n = D['n']
    f = [F(x) for x in D['field']['f']]
    E.f = f
    ta, tb = (F(x) for x in D['field']['t_interval'])
    fv = lambda x: sum(c * x ** i for i, c in enumerate(f))
    if ta == tb:
        assert fv(ta) == 0, 'f(t) != 0'
    else:
        assert ta < tb and fv(ta) * fv(tb) < 0, 'no sign change of f on the t interval'
        for _ in range(200):                     # narrow it (exact bisection keeps a root inside)
            mid = (ta + tb) / 2
            if fv(mid) == 0:
                ta = tb = mid
                break
            if fv(ta) * fv(mid) < 0:
                tb = mid
            else:
                ta = mid
            ta, tb = rdn(ta), rup(tb)
            if fv(ta) * fv(tb) >= 0:
                raise RuntimeError('lost the sign change while narrowing')
    T = I(ta, tb)

    def val(coeffs):
        p = [F(x) for x in coeffs]
        return V(E(p), ev_iv(p, T))

    def val_poly(p):
        return V(E(p), ev_iv(p, T))
    sq = []
    for q in D['squares']:
        x, y, u = val(q['x']), val(q['y']), val(q['u'])
        den = 1 + u * u
        dinv_i = den.i.inv()
        c = V(E((1 - u * u).e.n, (den.e.n)), (1 - u * u).i * dinv_i)
        s = V(E((2 * u).e.n, den.e.n), (2 * u).i * dinv_i)
        for _ in range(q['m'] % 4):
            c, s = -s, c
        sq.append((x, y, c, s))
    S = val(D['S']['in_K'])
    # p(S) = 0 in K, p has a unique root in [Sa, Sb] and S(t*) lies in it
    p = [F(x) for x in D['S']['poly']]
    pv = V(E([]), I(0))
    for cf in reversed(p):
        pv = pv * S + cf
    assert pv.e.is_zero(), 'p(S) != 0 mod f'
    Sa, Sb = (F(x) for x in D['S']['interval'])
    assert Sa <= S.i.lo and S.i.hi <= Sb, 'S(t*) not inside [Sa, Sb]'
    pS = lambda x: sum(c * x ** i for i, c in enumerate(p))
    dp = [i * c for i, c in enumerate(p)][1:]
    # uniqueness: p changes sign and p' has constant sign on [Sa, Sb]; if the given interval is too wide for the
    # interval bound on p', tighten it around the enclosure of S(t*) (the statement then uses the tighter interval)
    for delta in [None] + [F(1, 10 ** e) for e in (30, 40, 50, 60, 70, 80)]:
        if delta is not None:
            Sa, Sb = rdn(S.i.lo - delta), rup(S.i.hi + delta)
        dpi = ev_iv(dp, I(Sa, Sb))
        if (dpi.lo > 0 or dpi.hi < 0) and pS(Sa) * pS(Sb) < 0:
            break
    else:
        raise AssertionError("p' changes sign on [Sa, Sb]: root not proved unique")

    H = F(1, 2)

    def corners(k):
        x, y, c, s = sq[k]
        return [(x + (c * a - s * b) * H, y + (s * a + c * b) * H) for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]

    def normals(k):
        _, _, c, s = sq[k]
        return [(c, s), (-s, c), (-c, -s), (s, -c)]
    CO = [corners(k) for k in range(n)]
    stats = {'gt': 0, 'eq': 0, 'disc': 0}
    # inside the box
    for k in range(n):
        for (px, py) in CO[k]:
            for g in (px, S - px, py, S - py):
                r = nonneg(g)
                if r is None:
                    raise AssertionError(f'square {k}: corner outside the box (or not proved inside)')
                stats[r] += 1
    # pairs
    mids = [((sq[k][0].i.lo + sq[k][0].i.hi) / 2, (sq[k][1].i.lo + sq[k][1].i.hi) / 2) for k in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if (mids[i][0] - mids[j][0]) ** 2 + (mids[i][1] - mids[j][1]) ** 2 > 3:
                dx, dy = sq[j][0].i - sq[i][0].i, sq[j][1].i - sq[i][1].i
                if (dx * dx + dy * dy).lo >= 2:
                    stats['disc'] += 1
                    continue
            # candidate separating lines, best first (by interval midpoint of the worst corner)
            cand = []
            for own, oth in ((i, j), (j, i)):
                ox, oy = sq[own][0], sq[own][1]
                for nx, ny in normals(own):
                    gs = [nx * (px - ox) + ny * (py - oy) - H for (px, py) in CO[oth]]
                    cand.append((min(g.i.lo + g.i.hi for g in gs), gs))
            cand.sort(key=lambda z: -z[0])
            for _, gs in cand:
                rs = [nonneg(g) for g in gs]
                if all(rs):
                    for r in rs:
                        stats[r] += 1
                    break
            else:
                raise AssertionError(f'pair ({i}, {j}): no separating line proved')
    if not quiet:
        print(f'{path}: VALID.  n = {n}: s({n}) <= S*, S* the unique root of p (degree {len(p) - 1}) in '
              f'[{float(Sa):.15g}, {float(Sb):.15g}]; field degree {len(f) - 1}; '
              f'{stats["eq"]} touching incidences proved as identities in K, {stats["gt"]} strict by intervals, '
              f'{stats["disc"]} pairs by discs')
    return stats


if __name__ == '__main__':
    bad = 0
    for pth in sys.argv[1:]:
        try:
            check(pth)
        except (AssertionError, RuntimeError) as ex:
            bad += 1
            print(f'{pth}: NOT VERIFIED: {ex}')
    sys.exit(1 if bad else 0)
