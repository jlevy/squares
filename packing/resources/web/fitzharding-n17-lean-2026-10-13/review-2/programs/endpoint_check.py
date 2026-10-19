"""Independent re-derivation of the endpoint constant and the header frames.

Reads EndpointRootData.lean as text (the polynomials and the midpoint), solves the
two-variable system with mpmath Newton iteration at 80 digits from a crude start,
compares with the declared midpoint, computes side = (6+4t)/(1+2t-t^2), and compares
the two header frames of HalfPlaneFrameBounds.lean with L and U = 1169/250.
Nothing here executes any source; the Lean files are read as data only.
"""
import re
import sys
from fractions import Fraction
from pathlib import Path

import mpmath as mp

mp.mp.dps = 80
src = Path(sys.argv[1])
text = (src / "Sq17Lean/EndpointRootData.lean").read_text()


def terms(name):
    block = re.search(rf"def {name} : List Term := \[(.*?)\]", text, re.S).group(1)
    out = []
    for m in re.finditer(r"⟨(\d+),(\d+),\(?(-?\d+)(?:/(\d+))?\)?⟩", block):
        i, j, num, den = m.groups()
        out.append((int(i), int(j), Fraction(int(num), int(den or 1))))
    return out


p0 = terms("polynomial0")
p1 = terms("polynomial1")
mid = re.search(r"def midpoint : ℚ × ℚ := \(\((\d+)/(\d+)\),\((\d+)/(\d+)\)\)", text)
m1 = Fraction(int(mid.group(1)), int(mid.group(2)))
m2 = Fraction(int(mid.group(3)), int(mid.group(4)))
print("polynomial0 terms:", [(i, j, str(c)) for i, j, c in p0])
print("polynomial1 terms:", [(i, j, str(c)) for i, j, c in p1])


def ev(poly, x, y):
    return sum(mp.mpf(c.numerator) / c.denominator * x**i * y**j for i, j, c in poly)


def jac(poly, x, y):
    dx = sum(mp.mpf(c.numerator) / c.denominator * i * x ** (i - 1) * y**j for i, j, c in poly if i)
    dy = sum(mp.mpf(c.numerator) / c.denominator * j * x**i * y ** (j - 1) for i, j, c in poly if j)
    return dx, dy


# crude start far from the declared midpoint, in the box t in [0.36,0.37], beta in [0.33,0.34]
x, y = mp.mpf("0.365"), mp.mpf("0.335")
for _ in range(60):
    f0, f1 = ev(p0, x, y), ev(p1, x, y)
    a, b = jac(p0, x, y)
    c, d = jac(p1, x, y)
    det = a * d - b * c
    dx = (d * f0 - b * f1) / det
    dy = (a * f1 - c * f0) / det
    x, y = x - dx, y - dy
print("my root t    =", mp.nstr(x, 65))
print("my root beta =", mp.nstr(y, 65))
tm = mp.mpf(m1.numerator) / m1.denominator
bm = mp.mpf(m2.numerator) / m2.denominator
print("declared mid t    =", mp.nstr(tm, 65))
print("declared mid beta =", mp.nstr(bm, 65))
print("|t - mid|    =", mp.nstr(abs(x - tm), 5), "  |beta - mid| =", mp.nstr(abs(y - bm), 5))
print("residuals at my root:", mp.nstr(ev(p0, x, y), 5), mp.nstr(ev(p1, x, y), 5))
L = (6 + 4 * x) / (1 + 2 * x - x * x)
print("L = side =", mp.nstr(L, 40))
U = mp.mpf(1169) / 250
print("U - L =", mp.nstr(U - L, 12), " (U - L)/2 =", mp.nstr((U - L) / 2, 12))

# Frames from HalfPlaneFrameBounds.lean
ordinary_side = mp.mpf(2632353982198055) / 562949953421312
padding = mp.mpf(4951760157141521) / mp.mpf(4951760157141521099596496896)
cn_side = mp.mpf(5264178896829249) / 1125899906842624
cn_sigma = mp.mpf(8668243015428611) / mp.mpf(36893488147419103232)
print("padding =", mp.nstr(padding, 8), "(2^-40 =", mp.nstr(mp.mpf(2) ** -40, 8), ")")
print("ordinary.side =", mp.nstr(ordinary_side, 25), " (U+L)/2 =", mp.nstr((U + L) / 2, 25),
      " diff =", mp.nstr(ordinary_side - (U + L) / 2, 8))
print("captureNeighbour.side - L =", mp.nstr(cn_side - L, 8))
print("captureNeighbour.sigma =", mp.nstr(cn_sigma, 25), " delta(L) =", mp.nstr((U - L) / 2, 25),
      " delta(L) - sigma =", mp.nstr((U - L) / 2 - cn_sigma, 8))
# Frame.Lower: -pad <= delta L - sigma ; Frame.Upper: delta L - sigma + L <= side + pad, at L
print("neighbour Lower slack (delta-sigma+pad) =", mp.nstr((U - L) / 2 - cn_sigma + padding, 8))
print("neighbour Upper slack (side+pad-(delta-sigma+L)) =",
      mp.nstr(cn_side + padding - ((U - L) / 2 - cn_sigma + L), 8))
print("ordinary Lower slack (delta+pad) =", mp.nstr((U - L) / 2 + padding, 8))
print("ordinary Upper slack (side+pad-(delta+L)) =", mp.nstr(ordinary_side + padding - ((U - L) / 2 + L), 8))
# container side in the neighbour frame
print("neighbour container side (side+2pad) - L =", mp.nstr(cn_side + 2 * padding - L, 8))
print("ordinary container side (side+2pad) - L =", mp.nstr(ordinary_side + 2 * padding - L, 8))
r = mp.mpf(884279719004579) / 1125899906842624
print("initialAngleRadius =", mp.nstr(r, 25), " pi/4 =", mp.nstr(mp.pi / 4, 25), " diff =", mp.nstr(r - mp.pi / 4, 6))
# Sharp enclosure claims
print("side_decimal_bounds: 4.6755300936045509 <= L <= 4.6755300936045510 ?",
      mp.mpf("4.6755300936045509") <= L <= mp.mpf("4.6755300936045510"))
lo = mp.mpf(2337765046802275475291744012927) / mp.mpf(500000000000000000000000000000)
hi = mp.mpf(4675530093604550952684734515111) / mp.mpf(1000000000000000000000000000000)
print("side_sharp_bounds hold?", lo <= L <= hi, " width", mp.nstr(hi - lo, 5))
