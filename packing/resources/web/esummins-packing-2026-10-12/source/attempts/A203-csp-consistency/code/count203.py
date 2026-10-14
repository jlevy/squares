"""A203 -- A202's capped exact cover search (count202 / A198 Theorem COUNT) carrying the H-CONSISTENCY bitmask:
the chosen H row starts the mask (its units), every chosen free option ANDs its compatibility mask (csp203b), an
empty mask prunes; chosen options must be pairwise PIECE-compatible (csp203.Compat on the rows' piece trees,
forward checking).  Sound direction only: a pair or an (option, unit) is excluded only by rule S at every leaf pair."""
import fastprop as FP                                          # READ-ONLY (A198)
import rules202 as R
import csp203 as C


class PieceTable:
    """pairwise compatibility of option rows on their PIECE trees (free rows), the hull x bins for fixed rows."""

    def __init__(self, trees, compat):
        self.trees, self.compat = trees, compat
        self.cache, self.leaf = {}, {}
        self.stats = dict(A1=0, S=0, ok=0)
        self.used = []

    def node(self, o):
        k = (o[0], o[1])
        n = self.trees.get(k)
        if n is None:
            n = self.leaf.get(k)
            if n is None:
                n = self.leaf[k] = C.Node(R.fr(o[3]), [tuple(b) for b in o[4]] or [(0.0, 90.0)])
        return n

    def ok(self, o1, o2):
        k = (o1[0], o1[1], o2[0], o2[1]) if (o1[0], sorted(o1[1])) <= (o2[0], sorted(o2[1])) else (o2[0], o2[1], o1[0], o1[1])
        v = self.cache.get(k)
        if v is not None:
            return v
        why = None
        if not FP.a1_compatible(o1[3], o2[3]):
            why = "A1"
        elif not self.compat.ok(self.node(o1), self.node(o2)):
            why = "S"
        self.stats[why or "ok"] += 1
        if why and len(self.used) < 400:
            n1, n2 = self.node(o1), self.node(o2)
            self.used.append(dict(rule=why, a=[o1[0], sorted(o1[1])], b=[o2[0], sorted(o2[1])], hull_a=list(n1.rect), hull_b=list(n2.rect),
                                  maxdist=C.maxdist(n1, n2), pieces=[len(n1.kids) or 1, len(n2.kids) or 1]))
        self.cache[k] = (why is None)
        return why is None


def count_search(slots, free_opts, fixed_opts, n_free, lines, base_chords, s, caps, pair_ok, hname, row_mask, cmask,
                 node_cap=200000, use_chords=True):
    names = list(fixed_opts)
    nodes = [0]
    capped = [False]
    prunes = dict(mask=0, pair=0, chord=0)
    by_slot = {p: [o for o in free_opts if p in o[1]] for p in slots}
    maxS = max([len(o[1]) for o in free_opts] or [0])

    def chords_ok(ch):
        return (not use_chords) or all(ch[L] <= s for L in lines)

    def add(ch, c):
        return {L: ch[L] + c.get(L, 0) for L in lines}

    def compat(o, chosen):
        return all(pair_ok(o, c[1]) for c in chosen)

    def rec_free(demand, used, ch, left, chosen, anon, hm):
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
            cs = [o for o in by_slot[p] if o[0] not in used and anon[p] < caps[p]
                  and all(anon[q] < caps[q] for q in o[1] if q in anon)]
            if best is None or len(cs) < len(cands):
                best, cands = p, cs
            if not cs:
                return None
        if left * maxS < tot:
            return None
        for o in cands:
            hm2 = hm & cmask.get((o[0], o[1]), -1)
            if hm2 == 0:
                prunes["mask"] += 1
                continue
            if not compat(o, chosen):
                prunes["pair"] += 1
                continue
            ch2 = add(ch, o[2])
            if not chords_ok(ch2):
                prunes["chord"] += 1
                continue
            d2 = dict(demand)
            a2 = dict(anon)
            for q in o[1]:
                if q in d2:
                    d2[q] -= 1
                    a2[q] += 1
            r = rec_free(d2, used | {o[0]}, ch2, left - 1, chosen + [("free", o)], a2, hm2)
            if r is not None:
                return r
            if capped[0]:
                return None
        return None

    def rec_fixed(k, demand, used, ch, chosen, hm):
        if k == len(names):
            return rec_free(demand, used, ch, n_free, chosen, {p: 0 for p in slots}, hm)
        for o in fixed_opts[names[k]]:
            if o[0] in used or not compat(o, chosen):
                continue
            hm2 = hm
            if names[k] == hname:
                hm2 = row_mask.get((o[0], o[1]), 0)
                if hm2 == 0:
                    prunes["mask"] += 1
                    continue
            ch2 = add(ch, o[2])
            if not chords_ok(ch2):
                continue
            d2 = dict(demand)
            for q in o[1]:
                if q in d2:
                    d2[q] -= 1
            r = rec_fixed(k + 1, d2, used | {o[0]}, ch2, chosen + [(names[k], o)], hm2)
            if r is not None:
                return r
            if capped[0]:
                return None
        return None

    w = rec_fixed(0, {p: 2 for p in slots}, frozenset(), dict(base_chords), [], -1)
    res = FP.CountResult(w is not None or capped[0], w, nodes[0], capped[0])
    res.prunes = prunes
    return res
