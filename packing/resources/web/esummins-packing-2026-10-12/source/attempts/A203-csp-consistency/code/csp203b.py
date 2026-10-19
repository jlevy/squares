"""A203 -- wiring the CSP (csp203) into the fast30 round: H's UNITS (its pieces at depth `ud`, each holding its
alive fine pieces), the option rows' PIECE sets (the dyadic intersection over the row's slots of the surviving
pieces of the cell: a pose meeting every slot of S lies in a surviving piece of each), the masks, the mutual clip,
the kills fed back (singleton rows -> the slot's pieces; H units -> H's pieces), the record for the certificate."""
import math
import time
from fractions import Fraction as Fr

import rules202 as R
import csp203 as C
import csp203c as CC


def piece_addr(st, pc):
    """dyadic address (ci, si, cb, depth, ix, iy, ib) of a free piece from its geometry (midpoints: robust); cached per piece."""
    a = st.addr_cache.get(id(pc))
    if a is None:
        a = st.addr_cache[id(pc)] = _piece_addr(st, pc)
    return a


def _piece_addr(st, pc):
    ci, rf, bn = pc[0], pc[1], pc[3]
    c = st.cells[ci]["rect"]
    w = (c[1] - c[0]) / st.nsub
    xm, ym = (rf[0] + rf[1]) / 2, (rf[2] + rf[3]) / 2
    i, j = int((xm - c[0]) / w), int((ym - c[2]) / w)
    ratio = w / (rf[1] - rf[0])
    depth = max(0, int(round(math.log2(float(ratio)))))
    wd = w / (1 << depth)
    ix, iy = int((xm - c[0] - i * w) / wd), int((ym - c[2] - j * w) / wd)
    tm = (bn.t0 + bn.t1) / 2
    cb = int(tm * st.nbins)
    ib = int((tm - Fr(cb, st.nbins)) * st.nbins * (1 << depth))
    return (ci, i * st.nsub + j, cb, depth, ix, iy, ib)


def ancestor(a, d):
    sh = a[3] - d
    return (a[0], a[1], a[2], d, a[4] >> sh, a[5] >> sh, a[6] >> sh)


def inter_pieces(A, B):
    """the pieces common to two dyadic piece lists (each a list of (addr, Piece)): a of A is kept when B holds an
    ancestor-or-self of it, else B's descendants of a are kept."""
    bset = {a for a, _ in B}
    bpref = {}
    for a, pc in B:
        for d in range(a[3]):
            bpref.setdefault(ancestor(a, d), []).append((a, pc))
    out = []
    for a, pc in A:
        if any(ancestor(a, d) in bset for d in range(a[3] + 1)):
            out.append((a, pc))
        else:
            out.extend(bpref.get(a, ()))
    return out


def opt_pieces(st, ci, S, by_cell_slot):
    ps = sorted(S, key=lambda p: len(by_cell_slot.get((ci, p), ())))
    cur = by_cell_slot.get((ci, ps[0]), [])
    for p in ps[1:]:
        cur = inter_pieces(cur, by_cell_slot.get((ci, p), []))
        if not cur:
            break
    return [pc for _, pc in cur]


def opt_node(st, pieces, tag):
    """option tree: hull -> coarse groups (sub-rect x coarse bin) -> fine pieces."""
    groups = {}
    for pc in pieces:
        a = piece_addr(st, pc)
        groups.setdefault(a[:3], []).append(pc)
    kids = [C.node_of(v, tag=k) for k, v in groups.items()]
    if len(kids) == 1:
        return C.Node(kids[0].rect, kids[0].bins, (), tag, leaves=kids[0].leaves)
    rect = (min(k.rect[0] for k in kids), max(k.rect[1] for k in kids), min(k.rect[2] for k in kids), max(k.rect[3] for k in kids))
    return C.Node(rect, C.merge_bins([b for k in kids for b in k.bins]), kids, tag)


def unit_key(st, hp, ud):
    hb = st.base[st.H]
    w, h = (hb[1] - hb[0]) / (st.nsub_h << ud), (hb[3] - hb[2]) / (st.nsub_h << ud)
    xm, ym = float((hp[1][0] + hp[1][1]) / 2), float((hp[1][2] + hp[1][3]) / 2)
    T0, T1 = st.h_t0, st.h_t1
    tm = (hp[3].t0 + hp[3].t1) / 2
    ib = int((tm - T0) / (T1 - T0) * (st.nbins_h << ud)) if T1 > T0 else 0
    return (int((xm - hb[0]) / w), int((ym - hb[2]) / h), ib)


def build_units(st, ud):
    groups = {}
    for hp in st.hpieces:
        groups.setdefault(unit_key(st, hp, ud), []).append(hp)
    return {k: C.node_of(v, tag=k) for k, v in groups.items()}, groups


def run_csp(st, free_opts, roles_reach, ud=1, step=4.0):
    """the CSP on the current round's rows; mutates st.alive (singleton rows), st.hpieces (dead units),
    st.letters_csp; returns (surviving free_opts, masks, unit index, record)."""
    t0 = time.perf_counter()
    if st.compat is None:
        st.compat = C.Compat(step)
    compat = st.compat
    compat.reset()
    units, ugroups = build_units(st, ud)
    by_cell_slot = {}
    for p in st.slots:
        for pc in st.alive[p]:
            by_cell_slot.setdefault((pc[0], p), []).append((piece_addr(st, pc), pc))
    opts, trees = {}, {}
    n_pieces = 0
    for ci, S, ch, h, b in free_opts:
        pcs = opt_pieces(st, ci, S, by_cell_slot)
        if not pcs:
            continue
        n_pieces += len(pcs)
        node = opt_node(st, pcs, (ci, tuple(sorted(S))))
        opts[(ci, S)] = (node, S)
        trees[(ci, S)] = node
    t_build = 1000 * (time.perf_counter() - t0)
    others = {p for r, v in roles_reach.items() if r != st.H for p in v}
    slots_free = [p for p in st.slots if p not in others]
    masks, alive_u, dead_opts, dead_units, iters, t_clip, uidx, srec = CC.mutual_clip(st, opts, units, slots_free, compat, settle_on=st.settle)
    # feed back: singleton rows kill the slot's pieces of the cell; dead units kill H's pieces
    dead_keys = {k: r for k, r, _ in dead_opts}
    killed_pieces = 0
    for (ci, S), r in dead_keys.items():
        if len(S) == 1:
            (p,) = tuple(S)
            before = len(st.alive[p])
            st.alive[p] = [pc for pc in st.alive[p] if pc[0] != ci]
            killed_pieces += before - len(st.alive[p])
            for pc in by_cell_slot.get((ci, p), ()):
                st.letters_csp[(ci, pc[1][1])] = r
    dead_set = set(dead_units)
    if dead_set:
        st.hpieces = [hp for u, hps in ugroups.items() if u not in dead_set for hp in hps]
        st.refresh_H()
    dead_sub = {}
    for ci, S in dead_keys:
        dead_sub.setdefault(ci, []).append(S)
    surv = [o for o in free_opts if (o[0], o[1]) in opts and (o[0], o[1]) not in dead_keys
            and not any(S2 <= o[1] for S2 in dead_sub.get(o[0], ()))]          # a row above a dead row is dead too
    rec = dict(n_units=len(units), n_hpieces=len(st.hpieces), alive_units=len(alive_u), n_opts=len(opts), n_opt_pieces=n_pieces,
               ud=ud, step=step, iterations=iters, slots_free=slots_free,
               dead_opts=[dict(info, cell=k[0], S=sorted(k[1]), rule=r) for k, r, info in dead_opts],
               dead_units=[dict(unit=list(u), rule=r) for u, r in sorted(dead_units.items())],
               dead_unit_count={}, killed_pieces=killed_pieces,
               ms=dict(build=round(t_build, 1), masks=t_clip["masks"], settle=(srec or {}).get("ms"), clip_total=t_clip["total"], sat=round(compat.ms, 1)),
               sat_tests=compat.n_sat, sat_dead=compat.n_dead, leaf_pairs=compat.n_leaf, block_hits=compat.n_hit, pairs_cached=len(compat.cache), settle=srec,
               unit_rects={str(list(u)): [round(v, 5) for v in n.rect] + [round(b, 3) for b in n.bins[0]] for u, n in units.items()},
               unit_alive=[list(u) for u in alive_u],
               mask_bits={"%d|%s" % (k[0], ",".join(sorted(k[1]))): bin(m).count("1") for k, m in masks.items()})
    for r in dead_units.values():
        rec["dead_unit_count"][r] = rec["dead_unit_count"].get(r, 0) + 1
    st.T.step("csp", time.perf_counter() - t0, n_units=len(units), alive_units=len(alive_u), dead_opts=len(dead_opts),
              dead_units=len(dead_units), killed_pieces=killed_pieces, iterations=iters, sat_tests=compat.n_sat)
    return surv, masks, uidx, trees, rec, alive_u
