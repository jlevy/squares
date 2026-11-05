"""Exploratory: float local minima of F_r over the quadrant (decides nothing)."""
import gzip, json, sys, time
import numpy as np
from fractions import Fraction as Fr

cert = json.loads(gzip.open(sys.argv[1], 'rb').read())
r = int(sys.argv[2])
L = Fr(cert['L']); B = Fr(cert['B']); D = Fr(cert['proof_net']['step'])
def images(x1, y1, x2, y2):
    out = []
    for (a1, a2, b1, b2) in [(x1, x2, y1, y2), (y1, y2, x1, x2)]:
        for fx in (False, True):
            for fy in (False, True):
                X = (L - a2, L - a1) if fx else (a1, a2)
                Y = (L - b2, L - b1) if fy else (b1, b2)
                out.append((X[0], Y[0], X[1], Y[1]))
    return out
exp = {}
for row in cert['rectangles']:
    w = Fr(row['mass']); x1, y1, x2, y2 = (Fr(v) for v in row['rectangle'])
    for im in images(x1, y1, x2, y2):
        exp[im] = exp.get(im, 0) + w / 8 / ((x2 - x1) * (y2 - y1))
R = np.array([[float(v) for v in k] for k in exp]); rho = np.array([float(v) for v in exp.values()])
t = Fr(r) * D; c = (1 - t * t) / (1 + t * t); s = 2 * t / (1 + t * t)
a = max(Fr(0), t - D / 2); rho_a = (1 + 2 * a - a * a) / (2 * (1 + a * a)); U = float(L - rho_a)
h = float(B / 2); cf, sf = float(c), float(s); lo = float(L / 2)
vx = [h * (cf - sf), h * (cf + sf), h * (-cf - sf), h * (-cf + sf)]
ext = h * (cf + sf)

def area(Rs, px, py):
    x1, y1, x2, y2 = Rs[:, 0] - px, Rs[:, 1] - py, Rs[:, 2] - px, Rs[:, 3] - py
    if sf == 0.0:
        return np.clip(np.minimum(x2, h) - np.maximum(x1, -h), 0, None) * np.clip(np.minimum(y2, h) - np.maximum(y1, -h), 0, None)
    cand = [x1, x2] + [np.full_like(x1, v) for v in vx]
    for yy in (y1, y2):
        cand += [(h - sf * yy) / cf, (cf * yy - h) / sf, (-h - sf * yy) / cf, (cf * yy + h) / sf]
    C = np.clip(np.stack(cand, axis=1), x1[:, None], x2[:, None]); C.sort(axis=1)
    f1 = (h - cf * C) / sf; f2 = (h + sf * C) / cf; g1 = (-h - cf * C) / sf; g2 = (sf * C - h) / cf
    eta = np.clip(np.minimum(np.minimum(f1, f2), y2[:, None]) - np.maximum(np.maximum(g1, g2), y1[:, None]), 0, None)
    return np.sum(np.diff(C, axis=1) * (eta[:, 1:] + eta[:, :-1]) / 2, axis=1)

def F(px, py):
    m = (R[:, 0] < px + ext) & (R[:, 2] > px - ext) & (R[:, 1] < py + ext) & (R[:, 3] > py - ext)
    return float(np.dot(rho[m], area(R[m], px, py)))

def clampP(p):
    return (min(max(p[0], lo), U), min(max(p[1], lo), U))

def local_min(p, step):
    p = clampP(p); f = F(*p)
    while step > 1e-9:
        moved = False
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
            q = clampP((p[0] + dx*step, p[1] + dy*step)); fq = F(*q)
            if fq < f:
                p, f, moved = q, fq, True
                break
        if not moved:
            step /= 2
    return p, f

ng = int(sys.argv[3])
xs = np.linspace(lo, U, ng)
t0 = time.time()
vals = np.array([[F(x, y) for y in xs] for x in xs])
order = np.argsort(vals, axis=None)[:int(sys.argv[4])]
res = []
seen = []
for idx in order:
    i, j = np.unravel_index(idx, vals.shape)
    p, f = local_min((xs[i], xs[j]), (U - lo) / ng)
    if any(abs(p[0]-q[0]) < 1e-6 and abs(p[1]-q[1]) < 1e-6 for q in seen):
        continue
    seen.append(p); res.append((f, p))
res.sort()
print('r', r, 'theta_deg', round(float(np.degrees(2*np.arctan(float(t)))), 4), 'grid', ng, 'secs', round(time.time()-t0,1))
for f, p in res[:8]:
    wall = 'U-x=%.2e U-y=%.2e' % (U - p[0], U - p[1])
    print('  local min F-1 = %.6e at (%.9f, %.9f) %s' % (f - 1, p[0], p[1], wall))
