"""Lane L109's self-test of both methods and the reader.

Usage: python -I -B l109_selftest.py OUT.json

Hand-derived cases (contacts, 1e-30 apart and past, overlaps with areas derived by
hand), shapes both methods must refuse, random rational pairs closed along their centre
line, random squares taken to a wall, and malformed files the reader must refuse. It then
runs the geometric cases again against two deliberately broken copies of the methods
(method A counting a zero margin as apart; method B clipping with open half-planes),
each of which must fail.

Imports nothing from the repository or the source.
"""

from __future__ import annotations

import json
import os
import random
import sys
from collections.abc import Callable
from fractions import Fraction as Q
from math import gcd
from typing import Any

from gmpy2 import mpq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_axes as A  # noqa: E402
import l109_check as C  # noqa: E402
import l109_clip as B  # noqa: E402
import l109_geom as G  # noqa: E402
import l109_reader as R  # noqa: E402

E = Q(1, 10**30)
PROGRAMS = ["l109_reader.py", "l109_axes.py", "l109_clip.py", "l109_check.py", "l109_geom.py", "l109_selftest.py"]


class Suite:
    def __init__(self) -> None:
        self.cases = 0
        self.failures: list[str] = []

    def ok(self, cond: bool, what: str) -> None:
        self.cases += 1
        if not cond:
            self.failures.append(what)


def qb(pts: list[tuple[Q, Q]]) -> list[tuple[mpq, mpq]]:
    return [(mpq(x.numerator, x.denominator), mpq(y.numerator, y.denominator)) for x, y in pts]


def both_squares(pts: list[tuple[Q, Q]]):
    return A.make(pts), B.make(qb(pts))


def pair_both(p: list[tuple[Q, Q]], q: list[tuple[Q, Q]]) -> tuple[Q, str, str, mpq]:
    a1, b1 = both_squares(p)
    a2, b2 = both_squares(q)
    return C.decide_pair(a1, a2, b1, b2)


def walls_both(p: list[tuple[Q, Q]], side: Q):
    a, b = both_squares(p)
    return C.decide_walls(a, b, side, mpq(side.numerator, side.denominator)), B.inside(b, mpq(side.numerator, side.denominator))


ROTS = [
    (Q(1), Q(0)),
    (Q(0), Q(1)),
    (Q(-1), Q(0)),
    (Q(0), Q(-1)),
    (Q(3, 5), Q(4, 5)),
    (Q(4, 5), Q(3, 5)),
    (Q(-3, 5), Q(4, 5)),
    (Q(5, 13), Q(12, 13)),
    (Q(8, 17), Q(-15, 17)),
    (Q(20, 29), Q(21, 29)),
]


def triples(limit: int) -> list[tuple[Q, Q]]:
    out = []
    for m in range(2, limit):
        for n in range(1, m):
            if gcd(m, n) == 1 and (m - n) % 2 == 1:
                h = m * m + n * n
                out.append((Q(m * m - n * n, h), Q(2 * m * n, h)))
    return out


def geometric(s: Suite, rng: random.Random, n_random_pairs: int, n_random_walls: int) -> None:
    # 1. unit squares accepted, all rotations, both senses, all starting corners
    for c, sn in ROTS:
        for ccw in (True, False):
            for st in range(4):
                pts = G.square(Q(7, 3), Q(-5, 11), c, sn, ccw, st)
                try:
                    a, _b = both_squares(pts)
                    s.ok(a.ccw == ccw, f"unit square sense {c},{sn},{ccw},{st}")
                except (A.NotUnit, B.NotUnit) as exc:
                    s.ok(False, f"unit square refused {c},{sn},{ccw},{st}: {exc}")
    # 2. shapes both methods must refuse
    z, o = Q(0), Q(1)
    sq0 = [(z, z), (o, z), (o, o), (z, o)]
    rot = G.square(Q(1), Q(1), Q(3, 5), Q(4, 5))
    bad = {
        "rhombus 3-4-5": [(z, z), (o, z), (o + Q(3, 5), Q(4, 5)), (Q(3, 5), Q(4, 5))],
        "bowtie order": [sq0[0], sq0[2], sq0[1], sq0[3]],
        "rectangle 1 x (1+1e-30)": [(z, z), (o, z), (o, o + E), (z, o + E)],
        "third corner off by 1e-30": [(z, z), (o, z), (o + E, o), (z, o)],
        "square of side 2": [(z, z), (Q(2), z), (Q(2), Q(2)), (z, Q(2))],
        "a point": [(z, z)] * 4,
        "tilted, last corner off": rot[:3] + [(rot[3][0] + E, rot[3][1])],
    }
    for name, pts in bad.items():
        ra = rb = False
        try:
            A.make(pts)
        except A.NotUnit:
            ra = True
        try:
            B.make(qb(pts))
        except B.NotUnit:
            rb = True
        s.ok(ra, f"method A refuses {name}")
        s.ok(rb, f"method B refuses {name}")
    # 3. pairs with hand-derived outcomes, both orders and both senses of listing
    t = G.translate
    T = G.square(Q(2, 5), Q(17, 10), Q(3, 5), Q(4, 5))  # lowest vertex at (1/2, 1)
    cases: list[tuple[str, list[tuple[Q, Q]], list[tuple[Q, Q]], Q, str, Q]] = [
        ("edge contact", sq0, t(sq0, o, z), z, "contact", z),
        ("edge apart 1e-30", sq0, t(sq0, o + E, z), E, "apart", z),
        ("edge past 1e-30", sq0, t(sq0, o - E, z), -E, "overlap", E),
        ("corner contact", sq0, t(sq0, o, o), z, "contact", z),
        ("corner past 1e-30", sq0, t(sq0, o - E, o - E), -E, "overlap", E * E),
        ("corner apart 1e-30", sq0, t(sq0, o + E, o), E, "apart", z),
        ("3-4-5 vertex on edge", sq0, T, z, "contact", z),
        ("3-4-5 vertex past 1e-30", sq0, t(T, z, -E), -E, "overlap", Q(25, 24) * E * E),
        ("3-4-5 vertex apart 1e-30", sq0, t(T, z, E), E, "apart", z),
        ("duplicate", sq0, list(sq0), -o, "overlap", o),
        (
            "concentric 3-4-5",
            G.square(Q(1, 2), Q(1, 2), o, z),
            G.square(Q(1, 2), Q(1, 2), Q(3, 5), Q(4, 5)),
            Q(-6, 5),
            "overlap",
            Q(5, 6),
        ),
        (
            "concentric 4-3-5",
            G.square(Q(1, 2), Q(1, 2), o, z),
            G.square(Q(1, 2), Q(1, 2), Q(4, 5), Q(3, 5)),
            Q(-6, 5),
            "overlap",
            Q(5, 6),
        ),
    ]
    for name, p, q, m_exp, cls, ar_exp in cases:
        variants = [(p, q), (q, p), (p[::-1], q), (p, q[::-1]), (p[1:] + p[:1], q[2:] + q[:2])]
        for k, (u, v) in enumerate(variants):
            m, ca, cb, ar = pair_both(u, v)
            s.ok(m == m_exp, f"{name} [{k}]: margin {m} != {m_exp}")
            s.ok(ca == cls and cb == cls, f"{name} [{k}]: classes {ca},{cb} != {cls}")
            s.ok(ar == mpq(ar_exp.numerator, ar_exp.denominator), f"{name} [{k}]: area {ar} != {ar_exp}")
    # 4. walls by hand, side 2
    side = Q(2)
    w, ins = walls_both(sq0, side)
    s.ok(w["left"][1:3] == ("contact", "contact") and w["bottom"][1:3] == ("contact", "contact"), "corner square walls")
    s.ok(w["right"][0] == 1 and w["right"][1:3] == ("clear", "clear") and ins, "corner square right and inside")
    w, ins = walls_both(t(sq0, -E, z), side)
    s.ok(w["left"][0] == -E and w["left"][1:3] == ("outside", "outside") and not ins, "left past 1e-30")
    s.ok(w["left"][3] == mpq(1, 10**30), "left past area 1e-30")
    w, ins = walls_both(t(sq0, E, o - E), side)
    s.ok(w["left"][0] == E and w["left"][1:3] == ("clear", "clear") and ins, "left short 1e-30")
    s.ok(w["top"][0] == E and w["top"][1:3] == ("clear", "clear"), "top short 1e-30")
    w, ins = walls_both(t(sq0, o, o), side)
    s.ok(w["right"][1:3] == ("contact", "contact") and w["top"][1:3] == ("contact", "contact") and ins, "far corner contact")
    top_vertex = G.square(Q(1), side - Q(7, 10), Q(3, 5), Q(4, 5))  # top vertex at y = 2
    w, ins = walls_both(top_vertex, side)
    s.ok(w["top"][0] == 0 and w["top"][1:3] == ("contact", "contact") and ins, "3-4-5 vertex at top")
    w, ins = walls_both(t(top_vertex, z, E), side)
    s.ok(w["top"][1:3] == ("outside", "outside") and not ins, "3-4-5 vertex past top")
    s.ok(w["top"][3] == mpq(25, 24) * mpq(1, 10**60), "3-4-5 vertex past top area")
    # 5. random pairs closed along the centre line
    trip = triples(14)
    for k in range(n_random_pairs):
        def rnd_rot() -> tuple[Q, Q]:
            c, sn = rng.choice(trip)
            if rng.random() < 0.5:
                c, sn = sn, c
            return (c * rng.choice((1, -1)), sn * rng.choice((1, -1)))

        ca_ = (Q(rng.randint(-10**6, 10**6), rng.randint(1, 10**5)), Q(rng.randint(-10**6, 10**6), rng.randint(1, 10**5)))
        ang = rng.random()
        dirx = Q(rng.randint(-1000, 1000), 997)
        diry = Q(rng.randint(-1000, 1000), 991)
        if dirx == 0 and diry == 0:
            dirx = Q(1)
        nrm = abs(dirx) + abs(diry)
        dist = Q(3) + Q(int(ang * 1000), 1000)
        cb_ = (ca_[0] + dist * dirx / nrm * 2, ca_[1] + dist * diry / nrm * 2)
        r1, r2 = rnd_rot(), rnd_rot()
        p = G.square(ca_[0], ca_[1], r1[0], r1[1], rng.random() < 0.5, rng.randrange(4))
        q = G.square(cb_[0], cb_[1], r2[0], r2[1], rng.random() < 0.5, rng.randrange(4))
        m0, c0a, c0b, _ = pair_both(p, q)
        s.ok(m0 > 0 and c0a == c0b == "apart", f"random {k}: start apart")
        info = G.close_along_centres(p, q, E)
        d, t0, t1, sl = info["d"], info["t0"], info["t1"], info["slope"]
        assert isinstance(t0, Q) and isinstance(t1, Q) and isinstance(sl, Q) and isinstance(d, tuple)
        m, xa, xb, ar = pair_both(p, G.moved(q, d, t0))
        s.ok(m == 0 and xa == xb == "contact" and ar == 0, f"random {k}: contact ({m}, {xa}, {xb})")
        m, xa, xb, ar = pair_both(p, G.moved(q, d, t1))
        s.ok(m == -E and xa == xb == "overlap" and ar > 0, f"random {k}: past ({float(m)}, {xa}, {xb})")
        m, xa, xb, ar = pair_both(p, G.moved(q, d, t0 - E / (-sl)))
        s.ok(m > 0 and xa == xb == "apart", f"random {k}: short ({float(m)}, {xa}, {xb})")
    # 6. random squares to a wall: contact, past, short
    side = Q(10)
    for k in range(n_random_walls):
        c, sn = rng.choice(trip)
        pts = G.square(Q(rng.randint(2000, 8000), 1000), Q(rng.randint(2000, 8000), 1000), c, sn, rng.random() < 0.5, rng.randrange(4))
        wall = rng.choice(A.WALLS)
        xs = [x for x, _ in pts]
        ys = [y for _, y in pts]
        cl = {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}[wall]
        for past, cls, ins_exp in ((z, "contact", True), (E, "outside", False), (-E, "clear", True)):
            w, ins = walls_both(G.to_wall(pts, wall, cl, past), side)
            s.ok(w[wall][1:3] == (cls, cls) and ins == ins_exp, f"random wall {k} {wall} {cls}")


# ----- reader cases -------------------------------------------------------------------

BASE_YAML = """softschema:
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
    - - '0'
      - '0'
    - - '1'
      - '0'
    - - '1'
      - '1'
    - - '0'
      - '1'
  - id: 2
    corners:
    - - 6/5
      - 1/2
    - - 9/5
      - 13/10
    - - '1'
      - 19/10
    - - 2/5
      - 11/10
  claim:
    coordinate_provenance: verified
    method: exact-algebraic
    limitations: test
  source:
    path: test
  certificate:
    kind: test
"""


def base_twin() -> dict[str, Any]:
    return R.yaml_tree(BASE_YAML)


def reader_cases(s: Suite) -> list[dict[str, str]]:
    log: list[dict[str, str]] = []
    good_twin = json.dumps(base_twin())

    def expect_ok(name: str, y: str, j: str | None) -> None:
        try:
            r = R.read_texts(y, j)
            s.ok(r.n == 2, f"reader accepts {name}")
            log.append({"case": name, "outcome": "accepted"})
        except R.ReadRefused as exc:
            s.ok(False, f"reader refused good {name}: {exc}")

    def expect_refused(name: str, y: str, j: str | None) -> None:
        try:
            R.read_texts(y, j)
            s.ok(False, f"reader accepted bad {name}")
        except R.ReadRefused as exc:
            s.ok(True, name)
            log.append({"case": name, "refused": str(exc)[:120]})

    expect_ok("the base file and its twin", BASE_YAML, good_twin)
    expect_ok("the base file, no twin, plain scalars quoted", BASE_YAML.replace("- 6/5", "- '6/5'"), None)
    # an integer coordinate written plainly is not the string the schema asks for
    yb = BASE_YAML

    def sub(old: str, new: str, count: int = 1) -> str:
        assert old in yb, old
        return yb.replace(old, new, count)

    bad_yaml = {
        "anchor": sub("  side: '2'", "  side: &s '2'"),
        "alias": sub("  side: '2'", "  side: &s '2'").replace("    path: test", "    path: *s"),
        "explicit !!str tag": sub("  side: '2'", "  side: !!str 2"),
        "python object tag": sub("  side: '2'", "  side: !!python/object:fractions.Fraction {}"),
        "local tag": sub("  side: '2'", "  side: !rational '2'"),
        "duplicate key in witness": sub("  n: 2\n", "  n: 2\n  n: 2\n"),
        "duplicate key in square": sub("  - id: 2\n", "  - id: 2\n    id: 2\n"),
        "float n": sub("  n: 2\n", "  n: 2.0\n"),
        "boolean n": sub("  n: 2\n", "  n: yes\n"),
        "null side": sub("  side: '2'", "  side:"),
        "hex n": sub("  n: 2\n", "  n: 0x2\n"),
        "underscored n": sub("  n: 2\n", "  n: 0_2\n"),
        "sexagesimal n": sub("  n: 2\n", "  n: 0:02\n"),
        "merge key": sub("  scalar:\n    kind: rational", "  scalar:\n    <<: {kind: rational}"),
        "side 4/2 not lowest": sub("  side: '2'", "  side: 4/2"),
        "side 2/1": sub("  side: '2'", "  side: 2/1"),
        "side 02": sub("  side: '2'", "  side: '02'"),
        "side +2": sub("  side: '2'", "  side: '+2'"),
        "side 2.0 string": sub("  side: '2'", "  side: '2.0'"),
        "side 2e0 string": sub("  side: '2'", "  side: '2e0'"),
        "side with space": sub("  side: '2'", "  side: ' 2'"),
        "side 0": sub("  side: '2'", "  side: '0'"),
        "side negative": sub("  side: '2'", "  side: '-2'"),
        "coordinate -0": sub("    - - '0'\n      - '0'", "    - - '-0'\n      - '0'"),
        "coordinate 0/5": sub("    - - '0'\n      - '0'", "    - - 0/5\n      - '0'"),
        "coordinate 1/-2": sub("    - - 6/5", "    - - 6/-5"),
        "coordinate 1/0": sub("    - - 6/5", "    - - 6/0"),
        "coordinate plain integer 0": sub("    - - '0'\n      - '0'", "    - - 0\n      - '0'"),
        "id as string": sub("  - id: 2\n", "  - id: '2'\n"),
        "ids out of order": sub("  - id: 1\n", "  - id: 2\n", 1),
        "n too large": sub("  n: 2\n", "  n: 3\n"),
        "extra square key": sub("  - id: 2\n", "  - id: 2\n    angle: '0'\n"),
        "three corners": sub("    - - 2/5\n      - 11/10\n", ""),
        "three coordinates": sub("    - - 2/5\n      - 11/10\n", "    - - 2/5\n      - 11/10\n      - '0'\n"),
        "representation": sub("representation: corners", "representation: center-angle"),
        "scalar kind": sub("    kind: rational", "    kind: decimal"),
        "square_size": sub("square_size: '1'", "square_size: '2'"),
        "origin": sub("origin: lower-left", "origin: container-center"),
        "angle unit": sub("angle_unit: not-applicable", "angle_unit: degrees"),
        "unknown witness key": sub("  n: 2\n", "  n: 2\n  extra: x\n"),
        "missing claim": sub("  claim:\n    coordinate_provenance: verified\n    method: exact-algebraic\n    limitations: test\n", ""),
        "contract": sub("packing.squares:Witness/v2", "packing.squares:Witness/v1"),
        "extra envelope key": yb + "extra: 1\n",
        "two documents": yb + "---\na: 1\n",
    }
    for name, y in bad_yaml.items():
        expect_refused(f"yaml: {name}", y, None)
    tw = base_twin()
    bad_json: dict[str, str] = {}
    t1 = json.loads(json.dumps(tw))
    t1["witness"]["side"] = "3"
    bad_json["value differs"] = json.dumps(t1)
    t2 = json.loads(json.dumps(tw))
    t2["witness"]["n"] = "2"
    bad_json["type differs"] = json.dumps(t2)
    bad_json["float"] = good_twin.replace('"n": 2', '"n": 2.0')
    bad_json["NaN"] = good_twin.replace('"n": 2', '"n": NaN')
    bad_json["duplicate key"] = good_twin.replace('"n": 2', '"n": 2, "n": 2')
    t3 = json.loads(json.dumps(tw))
    del t3["witness"]["source"]
    bad_json["missing key"] = json.dumps(t3)
    t4 = json.loads(json.dumps(tw))
    t4["witness"]["squares"][1]["corners"][0][0] = "7/5"
    bad_json["coordinate differs"] = json.dumps(t4)
    bad_json["not JSON"] = good_twin[:-2]
    for name, j in bad_json.items():
        expect_refused(f"twin: {name}", BASE_YAML, j)
    return log


def broken_runs(rng_seed: int) -> dict[str, int]:
    """Run the geometric cases against two broken copies; each must fail."""
    out = {}
    orig_sign, orig_clip = A.sign_class, B.clip

    def sign_broken(v: Q) -> str:
        return "apart" if v >= 0 else "overlap"

    def clip_open(poly: list[Any], h: Any) -> list[Any]:
        a, b, c = h
        if not poly:
            return []
        vals = [a * p[0] + b * p[1] + c for p in poly]
        res = []
        for i in range(len(poly)):
            cur, vc, prv, vp = poly[i], vals[i], poly[i - 1], vals[i - 1]
            if (vp > 0 and vc < 0) or (vp < 0 and vc > 0):
                tt = vp / (vp - vc)
                res.append((prv[0] + tt * (cur[0] - prv[0]), prv[1] + tt * (cur[1] - prv[1])))
            if vc > 0:
                res.append(cur)
        return res

    variants: dict[str, tuple[Callable[..., Any], Callable[..., Any]]] = {
        "A counts a zero margin as apart": (sign_broken, orig_clip),
        "B clips with open half-planes": (orig_sign, clip_open),
    }
    for name, (sg, cl) in variants.items():
        A.sign_class = sg
        B.clip = cl
        s = Suite()
        try:
            geometric(s, random.Random(rng_seed), 40, 30)
            out[name] = len(s.failures)
        except Exception as exc:  # a broken copy may also crash
            out[name] = -1
            out[name + " (raised)"] = 1
            print("broken copy raised:", type(exc).__name__, exc)
        finally:
            A.sign_class = orig_sign
            B.clip = orig_clip
    return out


def main() -> int:
    out_path = sys.argv[1]
    s = Suite()
    geometric(s, random.Random(20261111), 400, 300)
    log = reader_cases(s)
    broken = broken_runs(20261112)
    teeth_ok = all(v != 0 for v in broken.values())
    passed = not s.failures and teeth_ok
    receipt = {
        "program": "l109_selftest.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "python": sys.version.split()[0],
        "verdict": "PASSED" if passed else "FAILED",
        "cases": s.cases,
        "failures": s.failures[:50],
        "reader_cases": log,
        "broken_copies_failures": broken,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(receipt["verdict"], f"{s.cases} cases, {len(s.failures)} failed; broken copies: {broken}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
