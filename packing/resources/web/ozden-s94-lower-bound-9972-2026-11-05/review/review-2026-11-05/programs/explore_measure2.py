"""Exploratory: D4 expansion and density profile (decides nothing)."""
import gzip, json, sys
from gmpy2 import mpq
from collections import Counter, defaultdict

path = sys.argv[1]
cert = json.loads(gzip.open(path, 'rb').read())
L = mpq(cert['L'])
rows = [(mpq(r['mass']), [mpq(v) for v in r['rectangle']]) for r in cert['rectangles']]
def images(x1, y1, x2, y2):
    out = []
    for (a1, a2, b1, b2) in [(x1, x2, y1, y2), (y1, y2, x1, x2)]:
        for fx in (False, True):
            for fy in (False, True):
                X = (L - a2, L - a1) if fx else (a1, a2)
                Y = (L - b2, L - b1) if fy else (b1, b2)
                out.append((X[0], Y[0], X[1], Y[1]))
    return out
exp = defaultdict(lambda: mpq(0))
for w, (x1, y1, x2, y2) in rows:
    area = (x2 - x1) * (y2 - y1)
    for im in images(x1, y1, x2, y2):
        exp[im] += w / 8 / area      # density contributed by this image
tot = sum(d * (k[2] - k[0]) * (k[3] - k[1]) for k, d in exp.items())
print('expanded distinct rectangles', len(exp), 'integrated mass == total_mass:', tot == mpq(cert['total_mass']), float(tot))
dens = sorted(float(d) for d in exp.values())
print('density min/median/max', dens[0], dens[len(dens)//2], dens[-1])
ws = sorted(float(k[2]-k[0]) for k in exp); hs = sorted(float(k[3]-k[1]) for k in exp)
thin = sum(1 for k in exp if min(k[2]-k[0], k[3]-k[1]) < mpq(1, 100))
print('thin (<0.01) rectangles', thin)
print('width quantiles', [round(ws[int(q*(len(ws)-1))], 6) for q in (0, .1, .5, .9, 1)])
# representative-row geometry
mass_by_kind = Counter()
for w, (x1, y1, x2, y2) in rows:
    mind = min(x2 - x1, y2 - y1)
    kind = 'strip' if mind < mpq(1, 100) else 'block'
    mass_by_kind[kind] += float(w)
print('orbit mass by kind', dict(mass_by_kind))
# distinct x-coordinates of expanded rectangles' edges
xs = set(); ys = set()
for k in exp:
    xs.update((k[0], k[2])); ys.update((k[1], k[3]))
print('distinct edge x', len(xs), 'edge y', len(ys))
# denominators
from math import lcm
dx = 1
for x in xs:
    dx = lcm(dx, int(x.denominator))
print('lcm of edge-coordinate denominators bits', dx.bit_length())
dm = 1
for d in exp.values():
    dm = lcm(dm, int(d.denominator))
print('lcm of density denominators bits', dm.bit_length())
