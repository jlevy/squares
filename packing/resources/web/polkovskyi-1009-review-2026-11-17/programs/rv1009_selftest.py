"""Self-test of the readers, both methods, the forms and the closed forms.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

    python -I -B rv1009_selftest.py OUT.json

Reads no certificate. Every expected answer is derived by hand in the comments beside
it. The suite is run once as written and once under each of six deliberately broken
copies of the code, each of which must fail it.
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1009_axes as axes  # noqa: E402
import rv1009_clip as clip  # noqa: E402
import rv1009_decide as decide  # noqa: E402
import rv1009_files as files  # noqa: E402
import rv1009_forms as forms  # noqa: E402
import rv1009_geom as geom  # noqa: E402
import rv1009_reader as reader  # noqa: E402
import rv1009_write as write  # noqa: E402
from gmpy2 import mpq  # noqa: E402

F = Fraction
EPS = geom.PAST
DELTAS = (EPS, F(0), -EPS, F(1, 7), -F(1, 7))
ANGLES = (F(0), F(1, 2), F(2, 3), F(1, 4))  # directions (1,0), (3,4)/5, (5,12)/13, (15,8)/17


class Tally:
    def __init__(self) -> None:
        self.cases = 0
        self.failed = 0
        self.first: list[str] = []

    def check(self, ok: bool, label: str) -> None:
        self.cases += 1
        if not ok:
            self.failed += 1
            if len(self.first) < 12:
                self.first.append(label)


def pair(value: Fraction) -> tuple[int, int]:
    return value.numerator, value.denominator


def pose_of(row: geom.Row) -> axes.Pose:
    return axes.pose_from_xyt(pair(row[0]), pair(row[1]), pair(row[2]))


def quad_of(row: geom.Row) -> list[clip.Point]:
    corners = forms.corners_from_xyt(pair(row[0]), pair(row[1]), pair(row[2]))
    return clip.points(forms.pairs_of(corners))


def listings(corners: tuple) -> list[tuple]:
    """The eight listings of four corners: each start, both senses."""
    out = []
    for sense in (1, -1):
        for k in range(4):
            out.append(tuple(corners[(k + sense * m) % 4] for m in range(4)))
    return out


def a_class(margin: Fraction) -> str:
    return decide.A_CLASS[decide.sign(margin)]


def expected_class(margin: Fraction) -> str:
    return "apart" if margin > 0 else ("touch" if margin == 0 else "overlap")


def check_pair(
    tally: Tally,
    label: str,
    ri: geom.Row,
    rj: geom.Row,
    margin: Fraction,
    area: Fraction | None,
    *,
    all_listings: bool = True,
) -> None:
    """A pair with a known margin and, where derived, a known overlap area: method A both
    ways round, the Fraction closed form, the corner projections, method B on the eight
    listings of square j, and method A on the pose taken from each listing."""
    pi, pj = pose_of(ri), pose_of(rj)
    want = expected_class(margin)
    tally.check(axes.pair_margin(pi, pj) == margin, f"{label}: A margin")
    tally.check(axes.pair_margin(pj, pi) == margin, f"{label}: A margin, other order")
    tally.check(a_class(axes.pair_margin(pi, pj)) == want, f"{label}: A class")
    tally.check(axes.pair_sign(pi, pj) == decide.sign(margin), f"{label}: A sign")
    tally.check(geom.margin(ri, rj) == margin, f"{label}: closed form")
    ci = forms.corners_from_xyt(pair(ri[0]), pair(ri[1]), pair(ri[2]))
    cj = forms.corners_from_xyt(pair(rj[0]), pair(rj[1]), pair(rj[2]))
    tally.check(geom.corner_margin(ci, cj) == margin, f"{label}: corner projections")
    qi = clip.points(forms.pairs_of(ci))
    for idx, listing in enumerate(listings(cj) if all_listings else [cj]):
        raw = forms.pairs_of(listing)
        qj = clip.points(raw)
        sense = clip.unit_sense(qj)
        tally.check(sense == (1 if idx < 4 else -1), f"{label}: B sense, listing {idx}")
        if sense == 0:
            continue
        cls, got_area = clip.pair_class(qi, clip.counterclockwise(qj))
        tally.check(cls == want, f"{label}: B class, listing {idx}")
        if area is not None:
            tally.check(got_area == mpq(area.numerator, area.denominator), f"{label}: B area")
        try:
            pose, got_sense = forms.pose_from_corners(raw)
        except ValueError:
            tally.check(False, f"{label}: pose from corners, listing {idx}")
            continue
        tally.check(got_sense == (1 if idx < 4 else -1), f"{label}: pose sense")
        tally.check(axes.is_unit_pose(pose), f"{label}: pose is unit")
        tally.check(axes.pair_margin(pi, pose) == margin, f"{label}: A on pose from corners")


def t_forms(tally: Tally) -> None:
    # t = 1/2: u = (3/5, 4/5), v = (-4/5, 3/5). Corners about the origin:
    # -u/2 - v/2 = (1/10, -7/10); u/2 - v/2 = (7/10, 1/10); u/2 + v/2 = (-1/10, 7/10);
    # -u/2 + v/2 = (-7/10, -1/10).
    want = ((F(1, 10), F(-7, 10)), (F(7, 10), F(1, 10)), (F(-1, 10), F(7, 10)), (F(-7, 10), F(-1, 10)))
    tally.check(forms.corners_from_xyt((0, 1), (0, 1), (1, 2)) == want, "corners at t = 1/2")
    tally.check(geom.corners((F(0), F(0), F(1, 2))) == want, "geom corners at t = 1/2")
    # t = 0 about (1/2, 1/2): the square [0,1]^2 from its lower-left corner, counterclockwise
    unit = ((F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1)))
    tally.check(forms.corners_from_xyt((1, 2), (1, 2), (0, 1)) == unit, "corners at t = 0")
    # t = 1: u = (0, 1), v = (-1, 0); -u/2 - v/2 = (1/2, -1/2): [0,1]^2 from (1, 0)
    turned = ((F(1), F(0)), (F(1), F(1)), (F(0), F(1)), (F(0), F(0)))
    tally.check(forms.corners_from_xyt((1, 2), (1, 2), (1, 1)) == turned, "corners at t = 1")
    # t = -1/2: u = (3/5, -4/5), v = (4/5, 3/5); -u/2 - v/2 = (-7/10, 1/10)
    tally.check(
        forms.corners_from_xyt((0, 1), (0, 1), (-1, 2))[0] == (F(-7, 10), F(1, 10)),
        "corners at t = -1/2",
    )
    # poses: t = p/q gives (q^2 - p^2, 2pq, q^2 + p^2)
    for t, abr in (
        ((1, 2), (3, 4, 5)),
        ((2, 3), (5, 12, 13)),
        ((1, 4), (15, 8, 17)),
        ((0, 1), (1, 0, 1)),
        ((1, 1), (0, 2, 2)),
        ((-1, 2), (3, -4, 5)),
        ((3, 1), (-8, 6, 10)),
    ):
        pose = axes.pose_from_xyt((7, 3), (5, 6), t)
        tally.check(pose == (14, 5, 6, *abr), f"pose at t = {t}")
        tally.check(axes.is_unit_pose(pose), f"unit pose at t = {t}")
    # (cos, sin) and the half-extent
    tally.check(geom.direction(F(1, 2)) == (F(3, 5), F(4, 5)), "direction at 1/2")
    tally.check(geom.direction(F(3)) == (F(-4, 5), F(3, 5)), "direction at 3")
    tally.check(geom.half_extent(F(1, 2)) == F(7, 10), "half-extent at 1/2")
    tally.check(geom.half_extent(F(0)) == F(1, 2), "half-extent at 0")
    # the transposed and mirrored tangents: (c, s) -> (s, c) and (c, s) -> (c, -s)
    for t in (F(0), F(1, 2), F(2, 3), F(-1, 4), F(3), F(-1)):
        c, s = geom.direction(t)
        c2, s2 = geom.direction(geom.transposed_t(t))
        # the same square: its edge directions are (s, c) up to a quarter turn
        same = (c2, s2) in ((s, c), (-c, s), (-s, -c), (c, -s))
        tally.check(same, f"transposed tangent at {t}")
    # same_square
    for t in ANGLES:
        base = forms.corners_from_xyt((2, 3), (5, 7), pair(t))
        for idx, listing in enumerate(listings(base)):
            rel = forms.same_square(forms.pairs_of(base), forms.pairs_of(listing))
            want_rel = (idx % 4, 1 if idx < 4 else -1)
            tally.check(rel == want_rel, f"same_square listing {idx} at {t}")
        moved = tuple((x + EPS, y) for x, y in base)
        tally.check(
            forms.same_square(forms.pairs_of(base), forms.pairs_of(moved)) is None,
            f"same_square refuses a shift at {t}",
        )
        one_off = (base[0], base[1], (base[2][0], base[2][1] + EPS), base[3])
        tally.check(
            forms.same_square(forms.pairs_of(base), forms.pairs_of(one_off)) is None,
            f"same_square refuses one corner at {t}",
        )


def t_edge_contacts(tally: Tally) -> None:
    # Parallel squares. Square j is square i moved by (1 + d) along an edge normal w and
    # by tau along the edge. On w the separation is (1 + d) - 1 = d; on the other normal
    # it is |tau| - 1 <= -2/3. So the margin is d for d >= -1/7, and for d < 0 the
    # overlap is a |d| by (1 - |tau|) rectangle.
    cx, cy = F(2, 3), F(5, 7)
    for t in ANGLES:
        c, s = geom.direction(t)
        normals = ((c, s), (-s, c), (-c, -s), (s, -c))
        for w, (wx, wy) in enumerate(normals):
            px, py = -wy, wx
            for tau in (F(0), F(1, 3), F(-1, 3)):
                for d in DELTAS:
                    rj = (cx + (1 + d) * wx + tau * px, cy + (1 + d) * wy + tau * py, t)
                    area = -d * (1 - abs(tau)) if d < 0 else F(0)
                    check_pair(tally, f"edge t={t} w={w} tau={tau} d={d}", (cx, cy, t), rj, d, area)


def t_corner_contacts(tally: Tally) -> None:
    # Parallel squares moved by (1 + d) along both edge normals: both separations are d,
    # and for d < 0 the overlap is a |d| by |d| square.
    cx, cy = F(-3, 4), F(1, 9)
    for t in ANGLES:
        c, s = geom.direction(t)
        for sa in (1, -1):
            for sb in (1, -1):
                for d in DELTAS:
                    rj = (
                        cx + (1 + d) * (sa * c - sb * s),
                        cy + (1 + d) * (sa * s + sb * c),
                        t,
                    )
                    area = d * d if d < 0 else F(0)
                    check_pair(tally, f"corner t={t} {sa}{sb} d={d}", (cx, cy, t), rj, d, area)


def quarter(row: geom.Row, turns: int) -> geom.Row:
    """A row turned by quarter turns about the origin; a square keeps its tangent."""
    x, y, t = row
    for _ in range(turns):
        x, y = -y, x
    return x, y, t


def t_corner_on_edge(tally: Tally) -> None:
    # Upright square i = [0,1]^2. Square j at t = 1/2 has u = (3/5, 4/5), v = (-4/5, 3/5),
    # half-extent 7/10, and its lowest corner is its centre plus (1/10, -7/10). With centre
    # (2/5, 17/10 + d) that corner is (1/2, 1 + d): above the middle of i's top edge by d.
    # On i's normal (0,1) the separation is (17/10 + d - 1/2) - (1/2 + 7/10) = d; on the
    # others it is below -3/10 + d. For d < 0 the corner cuts a triangle of height |d| and
    # base |d|*(3/4 + 4/3), area (25/24) d^2.
    # At t = 2/3: u = (5/13, 12/13), half-extent 17/26, lowest corner at centre plus
    # (7/26, -17/26); centre (3/13, 43/26 + d); base |d|*(5/12 + 12/5), area (169/120) d^2.
    upright = (F(1, 2), F(1, 2), F(0))
    for t, x0, y0, coeff in (
        (F(1, 2), F(2, 5), F(17, 10), F(25, 24)),
        (F(2, 3), F(3, 13), F(43, 26), F(169, 120)),
    ):
        for turns in range(4):
            for d in DELTAS:
                ri = quarter(upright, turns)
                rj = quarter((x0, y0 + d, t), turns)
                area = coeff * d * d if d < 0 else F(0)
                check_pair(tally, f"corner on edge t={t} turns={turns} d={d}", ri, rj, d, area)
                check_pair(tally, f"edge under corner t={t} turns={turns} d={d}", rj, ri, d, area)


def t_lines(tally: Tally) -> None:
    # the line of the directed edge (0,0) -> (1,0) is y >= 0: (a, b, c) = (0, 1, 0);
    # of (1,0) -> (1,1) it is 1 - x >= 0: (-1, 0, 1)
    unit = clip.points(forms.pairs_of(((F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1)))))
    lines = clip.edge_lines(unit)
    tally.check(lines[0] == (0, 1, 0) and lines[1] == (-1, 0, 1), "edge lines of the unit square")
    tally.check(lines[2] == (0, -1, 1) and lines[3] == (1, 0, 0), "edge lines, the other two")
    # half of the unit square: x >= 1/2 keeps a 1/2 by 1 rectangle of twice-area 1
    half = clip.clip_line(unit, mpq(1), mpq(0), mpq(-1, 2))
    tally.check(clip.twice_area(half) == 1 and len(half) == 4, "clip_line halves the square")
    # a line through two opposite corners keeps a triangle of twice-area 1; a corner on
    # the line may be listed twice, which changes no area
    tri = clip.clip_line(unit, mpq(1), mpq(-1), mpq(0))
    tally.check(
        clip.twice_area(tri) == 1 and set(tri) == {unit[0], unit[1], unit[2]},
        "clip_line along the diagonal",
    )
    # a line through one corner only keeps that corner: a degenerate polygon of area 0
    point = clip.clip_line(unit, mpq(-1), mpq(-1), mpq(0))
    tally.check(
        set(point) == {unit[0]} and clip.twice_area(point) == 0, "clip_line at a corner"
    )
    tally.check(clip.clip_line(unit, mpq(-1), mpq(0), mpq(-1)) == [], "clip_line misses")
    other = quad_of((F(3, 2), F(1, 3), F(1, 2)))
    with_lines = clip.pair_class(unit, other, lines, clip.edge_lines(other))
    tally.check(with_lines == clip.pair_class(unit, other), "pair_class with and without lines")
    tally.check(clip.area_in_box(unit, mpq(1)) == 1, "the unit square fills its box")
    tally.check(clip.area_in_box(unit, mpq(1, 2)) == mpq(1, 4), "a quarter of it in half the box")


def t_overlaps(tally: Tally) -> None:
    # A square on itself: every |d.w| is 0 and H = 1, margin -1, area 1.
    for t in ANGLES:
        row = (F(3, 7), F(-2, 5), t)
        check_pair(tally, f"duplicate t={t}", row, row, F(-1), F(1))
    # Concentric squares turned by D: margin -(1/2 + (|cos D| + |sin D|)/2), and the
    # octagon they share has area 2/(1 + |cos D| + |sin D|).
    # D from t = 1/2: -(1/2 + 7/10) = -6/5 and 2/(12/5) = 5/6.
    # D from t = 2/3: -(1/2 + 17/26) = -15/13 and 2/(30/13) = 13/15.
    centre = (F(1, 3), F(1, 5))
    check_pair(tally, "concentric 3-4-5", (*centre, F(0)), (*centre, F(1, 2)), F(-6, 5), F(5, 6))
    check_pair(tally, "concentric 5-12-13", (*centre, F(0)), (*centre, F(2, 3)), F(-15, 13), F(13, 15))
    # the same pair turned together by t = 1/4 keeps D, so the same margin and area;
    # the tangent of the sum of two half-angles is (t1 + t2)/(1 - t1 t2)
    t0 = F(1, 4)
    t1 = (t0 + F(1, 2)) / (1 - t0 * F(1, 2))
    check_pair(tally, "concentric turned", (*centre, t0), (*centre, t1), F(-6, 5), F(5, 6))


def t_walls(tally: Tally) -> None:
    # A square with half-extent h whose centre is h + d from a wall clears it by d.
    # Crossing by e, an upright square has area e outside; a tilted one a triangle of
    # height e and base e*(c/s + s/c), area e^2/(2|c||s|).
    side = F(5)
    for t in (F(0), F(1, 2), F(2, 3), F(1, 4), F(-1, 2)):
        c, s = geom.direction(t)
        h = geom.half_extent(t)
        for w in range(4):
            for d in (EPS, F(0), -EPS, F(1, 9), -F(1, 9)):
                x, y = F(5, 2), F(12, 5)
                if w == 0:
                    x = h + d
                elif w == 1:
                    y = h + d
                elif w == 2:
                    x = side - h - d
                else:
                    y = side - h - d
                row = (x, y, t)
                label = f"wall {w} t={t} d={d}"
                got = axes.wall_clearances(pose_of(row), pair(side))
                tally.check(got[w] == d, f"{label}: A clearance")
                tally.check(geom.clearances(row, side)[w] == d, f"{label}: closed form")
                tally.check(all(got[k] > 0 for k in range(4) if k != w), f"{label}: A others")
                if d >= 0:
                    out_area = F(0)
                elif t == 0:
                    out_area = -d
                else:
                    out_area = d * d / (2 * abs(c) * abs(s))
                want = expected_class(d)
                corners = forms.corners_from_xyt(pair(x), pair(y), pair(t))
                for idx, listing in enumerate(listings(corners)):
                    quad = clip.counterclockwise(clip.points(forms.pairs_of(listing)))
                    classes = clip.wall_classes(quad, mpq(5))
                    tally.check(classes[w][0] == want, f"{label}: B class, listing {idx}")
                    tally.check(
                        classes[w][1] == mpq(out_area.numerator, out_area.denominator),
                        f"{label}: B area outside",
                    )
                    tally.check(
                        all(classes[k][0] == "apart" for k in range(4) if k != w),
                        f"{label}: B others",
                    )
                    inside = clip.area_in_box(quad, mpq(5))
                    want_in = 1 - out_area
                    tally.check(
                        inside == mpq(want_in.numerator, want_in.denominator),
                        f"{label}: B area inside",
                    )


def t_unit(tally: Tally) -> None:
    for t in (F(0), F(1, 2), F(2, 3), F(1, 4), F(-3, 7), F(5)):
        corners = forms.corners_from_xyt((1, 3), (2, 7), pair(t))
        tally.check(clip.unit_sense(clip.points(forms.pairs_of(corners))) == 1, f"ccw at {t}")
        back = (corners[0], corners[3], corners[2], corners[1])
        tally.check(clip.unit_sense(clip.points(forms.pairs_of(back))) == -1, f"cw at {t}")
    p = [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1))]
    shapes = {
        "corner off by the least step": [p[0], p[1], (F(1) + EPS, F(1)), p[3]],
        "bowtie listing": [p[0], p[2], p[1], p[3]],
        # sides (1,0) and (3/5,4/5): all four sides 1, diagonals^2 16/5 and 4/5
        "unit rhombus": [(F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "rectangle": [p[0], p[1], (F(1), F(1) + EPS), (F(0), F(1) + EPS)],
        "square of side 2": [(F(0), F(0)), (F(2), F(0)), (F(2), F(2)), (F(0), F(2))],
        "a point": [p[0], p[0], p[0], p[0]],
        "repeated corner": [p[0], p[0], p[2], p[3]],
    }
    for name, shape in shapes.items():
        raw = forms.pairs_of(tuple(shape))
        tally.check(clip.unit_sense(clip.points(raw)) == 0, f"B refuses {name}")
        try:
            forms.pose_from_corners(raw)
            refused = False
        except ValueError:
            refused = True
        tally.check(refused, f"pose from corners refuses {name}")
    tally.check(axes.is_unit_pose((0, 0, 1, 3, 4, 5)), "A accepts (3,4,5)")
    for bad in ((0, 0, 1, 3, 4, 6), (0, 0, 1, 3, 4, -5), (0, 0, 0, 3, 4, 5), (0, 0, -1, 3, 4, 5), (0, 0, 1, 0, 0, 0)):
        tally.check(not axes.is_unit_pose(bad), f"A refuses {bad}")


def random_row(rng: random.Random, span: int) -> geom.Row:
    q = rng.randint(1, 10**6)
    p = rng.randint(-(10**6), 10**6)
    x = F(rng.randint(-span * 10**9, span * 10**9), rng.randint(1, 10**9))
    y = F(rng.randint(-span * 10**9, span * 10**9), rng.randint(1, 10**9))
    return x, y, F(p, q)


def t_random(tally: Tally) -> None:
    rng = random.Random(1009)
    done = 0
    while done < 300:
        ri = random_row(rng, 2)
        rj = random_row(rng, 2)
        if ri[0] == rj[0] and ri[1] == rj[1]:
            continue
        done += 1
        pi, pj = pose_of(ri), pose_of(rj)
        m = axes.pair_margin(pi, pj)
        tally.check(axes.pair_margin(pj, pi) == m, f"random {done}: A symmetric")
        tally.check(geom.margin(ri, rj) == m, f"random {done}: closed form")
        ci, cj = geom.corners(ri), geom.corners(rj)
        tally.check(geom.corner_margin(ci, cj) == m, f"random {done}: corner projections")
        cls, _area = clip.pair_class(quad_of(ri), quad_of(rj))
        tally.check(cls == expected_class(m), f"random {done}: B class")
        for target in (EPS, F(0), -EPS):
            moved, _s = geom.close_pair(ri, rj, target)
            pm = pose_of(moved)
            tally.check(axes.pair_margin(pi, pm) == target, f"random {done}: closed to {target}, A")
            tally.check(
                geom.corner_margin(ci, geom.corners(moved)) == target,
                f"random {done}: closed to {target}, corner projections",
            )
            cls, area = clip.pair_class(quad_of(ri), quad_of(moved))
            tally.check(cls == expected_class(target), f"random {done}: closed to {target}, B")
            tally.check((area > 0) == (target < 0), f"random {done}: closed to {target}, B area")
    side = F(9)
    for k in range(100):
        row = random_row(rng, 1)
        h = geom.half_extent(row[2])
        for w in range(4):
            for d in (EPS, F(0), -EPS):
                x, y = F(9, 2), F(9, 2)
                if w == 0:
                    x = h + d
                elif w == 1:
                    y = h + d
                elif w == 2:
                    x = side - h - d
                else:
                    y = side - h - d
                moved = (x, y, row[2])
                got = axes.wall_clearances(pose_of(moved), pair(side))
                tally.check(got[w] == d, f"random wall {k} {w} {d}: A")
                quad = quad_of(moved)
                classes = clip.wall_classes(quad, mpq(9))
                tally.check(classes[w][0] == expected_class(d), f"random wall {k} {w} {d}: B")
                inside = clip.area_in_box(quad, mpq(9))
                tally.check((inside == 1) == (d >= 0), f"random wall {k} {w} {d}: B inside")


def grid_rows() -> list[geom.Row]:
    return [(F(1, 2) + i, F(1, 2) + j, F(0)) for j in range(2) for i in range(2)]


def refused(read: object, data: bytes) -> bool:
    try:
        read(data)  # type: ignore[operator]
    except reader.ReadError:
        return True
    return False


def t_reader(tally: Tally) -> None:
    rows = [(F(1, 2), F(7, 10), F(0)), (F(7, 3), F(22, 7), F(1, 2)), (F(5), F(11, 4), F(-2, 3))]
    side = F(15, 2)
    cert, wit = write.both_forms(rows, side)
    got = reader.read_cert(cert)
    tally.check(got["n"] == 3 and got["side"] == (15, 2), "cert: n and side")
    tally.check(
        got["poses"] == [tuple(pair(v) for v in row) for row in rows], "cert: rows read back"
    )
    tally.check(got["noncanonical"] == [] and got["scalars"] == 10, "cert: canonical")
    tally.check(len(got["comments"]) == 1, "cert: one comment")
    wgot = reader.read_witness(wit)
    tally.check(wgot["n"] == 3 and wgot["side"] == (15, 2), "witness: n and side")
    want = [forms.pairs_of(geom.corners(r)) for r in rows]
    tally.check(wgot["squares"] == want, "witness: corners read back")
    tally.check(wgot["noncanonical"] == [] and wgot["scalars"] == 25, "witness: canonical")
    tally.check(wgot["id_style"] == "square-k", "witness: id style")
    # a non-canonical side is read with its value and flagged
    c2 = write.cert_bytes(rows, side, side_text="30/4")
    g2 = reader.read_cert(c2)
    tally.check(g2["side"] == (30, 4) and g2["noncanonical"] == ["side"], "cert: 30/4 flagged")
    w2 = write.witness_bytes([geom.corners(r) for r in rows], side, side_text="30/4")
    g3 = reader.read_witness(w2)
    tally.check(g3["side"] == (30, 4) and g3["noncanonical"] == ["side"], "witness: 30/4 flagged")
    # integer ids are read as well
    w3 = write.witness_bytes([geom.corners(r) for r in rows], side, ids=["1", "2", "3"])
    tally.check(reader.read_witness(w3)["id_style"] == "integer", "witness: integer ids")

    text = cert.decode()
    cert_bad = {
        "no final newline": (text[:-1], True),
        "carriage returns": (text.replace("\n", "\r\n"), True),
        "a tab": (text.replace("3 15/2", "3\t15/2"), True),
        "two spaces": (text.replace("3 15/2", "3  15/2"), True),
        "trailing space": (text.replace("15/2\n", "15/2 \n"), True),
        "blank line": (text.replace("15/2\n", "15/2\n\n"), True),
        "comment after the header": (text.replace("15/2\n", "15/2\n# late\n"), True),
        "one square too few": (text.replace("3 15/2", "4 15/2"), True),
        "one square too many": (text.replace("3 15/2", "2 15/2"), True),
        "three header tokens": (text.replace("3 15/2", "3 15/2 1"), True),
        "n with a leading zero": (text.replace("3 15/2", "03 15/2"), True),
        "n of zero": (text.replace("3 15/2", "0 15/2"), True),
        "a plus sign": (text.replace("7/3", "+7/3"), True),
        "a leading zero": (text.replace("7/3", "07/3"), True),
        "a decimal": (text.replace("7/3", "2.5"), True),
        "a zero denominator": (text.replace("7/3", "7/0"), True),
        "an exponent": (text.replace("7/3", "7e3"), True),
        "a negative side": (text.replace("3 15/2", "3 -15/2"), True),
        "a zero side": (text.replace("3 15/2", "3 0"), True),
        "two scalars in a row": (text.replace(" -2/3", ""), True),
        "four scalars in a row": (text.replace(" -2/3", " -2/3 1"), True),
        "two slashes": (text.replace("7/3", "7/3/2"), True),
        "a negative denominator": (text.replace("7/3", "7/-3"), True),
        "no header": ("# only a comment\n", False),
    }
    for name, (bad, must_differ) in cert_bad.items():
        applied = bad != text if must_differ else True
        tally.check(applied, f"cert mutation applied: {name}")
        tally.check(refused(reader.read_cert, bad.encode()), f"cert refused: {name}")
    tally.check(refused(reader.read_cert, text.encode() + b"\xc3\xa9\n"), "cert refused: non-ASCII")

    wtext = wit.decode()
    first = "    - - '0'\n"
    tally.check(first in wtext, "witness sample has the corner the mutations use")
    wit_bad = {
        "an anchor": wtext.replace("  scalar:\n", "  scalar: &a\n"),
        "an alias": wtext.replace("    kind: rational\n", "    kind: &a rational\n").replace(
            "    method: exact-algebraic", "    method: *a"
        ),
        "an explicit tag": wtext.replace("  square_size: '1'", "  square_size: !!str '1'"),
        "a duplicate key": wtext.replace("  square_size: '1'\n", "  square_size: '1'\n  square_size: '1'\n"),
        "a tab": wtext.replace("  n: 3", "  n:\t3"),
        "carriage returns": wtext.replace("\n", "\r\n"),
        "a float side": wtext.replace("  side: '15/2'", "  side: 7.5"),
        "an integer side": wtext.replace("  side: '15/2'", "  side: 7"),
        "n as a string": wtext.replace("  n: 3", "  n: '3'"),
        "n of zero": wtext.replace("  n: 3", "  n: 0"),
        "n in hexadecimal": wtext.replace("  n: 3", "  n: 0x3"),
        "square_size 2": wtext.replace("  square_size: '1'", "  square_size: '2'"),
        "another representation": wtext.replace("representation: corners", "representation: center-angle"),
        "decimal scalars": wtext.replace("kind: rational", "kind: decimal"),
        "a centred origin": wtext.replace("origin: lower-left", "origin: container-center"),
        "other axes": wtext.replace("axes: x-right-y-up", "axes: x-right-y-down"),
        "no claim method": wtext.replace("    method: exact-algebraic\n", ""),
        "an extra top-level key": wtext + "extra: 1\n",
        "an extra envelope key": wtext.replace("  status: enforced\n", "  status: enforced\n  more: x\n"),
        "another contract": wtext.replace("Witness/v2", "Witness/v1"),
        "an unknown witness key": wtext.replace("  square_size: '1'\n", "  square_size: '1'\n  bogus: x\n"),
        "one square too few": wtext.replace("  n: 3", "  n: 4"),
        "one square too many": wtext.replace("  n: 3", "  n: 2"),
        "ids out of order": wtext.replace("id: square-1", "id: square-9", 1),
        "ids of two styles": wtext.replace("id: square-2", "id: 2"),
        "three corners": wtext.replace(first + "      - '1/5'\n", "", 1),
        "a corner of three scalars": wtext.replace(first, first + "      - '0'\n", 1),
        "a scalar that is a number": wtext.replace(first, "    - - 0\n", 1),
        "a plus sign": wtext.replace(first, "    - - '+0'\n", 1),
        "a leading zero": wtext.replace(first, "    - - '00'\n", 1),
        "a decimal scalar": wtext.replace(first, "    - - '0.0'\n", 1),
        "two documents": wtext + "---\nsoftschema: {}\n",
        "a document marker": "---\n" + wtext,
        "a boolean": wtext.replace("  status: enforced", "  status: true"),
        "a null": wtext.replace("  status: enforced", "  status: ~"),
        "a square with an extra key": wtext.replace("  - id: square-1\n", "  - id: square-1\n    note: x\n"),
        "not YAML": wtext.replace("witness:\n", "witness: [\n"),
        "an empty document": "\n",
    }
    for name, bad in wit_bad.items():
        tally.check(bad != wtext, f"witness mutation applied: {name}")
        tally.check(refused(reader.read_witness, bad.encode()), f"witness refused: {name}")
    for text_value, want_value in (
        ("0", (0, 1, True)),
        ("-0", (0, 1, False)),
        ("12", (12, 1, True)),
        ("-12/5", (-12, 5, True)),
        ("12/1", (12, 1, False)),
        ("6/4", (6, 4, False)),
        ("0/5", (0, 5, False)),
    ):
        tally.check(reader.parse_scalar(text_value, "t") == want_value, f"scalar {text_value}")
    for bad_scalar in ("", "+1", "01", "1/0", "1/02", "1.0", "1e3", " 1", "1 ", "--1", "1/-2", "a"):
        try:
            reader.parse_scalar(bad_scalar, "t")
            ok = False
        except reader.ReadError:
            ok = True
        tally.check(ok, f"scalar refused: {bad_scalar!r}")


def t_files(tally: Tally) -> None:
    # A 2 by 2 grid of upright unit squares in the box of side 2: six pairs, four sharing
    # an edge and two a corner, all touching; eight wall contacts.
    rows = grid_rows()
    cert, wit = write.both_forms(rows, F(2))
    got = files.decide_files(cert, wit, cross=True)
    tally.check(got["verdict"] == "ACCEPT", "grid: accepted")
    nat = got["native"]
    tally.check(nat["pair_counts_a"] == {"apart": 0, "touch": 6, "overlap": 0}, "grid: A touching")
    tally.check(nat["pair_counts_b"] == {"apart": 0, "touch": 6, "overlap": 0}, "grid: B touching")
    tally.check(len(nat["wall_touching"]) == 8 and not nat["wall_crossing"], "grid: 8 wall contacts")
    tally.check(nat["least_margin"] == 0 and got["twin_fails"] == [], "grid: least margin, twin")
    tally.check(got["margin_digests_equal"], "grid: two decisions, one digest")
    tally.check(got["clearances_equal"], "grid: two decisions, the same clearances")
    tally.check(got["crossed"]["verdict"] == "ACCEPT", "grid: accepted the other way round")
    # the same files with method A on the poses taken from form C
    alone = files.decide_files(cert, wit, a_from="c")
    tally.check(alone["verdict"] == "ACCEPT", "grid: form C alone")
    tally.check(alone["native"]["margins_sha256"] == nat["margins_sha256"], "grid: form C digest")
    # a partial decision: only the pairs with square 4
    part = files.decide_files(cert, wit, only={4})
    tally.check(part["verdict"] == "PARTIAL", "grid: partial")
    tally.check(part["native"]["pairs_decided"] == 3, "grid: partial decides three pairs")
    tally.check(
        part["native"]["margins_of"] == {(1, 4): F(0), (2, 4): F(0), (3, 4): F(0)},
        "grid: partial margins",
    )
    none = files.decide_files(cert, wit, only=set())
    tally.check(none["verdict"] == "PARTIAL" and none["native"]["pairs_decided"] == 0, "grid: no pairs")
    tally.check(len(none["native"]["wall_touching"]) == 8, "grid: no pairs, walls decided")
    # the same grid in a box too small by the least step: squares 2 and 4 cross the right
    # wall and 3 and 4 the top
    cert, wit = write.both_forms(rows, F(2) - EPS)
    got = files.decide_files(cert, wit, cross=True)
    tally.check(got["verdict"] == "REFUSE", "small box: refused")
    tally.check(
        got["native"]["wall_crossing"] == [(2, "right"), (3, "top"), (4, "right"), (4, "top")],
        "small box: the four crossings",
    )
    tally.check(got["native"]["not_inside_b"] == [2, 3, 4], "small box: B containment")
    tally.check(not got["native"]["pair_overlapping"], "small box: no pair overlaps")
    # a duplicate square
    dup = [*rows[:3], rows[0]]
    cert, wit = write.both_forms(dup, F(2))
    got = files.decide_files(cert, wit, cross=True)
    tally.check(got["verdict"] == "REFUSE", "duplicate: refused")
    tally.check(got["native"]["pair_overlapping"] == [(1, 4)], "duplicate: the pair")
    tally.check(got["native"]["overlap_area_b"] == 1, "duplicate: area 1")
    part = files.decide_files(cert, wit, only={4})
    tally.check(part["verdict"] == "REFUSE", "duplicate: partial refused")
    tally.check(part["native"]["pair_overlapping"] == [(1, 4)], "duplicate: partial pair")
    part = files.decide_files(cert, wit, only={2})
    tally.check(part["verdict"] == "PARTIAL", "duplicate: the pairs of square 2 are fine")
    # one 3-4-5 square in its own box of side 7/5: all four walls touched
    cert, wit = write.both_forms([(F(7, 10), F(7, 10), F(1, 2))], F(7, 5))
    got = files.decide_files(cert, wit, cross=True)
    tally.check(got["verdict"] == "ACCEPT", "3-4-5 in its box: accepted")
    tally.check(len(got["native"]["wall_touching"]) == 4, "3-4-5 in its box: four contacts")
    # the two files must be one packing: a witness whose second square is moved
    cert, _wit = write.both_forms(rows, F(5))
    other = [geom.corners(r) for r in rows]
    other[1] = geom.corners((F(3, 2), F(1, 2) + EPS, F(0)))
    got = files.decide_files(cert, write.witness_bytes(other, F(5)), cross=True)
    tally.check(got["verdict"] == "REFUSE" and got["twin_fails"] == [2], "twin: square 2 differs")
    # different sides, different counts
    got = files.decide_files(cert, write.witness_bytes([geom.corners(r) for r in rows], F(6)))
    tally.check(got["verdict"] == "REFUSE" and "native" not in got, "twin: sides differ")
    got = files.decide_files(cert, write.witness_bytes([geom.corners(r) for r in rows[:3]], F(5)))
    tally.check(got["verdict"] == "REFUSE" and "native" not in got, "twin: counts differ")
    # the tangent read the other way round: a tilted square is another square, an
    # upright one (t = 0) and one at a quarter turn (t = 1) are the same
    tilted = [(F(1), F(1), F(1, 2)), (F(3), F(1), F(0)), (F(1), F(3), F(1)), (F(3), F(3), F(-2, 3))]
    flipped = [(x, y, -t) for x, y, t in tilted]
    got = files.decide_files(
        write.cert_bytes(flipped, F(4)), write.witness_bytes([geom.corners(r) for r in tilted], F(4))
    )
    tally.check(got["twin_fails"] == [1, 4], "twin: the other sense differs at tilted squares")
    # a square that is not a unit square in form C
    bad = [geom.corners(r) for r in rows]
    bad[2] = (bad[2][0], bad[2][1], (bad[2][2][0] + EPS, bad[2][2][1]), bad[2][3])
    got = files.decide_files(cert, write.witness_bytes(bad, F(5)), cross=True)
    tally.check(got["verdict"] == "REFUSE", "not unit: refused")
    tally.check(got["native"].get("not_unit_b") == [3], "not unit: B names square 3")
    tally.check(got["form_c_no_pose"] == [3] and got["twin_fails"] == [3], "not unit: no pose, no twin")
    tally.check(got["crossed"]["verdict"] == "REFUSE", "not unit: refused the other way round")
    tally.check(got["crossed"].get("not_unit_a") == [3], "not unit: A names square 3")
    # an unreadable file is a refusal, not an exception
    got = files.decide_files(cert[:-1], wit)
    tally.check(got["verdict"] == "REFUSE" and "read_error_p" in got, "unreadable form P")
    tally.check(decide.pair_index(4, 1, 2) == 0 and decide.pair_index(4, 2, 3) == 3, "pair index")
    tally.check(decide.pair_index(4, 3, 4) == 5 and decide.pair_index(5, 2, 5) == 6, "pair index 2")


SUITE = (
    t_forms,
    t_edge_contacts,
    t_corner_contacts,
    t_corner_on_edge,
    t_lines,
    t_overlaps,
    t_walls,
    t_unit,
    t_random,
    t_reader,
    t_files,
)


def run_suite() -> Tally:
    tally = Tally()
    for test in SUITE:
        try:
            test(tally)
        except Exception as exc:  # noqa: BLE001  a broken copy may raise anywhere
            tally.check(False, f"{test.__name__} raised {type(exc).__name__}: {exc}")
    return tally


def broken_only_first_normals(pi: axes.Pose, pj: axes.Pose) -> tuple:
    proj, k, den = ORIGINAL["pair_numbers"](pi, pj)
    return (proj[0], proj[1], proj[0], proj[1]), k, den


def broken_open_clip(poly: list, a: mpq, b: mpq, c: mpq) -> list:
    out = []
    count = len(poly)
    if count == 0:
        return out
    values = [a * p[0] + b * p[1] + c for p in poly]
    for k in range(count):
        cur, prev = poly[k], poly[k - 1]
        vc, vp = values[k], values[k - 1]
        if vc > 0:
            if vp <= 0:
                s = vp / (vp - vc)
                out.append((prev[0] + s * (cur[0] - prev[0]), prev[1] + s * (cur[1] - prev[1])))
            out.append(cur)
        elif vp > 0:
            s = vp / (vp - vc)
            out.append((prev[0] + s * (cur[0] - prev[0]), prev[1] + s * (cur[1] - prev[1])))
    return out


def broken_other_sense(x: tuple, y: tuple, t: tuple) -> tuple:
    return ORIGINAL["corners_from_xyt"](x, y, (-t[0], t[1]))


def broken_no_diagonals(quad: list) -> int:
    if len(quad) != 4:
        return 0
    for k in range(4):
        dx = quad[k][0] - quad[(k + 1) % 4][0]
        dy = quad[k][1] - quad[(k + 1) % 4][1]
        if dx * dx + dy * dy != 1:
            return 0
    area2 = clip.twice_area(quad)
    return 1 if area2 > 0 else (-1 if area2 < 0 else 0)


ORIGINAL: dict = {}


def main(argv: list[str]) -> int:
    import re

    started = time.process_time()
    plain = run_suite()
    ORIGINAL["pair_numbers"] = axes.pair_numbers
    ORIGINAL["corners_from_xyt"] = forms.corners_from_xyt
    mutants = {
        "method A with only the first square's normals": (axes, "pair_numbers", broken_only_first_normals),
        "method A counting a zero margin as apart": (decide, "A_CLASS", {1: "apart", 0: "apart", -1: "overlap"}),
        "method B clipping with open half-planes": (clip, "clip_line", broken_open_clip),
        "form P read with the other rotation sense": (forms, "corners_from_xyt", broken_other_sense),
        "method B without the diagonal test": (clip, "unit_sense", broken_no_diagonals),
        "a reader that takes a plus sign": (
            reader,
            "SCALAR",
            re.compile(r"[-+]?(0|[1-9][0-9]*)(/[1-9][0-9]*)?"),
        ),
    }
    broken = {}
    for name, (module, attr, replacement) in mutants.items():
        saved = getattr(module, attr)
        setattr(module, attr, replacement)
        try:
            result = run_suite()
        finally:
            setattr(module, attr, saved)
        broken[name] = {"cases": result.cases, "failed": result.failed}
    again = run_suite()
    passed = (
        plain.failed == 0
        and again.failed == 0
        and again.cases == plain.cases
        and all(entry["failed"] > 0 for entry in broken.values())
    )
    receipt = {
        "program": "rv1009_selftest.py",
        "lane": "c-review-1009-1117",
        "verdict": "PASSED" if passed else "FAILED",
        "cases": plain.cases,
        "failed": plain.failed,
        "first_failures": plain.first,
        "broken_copies": broken,
        "after_the_broken_copies": {"cases": again.cases, "failed": again.failed},
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    Path(argv[1]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="ascii")
    sys.stdout.write(
        f"{receipt['verdict']} {plain.cases} cases {plain.failed} failed; broken copies: "
        + ", ".join(str(entry["failed"]) for entry in broken.values())
        + "\n"
    )
    for label in plain.first:
        sys.stdout.write(f"  failed: {label}\n")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
