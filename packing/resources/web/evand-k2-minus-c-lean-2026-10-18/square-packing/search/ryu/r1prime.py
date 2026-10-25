"""Ryu's L-shaped packing (Theorem 1.3) with filled band ends ("R1'", literature/waste-constructions-2026-10-17.md
§3), in exact rationals, in the frame of lean/Sqpack/RyuBand.lean.

Band frame: strip [0, w] x [0, L], w = b*gam + sig, rows j = 0..R-1 of b squares at angle theta (cos = gam,
sin = sig), centres ctr(i, j) as in RyuBand.ctr.  Rotated coordinate V(p) = -p.x*sig + p.y*gam; band squares fill
V in [-sig^2, R - sig^2].
* bottom fill: axis squares [x, x+1] x [0, 1] with all corners at V <= -sig^2;
* top fill: axis squares [x, x+1] x [L-1-r, L-r] (layers r = 0, 1, ...) with all corners at V >= R - sig^2.
L-shape: right band in [m, m+w] x [0, m+w], top band (transposed) in [0, m] x [m, m+w], grid m x m, m = k - b.

  python3 search/ryu/r1prime.py K [K ...]          best b per k: c = k^2 - N, and Ryu's 8*ceil(sqrt(k-4))
  python3 search/ryu/r1prime.py --check K B       build the packing, exact pairwise check, write it out
"""
import sys, math
from fractions import Fraction as F


def trig(t):
    return (1 - t * t) / (1 + t * t), 2 * t / (1 + t * t)


def floor(x):
    return math.floor(x)


def band_counts(b, L, t):
    """rows R (max), bottom fill, top fill counts in the strip [0, w] x [0, L]."""
    gam, sig = trig(t)
    w = b * gam + sig
    h = b * sig + gam
    if h > L:
        return 0, 0, 0, w
    R = floor((L - h) * gam) + 1           # (R - 1)/gam + h <= L
    # bottom: x >= (gam + sig^2)/sig and x + 1 <= w
    x0 = (gam + sig * sig) / sig
    nb = max(0, floor(w - x0))             # x = w-1, w-2, ..., >= x0
    # top: layer r, x + 1 <= ((L - 1 - r) gam - R + sig^2)/sig, x >= 0, x + 1 <= w
    nt = 0
    r = 0
    while True:
        cap = ((L - 1 - r) * gam - R + sig * sig) / sig
        n = min(floor(cap), floor(w))
        if n <= 0 or L - 1 - r < 0:
            break
        nt += n
        r += 1
    return R, nb, nt, w


def count(k, b, t=None, fills=True):
    if t is None:
        t = F(1, b) + F(1, 10 ** 12)
    m = k - b
    gam, sig = trig(t)
    w = b * gam + sig
    if not w < b:
        return None
    R1, nb1, nt1, _ = band_counts(b, m + w, t)
    R2, nb2, nt2, _ = band_counts(b, F(m), t)
    N = m * m + b * (R1 + R2) + (nb1 + nt1 + nb2 + nt2 if fills else 0)
    return N, dict(R1=R1, R2=R2, nb1=nb1, nt1=nt1, nb2=nb2, nt2=nt2)


def best(k, fills=True):
    res = None
    for b in range(2, k - 3):
        r = count(k, b, fills=fills)
        if r and (res is None or r[0] > res[1]):
            res = (b, r[0], r[1])
    return res


# ---------------------------------------------------------------- explicit packing + exact check
def squares(k, b, t):
    """list of (cx, cy, c, s): centre and (cos, sin), container [0, k - (b - w)]^2."""
    m = k - b
    gam, sig = trig(t)
    w = b * gam + sig
    out = []
    for i in range(m):
        for j in range(m):
            out.append((F(2 * i + 1, 2), F(2 * j + 1, 2), F(1), F(0)))

    def band(L):
        R, nb, nt, _ = band_counts(b, L, t)
        sq = []
        for j in range(R):
            for i in range(b):
                a = i + F(1, 2) + j * (sig / gam)
                c2 = j + F(1, 2)
                sq.append((sig + a * gam - c2 * sig, a * sig + c2 * gam, gam, sig))
        for q in range(nb):
            x = floor(w) - 1 - q if False else None
        # bottom fill: x = w - 1 - q exactly would leave x non-integer; use x = w - 1 - q
        for q in range(nb):
            x = w - 1 - q
            sq.append((x + F(1, 2), F(1, 2), F(1), F(0)))
        r = 0
        left = nt
        while left > 0:
            cap = ((L - 1 - r) * gam - R + sig * sig) / sig
            n = min(floor(cap), floor(w))
            for q in range(n):
                sq.append((q + F(1, 2), L - r - F(1, 2), F(1), F(0)))
            left -= n
            r += 1
        return sq

    for (x, y, c, s) in band(m + w):                     # right band at x in [m, m+w]
        out.append((m + x, y, c, s))
    for (x, y, c, s) in band(F(m)):                      # top band, transposed: (x, y) -> (y, x), angle pi/2 - theta
        out.append((y, m + x, s, c))
    return out, m + w


def corners(q):
    x, y, c, s = q
    return [(x + c * a - s * bb, y + s * a + c * bb) for a in (F(1, 2), F(-1, 2)) for bb in (F(1, 2), F(-1, 2))]


def separated(p, q):
    """some side line of p or q has the other's corners on its closed outer side"""
    for (A, B) in ((p, q), (q, p)):
        x, y, c, s = A
        for (nx, ny) in ((c, s), (-s, c), (-c, -s), (s, -c)):
            if all(nx * (X - x) + ny * (Y - y) >= F(1, 2) for (X, Y) in corners(B)):
                return True
    return False


def check(k, b, t=None):
    if t is None:
        t = F(1, b) + F(1, 10 ** 12)
    sq, S = squares(k, b, t)
    for q in sq:
        for (X, Y) in corners(q):
            assert 0 <= X <= S and 0 <= Y <= S, ('wall', q)
    sq_sorted = sorted(sq, key=lambda q: q[0])
    n = len(sq_sorted)
    for i in range(n):
        for j in range(i + 1, n):
            if sq_sorted[j][0] - sq_sorted[i][0] >= F(3, 2):
                break
            p, q = sq_sorted[i], sq_sorted[j]
            if (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 >= 2:
                continue
            assert separated(p, q), ('pair', p, q)
    return n, S


if __name__ == '__main__':
    if sys.argv[1] == '--check':
        k, b = int(sys.argv[2]), int(sys.argv[3])
        n, S = check(k, b)
        print(f'k={k} b={b}: {n} squares, side {float(S):.12f} < {k}: VALID (exact, closed)', 'c =', k * k - n)
    else:
        for k in map(int, sys.argv[1:]):
            bb, N, info = best(k)
            b0, N0, _ = best(k, fills=False)
            print(f'k={k}: best b={bb} c={k*k-N} {info} | no fills: b={b0} c={k*k-N0} | Ryu 8ceil(sqrt(k-4)) = '
                  f'{8*math.ceil(math.sqrt(k-4))}')
