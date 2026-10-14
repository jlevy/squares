"""Recompute the budget of every capture certificate from its features (fixed-image shape) or its point and
threshold orbits (symmetric shape), with the capacities of the class-row lemma: a threshold feature counts
floor(sum of coefficients / threshold) times its weight, a winning-mask feature once; a point orbit counts its
orbit size times its weight. Compare with budget_units and report the surplus bound*minimum - budget.
usage: budgets.py STATEMENTS_DIR"""
import sys, os, json, glob
from fractions import Fraction as Fr
root = sys.argv[1]
bad = []; rows = []
for d in sorted(glob.glob(os.path.join(root, '*'))):
    c = json.load(open(os.path.join(d, 'certificate.json')))
    cl = json.load(open(os.path.join(d, 'classes.json')))
    if 'features' in c:
        b = sum(f['weight']*(1 if f.get('winning_masks') else sum(f.get('coefficients', [1]*len(f['sites'])))//f.get('threshold', 1))
                for f in c['features'])
    else:
        LD = int(Fr(c['L'])*c.get('coordinate_denominator', 100000))
        b = 0
        for x, y, w in c['point_orbits']:
            b += w*len({(a, bb) for u, v in [(x, y), (y, x)] for a in (u, LD - u) for bb in (v, LD - v)})
        for e in c['threshold_orbits']:
            g = e['sets']
            b += e['weight']*len(g)*(1 if e.get('winning_masks') else sum(e.get('coefficients', [1]*len(g[0])))//e.get('threshold', 2))
    if b != c['budget_units']:
        bad.append(os.path.basename(d))
    s = Fr(cl['bound'])*c['minimum_units'] - b
    rows.append((s, os.path.basename(d), float(s/(Fr(cl['bound'])*c['minimum_units']))))
rows.sort()
print('statements', len(rows), '; budgets differing from budget_units:', bad)
print('smallest surpluses (units):', [(float(s), n) for s, n, _ in rows[:3]], '; largest:', [(float(s), n) for s, n, _ in rows[-1:]])
print('relative surplus range: %.2e to %.2e' % (min(r for _, _, r in rows), max(r for _, _, r in rows)))
print('all strict:', all(s > 0 for s, _, _ in rows))
