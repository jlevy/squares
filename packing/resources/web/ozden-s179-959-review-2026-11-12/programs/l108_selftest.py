"""Self-test of the reader and both deciding methods; and of two broken copies.

Lane L108, blind stage 4 review of jlevy/squares#959. Every expected value below is
derived by hand in its comment, not by either method.

Usage: python -I -B l108_selftest.py OUT.json
"""

from __future__ import annotations

import json
import random
import sys
import time
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_check as check  # noqa: E402
import l108_clip as clipm  # noqa: E402
import l108_geom as geom  # noqa: E402
import l108_reader as reader  # noqa: E402
import l108_sat as satm  # noqa: E402

EPS = Fraction(1, 10**30)
F = Fraction
HALF = F(1, 2)


class Tally:
    def __init__(self) -> None:
        self.cases = 0
        self.failures: list[str] = []

    def ok(self, cond: bool, what: str) -> None:
        self.cases += 1
        if not cond:
            self.failures.append(what)


def both_pair(p: geom.Corners, q: geom.Corners) -> tuple[Any, str, str, Fraction] | None:
    """(margin, class A, class B, area B), or None when either method refuses a square."""
    a1, a2 = satm.build(geom.to_raw(p)), satm.build(geom.to_raw(q))
    b1, b2 = clipm.build(geom.to_raw(p)), clipm.build(geom.to_raw(q))
    if a1 is None or a2 is None or b1 is None or b2 is None:
        return None
    m = satm.margin(a1, a2)
    cb, area = clipm.pair(b1, clipm.inner_half_planes(b2))
    return (m, satm.classify(m), cb, area)


def expect_pair(t: Tally, p: geom.Corners, q: geom.Corners, cls: str, margin: Fraction | None, area: Fraction | None, what: str) -> None:
    for order, (x, y) in (("pq", (p, q)), ("qp", (q, p))):
        r = both_pair(x, y)
        t.ok(r is not None, f"{what} {order}: a square refused")
        if r is None:
            continue
        m, ca, cb, ar = r
        t.ok(ca == cls, f"{what} {order}: class A {ca} != {cls}")
        t.ok(cb == cls, f"{what} {order}: class B {cb} != {cls}")
        if margin is not None:
            t.ok(check.as_fraction(m) == margin, f"{what} {order}: margin {check.dec(check.as_fraction(m))} != {check.dec(margin)}")
        if area is not None:
            t.ok(ar == area, f"{what} {order}: area {check.dec(ar)} != {check.dec(area)}")


def variants(sq: geom.Corners) -> list[tuple[str, geom.Corners]]:
    """The same square listed counterclockwise and clockwise, from two starting corners."""
    p0, p1, p2, p3 = sq
    ccw = (p0, p1, p2, p3)
    cw = (p0, p3, p2, p1)
    out = []
    for name, s in (("ccw", ccw), ("cw", cw)):
        for start in (0, 2):
            r = s[start:] + s[:start]
            out.append((f"{name}{start}", (r[0], r[1], r[2], r[3])))
    return out


def axis_square(x0: Fraction, y0: Fraction) -> geom.Corners:
    return ((x0, y0), (x0 + 1, y0), (x0 + 1, y0 + 1), (x0, y0 + 1))


def contact_cases(t: Tally) -> None:
    base = axis_square(F(0), F(0))
    for delta, cls in ((EPS, "clear"), (F(0), "contact"), (-EPS, "overlap")):
        # Edge to edge: Q = [1 + d, 2 + d] x [0, 1]; margin d, overlap a 1 x |d| strip.
        q = axis_square(1 + delta, F(0))
        area = -delta if delta < 0 else F(0)
        for nv, vp in variants(base):
            for nq, vq in variants(q):
                expect_pair(t, vp, vq, cls, delta, area, f"edge d={check.dec(delta, 1)} {nv}/{nq}")
        # Corner to corner: Q = [1 + d, 2 + d]^2; margin d, overlap a |d| x |d| square.
        q = axis_square(1 + delta, 1 + delta)
        area = delta * delta if delta < 0 else F(0)
        for nv, vp in variants(base):
            for nq, vq in variants(q):
                expect_pair(t, vp, vq, cls, delta, area, f"corner d={check.dec(delta, 1)} {nv}/{nq}")
        # A 3-4-5 vertex on the top edge of [0, 1]^2 at x = 1/2, edges (4/5, 3/5) and
        # (-3/5, 4/5) from it. The binding axis is (0, 1), margin d. Below y = 1 at depth
        # |d| the two edges reach x offsets 4|d|/3 and -3|d|/4: a triangle of base
        # 25|d|/12 and height |d|, area 25 d^2 / 24.
        v = (HALF, 1 + delta)
        e1, e2 = (F(4, 5), F(3, 5)), (F(-3, 5), F(4, 5))
        tilt = (v, (v[0] + e1[0], v[1] + e1[1]), (v[0] + e1[0] + e2[0], v[1] + e1[1] + e2[1]), (v[0] + e2[0], v[1] + e2[1]))
        area = F(25, 24) * delta * delta if delta < 0 else F(0)
        for nv, vp in variants(base):
            for nq, vq in variants(tilt):
                expect_pair(t, vp, vq, cls, delta, area, f"vertex-edge d={check.dec(delta, 1)} {nv}/{nq}")


def overlap_cases(t: Tally) -> None:
    base = axis_square(F(0), F(0))
    # A duplicate: on its own axes the projections coincide, gap -1; area 1.
    expect_pair(t, base, base, "overlap", F(-1), F(1), "duplicate")
    # Concentric with a rotation by (c, s): on every axis the half-widths are 1/2 and
    # (c + s)/2, so the gap is -(1 + c + s)/2 = -6/5 for (3/5, 4/5). The overlap is the
    # square less four corner triangles of legs (c + s - 1)/(2s) and (c + s - 1)/(2c), so
    # 1 - (c + s - 1)^2 / (2sc) = 2 / (1 + c + s) = 5/6.
    ctr = (HALF, HALF)
    for rot in ((F(3, 5), F(4, 5)), (F(4, 5), F(3, 5))):
        q = geom.square(ctr, rot)
        expect_pair(t, base, q, "overlap", F(-6, 5), F(5, 6), f"concentric {rot}")


def wall_cases(t: Tally) -> None:
    sq = axis_square(F(0), F(0))
    for side, expect in (
        (F(1), {"left": "contact", "bottom": "contact", "right": "contact", "top": "contact"}),
        (1 + EPS, {"left": "contact", "bottom": "contact", "right": "clear", "top": "clear"}),
        (1 - EPS, {"left": "contact", "bottom": "contact", "right": "overlap", "top": "overlap"}),
    ):
        for name, v in variants(sq):
            a = satm.build(geom.to_raw(v))
            b = clipm.build(geom.to_raw(v))
            assert a is not None and b is not None
            ca = satm.walls(a, satm.side_q((side.numerator, side.denominator)))
            planes = clipm.wall_planes(side)
            for wall, cls in expect.items():
                t.ok(satm.classify(ca[wall]) == cls, f"wall {wall} side {check.dec(side, 3)} {name}: A")
                t.ok(clipm.wall(b, planes[wall])[0] == cls, f"wall {wall} side {check.dec(side, 3)} {name}: B")
            inside = all(c != "overlap" for c in expect.values())
            t.ok((clipm.area_in_box(b, side) == 1) == inside, f"box area side {check.dec(side, 3)} {name}")
    # A 3-4-5 square with its top vertex at height H + d, in a box of side H = 3.
    for delta, cls in ((EPS, "overlap"), (F(0), "contact"), (-EPS, "clear")):
        top = (F(3, 2), 3 + delta)
        e1, e2 = (F(-4, 5), F(-3, 5)), (F(3, 5), F(-4, 5))
        sq = (top, (top[0] + e1[0], top[1] + e1[1]), (top[0] + e1[0] + e2[0], top[1] + e1[1] + e2[1]), (top[0] + e2[0], top[1] + e2[1]))
        for name, v in variants(sq):
            a = satm.build(geom.to_raw(v))
            b = clipm.build(geom.to_raw(v))
            t.ok(a is not None and b is not None, f"tilted wall square {name} refused")
            if a is None or b is None:
                continue
            clear_top = satm.walls(a, satm.side_q((3, 1)))["top"]
            t.ok(check.as_fraction(clear_top) == -delta, f"tilted top clearance {name}")
            t.ok(satm.classify(clear_top) == cls, f"tilted top class A {name}")
            t.ok(clipm.wall(b, clipm.wall_planes(F(3))["top"])[0] == cls, f"tilted top class B {name}")


def refuse_shapes(t: Tally) -> None:
    c, s = F(3, 5), F(4, 5)
    tilted = geom.square((F(2), F(2)), (c, s))
    shapes = {
        "rhombus 3-4-5": ((F(0), F(0)), (F(1), F(0)), (1 + c, s), (c, s)),
        "bowtie order": ((F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(1), F(1))),
        "rectangle 1 x (1 + eps)": ((F(0), F(0)), (F(1), F(0)), (F(1), 1 + EPS), (F(0), 1 + EPS)),
        "corner off by eps": ((F(0), F(0)), (F(1), F(0)), (1 + EPS, F(1)), (F(0), F(1))),
        "square of side 2": ((F(0), F(0)), (F(2), F(0)), (F(2), F(2)), (F(0), F(2))),
        "a point": ((F(0), F(0)),) * 4,
        "tilted, a corner off": tilted[:3] + ((tilted[3][0], tilted[3][1] + EPS),),
    }
    for name, sh in shapes.items():
        raw = geom.to_raw(sh)  # type: ignore[arg-type]
        t.ok(satm.build(raw) is None, f"method A accepts the {name}")
        t.ok(clipm.build(raw) is None, f"method B accepts the {name}")


def random_closing(t: Tally, rng: random.Random, count: int) -> None:
    """Random rational pairs closed along their centre line: before, at and past contact."""
    for k in range(count):
        rots = [geom.pythagorean(rng.randint(2, 40), rng.randint(1, 39)) for _ in range(2)]
        rots = [r if rng.random() < 0.5 else (r[1], r[0]) for r in rots]
        p = geom.square((F(rng.randint(0, 999), 97), F(rng.randint(0, 999), 89)), rots[0], ccw=rng.random() < 0.5, start=rng.randint(0, 3))
        q0 = geom.square((F(rng.randint(0, 999), 97) + 3, F(rng.randint(0, 999), 89) - 2), rots[1], ccw=rng.random() < 0.5, start=rng.randint(0, 3))
        info = geom.closing(p, q0)
        tau = info["tau"]
        assert isinstance(tau, Fraction)
        for label, tt, cls in (("short", tau - EPS, "clear"), ("at", tau, "contact"), ("past", geom.past_tau(info, EPS), "overlap")):
            q = geom.moved(q0, info, tt)
            r = both_pair(p, q)
            t.ok(r is not None, f"random {k} {label}: refused")
            if r is None:
                continue
            m, ca, cb, area = r
            t.ok(ca == cls and cb == cls, f"random {k} {label}: classes {ca}/{cb} != {cls}")
            t.ok(check.as_fraction(m) == geom.gap_at(info, tt), f"random {k} {label}: margin != closed form")
            if label == "past":
                t.ok(area > 0, f"random {k} past: area 0")


def random_general(t: Tally, rng: random.Random, count: int) -> None:
    """Random pairs anywhere near each other: the two methods' classes agree."""
    seen = {"clear": 0, "overlap": 0}
    for k in range(count):
        rots = [geom.pythagorean(rng.randint(2, 30), rng.randint(1, 29)) for _ in range(2)]
        p = geom.square((F(rng.randint(0, 300), 100), F(rng.randint(0, 300), 100)), rots[0])
        q = geom.square((F(rng.randint(0, 300), 100), F(rng.randint(0, 300), 100)), rots[1], ccw=False)
        r = both_pair(p, q)
        t.ok(r is not None, f"general {k}: refused")
        if r is None:
            continue
        m, ca, cb, area = r
        t.ok(ca == cb, f"general {k}: classes {ca}/{cb}")
        t.ok((area > 0) == (check.as_fraction(m) < 0), f"general {k}: area sign vs margin sign")
        if ca in seen:
            seen[ca] += 1
    t.ok(seen["clear"] > 20 and seen["overlap"] > 20, f"general: too few of a class {seen}")


def random_walls(t: Tally, rng: random.Random, count: int) -> None:
    side = F(10)
    names = ("left", "bottom", "right", "top")
    for k in range(count):
        rot = geom.pythagorean(rng.randint(2, 40), rng.randint(1, 39))
        sq = geom.square((F(rng.randint(100, 900), 100), F(rng.randint(100, 900), 100)), rot, ccw=rng.random() < 0.5)
        wall = names[k % 4]
        dist = geom.clearances(sq, side)[wall]
        for label, move, cls in (("short", dist - EPS, "clear"), ("at", dist, "contact"), ("past", dist + EPS, "overlap")):
            v = geom.to_wall(sq, wall, move)
            a = satm.build(geom.to_raw(v))
            b = clipm.build(geom.to_raw(v))
            t.ok(a is not None and b is not None, f"wall {k}: refused")
            if a is None or b is None:
                continue
            ca = satm.classify(satm.walls(a, satm.side_q((10, 1)))[wall])
            cb = clipm.wall(b, clipm.wall_planes(side)[wall])[0]
            t.ok(ca == cls and cb == cls, f"wall {k} {wall} {label}: {ca}/{cb} != {cls}")


TINY_YAML = """softschema:
  contract: packing.squares:Witness/v2
  schema: witness.schema.yaml
  envelope: witness
  status: enforced
witness:
  id: W-tiny
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
    - ['0', '0']
    - ['1', '0']
    - ['1', '1']
    - ['0', '1']
  - id: 2
    corners:
    - [3/2, 3/2]
    - [5/2, 3/2]
    - [5/2, 5/2]
    - [3/2, 5/2]
  claim:
    coordinate_provenance: verified
    method: exact-algebraic
    limitations: test
"""


def tiny_json(tree: Any) -> str:
    return json.dumps(tree)


def reader_cases(t: Tally) -> None:
    good_tree = reader.load_yaml_tree(TINY_YAML)
    good_json = tiny_json(good_tree)

    def accepts(y: str, j: str | None, what: str) -> None:
        try:
            reader.read_texts(y, j)
            t.ok(True, what)
        except reader.Refused as exc:
            t.ok(False, f"reader refused {what}: {exc}")

    def refuses(y: str, j: str | None, what: str) -> None:
        try:
            reader.read_texts(y, j)
            t.ok(False, f"reader accepted {what}")
        except reader.Refused:
            t.ok(True, what)

    accepts(TINY_YAML, good_json, "the tiny file with its twin")
    accepts(TINY_YAML, None, "the tiny file alone")
    sub = TINY_YAML.replace
    yaml_cases = {
        "anchor and alias": sub("  scalar:\n    kind: rational", "  scalar: &k\n    kind: rational\n  extra: *k"),
        "anchor alone": sub("  scalar:\n    kind: rational", "  scalar: &k\n    kind: rational"),
        "explicit str tag": sub("side: 5/2", "side: !!str 5/2"),
        "duplicate key": sub("  n: 2\n", "  n: 2\n  n: 2\n"),
        "float side": sub("side: 5/2", "side: 2.5"),
        "integer side": sub("side: 5/2", "side: 3"),
        "bool value": sub("status: enforced", "status: true"),
        "null value": sub("status: enforced", "status:"),
        "side 10/4": sub("side: 5/2", "side: 10/4"),
        "side 5/1": sub("side: 5/2", "side: '5/1'"),
        "side -0": sub("side: 5/2", "side: '-0'"),
        "side 0": sub("side: 5/2", "side: '0'"),
        "side negative": sub("side: 5/2", "side: -5/2"),
        "side +5/2": sub("side: 5/2", "side: +5/2"),
        "side 05/2": sub("side: 5/2", "side: 05/2"),
        "side 5/02": sub("side: 5/2", "side: 5/02"),
        "side 5/0": sub("side: 5/2", "side: 5/0"),
        "side 5/-2": sub("side: 5/2", "side: 5/-2"),
        "side with space": sub("side: 5/2", "side: '5/2 '"),
        "side 2.5 quoted": sub("side: 5/2", "side: '2.5'"),
        "coordinate 1/1": sub("- ['1', '0']", "- ['1/1', '0']"),
        "coordinate 2/2": sub("- ['1', '0']", "- ['2/2', '0']"),
        "coordinate as integer": sub("- ['1', '0']", "- [1, '0']"),
        "representation center-angle": sub("representation: corners", "representation: center-angle"),
        "scalar decimal": sub("kind: rational", "kind: decimal"),
        "scalar extra key": sub("    kind: rational", "    kind: rational\n    extra: x"),
        "origin centre": sub("origin: lower-left", "origin: container-center"),
        "axes": sub("axes: x-right-y-up", "axes: x-right-y-down"),
        "angle unit": sub("angle_unit: not-applicable", "angle_unit: degrees"),
        "square size 2": sub("square_size: '1'", "square_size: '2'"),
        "square size integer": sub("square_size: '1'", "square_size: 1"),
        "n 3": sub("  n: 2\n", "  n: 3\n"),
        "n as string": sub("  n: 2\n", "  n: '2'\n"),
        "ids out of order": sub("  - id: 1\n", "  - id: 9\n"),
        "id as string": sub("  - id: 1\n", "  - id: '1'\n"),
        "three corners": sub("    - ['0', '1']\n", ""),
        "five corners": sub("    - ['0', '1']\n", "    - ['0', '1']\n    - ['0', '1']\n"),
        "a point of three": sub("- ['1', '0']", "- ['1', '0', '0']"),
        "extra square key": sub("  - id: 1\n", "  - id: 1\n    angle: '0'\n"),
        "unknown witness key": sub("  n: 2\n", "  n: 2\n  lineage: x\n"),
        "missing claim": TINY_YAML.split("  claim:")[0],
        "wrong contract": sub("Witness/v2", "Witness/v1"),
        "extra top-level key": TINY_YAML + "extra: 1\n",
        "two documents": TINY_YAML + "---\nx: 1\n",
        "hex integer": sub("  n: 2\n", "  n: 0x2\n"),
    }
    for what, text in yaml_cases.items():
        t.ok(text != TINY_YAML, f"case {what} did not change the text")
        refuses(text, None, what)
    twin_cases = {
        "twin side changed": good_json.replace('"5/2"', '"5/3"', 1),
        "twin n as string": good_json.replace('"n": 2', '"n": "2"'),
        "twin float": good_json.replace('"n": 2', '"n": 2.0'),
        "twin NaN": good_json.replace('"n": 2', '"n": NaN'),
        "twin bool": good_json.replace('"n": 2', '"n": true'),
        "twin duplicate key": good_json.replace('"n": 2', '"n": 2, "n": 2'),
        "twin extra key": good_json.replace('"n": 2', '"n": 2, "x": "y"'),
        "twin missing key": good_json.replace('"n": 2, ', ""),
        "twin coordinate changed": good_json.replace('"3/2"', '"3/4"', 1),
        "twin not JSON": good_json[:-1],
    }
    for what, text in twin_cases.items():
        t.ok(text != good_json, f"case {what} did not change the twin")
        refuses(TINY_YAML, text, what)


def run_suite() -> Tally:
    t = Tally()
    rng = random.Random(959_108)
    contact_cases(t)
    overlap_cases(t)
    wall_cases(t)
    refuse_shapes(t)
    random_closing(t, rng, 400)
    random_general(t, rng, 300)
    random_walls(t, rng, 300)
    reader_cases(t)
    return t


def with_patch(module: Any, name: str, replacement: Callable[..., Any]) -> Tally:
    original = getattr(module, name)
    setattr(module, name, replacement)
    try:
        return run_suite()
    finally:
        setattr(module, name, original)


def broken_classify(value: Any) -> str:
    """Method A broken: a zero margin counted as clear."""
    return "clear" if value >= 0 else "overlap"


def broken_clip(poly: list[clipm.FPoint], h: clipm.HalfPlane) -> list[clipm.FPoint]:
    """Method B broken: open half-planes, boundary points dropped."""
    out: list[clipm.FPoint] = []
    m = len(poly)
    for k in range(m):
        p, q = poly[k], poly[(k + 1) % m]
        vp, vq = clipm._value(h, p), clipm._value(h, q)  # noqa: SLF001
        if vp > 0:
            out.append(p)
        if (vp > 0 > vq) or (vp < 0 < vq):
            s = vp / (vp - vq)
            out.append((p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1])))
    return out


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    good = run_suite()
    broken_a = with_patch(satm, "classify", broken_classify)
    broken_b = with_patch(clipm, "clip", broken_clip)
    receipt = {
        "program": "l108_selftest.py",
        "lane": "L108",
        "python": sys.version.split()[0],
        "cases": good.cases,
        "failures": good.failures[:50],
        "failure_count": len(good.failures),
        "broken_method_a_zero_margin_clear": {"cases": broken_a.cases, "failure_count": len(broken_a.failures), "first": broken_a.failures[:3]},
        "broken_method_b_open_half_planes": {"cases": broken_b.cases, "failure_count": len(broken_b.failures), "first": broken_b.failures[:3]},
        "verdict": "PASSED" if not good.failures and broken_a.failures and broken_b.failures else "FAILED",
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    Path(argv[1]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(receipt["verdict"], good.cases, "cases,", len(good.failures), "failed; broken A fails", len(broken_a.failures), "; broken B fails", len(broken_b.failures))
    for f in good.failures[:10]:
        print("  ", f)
    return 0 if receipt["verdict"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
