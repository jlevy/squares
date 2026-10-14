"""Option audit at the finite entry: positions <= 1/200, independent angles <= 1/400 rad, sliders a in [0,8/25],
b in [-1/20,1/5], z in [-1/5,3/40] (unpadded). Exact-root reference (the rational reference differs by < 1e-16,
paid by a 1e-12 allowance). Bound: max_w n.d(w) + rp*dr + ra*(D + rp*dr) + sqrt(2)*ra - 1/2 - max_v n.v + 1e-12."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import rows as R

def main():
    geo = R.Geo()
    rp, ra = Fr(1, 200), Fr(1, 400)
    box = [(Fr(-1), Fr(1))]*51 + [(Fr(-1), Fr(0))]
    for j in R.DUMMY:
        box[j] = (Fr(0), Fr(0))
    box[2] = (Fr(0), Fr(8, 25)); box[21] = (Fr(-1, 20), Fr(1, 5)); box[25] = (Fr(-1, 5), Fr(3, 40))
    sqrt2 = Fr(14143, 10000)
    total = 0; worst = None; retained = {}
    for (l, r) in R.PAIRS:
        d0, wv = R.ref_diff(geo, l, r, box)
        Dmax = R.dnorm_upper(geo, l, r, box)
        dr = R.diff_disp_norm(geo, l, r, box)    # normalized unit box -> scale by rp
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
                    upper = (R.geom.to_fr(nd.b) + rp*dr + ra*(Dmax + rp*dr) + sqrt2*ra - Fr(1, 2)
                             - R.geom.to_fr(sup) + Fr(1, 10**12))
                    if upper >= 0:
                        alive.append((o, ax, sg))
                    elif worst is None or upper > worst[0]:
                        worst = (upper, (l, r, o, ax, sg))
        retained[(l, r)] = alive; total += len(alive)
    print('finite entry: retained', total, 'excluded', 152 - total)
    print('largest excluded upper bound', float(worst[0]), worst[1])
    print(retained)

main()
