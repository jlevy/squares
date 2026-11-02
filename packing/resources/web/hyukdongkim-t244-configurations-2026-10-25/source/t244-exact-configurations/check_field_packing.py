"""Independent exact checker for packings over a number field K = Q[t]/f (minpoly.json format).

Usage: python check_field_packing.py CERT.json [...]
Requires python-flint (FLINT/Arb: exact rationals and rigorous ball arithmetic).

Claim checked: n closed unit squares lie in [0, S*]^2 with pairwise disjoint interiors, where t* is
the root of f in the rational interval [ta, tb], S* = S(t*), and S* is the only root of the integer
polynomial p in [Sa, Sb].

Each square: centre (x, y) in K, angle parameter u in K, quarter turns m; its side directions are
(c, s) = R^m((1-u^2)/(1+u^2), 2u/(1+u^2)) and (-s, c).  Every quantity is an element of K, held
exactly as a rational polynomial reduced mod f.  An inequality g >= 0 is proved either by an Arb ball
for g(t*) lying in (0, inf), or by g being exactly 0 in K.

Separation of a pair: centres at distance >= sqrt 2, or one of the four side normals a of the two
squares with |(c_i - c_j).a| - h_i(a) - h_j(a) >= 0, where h(a) is the half-width of a square on a.
Inside: x - h, S - x - h, y - h and S - y - h are all >= 0 for the half-width h on the axes.

Shares no code with evand/square-packing's verify_exact.py: different arithmetic (Arb balls and
FLINT polynomials instead of Fraction intervals) and a different separation test (projections on
side normals instead of corners against side lines).
"""
import json, sys, gzip
from flint import fmpq, fmpq_poly, fmpz, arb, ctx

ctx.prec = 4000


class K:
    """Element of Q[t]/f with a lazily computed Arb enclosure of its value at t*."""
    f = None
    T = None

    __slots__ = ("p", "_b")

    def __init__(self, p):
        self.p = p % K.f if p.degree() >= K.f.degree() else p
        self._b = None

    @staticmethod
    def of(x):
        return K(fmpq_poly([x]))

    @property
    def ball(self):
        if self._b is None:
            acc = arb(0)
            for c in reversed(self.p.coeffs()):
                acc = acc * K.T + arb(c)
            self._b = acc
        return self._b

    def __add__(a, b):
        return K(a.p + (b.p if isinstance(b, K) else fmpq_poly([b])))

    __radd__ = __add__

    def __sub__(a, b):
        return K(a.p - (b.p if isinstance(b, K) else fmpq_poly([b])))

    def __rsub__(a, b):
        return K(fmpq_poly([b]) - a.p)

    def __neg__(a):
        return K(-a.p)

    def __mul__(a, b):
        return K(a.p * (b.p if isinstance(b, K) else fmpq_poly([b])))

    __rmul__ = __mul__

    def inv(a):
        g, s, _ = a.p.xgcd(K.f)
        assert g.degree() == 0 and not g.is_zero(), "element not invertible mod f"
        return K(s * fmpq_poly([1 / g.coeffs()[0]]))

    def is_zero(a):
        return a.p.is_zero()

    def sign(a):
        """Exact sign at t*: from the ball, or 0 when the element is exactly zero."""
        b = a.ball
        if b > 0:
            return 1
        if b < 0:
            return -1
        if a.is_zero():
            return 0
        raise ArithmeticError("sign undecided: ball contains 0 but the element is not 0 in K")


def proof_nonneg(g):
    s = g.sign()
    if s < 0:
        return None
    return "eq" if s == 0 else "gt"


def kabs(a):
    return -a if a.sign() < 0 else a


def load(path):
    return json.load(gzip.open(path, "rt") if path.endswith(".gz") else open(path))


def check(path):
    D = load(path)
    n = D["n"]
    assert len(D["squares"]) == n, "number of squares differs from n"
    fq = [fmpq(*map(int, (str(c) + "/1").split("/")[:2])) for c in D["field"]["f"]]
    f = fmpq_poly(fq)
    fac = f.factor()
    assert len(fac[1]) == 1 and fac[1][0][1] == 1, "f is not irreducible over Q"
    K.f = f
    to_q = lambda s: fmpq(*map(int, (str(s) + "/1").split("/")[:2]))
    ta, tb = (to_q(x) for x in D["field"]["t_interval"])
    fe = lambda q: sum((c * q ** i for i, c in enumerate(fq)), fmpq(0))
    assert ta < tb and fe(ta) * fe(tb) < 0, "f does not change sign on the t interval"
    for _ in range(600):                                  # exact bisection to a tiny interval
        mid = (ta + tb) / 2
        if fe(mid) == 0:
            ta = tb = mid
            break
        if fe(ta) * fe(mid) < 0:
            tb = mid
        else:
            ta = mid
    K.T = arb(ta).union(arb(tb))
    el = lambda cs: K(fmpq_poly([to_q(c) for c in cs])) if cs else K.of(0)
    S = el(D["S"]["in_K"])
    p = [int(c) for c in D["S"]["poly"]]
    pk = K.of(0)
    for c in reversed(p):
        pk = pk * S + c
    assert pk.is_zero(), "p(S) is not 0 in K"
    Sa, Sb = (to_q(x) for x in D["S"]["interval"])
    pe = lambda q: sum((c * q ** i for i, c in enumerate(p)), fmpq(0))
    assert pe(Sa) * pe(Sb) < 0, "p does not change sign on [Sa, Sb]"
    assert S.ball > arb(Sa) and S.ball < arb(Sb), "S(t*) not inside [Sa, Sb]"
    # uniqueness of the root of p in [Sa, Sb]: p' has constant sign there (Arb ball)
    dp = fmpq_poly(p).derivative()
    lo_hi = arb(Sa).union(arb(Sb))
    dval = arb(0)
    for c in reversed(dp.coeffs()):
        dval = dval * lo_hi + arb(c)
    if not (dval > 0 or dval < 0):                        # tighten around S if needed
        w = fmpq(1, 10 ** 60)
        mid = fmpq(int((S.ball.mid() * 10 ** 70).floor().unique_fmpz()), 10 ** 70)
        Sa, Sb = mid - w, mid + w
        assert pe(Sa) * pe(Sb) < 0
        lo_hi = arb(Sa).union(arb(Sb))
        dval = arb(0)
        for c in reversed(dp.coeffs()):
            dval = dval * lo_hi + arb(c)
        assert dval > 0 or dval < 0, "root of p not proved unique"
    sq = []
    for q in D["squares"]:
        x, y, u = el(q["x"]), el(q["y"]), el(q["u"])
        den = (u * u + 1).inv()
        c, s = (1 - u * u) * den, (u * 2) * den
        for _ in range(q["m"] % 4):
            c, s = -s, c
        assert (c * c + s * s - 1).is_zero()
        sq.append((x, y, c, s))
    half = fmpq(1, 2)
    stats = {"gt": 0, "eq": 0, "far": 0}
    for k, (x, y, c, s) in enumerate(sq):
        h = (kabs(c) + kabs(s)) * half
        for g in (x - h, S - x - h, y - h, S - y - h):
            r = proof_nonneg(g)
            assert r, f"square {k} not proved inside the box"
            stats[r] += 1
    two = arb(2)
    for i in range(n):
        xi, yi, ci, si = sq[i]
        for j in range(i + 1, n):
            xj, yj, cj, sj = sq[j]
            dx, dy = xi - xj, yi - yj
            if (dx.ball * dx.ball + dy.ball * dy.ball) >= two:
                stats["far"] += 1
                continue
            ok = None
            for ax in ((ci, si), (-si, ci), (cj, sj), (-sj, cj)):
                hi_ = (kabs(ci * ax[0] + si * ax[1]) + kabs(-si * ax[0] + ci * ax[1])) * half
                hj_ = (kabs(cj * ax[0] + sj * ax[1]) + kabs(-sj * ax[0] + cj * ax[1])) * half
                g = kabs(dx * ax[0] + dy * ax[1]) - hi_ - hj_
                ok = proof_nonneg(g)
                if ok:
                    break
            assert ok, f"pair ({i}, {j}) not proved separated"
            stats[ok] += 1
    print(f"{path}: VALID. n = {n}; field degree {f.degree()}; side = the root of p (degree {len(p) - 1}) "
          f"in [{float(Sa):.15f}, {float(Sb):.15f}]; {stats['eq']} contacts proved exactly in K, "
          f"{stats['gt']} strict inequalities by Arb balls, {stats['far']} pairs far apart")


if __name__ == "__main__":
    bad = 0
    for pth in sys.argv[1:]:
        try:
            check(pth)
        except (AssertionError, ArithmeticError) as ex:
            bad += 1
            print(f"{pth}: NOT VERIFIED: {ex}")
    sys.exit(1 if bad else 0)
