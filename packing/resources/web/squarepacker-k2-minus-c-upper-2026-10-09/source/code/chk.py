# chk.py -- generic exact certificate for a set of 1 x n rectangles in a convex polygon.
#  (1) shape: |v1-v0|^2 = 1, (v1-v0).(v3-v0) = 0, |v3-v0|^2 = n^2, v2 = v1 + v3 - v0 (exact)
#  (2) containment: every vertex in the closed convex polygon (exact cross products)
#  (3) interior-disjointness: every pair whose (outward-enlarged) float bounding boxes overlap is tested
#      by an exact separating-axis test (axes = the 2 edge directions of each rectangle; touching allowed).
#      Candidate pairs are found with per-orientation groups sorted by projection on the unit side and a
#      2-level bbox hierarchy; pruning is by bounding boxes only, so no overlapping pair can be missed.
import numpy as np
from r38 import QQ

MARG = 1e-6

def shape_ok(v, n):
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = v
    dx, dy = x1 - x0, y1 - y0; ex, ey = x3 - x0, y3 - y0
    return (dx * dx + dy * dy == 1 and dx * ex + dy * ey == 0 and ex * ex + ey * ey == n * n
            and x2 == x1 + ex and y2 == y1 + ey and n >= 1)

def inside(poly, v):
    k = len(poly)
    for (px, py) in v:
        for i in range(k):
            ax, ay = poly[i]; bx, by = poly[(i + 1) % k]
            if (bx - ax) * (py - ay) - (by - ay) * (px - ax) < 0:
                return False
    return True

def sat_disjoint(A, B):
    """exact: True iff interiors disjoint (A, B rectangles, 4 vertices each)."""
    for R in (A, B):
        x0, y0 = R[0]
        for (qx, qy) in (R[1], R[3]):
            ax, ay = qx - x0, qy - y0
            pa = [x * ax + y * ay for (x, y) in A]
            pb = [x * ax + y * ay for (x, y) in B]
            if max(pa) <= min(pb) or max(pb) <= min(pa):
                return True
    return False

def certify(pieces, poly, chunk=32, log=None, max_report=5):
    """pieces: list of (tag, verts, n). Returns dict."""
    npc = len(pieces)
    bad_shape = []; bad_cont = []
    groups = {}
    for idx, (tag, v, n) in enumerate(pieces):
        if not shape_ok(v, n):
            bad_shape.append(idx)
        if not inside(poly, v):
            bad_cont.append(idx)
        dx = v[1][0] - v[0][0]; dy = v[1][1] - v[0][1]
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        groups.setdefault((dx, dy), []).append(idx)
    # float data
    fx = np.empty((npc, 4)); fy = np.empty((npc, 4))
    for idx, (tag, v, n) in enumerate(pieces):
        for q in range(4):
            fx[idx, q] = float(v[q][0]); fy[idx, q] = float(v[q][1])
    bx0 = fx.min(1) - MARG; bx1 = fx.max(1) + MARG; by0 = fy.min(1) - MARG; by1 = fy.max(1) + MARG
    gdata = []
    for gi, (key, ids) in enumerate(groups.items()):
        dx, dy = float(key[0]), float(key[1])
        ids = np.array(ids, dtype=np.int64)
        proj = fx[ids] * dx + fy[ids] * dy
        p0 = proj.min(1)
        perp = (fx[ids] * (-dy) + fy[ids] * dx).min(1)
        order = np.lexsort((perp, p0))
        ids = ids[order]; p0 = p0[order]
        nc = (len(ids) + chunk - 1) // chunk
        cx0 = np.array([bx0[ids[c * chunk:(c + 1) * chunk]].min() for c in range(nc)])
        cx1 = np.array([bx1[ids[c * chunk:(c + 1) * chunk]].max() for c in range(nc)])
        cy0 = np.array([by0[ids[c * chunk:(c + 1) * chunk]].min() for c in range(nc)])
        cy1 = np.array([by1[ids[c * chunk:(c + 1) * chunk]].max() for c in range(nc)])
        gdata.append(dict(key=key, d=(dx, dy), ids=ids, p0=p0, cx0=cx0, cx1=cx1, cy0=cy0, cy1=cy1,
                          gx0=cx0.min(), gx1=cx1.max(), gy0=cy0.min(), gy1=cy1.max(),
                          pos={int(i): k for k, i in enumerate(ids)}))
    ncand = 0; nexact = 0; overl = []
    ng = len(gdata)
    def query(src, G, same):
        nonlocal ncand, nexact
        dx, dy = G['d']
        qx0, qx1, qy0, qy1 = bx0[src], bx1[src], by0[src], by1[src]
        pr = fx[src] * dx + fy[src] * dy
        lo = np.searchsorted(G['p0'], pr.min() - 1.0 - MARG - 1e-12 * abs(pr.min()), 'left')
        hi = np.searchsorted(G['p0'], pr.max() + MARG + 1e-12 * abs(pr.max()), 'right')
        if same:
            lo = max(lo, G['pos'][src] + 1)
        if hi <= lo:
            return
        c0 = lo // chunk; c1 = (hi - 1) // chunk + 1
        cm = ((G['cx0'][c0:c1] < qx1) & (qx0 < G['cx1'][c0:c1]) & (G['cy0'][c0:c1] < qy1) & (qy0 < G['cy1'][c0:c1]))
        nz = np.nonzero(cm)[0]
        if len(nz) == 0:
            return
        parts = []
        for cc in nz:
            a = max(lo, (c0 + cc) * chunk); b2 = min(hi, (c0 + cc + 1) * chunk)
            parts.append(G['ids'][a:b2])
        cid = np.concatenate(parts)
        mm = (bx0[cid] < qx1) & (qx0 < bx1[cid]) & (by0[cid] < qy1) & (qy0 < by1[cid])
        cid = cid[mm]
        if len(cid) == 0:
            return
        ncand += len(cid)
        # float SAT prefilter with margin (sound: float rounding error << MARG for |coords| < 1e8)
        ax = fx[src]; ay = fy[src]
        keep = np.ones(len(cid), dtype=bool)
        sd = (ax[1] - ax[0], ay[1] - ay[0])
        for (ux, uy) in (sd, (-sd[1], sd[0]), (dx, dy), (-dy, dx)):
            pa = ax * ux + ay * uy
            pb = fx[cid] * ux + fy[cid] * uy
            sep = (pa.max() + 2 * MARG < pb.min(1)) | (pb.max(1) + 2 * MARG < pa.min())
            keep &= ~sep
        for jdx in cid[keep]:
            jdx = int(jdx)
            nexact += 1
            if not sat_disjoint(pieces[src][1], pieces[jdx][1]):
                overl.append((int(src), jdx))
    rng = np.random.default_rng(1)
    def est(S, G):
        smp = S['ids'] if len(S['ids']) <= 300 else rng.choice(S['ids'], 300, replace=False)
        dx, dy = G['d']; tot = 0
        for q in smp:
            pr = fx[q] * dx + fy[q] * dy
            tot += np.searchsorted(G['p0'], pr.max(), 'right') - np.searchsorted(G['p0'], pr.min() - 1.0, 'left')
        return tot * len(S['ids']) / len(smp)
    for ga in range(ng):
        A = gdata[ga]
        for gb in range(ga, ng):
            B = gdata[gb]
            if A['gx1'] <= B['gx0'] or B['gx1'] <= A['gx0'] or A['gy1'] <= B['gy0'] or B['gy1'] <= A['gy0']:
                continue
            if ga == gb:
                src_ids, G, same = A['ids'], A, True
            elif est(A, B) <= est(B, A):
                src_ids, G, same = A['ids'], B, False
            else:
                src_ids, G, same = B['ids'], A, False
            for cnt, q in enumerate(src_ids):
                query(int(q), G, same)
                if log and cnt % 500000 == 0 and cnt:
                    log('  chk groups %d,%d: %d/%d cand=%d exact=%d overl=%d' % (ga, gb, cnt, len(src_ids), ncand, nexact, len(overl)))
    return {'n_pieces': npc, 'n_groups': len(gdata), 'bad_shape': len(bad_shape), 'bad_cont': len(bad_cont),
            'n_cand_pairs': ncand, 'n_exact_sat': nexact, 'n_overlap': len(overl), 'overlap_examples': overl[:max_report],
            'shape_examples': bad_shape[:max_report], 'cont_examples': bad_cont[:max_report],
            'pass': (not bad_shape and not bad_cont and not overl)}

def brute_pairs(pieces):
    """literal all-pairs exact SAT (small cases only)"""
    bad = 0
    for i in range(len(pieces)):
        for j in range(i + 1, len(pieces)):
            if not sat_disjoint(pieces[i][1], pieces[j][1]):
                bad += 1
    return bad
