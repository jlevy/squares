"""Mixed covers (points + axis-parallel segments) and unit-square capture.

Format (Evan Daniel's "mixed 1"): header, container s_num s_den, D, W, m points
"X Y w", then a segment count and segments "X1 Y1 X2 Y2 w", then a polygon count.
Coordinates are X/D, weights w/W. A closed unit square captures a point on its
boundary in full, and a segment in proportion to the length inside it.
"""
import gzip
import numpy as np


def load_mixed(path):
    op = gzip.open if path.endswith(".gz") else open
    with op(path, "rt") as f:
        toks = [ln.split() for ln in f if ln.strip() and not ln.startswith("#")]
    assert toks[0] == ["mixed", "1"]
    s_num, s_den = map(int, toks[1])
    D = int(toks[2][0]); W = int(toks[3][0]); m = int(toks[4][0])
    pts = np.array(toks[5:5 + m], dtype=np.int64)
    k = int(toks[5 + m][0])
    segs = np.array(toks[6 + m:6 + m + k], dtype=np.int64).reshape(-1, 5)
    return dict(side=s_num / s_den, D=D, W=W, pts=pts, segs=segs)


def to_float(c):
    D, W = c["D"], c["W"]
    P = c["pts"].astype(np.float64)
    S = c["segs"].astype(np.float64)
    return (P[:, :2] / D, P[:, 2] / W, S[:, :4] / D, S[:, 4] / W)


def insert_band(c, a=4):
    """Cut at x = a and y = a (container units), shift the far side by +1.

    Mass on a cut line is split in halves between the two copies of the line.
    Works in exact integers: the weight unit is refined by 4 so halves and
    quarters stay integral. Returns a new cover dict on the side+1 container.
    """
    D = c["D"]; A = a * D; one = D
    pts_out = []
    for X, Y, w in c["pts"].tolist():
        xs = [(X, 2)] if X < A else [(X + one, 2)] if X > A else [(A, 1), (A + one, 1)]
        ys = [(Y, 2)] if Y < A else [(Y + one, 2)] if Y > A else [(A, 1), (A + one, 1)]
        for x, fx in xs:
            for y, fy in ys:
                pts_out.append((x, y, w * fx * fy))     # weight unit W*4
    segs_out = []

    def split_1d(lo, hi):
        """Pieces of [lo, hi] after the cut at A, as (lo', hi', frac_num, frac_den)."""
        L = hi - lo
        if hi <= A:
            return [(lo, hi, L, L)]
        if lo >= A:
            return [(lo + one, hi + one, L, L)]
        return [(lo, A, A - lo, L), (A + one, hi + one, hi - A, L)]

    for X1, Y1, X2, Y2, w in c["segs"].tolist():
        if Y1 == Y2:            # horizontal segment
            ys = [(Y1, 2)] if Y1 < A else [(Y1 + one, 2)] if Y1 > A else [(A, 1), (A + one, 1)]
            for lo, hi, fn, fd in split_1d(min(X1, X2), max(X1, X2)):
                for y, fy in ys:
                    segs_out.append((lo, y, hi, y, w * fy * 2 * fn / fd))
        else:                   # vertical segment
            assert X1 == X2
            xs = [(X1, 2)] if X1 < A else [(X1 + one, 2)] if X1 > A else [(A, 1), (A + one, 1)]
            for lo, hi, fn, fd in split_1d(min(Y1, Y2), max(Y1, Y2)):
                for x, fx in xs:
                    segs_out.append((x, lo, x, hi, w * fx * 2 * fn / fd))
    P = np.array(pts_out, dtype=np.float64)
    S = np.array(segs_out, dtype=np.float64)
    return dict(side=c["side"] + 1, D=D, W=c["W"] * 4, ptsf=P, segsf=S)


def measure_arrays(c):
    """Float arrays (pts_xy, pts_w, segs_xyxy, segs_w) for either cover kind."""
    if "ptsf" in c:
        D, W = c["D"], c["W"]
        return (c["ptsf"][:, :2] / D, c["ptsf"][:, 2] / W,
                c["segsf"][:, :4] / D, c["segsf"][:, 4] / W)
    return to_float(c)


# ---------------------------------------------------------------- capture (CPU, float64)

def capture_cpu(poses, pxy, pw, sxy, sw, tol=1e-9, chunk=256):
    """Captured mass for each pose (cx, cy, theta) of a closed unit square.

    tol > 0 is lenient (counts near-boundary mass), tol < 0 is strict.
    Brute force in chunks; fine for up to ~1e5 poses x 3e4 elements.
    """
    poses = np.asarray(poses, dtype=np.float64)
    out = np.empty(len(poses))
    h = 0.5 + tol
    for i in range(0, len(poses), chunk):
        cx, cy, th = (poses[i:i + chunk, j][:, None] for j in range(3))
        co, si = np.cos(th), np.sin(th)
        dx = pxy[None, :, 0] - cx; dy = pxy[None, :, 1] - cy
        u = co * dx + si * dy; v = -si * dx + co * dy
        inside = (np.abs(u) <= h) & (np.abs(v) <= h)
        cap = inside @ pw
        if len(sw):
            ax = sxy[None, :, 0] - cx; ay = sxy[None, :, 1] - cy
            bx = sxy[None, :, 2] - cx; by = sxy[None, :, 3] - cy
            ua = co * ax + si * ay; va = -si * ax + co * ay
            ub = co * bx + si * by; vb = -si * bx + co * by
            lo = np.zeros_like(ua); hi = np.ones_like(ua)
            for a0, b0 in ((ua, ub), (va, vb)):
                d = b0 - a0
                with np.errstate(divide="ignore", invalid="ignore"):
                    t1 = (-h - a0) / d; t2 = (h - a0) / d
                tl = np.where(d != 0, np.minimum(t1, t2), np.where(np.abs(a0) <= h, -np.inf, np.inf))
                tr = np.where(d != 0, np.maximum(t1, t2), np.where(np.abs(a0) <= h, np.inf, -np.inf))
                lo = np.maximum(lo, tl); hi = np.minimum(hi, tr)
            cap = cap + np.clip(hi - lo, 0, None) @ sw
        out[i:i + chunk] = cap
    return out


def admissible(poses, side):
    cx, cy, th = poses[:, 0], poses[:, 1], poses[:, 2]
    w = np.abs(np.cos(th)) + np.abs(np.sin(th))
    return (cx - w / 2 >= 0) & (cx + w / 2 <= side) & (cy - w / 2 >= 0) & (cy + w / 2 <= side)


def random_poses(n, side, rng):
    th = rng.uniform(0, np.pi / 2, n)
    w = np.abs(np.cos(th)) + np.abs(np.sin(th))
    cx = w / 2 + rng.uniform(0, 1, n) * (side - w)
    cy = w / 2 + rng.uniform(0, 1, n) * (side - w)
    return np.stack([cx, cy, th], 1)
