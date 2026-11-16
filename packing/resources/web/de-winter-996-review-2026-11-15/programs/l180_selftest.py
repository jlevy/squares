"""Lane L180 self-test: both methods, the closed form and the reader against known answers.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review.

Usage: l180_selftest.py OUT

Every expected margin, area and class below is derived by hand in the comments, not
computed by the code under test. Three deliberately broken copies of the methods must
each fail some of the pair and wall cases.
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from collections.abc import Callable
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l180_axes as A  # noqa: E402
import l180_clip as B  # noqa: E402
import l180_decide as D  # noqa: E402
import l180_geom as G  # noqa: E402
import l180_reader as R  # noqa: E402
from gmpy2 import mpq  # noqa: E402
from l180_reader import Pose  # noqa: E402

TINY = F(1, 10**30)
DELTAS = (TINY, F(0), -TINY)
ANGLES = ((F(1), F(0)), (F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)))


class Tally:
    def __init__(self) -> None:
        self.cases = 0
        self.failed: list[str] = []

    def check(self, ok: bool, label: str) -> None:
        self.cases += 1
        if not ok:
            self.failed.append(label)


def sign_class(m: F) -> str:
    return "apart" if m > 0 else "touch" if m == 0 else "overlap"


def equivalents(p: Pose) -> list[Pose]:
    """The four edge directions that describe the same square."""
    c, s = p.c, p.s
    return [Pose(p.x, p.y, c, s), Pose(p.x, p.y, -s, c), Pose(p.x, p.y, -c, -s), Pose(p.x, p.y, s, -c)]


def quarter(p: Pose, k: int) -> Pose:
    """The pose turned k quarter turns about the origin."""
    for _ in range(k):
        p = Pose(-p.y, p.x, -p.s, p.c)
    return p


def b_square(p: Pose) -> list[B.Pt]:
    return B.ccw(B.to_mpq(R.json_corners(p)))


def pair_case(t: Tally, p: Pose, q: Pose, margin: F, area: F, label: str) -> None:
    """Both methods and the closed form on (p, q) under every equivalent direction, both orders."""
    for pe in equivalents(p):
        for qe in equivalents(q):
            for a, b in ((pe, qe), (qe, pe)):
                ia, ib = A.to_ints(a.x, a.y, a.c, a.s), A.to_ints(b.x, b.y, b.c, b.s)
                ma, _ = A.pair_margin(ia, ib)
                t.check(ma == margin, f"{label}: A margin {ma} != {margin}")
                t.check(A.pair_class(ma) == sign_class(margin), f"{label}: A class")
                t.check(G.margin(a, b) == margin, f"{label}: closed form margin")
                cb, ab, both = B.pair(b_square(a), b_square(b))
                t.check(both, f"{label}: B orders disagree")
                t.check(cb == sign_class(margin), f"{label}: B class {cb} for margin {margin}")
                t.check(ab == mpq(area.numerator, area.denominator), f"{label}: B area {ab} != {area}")


def unit_cases(t: Tally) -> None:
    for c, s in ANGLES:
        for k in range(4):
            p = quarter(Pose(F(0), F(0), c, s), k)
            t.check(A.is_unit(A.to_ints(p.x, p.y, p.c, p.s)), "A unit")
            ok, sense = B.unit_square(B.to_mpq(R.json_corners(p)))
            t.check(ok and sense == 1, "B unit, counterclockwise")
            ok2, sense2 = B.unit_square(list(reversed(B.to_mpq(R.json_corners(p)))))
            t.check(ok2 and sense2 == -1, "B unit, clockwise listing")
    tt = F(1, 10**30)
    co, si = G.rotation(tt)
    t.check(A.is_unit(A.to_ints(F(0), F(0), co, si)), "A unit at t = 1e-30")
    # Method A must refuse these directions: c^2 + s^2 != 1.
    for c, s in ((F(1), TINY), (F(1, 2), F(1, 2)), (F(3, 5) + TINY, F(4, 5)), (F(0), F(0)), (F(2), F(0))):
        t.check(not A.is_unit(A.to_ints(F(0), F(0), c, s)), f"A refuses ({c}, {s})")
    # Method B must refuse these shapes as unit squares in cyclic order.
    z = F(0)
    shapes = [
        [(z, z), (F(2), z), (F(2), F(2)), (z, F(2))],  # side 2
        [(z, z), (z, z), (z, z), (z, z)],  # a point
        [(z, z), (F(1), z), (F(1), F(1))],  # three points
        [(z, z), (F(1), F(1)), (F(1), z), (z, F(1))],  # a unit square's corners out of cyclic order
        [(z, z), (F(1), z), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],  # a rhombus of side 1
        [(z, z), (F(1) + TINY, z), (F(1), F(1)), (z, F(1))],  # one corner off by 1e-30
        [(z, z), (F(1), z), (F(1), F(1)), (z, F(1) - TINY)],  # another
    ]
    for k, sh in enumerate(shapes):
        ok, _ = B.unit_square(B.to_mpq(sh))
        t.check(not ok, f"B refuses shape {k}")


def edge_cases(t: Tally) -> int:
    """Two parallel squares, edge to edge across each of the four edges.

    Q = P's centre + (1 + delta) w + tau w_perp, w a unit normal of P, so the gap on w
    is delta and the shared edge has length 1 - tau: margin delta, and for delta < 0 an
    overlap strip |delta| deep and 1 - tau long, area |delta| (1 - tau).
    """
    n0 = t.cases
    for c, s in ANGLES:
        u, v = (c, s), (-s, c)
        for w, wp in ((u, v), (v, (-u[0], -u[1])), ((-u[0], -u[1]), (-v[0], -v[1])), ((-v[0], -v[1]), u)):
            for tau in (F(0), F(1, 3)):
                for dl in DELTAS:
                    p = Pose(F(1, 7), F(-2, 9), c, s)
                    q = Pose(p.x + (1 + dl) * w[0] + tau * wp[0], p.y + (1 + dl) * w[1] + tau * wp[1], c, s)
                    area = abs(dl) * (1 - tau) if dl < 0 else F(0)
                    pair_case(t, p, q, dl, area, f"edge {c},{s} w={w} tau={tau} d={dl}")
    return t.cases - n0


def corner_cases(t: Tally) -> int:
    """Two parallel squares corner to corner: Q = P + (1 + delta)(e1 u + e2 v).

    Gaps on u and on v are both delta: margin delta; overlap a square of side |delta|.
    """
    n0 = t.cases
    for c, s in ANGLES:
        u, v = (c, s), (-s, c)
        for e1, e2 in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
            for dl in DELTAS:
                p = Pose(F(-3, 11), F(5, 13), c, s)
                k = 1 + dl
                q = Pose(p.x + k * (e1 * u[0] + e2 * v[0]), p.y + k * (e1 * u[1] + e2 * v[1]), c, s)
                pair_case(t, p, q, dl, dl * dl if dl < 0 else F(0), f"corner {c},{s} {e1},{e2} d={dl}")
    return t.cases - n0


def vertex_on_edge_cases(t: Tally) -> int:
    """A turned square's lowest corner on an upright square's top edge.

    P upright at the origin. Q turned by (c, s), c, s > 0, has half-height (c + s)/2;
    at Q = (0, 1/2 + (c + s)/2 + delta) its lowest corner, at x = (s - c)/2, lies
    delta above y = 1/2. The other three gaps are negative (by hand: -6/25 and -12/25
    on Q's normals for 3-4-5, -30/338 and -240/338 for 5-12-13, and below -1 on P's
    other normal), so the margin is delta. For delta < 0 the corner
    cuts a right triangle with legs |delta|/s and |delta|/c: area delta^2 / (2cs),
    25/24 delta^2 and 169/120 delta^2. Turned by each quarter turn of the plane.
    """
    n0 = t.cases
    for c, s in ANGLES[1:]:
        for k in range(4):
            for dl in DELTAS:
                p = quarter(Pose(F(0), F(0), F(1), F(0)), k)
                q = quarter(Pose(F(0), F(1, 2) + (c + s) / 2 + dl, c, s), k)
                area = dl * dl / (2 * c * s) if dl < 0 else F(0)
                pair_case(t, p, q, dl, area, f"vertex {c},{s} k={k} d={dl}")
    return t.cases - n0


def overlap_cases(t: Tally) -> int:
    """Duplicates (margin -1, area 1) and concentric rotations.

    Upright P and Q turned by (c, s) about the same centre: the gap on P's normals is
    0 - 1/2 - (c + s)/2, so the margin is -(1 + c + s)/2 (-6/5 for 3-4-5, -15/13 for
    5-12-13). Each square's corners stick out of the other by h = (c + s - 1)/2 in four
    right triangles of legs h/s and h/c, so the area is 1 - (c + s - 1)^2 / (2cs):
    5/6 and 13/15.
    """
    n0 = t.cases
    for c, s in ANGLES:
        p = Pose(F(2, 3), F(-1, 5), c, s)
        pair_case(t, p, p, F(-1), F(1), f"duplicate {c},{s}")
    for c, s in ANGLES[1:]:
        p = Pose(F(1, 3), F(1, 4), F(1), F(0))
        q = Pose(F(1, 3), F(1, 4), c, s)
        pair_case(t, p, q, -(1 + c + s) / 2, 1 - (c + s - 1) ** 2 / (2 * c * s), f"concentric {c},{s}")
    return t.cases - n0


def wall_cases(t: Tally) -> int:
    """Each wall at 1e-30 inside, at contact and 1e-30 out, for three angles.

    A square turned by (c, s) has half-extent h = (|c| + |s|)/2 in x and in y. Centred
    at h + delta from the left wall its left clearance is delta; the other walls of a
    box of side 3 are far. Inside the box by area exactly when delta >= 0.
    """
    n0 = t.cases
    side = F(3)
    sq = mpq(3)
    for c, s in (*ANGLES, (F(-8, 17), F(15, 17))):
        h = (abs(c) + abs(s)) / 2
        for dl in DELTAS:
            for wall in ("left", "bottom", "right", "top"):
                x = y = F(3, 2)
                if wall == "left":
                    x = h + dl
                elif wall == "bottom":
                    y = h + dl
                elif wall == "right":
                    x = side - h - dl
                else:
                    y = side - h - dl
                p = Pose(x, y, c, s)
                for pe in equivalents(p):
                    cl = A.wall_clearances(A.to_ints(pe.x, pe.y, pe.c, pe.s), side)
                    t.check(cl[wall] == dl, f"wall {wall} {c},{s} d={dl}: A clearance {cl[wall]}")
                    t.check(G.clearances(pe, side)[wall] == dl, f"wall {wall}: closed form")
                    expect = "inside" if dl > 0 else "touch" if dl == 0 else "cross"
                    t.check(A.wall_class(cl[wall]) == expect, f"wall {wall}: A class")
                    wb = B.walls(b_square(pe), sq)
                    t.check(wb[wall][0] == expect, f"wall {wall} {c},{s} d={dl}: B class {wb[wall][0]}")
                    others = [w for w in wb if w != wall]
                    t.check(all(wb[w][0] == "inside" for w in others), "other walls inside")
                    inside = B.area_inside(b_square(pe), sq)
                    t.check((inside == 1) == (dl >= 0), f"wall {wall}: B containment {inside}")
    return t.cases - n0


def random_pose(rng: random.Random, near: Pose | None = None) -> Pose:
    p, q = rng.randint(-40, 40), rng.randint(1, 40)
    c, s = G.rotation(F(p, q))
    den = 10**20
    if near is None:
        return Pose(F(rng.randint(-den, den), den), F(rng.randint(-den, den), den), c, s)
    return Pose(near.x + F(rng.randint(-16 * den, 16 * den), 10 * den), near.y + F(rng.randint(-16 * den, 16 * den), 10 * den), c, s)


def random_cases(t: Tally) -> int:
    """Random rational pairs: A equals the closed form; B's class is its sign, both ways.

    Then pairs closed along their centre line to 1e-30 short of contact, to it and
    1e-30 past (A and the closed form exactly the target, B's class its sign), and
    turned squares taken to a wall the same way.
    """
    n0 = t.cases
    rng = random.Random(180)
    for k in range(300):
        p = random_pose(rng)
        q = random_pose(rng, p)
        ip, iq = A.to_ints(p.x, p.y, p.c, p.s), A.to_ints(q.x, q.y, q.c, q.s)
        m = G.margin(p, q)
        t.check(A.pair_margin(ip, iq)[0] == m, f"random {k}: A != closed form")
        t.check(A.pair_margin(iq, ip)[0] == m, f"random {k}: A reversed")
        cb, _, both = B.pair(b_square(p), b_square(q))
        t.check(both and cb == sign_class(m), f"random {k}: B class {cb}, margin sign {sign_class(m)}")
    for k in range(300):
        p = random_pose(rng)
        q = random_pose(rng, p)
        if p.x == q.x and p.y == q.y:
            continue
        for target in DELTAS:
            q2, _ = G.close_pair(p, q, target)
            ip, iq = A.to_ints(p.x, p.y, p.c, p.s), A.to_ints(q2.x, q2.y, q2.c, q2.s)
            t.check(A.pair_margin(ip, iq)[0] == target, f"closing {k} {target}: A")
            t.check(G.margin(p, q2) == target, f"closing {k} {target}: closed form")
            cb, _, both = B.pair(b_square(p), b_square(q2))
            t.check(both and cb == sign_class(target), f"closing {k} {target}: B {cb}")
    side = F(5)
    for k in range(300):
        p = random_pose(rng)
        p = Pose(F(5, 2), F(5, 2), p.c, p.s)
        wall = ("left", "bottom", "right", "top")[k % 4]
        target = DELTAS[k % 3]
        cl = G.clearances(p, side)[wall]
        q = G.move_to_wall(p, wall, cl - target)
        iq = A.to_ints(q.x, q.y, q.c, q.s)
        t.check(A.wall_clearances(iq, side)[wall] == target, f"wall move {k}: A")
        expect = "inside" if target > 0 else "touch" if target == 0 else "cross"
        t.check(B.walls(b_square(q), mpq(5))[wall][0] == expect, f"wall move {k}: B")
    return t.cases - n0


# ----------------------------------------------------------------------------- reader

VALID_JSON = (
    '{"n": 2, "side": "2", "square_size": "1", "format": "f", "squares": ['
    '["1/2", "1/2", "1", "0"], ["3/2", "1/2", "0", "1"]]}'
)


def reader_cases(t: Tally) -> int:
    n0 = t.cases
    r = R.read_json_text(VALID_JSON.encode())
    t.check(r.n == 2 and r.side == 2 and r.poses[1] == Pose(F(3, 2), F(1, 2), F(0), F(1)), "valid JSON read")
    back = R.read_json_text(R.write_json_text(r))
    t.check(back == r, "JSON write and read back")
    bad_json = {
        "float n": VALID_JSON.replace('"n": 2', '"n": 2.0'),
        "bool n": VALID_JSON.replace('"n": 2', '"n": true'),
        "float scalar": VALID_JSON.replace('"1/2", "1/2", "1"', '0.5, "1/2", "1"'),
        "int scalar": VALID_JSON.replace('"1/2", "1/2", "1"', '"1/2", "1/2", 1'),
        "NaN": VALID_JSON.replace('"n": 2', '"n": NaN'),
        "duplicate key": VALID_JSON.replace('"n": 2,', '"n": 2, "n": 2,'),
        "extra key": VALID_JSON.replace('"n": 2,', '"n": 2, "x": "1",'),
        "missing key": VALID_JSON.replace('"format": "f", ', ""),
        "count": VALID_JSON.replace('"n": 2', '"n": 3'),
        "1/1": VALID_JSON.replace('"side": "2"', '"side": "2/1"'),
        "2/4": VALID_JSON.replace('"1/2", "1/2", "1"', '"2/4", "1/2", "1"'),
        "-0": VALID_JSON.replace('"0", "1"]]', '"-0", "1"]]'),
        "0/3": VALID_JSON.replace('"0", "1"]]', '"0/3", "1"]]'),
        "leading zero": VALID_JSON.replace('"side": "2"', '"side": "02"'),
        "plus": VALID_JSON.replace('"side": "2"', '"side": "+2"'),
        "space": VALID_JSON.replace('"side": "2"', '"side": " 2"'),
        "negative denominator": VALID_JSON.replace('"1/2", "1/2", "1"', '"1/-2", "1/2", "1"'),
        "decimal": VALID_JSON.replace('"side": "2"', '"side": "2.0"'),
        "exponent": VALID_JSON.replace('"side": "2"', '"side": "2e0"'),
        "zero denominator": VALID_JSON.replace('"side": "2"', '"side": "2/0"'),
        "three scalars": VALID_JSON.replace('["3/2", "1/2", "0", "1"]', '["3/2", "1/2", "0"]'),
        "square_size": VALID_JSON.replace('"square_size": "1"', '"square_size": "2"'),
        "zero side": VALID_JSON.replace('"side": "2"', '"side": "0"'),
        "negative side": VALID_JSON.replace('"side": "2"', '"side": "-2"'),
        "format not string": VALID_JSON.replace('"format": "f"', '"format": 1'),
        "squares not list": VALID_JSON.replace('"squares": [', '"squares": {"a": [').replace("]]}", "]]}}"),
        "top level list": "[" + VALID_JSON + "]",
        "tab": VALID_JSON.replace('"n": 2', '"n":\t2'),
    }
    for label, text in bad_json.items():
        if text in (VALID_JSON, "[" + VALID_JSON):
            t.check(False, f"JSON mutation did not apply: {label}")
            continue
        try:
            R.read_json_text(text.encode())
        except R.ReadError:
            t.check(True, label)
        else:
            t.check(False, f"JSON reader accepted: {label}")
    for label, data in (("BOM", b"\xef\xbb\xbf" + VALID_JSON.encode()), ("not UTF-8", VALID_JSON.encode() + b"\xff")):
        try:
            R.read_json_text(data)
        except R.ReadError:
            t.check(True, label)
        else:
            t.check(False, f"JSON reader accepted: {label}")
    # The twin: built from the valid JSON, then broken one way at a time.
    twin = R.TwinReading(
        n=2,
        side=F(2),
        side_text="2",
        ids=("square-1", "square-2"),
        corners=tuple(R.json_corners(p) for p in r.poses),
        envelope={"contract": "packing.squares:Witness/v2", "schema": "s", "envelope": "witness", "status": "enforced"},
        header={
            "id": "W-test",
            "representation": "corners",
            "scalar": {"kind": "rational"},
            "coordinates": {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"},
            "claim": {"coordinate_provenance": "reported", "method": "exact-algebraic", "limitations": "none"},
        },
    )
    good = R.write_twin_text(twin).decode()
    tw = R.read_twin_text(good.encode())
    t.check(tw.corners == twin.corners and tw.n == 2 and tw.side == 2, "valid twin read")
    t.check(R.compare_twin(r, tw)["agree"], "twin agrees")
    t.check(R.compare_twin(r, tw)["listings"] == {"start 0, sense +": 2}, "twin listing start 0, sense +")
    rot = R.TwinReading(**{**tw.__dict__, "corners": tuple(cs[1:] + cs[:1] for cs in tw.corners)})
    t.check(R.compare_twin(r, rot)["agree"] and R.compare_twin(r, rot)["listings"] == {"start 1, sense +": 2}, "twin rotated start")
    rev = R.TwinReading(**{**tw.__dict__, "corners": tuple(tuple(reversed(cs)) for cs in tw.corners)})
    t.check(R.compare_twin(r, rev)["agree"] and R.compare_twin(r, rev)["listings"] == {"start 3, sense -": 2}, "twin reversed")
    c0 = tw.corners[0]
    off = ((c0[0][0] + TINY, c0[0][1]), c0[1], c0[2], c0[3])
    moved = R.TwinReading(**{**tw.__dict__, "corners": (off, tw.corners[1])})
    t.check(not R.compare_twin(r, moved)["agree"], "twin corner off by 1e-30")
    swapped = R.TwinReading(**{**tw.__dict__, "corners": ((c0[1], c0[0], c0[2], c0[3]), tw.corners[1])})
    t.check(not R.compare_twin(r, swapped)["agree"], "twin corners out of cyclic order")
    t.check(not R.compare_twin(r, R.TwinReading(**{**tw.__dict__, "side": F(3), "side_text": "3"}))["agree"], "twin side differs")
    bad_twin = {
        "anchor and alias": good.replace("kind: rational", "kind: &k rational").replace("origin: lower-left", "origin: *k"),
        "explicit tag": good.replace("kind: rational", "kind: !!str rational"),
        "two documents": good + "---\na: b\n",
        "duplicate key": good.replace("  n: 2\n", "  n: 2\n  n: 2\n"),
        "float": good.replace("  n: 2\n", "  n: 2.0\n"),
        "bool": good.replace("status: enforced", "status: yes"),
        "null": good.replace("status: enforced", "status:"),
        "hex int": good.replace("  n: 2\n", "  n: 0x2\n"),
        "key outside schema": good.replace("  n: 2\n", "  n: 2\n  extra: x\n"),
        "missing claim": good.replace("  claim:\n", "  claimx:\n"),
        "representation": good.replace("representation: corners", "representation: center-basis"),
        "scalar kind": good.replace("kind: rational", "kind: decimal"),
        "origin": good.replace("origin: lower-left", "origin: container-center"),
        "contract": good.replace("contract: packing.squares:Witness/v2", "contract: packing.squares:Witness/v1"),
        "id order": good.replace("id: square-1", "id: square-9"),
        "count": good.replace("  n: 2\n", "  n: 3\n"),
        "unquoted int scalar": good.replace("- '0'", "- 0", 1),
        "non-canonical scalar": good.replace("- '2'", "- 4/2", 1),
    }
    for label, text in bad_twin.items():
        if text == good:
            t.check(False, f"twin mutation did not apply: {label}")
            continue
        try:
            R.read_twin_text(text.encode())
        except R.ReadError:
            t.check(True, label)
        else:
            t.check(False, f"twin reader accepted: {label}")
    for label, corners in (
        ("three corners", (tw.corners[0][:3], tw.corners[1])),
        ("five corners", (tw.corners[0] + tw.corners[0][:1], tw.corners[1])),
    ):
        text = R.write_twin_text(R.TwinReading(**{**tw.__dict__, "corners": corners})).decode()
        try:
            R.read_twin_text(text.encode())
        except R.ReadError:
            t.check(True, label)
        else:
            t.check(False, f"twin reader accepted: {label}")
    return t.cases - n0


def whole_file_cases(t: Tally) -> int:
    """Four whole-file decisions with known verdicts."""
    n0 = t.cases
    half, three = F(1, 2), F(3, 2)
    grid = [Pose(half, half, F(1), F(0)), Pose(three, half, F(1), F(0)), Pose(half, three, F(1), F(0)), Pose(three, three, F(1), F(0))]
    d = D.decide(4, F(2), grid, [R.json_corners(p) for p in grid])
    # 2x2 grid in [0, 2]^2: every pair touches (four edges, two corners); 8 wall contacts.
    t.check(d.verdict == "ACCEPT", "grid accepted")
    t.check(all(c == "touch" for c in d.class_a.values()) and all(c == "touch" for c in d.class_b.values()), "grid: 6 touching")
    t.check(sum(1 for c in d.clear.values() if c == 0) == 8, "grid: 8 wall contacts")
    dup = [grid[0], grid[0], grid[2], grid[3]]
    d = D.decide(4, F(2), dup, [R.json_corners(p) for p in dup])
    t.check(d.verdict == "REFUSE" and d.class_a[(1, 2)] == "overlap" and d.margins[(1, 2)] == -1, "duplicate refused")
    d = D.decide(4, F(2) - TINY, grid, [R.json_corners(p) for p in grid])
    t.check(d.verdict == "REFUSE" and d.clear[(4, "right")] == -TINY, "box 1e-30 too small refused")
    # A 3-4-5 square has half-extent 7/10, so in the box of side 7/5 centred it touches all four walls.
    one = [Pose(F(7, 10), F(7, 10), F(3, 5), F(4, 5))]
    d = D.decide(1, F(7, 5), one, [R.json_corners(p) for p in one])
    t.check(d.verdict == "ACCEPT" and all(c == 0 for c in d.clear.values()), "3-4-5 touching four walls")
    return t.cases - n0


def run_pairs_and_walls(t: Tally) -> dict[str, int]:
    return {
        "edge": edge_cases(t),
        "corner": corner_cases(t),
        "vertex_on_edge": vertex_on_edge_cases(t),
        "overlap": overlap_cases(t),
        "walls": wall_cases(t),
    }


def broken(name: str, patch: Callable[[], Callable[[], None]]) -> int:
    undo = patch()
    try:
        t = Tally()
        run_pairs_and_walls(t)
        return len(t.failed)
    finally:
        undo()


def patch_a_own_normals() -> Callable[[], None]:
    orig = A.pair_margin

    def only_first(p: A.IntSquare, q: A.IntSquare) -> tuple[F, int]:
        gaps, den = A.pair_gaps(p, q)
        return F(max(gaps[:2]), den), 1

    A.pair_margin = only_first

    def undo() -> None:
        A.pair_margin = orig

    return undo


def patch_a_zero_apart() -> Callable[[], None]:
    orig = A.pair_class
    A.pair_class = lambda m: "apart" if m >= 0 else "overlap"

    def undo() -> None:
        A.pair_class = orig

    return undo


def patch_b_open() -> Callable[[], None]:
    orig = B.clip_by

    def open_clip(poly: list[B.Pt], f: B.Lin) -> list[B.Pt]:
        out: list[B.Pt] = []
        n = len(poly)
        for k in range(n):
            cur, prev = poly[k], poly[k - 1]
            fc, fp = f(cur), f(prev)
            if fc > 0:
                if fp <= 0:
                    tt = fp / (fp - fc)
                    out.append((prev[0] + tt * (cur[0] - prev[0]), prev[1] + tt * (cur[1] - prev[1])))
                out.append(cur)
            elif fp > 0:
                tt = fp / (fp - fc)
                out.append((prev[0] + tt * (cur[0] - prev[0]), prev[1] + tt * (cur[1] - prev[1])))
        return out

    B.clip_by = open_clip

    def undo() -> None:
        B.clip_by = orig

    return undo


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    t0 = time.process_time()
    t = Tally()
    groups: dict[str, int] = {}
    n0 = t.cases
    unit_cases(t)
    groups["unit"] = t.cases - n0
    groups.update(run_pairs_and_walls(t))
    groups["random"] = random_cases(t)
    groups["reader"] = reader_cases(t)
    groups["whole_file"] = whole_file_cases(t)
    broken_counts = {
        "method A with only square i's normals": broken("a-own", patch_a_own_normals),
        "method A counting a zero margin as apart": broken("a-zero", patch_a_zero_apart),
        "method B clipping with open half-planes": broken("b-open", patch_b_open),
    }
    passed = not t.failed and all(v > 0 for v in broken_counts.values())
    receipt = {
        "program": "l180_selftest.py",
        "lane": "L180",
        "verdict": "PASSED" if passed else "FAILED",
        "cases": t.cases,
        "failed": len(t.failed),
        "first_failures": t.failed[:30],
        "groups": groups,
        "broken_copies_failures": broken_counts,
        "cpu_seconds": round(time.process_time() - t0, 2),
    }
    with open(argv[1], "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=1)
        fh.write("\n")
    print(f"{receipt['verdict']} {t.cases} cases {len(t.failed)} failed; broken copies fail {broken_counts}")
    for f in t.failed[:10]:
        print("  ", f)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
