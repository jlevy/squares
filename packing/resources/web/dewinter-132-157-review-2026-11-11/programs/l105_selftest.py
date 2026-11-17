"""Lane L105's self-test of the reader and both methods.

Usage: python -I -B l105_selftest.py OUT_JSON [--mutant A0|Bopen]

Hand cases with outcomes derived by hand, random exact closing moves, random wall
moves, malformed files the reader must refuse, and two small packings through
`l105_check.decide`. With --mutant it runs against a deliberately broken method
(A0: method A counts a zero margin as apart; Bopen: method B clips with open
half-planes) and is expected to fail.
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l105_check as K  # noqa: E402
import l105_clip as B  # noqa: E402
import l105_geom as G  # noqa: E402
import l105_reader as R  # noqa: E402
import l105_sat as A  # noqa: E402

EPS = F(1, 10**30)
cases: list[dict[str, Any]] = []


def record(name: str, ok: bool, detail: str = "") -> None:
    cases.append({"case": name, "ok": bool(ok), "detail": detail})


def pair_both(si: G.Sq, sj: G.Sq) -> tuple[F, str, str, F]:
    m, _ = A.margin(A.build(si), A.build(sj))
    pi, pj = B.ccw(B.corners(si)), B.ccw(B.corners(sj))
    cb, ar = B.pair_class(pi, pj)
    cb2, ar2 = B.pair_class(pj, pi)
    assert cb == cb2 and ar == ar2, (cb, cb2, ar, ar2)
    return m, A.classify(m), cb, F(int(ar.numerator), int(ar.denominator))


def expect_pair(name: str, si: G.Sq, sj: G.Sq, cls: str, margin: F | None = None, area: F | None = None) -> None:
    m, ca, cb, ar = pair_both(si, sj)
    ok = ca == cls and cb == cls
    if margin is not None:
        ok = ok and m == margin
    if area is not None:
        ok = ok and ar == area
    record(name, ok, f"A={ca} m={K.sci(m)} B={cb} area={K.sci(ar)}")


def transpose(s: G.Sq) -> G.Sq:
    x, y, c, si = G.unpack(s)
    return G.sq(y, x, si, c)


def flip_order(s: G.Sq) -> G.Sq:
    """The same square described from another edge: (c, s) -> (-s, c)."""
    x, y, c, si = G.unpack(s)
    return G.sq(x, y, -si, c)


def hand_pairs() -> None:
    z, one, half = F(0), F(1), F(1, 2)
    a0 = G.sq(z, z, one, z)
    # Closing along the centre line d moves B to (1 - eps) d, so the overlap is the
    # rectangle (1 - |x'|)(1 - |y'|): eps for d = (1, 0); eps (2 + eps) / 3 for
    # d = (1, 1/3); eps^2 for d = (1, 1).
    variants = {
        "edge": (G.sq(one, z, one, z), EPS),
        "edge-offset": (G.sq(one, F(1, 3), one, z), EPS * (2 + EPS) / 3),
        "corner": (G.sq(one, one, one, z), EPS * EPS),
    }
    for nm, (b, area) in variants.items():
        for tag, f in (("as-is", lambda s: s), ("transposed", transpose), ("other-edge", flip_order)):
            ai, bj = f(a0), f(b)
            expect_pair(f"{nm} contact {tag}", ai, bj, "contact", F(0), F(0))
            expect_pair(f"{nm} contact swapped {tag}", bj, ai, "contact", F(0), F(0))
            apart = G.close_pair(ai, bj, EPS)
            past = G.close_pair(ai, bj, -EPS)
            expect_pair(f"{nm} 1e-30 apart {tag}", ai, apart, "apart", EPS)
            expect_pair(f"{nm} 1e-30 past {tag}", ai, past, "overlap", -EPS, area)
    # 3-4-5 vertex on an edge: B turned by (4/5, 3/5), half-extent 7/10 along y; its
    # lowest corner is at (-1/10, 1/2) on A's top edge. Past by eps: a triangle of
    # area (1/2) eps * eps (4/3 + 3/4) = (25/24) eps^2.
    c, s = F(4, 5), F(3, 5)
    for tag, f in (("as-is", lambda t: t), ("transposed", transpose), ("other-edge", flip_order)):
        bt = f(G.sq(z, half + F(7, 10), c, s))
        expect_pair(f"3-4-5 vertex contact {tag}", f(a0), bt, "contact", F(0), F(0))
        bp = f(G.sq(z, half + F(7, 10) - EPS, c, s))
        expect_pair(f"3-4-5 vertex past {tag}", f(a0), bp, "overlap", -EPS, F(25, 24) * EPS * EPS)
        ba = f(G.sq(z, half + F(7, 10) + EPS, c, s))
        expect_pair(f"3-4-5 vertex apart {tag}", f(a0), ba, "apart", EPS)
    expect_pair("duplicate", a0, a0, "overlap", F(-1), F(1))
    expect_pair("concentric (3/5,4/5)", a0, G.sq(z, z, F(3, 5), F(4, 5)), "overlap", F(-6, 5), F(5, 6))
    expect_pair("concentric (4/5,3/5)", a0, G.sq(z, z, F(4, 5), F(3, 5)), "overlap", F(-6, 5), F(5, 6))
    # Not unit squares: both methods refuse.
    for nm, (cc, ss) in {
        "basis (1, 1e-30)": (one, EPS),
        "basis (3/5, 4/5 + 1e-30)": (F(3, 5), F(4, 5) + EPS),
        "basis (0, 0)": (z, z),
        "basis (2, 0)": (F(2), z),
        "basis (1/2, 1/2)": (half, half),
        "basis (1 - 1e-30, 0)": (one - EPS, z),
    }.items():
        s0 = G.sq(z, z, cc, ss)
        record(f"not unit: {nm}", (not A.build(s0).unit) and (not B.is_unit_square(B.corners(s0))))
    for nm, (cc, ss) in {"(1,0)": (one, z), "(0,1)": (z, one), "(-1,0)": (-one, z), "(-4/5,3/5)": (F(-4, 5), F(3, 5))}.items():
        s0 = G.sq(F(3), F(7, 2), cc, ss)
        record(f"unit: {nm}", A.build(s0).unit and B.is_unit_square(B.corners(s0)))


def walls_both(s: G.Sq, side: F) -> list[tuple[str, F, str, F]]:
    qa = A.build(s)
    ca = A.clearances(qa, side)
    wb = B.wall_facts(B.ccw(B.corners(s)), B.q(G.rat(side)))
    out = []
    for k in range(4):
        cls_b, clr_b, _ = wb[k]
        out.append((A.wall_class(ca[k]), ca[k], cls_b, F(int(clr_b.numerator), int(clr_b.denominator))))
    return out


def expect_walls(name: str, s: G.Sq, side: F, want: tuple[str, str, str, str], clr: tuple[F | None, ...] = (None,) * 4) -> None:
    got = walls_both(s, side)
    ok = all(g[0] == w and g[2] == w and g[1] == g[3] for g, w in zip(got, want, strict=True))
    ok = ok and all(c is None or g[1] == c for g, c in zip(got, clr, strict=True))
    record(name, ok, str([(g[0], K.sci(g[1]), g[2]) for g in got]))


def hand_walls() -> None:
    z, one, half = F(0), F(1), F(1, 2)
    s = G.sq(half, half, one, z)
    expect_walls("unit box: four contacts", s, one, ("contact",) * 4, (F(0),) * 4)
    expect_walls("box 1+eps: left, bottom contact", s, one + EPS, ("contact", "contact", "inside", "inside"), (F(0), F(0), EPS, EPS))
    expect_walls("left past", G.sq(half - EPS, F(2), one, z), F(4), ("outside", "inside", "inside", "inside"), (-EPS, None, None, None))
    expect_walls("left short", G.sq(half + EPS, F(2), one, z), F(4), ("inside",) * 4, (EPS, None, None, None))
    t = G.sq(F(2), F(4) - F(7, 10), F(4, 5), F(3, 5))
    expect_walls("3-4-5 vertex at top", t, F(4), ("inside", "inside", "inside", "contact"))
    t2 = G.sq(F(2), F(4) - F(7, 10) + EPS, F(4, 5), F(3, 5))
    expect_walls("3-4-5 vertex past top", t2, F(4), ("inside", "inside", "inside", "outside"), (None, None, None, -EPS))
    t3 = G.sq(F(7, 10), F(2), F(-3, 5), F(4, 5))
    expect_walls("3-4-5 vertex at left", t3, F(4), ("contact", "inside", "inside", "inside"), (F(0), None, None, None))
    record("contained: unit box", B.contained(B.ccw(B.corners(s)), B.q((1, 1))))
    record("not contained: past", not B.contained(B.ccw(B.corners(G.sq(half - EPS, half, one, z))), B.q((1, 1))))


def random_pairs(rng: random.Random, count: int) -> None:
    for k in range(count):
        m1, n1 = rng.randint(2, 60), rng.randint(1, 59)
        if m1 == n1:
            m1 += 1
        c1, s1 = G.pythagorean(m1, n1)
        m2, n2 = rng.randint(2, 60), rng.randint(1, 59)
        if m2 == n2:
            m2 += 1
        c2, s2 = G.pythagorean(m2, n2)
        if rng.random() < 0.5:
            s1 = -s1
        if rng.random() < 0.3:
            c2, s2 = F(1), F(0)
        dm, dn = rng.randint(2, 40), rng.randint(1, 39)
        if dm == dn:
            dm += 1
        dx, dy = G.pythagorean(dm, dn)
        if rng.random() < 0.5:
            dx = -dx
        if rng.random() < 0.5:
            dy = -dy
        x0 = F(rng.randint(-1000, 1000), rng.randint(1, 997))
        y0 = F(rng.randint(-1000, 1000), rng.randint(1, 991))
        si = G.sq(x0, y0, c1, s1)
        sj = G.sq(x0 + F(5, 2) * dx, y0 + F(5, 2) * dy, c2, s2)
        for t, cls in ((F(0), "contact"), (EPS, "apart"), (-EPS, "overlap")):
            mv = G.close_pair(si, sj, t)
            m, ca, cb, _ = pair_both(si, mv)
            record(f"random pair {k} t={K.sci(t)}", m == t and ca == cls and cb == cls, f"m={K.sci(m)} A={ca} B={cb}")


def random_walls(rng: random.Random, count: int) -> None:
    side = F(10)
    for k in range(count):
        m1, n1 = rng.randint(2, 60), rng.randint(1, 59)
        if m1 == n1:
            m1 += 1
        c1, s1 = G.pythagorean(m1, n1)
        if rng.random() < 0.5:
            s1 = -s1
        if rng.random() < 0.25:
            c1, s1 = F(1), F(0)
        s0 = G.sq(F(5) + F(rng.randint(-100, 100), 97), F(5) + F(rng.randint(-100, 100), 89), c1, s1)
        wall = ("left", "bottom", "right", "top")[k % 4]
        for t, cls in ((F(0), "contact"), (EPS, "inside"), (-EPS, "outside")):
            mv = G.move_to_wall(s0, wall, side, t)
            got = walls_both(mv, side)[("left", "bottom", "right", "top").index(wall)]
            record(f"random wall {k} {wall} t={K.sci(t)}", got[0] == cls and got[2] == cls and got[1] == t and got[3] == t)


TINY_JSON = (
    '{\n"n": 2,\n"side": "2",\n"square_size": "1",\n"format": "'
    + R.JSON_FORMAT
    + '",\n"squares": [\n["1/2", "1/2", "1", "0"],\n["3/2", "1/2", "1", "0"]\n]\n}\n'
)
TINY_YAML = """witness:
  id: W-tiny
  n: 2
  side: '2'
  square_size: '1'
  representation: center-basis
  scalar:
    kind: rational
  coordinates:
    origin: lower-left
    axes: x-right-y-up
    angle_unit: not-applicable
  squares:
  - id: 1
    center:
    - 1/2
    - 1/2
    basis:
    - '1'
    - '0'
  - id: 2
    center:
    - 3/2
    - 1/2
    basis:
    - '1'
    - '0'
"""


def reader_cases() -> None:
    try:
        js = R.read_json_text(TINY_JSON)
        ym = R.read_yaml_text(TINY_YAML)
        cmp = R.compare(js, ym)
        record("reader accepts tiny JSON and YAML, same packing", cmp["same_packing"] and cmp["squares_with_text_differences"] == 0)
    except R.ReadError as exc:
        record("reader accepts tiny JSON and YAML, same packing", False, str(exc))
    bad_json = {
        "float": (TINY_JSON.replace('"n": 2', '"n": 2.0'), "float"),
        "duplicate key": (TINY_JSON.replace('"n": 2,', '"n": 2,\n"n": 2,'), "duplicate"),
        "extra key": (TINY_JSON.replace('"n": 2,', '"n": 2,\n"x": 1,'), "keys"),
        "missing key": (TINY_JSON.replace('"square_size": "1",\n', ""), "keys"),
        "n mismatch": (TINY_JSON.replace('"n": 2', '"n": 3'), "entries"),
        "side 1/1": (TINY_JSON.replace('"side": "2"', '"side": "2/1"'), "denominator"),
        "minus zero": (TINY_JSON.replace('"1/2", "1/2", "1", "0"', '"1/2", "1/2", "1", "-0"'), "-0"),
        "leading zero": (TINY_JSON.replace('"3/2"', '"03/2"'), "not a rational"),
        "zero denominator": (TINY_JSON.replace('"3/2"', '"3/0"'), "not a rational"),
        "negative denominator": (TINY_JSON.replace('"3/2"', '"3/-2"'), "not a rational"),
        "padded scalar": (TINY_JSON.replace('"3/2"', '" 3/2"'), "not a rational"),
        "decimal point": (TINY_JSON.replace('"3/2"', '"1.5"'), "not a rational"),
        "number not string": (TINY_JSON.replace('"1", "0"]\n]', '1, "0"]\n]'), "not a string"),
        "three items": (TINY_JSON.replace('["3/2", "1/2", "1", "0"]', '["3/2", "1/2", "1"]'), "four items"),
        "format sentence": (TINY_JSON.replace("one edge", "an edge"), "format"),
        "square_size": (TINY_JSON.replace('"square_size": "1"', '"square_size": "2"'), "square_size"),
        "NaN": (TINY_JSON.replace('"n": 2', '"n": NaN'), "constant"),
        "trailing text": (TINY_JSON + "x", "syntax"),
        "zero numerator fraction": (TINY_JSON.replace('"3/2"', '"0/2"'), "not a rational"),
    }
    for nm, (text, why) in bad_json.items():
        try:
            R.read_json_text(text)
            record(f"reader refuses JSON: {nm}", False, "accepted")
        except R.ReadError as exc:
            record(f"reader refuses JSON: {nm}", why in str(exc), str(exc))
    bad_yaml = {
        "anchor": (TINY_YAML.replace("  scalar:\n", "  scalar: &s\n"), "anchor"),
        "anchored scalar reused by alias": (
            TINY_YAML.replace("    - 3/2\n    - 1/2\n", "    - &h 3/2\n    - *h\n"),
            "anchor",
        ),
        "alias": (TINY_YAML.replace("  coordinates:\n    origin: lower-left\n    axes: x-right-y-up\n    angle_unit: not-applicable\n", "  coordinates: *x\n"), "alias"),
        "explicit tag": (TINY_YAML.replace("side: '2'", "side: !!str 2"), "explicit tag"),
        "duplicate key": (TINY_YAML.replace("  n: 2\n", "  n: 2\n  n: 2\n"), "duplicate"),
        "extra key": (TINY_YAML.replace("  n: 2\n", "  n: 2\n  claim: x\n"), "keys"),
        "id out of order": (TINY_YAML.replace("- id: 2", "- id: 3"), "order"),
        "id quoted": (TINY_YAML.replace("- id: 1", "- id: '1'"), "plain integer"),
        "n quoted": (TINY_YAML.replace("  n: 2", "  n: '2'"), "plain integer"),
        "representation": (TINY_YAML.replace("center-basis", "corners"), "representation"),
        "scalar kind": (TINY_YAML.replace("kind: rational", "kind: decimal"), "kind"),
        "origin": (TINY_YAML.replace("lower-left", "container-center"), "origin"),
        "angle unit": (TINY_YAML.replace("not-applicable", "degrees"), "angle_unit"),
        "three-item basis": (TINY_YAML.replace("    - '1'\n    - '0'\n", "    - '1'\n    - '0'\n    - '0'\n", 1), "two items"),
        "plain integer coordinate": (TINY_YAML.replace("    - 3/2\n", "    - 3\n"), "string scalar"),
        "float coordinate": (TINY_YAML.replace("    - 3/2\n", "    - 1.5\n"), "string scalar"),
        "count": (TINY_YAML.replace("  n: 2", "  n: 3"), "entries"),
        "no wrapper": ("\n".join(line[2:] for line in TINY_YAML.splitlines()[1:]) + "\n", "keys"),
        "directive": ("%YAML 1.1\n---\n" + TINY_YAML, "directive"),
        "non-lowest is read": (TINY_YAML.replace("    - 3/2\n", "    - 6/4\n"), None),
    }
    for nm, (text, why) in bad_yaml.items():
        try:
            out = R.read_yaml_text(text)
            if why is None:
                js = R.read_json_text(TINY_JSON)
                cmp = R.compare(js, out)
                record(f"reader: {nm}", out["lowest_terms"] == out["scalars"] - 1 and cmp["same_packing"] and cmp["squares_with_text_differences"] == 1)
            else:
                record(f"reader refuses YAML: {nm}", False, "accepted")
        except R.ReadError as exc:
            record(f"reader refuses YAML: {nm}", why is not None and why in str(exc), str(exc))
    js = R.read_json_text(TINY_JSON)
    ym = R.read_yaml_text(TINY_YAML.replace("    - 3/2\n", "    - 3/2\n", 1).replace("  - id: 2\n    center:\n    - 3/2\n    - 1/2", "  - id: 2\n    center:\n    - 3/2\n    - 1/3"))
    cmp = R.compare(js, ym)
    record("compare: one scalar differs", (not cmp["same_packing"]) and cmp["scalar_difference_count"] == 1, str(cmp["scalar_differences"]))


def packing_cases() -> None:
    def pk(side: F, sqs: list[G.Sq]) -> dict[str, Any]:
        return {"n": len(sqs), "side": G.rat(side), "squares": sqs}

    one, z, h = F(1), F(0), F(1, 2)
    four = [G.sq(h, h, one, z), G.sq(3 * h, h, one, z), G.sq(h, 3 * h, one, z), G.sq(3 * h, 3 * h, one, z)]
    r = K.decide(pk(F(2), four))
    record("2x2 grid: ACCEPT, 6 touching pairs (4 edges, 2 corners), 8 wall contacts", r["verdict"] == "ACCEPT" and len(r["touching_pairs"]) == 6 and len(r["wall_contacts"]) == 8)
    bad = list(four)
    bad[3] = G.sq(3 * h - EPS, 3 * h, one, z)
    r = K.decide(pk(F(2), bad))
    record("2x2 grid, one square moved 1e-30 left: REFUSE, one overlap", r["verdict"] == "REFUSE" and r["overlapping_pair_count"] == 1)
    r = K.decide(pk(F(2) - EPS, four))
    record("2x2 grid in a box 1e-30 short: REFUSE, walls out", r["verdict"] == "REFUSE" and len(r["walls_outside"]) == 4)
    tilt = [G.sq(F(7, 10), F(7, 10), F(3, 5), F(4, 5))]
    r = K.decide(pk(F(7, 5), tilt))
    record("one 3-4-5 square in a box of 7/5: ACCEPT, four contacts", r["verdict"] == "ACCEPT" and len(r["wall_contacts"]) == 4)
    r = K.decide(pk(F(7, 5) - EPS, tilt))
    record("one 3-4-5 square in a box of 7/5 - 1e-30: REFUSE", r["verdict"] == "REFUSE" and len(r["walls_outside"]) == 2)


def main() -> None:
    sys.set_int_max_str_digits(0)
    outp = Path(sys.argv[1])
    mutant = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == "--mutant" else None
    if mutant == "A0":
        A.classify = lambda m: "apart" if m >= 0 else "overlap"  # type: ignore[assignment]
    elif mutant == "Bopen":
        orig = B.clip_halfplane

        def open_clip(poly, a, b, c0):  # type: ignore[no-untyped-def]
            out = orig(poly, a, b, c0)
            return [p for p in out if a * p[0] + b * p[1] + c0 > 0]

        B.clip_halfplane = open_clip  # type: ignore[assignment]
    rng = random.Random(20261111)
    sections = (
        ("hand pairs", hand_pairs),
        ("hand walls", hand_walls),
        ("random pairs", lambda: random_pairs(rng, 400)),
        ("random walls", lambda: random_walls(rng, 300)),
        ("reader", reader_cases),
        ("packings", packing_cases),
    )
    errors = []
    for nm, fn in sections:
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{nm}: {type(exc).__name__}: {exc}")
    failed = [c for c in cases if not c["ok"]]
    status = "PASSED" if not failed and not errors else "FAILED"
    me = {p: hashlib.sha256((HERE / p).read_bytes()).hexdigest() for p in ("l105_selftest.py", "l105_geom.py", "l105_reader.py", "l105_sat.py", "l105_clip.py", "l105_check.py")}
    out = {
        "program": "l105_selftest.py",
        "mutant": mutant,
        "status": status,
        "cases": len(cases),
        "failed": len(failed),
        "errors": errors,
        "failures": failed[:40],
        "program_sha256": me,
        "all_cases": [c["case"] for c in cases] if mutant is None else None,
    }
    outp.write_text(json.dumps(out, indent=1) + "\n")
    print(f"{status} {len(cases)} cases, {len(failed)} failed, {len(errors)} errors" + (f" (mutant {mutant})" if mutant else ""))
    for e in errors:
        print("  error:", e)
    for c in failed[:10]:
        print("  fail:", c["case"], c["detail"])


if __name__ == "__main__":
    main()
