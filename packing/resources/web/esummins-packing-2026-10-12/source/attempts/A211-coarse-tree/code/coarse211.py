"""A211 -- the COARSE node (notes/coarse_tree.md, soundness points S1-S4): A207's TreePage207 (A206 Rule NS + A205's
clips + A204's cascade + the basin clip) with a `coarse` switch.  In coarse mode (every INTERNAL node):
  * every non-pin role with more than CAP pieces is RE-BINNED onto NX x NY sub-rects x NB tilt bins of its own hull
    (exact rationals); a unit is kept iff it meets some piece, so the union of the units is a SUPERSET of the union of
    the pieces (S1: sound, weaker);
  * the polygon fixed point runs with refine REFINE, at most MAX_ITER mutual-clip passes, NO lonely clip, K' rebuilt
    in KMODE ("union" = A171's polygon on the union hull of the surviving pieces) on the coarser NGRID tilt grid --
    a PREFIX of A204's clip chain on a WEAKER core (S2': the union-hull K' is a subset of A172's per-piece K', and
    every vertex of either is exactly certified against the whole tilt interval, so a coarse K' is a sound obstacle);
  * the option table's reach bisects DEPTH levels per cell (JDEPTH for joint slot sets) instead of A198's 5 / 2, and a
    role's reach is clipped in place (depth 0) -- a shallower bisection keeps a superset (S3);
  * the basin clip is off (it returns with the exact leaf cascade; skipping a clip keeps more: S2).
In exact mode (the leaf's cascade, rule (e)) everything is A209's: nsub 4 / refine 2, lonely clip, the basins, depth
5 / 2, the sharp round.  Every coarse DEAD is a genuine DEAD (every test is a sound necessary condition); a coarse
ALIVE only says "branch further"."""
import os
import time
from fractions import Fraction as Fr

import poly204 as P
import tree207 as N7
import fastclip211 as FC
import noroommemo211 as NRM

FP, MB = P.FP, P.MB
NX, NY, NB = 4, 4, 6                     # the coarse grid: 16 sub-rects x 6 tilt bins
CAP = 96                                 # a role carrying more pieces than this is re-binned (<= NX*NY*NB units)
REFINE, MAX_ITER, NSUB = 1, 2, 2         # the coarse fixed point: refine 1, <= 2 mutual passes, nsub 2 for box-only roles
DEPTH, JDEPTH = 2, 1                     # the coarse reach depths (A198: 5 / 2)
KMODE = os.environ.get("A211_KMODE", "union")     # the COARSE core: A171's union-hull K' (a subset of A172's per-piece
NGRID = int(os.environ.get("A211_NGRID", "33"))   # K': S2'), on a coarser tilt grid than A171/A132's 97.  The two env
                                                  # knobs re-run the pre-A211e node ("pieces" / 97) for a comparison.
NGRID_FALL = 97                          # ... and the fallback when the coarse grid will not certify at all
_GRID = [0, 0, 0, 0]                     # [coarse builds, grid fallbacks, per-piece fallbacks, exact-mode builds]
# A211f -- the coarse core is CONDITIONAL (NOTES_A211f (3)).  A211e measured the trade exactly: the union-hull K'
# makes a node 2.8x cheaper but kills later, so it pays only where the fixed point is the expensive part (Y0202:
# -86 % a node, +3 kills in the wall) and costs where the node is already cheap and the kills come from EmptyBox /
# COUNT off a strong clip (Y0036_D07: +45 % wall).  The predicate is the PARENT's own cascade seconds -- the one
# number that separates the two pages (Y0202: 89-214 s a node; Y0036_D07: mean 12.1 s, max 38.3 s) -- with the role
# count as a second, off-by-default trigger (on Y0036_D07 every node from depth 1 carries >= 8 roles, so the role
# count alone would just restore A211e).  A start node's ROOT has no parent: it runs with the exact per-piece core.
# Soundness is untouched either way: S2' says the coarse K' is a subset of the per-piece one, so both are sound
# obstacles; the choice is a BUDGET decision and is recorded per node (`coarse_core` in the round report).
COARSE_SECONDS = float(os.environ.get("A211_COARSE_SECONDS", "20"))
COARSE_ROLES = int(os.environ.get("A211_COARSE_ROLES", "99"))
_CORE = [False]                          # the core the NEXT coarse_fixpoint uses
_CORE_N = [0, 0]                         # [nodes with the coarse core, nodes with the exact per-piece core]
EXACT = dict(depth=5, joint_depth=2, refine_mb=2, nsub_mb=4)
_BINS = {}


def mkbin(a, b):
    k = (a, b)
    if k not in _BINS:
        _BINS[k] = MB.Bin(a, b)
    return _BINS[k]


def _ov(a0, a1, b0, b1):
    """the intervals meet (open overlap; a degenerate interval counts when it lies inside the other)."""
    return max(a0, b0) < min(a1, b1) or (a0 == a1 and b0 <= a0 <= b1) or (b0 == b1 and a0 <= b0 <= a1)


def rebin(pcs, nx=NX, ny=NY, nb=NB):
    """the pieces re-gridded onto nx x ny x nb units of their hull; a unit is kept iff it meets some piece (S1)."""
    x0, x1, y0, y1, t0, t1 = FP.pieces_hull(pcs)
    xs = [x0 + (x1 - x0) * Fr(i, nx) for i in range(nx + 1)]
    ys = [y0 + (y1 - y0) * Fr(j, ny) for j in range(ny + 1)]
    ts = MB.sub_bins(t0, t1, nb)
    out = []
    for i in range(nx):
        for j in range(ny):
            u = (xs[i], xs[i + 1], ys[j], ys[j + 1])
            hit = [(b, r) for b, r in pcs if _ov(r[0], r[1], u[0], u[1]) and _ov(r[2], r[3], u[2], u[3])]
            if not hit:
                continue
            for (a, c) in ts:
                if any(_ov(b.t0, b.t1, a, c) for b, _ in hit):
                    out.append((mkbin(a, c), u))
    return out


# --------------------------------------------------------------------------- the COARSE core (S2')
_REBUILD = [None]


def grid_rebuild(self, *a, **kw):
    """`MBox.rebuild` with the COARSE tilt grid whenever the box is in kmode "union" -- i.e. at every internal node,
    where `coarse_fixpoint` sets kmode = KMODE.  In kmode "pieces" (the exact leaf cascade, and A171's own fallback
    inside `rebuild`) nothing changes: the call goes straight through with the library's n_grid 97.

    SOUNDNESS (notes/coarse_tree.md S2').  `polycore.build` clips a start polygon by the half-planes of the n_grid
    sampled tilts, shrinks, rounds to rationals, and then CERTIFIES every vertex with the exact `vertex_ok` against
    the WHOLE tilt interval [t0, t1], retrying with a larger shrink until every vertex certifies (or raising).  So
    whatever polygon comes back is exactly certified whatever n_grid was: a coarse grid needs a larger shrink and
    therefore returns a SMALLER polygon -- weaker, never wrong.  A178's `mbpatch178.rebuild` turns "no certified polygon" into an EMPTY K'
    (k_source "empty", no obstacle, no clip: sound but blind), and a WIDE role's union hull certifies nothing while
    its per-piece K' still does -- so an empty coarse K' retries on the library grid and then, still empty, on kmode
    "pieces": a STRONGER core, i.e. exactly the pre-A211e node.  EmptyBox propagates as always."""
    if a or "n_grid" in kw or (kw.get("kmode") or self.kmode) != "union":
        _GRID[3] += 1
        return _REBUILD[0](self, *a, **kw)
    out = _REBUILD[0](self, n_grid=NGRID, **kw)
    if self.k_source != "empty":
        _GRID[0] += 1
        return out
    out = _REBUILD[0](self, n_grid=NGRID_FALL, **kw)             # the coarse grid certified nothing: the library grid
    if self.k_source != "empty":
        _GRID[1] += 1
        return out
    kw.pop("kmode", None)                                        # no certified polygon on the UNION HULL at any grid
    out = _REBUILD[0](self, kmode="pieces", **kw)                # (a wide role): back to A172's per-piece K' -- a
    _GRID[2] += 1                                                # STRONGER core, i.e. exactly the pre-A211e node
    return out


def grid_rep():
    return dict(kmode=KMODE, n_grid=NGRID, coarse_builds=_GRID[0], grid_fallbacks=_GRID[1],
                pieces_fallbacks=_GRID[2], exact_builds=_GRID[3], conditional=dict(
                    parent_seconds=COARSE_SECONDS, roles=COARSE_ROLES, coarse_nodes=_CORE_N[0], exact_core_nodes=_CORE_N[1]))


def coarse_fixpoint(nd, corners, s, refine=REFINE, max_iter=MAX_ITER, max_pieces=96, near=True):
    """A204's fixpoint (poly204.fixpoint) with the lonely clip OFF, refine / max_iter capped and K' in KMODE (S2')
    -- but only at a node the predicate calls expensive (A211f): elsewhere the per-piece core of the pre-A211e node."""
    names = nd.names
    st = nd.stats
    km = KMODE if _CORE[0] else "pieces"
    rep = dict(lonely=[], passes=0, refine=refine, coarse=True, kmode=km, n_grid=NGRID if _CORE[0] else NGRID_FALL,
               coarse_core=_CORE[0])

    def clip_all(cur, bn, k, obst):
        for j in names:
            if j == k or cur is None:
                continue
            ob = obst[j]
            if ob is None or (near and not FP.obstacle_near(ob, cur)):
                continue
            cur = MB._clip_rect_obstacle(cur, ob, bn, st)
        return cur

    for mb in nd.boxes.values():
        keep = []
        for (bn, r) in mb.pieces:
            nr, _sl = MB.container_clip(r, bn, s, strict=False)
            if nr is not None:
                keep.append((bn, nr))
        if not keep:
            raise MB.EmptyBox(mb.name, dict(reason="container"))
        mb.pieces = keep
        mb.kmode = km
    for lvl in range(max(0, refine)):
        for mb in nd.boxes.values():
            mb.rebuild()
        obst = {k: nd.boxes[k].obstacle("poly") for k in names}
        for k in names:
            mb = nd.boxes[k]
            if len(mb.pieces) * 2 > max_pieces:
                continue
            new = []
            for (bn, r) in mb.pieces:
                for (bn2, r2) in MB.split_piece(bn, r):
                    cur, _sl = MB.container_clip(r2, bn2, s, strict=False)
                    cur = clip_all(cur, bn2, k, obst)
                    if cur is not None:
                        new.append((bn2, cur))
            if not new:
                raise MB.EmptyBox(mb.name, dict(reason="refine", level=lvl + 1))
            mb.pieces = new
    vprev = sum(P.vol(mb.pieces) for mb in nd.boxes.values())
    for it in range(max_iter):
        moved = False
        for mb in nd.boxes.values():
            mb.rebuild()
        obst = {k: nd.boxes[k].obstacle("poly") for k in names}
        for k in names:
            mb = nd.boxes[k]
            keep = []
            for (bn, r) in mb.pieces:
                cur = clip_all(r, bn, k, obst)
                if cur != r:
                    moved = True
                if cur is not None:
                    keep.append((bn, cur))
            if not keep:
                raise MB.EmptyBox(mb.name, dict(reason="mutual", pass_=it + 1))
            mb.pieces = keep
        rep["passes"] = it + 1
        vnow = sum(P.vol(mb.pieces) for mb in nd.boxes.values())
        if not moved or vnow > vprev * (1 - Fr(1, 1000)):
            rep["stopped"] = "moved < 0.1%" if moved else "fixed"
            break
        vprev = vnow
    for mb in nd.boxes.values():
        mb.rebuild()
        mb.kept = mb.kept_fraction()
    nd.normalised = True
    return rep


class CoarsePage(N7.TreePage207):
    def __init__(self, *a, **kw):
        N7.TreePage207.__init__(self, *a, **kw)
        self.all_basins = list(self.basins)
        self.rebin_rep = []
        self.coarse = None
        self.last_round_seconds = 0.0                             # A211f: the PARENT's cascade seconds (save/restore)
        self.core_rep = []
        self.set_coarse(True)

    def set_coarse(self, on):
        self.coarse = bool(on)
        if on:
            self.depth, self.joint_depth, self.refine_mb, self.nsub_mb = DEPTH, JDEPTH, REFINE, NSUB
            self.basins = []
        else:
            self.depth, self.joint_depth, self.refine_mb, self.nsub_mb = EXACT["depth"], EXACT["joint_depth"], EXACT["refine_mb"], EXACT["nsub_mb"]
            self.basins = list(self.all_basins)

    def coarse_core_on(self, label):
        """A211f: does THIS node get the coarse union-hull core?  Only when the fixed point is the expensive part --
        the parent's cascade took more than COARSE_SECONDS (or the node carries COARSE_ROLES roles).  A budget
        decision, recorded: both cores are sound (S2'), the coarse one is simply weaker."""
        par, nr = float(self.last_round_seconds or 0.0), len(self.roles)
        on = par > COARSE_SECONDS or nr >= COARSE_ROLES
        _CORE[0] = on
        _CORE_N[0 if on else 1] += 1
        self.core_rep.append(dict(label=label, coarse_core=on, parent_seconds=round(par, 1), n_roles=nr))
        self.T.test("COARSE-CORE", label=label, coarse_core=on, parent_seconds=round(par, 1), n_roles=nr,
                    kmode=(KMODE if on else "pieces"), n_grid=(NGRID if on else NGRID_FALL),
                    rule="parent cascade > %.0f s or >= %d roles" % (COARSE_SECONDS, COARSE_ROLES))
        return on

    def normalise(self, label):
        FC.drop(self)                                             # the node's nd (and every K' in it) is rebuilt here
        if not self.coarse:
            return N7.TreePage207.normalise(self, label)
        t0 = time.time()
        self.coarse_core_on(label)
        for k, pcs in list(self.pieces.items()):
            if k.startswith("P") or not pcs or len(pcs) <= CAP:
                continue
            new = rebin(pcs)
            self.pieces[k] = new
            self.rebin_rep.append(dict(label=label, role=k, n_before=len(pcs), n_after=len(new)))
            self.T.test("REBIN", role=k, label=label, n_before=len(pcs), n_after=len(new), grid=[NX, NY, NB])
        self.T.step("rebin", time.time() - t0, label=label)
        old = P.fixpoint
        P.fixpoint = coarse_fixpoint
        try:
            return N7.TreePage207.normalise(self, label)
        finally:
            P.fixpoint = old
            self.last_round_seconds = time.time() - t0            # the number this node's CHILDREN are judged on

    def role_reach(self, role, S):
        if not self.coarse:
            return N7.TreePage207.role_reach(self, role, S)
        key = (role, S)
        if key in self.reach_cache:
            return self.reach_cache[key]
        t0 = time.time()
        # FP.bisect_region(None, obstacles_except(role), the windows of S, s, stats, depth=0, seed_pieces=pieces,
        # max_pieces=4096) with the S-INDEPENDENT prefix (container + obstacles) shared across this role's slot sets
        # at this node: the same survivors, the same fraction, the same exact-test count (fastclip211 (2)).
        res = FC.reach0(self, role, [self.item[p]["wb"] for p in S])
        self.T.test("ROLE-REACH", role=role, slots=sorted(S), depth=0, coarse=True, frac=round(res[0], 6), n_pieces=len(res[1]), n_exact=res[2], seconds=round(time.time() - t0, 3))
        self.reach_cache[key] = res
        return res


def save_state(pg):
    st = N7.save_state(pg)
    st["coarse"], st["rebin_rep"], st["noroom_k"] = pg.coarse, list(pg.rebin_rep), getattr(pg, "noroom_k", None)
    st["last_round_seconds"] = getattr(pg, "last_round_seconds", 0.0)
    return st


def restore_state(pg, st):
    N7.restore_state(pg, st)
    pg.set_coarse(st["coarse"])
    pg.rebin_rep = list(st["rebin_rep"])
    pg.noroom_k = st.get("noroom_k")
    pg.last_round_seconds = st.get("last_round_seconds", 0.0)     # A211f: every child is judged on ITS parent


def install():
    """route the tree's save / restore through the coarse flag (after tree207.install), install A211d's two pure
    caches on the clip hot path (fastclip211: same results, same test counts -- only the recomputation is skipped),
    and A211e's coarse-grid rebuild on top of them (S2': a weaker, still certified K' at internal nodes)."""
    import tree206 as N6
    N7.install()
    N6.save_state = save_state
    N6.restore_state = restore_state
    FC.install_rebuild()
    FC.install_memo()
    _REBUILD[0] = MB.MBox.rebuild                                 # on top of the memo: the memo keys on the n_grid it is given
    MB.MBox.rebuild = grid_rebuild
    NRM.install()                                                 # A211f: the no-room memos (A189 wrapped, not edited)
    install_a213()


def install_a213():
    """A213: the K' build in INTEGER space (polycore_int / polycore_fast via mbpatch213) -- bit-exact (the replay of
    every rebuild of A211d's profile run and a fuzz: identical vertices, cores, k_info), only faster.  Behind the flag
    A213_INTCORE (default on; =0 restores the library build); A213_VERIFY=1 runs both and asserts on every call."""
    import sys
    a213 = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "A213-int-polycore", "code"))
    try:
        if a213 not in sys.path:
            sys.path.insert(0, a213)
        import mbpatch213 as M213
        return M213.install()
    except Exception as e:                                        # noqa: BLE001  -- never let the patch stop a node
        print("   A213 int-polycore NOT installed (library build in use): %r" % (e,), flush=True)
        return False
