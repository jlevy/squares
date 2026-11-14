#!/usr/bin/env python3
"""Exact bookkeeping for the k^2 - 5 family's 11 x 11 board (this repository; shares no code with the checkers).
Checks, in exact rational arithmetic:
  1. the board file is well formed: side 11, coordinates on the 1/10 grid, unit-length axis-parallel segments of
     positive mass inside [0,11]^2, one Lebesgue square [19/5, 36/5]^2 of density 1;
  2. D (from sol_exact.json) satisfies D > 5/4, and the total mass equals 121 - 4D;
  3. the measure is invariant under the eight symmetries of [0,11]^2 (as a multiset of weighted segments);
  4. the family file's header D equals the board's D.
usage: sanity_k2m5.py certificate/sol_exact_box11.txt certificate/sol_exact.json certificate/sol_exact_family.txt"""
import sys, json, re
from fractions import Fraction as F
from collections import Counter
box, js, fam = sys.argv[1:4]
L = open(box).read().split('\n'); i = 0
while not L[i].split() or L[i].startswith('#') or L[i].startswith('mixed'): i += 1
sn, sd = map(int, L[i].split()); pitch = int(L[i+1]); wden = int(L[i+2]); npts = int(L[i+3]); n = int(L[i+4])
assert (sn, sd) == (11, 1) and pitch == 10 and npts == 0, 'header'
segs = [tuple(map(int, L[i+5+j].split())) for j in range(n)]
for x0, y0, x1, y1, w in segs:
    assert w > 0 and min(x0, y0, x1, y1) >= 0 and max(x0, y0, x1, y1) <= 110, 'range'
    assert (x0 == x1 and abs(y1 - y0) == 1) or (y0 == y1 and abs(x1 - x0) == 1), 'unit grid segment'
rest = [l for l in L[i+5+n:] if l.strip()]
assert rest[0].split() == ['1'], 'one polygon'
v = list(map(int, rest[1].split())); assert v[0] == 4 and v[2:] == [38, 38, 72, 38, 72, 72, 38, 72], 'Lebesgue square'
area = F(72 - 38, 10) ** 2; assert F(v[1], wden) == area, 'density 1'
D = F(json.load(open(js))['D'])
tot = F(sum(s[4] for s in segs), wden) + area
print(f'segments {n}, total {tot} = {float(tot):.12f}, D = {D} = {float(D):.12f}')
assert D > F(5, 4), 'D > 5/4'
assert tot == 121 - 4*D, 'total = 121 - 4D'
def key(s):
    x0, y0, x1, y1, w = s
    return (min((x0, y0), (x1, y1)), max((x0, y0), (x1, y1)), w)
C = Counter(key(s) for s in segs)
syms = [lambda x, y: (y, x), lambda x, y: (110 - x, y), lambda x, y: (x, 110 - y)]   # generate D4
for g in syms:
    Cg = Counter(key((*g(s[0], s[1]), *g(s[2], s[3]), s[4])) for s in segs)
    assert Cg == C, 'D4 invariance'
hdr = open(fam).read()
m = re.search(r'D = (\d+)/(\d+)', hdr); assert F(int(m.group(1)), int(m.group(2))) == D, 'family D'
print('total = 121 - 4D exactly; D > 5/4 (so k^2 - 4D < k^2 - 5 for every k); D4-invariant; family file agrees')
print('SANITY-OK')
