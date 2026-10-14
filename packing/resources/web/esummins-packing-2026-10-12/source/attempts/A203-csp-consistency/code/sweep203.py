"""A203 -- the piece rules of A202's Stage0 as a mixin (moved verbatim from the copy of fast30.py at d13f7420 to keep
the files <= 250 lines): kill_base (P, W, C, M, L), kill_slot (R, X), sweep, h_may_meet, clip_H."""
import time

import fastprop as FP                                          # READ-ONLY (A198)
import rules202 as R

MB = FP.MB


def split(pc):
    import fast30
    return fast30.split(pc)


class Rules:
    # ------------------------------------------------------------------ the rules on one piece
    def kill_base(self, pc, cnt, tm):
        rr, rf, bn, bd = pc[2], pc[1], pc[3], pc[4]
        t = time.perf_counter()
        if R.pin_dead(rr, self.cores):
            tm["P"] += time.perf_counter() - t; cnt["P"] += 1; return "P"
        tm["P"] += time.perf_counter() - t; t = time.perf_counter()
        if R.wall_dead(rr, bn, self.s):
            tm["W"] += time.perf_counter() - t; cnt["W"] += 1; return "W"
        tm["W"] += time.perf_counter() - t; t = time.perf_counter()
        d2 = R.rect_maxdist2(rr, self.hhull) if self.hhull else 9.0
        if (d2 < 1.0 and all(R.cn_dead_pair(rr, hr) for hr in self.hrects)) or any(R.cn_dead_pair(rr, o) for o in self.other_rects):
            tm["C"] += time.perf_counter() - t; cnt["C"] += 1; return "C"
        tm["C"] += time.perf_counter() - t; t = time.perf_counter()
        if d2 < 1.46 and all(R.mk_dead(rr, bd, hr, hd) for hr, hd in zip(self.hrects, self.hbd)):
            tm["M"] += time.perf_counter() - t; cnt["M"] += 1; return "M"
        tm["M"] += time.perf_counter() - t; t = time.perf_counter()
        if pc[5] is None:
            pc[5] = R.piece_chords(rf, bn, self.lines)
        if R.chord_dead(pc[5], self.base_ch, self.s_fr) is not None:
            tm["L"] += time.perf_counter() - t; cnt["L"] += 1; return "L"
        tm["L"] += time.perf_counter() - t
        return None

    def kill_slot(self, pc, p, cnt, tm, exact=True):
        t = time.perf_counter()
        if R.reach_dead(pc[2], pc[3], self.wbox[p]):
            tm["R"] += time.perf_counter() - t; cnt["R"] += 1; return "R"
        tm["R"] += time.perf_counter() - t; t = time.perf_counter()
        if not exact:
            return None
        bx = MB.piece_box(pc[3], pc[1])[0]
        if FP.CLN.box_misses_cell_exact(bx, self.wbfr[p])[0]:
            tm["X"] += time.perf_counter() - t; cnt["X"] += 1; return "X"
        tm["X"] += time.perf_counter() - t
        return None

    def sweep(self, pieces, p, cnt, tm, depth):
        """the survivors of `pieces` under every rule for slot p, refined `depth` levels (piece budget)."""
        cur = [pc for pc in pieces if self.kill_base(pc, cnt, tm) is None and (p is None or self.kill_slot(pc, p, cnt, tm) is None)]
        for d in range(depth):
            if len(cur) * 8 > self.max_pieces:
                break
            last = (d == depth - 1) or (len(cur) * 64 > self.max_pieces)
            nxt = []
            for pc in cur:
                for ch in split(pc):
                    if self.kill_base(ch, cnt, tm) is None and (p is None or self.kill_slot(ch, p, cnt, tm, exact=last) is None):
                        nxt.append(ch)
            cur = nxt
        return cur

    def h_may_meet(self, hp, p):
        """False only when NO pose of H's piece meets the open box of p: the l-inf ball test, then A161's exact
        separating-axis miss test on the piece's pose box (cached per piece and slot)."""
        key = (id(hp), p)
        v = self.hmeet.get(key)
        if v is None:
            v = R.may_meet(hp[2], hp[3], self.wbox[p])
            if v:
                bx = MB.piece_box(hp[3], hp[1])[0]
                v = not FP.CLN.box_misses_cell_exact(bx, self.wbfr[p])[0]
            self.hmeet[key] = v
        return v

    # ------------------------------------------------------------------ H's own closed-form clip (P, W, meet)
    def clip_H(self, forced=(), depth=0):
        t0 = time.perf_counter()
        n0 = len(self.hpieces)
        cur = self.hpieces
        for d in range(depth + 1):
            keep = []
            for hp in cur:
                if R.pin_dead(hp[2], self.cores) or R.wall_dead(hp[2], hp[3], self.s):
                    continue
                if any(not self.h_may_meet(hp, p) for p in forced):
                    continue
                keep.append(hp)
            cur = keep if d == depth else [ch for hp in keep for ch in split(hp)]
        self.hpieces = cur
        self.tally("H-clip", max(0, n0 - len(cur)), time.perf_counter() - t0)
        self.refresh_H()
        return len(cur)

