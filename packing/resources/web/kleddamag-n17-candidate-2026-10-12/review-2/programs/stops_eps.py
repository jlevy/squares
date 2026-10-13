"""Independent check of the physical stop theorem used before the stopped rounds (stop-proof.md).

Pairs (9,11) and (11,13) on the padded exact-root domain, eps = 1/5000:
 1. option audit: of the 8 separating options of each pair, all except the two "-v" options (owner 9 or 11,
    resp. 11 or 13, normal pointing from the first to the second label = -v) have a strictly negative gap bound;
 2. for a retained -v option of owner o: 1 <= N cos th_o + X sin th_o <= N + eps |X| (N > 0), giving
    (9,11): b >= -(v.h9) - eps|X|,  |v.h9| <= (c+s) eps,  |X| <= |c(1-s)| + eps + (c+s) eps;
    (11,13): b + z <= T/3 + eps |X|,  |X| <= |c - s| + 2 eps;
 3. the stated rational consequences b >= -17/50000, b+z <= 3/125, z <= 1/40 at eps = 1/5000.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import rows as R
from mpmath import iv


def main():
    geo = R.Geo()
    PAD = Fr(1, 10**12)
    box = [(Fr(-1), Fr(1))]*51 + [(Fr(-1), Fr(0))]
    for j in R.DUMMY:
        box[j] = (Fr(0), Fr(0))
    box[2] = (Fr(0), Fr(8, 25) + PAD); box[21] = (Fr(-1, 20) - PAD, Fr(1, 5) + PAD); box[25] = (Fr(-1, 5) - PAD, Fr(3, 40) + PAD)
    eps = Fr(int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else R.EPS
    sqrt2 = Fr(14143, 10000)
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
                    upper = R.geom.to_fr(nd.b) + eps*Dmax + eps*dr - Fr(1, 2) - R.geom.to_fr(sup) + sqrt2*eps
                    if upper >= 0:
                        alive.append((o, ax, sg))
        print('pair', (l, r), 'D <', float(Dmax), 'dr <', float(dr), 'retained options', alive)
    c, s, T = geo.aux['c'], geo.aux['s'], geo.aux['T']
    f = R.geom.to_fr
    cps = c + s; c1s = c*(1 - s); cms = c - s
    print('c+s <', float(f(cps.b)), ' < 141/100:', f(cps.b) < Fr(141, 100))
    print('|c(1-s)| <', float(max(abs(f(c1s.a)), abs(f(c1s.b)))), ' < 277/1000:', max(abs(f(c1s.a)), abs(f(c1s.b))) < Fr(277, 1000))
    print('|c-s| <', float(max(abs(f(cms.a)), abs(f(cms.b)))), ' < 129/1000:', max(abs(f(cms.a)), abs(f(cms.b))) < Fr(129, 1000))
    Xmax9 = Fr(277, 1000) + eps + Fr(141, 100)*eps
    blow = -(Fr(141, 100)*eps + eps*Xmax9)
    print('b >=', float(blow), ' >= -17/50000:', blow >= Fr(-17, 50000))
    T3 = T/3
    Xmax13 = Fr(129, 1000) + 2*eps
    sumhi = f(T3.b) + eps*Xmax13
    print('b+z <=', float(sumhi), ' <= 3/125:', sumhi <= Fr(3, 125))
    zhi = sumhi + Fr(17, 50000)
    print('z <=', float(zhi), ' <= 1/40:', zhi <= Fr(1, 40))
    # N > 0 on the padded domain
    N9 = 1 + box[21][0] - (Fr(141, 100))*eps
    N13 = 1 + f(T3.a) - box[21][1] - box[25][1]
    print('N(9,11) >=', float(N9), ' N(11,13) >=', float(N13))


if __name__ == '__main__':
    main()
