"""A209 COPY of A206 tree206b (df5aebc9, unchanged). A206 -- the tree with Rule NS: A205's Tree (tree205b, the copy) with the NS split at the fully named stop.  expand() is
A205's, extended in two places: (i) at the stop (candidates() is None) the SOFT-named pairs are split BEFORE the sharp
round -- [r meets p] / [r misses p], each a node with A204's cascade; (ii) the node state carries `miss`.  DEAD iff
every branch DEAD; undecided = ALIVE; every kill [C: library clip trace] with branch / clip / round."""
import time

import tree205b as TB
import tree206 as N6


class Tree206(TB.Tree):
    def __init__(self, pg, rounds=3, depth_cap=6, node_cap=200, on_node=None, log=print, root_label="R", only=None):
        TB.Tree.__init__(self, pg, rounds=rounds, depth_cap=depth_cap, node_cap=node_cap, on_node=on_node, log=log)
        self.root_label = root_label
        self.ns_splits = 0
        self.only = only                # run only the branches on the path to / under this label (the others recorded as skipped)

    def snap(self, pg, cap=1500):
        return TB.Tree.snap(self, pg, cap=cap)

    def on_path(self, lab):
        return self.only is None or lab == self.only or self.only.startswith(lab + ".") or lab.startswith(self.only + ".") or lab.startswith(self.only + "u") or lab.startswith(self.only + "s")

    def record(self, label, depth, br, verdict, clip, rnd, t0, reason=None):
        cb, self.on_node = self.on_node, None                       # the NS fields go in BEFORE the certificate is saved
        r = TB.Tree.record(self, label, depth, br, verdict, clip, rnd, t0, reason=reason)
        self.on_node = cb
        r["miss"] = {k: sorted(v) for k, v in self.pg.miss.items()}
        r["miss_rep"] = list(self.pg.miss_rep)[-6:]
        if br and str(br.get("kind", "")).startswith("ns-"):
            r.update(role=br.get("role"), frac=br.get("frac"), alive_rows=br.get("alive_rows"))
        if self.on_node:
            self.on_node(self)
        return r

    def run(self):
        pg = self.pg
        t0 = time.time()
        clip, rnd = N6.cascade(pg, self.rounds, log=self.log)
        self.n_nodes = 1
        if pg.dead:
            self.record(self.root_label, 0, None, "DEAD", clip, rnd, t0)
            return self.result()
        self.record(self.root_label, 0, None, "INTERNAL", None, None, t0)
        self.expand(0, self.root_label)
        return self.result()

    def leaf_alive(self, why):
        self.nodes[-1].update(verdict="ALIVE", reason=why)
        self.alive_leaves += 1

    def expand(self, depth, label):
        pg = self.pg
        ns = None
        while True:
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
                return self.leaf_alive("undecided: the option table stayed stale after 4 refresh rounds")
            if ch is None:
                cands = N6.ns_candidates(pg)
                self.nodes[-1]["ns_candidates"] = cands
                if cands and not (depth >= self.depth_cap or self.n_nodes >= self.node_cap or pg.T.out_of_time()):
                    ns = cands[0]
                    break
                if cands:
                    why = "depth cap" if depth >= self.depth_cap else ("node cap" if self.n_nodes >= self.node_cap else "wall")
                    return self.leaf_alive("undecided (%s) before Rule NS on %s at %s (frac %s)" % (why, cands[0]["role"], cands[0]["slot"], cands[0]["frac"]))
                if TB.SHARP and not getattr(pg, "sharpened", False):
                    t0 = time.time()
                    pg.refine_mb, pg.nsub_mb, pg.sharpened = 3, 8, True
                    clip, rnd = N6.cascade(pg, 1, log=self.log)
                    pg.refine_mb, pg.nsub_mb = 2, 4
                    self.n_nodes += 1
                    self.record(label + "s", depth, dict(slot=None, kind="sharp", rows=None, named=None), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
                    if pg.dead:
                        return
                    continue
                soft = [c for c in N6.ns_candidates(pg)]
                return self.leaf_alive("every forced slot has two named meeters, %s (next lever: LP on the node)" % (
                    ("the soft names all at fraction >= %s: %s -- not split" % (N6.MAX_FRAC, [(c["role"], c["slot"], c["frac"]) for c in soft][:4])) if soft else "every name HARD (no soft name left to split)"))
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
            TB.apply_branch(pg, br)
            clip, rnd = N6.cascade(pg, self.rounds, log=self.log)
            self.n_nodes += 1
            self.record(label + "u", depth, dict(br, unit=True), "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            if pg.dead:
                return
        if ns is not None:
            branches = N6.ns_branches(ns)
            self.ns_splits += 1
            self.nodes[-1].update(branch_slot=ns["slot"], branch_role=ns["role"], n_branches=2, branch_rows=["meets", "misses"], ns=ns)
            self.log("   Rule NS at %s: split %s at %s (meeting fraction %s; alive rows %s; named %s)" % (label, ns["role"], ns["slot"], ns["frac"], ns["rows"], ns["named"]))
        else:
            if depth >= self.depth_cap or self.n_nodes >= self.node_cap or pg.T.out_of_time():
                why = "depth cap" if depth >= self.depth_cap else ("node cap" if self.n_nodes >= self.node_cap else "wall")
                return self.leaf_alive("undecided (%s) before branching on %s over %s" % (why, ch["slot"], [b["rows"] for b in ch["branches"]]))
            branches = ch["branches"]
            self.nodes[-1].update(branch_slot=ch["slot"], n_branches=len(branches), branch_rows=[b["rows"] for b in branches])
        st = N6.save_state(pg)
        for i, br in enumerate(branches):
            lab = "%s.%d" % (label, i + 1)
            if not self.on_path(lab):
                self.undecided(lab, depth + 1, br, "undecided: skipped (not on the requested path %s)" % self.only)
                continue
            if pg.T.out_of_time() or self.n_nodes >= self.node_cap:
                self.undecided(lab, depth + 1, br, "undecided: %s before this branch ran" % ("wall" if pg.T.out_of_time() else "node cap"))
                continue
            N6.restore_state(pg, st)
            t0 = time.time()
            pg.sharpened = False
            if str(br.get("kind", "")).startswith("ns-"):
                N6.apply_ns(pg, br)
            else:
                TB.apply_branch(pg, br)
            clip, rnd = N6.cascade(pg, self.rounds, log=self.log)
            self.n_nodes += 1
            self.record(lab, depth + 1, br, "DEAD" if pg.dead else "INTERNAL", clip, rnd, t0)
            if not pg.dead:
                self.expand(depth + 1, lab)
        N6.restore_state(pg, st)

    def result(self):
        out = TB.Tree.result(self)
        out["ns_splits"] = self.ns_splits
        out["killing"] = [dict(k, kind=n.get("kind"), role=n.get("role")) for k, n in zip(out["killing"], [n for n in self.nodes if n["verdict"] == "DEAD"])]
        return out
