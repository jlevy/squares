"""A205 -- the CLIP TREE's node: A204's PolyPage (copied poly204 / poly204b) extended with

  * the seeded reach that returns EMPTY without recomputation when the ancestor's reach was empty (K' only grows and
    obstacles are only added down the tree, so the ancestor's survivors are a superset: sound);
  * the rule-S clip between roles (A203 Lemma PC on the pieces): H, every instantiated meeter and the branch's
    instantiated rows all exist in the packing and are pairwise interior-disjoint, so a piece of A with no rule-S-
    compatible piece of B (B coarsened to per-tilt-bin hulls: a superset, sound) holds no pose of A -- dropped;
  * Lemma HC on the option rows (A203's H-mask at the node's resolution): a free row whose coarsened pieces are all
    rule-S-dead against H's (or an instantiated role's) coarsened pieces is dead, with every superset row at its cell;
  * the count with A203's pair table: two chosen rows must be rule-S compatible on their pieces (Lemma A1 on the hulls
    kept), never over cell hulls alone;
  * save / restore of the node state for the depth-first tree (tree205b).
Every kill is [C: library clip trace] (no verifier clause; the certificate is the trace).
"""
import os
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "attempts", "A203-csp-consistency", "code"))
import poly204 as P                                            # noqa: E402  (the A204 copy in this directory)
import csp203 as CS                                            # noqa: E402  READ-ONLY (A203): sat_dead = rule S

FP, MB, QP, INF = P.FP, P.MB, P.QP, P.QP.INF


def pdeg(b, r):
    """a piece (Bin, rect) as rule S wants it: float rect, tilt bin in degrees."""
    return ((float(r[0]), float(r[1]), float(r[2]), float(r[3])), (MB.deg_of_t(b.t0), MB.deg_of_t(b.t1)))


def coarse(pcs, nbins=8):
    """<= nbins per-tilt-bin hulls of a piece list (a superset: sound), in rule-S form."""
    return [pdeg(b, r) for b, r in P.coarsen(pcs, nbins=nbins, keep_if=nbins)]


def s_compatible(A, B):
    """rule S over two coarse piece lists: False only when EVERY pair is dead (no interior-disjoint pose pair)."""
    for (ra, ba) in A:
        for (rb, bb) in B:
            if not CS.sat_dead(ra, ba, rb, bb):
                return True
    return False


class TreePage(P.PolyPage):
    def __init__(self, *a, **kw):
        P.PolyPage.__init__(self, *a, **kw)
        self.cell_role = {}
        self.row_pieces = {}
        self.pair_cache = {}
        self.sclip_rep = []
        self.hc_dead = []
        self.prev_obst = {}

    # ------------------------------------------------------------------ the seeded reach with the empty short-cut
    def reach(self, ci, S):
        """A198's cell reach: from scratch when no ancestor computed it; EMPTY when the ancestor's was empty; otherwise the
        ancestor's survivors re-clipped IN PLACE against the obstacles that CHANGED since (a K' grown by a clip, a new
        role) plus the exact miss test on the shrunken pieces -- unchanged obstacles, the lonely test and the container
        clip were already applied to every seed piece (skipping a clip only keeps more: sound)."""
        key = (ci, S)
        if key in self.reach_cache:
            return self.reach_cache[key]
        prev = self.prev_reach.get(key)
        if prev is None:
            return P.PolyPage.reach(self, ci, S)
        if not prev[1]:
            self.reach_cache[key] = (0.0, [], 0)
            return self.reach_cache[key]
        po = self.prev_obst or {}
        changed = [ob for k, ob in self.obst.items() if ob is not None and (k not in po or po[k] is None or po[k].verts != ob.verts)]
        if not changed:
            self.reach_cache[key] = prev
            self.n_reach_skip = getattr(self, "n_reach_skip", 0) + 1
            return prev
        t0 = time.time()
        res = FP.bisect_region(None, changed, [self.item[p]["wb"] for p in S], self.s, self.nd.stats, depth=0, corner=None,
                               seed_pieces=prev[1], max_pieces=512)
        self.T.test("REACH", cell=ci, slots=sorted(S), seeded=True, n_changed_obst=len(changed), frac=round(res[0], 6), n_pieces=len(res[1]),
                    n_exact=res[2], seconds=round(time.time() - t0, 3))
        self.reach_cache[key] = res
        return res

    # ------------------------------------------------------------------ the rule-S clip between the roles
    def sclip(self):
        names = [k for k in self.nd.names if not k.startswith("P")]
        dropped = {}
        for a in names:
            for b in names:
                if a == b:
                    continue
                Bc = coarse(self.nd.boxes[b].pieces)
                keep = []
                for (bn, r) in self.nd.boxes[a].pieces:
                    ra, ba = pdeg(bn, r)
                    if any(not CS.sat_dead(ra, ba, rb, bb) for rb, bb in Bc):
                        keep.append((bn, r))
                n = len(self.nd.boxes[a].pieces) - len(keep)
                if n:
                    dropped[a] = dropped.get(a, 0) + n
                    self.nd.boxes[a].pieces = keep
                    if not keep:
                        return dropped, a
        return dropped, None

    def normalise(self, label):
        """A204's seeded polygon + lonely clip fixed point, then the rule-S clip; re-run while the S clip moves (<= 3)."""
        old_obst = dict(getattr(self, "obst", None) or {})
        nd = P.PolyPage.normalise(self, label)
        pr = self.prev_reach
        self.prev_obst = old_obst
        for it in range(3):
            if nd is None:
                return None
            t0 = time.time()
            dropped, empty = self.sclip()
            if empty is not None:
                self.T.step("sclip", time.time() - t0, label=label, dead=empty, dropped=dropped)
                self.T.test("S-CLIP", role=empty, label=label, verdict="DEAD", dropped=dropped)
                self.dead = "S-CLIP(%s) at %s: every piece of %s is rule-S-dead against another role's pieces (Lemma PC; no interior-disjoint pose pair)" % (empty, label, empty)
                self.fix_rep = dict(dead=empty, detail="sclip", seconds=round(time.time() - t0, 1))
                return None
            self.T.step("sclip", time.time() - t0, label=label, dropped=dropped)
            for k, mb in self.nd.boxes.items():
                self.pieces[k] = list(mb.pieces)
            big = any(n >= 0.05 * (len(self.nd.boxes[k].pieces) + n) for k, n in dropped.items())
            if not dropped or it >= 1 or not big:
                if dropped:
                    self.sclip_rep.append(dict(label=label, it=it + 1, dropped=dropped, renorm=False))
                    for k, mb in self.nd.boxes.items():
                        mb.rebuild()
                    self.obst = {k: mb.obstacle("poly") for k, mb in self.nd.boxes.items()}
                break
            self.sclip_rep.append(dict(label=label, it=it + 1, dropped=dropped, renorm=True))
            nd = P.PolyPage.normalise(self, label + "s%d" % (it + 1))
            self.prev_reach, self.prev_obst = pr, old_obst
            self.norm_shrunk = True
        return nd

    # ------------------------------------------------------------------ Lemma HC on the rows + the pieces per row
    def build_options(self):
        free_opts, fixed_opts, single = P.PolyPage.build_options(self)
        t0 = time.time()
        roles_c = {k: coarse(self.nd.boxes[k].pieces) for k in self.nd.names if not k.startswith("P")}
        self.row_pieces = {}
        dead_cells = set()
        kept = []
        for o in free_opts:
            ci, S = o[0], o[1]
            pcs = coarse(self.reach(ci, S)[1])
            self.row_pieces[("free", ci, S)] = pcs
            bad = [k for k, Bc in roles_c.items() if not s_compatible(pcs, Bc)]
            if bad:
                self.hc_dead.append(dict(cell=ci, slots=sorted(S), against=bad))
                if len(S) == 1:
                    dead_cells.add((ci, next(iter(S))))
                continue
            kept.append(o)
        free_opts = [o for o in kept if not any((o[0], p) in dead_cells for p in o[1])]
        for ci, p in dead_cells:
            single[p].pop(ci, None)
        for role, opts in fixed_opts.items():
            for o in opts:
                self.row_pieces[(role, o[0], o[1])] = coarse(self.role_pieces_in_cell(role, o[1], o[0]))
        self.T.step("hc-rows", time.time() - t0, n_dead=len(dead_cells), n_free_opts=len(free_opts), alive_cells={p: len(v) for p, v in single.items()})
        self.last_opts = (free_opts, fixed_opts, single)
        return free_opts, fixed_opts, single

    def pair_ok(self, n1, o1, n2, o2):
        """Lemma A1 on the hulls, then rule S on the rows' coarse pieces (cached)."""
        if not FP.a1_compatible(o1[3], o2[3]):
            return False
        k1, k2 = (n1, o1[0], o1[1]), (n2, o2[0], o2[1])
        key = (k1, k2) if k1 <= k2 else (k2, k1)
        v = self.pair_cache.get(key)
        if v is None:
            A, B = self.row_pieces.get(k1), self.row_pieces.get(k2)
            v = True if (A is None or B is None) else s_compatible(A, B)
            self.pair_cache[key] = v
        return v

    def count_search(self, *a, **kw):
        return count_search(self, *a, **kw)


# ----------------------------------------------------------------------------- the count with the pair table
def count_search(pg, slots, free_opts, fixed_opts, n_free, lines, base_chords, s, caps, node_cap=200000, use_chords=True):
    """A200's capped exact cover search with A203's pair rule: chosen rows pairwise compatible on their pieces."""
    names = list(fixed_opts)
    nodes, capped = [0], [False]
    by_slot = {p: [o for o in free_opts if p in o[1]] for p in slots}

    def chords_ok(ch):
        return (not use_chords) or all(ch[L] <= s for L in lines)

    def add(ch, c):
        return {L: ch[L] + c[L] for L in lines}

    def compat(name, o, chosen):
        return all(pg.pair_ok(name, o, c[0], c[1]) for c in chosen)

    def rec_free(demand, used, ch, left, chosen, anon):
        nodes[0] += 1
        if nodes[0] > node_cap:
            capped[0] = True
            return None
        need = [p for p in slots if demand[p] > 0]
        if not need:
            return list(chosen)
        if left == 0:
            return None
        tot = sum(demand[p] for p in need)
        best, cands = None, None
        for p in need:
            cs = [o for o in by_slot[p] if o[0] not in used and anon[p] < caps[p] and all(anon[q] < caps[q] for q in o[1] if q in anon)]
            if best is None or len(cs) < len(cands):
                best, cands = p, cs
            if not cs:
                return None
        maxS = max(len(o[1]) for o in free_opts) if free_opts else 0
        if left * maxS < tot:
            return None
        for o in cands:
            if not compat("free", o, chosen):
                continue
            ch2 = add(ch, o[2])
            if not chords_ok(ch2):
                continue
            d2, a2 = dict(demand), dict(anon)
            for q in o[1]:
                if q in d2:
                    d2[q] -= 1
                    a2[q] += 1
            r = rec_free(d2, used | {o[0]}, ch2, left - 1, chosen + [("free", o)], a2)
            if r is not None:
                return r
            if capped[0]:
                return None
        return None

    def rec_fixed(k, demand, used, ch, chosen):
        if k == len(names):
            return rec_free(demand, used, ch, n_free, chosen, {p: 0 for p in slots})
        for o in fixed_opts[names[k]]:
            if o[0] in used or not compat(names[k], o, chosen):
                continue
            ch2 = add(ch, o[2])
            if not chords_ok(ch2):
                continue
            d2 = dict(demand)
            for q in o[1]:
                if q in d2:
                    d2[q] -= 1
            r = rec_fixed(k + 1, d2, used | {o[0]}, ch2, chosen + [(names[k], o)])
            if r is not None:
                return r
            if capped[0]:
                return None
        return None

    w = rec_fixed(0, {p: 2 for p in slots}, frozenset(), dict(base_chords), [])
    return FP.CountResult(w is not None or capped[0], w, nodes[0], capped[0])


# ----------------------------------------------------------------------------- node state for the depth-first tree
STATE = ("roles", "pieces", "forced_H", "role_slots", "role_cell", "cell_role", "role_corner", "reach_cache", "prev_reach",
         "vol_record", "rounds", "witness", "caps_last", "union_last", "nd", "obst", "fix_rep", "dead", "norm_shrunk",
         "snapshots", "round_times", "row_pieces", "pair_cache", "prev_obst")


def save_state(pg):
    st = {}
    for k in STATE:
        v = getattr(pg, k, None)
        if isinstance(v, dict):
            v = {a: (list(b) if isinstance(b, list) else b) for a, b in v.items()}
        elif isinstance(v, (list, set)):
            v = type(v)(v)
        st[k] = v
    return st


def restore_state(pg, st):
    for k in STATE:
        v = st[k]
        if isinstance(v, dict):
            v = {a: (list(b) if isinstance(b, list) else b) for a, b in v.items()}
        elif isinstance(v, (list, set)):
            v = type(v)(v)
        setattr(pg, k, v)
