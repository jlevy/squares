"""The Lebesgue credit of a leaf, exactly: horizontal strips of height h, each inside the Lebesgue
rectangle and inside the closed unit square of every admissible pose of the leaf box.

A point p lies in the square of centre c and angle theta = 2 arctan u iff
    |(p - c) . (cos, sin)| <= 1/2  and  |(p - c) . (-sin, cos)| <= 1/2;
times 1 + u^2 > 0 each side is a polynomial of degree 2 in u, affine in c, so it holds for every centre
of the box and every u of the bin iff it holds at the four corners of the box, checked by Bernstein
on [U0/R, U1/R] (`lemmae_mirror.check`, the kernel's test).  The square is convex, so a strip whose
four corners pass lies in every square; the strips are disjoint, so their areas add up to a lower
bound of the Lebesgue mass of every admissible square (density 1).

    credit(box, U0, U1, R, rect, h) -> (strips [(xa, xb, yb)], area)   (all Fractions; strip
    [xa, xb] x [yb, yb + h])
"""
from fractions import Fraction as Fr
from math import lcm

from lemmae_mirror import check

HALF = Fr(1, 2)


def corner_ok(p, box, U0, U1, R):
    """p in the square of every centre of `box` = (x0, x1, y0, y1) and every u in [U0/R, U1/R]"""
    for cx in (box[0], box[1]):
        for cy in (box[2], box[3]):
            dx, dy = p[0] - cx, p[1] - cy
            for q in ((HALF - dx, -2 * dy, HALF + dx), (HALF + dx, 2 * dy, HALF - dx),
                      (HALF - dy, 2 * dx, HALF + dy), (HALF + dy, -2 * dx, HALF - dy)):
                L = lcm(*(x.denominator for x in q))
                if not check([int(x * L) for x in q], 2, U0, U1, R):
                    return False
    return True


def _interval(y, box, U0, U1, R, xlo, xhi, hx):
    """the grid points x = xlo + k hx in [xlo, xhi] with (x, y) in the core: an interval (the core is
    convex), found from a passing column outwards; None if no column passes"""
    n = int((xhi - xlo) / hx)
    if n < 0:
        return None
    ok = lambda k: corner_ok((xlo + k * hx, y), box, U0, U1, R)
    # a passing column: the box centre first, then a scan (the passing set is an interval)
    xm = (box[0] + box[1]) / 2
    km = max(0, min(n, int((xm - xlo) / hx)))
    if not ok(km):
        step = max(1, n // 256)
        km = next((k for k in range(0, n + 1, step) if ok(k)), None)
        if km is None:
            return None
    lo, hi = 0, km            # smallest passing k in [lo, km]
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid): hi = mid
        else: lo = mid + 1
    a = lo
    lo, hi = km, n            # largest passing k in [km, n]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid): lo = mid
        else: hi = mid - 1
    return xlo + a * hx, xlo + lo * hx


def credit(box, U0, U1, R, rect, h=Fr(1, 256), hx=None):
    """box: centre box (x0, x1, y0, y1) as Fractions; rect: (X0, Y0, X1, Y1) as Fractions"""
    hx = hx or h / 8
    reach = Fr(7072, 10000)
    ylo = max(rect[1], box[3] - reach); yhi = min(rect[3], box[2] + reach)
    xlo = max(rect[0], box[1] - reach); xhi = min(rect[2], box[0] + reach)
    if ylo >= yhi or xlo >= xhi:
        return [], Fr(0)
    # grid aligned at multiples of h (and hx)
    import math
    yb = Fr(math.ceil(ylo / h)) * h
    xlo = Fr(math.ceil(xlo / hx)) * hx
    cache = {}
    def iv(y):
        if y not in cache:
            cache[y] = _interval(y, box, U0, U1, R, xlo, xhi, hx)
        return cache[y]
    strips, area = [], Fr(0)
    while yb + h <= yhi:
        a, b = iv(yb), iv(yb + h)
        if a and b:
            xa, xb = max(a[0], b[0]), min(a[1], b[1])
            if xa < xb:
                strips.append((xa, xb, yb))
                area += (xb - xa) * h
        yb += h
    return strips, area
