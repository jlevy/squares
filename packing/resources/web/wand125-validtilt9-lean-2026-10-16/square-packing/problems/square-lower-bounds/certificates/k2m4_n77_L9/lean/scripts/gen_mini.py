#!/usr/bin/env python3
"""A rehearsal of `gen_main.py`: the roots of a block of the grid (around a given root, `nx × ny` in
x, y, all u bins) glued into one `CovT`, in `MiniMain.lean`.  Prints the roots' indices.

    gen_mini.py ROOT NX NY OUT.lean
"""
import os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tree_rebuild import load  # noqa: E402
from run_v7 import LEAVES, SG, RG, MQ  # noqa: E402

D, W = 5, 10 ** 12
Q = D * SG


def main(root, nx, ny, out):
    roots = [(i, r) for i, (r, l, u) in enumerate(load(LEAVES))]
    xs = sorted({r[0] for _, r in roots} | {r[1] for _, r in roots})
    ys = sorted({r[2] for _, r in roots} | {r[3] for _, r in roots})
    us = sorted({r[4] for _, r in roots} | {r[5] for _, r in roots})
    at = {(xs.index(r[0]), ys.index(r[2]), us.index(r[4])): i for i, r in roots}
    r0 = dict(roots)[root]
    a0, b0 = min(xs.index(r0[0]), len(xs) - 1 - nx), min(ys.index(r0[2]), len(ys) - 1 - ny)
    a1, b1, c0, c1 = a0 + nx, b0 + ny, 0, len(us) - 1
    iq = lambda x: int(x * Q)
    ir = lambda u: int(u * RG)

    def glue(a0, a1, b0, b1, c0, c1):
        if a1 - a0 == 1 and b1 - b0 == 1 and c1 - c0 == 1:
            return f"root_{at[(a0, b0, c0)]:05d}"
        if c1 - c0 > 1:
            m = (c0 + c1) // 2
            return f"(CovT.splitU {ir(us[m])} {glue(a0, a1, b0, b1, c0, m)} {glue(a0, a1, b0, b1, m, c1)})"
        if a1 - a0 >= b1 - b0:
            m = (a0 + a1) // 2
            return f"(CovT.splitX {iq(xs[m])} {glue(a0, m, b0, b1, c0, c1)} {glue(m, a1, b0, b1, c0, c1)})"
        m = (b0 + b1) // 2
        return f"(CovT.splitY {iq(ys[m])} {glue(a0, a1, b0, m, c0, c1)} {glue(a0, a1, m, b1, c0, c1)})"

    idx = sorted(at[(a, b, c)] for a in range(a0, a1) for b in range(b0, b1) for c in range(c0, c1))
    lines = ["import Sqpack.V7.Data"] + [f"import Sqpack.V7.R{i:05d}" for i in idx]
    lines += ["namespace SquarePacking", "namespace LemmaELeaf", "open ZMTreeM ZMTree", "",
              f"theorem mini : CovT {D} {SG} {MQ} {RG} {W} [] tsegs trects {iq(xs[a0])} {iq(xs[a1])} "
              f"{iq(ys[b0])} {iq(ys[b1])} {ir(us[c0])} {ir(us[c1])} :=",
              f"  {glue(a0, a1, b0, b1, c0, c1)}", "", "end LemmaELeaf", "end SquarePacking"]
    open(out, 'w').write("\n".join(lines) + "\n")
    print(" ".join(str(i) for i in idx))


if __name__ == '__main__':
    main(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
