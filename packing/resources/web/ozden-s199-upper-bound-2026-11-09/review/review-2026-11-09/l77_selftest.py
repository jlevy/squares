"""Self-test of the L77 clean-room checker: both methods and the reader, on stated cases.

Run: python -I -B l77_selftest.py OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l77_checker as C  # noqa: E402

EPS = F(1, 10**30)
results: list[dict] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    results.append({"case": name, "ok": bool(ok), **({"detail": detail} if detail and not ok else {})})


def q(x: F) -> tuple[int, int]:
    return (x.numerator, x.denominator)


def square(p0: tuple[F, F], u: tuple[F, F], ccw: bool = True, start: int = 0) -> list:
    """Corners of the unit square at p0 with first edge u, listed from corner ``start``."""
    ux, uy = u
    fx, fy = (-uy, ux) if ccw else (uy, -ux)
    x0, y0 = p0
    pts = [(x0, y0), (x0 + ux, y0 + uy), (x0 + ux + fx, y0 + uy + fy), (x0 + fx, y0 + fy)]
    pts = pts[start:] + pts[:start]
    return [(q(x), q(y)) for x, y in pts]


def shift(cs: list, dx: F, dy: F) -> list:
    return [(q(F(*x) + dx), q(F(*y) + dy)) for x, y in cs]


def pair_both(a: list, b: list) -> tuple[F, str, str, F]:
    sa, sb = C.SquareA(a), C.SquareA(b)
    m, _ = C.margin_a(sa, sb)
    cls_b, area = C.pair_b(C.SquareB(a), C.SquareB(b))
    return m, C._class_a(m), cls_b, F(int(area.numerator), int(area.denominator))


def expect_pair(name: str, a: list, b: list, cls: str, margin: F | None = None, area: F | None = None) -> None:
    try:
        m, ca, cb, ar = pair_both(a, b)
        ok = ca == cls and cb == cls
        if margin is not None:
            ok = ok and m == margin
        if area is not None:
            ok = ok and ar == area
        # symmetric order
        m2, ca2, cb2, ar2 = pair_both(b, a)
        ok = ok and ca2 == cls and cb2 == cls and ar2 == ar and m2 == m
        record(name, ok, f"A {ca} margin {m}; B {cb} area {ar}")
    except C.Refused as e:
        record(name, False, f"refused: {e}")


U0 = (F(1), F(0))
U34 = (F(3, 5), F(4, 5))
U43 = (F(4, 5), F(3, 5))

# 1. axis-aligned edge and corner contacts, both listing senses, every starting corner
for ccw in (True, False):
    for start in range(4):
        tag = f"{'ccw' if ccw else 'cw'}{start}"
        base = (F(0), F(0)) if ccw else (F(0), F(1))
        a = square(base, U0, ccw, start)
        for s2 in (0, 3):
            b = shift(a, F(1), F(0))
            b = b[s2:] + b[:s2]
            expect_pair(f"edge-contact-{tag}-{s2}", a, b, "contact", F(0), F(0))
        expect_pair(f"edge-apart-{tag}", a, shift(a, 1 + EPS, F(0)), "clear", EPS, F(0))
        expect_pair(f"edge-overlap-{tag}", a, shift(a, 1 - EPS, F(0)), "overlap", -EPS, EPS)
        expect_pair(f"corner-contact-{tag}", a, shift(a, F(1), F(1)), "contact", F(0), F(0))
        expect_pair(f"corner-overlap-{tag}", a, shift(a, 1 - EPS, 1 - EPS), "overlap", -EPS, EPS * EPS)
        expect_pair(f"corner-apart-{tag}", a, shift(a, 1 + EPS, 1 - EPS), "clear", EPS, F(0))

# 2. a 3-4-5 vertex on an edge, both senses
for ccw in (True, False):
    a = square((F(0), F(0)), U0, True, 0)
    if ccw:
        b = square((F(1, 2), F(1)), U34, True, 0)
    else:
        # the same square listed clockwise: start at p0, first edge f = perp(u), then u
        b = square((F(1, 2), F(1)), (F(-4, 5), F(3, 5)), False, 0)
    tag = "ccw" if ccw else "cw"
    expect_pair(f"vertex-edge-contact-{tag}", a, b, "contact", F(0), F(0))
    expect_pair(f"vertex-edge-overlap-{tag}", a, shift(b, F(0), -EPS), "overlap", -EPS, F(25, 24) * EPS * EPS)
    expect_pair(f"vertex-edge-apart-{tag}", a, shift(b, F(0), EPS), "clear", EPS, F(0))

# 3. a duplicate, and a square against its own rotation about its centre
a = square((F(0), F(0)), U0)
expect_pair("duplicate", a, list(a), "overlap", F(-1), F(1))
for name, u in (("rot-3-4", U34), ("rot-4-3", U43)):
    cx = cy = F(1, 2)
    ux, uy = u
    p0 = (cx - (ux - uy) / 2, cy - (uy + ux) / 2)
    b = square(p0, u)
    expect_pair(name, a, b, "overlap", F(-6, 5), F(5, 6))


# 4. walls
def expect_walls(name: str, cs: list, side: F, outside: bool, contacts: set[str]) -> None:
    try:
        r = C.decide(q(side), [cs])
        got_out = bool(r["outside"]["A"]) and bool(r["outside"]["B"])
        same = r["outside"]["A"] == r["outside"]["B"]
        ca = {w for _, w in r["wall_contacts"]["A"]}
        cb = {w for _, w in r["wall_contacts"]["B"]}
        ok = same and got_out == outside and ca == contacts and cb == contacts and not r["wall_class_disagreements"]
        record(name, ok, json.dumps({"outside": r["outside"], "contacts": r["wall_contacts"]}))
    except C.Refused as e:
        record(name, False, f"refused: {e}")


S2 = F(5, 2)
a = square((F(0), F(0)), U0)
expect_walls("wall-ll-contact", a, S2, False, {"left", "bottom"})
expect_walls("wall-left-past", shift(a, -EPS, F(0)), S2, True, {"bottom"})
expect_walls("wall-bottom-past", shift(a, F(0), -EPS), S2, True, {"left"})
expect_walls("wall-left-short", shift(a, EPS, EPS), S2, False, set())
b = square((S2 - 1, S2 - 1), U0)
expect_walls("wall-ur-contact", b, S2, False, {"right", "top"})
expect_walls("wall-right-past", shift(b, EPS, F(0)), S2, True, {"top"})
expect_walls("wall-top-past", shift(b, F(0), EPS), S2, True, {"right"})
r345 = square((F(4, 5), F(0)), U34)  # lowest corner on the bottom wall, leftmost at x = 0
expect_walls("wall-tilted-two-contacts", r345, S2, False, {"left", "bottom"})
expect_walls("wall-tilted-left-past", shift(r345, -EPS, F(1, 10)), S2, True, set())


# 5. shapes both methods must refuse
def expect_refused_shape(name: str, cs: list) -> None:
    ra = rb = False
    try:
        C.SquareA(cs)
    except C.Refused:
        ra = True
    try:
        C.SquareB(cs)
    except C.Refused:
        rb = True
    record(name, ra and rb, f"A refused {ra}, B refused {rb}")


def pts(*xy: tuple[F, F]) -> list:
    return [(q(F(x)), q(F(y))) for x, y in xy]


one = F(1)
expect_refused_shape("shape-scaled", pts((0, 0), (1 + EPS, 0), (1 + EPS, 1 + EPS), (0, 1 + EPS)))
expect_refused_shape("shape-rhombus", pts((0, 0), (1, 0), (one + F(3, 5), F(4, 5)), (F(3, 5), F(4, 5))))
expect_refused_shape("shape-bowtie", pts((0, 0), (1, 1), (1, 0), (0, 1)))
expect_refused_shape("shape-rectangle", pts((0, 0), (1, 0), (1, 1 + EPS), (0, 1 + EPS)))
expect_refused_shape("shape-repeated-corner", pts((0, 0), (1, 0), (1, 1), (1, 1)))
expect_refused_shape("shape-third-corner-moved", pts((0, 0), (1, 0), (1 + EPS, 1), (0, 1)))
expect_refused_shape("shape-last-corner-moved", pts((0, 0), (1, 0), (1, 1), (0, 1 + EPS)))

# 6. random rational pairs taken exactly to contact along a line, and EPS either side
rng = random.Random(77938)


def rand_unit() -> tuple[F, F]:
    t = F(rng.randint(-60, 60), rng.randint(1, 60))
    d = 1 + t * t
    return ((1 - t * t) / d, 2 * t / d)


def rand_sq(p0: tuple[F, F]) -> list:
    return square(p0, rand_unit(), rng.random() < 0.5, rng.randrange(4))


def centre(cs: list) -> tuple[F, F]:
    xs = [F(*x) for x, _ in cs]
    ys = [F(*y) for _, y in cs]
    return (sum(xs) / 4, sum(ys) / 4)


random_fail = 0
for k in range(3000):
    a = rand_sq((F(rng.randint(0, 999), 97), F(rng.randint(0, 999), 89)))
    b0 = rand_sq((F(0), F(0)))
    ca, cb = centre(a), centre(b0)
    b = shift(b0, ca[0] - cb[0], ca[1] - cb[1])  # concentric: overlapping
    d = (F(rng.randint(-50, 50), rng.randint(1, 50)), F(rng.randint(-50, 50), rng.randint(1, 50)))
    if d == (0, 0):
        d = (F(1), F(0))
    sa, sb = C.SquareA(a), C.SquareA(b)
    lams = []
    for ax, ay in sa.axes + sb.axes:
        pa = [ax * x + ay * y for x, y in sa.pts]
        pb = [ax * x + ay * y for x, y in sb.pts]
        da = ax * d[0] + ay * d[1]
        # gap1 = min(pb) - max(pa) + lam*da ; gap2 = min(pa) - max(pb) - lam*da
        for a0, b1 in ((min(pb) - max(pa), da), (min(pa) - max(pb), -da)):
            assert a0 < 0
            if b1 > 0:
                lams.append(-a0 / b1)
    lam = min(lams)
    ok = True
    for dl, cls in ((F(0), "contact"), (EPS, "clear"), (-EPS, "overlap")):
        bb = shift(b, (lam + dl) * d[0], (lam + dl) * d[1])
        m, ca_, cb_, ar = pair_both(a, bb)
        good = ca_ == cls and cb_ == cls
        if cls == "contact":
            good = good and m == 0 and ar == 0
        ok = ok and good
    if not ok:
        random_fail += 1
record("random-pairs-3000-contact-and-either-side", random_fail == 0, f"{random_fail} failed")

# 7. random squares taken exactly to a wall, past it and short of it
SW = F(3)
wall_fail = 0
for k in range(1000):
    cs = rand_sq((F(1), F(1)))
    c0 = centre(cs)
    cs = shift(cs, SW / 2 - c0[0], SW / 2 - c0[1])  # centred: clear of every wall
    xs = [F(*x) for x, _ in cs]
    ys = [F(*y) for _, y in cs]
    wall = rng.choice(["left", "right", "bottom", "top"])
    if wall == "left":
        base = shift(cs, -min(xs), F(0))
        vec = (F(-1), F(0))
    elif wall == "right":
        base = shift(cs, SW - max(xs), F(0))
        vec = (F(1), F(0))
    elif wall == "bottom":
        base = shift(cs, F(0), -min(ys))
        vec = (F(0), F(-1))
    else:
        base = shift(cs, F(0), SW - max(ys))
        vec = (F(0), F(1))
    ok = True
    for dl, outside, touch in ((F(0), False, True), (EPS, True, False), (-EPS, False, False)):
        cc = shift(base, dl * vec[0], dl * vec[1])
        r = C.decide(q(SW), [cc])
        wa = {w for _, w in r["wall_contacts"]["A"]}
        wb = {w for _, w in r["wall_contacts"]["B"]}
        good = (bool(r["outside"]["A"]) == outside == bool(r["outside"]["B"])) and (
            (wall in wa) == touch == (wall in wb)
        ) and not r["wall_class_disagreements"]
        ok = ok and good
    if not ok:
        wall_fail += 1
record("random-walls-1000-contact-past-short", wall_fail == 0, f"{wall_fail} failed")

# 8. the reader
BASE = """softschema:
  contract: packing.squares:Witness/v2
  schema: witness.schema.yaml
  envelope: witness
  status: enforced
witness:
  id: W-test-n2
  n: 2
  side: '2'
  square_size: '1'
  representation: corners
  scalar:
    kind: rational
  coordinates:
    origin: lower-left
    axes: x-right-y-up
    angle_unit: not-applicable
  squares:
  - id: 1
    corners:
    - ['0', '0']
    - ['1', '0']
    - ['1', '1']
    - ['0', '1']
  - id: 2
    corners:
    - ['1', '0']
    - [3/2, '0']
    - [3/2, 1/2]
    - ['1', 1/2]
  claim:
    coordinate_provenance: verified
    method: exact-algebraic
    limitations: test
"""


def expect_reader(name: str, text: str, accept: bool) -> None:
    try:
        C.read_witness_text(text)
        got = True
        why = "accepted"
    except C.Refused as e:
        got = False
        why = str(e)
    record(name, got == accept, why)


expect_reader("reader-base-accepted", BASE, True)
flow = (
    '{"softschema": {"contract": "packing.squares:Witness/v2", "envelope": "witness"}, '
    '"witness": {"id": "W-test-n2", "n": 2, "side": "2", "square_size": "1", '
    '"representation": "corners", "scalar": {"kind": "rational"}, '
    '"coordinates": {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"}, '
    '"squares": [{"id": 1, "corners": [["0","0"],["1","0"],["1","1"],["0","1"]]}, '
    '{"id": 2, "corners": [["1","0"],["3/2","0"],["3/2","1/2"],["1","1/2"]]}], '
    '"claim": {"coordinate_provenance": "verified", "method": "exact-algebraic", "limitations": "test"}}}'
)
expect_reader("reader-flow-accepted", flow, True)
try:
    r1 = C.read_witness_text(BASE)
    r2 = C.read_witness_text(flow)
    record("reader-flow-same-witness", r1["corners"] == r2["corners"] and r1["side"] == r2["side"])
except C.Refused as e:
    record("reader-flow-same-witness", False, str(e))

MUT = [
    ("contract", "contract: packing.squares:Witness/v2", "contract: packing.squares:Witness/v1"),
    ("envelope", "envelope: witness", "envelope: other"),
    ("representation", "representation: corners", "representation: center-angle"),
    ("scalar-kind", "kind: rational", "kind: decimal"),
    ("square-size", "square_size: '1'", "square_size: '2'"),
    ("origin", "origin: lower-left", "origin: container-center"),
    ("axes", "axes: x-right-y-up", "axes: x-right-y-down"),
    ("angle-unit", "angle_unit: not-applicable", "angle_unit: turns"),
    ("n-mismatch", "n: 2", "n: 3"),
    ("n-negative", "n: 2", "n: -2"),
    ("n-quoted-float", "n: 2", "n: 2.0"),
    ("duplicate-id", "  - id: 2", "  - id: 1"),
    ("id-zero", "  - id: 2", "  - id: 0"),
    ("id-float", "  - id: 2", "  - id: 2.0"),
    ("three-corners", "    - ['0', '1']\n", ""),
    ("corner-three-coords", "    - ['1', '1']\n", "    - ['1', '1', '0']\n"),
    ("non-lowest", "[3/2, '0']", "[6/4, '0']"),
    ("denominator-one", "[3/2, '0']", "[3/1, '0']"),
    ("minus-zero", "['0', '0']", "['-0', '0']"),
    ("leading-zero", "['1', '0']\n    - ['1', '1']", "['01', '0']\n    - ['1', '1']"),
    ("zero-denominator", "[3/2, '0']", "[3/0, '0']"),
    ("negative-denominator", "[3/2, '0']", "[3/-2, '0']"),
    ("zero-over-q", "['1', 1/2]", "['1', 0/2]"),
    ("plain-float", "[3/2, 1/2]", "[3/2, 0.5]"),
    ("quoted-decimal", "[3/2, 1/2]", "[3/2, '0.5']"),
    ("plus-sign", "['1', '1']", "['+1', '1']"),
    ("exponent", "['1', '1']", "['1e0', '1']"),
    ("extra-witness-key", "  square_size: '1'", "  square_size: '1'\n  extra: x"),
    ("extra-square-key", "  - id: 2\n    corners:", "  - id: 2\n    angle: '0'\n    corners:"),
    ("missing-claim", "  claim:\n    coordinate_provenance: verified\n    method: exact-algebraic\n    limitations: test\n", ""),
    ("duplicate-key", "  side: '2'", "  side: '2'\n  side: '3'"),
    ("side-zero", "side: '2'", "side: '0'"),
    ("side-negative", "side: '2'", "side: '-2'"),
    ("side-text", "side: '2'", "side: two"),
    ("side-bool", "side: '2'", "side: true"),
    ("side-null", "side: '2'", "side: ~"),
    ("squares-mapping", "  squares:\n  - id: 1", "  squares:\n    first:\n  - id: 1"),
    ("top-extra", "witness:\n  id:", "extra: 1\nwitness:\n  id:"),
    ("scalar-extra", "    kind: rational", "    kind: rational\n    minimal_polynomial: [x]"),
    ("coordinates-extra", "    angle_unit: not-applicable", "    angle_unit: not-applicable\n    unit: m"),
]
for name, old, new in MUT:
    assert BASE.count(old) >= 1, name
    expect_reader(f"reader-refuses-{name}", BASE.replace(old, new, 1), False)
expect_reader("reader-refuses-empty", "", False)
expect_reader("reader-refuses-not-yaml", "softschema: [unclosed", False)

# JSON twin reader on temporary files written beside the receipt
tmpdir = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), "selftest-tmp")
os.makedirs(tmpdir, exist_ok=True)


def expect_json(name: str, text: bytes, accept: bool) -> None:
    p = os.path.join(tmpdir, name + ".json")
    with open(p, "wb") as fh:
        fh.write(text)
    try:
        C.read_witness_json(p)
        got, why = True, "accepted"
    except C.Refused as e:
        got, why = False, str(e)
    os.remove(p)
    record(name, got == accept, why)


expect_json("json-accepted", flow.encode(), True)
expect_json("json-refuses-float", flow.replace('"n": 2', '"n": 2.0').encode(), False)
expect_json("json-refuses-bool", flow.replace('"n": 2', '"n": true').encode(), False)
expect_json("json-refuses-duplicate-key", flow.replace('"n": 2', '"n": 2, "n": 2').encode(), False)
expect_json("json-refuses-not-utf8", flow.encode().replace(b"W-test", b"W-\xfftest"), False)
p = os.path.join(tmpdir, "bad.yaml")
with open(p, "wb") as fh:
    fh.write(BASE.encode().replace(b"W-test", b"W-\xfftest"))
try:
    C.read_witness(p)
    record("reader-refuses-not-utf8", False, "accepted")
except C.Refused:
    record("reader-refuses-not-utf8", True)
os.remove(p)
os.rmdir(tmpdir)

# 9. decide() end to end on small packings
grid = [square((F(i), F(j)), U0) for i in range(2) for j in range(2)]
r = C.decide((2, 1), grid)
record("decide-2x2-grid-accept", r["verdict"] == "ACCEPT" and len(r["touching_pairs"]["A"]) == 6
       and r["touching_pairs"]["A"] == r["touching_pairs"]["B"] and r["sum_clipped_areas"] == "0",
       json.dumps(r["touching_pairs"]))
# ids: 1 = (0,0), 2 = (0,1), 3 = (1,0), 4 = (1,1)
r = C.decide(q(2 - EPS), grid)
record("decide-2x2-grid-side-short-refuse",
       r["verdict"] == "REFUSE" and r["outside"]["A"] == [2, 3, 4] == r["outside"]["B"]
       and not r["overlapping_pairs"]["A"],
       json.dumps(r["outside"]))
g2 = list(grid)
g2[3] = shift(g2[3], -EPS, F(0))
r = C.decide((2, 1), g2)
record("decide-2x2-grid-shifted-refuse",
       r["verdict"] == "REFUSE" and r["overlapping_pairs"]["A"] == [[2, 4, C.q_str(-EPS)]]
       and r["overlapping_pairs"]["B"] == [[2, 4, C.q_str(EPS)]] and not r["outside"]["A"],
       json.dumps(r["overlapping_pairs"]))
g3 = grid[:3]
r = C.decide((2, 1), g3)
record("decide-grid-one-removed-accept", r["verdict"] == "ACCEPT" and r["n"] == 3, r["verdict"])

passed = all(x["ok"] for x in results)
out = {
    "program": "l77_selftest.py",
    "program_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
    "checker_sha256": hashlib.sha256(open(os.path.join(HERE, "l77_checker.py"), "rb").read()).hexdigest(),
    "verdict": "PASSED" if passed else "FAILED",
    "cases": len(results),
    "failed": [x for x in results if not x["ok"]],
    "case_names": [x["case"] for x in results],
}
with open(sys.argv[1], "w") as fh:
    json.dump(out, fh, indent=1)
    fh.write("\n")
print(out["verdict"], out["cases"], "cases", len(out["failed"]), "failed")
sys.exit(0 if passed else 1)
