#!/usr/bin/env python3
"""Independent exact sanity checks of a mixed cover file (written from scratch, no shared code with the checkers).
Checks: format, s = 7, every point in [0,s]^2, positive integer weights, segments axis-parallel inside [0,s]^2,
exact total weight (as a Fraction) < n, and D4 invariance of the measure (as multisets, segments merged per line).
usage: sanity.py FILE N"""
import sys
from fractions import Fraction as F
from collections import Counter

path, N = sys.argv[1], int(sys.argv[2])
L = [l.split() for l in open(path) if l.strip() and not l.startswith('#')]
assert L[0] == ['mixed', '1'], L[0]
s = F(int(L[1][0]), int(L[1][1])); D = int(L[2][0]); W = int(L[3][0])
i = 4; npt = int(L[i][0]); i += 1
pts = [tuple(map(int, L[i + k])) for k in range(npt)]; i += npt
nsg = int(L[i][0]); i += 1
sgs = [tuple(map(int, L[i + k])) for k in range(nsg)]; i += nsg
npg = int(L[i][0]); i += 1
assert npg == 0 and i == len(L), (npg, i, len(L))
S = s * D; assert S.denominator == 1; S = int(S)
K = int(sys.argv[3]) if len(sys.argv) > 3 else 7
assert s == K, s
for x, y, w in pts:
    assert 0 <= x <= S and 0 <= y <= S and w > 0, (x, y, w)
for x0, y0, x1, y1, w in sgs:
    assert w > 0 and (x0 == x1 or y0 == y1) and min(x0, x1, y0, y1) >= 0 and max(x0, x1, y0, y1) <= S
tp = sum(w for *_, w in pts); ts = sum(w for *_, w in sgs)
tot = F(tp + ts, W)
print(f's = {s}, D = {D}, W = {W}, points {npt}, segments {nsg}')
print(f'total weight = {tot} = {float(tot):.12f}  (points {float(F(tp, W)):.6f}, segments {float(F(ts, W)):.6f})')
print('total < N:', tot < N)

# D4 invariance.  Points: multiset of (x, y, w).  Segments: measure density per unit length on each line, as a
# piecewise-constant function; compare the merged step functions under the 8 symmetries.
def maps():
    for sw in (False, True):
        for fx in (False, True):
            for fy in (False, True):
                def g(x, y, sw=sw, fx=fx, fy=fy):
                    if fx: x = S - x
                    if fy: y = S - y
                    if sw: x, y = y, x
                    return x, y
                yield g

P0 = Counter(pts)
ok = True
for g in maps():
    P1 = Counter((*g(x, y), w) for x, y, w in pts)
    if P1 != P0: ok = False
print('points D4-invariant:', ok)

def seg_density(sgs):
    # line key -> Counter of (t0, t1) -> density (exact Fraction, weight per unit length)
    out = {}
    for x0, y0, x1, y1, w in sgs:
        if x0 == x1: key = ('v', x0); a, b = sorted((y0, y1))
        else: key = ('h', y0); a, b = sorted((x0, x1))
        out.setdefault(key, []).append((a, b, F(w, b - a)))
    # merge to a canonical step function on a breakpoint grid
    canon = {}
    for key, ivs in out.items():
        bk = sorted(set([a for a, _, _ in ivs] + [b for _, b, _ in ivs]))
        dens = []
        for p, q in zip(bk, bk[1:]):
            d = sum(r for a, b, r in ivs if a <= p and q <= b)
            dens.append((p, q, d))
        # drop zero pieces, merge equal neighbors
        m = []
        for p, q, d in dens:
            if d == 0: continue
            if m and m[-1][1] == p and m[-1][2] == d: m[-1] = (m[-1][0], q, d)
            else: m.append((p, q, d))
        canon[key] = tuple(m)
    return canon

C0 = seg_density(sgs); okS = True
for g in maps():
    img = []
    for x0, y0, x1, y1, w in sgs:
        a = g(x0, y0); b = g(x1, y1); img.append((a[0], a[1], b[0], b[1], w))
    if seg_density(img) != C0: okS = False
print('segments D4-invariant (as measures):', okS)
lines = sorted(set(k for k in C0))
print('segment lines:', lines)
