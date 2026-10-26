#!/usr/bin/env python3
"""The face theta = 0 of Valid7 (Lemma Z, `LemmaZ.lean`): cells of the 1/10 grid on [1/2, 7/2]^2, each
`CovMP.of_ax`, glued by `CovMP.splitX/Y` and extended to the root [0, 7/2]^2 by `CovMP.face_wallX/Y`
(an admissible centre at theta = 0 has c >= 1/2).

    gen_face.py OUT.lean
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gen_axis import read_cover, claim  # noqa: E402
from gen_exact import ltup  # noqa: E402

COVER = os.path.join(HERE, '..', '..', 'certificates', 'k2m3', 'L4_k02_box7.txt')
S, R, MQ = 128, 1 << 72, 35


def main(out):
    side, D, W, pts, segs, rects = read_cover(COVER)
    Q = D * S
    step = Q // 10                      # 1/10
    lo, hi = Q // 2, 7 * Q // 2         # 1/2 .. 7/2
    xs = list(range(lo, hi + 1, step))
    lines = ["import Sqpack.V7.Data", "import Sqpack.LemmaZ", "namespace SquarePacking.LemmaELeaf",
             "open ZMTreeM ZMTree", "set_option maxRecDepth 100000", ""]
    names = {}
    for i in range(len(xs) - 1):
        for j in range(len(xs) - 1):
            x0, x1, y0, y1 = xs[i], xs[i + 1], xs[j], xs[j + 1]
            Lc, cps, chs, cvs, crs, vals, ok, K = claim(D, S, W, x0, x1, y0, y1, pts, segs, rects)
            assert all(ok), (x0, x1, y0, y1)
            nm = f"face_{i:02d}_{j:02d}"
            names[(i, j)] = nm
            lst = lambda l: "[" + ", ".join(ltup(e) for e in l) + "]"
            lines.append(
                f"theorem {nm} : CovMP {D} {S} {MQ} {R} {W} [] tsegs trects {x0} {x1} {y0} {y1} 0 0 :=\n"
                f"  CovMP.of_ax (Lc := {Lc}) (cps := {lst(cps)}) (chs := {lst(chs)}) (cvs := {lst(cvs)})\n"
                f"    (crs := {lst(crs)}) (by decide) (by decide) (by decide +kernel)\n")

    def glue(i0, i1, j0, j1):
        if i1 - i0 == 1 and j1 - j0 == 1:
            return names[(i0, j0)]
        if i1 - i0 >= j1 - j0:
            im = (i0 + i1) // 2
            return f"(CovMP.splitX {xs[im]} {glue(i0, im, j0, j1)} {glue(im, i1, j0, j1)})"
        jm = (j0 + j1) // 2
        return f"(CovMP.splitY {xs[jm]} {glue(i0, i1, j0, jm)} {glue(i0, i1, jm, j1)})"

    n = len(xs) - 1
    lines.append(f"theorem face_cells : CovMP {D} {S} {MQ} {R} {W} [] tsegs trects {lo} {hi} {lo} {hi} 0 0 :=\n"
                 f"  {glue(0, n, 0, n)}\n")
    lines.append(f"/-- **The face `θ = 0`** on the D4 root `[0, 7/2]²`. -/\n"
                 f"theorem face_root : CovMP {D} {S} {MQ} {R} {W} [] tsegs trects 0 {hi} 0 {hi} 0 0 :=\n"
                 f"  CovMP.face_wallX (m := {lo}) (by decide) (by decide) (by decide)\n"
                 f"    (CovMP.face_wallY (m := {lo}) (by decide) (by decide) (by decide) face_cells)\n")
    lines.append("end SquarePacking.LemmaELeaf")
    open(out, 'w').write("\n".join(lines) + "\n")
    print(n * n, "cells")


if __name__ == '__main__':
    main(sys.argv[1])
