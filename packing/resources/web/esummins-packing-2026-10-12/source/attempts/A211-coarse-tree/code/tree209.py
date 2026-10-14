"""A209 -- the composed tree: A207's TreePage207 (A206's Rule NS + A205's clips + A204's cascade + the basin clip when a
certified basin covers the page's window) under A206's Tree206, extended at EVERY ALIVE LEAF that carries >= 9 roles
(5 pins + H + >= 3 meeters) by A208's NO-ROOM leaf:
  * k = 10 (one free square): A189 Lemma 1 with the full budget on the roles' BOXES (cores from boxes are inside the
    cores from pieces: sound, weaker) -- DEAD by the bisection alone or by the pocket LANE sum (clip NOROOM);
  * k = 9 (two free squares): the residue's pockets (A189's cover of the open centres) and the pocket CN bound -- every
    pocket of diameter < 1 holds at most one centre (Lemma CN), so #pocket groups < 2 is DEAD (clip NOROOM-CN); otherwise
    the pockets are BRANCHED on (Lemma POCKET below): a free square distinct from every role has its centre in some
    pocket P_j (the pockets cover every centre of a free pose), so the disjunction over j is exhaustive; branch j
    instantiates that square as a role with pieces P_j x [0, 90] (a superset: sound), runs the cascade and recurses --
    the leaf reached there has k = 10.
Kills: [C: library clip trace (+ A189 Lemma 1 / Lemma CN / Lemma BASIN)] with branch / clip / round; no verifier clause.
The closed top-level branches of an A206 whole-tree run of the same page and pad (the same (slot, rows) hypothesis at
depth 1 from the same A203 start; A209's root is a subset of A206's) are inherited as DEAD, not re-run."""
import math
import os
import time
from fractions import Fraction as Fr

import poly204 as P
import tree205b as TB
import tree206 as N6
import tree206b as NB
import tree207 as N7

FP, MB = P.FP, P.MB
N7.install()
_NR = None
_N221 = None
A221 = os.environ.get("A221_LANE") == "1"       # A221: the POCKET COVER (Lemma POCKET-DEAD) in place of A189's lane


def NR():
    global _NR
    if _NR is None:
        import os
        import sys
        for d in (os.path.join(P.ROOT, "attempts", "A189-noroom", "code"), os.path.join(P.ROOT, "attempts", "A171-multibox-invariant", "code")):
            if d not in sys.path:
                sys.path.insert(0, d)
        import noroom189
        _NR = noroom189
    return _NR


def N221():
    global _N221
    if _N221 is None:
        import sys
        d = os.path.join(P.ROOT, "attempts", "A221-lane-cover", "code")
        if d not in sys.path:
            sys.path.insert(0, d)
        import noroom221
        _N221 = noroom221
    return _N221


def diam(p):
    return math.hypot(p[1] - p[0], p[3] - p[2])


def linf_gap(p, q):
    return max(max(p[0] - q[1], q[0] - p[1], 0.0), max(p[2] - q[3], q[2] - p[3], 0.0))


def cn_groups(pockets):
    """pockets grouped so that any two centres in one group are < 1 apart (l-inf, hence a group holds <= 1 centre by
    Lemma CN); -> (n_groups, ok) with ok False when some group has diameter >= 1 (the bound then says nothing)."""
    groups = []
    for p in pockets:
        for g in groups:
            if all(max(max(q[1], p[1]) - min(q[0], p[0]), max(q[3], p[3]) - min(q[2], p[2])) < 1 for q in g):
                g.append(p)
                break
        else:
            groups.append([p])
    ok = all(max(max(q[1] for q in g) - min(q[0] for q in g), max(q[3] for q in g) - min(q[2] for q in g)) < 1 for g in groups)
    return len(groups), ok


def noroom_at(pg, wall_left, log=print, deadline=None, parent_pockets=None):
    """A208's leaf on the node's role boxes; -> dict(verdict, clip, reason, k, m, pockets, cn_bound, seconds).
    A220: `deadline` (seconds) overrides the wall-derived budget, which has a 60 s FLOOR -- the short child cap of
    the A220 addendum (A220_NOROOM_CHILD_CAP) has to be able to go below it.  deadline=None is the old behaviour.
    A221 (flag A221_LANE=1): the POCKET COVER of attempts/A221-lane-cover/notes/lane221.md replaces A189's lane --
    each pocket is covered by the exact clip ROOTED AT THE POCKET (Lemma POCKET-DEAD), and `parent_pockets` (the
    nearest recorded no-room ANCESTOR's pocket list, which covers this node's free centres by Lemma POCKET-INHERIT)
    lets the child skip the container-wide bisection."""
    roles = {k: tuple(float(v) for v in b) for k, b in pg.roles.items()}
    k, m = len(roles), 11 - len(roles)
    t0 = time.time()
    bud = dict(total_deadline=max(60.0, min(900.0, wall_left - 30)) if deadline is None else float(deadline))
    if m >= 2:
        bud["max_pocket_area"] = 0.0
    try:
        if A221 and parent_pockets:
            out = N221().noroom_child(roles, parent_pockets, budget=bud, name=pg.name, n=11)
        elif A221:
            out = N221().noroom(roles, s0=None, budget=bud, name=pg.name, n=11)
        else:
            out = NR().noroom(roles, s0=None, budget=bud, name=pg.name, n=11)
    except Exception as e:                                        # noqa: BLE001
        out = dict(verdict="ERROR", reason=repr(e)[:200])
    res = dict(k=k, m=m, verdict=out.get("verdict"), clip=None, reason=str(out.get("reason"))[:300], bound=out.get("bound"), pockets=out.get("pockets") or [],
               cn_bound=None, bisect=out.get("bisect"), lanes=out.get("lanes"), seconds=round(time.time() - t0, 1))
    if res["verdict"] == "DEAD":
        res["clip"] = out.get("clip") or ("NOROOM" if out.get("leaf") != "EmptyBox (A171 pair leaf)" else "EmptyBox")
    elif res["verdict"] == "UNDECIDED" and res["pockets"]:
        n, ok = cn_groups(res["pockets"])
        if ok:
            res["cn_bound"] = n
            if n < m:
                res.update(verdict="DEAD", clip="NOROOM-CN", reason="pocket CN bound %d < %d free squares (%d pocket group(s) of diameter < 1; Lemma CN)" % (n, m, n))
    pg.T.test("NOROOM", k=k, m=m, verdict=res["verdict"], clip=res["clip"], bound=res["bound"], cn_bound=res["cn_bound"], n_pockets=len(res["pockets"]), seconds=res["seconds"])
    log("   no-room (k=%d, m=%d): %s%s in %.0f s (%d pockets; %s)" % (k, m, res["verdict"], (" by " + res["clip"]) if res["clip"] else "", res["seconds"], len(res["pockets"]), res["reason"][:80]))
    return res


def apply_pocket(pg, pocket, j):
    """the free square whose centre lies in the pocket instantiated as a role: pieces = the pocket rect x [0, 90] in 4 tilt
    sub-bins (a superset of its poses), not cell-bound (role_cell -1: the anonymous count loses one square), no slot."""
    x0, x1, y0, y1 = (Fr(v) for v in pocket)
    S = pg.s
    rect = (max(x0, Fr(1, 2)), min(x1, S - Fr(1, 2)), max(y0, Fr(1, 2)), min(y1, S - Fr(1, 2)))
    pcs = [(MB.Bin(a, b), rect) for a, b in MB.sub_bins(Fr(0), Fr(1), 4)]
    role = "F%d" % (len(pg.role_cell) + 1)
    pg.roles[role] = P.hull_box(pcs)
    pg.pieces[role] = pcs
    pg.role_cell[role] = -1
    pg.role_slots[role] = ()
    pg.T.test("POCKET-INSTANTIATE", role=role, pocket=j, rect=FP.rect_f(rect), n_pieces=len(pcs))
    return role


class Tree209(NB.Tree206):
    def __init__(self, pg, inherited=None, log=print, **kw):
        NB.Tree206.__init__(self, pg, log=log, **kw)
        self.inherited = inherited or {}          # (slot, tuple(rows)) -> dict(label, cert, run) of an A206 DEAD depth-1 branch
        self.inherit_hits = {}
        self.noroom_runs = []
        self.pocket_splits = 0
        self._ctx = []

    # ------------------------------------------------------------------ the inherited depth-1 kills
    def on_path(self, lab):
        if self.inherited and self._ctx and self._ctx[-1][1] == self.root_label and "." in lab and lab.rsplit(".", 1)[0] == self.root_label:
            R = self.root_label
            root = next((n for n in reversed(self.nodes) if n.get("branch_rows") and (n["label"] == R or (n["label"].startswith(R) and "." not in n["label"][len(R):]))), None)
            try:
                i = int(lab.rsplit(".", 1)[1]) - 1
                rows = tuple(root["branch_rows"][i])
                key = (root.get("branch_slot"), rows)
            except Exception:
                key = None
            if key in self.inherited and not root.get("branch_role"):
                self.inherit_hits[lab] = dict(self.inherited[key], slot=key[0], rows=list(rows))
                return False
        return NB.Tree206.on_path(self, lab)

    def undecided(self, label, depth, br, why):
        h = self.inherit_hits.get(label)
        if h is None:
            return NB.Tree206.undecided(self, label, depth, br, why)
        pg = self.pg
        self.nodes.append(dict(label=label, depth=depth, slot=(br or {}).get("slot"), kind="inherited", rows=(br or {}).get("rows"), named=(br or {}).get("named"),
                               verdict="DEAD", clip="A206-CLOSED", killed_round=None, reason="inherited from A206 %s branch %s (%s)" % (h.get("run"), h.get("label"), h.get("cert")),
                               leaf="the same hypothesis (%s <- %s from the same A203 start; A209's root is a subset of A206's) is DEAD in A206's whole-tree run: %s" % (h["slot"], h["rows"], str(h.get("leaf") or "")[:200]),
                               seconds=0.0, t=round(pg.T.now(), 1), n_rounds=0, snapshot=None, verifier="[C: library clip trace] inherited (A206 namedsplit206)"))
        self.dead_leaves += 1
        self.log("   node %-10s d%d %s<-%s: DEAD inherited from A206 %s %s" % (label, depth, h["slot"], h["rows"], h.get("run"), h.get("label")))
        if self.on_node:
            self.on_node(self)

    # ------------------------------------------------------------------ the no-room leaf with pocket branching
    def parent_pockets(self, label):
        """A221 Lemma POCKET-INHERIT: the pocket list of the nearest ANCESTOR (never a sibling) that recorded one.
        Every branch rule of this tree shrinks a role's pose set or adds a role, so the ancestor's pockets cover this
        node's free centres."""
        seen = {r["label"]: r for r in self.noroom_runs}
        lab = label
        while "." in lab:
            lab = lab.rsplit(".", 1)[0]
            r = seen.get(lab)
            if r and r.get("pockets"):
                return [list(map(float, p)) for p in r["pockets"]]
        return None

    def expand(self, depth, label):
        self._ctx.append((depth, label))
        try:
            return NB.Tree206.expand(self, depth, label)
        finally:
            self._ctx.pop()

    def leaf_alive(self, why):
        pg = self.pg
        depth, label = self._ctx[-1] if self._ctx else (0, self.root_label)
        fully = why.startswith("every forced slot has two named meeters")
        if len(pg.roles) < 9 or pg.T.out_of_time() or "wall" in why:
            return NB.Tree206.leaf_alive(self, why)
        res = noroom_at(pg, pg.T.left(), log=self.log, parent_pockets=self.parent_pockets(label) if A221 else None)
        rec = dict(label=label, depth=depth, k=res["k"], m=res["m"], verdict=res["verdict"], clip=res["clip"], bound=res["bound"], cn_bound=res["cn_bound"],
                   n_pockets=len(res["pockets"]), pockets=res["pockets"], seconds=res["seconds"], reason=res["reason"])
        self.noroom_runs.append(rec)
        self.nodes[-1]["noroom"] = rec
        if res["verdict"] == "DEAD":
            pg.dead = "no-room at %s (k=%d, m=%d; A189 Lemma 1%s on the role boxes): %s" % (label, res["k"], res["m"], " + Lemma CN" if res["clip"] == "NOROOM-CN" else "", res["reason"])
            self.nodes[-1].update(verdict="DEAD", clip=res["clip"], leaf=pg.dead, killed_round=len(pg.round_times), reason=None)
            self.dead_leaves += 1
            self.log("   node %-10s d%d: DEAD by %s (no-room, k=%d) %s s" % (label, depth, res["clip"], res["k"], res["seconds"]))
            if self.on_node:
                self.on_node(self)
            return
        pk = res["pockets"]
        if not (fully and res["m"] >= 2 and pk and depth < self.depth_cap and self.n_nodes < self.node_cap and not pg.T.out_of_time()):
            return NB.Tree206.leaf_alive(self, why + ("; no-room %s (k=%d, %d pockets)" % (res["verdict"], res["k"], len(pk)) if res["verdict"] != "ERROR" else "; no-room ERROR"))
        self.pocket_splits += 1
        self.nodes[-1].update(branch_slot="pocket", n_branches=len(pk), branch_rows=[[j] for j in range(len(pk))], pockets=pk, verdict="INTERNAL", reason=None)
        self.log("   Lemma POCKET at %s: %d pockets %s (k=%d, m=%d): the 10th square instantiated in each" % (label, len(pk), [[round(v, 3) for v in p] for p in pk], res["k"], res["m"]))
        st = N6.save_state(pg)
        for j, pocket in enumerate(pk):
            lab = "%s.p%d" % (label, j + 1)
            br = dict(slot="pocket", kind="pocket", rows=[j], named=None, pocket=[round(v, 6) for v in pocket], diam=round(diam(pocket), 4))
            if pg.T.out_of_time() or self.n_nodes >= self.node_cap:
                NB.Tree206.undecided(self, lab, depth + 1, br, "undecided: %s before this pocket branch ran" % ("wall" if pg.T.out_of_time() else "node cap"))
                continue
            N6.restore_state(pg, st)
            t0 = time.time()
            pg.sharpened = False
            role = apply_pocket(pg, pocket, j)
            clip, rnd = N6.cascade(pg, self.rounds, log=self.log)
            self.n_nodes += 1
            r = self.record(lab, depth + 1, br, "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            r["pocket_role"] = role
            if not pg.dead:
                self.expand(depth + 1, lab)
        N6.restore_state(pg, st)

    def result(self):
        out = NB.Tree206.result(self)
        out["pocket_splits"] = self.pocket_splits
        out["noroom_runs"] = self.noroom_runs
        out["inherited"] = {k: v for k, v in self.inherit_hits.items()}
        return out
