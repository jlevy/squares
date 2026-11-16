"""Lane L186: self-test of the reader, both methods and the closed form.

Every expected value is derived by hand in the comments, or is a property that
must hold exactly (a margin equal to the closed form, a closing move landing
exactly on its target). Three deliberately broken copies of the methods must
fail it. It reads no certificate.

Usage: python -I -B l186_selftest.py OUT.json
"""

from __future__ import annotations

import json
import os
import random
import sys
import time
from collections.abc import Callable
from fractions import Fraction as F
from typing import Any

# -I leaves the script's own directory off the module path; these modules are this lane's.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l186_clip as mb  # noqa: E402
import l186_geom as geo  # noqa: E402
import l186_sat as ma  # noqa: E402
from l186_decide import decide  # noqa: E402
from l186_reader import ReadError, Square, Witness, dump_witness_text, read_witness_text  # noqa: E402

EPS = F(1, 10**30)
DIRS = [(F(1), F(0)), (F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17))]


class Tally:
    def __init__(self) -> None:
        self.cases = 0
        self.fail: list[str] = []

    def check(self, ok: bool, label: str) -> None:
        self.cases += 1
        if not ok:
            self.fail.append(label)


def make(cx: F, cy: F, c: F, s: F) -> Square:
    """Counterclockwise unit square with centre (cx, cy) and edge direction (c, s)."""
    ux, uy = c / 2, s / 2
    vx, vy = -s / 2, c / 2
    p0 = (cx - ux - vx, cy - uy - vy)
    p1 = (cx + ux - vx, cy + uy - vy)
    p2 = (cx + ux + vx, cy + uy + vy)
    p3 = (cx - ux + vx, cy - uy + vy)
    return (p0, p1, p2, p3)


def relist(sq: Square, k: int, rev: bool) -> Square:
    p = list(sq)
    if rev:
        p = list(reversed(p))
    p = p[k:] + p[:k]
    return (p[0], p[1], p[2], p[3])


def quarter(sq: Square, times: int) -> Square:
    p = list(sq)
    for _ in range(times):
        p = [(-y, x) for x, y in p]
    return (p[0], p[1], p[2], p[3])


def pair_both(a: Square, b: Square) -> tuple[F, str, Any, bool]:
    m = ma.pair_margin(ma.prepare(a), ma.prepare(b))
    cls, area, agree = mb.pair_class(mb.ccw(mb.to_mpq(a)), mb.ccw(mb.to_mpq(b)))
    return m, cls, area, agree


def expect_pair(t: Tally, a: Square, b: Square, m_exp: F, area_exp: F, label: str) -> None:
    for k in range(4):
        for rev in (False, True):
            aa, bb = relist(a, k, rev), relist(b, (k + 1) % 4, not rev)
            for x, y in ((aa, bb), (bb, aa)):
                m, cls, area, agree = pair_both(x, y)
                t.check(m == m_exp, f"{label} A margin {m} != {m_exp} (k={k} rev={rev})")
                t.check(geo.margin(x, y) == m_exp, f"{label} closed form (k={k} rev={rev})")
                t.check(cls == ma.sign_class(m_exp), f"{label} B class {cls} (k={k} rev={rev})")
                t.check(area == mb.mpq(area_exp.numerator, area_exp.denominator), f"{label} B area {area} != {area_exp}")
                t.check(agree, f"{label} B two ways")


def hand_pairs(t: Tally) -> None:
    deltas = [EPS, F(0), -EPS, F(1, 7), -F(1, 7)]
    for c, s in DIRS:
        u = (c, s)
        v = (-s, c)
        normals = [u, (-u[0], -u[1]), v, (-v[0], -v[1])]
        for ni, nrm in enumerate(normals):
            tang = (-nrm[1], nrm[0])
            for tau in (F(0), F(1, 3)):
                for d in deltas:
                    a = make(F(0), F(0), c, s)
                    off = (nrm[0] * (1 + d) + tang[0] * tau, nrm[1] * (1 + d) + tang[1] * tau)
                    b = make(off[0], off[1], c, s)
                    # edge contact: margin d; overlap area |d| (1 - tau) when d < 0
                    area = -d * (1 - tau) if d < 0 else F(0)
                    for q in range(4):
                        expect_pair(t, quarter(a, q), quarter(b, q), d, area, f"edge dir={c},{s} n={ni} tau={tau} d={d} q={q}")
        for sx in (1, -1):
            for sy in (1, -1):
                for d in deltas:
                    a = make(F(0), F(0), c, s)
                    diag = (sx * u[0] + sy * v[0], sx * u[1] + sy * v[1])
                    b = make(diag[0] * (1 + d), diag[1] * (1 + d), c, s)
                    # corner to corner: margin d; overlap a d-by-d square when d < 0
                    area = d * d if d < 0 else F(0)
                    expect_pair(t, a, b, d, area, f"diag dir={c},{s} {sx},{sy} d={d}")
    # a turned corner on an upright edge: 3-4-5 (area 25/24 d^2) and 5-12-13 (169/120 d^2)
    for (c, s), corner, coef in (
        ((F(3, 5), F(4, 5)), (F(1, 10), F(-7, 10)), F(25, 24)),
        ((F(5, 13), F(12, 13)), (F(7, 26), F(-17, 26)), F(169, 120)),
    ):
        for d in (EPS, F(0), -EPS, -F(1, 1000)):
            a = make(F(0), F(0), F(1), F(0))
            b = make(-corner[0], F(1, 2) - corner[1] + d, c, s)
            area = coef * d * d if d < 0 else F(0)
            for q in range(4):
                expect_pair(t, quarter(a, q), quarter(b, q), d, area, f"corner-on-edge {c},{s} d={d} q={q}")
    # duplicates: margin -1, area 1
    for c, s in DIRS[:3]:
        a = make(F(1, 3), F(2, 7), c, s)
        expect_pair(t, a, a, F(-1), F(1), f"duplicate {c},{s}")
    # concentric: upright against a turned square, margin -(1 + c + s)/2, area 1 - (c + s - 1)^2/(2cs)
    for (c, s), m_exp, area_exp in (
        ((F(3, 5), F(4, 5)), F(-6, 5), F(5, 6)),
        ((F(5, 13), F(12, 13)), F(-15, 13), F(13, 15)),
    ):
        a = make(F(0), F(0), F(1), F(0))
        b = make(F(0), F(0), c, s)
        expect_pair(t, a, b, m_exp, area_exp, f"concentric {c},{s}")


def hand_walls(t: Tally) -> None:
    side = F(10)
    for c, s in DIRS:
        h = (abs(c) + abs(s)) / 2
        for wi, wall in enumerate(("left", "bottom", "right", "top")):
            for d in (EPS, F(0), -EPS):
                # place the square at clearance d from this wall
                cx = cy = F(5)
                if wall == "left":
                    cx = h + d
                elif wall == "bottom":
                    cy = h + d
                elif wall == "right":
                    cx = side - h - d
                else:
                    cy = side - h - d
                for q in range(4):
                    sq = make(cx, cy, c, s)
                    if q:
                        # same square under its other edge directions
                        cc, ss = c, s
                        for _ in range(q):
                            cc, ss = -ss, cc
                        sq = make(cx, cy, cc, ss)
                    for k in range(4):
                        for rev in (False, True):
                            x = relist(sq, k, rev)
                            pa = ma.prepare(x)
                            clr = ma.wall_clearances(pa, side)
                            t.check(clr[wi] == d, f"wall {wall} dir={c},{s} d={d} A {clr[wi]}")
                            t.check(geo.clearances(x, side)[wi] == d, f"wall {wall} closed form")
                            classes, area_in = mb.wall_classes(mb.ccw(mb.to_mpq(x)), mb.mpq(side))
                            exp = "apart" if d > 0 else ("touch" if d == 0 else "cross")
                            t.check(classes[wi] == exp, f"wall {wall} dir={c},{s} d={d} B {classes[wi]}")
                            t.check((area_in == 1) == (d >= 0), f"wall {wall} containment d={d}")


def hand_units(t: Tally) -> None:
    for c, s in DIRS + [(F(-3, 5), F(4, 5)), (F(0), F(1))]:
        sq = make(F(2, 3), F(-5, 7), c, s)
        for k in range(4):
            for rev in (False, True):
                x = relist(sq, k, rev)
                pa = ma.prepare(x)
                okb, senseb = mb.unit_square(mb.to_mpq(x))
                t.check(pa.unit and okb, f"unit {c},{s} k={k} rev={rev}")
                exp = -1 if rev else 1
                t.check(pa.sense == exp and senseb == exp, f"sense {c},{s} k={k} rev={rev}")
    base = make(F(0), F(0), F(3, 5), F(4, 5))
    bad: list[tuple[str, Square]] = []
    p = list(base)
    bad.append(("corner off by 1e-30", ((p[0][0] + EPS, p[0][1]), p[1], p[2], p[3])))
    bad.append(("bowtie order", (p[0], p[2], p[1], p[3])))
    r = ((F(0), F(0)), (F(1), F(0)), (F(8, 5), F(4, 5)), (F(3, 5), F(4, 5)))
    bad.append(("rhombus 1, 3-4-5", r))
    bad.append(("rectangle 1 x (1+1e-30)", ((F(0), F(0)), (F(1), F(0)), (F(1), 1 + EPS), (F(0), 1 + EPS))))
    bad.append(("square of side 2", ((F(0), F(0)), (F(2), F(0)), (F(2), F(2)), (F(0), F(2)))))
    bad.append(("degenerate", ((F(0), F(0)),) * 4))
    bad.append(("three corners repeated", (p[0], p[1], p[2], p[2])))
    for label, sq in bad:
        pa = ma.prepare(sq)
        okb, _ = mb.unit_square(mb.to_mpq(sq))
        t.check(not pa.unit, f"A must refuse {label}")
        t.check(not okb, f"B must refuse {label}")


def pyth(rng: random.Random) -> tuple[F, F]:
    while True:
        m = rng.randint(1, 10**6)
        k = rng.randint(1, 10**6)
        if m != k:
            break
    den = m * m + k * k
    c, s = F(m * m - k * k, den), F(2 * m * k, den)
    if rng.random() < 0.5:
        c, s = s, c
    if rng.random() < 0.5:
        c = -c
    if rng.random() < 0.5:
        s = -s
    return c, s


def random_pairs(t: Tally, rng: random.Random, count: int) -> None:
    for r in range(count):
        c1, s1 = pyth(rng)
        c2, s2 = pyth(rng)
        a = make(F(rng.randint(-10**9, 10**9), 10**9), F(rng.randint(-10**9, 10**9), 10**9), c1, s1)
        b = make(
            F(rng.randint(-3 * 10**9, 3 * 10**9), 10**9),
            F(rng.randint(-3 * 10**9, 3 * 10**9), 10**9),
            c2,
            s2,
        )
        m1 = ma.pair_margin(ma.prepare(a), ma.prepare(b))
        m2 = ma.pair_margin(ma.prepare(b), ma.prepare(a))
        cf = geo.margin(a, b)
        t.check(m1 == m2 == cf, f"random {r}: A {m1} / {m2} closed form {cf}")
        cls, _, agree = mb.pair_class(mb.ccw(mb.to_mpq(a)), mb.ccw(mb.to_mpq(b)))
        t.check(cls == ma.sign_class(m1) and agree, f"random {r}: B {cls} vs A {m1}")
        if geo.centre(a) == geo.centre(b):
            continue
        for target in (EPS, F(0), -EPS):
            moved, _ = geo.close_pair(a, b, target)
            mm = ma.pair_margin(ma.prepare(a), ma.prepare(moved))
            t.check(mm == target, f"random close {r} target {target}: A {mm}")
            t.check(geo.margin(a, moved) == target, f"random close {r}: closed form")
            cls2, _, agree2 = mb.pair_class(mb.ccw(mb.to_mpq(a)), mb.ccw(mb.to_mpq(moved)))
            t.check(cls2 == ma.sign_class(target) and agree2, f"random close {r} target {target}: B {cls2}")


def random_walls(t: Tally, rng: random.Random, count: int) -> None:
    side = F(7)
    for r in range(count):
        c, s = pyth(rng)
        sq = make(F(rng.randint(2 * 10**9, 5 * 10**9), 10**9), F(rng.randint(2 * 10**9, 5 * 10**9), 10**9), c, s)
        clr = geo.clearances(sq, side)
        for wi, wall in enumerate(("left", "bottom", "right", "top")):
            for extra in (-EPS, F(0), EPS):
                moved = geo.to_wall(sq, wall, clr[wi] + extra)
                a = ma.wall_clearances(ma.prepare(moved), side)[wi]
                t.check(a == -extra, f"random wall {r} {wall}: A {a}")
                classes, area_in = mb.wall_classes(mb.ccw(mb.to_mpq(moved)), mb.mpq(side))
                exp = "apart" if -extra > 0 else ("touch" if extra == 0 else "cross")
                t.check(classes[wi] == exp, f"random wall {r} {wall}: B {classes[wi]}")
                t.check((area_in == 1) == (extra <= 0), f"random wall {r} {wall}: containment")


GOOD = """softschema:
  contract: packing.squares:Witness/v2
  schema: witness.schema.yaml
  envelope: witness
  status: enforced
witness:
  id: W-test
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
    - - '1'
      - '0'
    - - '2'
      - '0'
    - - '2'
      - '1'
    - - '1'
      - '1'
  claim:
    coordinate_provenance: reported
    method: exact-algebraic
    limitations: test
"""


def reader_tests(t: Tally) -> None:
    good = GOOD
    try:
        w = read_witness_text(good)
        t.check(w.n == 2 and w.side == 2 and w.squares[1][0] == (F(1), F(0)), "good file values")
        t.check(not w.noncanonical, "good file canonical")
        back = read_witness_text(dump_witness_text(w))
        t.check(back.squares == w.squares and back.side == w.side, "round trip")
    except ReadError as exc:
        t.check(False, f"good file refused: {exc}")
    # a non-canonical but valid side: read, value kept, flagged
    w2 = read_witness_text(good.replace("side: '2'", "side: 4/2"))
    t.check(w2.side == 2 and w2.noncanonical == ["side"], "non-canonical side read and flagged")
    w3 = read_witness_text(good.replace("side: '2'", "side: 2/1"))
    t.check(w3.side == 2 and w3.noncanonical == ["side"], "2/1 read and flagged")
    bad: list[tuple[str, str]] = [
        ("alias", good.replace("  - id: 2\n    corners:", "  - id: 2\n    corners: &a").replace("    limitations: test", "    limitations: *a")),
        ("anchor", good.replace("  n: 2", "  n: &x 2")),
        ("explicit tag", good.replace("  side: '2'", "  side: !!str 2")),
        ("duplicate key", good.replace("  n: 2\n", "  n: 2\n  n: 2\n")),
        ("tab", good.replace("limitations: test", "limitations:\ttest")),
        ("carriage return", good.replace("\n", "\r\n")),
        ("wrong contract", good.replace("Witness/v2", "Witness/v1")),
        ("wrong representation", good.replace("representation: corners", "representation: center-basis")),
        ("container-center origin", good.replace("origin: lower-left", "origin: container-center")),
        ("n too large", good.replace("  n: 2", "  n: 3")),
        ("id order", good.replace("  - id: 2", "  - id: 3")),
        ("plain int corner", good.replace("    - - '2'\n      - '0'", "    - - 2\n      - '0'")),
        ("decimal scalar", good.replace("side: '2'", "side: '2.0'")),
        ("float side", good.replace("side: '2'", "side: 2.0")),
        ("zero denominator", good.replace("side: '2'", "side: 2/0")),
        ("leading zero", good.replace("side: '2'", "side: '02'")),
        ("plus sign", good.replace("side: '2'", "side: '+2'")),
        ("leading zero denominator", good.replace("side: '2'", "side: 4/02")),
        ("space", good.replace("side: '2'", "side: ' 2'")),
        ("three corners", good.replace("    - - '0'\n      - '1'\n  - id: 2", "  - id: 2")),
        ("three coordinates", good.replace("    - - '1'\n      - '1'\n", "    - - '1'\n      - '1'\n      - '1'\n", 1)),
        ("extra key", good.replace("  square_size: '1'", "  square_size: '1'\n  extra: x")),
        ("null scalar", good.replace("side: '2'", "side: null")),
        ("bool scalar", good.replace("side: '2'", "side: true")),
        ("hex int", good.replace("  n: 2", "  n: 0x2")),
        ("two documents", good + "---\nfoo: 1\n"),
        ("square size", good.replace("square_size: '1'", "square_size: '2'")),
        ("zero side", good.replace("side: '2'", "side: '0'")),
        ("missing claim", good.split("  claim:")[0]),
    ]
    for label, text in bad:
        t.check(text != good, f"mutation {label} applied")
        try:
            read_witness_text(text)
            t.check(False, f"reader must refuse {label}")
        except ReadError:
            t.check(True, label)


def whole_files(t: Tally) -> None:
    one, zero, two = F(1), F(0), F(2)
    grid = [
        make(F(1, 2), F(1, 2), one, zero),
        make(F(3, 2), F(1, 2), one, zero),
        make(F(1, 2), F(3, 2), one, zero),
        make(F(3, 2), F(3, 2), one, zero),
    ]
    r = decide(two, grid)
    t.check(r["verdict"] == "ACCEPT", f"grid verdict {r['verdict']}")
    t.check(len(r["pairs"]["touching"]) == 6 and r["walls"]["contact_count"] == 8, "grid contacts")
    r = decide(two - EPS, grid)
    t.check(r["verdict"] == "REFUSE" and len(r["walls"]["crossing"]) == 4, "grid in a box 1e-30 too small")
    r = decide(two, grid[:3] + [grid[0]])
    t.check(r["verdict"] == "REFUSE" and r["pairs"]["overlapping"][0][:3] == [1, 4, "-1"], "grid duplicate")
    # a 3-4-5 square touching all four walls of its box, side (3 + 4)/5
    sq = make(F(7, 10), F(7, 10), F(3, 5), F(4, 5))
    r = decide(F(7, 5), [sq])
    t.check(r["verdict"] == "ACCEPT" and r["walls"]["contact_count"] == 4, "3-4-5 in its box")
    r = decide(F(7, 5) - EPS, [sq])
    t.check(r["verdict"] == "REFUSE" and len(r["walls"]["crossing"]) == 2, "3-4-5 in a box 1e-30 too small")
    w = Witness(n=4, side=two, side_text="2", squares=grid, sha256="", witness_id="W-grid")
    back = read_witness_text(dump_witness_text(w))
    t.check(decide(back.side, back.squares)["digests"] == decide(two, grid)["digests"], "grid written and read back")


def run_all(seed: int = 186) -> Tally:
    t = Tally()
    rng = random.Random(seed)
    hand_pairs(t)
    hand_walls(t)
    hand_units(t)
    random_pairs(t, rng, 300)
    random_walls(t, rng, 100)
    reader_tests(t)
    whole_files(t)
    return t


def broken(name: str, patch: Callable[[], Callable[[], None]]) -> int:
    undo = patch()
    try:
        t = Tally()
        rng = random.Random(7)
        hand_pairs(t)
        hand_walls(t)
        random_pairs(t, rng, 50)
        whole_files(t)
        return len(t.fail)
    finally:
        undo()


def patch_one_sided() -> Callable[[], None]:
    orig = ma.pair_margin

    def only_i(a: ma.SqA, b: ma.SqA) -> F:
        gaps = ma._axis_gaps(a, b)  # pyright: ignore[reportPrivateUsage]
        return max(F(n, d) for n, d in gaps)

    ma.pair_margin = only_i

    def undo() -> None:
        ma.pair_margin = orig

    return undo


def patch_zero_apart() -> Callable[[], None]:
    orig = ma.sign_class

    def zero_apart(v: F) -> str:
        return "apart" if v >= 0 else "overlap"

    ma.sign_class = zero_apart

    def undo() -> None:
        ma.sign_class = orig

    return undo


def patch_open_halfplanes() -> Callable[[], None]:
    orig = mb.clip_halfplane

    def open_clip(poly: list[mb.Pt], a: Any, b: Any, c: Any) -> list[mb.Pt]:
        m = len(poly)
        vals = [a * p[0] + b * p[1] + c for p in poly]
        out: list[mb.Pt] = []
        for k in range(m):
            p, fp = poly[k], vals[k]
            r, fr = poly[(k + 1) % m], vals[(k + 1) % m]
            if fp > 0:
                out.append(p)
            if (fp > 0 and fr < 0) or (fp < 0 and fr > 0):
                tt = fp / (fp - fr)
                out.append((p[0] + (r[0] - p[0]) * tt, p[1] + (r[1] - p[1]) * tt))
        return out

    mb.clip_halfplane = open_clip

    def undo() -> None:
        mb.clip_halfplane = orig

    return undo


def main() -> None:
    out_path = sys.argv[1]
    t0 = time.process_time()
    t = run_all()
    broken_counts = {
        "A with only square i's normals": broken("one-sided", patch_one_sided),
        "A counting a zero margin as apart": broken("zero-apart", patch_zero_apart),
        "B clipping with open half-planes": broken("open", patch_open_halfplanes),
    }
    status = "PASSED" if not t.fail and all(v > 0 for v in broken_counts.values()) else "FAILED"
    rec = {
        "status": status,
        "cases": t.cases,
        "failed": len(t.fail),
        "failures": t.fail[:50],
        "broken_copies_failures": broken_counts,
        "python": sys.version,
        "method_B": mb.version(),
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    with open(out_path, "w") as fh:
        json.dump(rec, fh, indent=1)
        fh.write("\n")
    print(status, t.cases, "cases", len(t.fail), "failed", broken_counts)


if __name__ == "__main__":
    main()
