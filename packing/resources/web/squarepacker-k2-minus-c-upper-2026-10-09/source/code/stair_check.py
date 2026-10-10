# stair_check.py -- independent exact checker of the staircase certificates data/stair_k<k>.json.gz (Table 1).
# It does not import the generating program.  It reads only the certificate file and k, and recomputes from b:
#   the band (tan(theta/2) = b/(b^2-1), cos theta, sin theta, W, T, d = sec theta, h = b sin theta + cos theta),
#   S = k - b + W (and checks S < k), the numbers of lifted rows R = floor((L - h - 2 y0)/d) + 1 of both bands
#   (L = S for the right band, L = k - b for the top band) and the top lift y1 = L - h - (R - 1) d - y0,
#   which must equal the certificate's y of the top end of that band (the bottom ends must have y = y0);
# then, for each of the four ends, with the explicit pieces of the certificate:
#   shape (ca^2 + sa^2 = 1, ca, sa > 0; integer lengths n >= 1), containment of every vertex in
#   Reg(y) = {0 <= X <= W, 0 <= Y <= y + (X - s) T} (Reg(y) is convex, so the pieces lie in it),
#   pairwise interior-disjointness: every pair whose bounding boxes overlap (candidates by floats with a margin
#   1e-6, a superset) is decided exactly by the separating-axis test on the edge normals of the two pieces;
# and finally N = (k - b)^2 + b (R_right + R_top) + (squares in the four ends), c = k^2 - N, and the waste identity
#   k^2 - N = (k^2 - S^2) + sum over bands (R - 1) T + sum over ends E(y),  E(y) = area(Reg(y)) - V(y) + T/2.
# The rows and the placement of the ends at the two ends of each band (the L-shaped frame) are proved in the paper
# and are not re-checked here; only the conditions y0 >= 0, R >= 1, y0 <= y1 < y0 + d and y + (W - s) T < L are.
# Exact rationals: gmpy2.mpq if available, else fractions.Fraction.
# Usage: python code/stair_check.py data/stair_k<k>.json.gz <k> [mutate]
import sys, json, gzip, time
from fractions import Fraction
import numpy as np
try:
    import gmpy2
    Q = gmpy2.mpq
    ARITH = 'gmpy2.mpq'
except Exception:
    Q = Fraction
    ARITH = 'fractions.Fraction'


def fl(x):
    x = Q(x); return int(x.numerator) // int(x.denominator)


def myband(b):
    t = Q(b, b * b - 1)
    g = (1 - t * t) / (1 + t * t); s = 2 * t / (1 + t * t)
    return dict(g=g, s=s, W=b * g + s, T=s / g, d=1 / g, h=b * s + g)


def pieces(e, mut=None):
    """explicit vertices (counter-clockwise) of every piece of one end; mut = negative control"""
    ca, sa = Q(e['ca']), Q(e['sa'])
    P = []
    cols = e['columns']; nc = len(cols)
    down = next((i for i in range(nc // 2, nc) if cols[i][1] > 0 and cols[i][1] == cols[i - 1][1]), None)
    for i, (X, Y, n) in enumerate(cols):
        x, y = Q(X), Q(Y)
        if mut == 'colshift' and i == nc // 2: x += Q(1, 10 ** 6)
        if mut == 'coldown' and i == down: y -= Q(1, 10 ** 6); x += Q(1, 10 ** 6) * sa / ca
        if mut == 'colgrow' and i == 0: n += 1
        P.append(('col', n, [(x, y), (x + ca, y + sa), (x + ca - n * sa, y + sa + n * ca), (x - n * sa, y + n * ca)]))
    nl = len(e['layers'])
    for li, (x0, j, L) in enumerate(e['layers']):
        x, y = Q(x0), Q(j)
        if mut == 'layerup' and li == nl // 3: y += Q(1, 10 ** 6)
        if mut == 'layerlong' and li == nl // 2: x -= 1
        P.append(('lay', L, [(x, y), (x + L, y), (x + L, y + 1), (x, y + 1)]))
    for ri, (h, l) in enumerate(e['wedge']):
        if mut == 'wedgeplus' and ri == len(e['wedge']) // 2: l += 1
        P.append(('wed', l, [(Q(0), Q(h)), (Q(l), Q(h)), (Q(l), Q(h + 1)), (Q(0), Q(h + 1))]))
    return P


def check_end(B, e, yreg, mut=None):
    W, s, T = B['W'], B['s'], B['T']
    ca, sa = Q(e['ca']), Q(e['sa'])
    r = {'unit_tilt': bool(ca * ca + sa * sa == 1 and ca > 0 and sa > 0)}
    ints = all(isinstance(v, int) for c in e['columns'] for v in c[1:]) and \
        all(isinstance(v, int) for c in e['layers'] for v in c[1:]) and all(isinstance(v, int) for c in e['wedge'] for v in c)
    P = pieces(e, mut)
    r['bad_shape'] = (0 if ints else 1) + sum(1 for kind, n, v in P if n < 1) + \
        sum(1 for (_, j, _) in e['layers'] if j < 0) + sum(1 for (h, _) in e['wedge'] if h < 0)
    V = sum(n for kind, n, v in P)
    bad_c = 0
    for kind, n, v in P:
        if not all(0 <= x <= W and 0 <= y <= yreg + (x - s) * T for (x, y) in v):
            bad_c += 1
    r['bad_contain'] = bad_c
    ex = []                    # exact extents along x, y, u = (ca, sa), w = (-sa, ca)
    for kind, n, v in P:
        xs = [p[0] for p in v]; ys = [p[1] for p in v]
        us = [p[0] * ca + p[1] * sa for p in v]; ws = [-p[0] * sa + p[1] * ca for p in v]
        ex.append((kind, (min(xs), max(xs)), (min(ys), max(ys)), (min(us), max(us)), (min(ws), max(ws))))
    del P
    fx0 = np.array([float(z[1][0]) for z in ex]); fx1 = np.array([float(z[1][1]) for z in ex])
    fy0 = np.array([float(z[2][0]) for z in ex]); fy1 = np.array([float(z[2][1]) for z in ex])
    order = np.argsort(fx0, kind='stable')
    sx0 = fx0[order]; sx1 = fx1[order]; sy0 = fy0[order]; sy1 = fy1[order]
    eps = 1e-6
    cand = bbp = over = 0
    N = len(ex)
    for a_ in range(N):
        hi = int(np.searchsorted(sx0, sx1[a_] + eps, side='right'))
        if hi <= a_ + 1: continue
        msk = (sx1[a_ + 1:hi] > sx0[a_] - eps) & (sy0[a_ + 1:hi] < sy1[a_] + eps) & (sy1[a_ + 1:hi] > sy0[a_] - eps)
        a = ex[int(order[a_])]
        for jj in np.nonzero(msk)[0]:
            c = ex[int(order[a_ + 1 + int(jj)])]
            cand += 1
            if not (a[1][0] < c[1][1] and c[1][0] < a[1][1] and a[2][0] < c[2][1] and c[2][0] < a[2][1]):
                continue                                    # bounding boxes do not overlap in their interiors
            bbp += 1
            axes = set()
            for z in (a, c):
                axes.update((1, 2) if z[0] != 'col' else (3, 4))   # edge normals of the two pieces
            if not any(a[q][1] <= c[q][0] or c[q][1] <= a[q][0] for q in axes):
                over += 1
    # the candidate generation must cover all pairs with overlapping boxes: the float margin 1e-6 is far above
    # the rounding error of the coordinates (all below 1e9 in absolute value, relative error 2^-53)
    r.update(pieces=N, V=int(V), cand_pairs=cand, bbox_pairs=bbp, overlaps=over)
    r['U'] = yreg * W + T * (W * W / 2 - s * W) - V
    r['pass'] = bool(r['unit_tilt'] and r['bad_shape'] == 0 and bad_c == 0 and over == 0)
    return r


def main():
    path, k = sys.argv[1], int(sys.argv[2])
    mutate = 'mutate' in sys.argv[3:]
    t0 = time.time()
    doc = json.loads(gzip.open(path, 'rb').read().decode('ascii') if path.endswith('.gz') else open(path).read())
    b = int(doc['b']); y0 = Q(doc['y0'])
    print(f'certificate {path}: k = {doc["k"]}, b = {b}, y0 = {doc["y0"]}, construction = {doc.get("construction")}; '
          f'arithmetic {ARITH}')
    ok = True
    if int(doc['k']) != k:
        print('FAIL: k in the file differs from the command line'); ok = False
    B = myband(b); W, T, d, h, s = B['W'], B['T'], B['d'], B['h'], B['s']
    S = k - b + W
    print(f'S < k: {S < k}   (k - S = {float(k - S):.6e})'); ok = ok and S < k and y0 >= 0
    ends = doc['ends']
    if [(e['band'], e['end']) for e in ends] != [('right', 'bottom'), ('right', 'top'), ('top', 'bottom'), ('top', 'top')]:
        print('FAIL: the file must list the ends right/bottom, right/top, top/bottom, top/top'); ok = False
    if mutate:
        e = ends[0]; ylift = Q(e['y'])
        base = check_end(B, e, ylift)
        print(f'unmutated end right/bottom: pass {base["pass"]}')
        acc = 0
        for mut in ('colshift', 'coldown', 'colgrow', 'layerup', 'layerlong', 'wedgeplus', 'region_lowered_1/100'):
            r = check_end(B, e, ylift - Q(1, 100), None) if mut.startswith('region') else check_end(B, e, ylift, mut)
            acc += r['pass']
            print(f'mutation {mut}: contain failures {r["bad_contain"]}, overlaps {r["overlaps"]}, '
                  f'shape failures {r["bad_shape"]} -> {"ACCEPTED (bad)" if r["pass"] else "rejected"}')
        print(f'wrongly accepted: {acc}')
        print(f'MUTATION TEST: {"PASS" if acc == 0 and base["pass"] else "FAIL"}  ({time.time() - t0:.1f} s)')
        return
    N = Q((k - b) ** 2); ident = Q(k) ** 2 - S * S; tot_pairs = 0
    for bi, (name, L) in enumerate([('right', S), ('top', Q(k - b))]):
        R = fl((L - h - 2 * y0) / d) + 1
        y1 = L - h - (R - 1) * d - y0
        cond = R >= 1 and y0 <= y1 < y0 + d
        print(f'{name} band: L = {float(L):.6f}, rows R = {R}, y1 = {float(y1):.9f}, y0 <= y1 < y0 + d: {cond}')
        ok = ok and cond
        N += b * R; ident += (R - 1) * T
        for e, yexp in ((ends[2 * bi], y0), (ends[2 * bi + 1], y1)):
            te = time.time()
            yl = Q(e['y'])
            room = yl + (W - s) * T < L
            r = check_end(B, e, yl)
            good = r['pass'] and yl == yexp and room
            ok = ok and good
            N += r['V']; ident += r['U'] + T / 2; tot_pairs += r['bbox_pairs']
            print(f'  {name}/{e["end"]} end: y matches {yl == yexp}, m = {e["m"]}, pieces {r["pieces"]} '
                  f'(columns {len(e["columns"])}, layers {len(e["layers"])}, wedge rows {len(e["wedge"])}), squares {r["V"]}, '
                  f'waste U = {float(r["U"]):.6f}; shape failures {r["bad_shape"]}, containment failures {r["bad_contain"]}, '
                  f'pairs with overlapping boxes {r["bbox_pairs"]} (candidates {r["cand_pairs"]}), overlaps {r["overlaps"]}, '
                  f'region below L {room} -> {"pass" if good else "FAIL"} ({time.time() - te:.1f} s)', flush=True)
    c = Q(k) ** 2 - N
    print(f'N = {int(N)}')
    print(f'c = k^2 - N = {int(c)}')
    print(f'waste identity holds exactly: {c == ident}'); ok = ok and c == ident
    print(f'exact pair decisions in the four ends: {tot_pairs}')
    print(f'c*(k) <= {int(c) - 1}   (N squares in a square of side S < k)')
    print(f'OVERALL: {"PASS" if ok else "FAIL"}  ({time.time() - t0:.1f} s)')


if __name__ == '__main__':
    main()
