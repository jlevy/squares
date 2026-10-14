"""A211c -- Lemma ROLE-SPLIT (notes/coarse_tree.md s.5): at a fully named leaf where no-room did NOT kill, bisect the
widest named role's box and recurse into the two halves.

The lemma: for a role r, a coordinate u in {x, y, t} (t = tan(tilt/2)) and a value m inside its hull, "u(r) <= m" or
"u(r) >= m" is an exhaustive disjunction over the genuine packings of the node, and the child's pieces (the parent's
pieces intersected with the halfspace: the rect clipped for a position coordinate, the sub-bin cut for the tilt one)
are a SUPERSET of the poses of r allowed by the child's hypothesis.  So the node is DEAD iff both children are, and
each child is an ordinary coarse node: the cascade round, then the leaf rules from the top (no-room included).

The steering is heuristic (soundness does not depend on it): among the non-pin roles, WIDE = position extent > 0.25 or
tilt range > 30 deg; a role whose core K' is EMPTY (`pg.obst[r] is None`) is preferred (an empty core is exactly what
makes no-room, the mutual clip and rule CC blind); then the widest role, scored against those two gates, split on its
widest dimension at the midpoint.  At most CAP = 4 splits per role along a path."""
from fractions import Fraction as Fr

import coarse211 as C11
import poly204 as P

FP, MB = P.FP, P.MB

WIDE_POS = 0.25                          # a position extent wider than this makes the role a split candidate
WIDE_TILT = 30.0                         # ... or a tilt range wider than this many degrees
CAP = 4                                  # splits of one role along one path (notes/coarse_tree.md s.5)


def deg(t):
    return MB.deg_of_t(t)


def hull_of(pcs):
    """the exact (x0, x1, y0, y1, t0, t1) hull of the role's current pieces (rationals)."""
    return FP.pieces_hull(pcs)


def role_spec(pg, role, pcs):
    """the split this role would take, or None when it is not WIDE: dict(role, dim, m, extents, score, core_empty)."""
    x0, x1, y0, y1, t0, t1 = hull_of(pcs)
    wx, wy = float(x1 - x0), float(y1 - y0)
    wt = deg(t1) - deg(t0)
    sc = dict(x=wx / WIDE_POS, y=wy / WIDE_POS, t=wt / WIDE_TILT)     # each gate scaled to 1: comparable dimensions
    dim = max(sc, key=lambda k: sc[k])
    if sc[dim] <= 1.0:
        return None
    m = {"x": (x0 + x1) / 2, "y": (y0 + y1) / 2, "t": (t0 + t1) / 2}[dim]
    return dict(role=role, dim=dim, m=m, score=round(sc[dim], 4), scores={k: round(v, 4) for k, v in sc.items()},
                extents=dict(x=round(wx, 6), y=round(wy, 6), tilt=round(wt, 4)),
                box=[round(float(v), 6) for v in (x0, x1, y0, y1)] + [round(deg(t0), 4), round(deg(t1), 4)],
                core_empty=bool((pg.obst or {}).get(role) is None), n_pieces=len(pcs))


def candidates(pg, used=None):
    """every WIDE non-pin role of the live node, best first (core empty first, then the widest); `used` counts the
    splits already taken per role on this path (a role at the CAP is dropped)."""
    used = used or {}
    out = []
    for role, pcs in sorted(pg.pieces.items()):
        if role.startswith("P") or not pcs or used.get(role, 0) >= CAP:
            continue
        sp = role_spec(pg, role, pcs)
        if sp is not None:
            sp["n_splits"] = used.get(role, 0)
            out.append(sp)
    out.sort(key=lambda d: (0 if d["core_empty"] else 1, -d["score"]))
    return out


def branches(sp):
    """the two children of Lemma ROLE-SPLIT: sides 'lo' (u <= m) and 'hi' (u >= m), as ordinary branch dicts."""
    md = round(deg(sp["m"]), 4) if sp["dim"] == "t" else round(float(sp["m"]), 6)
    return [dict(slot=sp["role"], kind="rsplit", rows=["%s%s%s" % (sp["dim"], "<=" if side == "lo" else ">=", md)],
                 named=None, role=sp["role"], dim=sp["dim"], side=side, m=sp["m"], m_f=md,
                 extents=sp["extents"], core_empty=sp["core_empty"], box=sp["box"]) for side in ("lo", "hi")]


def _clip_pos(pcs, i0, i1, m, lo):
    """the pieces intersected with the halfspace on the position coordinate whose rect slots are (i0, i1)."""
    out = []
    for b, r in pcs:
        a, c = r[i0], r[i1]
        na, nc = (a, min(c, m)) if lo else (max(a, m), c)
        if na > nc:
            continue
        r2 = list(r)
        r2[i0], r2[i1] = na, nc
        out.append((b, tuple(r2)))
    return out


def _clip_tilt(pcs, m, lo):
    """the pieces with every sub-bin cut at m (a bin entirely on the far side is dropped; one that straddles is cut)."""
    out = []
    for b, r in pcs:
        if lo:
            if b.t0 >= m:
                continue
            out.append((b if b.t1 <= m else C11.mkbin(b.t0, m), r))
        else:
            if b.t1 <= m:
                continue
            out.append((b if b.t0 >= m else C11.mkbin(m, b.t1), r))
    return out


def apply_rsplit(pg, br):
    """instantiate the branch: the role's pieces intersected with its halfspace, its hull box re-taken (Lemma
    ROLE-SPLIT).  Raises ValueError when the half is empty -- the caller records the child DEAD by the split itself."""
    role, dim, lo = br["role"], br["dim"], br["side"] == "lo"
    m = Fr(br["m"])
    pcs = pg.pieces.get(role) or []
    if not pcs:
        raise ValueError("role %s carries no pieces" % role)
    new = _clip_tilt(pcs, m, lo) if dim == "t" else _clip_pos(pcs, 0 if dim == "x" else 2, 1 if dim == "x" else 3, m, lo)
    if not new:
        raise ValueError("the %s half of %s (%s %s %s) is empty" % (br["side"], role, dim, "<=" if lo else ">=", br["m_f"]))
    pg.pieces[role] = new
    pg.roles[role] = P.hull_box(new)
    pg.T.test("RSPLIT-APPLY", role=role, dim=dim, side=br["side"], m=br["m_f"], n_before=len(pcs), n_after=len(new),
              box=[round(float(v), 6) for v in pg.roles[role]])
    return len(new)
