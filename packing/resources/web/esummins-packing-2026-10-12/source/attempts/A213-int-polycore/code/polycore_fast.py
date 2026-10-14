"""A213 -- polycore.build, bit-identical, without the pure-Python loops.

A132's `build` is a FLOAT pipeline (clip a square by the sampled half-planes, drop negligible vertices, round to the
1e-9 grid) followed by the EXACT certification of the rounded vertices.  A211d's profile: the float part is the
largest single item of a coarse node (`_clip` 107 s + `_simplify` 159 s of 902 s -- `_simplify` recomputes EVERY
triangle area after EVERY pop, O(m^2) per build).  Here the same IEEE-754 operations are issued in the same order:

  * `_clip`: the signed distances `nx*px + ny*py - b` of all vertices in one numpy expression (numpy's add / multiply
    loops are the same binary64 operations as CPython's, no fused multiply-add), the <= 2 crossing points by the
    library's own scalar formula `t = dp/(dp-dq); p + t*(q-p)` on the very same doubles, the output in the library's
    order (each kept vertex, then the crossing point of its outgoing edge);
  * `_simplify`: a triangle area is a function of its three vertices only, so after a pop only the two neighbours'
    areas change -- the array is kept and those two are recomputed with the library's formula; `np.argmin` (first
    minimum) on the same values gives the same index;
  * the 1e-9 rounding is `round(x * VDEN)` on the identical doubles; the hull is A132's own `_hull_frac` on integer
    pairs (the same comparisons); the certification is polycore_int.vertex_ok_h (integer, exact).
So the vertices, the shrink that certified and the PolyCore returned are the library's, bit for bit (tests/).
"""
import heapq
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import polycore_int as PI                                      # noqa: E402  (sets the library path)
import numpy as np                                             # noqa: E402
import polycore as PC                                          # noqa: E402  READ-ONLY (A132)
from caselp import t_lo, t_hi                                  # noqa: E402  READ-ONLY

VDEN = PC.VDEN


def _clip_general(X, Y, dp, inside, pos):
    """PC._clip for any sign pattern (a convex polygon has <= 2 crossings; this is the general fallback)."""
    m = len(X)
    cross = pos != np.roll(pos, -1)
    ci = np.flatnonzero(cross)
    xs, ys = [], []
    prev = 0
    for i in ci.tolist():
        j = (i + 1) % m
        sl = slice(prev, i + 1)
        keep = inside[sl]
        xs.append(X[sl][keep])
        ys.append(Y[sl][keep])
        xs.append(np.array([_cross(X, Y, dp, i, j)[0]]))
        ys.append(np.array([_cross(X, Y, dp, i, j)[1]]))
        prev = i + 1
    if prev < m:
        sl = slice(prev, m)
        keep = inside[sl]
        xs.append(X[sl][keep])
        ys.append(Y[sl][keep])
    return np.concatenate(xs), np.concatenate(ys)


def _cross(X, Y, dp, i, j):
    """the library's crossing point of edge (i, j):  t = dp/(dp-dq); p + t (q - p)  on the same doubles."""
    px, py, qx, qy = float(X[i]), float(Y[i]), float(X[j]), float(Y[j])
    dpi, dqi = float(dp[i]), float(dp[j])
    t = dpi / (dpi - dqi)
    return px + t * (qx - px), py + t * (qy - py)


def _clip_np(X, Y, nx, ny, b):
    """PC._clip on parallel coordinate arrays; returns (X, Y) arrays in the library's vertex order."""
    m = len(X)
    if m == 0:
        return X, Y
    dp = nx * X + ny * Y - b
    pos = dp > 0.0
    if not pos.any():
        return X, Y
    if pos.all():
        return X[:0], Y[:0]
    ch = np.flatnonzero(pos[:-1] != pos[1:])
    wrap = bool(pos[-1] != pos[0])
    if len(ch) + wrap != 2:
        return _clip_general(X, Y, dp, dp <= 0.0, pos)
    i1, i2 = (int(ch[0]), m - 1) if wrap else (int(ch[0]), int(ch[1]))
    c1x, c1y = _cross(X, Y, dp, i1, i1 + 1)
    c2x, c2y = _cross(X, Y, dp, i2, (i2 + 1) % m)
    if pos[0]:                                                 # 0..i1 out, i1+1..i2 in, i2+1.. out
        return (np.concatenate(([c1x], X[i1 + 1:i2 + 1], [c2x])),
                np.concatenate(([c1y], Y[i1 + 1:i2 + 1], [c2y])))
    return (np.concatenate((X[:i1 + 1], [c1x, c2x], X[i2 + 1:])),
            np.concatenate((Y[:i1 + 1], [c1y, c2y], Y[i2 + 1:])))


def _tri(ax, ay, bx, by, cx, cy):
    return 0.5 * abs((bx - ax) * (cy - ay) - (by - ay) * (cx - ax))


def _simplify_np(X, Y, max_v=40, area_tol=2e-8):
    """PC._simplify: pop the FIRST minimal-area vertex while too many or negligible.  A heap of (area, original
    index, version) with lazy invalidation: the current list keeps the original order, so the smallest original
    index among equal areas IS the first index of the library's argmin.  -> list of (x, y) Python floats."""
    P = list(zip(X.tolist(), Y.tolist()))
    m = len(P)
    if m <= 3:
        return P
    A, B, C, D = np.roll(X, 1), np.roll(Y, 1), np.roll(X, -1), np.roll(Y, -1)
    areas = (0.5 * np.abs((X - A) * (D - B) - (Y - B) * (C - A))).tolist()
    nxt = list(range(1, m)) + [0]
    prv = [m - 1] + list(range(m - 1))
    ver = [0] * m
    alive = m
    heap = [(areas[i], i, 0) for i in range(m)]
    heapq.heapify(heap)
    while alive > 3 and heap:
        a, i, v = heap[0]
        if v != ver[i]:
            heapq.heappop(heap)
            continue
        if not (alive > max_v or a < area_tol):
            break
        heapq.heappop(heap)
        p, n = prv[i], nxt[i]
        nxt[p], prv[n], ver[i] = n, p, -1
        alive -= 1
        for k in (p, n):
            a0, b0, c0 = P[prv[k]], P[k], P[nxt[k]]
            areas[k] = _tri(a0[0], a0[1], b0[0], b0[1], c0[0], c0[1])
            ver[k] += 1
            heapq.heappush(heap, (areas[k], k, ver[k]))
    return [P[i] for i in range(m) if ver[i] >= 0]


def build(box, n_grid=129, shrink=1e-6, max_v=40, retries=(1e-6, 1e-5, 1e-4, 1e-3)):
    """polycore.build, bit-identical (same vertices, same shrink, same PolyCore; the same RuntimeError text)."""
    t0, t1 = t_lo(box.th0), t_hi(box.th1)
    ib = PI.ibox_of(box, t0, t1)
    cx = 0.5 * (box.x0 + box.x1)
    cy = 0.5 * (box.y0 + box.y1)
    ths = np.linspace(math.radians(box.th0), math.radians(box.th1), n_grid) \
        if box.th1 > box.th0 else np.array([math.radians(box.th0)])
    HP = PC.halfplanes(box, ths)
    last = None
    for sh in ((shrink,) + tuple(s for s in retries if s > shrink)):
        X = np.array([cx - 1.2, cx + 1.2, cx + 1.2, cx - 1.2])
        Y = np.array([cy - 1.2, cy - 1.2, cy + 1.2, cy + 1.2])
        for (nx, ny, b) in HP:
            X, Y = _clip_np(X, Y, nx, ny, b - sh)
            if len(X) == 0:
                break
        if len(X) == 0:
            continue
        poly = _simplify_np(X, Y, max_v=max_v)
        vi = PC._hull_frac([(round(x * VDEN), round(y * VDEN)) for (x, y) in poly])
        if len(vi) < 3:
            continue
        bad = [i for i, (a, b) in enumerate(vi) if not PI.vertex_ok_h(a, b, VDEN, ib)]
        vf = [(Fr(a, VDEN), Fr(b, VDEN)) for (a, b) in vi]
        last = (vf, sh, bad)
        if not bad:
            return PC.PolyCore(box, vf, len(ths), sh, True)
    raise RuntimeError(f"polycore: no certified polygon for {box!r}; "
                       f"last had {len(last[2]) if last else '?'} bad vertices")
