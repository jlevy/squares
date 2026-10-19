"""A205 COPY of A204 (57f8d6ae, unchanged). A204 -- the POLYGON-CLIP CASCADE to a fixed point on the k>=1 survivors of the closed-form layers (A202 / A203).

The node = pins + H + the instantiated forced meeters (Theorem FC, forced_corners.md), every role carried as PIECES
(rational centre rect x tilt sub-bin, A171's representation) that are SEEDED and never re-merged into a box (A181's
rule): H starts from A203's alive units (its box x 8 x 8 sub-rects x 8 tilt bins minus the units the mutual clip killed,
each padded outward), a forced meeter from the per-tilt-bin hulls of its union's surviving pieces, and every round's
clip (the polygon + lonely clip fixed point of A171/A172/A173, then the exact reach clip against the forced slots) is
re-run ON THE PIECES so that K'(role) grows on the far side and clips the neighbours harder (memory: geometry-before-LP).
A200's QPage (READ-ONLY import) supplies the option table, the union caps, Theorem FC's forcing, the count with caps
and the bar-H forcing; this module replaces its normalise (box re-split) by the seeded fixed point and its round by a
piece-carrying round (poly204b.py), iterated until nothing moves.  NO LP, NO branched tree.
"""
import json
import math
import os
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ATT = os.path.join(ROOT, "attempts")
for _p in (os.path.join(ATT, "A200-k516-quick", "code"), os.path.join(ATT, "A198-fastprop", "code")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import quick200 as QP                                          # noqa: E402  READ-ONLY (A200; imports A198 fastprop, A178, A171)
FP, MB = QP.FP, QP.MB
CERTS203 = os.path.join(ATT, "A203-csp-consistency", "certs")
CERTS202 = os.path.join(ATT, "A202-fast30", "certs")
EPS_R = Fr(1, 10 ** 9)
EPS_T = Fr(1, 10 ** 12)


# ----------------------------------------------------------------------------- the starting node (stage 0's survivors)
def load_start(nid, pad):
    """H's clipped box, the forced slots and H's alive units from A203's certificate (A202's as the fallback)."""
    f = os.path.join(CERTS203, "csp203_%s_%s_s0.json" % (nid, pad))
    src = "A203 csp203"
    if not os.path.exists(f):
        f = os.path.join(CERTS202, "f30_%s_%s_s0.json" % (nid, pad))
        src = "A202 fast30"
    if not os.path.exists(f):
        return dict(source=None, H_box=None, forced_H=[], units=None)
    c = json.load(open(f, encoding="utf-8"))
    st = dict(source=src, file=os.path.relpath(f, ROOT).replace("\\", "/"), verdict=c.get("verdict"),
              H_box=list(c["roles"]["H"]), forced_H=sorted(c.get("forced_H") or []), role_slots=c.get("role_slots") or {},
              units=None, n_units=None, n_units_alive=None)
    csp = c.get("csp") or []
    if csp and csp[-1].get("unit_rects") and csp[-1].get("unit_alive"):
        last = csp[-1]
        keys = [tuple(int(v) for v in k.strip("[]").split(",")) for k in last["unit_rects"]]
        st["units"] = dict(nx=max(k[0] for k in keys) + 1, ny=max(k[1] for k in keys) + 1, nb=max(k[2] for k in keys) + 1,
                           alive=[tuple(u) for u in last["unit_alive"]])
        st["n_units"], st["n_units_alive"] = len(keys), len(last["unit_alive"])
    return st


def unit_pieces(box, units):
    """A203's units of H's box reconstructed EXACTLY (sub-rects uniform in x / y, tilt bins uniform in t = tan(th/2)),
    each alive unit padded OUTWARD (a superset of the exact unit: sound)."""
    x0, x1, y0, y1 = (Fr(float(v)) for v in box[:4])
    t0, t1 = MB.t_lo(box[4]), MB.t_hi(box[5])
    nx, ny, nb = units["nx"], units["ny"], units["nb"]
    bins = MB.sub_bins(t0, t1, nb)
    out = []
    for (i, j, b) in sorted(set(units["alive"])):
        r = (x0 + (x1 - x0) * Fr(i, nx) - EPS_R, x0 + (x1 - x0) * Fr(i + 1, nx) + EPS_R,
             y0 + (y1 - y0) * Fr(j, ny) - EPS_R, y0 + (y1 - y0) * Fr(j + 1, ny) + EPS_R)
        a, c = bins[b]
        out.append((MB.Bin(max(t0, a - EPS_T), min(t1, c + EPS_T)), r))
    return out


def coarsen(pcs, nbins=8, keep_if=32):
    """a union of pieces -> at most `nbins` pieces (the hull of the rects per tilt bin): a SUPERSET (sound)."""
    if len(pcs) <= keep_if:
        return list(pcs)
    tmin, tmax = min(b.t0 for b, _ in pcs), max(b.t1 for b, _ in pcs)
    out = []
    for (a, c) in MB.sub_bins(tmin, tmax, nbins):
        rs = [r for b, r in pcs if b.t0 < c and b.t1 > a]
        if not rs:
            continue
        out.append((MB.Bin(a, c), (min(r[0] for r in rs), max(r[1] for r in rs), min(r[2] for r in rs), max(r[3] for r in rs))))
    return out


def vol(pcs):
    return sum(MB.rect_area(r) * (b.t1 - b.t0) for b, r in pcs)


def box_vol(b):
    return Fr(float(b[1]) - float(b[0])) * Fr(float(b[3]) - float(b[2])) * (MB.t_hi(b[5]) - MB.t_lo(b[4]))


def hull_box(pcs):
    h = FP.pieces_hull(pcs)
    return (float(h[0]), float(h[1]), float(h[2]), float(h[3]), MB.deg_of_t(h[4]), MB.deg_of_t(h[5]))


def piece6(b, r):
    return [round(float(r[0]), 7), round(float(r[1]), 7), round(float(r[2]), 7), round(float(r[3]), 7),
            round(MB.deg_of_t(b.t0), 4), round(MB.deg_of_t(b.t1), 4)]


# ----------------------------------------------------------------------------- the seeded polygon + lonely clip fixed point
def fixpoint(nd, corners, s, refine=2, max_iter=10, max_pieces=96, near=True):
    """A171's Node.normalise (mode poly, kmode pieces, strict_container False, corners = the lonely clip) driven on the
    node's CURRENT pieces (never re-split from the boxes): container clip, lonely clip, `refine` levels of tautologous
    bisection interleaved with the clip against every other role's polygon K', then lonely + mutual clip to a fixed point
    with K' rebuilt from the survivors after every pass.  Raises MB.EmptyBox = the pair leaf."""
    names = nd.names
    st = nd.stats
    rep = dict(lonely=[], passes=0, refine=refine)

    def lonely_pass(tag):
        moved = False
        for k, corner in corners.items():
            mb = nd.boxes[k]
            lr = MB.lonely_clip(mb, corner, c=MB.C_WIDEN, s=s, nsub=4, refine=0, max_pieces=4096, pass_=tag)
            if lr["removed"] > 0 or lr["dropped_pieces"]:
                moved = True
                rep["lonely"].append(dict(box=k, stage=tag, removed=lr["removed"], dropped=lr["dropped_pieces"], n_after=lr["n_after"]))
        return moved

    def clip_all(cur, bn, k, obst):
        for j in names:
            if j == k or cur is None:
                continue
            ob = obst[j]
            if ob is None or (near and not FP.obstacle_near(ob, cur)):
                continue
            cur = MB._clip_rect_obstacle(cur, ob, bn, st)
        return cur

    for mb in nd.boxes.values():
        keep = []
        for (bn, r) in mb.pieces:
            nr, _sl = MB.container_clip(r, bn, s, strict=False)
            if nr is not None:
                keep.append((bn, nr))
        if not keep:
            raise MB.EmptyBox(mb.name, dict(reason="container"))
        mb.pieces = keep
        mb.kmode = "pieces"
    if corners:
        lonely_pass("container")
    for lvl in range(max(0, refine)):
        if corners:
            lonely_pass("refine%d" % (lvl + 1))
        for mb in nd.boxes.values():
            mb.rebuild()
        obst = {k: nd.boxes[k].obstacle("poly") for k in names}
        for k in names:
            mb = nd.boxes[k]
            if len(mb.pieces) * 2 > max_pieces:
                continue
            new = []
            for (bn, r) in mb.pieces:
                for (bn2, r2) in MB.split_piece(bn, r):
                    cur, _sl = MB.container_clip(r2, bn2, s, strict=False)
                    cur = clip_all(cur, bn2, k, obst)
                    if cur is not None:
                        new.append((bn2, cur))
            if not new:
                raise MB.EmptyBox(mb.name, dict(reason="refine", level=lvl + 1))
            mb.pieces = new
    vprev = sum(vol(mb.pieces) for mb in nd.boxes.values())
    for it in range(max_iter):
        moved = lonely_pass("pass%d" % (it + 1)) if corners else False
        for mb in nd.boxes.values():
            mb.rebuild()
        obst = {k: nd.boxes[k].obstacle("poly") for k in names}
        for k in names:
            mb = nd.boxes[k]
            keep = []
            for (bn, r) in mb.pieces:
                cur = clip_all(r, bn, k, obst)
                if cur != r:
                    moved = True
                if cur is not None:
                    keep.append((bn, cur))
            if not keep:
                raise MB.EmptyBox(mb.name, dict(reason="mutual", pass_=it + 1))
            mb.pieces = keep
        rep["passes"] = it + 1
        vnow = sum(vol(mb.pieces) for mb in nd.boxes.values())
        if not moved or vnow > vprev * (1 - Fr(1, 1000)):          # A205: a pass that moved < 0.1 % of the volume ends the loop (sound: any prefix of the clip chain is)
            rep["stopped"] = "moved < 0.1%%" if moved else "fixed"
            break
        vprev = vnow
    for mb in nd.boxes.values():
        mb.rebuild()
        mb.kept = mb.kept_fraction()
    nd.normalised = True
    return rep


# ----------------------------------------------------------------------------- the page
class PolyPage(QP.QPage):
    def __init__(self, rec, cls, nid, T, pad, start, depth=5, joint_depth=2, refine_union=2, seed_units=True):
        QP.QPage.__init__(self, rec, cls, nid, T, depth=depth, joint_depth=joint_depth, refine_union=refine_union, pad=pad)
        self.start = start
        self.record_H = tuple(self.roles[self.H])
        self.vol_record = {k: box_vol(v) for k, v in self.roles.items()}
        hb = start.get("H_box")
        if hb:
            old = self.roles[self.H]
            self.roles[self.H] = (max(hb[0], old[0]), min(hb[1], old[1]), max(hb[2], old[2]), min(hb[3], old[3]), max(hb[4], old[4]), min(hb[5], old[5]))
        self.forced_H = set(start.get("forced_H") or [])
        self.pieces = {}
        if seed_units and start.get("units"):
            self.pieces[self.H] = unit_pieces(self.roles[self.H], start["units"])
        self.prev_reach = {}
        self.pcache = {}
        self.snapshots = []
        self.on_round = None
        self.round_times = []
        self.fix_rep = None

    def corners_now(self):
        c = {k: v for k, v in self.role_corner.items() if k in self.roles}
        for p in self.forced_H:
            if self.item[p]["is_corner"]:
                c[self.H] = self.item[p]["corner"]
        return c

    def normalise(self, label):
        """the seeded polygon + lonely clip fixed point on the CURRENT pieces of every role."""
        t0 = time.time()
        nd = MB.Node(dict(self.roles), name=self.name + "/" + label)
        for k, mb in nd.boxes.items():
            if k in self.pieces and self.pieces[k]:
                mb.pieces = list(self.pieces[k])
            else:
                r0 = MB.PIN.outer_rect(mb.box0)
                mb.pieces = [(MB.Bin(a, b), r0) for (a, b) in MB.sub_bins(mb.t0, mb.t1, self.nsub_mb)]
            mb.kmode = "pieces"
            if len(self.pcache) > 30000:
                self.pcache.clear()
            mb._pcache = self.pcache                                  # per-piece K' reused across rounds (PC.build is pure)
        corners = self.corners_now()
        v0 = {k: vol(mb.pieces) for k, mb in nd.boxes.items()}
        for k in v0:
            self.vol_record.setdefault(k, v0[k])                       # an instantiated role: kept relative to its seed
        try:
            rep = fixpoint(nd, corners, self.s, refine=self.refine_mb)
        except MB.EmptyBox as e:
            self.nd = nd
            self.T.step("normalise", time.time() - t0, label=label, dead=e.name, detail=e.detail)
            self.T.test("EMPTYBOX", role=e.name, label=label, detail=e.detail, roles={k: FP.rect_f(v) for k, v in self.roles.items()})
            self.dead = "EmptyBox(%s) at %s: every pose of %s is outside the container, lonely, or meets another role's K' at every tilt of its sub-bin (A171 pair leaf; %s)" % (e.name, label, e.name, e.detail)
            self.fix_rep = dict(dead=e.name, detail=e.detail, seconds=round(time.time() - t0, 1))
            return None
        self.nd = nd
        nd.normalised = True
        self.obst = {k: nd.boxes[k].obstacle("poly") for k in nd.names}
        self.prev_reach = {k: v for k, v in self.reach_cache.items() if isinstance(k[0], int)}
        self.reach_cache = {}
        v1 = {k: vol(mb.pieces) for k, mb in nd.boxes.items()}
        self.norm_shrunk = label != "round1" and any(v1[k] < v0[k] * (1 - Fr(1, 10 ** 6)) for k in v1)
        for k, mb in nd.boxes.items():
            self.pieces[k] = list(mb.pieces)
            self.roles[k] = hull_box(mb.pieces) if k != self.H or mb.pieces else self.roles[k]
        rep["seconds"] = round(time.time() - t0, 1)
        rep["kept"] = {k: round(float(v1[k] / self.vol_record[k]), 6) if self.vol_record[k] else 1.0 for k in v1}
        rep["n_pieces"] = {k: len(mb.pieces) for k, mb in nd.boxes.items()}
        rep["k_area"] = {k: (mb.pc.area() if mb.pc is not None else 0.0) for k, mb in nd.boxes.items()}
        rep["corners"] = corners
        self.fix_rep = rep
        self.T.step("normalise", time.time() - t0, label=label, kept=rep["kept"], passes=rep["passes"], n_pieces=rep["n_pieces"], corners=corners)
        return nd

    def reach(self, ci, S):
        """A198's cell reach, SEEDED from the previous round's survivors (K' only grows: a subset, sound) and re-clipped
        in place; from scratch when there is no previous record."""
        key = (ci, S)
        if key in self.reach_cache:
            return self.reach_cache[key]
        prev = self.prev_reach.get(key)
        if prev is None or not prev[1]:
            return QP.QPage.reach(self, ci, S)
        t0 = time.time()
        corner = None
        for p in S:
            if self.item[p]["is_corner"]:
                corner = self.item[p]["corner"]
        res = FP.bisect_region(None, self.obstacles_for_free(), [self.item[p]["wb"] for p in S], self.s, self.nd.stats, depth=0,
                               corner=corner, seed_pieces=prev[1], max_pieces=512)
        self.T.test("REACH", cell=ci, slots=sorted(S), seeded=True, frac=round(res[0], 6), n_pieces=len(res[1]), n_exact=res[2],
                    lonely=corner, seconds=round(time.time() - t0, 3))
        self.reach_cache[key] = res
        return res

    def role_reach(self, role, S):
        """pieces of H / an instantiated role not provably missing every slot of S, re-clipped against the other roles' K';
        bisected two levels when the role has few pieces, clipped in place (depth 0) when it is carried at unit resolution."""
        key = (role, S)
        if key in self.reach_cache:
            return self.reach_cache[key]
        pcs = self.nd.boxes[role].pieces
        depth = 2 if len(pcs) <= 64 else 0
        t0 = time.time()
        res = FP.bisect_region(None, self.obstacles_except(role), [self.item[p]["wb"] for p in S], self.s, self.nd.stats,
                               depth=depth, seed_pieces=pcs, max_pieces=4096)
        self.T.test("ROLE-REACH", role=role, slots=sorted(S), depth=depth, frac=round(res[0], 6), n_pieces=len(res[1]), n_exact=res[2],
                    seconds=round(time.time() - t0, 3))
        self.reach_cache[key] = res
        return res

    def snapshot(self, rnd, label):
        """what the panel IS: the node after this round's fixed point, pieces + K' per role, drawn from here."""
        nd = self.nd
        roles = {}
        for k, mb in nd.boxes.items():
            pc = getattr(mb, "pc", None)
            roles[k] = dict(box=[round(float(v), 6) for v in self.roles[k]], n_pieces=len(mb.pieces),
                            pieces=[piece6(b, r) for b, r in mb.pieces][:600],
                            kprime=[[float(a), float(b)] for a, b in (pc.verts if pc is not None else ())],
                            kept=(self.fix_rep or {}).get("kept", {}).get(k), corner=self.corners_now().get(k))
        snap = dict(pad=self.pad, round=rnd, label=label, roles=roles, forced_H=sorted(self.forced_H),
                    role_slots={k: list(v) for k, v in self.role_slots.items()}, t=round(self.T.now(), 1),
                    fix=(self.fix_rep or {}), dead=self.dead)
        self.snapshots.append(snap)
        return snap
