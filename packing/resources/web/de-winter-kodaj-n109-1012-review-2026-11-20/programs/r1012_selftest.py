"""Lane r1012's self-test: the reader, both methods and the third formulation.

Usage: r1012_selftest.py OUT.json

Every expected value below was derived by hand (the comments give the
derivation) or is an identity between the methods. It reads no certificate.
"""

import json
import os
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)

import r1012_clip  # noqa: E402
import r1012_decide  # noqa: E402
import r1012_geom as G  # noqa: E402
import r1012_reader  # noqa: E402
import r1012_sat  # noqa: E402
import r1012_writer  # noqa: E402

CHECKS = [0]
FAILS = []


def check(cond, label):
    CHECKS[0] += 1
    if not cond:
        FAILS.append(label)


def refused(data, label):
    try:
        r1012_reader.read_bytes(data)
    except r1012_reader.ReadError:
        check(True, label)
        return
    check(False, label + " (was read)")


def sq_from(c, e):
    """Corners c - e/2 - f/2, c + e/2 - f/2, c + e/2 + f/2, c - e/2 + f/2, f = e turned left."""
    f = (-e[1], e[0])
    h = F(1, 2)
    return [
        (c[0] - h * e[0] - h * f[0], c[1] - h * e[1] - h * f[1]),
        (c[0] + h * e[0] - h * f[0], c[1] + h * e[1] - h * f[1]),
        (c[0] + h * e[0] + h * f[0], c[1] + h * e[1] + h * f[1]),
        (c[0] - h * e[0] + h * f[0], c[1] - h * e[1] + h * f[1]),
    ]


def box(x0, y0):
    x0, y0 = F(x0), F(y0)
    return [(x0, y0), (x0 + 1, y0), (x0 + 1, y0 + 1), (x0, y0 + 1)]


def amargin(qi, qj):
    a = r1012_sat.Square(qi)
    b = r1012_sat.Square(qj)
    m, _ = r1012_sat.pair_margin(a, b)
    return F(*m)


def bclass(qi, qj):
    pi = r1012_clip.to_mpq(qi)
    pj = r1012_clip.to_mpq(qj)
    oi, si, _ = r1012_clip.unit_square(pi)
    oj, sj, _ = r1012_clip.unit_square(pj)
    assert oi and oj
    c1, a1 = r1012_clip.classify_intersection(
        r1012_clip.clip_by_convex(r1012_clip.ccw(pj, sj), r1012_clip.ccw(pi, si)))
    c2, a2 = r1012_clip.classify_intersection(
        r1012_clip.clip_by_convex(r1012_clip.ccw(pi, si), r1012_clip.ccw(pj, sj)))
    return c1, F(int(a1.numerator), int(a1.denominator)), c2 == c1 and a2 == a1


def test_scalars():
    good = {
        "0": (F(0), "integer", True), "-0": (F(0), "integer", False), "12": (F(12), "integer", True),
        "-7": (F(-7), "integer", True), "1/2": (F(1, 2), "fraction", True),
        "2/4": (F(1, 2), "fraction", False), "-3/7": (F(-3, 7), "fraction", True),
        "1/1": (F(1), "fraction", False), "0/5": (F(0), "fraction", False),
        "0.5": (F(1, 2), "decimal", True), "-0.25": (F(-1, 4), "decimal", True),
        "1.50": (F(3, 2), "decimal", False), "10.949289580944": (F(10949289580944, 10 ** 12), "decimal", True),
    }
    for text, expected in good.items():
        check(r1012_reader.parse_scalar(text, "t") == expected, f"scalar {text!r}")
    for text in ["012", "+1", "3/0", "3/-7", "1e-3", " 1/2", "1/2 ", ".5", "5.", "", "1_000",
                 "0x10", "1/2/3", "--1", "−1", "1,5", "nan", "inf", "1/02", "00.5"]:
        try:
            r1012_reader.parse_scalar(text, "t")
            check(False, f"scalar {text!r} accepted")
        except r1012_reader.ReadError:
            check(True, f"scalar {text!r} refused")
    for value in [5, 0.5, None, True]:
        try:
            r1012_reader.parse_scalar(value, "t")
            check(False, f"non-string {value!r} accepted")
        except r1012_reader.ReadError:
            check(True, f"non-string {value!r} refused")


def test_reader():
    rot = (F(3, 5), F(4, 5))
    quads = [box(0, 0), box(1, 0), sq_from((F(19, 10), F(27, 10)), rot)]
    ids = ["square-0", "square-1", "square-2"]
    side = F(4)
    data = r1012_writer.write(3, side, ids, quads)
    p = r1012_reader.read_bytes(data)
    check(p["n"] == 3 and p["side"] == side and p["ids"] == ids and p["corners"] == quads, "round trip")
    check(p["noncanonical"] == [] and p["scalar_forms"]["decimal"] == 0, "canonical writer")
    check(p["enveloped"] and p["origin"] == "lower-left", "envelope and origin")
    text = data.decode()
    # origin container-center: same lower-left values back
    pc = r1012_reader.read_bytes(r1012_writer.write(3, side, ids, quads, origin="container-center"))
    check(pc["corners"] == quads and pc["origin"] == "container-center", "container-center shift")
    # integer ids
    pi = r1012_reader.read_bytes(r1012_writer.write(3, side, [1, 2, 3], quads))
    check(pi["ids"] == [1, 2, 3], "integer ids")
    # the bare witness (no envelope)
    bare = "\n".join(line[2:] for line in text.splitlines()[6:]) + "\n"
    pb = r1012_reader.read_bytes(bare.encode())
    check(not pb["enveloped"] and pb["corners"] == quads, "bare witness")
    # refusals
    first_corner = text.splitlines()[20]
    check(first_corner.startswith("    - ['0', '0']"), "layout assumption")
    refused(text.replace("  n: 3\n", "  n: 4\n").encode(), "n too large")
    refused(text.replace("  side: '4'\n", "  side: 4.0\n").encode(), "float side")
    refused(text.replace("  side: '4'\n", "  side: 4\n").encode(), "integer side")
    refused(text.replace("    - ['0', '0']", "    - ['+0', '0']", 1).encode(), "plus sign")
    refused(text.replace("    - ['0', '0']", "    - [0, '0']", 1).encode(), "plain integer coordinate")
    refused(text.replace("    - ['0', '0']", "    - ['0', '0', '0']", 1).encode(), "three scalars")
    refused(text.replace("    corners:\n    - ['0', '0']", "    corners:\n    - ['0', '0']\n    - ['0', '0']", 1).encode(), "five corners")
    refused(text.replace("  side: '4'\n", "  side: '4'\n  side: '4'\n").encode(), "duplicate key")
    refused(text.replace("  - id: 'square-0'\n    corners:\n", "  - id: 'square-0'\n    corners: &a\n", 1).encode(), "anchor")
    anchored = text.replace("  - id: 'square-0'\n    corners:\n", "  - id: 'square-0'\n    corners: &a\n", 1)
    lines = anchored.splitlines()
    k = lines.index("  - id: 'square-1'")
    alias = "\n".join(lines[: k + 1] + ["    corners: *a"] + lines[k + 6:]) + "\n"
    refused(alias.encode(), "alias")
    refused(text.replace("  side: '4'\n", "  side: !!str '4'\n").encode(), "explicit tag")
    refused(("%YAML 1.1\n---\n" + text).encode(), "directive")
    refused((text + "---\n" + text).encode(), "two documents")
    refused(text.replace("representation: corners", "representation: center-angle").encode(), "representation")
    refused(text.replace("    kind: rational", "    kind: decimal").encode(), "scalar kind")
    refused(text.replace("  square_size: '1'", "  square_size: '2'").encode(), "square size")
    refused(text.replace("    axes: x-right-y-up", "    axes: x-right-y-down").encode(), "axes")
    refused(text.replace("    origin: lower-left", "    origin: upper-left").encode(), "origin")
    refused(text.replace("  - id: 'square-1'", "  - id: 'square-0'").encode(), "duplicate id")
    refused(text.replace("  - id: 'square-1'", "  - id: 0").encode(), "id zero")
    refused(text.replace("    method: exact-algebraic\n", "").encode(), "claim key missing")
    refused(text.replace("  square_size:", "  colour: red\n  square_size:").encode(), "unknown witness key")
    refused(text.replace("  contract: packing.squares:Witness/v2", "  contract: packing.squares:Witness/v1").encode(), "contract v1")
    refused(text.replace("  side: '4'", "  side: '4/0'").encode(), "zero denominator")
    refused(text.replace("  side: '4'", "  side: '-4'").encode(), "negative side")
    refused(text.replace("  side: '4'", "  side: '1e1'").encode(), "exponent")
    refused(b"\xff\xfe" + data, "not UTF-8")
    refused(text.replace("  - id: 'square-0'\n", "  - id: 'square-0'\n    colour: red\n", 1).encode(), "unknown square key")
    # accepted variants
    p2 = r1012_reader.read_bytes(text.replace("  side: '4'", "  side: '8/2'").encode())
    check(p2["side"] == 4 and p2["noncanonical"] == ["side"], "2p/2q side read, flagged")
    p3 = r1012_reader.read_bytes(text.replace("  side: '4'", "  side: '4.0'").encode())
    check(p3["side"] == 4 and p3["scalar_forms"]["decimal"] == 1, "quoted decimal side read")
    p4 = r1012_reader.read_bytes(("---\n" + text).encode())
    check(p4["corners"] == quads, "explicit document start read")
    p5 = r1012_reader.read_bytes(text.replace("  - id: 'square-0'\n", "  - id: 'square-0'\n    center: ['1/2', '1/2']\n", 1).encode())
    check(p5["square_info_keys"] == {"center": 1} and p5["corners"] == quads, "informational centre ignored")


def test_hand_geometry():
    A = box(0, 0)
    # T1 shared edge: margin 0, touch, intersection a segment of area 0
    B = box(1, 0)
    check(amargin(A, B) == 0, "T1 A margin")
    check(G.margin(A, B) == 0, "T1 geom margin")
    c, a, agree = bclass(A, B)
    check(c == "touch" and a == 0 and agree, "T1 B")
    # T2 gap 1/2
    B = box(F(3, 2), 0)
    check(amargin(A, B) == F(1, 2) and G.margin(A, B) == F(1, 2), "T2 margin")
    check(G.gap2(A, B) == F(1, 4), "T2 gap")
    c, a, agree = bclass(A, B)
    check(c == "apart" and agree, "T2 B")
    # T3 overlap by 1/4: x in [3/4, 7/4]
    B = box(F(3, 4), 0)
    check(amargin(A, B) == F(-1, 4) and G.margin(A, B) == F(-1, 4), "T3 margin")
    c, a, agree = bclass(A, B)
    check(c == "overlap" and a == F(1, 4) and agree, "T3 B area 1/4")
    # T4 diagonal neighbours: margin 1/2, gap^2 = 1/2
    B = box(F(3, 2), F(3, 2))
    check(amargin(A, B) == F(1, 2), "T4 margin")
    check(G.gap2(A, B) == F(1, 2), "T4 gap")
    # T5 corner contact at (1, 1)
    B = box(1, 1)
    check(amargin(A, B) == 0, "T5 margin")
    c, a, agree = bclass(A, B)
    check(c == "touch" and a == 0 and agree, "T5 B")
    # T6 3-4-5 square R: e = (3/5, 4/5), f = (-4/5, 3/5), p0 = (2, 0):
    # corners (2,0), (13/5,4/5), (9/5,7/5), (6/5,3/5); min x 6/5 so the x-gap to A is 1/5;
    # on e: R [6/5, 11/5], A [0, 7/5] -> -1/5; on f: R [-8/5, -3/5], A [-4/5, 3/5] -> -1/5.
    e = (F(3, 5), F(4, 5))
    f = (-e[1], e[0])
    R = [(F(2), F(0)), (F(13, 5), F(4, 5)), (F(9, 5), F(7, 5)), (F(6, 5), F(3, 5))]
    check(R == [(F(2), F(0)), G.add((F(2), F(0)), e), G.add(G.add((F(2), F(0)), e), f), G.add((F(2), F(0)), f)], "T6 corners")
    check(amargin(A, R) == F(1, 5) and G.margin(A, R) == F(1, 5), "T6 margin 1/5")
    check(G.gap2(A, R) == F(1, 25), "T6 gap 1/5")
    sa = r1012_sat.Square(R)
    check(sa.unit and sa.sense == 1, "T6 unit ccw")
    cl = r1012_sat.wall_clearances(sa, F(4))
    check([F(*v) for v in cl] == [F(6, 5), F(0), F(7, 5), F(13, 5)], "T6 clearances")
    check(G.clearances(R, F(4)) == (F(6, 5), F(0), F(7, 5), F(13, 5)), "T6 geom clearances")
    pts = r1012_clip.to_mpq(R)
    check(r1012_clip.wall_classes(pts, r1012_clip.mpq(4)) == ("clear", "touch", "clear", "clear"), "T6 B walls")
    check(r1012_clip.area_inside_box(pts, r1012_clip.mpq(4)) == 1, "T6 inside")
    # T7 R moved left by 1/5: vertex (1, 3/5) on A's edge
    R7 = G.translate(R, (F(-1, 5), F(0)))
    check(amargin(A, R7) == 0 and G.margin(A, R7) == 0, "T7 margin 0")
    c, a, agree = bclass(A, R7)
    check(c == "touch" and agree, "T7 B touch")
    # T8 R moved left by 2/5: margin -1/5; the corner (4/5, 3/5) pokes in a right triangle
    # with legs 1/4 (along -f to x = 1) and 1/3 (along e to x = 1): area 1/24
    R8 = G.translate(R, (F(-2, 5), F(0)))
    check(amargin(A, R8) == F(-1, 5) and G.margin(A, R8) == F(-1, 5), "T8 margin")
    c, a, agree = bclass(A, R8)
    check(c == "overlap" and a == F(1, 24) and agree, "T8 B area 1/24")
    # T9 R and R moved along e by 11/10: margin 1/10, gap 1/10
    R9 = G.translate(R, (e[0] * F(11, 10), e[1] * F(11, 10)))
    check(amargin(R, R9) == F(1, 10) and G.gap2(R, R9) == F(1, 100), "T9")
    # walls: W2 [-1/10, 9/10] x [0, 1] in box 2: left -1/10, area inside 9/10
    W2 = box(F(-1, 10), 0)
    s2 = r1012_sat.Square(W2)
    check(F(*r1012_sat.wall_clearances(s2, F(2))[0]) == F(-1, 10), "W2 A left")
    check(r1012_clip.wall_classes(r1012_clip.to_mpq(W2), r1012_clip.mpq(2))[0] == "cross", "W2 B left")
    check(r1012_clip.area_inside_box(r1012_clip.to_mpq(W2), r1012_clip.mpq(2)) == F(9, 10), "W2 area")
    # W4: R moved down by 1/10: the corner p0 below y = 0 cuts a triangle with legs 1/8
    # (along e, rising 4/5) and 1/6 (along f, rising 3/5): area 1/96, inside 95/96
    R4 = G.translate(R, (F(0), F(-1, 10)))
    check(F(*r1012_sat.wall_clearances(r1012_sat.Square(R4), F(4))[1]) == F(-1, 10), "W4 A")
    check(r1012_clip.area_inside_box(r1012_clip.to_mpq(R4), r1012_clip.mpq(4)) == F(95, 96), "W4 area")
    check(r1012_clip.wall_classes(r1012_clip.to_mpq(R4), r1012_clip.mpq(4))[1] == "cross", "W4 B")
    # W1: the unit box in the unit square: four contacts
    s1 = r1012_sat.Square(A)
    check([F(*v) for v in r1012_sat.wall_clearances(s1, F(1))] == [0, 0, 0, 0], "W1 A")
    check(r1012_clip.wall_classes(r1012_clip.to_mpq(A), r1012_clip.mpq(1)) == ("touch",) * 4, "W1 B")
    # non-unit squares
    bad = {
        "N1 scaled": [(F(0), F(0)), (F(11, 10), F(0)), (F(11, 10), F(11, 10)), (F(0), F(11, 10))],
        "N2 rhombus": [(F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "N3 bow-tie": [(F(0), F(0)), (F(1), F(1)), (F(1), F(0)), (F(0), F(1))],
        "N5 degenerate": [(F(0), F(0)), (F(1), F(0)), (F(0), F(0)), (F(1), F(0))],
        "N6 off by 1e-30": [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (F(0), F(1) + F(1, 10 ** 30))],
        "N7 parallelogram": [(F(0), F(0)), (F(1), F(0)), (F(2), F(1)), (F(1), F(1))],
    }
    for label, q in bad.items():
        check(not r1012_sat.Square(q).unit, label + " A")
        ok, _, _ = r1012_clip.unit_square(r1012_clip.to_mpq(q))
        check(not ok, label + " B")
    cw = [(F(0), F(0)), (F(0), F(1)), (F(1), F(1)), (F(1), F(0))]
    s = r1012_sat.Square(cw)
    ok, sense, _ = r1012_clip.unit_square(r1012_clip.to_mpq(cw))
    check(s.unit and s.sense == -1 and ok and sense == -1, "N4 clockwise accepted")


def rational_rotations():
    triples = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (0, 1, 1)]
    out = []
    for a, b, c in triples:
        for x, y in ((a, b), (b, a)):
            for sx in (1, -1):
                for sy in (1, -1):
                    out.append((F(sx * x, c), F(sy * y, c)))
    return out


def test_random(seed, count):
    rng = random.Random(seed)
    rots = rational_rotations()
    quads = []
    for _ in range(count):
        den = rng.choice([1, 2, 7, 10, 97, 1000003, 10 ** 20 + 39])
        c = (F(rng.randrange(0, 12 * den), den), F(rng.randrange(0, 12 * den), den))
        q = sq_from(c, rng.choice(rots))
        k = rng.randrange(4)
        q = q[k:] + q[:k]
        if rng.random() < 0.5:
            q = list(reversed(q))
        quads.append(q)
    side = F(12)
    a = r1012_sat.decide(side, quads)
    b = r1012_clip.decide(side, quads)
    for k, q in enumerate(quads):
        check(a["unit"][k] and b["unit"][k], f"random unit {k}")
        check(a["sense"][k] == b["sense"][k], f"random sense {k}")
        check([F(*v) for v in a["walls"][k]] == list(G.clearances(q, side)), f"random clearances {k}")
        check(a["wall_class"][k] == b["wall_class"][k], f"random wall classes {k}")
    for (i, j), m in a["pairs"].items():
        mf = F(*m)
        check(mf == G.margin(quads[i], quads[j]), f"random margin {i},{j}")
        check(a["pair_class"][(i, j)] == b["pair_class"][(i, j)], f"random class {i},{j}")
    check(not b["order_disagree"], "random clip orders")
    # closing moves: exact contact and 1e-30 past, for a sample of pairs
    eps = F(1, 10 ** 30)
    keys = list(a["pairs"])
    rng.shuffle(keys)
    for i, j in keys[: max(1, len(keys) // 4)]:
        for target, cls in ((F(0), "touch"), (-eps, "overlap")):
            moved, _ = G.close_pair(quads[i], quads[j], target)
            check(amargin(quads[i], moved) == target, f"close {i},{j} A {target}")
            check(G.margin(quads[i], moved) == target, f"close {i},{j} geom {target}")
            c, _, agree = bclass(quads[i], moved)
            check(c == cls and agree, f"close {i},{j} B {target}")
    for k, q in enumerate(quads[: max(1, count // 2)]):
        for wall in range(4):
            for target, cls in ((F(0), "touch"), (-eps, "cross")):
                moved, _ = G.to_wall(q, side, wall, target)
                sa = r1012_sat.Square(moved)
                check(F(*r1012_sat.wall_clearances(sa, side)[wall]) == target, f"wall {k} {wall} A")
                check(r1012_clip.wall_classes(r1012_clip.to_mpq(moved), r1012_clip.mpq(12))[wall] == cls, f"wall {k} {wall} B")


def test_broken_packings():
    side = F(2)
    good = [box(0, 0), box(1, 0), box(0, 1), box(1, 1)]
    r = r1012_decide.decide(side, good)
    check(r["verdict"] == "ACCEPT", "2x2 grid accepted")
    check(sum(1 for c in r["a"]["pair_class"].values() if c == "touch") == 6, "2x2 grid six contacts")
    overlap = [box(0, 0), box(F(9, 10), 0), box(0, 1), box(1, 1)]
    r = r1012_decide.decide(side, overlap)
    check(r["verdict"] == "REFUSE" and ("overlap", (0, 1)) in r["problems"], "overlap refused")
    crossing = [box(0, 0), box(1, 0), box(0, 1), box(F(11, 10), 1)]
    r = r1012_decide.decide(side, crossing)
    check(r["verdict"] == "REFUSE" and ("crosses wall", 3, "R") in r["problems"], "crossing refused")
    nonunit = [box(0, 0), box(1, 0), box(0, 1), [(F(1), F(1)), (F(2), F(1)), (F(2), F(2)), (F(1), F(2) - F(1, 10 ** 30))]]
    r = r1012_decide.decide(side, nonunit)
    check(r["verdict"] == "REFUSE" and ("not a unit square", 3) in r["problems"], "non-unit refused")


def main(argv):
    out = argv[1]
    t0 = time.process_time()
    test_scalars()
    test_reader()
    test_hand_geometry()
    test_random(1012, 40)
    test_random(109, 24)
    test_broken_packings()
    status = "PASSED" if not FAILS else "FAILED"
    receipt = {
        "program": "r1012_selftest.py",
        "status": status,
        "checks": CHECKS[0],
        "failures": FAILS[:50],
        "failure_count": len(FAILS),
        "cpu_seconds": round(time.process_time() - t0, 2),
        "python": sys.version.split()[0],
    }
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=1)
        handle.write("\n")
    print(f"{status} {CHECKS[0] - len(FAILS)} of {CHECKS[0]}")
    return 0 if not FAILS else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
