"""A202 -- A200's capped exact cover search (quick200.count_search, A198 Theorem COUNT) with a PLUGGABLE pair test:
`pair_ok(o1, o2)` must return False only with a PROOF that no two distinct interior-disjoint squares realise the two
option rows (A1 / CN / MK on the rows' hulls and alive tilt bins -- rules202); an undecided pair is compatible."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (os.path.join(ROOT, "attempts", "A198-fastprop", "code"),):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import fastprop as FP                                          # noqa: E402  READ-ONLY (A198)
import rules202 as R                                           # noqa: E402


class PairTable:
    """cached A1 + CN + MK compatibility on option rows (cell, S, chords, hull, bins)."""

    def __init__(self):
        self.cache = {}
        self.stats = dict(A1=0, CN=0, MK=0, ok=0)
        self.used = []

    def ok(self, o1, o2):
        k = (o1[0], o1[1], o2[0], o2[1]) if (o1[0], sorted(o1[1])) <= (o2[0], sorted(o2[1])) else (o2[0], o2[1], o1[0], o1[1])
        v = self.cache.get(k)
        if v is not None:
            return v
        h1, h2 = R.fr(o1[3]), R.fr(o2[3])
        why = None
        if not FP.a1_compatible(o1[3], o2[3]):
            why = "A1"
        elif R.cn_dead_pair(h1, h2):
            why = "CN"
        else:
            b1, b2 = o1[4], o2[4]
            if b1 and b2 and all(R.mk_dead(h1, x, h2, y) for x in b1 for y in b2):
                why = "MK"
        self.stats[why or "ok"] += 1
        if why and len(self.used) < 400:
            self.used.append(dict(rule=why, a=[o1[0], sorted(o1[1])], b=[o2[0], sorted(o2[1])], hull_a=h1, hull_b=h2,
                                  maxdist=round(R.rect_maxdist2(h1, h2) ** 0.5, 5)))
        self.cache[k] = (why is None)
        return why is None


def count_search(slots, free_opts, fixed_opts, n_free, lines, base_chords, s, caps, pair_ok, node_cap=200000, use_chords=True):
    names = list(fixed_opts)
    nodes = [0]
    capped = [False]
    by_slot = {p: [o for o in free_opts if p in o[1]] for p in slots}
    maxS = max([len(o[1]) for o in free_opts] or [0])

    def chords_ok(ch):
        return (not use_chords) or all(ch[L] <= s for L in lines)

    def add(ch, c):
        return {L: ch[L] + c.get(L, 0) for L in lines}

    def compat(o, chosen):
        return all(pair_ok(o, c[1]) for c in chosen)

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
            cs = [o for o in by_slot[p] if o[0] not in used and anon[p] < caps[p]
                  and all(anon[q] < caps[q] for q in o[1] if q in anon)]
            if best is None or len(cs) < len(cands):
                best, cands = p, cs
            if not cs:
                return None
        if left * maxS < tot:
            return None
        for o in cands:
            if not compat(o, chosen):
                continue
            ch2 = add(ch, o[2])
            if not chords_ok(ch2):
                continue
            d2 = dict(demand)
            a2 = dict(anon)
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
            if o[0] in used or not compat(o, chosen):
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
