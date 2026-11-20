"""Self-test of the review of jlevy/squares#1031: synthetic data only.

Written for this review; imports nothing from this repository or the source.

    python -I -B rv1031_selftest.py --out selftest.json

Holds the readers, method A, method B, the third formulation (corner projections) and
the contraction program to values derived by hand, then runs the same suite under
deliberately broken copies, each of which must fail at least one check.
"""

from __future__ import annotations

import argparse
import json
import os
import math
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # this packet's own modules, under python -I

import rv1031_axes as A
import rv1031_clip as B
import rv1031_contract as K
import rv1031_decide as D
import rv1031_reader as R

TINY = F(1, 10**40)
GAPS = [TINY, F(0), -TINY, F(1, 7), -F(1, 7)]
DIRS = [(F(1), F(0)), (F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(15, 17), F(8, 17)), (F(-4, 5), F(3, 5))]


class Suite:
    def __init__(self) -> None:
        self.checks = 0
        self.failures: list[str] = []

    def ok(self, cond: bool, what: str) -> None:
        self.checks += 1
        if not cond:
            self.failures.append(what)


def b_pair(pi: A.Pose, pj: A.Pose, sense_j: str = "ccw", start_j: int = 0) -> tuple[str, object]:
    ci = B.ccw(B.to_mpq(R.pose_corners(pi)))
    cj = B.to_mpq(R.pose_corners(pj))
    cj = cj[start_j:] + cj[:start_j]
    if sense_j == "cw":
        cj = list(reversed(cj))
    return B.pair_class(ci, B.ccw(cj))


def expect_pair(s: Suite, pi: A.Pose, pj: A.Pose, margin: F, area: F | None, what: str) -> None:
    for a, b in ((pi, pj), (pj, pi)):
        m = A.pair_margin(a, b)
        s.ok(m == margin, f"{what}: A margin {D.short(m)} != {D.short(margin)}")
        cp = A.corner_projection_margin(R.pose_corners(a), R.pose_corners(b))
        s.ok(cp == margin, f"{what}: corner projections {D.short(cp)} != {D.short(margin)}")
    for sense in ("ccw", "cw"):
        for start in range(4):
            try:
                kb, ab = b_pair(pi, pj, sense, start)
            except (AssertionError, ValueError) as exc:
                s.ok(False, f"{what}: B raised {exc} ({sense}, {start})")
                continue
            s.ok(kb == A.klass(margin), f"{what}: B class {kb} != {A.klass(margin)} ({sense}, {start})")
            if area is not None:
                s.ok(B.mpq_to_fraction(ab) == area, f"{what}: B area {ab} != {area} ({sense}, {start})")


def edge_contacts(s: Suite) -> None:
    for ux, uy in DIRS:
        vx, vy = -uy, ux
        for nx, ny, tx, ty in ((ux, uy, vx, vy), (-ux, -uy, vx, vy), (vx, vy, ux, uy), (-vx, -vy, ux, uy)):
            for tau in (F(0), F(1, 3), -F(1, 3)):
                for g in GAPS:
                    pi = (F(0), F(0), ux, uy)
                    pj = ((1 + g) * nx + tau * tx, (1 + g) * ny + tau * ty, ux, uy)
                    area = -g * (1 - abs(tau)) if g < 0 else F(0)
                    expect_pair(s, pi, pj, g, area, f"edge dir {ux},{uy} tau {tau} gap {D.short(g)}")
            for g in GAPS:
                pi = (F(0), F(0), ux, uy)
                pj = ((1 + g) * (nx + tx), (1 + g) * (ny + ty), ux, uy)
                area = g * g if g < 0 else F(0)
                expect_pair(s, pi, pj, g, area, f"corner dir {ux},{uy} gap {D.short(g)}")


def rot90(p: A.Pose, k: int) -> A.Pose:
    x, y, ux, uy = p
    for _ in range(k):
        x, y, ux, uy = -y, x, -uy, ux
    return (x, y, ux, uy)


def tilted_corner(s: Suite) -> None:
    for (ux, uy), factor in (((F(3, 5), F(4, 5)), F(25, 24)), ((F(5, 13), F(12, 13)), F(169, 120))):
        h = (ux + uy) / 2
        for g in GAPS:
            pi = (F(0), F(0), F(1), F(0))
            pj = (F(1, 2) + h + g, F(0), ux, uy)
            area = factor * g * g if g < 0 else F(0)
            for k in range(4):
                expect_pair(s, rot90(pi, k), rot90(pj, k), g, area, f"tilted corner {ux},{uy} gap {D.short(g)} turn {k}")


def duplicates(s: Suite) -> None:
    for ux, uy in DIRS:
        p = (F(1, 3), F(2, 7), ux, uy)
        expect_pair(s, p, p, F(-1), F(1), f"duplicate {ux},{uy}")
    for (ux, uy), m, area in (((F(3, 5), F(4, 5)), -F(6, 5), F(5, 6)), ((F(5, 13), F(12, 13)), -F(15, 13), F(13, 15))):
        expect_pair(s, (F(0), F(0), F(1), F(0)), (F(0), F(0), ux, uy), m, area, f"concentric {ux},{uy}")


def walls(s: Suite) -> None:
    side = F(5)
    for ux, uy in DIRS:
        h = (abs(ux) + abs(uy)) / 2
        for g in (TINY, F(0), -TINY, F(1, 9), -F(1, 9)):
            cases = {
                0: (h + g, F(5, 2)),
                1: (F(5, 2), h + g),
                2: (side - h - g, F(5, 2)),
                3: (F(5, 2), side - h - g),
            }
            for w, (x, y) in cases.items():
                p = (x, y, ux, uy)
                c = A.clearances(p, side)
                s.ok(c[w] == g, f"wall {w} dir {ux},{uy}: A clearance {D.short(c[w])} != {D.short(g)}")
                cq = B.ccw(B.to_mpq(R.pose_corners(p)))
                wb = B.wall_terms(cq, B.mpq(5))
                s.ok(B.mpq_to_fraction(wb[w]) == g, f"wall {w} dir {ux},{uy}: B term != gap")
                inside = B.mpq_to_fraction(B.area_inside(cq, B.mpq(5)))
                if g >= 0:
                    want = F(1)
                elif ux == 0 or uy == 0:
                    want = 1 + g
                else:
                    want = 1 - g * g / (2 * abs(ux * uy))
                s.ok(inside == want, f"wall {w} dir {ux},{uy} gap {D.short(g)}: area inside {inside} != {want}")


def json_text(n: int, side: str, rows: list[list[str]]) -> bytes:
    doc = {"n": n, "side": side, "square_size": "1", "format": "synthetic", "squares": rows}
    return json.dumps(doc, indent=1).encode()


def witness_text(n: int, side: str, corners: list[list[tuple[str, str]]], quote: bool = True) -> bytes:
    lines = [
        "softschema:", "  contract: packing.squares:Witness/v2", "  schema: x", "  envelope: witness", "  status: enforced",
        "witness:", "  id: W-n002-selftest", f"  n: {n}", f"  side: '{side}'", "  square_size: '1'", "  representation: corners",
        "  scalar:", "    kind: rational", "  coordinates:", "    origin: lower-left", "    axes: x-right-y-up", "    angle_unit: not-applicable",
        "  claim:", "    coordinate_provenance: reported", "    method: exact-algebraic", "    limitations: synthetic", "  squares:",
    ]
    for k, cs in enumerate(corners, start=1):
        lines.append(f"  - id: square-{k}")
        lines.append("    corners:")
        for x, y in cs:
            # quote=False writes fractions plain and integers quoted, as the source does
            qx = "'" if quote or "/" not in x else ""
            qy = "'" if quote or "/" not in y else ""
            lines.append(f"    - - {qx}{x}{qx}")
            lines.append(f"      - {qy}{y}{qy}")
    return ("\n".join(lines) + "\n").encode()


def readers(s: Suite) -> None:
    rows = [["1/2", "1/2", "1", "0"], ["3/2", "7/10", "3/5", "4/5"]]
    good_j = json_text(2, "3", rows)
    dj = R.read_json_bytes(good_j)
    s.ok(dj["n"] == 2 and dj["side"] == 3 and dj["poses"][1] == (F(3, 2), F(7, 10), F(3, 5), F(4, 5)), "J: valid file not read back")
    corners = [[(D.fstr(x), D.fstr(y)) for x, y in R.pose_corners(p)] for p in dj["poses"]]
    good_c = witness_text(2, "3", corners)
    dc = R.read_witness_bytes(good_c)
    s.ok(dc["n"] == 2 and dc["corners"][1] == R.pose_corners(dj["poses"][1]), "C: valid file not read back")
    s.ok(R.read_witness_bytes(witness_text(2, "3", corners, quote=False))["corners"] == dc["corners"], "C: plain fractions not read")
    bad_j = {
        "plus": good_j.replace(b'"3/2"', b'"+3/2"', 1),
        "float string": good_j.replace(b'"3/2"', b'"1.5"', 1),
        "exponent string": good_j.replace(b'"3/2"', b'"15e-1"', 1),
        "space": good_j.replace(b'"3/2"', b'" 3/2"', 1),
        "leading zero": good_j.replace(b'"3/2"', b'"03/2"', 1),
        "zero denominator": good_j.replace(b'"3/2"', b'"3/0"', 1),
        "negative denominator": good_j.replace(b'"3/2"', b'"3/-2"', 1),
        "double minus": good_j.replace(b'"3/2"', b'"--3/2"', 1),
        "json number": good_j.replace(b'"3/2"', b"1.5", 1),
        "json integer scalar": good_j.replace(b'"3/2"', b"2", 1),
        "nan": good_j.replace(b'"3/2"', b"NaN", 1),
        "duplicate key": good_j.replace(b'"n": 2,', b'"n": 2, "n": 2,', 1),
        "missing key": good_j.replace(b'"format": "synthetic",', b"", 1),
        "extra key": good_j.replace(b'"n": 2,', b'"n": 2, "x": 1,', 1),
        "count": good_j.replace(b'"n": 2,', b'"n": 3,', 1),
        "bool n": good_j.replace(b'"n": 2,', b'"n": true,', 1),
        "string n": good_j.replace(b'"n": 2,', b'"n": "2",', 1),
        "square size": good_j.replace(b'"square_size": "1"', b'"square_size": "2"', 1),
        "not unit": good_j.replace(b'"3/5"', b'"3/4"', 1),
        "tab": good_j.replace(b'"n": 2,', b'"n":\t2,', 1),
        "carriage return": good_j.replace(b"\n", b"\r\n", 1),
        "non-ascii": good_j.replace(b'"synthetic"', '"synth\u00e9tic"'.encode(), 1),
        "row of three": good_j.replace(b'"1",\n   "0"', b'"1"', 1),
    }
    for name, raw in bad_j.items():
        s.ok(raw != good_j, f"J mutation {name} did not apply")
        try:
            R.read_json_bytes(raw)
            s.ok(False, f"J: {name} was read")
        except R.ReadError:
            s.ok(True, "")
    bad_c = {
        "contract": good_c.replace(b"Witness/v2", b"Witness/v1", 1),
        "missing claim": good_c.replace(b"  claim:\n    coordinate_provenance: reported\n    method: exact-algebraic\n    limitations: synthetic\n", b"", 1),
        "extra key": good_c.replace(b"  square_size: '1'", b"  square_size: '1'\n  extra: 1", 1),
        "anchor alias": good_c.replace(b"  scalar:\n    kind: rational", b"  scalar: &k\n    kind: rational\n  certificate: *k", 1),
        "tag": good_c.replace(b"  side: '3'", b"  side: !!str 3", 1),
        "duplicate key": good_c.replace(b"  n: 2", b"  n: 2\n  n: 2", 1),
        "tab": good_c.replace(b"  n: 2", b"  n:\t2", 1),
        "ids": good_c.replace(b"id: square-1", b"id: square-2", 1),
        "three scalars": good_c.replace(b"    - - '", b"    - - '1'\n      - '", 1),
        "plain float": good_c.replace(b"  side: '3'", b"  side: 3.0", 1),
        "quoted float": good_c.replace(b"  side: '3'", b"  side: '3.0'", 1),
        "plain integer side": good_c.replace(b"  side: '3'", b"  side: 3", 1),
        "representation": good_c.replace(b"representation: corners", b"representation: center-angle", 1),
        "kind": good_c.replace(b"kind: rational", b"kind: decimal", 1),
        "two documents": good_c + b"---\na: 1\n",
        "origin": good_c.replace(b"origin: lower-left", b"origin: upper-left", 1),
        "axes": good_c.replace(b"axes: x-right-y-up", b"axes: x-right-y-down", 1),
        "count": good_c.replace(b"  n: 2", b"  n: 3", 1),
        "plus": good_c.replace(b"    - - '", b"    - - '+", 1),
        "plain integer coordinate": witness_text(2, "3", [[("1", "1")] + cs[1:] for cs in corners], quote=True).replace(b"    - - '1'", b"    - - 1", 1),
    }
    for name, raw in bad_c.items():
        s.ok(raw != good_c, f"C mutation {name} did not apply")
        try:
            R.read_witness_bytes(raw)
            s.ok(False, f"C: {name} was read")
        except R.ReadError:
            s.ok(True, "")
    good_p = b"# synthetic\n2 3\n1/2 1/2 0\n3/2 7/10 1/2\n"
    dp = R.read_cert_bytes(good_p)
    s.ok(dp["poses"][1] == (F(3, 2), F(7, 10), F(3, 5), F(4, 5)), "P: valid file not read back (t = 1/2 gives (3/5, 4/5))")
    bad_p = {
        "no final newline": good_p[:-1],
        "comment after header": good_p.replace(b"2 3\n", b"2 3\n# x\n", 1),
        "row of two": good_p.replace(b"1/2 1/2 0", b"1/2 1/2", 1),
        "header": good_p.replace(b"2 3\n", b"2  3\n", 1),
        "count": good_p.replace(b"2 3\n", b"3 3\n", 1),
        "plus": good_p.replace(b"1/2 1/2 0", b"+1/2 1/2 0", 1),
    }
    for name, raw in bad_p.items():
        s.ok(raw != good_p, f"P mutation {name} did not apply")
        try:
            R.read_cert_bytes(raw)
            s.ok(False, f"P: {name} was read")
        except R.ReadError:
            s.ok(True, "")
    notes: list[str] = []
    s.ok(R.parse_scalar("6/4", "x", notes) == F(3, 2) and notes, "a non-canonical scalar is not read and flagged")
    # corners that are not unit squares
    sq = R.pose_corners((F(0), F(0), F(3, 5), F(4, 5)))
    shapes = {
        "corner off": [(sq[0][0] + TINY, sq[0][1])] + sq[1:],
        "bowtie": [sq[0], sq[2], sq[1], sq[3]],
        "rhombus": [(F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "rectangle": [(F(0), F(0)), (1 + TINY, F(0)), (1 + TINY, F(1)), (F(0), F(1))],
        "side two": [(F(0), F(0)), (F(2), F(0)), (F(2), F(2)), (F(0), F(2))],
        "point": [(F(0), F(0))] * 4,
        "repeated corner": [sq[0], sq[0], sq[2], sq[3]],
    }
    for name, cs in shapes.items():
        s.ok(B.unit_square_sense(B.to_mpq(cs)) is None, f"B: {name} taken for a unit square")
        s.ok(R.corners_pose(cs) is None, f"reader: {name} given a pose")
    s.ok(R.twin_match(sq, sq) == (0, "ccw"), "twin: identity")
    s.ok(R.twin_match(sq, sq[1:] + sq[:1]) == (1, "ccw"), "twin: rotation")
    s.ok(R.twin_match(sq, list(reversed(sq))) == (3, "cw"), "twin: reversal")
    s.ok(R.twin_match(sq, [(x + TINY, y) for x, y in sq]) is None, "twin: moved square")


def whole_files(s: Suite) -> None:
    grid = [(F(1, 2), F(1, 2), F(1), F(0)), (F(3, 2), F(1, 2), F(1), F(0)), (F(1, 2), F(3, 2), F(1), F(0)), (F(3, 2), F(3, 2), F(1), F(0))]
    for side, want_ok, contacts, wall_contacts in ((F(2), True, 6, 8), (2 - TINY, False, 6, 4), (2 + TINY, True, 6, 4)):
        da = D.decide_a(grid, side)
        db = D.decide_b([R.pose_corners(p) for p in grid], side)
        sa = D.summarize_a(da, side)
        c = D.compare(da, db)
        s.ok(D.verdict_ok(sa, c) == want_ok, f"grid in {D.short(side)}: verdict")
        s.ok(sa["classes"]["contact"] == contacts, f"grid in {D.short(side)}: {sa['classes']['contact']} contacts")
        s.ok(len(sa["wall_contacts"]) == wall_contacts, f"grid in {D.short(side)}: {len(sa['wall_contacts'])} wall contacts")
        s.ok(not c["pair_mismatches"] and not c["wall_mismatches"] and not c["inside_not_one"], f"grid in {D.short(side)}: methods disagree")
    dup = grid + [grid[0]]
    da = D.decide_a(dup, F(2))
    db = D.decide_b([R.pose_corners(p) for p in dup], F(2))
    s.ok(not D.verdict_ok(D.summarize_a(da, F(2)), D.compare(da, db)), "duplicate square accepted")
    s.ok(da["margins"][(0, 4)] == -1, "duplicate square margin")
    tilt = [(F(7, 10), F(7, 10), F(3, 5), F(4, 5))]
    da = D.decide_a(tilt, F(7, 5))
    db = D.decide_b([R.pose_corners(p) for p in tilt], F(7, 5))
    sa = D.summarize_a(da, F(7, 5))
    s.ok(D.verdict_ok(sa, D.compare(da, db)) and len(sa["wall_contacts"]) == 4, "3-4-5 square in its box of side 7/5")
    e = D.extent(grid)
    s.ok(e["width"] == 2 and e["height"] == 2 and e["xmin"] == 0, "extent of the grid")


def random_direction(rng: random.Random) -> tuple[F, F]:
    t = F(rng.randint(-10**6, 10**6), rng.randint(1, 10**6))
    return R.tangent_direction(t)


def random_pairs(s: Suite, rng: random.Random) -> None:
    for k in range(300):
        pi = (F(rng.randint(0, 10**9), 10**9), F(rng.randint(0, 10**9), 10**9), *random_direction(rng))
        ang = rng.random() * 6.283
        r = F(rng.randint(5 * 10**8, 16 * 10**8), 10**9)
        dx = r * F(round(math.cos(ang) * 10**9), 10**9)
        dy = r * F(round(math.sin(ang) * 10**9), 10**9)
        pj = (pi[0] + dx, pi[1] + dy, *random_direction(rng))
        m = A.pair_margin(pi, pj)
        cp = A.corner_projection_margin(R.pose_corners(pi), R.pose_corners(pj))
        s.ok(m == cp, f"random pair {k}: A and corner projections differ")
        s.ok(m == A.pair_margin(pj, pi), f"random pair {k}: A not symmetric")
        kb, _ = b_pair(pi, pj)
        s.ok(kb == A.klass(m), f"random pair {k}: B class {kb}, A {A.klass(m)}")
        big, h, _ = A.pair_terms(pi, pj)
        for target in (TINY, F(0), -TINY):
            sc = (target + h) / big
            pk = (pi[0] + sc * dx, pi[1] + sc * dy, pj[2], pj[3])
            mk = A.pair_margin(pi, pk)
            s.ok(mk == target, f"random pair {k} closed to {D.short(target)}: margin {D.short(mk)}")
            kb, ab = b_pair(pi, pk)
            s.ok(kb == A.klass(target), f"random pair {k} closed to {D.short(target)}: B {kb}")
            if target == 0:
                s.ok(ab == 0, f"random pair {k} at contact: area {ab}")
    side = F(9)
    for k in range(100):
        ux, uy = random_direction(rng)
        h = (abs(ux) + abs(uy)) / 2
        for w in range(4):
            for g in (TINY, F(0), -TINY):
                pos = {0: (h + g, F(9, 2)), 1: (F(9, 2), h + g), 2: (side - h - g, F(9, 2)), 3: (F(9, 2), side - h - g)}[w]
                p = (pos[0], pos[1], ux, uy)
                c = A.clearances(p, side)
                cq = B.ccw(B.to_mpq(R.pose_corners(p)))
                wb = B.mpq_to_fraction(B.wall_terms(cq, B.mpq(9))[w])
                inside = B.area_inside(cq, B.mpq(9))
                s.ok(c[w] == g and wb == g, f"random wall {k},{w}: clearance")
                s.ok((inside == 1) == (g >= 0), f"random wall {k},{w}: area inside {inside}")


def contraction(s: Suite) -> None:
    eps, gam = F(3, 10**30), F(1, 10**28)
    base = [(F(1, 2), F(1, 2)), (F(3, 2), F(1, 2)), (F(1, 2), F(3, 2)), (F(3, 2), F(3, 2))]
    poses = [(x * (1 + eps) + gam - eps / 2, y * (1 + eps) + gam - eps / 2, F(1), F(0)) for x, y in base]
    side = 2 + eps + 2 * gam
    rec = K.contraction(poses, side)
    s.ok(rec["verdict"] == "MEASURED", f"contraction: verdict {rec['verdict']}")
    s.ok(F(rec["g_star"]) == 1 / (1 + eps), "contraction: g* is 1/(1+eps)")
    s.ok(F(rec["contraction_margin"]) == eps + 2 * gam, "contraction: margin is eps + 2 gamma")
    s.ok(F(rec["wall_slack"]) == 2 * gam and F(rec["contraction_part"]) == eps, "contraction: wall slack and contraction part")
    s.ok(rec["first_contact_pair_count"] == 6, "contraction: six pairs first touch together")
    grid = [(x, y, F(1), F(0)) for x, y in base]
    rec = K.contraction(grid, F(2) + gam)
    s.ok(F(rec["g_star"]) == 1 and F(rec["contraction_margin"]) == gam, "contraction: a contact packing gives only its wall slack")
    tilted = [(F(1), F(1), F(3, 5), F(4, 5)), (F(1) + F(7, 5) + 2 * eps, F(1), F(3, 5), F(4, 5))]
    rec = K.contraction(tilted, F(5))
    m, h, _ = A.pair_terms(tilted[0], tilted[1])
    s.ok(F(rec["g_star"]) == h / m, "contraction: a tilted pair's factor")
    s.ok(K.contraction(grid + [grid[0]], F(2))["verdict"] == "NOT_A_PACKING", "contraction: an overlapping packing measured")


def suite(seed: int = 1031) -> Suite:
    s = Suite()
    rng = random.Random(seed)
    edge_contacts(s)
    tilted_corner(s)
    duplicates(s)
    walls(s)
    readers(s)
    whole_files(s)
    random_pairs(s, rng)
    contraction(s)
    return s


# ---------------------------------------------------------------------------- mutants


def _mutant_one_side(p: A.Pose, q: A.Pose) -> tuple[F, F, int]:
    cxi, cyi, uxi, uyi = p
    cxj, cyj, uxj, uyj = q
    dx, dy = cxj - cxi, cyj - cyi
    cos_d = uxi * uxj + uyi * uyj
    sin_d = uxi * uyj - uyi * uxj
    h = F(1, 2) + (abs(cos_d) + abs(sin_d)) / 2
    vals = (abs(dx * uxi + dy * uyi), abs(-dx * uyi + dy * uxi))
    return max(vals), h, 0


def _mutant_signed_sin(p: A.Pose, q: A.Pose) -> tuple[F, F, int]:
    m, h, k = ORIG["pair_terms"](p, q)
    cos_d = p[2] * q[2] + p[3] * q[3]
    sin_d = p[2] * q[3] - p[3] * q[2]
    return m, F(1, 2) + (abs(cos_d) + sin_d) / 2, k


def _mutant_klass(margin: F) -> str:
    return "apart" if margin > 0 else "overlap"


def _mutant_ccw(c: list) -> list:
    if B.unit_square_sense(c) is None:
        raise ValueError("not a unit square")
    return list(c)


def _mutant_scalar(text: object, where: str, notes: list[str] | None = None) -> F:
    if isinstance(text, str) and text.startswith("+"):
        text = text[1:]
    return ORIG["parse_scalar"](text, where, notes)


def _mutant_tangent(t: F) -> tuple[F, F]:
    c, s_ = ORIG["tangent_direction"](t)
    return c, -s_


ORIG = {"pair_terms": A.pair_terms, "klass": A.klass, "ccw": B.ccw, "parse_scalar": R.parse_scalar, "tangent_direction": R.tangent_direction}


PATCHES = {
    "method A with one square's normals only": [(A, "pair_terms", _mutant_one_side)],
    "method A with sin D signed in H": [(A, "pair_terms", _mutant_signed_sin)],
    "method A counting a zero margin as overlap": [(A, "klass", _mutant_klass)],
    "method B with open half-planes": [(B, "OPEN_HALF_PLANES", True)],
    "method B taking every listing as counterclockwise": [(B, "ccw", _mutant_ccw)],
    "a reader that takes a leading plus": [(R, "parse_scalar", _mutant_scalar)],
    "form P read clockwise": [(R, "tangent_direction", _mutant_tangent)],
}


class patched:
    """Apply one broken copy's patches for the length of a with-block."""

    def __init__(self, patches: list) -> None:
        self.patches = patches
        self.saved: list = []

    def __enter__(self) -> None:
        self.saved = [(mod, attr, getattr(mod, attr)) for mod, attr, _ in self.patches]
        for mod, attr, val in self.patches:
            setattr(mod, attr, val)

    def __exit__(self, *exc: object) -> None:
        for mod, attr, val in self.saved:
            setattr(mod, attr, val)


def run_mutant(name: str) -> int:
    with patched(PATCHES[name]):
        try:
            return len(suite().failures)
        except Exception:  # a broken copy may also crash: that is a failure of it
            return 10**6


MUTANTS = [
    "method A with one square's normals only",
    "method A with sin D signed in H",
    "method A counting a zero margin as overlap",
    "method B with open half-planes",
    "method B taking every listing as counterclockwise",
    "a reader that takes a leading plus",
    "form P read clockwise",
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-mutants", action="store_true")
    args = ap.parse_args()
    t0 = time.process_time()
    s = suite()
    rec: dict = {"program": "rv1031_selftest.py", "python": sys.version.split()[0], "arith": B.version(), "checks": s.checks, "failures": s.failures[:100], "failure_count": len(s.failures)}
    if not args.no_mutants:
        rec["mutants"] = {name: run_mutant(name) for name in MUTANTS}
        rec["every_mutant_fails"] = all(v > 0 for v in rec["mutants"].values())
    rec["verdict"] = "PASSED" if not s.failures and rec.get("every_mutant_fails", True) else "FAILED"
    rec["cpu_s"] = round(time.process_time() - t0, 2)
    with open(args.out, "w") as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(rec["verdict"], rec["checks"], rec["failure_count"], rec.get("mutants"))
    return 0 if rec["verdict"] == "PASSED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
