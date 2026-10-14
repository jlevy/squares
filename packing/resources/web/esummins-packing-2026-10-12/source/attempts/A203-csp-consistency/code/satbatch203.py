"""A203 -- rule S (csp203.sat_dead) vectorised over N piece pairs with numpy: identical logic (Lemma PC with the
tilt sub-intervals), one call per (group, unit) leaf-pair block instead of one Python call per pair."""
import numpy as np

EPS = 1e-9
R_MAX2 = (0.5 + np.sqrt(0.5)) ** 2 + 1e-6


def _dist90(a0, a1):
    """elementwise: min over a in [a0, a1] of the distance of a to the nearest multiple of 90 (degrees)."""
    m = np.floor(a0 / 90.0) * 90.0
    inside = ((a0 <= m + 90) & (m + 90 <= a1)) | ((a0 <= m) & (m <= a1)) | (a1 - a0 >= 90)
    d = np.minimum(a0 - m, m + 90 - a1)
    return np.where(inside, 0.0, np.maximum(d, 0.0))


def _wmin(lo, hi):
    """elementwise min of |cos| + |sin| over the degree interval [lo, hi]."""
    k0 = np.ceil(lo / 90.0)
    has_mult = (hi - lo >= 90) | (90 * k0 <= hi)
    w = lambda a: np.abs(np.cos(np.radians(a))) + np.abs(np.sin(np.radians(a)))
    return np.where(has_mult, 1.0, np.minimum(w(lo), w(hi)))


def _side_dead(r, al, bA, bB, nsub):
    """(N,) bool: no axis of square A (tilt in bA = (N,2)) separates, B's tilt in bB; r, al = (N,4) corner polar."""
    lo, hi = bA[:, 0:1], bA[:, 1:2]
    ks = np.arange(nsub, dtype=float)
    p0 = lo + (hi - lo) * ks[None, :] / nsub                             # (N, nsub)
    p1 = lo + (hi - lo) * (ks[None, :] + 1) / nsub
    lhs = np.zeros(p0.shape)
    for c in range(4):
        d = _dist90(p0 - al[:, c:c + 1], p1 - al[:, c:c + 1])
        lhs = np.maximum(lhs, r[:, c:c + 1] * np.cos(np.radians(d)))
    rhs = 0.5 + _wmin(bB[:, 0:1] - p1, bB[:, 1:2] - p0) / 2
    return np.all(lhs < rhs - EPS, axis=1)


def sat_dead_batch(r1, b1, r2, b2, step=4.0):
    """(N,) bool: rule S per pair; r = (N,4) rects (x0,x1,y0,y1), b = (N,2) degree bins.  The tilt sub-interval
    count is the max over the block of ceil(width / step) (finer than needed for the narrow bins: still sound)."""
    dx0, dx1 = r2[:, 0] - r1[:, 1], r2[:, 1] - r1[:, 0]
    dy0, dy1 = r2[:, 2] - r1[:, 3], r2[:, 3] - r1[:, 2]
    cx = np.stack([dx0, dx1, dx1, dx0], axis=1)
    cy = np.stack([dy0, dy0, dy1, dy1], axis=1)
    r = np.hypot(cx, cy)
    dmax2 = np.max(r * r, axis=1)
    cn = dmax2 < 1.0 - EPS
    far = dmax2 >= R_MAX2
    al = np.degrees(np.arctan2(cy, cx))
    w = max(float(np.max(b1[:, 1] - b1[:, 0])), float(np.max(b2[:, 1] - b2[:, 0])), 1e-9)
    nsub = max(1, int(np.ceil(w / step)))
    dead = _side_dead(r, al, b1, b2, nsub) & _side_dead(r, al, b2, b1, nsub)
    return (cn | dead) & ~far


def block(rects1, bins1, rects2, bins2, step=4.0):
    """all pairs of two leaf sets: (n1, n2) bool matrix of rule-S deaths."""
    n1, n2 = len(rects1), len(rects2)
    i = np.repeat(np.arange(n1), n2)
    j = np.tile(np.arange(n2), n1)
    return sat_dead_batch(rects1[i], bins1[i], rects2[j], bins2[j], step).reshape(n1, n2)
