"""Distinct-parent geometry of the three wall profiles (PROOF.md P044), recomputed with my own exact code.

usage: profiles.py EDITION_ROOT
For JQ, JPWS and JPW13: the seventeen targets (Q_j / PW_j / L_j literal target classes as run_adm.py selects
them, the slab target for label 11 of JPWS, and the L9 wall rectangle), each clipped to the physical centre box
[1000469/2000000, 8351531/2000000]^2 (P054); checks (1) every clipped target has squared diameter < 1
(capacity one, inscribed open disks), (2) all 136 cross-label pairs of clipped targets are disjoint as CLOSED
sets (strict separating line). Reads JSON class files only.
"""
import sys, os, json, hashlib
from fractions import Fraction as F

ROOT = sys.argv[1]
PKT = ROOT + '/research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011'
man = json.load(open(PKT + '/runtime/THEOREM_MANIFEST.json'))
BASE = {r['name']: r for r in man['base_capture_rows']}
LO, HI = F(1000469, 2000000), F(8351531, 2000000)
X0, X1, XW = F(-131, 250), F(4501, 5000), F(53, 100)
Y0, YC, Y13, Y1 = F(24137, 10000), F(129, 50), F(13, 5), F(29637, 10000)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def target(path, label):
    d = json.load(open(path))
    cs = [c for c in d['classes'] if F(c['threshold']) == 0 and any(c['name'].startswith(pre + 'label%d_' % label)
          for pre in ('PB_', 'HULLW_', 'QB_', 'HULL_', 'B_', 'T_', 'S_'))]
    assert len(cs) == 1, (path, label)
    assert len(cs[0]['slots']) == 1
    return [(F(a), F(b)) for a, b in cs[0]['slots'][0]['centre']['polygon']]


def clip(poly):
    """Sutherland-Hodgman against the square [LO,HI]^2, exact."""
    def cut(pts, inside, inter):
        out = []
        for k in range(len(pts)):
            p, q = pts[k], pts[(k + 1) % len(pts)]
            ip, iq = inside(p), inside(q)
            if ip:
                out.append(p)
            if ip != iq:
                out.append(inter(p, q))
        return out
    pts = list(poly)
    for axis, bound, keep_ge in ((0, LO, True), (0, HI, False), (1, LO, True), (1, HI, False)):
        def inside(p, axis=axis, bound=bound, keep_ge=keep_ge):
            return p[axis] >= bound if keep_ge else p[axis] <= bound

        def inter(p, q, axis=axis, bound=bound):
            t = (bound - p[axis])/(q[axis] - p[axis])
            return (p[0] + t*(q[0] - p[0]), p[1] + t*(q[1] - p[1]))
        pts = cut(pts, inside, inter)
        if not pts:
            return []
    out = []
    for p in pts:
        if not out or out[-1] != p:
            out.append(p)
    if len(out) > 1 and out[0] == out[-1]:
        out.pop()
    return out


def diam2(poly):
    return max((a[0] - b[0])**2 + (a[1] - b[1])**2 for a in poly for b in poly)


def strictly_separated(P, Q):
    """closed convex polygons P, Q (vertex lists) are disjoint iff some edge normal of P or Q strictly separates."""
    for A, B in ((P, Q), (Q, P)):
        n = len(A)
        for k in range(n):
            a, b = A[k], A[(k + 1) % n]
            nx, ny = b[1] - a[1], a[0] - b[0]
            pa = [nx*p[0] + ny*p[1] for p in A]; pb = [nx*p[0] + ny*p[1] for p in B]
            if max(pa) < min(pb) or max(pb) < min(pa):
                return True
    # also axis-aligned directions (helps degenerate polygons)
    for nx, ny in ((1, 0), (0, 1)):
        pa = [nx*p[0] + ny*p[1] for p in P]; pb = [nx*p[0] + ny*p[1] for p in Q]
        if max(pa) < min(pb) or max(pb) < min(pa):
            return True
    return False


def rect(x0, x1, y0, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def profile(name):
    RIGID = [1, 2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16]; LOOSE = [3, 4, 15, 17]
    s = {}
    def base(n):
        r = BASE[n]; p = ROOT + '/' + r['file']; assert sha(p) == r['sha256'], n; return p
    if name == 'JQ':
        for j in RIGID + LOOSE:
            s[j] = target(base('Q_%d' % j), j)
        s[9] = rect(X0, XW, Y0, YC)
    elif name == 'JPWS':
        for j in RIGID:
            s[j] = target(base('PW_%d' % j), j)
        sl = man['slab_capture']; p = ROOT + '/' + sl['file']; assert sha(p) == sl['sha256']
        s[11] = target(p, 11)
        for j in LOOSE:
            s[j] = target(base('Q_%d' % j), j)
        s[9] = rect(X0, XW, YC, Y13)
    elif name == 'JPW13':
        for j in RIGID:
            s[j] = target(base('PW_%d' % j), j)
        for j in LOOSE:
            s[j] = target(base('L_%d' % j), j)
        s[9] = rect(X0, XW, Y13, Y1)
    return s


for name in ('JQ', 'JPWS', 'JPW13'):
    s = profile(name)
    c = {j: clip(p) for j, p in s.items()}
    assert all(len(v) >= 3 for v in c.values()), name
    worst_d = max((diam2(v), j) for j, v in c.items())
    bad = [(i, j) for i in sorted(c) for j in sorted(c) if i < j and not strictly_separated(c[i], c[j])]
    print(name, 'labels', len(c), '; largest clipped squared diameter %.6f (label %d)' % (float(worst_d[0]), worst_d[1]),
          '; pairs not strictly separated:', bad)


# ---- off-wall profiles (P044: "imported in ROOT_ADMISSION"): rigid targets as run_adm.py selects them
sel = json.load(open(PKT + '/runtime/SELECTED_ORIGINAL_MAP.json'))
SEL = {(r['root'], r['label']): r for r in sel['rows']}
def offwall(name):
    RIGID = [1, 2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16]
    s = {}
    def base(n):
        r = BASE[n]; p = ROOT + '/' + r['file']; assert sha(p) == r['sha256'], n; return p
    for j in RIGID:
        if name == 'JG':
            s[j] = target(base('C_%d' % j), j)
        else:
            r = SEL[(name, j)]; f = r['literal']['file']; p = f if f.startswith('/') else ROOT + '/' + f
            assert sha(p) == r['literal']['sha256']
            s[j] = target(p, j)
    for j in (3, 4, 15, 17):
        s[j] = target(base('L_%d' % j), j)
    s[9] = rect(XW, X1, Y0, Y1)
    return s

for name in ('JG', 'JPA', 'JPG3m', 'JPG3p', 'JPG17m', 'JPG17p', 'JPG15m', 'JPG15p'):
    s = offwall(name)
    c = {j: clip(p) for j, p in s.items()}
    assert all(len(v) >= 3 for v in c.values()), name
    worst_d = max((diam2(v), j) for j, v in c.items())
    bad = [(i, j) for i in sorted(c) for j in sorted(c) if i < j and not strictly_separated(c[i], c[j])]
    print(name, 'labels', len(c), '; largest clipped squared diameter %.6f (label %d)' % (float(worst_d[0]), worst_d[1]),
          '; pairs not strictly separated:', bad)
