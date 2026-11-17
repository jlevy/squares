"""Lane L117: self-test of both methods and the reader. Decides nothing about #962.

Clean-room code for the stage 4 review of jlevy/squares#962. Every expected value below
is derived by hand or from l117_geom's closed form, which projects centres and
half-widths rather than corners. Two deliberately broken copies must fail it: method A
counting a zero margin as apart, and method B testing points and crossings with open
(strict) inequalities.

Usage: python -I -B l117_selftest.py OUT.json
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l117_check as ck  # noqa: E402
import l117_geom as g  # noqa: E402
import l117_hull as hb  # noqa: E402
import l117_reader as rd  # noqa: E402
import l117_sat as sa  # noqa: E402

E30 = F(1, 10**30)
DELTAS = [E30, F(0), -E30]


class Tally:
    def __init__(self) -> None:
        self.cases = 0
        self.failed: list[str] = []

    def check(self, ok: bool, name: str) -> None:
        self.cases += 1
        if not ok:
            self.failed.append(name)


def cls(d: F) -> str:
    return "apart" if d > 0 else ("contact" if d == 0 else "overlap")


def pair_model(P: list[g.Pt], Q: list[g.Pt]) -> ck.Model:
    return ck.Model((20, 1), [g.to_rat(P), g.to_rat(Q)])


def variants(P: list[g.Pt], Q: list[g.Pt]) -> list[tuple[list[g.Pt], list[g.Pt], str]]:
    """Both squares in both senses, from two starting corners, in both orders."""
    out = []
    for sp in (True, False):
        for sq in (True, False):
            for kp in (0, 3):
                for kq in (0, 3):
                    Pv = P if sp else [P[0], P[3], P[2], P[1]]
                    Qv = Q if sq else [Q[0], Q[3], Q[2], Q[1]]
                    Pv = Pv[kp:] + Pv[:kp]
                    Qv = Qv[kq:] + Qv[:kq]
                    out.append((Pv, Qv, f"sp{sp} sq{sq} kp{kp} kq{kq} PQ"))
                    out.append((Qv, Pv, f"sp{sp} sq{sq} kp{kp} kq{kq} QP"))
    return out


def pair_case(T: Tally, P: list[g.Pt], Q: list[g.Pt], margin: F, area: F | None, name: str) -> None:
    M = pair_model(P, Q)
    ca, cb, m, ar = M.pair(0, 1)
    T.check(m == margin, f"{name}: margin {m} != {margin}")
    T.check(ca == cls(margin), f"{name}: class A {ca}")
    T.check(cb == cls(margin), f"{name}: class B {cb}")
    if area is not None:
        T.check(F(int(ar.numerator), int(ar.denominator)) == area, f"{name}: area {ar} != {area}")


def contact_families(T: Tally) -> None:
    half = F(1, 2)
    up = (F(1), F(0))
    base = F(3)
    for d in DELTAS:
        P = g.square(base + half, base + half, up)
        # edge to edge
        Q = g.square(base + 3 * half + d, base + half, up)
        for Pv, Qv, tag in variants(P, Q):
            pair_case(T, Pv, Qv, d, abs(d) if d < 0 else F(0), f"edge d={d} {tag}")
        # corner to corner
        Q = g.square(base + 3 * half + d, base + 3 * half + d, up)
        for Pv, Qv, tag in variants(P, Q):
            pair_case(T, Pv, Qv, d, d * d if d < 0 else F(0), f"corner d={d} {tag}")
        # 3-4-5 vertex on the top edge
        u = (F(3, 5), F(4, 5))
        w = (-u[1], u[0])
        p0 = (base + half, base + 1 + d)
        Q = [p0, (p0[0] + u[0], p0[1] + u[1]), (p0[0] + u[0] + w[0], p0[1] + u[1] + w[1]), (p0[0] + w[0], p0[1] + w[1])]
        for Pv, Qv, tag in variants(P, Q):
            pair_case(T, Pv, Qv, d, F(25, 24) * d * d if d < 0 else F(0), f"vertex345 d={d} {tag}")


def deep_overlaps(T: Tally) -> None:
    c = F(7, 2)
    P = g.square(c, c, (F(1), F(0)))
    pair_case(T, P, P, F(-1), F(1), "duplicate")
    pair_case(T, P, P[2:] + P[:2], F(-1), F(1), "duplicate shifted listing")
    for u in ((F(3, 5), F(4, 5)), (F(4, 5), F(3, 5))):
        Q = g.square(c, c, u)
        area = F(2) / (1 + u[0] + u[1])
        pair_case(T, P, Q, F(-6, 5), area, f"concentric {u}")
        pair_case(T, Q, P, F(-6, 5), area, f"concentric {u} QP")


def wall_case(T: Tally, S: F, pts: list[g.Pt], wall: str, clear: F, name: str) -> None:
    M = ck.Model((S.numerator, S.denominator), [g.to_rat(pts)])
    cl, ca, cb, cin = M.walls(0)
    exp = "apart" if clear > 0 else ("contact" if clear == 0 else "outside")
    T.check(cl[wall] == clear, f"{name}: clearance {cl[wall]} != {clear}")
    T.check(ca[wall] == exp, f"{name}: A {ca[wall]}")
    T.check(cb[wall] == exp, f"{name}: B {cb[wall]}")
    for other in ("left", "bottom", "right", "top"):
        if other != wall:
            T.check(ca[other] == "apart" and cb[other] == "apart", f"{name}: other wall {other}")
    T.check(cin, f"{name}: centre outside")


def walls(T: Tally) -> None:
    S = F(5)
    half = F(1, 2)
    up = (F(1), F(0))
    for d in DELTAS:
        cases = {
            "left": g.square(half + d, F(5, 2), up),
            "right": g.square(S - half - d, F(5, 2), up),
            "bottom": g.square(F(5, 2), half + d, up),
            "top": g.square(F(5, 2), S - half - d, up),
        }
        for wall, pts in cases.items():
            for ccw in (True, False):
                for start in (0, 2):
                    v = pts if ccw else [pts[0], pts[3], pts[2], pts[1]]
                    v = v[start:] + v[:start]
                    wall_case(T, S, v, wall, d, f"wall {wall} d={d} ccw{ccw} s{start}")
        # 3-4-5 square with its top vertex at the top wall
        u = (F(3, 5), F(4, 5))
        top = g.square(F(5, 2), F(0), u)
        ymax = max(p[1] for p in top)
        pts = g.shift(top, F(0), S - d - ymax)
        wall_case(T, S, pts, "top", d, f"wall top 345 d={d}")
        wall_case(T, S, list(reversed(pts)), "top", d, f"wall top 345 reversed d={d}")


def malformed(T: Tally) -> None:
    e = E30
    shapes = {
        "rhombus 3-4-5": [(F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "bowtie order": [(F(0), F(0)), (F(1), F(0)), (F(0), F(1)), (F(1), F(1))],
        "rectangle 1 x (1+e)": [(F(0), F(0)), (F(1), F(0)), (F(1), 1 + e), (F(0), 1 + e)],
        "corner off by e": [(F(0), F(0)), (F(1), F(0)), (1 + e, F(1)), (F(0), F(1))],
        "square of side 2": [(F(0), F(0)), (F(2), F(0)), (F(2), F(2)), (F(0), F(2))],
        "a point": [(F(1), F(1))] * 4,
        "tilted, corner off by e": None,
        "kite with unit sides": [(F(0), F(0)), (F(1), F(0)), (F(1) + F(3, 5), F(4, 5)), (F(3, 5), F(4, 5))],
        "three corners right, fourth wrong": [(F(0), F(0)), (F(1), F(0)), (F(1), F(1)), (e, F(1))],
    }
    t = g.square(F(5, 2), F(5, 2), (F(3, 5), F(4, 5)))
    t[2] = (t[2][0] + e, t[2][1])
    shapes["tilted, corner off by e"] = t
    for name, pts in shapes.items():
        assert pts is not None
        shifted = g.shift(pts, F(2), F(2))
        A = sa.SquareA(g.to_rat(shifted))
        sB = hb.unit_sense(hb.to_points(g.to_rat(shifted)))
        T.check(not A.unit, f"malformed {name}: A accepted")
        T.check(sB == 0, f"malformed {name}: B accepted")
        res = ck.decide((10, 1), [g.to_rat(shifted), g.to_rat(g.square(F(8), F(8), (F(1), F(0))))])
        T.check(res["verdict"] == "REFUSE", f"malformed {name}: decide accepted")


def rand_rot(rng: random.Random) -> tuple[F, F]:
    m = rng.randint(2, 40)
    k = rng.randint(1, m - 1)
    c, s = g.pyth(m, k)
    choice = rng.randint(0, 7)
    if choice & 1:
        c, s = s, c
    if choice & 2:
        c = -c
    if choice & 4:
        s = -s
    if rng.random() < 0.15:
        c, s = F(1), F(0)
    return c, s


def rand_centre(rng: random.Random, lo: int, hi: int) -> tuple[F, F]:
    q = rng.randint(1, 10**6)
    return F(rng.randint(lo * q, hi * q), q), F(rng.randint(lo * q, hi * q), q)


def random_pairs(T: Tally, rng: random.Random) -> None:
    done = 0
    while done < 400:
        P = g.square(*rand_centre(rng, 4, 6), rand_rot(rng))
        Q = g.square(*rand_centre(rng, 4, 8), rand_rot(rng))
        if g.closed_margin(P, Q) <= 0:
            continue
        t_star, t_past, _, _ = g.closing(P, Q, E30)
        rate_short = max(ad for ad, h in g.axes_terms(P, Q) if ad > 0 and h / ad == 1 - t_star)
        t_short = t_star - E30 / rate_short
        for t, want in ((t_short, "apart"), (t_star, "contact"), (t_past, "overlap")):
            Qt = g.moved(Q, P, t)
            cm = g.closed_margin(P, Qt)
            M = pair_model(P, Qt)
            ca, cb, m, _ = M.pair(0, 1)
            T.check(m == cm, f"random close {done} {want}: A {m} != closed {cm}")
            T.check(ca == want and cb == want, f"random close {done} {want}: {ca} {cb}")
            if want == "contact":
                T.check(cm == 0, f"random close {done}: closed form not 0")
            if want == "overlap":
                T.check(cm == -E30, f"random close {done}: past margin {cm}")
            if want == "apart":
                T.check(cm == E30, f"random close {done}: short margin {cm}")
        done += 1
    for k in range(300):
        P = g.square(*rand_centre(rng, 4, 6), rand_rot(rng))
        Q = g.square(*rand_centre(rng, 4, 6), rand_rot(rng))
        cm = g.closed_margin(P, Q)
        M = pair_model(P, Q)
        ca, cb, m, ar = M.pair(0, 1)
        T.check(m == cm, f"random any {k}: A {m} != closed {cm}")
        T.check(ca == cb == cls(cm), f"random any {k}: {ca} {cb} {cls(cm)}")
        T.check((ar > 0) == (cm < 0), f"random any {k}: area sign")


def random_walls(T: Tally, rng: random.Random) -> None:
    S = F(9)
    names = ("left", "bottom", "right", "top")
    for k in range(300):
        pts = g.square(*rand_centre(rng, 2, 7), rand_rot(rng))
        wall = names[k % 4]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        clear = {"left": min(xs), "bottom": min(ys), "right": S - max(xs), "top": S - max(ys)}[wall]
        for d in DELTAS:
            mv = clear - d
            dx, dy = {"left": (-mv, F(0)), "right": (mv, F(0)), "bottom": (F(0), -mv), "top": (F(0), mv)}[wall]
            wall_case(T, S, g.shift(pts, dx, dy), wall, d, f"random wall {k} {wall} d={d}")


def reader_cases(T: Tally) -> None:
    def good_yaml(side: str = "'5'") -> str:
        sq = []
        for k, (cx, cy) in enumerate(((F(3, 2), F(3, 2)), (F(7, 2), F(5, 2))), start=1):
            pts = g.square(cx, cy, (F(3, 5), F(4, 5)) if k == 2 else (F(1), F(0)))
            lines = [f"  - id: {k}", "    corners:"]
            for x, y in pts:
                lines.append(f"    - - '{ck.frac_str(x)}'")
                lines.append(f"      - '{ck.frac_str(y)}'")
            sq.append("\n".join(lines))
        return (
            "softschema:\n  contract: packing.squares:Witness/v2\n  schema: witness.schema.yaml\n"
            "  envelope: witness\n  status: enforced\nwitness:\n  id: W-test\n  n: 2\n"
            f"  side: {side}\n  square_size: '1'\n  representation: corners\n  scalar:\n"
            "    kind: rational\n  coordinates:\n    origin: lower-left\n    axes: x-right-y-up\n"
            "    angle_unit: not-applicable\n  squares:\n" + "\n".join(sq) + "\n  claim:\n"
            "    coordinate_provenance: verified\n    method: exact-algebraic\n    limitations: test\n"
        )

    def twin(ytext: str) -> str:
        return json.dumps(rd._strict_yaml(ytext))

    base = good_yaml()
    bj = twin(base)
    try:
        r = rd.read_pair(base, bj)
        T.check(r["n"] == 2, "reader good: n")
        res = ck.decide(r["side"], r["squares"])  # type: ignore[arg-type]
        T.check(res["verdict"] == "ACCEPT", "reader good: decide")
    except rd.ReadRefused as exc:
        T.check(False, f"reader good refused: {exc}")
    plain = good_yaml("33/4")
    try:
        rd.read_pair(plain, twin(plain))
        T.check(True, "reader plain fraction side")
    except rd.ReadRefused as exc:
        T.check(False, f"reader plain fraction refused: {exc}")

    def y_sub(old: str, new: str, count: int = 1) -> str:
        assert old in base, old
        return base.replace(old, new, count)

    yaml_bad = {
        "anchor": (y_sub("kind: rational", "kind: &a rational"), "anchor"),
        "alias": (y_sub("limitations: test", "limitations: *a"), "alias"),
        "explicit str tag": (y_sub("kind: rational", "kind: !!str rational"), "explicit tag"),
        "local tag": (y_sub("kind: rational", "kind: !foo rational"), "explicit tag"),
        "non-specific tag": (y_sub("kind: rational", "kind: ! rational"), "explicit tag"),
        "duplicate key": (y_sub("  n: 2\n", "  n: 2\n  n: 2\n"), "duplicate key"),
        "float n": (y_sub("  n: 2\n", "  n: 2.0\n"), "float"),
        "bool n": (y_sub("  n: 2\n", "  n: true\n"), "bool"),
        "null source": (y_sub("  claim:\n", "  source:\n  claim:\n"), "null"),
        "hex n": (y_sub("  n: 2\n", "  n: 0x2\n"), "plain decimal"),
        "negative n": (y_sub("  n: 2\n", "  n: -2\n"), "plain decimal"),
        "n zero": (y_sub("  n: 2\n", "  n: 0\n"), "n not a positive integer"),
        "unquoted coordinate": (y_sub("- - '1'", "- - 1"), "not a string"),
        "not lowest terms": (y_sub("side: '5'", "side: '10/2'"), "lowest terms"),
        "denominator 1": (y_sub("side: '5'", "side: '5/1'"), "denominator 1"),
        "negative zero": (y_sub("- - '1'", "- - '-0'"), "negative zero"),
        "leading zero": (y_sub("side: '5'", "side: '05'"), "not canonical"),
        "plus sign": (y_sub("side: '5'", "side: '+5'"), "not canonical"),
        "space": (y_sub("side: '5'", "side: '5 '"), "not canonical"),
        "decimal": (y_sub("side: '5'", "side: '5.0'"), "not canonical"),
        "zero denominator": (y_sub("side: '5'", "side: '5/0'"), "not canonical"),
        "negative denominator": (y_sub("side: '5'", "side: '5/-1'"), "not canonical"),
        "zero over q": (y_sub("- - '1'", "- - '0/3'"), "lowest terms"),
        "ids swapped": (y_sub("- id: 1", "- id: 9").replace("- id: 2", "- id: 1").replace("- id: 9", "- id: 2"), "id"),
        "id as string": (y_sub("- id: 1", "- id: '1'"), "id"),
        "extra witness key": (y_sub("  claim:\n", "  extra: x\n  claim:\n"), "outside the schema"),
        "missing claim": (base.split("  claim:\n")[0], "missing"),
        "square extra key": (y_sub("    corners:", "    center: x\n    corners:"), "keys"),
        "representation": (y_sub("representation: corners", "representation: center-angle"), "representation"),
        "scalar kind": (y_sub("kind: rational", "kind: decimal"), "scalar kind"),
        "scalar extra key": (y_sub("    kind: rational\n", "    kind: rational\n    extra: x\n"), "scalar kind"),
        "origin": (y_sub("origin: lower-left", "origin: container-center"), "coordinates"),
        "axes": (y_sub("axes: x-right-y-up", "axes: x-right-y-down"), "coordinates"),
        "angle unit": (y_sub("angle_unit: not-applicable", "angle_unit: degrees"), "coordinates"),
        "square size 2": (y_sub("square_size: '1'", "square_size: '2'"), "square_size"),
        "square size int": (y_sub("square_size: '1'", "square_size: 1"), "square_size"),
        "contract": (y_sub("Witness/v2", "Witness/v3"), "contract"),
        "envelope": (y_sub("envelope: witness", "envelope: other"), "envelope"),
        "top-level extra": (base + "extra: x\n", "top-level keys"),
        "side zero": (y_sub("side: '5'", "side: '0'"), "side not positive"),
        "side negative": (y_sub("side: '5'", "side: '-5'"), "side not positive"),
        "two documents": (base + "---\na: b\n", "yaml compose"),
        "empty": ("", "empty yaml"),
        "list at top": ("- a\n- b\n", "top level not a mapping"),
        "integer key": (y_sub("  claim:\n", "  1: x\n  claim:\n"), "mapping key"),
        "syntax error": (base + "  bad: [\n", "yaml syntax"),
    }
    # structural edits on the tree
    tree = rd._strict_yaml(base)
    assert isinstance(tree, dict)

    def edited(fn: object) -> str:
        t = json.loads(json.dumps(tree))
        fn(t)  # type: ignore[operator]
        return json.dumps(t)

    def drop_square(t: dict) -> None:
        t["witness"]["squares"].pop()

    def extra_square(t: dict) -> None:
        t["witness"]["squares"].append(t["witness"]["squares"][0])

    def three_corners(t: dict) -> None:
        t["witness"]["squares"][0]["corners"].pop()

    def five_corners(t: dict) -> None:
        cs = t["witness"]["squares"][0]["corners"]
        cs.append(cs[0])

    def three_coords(t: dict) -> None:
        t["witness"]["squares"][0]["corners"][0].append("0")

    tree_bad = {
        "missing square": (drop_square, "squares for n"),
        "extra square": (extra_square, "squares for n"),
        "three corners": (three_corners, "corners"),
        "five corners": (five_corners, "corners"),
        "three coordinates": (three_coords, "point"),
    }
    for name, (fn, why) in tree_bad.items():
        txt = edited(fn)  # JSON is YAML; use it as both
        yaml_bad[name] = (txt, why)
    for name, (ytext, why) in yaml_bad.items():
        try:
            jt = json.dumps(rd._strict_yaml(ytext)) if why not in ("anchor", "alias", "explicit tag", "duplicate key", "float", "bool", "null", "plain decimal", "yaml compose", "empty yaml", "mapping key", "yaml syntax") else bj
            rd.read_pair(ytext, jt)
            T.check(False, f"reader accepted: {name}")
        except rd.ReadRefused as exc:
            T.check(why in str(exc), f"reader {name}: refused for {exc!s}, expected {why}")
    jbad = {
        "twin missing": (None, "twin missing"),
        "twin side digit": (bj.replace('"side": "5"', '"side": "6"'), "twin differs"),
        "twin n string": (bj.replace('"n": 2', '"n": "2"'), "twin differs"),
        "twin n float": (bj.replace('"n": 2', '"n": 2.0'), "json float"),
        "twin NaN": (bj.replace('"n": 2', '"n": NaN'), "json constant"),
        "twin duplicate key": (bj.replace('"n": 2', '"n": 2, "n": 2'), "json duplicate key"),
        "twin bool": (bj.replace('"n": 2', '"n": true'), "twin differs"),
        "twin extra key": (bj.replace('"n": 2', '"n": 2, "x": 1'), "twin differs"),
        "twin syntax": (bj[:-1], "json syntax"),
        "twin list order": (bj.replace('"id": 1', '"id": 3'), "twin differs"),
    }
    for name, (jt, why) in jbad.items():
        if jt is not None:
            assert jt != bj, name
        try:
            rd.read_pair(base, jt)
            T.check(False, f"reader accepted: {name}")
        except rd.ReadRefused as exc:
            T.check(why in str(exc), f"reader {name}: refused for {exc!s}, expected {why}")


def geometric(T: Tally) -> None:
    rng = random.Random(20261112)
    contact_families(T)
    deep_overlaps(T)
    walls(T)
    malformed(T)
    random_pairs(T, rng)
    random_walls(T, rng)


def broken_a() -> int:
    saved = (sa.pair_class, sa.wall_class)
    sa.pair_class = lambda m: "apart" if m >= 0 else "overlap"  # type: ignore[assignment]
    sa.wall_class = lambda c: "apart" if c >= 0 else "outside"  # type: ignore[assignment]
    try:
        T = Tally()
        geometric(T)
        return len(T.failed)
    finally:
        sa.pair_class, sa.wall_class = saved


def broken_b() -> int:
    saved = (hb._in_closed, hb._crossings)

    def in_open(p: hb.Pt, poly: list[hb.Pt]) -> bool:
        m = len(poly)
        return all(hb._cross(hb._sub(poly[(k + 1) % m], poly[k]), hb._sub(p, poly[k])) > 0 for k in range(m))

    def crossings_open(P: list[hb.Pt], Q: list[hb.Pt]) -> list[hb.Pt]:
        pts = saved[1](P, Q)
        return [p for p in pts if in_open(p, P) or in_open(p, Q)]

    hb._in_closed = in_open  # type: ignore[assignment]
    hb._crossings = crossings_open  # type: ignore[assignment]
    try:
        T = Tally()
        geometric(T)
        return len(T.failed)
    finally:
        hb._in_closed, hb._crossings = saved


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    T = Tally()
    geometric(T)
    reader_cases(T)
    ba = broken_a()
    bb = broken_b()
    ok = not T.failed and ba > 0 and bb > 0
    out = {
        "program": "l117_selftest.py",
        "verdict": "PASSED" if ok else "FAILED",
        "cases": T.cases,
        "failed": len(T.failed),
        "failures": T.failed[:50],
        "broken_method_A_failures": ba,
        "broken_method_B_failures": bb,
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    with open(argv[1], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(out["verdict"], T.cases, "cases,", len(T.failed), "failed; broken A", ba, "broken B", bb)
    for f in T.failed[:20]:
        print(" FAIL", f)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
