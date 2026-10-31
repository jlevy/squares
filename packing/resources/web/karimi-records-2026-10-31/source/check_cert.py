#!/usr/bin/env python3
"""Independent exact checker for square-packing certificates.

Format: '# ...' comment lines, then 'n S', then n lines 'x y t'
(centre, t = tan(theta/2)). Every unit square must lie in [0, S]^2 and
no two may share interior points (touching allowed). Exact rationals,
separating-axis test for every pair whose centres are closer than sqrt(2).

    python3 check_cert.py file.cert [--mutate]
"""
import sys, random
from fractions import Fraction as F


def corners(x, y, t):
    c = (1 - t * t) / (1 + t * t)
    s = 2 * t / (1 + t * t)
    ex, ey = c / 2, s / 2          # half edge along (c, s)
    fx, fy = -s / 2, c / 2         # half edge along (-s, c)
    return [(x + a * ex + b * fx, y + a * ey + b * fy)
            for a in (1, -1) for b in (1, -1)], [(c, s), (-s, c)]


def proj(pts, ax):
    v = [p[0] * ax[0] + p[1] * ax[1] for p in pts]
    return min(v), max(v)


def interiors_disjoint(A, B):
    pa, axa = A
    pb, axb = B
    for ax in axa + axb:
        a0, a1 = proj(pa, ax)
        b0, b1 = proj(pb, ax)
        if a1 <= b0 or b1 <= a0:
            return True
    return False


def check(n, S, sq):
    if len(sq) != n:
        return f'count {len(sq)} != {n}'
    shapes = [corners(*q) for q in sq]
    for k, (pts, _) in enumerate(shapes):
        for px, py in pts:
            if px < 0 or py < 0 or px > S or py > S:
                return f'square {k} leaves the container'
    cells = {}
    for k, (x, y, t) in enumerate(sq):
        cells.setdefault((int(x // 1), int(y // 1)), []).append(k)
    for (cx, cy), lst in cells.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                other = cells.get((cx + dx, cy + dy), [])
                for i in lst:
                    for j in other:
                        if j <= i:
                            continue
                        xi, yi, _ = sq[i]
                        xj, yj, _ = sq[j]
                        if (xi - xj) ** 2 + (yi - yj) ** 2 >= 2:
                            continue
                        if not interiors_disjoint(shapes[i], shapes[j]):
                            return f'squares {i} and {j} overlap'
    return 'OK'


def read(path):
    lines = [l for l in open(path) if l.strip() and not l.startswith('#')]
    n, S = lines[0].split()
    sq = [tuple(F(v) for v in l.split()) for l in lines[1:]]
    return int(n), F(S), sq


if __name__ == '__main__':
    n, S, sq = read(sys.argv[1])
    print('check:', check(n, S, sq))
    if '--mutate' in sys.argv:
        random.seed(1)
        bad = 0
        for trial in range(5):
            m = list(sq)
            k = random.randrange(len(m))
            x, y, t = m[k]
            m[k] = (x + F(1, 1000), y, t)     # small push
            r = check(n, S, m)
            bad += r != 'OK'
            print('mutation', trial, '->', r)
        m = list(sq); m.append(m[0])
        print('duplicate ->', check(n + 1, S, m))
