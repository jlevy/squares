"""Root admission (PROOF.md P073-P080), recomputed with my own exact code for the eleven roots.

usage: admission.py EDITION_ROOT
For each root and each of the 17 labels: the target (centre polygon x direction set) of the case, transported
into the endpoint chart xi = e.(c - (U-L)(1,1)/2 - p) for every L in my own enclosure [Llo, Lhi] (affine in c and
L, so extremes at polygon vertices x interval ends), clipped by physical containment (centre in [1/2, L-1/2]),
with the gated-9 support cut; the box must lie in the root box and the direction set in the root arc (absolute
arc ends u_i * c * lo, u_i * c * hi; quarter-turn lifts allowed for slots; uniqueness of the lift is not needed
for the inclusion). Prints the smallest margin per root. Direction sets per case follow PROOF.md P050-P056,
P078 (label 12 cut by the half-marker end rho) and the wall lemma (|theta9| < 2 atan(31/1000)).
"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
import geom, mpmath
from mpmath import mp

ROOT = sys.argv[1]
PKT = ROOT + '/research/finishing-threshold-goal-20261007/current-author-20261012t/fifth-order-20261010/public-edition-round2-20261011'
JOIN = ROOT + '/research/window-extension-20261008/bigbox/join'
man = json.load(open(PKT + '/runtime/THEOREM_MANIFEST.json'))
BASE = {r['name']: r for r in man['base_capture_rows']}
sel = json.load(open(PKT + '/runtime/SELECTED_ORIGINAL_MAP.json'))
SEL = {(r['root'], r['label']): r for r in sel['rows']}
U = F(1169, 250)
RHO = F(207107, 500000)
X0, X1, XW = F(-131, 250), F(4501, 5000), F(53, 100)
Y0, YC, Y13, Y1 = F(24137, 10000), F(129, 50), F(13, 5), F(29637, 10000)
G9LO, G9HI, KWHI = F(61301, 200000), F(591183, 1408817), F(44941, 100000)
GT, TW = F(1, 20), F(31, 1000)

# my L enclosure: Newton point +- 1e-40 is inside the Krawczyk box; L is increasing in t near the root
mp.dps = 80
t, b = geom.newton_root()
Lmid = geom.to_fr((6 + 4*t)/(1 + 2*t - t*t))
Llo, Lhi = Lmid - F(1, 10**40), Lmid + F(1, 10**40)
assert Lhi < F(4675530093604551, 10**15)


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def rot(t):
    return ((1 - t*t)/(1 + t*t), 2*t/(1 + t*t))


def mul(p, q):
    return (p[0]*q[0] - p[1]*q[1], p[0]*q[1] + p[1]*q[0])


def cross(a, b):
    return a[0]*b[1] - a[1]*b[0]


pk = json.load(open(ROOT + '/upper-packing-certificate.json'))
p, u = {}, {}
for k, s in enumerate(pk['squares']):
    i = k + 1; p[i] = (F(s['x']), F(s['y'])); u[i] = rot(F(s['t']))
c9 = u[9][0]; T0 = c9*(c9 + 4 - F(pk['side']))
v13 = (-u[13][1], u[13][0])
p[13] = (p[13][0] - T0/3*v13[0], p[13][1] - T0/3*v13[1])
frame = {i: ((u[i], (-u[i][1], u[i][0])) if i in (11, 13) else ((F(1), F(0)), (F(0), F(1)))) for i in p}


def target(path, label):
    d = json.load(open(path))
    cs = [c for c in d['classes'] if F(c['threshold']) == 0 and any(c['name'].startswith(pre + 'label%d_' % label)
          for pre in ('PB_', 'HULLW_', 'QB_', 'HULL_', 'B_', 'T_', 'S_'))]
    assert len(cs) == 1
    sl = cs[0]['slots'][0]
    return [(F(a), F(b)) for a, b in sl['centre']['polygon']], (F(sl['angle_tan_half'][0]), F(sl['angle_tan_half'][1]))


def base(n):
    r = BASE[n]; path = ROOT + '/' + r['file']; assert sha(path) == r['sha256']; return path


def transport(i, poly):
    out = []
    for k in (0, 1):
        vals = [frame[i][k][0]*(c[0] - (U - L)/2 - p[i][0]) + frame[i][k][1]*(c[1] - (U - L)/2 - p[i][1])
                for c in poly for L in (Llo, Lhi)]
        lo, hi = min(vals), max(vals)
        if i not in (11, 13):
            lo = max(lo, F(1, 2) - p[i][k]); hi = min(hi, Lhi - F(1, 2) - p[i][k])
        out.append((lo, hi))
    return out


def arc_contains(A, B, D1, D2):
    """the ccw arc [A,B] (shorter than a half turn) contains the ccw arc [D1,D2] (shorter than a half turn)."""
    return cross(A, D1) >= 0 and cross(D1, D2) >= 0 and cross(D2, B) >= 0


def spec(name):
    RIGID = [1, 2, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16]
    s = {}
    if name in ('JQ', 'JPWS', 'JPW13'):
        for j in RIGID:
            poly, th = target(base(('Q_%d' if name == 'JQ' else 'PW_%d') % j), j); s[j] = (poly, ('slot', th))
        if name == 'JPWS':
            sl = man['slab_capture']; path = ROOT + '/' + sl['file']; assert sha(path) == sl['sha256']
            poly, th = target(path, 11); s[11] = (poly, ('slot', th))
        for j in (3, 4, 15, 17):
            poly, th = target(base(('L_%d' if name == 'JPW13' else 'Q_%d') % j), j); s[j] = (poly, ('slot', th))
        ylo, yhi = {'JQ': (Y0, YC), 'JPWS': (YC, Y13), 'JPW13': (Y13, Y1)}[name]
        s[9] = ([(X0, ylo), (XW, ylo), (XW, yhi), (X0, yhi)], ('wall',))
        return s
    for j in RIGID:
        if name == 'JG':
            poly, th = target(base('C_%d' % j), j)
        else:
            r = SEL[(name, j)]; f = r['literal']['file']; path = f if f.startswith('/') else ROOT + '/' + f
            assert sha(path) == r['literal']['sha256']
            poly, th = target(path, j)
        s[j] = (poly, ('slot', th))
    order = (3, 17, 15)
    kinds = {k: ('free',) for k in order}
    if name == 'JG':
        kinds = {k: ('gate',) for k in order}
    elif name != 'JPA':
        k = int(name[3:-1]); sgn = name[-1]
        for kk in order[:order.index(k)]:
            kinds[kk] = ('gate',)
        kinds[k] = ('below',) if sgn == 'm' else ('above',)
    for j in order:
        poly, th = target(base('L_%d' % j), j); s[j] = (poly, kinds[j])
    poly, th = target(base('L_4'), 4); s[4] = (poly, ('slot', th))
    s[9] = ([(XW, Y0), (X1, Y0), (X1, Y1), (XW, Y1)], ('exit9',) if name == 'JPA' else ('gate9',))
    return s


ROOTS = {'JQ': 'JQ_exact_v1', 'JPWS': 'JPWS_exact_v4', 'JPW13': 'JPW13_exact_v2x', 'JG': 'JG_exact_v2',
         'JPA': 'JPA_exact_v5', 'JPG3m': 'JPG3m_exact_v5', 'JPG3p': 'JPG3p_exact_v5', 'JPG17m': 'JPG17m_exact_v5',
         'JPG17p': 'JPG17p_exact_v5', 'JPG15m': 'JPG15m_exact_v5', 'JPG15p': 'JPG15p_exact_v5'}
for name, fn in ROOTS.items():
    d = json.load(open(JOIN + '/' + fn + '.json'))
    assert F(d['S'][0]) == F(d['S'][1]) == F(d['Sref']) and d['labels'] == 17
    box = {int(i): [(F(a), F(b)) for a, b in bb] for i, bb in d['window']['box'].items()}
    arc = {}
    for i, a in d['root_arc'].items():
        cc, lo, hi = (tuple(F(x) for x in a[key]) for key in ('c', 'lo', 'hi'))
        assert all(g[0]**2 + g[1]**2 == 1 for g in (cc, lo, hi)) and lo[0] > 0 and hi[0] > 0 and lo[1] <= hi[1]
        arc[int(i)] = (mul(u[int(i)], mul(cc, lo)), mul(u[int(i)], mul(cc, hi)))
    s = spec(name)
    worst = None; fails = []
    for i in range(1, 18):
        poly, kind = s[i]
        tr = transport(i, poly)
        if kind[0] == 'gate9':
            smin = min(sum(rot(G9LO)), sum(rot(G9HI)))/2
            tr[0] = (max(tr[0][0], smin - p[9][0]), tr[0][1])
        for k in (0, 1):
            for m in (tr[k][0] - box[i][k][0], box[i][k][1] - tr[k][1]):
                if m < 0: fails.append((i, 'box', k, float(m)))
                if worst is None or m < worst[0]: worst = (m, i, 'box')
        A, B = arc[i]
        if kind[0] == 'slot':
            lo, hi = kind[1]
            if (lo, hi) == (-RHO, RHO):
                ok = -(A[0]*B[0] + A[1]*B[1]) >= 0          # free: arc at least a quarter turn
            else:
                if i == 12:
                    hi = min(hi, RHO)
                D1, D2 = rot(lo), rot(hi)
                ok = False
                for q in range(4):
                    if arc_contains(A, B, D1, D2): ok = True
                    D1, D2 = mul(D1, (F(0), F(1))), mul(D2, (F(0), F(1)))
        elif kind[0] == 'free':
            ok = -(A[0]*B[0] + A[1]*B[1]) >= 0
        elif kind[0] == 'gate':
            ok = arc_contains(A, B, rot(-GT), rot(GT))
        elif kind[0] == 'below':
            ok = arc_contains(A, B, (F(1), F(-1)), rot(-GT))
        elif kind[0] == 'above':
            ok = arc_contains(A, B, rot(GT), (F(1), F(1)))
        elif kind[0] == 'wall':
            ok = arc_contains(A, B, rot(-TW), rot(TW))
        elif kind[0] in ('gate9', 'exit9'):
            lo, hi = (G9LO, G9HI) if kind[0] == 'gate9' else (G9HI, KWHI)
            ok = arc_contains(A, B, rot(lo), rot(hi))
        if not ok:
            fails.append((i, 'arc', kind[0]))
    print('%-7s smallest box margin %.3e (label %d); failures: %s' % (name, float(worst[0]), worst[1], fails if fails else 'none'))
