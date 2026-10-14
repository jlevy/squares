"""A203 (copy of A202's fast30b at d13f7420; the CSP of csp203/csp203b wired into the round, count203) -- part b: the option table, the union caps, Theorem FC, the count, the H forcing; the
certificate (live200-compatible fields: nid / verdict / pad / steps / rounds / witness / roles / tests / caps)."""
import itertools
import math
import time
from fractions import Fraction as Fr

import fastprop as FP                                          # READ-ONLY (A198)
import quick200 as Q                                           # READ-ONLY (A200)
import rules202 as R
import count203 as C3
import csp203b as CB
import cert203 as CT

INF = 99
S_RAT = FP.S_RAT


def chords_of(st, pcs):
    out = {}
    for L in st.lines:
        m = None
        for pc in pcs:
            c = (pc[5] or {}).get(L, Fr(0))
            m = c if m is None else min(m, c)
            if m <= 0:
                break
        out[L] = Fr(0) if m is None else m
    return out


def bbox(rects):
    return (min(r[0] for r in rects), max(r[1] for r in rects), min(r[2] for r in rects), max(r[3] for r in rects))


def closure(singles, inter):
    """upward closure over slot sets: S is kept only when every (|S|-1)-subset is alive and the combination is."""
    alive = {frozenset([p]): v for p, v in singles.items()}
    keys = sorted(singles)
    for k in range(2, len(keys) + 1):
        new = False
        for S in itertools.combinations(keys, k):
            S = frozenset(S)
            if all((S - {q}) in alive for q in S):
                v = inter([alive[S - {q}] for q in S])
                if v is not None:
                    alive[S] = v
                    new = True
        if not new:
            break
    return alive


def bins_inter(b1, b2):
    """the overlaps of two lists of closed degree intervals (a pose's tilt lies in one interval of each list)."""
    out = set()
    for a0, a1 in b1:
        for c0, c1 in b2:
            lo, hi = max(a0, c0), min(a1, c1)
            if lo <= hi:
                out.add((lo, hi))
    return sorted(out)


def combine(vs):
    """(hull, bins, chords) of a joint option: the hulls' intersection (a pose meeting every slot lies in each slot's
    alive set), the bins' intersection, the chords' maximum -- all sound over-approximations; None when empty."""
    h = (max(v[0][0] for v in vs), min(v[0][1] for v in vs), max(v[0][2] for v in vs), min(v[0][3] for v in vs))
    if h[1] < h[0] or h[3] < h[2]:
        return None
    b = list(vs[0][1])
    for v in vs[1:]:
        b = bins_inter(b, v[1])
        if not b:
            return None
    ch = {L: max(v[2][L] for v in vs) for L in vs[0][2]}
    return (h, sorted(b), ch)


def free_options(st):
    single = {p: {} for p in st.slots}
    by_cell = {}
    for p in st.slots:
        for pc in st.alive[p]:
            by_cell.setdefault(pc[0], {}).setdefault(p, []).append(pc)
    opts = []
    for ci in sorted(by_cell):
        singles = {}
        for p, pcs in by_cell[ci].items():
            singles[p] = (bbox([pc[2] for pc in pcs]), sorted({pc[4] for pc in pcs}), chords_of(st, pcs))
            rects = {pc[1] for pc in pcs}
            single[p][ci] = round(float(sum((r[1] - r[0]) * (r[3] - r[2]) for r in rects) / (st.side * st.side)), 4)
        for S, (h, b, ch) in closure(singles, combine).items():
            opts.append((ci, S, ch, h, b))
    return opts, single


def role_options(st, pieces, units=False):
    """pieces: [Piece] of a fixed role (H or a further H_k) -> option rows per grid cell, S = the slot sets some
    clipped piece may meet (the empty set included: the role may meet no slot)."""
    opts = []
    reach = set()
    for ci, c in enumerate(st.cells):
        cr = R.fr(c["rect"])
        crf = c["rect"]
        clipped, pidx = [], []
        for pc in pieces:
            rr, rf = pc[2], pc[1]
            x0, x1, y0, y1 = max(rr[0], cr[0]), min(rr[1], cr[1]), max(rr[2], cr[2]), min(rr[3], cr[3])
            if x1 <= x0 or y1 <= y0:
                continue
            if pc[5] is None:
                pc[5] = R.piece_chords(rf, pc[3], st.lines)                # the whole piece's chords: a lower bound for its clip
            clipped.append((pc[3], (max(rf[0], crf[0]), min(rf[1], crf[1]), max(rf[2], crf[2]), min(rf[3], crf[3])), (x0, x1, y0, y1), pc[4], len(clipped)))
            pidx.append(pc)
        if not clipped:
            continue
        singles = {p: set(k for k, c in enumerate(clipped) if R.may_meet(c[2], c[0], st.wbox[p]) and st.h_may_meet(pidx[k], p)) for p in st.slots}
        singles = {p: v for p, v in singles.items() if v}
        reach |= set(singles)
        sets = closure(singles, lambda vs: (set.intersection(*vs) or None))
        sets[frozenset()] = set(range(len(clipped)))
        for S, ks in sets.items():
            ps = [clipped[k] for k in ks]
            opts.append((ci, S, chords_of(st, [pidx[k] for k in ks]), bbox([c[2] for c in ps]), sorted({c[3] for c in ps}),
                         frozenset(CB.unit_key(st, pidx[k], st.ud) for k in ks) if units else frozenset()))
    return opts, reach


def propagate(st, rnd):
    t0 = time.time()
    free_opts, single = free_options(st)
    fixed_opts, roles_reach = {}, {}
    fixed_opts[st.H], roles_reach[st.H] = role_options(st, st.hpieces, units=True)
    for k, v in st.other_h.items():
        ta, tb = FP.MB.t_lo(v[4]), FP.MB.t_hi(v[5])
        import fast30
        fixed_opts[k], roles_reach[k] = role_options(st, [fast30.mkpiece(-1, tuple(Fr(x) for x in v[:4]), fast30.mkbin(ta, tb))])
    st.T.step("options", time.time() - t0, round=rnd, n_free_opts=len(free_opts), n_fixed={r: len(v) for r, v in fixed_opts.items()},
              alive_cells={p: len(v) for p, v in single.items()})
    n_h0 = len(st.hpieces)
    free_opts, cmask, uidx, trees, csp_rec, alive_u = CB.run_csp(st, free_opts, roles_reach, ud=st.ud, step=st.sat_step)
    csp_rec["round"] = rnd
    st.csp.append(csp_rec)
    csp_changed = bool(csp_rec["dead_opts"]) or len(st.hpieces) != n_h0
    if csp_rec["dead_opts"]:
        _, single = free_options(st)                                           # the singleton kills changed the alive cells
    if not st.hpieces:
        st.verdict_leaf = "H-CONSISTENCY: no piece of H is compatible with any option of a forced slot (mutual clip %s; %d units, %d options)" % (
            csp_rec["dead_unit_count"], csp_rec["n_units"], csp_rec["n_opts"])
        st.T.test("CSP", verdict="DEAD", **{k: csp_rec[k] for k in ("dead_unit_count", "n_units", "n_opts", "ms")})
        info = dict(round=rnd, single=single, dead=st.verdict_leaf, csp=csp_rec)
        return info
    alive_bits = 0
    for u in alive_u:
        alive_bits |= 1 << uidx[u]
    row_mask = {}
    for o in fixed_opts[st.H]:
        m = 0
        for u in o[5]:
            if u in uidx:
                m |= 1 << uidx[u]
        row_mask[(o[0], o[1])] = m & alive_bits
    fixed_opts[st.H] = [o for o in fixed_opts[st.H] if row_mask[(o[0], o[1])]]
    roles_reach[st.H] = {p for o in fixed_opts[st.H] for p in o[1]}
    info = dict(round=rnd, single=single, n_free_opts=len(free_opts), H_reach=sorted(roles_reach[st.H]), csp=csp_rec,
                fixed={r: [(o[0], sorted(o[1])) for o in v] for r, v in fixed_opts.items()},
                free_opts=[(o[0], sorted(o[1]), list(o[3])) for o in free_opts])
    t0 = time.time()
    caps, urec = CT.union_caps(st, single)
    info["union"], info["caps"] = urec, {p: (None if c >= INF else c) for p, c in caps.items()}
    st.T.step("union", time.time() - t0, caps=info["caps"])
    st.caps_last = caps
    forced_H = set()
    for p in st.slots:
        H_p = p in roles_reach[st.H]
        R_p = [r for r in roles_reach if r != st.H and p in roles_reach[r]]
        avail = (1 if H_p else 0) + len(R_p) + caps[p]
        rec = dict(slot=p, H=H_p, roles=R_p, cap=info["caps"][p])
        if avail < 2:
            st.verdict_leaf = "FC at %s: at most %d distinct non-pin meeter(s) (H %s; anonymous cap %d by %s)" % (
                p, avail, "reaches" if H_p else "provably misses", caps[p], urec[p]["why"])
            st.T.test("FC-AVAIL", verdict="DEAD", avail=avail, **rec)
            info["dead"] = st.verdict_leaf
            return info
        if avail == 2 and H_p:
            forced_H.add(p)
            st.T.test("FC-AVAIL", verdict="H forced", avail=2, **rec)
    pair = C3.PieceTable(trees, st.compat)
    n_free = st.n_free
    cs = lambda fo, use: C3.count_search(st.slots, free_opts, fo, n_free, st.lines, st.pin_chords, S_RAT, caps, pair.ok, st.H, row_mask, cmask, use_chords=use)
    for tag, use in (("count_nochord", False), ("count_chord", True)):
        t0 = time.time()
        r = cs(fixed_opts, use)
        info[tag] = dict(feasible=r.feasible, nodes=r.nodes, capped=r.capped, prunes=r.prunes)
        st.T.step("count", time.time() - t0, chords=use, feasible=r.feasible, nodes=r.nodes, capped=r.capped, pairs=dict(pair.stats), prunes=r.prunes)
        if not r.feasible:
            st.verdict_leaf = "ASSIGNMENT COUNT%s with the H-consistency mask and piece-compatible pairs (caps %s; prunes %s; pair table A1/S %s): no cover of the %d forced slots by H + %d free squares" % (
                " + CHORD ROWS" if use else "", info["caps"], r.prunes, pair.stats, len(st.slots), n_free)
            st.T.test("COUNT", chords=use, verdict="DEAD", nodes=r.nodes, n_free_opts=len(free_opts), prunes=r.prunes, pair_excl=pair.used[:60])
            info["dead"] = st.verdict_leaf
            info["pair_excl"] = pair.used[:60]
            return info
        st.witness = r.witness
    info["witness"] = [(who, o[0], sorted(o[1])) for who, o in (st.witness or [])]
    info["pair_stats"] = dict(pair.stats)
    for p in st.slots:
        if p in forced_H or p not in roles_reach[st.H]:
            continue
        fo = dict(fixed_opts)
        fo[st.H] = [o for o in fixed_opts[st.H] if p not in o[1]]
        t0 = time.time()
        rr = cs(fo, False)
        if rr.feasible:
            rr = cs(fo, True)
        st.T.step("count-barH", time.time() - t0, slot=p, feasible=rr.feasible, nodes=rr.nodes, capped=rr.capped)
        if not rr.feasible:
            forced_H.add(p)
            st.T.test("COUNT", barH=p, verdict="H forced at %s" % p, nodes=rr.nodes)
    info["forced_H"] = sorted(forced_H)
    changed = False
    if forced_H - st.forced_H:
        st.forced_H |= forced_H
        before = st.h_hull()
        st.clip_H(forced=st.forced_H)
        after = st.h_hull()
        if after is None:
            st.verdict_leaf = "H forced at %s but no piece of its box may meet them all (closed-form meet test)" % sorted(st.forced_H)
            st.T.test("H-JOINT", slots=sorted(st.forced_H), verdict="DEAD")
            info["dead"] = st.verdict_leaf
            return info
        st.T.test("H-CLIP", slots=sorted(st.forced_H), box_before=FP.rect_f(before), box_after=FP.rect_f(after))
        info["H_box"] = FP.rect_f(after)
        changed = after != before
    info["changed"] = changed or csp_changed
    return info


