"""A211d -- three PURE CACHES on the clip hot path (no rule, no semantics, no lemma changes).

The instrumented node kill (A211d, logs/profile) says the coarse tree spends ~70% of a node in `normalise` (the
coarse fixed point's mutual clip) and ~21% in the option table's ROLE-REACH, and that BOTH are the same primitive:
`multibox._clip_rect_obstacle(rect, obstacle, bin)`, an exact deterministic function of its three arguments.

  (0) K' MEMO.  `MBox.rebuild` (A171/A172: the per-piece K' intersection, its inward rounding, the certification of
      every vertex against every piece, and the exact axis core) is a pure function of the SURVIVING PIECES and the
      four build parameters -- it reads nothing else and writes only ubox / pc / core / k_source / k_info.  The
      fixed point rebuilds EVERY role after EVERY pass, but a pass moves only the roles its clip touched, so most of
      those rebuilds are on a piece set that has already been built (and a sibling branch re-runs the cascade from
      its parent's state, so whole roles arrive with the same pieces again).  The memo is keyed on the exact piece
      list and the parameters; PolyCore / Core are immutable (`__slots__`, never written after construction) and
      `k_info` is copied, so a shared value cannot be aliased into a different box.

  (1) CLIP MEMO.  `_clip_rect_obstacle` is pure given (rect, obstacle object, tilt bin): the obstacle is the compiled
      K' (A171 `MultiBox.obstacle` already returns the SAME object while K' is unchanged -- it is keyed on the exact
      rational vertices) and `Bin` caches its per-edge radii under that obstacle's uid.  The memo therefore returns
      the value the library would have computed, and it also REPLAYS the `stats` deltas the call would have made, so
      the exact-call counters in the trace are unchanged too.  Hits come from the fixed point's repeated mutual
      passes and, above all, from SIBLING NODES: a branch restores its parent's state, so every role but the branched
      one arrives with the pieces and the K' its sibling already clipped.
  (2) ROLE-REACH PREFIX.  At depth 0 (every coarse role reach, and an exact one on a role carried at unit
      resolution) `fastprop.bisect_region` is exactly:  container clip -> every obstacle -> the A161 exact MISS test
      against the slot windows of S.  Only the last stage depends on S, so the prefix is computed ONCE per (role,
      current node) and every slot set reuses it.  Same survivors, same order, same test count (the counts of the
      prefix and of the misses are added back exactly as the library counts them).

Both caches are keyed on the CONTENT that the library's own result depends on, and both are dropped when the node's
`nd` is rebuilt (`normalise`).  A211d verified them call-by-call against the library (A211_CLIP_VERIFY=1): identical
survivors, identical fraction, identical test counts -- so every certificate is identical.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import poly204 as P                                            # noqa: E402

FP, MB = P.FP, P.MB
CLN = FP.CLN                                                   # A161 chordlane (READ-ONLY)
VERIFY = os.environ.get("A211_CLIP_VERIFY") == "1"
CAP = 200000                                                   # clip memo entries before it is dropped (memory guard)
RCAP = 3000                                                    # K' memo entries before it is dropped
_ORIG_CLIP = MB._clip_rect_obstacle
_ORIG_REBUILD = MB.MBox.rebuild
_MEMO = {}
_RMEMO = {}
HITS = [0, 0]                                                  # [hits, misses]
RHITS = [0, 0]


# ----------------------------------------------------------------------------- (0) the K' memo
def rebuild_memo(self, *a, **kw):
    """MBox.rebuild memoised on (the surviving pieces, n_grid, max_v, aden, kmode)."""
    n_grid = a[0] if len(a) > 0 else kw.get("n_grid", 97)
    max_v = a[1] if len(a) > 1 else kw.get("max_v", 16)
    aden = a[2] if len(a) > 2 else kw.get("aden", MB.ADEN_DEFAULT)
    kmode = a[3] if len(a) > 3 else kw.get("kmode", None)
    if not self.pieces:
        return _ORIG_REBUILD(self, *a, **kw)
    key = (self.kmode if kmode is None else kmode, n_grid, max_v, aden,
           tuple((bn.t0, bn.t1, r) for bn, r in self.pieces))
    hit = _RMEMO.get(key)
    if hit is not None:
        self.ubox, self.pc, self.core, self.k_source, k_info = hit
        self.k_info = dict(k_info)
        RHITS[0] += 1
        if VERIFY:
            pc, core, src = self.pc, self.core, self.k_source
            _ORIG_REBUILD(self, *a, **kw)
            assert list(getattr(pc, "verts", ())) == list(getattr(self.pc, "verts", ())) and self.k_source == src, (
                "K' memo: %s rebuilt differently" % self.name)
            assert (core is None) == (self.core is None) and (core is None or core.a == self.core.a), (
                "K' memo: %s core differs" % self.name)
        return self.pc
    out = _ORIG_REBUILD(self, *a, **kw)
    if len(_RMEMO) >= RCAP:
        _RMEMO.clear()
    _RMEMO[key] = (self.ubox, self.pc, self.core, self.k_source, dict(self.k_info))
    RHITS[1] += 1
    return out


def install_rebuild():
    MB.MBox.rebuild = rebuild_memo


def rebuild_rep():
    return dict(hits=RHITS[0], misses=RHITS[1], entries=len(_RMEMO))


# ----------------------------------------------------------------------------- (1) the clip memo
def clip_memo(rect, obs, bn, stats, trace=None, tag=""):
    """MB._clip_rect_obstacle memoised on (obstacle object, tilt bin, rect); the stats deltas replayed on a hit."""
    if trace is not None:
        return _ORIG_CLIP(rect, obs, bn, stats, trace=trace, tag=tag)
    key = (id(obs), bn.t0, bn.t1, rect)
    hit = _MEMO.get(key)
    if hit is not None:
        _obs, out, delta = hit                                 # _obs keeps the obstacle alive, so id() cannot be reused
        for k, v in delta:
            stats[k] = stats.get(k, 0) + v
        HITS[0] += 1
        if VERIFY:
            chk = dict(stats)
            ref = _ORIG_CLIP(rect, obs, bn, chk)
            assert ref == out, ("clip memo: %r != %r" % (ref, out))
        return out
    before = dict(stats)
    out = _ORIG_CLIP(rect, obs, bn, stats)
    delta = tuple((k, stats[k] - before.get(k, 0)) for k in stats if stats[k] != before.get(k, 0))
    if len(_MEMO) >= CAP:
        _MEMO.clear()
    _MEMO[key] = (obs, out, delta)
    HITS[1] += 1
    return out


def install_memo():
    MB._clip_rect_obstacle = clip_memo


def memo_rep():
    return dict(hits=HITS[0], misses=HITS[1], entries=len(_MEMO))


# ----------------------------------------------------------------------------- (2) the depth-0 reach prefix
def prefix_clip(pcs, obst, s, stats):
    """the S-INDEPENDENT prefix of FP.bisect_region(depth=0): the container clip then every obstacle, in the
    library's order, counting the library's tests."""
    out, n = [], 0
    for bn, r in pcs:
        cur, _sl = MB.container_clip(r, bn, s, strict=False)
        if cur is None:
            n += 1
            continue
        for ob in obst:
            if ob is None:
                continue
            cur = MB._clip_rect_obstacle(cur, ob, bn, stats)
            n += 1
            if cur is None:
                break
        if cur is None:
            continue
        out.append((bn, cur))
    return out, n


def miss_filter(pcs, wbs):
    """the S-DEPENDENT tail: A161's exact MISS test of every piece against every widened slot box of S."""
    if not wbs:
        return list(pcs), 0
    out, n = [], 0
    for bn, cur in pcs:
        bx = MB.piece_box(bn, cur)[0]
        dead = False
        for wb in wbs:
            n += 1
            if CLN.box_misses_cell_exact(bx, wb)[0]:
                dead = True
                break
        if dead:
            continue
        out.append((bn, cur))
    return out, n


def reach0(pg, role, wbs):
    """FP.bisect_region(None, obstacles_except(role), wbs, s, stats, depth=0, seed_pieces=pieces) with the prefix
    shared across the slot sets of this role at this node.  Returns the library's (frac, pieces, n_tests)."""
    pcs = pg.nd.boxes[role].pieces
    if not pcs:
        return 0.0, [], 0
    ent = getattr(pg, "_reach0", None)
    if ent is None:
        ent = pg._reach0 = {}
    e = ent.get(role)
    if e is None:
        R = FP.pieces_hull(pcs)[:4]
        obst = [ob for ob in pg.obstacles_except(role) if FP.obstacle_near(ob, R)]
        vol0 = sum(MB.rect_area(r) * (bn.t1 - bn.t0) for bn, r in pcs)
        if vol0 <= 0:
            e = ent[role] = ([], 0, 0)
        else:
            kept, n0 = prefix_clip(pcs, obst, pg.s, pg.nd.stats)
            e = ent[role] = (kept, n0, vol0)
    kept, n0, vol0 = e
    if vol0 <= 0:
        return 0.0, [], 0
    out, n1 = miss_filter(kept, wbs)
    if not out:
        res = (0.0, [], n0 + n1)
    else:
        vol = sum(MB.rect_area(r) * (bn.t1 - bn.t0) for bn, r in out)
        res = (float(vol / vol0), out, n0 + n1)
    if VERIFY:
        ref = FP.bisect_region(None, pg.obstacles_except(role), wbs, pg.s, pg.nd.stats, depth=0, seed_pieces=pcs, max_pieces=4096)
        assert ref[0] == res[0] and ref[1] == res[1] and ref[2] == res[2], (
            "reach0 %s: %r / %r vs %r / %r" % (role, res[0], res[2], ref[0], ref[2]))
    return res


def drop(pg):
    """the node's nd was rebuilt: the per-role prefixes belong to the old K's."""
    if getattr(pg, "_reach0", None):
        pg._reach0 = {}
