"""Re-decide every stored row of one capture statement from its recorded minima: a row passes iff its default
cells have minimum >= Gamma and each class's cells have minimum >= Gamma * threshold (exact integers);
compare with the stored flag; compare Python and Node slice rows field by field (timing fields excepted).
usage: frame0917.py STATEMENT_DIR"""
import sys, os, json, glob
from fractions import Fraction as Fr
d = sys.argv[1]
cl = json.load(open(os.path.join(d, 'classes.json'))); c = json.load(open(os.path.join(d, 'certificate.json')))
G = c['minimum_units']; thr = {k['name']: Fr(k['threshold']) for k in cl['classes']}
rows = {}; same = total = 0
for f in sorted(glob.glob(os.path.join(d, 'slices', '*', 'py.json'))):
    py = json.load(open(f)); nd = json.load(open(f.replace('py.json', 'node.json')))
    for a, b in zip(py['rows'], nd['rows']):
        total += 1
        same += {k: v for k, v in a.items() if k not in ('cpu_seconds', 'seconds')} == {k: v for k, v in b.items() if k not in ('cpu_seconds', 'seconds')}
    for r in py['rows']:
        assert r['interval'] not in rows; rows[r['interval']] = r
assert sorted(rows) == list(range(len(c['entries'])))
mism = 0; tight = None
for i, r in rows.items():
    ok = r['default']['cells'] == 0 or r['default']['minimum_units'] >= G
    for k in r['classes']:
        if k['cells']:
            t = thr[k['name']]; ok = ok and k['minimum_units']*t.denominator >= t.numerator*G
            m = Fr(k['minimum_units']) - t*G
            tight = m if tight is None or m < tight else tight
    mism += (ok != r['passed']) or not ok
print('rows', len(rows), '; re-decided mismatches or failures:', mism, '; tightest class margin (units):', float(tight))
print('python/node rows identical:', same, 'of', total)
