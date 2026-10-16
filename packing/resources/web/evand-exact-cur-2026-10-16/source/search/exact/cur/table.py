#!/usr/bin/env python3
"""Table of the exact forms in cur/data (2026-10-15) -> cur/RESULTS.md and cur/results.json.
Per n: S* (30 digits), p (shown when short), isolating interval, field degree, the record's credit as the store's
frontier prints it ("best known by"; pending = open register issue), and the exact form it replaces, if any
(exact_forms.json: the 10-07 table, now for a superseded packing)."""
import glob, gzip, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); EX = os.path.dirname(HERE); ROOT = os.path.abspath(os.path.join(EX, '..', '..'))
sys.path.insert(0, os.path.join(EX, 'minpoly')); from table import poly_str
fr = subprocess.run([sys.executable, os.path.join(ROOT, 'search/packer/pk.py'), 'frontier'], capture_output=True, text=True).stdout
by = {}
for l in fr.split('\n'):
    m = re.match(r'\s*(\d+)\s+([\d.]+)(\*?)\s+(.*?)\s+\d+\.\d{6,}', l)
    if m:
        name = m.group(4).strip(); pend = bool(m.group(3)) or name.endswith('*'); name = name.rstrip('*').strip()
        name = {'Nate Chaoweerapr': 'Nate Chaoweeraprasit (itsnaka)'}.get(name, name)   # frontier column width
        by[int(m.group(1))] = (name or '—') + (' (pending)' if pend else '')
old = {r['n']: r for r in json.load(open(os.path.join(EX, 'exact_forms.json')))}
cc = {r['n']: r for r in json.load(open(os.path.join(HERE, 'crosscheck.json')))}


def closed(p):
    """Quadratic c + b x + a x^2 with positive root -> 'q + r*sqrt(d)' (exact, rational q, r)."""
    from fractions import Fraction as F
    c, b, a = p; D = b * b - 4 * a * c; k, d = 1, D
    for f in range(2, int(D ** 0.5) + 2):
        while d % (f * f) == 0: d //= f * f; k *= f
    q, r = F(-b, 2 * a), F(k, 2 * a)
    return f"{q} + {r}*sqrt({d})"


rows = []
for f in sorted(glob.glob(os.path.join(HERE, 'data', 'n-*.minpoly.json.gz')), key=lambda s: int(s.split('-')[-1].split('.')[0])):
    m = json.load(gzip.open(f)); n = int(m['n']); p = [int(c) for c in m['S']['poly']]
    o = old[n]
    was = 'new (open on 10-07)' if o['status'] != 'exact' else f"replaces deg {o['S_degree']} (S = {float(o['S']):.12f}, superseded)"
    rows.append(dict(n=n, S=cc[n]['S'], S_poly_ascending=p, S_degree=len(p) - 1, S_interval=m['S']['interval'],
                     field_degree=len(m['field']['f']) - 1, closed_form=closed(p) if len(p) == 3 else None, height_digits=len(str(max(abs(c) for c in p))),
                     record_by=by.get(n, '?'), status=was, findpoly=cc[n]['findpoly'],
                     data=f'cur/data/n-{n}.minpoly.json.gz'))
json.dump(rows, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
L = ['| n | S* | deg p | p | field deg | record (frontier credit) | status |', '|---|---|---|---|---|---|---|']
for r in rows:
    ps = poly_str(r['S_poly_ascending'])
    ps = f'`{ps}`' + (f" = `{r['closed_form']}`" if r['closed_form'] else '') if len(ps) <= 110 else f"degree {r['S_degree']}, {r['height_digits']}-digit coefficients (JSON)"
    L.append(f"| {r['n']} | {r['S']} | {r['S_degree']} | {ps} | {r['field_degree']} | {r['record_by']} | {r['status']} |")
open(os.path.join(HERE, 'RESULTS.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
