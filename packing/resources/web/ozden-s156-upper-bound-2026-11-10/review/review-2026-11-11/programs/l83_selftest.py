"""Self-test of both methods and the reader (review L83, clean room).

Usage: python -I -B l83_selftest.py OUT.json
"""

from __future__ import annotations

import json
import random
import sys
import time
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gmpy2 import mpq  # noqa: E402

import l83_check as C  # noqa: E402
import l83_clip as B  # noqa: E402
import l83_geom as G  # noqa: E402
import l83_reader as R  # noqa: E402
import l83_sat as A  # noqa: E402

E30 = F(1, 10**30)
AX = (F(1), F(0))
P34 = (F(3, 5), F(4, 5))
P43 = (F(4, 5), F(3, 5))
results: list[dict] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    results.append({"case": name, "ok": bool(ok), "detail": detail})


def pair(a, b):
    """(margin A, class A, class B, area B) for two point lists."""
    sa, sb = A.Square(a), A.Square(b)
    m = A.pair_margin(sa, sb)
    pa, pb = B.points(G.to_pq(a)), B.points(G.to_pq(b))
    cls, ar = B.pair_class(pa, B.halfplanes(pb, B.unit_square_sense(pb)))
    cls2, ar2 = B.pair_class(pb, B.halfplanes(pa, B.unit_square_sense(pa)))
    assert (cls, ar) == (cls2, ar2), "method B not symmetric"
    return m, A.classify(m), cls, F(int(ar.numerator), int(ar.denominator))


def expect_pair(name, a, b, cls, margin=None, area=None):
    m, ca, cb, ar = pair(a, b)
    ok = ca == cls and cb == cls and (margin is None or m == margin) and (area is None or ar == area)
    record(name, ok, f"margin {m} classA {ca} classB {cb} area {ar}")


def unit(c, u=AX, s=1, start=0):
    return G.make_square(F(c[0]), F(c[1]), u, s, start)


def deterministic():
    a = unit((F(1, 2), F(1, 2)))
    for s in (1, -1):
        for st in (0, 2):
            tag = f"sense{s}-start{st}"
            expect_pair(f"edge contact {tag}", a, unit((F(3, 2), F(1, 2)), AX, s, st), "contact", 0, 0)
            expect_pair(f"edge overlap 1e-30 {tag}", a, unit((F(3, 2) - E30, F(1, 2)), AX, s, st), "overlap", -E30, E30)
            expect_pair(f"edge apart 1e-30 {tag}", a, unit((F(3, 2) + E30, F(1, 2)), AX, s, st), "clear", E30)
            expect_pair(f"corner contact {tag}", a, unit((F(3, 2), F(3, 2)), AX, s, st), "contact", 0, 0)
            expect_pair(f"corner overlap {tag}", a, unit((F(3, 2) - E30, F(3, 2) - E30), AX, s, st), "overlap", -E30, E30 * E30)
            # 3-4-5 vertex on the top edge of a at (1/2, 1)
            u, v = P34, (-P34[1], P34[0])
            cx = F(1, 2) + u[0] / 2 + v[0] / 2
            cy = F(1) + u[1] / 2 + v[1] / 2
            b = G.make_square(cx, cy, u, s, st)
            expect_pair(f"3-4-5 vertex-edge contact {tag}", a, b, "contact", None, 0)
            expect_pair(f"3-4-5 vertex-edge overlap {tag}", a, G.translate(b, F(0), -E30), "overlap", None, F(25, 24) * E30 * E30)
            expect_pair(f"3-4-5 vertex-edge apart {tag}", a, G.translate(b, F(0), E30), "clear")
    expect_pair("duplicate", a, unit((F(1, 2), F(1, 2))), "overlap", -1, 1)
    expect_pair("own rotation 3/5,4/5", a, unit((F(1, 2), F(1, 2)), P34), "overlap", F(-6, 5), F(5, 6))
    expect_pair("own rotation 4/5,3/5", a, unit((F(1, 2), F(1, 2)), P43), "overlap", F(-6, 5), F(5, 6))
    # walls
    S = F(3)
    for name, sq, wall, cls in [
        ("left contact", unit((F(1, 2), F(3, 2))), "left", "contact"),
        ("left past", unit((F(1, 2) - E30, F(3, 2))), "left", "overlap"),
        ("right contact", unit((F(5, 2), F(3, 2))), "right", "contact"),
        ("right past", unit((F(5, 2) + E30, F(3, 2))), "right", "overlap"),
        ("bottom contact", unit((F(3, 2), F(1, 2))), "bottom", "contact"),
        ("bottom past", unit((F(3, 2), F(1, 2) - E30)), "bottom", "overlap"),
        ("top contact 3-4-5", G.make_square(F(3, 2), S - F(7, 10), P34), "top", "contact"),
        ("top past 3-4-5", G.make_square(F(3, 2), S - F(7, 10) + E30, P34), "top", "overlap"),
        ("top short 3-4-5", G.make_square(F(3, 2), S - F(7, 10) - E30, P34), "top", "clear"),
    ]:
        ca = A.classify(A.wall_clearances(sq, S)[wall])
        cb = B.wall_classes(B.points(G.to_pq(sq)), mpq(3))[wall]
        inside_b = B.box_area(B.points(G.to_pq(sq)), mpq(3)) == 1
        record(f"wall {name}", ca == cls and cb == cls and inside_b == (cls != "overlap"), f"{ca} {cb} {inside_b}")
    # shapes both methods must refuse
    bad = {
        "rectangle 1x2": [(F(0), F(0)), (F(1), F(0)), (F(1), F(2)), (F(0), F(2))],
        "rhombus side 1": [(F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "square side 2": [(F(0), F(0)), (F(2), F(0)), (F(2), F(2)), (F(0), F(2))],
        "bow-tie order": [(F(0), F(0)), (F(1), F(1)), (F(1), F(0)), (F(0), F(1))],
        "corner moved 1e-30": [(F(0), F(0)), (F(1), F(0)), (F(1) + E30, F(1)), (F(0), F(1))],
        "collapsed": [(F(0), F(0))] * 4,
        "zigzag of unit edges": [(F(0), F(0)), (F(1), F(0)), (F(0), F(0)), (F(1), F(0))],
    }
    for name, pts in bad.items():
        try:
            A.Square(pts)
            ra = False
        except ValueError:
            ra = True
        try:
            B.unit_square_sense(B.points(G.to_pq(pts)))
            rb = False
        except ValueError:
            rb = True
        record(f"refuse shape {name}", ra and rb, f"A refused {ra}, B refused {rb}")


def randomised(rng: random.Random, pairs: int, walls: int):
    fails = 0
    tested = 0
    for k in range(pairs):
        u = G.pyth(rng.randint(2, 40), rng.randint(1, 39)) if rng.random() < 0.85 else AX
        v = G.pyth(rng.randint(2, 40), rng.randint(1, 39)) if rng.random() < 0.85 else AX
        if u[0] <= 0 or v[0] <= 0:
            u, v = AX, P34
        a = G.make_square(F(rng.randint(0, 10**6), 10**6), F(rng.randint(0, 10**6), 10**6), u, rng.choice((1, -1)), rng.randint(0, 3))
        ang = F(rng.randint(-10**6, 10**6), 10**6)
        b = G.make_square(F(3) + ang, F(2) - ang, v, rng.choice((1, -1)), rng.randint(0, 3))
        if A.pair_margin(A.Square(a), A.Square(b)) <= 0:
            continue
        tested += 1
        for extra, cls in ((F(0), "contact"), (E30, "overlap"), (-E30, "clear")):
            m, ca, cb, _ = pair(a, G.close_pair(a, b, extra))
            if not (ca == cls and cb == cls and (cls != "contact" or m == 0)):
                fails += 1
    record(f"random centre-line closings ({pairs} drawn, three positions each)", fails == 0 and tested > pairs // 2, f"closed {tested}, failures {fails}")
    fails = 0
    S = F(7)
    for k in range(walls):
        u = G.pyth(rng.randint(2, 40), rng.randint(1, 39))
        sq = G.make_square(F(rng.randint(2 * 10**6, 5 * 10**6), 10**6), F(rng.randint(2 * 10**6, 5 * 10**6), 10**6), u, rng.choice((1, -1)))
        cl = A.wall_clearances(sq, S)
        wall = rng.choice(C.WALLS)
        dx, dy = {"left": (-1, 0), "right": (1, 0), "bottom": (0, -1), "top": (0, 1)}[wall]
        for extra, cls in ((F(0), "contact"), (E30, "overlap"), (-E30, "clear")):
            d = cl[wall] + extra
            moved = G.translate(sq, d * dx, d * dy)
            ca = A.classify(A.wall_clearances(moved, S)[wall])
            cb = B.wall_classes(B.points(G.to_pq(moved)), mpq(7))[wall]
            if ca != cls or cb != cls:
                fails += 1
    record(f"random wall closings ({walls} squares, three positions each)", fails == 0, f"failures {fails}")


GOOD = """softschema:
  contract: packing.squares:Witness/v2
  schema: witness.schema.yaml
  envelope: witness
  status: enforced
witness:
  id: W-test
  n: 2
  side: 2
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
    - [1, 1/2]
    - [2, 1/2]
    - [2, 3/2]
    - [1, 3/2]
"""


def reader_cases():
    ok_flow = GOOD.replace("  - id: 2\n", "  - {id: 2, corners: [[1, 1/2], [2, 1/2], [2, 3/2], [1, 3/2]]}\n  - id: 99\n").split("  - id: 99\n")[0]
    for name, text in (("good", GOOD), ("good, flow style", ok_flow)):
        try:
            w = R.read_text(text)
            res = C.decide(w.n, w.side, w.ids, w.corners)
            record(f"reader accepts {name}", res["accept"] and res["touching"] == [(1, 2)], str(res["touching"]))
        except R.Refused as exc:
            record(f"reader accepts {name}", False, str(exc))
    bad = {
        "wrong contract": ("Witness/v2", "Witness/v1"),
        "wrong envelope": ("envelope: witness", "envelope: other"),
        "center-basis": ("representation: corners", "representation: center-basis"),
        "decimal scalars": ("kind: rational", "kind: decimal"),
        "centre origin": ("origin: lower-left", "origin: container-center"),
        "angle unit": ("not-applicable", "radians"),
        "square size 2": ("square_size: '1'", "square_size: '2'"),
        "n mismatch": ("n: 2", "n: 3"),
        "repeated id": ("- id: 2", "- id: 1"),
        "id 0": ("- id: 2", "- id: 0"),
        "id 3": ("- id: 2", "- id: 3"),
        "string id": ("- id: 2", "- id: b"),
        "three corners": ("    - [1, 3/2]\n", ""),
        "corner triple": ("[2, 3/2]", "[2, 3/2, 0]"),
        "leading zero": ("[2, 1/2]", "[02, 1/2]"),
        "denominator 1": ("[2, 1/2]", "[2/1, 1/2]"),
        "not lowest terms": ("[2, 1/2]", "[2, 2/4]"),
        "negative zero": ("['0', '0']", "['-0', '0']"),
        "zero over q": ("['0', '0']", "['0/5', '0']"),
        "decimal point": ("[2, 1/2]", "[2, 0.5]"),
        "exponent": ("[2, 1/2]", "[2, 5e-1]"),
        "plus sign": ("[2, 1/2]", "['+2', 1/2]"),
        "space": ("[2, 1/2]", "[' 2', 1/2]"),
        "negative denominator": ("[2, 1/2]", "[2, 1/-2]"),
        "zero denominator": ("[2, 1/2]", "[2, 1/0]"),
        "duplicate key": ("  n: 2\n", "  n: 2\n  n: 2\n"),
        "extra square key": ("  - id: 2\n", "  - id: 2\n    angle: '0'\n"),
        "extra witness key": ("  n: 2\n", "  n: 2\n  extra: x\n"),
        "extra top key": ("softschema:\n", "other: 1\nsoftschema:\n"),
        "side zero": ("side: 2", "side: 0"),
        "side negative": ("side: 2", "side: -2"),
        "custom tag": ("side: 2", "side: !thing 2"),
        "null corner": ("[2, 1/2]", "[2, null]"),
        "boolean size": ("square_size: '1'", "square_size: yes"),
        "missing squares": ("  squares:\n", "  squarez:\n"),
        "not yaml": ("witness:\n", "witness: [\n"),
    }
    for name, (old, new) in bad.items():
        assert old in GOOD, name
        text = GOOD.replace(old, new, 1)
        try:
            R.read_text(text)
            record(f"reader refuses {name}", False, "accepted")
        except R.Refused as exc:
            record(f"reader refuses {name}", True, str(exc))
    # JSON twin normalisation
    try:
        R.normalise_json({"a": 1.5})
        record("JSON float refused", False)
    except R.Refused:
        record("JSON float refused", True)


def main(argv):
    t0 = time.process_time()
    deterministic()
    randomised(random.Random(20261111), 1500, 600)
    reader_cases()
    passed = all(r["ok"] for r in results)
    out = {
        "verdict": "PASSED" if passed else "FAILED",
        "cases": len(results),
        "failed": [r for r in results if not r["ok"]],
        "results": results,
        "cpu_seconds": round(time.process_time() - t0, 1),
        "programs": C.program_digests(),
    }
    Path(argv[1]).write_text(json.dumps(out, indent=1) + "\n")
    print(out["verdict"], out["cases"], "cases", "failed", len(out["failed"]), "cpu", out["cpu_seconds"])
    for r in out["failed"]:
        print("FAIL", r)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
