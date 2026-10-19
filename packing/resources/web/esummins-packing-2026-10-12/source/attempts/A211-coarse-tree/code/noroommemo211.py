"""A211f -- PURE MEMOS around A189's no-room leaf, across a parent node and its children.  A189 (noroom189.py),
A208 (noroom208.py) and A171/A132 are READ-ONLY: this module WRAPS them (module-attribute patches), never edits them.

A211e's profile: no-room is 82 % of an expensive page (749 s of 908 s), and inside it `build_node` (345 s) and
`bisect_free` (386 s) are everything.  Both are PURE functions of content that a child node shares with its parent:

 (0) OBSTACLE INTERNING.  `MBox.obstacle(mode)` already caches the compiled `Obstacle` per box on the CONTENT key
     (A173: the exact rational vertices, or the core's five exact parameters), but the cache lives on the BOX, so a
     freshly built no-room node -- and every sibling branch -- compiles a brand new `Obstacle` for a K' that is
     bit-identical to one already compiled.  A new object means a new `uid`, so `Bin.radii` recomputes its exact
     per-edge bounds, and A211d's clip memo (keyed on `id(obs)`) misses every time.  Interning on
     (name, mode, content) hands back the SAME object for the SAME K' of the SAME role, so both caches start hitting
     across nodes.  `Obstacle` is immutable (`__slots__`, built once from the vertices) and its geometry is the only
     thing `_clip_rect_obstacle`, `dead_poly` and `Bin.radii` read, so a shared object returns exactly the library's
     value.  The name is part of the key purely so that nothing that prints an obstacle's name can change.

 (1) build_node MEMO.  `build_node(roles, s0, budget)` = `MB.Node(roles).normalise(nsub, refine, "poly", "pieces")`:
     a deterministic fixed point over the role BOXES alone.  Keyed on the exact boxes, s0 and (nsub, refine) it
     returns the same node -- and the same `MB.EmptyBox` kill, which is replayed rather than swallowed.

 (2) bisect_free MEMO.  The bisection reads only the node's OBSTACLES (`nd.boxes[k].obstacle("poly")` for k in
     `nd.names`), the container side `nd.s` and (tsub, depth, max_pieces).  So it is keyed on the tuple of obstacle
     CONTENT keys: two nodes whose cores agree bisect the free square identically even when their role boxes differ
     -- exactly the parent/child case Lemma ROLE-SPLIT creates, where the split role is preferred to be one whose K'
     is EMPTY (rsplit211: `core_empty` first), i.e. one that contributes no obstacle at all.  A run stopped by the
     DEADLINE is never cached (its result is budget-dependent, not content-dependent).

Nothing here changes a verdict: every memoised value is the value the library would have returned for the same
content.  The certificate fields are identical; only `seconds` (and the internal `nd.stats` counters, which no
certificate carries) differ.  `A211_NOROOM_MEMO=0` turns the whole module off; `A211_NOROOM_VERIFY=1` recomputes
every hit with the library and asserts equality.
"""
import os
import time

BCAP = 400                               # build_node entries before the memo is dropped (each holds one MB.Node)
SCAP = 400                               # bisect_free entries
OCAP = 8000                              # interned obstacles
ON = os.environ.get("A211_NOROOM_MEMO", "1") != "0"
VERIFY = os.environ.get("A211_NOROOM_VERIFY") == "1"

_OBS = {}
_BMEMO = {}
_SMEMO = {}
HITS = dict(obs_hits=0, obs_misses=0, build_hits=0, build_misses=0, bisect_hits=0, bisect_misses=0,
            build_saved=0.0, bisect_saved=0.0)
_ORIG = {}


def rep():
    d = dict(HITS)
    d.update(obs_entries=len(_OBS), build_entries=len(_BMEMO), bisect_entries=len(_SMEMO), on=ON)
    d["build_saved"] = round(d["build_saved"], 1)
    d["bisect_saved"] = round(d["bisect_saved"], 1)
    return d


# ------------------------------------------------------------------ (0) obstacle interning
def obstacle_intern(self, mode="poly"):
    """MBox.obstacle with the per-box content cache promoted to a PROCESS-WIDE one (same key, same object)."""
    key = ((self.name, mode, tuple(self.pc.verts)) if mode == "poly" else
           (self.name, mode, self.core.kx, self.core.ky, self.core.cm, self.core.sm, self.core.a))
    hit = _OBS.get(key)
    if hit is not None:
        HITS["obs_hits"] += 1
        self._obs_cache = (key[1:], hit)
        return hit
    obs = _ORIG["obstacle"](self, mode)
    if len(_OBS) >= OCAP:
        _OBS.clear()
    _OBS[key] = obs
    HITS["obs_misses"] += 1
    return obs


def obs_key(ob):
    """the CONTENT of a compiled obstacle -- what `_clip_rect_obstacle` and `dead_poly` actually read."""
    return (ob.kind, tuple(ob.verts))


# ------------------------------------------------------------------ (1) build_node
def build_memo(roles, s0=None, budget=None, name="node", verbose=False):
    """noroom189.build_node memoised on (the exact role boxes, s0, nsub, refine).  An `MB.EmptyBox` -- A171's pair
    leaf, i.e. a KILL -- is cached and re-raised, never swallowed."""
    NR = _ORIG["mod"]
    b = dict(NR.DEFAULT_BUDGET)
    b.update(budget or {})
    key = (tuple(sorted((k, tuple(v)) for k, v in roles.items())), s0, b["nsub"], b["refine"])
    hit = _BMEMO.get(key)
    if hit is not None:
        HITS["build_hits"] += 1
        HITS["build_saved"] += hit[1]
        if hit[0] is None:
            raise hit[2]
        if VERIFY:
            ref, _b = _ORIG["build_node"](roles, s0, budget, name=name, verbose=verbose)
            assert ref.names == hit[0].names and ref.s == hit[0].s, "build memo: a different node"
            for k in ref.names:
                assert list(ref.boxes[k].pc.verts) == list(hit[0].boxes[k].pc.verts) and                     ref.boxes[k].k_source == hit[0].boxes[k].k_source and                     [(bn.t0, bn.t1, r) for bn, r in ref.boxes[k].pieces] ==                     [(bn.t0, bn.t1, r) for bn, r in hit[0].boxes[k].pieces], "build memo: %s differs" % k
        return hit[0], b
    t0 = time.time()
    try:
        nd, _b = _ORIG["build_node"](roles, s0, budget, name=name, verbose=verbose)
    except Exception as e:                                        # noqa: BLE001  -- EmptyBox is a VERDICT: cache it
        if isinstance(e, _ORIG["mod"].MB.EmptyBox):
            if len(_BMEMO) >= BCAP:
                _BMEMO.clear()
            _BMEMO[key] = (None, round(time.time() - t0, 2), e)
        raise
    if len(_BMEMO) >= BCAP:
        _BMEMO.clear()
    _BMEMO[key] = (nd, round(time.time() - t0, 2), None)
    HITS["build_misses"] += 1
    return nd, b


# ------------------------------------------------------------------ (2) bisect_free
def bisect_memo(nd, budget, deadline=None):
    """noroom189.bisect_free memoised on the node's OBSTACLE CONTENT (plus s, tsub, depth, max_pieces): the only
    things the bisection reads.  A deadline-stopped run is not cached -- its residue depends on the clock."""
    NR = _ORIG["mod"]
    try:
        key = (tuple(obs_key(nd.boxes[k].obstacle("poly")) for k in nd.names), nd.s,
               budget["tsub"], budget["depth"], budget["max_pieces"])
    except Exception:                                             # noqa: BLE001 -- no key, no memo
        return _ORIG["bisect_free"](nd, budget, deadline=deadline)
    hit = _SMEMO.get(key)
    if hit is not None:
        HITS["bisect_hits"] += 1
        HITS["bisect_saved"] += hit[1]
        if VERIFY:
            ref = _ORIG["bisect_free"](nd, budget, deadline=None)
            assert list(ref[0]) == list(hit[0]) and {k: v for k, v in ref[1].items() if k != "seconds"} == {
                k: v for k, v in hit[2].items() if k != "seconds"}, "bisect memo: the residue differs"
        return list(hit[0]), dict(hit[2])
    t0 = time.time()
    pieces, cert = _ORIG["bisect_free"](nd, budget, deadline=deadline)
    HITS["bisect_misses"] += 1
    if cert.get("stop") != "deadline":
        if len(_SMEMO) >= SCAP:
            _SMEMO.clear()
        _SMEMO[key] = (list(pieces), round(time.time() - t0, 2), dict(cert))
    return pieces, cert


def install():
    """patch MB.MBox.obstacle and noroom189's two hot functions (module attributes: A189's file is untouched)."""
    if not ON or _ORIG:
        return False
    import sys
    import poly204 as P
    for d in (os.path.join(P.ROOT, "attempts", "A189-noroom", "code"),
              os.path.join(P.ROOT, "attempts", "A171-multibox-invariant", "code")):
        if d not in sys.path:
            sys.path.insert(0, d)
    import noroom189 as NR
    _ORIG["mod"] = NR
    _ORIG["obstacle"] = P.MB.MBox.obstacle
    _ORIG["build_node"] = NR.build_node
    _ORIG["bisect_free"] = NR.bisect_free
    P.MB.MBox.obstacle = obstacle_intern
    NR.build_node = build_memo
    NR.bisect_free = bisect_memo
    return True
