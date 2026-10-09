#!/usr/bin/env python3
"""gen_bentzfam_data.py -- write the data module for `BentzFam.lean` (task lean-k2m4-reduction).

Generic in the edge-zone width R (pitch 1/5).  Default: the k^2 - 4 family (R = 3, box 2R + 3 = 9), writing
lean/Sqpack/Bentz4Data.lean from
  search/qx2_data/K4_k008_box9.txt    the box cover k = 9 (FORMAT.md v1, verbatim: `boxSegs`, `boxPolyVerts`,
                                      `boxPolyW` -- this is what `Bentz4.Valid9` is about);
  search/qx2_data/K4_k008_family.txt  the fixed-profile family (R = w = 3, pitch 1/5): the tables `famTab`,
                                      `famTab2` from which `BentzFam.famCover` builds mu_k for every k.
Nothing here is trusted by Lean: `BentzFam.lean` / `Bentz4.lean` prove (kernel evaluation) that `famCover 9` is
the box file's cover, and prove the accounting and the reduction for all k.

Codes (N = 5R, table width B = 5R + 7, `OUT` = 5R + 6):
  cell [i/5, (i+1)/5] of [0,k]:  offset 0..N-1 from the nearer wall (i < N, or i >= 5k - N: 5k - 1 - i);
                                 N + p for a band cell of phase p = i mod 5;  OUT outside [0,k].
  line j/5 of [0,k]:             offset 0..N from the nearer wall (j <= N, or j >= 5k - N: 5k - j) -- the
                                 band's closed ends R, k - R have their own code N;  N + 1 + p for an interior
                                 band line of phase p = j mod 5;  OUT outside.
famTab[c][l] = mass (units 1/den) of the horizontal unit segment whose x-cell has code c and y-line code l
(vertical segments: the diagonal image).
  corner module:  H y x0 x1 m -> (5 x0, 5 y)   (V x y0 y1 m -> (5 y0, 5 x), the same entry: nu is diagonal-
                  symmetric; checked).  Pieces on the line y = R (offset N) go to the second layer `famTab2`;
  profile:        h y p0 p1 m -> (N + 5 p0, 5 y);
                  v p y0 y1 m -> (5 y0, N + 1 + 5 p), and for p = 0 also (5 y0, N) (the band's end line).
The second layer exists because the box file lists the corner-module piece and the profile piece on the band's
end line x = R (or y = R) as two separate entries of the same unit segment; layer 2 holds the corner-module part,
so every file entry is one (layer, segment) of the family.  (For R = 2, `L4_k02_*`, layer 2 would be empty.)

usage: python3 lean/scripts/gen_bentzfam_data.py [--search search] [--out lean/Sqpack/Bentz4Data.lean]
(run from s12/; deterministic)
"""
import argparse, hashlib, os, re
from collections import Counter
from fractions import Fraction as F


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def read_box(path, K):
    tok = []
    for ln in open(path):
        tok += ln.split('#', 1)[0].split()
    it = iter(tok)
    assert next(it) == 'mixed' and next(it) == '1'
    sn, sd, D, Wd = (int(next(it)) for _ in range(4))
    assert (sn, sd, D) == (K, 1, 5), (sn, sd, D)
    npt = int(next(it)); assert npt == 0, 'points present'
    ns = int(next(it))
    segs = [tuple(int(next(it)) for _ in range(5)) for _ in range(ns)]
    npg = int(next(it)); assert npg == 1
    kk = int(next(it)); pw = int(next(it))
    verts = [(int(next(it)), int(next(it))) for _ in range(kk)]
    rest = list(it); assert not rest, rest
    return segs, verts, pw, Wd


def read_family(path, Wd):
    head = open(path).read()
    R = int(re.search(r'R = (\d+)', head).group(1))
    a = F(re.search(r'a = (\d+/\d+)', head).group(1))
    N = 5 * R
    tab, tab2 = {}, {}

    def put(t, c, l, m):
        assert 0 <= c < N + 5 and 0 <= l <= N + 5, (c, l)
        assert (c, l) not in t or t[(c, l)] == m, ('conflict', c, l)
        t[(c, l)] = m

    for ln in open(path):
        if ln.startswith('#'):
            continue
        t = ln.split()
        if not t:
            continue
        v = [F(x) for x in t[1:]]
        m = v[-1] * Wd
        assert m.denominator == 1 and m > 0
        m = int(m)
        if t[0] == 'H':
            y, x0, x1 = v[:3]; assert x1 - x0 == F(1, 5) and 0 <= x0 and x1 <= R and 0 < y <= R
            put(tab2 if y == R else tab, int(5 * x0), int(5 * y), m)
        elif t[0] == 'V':
            x, y0, y1 = v[:3]; assert y1 - y0 == F(1, 5) and 0 <= y0 and y1 <= R and 0 < x <= R
            put(tab2 if x == R else tab, int(5 * y0), int(5 * x), m)
        elif t[0] == 'h':
            y, p0, p1 = v[:3]; assert p1 - p0 == F(1, 5) and 0 <= p0 and p1 <= 1 and 0 < y < R
            put(tab, N + int(5 * p0), int(5 * y), m)
        elif t[0] == 'v':
            p, y0, y1 = v[:3]; assert y1 - y0 == F(1, 5) and 0 <= p < 1 and 0 <= y0 and y1 <= R
            put(tab, int(5 * y0), N + 1 + int(5 * p), m)
            if p == 0:
                put(tab, int(5 * y0), N, m)
        else:
            raise ValueError(ln)
    return R, a, tab, tab2


def cellT(R, k, i):
    N = 5 * R
    if i < 0 or 5 * k <= i:
        return N + 6
    if i < N:
        return i
    if 5 * k - N <= i:
        return 5 * k - 1 - i
    return N + i % 5


def lineT(R, k, j):
    N = 5 * R
    if j < 0 or 5 * k < j:
        return N + 6
    if j <= N:
        return j
    if 5 * k - N <= j:
        return 5 * k - j
    return N + 1 + j % 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--search', default='search')
    ap.add_argument('--box', default='qx2_data/K4_k008_box9.txt')
    ap.add_argument('--family', default='qx2_data/K4_k008_family.txt')
    ap.add_argument('--ns', default='Bentz4')
    ap.add_argument('--out', default='lean/Sqpack/Bentz4Data.lean')
    A = ap.parse_args()
    boxp = os.path.join(A.search, A.box)
    famp = os.path.join(A.search, A.family)
    # the box header's mass denominator (`mixed 1 / side / coordinate denominator / mass denominator`)
    tok = []
    for ln in open(boxp):
        tok += ln.split('#', 1)[0].split()
    Wd = int(tok[5])
    R, a, tab, tab2 = read_family(famp, Wd)
    K = 2 * R + 3
    segs, verts, pw, Wd2 = read_box(boxp, K)
    assert Wd2 == Wd
    N, B = 5 * R, 5 * R + 7
    Aq = 5 * a; assert Aq.denominator == 1 and 0 <= Aq <= N; Aq = int(Aq)
    # Python mirror of the kernel checks: every file segment is a unit grid segment whose mass is the family's in
    # layer 1 or (if not) layer 2; no (layer, segment) twice; every nonzero (layer, segment) of [0,K]^2 is listed.
    T = [dict(tab), dict(tab2)]

    def wN(lay, o, i, j):
        c, l = (cellT(R, K, j), lineT(R, K, i)) if o else (cellT(R, K, i), lineT(R, K, j))
        return T[lay].get((c, l), 0)

    keys = []
    for (x0, y0, x1, y1, w) in segs:
        if y0 == y1:
            assert abs(x1 - x0) == 1; o, i, j = 0, min(x0, x1), y0
        else:
            assert x0 == x1 and abs(y1 - y0) == 1; o, i, j = 1, x0, min(y0, y1)
        lay = 0 if wN(0, o, i, j) == w else 1
        assert w > 0 and wN(lay, o, i, j) == w, (x0, y0, x1, y1, w)
        keys.append((lay, o, i, j))
    assert len(set(keys)) == len(keys)
    full = {(lay, o, i, j) for lay in (0, 1) for o in (0, 1) for i in range(5 * K + 1) for j in range(5 * K + 1)
            if wN(lay, o, i, j)}
    assert full == set(keys), (len(full), len(keys))
    assert verts == [(Aq, Aq), (5 * K - Aq, Aq), (5 * K - Aq, 5 * K - Aq), (Aq, 5 * K - Aq)], verts
    assert F(pw, Wd) == (K - F(2 * Aq, 5)) ** 2
    nlay2 = sum(1 for k in keys if k[0] == 1)
    flat = [tab.get((c, l), 0) for c in range(B) for l in range(B)]
    flat2 = [tab2.get((c, l), 0) for c in range(B) for l in range(B)]
    out = []
    out.append(f'/-!\n# Data for `{A.ns}.lean` (generated by `lean/scripts/gen_bentzfam_data.py`; do not edit)\n')
    out.append(f'* `search/{A.box}` sha256 `{sha(boxp)}`')
    out.append(f'* `search/{A.family}` sha256 `{sha(famp)}`\n')
    out.append(f'`boxSegs`, `boxPolyVerts`, `boxPolyW` are the box file verbatim (header `mixed 1`, side `{K}/1`, '
               f'coordinate\ndenominator `5`, mass denominator `{Wd}`, no points, '
               f'{len(segs)} segments `(X0, Y0, X1, Y1, w)` in file order, one polygon).\n'
               f'`famTab`, `famTab2` are the family file as two {B} × {B} tables (R = {R}, see the script; '
               f'{nlay2} file entries are layer 2).\n-/\n')
    out.append(f'namespace SquarePacking.{A.ns}\n')
    out.append('set_option maxRecDepth 20000 in')
    out.append(f'/-- The {len(segs)} segments `(X0, Y0, X1, Y1, w)` of `{os.path.basename(A.box)}`, in file order. -/')
    out.append('def boxSegs : List (Nat × Nat × Nat × Nat × Nat) := [')
    body = [f'  ({a_}, {b}, {c}, {d}, {w})' for (a_, b, c, d, w) in segs]
    out.append(',\n'.join(body) + ']\n')
    out.append(f'/-- The polygon of `{os.path.basename(A.box)}`: its vertices `(X, Y)` (counter-clockwise), '
               'and its mass `w`. -/')
    out.append('def boxPolyVerts : List (Nat × Nat) := [' + ', '.join(f'({x}, {y})' for x, y in verts) + ']\n')
    out.append(f'def boxPolyW : Nat := {pw}\n')
    for nm, fl, what in (('famTab', flat, 'layer 1'), ('famTab2', flat2, 'layer 2: the corner module on the '
                                                                          "band's end lines")):
        out.append(f'/-- The family `{os.path.basename(A.family)}`, {what}: row `c`, column `l` (units `1/{Wd}`). -/')
        out.append(f'def {nm} : List (List Nat) := [')
        rows = ['  [' + ', '.join(str(x) for x in fl[B * c:B * c + B]) + ']' for c in range(B)]
        out.append(',\n'.join(rows) + ']\n')
    out.append('set_option maxRecDepth 20000 in')
    out.append('/-- The keys `keyN (fileIx e)` of the box file entries, in file order (checked by the kernel). -/')
    out.append('def boxKeys : List Nat := [')
    kl = [((o * 4096 + i) * 4096 + j) * 2 + lay for (lay, o, i, j) in keys]
    out.append(',\n'.join('  ' + ', '.join(str(x) for x in kl[r:r + 12]) for r in range(0, len(kl), 12)) + ']\n')
    gk = sorted(kl)
    out.append('set_option maxRecDepth 20000 in')
    out.append('/-- The same keys sorted: the keys of the non-zero (segment, layer)s of the box (checked by the kernel). -/')
    out.append('def boxGridKeys : List Nat := [')
    out.append(',\n'.join('  ' + ', '.join(str(x) for x in gk[r:r + 12]) for r in range(0, len(gk), 12)) + ']\n')
    out.append(f'end SquarePacking.{A.ns}')
    open(A.out, 'w').write('\n'.join(out) + '\n')
    print(f'wrote {A.out}: R = {R}, A = {Aq}/5, K = {K}, den = {Wd}, {len(segs)} segments ({nlay2} in layer 2), '
          f'{len(tab)} + {len(tab2)} nonzero table entries')


if __name__ == '__main__':
    main()
