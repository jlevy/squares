"""Own enclosure of the root (t*, b*) and of L by one exact Krawczyk step (see root_isolation.py)."""
from fractions import Fraction as Fr
import math

t0 = Fr(362043893314323383453621978739944164218293243036741520638379, 10**60)
b0 = Fr(330948674722739910429808533282915634174672003999685385633441, 10**60)
rad = Fr(1, 10**12)


def F(t, b):
    return t - 3*t**2 - t**3 - t**4 + (1 - t - t**4 + t**5)*b + (-3*t + t**2 - t**3 - t**4)*b**2


def G(t, b):
    return (-2*t**3 - 2*t**4 + (-1 + 3*t - 4*t**2 + t**4 + t**5)*b + (4 - 2*t - 2*t**2 + 2*t**3 - 2*t**4)*b**2
            + (-1 - 5*t + 4*t**2 + t**4 + t**5)*b**3 + (2*t + 2*t**2)*b**4)


def Ft(t, b):
    return 1 - 6*t - 3*t**2 - 4*t**3 + (-1 - 4*t**3 + 5*t**4)*b + (-3 + 2*t - 3*t**2 - 4*t**3)*b**2


def Fb(t, b):
    return (1 - t - t**4 + t**5) + 2*(-3*t + t**2 - t**3 - t**4)*b


def Gt(t, b):
    return (-6*t**2 - 8*t**3 + (3 - 8*t + 4*t**3 + 5*t**4)*b + (-2 - 4*t + 6*t**2 - 8*t**3)*b**2
            + (-5 + 8*t + 4*t**3 + 5*t**4)*b**3 + (2 + 4*t)*b**4)


def Gb(t, b):
    return ((-1 + 3*t - 4*t**2 + t**4 + t**5) + 2*(4 - 2*t - 2*t**2 + 2*t**3 - 2*t**4)*b
            + 3*(-1 - 5*t + 4*t**2 + t**4 + t**5)*b**2 + 4*(2*t + 2*t**2)*b**3)


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


def krawczyk(T, B):
    mt, mb = (T.lo + T.hi)/2, (B.lo + B.hi)/2
    a, b_, c, d = Ft(mt, mb), Fb(mt, mb), Gt(mt, mb), Gb(mt, mb)
    det = a*d - b_*c
    Y = [[d/det, -b_/det], [-c/det, a/det]]
    fm = [F(mt, mb), G(mt, mb)]
    Jm = [[Ft(T, B), Fb(T, B)], [Gt(T, B), Gb(T, B)]]
    M = [[I(1) - (Y[0][0]*Jm[0][0] + Y[0][1]*Jm[1][0]), -(Y[0][0]*Jm[0][1] + Y[0][1]*Jm[1][1])],
         [-(Y[1][0]*Jm[0][0] + Y[1][1]*Jm[1][0]), I(1) - (Y[1][0]*Jm[0][1] + Y[1][1]*Jm[1][1])]]
    dT, dB = T - mt, B - mb
    KT = mt - (Y[0][0]*fm[0] + Y[0][1]*fm[1]) + M[0][0]*dT + M[0][1]*dB
    KB = mb - (Y[1][0]*fm[0] + Y[1][1]*fm[1]) + M[1][0]*dT + M[1][1]*dB
    inside = (T.lo < KT.lo and KT.hi < T.hi and B.lo < KB.lo and KB.hi < B.hi)
    return KT, KB, inside


def round_out(iv, den=10**60):
    return I(Fr(math.floor(iv.lo * den), den), Fr(math.ceil(iv.hi * den), den))


def enclosure(steps=2):
    T = I(t0 - rad, t0 + rad)
    B = I(b0 - rad, b0 + rad)
    KT, KB, inside = krawczyk(T, B)
    assert inside
    for _ in range(steps):
        T = round_out(I(max(T.lo, KT.lo), min(T.hi, KT.hi)))
        B = round_out(I(max(B.lo, KB.lo), min(B.hi, KB.hi)))
        KT, KB, inside = krawczyk(T, B)
        assert inside
    T = round_out(I(max(T.lo, KT.lo), min(T.hi, KT.hi)))
    B = round_out(I(max(B.lo, KB.lo), min(B.hi, KB.hi)))
    # L = (6+4t)/(1+2t-t^2) is decreasing on the box (derivative numerator 4t^2+12t-8 < 0)
    assert 4*T.hi**2 + 12*T.hi - 8 < 0 and 1 + 2*T.lo - T.hi**2 > 0
    Llo = (6 + 4*T.hi) / (1 + 2*T.hi - T.hi**2)
    Lhi = (6 + 4*T.lo) / (1 + 2*T.lo - T.lo**2)
    return (T.lo, T.hi), (B.lo, B.hi), (Llo, Lhi)


if __name__ == "__main__":
    (tl, th), (bl, bh), (Ll, Lh) = enclosure()
    print("t in [%s, %s]" % (tl, th))
    print("L in [%s, %s], width %s" % (float(Ll), float(Lh), float(Lh - Ll)))
