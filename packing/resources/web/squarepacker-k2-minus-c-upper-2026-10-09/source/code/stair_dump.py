# stair_dump.py -- writes the explicit certificate of the "staircase" packing used for Table 1 of the paper.
#
# The packing of the square of side S = k - b + W is the L-shaped packing with lifted rows (Section "Band ends"
# of the paper): the (k-b)^2 grid, two bands of b x 1 tilted rows, and four end regions Reg(y), one at each end of
# each band.  Each end region is filled by the staircase construction: columns of one fixed tilt alpha whose lower
# squares are replaced by horizontal unit-square layers along a nondecreasing staircase, plus axis-parallel rows in
# the left wall wedge (idea: D. Bui, arXiv 2508.04603v2, Sec. 3).  This is the tuned variant used for the table:
# for each end, m (squares per column) is chosen by a floating-point pre-run among floor(y + rho) and
# floor(y + rho) + 1, and the tilt is the smallest t = u/2^40 (t = tan(alpha/2)) with m ca + sa <= y + (ca - s) T
# (column 0 fits; ca = cos alpha, sa = sin alpha).  The choices only select the packing; stair_check.py verifies the result exactly.
#
# Output (gzip-compressed JSON, exact rationals as strings "p/q"):
#   {"k", "b", "y0", "construction": "stair",
#    "ends": [ {"band": "right"|"top", "end": "bottom"|"top", "y", "m", "t", "ca", "sa",
#               "columns": [[X, Y, n], ...],  tilted 1 x n rectangle with vertices (X, Y), (X, Y) + (ca, sa),
#                                              (X, Y) + (ca, sa) + n (-sa, ca), (X, Y) + n (-sa, ca)
#               "layers":  [[x0, j, L], ...], axis rectangle [x0, x0 + L] x [j, j + 1]
#               "wedge":   [[h, l], ...]  },  axis rectangle [0, l] x [h, h + 1]
#             ... four ends ...]}
# Coordinates are in the end's own frame: Reg(y) = {0 <= X <= W, 0 <= Y <= y + (X - s) T}.
#
# Usage: python code/stair_dump.py <k> <b> <y0> [out.json.gz]      (y0 may be "p/q")
#        python code/stair_dump.py table [outdir]                     (the five rows of Table 1)
import sys, os, math, json, gzip, time
try:
    import gmpy2
    F = gmpy2.mpq
    def floor(x): return int(gmpy2.floor(x))
except ImportError:
    from fractions import Fraction as F
    def floor(x): return math.floor(x)

TABLE = [(100000, 623, '257/4'), (1000000, 2481, '653/4'), (10000000, 9875, '1663/4'),
         (38250000, 22086, '710'), (100000000, 39314, '1041')]


def band(b, Fr=F):
    tt = (b / (b * b - 1)) if Fr is float else Fr(b, b * b - 1)      # tan(theta/2) = b/(b^2-1)
    c = (1 - tt * tt) / (1 + tt * tt); s = 2 * tt / (1 + tt * tt)
    return dict(c=c, s=s, W=b * c + s, T=s / c)


def tilt(t):
    ca = (1 - t * t) / (1 + t * t); sa = 2 * t / (1 + t * t)
    return ca, sa, sa / ca, 1 / ca


def choose_t(B, y, m, Fr, Q=2 ** 40):
    """smallest grid t = u/Q with m ca + sa <= y + (ca - s) T (column 0 with J = 0 fits under the ceiling)."""
    def ok(t):
        ca, sa, ta, se = tilt(t)
        return m * ca + sa <= y + (ca - B['s']) * B['T']
    lo, hi = 0.0, 0.9
    yf = float(y); sf = float(B['s']); Tf = float(B['T'])
    for _ in range(200):
        mid = (lo + hi) / 2
        ca = (1 - mid * mid) / (1 + mid * mid); sa = 2 * mid / (1 + mid * mid)
        if m * ca + sa <= yf + (ca - sf) * Tf: hi = mid
        else: lo = mid
    if Fr is float:
        return hi
    u = math.ceil(hi * Q); t = Fr(u, Q)
    while not ok(t): u += 1; t = Fr(u, Q)
    while u > 1 and ok(Fr(u - 1, Q)): u -= 1; t = Fr(u, Q)
    return t


def construct(b, y, m, Fr=F):
    B = band(b, Fr); y = Fr(y) if Fr is not float else float(y)
    W, T, s = B['W'], B['T'], B['s']
    g = lambda x: y + (x - s) * T
    fl = floor if Fr is not float else math.floor
    t = choose_t(B, y, m, Fr)
    ca, sa, ta, se = tilt(t)
    c0 = m * sa
    cols = []                                    # (c_i, J_i, n_i); column i lies in the slab c_i <= X + Y ta <= c_i + se
    J = 0; i = 0
    while True:
        ci = c0 + i * se
        def fits(Jp):
            n = m - Jp; px = ci - Jp * ta
            if px + ca > W: return None
            if n == 0: return True
            return (Jp + n * ca <= g(px - n * sa)) and (Jp + sa + n * ca <= g(px + ca - n * sa))
        f = fits(J)
        if f is None: break
        if not f:
            raise RuntimeError('column %d does not fit at J=%d' % (i, J))
        while J < m and fits(J + 1): J += 1
        if J == m: break
        cols.append((ci, J, m - J)); i += 1
    layers = []                                  # (j, a_j, L_j)
    idx = 0
    for j in range(0, fl(g(W)) - 1 + 1):
        while idx + 1 < len(cols) and cols[idx + 1][1] <= j: idx += 1
        ci, Ji, ni = cols[idx]
        a = ci + se - j * ta
        if not (j + 1 <= g(a)):
            a = s + (j + 1 - y) / T              # ceiling too low at the left end: start where the row fits
        L = fl(W - a)
        if L >= 1: layers.append((j, a, L))
    wedge = []                                   # (h, l)
    h = 0; g0 = g(Fr(0) if Fr is not float else 0.0)
    while h + 1 <= g0:
        L = fl(c0 - (h + 1) * ta)
        if L >= 1: wedge.append((h, L))
        h += 1
    return dict(B=B, y=y, m=m, t=t, ca=ca, sa=sa, ta=ta, se=se, cols=cols, layers=layers, wedge=wedge)


def waste(C):
    B = C['B']; W, T, s, y = B['W'], B['T'], B['s'], C['y']
    V = sum(n for (_, _, n) in C['cols']) + sum(L for (_, _, L) in C['layers']) + sum(L for (_, L) in C['wedge'])
    return y * W + T * (W * W / 2 - s * W) - V


def best_m(b, y):
    """float pre-run: m in {floor(y + rho), floor(y + rho) + 1} with the smaller waste (a choice only)."""
    Bf = band(b, float); rho = Bf['W'] * Bf['T']; yf = float(y)
    best = None
    for m in (math.floor(yf + rho), math.floor(yf + rho) + 1):
        try:
            U = waste(construct(b, yf, m, float))
            if best is None or U < best[1]: best = (m, U)
        except Exception:
            pass
    return best[0]


def q(x):
    x = F(x); return str(x.numerator) if x.denominator == 1 else '%d/%d' % (x.numerator, x.denominator)


def dump(k, b, y0, out):
    t0 = time.time()
    y0 = F(*map(int, y0.split('/'))) if '/' in str(y0) else F(int(y0))
    B = band(b); W, c, s = B['W'], B['c'], B['s']
    d = 1 / c; h = b * s + c; S = k - b + W
    assert S < k
    doc = {'k': k, 'b': b, 'y0': q(y0), 'construction': 'stair', 'ends': []}
    nV = 0
    for name, L in (('right', S), ('top', F(k - b))):
        R = floor((L - h - 2 * y0) / d) + 1
        y1 = L - h - (R - 1) * d - y0
        assert R >= 1 and y0 <= y1 < y0 + d
        for endname, y in (('bottom', y0), ('top', y1)):
            m = best_m(b, y)
            C = construct(b, y, m)
            ca, sa, ta = C['ca'], C['sa'], C['ta']
            e = {'band': name, 'end': endname, 'y': q(y), 'm': m, 't': q(C['t']), 'ca': q(ca), 'sa': q(sa),
                 'columns': [[q(ci - J * ta), J, n] for (ci, J, n) in C['cols']],
                 'layers': [[q(a), j, Ln] for (j, a, Ln) in C['layers']],
                 'wedge': [[hh, Ln] for (hh, Ln) in C['wedge']]}
            nV += sum(n for (_, _, n) in C['cols']) + sum(Ln for (_, _, Ln) in C['layers']) + sum(Ln for (_, Ln) in C['wedge'])
            doc['ends'].append(e)
            print(f'  {name} band, {endname} end: y = {float(y):.6f}, m = {m}, columns {len(e["columns"])}, '
                  f'layers {len(e["layers"])}, wedge rows {len(e["wedge"])}', flush=True)
    raw = json.dumps(doc, separators=(',', ':')).encode('ascii')
    with open(out, 'wb') as fh:
        with gzip.GzipFile(filename='', mode='wb', fileobj=fh, mtime=0) as gz:
            gz.write(raw)
    print(f'k = {k}: wrote {out} ({os.path.getsize(out)} bytes); squares in the four ends: {nV}; '
          f'{time.time() - t0:.1f} s', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'table':
        od = sys.argv[2] if len(sys.argv) > 2 else 'data'
        for k, b, y0 in TABLE:
            dump(k, b, y0, os.path.join(od, f'stair_k{k}.json.gz'))
    else:
        k, b, y0 = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
        dump(k, b, y0, sys.argv[4] if len(sys.argv) > 4 else os.path.join('data', f'stair_k{k}.json.gz'))
