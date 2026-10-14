"""Independent exact check of the statement's root isolation (ALGEBRAIC_ENDPOINT) and of L.

Everything is exact rational arithmetic (fractions.Fraction) except where noted.

1. F and G as in STATEMENT.md.
2. Krawczyk / interval-Newton test on the box [t0 +- 1e-12] x [b0 +- 1e-12]:
   K(X) = m - Y f(m) + (I - Y J(X)) (X - m), with exact rational interval arithmetic for J(X).
   If K(X) is strictly inside X, there is exactly one root in X (Krawczyk's theorem).
3. Separately, a Miranda-style sign check is not needed given Krawczyk.
4. Enclosure of L = (6+4t)/(1+2t-t^2) from the Krawczyk box, and comparison with R, C, U and the 20-place bound.
5. A tighter enclosure by iterating Krawczyk (contracting the box), to get the 20-digit interval.
"""
from fractions import Fraction as Fr
import sys

t0 = Fr(362043893314323383453621978739944164218293243036741520638379, 10**60)
b0 = Fr(330948674722739910429808533282915634174672003999685385633441, 10**60)
rad = Fr(1, 10**12)

def F(t, b):
    return t - 3*t**2 - t**3 - t**4 + (1 - t - t**4 + t**5)*b + (-3*t + t**2 - t**3 - t**4)*b**2

def G(t, b):
    return (-2*t**3 - 2*t**4 + (-1 + 3*t - 4*t**2 + t**4 + t**5)*b
            + (4 - 2*t - 2*t**2 + 2*t**3 - 2*t**4)*b**2
            + (-1 - 5*t + 4*t**2 + t**4 + t**5)*b**3 + (2*t + 2*t**2)*b**4)

# partial derivatives (hand-derived, then checked numerically below against finite differences)
def Ft(t, b):
    return 1 - 6*t - 3*t**2 - 4*t**3 + (-1 - 4*t**3 + 5*t**4)*b + (-3 + 2*t - 3*t**2 - 4*t**3)*b**2

def Fb(t, b):
    return (1 - t - t**4 + t**5) + 2*(-3*t + t**2 - t**3 - t**4)*b

def Gt(t, b):
    return (-6*t**2 - 8*t**3 + (3 - 8*t + 4*t**3 + 5*t**4)*b
            + (-2 - 4*t + 6*t**2 - 8*t**3)*b**2
            + (-5 + 8*t + 4*t**3 + 5*t**4)*b**3 + (2 + 4*t)*b**4)

def Gb(t, b):
    return ((-1 + 3*t - 4*t**2 + t**4 + t**5)
            + 2*(4 - 2*t - 2*t**2 + 2*t**3 - 2*t**4)*b
            + 3*(-1 - 5*t + 4*t**2 + t**4 + t**5)*b**2 + 4*(2*t + 2*t**2)*b**3)

# --- derivative sanity check by central differences (exact rationals, small h) ---
h = Fr(1, 10**8)
for name, f, dft, dfb in (("F", F, Ft, Fb), ("G", G, Gt, Gb)):
    num_t = (f(t0 + h, b0) - f(t0 - h, b0)) / (2*h)
    num_b = (f(t0, b0 + h) - f(t0, b0 - h)) / (2*h)
    assert abs(num_t - dft(t0, b0)) < Fr(1, 10**12), (name, "t")
    assert abs(num_b - dfb(t0, b0)) < Fr(1, 10**12), (name, "b")
print("derivatives agree with central differences at (t0,b0)")

# --- interval arithmetic on rationals ---
class I:
    __slots__ = ("lo", "hi")
    def __init__(self, lo, hi=None):
        if hi is None:
            hi = lo
        self.lo, self.hi = Fr(lo), Fr(hi)
        assert self.lo <= self.hi
    def __add__(s, o):
        o = o if isinstance(o, I) else I(o)
        return I(s.lo + o.lo, s.hi + o.hi)
    __radd__ = __add__
    def __neg__(s):
        return I(-s.hi, -s.lo)
    def __sub__(s, o):
        o = o if isinstance(o, I) else I(o)
        return I(s.lo - o.hi, s.hi - o.lo)
    def __rsub__(s, o):
        return I(o) - s
    def __mul__(s, o):
        o = o if isinstance(o, I) else I(o)
        c = [s.lo*o.lo, s.lo*o.hi, s.hi*o.lo, s.hi*o.hi]
        return I(min(c), max(c))
    __rmul__ = __mul__
    def __pow__(s, n):
        r = I(1)
        for _ in range(n):
            r = r * s
        return r
    def width(s):
        return s.hi - s.lo
    def __repr__(s):
        return f"[{float(s.lo)!r}, {float(s.hi)!r}]"

def krawczyk(T, B):
    """One Krawczyk step on the box T x B. Returns (K_T, K_B, contained)."""
    mt, mb = (T.lo + T.hi)/2, (B.lo + B.hi)/2
    # exact Jacobian at midpoint and its inverse Y
    a, b_, c, d = Ft(mt, mb), Fb(mt, mb), Gt(mt, mb), Gb(mt, mb)
    det = a*d - b_*c
    assert det != 0
    Y = [[d/det, -b_/det], [-c/det, a/det]]
    fm = [F(mt, mb), G(mt, mb)]
    # interval Jacobian over the box
    J = [[Ft(T, B), Fb(T, B)], [Gt(T, B), Gb(T, B)]]
    # M = I - Y J
    M = [[I(1) - (Y[0][0]*J[0][0] + Y[0][1]*J[1][0]), -(Y[0][0]*J[0][1] + Y[0][1]*J[1][1])],
         [-(Y[1][0]*J[0][0] + Y[1][1]*J[1][0]), I(1) - (Y[1][0]*J[0][1] + Y[1][1]*J[1][1])]]
    dT, dB = T - mt, B - mb
    KT = mt - (Y[0][0]*fm[0] + Y[0][1]*fm[1]) + M[0][0]*dT + M[0][1]*dB
    KB = mb - (Y[1][0]*fm[0] + Y[1][1]*fm[1]) + M[1][0]*dT + M[1][1]*dB
    inside = (T.lo < KT.lo and KT.hi < T.hi and B.lo < KB.lo and KB.hi < B.hi)
    # operator norm bound of M (max row sum of magnitudes)
    mag = lambda x: max(abs(x.lo), abs(x.hi))
    norm = max(mag(M[0][0]) + mag(M[0][1]), mag(M[1][0]) + mag(M[1][1]))
    return KT, KB, inside, norm

T = I(t0 - rad, t0 + rad)
B = I(b0 - rad, b0 + rad)
KT, KB, inside, norm = krawczyk(T, B)
print("Krawczyk on the statement box: K(X) strictly inside X ->", inside)
print("  ||I - Y J(X)||_inf <=", float(norm))
print("  K_T width", float(KT.width()), " K_B width", float(KB.width()))
assert inside and norm < 1
print("=> exactly one simultaneous real zero in the statement rectangle (Krawczyk).")

# refine by intersecting and iterating; round the box OUTWARD to denominator 10^90 at every
# step so that rational sizes stay bounded (an enlarged box is still a valid enclosure once
# Krawczyk re-verifies containment on it)
import math
def round_out(iv, den=10**90):
    lo = Fr(math.floor(iv.lo * den), den)
    hi = Fr(math.ceil(iv.hi * den), den)
    return I(lo, hi)
for it in range(5):
    T = round_out(I(max(T.lo, KT.lo), min(T.hi, KT.hi)))
    B = round_out(I(max(B.lo, KB.lo), min(B.hi, KB.hi)))
    KT, KB, inside, norm = krawczyk(T, B)
    assert inside, it
print("refined box widths:", float(T.width()), float(B.width()))

# L = (6+4t)/(1+2t-t^2) on the refined t interval; denominator positive, numerator positive -> monotone?
# Just use interval arithmetic with exact division via bounds: f(t) = (6+4t)/(1+2t-t^2).
# f'(t) = [4(1+2t-t^2) - (6+4t)(2-2t)]/den^2 = [4+8t-4t^2 -12+12t-8t+8t^2]/den^2 = (4t^2+12t-8)/den^2, negative for t ~0.36.
# so f is decreasing on the interval: L in [f(t.hi), f(t.lo)].
def f(t):
    return (6 + 4*t)/(1 + 2*t - t**2)
assert 4*T.lo**2 + 12*T.hi - 8 < 0  # derivative numerator negative on the whole interval (4t^2+12t-8 <= 4*T.hi^2+12*T.hi-8)
assert 4*T.hi**2 + 12*T.hi - 8 < 0
assert 1 + 2*T.lo - T.hi**2 > 0
Llo, Lhi = f(T.hi), f(T.lo)
print("L in [%s, %s]" % (Llo, Lhi))
import decimal
decimal.getcontext().prec = 60
def dec(x):
    return decimal.Decimal(x.numerator) / decimal.Decimal(x.denominator)
print("L in [%s, %s] (decimal)" % (dec(Llo), dec(Lhi)))
R = Fr(4675530093604551, 10**15)
C = Fr(4675531, 10**6)
U = Fr(1169, 250)
print("L < R:", Lhi < R, " R - L >=", float(R - Lhi), " <=", float(R - Llo))
print("R < C < U:", R < C < U)
lo20 = Fr(467553009360455095163, 10**20)
hi20 = Fr(467553009360455095164, 10**20)
print("20-place bound 4.67553009360455095163 < L < 4.67553009360455095164:", lo20 < Llo and Lhi < hi20)
eps = Fr(323264740583067756265381186720884493986257, 625 * 10**56)
print("eps =", float(eps), " R - L - eps > 0:", R - Lhi - eps > 0, " (R-L-eps in [%g, %g])" % (float(R - Lhi - eps), float(R - Llo - eps)))
print("denominator 1+2t-t^2 positive on the statement box:", 1 + 2*(t0 - rad) - (t0 + rad)**2 > 0)
