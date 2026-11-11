"""Hold both methods and the reader to cases whose answers are known by hand.

Usage: python -I -B l101_selftest.py OUT.json

Pairs: edge, corner and 3-4-5 vertex-edge contacts, 1e-30 apart and 1e-30 past, each in
both listing senses, from two starting corners and in both orders; a duplicate; a square
against its concentric rotation by (3/5, 4/5) and (4/5, 3/5). Walls: contact, 1e-30
past, 1e-30 short, a 3-4-5 vertex at the top. Shapes both methods must refuse. Random
rational pairs closed along their centre line to exact contact and 1e-30 either side,
random squares taken to a wall. Malformed files the reader must refuse.
"""

from __future__ import annotations

import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402
from gmpy2 import mpq  # noqa: E402

import l101_clip as clip  # noqa: E402
import l101_geom as geom  # noqa: E402
import l101_reader as reader  # noqa: E402
import l101_sat as sat  # noqa: E402

D = F(1, 10**30)
ZERO = F(0)
RESULTS: list[dict] = []


def record(name: str, ok: bool, detail: object = "") -> None:
    RESULTS.append({"case": name, "ok": bool(ok), "detail": str(detail)[:300]})


def variants(points: list) -> list[tuple[str, list]]:
    """The same square listed counterclockwise and clockwise, from two starting corners."""
    rev = [points[0], points[3], points[2], points[1]]
    return [
        ("as-given", points),
        ("rotated-start", points[1:] + points[:1]),
        ("reversed", rev),
        ("reversed-rotated", rev[1:] + rev[:1]),
    ]


def both_pair(a_pts: list, b_pts: list) -> tuple[str, F, str, mpq]:
    a_a, b_a = sat.make_square(a_pts), sat.make_square(b_pts)
    a_b, b_b = clip.make_square(a_pts), clip.make_square(b_pts)
    assert not isinstance(a_a, str) and not isinstance(b_a, str), (a_a, b_a)
    assert not isinstance(a_b, str) and not isinstance(b_b, str), (a_b, b_b)
    m = sat.pair_margin(a_a, b_a)
    cb, area = clip.pair(a_b, b_b)
    return sat.classify(m), m, cb, area


def check_pair(name: str, a_pts: list, b_pts: list, cls: str, margin: F, area: F) -> None:
    for va, pa in variants(a_pts)[:2]:
        for vb, pb in variants(b_pts):
            for order, (x, y) in (("ab", (pa, pb)), ("ba", (pb, pa))):
                ca, m, cb, ar = both_pair(x, y)
                ok = ca == cls and cb == cls and m == margin and F(int(ar.numerator), int(ar.denominator)) == area
                record(f"pair {name} [{va}/{vb}/{order}]", ok, (ca, m, cb, ar))


def unit_axis(x: F, y: F) -> list:
    return geom.square_from((x, y), (F(1), F(0)))


def tilted(p0: tuple[F, F], u: tuple[F, F], sense: int = 1) -> list:
    return geom.square_from(p0, u, sense)


def centred(cx: F, cy: F, c: F, s: F) -> list:
    h = F(1, 2)
    local = [(-h, -h), (h, -h), (h, h), (-h, h)]
    pts = [(cx + c * x - s * y, cy + s * x + c * y) for x, y in local]
    return geom.to_ints(pts)


def pair_cases() -> None:
    a = unit_axis(ZERO, ZERO)
    check_pair("edge contact", a, unit_axis(F(1), ZERO), "contact", ZERO, ZERO)
    check_pair("edge apart", a, unit_axis(1 + D, ZERO), "clear", D, ZERO)
    check_pair("edge past", a, unit_axis(1 - D, ZERO), "overlap", -D, D)
    check_pair("corner contact", a, unit_axis(F(1), F(1)), "contact", ZERO, ZERO)
    check_pair("corner apart", a, unit_axis(1 + D, 1 + D), "clear", D, ZERO)
    check_pair("corner past", a, unit_axis(1 - D, 1 - D), "overlap", -D, D * D)
    u345 = (F(3, 5), F(4, 5))
    check_pair("3-4-5 vertex contact", a, tilted((F(1, 2), F(1)), u345), "contact", ZERO, ZERO)
    check_pair("3-4-5 vertex apart", a, tilted((F(1, 2), 1 + D), u345), "clear", D, ZERO)
    check_pair("3-4-5 vertex past", a, tilted((F(1, 2), 1 - D), u345), "overlap", -D,
               F(25, 24) * D * D)
    check_pair("duplicate", a, a, "overlap", F(-1), F(1))
    sq = centred(F(1, 2), F(1, 2), F(1), F(0))
    check_pair("concentric (3/5, 4/5)", sq, centred(F(1, 2), F(1, 2), F(3, 5), F(4, 5)),
               "overlap", F(-6, 5), F(5, 6))
    check_pair("concentric (4/5, 3/5)", sq, centred(F(1, 2), F(1, 2), F(4, 5), F(3, 5)),
               "overlap", F(-6, 5), F(5, 6))


def both_wall(points: list, side: F, wall: str) -> tuple[str, F, str, mpq]:
    sa = sat.make_square(points)
    sb = clip.make_square(points)
    assert not isinstance(sa, str) and not isinstance(sb, str)
    c = sat.wall_clearances(sa, side)[wall]
    cb, area = clip.wall(sb, clip.outer_planes(mpq(side.numerator, side.denominator))[wall])
    return sat.wall_class(c), c, cb, area


def check_wall(name: str, points: list, side: F, wall: str, cls: str, clearance: F, area: F) -> None:
    for v, p in variants(points):
        ca, c, cb, ar = both_wall(p, side, wall)
        ok = ca == cls and cb == cls and c == clearance and F(int(ar.numerator), int(ar.denominator)) == area
        record(f"wall {name} [{v}]", ok, (ca, c, cb, ar))


def wall_cases() -> None:
    s = F(3)
    check_wall("left contact", unit_axis(ZERO, F(1)), s, "left", "contact", ZERO, ZERO)
    check_wall("left past", unit_axis(-D, F(1)), s, "left", "outside", -D, D)
    check_wall("left short", unit_axis(D, F(1)), s, "left", "clear", D, ZERO)
    check_wall("bottom contact", unit_axis(F(1), ZERO), s, "bottom", "contact", ZERO, ZERO)
    check_wall("right contact", unit_axis(F(2), F(1)), s, "right", "contact", ZERO, ZERO)
    check_wall("right past", unit_axis(2 + D, F(1)), s, "right", "outside", -D, D)
    check_wall("top contact", unit_axis(F(1), F(2)), s, "top", "contact", ZERO, ZERO)
    u345 = (F(-3, 5), F(-4, 5))  # p0 is the highest corner
    check_wall("3-4-5 top contact", tilted((F(3, 2), s), u345), s, "top", "contact", ZERO, ZERO)
    check_wall("3-4-5 top short", tilted((F(3, 2), s - D), u345), s, "top", "clear", D, ZERO)
    check_wall("3-4-5 top past", tilted((F(3, 2), s + D), u345), s, "top", "outside", -D,
               F(25, 24) * D * D)
    # containment by clipping to the box
    for name, pts, expect in (
        ("inside", unit_axis(F(1), F(1)), F(1)),
        ("half out", unit_axis(F(5, 2), F(1)), F(1, 2)),
    ):
        sb = clip.make_square(pts)
        assert not isinstance(sb, str)
        area = clip.inside_area(sb, mpq(3))
        record(f"containment {name}", F(int(area.numerator), int(area.denominator)) == expect, area)


def shape_cases() -> None:
    o = (ZERO, ZERO)
    unit = unit_axis(ZERO, ZERO)
    fr = geom.to_fracs(unit)
    bad = {
        "rhombus 3-4-5": geom.to_ints([o, (F(1), ZERO), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))]),
        "bowtie order": geom.to_ints([fr[0], fr[2], fr[1], fr[3]]),
        "rectangle 1 x (1 + d)": geom.to_ints([o, (F(1), ZERO), (F(1), 1 + D), (ZERO, 1 + D)]),
        "third corner off by d": geom.to_ints([fr[0], fr[1], (fr[2][0] + D, fr[2][1]), fr[3]]),
        "side 2": geom.to_ints([o, (F(2), ZERO), (F(2), F(2)), (ZERO, F(2))]),
        "one point": geom.to_ints([o, o, o, o]),
        "3-4-5 third corner off by d": (lambda p: geom.to_ints([p[0], p[1], (p[2][0], p[2][1] + D), p[3]]))(
            geom.to_fracs(tilted((F(1), F(1)), (F(3, 5), F(4, 5))))),
    }
    for name, pts in bad.items():
        ra = sat.make_square(pts)
        rb = clip.make_square(pts)
        record(f"refuse shape {name}", isinstance(ra, str) and isinstance(rb, str), (ra, rb))


def pythagorean(rng: random.Random) -> tuple[F, F]:
    m = rng.randint(2, 40)
    n = rng.randint(1, m - 1)
    a, b, c = m * m - n * n, 2 * m * n, m * m + n * n
    x, y = F(a, c), F(b, c)
    if rng.random() < 0.5:
        x, y = y, x
    return (x if rng.random() < 0.5 else -x, y if rng.random() < 0.5 else -y)


def random_pairs(rng: random.Random, count: int) -> None:
    for k in range(count):
        a = tilted((F(rng.randint(0, 10**6), 10**6), F(rng.randint(0, 10**6), 10**6)), pythagorean(rng),
                   rng.choice((1, -1)))
        b = tilted((F(rng.randint(2 * 10**6, 4 * 10**6), 10**6), F(rng.randint(-2 * 10**6, 3 * 10**6), 10**6)),
                   pythagorean(rng), rng.choice((1, -1)))
        info = geom.closing(a, b)
        t = info["t_contact"]
        w = info["w"]
        expect_past = "overlap" if info["active_all_decreasing"] else None
        before = t - (info["t_past"] - t if info["t_past"] is not None else D)
        cases = [("contact", t, "contact"), ("before", before, "clear")]
        if expect_past is not None:
            cases.append(("past", info["t_past"], "overlap"))
        ok = True
        detail = []
        for label, tt, cls in cases:
            moved = geom.moved(b, w, tt)
            ca, m, cb, area = both_pair(a, moved)
            good = ca == cls and cb == cls
            if label == "past":
                good = good and m == -D
            if label == "contact":
                good = good and m == 0 and area == 0
            ok = ok and good
            detail.append((label, ca, cb, float(m)))
        record(f"random pair {k}", ok, detail)


def random_walls(rng: random.Random, count: int) -> None:
    side = F(10)
    for k in range(count):
        p0 = (F(rng.randint(2 * 10**6, 7 * 10**6), 10**6), F(rng.randint(2 * 10**6, 7 * 10**6), 10**6))
        pts = tilted(p0, pythagorean(rng), rng.choice((1, -1)))
        wall = rng.choice(("left", "bottom", "right", "top"))
        sa = sat.make_square(pts)
        assert not isinstance(sa, str)
        c = sat.wall_clearances(sa, side)[wall]
        direction = {"left": (-1, 0), "bottom": (0, -1), "right": (1, 0), "top": (0, 1)}[wall]
        ok = True
        detail = []
        for label, dist, cls in (("at", c, "contact"), ("past", c + D, "outside"), ("short", c - D, "clear")):
            moved = geom.translate(pts, dist * direction[0], dist * direction[1])
            ca, cc, cb, _ = both_wall(moved, side, wall)
            good = ca == cls and cb == cls
            ok = ok and good
            detail.append((label, ca, cb))
        record(f"random wall {k} {wall}", ok, detail)


def base_tree() -> dict:
    sq1 = unit_axis(ZERO, ZERO)
    sq2 = unit_axis(F(1), ZERO)

    def s(r: tuple[int, int]) -> str:
        return str(r[0]) if r[1] == 1 else f"{r[0]}/{r[1]}"

    return {
        "softschema": {"contract": "packing.squares:Witness/v2", "schema": "witness.schema.yaml",
                       "envelope": "witness", "status": "enforced"},
        "witness": {
            "id": "W-test", "n": 2, "side": "5/2", "square_size": "1", "representation": "corners",
            "scalar": {"kind": "rational"},
            "coordinates": {"origin": "lower-left", "axes": "x-right-y-up", "angle_unit": "not-applicable"},
            "squares": [{"id": i + 1, "corners": [[s(x), s(y)] for x, y in sq]} for i, sq in enumerate((sq1, sq2))],
            "claim": {"coordinate_provenance": "verified", "method": "exact-algebraic", "limitations": "test"},
        },
    }


def dump_yaml(tree: dict) -> str:
    return yaml.safe_dump(tree, sort_keys=False, default_flow_style=False, allow_unicode=True)


def reader_cases() -> None:
    import copy  # noqa: PLC0415

    good = base_tree()
    try:
        w = reader.read_texts(dump_yaml(good), json.dumps(good), 2)
        record("reader accepts base", w.side == (5, 2) and len(w.squares) == 2, w.side)
    except reader.ReadError as error:
        record("reader accepts base", False, error)
    try:
        w = reader.read_texts(dump_yaml(good), None, 2)
        record("reader accepts base without twin", w.n == 2)
    except reader.ReadError as error:
        record("reader accepts base without twin", False, error)

    def mutate(fn) -> dict:
        t = copy.deepcopy(good)
        fn(t)
        return t

    def setw(key: str, value: object):
        return lambda t: t["witness"].__setitem__(key, value)

    def setc(idx: int, k: int, axis: int, value: object):
        return lambda t: t["witness"]["squares"][idx]["corners"][k].__setitem__(axis, value)

    tree_mutations = {
        "wrong contract": lambda t: t["softschema"].__setitem__("contract", "packing.squares:Witness/v1"),
        "extra top key": lambda t: t.__setitem__("extra", 1),
        "extra softschema key": lambda t: t["softschema"].__setitem__("x", "y"),
        "missing claim": lambda t: t["witness"].pop("claim"),
        "unknown witness key": setw("note", "x"),
        "n is 3": setw("n", 3),
        "n as string": setw("n", "2"),
        "square_size 2": setw("square_size", "2"),
        "representation center-angle": setw("representation", "center-angle"),
        "scalar kind decimal": setw("scalar", {"kind": "decimal"}),
        "origin container-center": lambda t: t["witness"]["coordinates"].__setitem__("origin", "container-center"),
        "angle unit degrees": lambda t: t["witness"]["coordinates"].__setitem__("angle_unit", "degrees"),
        "side 10/4": setw("side", "10/4"),
        "side 5/1": setw("side", "5/1"),
        "side 0": setw("side", "0"),
        "side negative": setw("side", "-5/2"),
        "side decimal": setw("side", "2.5"),
        "side with plus": setw("side", "+5/2"),
        "side leading zero": setw("side", "05/2"),
        "side minus zero": setw("side", "-0"),
        "side as int": setw("side", 3),
        "one square": lambda t: t["witness"]["squares"].pop(),
        "ids reversed": lambda t: t["witness"]["squares"].reverse(),
        "id repeated": lambda t: t["witness"]["squares"][1].__setitem__("id", 1),
        "id as string": lambda t: t["witness"]["squares"][0].__setitem__("id", "1"),
        "square extra key": lambda t: t["witness"]["squares"][0].__setitem__("angle", "0"),
        "three corners": lambda t: t["witness"]["squares"][0]["corners"].pop(),
        "point of three": lambda t: t["witness"]["squares"][0]["corners"][0].append("0"),
        "corner 2/4": setc(0, 1, 0, "2/4"),
        "corner as int": setc(0, 1, 0, 1),
        "corner denominator zero": setc(0, 1, 0, "1/0"),
        "corner with space": setc(0, 1, 0, "1 "),
    }
    for name, fn in tree_mutations.items():
        t = mutate(fn)
        try:
            reader.read_texts(dump_yaml(t), json.dumps(t), 2)
            record(f"reader refuses {name}", False, "accepted")
        except reader.ReadError as error:
            record(f"reader refuses {name}", True, error)
    text = dump_yaml(good)
    text_mutations = {
        "twin differs in one digit": (text, json.dumps(good).replace('"5/2"', '"7/2"')),
        "twin with float": (text, json.dumps(good).replace('"n": 2', '"n": 2.0')),
        "twin with duplicate key": (text, json.dumps(good).replace('"n": 2', '"n": 2, "n": 2')),
        "twin with true for n": (text, json.dumps(good).replace('"n": 2', '"n": true')),
        "yaml duplicate key": (text.replace("  n: 2\n", "  n: 2\n  n: 2\n"), None),
        "yaml alias": ("a: &x 1\nb: *x\n", None),
        "yaml two documents": (text + "---\n" + text, None),
        "yaml float n": (text.replace("  n: 2\n", "  n: 2.0\n"), None),
        "yaml bool n": (text.replace("  n: 2\n", "  n: true\n"), None),
        "yaml tagged scalar": (text.replace("side: 5/2", "side: !!binary YQ=="), None),
        "yaml octal-looking n": (text.replace("  n: 2\n", "  n: 0o2\n"), None),
        "yaml unquoted 0 scalar": (text.replace("- '0'", "- 0", 1), None),
    }
    for name, (ytext, jtext) in text_mutations.items():
        try:
            reader.read_texts(ytext, jtext, 2)
            record(f"reader refuses {name}", False, "accepted")
        except reader.ReadError as error:
            record(f"reader refuses {name}", True, error)


def main() -> int:
    out = Path(sys.argv[1])
    pair_cases()
    wall_cases()
    shape_cases()
    rng = random.Random(20261111)
    random_pairs(rng, 400)
    random_walls(rng, 300)
    reader_cases()
    failed = [r for r in RESULTS if not r["ok"]]
    receipt = {
        "program": "l101_selftest.py",
        "cases": len(RESULTS),
        "failed": failed,
        "verdict": "PASSED" if not failed else "FAILED",
        "results": RESULTS,
    }
    out.write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(receipt["verdict"], len(RESULTS), "cases,", len(failed), "failed")
    for r in failed[:20]:
        print("FAILED", r)
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
