"""Exploratory float landscape of the capture F_r on the quadrant (decides nothing)."""
import gzip, json, sys, time
import numpy as np
from fractions import Fraction as Fr

cert = json.loads(gzip.open(sys.argv[1], 'rb').read())
r = int(sys.argv[2]); ngrid = int(sys.argv[3])
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
a = max(Fr(0), t - D / 2); rho_a = (1 + 2 * a - a * a) / (2 * (1 + a * a)); U = L - rho_a
h = float(B / 2); cf, sf = float(c), float(s)
print('r', r, 't', float(t), 'theta deg', np.degrees(2*np.arctan(float(t))), 'U', float(U), 'quadrant side', float(U - L/2))

def area(px, py):
    """Area of R_k ∩ Q(p) for all k, p scalar; via section integral with candidate breakpoints."""
    x1, y1, x2, y2 = R[:, 0] - px, R[:, 1] - py, R[:, 2] - px, R[:, 3] - py
    if sf == 0.0:
        ox = np.clip(np.minimum(x2, h) - np.maximum(x1, -h), 0, None)
        oy = np.clip(np.minimum(y2, h) - np.maximum(y1, -h), 0, None)
        return ox * oy
    # lines: f1=(h-c x)/s, f2=(h+s x)/c, g1=(-h-c x)/s, g2=(s x-h)/c
    cand = [x1, x2,
            np.full_like(x1, (h * cf - h * sf) * 0 + (-h * (cf - sf))), ]  # placeholder, replaced below
    # square vertices in offsets: h(±u ± v), u=(c,s), v=(-s,c)
    vx = [h * (cf - sf), h * (cf + sf), h * (-cf - sf), h * (-cf + sf)]
    cand = [x1, x2] + [np.full_like(x1, v) for v in vx]
    # y = f1 -> x = (h - s y)/c ; y = f2 -> x = (c y - h)/s ; y = g1 -> x = (-h - s y)/c ; y = g2 -> x = (c y + h)/s
    for yy in (y1, y2):
        cand += [(h - sf * yy) / cf, (cf * yy - h) / sf, (-h - sf * yy) / cf, (cf * yy + h) / sf]
    C = np.stack(cand, axis=1)
    C = np.clip(C, x1[:, None], x2[:, None])
    C.sort(axis=1)
    f1 = (h - cf * C) / sf; f2 = (h + sf * C) / cf; g1 = (-h - cf * C) / sf; g2 = (sf * C - h) / cf
    top = np.minimum(np.minimum(f1, f2), y2[:, None]); bot = np.maximum(np.maximum(g1, g2), y1[:, None])
    eta = np.clip(top - bot, 0, None)
    return np.sum(np.diff(C, axis=1) * (eta[:, 1:] + eta[:, :-1]) / 2, axis=1)

def F(px, py):
    # restrict to rectangles near the square
    return float(np.dot(rho, area(px, py)))

lo, hi = float(L / 2), float(U)
xs = np.linspace(lo, hi, ngrid)
t0 = time.time()
vals = np.empty((ngrid, ngrid))
for i, x in enumerate(xs):
    for j, y in enumerate(xs):
        vals[i, j] = F(x, y)
print('grid', ngrid, 'secs', round(time.time() - t0, 1))
i, j = np.unravel_index(np.argmin(vals), vals.shape)
print('grid min', vals.min(), 'at', xs[i], xs[j])
q = np.quantile(vals, [0, 0.001, 0.01, 0.1, 0.5, 0.9])
print('quantiles of F-1', [f'{v-1:.3e}' for v in q])
np.save(sys.argv[4], vals)
