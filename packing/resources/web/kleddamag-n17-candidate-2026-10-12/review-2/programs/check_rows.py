"""Check the producer's stored normalized models against my independent row derivation.

usage: check_rows.py LABELS_JSON ROUND_DIR [ROUND_DIR ...]

For every stored round (round.json with incoming_bounds, model.json with 245 rows), and every one of the 52
geometric rows, verify with exact rationals that the producer's row  a_p . x >= b_p  is IMPLIED on the incoming
box by my independently derived necessary inequality  a_true . x + rem >= 0,  |rem| <= E_mine, a_true in my
coefficient enclosure:
      b_p <= -E_mine - sum_j max(|a_p,j - lo_j|, |a_p,j - hi_j|) * radius_j .
Also checks: the base gap and slider coefficients of every row are zero to 1e-90 (numerical, at the
Krawczyk-verified root box), the 192 product rows are exactly the McCormick rows of the incoming box (up to
the producer's coefficient grid, again checked as an implication), the extra row is -x21-x25 >= -3/125.
Reads JSON data only.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
import rows as R

NORMALS = {}


def main():
    labels = json.load(open(sys.argv[1]))['new_labels']
    audit = json.load(open(sys.argv[2]))['retained']
    for key, opts in audit.items():
        l, r = map(int, key.split('-'))
        axes = {(a, s) for _, a, s in opts}
        assert len(axes) == 1
        NORMALS[(l, r)] = next(iter(axes))
    geo = R.Geo()
    worst_margin = None
    for rd in sys.argv[3:]:
        rnd = json.load(open(os.path.join(rd, 'round.json')))
        model = json.load(open(os.path.join(rd, 'model.json')))
        box = [tuple(map(Fr, v)) for v in rnd['incoming_bounds']]
        mine = R.build_rows(geo, labels, box, NORMALS)
        assert [r['label'] for r in model[:52]] == labels
        maxdiff = Fr(0)
        for row, prod in zip(mine, model[:52]):
            # zero base gap and slider coefficients (numerical check at the root box)
            assert abs(R.geom.to_fr(row.base.a)) < Fr(1, 10**90) and abs(R.geom.to_fr(row.base.b)) < Fr(1, 10**90), row.label
            for j, val in row.slider.items():
                assert abs(R.geom.to_fr(val.a)) < Fr(1, 10**90) and abs(R.geom.to_fr(val.b)) < Fr(1, 10**90), (row.label, j)
            ap = {j: Fr(x) for j, x in enumerate(prod['a']) if Fr(x)}
            bp = Fr(prod['b'])
            need = row.err
            keys = set(ap) | set(row.coef)
            for j in keys:
                lo, hi = R.ivfr(row.coef[j]) if j in row.coef else (Fr(0), Fr(0))
                pj = ap.get(j, Fr(0))
                dev = max(abs(pj - lo), abs(pj - hi))
                maxdiff = max(maxdiff, dev)
                need += dev*R.bnd(box, j)
            margin = -need - bp       # must be >= 0
            if worst_margin is None or margin < worst_margin[0]:
                worst_margin = (margin, rd, row.label, float(bp), float(need))
            assert margin >= 0, (rd, row.label, float(bp), float(need))
        # product rows
        pr = R.product_rows(box)
        for (a, b), prod in zip(pr, model[52:244]):
            ap = {j: Fr(x) for j, x in enumerate(prod['a']) if Fr(x)}
            bp = Fr(prod['b'])
            need = Fr(0)
            for j in set(ap) | set(a):
                need += abs(ap.get(j, Fr(0)) - a.get(j, Fr(0)))*R.bnd(box, j)
            # my row a.x >= b holds exactly; producer row holds if bp <= b - need
            assert bp <= b - need, (rd, prod['label'])
        if len(model) == 245:
            ex = model[244]
            assert {j: Fr(x) for j, x in enumerate(ex['a']) if Fr(x)} == {21: Fr(-1), 25: Fr(-1)} and Fr(ex['b']) == Fr(-3, 125)
        print(rd, 'rows', len(model), 'all 52 geometric rows implied by my derivation; max |coef diff| =', float(maxdiff),
              '; 192 product rows implied by McCormick')
    print('smallest implication margin:', float(worst_margin[0]), worst_margin[1:])


if __name__ == '__main__':
    main()
