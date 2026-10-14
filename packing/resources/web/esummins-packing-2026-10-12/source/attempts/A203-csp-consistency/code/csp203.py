"""A203 -- the closed-form CSP layer on PIECES (the PI's readings of 2026-09-10 on Y0839 / Y0191; lemmas in
notes/csp_consistency.md).  Rule S: piece-pair compatibility by the separating-axis bound with the tilt bins
(Lemma PC); H-CONSISTENCY: an option row with no piece compatible with any alive H unit is dead (H exists);
the MUTUAL CLIP: an H unit compatible with no option of a forced slot that some FREE square must meet is dead
(Corollary FC-count); iterated to a fixed point.  Every exclusion is a SOUND necessary condition; an undecided
pair is compatible.  Leaf blocks are evaluated by satbatch203 (numpy), cached per (node, node)."""
import itertools
import math
import time

import numpy as np

import rules202 as R
import satbatch203 as SB

EPS = 1e-9
SQ2H = math.sqrt(0.5)
R_MAX2 = (0.5 + SQ2H) ** 2 + 1e-6          # beyond this centre distance no piece pair can be excluded by rule S
_UID = itertools.count(1)


def dist90(a0, a1):
    """min over a in [a0, a1] (degrees) of the distance from a to the nearest multiple of 90 (<= 45)."""
    if a1 - a0 >= 90:
        return 0.0
    m = math.floor(a0 / 90.0) * 90.0
    if a0 <= m + 90 <= a1 or a0 <= m <= a1:
        return 0.0
    return min(a0 - m, m + 90 - a1)


def _side_dead(polar, bA, bB, step):
    """no axis of square A (tilt in bA, axes phi and phi + 90) separates: for every phi the projection distance
    max_D |d . a(phi)| is < 1/2 + w(theta_B - phi)/2 for every theta_B in bB."""
    lo, hi = bA
    n = max(1, int(math.ceil((hi - lo) / step)))
    for k in range(n):
        p0, p1 = lo + (hi - lo) * k / n, lo + (hi - lo) * (k + 1) / n
        lhs = 0.0
        for r, al in polar:
            v = r * math.cos(math.radians(dist90(p0 - al, p1 - al)))
            if v > lhs:
                lhs = v
        rhs = 0.5 + R.wmin_deg(bB[0] - p1, bB[1] - p0) / 2
        if lhs >= rhs - EPS:
            return False
    return True


def sat_dead(r1, b1, r2, b2, step=4.0):
    """Rule S (Lemma PC): TRUE only when NO pose pair (c1 in r1, tilt in b1) x (c2 in r2, tilt in b2) is interior-
    disjoint: neither square's axes can separate the projections (SAT), the centre difference d = c2 - c1 ranging
    over the closed rect D = r2 - r1 (|d . a| is maximal at a corner of D), the tilt sub-intervals of width <= step."""
    D = (r2[0] - r1[1], r2[1] - r1[0], r2[2] - r1[3], r2[3] - r1[2])
    corners = [(x, y) for x in (D[0], D[1]) for y in (D[2], D[3])]
    dmax2 = max(x * x + y * y for x, y in corners)
    if dmax2 < 1.0 - EPS:
        return True                                                    # Lemma CN (every axis fails)
    if dmax2 >= R_MAX2:
        return False
    polar = [(math.hypot(x, y), math.degrees(math.atan2(y, x))) for x, y in corners]
    return _side_dead(polar, b1, b2, step) and _side_dead(polar, b2, b1, step)


class Node:
    """a hierarchical piece set: rect (float) x bins (degree intervals); kids = finer nodes, or LEAVES = the pieces
    (fast30.Piece) as numpy arrays (rects (n,4), bins (n,2)) for the block test."""
    __slots__ = ("rect", "bins", "kids", "uid", "tag", "leaves", "lr", "lb", "lkey")

    def __init__(self, rect, bins, kids=(), tag=None, leaves=None):
        self.rect, self.bins, self.kids, self.tag = rect, list(bins), list(kids), tag
        self.uid = next(_UID)
        self.leaves = leaves
        if leaves is not None:
            self.lr = np.array([p[2] for p in leaves], dtype=float)
            self.lb = np.array([p[4] for p in leaves], dtype=float)
            self.lkey = tuple(id(p) for p in leaves)                     # the block cache survives the round (same pieces)
        elif not self.kids:
            # a HULL-ONLY leaf (a fixed role's row: hull x its tilt intervals, no pieces): one block row per interval.
            # (A203 artefact caught 2026-09-10 17:50: such a node was walked as an internal node with no children, so
            # every (free row, H row) pair surviving the hull test was vacuously EXCLUDED -- Y0054 "died" at the g1 pad.)
            self.leaves = []
            self.lr = np.array([rect] * len(self.bins), dtype=float)
            self.lb = np.array(self.bins, dtype=float)
            self.lkey = ("hull", self.uid)
        else:
            self.lr = self.lb = self.lkey = None


def node_of(pieces, tag=None):
    """one node over a list of Pieces -- hull rect, bin hull, the pieces as leaves."""
    rect = (min(p[2][0] for p in pieces), max(p[2][1] for p in pieces), min(p[2][2] for p in pieces), max(p[2][3] for p in pieces))
    return Node(rect, merge_bins([p[4] for p in pieces]), (), tag, leaves=list(pieces))


def merge_bins(bs):
    bs = sorted(set(bs))
    out = []
    for lo, hi in bs:
        if out and lo <= out[-1][1] + 1e-12:
            out[-1] = (out[-1][0], max(out[-1][1], hi))
        else:
            out.append((lo, hi))
    return out


class Compat:
    """cached node-pair compatibility (the sound direction: False only with a proof by rule S at every leaf pair).
    `pairs` remembers, per compatible leaf-block pair, the surviving leaf index pairs (for the settle step)."""

    def __init__(self, step=4.0):
        self.cache = {}
        self.pairs = {}
        self.blocks = {}                                               # (lkey, lkey) -> alive leaf index pairs (persistent)
        self.step = step
        self.n_sat = 0
        self.n_dead = 0
        self.n_leaf = 0
        self.n_hit = 0
        self.ms = 0.0

    def reset(self):
        """a new round: the node caches go (new nodes), the leaf-block cache stays."""
        self.cache, self.pairs = {}, {}

    def dead(self, A, B):
        self.n_sat += 1
        for ba in A.bins:
            for bb in B.bins:
                if not sat_dead(A.rect, ba, B.rect, bb, self.step):
                    return False
        self.n_dead += 1
        return True

    def ok(self, A, B):
        k = (A.uid, B.uid) if A.uid <= B.uid else (B.uid, A.uid)
        v = self.cache.get(k)
        if v is not None:
            return v
        t = time.perf_counter()
        v = self._ok(A, B)
        self.ms += 1000 * (time.perf_counter() - t)
        self.cache[k] = v
        return v

    def _ok(self, A, B):
        if R.rect_maxdist2(A.rect, B.rect) >= R_MAX2:
            return True
        if self.dead(A, B):
            return False
        if A.leaves is not None and B.leaves is not None:
            return self.block(A, B)
        if A.leaves is None and B.leaves is None:
            assert A.kids and B.kids
            for a in A.kids:
                if not self.dead(a, B):
                    for b in B.kids:
                        if self._ok(a, b):
                            return True
            return False
        big, small = (A, B) if A.leaves is None else (B, A)
        return any(self._ok(k, small) for k in big.kids)

    def block(self, A, B):
        k = (A.uid, B.uid) if A.uid <= B.uid else (B.uid, A.uid)
        v = self.cache.get(k)
        if v is not None:
            return v
        bk = (A.lkey, B.lkey)
        prs = self.blocks.get(bk)
        if prs is None:
            d = SB.block(A.lr, A.lb, B.lr, B.lb, self.step)
            self.n_leaf += d.size
            prs = self.blocks[bk] = [(int(i), int(j)) for i, j in np.argwhere(~d)]
            self.blocks[(B.lkey, A.lkey)] = [(j, i) for i, j in prs]
        else:
            self.n_hit += 1
        v = len(prs) > 0
        if v:
            self.pairs[k] = prs if A.uid <= B.uid else [(j, i) for i, j in prs]
        self.cache[k] = v
        return v

    def forget(self, A, B):
        """drop a cached block verdict (the settle step re-decides it)."""
        k = (A.uid, B.uid) if A.uid <= B.uid else (B.uid, A.uid)
        self.cache.pop(k, None)
        self.pairs.pop(k, None)


def maxdist(A, B):
    return round(math.sqrt(R.rect_maxdist2(A.rect, B.rect)), 4)


def leaf_blocks(A, B):
    """the (leaf node of A, leaf node of B) pairs under two nodes (each side: itself if it has leaves, else its kids' leaf nodes)."""
    la = [A] if A.leaves is not None else [k for k in A.kids if k.leaves is not None]
    lb = [B] if B.leaves is not None else [k for k in B.kids if k.leaves is not None]
    return [(a, b) for a in la for b in lb]
