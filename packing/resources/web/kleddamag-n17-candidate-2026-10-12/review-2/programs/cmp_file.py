import json, sys
from fractions import Fraction as Fr
import mpmath
from mpmath import mp
sys.path.insert(0, sys.argv[1])
import geom
mp.dps = 60
t, b = geom.newton_root()
side, pts, axes, aux = geom.layout(t, b)
d = json.load(open(sys.argv[2]))
print('Sref - L =', mpmath.nstr(mp.mpf(Fr(d['side']).numerator)/Fr(d['side']).denominator - side, 6))
c, s = aux['c'], aux['s']
for i, sq in enumerate(d['squares']):
    fx, fy = Fr(sq['x']), Fr(sq['y'])
    fx = mp.mpf(fx.numerator)/fx.denominator; fy = mp.mpf(fy.numerator)/fy.denominator
    dx, dy = fx - pts[i][0], fy - pts[i][1]
    # project on v (for square 13 the shift is along v)
    vx, vy = -axes[i][1], axes[i][0]
    print(i+1, 'dx', mpmath.nstr(dx, 6), 'dy', mpmath.nstr(dy, 6), 'v.d', mpmath.nstr(vx*dx + vy*dy, 6))
print('T/3 =', mpmath.nstr(aux['T']/3, 20), ' T/(3s) =', mpmath.nstr(aux['T']/(3*s), 20))
