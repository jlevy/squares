"""Self-test of this review's checker: answers derived by hand, and broken copies.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

    python -I -B r1_selftest.py OUT.json

It reads no certificate.  It holds the readers (r1_read), method A (r1_axes),
method B (r1_area), the closed form (r1_frame), the decision (r1_decide), the twin
comparison (r1_twin) and the printing (r1_fmt) to configurations whose margins,
classes and areas are derived by hand in the comments below, and to malformed
files the readers must refuse.

Then it runs the same suite against broken copies of the programs, each made by
one stated replacement in a program's source text (the replacement must occur
exactly once; one copy makes three replacements together), and requires every broken
copy to fail.

One broken copy needs its three replacements: method B finds a point of contact
twice, as a vertex of one square that lies in the other (a closed test) and as a
point where two edges meet (a closed test), so opening either test alone changes
nothing; opening both loses the contact.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
import types
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ("r1_fmt", "r1_read", "r1_axes", "r1_area", "r1_frame", "r1_decide", "r1_twin")
E30 = F(1, 10**30)

MUTANTS = (
    ("A uses only the first square's two directions", "r1_axes",
     "    for owner in (si, sj):", "    for owner in (si,):"),
    ("A counts a zero margin as apart", "r1_axes",
     "    if value > 0:\n        return \"apart\"", "    if value >= 0:\n        return \"apart\""),
    ("A measures the separation on one side only", "r1_axes",
     "num = max(min(pj) - max(pi), min(pi) - max(pj))", "num = min(pj) - max(pi)"),
    ("A's unit test drops perpendicularity", "r1_axes",
     "    if E[0][0] * E[1][0] + E[0][1] * E[1][1] != 0:", "    if False:"),
    ("A's right clearance uses the least x", "r1_axes",
     "        side - Fraction(max(xs), D),", "        side - Fraction(min(xs), D),"),
    ("B's point-in-polygon test and its crossing test are both open", "r1_area",
     ("        if (bx - ax) * (py - ay) - (by - ay) * (px - ax) < 0:",
      "            if t < 0 or t > 1:", "            if u < 0 or u > 1:"),
     ("        if (bx - ax) * (py - ay) - (by - ay) * (px - ax) <= 0:",
      "            if t <= 0 or t >= 1:", "            if u <= 0 or u >= 1:")),
    ("B skips the edge crossings", "r1_area",
     "            if den == 0:\n                continue", "            if True:\n                continue"),
    ("B's unit test drops the diagonals", "r1_area",
     "    diagonals = _d2(points[0], points[2]) == TWO and _d2(points[1], points[3]) == TWO",
     "    diagonals = True"),
    ("B calls fewer than three contact points apart", "r1_area",
     "    if not candidates:\n        return apart_word, ZERO",
     "    if len(candidates) < 3:\n        return apart_word, ZERO"),
    ("B's wall test is open", "r1_area",
     "    candidates = [p for p, f in zip(P, values) if f >= 0]",
     "    candidates = [p for p, f in zip(P, values) if f > 0]"),
    ("the closed form's half-extent is doubled", "r1_frame",
     "    return (abs(_dot(frame.u, w)) + abs(_dot(frame.v, w))) / 2",
     "    return abs(_dot(frame.u, w)) + abs(_dot(frame.v, w))"),
    ("the YAML reader lets a duplicate key through", "r1_read",
     "                if key in mapping:", "                if False:"),
    ("the witness reader ignores the stated count", "r1_read",
     "    if len(listed) != n:\n        raise Refusal(f\"witness.n states",
     "    if False:\n        raise Refusal(f\"witness.n states"),
    ("the decision ignores wall crossings", "r1_decide",
     "            if self.clear[k][w] < 0 or self.wall_b[k][w][0] == \"overlapping\"",
     "            if False"),
)


def replacements(mutation):
    """A broken copy's replacements: one, or several made together."""
    olds, news = mutation[2], mutation[3]
    if isinstance(olds, str):
        olds, news = (olds,), (news,)
    return olds, news


def load(mutation=None):
    """Fresh copies of the seven modules, one of them optionally mutated."""
    saved = {name: sys.modules.get(name) for name in ORDER}
    mods = {}
    try:
        for name in ORDER:
            with open(os.path.join(HERE, name + ".py")) as handle:
                source = handle.read()
            if mutation is not None and mutation[1] == name:
                for old, new in zip(*replacements(mutation)):
                    if source.count(old) != 1:
                        raise SystemExit(f"mutation {mutation[0]!r}: pattern occurs "
                                         f"{source.count(old)} times in {name}.py")
                    source = source.replace(old, new)
            module = types.ModuleType(name)
            module.__file__ = os.path.join(HERE, name + ".py")
            sys.modules[name] = module
            exec(compile(source, name + ".py", "exec"), module.__dict__)
            mods[name[3:]] = module
    finally:
        for name, module in saved.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module
    return types.SimpleNamespace(**mods)


class Tally:
    def __init__(self):
        self.total = 0
        self.failed = 0
        self.first = []

    def check(self, name, condition):
        self.total += 1
        if not condition:
            self.failed += 1
            if len(self.first) < 12:
                self.first.append(name)


# ------------------------------------------------------------ geometry helpers

PYTH = ((F(1), F(0)), (F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17)),
        (F(20, 29), F(21, 29)))


def upright(x, y):
    x, y = F(x), F(y)
    return [(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)]


def move(points, rot, shift, mirror=False):
    """A rigid motion of the plane: optional mirror in the y axis, a turn, a shift."""
    c, s = rot
    out = []
    for x, y in points:
        if mirror:
            x = -x
        out.append((c * x - s * y + shift[0], s * x + c * y + shift[1]))
    return out


def listings(points):
    """The eight listings of a quadrilateral: from each corner, in both senses."""
    for start in range(4):
        yield [points[(start + m) % 4] for m in range(4)]
        yield [points[(start - m) % 4] for m in range(4)]


def cls_of(value):
    return "apart" if value > 0 else ("touching" if value == 0 else "overlapping")


def ref_clip_area(P, Q):
    """Reference area of the intersection of two counterclockwise convex polygons, by
    successive clipping (Sutherland-Hodgman) in fractions.  Used only to check B."""
    poly = list(P)
    for k in range(len(Q)):
        ax, ay = Q[k]
        bx, by = Q[(k + 1) % len(Q)]
        nxt = []
        for m in range(len(poly)):
            p, q = poly[m], poly[(m + 1) % len(poly)]
            fp = (bx - ax) * (p[1] - ay) - (by - ay) * (p[0] - ax)
            fq = (bx - ax) * (q[1] - ay) - (by - ay) * (q[0] - ax)
            if fp >= 0:
                nxt.append(p)
            if (fp > 0 > fq) or (fq > 0 > fp):
                t = fp / (fp - fq)
                nxt.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        poly = nxt
        if not poly:
            return F(0)
    twice = sum(poly[m][0] * poly[(m + 1) % len(poly)][1]
                - poly[(m + 1) % len(poly)][0] * poly[m][1] for m in range(len(poly)))
    return abs(twice) / 2


def ccw(points):
    twice = sum(points[m][0] * points[(m + 1) % 4][1] - points[(m + 1) % 4][0] * points[m][1]
                for m in range(4))
    return list(points) if twice > 0 else list(reversed(points))


def pair_checks(t, m, name, P, Q, margin, area):
    """Hold A, the closed form and B to a pair's hand-derived margin and overlap area."""
    a_p, a_q = m.axes.from_corners(P), m.axes.from_corners(Q)
    t.check(name + " A unit", a_p.unit and a_q.unit)
    t.check(name + " A margin", m.axes.margin(a_p, a_q) == margin)
    t.check(name + " A margin, other order", m.axes.margin(a_q, a_p) == margin)
    t.check(name + " A class", m.axes.classify(margin) == cls_of(margin))
    f_p, f_q = m.frame.from_corners(P), m.frame.from_corners(Q)
    t.check(name + " closed form", m.frame.margin(f_p, f_q) == margin)
    b_p = m.area.counterclockwise(m.area.points_from_corners(P))
    b_q = m.area.counterclockwise(m.area.points_from_corners(Q))
    for first, second, tag in ((b_p, b_q, ""), (b_q, b_p, ", other order")):
        got_cls, got_area = m.area.pair(first, second)
        t.check(name + " B class" + tag, got_cls == cls_of(margin))
        t.check(name + " B area" + tag, m.decide.from_mpq(got_area) == area)


# ------------------------------------------------------------ the suite


def suite_pairs(t, m):
    shifts = ((F(0), F(0)), (F(7, 3), F(-11, 5)))
    deltas = (E30, F(0), -E30, F(1, 7), F(-1, 7))
    # Edge contacts.  A = [0,1]^2 and B = A shifted by (1 + d, tau) (right edge), and the
    # three quarter turns of that.  On x the separation is d, on y it is tau - 1 < d, so
    # the margin is d; for d < 0 the overlap is a |d| by (1 - tau) rectangle.
    for rot in PYTH:
        for shift in shifts:
            for mirror in (False, True):
                for quarter in range(4):
                    for tau in (F(0), F(1, 3), F(2, 3)):
                        for d in deltas:
                            A = upright(0, 0)
                            B = upright(1 + d, tau)
                            for _ in range(quarter):
                                A = [(-y, x) for x, y in A]
                                B = [(-y, x) for x, y in B]
                            A = move(A, rot, shift, mirror)
                            B = move(B, rot, shift, mirror)
                            area = abs(d) * (1 - tau) if d < 0 else F(0)
                            pair_checks(t, m, f"edge {rot} q{quarter} tau {tau} d {d}",
                                        A, B, d, area)
    # Corner contacts.  B = A shifted by (+-(1 + d), +-(1 + d)): the separation is d on
    # both axes, so the margin is d; for d < 0 the overlap is a |d| by |d| square.
    for rot in PYTH:
        for sx, sy in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            for d in deltas:
                A = move(upright(0, 0), rot, shifts[1])
                B = move(upright(sx * (1 + d), sy * (1 + d)), rot, shifts[1])
                pair_checks(t, m, f"corner {rot} {sx}{sy} d {d}", A, B, d,
                            d * d if d < 0 else F(0))
    # Listings: the margin and the area do not depend on where a listing starts or on
    # its sense.
    A = move(upright(0, 0), PYTH[1], shifts[1])
    for d in (E30, F(0), -E30):
        B = move(upright(1 + d, F(1, 3)), PYTH[1], shifts[1])
        for la in listings(A):
            for lb in listings(B):
                pair_checks(t, m, f"listing d {d}", la, lb, d,
                            abs(d) * F(2, 3) if d < 0 else F(0))
    # A corner on an edge.  A = [0,1]^2; B has its lowest corner p = (1/2, 1 + d) and
    # edges along u = (c, s) and v = (-s, c), both rising.  On A's y direction the
    # separation is d; on the other three it is below -9/50 (worked in the review's
    # design notes for 3-4-5, 5-12-13 and 8-15-17), so the margin is d.  For d < 0 the
    # line y = 1 cuts a right triangle off B's corner with legs |d|/s and |d|/c:
    # area d^2 / (2 s c).
    for c, s in ((F(4, 5), F(3, 5)), (F(12, 13), F(5, 13)), (F(15, 17), F(8, 17))):
        for d in (E30, F(0), -E30, F(-1, 100)):
            p = (F(1, 2), 1 + d)
            B = [p, (p[0] + c, p[1] + s), (p[0] + c - s, p[1] + s + c), (p[0] - s, p[1] + c)]
            for rot in PYTH[:3]:
                pair_checks(t, m, f"corner-on-edge {c} d {d} {rot}",
                            move(upright(0, 0), rot, shifts[1]), move(B, rot, shifts[1]),
                            d, d * d / (2 * s * c) if d < 0 else F(0))
    # A duplicate: margin -1, area 1.
    pair_checks(t, m, "duplicate", upright(2, 3), upright(2, 3), F(-1), F(1))
    # A square and its concentric turn by (c, s): on the upright square's x direction
    # the turned square's half-extent is (c + s)/2, so the separation there is
    # -(1 + c + s)/2, and by symmetry it is the same on all four; each corner of the
    # upright square loses a right triangle with legs (c+s-1)/(2c) and (c+s-1)/(2s), so
    # the common area is 1 - (c + s - 1)^2 / (2 c s).
    for c, s, margin, area in ((F(3, 5), F(4, 5), F(-6, 5), F(5, 6)),
                               (F(5, 13), F(12, 13), F(-15, 13), F(13, 15))):
        t.check("concentric formulas", margin == -(1 + c + s) / 2
                and area == 1 - (c + s - 1) ** 2 / (2 * c * s))
        A = upright(F(-1, 2), F(-1, 2))
        B = move(A, (c, s), (F(0), F(0)))
        pair_checks(t, m, f"concentric {c}", A, B, margin, area)


def suite_walls(t, m):
    side = F(5)
    for c, s in PYTH:
        H = (abs(c) + abs(s)) / 2
        for w, wall in enumerate(m.frame.WALLS):
            for eps in (E30, F(0), -E30, F(-1, 100)):
                # centre at distance H + eps from the wall, mid-box on the other axis
                centre = {"left": (H + eps, F(5, 2)), "bottom": (F(5, 2), H + eps),
                          "right": (side - H - eps, F(5, 2)), "top": (F(5, 2), side - H - eps)}[wall]
                square = (centre[0], centre[1], c, s)
                a = m.axes.from_centre(*square)
                name = f"wall {wall} {c} eps {eps}"
                t.check(name + " A unit", a.unit)
                t.check(name + " A", m.axes.clearances(a, side)[w] == eps)
                t.check(name + " closed form",
                        m.frame.clearances(m.frame.from_centre(*square), side)[w] == eps)
                pts = m.area.counterclockwise(m.area.points_from_centre(*square))
                t.check(name + " B unit", m.area.unit_square(pts)[0])
                got = m.area.walls(pts, side)[w]
                want = {"apart": "apart", "touching": "touching",
                        "overlapping": "overlapping"}[cls_of(eps)]
                t.check(name + " B class", got[0] == want)
                # outside area: an upright square loses a |eps| by 1 strip; a tilted one
                # a right triangle of area eps^2 / (2 c s)
                if eps < 0:
                    outside = -eps if s == 0 else eps * eps / (2 * c * s)
                else:
                    outside = F(0)
                t.check(name + " B outside area", m.decide.from_mpq(got[1]) == outside)
                t.check(name + " B inside area",
                        m.decide.from_mpq(m.area.area_inside_box(pts, side)) == 1 - outside)
                others = [m.area.walls(pts, side)[x][0] for x in range(4) if x != w]
                t.check(name + " B other walls", others == ["apart"] * 3)


def suite_unit(t, m):
    for c, s in PYTH:
        base = move(upright(0, 0), (c, s), (F(2), F(3)))
        for index, listing in enumerate(listings(base)):
            a = m.axes.from_corners(listing)
            ok_b, sense_b = m.area.unit_square(m.area.points_from_corners(listing))
            want = 1 if index % 2 == 0 else -1
            t.check(f"unit {c} listing {index}", a.unit and ok_b)
            t.check(f"sense {c} listing {index}", a.sense == want and sense_b == want)
        a = m.axes.from_centre(F(2), F(3), c, s)
        pts = m.area.points_from_centre(F(2), F(3), c, s)
        t.check(f"centre form unit {c}", a.unit and m.area.unit_square(pts)[0])
        t.check(f"centre form sense {c}", a.sense == 1 and m.area.unit_square(pts)[1] == 1)
        t.check(f"centre form corners agree {c}",
                [(F(int(x.numerator), int(x.denominator)), F(int(y.numerator), int(y.denominator)))
                 for x, y in pts] == [(F(qx, a.D), F(qy, a.D)) for qx, qy in a.Q])
    P = upright(0, 0)
    bad = {
        "corner off by 1e-30": [(P[0][0] + E30, P[0][1])] + P[1:],
        "bowtie": [P[0], P[2], P[1], P[3]],
        "rhombus with unit sides": [(F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "1 by 1+1e-30 rectangle": [(F(0), F(0)), (F(1), F(0)), (F(1), 1 + E30), (F(0), 1 + E30)],
        "side 2": [(F(0), F(0)), (F(2), F(0)), (F(2), F(2)), (F(0), F(2))],
        "a point four times": [P[0]] * 4,
        "a repeated corner": [P[0], P[0], P[2], P[3]],
        "a folded rhombus": [P[0], P[1], P[0], P[1]],
        "parallelogram": [(F(0), F(0)), (F(1), F(0)), (F(2), F(1)), (F(1), F(1))],
    }
    for name, shape in bad.items():
        t.check("refuse A: " + name, not m.axes.from_corners(shape).unit)
        t.check("refuse B: " + name, not m.area.unit_square(m.area.points_from_corners(shape))[0])
    for ux, uy in ((F(3, 5), F(4, 5) + E30), (F(1), F(1)), (F(0), F(0)), (F(2), F(0)),
                   (F(1, 2), F(1, 2)), (F(3, 5) + E30, F(4, 5))):
        t.check(f"refuse A direction {ux},{uy}", not m.axes.from_centre(F(1), F(1), ux, uy).unit)
        t.check(f"refuse B direction {ux},{uy}",
                not m.area.unit_square(m.area.points_from_centre(F(1), F(1), ux, uy))[0])


def random_direction(rng, big):
    a = rng.randrange(2, big)
    b = rng.randrange(1, a)
    c, s = F(a * a - b * b, a * a + b * b), F(2 * a * b, a * a + b * b)
    for _ in range(rng.randrange(4)):
        c, s = -s, c
    return c, s


def suite_random(t, m):
    rng = random.Random(1005)
    for trial in range(400):
        big = 10 ** rng.choice((2, 4, 7))
        ci, si = random_direction(rng, big)
        cj, sj = random_direction(rng, big)
        reach = rng.choice((F(1, 2), F(1), F(3, 2), F(5, 2)))
        sq_i = (F(rng.randrange(-10**6, 10**6), 10**6), F(rng.randrange(-10**6, 10**6), 10**6), ci, si)
        dx = F(rng.randrange(-10**6, 10**6), 10**6) * reach
        dy = F(rng.randrange(-10**6, 10**6), 10**6) * reach
        sq_j = (sq_i[0] + dx, sq_i[1] + dy, cj, sj)
        fi, fj = m.frame.from_centre(*sq_i), m.frame.from_centre(*sq_j)
        want = m.frame.margin(fi, fj)
        ai, aj = m.axes.from_centre(*sq_i), m.axes.from_centre(*sq_j)
        name = f"random {trial}"
        t.check(name + " A = closed form", m.axes.margin(ai, aj) == want == m.axes.margin(aj, ai))
        bi = m.area.counterclockwise(m.area.points_from_centre(*sq_i))
        bj = m.area.counterclockwise(m.area.points_from_centre(*sq_j))
        got_cls, got_area = m.area.pair(bi, bj)
        t.check(name + " B class", got_cls == cls_of(want))
        back_cls, back_area = m.area.pair(bj, bi)
        t.check(name + " B both orders", (back_cls, back_area) == (got_cls, got_area))
        # B's area against successive clipping, an algorithm B does not use
        ref_i = ccw(m.twin.corner_list("centre", sq_i))
        ref_j = ccw(m.twin.corner_list("centre", sq_j))
        t.check(name + " B area = clipped area",
                m.decide.from_mpq(got_area) == ref_clip_area(ref_i, ref_j))
        if dx == 0 and dy == 0:
            continue
        for target in (E30, F(0), -E30):
            shift = m.frame.closing_shift(fi, fj, target)
            moved = m.frame.translate_square("centre", sq_j, shift)
            am = m.axes.from_centre(*moved)
            t.check(name + f" closed to {target}: A", m.axes.margin(ai, am) == target
                    and m.axes.margin(am, ai) == target)
            t.check(name + f" closed to {target}: closed form",
                    m.frame.margin(fi, m.frame.from_centre(*moved)) == target)
            bm = m.area.counterclockwise(m.area.points_from_centre(*moved))
            cls_m, area_m = m.area.pair(bi, bm)
            t.check(name + f" closed to {target}: B", cls_m == cls_of(target)
                    and (area_m > 0) == (target < 0))
    for trial in range(120):
        c, s = random_direction(rng, 10**5)
        side = F(9)
        sq = (F(rng.randrange(10**6, 8 * 10**6), 10**6), F(rng.randrange(10**6, 8 * 10**6), 10**6), c, s)
        a = m.axes.from_centre(*sq)
        clear = m.axes.clearances(a, side)
        t.check(f"random wall {trial} closed form",
                m.frame.clearances(m.frame.from_centre(*sq), side) == clear)
        for w, wall in enumerate(m.frame.WALLS):
            for extra, want in ((-E30, "apart"), (F(0), "touching"), (E30, "overlapping")):
                moved = m.frame.translate_square("centre", sq, m.frame.wall_shift(wall, clear[w] + extra))
                am = m.axes.from_centre(*moved)
                t.check(f"random wall {trial} {wall} {want}: A",
                        m.axes.clearances(am, side)[w] == -extra)
                pts = m.area.counterclockwise(m.area.points_from_centre(*moved))
                t.check(f"random wall {trial} {wall} {want}: B",
                        m.area.walls(pts, side)[w][0] == want)
                t.check(f"random wall {trial} {wall} {want}: B inside",
                        (m.area.area_inside_box(pts, side) == 1) == (want != "overlapping"))


def grid(k, gap=F(0)):
    return [upright((1 + gap) * i, (1 + gap) * j) for j in range(k) for i in range(k)]


def as_form(form, corner_squares):
    """Upright or turned squares given by corners, in the reader's two forms."""
    if form == "corners":
        return [tuple(sq) for sq in corner_squares]
    out = []
    for sq in corner_squares:
        cx, cy = (sq[0][0] + sq[2][0]) / 2, (sq[0][1] + sq[2][1]) / 2
        out.append((cx, cy, sq[1][0] - sq[0][0], sq[1][1] - sq[0][1]))
    return out


def decide_text(m, kind, n, side, squares):
    form = "centre" if kind == "centre-json" else "corners"
    raw = m.read.WRITERS[kind](n, side, as_form(form, squares))
    packing = m.read.READERS[kind](raw)
    dec, _, _ = m.decide.decide(packing)
    return packing, dec


def suite_files(t, m):
    for kind in ("witness-yaml", "witness-json", "centre-json"):
        # 2 by 2 grid in a box of side 2: all six pairs touch (four along an edge, two
        # at a corner); each square touches two walls.
        packing, dec = decide_text(m, kind, 4, F(2), grid(2))
        verdict, reasons = dec.verdict()
        t.check(kind + " 2x2 accepted", verdict == "ACCEPT" and reasons == [])
        t.check(kind + " 2x2 six touching pairs",
                sorted(dec.margin.values()) == [F(0)] * 6
                and set(dec.class_b.values()) == {"touching"})
        t.check(kind + " 2x2 eight wall contacts",
                sum(1 for k in range(4) for w in range(4) if dec.clear[k][w] == 0) == 8
                and sum(1 for k in range(4) for w in range(4) if dec.wall_b[k][w][0] == "touching") == 8)
        # the same grid in a box 1e-30 too small: squares 2 and 4 cross the right wall
        # and squares 3 and 4 the top wall
        _, dec = decide_text(m, kind, 4, 2 - E30, grid(2))
        verdict, reasons = dec.verdict()
        t.check(kind + " 2x2 box too small", verdict == "REFUSE" and reasons == [
            ("crossing", [(2, "right"), (3, "top"), (4, "right"), (4, "top")]),
            ("area-inside-below-1", [2, 3, 4])])
        # 3 by 3 grid: 12 pairs share an edge, 8 a corner, 16 are apart by 1
        _, dec = decide_text(m, kind, 9, F(3), grid(3))
        values = sorted(dec.margin.values())
        t.check(kind + " 3x3", dec.verdict()[0] == "ACCEPT" and values == [F(0)] * 20 + [F(1)] * 16
                and sorted(dec.class_b.values()) == ["apart"] * 16 + ["touching"] * 20)
        # a loose 3 by 3 grid, gap 1/1000: least margin 1/1000 at 12 pairs
        _, dec = decide_text(m, kind, 9, 3 + F(2, 1000), grid(3, F(1, 1000)))
        values = sorted(dec.margin.values())
        t.check(kind + " loose 3x3", dec.verdict()[0] == "ACCEPT"
                and values[:20] == [F(1, 1000)] * 20 and values[20] == 1 + F(2, 1000)
                and set(dec.class_b.values()) == {"apart"})
        # a duplicate square
        squares = grid(2) + [upright(1, 1)]
        _, dec = decide_text(m, kind, 5, F(2), squares)
        verdict, reasons = dec.verdict()
        t.check(kind + " duplicate", verdict == "REFUSE" and reasons == [("overlapping", [(4, 5)])]
                and dec.margin[(4, 5)] == -1 and dec.area_b[(4, 5)] == 1)
        # a 3-4-5 square alone in the box of side 7/5 touches all four walls
        turned = move(upright(F(-1, 2), F(-1, 2)), (F(3, 5), F(4, 5)), (F(7, 10), F(7, 10)))
        _, dec = decide_text(m, kind, 1, F(7, 5), [turned])
        t.check(kind + " 3-4-5 in its box", dec.verdict()[0] == "ACCEPT"
                and dec.clear[0] == (0, 0, 0, 0)
                and [c for c, _ in dec.wall_b[0]] == ["touching"] * 4 and dec.inside_b[0] == 1)
        _, dec = decide_text(m, kind, 1, F(7, 5) - E30, [turned])
        t.check(kind + " 3-4-5 box too small", dec.verdict() == ("REFUSE", [
            ("crossing", [(1, "right"), (1, "top")]), ("area-inside-below-1", [1])]))
        # a square that is not unit is named, and the rest is still decided
        squares = grid(2)
        if kind == "centre-json":
            raw = m.read.write_centre_json(4, F(2), [(F(1, 2), F(1, 2), F(1) + E30, F(0))]
                                           + as_form("centre", squares[1:]))
        else:
            broken = [(squares[0][0][0] + E30, squares[0][0][1])] + squares[0][1:]
            raw = m.read.WRITERS[kind](4, F(2), [tuple(broken)] + [tuple(s) for s in squares[1:]])
        dec, _, _ = m.decide.decide(m.read.READERS[kind](raw))
        verdict, reasons = dec.verdict()
        t.check(kind + " not unit", verdict == "REFUSE" and reasons == [("not-unit", [1])]
                and len(dec.margin) == 3)
        # redecide: moving square 4 of the loose grid by its gap brings it to contact
        packing, dec = decide_text(m, kind, 9, 3 + F(2, 1000), grid(3, F(1, 1000)))
        base = (dec, None, None)
        form = packing.form
        moved = list(packing.squares)
        moved[8] = m.frame.translate_square(form, moved[8], (F(-1, 1000), F(0)))
        again = m.read.Packing(form, 9, packing.side, moved, packing.ids, {})
        fresh, _, _ = m.decide.decide(again)
        patched, _, _ = m.decide.redecide(again, base, {8})
        t.check(kind + " redecide equals a fresh decision",
                fresh.margin == patched.margin and fresh.class_b == patched.class_b
                and fresh.clear == patched.clear and fresh.wall_b == patched.wall_b
                and fresh.verdict() == patched.verdict() and fresh.margin[(8, 9)] == 0)
    # twins: the same packing in two forms, and one square moved by 1e-30
    squares = grid(3, F(1, 1000)) + [move(upright(F(-1, 2), F(-1, 2)), (F(3, 5), F(4, 5)), (F(9), F(9)))]
    pa = m.read.read_witness_yaml(m.read.write_witness_yaml(10, F(12), as_form("corners", squares)))
    pb = m.read.read_centre_json(m.read.write_centre_json(10, F(12), as_form("centre", squares)))
    same = m.twin.compare(pb, pa)
    t.check("twin same", same["same_packing"] and same["equal_as_collections"]
            and same["second_file_listing_relative_to_first"]
            == {"same sense, from corner 0 of the first file's listing": 10})
    shifted = as_form("centre", squares)
    shifted[6] = m.frame.translate_square("centre", shifted[6], (E30, F(0)))
    pc = m.read.read_centre_json(m.read.write_centre_json(10, F(12), shifted))
    diff = m.twin.compare(pc, pa)
    t.check("twin differs in one square", not diff["same_packing"]
            and diff["unequal_in_file_order"] == {"count": 1, "first": [7]}
            and not diff["equal_as_collections"])
    swapped = as_form("corners", squares)
    swapped[0], swapped[1] = swapped[1], swapped[0]
    pd = m.read.read_witness_yaml(m.read.write_witness_yaml(10, F(12), swapped))
    perm = m.twin.compare(pb, pd)
    t.check("twin as collections", not perm["same_packing"] and perm["equal_as_collections"]
            and perm["unequal_in_file_order"]["first"] == [1, 2])
    t.check("twin side", not m.twin.compare(
        pb, m.read.read_witness_yaml(m.read.write_witness_yaml(10, F(12) + E30, as_form("corners", squares)))
    )["same_packing"])


def refused(m, kind, raw):
    try:
        m.read.READERS[kind](raw)
    except m.read.Refusal:
        return True
    return False


def suite_reader(t, m):
    squares = grid(2, F(1, 3))
    side = F(7, 3)
    for kind in ("witness-yaml", "witness-json", "centre-json"):
        form = "centre" if kind == "centre-json" else "corners"
        raw = m.read.WRITERS[kind](4, side, as_form(form, squares))
        packing = m.read.READERS[kind](raw)
        t.check(kind + " round trip", packing.n == 4 and packing.side == side
                and [tuple(s) for s in packing.squares] == [tuple(s) for s in as_form(form, squares)])
        t.check(kind + " canonical", packing.notes["scalars_in_lowest_terms"] == packing.notes["scalars"])
    good = m.read.write_witness_yaml(4, side, as_form("corners", squares)).decode()
    t.check("yaml valid", not refused(m, "witness-yaml", good.encode()))

    def swap(old, new, count=1):
        if good.count(old) < 1:
            raise SystemExit(f"selftest: pattern {old!r} not in the valid YAML file")
        return good.replace(old, new, count)

    first_corner = "    - - '0'\n"
    yaml_bad = {
        "tab": swap("  n: 4", "  n:\t4"),
        "carriage return": swap("  n: 4\n", "  n: 4\r\n"),
        "byte-order mark": "\ufeff" + good,
        "anchor": swap("  - id: 1\n    corners:", "  - id: 1\n    corners: &a"),
        "alias": swap("  - id: 1\n    corners:", "  - id: 1\n    corners: &a").replace(
            "  - id: 2\n    corners:\n", "  - id: 2\n    corners: *a\n", 1),
        "explicit tag": swap("  n: 4", "  n: !!int 4"),
        "flow sequence": swap(first_corner + "      - '0'\n", "    - ['0', '0']\n"),
        "double-quoted scalar": swap("square_size: '1'", 'square_size: "1"'),
        "duplicate key": swap("  square_size: '1'\n", "  square_size: '1'\n  side: 8\n"),
        "duplicate key, larger side": swap("  square_size: '1'\n", "  square_size: '1'\n  side: 10/3\n"),
        "second document": good + "---\nwitness: {}\n",
        "directive": "%YAML 1.1\n---\n" + good,
        "count too large": swap("  n: 4", "  n: 5"),
        "count too small": swap("  n: 4", "  n: 3"),
        "count quoted": swap("  n: 4", "  n: '4'"),
        "count zero": swap("  n: 4", "  n: 0"),
        "plain integer corner": swap(first_corner, "    - - 0\n"),
        "decimal corner": swap(first_corner, "    - - 0.5\n"),
        "exponent corner": swap(first_corner, "    - - 1e3\n"),
        "signed corner": swap(first_corner, "    - - +1/2\n"),
        "leading zero": swap(first_corner, "    - - 01/2\n"),
        "zero denominator": swap(first_corner, "    - - 1/0\n"),
        "negative denominator": swap(first_corner, "    - - 1/-2\n"),
        "negative zero": swap(first_corner, "    - - '-0'\n"),
        "empty corner": swap(first_corner, "    - -\n"),
        "null corner": swap(first_corner, "    - - ~\n"),
        "boolean corner": swap(first_corner, "    - - yes\n"),
        "hexadecimal corner": swap(first_corner, "    - - 0x10\n"),
        "underscored corner": swap(first_corner, "    - - 1_000/3\n"),
        "corner with a comment": swap(first_corner, "    - - '0' # zero\n"),
        "decimal side": swap(f"  side: {m.read.scalar_text(side)}", "  side: 2.3334"),
        "integer side unquoted": swap(f"  side: {m.read.scalar_text(side)}", "  side: 3"),
        "unknown witness key": swap("  square_size: '1'\n", "  square_size: '1'\n  scale: '2'\n"),
        "missing claim": good[: good.index("  claim:")],
        "center-angle": swap("representation: corners", "representation: center-angle"),
        "decimal kind": swap("kind: rational", "kind: decimal"),
        "container-center": swap("origin: lower-left", "origin: container-center"),
        "other axes": swap("axes: x-right-y-up", "axes: x-left-y-up"),
        "square size 2": swap("square_size: '1'", "square_size: '2'"),
        "square size plain": swap("square_size: '1'", "square_size: 1"),
        "three corners": swap(first_corner + "      - '0'\n", ""),
        "five corners": swap(first_corner + "      - '0'\n", first_corner + "      - '0'\n" + first_corner + "      - '0'\n"),
        "point of three": swap(first_corner + "      - '0'\n", first_corner + "      - '0'\n      - '0'\n"),
        "extra key in a square": swap("  - id: 1\n", "  - id: 1\n    angle: '0'\n"),
        "duplicate id": swap("  - id: 2\n", "  - id: 1\n"),
        "id zero": swap("  - id: 2\n", "  - id: 0\n"),
        "other contract": swap("Witness/v2", "Witness/v1"),
        "other envelope": swap("envelope: witness", "envelope: record"),
        "extra top-level key": good + "extra: '1'\n",
        "not UTF-8": None,
    }
    for name, text in yaml_bad.items():
        raw = b"\xff\xfe" + good.encode() if text is None else text.encode()
        t.check("yaml changed: " + name, raw != good.encode())
        t.check("yaml refused: " + name, refused(m, "witness-yaml", raw))
    # written out of lowest terms is read and recorded, not refused
    loose = m.read.read_witness_yaml(swap(f"  side: {m.read.scalar_text(side)}", "  side: 14/6").encode())
    t.check("yaml side out of lowest terms", loose.side == side
            and not loose.notes["side_written_in_lowest_terms"]
            and loose.notes["scalars_in_lowest_terms"] == loose.notes["scalars"] - 1)
    named = m.read.read_witness_yaml(
        m.read.write_witness_yaml(4, side, as_form("corners", squares),
                                  ids=[f"square-{k}" for k in range(1, 5)]))
    t.check("yaml string ids", named.notes["id_form"] == "strings square-1 to square-n in order")

    jgood = m.read.write_witness_json(4, side, as_form("corners", squares)).decode()
    side_text = m.read.scalar_text(side)

    def jswap(old, new):
        if jgood.count(old) < 1:
            raise SystemExit(f"selftest: pattern {old!r} not in the valid JSON witness")
        return jgood.replace(old, new, 1)

    json_bad = {
        "float side": jswap(f'"side": "{side_text}"', '"side": 2.3334'),
        "integer side": jswap(f'"side": "{side_text}"', '"side": 3'),
        "duplicate key": jswap(f'"side": "{side_text}"', f'"side": "{side_text}", "side": "10/3"'),
        "null": jswap('"square_size": "1"', '"square_size": null'),
        "true": jswap('"square_size": "1"', '"square_size": true'),
        "count as a string": jswap('"n": 4', '"n": "4"'),
        "count too large": jswap('"n": 4', '"n": 5'),
        "NaN": jswap('"n": 4', '"n": NaN'),
        "signed scalar": jswap('"0"', '"+0"'),
        "integer corner": jswap('"0"', "0"),
        "trailing text": jgood + "{}",
        "unknown key": jswap('"square_size": "1"', '"square_size": "1", "scale": "2"'),
        "duplicate id": jswap('"id": 2', '"id": 1'),
        "center-basis": jswap('"representation": "corners"', '"representation": "center-basis"'),
    }
    for name, text in json_bad.items():
        t.check("json changed: " + name, text != jgood)
        t.check("json refused: " + name, refused(m, "witness-json", text.encode()))

    cgood = m.read.write_centre_json(4, side, as_form("centre", squares)).decode()

    def cswap(old, new):
        if cgood.count(old) < 1:
            raise SystemExit(f"selftest: pattern {old!r} not in the valid centre file")
        return cgood.replace(old, new, 1)

    centre_bad = {
        "format sentence changed": cswap("cos, sin]", "sin, cos]"),
        "float side": cswap(f'"side": "{side_text}"', '"side": 2.3334'),
        "duplicate key": cswap(f'"side": "{side_text}"', f'"side": "{side_text}",\n"side": "10/3"'),
        "count too large": cswap('"n": 4', '"n": 5'),
        "square size as a number": cswap('"square_size": "1"', '"square_size": 1'),
        "three scalars": cswap('"1",\n"0"\n]', '"1"\n]'),
        "five scalars": cswap('"1",\n"0"\n]', '"1",\n"0",\n"0"\n]'),
        "signed scalar": cswap('"1",\n"0"\n]', '"+1",\n"0"\n]'),
        "float scalar": cswap('"1",\n"0"\n]', '1.0,\n"0"\n]'),
        "extra top-level key": cswap('"n": 4', '"n": 4,\n"origin": "container-center"'),
        "missing format": cswap(f'"format": "{m.read.FORMAT_SENTENCE}",\n', ""),
    }
    for name, text in centre_bad.items():
        t.check("centre changed: " + name, text != cgood)
        t.check("centre refused: " + name, refused(m, "centre-json", text.encode()))


def suite_fmt(t, m):
    f = m.fmt
    t.check("fmt frac", f.frac(F(6, 4)) == "3/2" and f.frac(F(4, 2)) == "2")
    t.check("fmt dec", f.dec(F(-5, 3), 5) == "-1.66666" and f.dec(F(17590104218681834, 10**15), 12)
            == "17.590104218681")
    t.check("fmt sci", f.sci(F(112027011549, 10**22)) == "1.12027011549e-11"
            and f.sci(F(1, 10**30), 3) == "1.00e-30" and f.sci(F(-5, 3), 4) == "-1.666e0"
            and f.sci(F(0)) == "0" and f.sci(F(10**40), 2) == "1.0e40")
    t.check("fmt ceil", f.ceil_places(F(17590104218681834, 10**15), 12) == F(17590104218682, 10**12)
            and f.ceil_places(F(3, 2), 0) == 2 and f.ceil_places(F(-3, 2), 0) == -1
            and f.ceil_places(F(2), 12) == 2)
    t.check("fmt terminating", f.is_exact_decimal(F(1, 8)) and not f.is_exact_decimal(F(1, 3)))
    # closing two upright squares with centres 3 apart: tau = 1 - 1/3, the moved
    # centre lands 1 from the other
    fi, fj = m.frame.from_centre(F(0), F(0), F(1), F(0)), m.frame.from_centre(F(3), F(0), F(1), F(0))
    t.check("closing time", m.frame.closing_time(fi, fj, F(0)) == F(2, 3)
            and m.frame.closing_shift(fi, fj, F(0)) == (F(-2), F(0))
            and m.frame.closing_time(fi, fi, F(0)) is None)


def run_suite(m):
    t = Tally()
    for part in (suite_pairs, suite_walls, suite_unit, suite_random, suite_files, suite_reader,
                 suite_fmt):
        try:
            part(t, m)
        except SystemExit:
            raise
        except Exception as exc:  # a broken copy may crash; that is a failure of the copy
            t.check(f"{part.__name__} raised {type(exc).__name__}: {exc}", False)
    return t


def main(argv):
    if len(argv) != 2:
        raise SystemExit(__doc__)
    started = time.process_time()
    tally = run_suite(load())
    receipt = {
        "program": "r1_selftest.py",
        "lane": "R1 (c-review-1005-1117)",
        "checks": tally.total,
        "failed": tally.failed,
        "first_failures": tally.first,
        "broken_copies": [],
    }
    all_fail = True
    for mutation in MUTANTS:
        broken = run_suite(load(mutation))
        receipt["broken_copies"].append({
            "what": mutation[0], "program": mutation[1] + ".py",
            "replaced": [text.strip() for text in replacements(mutation)[0]],
            "by": [text.strip() for text in replacements(mutation)[1]],
            "checks": broken.total, "failed": broken.failed, "first_failure": broken.first[:1],
        })
        all_fail = all_fail and broken.failed > 0
    receipt["every_broken_copy_fails"] = all_fail
    receipt["verdict"] = "PASSED" if tally.failed == 0 and all_fail else "FAILED"
    receipt["cpu_seconds"] = round(time.process_time() - started, 1)
    with open(argv[1], "w") as handle:
        json.dump(receipt, handle, indent=1)
        handle.write("\n")
    print(receipt["verdict"], tally.total, "checks", tally.failed, "failed;",
          ", ".join(f"{b['failed']}" for b in receipt["broken_copies"]), "failures in the broken copies")
    return 0 if receipt["verdict"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
