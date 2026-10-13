# cert.py -- generic exact certificate for a list of pieces (each a CCW list of 4 exact vertices) in
#   Reg(y) = {0 <= X <= W, 0 <= Y <= y + (X - s) T}.  Independent of how the pieces were built.
# (1) shape: V2 = V1 + V3 - V0, (V1-V0).(V3-V0) = 0, squared side lengths {1, n^2}, n integer >= 1  -> 1 x n rectangle
# (2) containment: every vertex in Reg(y) (Reg convex)
# (3) disjointness, complete:
#     intra-frame: pieces whose sides are parallel to the same frame (direction up to 90 deg) are axis-aligned in that
#       frame; candidate pairs from a float sweep with boxes inflated by EPS, then exact interval test on both frame
#       axes (= SAT on the only two axes of such a pair);
#     inter-frame: candidate pairs = all pairs with overlapping (inflated float) real bounding boxes, exact SAT.
#     Inflation EPS = 1e-6 >> float rounding (|coord| < 1e7 -> error < 2e-9), so every pair with overlapping exact boxes
#     is a candidate.
#   brute(): literal exact all-pairs bbox sweep + SAT (no frames, no floats) for small instances.
# (4) U = area(Reg) - sum n (n from the shape check).
import math, bisect, heapq
EPS = 1e-6

def shape_n(V):
    (a, b), (c, d), (e, f), (g, h) = V
    if not (e == c + g - a and f == d + h - b): return None
    u = (c - a, d - b); w = (g - a, h - b)
    if u[0] * w[0] + u[1] * w[1] != 0: return None
    l1 = u[0] * u[0] + u[1] * u[1]; l3 = w[0] * w[0] + w[1] * w[1]
    for one, other in ((l1, l3), (l3, l1)):
        if one == 1:
            n = math.isqrt(int(other)) if other == int(other) else -1
            if n >= 1 and n * n == other: return n
    return None

def frame_key(V):
    (a, b), (c, d) = V[0], V[1]
    ux, uy = c - a, d - b
    l2 = ux * ux + uy * uy; l = math.isqrt(int(l2)); ux, uy = ux / l, uy / l
    for _ in range(4):
        if ux > 0 and uy >= 0: return (ux, uy)
        ux, uy = -uy, ux
    raise ValueError('bad direction')

def sat_disjoint(A, B):
    for Pq in (A, B):
        for i in range(2):
            (x0, y0), (x1, y1) = Pq[i], Pq[i + 1]
            nx, ny = y1 - y0, x0 - x1
            pa = [nx * p + ny * q for (p, q) in A]; pb = [nx * p + ny * q for (p, q) in B]
            if max(pa) <= min(pb) or max(pb) <= min(pa): return True
    return False

def cand_pairs(boxes, sub, grp, inter_only):
    """boxes[i] = (x0,x1,y0,y1) floats (inflated); returns all pairs (i,j) with overlapping boxes
    (restricted to different grp if inter_only).  Active pieces kept per sub-list sorted by y0."""
    hmax = {}
    for i, bx in enumerate(boxes): hmax[sub[i]] = max(hmax.get(sub[i], 0.0), bx[3] - bx[2])
    act = {k: [] for k in hmax}; hp = {k: [] for k in hmax}
    live = set()                                  # sub-lists with active pieces
    out = []
    for i in sorted(range(len(boxes)), key=lambda i: boxes[i][0]):
        x0, x1, y0, y1 = boxes[i]
        for k in list(live):
            L = act[k]; H = hp[k]
            while H and H[0][0] <= x0:
                _, yy, jj = heapq.heappop(H); L.pop(bisect.bisect_left(L, (yy, jj)))
            if not L: live.discard(k); continue
            if inter_only and k[0] == grp[i]: continue
            lo = bisect.bisect_left(L, (y0 - hmax[k], -1)); hi = bisect.bisect_left(L, (y1, -1))
            for pos in range(lo, hi):
                jj = L[pos][1]
                if boxes[jj][3] > y0: out.append((jj, i))
        bisect.insort(act[sub[i]], (y0, i)); heapq.heappush(hp[sub[i]], (x1, y0, i)); live.add(sub[i])
    return out

def certify(P, y, W, T, s, area):
    res = dict(npieces=len(P))
    ns = [shape_n(V) for V in P]
    res['shape_bad'] = sum(1 for n in ns if n is None)
    g = lambda X: y + (X - s) * T
    res['contain_bad'] = sum(1 for V in P if not all(0 <= X <= W and 0 <= Y <= g(X) for (X, Y) in V))
    if res['shape_bad']: return res
    keys = [frame_key(V) for V in P]
    kid = {}; grp = [kid.setdefault(k, len(kid)) for k in keys]
    res['nframes'] = len(kid)
    # intra-frame
    fr = []
    for V, k in zip(P, keys):
        ps = [X * k[0] + Y * k[1] for (X, Y) in V]; qs = [-X * k[1] + Y * k[0] for (X, Y) in V]
        fr.append((min(ps), max(ps), min(qs), max(qs)))
    ov = 0; npairs = 0
    members = {}
    for i, gi in enumerate(grp): members.setdefault(gi, []).append(i)
    for gi in range(len(kid)):
        idx = members[gi]
        bx = []
        for i in idx:
            a, b_, c, d = (float(v) for v in fr[i])
            bx.append((a - EPS, b_ + EPS, c - EPS, d + EPS))
        sub = [(0, (q[3] - q[2]) > 4) for q in bx]
        for (u, v) in cand_pairs(bx, sub, [0] * len(bx), False):
            A, B = fr[idx[u]], fr[idx[v]]; npairs += 1
            if A[0] < B[1] and B[0] < A[1] and A[2] < B[3] and B[2] < A[3]: ov += 1
    res['intra_pairs'] = npairs; res['intra_overlaps'] = ov
    # inter-frame
    bx = []
    for V in P:
        xs = [float(X) for X, _ in V]; ys = [float(Y) for _, Y in V]
        bx.append((min(xs) - EPS, max(xs) + EPS, min(ys) - EPS, max(ys) + EPS))
    sub = [(grp[i], (bx[i][3] - bx[i][2]) > 4) for i in range(len(P))]
    cp = cand_pairs(bx, sub, grp, True)
    res['inter_pairs'] = len(cp)
    res['inter_overlaps'] = sum(1 for (u, v) in cp if not sat_disjoint(P[u], P[v]))
    V = sum(ns)
    res['V'] = int(V); res['U'] = area - V
    res['all_pass'] = (res['shape_bad'] == 0 and res['contain_bad'] == 0 and ov == 0 and res['inter_overlaps'] == 0)
    return res

def brute(P):
    """literal: every pair with overlapping exact bounding boxes, exact SAT (A's method)."""
    bb = sorted(((min(p[0] for p in V), max(p[0] for p in V), min(p[1] for p in V), max(p[1] for p in V), i)
                 for i, V in enumerate(P)), key=lambda z: z[0])
    over = pairs = 0
    for a in range(len(bb)):
        for c in range(a + 1, len(bb)):
            if bb[c][0] >= bb[a][1]: break
            if bb[c][2] >= bb[a][3] or bb[a][2] >= bb[c][3]: continue
            pairs += 1
            if not sat_disjoint(P[bb[a][4]], P[bb[c][4]]): over += 1
    return dict(pairs=pairs, overlaps=over)
