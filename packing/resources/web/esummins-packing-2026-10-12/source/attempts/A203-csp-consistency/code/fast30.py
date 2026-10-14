"""A203 (copy of A202's fast30 at d13f7420, modified: H units, the CSP letters) -- fast30 STAGE 0: the closed-form geometric kill layer over a gallery page (<= 30 s), n-general.
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


import sweep203 as SW                                          # noqa: E402


class Stage0(SW.Rules):
    def __init__(self, nid, pad="g1", nsub=4, nbins=6, depth=3, max_pieces=12000, nsub_h=4, nbins_h=4, depth_h=2, n=11, log=print, ud=1, sat_step=4.0, settle=True):
        self.ud, self.sat_step, self.settle = ud, sat_step, settle
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
        self.nsub_h, self.nbins_h, self.h_t0, self.h_t1 = nsub_h, nbins_h, t0, t1
        self.letters_csp = {}                                                  # (ci, sub-rect) -> 'H' (CSP kill)
        self.compat = None
        self.addr_cache = {}
        self.settled = {}                                                      # (id piece, id H piece, S) -> settled dead?
        self.csp = []                                                          # per-round CSP records
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
        import cert203 as CT
        return CT.certificate(self)


if __name__ == "__main__":
    import json
    nid = sys.argv[1]
    pad = sys.argv[2] if len(sys.argv) > 2 else "g1"
    st = Stage0(nid, pad)
    out = st.run()
    print(json.dumps({k: out[k] for k in ("nid", "pad", "verdict", "leaf", "seconds", "kills", "caps", "forced_H")}, default=str, indent=1))
