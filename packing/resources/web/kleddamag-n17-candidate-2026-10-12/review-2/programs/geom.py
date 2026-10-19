"""Independent exact-root geometry for the 17-square layout (second adversarial review, think-4j3n).

Written from STATEMENT.md (F, G, t0, b0) and UPPER_FORMULAS.md (layout), relabelled to the capture
labels (construction labels (1,5,2,6,3,7,4,8,9,...,17) for capture labels 1..17). No producer code is
imported. Root: Newton in mpmath at high precision, then a Krawczyk test in mpmath interval arithmetic
(outward rounding) on a small box, which proves existence and uniqueness in that box.
"""
from fractions import Fraction as Fr
import mpmath
from mpmath import mp, iv

DPS = 160
mp.dps = DPS
iv.dps = DPS

T0 = Fr(362043893314323383453621978739944164218293243036741520638379, 10**60)
B0 = Fr(330948674722739910429808533282915634174672003999685385633441, 10**60)


def F(t, b):
    return t - 3*t**2 - t**3 - t**4 + (1 - t - t**4 + t**5)*b + (-3*t + t**2 - t**3 - t**4)*b**2


def G(t, b):
    return (-2*t**3 - 2*t**4 + (-1 + 3*t - 4*t**2 + t**4 + t**5)*b + (4 - 2*t - 2*t**2 + 2*t**3 - 2*t**4)*b**2
            + (-1 - 5*t + 4*t**2 + t**4 + t**5)*b**3 + (2*t + 2*t**2)*b**4)


def jac(t, b, h=None):
    # analytic partial derivatives
    Ft = 1 - 6*t - 3*t**2 - 4*t**3 + (-1 - 4*t**3 + 5*t**4)*b + (-3 + 2*t - 3*t**2 - 4*t**3)*b**2
    Fb = (1 - t - t**4 + t**5) + 2*(-3*t + t**2 - t**3 - t**4)*b
    Gt = (-6*t**2 - 8*t**3 + (3 - 8*t + 4*t**3 + 5*t**4)*b + (-2 - 4*t + 6*t**2 - 8*t**3)*b**2
          + (-5 + 8*t + 4*t**3 + 5*t**4)*b**3 + (2 + 4*t)*b**4)
    Gb = ((-1 + 3*t - 4*t**2 + t**4 + t**5) + 2*(4 - 2*t - 2*t**2 + 2*t**3 - 2*t**4)*b
          + 3*(-1 - 5*t + 4*t**2 + t**4 + t**5)*b**2 + 4*(2*t + 2*t**2)*b**3)
    return Ft, Fb, Gt, Gb


def newton_root():
    t, b = mp.mpf(T0.numerator)/T0.denominator, mp.mpf(B0.numerator)/B0.denominator
    for _ in range(12):
        f, g = F(t, b), G(t, b)
        a11, a12, a21, a22 = jac(t, b)
        det = a11*a22 - a12*a21
        dt = (a22*f - a12*g)/det
        db = (-a21*f + a11*g)/det
        t, b = t - dt, b - db
    return t, b


def krawczyk(t, b, rad):
    """Krawczyk test on the box [t-rad,t+rad] x [b-rad,b+rad]; returns True if K(X) is inside int(X)."""
    a11, a12, a21, a22 = jac(t, b)
    det = a11*a22 - a12*a21
    Y = [[a22/det, -a12/det], [-a21/det, a11/det]]  # approximate inverse (point values)
    X = [iv.mpf([t - rad, t + rad]), iv.mpf([b - rad, b + rad])]
    tc, bc = iv.mpf(t), iv.mpf(b)
    fc = [F(tc, bc), G(tc, bc)]
    J11, J12, J21, J22 = jac(X[0], X[1])
    Jx = [[J11, J12], [J21, J22]]
    Yi = [[iv.mpf(Y[i][j]) for j in range(2)] for i in range(2)]
    centre = [tc, bc]
    K = []
    for i in range(2):
        val = centre[i] - (Yi[i][0]*fc[0] + Yi[i][1]*fc[1])
        for j in range(2):
            m = (1 if i == j else 0) - (Yi[i][0]*Jx[0][j] + Yi[i][1]*Jx[1][j])
            val = val + m*(X[j] - centre[j])
        K.append(val)
    inside = all(X[i].a < K[i].a and K[i].b < X[i].b for i in range(2))
    return inside, K


def to_fr(x):
    """mpf (or degenerate interval endpoint) -> Fraction exactly; refuses inf/nan."""
    y = mpmath.mpf(x)
    if not mpmath.isfinite(y):
        raise ValueError('non-finite value')
    sign, man, exp, _ = y._mpf_
    v = Fr(int(man)) * (Fr(2)**exp if exp >= 0 else Fr(1, 2**(-exp)))
    return -v if sign else v


def layout(t, b, one=1):
    """Capture-label layout (index 0..16 for labels 1..17); returns side, centres, first axes."""
    half = one/2
    c = (1 - t*t)/(1 + t*t); s = 2*t/(1 + t*t)
    d = (1 - b*b)/(1 + b*b); e = 2*b/(1 + b*b)
    side = (6 + 4*t)/(1 + 2*t - t*t)
    h = (c + s)/2
    x = half + (2 + c*s + 3*s - s*side)/c
    y = 3*half + (2 + 3*c - c*side)/s
    aa = d*(x + half) - e*(side - 1) + half
    bb = (d + e)*(side - 1) - half
    u10, v10 = 3*half + c*s + 2*s, c*(side - 1) - s - half
    u11, v11 = c + 2*s + half, 2*c + (c*c - s*s)/2 - 1
    u12, v12 = u11 + 1, v10 - 1
    u13 = 2*c + s + half
    u14, v14 = u13 + 1, v10 - 2
    r, hh = side - 3*half, v11 - 1
    slack = c*(c + 4 - side)
    lam6, lam13 = r - slack/(3*s), hh - slack/3
    rot = lambda uu, vv: (c*uu - s*vv, s*uu + c*vv)
    con = {1: (half, half), 2: (3*half, half), 3: (half, 3*half), 4: (half, side - half),
           5: (side - half, half), 6: (lam6, half), 7: (side - half, 3*half), 8: (side - half, side - half),
           9: (h, 2 + h), 10: rot(u10, v10), 11: rot(u11, v11), 12: rot(u12, v12), 13: rot(u13, lam13),
           14: rot(u14, v14), 15: (x, side - half), 16: (d*aa + e*bb, -e*aa + d*bb), 17: (side - half, y)}
    caxis = {k: (one*1, one*0) for k in range(1, 18)}
    for k in range(9, 15):
        caxis[k] = (c, s)
    caxis[16] = (d, -e)
    perm = (1, 5, 2, 6, 3, 7, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17)  # capture label i -> construction label
    pts = [con[perm[i]] for i in range(17)]
    axes = [caxis[perm[i]] for i in range(17)]
    return side, pts, axes, dict(c=c, s=s, d=d, e=e, T=slack)


if __name__ == '__main__':
    t, b = newton_root()
    print('t* =', mpmath.nstr(t, 70))
    print('b* =', mpmath.nstr(b, 70))
    print('|F|,|G| at Newton point:', mpmath.nstr(abs(F(t, b)), 5), mpmath.nstr(abs(G(t, b)), 5))
    for rad in (mp.mpf(10)**-100, mp.mpf(10)**-12):
        ok, K = krawczyk(t, b, rad)
        print('Krawczyk radius', mpmath.nstr(rad, 3), 'inside:', ok)
    side, pts, axes, aux = layout(t, b)
    print('L =', mpmath.nstr(side, 40))
    print('distance of Newton point from (t0,b0):', mpmath.nstr(t - mp.mpf(T0.numerator)/T0.denominator, 5),
          mpmath.nstr(b - mp.mpf(B0.numerator)/B0.denominator, 5))
