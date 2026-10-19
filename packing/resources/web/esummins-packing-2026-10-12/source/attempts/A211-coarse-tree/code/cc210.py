"""A210 -- rule CC: Lemma CORNER-COVER as a closed-form stage-0 rule (any n).  Statement and proof:
attempts/A210-corner-cover/notes/corner_cover.md (Lemma CORNER-COVER, Corollaries CC0 / CC1 / CC').
A square Q pushed into an unpinned container corner c (distances d1, d2 <= delta from the two walls, tilt theta)
covers the corner slot's unit cell in the PACKING's frame except the three wedges W0 (corner), W1, W2 (the two wall
wedges); CC1 bounds them by three axis rectangles of the cell from (theta0, theta1, D1, D2) alone.  Every OTHER
meeter of the corner slot must have an interior point in that band, hence (CC'(b)) a centre within lambda/sqrt2
(Euclid) and lambda w_max/2 (per axis) of the band grown by lambda - 1 on its far sides -- lambda = 1 at pad 0.
Rows outside the band are dead (letter Q); no second meeter left => Theorem FC's demand 2 fails => DEAD.
Closed form, microseconds; the pad enters ONLY through lambda (the PI, 2026-09-12 01:50: pad the contact region,
never the box)."""
import math
import time

SQ2H = 0.7071067811865476
EPS = 1e-9
DELTA = 0.05                                                   # the PI's "pushed into the corner" regime (reporting)
NEAR = 0.6                                                     # gate: beyond this the band is the whole cell anyway
SQ2 = 1.4142135623730951
TINY = 1e-12


# ----------------------------------------------------------------------------- the corner frame
def frame_flags(corner):
    """(reflect_x, reflect_y, flip_tilt) for a corner name: u = x or s - x, v = y or s - y; an odd number of
    reflections sends the tilt theta to 90 - theta."""
    rx = corner in ("BR", "TR")
    ry = corner in ("TR", "TL")
    return rx, ry, (rx != ry)


def to_frame(rect, corner, s):
    """container rect (x0, x1, y0, y1) -> corner-frame rect (u0, u1, v0, v1)."""
    rx, ry, _ = frame_flags(corner)
    u0, u1 = (s - rect[1], s - rect[0]) if rx else (rect[0], rect[1])
    v0, v1 = (s - rect[3], s - rect[2]) if ry else (rect[2], rect[3])
    return (u0, u1, v0, v1)


def from_frame(rect, corner, s):
    """the same involution back to container coordinates (for the page)."""
    return to_frame(rect, corner, s)


def frame_tilt(t0, t1, corner):
    return (90.0 - t1, 90.0 - t0) if frame_flags(corner)[2] else (t0, t1)


# ----------------------------------------------------------------------------- CC1: the band of one piece
def wedge_rects(t0, t1, D1, D2, cap=1.0):
    """CC1: the three rectangles of the corner cell [0, cap]^2 containing W0 u W1 u W2 for every tilt in
    [t0, t1] (degrees, in the corner frame) and every slack d1 in [0, D1], d2 in [0, D2]."""
    t0 = max(0.0, min(90.0, t0))
    t1 = max(t0, min(90.0, t1))
    c1, c0 = math.cos(math.radians(t0)), math.cos(math.radians(t1))            # c1 = max cos, c0 = min cos
    s0, s1 = math.sin(math.radians(t0)), math.sin(math.radians(t1))            # s0 = min sin, s1 = max sin
    big = cap

    def clamp(v):
        return max(0.0, min(cap, v))
    u0 = s1 + D1 + (s1 / c0 * D2 if c0 > TINY else big)
    v0 = c1 + D2 + (c1 / s0 * D1 if s0 > TINY else big)
    R0 = (0.0, clamp(u0), 0.0, clamp(v0))                                      # corner wedge W0
    R1 = (0.0, cap, 0.0, clamp(D2 + c1 * s1 / (1.0 + s0)))                     # wall wedge W1 (the v = 0 wall)
    R2 = (0.0, clamp(D1 + c1 * s1 / (1.0 + c0)), 0.0, cap)                     # wall wedge W2 (the u = 0 wall)
    return [r for r in (R0, R1, R2) if r[1] > 0 and r[3] > 0]


def push_slack(urect, vrect, t0, t1):
    """(D1, D2) = the frame distances to the two walls, over a piece (frame rect + tilt interval), or None when the
    piece is not pushed into the corner (some pose further than DELTA from a wall)."""
    hmin = min(_h(t0), _h(t1))
    D1, D2 = max(0.0, urect[1] - hmin), max(0.0, vrect[1] - hmin)
    if D1 > DELTA + EPS or D2 > DELTA + EPS:
        return None
    return D1, D2


def _h(tdeg):
    r = math.radians(tdeg)
    return 0.5 * (math.cos(r) + math.sin(r))


def piece_bands(pieces, corner, s, lam):
    """[(key, [container rects])] -- CC1's band of EVERY pose class of a square near the corner, deduplicated by
    (tilt interval, slacks).  `near`: skip a piece whose wall distances exceed it (its band is then the whole cell
    and constrains nothing).  Each rectangle is grown by lambda - 1 on its far sides (CC'(b))."""
    out, seen = [], {}
    for (rect, t0, t1) in pieces:
        fr = to_frame(rect, corner, s)
        a, b = frame_tilt(t0, t1, corner)
        hmin = min(_h(a), _h(b))
        D1, D2 = max(0.0, fr[1] - hmin), max(0.0, fr[3] - hmin)
        key = (round(a, 6), round(b, 6), round(D1, 6), round(D2, 6))
        if key in seen:
            continue
        g = lam - 1.0
        seen[key] = [from_frame((w[0], w[1] + g, w[2], w[3] + g), corner, s) for w in wedge_rects(a, b, D1, D2)]
        out.append((key, seen[key]))
    return out or None


def band_of_pieces(pieces, corner, s, lam):
    """the UNION of the pose classes' bands: where a second meeter must lie when the square's pose is unknown."""
    bs = piece_bands(pieces, corner, s, lam)
    if not bs:
        return None
    return [w for _, ws in bs for w in ws]


# ----------------------------------------------------------------------------- the test on a candidate
def rect_gap(a, b):
    return (max(0.0, a[0] - b[1], b[0] - a[1]), max(0.0, a[2] - b[3], b[2] - a[3]))


def reaches(rect, wmax, band, lam):
    """CC'(b): can a square with centre in `rect` (container) and axis width <= wmax have an interior point in the
    band?  False => the square cannot be a second meeter of the corner slot (rule CC kills it)."""
    r2 = (lam * SQ2H) ** 2
    hw = lam * float(wmax) / 2
    for w in band:
        dx, dy = rect_gap(rect, w)
        if dx * dx + dy * dy < r2 + EPS and dx < hw + EPS and dy < hw + EPS:   # EPS on the SAFE side (over-reach)
            return True
    return False


# ----------------------------------------------------------------------------- the rule on a Stage0 state
def corner_slots(st):
    return [it for it in st.items if it["i"] == 0 and it["j"] == 0]


def role_pieces(st, name):
    """[(container rect, t0, t1)] of a named role's alive pieces."""
    if name == st.H:
        return [(p[2], p[4][0], p[4][1]) for p in st.hpieces]
    v = st.other_h.get(name)
    return [(tuple(float(x) for x in v[:4]), float(v[4]), float(v[5]))] if v is not None else []


def mark_coarse(st, pc):
    """the coarse sub-rect (the page's drawing unit) a killed piece lies in, lettered Q."""
    ci = pc[0]
    tab = st.__dict__.setdefault("_cc_sub", {})
    if ci not in tab:
        tab[ci] = [(rr, rf) for (c, si), (rf, rr) in st.sub.items() if c == ci]
    for rr, rf in tab[ci]:
        if rr[0] - EPS <= pc[2][0] and pc[2][1] <= rr[1] + EPS and rr[2] - EPS <= pc[2][2] and pc[2][3] <= rr[3] + EPS:
            st.letters_cc[(ci, rf[1])] = "Q"
            return


def cell_hulls(st, p):
    """the alive anonymous candidates of slot p, one bounding rect per grid cell (a sound over-approximation)."""
    by = {}
    for pc in (st.alive.get(p) or []):
        r = by.get(pc[0])
        by[pc[0]] = (min(r[0], pc[2][0]), max(r[1], pc[2][1]), min(r[2], pc[2][2]), max(r[3], pc[2][3])) if r else tuple(pc[2])
    return by


def apply_cc(st, rnd):
    """rule CC on every corner slot p and every non-pin role R near that corner (Lemma CORNER-COVER):
      (i) an anonymous piece of p that reaches NO pose class's band of R cannot be the second meeter -> dead (Q);
     (ii) a pose class of R that leaves NO candidate second meeter at all (no anonymous piece, no other role) is
          impossible by Theorem FC -> R's pieces in it are dead (H's pieces are dropped; a role reduced to nothing
          kills the page).
    The band of the LAST R examined is kept for h_may_meet's H-reach test."""
    t0 = time.perf_counter()
    lam, rec = float(st.lam_cc), dict(round=rnd, slots=[], killed=0, h_killed=0)
    st.cc_band = {}
    for it in corner_slots(st):
        p, corner = it["cell"], it["corner"]
        names = [st.H] + list(st.other_h)
        for name in names:
            pcs = role_pieces(st, name)
            if not pcs:
                continue
            bands = piece_bands(pcs, corner, st.s, lam)
            if not bands:
                continue
            all_near = all(k[2] <= NEAR and k[3] <= NEAR for k, _ in bands)
            allb = [w for _, ws in bands for w in ws]
            n0 = len(st.alive.get(p) or [])
            keep = list(st.alive.get(p) or [])
            if all_near:                                                       # (i) the anonymous meeters
                keep = []
                for pc in (st.alive.get(p) or []):
                    if reaches(pc[2], pc[3].wmax, allb, lam):
                        keep.append(pc)
                    else:
                        st.letters[(pc[0], pc[1], pc[3].t0)] = "Q"
                        mark_coarse(st, pc)
                st.alive[p] = keep
            hulls = list(cell_hulls(st, p).values())
            others = [(tuple(float(x) for x in v[:4]), SQ2) for k, v in st.other_h.items() if k != name]
            if name != st.H and st.hhull:
                others.append((tuple(st.hhull), SQ2))
            dead_keys = set()                                                  # (ii) the pose classes of R
            for key, ws in bands:
                if key[2] > NEAR or key[3] > NEAR:                             # not a corner square: no claim
                    continue
                if any(reaches(r, SQ2, ws, lam) for r in hulls) or any(reaches(r, w, ws, lam) for r, w in others):
                    continue
                dead_keys.add(key)
            if dead_keys and name == st.H:
                nh = len(st.hpieces)
                st.hpieces = [hp for hp in st.hpieces if _key_of(hp, corner, st.s) not in dead_keys]
                rec["h_killed"] += nh - len(st.hpieces)
                if not st.hpieces:
                    st.verdict_leaf = ("rule CC (Lemma CORNER-COVER) at %s: every pose of %s near the corner leaves no "
                                       "second non-pin meeter of the slot (Theorem FC demands 2)" % (p, name))
                else:
                    st.refresh_H()
            elif dead_keys:
                st.verdict_leaf = ("rule CC (Lemma CORNER-COVER) at %s: role %s is at the corner and no second non-pin "
                                   "meeter of the slot can reach the wall wedges (Theorem FC demands 2)" % (p, name))
            if all_near:
                st.cc_band[p] = dict(who=name, band=allb, lam=lam)
            rec["killed"] += n0 - len(keep)
            rec["slots"].append(dict(slot=p, corner=corner, near_corner=name, n_classes=len(bands), n_band=len(allb),
                                     pieces_before=n0, pieces_after=len(keep), dead_classes=len(dead_keys), all_near=all_near,
                                     cells_after=sorted({pc[0] for pc in keep}),
                                     band=[[round(v, 6) for v in w] for w in allb[:12]]))
            if st.verdict_leaf:
                break
        if st.verdict_leaf:
            break
    rec["ms"] = round(1000 * (time.perf_counter() - t0), 2)
    st.tally("Q", rec["killed"] + rec["h_killed"], time.perf_counter() - t0)
    st.cc.append(rec)
    return rec


def _key_of(hp, corner, s):
    fr = to_frame(hp[2], corner, s)
    a, b = frame_tilt(hp[4][0], hp[4][1], corner)
    hmin = min(_h(a), _h(b))
    return (round(a, 6), round(b, 6), round(max(0.0, fr[1] - hmin), 6), round(max(0.0, fr[3] - hmin), 6))


def h_blocked(st, hp, p):
    """True when rule CC forbids H's piece from being a second meeter of the corner slot p (H is not itself the
    pushed-in square there)."""
    b = getattr(st, "cc_band", {}).get(p)
    if not b or b["who"] == st.H:
        return False
    return not reaches(hp[2], hp[3].wmax, b["band"], b["lam"])
