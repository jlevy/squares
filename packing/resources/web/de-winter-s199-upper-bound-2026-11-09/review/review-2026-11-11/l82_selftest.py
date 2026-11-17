"""Self-test of l82_check.py: contacts, gaps and overlaps down to 1e-320, by both methods.

Usage: python -I l82_selftest.py [MUTANT]   (exit 0 iff every case passes)
"""

from __future__ import annotations

import os
import random
import sys
import tempfile
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l82_check as C  # noqa: E402

if len(sys.argv) > 1:
    C.MUTANT = sys.argv[1]

FAILS: list[str] = []
COUNT = 0


def ok(cond: bool, label: str) -> None:
    global COUNT
    COUNT += 1
    if not cond:
        FAILS.append(label)


def mk(cx, cy, c=F(1), s=F(0)):
    return tuple((F(v).numerator, F(v).denominator) for v in (cx, cy, c, s))


def both(a, b):
    m = C.pair_margin_a(a, b)
    kb, area = C.pair_class_b(C._corners_b(a), C._corners_b(b))
    return m, C.classify_margin(m), kb, F(int(area.numerator), int(area.denominator))


def ratdir(t: F):
    return ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))


EPS = [F(1, 10**30), F(1, 10**320)]

# 1. edge contact, both orders and both listing senses (rotation by a quarter turn)
for c, s in ((F(1), F(0)), (F(0), F(1)), (F(-1), F(0)), (F(0), F(-1))):
    a = mk(F(1, 2), F(1, 2), c, s)
    b = mk(F(3, 2), F(1, 2), c, s)
    m, ka, kb, ar = both(a, b)
    ok(m == 0 and ka == kb == "contact" and ar == 0, f"edge contact {c},{s}")
    for e in EPS:
        m, ka, kb, ar = both(a, mk(F(3, 2) + e, F(1, 2), c, s))
        ok(m == e and ka == kb == "clear", f"edge gap {e}")
        m, ka, kb, ar = both(a, mk(F(3, 2) - e, F(1, 2), c, s))
        ok(m == -e and ka == kb == "overlap" and ar == e, f"edge overlap {e}")
        m, ka, kb, ar = both(mk(F(3, 2) - e, F(1, 2), c, s), a)
        ok(m == -e and ka == kb == "overlap" and ar == e, f"edge overlap swapped {e}")

# 2. corner-corner contact
a, b = mk(F(1, 2), F(1, 2)), mk(F(3, 2), F(3, 2))
m, ka, kb, ar = both(a, b)
ok(m == 0 and ka == kb == "contact" and ar == 0, "corner contact")
for e in EPS:
    m, ka, kb, ar = both(a, mk(F(3, 2) - e, F(3, 2) - e))
    ok(m == -e and ka == kb == "overlap" and ar == e * e, f"corner overlap {e}")
    m, ka, kb, ar = both(a, mk(F(3, 2) + e, F(3, 2)))
    ok(m == e and ka == kb == "clear", f"corner gap {e}")

# 3. 3-4-5 vertex on an edge: square b turned by (3/5, 4/5); lowest vertex on y = 1
u = (F(3, 5), F(4, 5))
h = (u[0] + u[1]) / 2  # half extent 7/10
a = mk(F(1, 2), F(1, 2))
for cx0 in (F(1, 2), F(3, 5)):
    for e in [F(0)] + EPS + [-x for x in EPS]:
        b = mk(cx0, 1 + h + e, *u)
        m, ka, kb, ar = both(a, b)
        want = "contact" if e == 0 else ("clear" if e > 0 else "overlap")
        ok(ka == kb == want, f"345 class {e}")
        if e < 0:
            ok(ar == F(25, 24) * e * e, f"345 area {e}")
            ok(m < 0, f"345 margin sign {e}")
        if e > 0:
            ok(m > 0, f"345 gap sign {e}")
        if e == 0:
            ok(m == 0, "345 contact margin")

# 4. duplicate, and a square against its own turn by (3/5, 4/5) and (4/5, 3/5)
a = mk(F(1, 2), F(1, 2))
m, ka, kb, ar = both(a, a)
ok(m == -1 and ka == kb == "overlap" and ar == 1, "duplicate")
for uu in ((F(3, 5), F(4, 5)), (F(4, 5), F(3, 5))):
    m, ka, kb, ar = both(a, mk(F(1, 2), F(1, 2), *uu))
    ok(m == F(-6, 5) and ka == kb == "overlap" and ar == F(5, 6), f"self-turn {uu} {m} {ar}")

# 5. walls
for S, ctr, uu, want in (
    (F(1), (F(1, 2), F(1, 2)), (F(1), F(0)), True),
    (F(1) - EPS[1], (F(1, 2), F(1, 2)), (F(1), F(0)), False),
    (F(1), (F(1, 2) + EPS[1], F(1, 2)), (F(1), F(0)), False),
    (F(7, 5), (F(7, 10), F(7, 10)), (F(3, 5), F(4, 5)), True),
    (F(7, 5) - EPS[1], (F(7, 10), F(7, 10)), (F(3, 5), F(4, 5)), False),
    (F(7, 5), (F(7, 10) - EPS[1], F(7, 10)), (F(4, 5), F(-3, 5)), False),
    (F(7, 5) + EPS[1], (F(7, 10), F(7, 10)), (F(-4, 5), F(3, 5)), True),
):
    sq = mk(*ctr, *uu)
    cl = C.wall_clearances_a(sq, S)
    ina = min(cl) >= 0
    inb = C.inside_b(C._corners_b(sq), C.gmpy2.mpq(S.numerator, S.denominator))
    ok(ina == inb == want, f"wall {S} {ctr} {uu}")
    if want and S in (F(1), F(7, 5)):
        ok(cl == (0, 0, 0, 0), "wall contacts all four")

# 6. non-unit shapes refused by both methods
for c, s in ((F(1) + EPS[0], F(0)), (F(3, 5), F(4, 5) + EPS[1]), (F(1, 2), F(1, 2)), (F(0), F(0)), (F(6, 5), F(8, 5))):
    sq = mk(0, 0, c, s)
    ok(not C.unit_a(sq) and not C.unit_b(sq), f"non-unit {c},{s}")
ok(C.unit_a(mk(0, 0, F(-5, 13), F(12, 13))) and C.unit_b(mk(0, 0, F(-5, 13), F(12, 13))), "5-12-13 unit")

# 7. random rational pairs taken exactly to contact along a line, then +-eps
rng = random.Random(20261111)
for trial in range(400):
    ti = F(rng.randint(-50, 50), rng.randint(1, 50))
    tj = F(rng.randint(-50, 50), rng.randint(1, 50))
    ui, uj = ratdir(ti), ratdir(tj)
    v = (F(rng.randint(-40, 40), rng.randint(1, 9)), F(rng.randint(-40, 40), rng.randint(1, 9)))
    if v == (0, 0):
        continue
    ci = (F(rng.randint(-9, 9), rng.randint(1, 7)), F(rng.randint(-9, 9), rng.randint(1, 7)))
    T = (1 + abs(ui[0] * uj[0] + ui[1] * uj[1]) + abs(-ui[0] * uj[1] + ui[1] * uj[0])) / 2
    ws = [ui, (-ui[1], ui[0]), uj, (-uj[1], uj[0])]
    mm = max(abs(w[0] * v[0] + w[1] * v[1]) for w in ws)
    kstar = T / mm
    a = mk(*ci, *ui)
    e = EPS[trial % 2]
    for de, want in ((F(0), "contact"), (e, "clear"), (-e, "overlap")):
        k = kstar + de / mm
        b = mk(ci[0] + k * v[0], ci[1] + k * v[1], *uj)
        m, ka, kb, ar = both(a, b)
        ok(m == de and ka == kb == want, f"random {trial} {want}")
        if want == "overlap":
            ok(ar > 0, f"random {trial} area")

# 8. reader refusals
BAD = [
    "1/2.0", "2/4", "-0", "01/3", "1/0", "1/-3", " 1/3", "1/3 ", "0x10", "1e3", "+1/3", "",
]
for s in BAD:
    try:
        C.parse_rat(s)
        ok(False, f"reader accepted {s!r}")
    except C.ReadError:
        ok(True, "")
for x in (0.5, True, None, [1]):
    try:
        C.parse_rat(x)
        ok(False, f"reader accepted {x!r}")
    except C.ReadError:
        ok(True, "")
ok(C.parse_rat("-3/7") == (-3, 7) and C.parse_rat(5) == (5, 1) and C.parse_rat("0") == (0, 1), "good literals")


def yaml_text(n, side, squares, rep="center-basis", extra=""):
    lines = ["witness:", f"  n: {n}", f"  side: {side}", "  square_size: '1'", f"  representation: {rep}",
             "  scalar:", "    kind: rational", "  squares:"]
    for k, sq in enumerate(squares, start=1):
        lines.append(f"  - id: {k}")
        if rep == "center-basis":
            lines.append(f"    center: [{sq[0]}, {sq[1]}]")
            lines.append(f"    basis: [{sq[2]}, {sq[3]}]")
        else:
            lines.append("    corners:")
            for p in sq:
                lines.append(f"    - [{p[0]}, {p[1]}]")
        if extra and k == 1:
            lines.append(extra)
    return "\n".join(lines) + "\n"


GRID = [("1/2", "1/2", 1, 0), ("3/2", "1/2", 1, 0), ("1/2", "3/2", 0, 1), ("3/2", "3/2", -1, 0)]
cases = {
    "good": (yaml_text(4, 2, GRID), True),
    "short": (yaml_text(5, 2, GRID), False),
    "extra key": (yaml_text(4, 2, GRID, extra="    angle: 0"), False),
    "float": (yaml_text(4, 2, [("0.5", "1/2", 1, 0)] + GRID[1:]), False),
    "not lowest": (yaml_text(4, 2, [("2/4", "1/2", 1, 0)] + GRID[1:]), False),
    "side float": (yaml_text(4, "2.0", GRID), False),
    "corners good": (yaml_text(4, 2, [[(0, 0), (1, 0), (1, 1), (0, 1)], [(1, 0), (2, 0), (2, 1), (1, 1)],
                                      [(0, 1), (0, 2), ("-1/1" if False else 1, 2), (1, 1)][::-1],
                                      [(2, 2), (1, 2), (1, 1), (2, 1)]], rep="corners"), True),
    "corners bad": (yaml_text(4, 2, [[(0, 0), (1, 0), (1, 1), ("1/1000", 1)]] + [[(1, 0), (2, 0), (2, 1), (1, 1)]] * 3,
                              rep="corners"), False),
}
with tempfile.TemporaryDirectory() as td:
    for name, (txt, want) in cases.items():
        p = os.path.join(td, "w.yaml")
        with open(p, "w") as fh:
            fh.write(txt)
        try:
            pk = C.read_witness_yaml(p)
            got = True
        except C.ReadError:
            got = False
        ok(got == want, f"yaml {name}")
        if name == "good":
            r = C.decide(pk)
            ok(r["verdict"] == "ACCEPT" and len(r["touching_pairs"]) == 6 and len(r["wall_contacts"]) == 8,
               f"grid decide {r['verdict']} {len(r['touching_pairs'])} {len(r['wall_contacts'])}")
            r = C.decide(pk, side=F(2) - EPS[1])
            ok(r["verdict"] == "REFUSE" and r["outside_a"] == r["outside_b"] == [2, 3, 4], "grid short side")
            pk2 = dict(pk, squares=[pk["squares"][0], C.mk if False else pk["squares"][1],
                                    tuple((F(v[0], v[1]).numerator, F(v[0], v[1]).denominator) for v in
                                          (mk(F(1, 2), F(3, 2) - EPS[1], 0, 1))), pk["squares"][3]])
            r = C.decide(pk2)
            ok(r["verdict"] == "REFUSE" and [x[:2] for x in r["overlapping_pairs"]] == [[1, 3]], "grid shifted")
        if name == "corners good":
            r = C.decide(pk)
            ok(r["verdict"] == "ACCEPT" and len(r["touching_pairs"]) == 6, "corners grid decide")

print(f"cases {COUNT}, failures {len(FAILS)}")
for f in FAILS[:20]:
    print("FAIL", f)
sys.exit(1 if FAILS else 0)
