"""A203 -- the masks, the SETTLE step and the mutual clip.  Settle (the PI's "settling the mutual clip", 18:20): an
option whose compatible leaf pairs are few is REFINED locally -- each surviving (option piece, H piece) pair has the
option piece split 2 x 2 x 2 up to `depth` levels, every child re-tested by A202's rules (P, W, C, M, L; R and A161's
exact miss X for every slot of the row) and by rule S against the H piece; a pair whose children all die is dead;
an option whose pairs all die is dead (rule F); a unit that loses every pair of an option loses that option's bit."""
import time

import rules202 as R
import csp203 as C


def settle_pair(st, pc, hp, S, depth, fanout, cnt, tm):
    """True only when every pose of the option piece pc that meets every slot of S is proved non-disjoint from
    every pose of H's piece hp (or dead by A202's rules), by refinement to `depth` levels."""
    import fast30
    key = (id(pc), id(hp), S)
    v = st.settled.get(key)
    if v is not None:
        return v
    cur = [pc]
    out = False
    for d in range(depth):
        nxt = []
        for q in cur:
            for ch in fast30.split(q):
                if st.kill_base(ch, cnt, tm) is not None:
                    continue
                if any(st.kill_slot(ch, p, cnt, tm, exact=False) is not None for p in S):
                    continue                                           # R (cheap) for every slot first
                if C.sat_dead(ch[2], ch[4], hp[2], hp[4], st.sat_step):
                    cnt["S"] += 1
                    continue
                if any(st.kill_slot(ch, p, cnt, tm, exact=True) is not None for p in S):
                    continue                                           # then A161's exact miss X
                nxt.append(ch)
        cur = nxt
        if not cur:
            out = True
            break
        if len(cur) > fanout:
            break
    st.settled[key] = out
    return out


def settle(st, opts, units, masks, uidx, compat, max_pairs=400, depth=3, fanout=64, t_opt=2.0, t_all=6.0):
    """refine the near-dead options; returns (dead option keys with info, records, ms)."""
    t0 = time.perf_counter()
    dead, recs = [], []
    cnt = {k: 0 for k in "PWCMLRXS"}
    tm = {k: 0.0 for k in "PWCMLRX"}
    ukeys = sorted(units, key=lambda u: uidx[u])
    work = []
    for key, (node, S) in opts.items():
        if masks[key] == 0:
            continue
        blocks = []
        for u in ukeys:
            if not masks[key] >> uidx[u] & 1:
                continue
            for a, b in C.leaf_blocks(node, units[u]):
                k = (a.uid, b.uid) if a.uid <= b.uid else (b.uid, a.uid)
                prs = compat.pairs.get(k)
                if prs:
                    blocks.append((u, a, b, prs))
        n = sum(len(x[3]) for x in blocks)
        if 0 < n <= max_pairs:
            work.append((n, key, blocks))
    work.sort(key=lambda w: w[0])
    for n, key, blocks in work:
        if time.perf_counter() - t0 > t_all:
            break
        node, S = opts[key]
        t1 = time.perf_counter()
        lost_units, n_dead, timed_out = set(), 0, False
        per_unit = {}
        for u, a, b, prs in blocks:
            per_unit.setdefault(u, []).append((a, b, prs))
        for u, bl in per_unit.items():
            alive_here = 0
            for a, b, prs in bl:
                for i, j in prs:
                    pa, pb = (a.leaves[i], b.leaves[j]) if a.uid <= b.uid else (a.leaves[j], b.leaves[i])
                    if time.perf_counter() - t1 > t_opt:
                        timed_out = True
                        alive_here += 1
                        break
                    if settle_pair(st, pa, pb, S, depth, fanout, cnt, tm):
                        n_dead += 1
                    else:
                        alive_here += 1
                if timed_out:
                    break
            if alive_here == 0:
                lost_units.add(u)
                masks[key] &= ~(1 << uidx[u])
            if timed_out:
                break
        rec = dict(cell=key[0], S=sorted(key[1]), pairs=n, pairs_dead=n_dead, units_lost=len(lost_units), timed_out=timed_out,
                   ms=round(1000 * (time.perf_counter() - t1), 1), hull=[round(v, 5) for v in node.rect], bins=node.bins)
        recs.append(rec)
        if masks[key] == 0:
            dead.append((key, "F", dict(rec, n_pieces=len(node.leaves) if node.leaves is not None else sum(len(k.leaves or ()) for k in node.kids))))
    return dead, recs, cnt, {k: round(1000 * v, 1) for k, v in tm.items()}, 1000 * (time.perf_counter() - t0)


def mutual_clip(st, opts, units, slots_free, compat, settle_on=True):
    """opts: {key: (Node, S)}; units: {ukey: Node}; slots_free: the forced slots some FREE square must meet.
    Returns (masks, alive unit keys, dead options [(key, rule, info)], dead units {ukey: rule}, iterations, ms, uidx, settle rec)."""
    t0 = time.perf_counter()
    ukeys = sorted(units)
    uidx = {u: i for i, u in enumerate(ukeys)}
    masks = {}
    for key, (node, S) in opts.items():
        m = 0
        for u in ukeys:
            if compat.ok(node, units[u]):
                m |= 1 << uidx[u]
        masks[key] = m
    t_mask = 1000 * (time.perf_counter() - t0)
    srec = None
    dead_opts = []
    if settle_on:
        sd, recs, cnt, tms, ms = settle(st, opts, units, masks, uidx, compat)
        dead_opts += sd
        srec = dict(options=recs, kills=cnt, rule_ms=tms, ms=round(ms, 1), n_dead_options=len(sd))
    alive_u = (1 << len(ukeys)) - 1
    alive_o = set(opts) - {k for k, _, _ in dead_opts}
    dead_units = {}
    it = 0
    while True:
        it += 1
        changed = False
        for key in sorted(alive_o):
            masks[key] &= alive_u
            if masks[key] == 0:
                node, S = opts[key]
                near = min(units, key=lambda u: R.rect_maxdist2(node.rect, units[u].rect))
                info = dict(hull=[round(v, 5) for v in node.rect], bins=node.bins, nearest_unit=list(near), nearest_maxdist=C.maxdist(node, units[near]),
                            n_pieces=len(node.leaves) if node.leaves is not None else sum(len(k.leaves or ()) for k in node.kids))
                dead_opts.append((key, "H", info))
                alive_o.discard(key)
                changed = True
        for p in slots_free:
            cover = 0
            for key in alive_o:
                if p in opts[key][1]:
                    cover |= masks[key]
            lost = alive_u & ~cover
            if lost:
                for u in ukeys:
                    if lost >> uidx[u] & 1:
                        dead_units[u] = "MC:%s" % p
                alive_u &= cover
                changed = True
        if not changed:
            break
    ms = dict(masks=round(t_mask, 1), total=round(1000 * (time.perf_counter() - t0), 1))
    return masks, [u for u in ukeys if alive_u >> uidx[u] & 1], dead_opts, dead_units, it, ms, uidx, srec
