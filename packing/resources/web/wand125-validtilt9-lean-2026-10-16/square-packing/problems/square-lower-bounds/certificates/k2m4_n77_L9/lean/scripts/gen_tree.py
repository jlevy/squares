#!/usr/bin/env python3
"""Lean proof terms for the pose trees of a qx2_zm run (`ExTree.lean`).

Every node is proved at the global scale (centres over Q = D*S, angles over R): splits by
`CovT.splitX/Y/U`, `clip_bin` by `CovT.clip`, and the leaves by `CovT.of_empty`, `CovT.of_sym`,
`CovT.of_top_zero`, `CovT.of_leb`, or a leaf theorem `<name> : exOk ... = true` (EXACT, checked at the
leaf's own scale and moved to the global one by `CovT.scaleS'` / `CovT.scaleR'`).  The Lean kernel
re-checks everything; this script only writes terms.
"""
from fractions import Fraction as F

from lemmae_mirror import widN, widD


class Glue:
    def __init__(self, D, S, R, W, Mq, segs="tsegs", rects="trects", pts="[]"):
        self.D, self.S, self.R, self.W, self.Mq = D, S, R, W, Mq
        self.Q = D * S
        self.segs, self.rects, self.pts = segs, rects, pts
        self.leaf_names = {}          # box -> (name, S_leaf, R_leaf) for EXACT-type leaves

    def iq(self, x):
        v = x * self.Q
        assert v.denominator == 1, f"{x} not on the 1/{self.Q} grid"
        return int(v)

    def ir(self, u):
        v = u * self.R
        assert v.denominator == 1, f"{u} not on the 1/{self.R} grid"
        return int(v)

    def stmt(self, box):
        x0, x1, y0, y1, u0, u1 = box
        return (f"CovT {self.D} {self.S} {self.Mq} {self.R} {self.W} {self.pts} {self.segs} {self.rects} "
                f"{self.iq(x0)} {self.iq(x1)} {self.iq(y0)} {self.iq(y1)} {self.ir(u0)} {self.ir(u1)}")

    def lebOk(self, box, e):
        """mirror of `CovMP.lebOk` at the global scale"""
        D, S, Mq, R, W = self.D, self.S, self.Mq, self.R, self.W
        x0, x1, y0, y1 = (self.iq(z) for z in box[:4])
        u0, u1 = self.ir(box[4]), self.ir(box[5])
        wD, wN = widD(R, u0), widN(R, u0, u1)
        return (u1 <= R and u0 <= u1 and W <= e[4]
                and (e[0] == 0 or 2 * e[0] * S * wD + D * S * wN <= 2 * x0 * wD)
                and (Mq <= e[2] or 2 * x1 * wD + D * S * wN <= 2 * e[2] * S * wD)
                and (e[1] == 0 or 2 * e[1] * S * wD + D * S * wN <= 2 * y0 * wD)
                and (Mq <= e[3] or 2 * y1 * wD + D * S * wN <= 2 * e[3] * S * wD))

    def leaf(self, box, kind, rects_list):
        dk = "(by decide)"
        if box[4] == box[5]:
            return "CovT.of_degen"
        if box in self.leaf_names:
            kind = 'EXACT'
        if kind == 'EMPTY':
            return f"(CovT.of_empty {dk} {dk} {dk} {dk} {dk})"
        if kind == 'SYM':
            return f"(CovT.of_sym {dk} {dk})"
        if kind == 'AXIS':
            assert box[5] == 0
            return f"(CovT.of_top_zero {dk})"
        if kind == 'LEB':
            assert len(rects_list) == 1
            return f"(CovT.of_leb (e := {tuple(rects_list[0])}) {dk} {dk} {dk} {dk} (by decide +kernel))".replace(
                "(e := (", "(e := (")
        name, Sl, Rl = self.leaf_names[box][:3]
        kS, kR = self.S // Sl, self.R // Rl
        assert kS * Sl == self.S and kR * Rl == self.R
        if len(self.leaf_names[box]) > 3 and self.leaf_names[box][3] == 'cap':
            t = f"(CovT.of_cap {dk} {dk} {dk} {name})"
        elif len(self.leaf_names[box]) > 3 and self.leaf_names[box][3] == 'x':
            t = f"(CovT.of_exactX {dk} {dk} {dk} {name})"
        else:
            t = f"(CovT.of_exact {dk} {dk} {dk} {name})"
        if kR != 1:
            t = f"(CovT.scaleR' (k := {kR}) {dk} {t})"
        if kS != 1:
            t = f"(CovT.scaleS' (k := {kS}) {dk} {t})"
        return t

    def term(self, t, box, rects_list):
        x0, x1, y0, y1, u0, u1 = box
        if t[0] == 'L':
            assert t[1] == box, (t[1], box)
            return self.leaf(box, t[2], rects_list)
        if t[0] == 'C':
            us = t[1]
            cb = (x0, x1, y0, y1, u0, us)
            return (f"(CovT.clip (us := {self.ir(us)}) (by decide) (by decide) (by decide) (by decide)\n  "
                    f"{self.term(t[2], cb, rects_list)})")
        ax, mid, l, r = t
        i = {'X': 0, 'Y': 2, 'U': 4}[ax]
        bl = list(box); bl[i + 1] = mid
        bh = list(box); bh[i] = mid
        m = self.ir(mid) if ax == 'U' else self.iq(mid)
        return (f"(CovT.split{ax} {m}\n  {self.term(l, tuple(bl), rects_list)}\n  "
                f"{self.term(r, tuple(bh), rects_list)})")

    def root_thm(self, name, root, tree, rects_list):
        return f"theorem {name} : {self.stmt(root)} :=\n  {self.term(tree, root, rects_list)}\n"
