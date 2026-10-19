"""A205 COPY of A204 (57f8d6ae; count_search routed through self.count_search = the pair-table count). A204 -- the piece-carrying ROUND and the fixed-point loop (poly204.PolyPage's engine).

One round = A200's option table on the node (every grid cell x forced slot bisected against every role's K' with the
exact dead / miss / lonely tests, seeded from the previous round), the union caps (CN / A1-U / CHORD-U), Theorem FC's
forcing (avail < 2 dead; avail = 2 -> H clipped to the poses meeting the slot, a role clipped likewise, the unique
anonymous meeter INSTANTIATED as a role seeded with its union's pieces), the count with caps and the bar-H forcing
(A180/A182's unit propagation without branching); then the APPLY on the PIECES: H and every instantiated role are
re-clipped by the exact reach against ALL their forced slots every round (the new K's clip harder), and the round is
"changed" iff a role was added, a forced set grew, or some role's pose volume fell.  The loop re-runs the seeded polygon
+ lonely clip fixed point at the top of every round and stops at the first round where neither moved (or on a kill, or
at the wall).  NO LP, NO branched tree.
"""
import time
from fractions import Fraction as Fr

import poly204 as P
import quick200 as QP

FP, MB, INF = P.FP, P.MB, QP.INF


def propagate_round(pg, rnd):
    self = pg
    free_opts, fixed_opts, single = self.build_options()
    info = dict(round=rnd, single={p: {ci: round(f, 4) for ci, f in v.items()} for p, v in single.items()},
                n_free_opts=len(free_opts), fixed={r: [(ci, sorted(S)) for ci, S, _, _ in v] for r, v in fixed_opts.items()},
                free_opts=[(ci, sorted(S), FP.rect_f(h)) for ci, S, _, h in free_opts])
    roles_reach = {r: set().union(*[S for _, S, _, _ in v]) if v else set() for r, v in fixed_opts.items()}
    H_reach = roles_reach[self.H]
    info["H_reach"] = sorted(H_reach)
    t0 = time.time()
    base_ch = self.fixed_chords()
    caps, urec = {}, {}
    self.union_last = {}
    for p in self.slots:
        pcs = self.slot_union(p, single)
        self.union_last[p] = pcs
        if len(single.get(p, {})) <= 1:
            cap = min(1, len(single.get(p, {})))
            rec = dict(slot=p, cap=cap, why="A1: %d alive cell(s)" % len(single.get(p, {})), n_pieces=len(pcs))
            if pcs:
                st = QP.union_stats(pcs)
                rec.update(bbox=FP.rect_f(st["bbox"]), diam=round(float(st["diam2"]) ** 0.5, 5), linf=round(float(st["linf"]), 5))
        else:
            cap, rec = self.union_cap(p, pcs, base_ch)
        caps[p], urec[p] = cap, rec
        self.T.test("UNION", **rec)
    self.caps_last = dict(caps)
    info["union"] = urec
    info["caps"] = {p: (None if c >= INF else c) for p, c in caps.items()}
    self.T.step("union", time.time() - t0, caps=info["caps"])
    forced_H, forced_role, instantiate = set(), {}, {}
    for p in self.slots:
        R_p = [r for r in roles_reach if r != self.H and p in roles_reach[r]]
        H_p = p in H_reach
        avail = (1 if H_p else 0) + len(R_p) + caps[p]
        rec = dict(slot=p, H=H_p, roles=R_p, cap=(None if caps[p] >= INF else caps[p]))
        if avail < 2:
            self.dead = "FC at %s: at most %d distinct non-pin meeter(s) (H %s; roles %s; anonymous cap %d by %s)" % (
                p, avail, "reaches" if H_p else "provably misses", R_p, caps[p], urec[p]["why"])
            self.T.test("FC-AVAIL", verdict="DEAD", avail=avail, **rec)
            info["dead"], info["clip"] = self.dead, "FC"
            return info
        if avail == 2:
            if H_p:
                forced_H.add(p)
            for r in R_p:
                forced_role.setdefault(r, set()).add(p)
            if caps[p] == 1:
                instantiate[p] = True
            self.T.test("FC-AVAIL", verdict="all forced", avail=2, **rec)
    n_anon = self.n_free - len(self.role_cell)
    for chords in (False, True):
        t0 = time.time()
        r = self.count_search(self.slots, free_opts, fixed_opts, n_anon, self.lines, self.pin_chords, self.s, caps, use_chords=chords)
        info["count_chord" if chords else "count_nochord"] = dict(feasible=r.feasible, nodes=r.nodes, capped=r.capped)
        self.T.step("count", time.time() - t0, chords=chords, feasible=r.feasible, nodes=r.nodes, capped=r.capped)
        if not r.feasible:
            self.dead = "JOINT COUNT%s (caps %s): no cover of the %d forced slots by H + %d role(s) + %d anonymous squares" % (
                " + CHORD ROWS" if chords else "", info["caps"], len(self.slots), len(self.role_cell), n_anon)
            self.T.test("COUNT", chords=chords, verdict="DEAD", nodes=r.nodes, n_free_opts=len(free_opts), caps=info["caps"])
            info["dead"], info["clip"] = self.dead, "COUNT"
            return info
        self.witness = r.witness
    info["witness"] = [(who, ci, sorted(S)) for who, (ci, S, _, _) in (self.witness or [])]
    for p in self.slots:
        if p in forced_H or p not in H_reach or self.T.out_of_time():
            continue
        fo = dict(fixed_opts)
        fo[self.H] = [o for o in fixed_opts[self.H] if p not in o[1]]
        t0 = time.time()
        rr = self.count_search(self.slots, free_opts, fo, n_anon, self.lines, self.pin_chords, self.s, caps, use_chords=False)
        if rr.feasible:
            rr = self.count_search(self.slots, free_opts, fo, n_anon, self.lines, self.pin_chords, self.s, caps, use_chords=True)
        self.T.step("count-barH", time.time() - t0, slot=p, feasible=rr.feasible, nodes=rr.nodes, capped=rr.capped)
        if not rr.feasible:
            forced_H.add(p)
            self.T.test("COUNT", barH=p, verdict="H forced at %s" % p, nodes=rr.nodes)
    info["forced_H"] = sorted(forced_H)
    info["forced_role"] = {r: sorted(v) for r, v in forced_role.items()}
    info["instantiate"] = sorted(instantiate)
    return apply_round(self, info, forced_H, forced_role, instantiate, urec)


def apply_round(self, info, forced_H, forced_role, instantiate, urec):
    """the APPLY on the pieces: every forced role re-clipped by the exact reach against all its slots, the anonymous
    meeters instantiated from their union pieces; changed = a role added / a forced set grew / a pose volume fell."""
    changed = bool(forced_H - self.forced_H)
    self.forced_H |= forced_H
    vol0 = {k: P.vol(v) for k, v in self.pieces.items()}
    clips = {}
    todo = [(self.H, frozenset(self.forced_H))] if self.forced_H else []
    for r in sorted(self.role_cell):
        S = frozenset(forced_role.get(r, ())) | frozenset(self.role_slots.get(r, ()))
        if S != frozenset(self.role_slots.get(r, ())):
            changed = True
        self.role_slots[r] = tuple(sorted(S))
        if S:
            todo.append((r, S))
    for r, S in todo:
        fr, pcs, _ = self.role_reach(r, S)
        if not pcs:
            self.dead = "%s forced to meet %s: no pose survives the exact reach (container, every other K', A161 miss per piece)" % (r, sorted(S))
            self.T.test("ROLE-JOINT", role=r, slots=sorted(S), verdict="DEAD")
            info["dead"], info["clip"] = self.dead, "REACH"
            return info
        v1 = P.vol(pcs)
        clips[r] = dict(slots=sorted(S), frac=round(fr, 6), n_pieces=len(pcs), vol=float(v1), vol_before=float(vol0.get(r, v1)),
                        box_after=FP.rect_f(P.hull_box(pcs)))
        if v1 < vol0.get(r, v1) * (1 - Fr(1, 10 ** 6)):
            changed = True
        self.pieces[r] = pcs
        self.roles[r] = P.hull_box(pcs)
        self.T.test("ROLE-CLIP", role=r, **clips[r])
    info["clips"] = clips
    new_boxes, named = [], []
    order = sorted(instantiate, key=lambda p: (not self.item[p]["is_corner"], (urec[p].get("diam") or 9)))
    for p in order:
        pcs = self.union_last.get(p) or []
        if not pcs:
            continue
        seed = P.coarsen(pcs)
        box = P.hull_box(seed)
        clash = [q for q, b in new_boxes if FP.rect_inter(box[:4], b[:4]) is not None and box[4] <= b[5] and b[4] <= box[5]]
        if clash:
            self.T.test("INSTANTIATE-DEFER", slot=p, box=FP.rect_f(box), clash_with=clash, why="pose set meets a same-round instantiation")
            continue
        role = "F%d" % (len(self.role_cell) + 1)
        new_boxes.append((p, box))
        self.roles[role] = box
        self.pieces[role] = seed
        self.role_cell[role] = -1
        self.role_slots[role] = (p,)
        if self.item[p]["is_corner"]:
            self.role_corner[role] = self.item[p]["corner"]
        self.T.test("INSTANTIATE", role=role, slot=p, box=FP.rect_f(box), n_pieces=len(seed), n_union_pieces=len(pcs), why=urec[p]["why"])
        named.append((p, role))
        changed = True
    info["instantiated"] = named
    info["changed"] = changed
    info["vol"] = {k: float(P.vol(v)) for k, v in self.pieces.items() if not k.startswith("P")}
    return info


def run(pg, max_rounds=10, on_round=None):
    """the loop: seeded fixed point, snapshot, page, round; stop on a kill, at the fixed point, or at the wall."""
    self = pg
    self.witness = None
    for rnd in range(1, max_rounds + 1):
        t0 = time.time()
        nd = self.normalise("round%d" % rnd)
        snap = self.snapshot(rnd, "round%d" % rnd)
        if nd is None:
            snap["note"] = "DEAD in the fixed point: " + str(self.dead)
            self.round_times.append(dict(round=rnd, seconds=round(time.time() - t0, 1), dead="EmptyBox"))
            if on_round:
                on_round(self)
            break
        if rnd >= 2 and not self.norm_shrunk and self.rounds and not self.rounds[-1].get("changed"):
            # A205: the fixed point did not move and the last apply changed nothing -> the node IS at its fixed point;
            # the option table would be the previous round's (skipped: ~100 s a node)
            info = dict(self.rounds[-1], round=rnd, fixed_point=True, instantiated=[], skipped="fixed point: nothing moved since round %d" % (rnd - 1))
            self.rounds.append(info)
            snap["forcing"] = dict(self.snapshots[-2].get("forcing") or {}) if len(self.snapshots) >= 2 else {}
            snap["note"] = info["skipped"]
            self.round_times.append(dict(round=rnd, seconds=round(time.time() - t0, 1), fix=(self.fix_rep or {}).get("seconds"), passes=(self.fix_rep or {}).get("passes"),
                                         changed=False, dead=None, kept=(self.fix_rep or {}).get("kept"), skipped=True))
            if on_round:
                on_round(self)
            break
        info = propagate_round(self, rnd)
        info["seconds"] = round(time.time() - t0, 1)
        info["fix_seconds"] = (self.fix_rep or {}).get("seconds")
        self.rounds.append(info)
        snap["forcing"] = dict(forced_H=info.get("forced_H"), forced_role=info.get("forced_role"), instantiated=info.get("instantiated"),
                               clips=info.get("clips"), caps=info.get("caps"), witness=info.get("witness"), dead=info.get("dead"),
                               single={p: sorted(v) for p, v in info.get("single", {}).items()}, changed=info.get("changed"),
                               union={p: {k: u.get(k) for k in ("bbox", "diam", "cap", "why")} for p, u in (info.get("union") or {}).items()})
        snap["dead"] = self.dead
        self.round_times.append(dict(round=rnd, seconds=info["seconds"], fix=info["fix_seconds"], passes=(self.fix_rep or {}).get("passes"),
                                     changed=info.get("changed"), dead=info.get("clip"), kept=(self.fix_rep or {}).get("kept")))
        if on_round:
            on_round(self)
        if self.dead:
            break
        if not info.get("changed") and not self.norm_shrunk:
            info["fixed_point"] = True
            break
        if self.T.out_of_time():
            info["wall"] = True
            break
    return self.result()
