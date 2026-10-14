"""A211 -- the COARSE TREE (notes/coarse_tree.md): A209's composed tree with CHEAP internal nodes (coarse211.CoarsePage:
one cascade round, re-binned pieces, refine 1, no lonely clip, shallow reach) branched at once on the tightest slot
(A205's rule: fewest rows, pairs when no named meeter, unit propagation), and at every FULLY NAMED leaf (every forced
slot has two named meeters on a fresh table) the leaf rules in order, cheapest first:
  (a) rule CC (Lemma CORNER-COVER, leaves211);  (b) NO-ROOM + the pocket CN bound at k >= 9 (A208 / A209: pockets
  branched on at k = 9, Lemma POCKET);  (c) the basin clip (A207, Lemma BASIN);  (d) Rule NS on a soft name (A206,
  slivers only: MAX_FRAC);  (d') Lemma ROLE-SPLIT (rsplit211, notes/coarse_tree.md s.5: where no-room did NOT kill,
  the widest non-pin role -- an empty core preferred -- is bisected at the midpoint of its widest dimension and both
  halves recurse through the coarse round and the leaf rules; <= 4 splits per role along a path);
  (e) the EXACT cascade at the leaf (nsub 4 / refine 2, lonely clip, basins, 3 rounds) then
  the sharp round -- after which the loop re-reads the table: new branches are coarse children again.
A leaf is DEAD iff one rule proves it; a node is DEAD iff every branch is (Lemma CT); undecided = ALIVE."""
import os
import sys
import time

_A224 = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "A224-snap-rule", "code"))
if _A224 not in sys.path:
    sys.path.insert(0, _A224)

import poly204 as P
import tree205b as TB
import tree206 as N6
import tree206b as NB
import tree209 as N9
import leaves211 as L11
import inherit211 as INH
import rsplit211 as RS
import snap224 as SNAP                    # A224 Rule SNAP (flag A224_SNAP=1, default OFF: with it off nothing here runs)

EXACT_ROUNDS = 3
NOROOM_CAP = 120.0                     # seconds for A189's no-room at a leaf (Y0202 test: 300 s UNDECIDED x 3 ate half the wall)

# ---------------------------------------------------------------------------- A220 (attempts/A220-exact-first), all OFF by default
EXACT_FIRST = (os.environ.get("A220_EXACT_FIRST") or "").strip().lower()   # "" off | "1"/"on" always | "small" only a positionally small role
BUDGET = float(os.environ.get("A220_BUDGET") or 45.0)                      # seconds for ONE budgeted exact round
EXACT_FIRST_ROUNDS = int(os.environ.get("A220_EXACT_ROUNDS") or 1)
SMALL_EXT = float(os.environ.get("A220_SMALL_EXT") or 0.25)                # variant "small": max position extent of the role the split would bisect
NOROOM_INHERIT = (os.environ.get("A220_NOROOM_INHERIT") or "") == "1"      # addendum: the SHORT child cap after an UNDECIDED parent
NOROOM_CHILD_CAP = float(os.environ.get("A220_NOROOM_CHILD_CAP") or 25.0)
NR_SHRINK = float(os.environ.get("A220_NOROOM_SHRINK") or 0.5)             # a role box that lost more than this fraction earns the FULL cap


def box_shrank(old, new, frac=NR_SHRINK):
    """A220 addendum: did the node change materially since the ancestor's no-room -- a NEW role, or some role box
    that lost more than `frac` of its (x, y, t) volume?  Then the ancestor's UNDECIDED says nothing and the child
    gets the full cap; otherwise the boxes are essentially the ancestor's and the search will cap again."""
    for k, b in (new or {}).items():
        a = (old or {}).get(k)
        if a is None:
            return True
        va, vb = P.box_vol(a), P.box_vol(b)
        if va > 0 and vb < va * (1.0 - frac):
            return True
    return False


class Tree211(N9.Tree209):
    def __init__(self, pg, dead_paths=None, path0=(), **kw):
        N9.Tree209.__init__(self, pg, **kw)
        self.cc_kills, self.exact_rounds, self.basin_kills = 0, 0, 0
        self.rsplits, self.rsplit_kills = 0, 0
        self._ns = self._rs = None
        self.ef_runs, self.ef_kills, self.ef_timeouts, self.ef_seconds = 0, 0, 0, 0.0      # A220 exact-first
        self.nr_short, self.nr_state, self.pocket_terminal = 0, {}, set()                  # A220 addendum: the short no-room cap
        self.snap_runs, self.snap_kills, self.snap_handoffs, self.snap_partial = 0, 0, 0, 0   # A224 Rule SNAP
        self.snap_cands, self.snap_seconds, self.snap_first, self.snap_rows = 0, 0.0, None, []
        self.eps_runs, self.eps_kills, self.eps_seconds, self.eps_rows = 0, 0, 0.0, []            # A230 Rule EPS
        self.eps_cands, self.eps_first, self.eps_ns_splits, self.eps_ns_kills = 0, None, 0, 0
        self._ens = None
        self.dead_paths = dead_paths or {}          # Lemma INHERIT: path -> the certificate that closed it
        self.pathof = {self.root_label: tuple(path0)}
        self.n_inherited = 0

    # ------------------------------------------------------------------ Lemma INHERIT at every depth
    def step_key(self, br):
        """the branch's hypothesis as inherit211's path step (a unit-propagation step adds none: it is derived)."""
        kind = str(br.get("kind") or "row")
        if kind.startswith("ns-"):
            return ("ns", str(br.get("slot")), str(br.get("role")), kind)
        if kind.startswith("epsns-"):                            # A230 Rule EPS at the wedge
            return ("epsns", str(br.get("slot")), str(br.get("role")), kind, str(br.get("wedge")))
        if kind == "pocket":
            return ("pocket", tuple(round(float(v), 6) for v in (br.get("pocket") or ())), tuple(br.get("rows") or ()))
        if kind == "rsplit":                                     # Lemma ROLE-SPLIT (notes/coarse_tree.md s.5)
            return ("rsplit", str(br.get("role")), str(br.get("dim")), str(br.get("m")), str(br.get("side")))
        return ("row", str(br.get("slot")), tuple(br.get("rows") or ()))

    def rsplit_used(self, label):
        """how often each role has already been bisected on this node's path (Lemma ROLE-SPLIT's per-role cap)."""
        c = {}
        for s in self.pathof.get(label, ()):
            if s and s[0] == "rsplit":
                c[s[1]] = c.get(s[1], 0) + 1
        return c

    def epsns_used(self, label):
        """how often each (slot, role) pair has already been split AT THE WEDGE on this node's path (A230: the clip
        tightens each time, but the returns diminish and the split would otherwise eat the whole depth budget)."""
        c = {}
        for s in self.pathof.get(label, ()):
            if s and s[0] == "epsns":
                c[(s[1], s[2])] = c.get((s[1], s[2]), 0) + 1
        return c

    def eff_depth(self, depth, label):
        """the depth the CAP counts: a role split is charged to its own per-role cap, not to the tree's depth."""
        return depth - sum(self.rsplit_used(label).values())

    def child_path(self, lab, parent, br):
        p = tuple(self.pathof.get(parent, ())) + (self.step_key(br),)
        self.pathof[lab] = p
        if not self.dead_paths:
            return None, None, p
        info, q = INH.covered(self.dead_paths, p)
        return info, q, p

    def record_inherited(self, lab, depth, br, info, p):
        pg = self.pg
        why = ("Lemma INHERIT: the hypothesis of this branch (%d step(s): %s) is already refuted -- %s closed it as %s in %s [%s]" % (
            len(p), "; ".join("%s<-%s" % (s[1], s[2]) for s in p), info.get("camp"), info.get("label"), info.get("cert"), info.get("rule")))
        self.nodes.append(dict(label=lab, depth=depth, slot=br.get("slot"), kind="inherited", rows=br.get("rows"), named=br.get("named"),
                               verdict="DEAD", clip="INHERIT", killed_round=None, reason="inherited DEAD from %s %s" % (info.get("camp"), info.get("cert")),
                               leaf=why, seconds=0.0, t=round(pg.T.now(), 1), n_rounds=0, snapshot=None,
                               source_cert=info.get("cert"), source_label=info.get("label"), source_camp=info.get("camp"),
                               source_rule=info.get("rule"), source_ledger=info.get("ledger"),
                               verifier="[C: library clip trace] inherited (Lemma INHERIT, notes/coarse_tree.md s.4): %s" % info.get("cert")))
        self.dead_leaves += 1
        self.n_inherited += 1
        self.inherit_hits[lab] = dict(info, path=[list(map(str, s)) for s in p], slot=br.get("slot"), rows=br.get("rows"))
        pg.T.test("INHERIT", label=lab, verdict="DEAD", cert=info.get("cert"), source=info.get("label"), rule=info.get("rule"))
        self.log("   node %-10s d%d %s<-%s: DEAD INHERITED from %s %s (%s)" % (lab, depth, br.get("slot"), br.get("rows"), info.get("camp"), info.get("label"), info.get("cert")))
        if self.on_node:
            self.on_node(self)

    def record(self, label, depth, br, verdict, clip, rnd, t0, reason=None):
        cb, self.on_node = self.on_node, None
        r = NB.Tree206.record(self, label, depth, br, verdict, clip, rnd, t0, reason=reason)
        self.on_node = cb
        pg = self.pg
        r["coarse"] = pg.coarse
        r["n_pieces"] = {k: len(v) for k, v in pg.pieces.items() if not k.startswith("P")}
        r["rebin"] = list(pg.rebin_rep)[-6:]
        if self.on_node:
            self.on_node(self)
        return r

    def fresh_child(self):
        pg = self.pg
        pg.set_coarse(True)
        pg.sharpened, pg.noroom_done, pg.basin_done = False, False, False

    def kill(self, label, depth, clip, leaf, **extra):
        pg = self.pg
        pg.dead = leaf
        self.nodes[-1].update(verdict="DEAD", clip=clip, leaf=leaf, killed_round=len(pg.round_times), reason=None, **extra)
        self.dead_leaves += 1
        pg.T.test(clip, label=label, verdict="DEAD", leaf=leaf[:200])
        self.log("   node %-10s d%d: DEAD by %s -- %s" % (label, depth, clip, leaf[:170]))
        if self.on_node:
            self.on_node(self)

    def alive(self, why):
        NB.Tree206.leaf_alive(self, why)
        self.log("   node %-10s: ALIVE [%s]" % (self.nodes[-1]["label"], why[:150]))

    # ------------------------------------------------------------------ A224: Rule SNAP (flag A224_SNAP=1, default OFF)
    def snap_try(self, depth, label, where):
        """Rule SNAP (attempts/A224-snap-rule, docs/proofs/snap_rule.md): a role whose box sits on a simple slot pose
        whose cell NO other square can meet teleports into the slot (Lemma SWAP / `teleport_of_swap`), so the packing
        lies in the extension stratum -- DEAD when that stratum is a FULL scoreboard row.  Cost with the flag off: nil;
        with it on: the near test (floats, roles x slots) and, only when it fires, one exact miss test per other role."""
        if not SNAP.ON or self.pg.dead or not self.nodes:
            return "OK"
        t0 = time.time()
        r = L11.snap_eval(self.pg, label, log=self.log)
        if r is None:
            return "OK"
        r["where"], r["depth"], r["seconds"] = where, depth, round(time.time() - t0, 3)
        self.snap_runs += 1
        self.snap_seconds += r["seconds"]
        self.snap_cands += r.get("n_cands") or 0
        self.snap_partial += 1 if r.get("partial") else 0
        self.nodes[-1].setdefault("snap", r)
        if r.get("n_cands"):
            self.snap_rows.append(dict(label=label, where=where, verdict=r.get("verdict"), kind=r.get("kind"),
                                       n_cands=r.get("n_cands"), n_anon=r.get("n_anon"), seconds=r["seconds"],
                                       cands=r.get("cands"), target=r.get("target"),
                                       snapped=[dict(role=c["role"], slot=c["slot"]) for c in (r.get("snapped") or [])]))
        self.pg.T.test("SNAP", label=label, where=where, verdict=r.get("verdict"), rule=r.get("kind"),
                       n_cands=r.get("n_cands"), n_anon=r.get("n_anon"), seconds=r["seconds"],
                       stratum=(r.get("target") or {}).get("stratum"))
        if r.get("verdict") == "DEAD":
            self.snap_kills += 1
            if self.snap_first is None:
                self.snap_first = round(self.pg.T.now(), 1)
            self.kill(label, depth, r["kind"], r["leaf"], snap=r, verifier=r["verifier"])
            return "DEAD"
        if r.get("verdict") == "HANDOFF":                      # snapped into a stratum that is NOT closed: hand off
            self.snap_handoffs += 1
            self.alive(r["leaf"])
            return "ALIVE"
        return "OK"

    # ------------------------------------------------------------------ A230: Rule EPS (flag A230_EPS=1, default OFF)
    def eps_try(self, depth, label, where):
        """Rule EPS (attempts/A230-eps-branch, docs/proofs/lemma_eps.md): at a FORCED cell where a role is near-simple,
        the second meeter Theorem FC demands must enter through a WEDGE of (role, cell) -- a free-side wedge polygon or
        the end zone of a pin/wall-backed side (EPS-3/4/5).  A230 evaluates EVERY candidate (smallest box first) and
        tests the exact wedge polygon, not only its bounding rectangle.  When every other role misses every target and
        no anonymous cell is within 1/sqrt2 of one, the node is DEAD by FC+EPS; when exactly ONE role survives with the
        anonymous clause certified empty, that role MUST meet the wedge -- the NS-at-wedge split ("EPSNS").  Flag off:
        nil (L11.EPS_ON is read once at import)."""
        if not L11.EPS_ON or self.pg.dead or not self.nodes:
            return "OK"
        t0 = time.time()
        used = self.epsns_used(label)
        skip = {k for k, v in used.items() if v >= L11.EPS_WEDGE_CAP}
        r = L11.eps_eval(self.pg, label, log=self.log, skip=skip)
        if r is None:
            return "OK"
        r["where"], r["depth"], r["seconds"] = where, depth, round(time.time() - t0, 3)
        self.eps_runs += 1
        self.eps_cands += r.get("n_cands") or 0
        self.eps_seconds += r["seconds"]
        self.nodes[-1].setdefault("eps", r)
        w = r.get("wedge_ns")
        self.eps_rows.append(dict(label=label, where=where, verdict=r.get("verdict"), n_cands=r.get("n_cands"),
                                  n_added=r.get("n_added"), taper=r.get("taper"), seconds=r["seconds"],
                                  wedge_ns=(dict(role=w["role"], slot=w["slot"], F=w["F"], n_targets=w["n_targets"]) if w else None),
                                  cands=[dict(role=c["role"], slot=c["slot"], only_new=c["only_new"], struck=c["struck"],
                                              survivors=sorted(c["survivors"]), anon_cells=c.get("anon_cells")) for c in (r.get("cands") or [])][:8]))
        self.pg.T.test("EPS", label=label, where=where, verdict=r.get("verdict"), n_cands=r.get("n_cands"),
                       seconds=r["seconds"], wedge_ns=bool(w))
        if r.get("verdict") == "DEAD":
            self.eps_kills += 1
            if self.eps_first is None:
                self.eps_first = round(self.pg.T.now(), 1)
            self.kill(label, depth, "FC+EPS", r["leaf"], eps=r["kill"], verifier=r["verifier"])
            return "DEAD"
        if w and self.eff_depth(depth, label) < self.depth_cap and self.n_nodes < self.node_cap and not self.pg.T.out_of_time():
            self._ens = w
            return "EPSNS"
        return "OK"

    # ------------------------------------------------------------------ A220: ONE budgeted exact cascade round, early
    def anc_noroom(self):
        """the nearest ANCESTOR on the live context stack whose no-room ran (A220 addendum)."""
        for _d, lab in reversed(self._ctx[:-1]):
            st = self.nr_state.get(lab)
            if st is not None:
                return st
        return None

    def exact_first(self, depth, label, node, why):
        """A220: run ONE exact cascade round (tree206.budget_cascade, A220_BUDGET seconds) BEFORE the expensive rule.
        On DEAD the kill is recorded as this node's `x` record exactly as rule (e) does; on a timeout the sound
        shrinks already made are KEPT (a prefix of a sound clip chain), coarse mode is restored and the caller falls
        through to the old rule.  At most one per node."""
        pg = self.pg
        if node.get("exact_first") or not pg.coarse or pg.T.out_of_time():
            return "OK"
        t0 = time.time()
        pg.set_coarse(False)
        out = N6.budget_cascade(pg, EXACT_FIRST_ROUNDS, BUDGET, log=self.log)
        self.ef_runs += 1
        self.ef_seconds += out["seconds"]
        self.ef_timeouts += 1 if out["timeout"] else 0
        node["exact_first"] = dict(why=why, budget=BUDGET, seconds=out["seconds"], timeout=out["timeout"],
                                   rounds=out["rounds"], clip=out["clip"], verdict="DEAD" if pg.dead else "undecided")
        self.log("   A220 exact-first at %-10s (%s): %s in %.1f s (%d round(s) of budget %.0f s)" % (
            label, why, ("DEAD by %s" % out["clip"]) if pg.dead else ("TIMEOUT" if out["timeout"] else "undecided"),
            out["seconds"], out["rounds"], BUDGET))
        if pg.dead:
            self.ef_kills += 1
            self.n_nodes += 1
            self.exact_rounds += 1
            self.record(label + "x", depth, dict(slot=None, kind="exact", rows=None, named=None), "DEAD", out["clip"], out["rnd"], t0)
            return "DEAD"
        pg.set_coarse(True)
        return "OK"

    # ------------------------------------------------------------------ the leaf rules at a fully named node
    def leaf_rules(self, depth, label):
        pg = self.pg
        node = self.nodes[-1]
        caps = self.eff_depth(depth, label) >= self.depth_cap or self.n_nodes >= self.node_cap
        if pg.T.out_of_time():
            self.alive("undecided (wall) at the fully named leaf before the leaf rules")
            return "ALIVE"
        s = self.snap_try(depth, label, "leaf")                                    # (0) A224 Rule SNAP, the FIRST rule
        if s != "OK":
            return s
        s = self.eps_try(depth, label, "leaf")                                     # (0') A230 Rule EPS, beside SNAP
        if s != "OK":
            return s
        t0 = time.time()                                                          # (a) rule CC
        rows = L11.cc_rows(pg, label)
        node["cc"] = dict(n_rows=len(rows), seconds=round(time.time() - t0, 3), rows=[{k: v for k, v in r.items() if k != "band"} for r in rows][:8])
        dead = [r for r in rows if r["verdict"] == "DEAD"]
        if dead:
            r = dead[0]
            self.cc_kills += 1
            self.kill(label, depth, "CC", "rule CC at %s (Lemma CORNER-COVER; %s pad, lam %s): %s" % (label, pg.pad, round(float(pg.lam), 6), r["why"]),
                      cc_slot=r["slot"], cc_role=r["role"], verifier=r["verifier"])
            return "DEAD"
        # (b) no-room + pockets: once per k along a path (an NS child adds no role: its boxes are subsets of the parent's,
        #     where the search was already UNDECIDED at the cap; a row / pocket child adds a role and runs it afresh)
        # PI 2026-09-12 19:40: run no-room at EVERY fully named leaf -- a child's smaller boxes mean LARGER cores, so an
        # UNDECIDED parent says nothing about the child (the once-per-k skip was backwards); node-level flag only.
        if len(pg.roles) >= 9 and not node.get("noroom"):
            # A220 addendum (i)/(ii): when the nearest ancestor's no-room already ran out its cap UNDECIDED and no role
            # box has since lost more than NR_SHRINK of its volume (and this is not a terminal m = 1 pocket child), the
            # same search will cap again -- run it under the SHORT cap instead, and spend the saved seconds on ONE
            # budgeted EXACT round first (which shrinks the boxes the search reads: smaller boxes, LARGER cores).
            cap, short = NOROOM_CAP, None
            if NOROOM_INHERIT:
                anc = self.anc_noroom()
                if anc and anc["capped"] and label not in self.pocket_terminal and not box_shrank(anc["roles"], pg.roles):
                    cap, short = NOROOM_CHILD_CAP, dict(anc=anc["label"], anc_seconds=anc["seconds"], anc_cap=anc["cap"], shrink=NR_SHRINK)
                    self.nr_short += 1
                    if self.exact_first(depth, label, node, "before no-room (ancestor %s UNDECIDED at %.0f s)" % (anc["label"], anc["seconds"])) == "DEAD":
                        return "DEAD"
            res = N9.noroom_at(pg, min(pg.T.left() or 0.0, cap + 30), log=self.log, deadline=(cap if short else None))
            rec = dict(label=label, depth=depth, k=res["k"], m=res["m"], verdict=res["verdict"], clip=res["clip"], bound=res["bound"], cn_bound=res["cn_bound"],
                       n_pockets=len(res["pockets"]), pockets=res["pockets"], seconds=res["seconds"], reason=res["reason"], cap=cap, short_cap=short)
            self.nr_state[label] = dict(label=label, verdict=res["verdict"], seconds=res["seconds"], cap=cap,
                                        capped=(res["verdict"] != "DEAD" and res["seconds"] >= 0.8 * cap),
                                        roles={k: tuple(v) for k, v in pg.roles.items()})
            self.noroom_runs.append(rec)
            node["noroom"] = rec
            if res["verdict"] == "DEAD":
                self.kill(label, depth, res["clip"], "no-room at %s (k=%d, m=%d; A189 Lemma 1%s on the role boxes): %s" % (
                    label, res["k"], res["m"], " + Lemma CN" if res["clip"] == "NOROOM-CN" else "", res["reason"]))
                return "DEAD"
            # PI 2026-09-14 16:40 (Y0130 R.3.1.1.p3.2): with m = 1 the LAST square's centre lies in one of the pockets
            # (A189's bisection certifies every centre outside them dead), so branch the 11th square into each pocket
            # too -- the child is fully named (11 roles) and the cascade decides; no lane cover needed (Lemma POCKET, m >= 1)
            # an m = 1 pocket split is TERMINAL (its children are fully named): it is exempt from the depth cap
            # (Y0130 g1 R.3.1.1.p3.2 sat at eff_depth 5 with two pockets and never branched); node cap and wall still apply
            terminal = res["m"] == 1
            if res["m"] >= 1 and res["pockets"] and (terminal or not caps) and self.n_nodes < self.node_cap and not pg.T.out_of_time():
                self.pocket_branches(depth, label, res["pockets"], res)
                return "BRANCHED"
        if pg.all_basins and not getattr(pg, "basin_done", False):                # (c) the basin clip
            pg.basin_done = True
            pg.basins = list(pg.all_basins)
            ok = pg.basin_clip(label)
            if pg.coarse:
                pg.basins = []
            if not ok:
                self.basin_kills += 1
                self.kill(label, depth, "BASIN", pg.dead)
                return "DEAD"
            for k, pcs in pg.pieces.items():
                if pcs and not k.startswith("P"):
                    pg.roles[k] = P.hull_box(pcs)
        cands = N6.ns_candidates(pg)                                              # (d) Rule NS, slivers only
        node["ns_candidates"] = cands
        if cands and not caps and not pg.T.out_of_time():
            self._ns = cands[0]
            return "NS"
        # (d') Lemma ROLE-SPLIT (notes/coarse_tree.md s.5): no-room ran here and did NOT kill -- the wide roles have
        # EMPTY cores, so every core-based test is blind; bisect the widest one and let the children decide.
        nr = node.get("noroom")
        if nr and nr.get("verdict") != "DEAD" and self.n_nodes < self.node_cap and not pg.T.out_of_time():
            sps = RS.candidates(pg, self.rsplit_used(label))
            # A220 (PI, Y0865): the 8 leaves of 3-4 blind tilt bisections all die by EmptyBox in the EXACT cascade in
            # 0.7-18 s -- so spend ONE budgeted exact round HERE, before the split, and kill the parent instead.
            if EXACT_FIRST and sps and (EXACT_FIRST != "small" or max(sps[0]["extents"]["x"], sps[0]["extents"]["y"]) < SMALL_EXT):
                if self.exact_first(depth, label, node, "before ROLE-SPLIT on %s (%s)" % (sps[0]["role"], sps[0]["dim"])) == "DEAD":
                    return "DEAD"
                sps = RS.candidates(pg, self.rsplit_used(label))   # the shrinks are kept: re-read the candidates
            node["rsplit_candidates"] = [{k: v for k, v in s.items() if k != "m"} for s in sps[:6]]
            if sps:
                self._rs = sps[0]
                return "RSPLIT"
        if pg.coarse and pg.T.out_of_time():                                      # A211d: the exact cascade cost 838 s past a
            self.alive("undecided (wall) at the fully named leaf before the exact cascade")   # spent wall -- leave it undecided
            return "ALIVE"
        if pg.coarse:                                                             # (e) the exact cascade at the leaf
            t0 = time.time()
            pg.set_coarse(False)
            clip, rnd = N6.cascade(pg, EXACT_ROUNDS, log=self.log)
            self.n_nodes += 1
            self.exact_rounds += 1
            self.record(label + "x", depth, dict(slot=None, kind="exact", rows=None, named=None), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            return "DEAD" if pg.dead else "CONTINUE"
        if TB.SHARP and not getattr(pg, "sharpened", False):
            t0 = time.time()
            pg.refine_mb, pg.nsub_mb, pg.sharpened = 3, 8, True
            clip, rnd = N6.cascade(pg, 1, log=self.log)
            pg.refine_mb, pg.nsub_mb = 2, 4
            self.n_nodes += 1
            self.record(label + "s", depth, dict(slot=None, kind="sharp", rows=None, named=None), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            return "DEAD" if pg.dead else "CONTINUE"
        if cands:
            why = "depth cap" if depth >= self.depth_cap else ("node cap" if self.n_nodes >= self.node_cap else "wall")
            self.alive("undecided (%s) before Rule NS on %s at %s (frac %s)" % (why, cands[0]["role"], cands[0]["slot"], cands[0]["frac"]))
        else:
            soft = N6.ns_candidates.__globals__["SOFT_ALL"]
            self.alive("every forced slot has two named meeters after the exact cascade and the sharp round; no soft name below MAX_FRAC %s left to split (next lever: LP on the node)" % N6.MAX_FRAC)
        return "ALIVE"

    def pocket_branches(self, depth, label, pk, res):
        pg = self.pg
        self.pocket_splits += 1
        self.nodes[-1].update(branch_slot="pocket", n_branches=len(pk), branch_rows=[[j] for j in range(len(pk))], pockets=pk, verdict="INTERNAL", reason=None)
        self.log("   Lemma POCKET at %s: %d pockets (k=%d, m=%d): the next square instantiated in each" % (label, len(pk), res["k"], res["m"]))
        st = N6.save_state(pg)
        for j, pocket in enumerate(pk):
            lab = "%s.p%d" % (label, j + 1)
            if res["m"] == 1:
                self.pocket_terminal.add(lab)                     # A220 addendum (i): a terminal pocket child keeps the FULL no-room cap
            br = dict(slot="pocket", kind="pocket", rows=[j], named=None, pocket=[round(v, 6) for v in pocket], diam=round(N9.diam(pocket), 4))
            info, _q, p = self.child_path(lab, label, br)
            if info is not None:
                self.record_inherited(lab, depth + 1, br, info, p)
                continue
            if pg.T.out_of_time() or self.n_nodes >= self.node_cap:
                NB.Tree206.undecided(self, lab, depth + 1, br, "undecided: %s before this pocket branch ran" % ("wall" if pg.T.out_of_time() else "node cap"))
                continue
            N6.restore_state(pg, st)
            self.fresh_child()
            t0 = time.time()
            role = N9.apply_pocket(pg, pocket, j)
            clip, rnd = N6.cascade(pg, self.rounds, log=self.log)
            self.n_nodes += 1
            r = self.record(lab, depth + 1, br, "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            r["pocket_role"] = role
            if not pg.dead:
                self.expand(depth + 1, lab)
        N6.restore_state(pg, st)

    # ------------------------------------------------------------------ the node
    def expand(self, depth, label):
        self._ctx.append((depth, label))
        try:
            return self._expand(depth, label)
        finally:
            self._ctx.pop()

    def _expand(self, depth, label):
        pg = self.pg
        ns = rs = ens = None
        if self.snap_try(depth, label, "internal") != "OK":                        # A224: cheap, after the coarse round
            return
        e = self.eps_try(depth, label, "internal")                                 # A230: cheap, beside SNAP
        if e == "DEAD":
            return
        if e == "EPSNS":
            ens = self._ens
        while ens is None:
            ch = TB.candidates(pg)
            n_stale = 0
            while ch == "stale" and n_stale < 4:
                t0 = time.time()
                clip, rnd = N6.cascade(pg, 1, log=self.log)
                self.n_nodes += 1
                n_stale += 1
                self.record(label + "r%d" % n_stale, depth, dict(slot=None, kind="refresh", rows=None, named=None), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
                if pg.dead:
                    return
                ch = TB.candidates(pg)
            if ch == "stale":
                return self.alive("undecided: the option table stayed stale after 4 refresh rounds")
            if ch is None:
                r = self.leaf_rules(depth, label)
                if r == "NS":
                    ns = self._ns
                    break
                if r == "RSPLIT":
                    rs = self._rs
                    break
                if r == "EPSNS":                                  # A230: Rule EPS handed back the NS-at-wedge split
                    ens = self._ens
                    break
                if r == "CONTINUE":
                    continue
                return
            if not ch["branches"]:
                self.kill(label, depth, "S-PAIR", "S-PAIR at %s: no rule-S / A1 compatible pair among its %d alive rows %s (Theorem FC needs two anonymous meeters; excluded %s)" % (
                    ch["slot"], len(ch["rows"]), ch["rows"], ch["excluded"]))
                return
            if len(ch["branches"]) > 1:
                break
            br = ch["branches"][0]
            t0 = time.time()
            TB.apply_branch(pg, br)
            self.fresh_child()
            clip, rnd = N6.cascade(pg, self.rounds, log=self.log)
            self.n_nodes += 1
            self.record(label + "u", depth, dict(br, unit=True), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            if pg.dead:
                return
        if ens is not None:                                                        # A230: Rule NS at the WEDGE
            branches = L11.eps_branches(ens)
            self.eps_ns_splits += 1
            self.nodes[-1].update(branch_slot=ens["slot"], branch_role=ens["role"], n_branches=2,
                                  branch_rows=["meets W", "misses W"], eps_ns=ens, verdict="INTERNAL")
            self.log("   Rule NS at the WEDGE at %s: %s meets / misses the wedge of (%s, %s) -- %d target(s): %s" % (
                label, ens["role"], ens["F"], ens["slot"], ens["n_targets"], ens["wedge"][:140]))
        elif ns is not None:
            branches = N6.ns_branches(ns)
            self.ns_splits += 1
            self.nodes[-1].update(branch_slot=ns["slot"], branch_role=ns["role"], n_branches=2, branch_rows=["meets", "misses"], ns=ns, verdict="INTERNAL")
            self.log("   Rule NS at %s: split %s at %s (meeting fraction %s; alive rows %s; named %s)" % (label, ns["role"], ns["slot"], ns["frac"], ns["rows"], ns["named"]))
        elif rs is not None:
            branches = RS.branches(rs)
            self.rsplits += 1
            self.nodes[-1].update(branch_slot=rs["role"], branch_role=rs["role"], n_branches=2, branch_rows=[b["rows"][0] for b in branches],
                                  rsplit=dict(rs, m=str(rs["m"])), verdict="INTERNAL")
            self.log("   Lemma ROLE-SPLIT at %s: bisect %s on %s at %s (extents %s, tilt %s deg, core %s, %d piece(s); split %d of %d)" % (
                label, rs["role"], rs["dim"], branches[0]["m_f"], (rs["extents"]["x"], rs["extents"]["y"]), rs["extents"]["tilt"],
                "EMPTY" if rs["core_empty"] else "non-empty", rs["n_pieces"], rs["n_splits"] + 1, RS.CAP))
        else:
            if self.eff_depth(depth, label) >= self.depth_cap or self.n_nodes >= self.node_cap or pg.T.out_of_time():
                why = "depth cap" if self.eff_depth(depth, label) >= self.depth_cap else ("node cap" if self.n_nodes >= self.node_cap else "wall")
                return self.alive("undecided (%s) before branching on %s over %s" % (why, ch["slot"], [b["rows"] for b in ch["branches"]]))
            branches = ch["branches"]
            self.nodes[-1].update(branch_slot=ch["slot"], n_branches=len(branches), branch_rows=[b["rows"] for b in branches])
        st = N6.save_state(pg)
        for i, br in enumerate(branches):
            lab = "%s.%d" % (label, i + 1)
            info, _q, p = self.child_path(lab, label, br)
            if info is not None:
                self.record_inherited(lab, depth + 1, br, info, p)
                continue
            if not self.on_path(lab):
                self.undecided(lab, depth + 1, br, "undecided: skipped (not on the requested path %s)" % self.only)
                continue
            if pg.T.out_of_time() or self.n_nodes >= self.node_cap:
                self.undecided(lab, depth + 1, br, "undecided: %s before this branch ran" % ("wall" if pg.T.out_of_time() else "node cap"))
                continue
            N6.restore_state(pg, st)
            self.fresh_child()
            t0 = time.time()
            if str(br.get("kind", "")).startswith("epsns-"):       # A230: Rule NS at the wedge
                if br["kind"] == "epsns-misses":                   # DEAD at once by FC+EPS: no second meeter is left
                    pg.dead = br["leaf"]
                    self.n_nodes += 1
                    self.eps_ns_kills += 1
                    self.record(lab, depth + 1, br, "DEAD", "FC+EPS", None, t0).update(verifier=br["verifier"])
                    continue
                try:
                    L11.eps_apply(pg, br)
                except ValueError as e:                            # nothing reaches the wedge: DEAD by the clip itself
                    pg.dead = "FC+EPS (wedge clip) at %s: %s" % (label, e)
                    self.n_nodes += 1
                    self.eps_ns_kills += 1
                    self.record(lab, depth + 1, br, "DEAD", "EPS-WEDGE-EMPTY", None, t0).update(verifier=br["verifier"])
                    continue
            elif str(br.get("kind", "")).startswith("ns-"):
                N6.apply_ns(pg, br)
            elif br.get("kind") == "rsplit":
                try:
                    RS.apply_rsplit(pg, br)
                except ValueError as e:                           # the half is empty: the branch is DEAD by the split itself
                    pg.dead = "Lemma ROLE-SPLIT at %s: %s -- the role has no pose in this half, so the branch is impossible" % (label, e)
                    self.n_nodes += 1
                    self.rsplit_kills += 1
                    self.record(lab, depth + 1, br, "DEAD", "RSPLIT-EMPTY", None, t0)
                    continue
            else:
                TB.apply_branch(pg, br)
            clip, rnd = N6.cascade(pg, self.rounds, log=self.log)
            self.n_nodes += 1
            self.record(lab, depth + 1, br, "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            if not pg.dead:
                self.expand(depth + 1, lab)
        N6.restore_state(pg, st)

    def result(self):
        out = N9.Tree209.result(self)
        out.update(cc_kills=self.cc_kills, exact_rounds=self.exact_rounds, basin_kills=self.basin_kills, n_inherited=self.n_inherited,
                   rsplits=self.rsplits, rsplit_kills=self.rsplit_kills,
                   ef_runs=self.ef_runs, ef_kills=self.ef_kills, ef_timeouts=self.ef_timeouts,
                   ef_seconds=round(self.ef_seconds, 1), nr_short=self.nr_short,
                   snap_runs=self.snap_runs, snap_kills=self.snap_kills, snap_handoffs=self.snap_handoffs,
                   snap_partial=self.snap_partial, snap_cands=self.snap_cands, snap_first=self.snap_first,
                   snap_seconds=round(self.snap_seconds, 2), snap_rows=self.snap_rows[-60:],
                   eps_runs=self.eps_runs, eps_kills=self.eps_kills, eps_cands=self.eps_cands, eps_first=self.eps_first,
                   eps_ns_splits=self.eps_ns_splits, eps_ns_kills=self.eps_ns_kills,
                   eps_seconds=round(self.eps_seconds, 2), eps_rows=self.eps_rows[-60:])
        return out
