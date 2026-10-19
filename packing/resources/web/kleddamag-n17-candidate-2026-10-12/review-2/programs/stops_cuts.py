"""The physical stop theorem (stop-proof.md) at both radii, against the cuts stated for each.

Added on 13 October 2026, after the second adversarial review, to correct `stops_eps.py`
(review A of jlevy/squares#577, finding A2). `stops_eps.py` is kept as run. At
eps = 501/100000 it compared b and b + z with the root-scale cuts -17/50000 and 3/125, not
with P096's raw cuts, and it bounded z by adding 17/50000 to the b + z bound, which is a
bound only where b >= -17/50000 holds. That is true at 1/5000 and false at 501/100000.

This program keeps `stops_eps.py`'s option audit and bounds unchanged and changes two
things:
 1. z is bounded from the b bound computed at the same radius: z <= (b + z)_hi - b_lo;
 2. each radius is compared with its own stated cuts:
      eps = 1/5000       (stop-proof.md, root scale):  b >= -17/50000,  b + z <= 3/125,   z <= 1/40
      eps = 501/100000   (PROOF.md P096, raw cuts):    b >= -213/25000, b + z <= 49/2000, z <= 33/1000

The domain is `stops_eps.py`'s: exact-root reference, padded slider box, every core
coordinate |h_j| <= eps. The margins printed are exact rationals, shown as floats, and
P096's transfer errors are below 10^-16.

usage: stops_cuts.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import rows as R

CUTS = (
    (Fr(1, 5000), 'root-scale cuts of stop-proof.md', Fr(-17, 50000), Fr(3, 125), Fr(1, 40)),
    (Fr(501, 100000), 'raw cuts of PROOF.md P096', Fr(-213, 25000), Fr(49, 2000), Fr(33, 1000)),
)


def fr_str(x):
    return f'{x.numerator}/{x.denominator}'


def main():
    geo = R.Geo()
    PAD = Fr(1, 10**12)
    box = [(Fr(-1), Fr(1))]*51 + [(Fr(-1), Fr(0))]
    for j in R.DUMMY:
        box[j] = (Fr(0), Fr(0))
    box[2] = (Fr(0), Fr(8, 25) + PAD); box[21] = (Fr(-1, 20) - PAD, Fr(1, 5) + PAD); box[25] = (Fr(-1, 5) - PAD, Fr(3, 40) + PAD)
    sqrt2 = Fr(14143, 10000)
    c, s, T = geo.aux['c'], geo.aux['s'], geo.aux['T']
    f = R.geom.to_fr
    cps = c + s; c1s = c*(1 - s); cms = c - s
    assert f(cps.b) < Fr(141, 100)
    assert max(abs(f(c1s.a)), abs(f(c1s.b))) < Fr(277, 1000)
    assert max(abs(f(cms.a)), abs(f(cms.b))) < Fr(129, 1000)
    print('c+s < 141/100, |c(1-s)| < 277/1000, |c-s| < 129/1000 at the root: True')
    T3 = T/3
    every = True
    for eps, name, b_cut, bz_cut, z_cut in CUTS:
        print(f'eps = {fr_str(eps)}, against the {name}')
        for (l, r) in ((9, 11), (11, 13)):
            d0, wv = R.ref_diff(geo, l, r, box)
            Dmax = R.dnorm_upper(geo, l, r, box)
            dr = R.diff_disp_norm(geo, l, r, box)
            alive = []
            for o in (l, r):
                t = r if o == l else l
                for ax in (0, 1):
                    for sg in (1, -1):
                        n = tuple(sg*x for x in geo.axis(o, ax))
                        nd = R.dot(n, d0)
                        for idx, vec in wv.items():
                            nd = nd + R.dot(n, vec)*R.box_iv(box, idx)
                        sup = max(R.dot(n, geo.corner(t, c)).a for c in range(4))
                        upper = f(nd.b) + eps*Dmax + eps*dr - Fr(1, 2) - f(sup) + sqrt2*eps
                        if upper >= 0:
                            alive.append((o, ax, sg))
            only_minus_v = alive == [(l, 1, -1), (r, 1, -1)]
            every = every and only_minus_v
            print('  pair', (l, r), 'retained options', alive, '; only the two -v options:', only_minus_v)
        Xmax9 = Fr(277, 1000) + eps + Fr(141, 100)*eps
        b_lo = -(Fr(141, 100)*eps + eps*Xmax9)
        Xmax13 = Fr(129, 1000) + 2*eps
        bz_hi = f(T3.b) + eps*Xmax13
        z_hi = bz_hi - b_lo
        N9 = 1 + box[21][0] - Fr(141, 100)*eps
        N13 = 1 + f(T3.a) - box[21][1] - box[25][1]
        for label, bound, cut, margin in (
            ('b     >=', b_lo, b_cut, b_lo - b_cut),
            ('b + z <=', bz_hi, bz_cut, bz_cut - bz_hi),
            ('z     <=', z_hi, z_cut, z_cut - z_hi),
        ):
            ok = margin > 0
            every = every and ok
            print(f'  {label} {float(bound):.10f}  against {fr_str(cut)}: {ok}  (margin {float(margin):.4e})')
        positive = N9 > 0 and N13 > 0
        every = every and positive
        print(f'  N(9,11) >= {float(N9):.12f}, N(11,13) >= {float(N13):.12f}, both positive: {positive}')
    print('all six stated cuts follow, with only the two -v options retained at both radii:', every)
    return 0 if every else 1


if __name__ == '__main__':
    sys.exit(main())
