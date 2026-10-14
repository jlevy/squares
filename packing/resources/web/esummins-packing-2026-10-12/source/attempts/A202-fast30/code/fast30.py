"""A202 -- fast30 STAGE 0: the closed-form geometric kill layer over a gallery page (<= 30 s), n-general.
Pieces: every half-grid cell (fastprop.make_grid, side < 1/sqrt2) split nsub x nsub, times nbins exact tilt sub-bins
of [0, 90] deg; the survivors of a slot are REFINED (2 x 2 in the centre, 2 in tilt) `depth` levels under the same
rules, so the alive region of a slot is a union of small pieces (the PI's discs / corners / columns read off it).
Rules (rules202; lemmas in notes/fast30.md): P pins, W walls, C Lemma CN against H's alive pieces, M the relative-
tilt separating-axis bound, L the open-chord row, R reach (disc / half-extent) and X A161's exact miss per slot;
then (fast30b) the per-slot union caps (CN / A1-U / CHORD-U), Theorem FC's demand 2, the assignment count with the
A1 / CN / MK pair table (count202), the bar-H forcing, H clipped to the poses that may meet its forced slots,
iterated to a fixed point.  DEAD verdicts are [C: closed-form trace]: no verifier clause exists yet."""
import os
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (os.path.join(ROOT, "attempts", "A198-fastprop", "code"), os.path.join(ROOT, "attempts", "A200-k516-quick", "code")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import fastprop as FP                                          # noqa: E402  READ-ONLY (A198)
import quick200 as Q                                           # noqa: E402  READ-ONLY (A200): set_pad, PADS, union_stats
import rules202 as R                                           # noqa: E402

MB, G = FP.MB, FP.G
S_RAT, HALF = FP.S_RAT, FP.HALF
INF = 99
_BINS = {}


def mkbin(t0, t1):
    b = _BINS.get((t0, t1))
    if b is None:
        b = _BINS[(t0, t1)] = MB.Bin(t0, t1)
    return b


class Piece(list):
    """[ci, rect_fr, rect_f, bin, bdeg, chords|None]"""
    __slots__ = ()


def mkpiece(ci, rf, bn):
    return Piece([ci, rf, R.fr(rf), bn, R.bin_deg(bn), None])


def split(pc):
    ci, rf, _, bn, _, ch = pc
    xm, ym = (rf[0] + rf[1]) / 2, (rf[2] + rf[3]) / 2
    tm = (bn.t0 + bn.t1) / 2
    out = []
    for r in ((rf[0], xm, rf[2], ym), (xm, rf[1], rf[2], ym), (rf[0], xm, ym, rf[3]), (xm, rf[1], ym, rf[3])):
        for b in (mkbin(bn.t0, tm), mkbin(tm, bn.t1)):
            q = mkpiece(ci, r, b)
            q[5] = ch                                                      # inherited: a lower bound for every child pose
            out.append(q)
    return out


class Stage0:
    def __init__(self, nid, pad="g1", nsub=4, nbins=6, depth=3, max_pieces=12000, nsub_h=4, nbins_h=4, depth_h=2, n=11, log=print):
        self.T = FP.Trace()
        self.log = log
        self.nid, self.pad, self.depth, self.max_pieces = nid, pad, depth, max_pieces
        self.rec, self.cls, self.row = FP.load_page(nid)
        self.s, self.s_fr = float(S_RAT), S_RAT
        self.base = G.base_roles(self.rec)
        self.pins = {k: v for k, v in self.base.items() if k.startswith("P")}
        self.hnames = [k for k in self.base if k.startswith("H")]
        self.H = self.hnames[0]
        self.n_free = n - len(self.pins) - len(self.hnames)
        self.items = G.forced_items(self.cls, self.rec)
        Q.set_pad(self.items, Q.PADS[pad], S_RAT)
        self.slots = [it["cell"] for it in self.items]
        self.wbox = {it["cell"]: R.fr(it["wb"]) for it in self.items}          # outward-rounded widened boxes
        self.wbfr = {it["cell"]: it["wb"] for it in self.items}
        self.cells, self.side = FP.make_grid(S_RAT)
        self.lines = FP.guard_lines(S_RAT)
        self.pin_chords = {L: Fr(0) for L in self.lines}
        for k, b in self.pins.items():
            mc = FP.minchord_box(b, self.lines)
            for L in self.lines:
                self.pin_chords[L] += mc[L]
        self.cores = []
        for p in self.rec["pins"]:
            a = float(Fr(str(p["a"]))) - 1e-12
            self.cores.append((p["kx"] - a, p["kx"] + a, p["ky"] - a, p["ky"] + a))
        bins = [mkbin(a, b) for a, b in MB.sub_bins(Fr(0), Fr(1), nbins)]
        self.sub = {}                                                          # (ci, si) -> (rect_fr, rect_f)
        self.coarse = []
        for ci, c in enumerate(self.cells):
            x0, x1, y0, y1 = c["rect"]
            w = (x1 - x0) / nsub
            for i in range(nsub):
                for j in range(nsub):
                    rf = (x0 + i * w, x0 + (i + 1) * w, y0 + j * w, y0 + (j + 1) * w)
                    self.sub[(ci, i * nsub + j)] = (rf, R.fr(rf))
                    self.coarse += [mkpiece(ci, rf, b) for b in bins]
        self.nsub, self.nbins, self.bins = nsub, nbins, bins
        self.letters = {}
        hb = self.base[self.H]
        t0, t1 = MB.t_lo(hb[4]), MB.t_hi(hb[5])
        self.hpieces = []
        w, h = (hb[1] - hb[0]) / nsub_h, (hb[3] - hb[2]) / nsub_h
        for i in range(nsub_h):
            for j in range(nsub_h):
                rf = (Fr(hb[0] + i * w), Fr(hb[0] + (i + 1) * w), Fr(hb[2] + j * h), Fr(hb[2] + (j + 1) * h))
                self.hpieces += [mkpiece(-1, rf, mkbin(a, b)) for a, b in MB.sub_bins(t0, t1, nbins_h)]
        self.depth_h = depth_h
        self.other_h = {k: self.base[k] for k in self.hnames[1:]}
        self.forced_H = set()
        self.hmeet = {}
        self.alive = {}                                                        # slot -> [Piece]
        self.rounds = []
        self.verdict_leaf = None
        self.kills = {}

    # ------------------------------------------------------------------ bookkeeping
    def tally(self, rule, n, dt):
        d = self.kills.setdefault(rule, dict(kills=0, ms=0.0))
        d["kills"] += n
        d["ms"] += 1000 * dt

    def h_hull(self):
        al = self.hpieces
        if not al:
            return None
        return (min(p[2][0] for p in al), max(p[2][1] for p in al), min(p[2][2] for p in al), max(p[2][3] for p in al),
                min(p[4][0] for p in al), max(p[4][1] for p in al))

    def h_chords(self):
        for p in self.hpieces:
            if p[5] is None:
                p[5] = R.piece_chords(p[1], p[3], self.lines)
        out = {}
        for L in self.lines:
            m = None
            for p in self.hpieces:
                c = p[5].get(L, Fr(0))
                m = c if m is None else min(m, c)
                if m <= 0:
                    break
            out[L] = Fr(0) if m is None else m
        return out

    def refresh_H(self):
        """H's alive rects / bins and the fixed chords, after every change of H."""
        # H's pieces grouped (tilt bin x 2x2 cell of H's box) into bboxes: C / M against a group's bbox is a sound
        # weakening of the test against each piece in it (max distance to the bbox >= to any piece inside)
        groups = {}
        hh = self.h_hull()
        for p in self.hpieces:
            gx = min(1, int(2 * (p[2][0] - hh[0]) / max(1e-12, hh[1] - hh[0])))
            gy = min(1, int(2 * (p[2][2] - hh[2]) / max(1e-12, hh[3] - hh[2])))
            groups.setdefault((p[3].t0, gx, gy), []).append(p)
        self.hrects, self.hbd = [], []
        for ps in groups.values():
            self.hrects.append((min(p[2][0] for p in ps), max(p[2][1] for p in ps), min(p[2][2] for p in ps), max(p[2][3] for p in ps)))
            self.hbd.append((min(p[4][0] for p in ps), max(p[4][1] for p in ps)))
        self.hhull = hh[:4] if hh else None
        self.other_rects = [R.fr(v[:4]) for v in self.other_h.values()]
        ch = dict(self.pin_chords)
        hc = self.h_chords()
        for L in self.lines:
            ch[L] += hc[L]
        for v in self.other_h.values():
            mc = FP.minchord_box(v, self.lines)
            for L in self.lines:
                ch[L] += mc[L]
        self.base_ch = ch

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

    # ------------------------------------------------------------------ the loop
    def run(self, max_rounds=6):
        import fast30b as B
        if self.clip_H(depth=self.depth_h) == 0:
            self.verdict_leaf = "H's box has no pose clear of the pins and walls (closed form)"
            return self.result()
        cnt = {k: 0 for k in "PWCMLRX"}
        tm = {k: 0.0 for k in "PWCMLRX"}
        t0 = time.perf_counter()
        base = []
        for pc in self.coarse:
            w = self.kill_base(pc, cnt, tm)
            if w:
                self.letters[(pc[0], pc[1], pc[3].t0)] = w
            else:
                base.append(pc)
        for p in self.slots:
            self.alive[p] = self.sweep(base, p, cnt, tm, self.depth)
        for k in cnt:
            self.tally(k, cnt[k], tm[k])
        self.T.step("pieces", time.perf_counter() - t0, coarse=len(self.coarse), base_alive=len(base), alive={p: len(v) for p, v in self.alive.items()})
        for rnd in range(1, max_rounds + 1):
            info = B.propagate(self, rnd)
            self.rounds.append(info)
            if self.verdict_leaf or not info.get("changed"):
                break
            cnt = {k: 0 for k in "PWCMLRX"}
            tm = {k: 0.0 for k in "PWCMLRX"}
            for p in self.slots:                                               # H shrank: the H-dependent rules again
                self.alive[p] = [pc for pc in self.alive[p] if self.kill_base(pc, cnt, tm) is None]
            for k in cnt:
                self.tally(k, cnt[k], tm[k])
        return self.result()

    def result(self):
        import fast30b as B
        return B.certificate(self)


if __name__ == "__main__":
    import json
    nid = sys.argv[1]
    pad = sys.argv[2] if len(sys.argv) > 2 else "g1"
    st = Stage0(nid, pad)
    out = st.run()
    print(json.dumps({k: out[k] for k in ("nid", "pad", "verdict", "leaf", "seconds", "kills", "caps", "forced_H")}, default=str, indent=1))
