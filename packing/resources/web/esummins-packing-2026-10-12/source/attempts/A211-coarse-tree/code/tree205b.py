"""A205 -- the CLIP TREE: depth-first over a forced slot's remaining meeter options with A204's cascade at every node.

Node = TreePage state (pins + H + instantiated meeters as PIECES).  At a node whose cascade left it alive: for every
forced slot p let named_p = {H if H is not provably missing p} u {instantiated roles not provably missing p}, rows_p =
the alive cells of p's anonymous option table (after Lemma HC).  Theorem FC gives two distinct non-pin meeters of p:
  |named_p| = 0  ->  two anonymous meeters: branch over unordered PAIRS of rows (distinct cells by Lemma A1; hulls at
                     l-inf distance >= 1/sqrt2; rule-S compatible on the rows' pieces) -- exhaustive;
  |named_p| = 1  ->  at least one anonymous meeter: branch over the rows singly -- exhaustive;
  |named_p| >= 2 ->  the slot is not branched on.
The slot with the fewest alive rows is chosen (ties: the one H reaches); a slot with ONE branch is applied without
branching (unit propagation); a branch instantiates each chosen row as a role seeded with the row's reach pieces (the
poses of a free square with centre in that cell meeting p, clipped against every role's K': a superset, sound), pins
that cell (Lemma A1: no other centre in a cell of side < 1/sqrt2) and runs the cascade.  A branch dies by EmptyBox /
S-CLIP / FC / REACH / COUNT / NOROOM / S-PAIR (no rule-S-compatible pair of rows); an undecided branch (depth cap /
node cap / wall) stays ALIVE; the node dies when every branch does.  Every kill: [C: library clip trace].
"""
import itertools
import time

import poly204 as P
import poly204b as PB
import tree205 as T5

QP, FP = P.QP, P.FP


def clip_of(pg):
    rt = pg.round_times[-1] if pg.round_times else {}
    if (pg.fix_rep or {}).get("detail") == "sclip":
        return "S-CLIP"
    return rt.get("dead") or ((pg.rounds[-1].get("clip") if pg.rounds else None) or "EmptyBox")


NOROOM = False
SHARP = True


def cascade(pg, rounds, on_round=None, log=print):
    """A204's loop (seeded fixed point + S clip, HC rows, caps / FC / pair-table count, apply) then the no-room leaf."""
    pg.rounds, pg.snapshots, pg.round_times, pg.dead, pg.witness = [], [], [], None, None
    pg.sclip_rep, pg.hc_dead, pg.pair_cache = [], [], {}
    pg.step0, pg.test0 = len(pg.T.steps), len(pg.T.tests)
    PB.run(pg, max_rounds=rounds, on_round=on_round)
    clip, rnd = None, None
    if pg.dead:
        clip, rnd = clip_of(pg), (pg.round_times[-1].get("round") if pg.round_times else None)
    elif NOROOM and len(pg.roles) >= 9:
        nr = QP.noroom_leaf(pg, log)
        if nr and nr.get("verdict") == "DEAD":
            pg.dead = "no-room (A189 Lemma 1): %s" % nr.get("reason")
            clip, rnd = "NOROOM", len(pg.round_times)
    return clip, rnd


def step_seconds(pg):
    """seconds per step name since the node's cascade started (the trace is shared across the tree)."""
    out = {}
    for st in pg.T.steps[getattr(pg, "step0", 0):]:
        out[st["step"]] = round(out.get(st["step"], 0.0) + float(st.get("seconds") or 0), 1)
    return out


def test_seconds(pg):
    out = {}
    for t in pg.T.tests[getattr(pg, "test0", 0):]:
        k = t.get("test")
        n, sec = out.get(k, (0, 0.0))
        out[k] = (n + 1, round(sec + float(t.get("seconds") or 0), 1))
    return out


def anon_needed(pg, p):
    """bar-anon forcing (the analogue of A204's bar-H): with the anonymous cap of p set to 0 the count has no cover
    (without and with the chord rows) => in every packing of the node an ANONYMOUS free square meets p, so one of
    p's alive rows is realised and the rows can be branched on singly.  Exact (the count is exhaustive unless capped)."""
    lo = getattr(pg, "last_opts", None)
    if lo is None or not pg.caps_last:
        return False
    free_opts, fixed_opts, _ = lo
    caps = dict(pg.caps_last)
    caps[p] = 0
    n_anon = pg.n_free - len(pg.role_cell)
    t0 = time.time()
    for chords in (False, True):
        r = pg.count_search(pg.slots, free_opts, fixed_opts, n_anon, pg.lines, pg.pin_chords, pg.s, caps, use_chords=chords)
        if not r.feasible:
            pg.T.test("COUNT", bar_anon=p, chords=chords, verdict="an anonymous meeter of %s is forced" % p, nodes=r.nodes, seconds=round(time.time() - t0, 3))
            return True
    return False


def candidates(pg):
    """-> (n_rows, tie, slot, branches) for the slot to branch on, or None when every slot has two named meeters."""
    if not pg.rounds:
        return None
    info = pg.rounds[-1]
    if info.get("instantiated"):
        return "stale"          # the option table predates the roles this round instantiated: one more cascade round first (SOUNDNESS: a
                                # branch row could otherwise duplicate an FC-instantiated anonymous meeter -- the Y0491 g1 artefact)
    single, H_reach = info.get("single") or {}, set(info.get("H_reach") or [])
    reach_r = {r: set().union(*[set(S) for _, S in rows]) if rows else set() for r, rows in (info.get("fixed") or {}).items()}
    inst = info.get("instantiated") or []
    best = None
    for p in pg.slots:
        named = ([pg.H] if p in H_reach else []) + [r for r in sorted(reach_r) if r != pg.H and p in reach_r[r]] + [role for q, role in inst if q == p]
        rows = sorted(int(c) for c in single.get(p, {}))
        anon_forced = False
        if len(named) >= 2:
            if not rows or not anon_needed(pg, p):
                continue
            anon_forced = True                                   # bar-anon: no cover without an anonymous meeter of p
        if len(named) == 1 or anon_forced:
            br = [dict(slot=p, kind="row-anon" if anon_forced else "row", rows=[ci], named=named) for ci in rows]
        else:
            br, excl = [], []
            for ci, cj in itertools.combinations(rows, 2):
                A, B = pg.reach(ci, frozenset([p]))[1], pg.reach(cj, frozenset([p]))[1]
                if not A or not B:
                    continue
                if not FP.a1_compatible(FP.pieces_hull(A)[:4], FP.pieces_hull(B)[:4]):
                    excl.append((ci, cj, "A1"))
                    continue
                if not T5.s_compatible(T5.coarse(A), T5.coarse(B)):
                    excl.append((ci, cj, "S"))
                    continue
                br.append(dict(slot=p, kind="pair", rows=[ci, cj], named=[]))
            for b in br:
                b["excluded"] = excl
        key = (len(rows), 0 if p in H_reach else 1, p)
        if best is None or key < best[0]:
            best = (key, p, br, rows, named, excl if len(named) == 0 else [])
    if best is None:
        return None
    (n, tie, _), p, br, rows, named, excl = best
    return dict(n_rows=n, slot=p, branches=br, rows=rows, named=named, excluded=excl)


def apply_branch(pg, br):
    """instantiate the branch's rows as roles (pieces = the row's reach survivors, cell pinned), name the slot."""
    p = br["slot"]
    out = []
    for ci in br["rows"]:
        pcs = pg.reach(ci, frozenset([p]))[1]
        seed = P.coarsen(pcs)
        role = "F%d" % (len(pg.role_cell) + 1)
        pg.roles[role] = P.hull_box(seed)
        pg.pieces[role] = seed
        pg.role_cell[role] = ci
        pg.cell_role[ci] = role
        pg.role_slots[role] = (p,)
        if pg.item[p]["is_corner"]:
            pg.role_corner[role] = pg.item[p]["corner"]
        pg.T.test("BRANCH-INSTANTIATE", role=role, slot=p, cell=ci, box=FP.rect_f(pg.roles[role]), n_pieces=len(seed), n_reach_pieces=len(pcs))
        out.append((ci, role))
    return out


class Tree:
    def __init__(self, pg, rounds=3, depth_cap=4, node_cap=200, on_node=None, log=print):
        self.pg, self.rounds, self.depth_cap, self.node_cap = pg, rounds, depth_cap, node_cap
        self.on_node, self.log = on_node, log
        self.nodes, self.n_nodes, self.max_depth = [], 0, 0
        self.alive_leaves, self.dead_leaves = 0, 0

    def snap(self, pg, cap=300):
        s = pg.snapshots[-1] if pg.snapshots else None
        if s is None:
            return None
        s = dict(s)
        s["roles"] = {k: dict(v, pieces=(v.get("pieces") or [])[:cap]) for k, v in s["roles"].items()}
        return s

    def record(self, label, depth, br, verdict, clip, rnd, t0, reason=None):
        pg = self.pg
        r = dict(label=label, depth=depth, slot=(br or {}).get("slot"), kind=(br or {}).get("kind"), rows=(br or {}).get("rows"),
                 named=(br or {}).get("named"), excluded=(br or {}).get("excluded"), verdict=verdict, clip=clip, killed_round=rnd,
                 leaf=pg.dead, reason=reason, seconds=round(time.time() - t0, 1), t=round(pg.T.now(), 1), n_rounds=len(pg.round_times),
                 round_times=list(pg.round_times), roles={k: [round(float(v), 6) for v in b] for k, b in pg.roles.items() if not k.startswith("P")},
                 role_slots={k: list(v) for k, v in pg.role_slots.items()}, role_cell=dict(pg.role_cell), forced_H=sorted(pg.forced_H),
                 kept=(pg.fix_rep or {}).get("kept"), sclip=list(pg.sclip_rep), hc_dead=list(pg.hc_dead)[:40],
                 alive_cells={p: sorted(v) for p, v in (pg.rounds[-1].get("single") or {}).items()} if pg.rounds else None,
                 snapshot=self.snap(pg), verifier="[C: library clip trace]", step_seconds=step_seconds(pg), test_seconds=test_seconds(pg))
        self.nodes.append(r)
        self.max_depth = max(self.max_depth, depth)
        if verdict == "DEAD":
            self.dead_leaves += 1
        elif verdict == "ALIVE":
            self.alive_leaves += 1
        self.log("   node %-10s d%d %s%s: %s%s (%s s, %d rounds; t=%s)" % (
            label, depth, (br or {}).get("slot") or "root", ("<-" + str((br or {}).get("rows"))) if br else "", verdict,
            (" by %s r%s" % (clip, rnd)) if clip else ((" [%s]" % reason) if reason else ""), r["seconds"], r["n_rounds"], r["t"]))
        if self.on_node:
            self.on_node(self)
        return r

    def run(self):
        pg = self.pg
        t0 = time.time()
        clip, rnd = cascade(pg, self.rounds, log=self.log)
        self.n_nodes = 1
        if pg.dead:
            self.record("R", 0, None, "DEAD", clip, rnd, t0)
            return self.result()
        self.record("R", 0, None, "INTERNAL", None, None, t0)
        self.expand(0, "R")
        return self.result()

    def undecided(self, label, depth, br, why):
        pg = self.pg
        self.nodes.append(dict(label=label, depth=depth, slot=(br or {}).get("slot"), kind=(br or {}).get("kind"), rows=(br or {}).get("rows"),
                               named=(br or {}).get("named"), verdict="ALIVE", clip=None, reason=why, seconds=0.0, t=round(pg.T.now(), 1),
                               n_rounds=0, snapshot=None, verifier="[C: library clip trace]"))
        self.alive_leaves += 1

    def expand(self, depth, label):
        pg = self.pg
        while True:
            ch = candidates(pg)
            n_stale = 0
            while ch == "stale" and n_stale < 4:
                # the last round instantiated a role: refresh the option table (one cascade round) before any branching
                t0 = time.time()
                clip, rnd = cascade(pg, 1, log=self.log)
                self.n_nodes += 1
                n_stale += 1
                self.record(label + "r%d" % n_stale, depth, dict(slot=None, kind="refresh", rows=None, named=None), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
                if pg.dead:
                    return
                ch = candidates(pg)
            if ch == "stale":
                self.nodes[-1].update(verdict="ALIVE", reason="undecided: the option table stayed stale after 4 refresh rounds")
                self.alive_leaves += 1
                return
            if ch is None and SHARP and not getattr(pg, "sharpened", False):
                # the SHARP leaf (A182's rule: a survivor of the 4/2 pass re-normalised at 8/3, seeded from its own fixed
                # point -- sound, never weaker): one more cascade round with refine 3 / nsub 8 on the fully named node
                t0 = time.time()
                pg.refine_mb, pg.nsub_mb, pg.sharpened = 3, 8, True
                clip, rnd = cascade(pg, 1, log=self.log)
                pg.refine_mb, pg.nsub_mb = 2, 4
                self.n_nodes += 1
                self.record(label + "s", depth, dict(slot=None, kind="sharp", rows=None, named=None), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
                if pg.dead:
                    return
                continue
            if ch is None:
                self.nodes[-1].update(verdict="ALIVE", reason="every forced slot has two named meeters: nothing to branch on (next lever: LP on the node)")
                self.alive_leaves += 1
                return
            if not ch["branches"]:
                pg.dead = "S-PAIR at %s: no rule-S / A1 compatible pair among its %d alive rows %s (Theorem FC needs two anonymous meeters; excluded %s)" % (
                    ch["slot"], len(ch["rows"]), ch["rows"], ch["excluded"])
                self.nodes[-1].update(verdict="DEAD", clip="S-PAIR", leaf=pg.dead, killed_round=len(pg.round_times))
                self.dead_leaves += 1
                pg.T.test("S-PAIR", slot=ch["slot"], rows=ch["rows"], verdict="DEAD")
                if self.on_node:
                    self.on_node(self)
                return
            if len(ch["branches"]) > 1:
                break
            br = ch["branches"][0]
            t0 = time.time()
            apply_branch(pg, br)
            clip, rnd = cascade(pg, self.rounds, log=self.log)
            self.n_nodes += 1
            self.record(label + "u", depth, dict(br, unit=True), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            if pg.dead:
                return
        if depth >= self.depth_cap or self.n_nodes >= self.node_cap or pg.T.out_of_time():
            why = "depth cap" if depth >= self.depth_cap else ("node cap" if self.n_nodes >= self.node_cap else "wall")
            self.nodes[-1].update(verdict="ALIVE", reason="undecided (%s) before branching on %s over %s" % (why, ch["slot"], [b["rows"] for b in ch["branches"]]))
            self.alive_leaves += 1
            return
        self.nodes[-1].update(branch_slot=ch["slot"], n_branches=len(ch["branches"]), branch_rows=[b["rows"] for b in ch["branches"]])
        st = T5.save_state(pg)
        for i, br in enumerate(ch["branches"]):
            lab = "%s.%d" % (label, i + 1)
            if pg.T.out_of_time() or self.n_nodes >= self.node_cap:
                self.undecided(lab, depth + 1, br, "undecided: %s before this branch ran" % ("wall" if pg.T.out_of_time() else "node cap"))
                continue
            T5.restore_state(pg, st)
            t0 = time.time()
            pg.sharpened = False
            apply_branch(pg, br)
            clip, rnd = cascade(pg, self.rounds, log=self.log)
            self.n_nodes += 1
            self.record(lab, depth + 1, br, "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            if not pg.dead:
                self.expand(depth + 1, lab)
        T5.restore_state(pg, st)

    def result(self):
        dead = [n for n in self.nodes if n["verdict"] == "DEAD"]
        verdict = "DEAD" if (self.alive_leaves == 0 and dead) else "ALIVE"
        return dict(verdict=verdict, n_nodes=self.n_nodes, n_records=len(self.nodes), max_depth=self.max_depth, alive_leaves=self.alive_leaves,
                    dead_leaves=self.dead_leaves, killing=[dict(label=n["label"], slot=n.get("slot"), rows=n.get("rows"), clip=n.get("clip"),
                                                              round=n.get("killed_round"), seconds=n.get("seconds")) for n in dead],
                    undecided=[dict(label=n["label"], reason=n.get("reason")) for n in self.nodes if n["verdict"] == "ALIVE"])
