"""Independent option audit of the 19 retained pairs at root scale (second adversarial review, think-4j3n).

Domain (THEOREM.md of full-stopped-propagation/continuation): exact-root reference, all 45 core
coordinates |h_j| <= eps = 1/5000 (positions and the sixteen independent angles, radians), sliders in the
padded box a in [0, 8/25+1e-12], b in [-1/20-1e-12, 1/5+1e-12], z in [-1/5-1e-12, 3/40+1e-12].

For option (owner o, reference normal n = +-axis of o; other t), with d = c_r - c_l (l<r, labels):
  gap = (R(th_o) n).(c_r - c_l) - 1/2 - h_t(R(th_o) n)       [owner l: n points l->r; owner r: n = -(outward)]
Upper bound used here (my own):
  gap <= max_w n.d(w) + eps*Dmax + eps*dr - 1/2 - max_v n.v + sqrt(2)*eps
since |R(th)n - n| <= |th| <= eps, |core displacement difference| <= eps*dr, and the support of t in a direction
rotated by |th_t - th_o| <= 2 eps differs from max_v n.v by at most 2 eps |v| = sqrt(2) eps.
For owner r the separating condition is n_r'.(c_l - c_r) >= 1/2 + h with n_r' its outward normal; writing
n = -n_r' gives the same expression n.(c_r - c_l) - 1/2 - h, so all 8 options are n = +-u_o, +-Ju_o, o in {l,r}.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import json
import mpmath
from mpmath import iv
import rows as R

out = {}


def main():
    geo = R.Geo()
    PAD = Fr(1, 10**12)
    box = [(Fr(-1), Fr(1))]*51 + [(Fr(-1), Fr(0))]
    for j in R.DUMMY:
        box[j] = (Fr(0), Fr(0))
    box[2] = (Fr(0), Fr(8, 25) + PAD); box[21] = (Fr(-1, 20) - PAD, Fr(1, 5) + PAD); box[25] = (Fr(-1, 5) - PAD, Fr(3, 40) + PAD)
    box = R.refresh(box)
    eps = R.EPS
    sqrt2 = Fr(14143, 10000)
    retained = {}
    worst_excluded = None
    for (l, r) in R.PAIRS:
        d0, wv = R.ref_diff(geo, l, r, box)
        Dmax = R.dnorm_upper(geo, l, r, box)
        dr = R.diff_disp_norm(geo, l, r, box)
        alive = []
        rec = []
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
                    rec.append(dict(owner=o, axis=ax, sign=sg, upper=float(upper)))
                    if upper >= 0:
                        alive.append((o, ax, sg))
                    else:
                        if worst_excluded is None or upper > worst_excluded[0]:
                            worst_excluded = (upper, (l, r, o, ax, sg))
        retained[(l, r)] = alive
        out[f'{l}-{r}'] = dict(retained=alive, D=float(Dmax), dr=float(dr), options=rec)
    n_alive = sum(len(v) for v in retained.values())
    print('retained options:', n_alive, ' excluded:', 152 - n_alive)
    for k, v in retained.items():
        print(k, v)
    print('largest excluded upper bound:', float(worst_excluded[0]), worst_excluded[1])
    json.dump(dict(retained={f'{k[0]}-{k[1]}': v for k, v in retained.items()},
                   largest_excluded=str(worst_excluded[0]), largest_excluded_option=worst_excluded[1], detail=out),
              open(sys.argv[1], 'w'), indent=1)


if __name__ == '__main__':
    main()
