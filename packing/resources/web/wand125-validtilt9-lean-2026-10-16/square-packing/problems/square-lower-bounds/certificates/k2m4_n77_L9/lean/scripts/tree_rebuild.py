#!/usr/bin/env python3
"""Rebuild the split trees of a qx2_zm leaf dump (runV3 *_leaves.jsonl.gz) from the leaves alone.

At a node (box B): clip the angle bin (zeromargin.clip_bin, as qx2_zm does), then either B is a leaf of
the dump, or exactly one of the midpoints in x, y, u puts every leaf inside B on one side.  The tree is
returned as nested tuples: ('L', box, kind) | ('C', us, child) | ('X'|'Y'|'U', mid, left, right).
Nothing here is trusted: the Lean proof re-derives every node from the lemmas of `ExTree.lean`.
"""
import gzip, json, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'certificates', 'k2m3', 'qx2_zm', 'checker'))
import zeromargin as zm  # noqa: E402

THETA_BIAS = 4


def inside(b, B):
    return B[0] <= b[0] and b[1] <= B[1] and B[2] <= b[2] and b[3] <= B[3] and B[4] <= b[4] and b[5] <= B[5]


def build(B, leaves, m, clip=True):
    cx0, cx1, cy0, cy1, u0, u1 = B
    node_clip = None
    if clip and u1 > u0:
        cu1 = zm.clip_bin(B, m)
        if cu1 < u1:
            node_clip = cu1
            B = (cx0, cx1, cy0, cy1, u0, cu1)
    for b, k in leaves:
        if b == B:
            if len(leaves) != 1:
                raise ValueError(f"leaf {B} with {len(leaves)} leaves inside")
            t = ('L', B, k)
            return ('C', node_clip, t) if node_clip is not None else t
    # the split rule of qx2_zm.QXChecker.run_box (zm_mixed's, theta_bias = 4)
    cx0, cx1, cy0, cy1, u0, u1 = B
    bd = zm.bin_data(u0, u1)
    dx, dy, du = cx1 - cx0, cy1 - cy0, 2 * (u1 - u0)
    if THETA_BIAS > 1 and u0 * 2 < bd['wlo'] and (
            cx0 < bd['whi'] / 2 or cx1 > m - bd['whi'] / 2 or cy0 < bd['whi'] / 2 or cy1 > m - bd['whi'] / 2):
        du = du * THETA_BIAS
    if dx >= dy and dx >= du: ax, i, j = 'X', 0, 1
    elif dy >= du: ax, i, j = 'Y', 2, 3
    else: ax, i, j = 'U', 4, 5
    mid = (B[i] + B[j]) / 2
    hi = [(b, k) for b, k in leaves if b[i] >= mid]
    lo = [(b, k) for b, k in leaves if b[i] < mid]
    if lo and hi and all(b[j] <= mid for b, _ in lo):
        Bl = list(B); Bl[j] = mid; Bh = list(B); Bh[i] = mid
        t = (ax, mid, build(tuple(Bl), lo, m, clip), build(tuple(Bh), hi, m, clip))
        return ('C', node_clip, t) if node_clip is not None else t
    raise ValueError(f"no split for {B} ({len(leaves)} leaves)")


def load(path):
    f = gzip.open(path, 'rt'); f.readline()
    for line in f:
        r = json.loads(line)
        root = tuple(F(x) for x in r['root'])
        leaves = [(tuple(F(x) for x in b), k) for b, k in r['leaves']]
        yield root, leaves, r['unc']


def count(t):
    if t[0] == 'L': return {t[2]: 1}
    if t[0] == 'C': return count(t[2])
    a, b = count(t[2]), count(t[3])
    for k, v in b.items(): a[k] = a.get(k, 0) + v
    return a


if __name__ == '__main__':
    path = sys.argv[1]; m = F(sys.argv[2]) if len(sys.argv) > 2 else F(7)
    tot = {}; nroot = 0; nclip = 0
    for root, leaves, unc in load(path):
        assert not unc
        t = build(root, leaves, m)
        c = count(t)
        assert sum(c.values()) == len(leaves)
        for k, v in c.items(): tot[k] = tot.get(k, 0) + v
        nroot += 1
    print(nroot, 'roots', tot)
