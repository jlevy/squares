"""Band LP for s(K^2 - 5) = K (K from env SQK, default 9): find a D4-symmetric measure nu on the cross region so that
base9 + nu captures >= 1 in every closed unit square meeting the band.
Float LP with cutting planes; the exact checker comes later."""
import numpy as np, time, json, sys, os
from scipy.optimize import linprog
from scipy import sparse
from cover import *
try:
    from gpu import GPUMeasure
except ImportError:
    pass

K = int(os.environ.get("SQK", "9")); S = float(K); C = S / 2


def d4_images(x1, y1, x2, y2):
    ims = []
    for (a, b, c, d) in [(x1, y1, x2, y2), (y1, x1, y2, x2)]:
        for fx in (False, True):
            for fy in (False, True):
                A = S - a if fx else a; Cc = S - c if fx else c
                B = S - b if fy else b; Dd = S - d if fy else d
                p = tuple(sorted([(round(A, 6), round(B, 6)), (round(Cc, 6), round(Dd, 6))]))
                ims.append(p)
    return ims


def candidates(pitch=0.1, seglen=None, lo=2.5, hi=None):
    hi = S - 2.5 if hi is None else hi
    seglen = seglen or (0.125 if pitch >= 0.1 else 0.0625)
    pts = []
    ks = np.arange(-round(C / pitch), round(C / pitch) + 1)
    grid = np.round(C + ks * pitch, 6)
    for x in grid:
        for y in grid:
            if lo <= x <= hi or lo <= y <= hi:
                pts.append((x, y))
    segs = []
    starts = np.round(np.arange(0, S - seglen + 1e-9, seglen), 6)
    for L in range(1, K):
        for t0 in starts:
            t1 = round(t0 + seglen, 6)
            if lo <= L <= hi or (t0 >= lo and t1 <= hi):
                segs.append((L, t0, L, t1))      # vertical on x = L
                segs.append((t0, L, t1, L))      # horizontal on y = L
    segs = sorted(set(segs))
    # orbits
    keys = {}
    p_orb = []
    for (x, y) in pts:
        k = ("p",) + tuple(sorted(set(im[0] for im in d4_images(x, y, x, y))))
        p_orb.append(keys.setdefault(k, len(keys)))
    s_orb = []
    for s in segs:
        k = ("s",) + tuple(sorted(set(d4_images(*s))))
        s_orb.append(keys.setdefault(k, len(keys)))
    return np.array(pts), np.array(segs, dtype=np.float64), np.array(p_orb), np.array(s_orb), len(keys)


def element_capture(poses, pxy, sxy, tol=1e-9):
    """Per-element capture for unit weights: (P x Np), (P x Ns) float64."""
    poses = np.asarray(poses, dtype=np.float64)
    cx, cy, th = (poses[:, j][:, None] for j in range(3))
    co, si = np.cos(th), np.sin(th); h = 0.5 + tol
    dx = pxy[None, :, 0] - cx; dy = pxy[None, :, 1] - cy
    u = co * dx + si * dy; v = -si * dx + co * dy
    Pm = ((np.abs(u) <= h) & (np.abs(v) <= h)).astype(np.float64)
    ax = sxy[None, :, 0] - cx; ay = sxy[None, :, 1] - cy
    bx = sxy[None, :, 2] - cx; by = sxy[None, :, 3] - cy
    lo = np.zeros(ax.shape); hi = np.ones(ax.shape)
    for a0, b0 in ((co * ax + si * ay, co * bx + si * by), (-si * ax + co * ay, -si * bx + co * by)):
        d = b0 - a0
        with np.errstate(divide="ignore", invalid="ignore"):
            t1 = (-h - a0) / d; t2 = (h - a0) / d
        tl = np.where(d != 0, np.minimum(t1, t2), np.where(np.abs(a0) <= h, -np.inf, np.inf))
        tr = np.where(d != 0, np.maximum(t1, t2), np.where(np.abs(a0) <= h, np.inf, -np.inf))
        lo = np.maximum(lo, tl); hi = np.minimum(hi, tr)
    Sm = np.clip(hi - lo, 0, None)
    return Pm, Sm


def meets_band(P):
    w = np.abs(np.cos(P[:, 2])) + np.abs(np.sin(P[:, 2]))
    return ((P[:, 0] - w / 2 <= 5) & (P[:, 0] + w / 2 >= 4)) | ((P[:, 1] - w / 2 <= 5) & (P[:, 1] + w / 2 >= 4))


def band_poses(n, rng):
    out = []
    while sum(len(o) for o in out) < n:
        P = random_poses(4 * n, S, rng)
        out.append(P[meets_band(P)])
    return np.concatenate(out)[:n]


def special_poses():
    """Zero-margin poses: band tiles and their germs (tiny shifts/tilts)."""
    out = []
    for j in range(9):
        for (cx, cy) in [(4.5, j + .5), (j + .5, 4.5)]:
            for th in [0, 1e-4, 1e-3, 0.01, 0.03, 0.06]:
                for sx in [-0.3, -0.1, -0.02, 0, 0.02, 0.1, 0.3]:
                    for sy in [-0.3, -0.1, 0, 0.1, 0.3]:
                        out.append((cx + sx, cy + sy, th))
                        out.append((cx + sx, cy + sy, np.pi / 2 - th) if th else (cx + sx, cy + sy, 0))
    P = np.array(out)
    return P[admissible(P, S) & meets_band(P)]


def refine(G, P, steps=40, scale=0.05, rng=None, region=None):
    """Greedy random descent of capture from each start (GPU)."""
    best = P.copy(); bc = G.capture(best)
    for k in range(steps):
        sc = scale * (0.85 ** k)
        Q = best + rng.normal(0, 1, best.shape) * np.array([sc, sc, sc * 0.6])
        Q[:, 2] = np.mod(Q[:, 2], np.pi / 2)
        ok = admissible(Q, S) & (region or meets_band)(Q)
        qc = np.full(len(Q), np.inf); qc[ok] = G.capture(Q[ok])
        better = qc < bc
        best[better] = Q[better]; bc[better] = qc[better]
    return best, bc
