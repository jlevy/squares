"""Self-test of lane L127's reader and both methods, with two deliberately broken copies.

Lane L127, clean room. Usage: python -I -B l127_selftest.py OUT.json

Every expected value comes from the construction (a gap delta set by hand, an area
derived by hand, or the closed form of l127_geom.py from centres and half-widths), never
from either method.
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections.abc import Callable
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_clip as mb  # noqa: E402
import l127_geom as g  # noqa: E402
import l127_reader as rd  # noqa: E402
import l127_sat as ma  # noqa: E402

TINY = F(1, 10**30)
HALF = F(1, 2)
C345, S345 = F(3, 5), F(4, 5)


def cls_of(delta: F) -> str:
    return "apart" if delta > 0 else ("touch" if delta == 0 else "overlap")


def wcls_of(delta: F) -> str:
    return "clear" if delta > 0 else ("touch" if delta == 0 else "outside")


class Suite:
    def __init__(self, broken: str | None) -> None:
        self.broken = broken
        self.cases = 0
        self.failures: list[str] = []

    # --- the methods, possibly broken
    def a_class(self, m: tuple[int, int]) -> str:
        if self.broken == "A-zero-is-apart":
            return "apart" if m[0] >= 0 else "overlap"
        return ma.pair_class(m)

    def a_wclass(self, m: tuple[int, int]) -> str:
        if self.broken == "A-zero-is-apart":
            return "clear" if m[0] >= 0 else "outside"
        return ma.wall_class(m)

    @property
    def keep(self) -> bool:
        return self.broken != "B-open"

    def check(self, ok: bool, what: str) -> None:
        self.cases += 1
        if not ok:
            self.failures.append(what)

    # --- pair case: two corner lists, expected margin, class and area
    def pair(
        self,
        c1: list[tuple[F, F]],
        c2: list[tuple[F, F]],
        margin: F,
        area: F | None,
        label: str,
    ) -> None:
        r1, r2 = g.to_reader(c1), g.to_reader(c2)
        a1, a2 = ma.make_square(r1), ma.make_square(r2)
        b1, b2 = mb.make_square(r1), mb.make_square(r2)
        for x, y, bx, by, order in ((a1, a2, b1, b2, "12"), (a2, a1, b2, b1, "21")):
            m = ma.pair_margin(x, y)
            got = F(m[0], m[1])
            want_cls = cls_of(margin)
            ca = self.a_class(m)
            cb, ar = mb.pair(bx, by, keep_boundary=self.keep)
            self.check(got == margin, f"{label} {order}: margin {got} != {margin}")
            self.check(ca == want_cls, f"{label} {order}: A class {ca} != {want_cls}")
            self.check(cb == want_cls, f"{label} {order}: B class {cb} != {want_cls}")
            if area is not None:
                self.check(F(int(ar.numerator), int(ar.denominator)) == area, f"{label} {order}: area {ar} != {area}")

    def listings(self, sq: g.Placed) -> list[tuple[str, list[tuple[F, F]]]]:
        return [
            (f"{'ccw' if ccw else 'cw'}{start}", g.corners(sq, ccw=ccw, start=start))
            for ccw in (True, False)
            for start in (0, 1)
        ]

    def pair_all_listings(self, p: g.Placed, q: g.Placed, margin: F, area: F | None, label: str) -> None:
        for l1, c1 in self.listings(p):
            for l2, c2 in self.listings(q):
                self.pair(c1, c2, margin, area, f"{label} [{l1},{l2}]")

    def sense(self, pts: list[tuple[F, F]], want: int, label: str) -> None:
        r = g.to_reader(pts)
        self.check(ma.make_square(r).sense == want, f"{label}: A sense")
        self.check(mb.make_square(r).sense == want, f"{label}: B sense")

    def wall(self, pts: list[tuple[F, F]], side: F, want: dict[str, F], label: str) -> None:
        r = g.to_reader(pts)
        a = ma.make_square(r)
        b = mb.make_square(r)
        sd = (side.numerator, side.denominator)
        cl = ma.wall_clearances(a, sd)
        cb = mb.wall_classes(b, sd, keep_boundary=self.keep)
        for wall, delta in want.items():
            got = F(cl[wall][0], cl[wall][1])
            self.check(got == delta, f"{label} {wall}: clearance {got} != {delta}")
            self.check(self.a_wclass(cl[wall]) == wcls_of(delta), f"{label} {wall}: A class")
            self.check(cb[wall] == wcls_of(delta), f"{label} {wall}: B class {cb[wall]}")
        inside = all(d >= 0 for d in want.values())
        self.check(mb.inside_box(b, sd, keep_boundary=self.keep) == inside, f"{label}: B inside")

    def refuse_shape(self, pts: list[tuple[F, F]], label: str) -> None:
        r = g.to_reader(pts)
        for name, mk, exc in (("A", ma.make_square, ma.NotUnit), ("B", mb.make_square, mb.NotUnit)):
            try:
                mk(r)
            except exc:
                self.check(True, "")
            else:
                self.check(False, f"{label}: {name} accepted a non-square")


# ------------------------------------------------------------------ cases


def contacts(s: Suite) -> None:
    o = g.Placed(F(0), F(0), F(1), F(0))
    for delta in (TINY, F(0), -TINY):
        # edge to edge, each of four directions
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            q = g.Placed(dx * (1 + delta), dy * (1 + delta), F(1), F(0))
            s.pair_all_listings(o, q, delta, abs(delta) if delta < 0 else F(0), f"edge{dx},{dy} d={delta}")
        # corner to corner
        q = g.Placed(1 + delta, 1 + delta, F(1), F(0))
        s.pair_all_listings(o, q, delta, delta * delta if delta < 0 else F(0), f"corner d={delta}")
        # 3-4-5 vertex on edge: lowest vertex of q at (1/10, 1/2 + delta)
        q = g.Placed(F(0), HALF + F(7, 10) + delta, C345, S345)
        s.pair_all_listings(o, q, delta, F(25, 24) * delta * delta if delta < 0 else F(0), f"v-on-e d={delta}")
    # duplicate, and concentric rotations
    s.pair_all_listings(o, o, F(-1), F(1), "duplicate")
    for c, sn in ((C345, S345), (S345, C345)):
        q = g.Placed(F(0), F(0), c, sn)
        area = 1 - 2 * c * sn / (1 + c + sn) ** 2
        s.pair_all_listings(o, q, F(-6, 5), area, f"concentric {c},{sn}")
        assert area == F(5, 6)


def senses(s: Suite) -> None:
    for sq in (g.Placed(F(0), F(0), F(1), F(0)), g.Placed(F(3), F(2), C345, S345)):
        for ccw in (True, False):
            for start in range(4):
                s.sense(g.corners(sq, ccw=ccw, start=start), 1 if ccw else -1, f"sense {sq} {ccw} {start}")


def walls(s: Suite) -> None:
    side = F(5)
    for delta in (TINY, F(0), -TINY):
        # upright square at each wall, other walls far
        cases = {
            "left": g.Placed(HALF + delta, F(2), F(1), F(0)),
            "bottom": g.Placed(F(2), HALF + delta, F(1), F(0)),
            "right": g.Placed(side - HALF - delta, F(2), F(1), F(0)),
            "top": g.Placed(F(2), side - HALF - delta, F(1), F(0)),
        }
        for wall, sq in cases.items():
            want = {
                "left": sq.cx - HALF,
                "bottom": sq.cy - HALF,
                "right": side - sq.cx - HALF,
                "top": side - sq.cy - HALF,
            }
            assert want[wall] == delta
            for lab, pts in s.listings(sq):
                s.wall(pts, side, want, f"wall {wall} d={delta} {lab}")
        # a 3-4-5 square whose top vertex is at the top wall (vertical half-extent 7/10)
        sq = g.Placed(F(2), side - F(7, 10) - delta, C345, S345)
        want = {"left": F(2) - F(7, 10), "bottom": sq.cy - F(7, 10), "right": side - F(2) - F(7, 10), "top": delta}
        for lab, pts in s.listings(sq):
            s.wall(pts, side, want, f"wall tilted top d={delta} {lab}")


def shapes(s: Suite) -> None:
    z, o = F(0), F(1)
    s.refuse_shape([(z, z), (o, z), (1 + C345, S345), (C345, S345)], "3-4-5 rhombus")
    sq = g.corners(g.Placed(F(1), F(1), F(1), F(0)))
    s.refuse_shape([sq[0], sq[2], sq[1], sq[3]], "bowtie order")
    s.refuse_shape([(z, z), (o + TINY, z), (o + TINY, o), (z, o)], "1 x (1 + 1e-30) rectangle")
    s.refuse_shape([(z, z), (o, z), (o + TINY, o), (z, o)], "third corner off by 1e-30")
    s.refuse_shape([(z, z), (o, z), (o, o), (z, o + TINY)], "fourth corner off by 1e-30")
    s.refuse_shape([(z, z), (F(2), z), (F(2), F(2)), (z, F(2))], "side 2")
    s.refuse_shape([(z, z)] * 4, "a point")
    s.refuse_shape([(z, z), (o, z), (o, o), (o, z)], "unit sides, one diagonal sqrt 2, P3 = P1")
    t = g.corners(g.Placed(F(2), F(2), C345, S345))
    t[2] = (t[2][0] + TINY, t[2][1])
    s.refuse_shape(t, "tilted square, a corner off by 1e-30")


def rand_placed(rng: random.Random, spread: int) -> g.Placed:
    m = rng.randint(2, 40)
    n = rng.randint(1, m - 1)
    c, sn = g.pythagorean(m, n)
    k = rng.randrange(8)
    if k & 1:
        c, sn = sn, c
    if k & 2:
        c = -c
    if k & 4:
        sn = -sn
    cx = F(rng.randint(-spread * 1000, spread * 1000), rng.randint(1, 997))
    cy = F(rng.randint(-spread * 1000, spread * 1000), rng.randint(1, 997))
    return g.Placed(cx, cy, c, sn)


def random_pairs(s: Suite, rng: random.Random) -> None:
    # closing along the centre line: short of, at, and past contact by 1e-30
    done = 0
    while done < 400:
        p = rand_placed(rng, 3)
        q = rand_placed(rng, 3)
        if p.cx == q.cx and p.cy == q.cy:
            continue
        cl = g.closing(p, q)
        rmax, rmin = max(cl.binding_rates), min(cl.binding_rates)
        # keep the move tiny against every non-binding axis's slack
        if cl.other_slack < F(1, 10**20):
            continue
        for label, t, want in (
            ("short", cl.t_star - TINY / rmax, TINY),
            ("at", cl.t_star, F(0)),
            ("past", cl.t_star + TINY / rmin, -TINY),
        ):
            q2 = g.moved(q, p, t)
            cf = g.closed_margin(p, q2)
            s.check(cf == want, f"random close {done} {label}: closed form {cf} != {want}")
            s.pair(g.corners(p), g.corners(q2, ccw=bool(done & 1)), want, None, f"random close {done} {label}")
        done += 1
    # random positions: methods, closed form and the sign of B's area agree
    for k in range(300):
        p = rand_placed(rng, 1)
        q = rand_placed(rng, 1)
        cf = g.closed_margin(p, q)
        s.pair(g.corners(p, start=k % 4), g.corners(q, ccw=bool(k & 1)), cf, None, f"random pair {k}")


def random_walls(s: Suite, rng: random.Random) -> None:
    side = F(9)
    for k in range(300):
        p = rand_placed(rng, 1)
        hx = g.half_width(p, (F(1), F(0)))
        hy = g.half_width(p, (F(0), F(1)))
        wall = ("left", "bottom", "right", "top")[k % 4]
        for delta in (TINY, F(0), -TINY):
            if wall == "left":
                q = g.Placed(hx + delta, F(4), p.c, p.s)
            elif wall == "bottom":
                q = g.Placed(F(4), hy + delta, p.c, p.s)
            elif wall == "right":
                q = g.Placed(side - hx - delta, F(4), p.c, p.s)
            else:
                q = g.Placed(F(4), side - hy - delta, p.c, p.s)
            want = {
                "left": q.cx - hx,
                "bottom": q.cy - hy,
                "right": side - q.cx - hx,
                "top": side - q.cy - hy,
            }
            s.check(want[wall] == delta, f"random wall {k}: construction")
            s.wall(g.corners(q, ccw=bool(k & 2)), side, want, f"random wall {k} {wall} d={delta}")


# ------------------------------------------------------------------ reader

VALID = """\
softschema:
  contract: packing.squares:Witness/v2
  schema: witness.schema.yaml
  envelope: witness
  status: enforced
witness:
  id: W-test-n2
  n: 2
  side: 5/2
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
    - - 3/2
      - 3/2
    - - 5/2
      - 3/2
    - - 5/2
      - 5/2
    - - 3/2
      - 5/2
  claim:
    coordinate_provenance: verified
    method: exact-algebraic
    limitations: test
  source:
    path: x.yaml
  certificate:
    kind: exact-rational-sat
    rational_digits: 36
    center_dilation: '1'
"""


def valid_json() -> str:
    return json.dumps(rd.load_yaml_tree(VALID))


def sub(old: str, new: str, count: int = 1) -> str:
    assert old in VALID, old
    return VALID.replace(old, new, count)


READER_CASES: list[tuple[str, str, str | None, str]] = [
    # (label, yaml, json or None meaning the valid twin, expected reason substring)
    ("anchor", sub("  id: W-test-n2", "  id: &a W-test-n2"), None, "anchor"),
    ("anchor and alias", sub("  id: W-test-n2", "  id: &a W-test-n2\n  zz: *a"), None, "anchor"),
    ("tag !!str", sub("  side: 5/2", "  side: !!str 5/2"), None, "explicit tag"),
    ("bare tag !", sub("  side: 5/2", "  side: ! 5/2"), None, "explicit tag"),
    ("tag !!int", sub("  n: 2", "  n: !!int 2"), None, "explicit tag"),
    ("duplicate key", sub("  n: 2", "  n: 2\n  n: 2"), None, "duplicate key"),
    ("two documents", VALID + "---\na: 1\n", None, "more than one document"),
    ("float n", sub("  n: 2", "  n: 2.0"), None, "scalar type"),
    ("bool n", sub("  n: 2", "  n: true"), None, "scalar type"),
    ("null side", sub("  side: 5/2", "  side: ~"), None, "scalar type"),
    ("hex n", sub("  n: 2", "  n: 0x2"), None, "not plain decimal"),
    ("signed n", sub("  n: 2", "  n: +2"), None, "not plain decimal"),
    ("octal n", sub("  n: 2", "  n: 02"), None, "not plain decimal"),
    ("underscore n", sub("  n: 2", "  n: 1_0"), None, "not plain decimal"),
    ("sexagesimal n", sub("  n: 2", "  n: 1:0"), None, "not plain decimal"),
    ("merge key", sub("  scalar:\n    kind: rational", "  scalar:\n    <<: {kind: rational}"), None, "non-string key"),
    ("syntax error", sub("  n: 2", "  n: [2"), None, "syntax"),
    ("side 5/1", sub("  side: 5/2", "  side: 5/1"), None, "not above 1"),
    ("side 10/4", sub("  side: 5/2", "  side: 10/4"), None, "lowest terms"),
    ("side 05/2", sub("  side: 5/2", "  side: 05/2"), None, "not canonical"),
    ("side +5/2", sub("  side: 5/2", "  side: +5/2"), None, "not canonical"),
    ("side 5/-2", sub("  side: 5/2", "  side: 5/-2"), None, "not canonical"),
    ("side 5/02", sub("  side: 5/2", "  side: 5/02"), None, "not canonical"),
    ("side 2.5 string", sub("  side: 5/2", "  side: '2.5'"), None, "not canonical"),
    ("side 2.5 float", sub("  side: 5/2", "  side: 2.5"), None, "scalar type"),
    ("side int", sub("  side: 5/2", "  side: 3"), None, "not a string"),
    ("side zero", sub("  side: 5/2", "  side: '0'"), None, "not positive"),
    ("side -0", sub("  side: 5/2", "  side: '-0'"), None, "not canonical"),
    ("side negative", sub("  side: 5/2", "  side: -5/2"), None, "not positive"),
    ("coordinate 0/1", sub("    - - '0'\n      - '0'", "    - - 0/1\n      - '0'"), None, "not above 1"),
    ("coordinate 0/2", sub("    - - '0'\n      - '0'", "    - - 0/2\n      - '0'"), None, "lowest terms"),
    ("coordinate int", sub("    - - '0'\n      - '0'", "    - - 0\n      - '0'"), None, "not a string"),
    ("coordinate spaces", sub("    - - 3/2\n", "    - - 3 / 2\n"), None, "not canonical"),
    ("n too large", sub("  n: 2", "  n: 3"), None, "entries for n"),
    ("n zero", sub("  n: 2", "  n: 0"), None, "positive integer"),
    ("ids swapped", sub("  - id: 1", "  - id: 2").replace("  - id: 2\n    corners:\n    - - 3/2", "  - id: 1\n    corners:\n    - - 3/2"), None, "id is not"),
    ("id string", sub("  - id: 1", "  - id: '1'"), None, "id is not"),
    ("id repeated", sub("  - id: 2", "  - id: 1"), None, "id is not"),
    ("missing claim", VALID.split("  claim:")[0] + "  source:\n    path: x.yaml\n", None, "missing"),
    ("extra witness key", sub("  n: 2", "  n: 2\n  foo: bar"), None, "outside the schema"),
    ("extra square key", sub("  - id: 1", "  - id: 1\n    angle: '0'"), None, "outside the schema"),
    ("three corners", sub("    - - '0'\n      - '1'\n", ""), None, "not four corners"),
    ("three coordinates", sub("    - - '0'\n      - '0'", "    - - '0'\n      - '0'\n      - '0'"), None, "not a point"),
    ("representation", sub("representation: corners", "representation: center-angle"), None, "representation"),
    ("scalar kind", sub("kind: rational", "kind: decimal"), None, "scalar"),
    ("origin", sub("origin: lower-left", "origin: container-center"), None, "coordinates"),
    ("square size", sub("square_size: '1'", "square_size: '2'"), None, "square_size"),
    ("contract", sub("Witness/v2", "Witness/v1"), None, "contract"),
    ("envelope", sub("envelope: witness", "envelope: other"), None, "envelope"),
    ("extra top key", VALID + "extra: 1\n", None, "outside the schema"),
    ("claim extra key", sub("    limitations: test", "    limitations: test\n    note: x"), None, "outside the schema"),
    ("source missing path", sub("    path: x.yaml", "    url: x"), None, "missing"),
    ("boolean in certificate", sub("    rational_digits: 36", "    rational_digits: 36\n    flag: yes"), None, "scalar type"),
    ("bad id", sub("  id: W-test-n2", "  id: X-test"), None, "witness.id"),
    ("twin differs", VALID, "DIFF", "twin differs"),
    ("twin type differs", VALID, "TYPE", "twin differs"),
    ("twin float", VALID, "FLOAT", "json: float"),
    ("twin NaN", VALID, "NAN", "json: constant"),
    ("twin duplicate key", VALID, "DUP", "duplicate key"),
    ("twin syntax", VALID, "SYNTAX", "json: syntax"),
    ("twin bool", VALID, "BOOL", "twin differs"),
]


def twin_for(kind: str | None) -> str:
    base = valid_json()
    if kind is None:
        return base
    if kind == "DIFF":
        return base.replace('"5/2"', '"5/3"', 1)
    if kind == "TYPE":
        return base.replace('"n": 2', '"n": "2"', 1)
    if kind == "FLOAT":
        return base.replace('"n": 2', '"n": 2.0', 1)
    if kind == "NAN":
        return base.replace('"n": 2', '"n": NaN', 1)
    if kind == "DUP":
        return base.replace('"n": 2', '"n": 2, "n": 2', 1)
    if kind == "SYNTAX":
        return base[:-1]
    if kind == "BOOL":
        return base.replace('"rational_digits": 36', '"rational_digits": true', 1)
    raise ValueError(kind)


def reader_cases(s: Suite) -> None:
    for label, ytext, jkind, reason in READER_CASES:
        jtext = twin_for(jkind)
        try:
            rd.read_certificate(ytext, jtext)
        except rd.Refused as exc:
            s.check(reason in str(exc), f"reader {label}: refused for {exc!s}, wanted {reason!r}")
        else:
            s.check(False, f"reader {label}: accepted")
    # two that must be accepted: the valid file, and the same in flow style with a comment
    for label, ytext in (
        ("valid", VALID),
        ("valid, comment and flow", sub("  scalar:\n    kind: rational", "  # comment\n  scalar: {kind: rational}")),
    ):
        try:
            out = rd.read_certificate(ytext, twin_for(None))
        except rd.Refused as exc:
            s.check(False, f"reader {label}: refused {exc}")
        else:
            s.check(out["n"] == 2 and out["side"] == (5, 2) and out["twin"] == "identical", f"reader {label}")


# ------------------------------------------------------------------ run


SECTIONS: list[tuple[str, Callable[[Suite], None]]] = [
    ("contacts", contacts),
    ("senses", senses),
    ("walls", walls),
    ("shapes", shapes),
    ("random", lambda s: (random_pairs(s, random.Random(20261112)), random_walls(s, random.Random(967)))),
    ("reader", reader_cases),
]


def run(broken: str | None) -> dict[str, Any]:
    s = Suite(broken)
    per: dict[str, int] = {}
    for name, fn in SECTIONS:
        before = s.cases
        fn(s)
        per[name] = s.cases - before
    return {"cases": s.cases, "failed": len(s.failures), "per_section": per, "first_failures": s.failures[:8]}


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    good = run(None)
    broken_a = run("A-zero-is-apart")
    broken_b = run("B-open")
    ok = good["failed"] == 0 and broken_a["failed"] > 0 and broken_b["failed"] > 0
    receipt = {
        "program": "l127_selftest.py",
        "verdict": "PASSED" if ok else "FAILED",
        "suite": good,
        "broken_method_a_zero_margin_counted_apart": {"cases": broken_a["cases"], "failed": broken_a["failed"]},
        "broken_method_b_open_half_planes": {"cases": broken_b["cases"], "failed": broken_b["failed"]},
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    Path(argv[1]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(receipt["verdict"], good["cases"], "cases", good["failed"], "failed;",
          "broken A fails", broken_a["failed"], "broken B fails", broken_b["failed"])
    if good["first_failures"]:
        for f in good["first_failures"]:
            print("  ", f)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
