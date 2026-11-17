"""Lane L153 self-test: both methods and the reader against cases with known answers.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

Every expected margin, class and area below is derived by hand from the construction
(`l153_geom`), not by either method. The suite is run three times: against the two
methods as they are (it must pass), and against two deliberately broken copies, method A
counting a zero margin as apart and method B clipping with open half-planes (each must
fail).

Usage: l153_selftest.py OUT.json
"""

from __future__ import annotations

import json
import random
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_clip as B  # noqa: E402
import l153_geom as G  # noqa: E402
import l153_reader as reader  # noqa: E402
import l153_sat as A  # noqa: E402
from gmpy2 import mpq  # noqa: E402

TINY = Fraction(1, 10**30)
DELTAS = (TINY, Fraction(0), -TINY)
F = Fraction


def cls_of(delta: Fraction) -> str:
    return "apart" if delta > 0 else ("contact" if delta == 0 else "overlap")


class Suite:
    def __init__(self, broken_a: bool = False, broken_b: bool = False) -> None:
        self.broken_a = broken_a
        self.broken_b = broken_b
        self.cases = 0
        self.failures: list[str] = []

    def fail(self, what: str) -> None:
        if len(self.failures) < 20:
            self.failures.append(what)
        else:
            self.failures.append("")

    def classify_a(self, m: Fraction) -> str:
        if self.broken_a:
            return "apart" if m >= 0 else "overlap"
        return A.classify(m)

    def pair(self, si: G.FSquare, sj: G.FSquare, margin: Fraction, area: Fraction, what: str) -> None:
        """Both orders, and each square under its four equivalent bases."""
        expected = cls_of(margin)
        variants_i = list(equivalents(si))
        variants_j = list(equivalents(sj))
        for k in range(4):
            a, b = variants_i[k], variants_j[(k + 1) % 4]
            for x, y in ((a, b), (b, a)):
                self.cases += 1
                ex, ey = G.encode(x), G.encode(y)
                px, py = A.prepare(ex), A.prepare(ey)
                if not (A.is_unit(px) and A.is_unit(py)):
                    self.fail(f"{what}: A says not unit")
                    continue
                m = A.margin(px, py)
                if m != margin:
                    self.fail(f"{what}: A margin {m} != {margin}")
                if self.classify_a(m) != expected:
                    self.fail(f"{what}: A class {self.classify_a(m)} != {expected}")
                qx, qy = B.corners(ex), B.corners(ey)
                if not (B.is_unit(qx) and B.is_unit(qy)):
                    self.fail(f"{what}: B says not unit")
                    continue
                cls, ar = B.pair(qx, qy, closed=not self.broken_b)
                if cls != expected:
                    self.fail(f"{what}: B class {cls} != {expected}")
                if F(ar.numerator, ar.denominator) != area:
                    self.fail(f"{what}: B area {ar} != {area}")

    def wall(self, sq: G.FSquare, side: Fraction, name: str, delta: Fraction, what: str) -> None:
        expected = {"apart": "apart", "contact": "contact", "overlap": "crossing"}[cls_of(delta)]
        for variant in equivalents(sq):
            self.cases += 1
            enc = G.encode(variant)
            pa = A.prepare(enc)
            value = A.clearances(pa, side)[name]
            if value != delta:
                self.fail(f"{what}: A clearance {value} != {delta}")
            cls_a = self.classify_a(value)
            cls_a = "crossing" if cls_a == "overlap" else cls_a
            if cls_a != expected:
                self.fail(f"{what}: A wall class {cls_a} != {expected}")
            poly = B.corners(enc)
            cls_b, _ = B.wall(poly, name, mpq(side.numerator, side.denominator), closed=not self.broken_b)
            if cls_b != expected:
                self.fail(f"{what}: B wall class {cls_b} != {expected}")
            inside = B.inside_area(poly, mpq(side.numerator, side.denominator)) == 1
            if inside != (delta >= 0):
                self.fail(f"{what}: B containment {inside} with delta {delta}")

    def refuse(self, sq: G.FSquare, what: str) -> None:
        self.cases += 1
        enc = G.encode(sq)
        if A.is_unit(A.prepare(enc)):
            self.fail(f"{what}: A accepts a non-unit square")
        if B.is_unit(B.corners(enc)):
            self.fail(f"{what}: B accepts a non-unit square")


def equivalents(sq: G.FSquare):
    """The same square under its four edge directions u, v, -u, -v."""
    cx, cy, c, s = sq
    for _ in range(4):
        yield (cx, cy, c, s)
        c, s = -s, c


def fixed_cases(suite: Suite) -> None:
    upright = (F(5, 2), F(7, 3), F(1), F(0))
    tilted345 = (F(5, 2), F(7, 3), F(3, 5), F(4, 5))
    for normal_index in (0, 1):
        for sign in (1, -1):
            for delta in DELTAS:
                tau = F(1, 3)
                j = G.side_by_side(upright, normal_index, sign, 0, tau, delta)
                area = abs(delta) * (1 - tau) if delta < 0 else F(0)
                suite.pair(upright, j, delta, area, f"edge-edge upright n{normal_index}{sign} d{delta}")
                j = G.side_by_side(tilted345, normal_index, sign, 1, -tau, delta)
                area = abs(delta) * (1 - tau) if delta < 0 else F(0)
                suite.pair(tilted345, j, delta, area, f"edge-edge 3-4-5 n{normal_index}{sign} d{delta}")
                # corner to corner: offset (1 + delta) along n and along the tangent
                j = G.side_by_side(upright, normal_index, sign, 0, 1 + delta, delta)
                area = delta * delta if delta < 0 else F(0)
                suite.pair(upright, j, delta, area, f"corner-corner n{normal_index}{sign} d{delta}")
                # 3-4-5 vertex on an upright edge, and an upright vertex... (j tilted)
                j, factor = G.vertex_on_edge(upright, normal_index, sign, (F(3, 5), F(4, 5)), F(1, 7), delta)
                if factor != F(25, 24):
                    suite.fail("3-4-5 area factor is not 25/24")
                area = factor * delta * delta if delta < 0 else F(0)
                suite.pair(upright, j, delta, area, f"vertex-edge 3-4-5 n{normal_index}{sign} d{delta}")
    # duplicates and concentric rotations
    suite.pair(upright, upright, F(-1), F(1), "duplicate upright")
    suite.pair(tilted345, tilted345, F(-1), F(1), "duplicate 3-4-5")
    for c, s in ((F(3, 5), F(4, 5)), (F(4, 5), F(3, 5))):
        turned = (upright[0], upright[1], c, s)
        # gap -1/2 - (c + s)/2 on every axis; area 1 - (c + s - 1)^2 / (2 c s)
        suite.pair(upright, turned, -(1 + c + s) / 2, 1 - (c + s - 1) ** 2 / (2 * c * s), f"concentric {c},{s}")
    # walls
    side = F(10)
    for basis in ((F(1), F(0)), (F(3, 5), F(4, 5)), (F(-5, 13), F(12, 13))):
        c, s = basis
        h = (abs(c) + abs(s)) / 2
        for delta in DELTAS:
            mid = F(37, 7)
            suite.wall((delta + h, mid, c, s), side, "left", delta, f"left {basis} {delta}")
            suite.wall((side - delta - h, mid, c, s), side, "right", delta, f"right {basis} {delta}")
            suite.wall((mid, delta + h, c, s), side, "bottom", delta, f"bottom {basis} {delta}")
            suite.wall((mid, side - delta - h, c, s), side, "top", delta, f"top {basis} {delta}")
    # shapes both methods must refuse
    suite.refuse((F(1), F(1), F(3, 5), F(4, 5) + TINY), "sin off by 1e-30")
    suite.refuse((F(1), F(1), F(3, 5) - TINY, F(4, 5)), "cos off by 1e-30")
    suite.refuse((F(1), F(1), F(6, 5), F(8, 5)), "side 2")
    suite.refuse((F(1), F(1), F(0), F(0)), "a point")
    suite.refuse((F(1), F(1), F(1), TINY), "upright with sin 1e-30")
    suite.refuse((F(1), F(1), F(1, 2), F(1, 2)), "side sqrt(2)/2")
    suite.refuse((F(1), F(1), F(-1) - TINY, F(0)), "cos -1 - 1e-30")


def big_rational(rng: random.Random, lo: int, hi: int) -> Fraction:
    q = rng.randrange(10**59, 10**61)
    return F(rng.randrange(lo * q, hi * q), q)


def rand_basis(rng: random.Random) -> tuple[Fraction, Fraction]:
    t = F(rng.randrange(-10**9, 10**9), rng.randrange(1, 10**9))
    c, s = G.pyth(t)
    if rng.random() < 0.5:
        c, s = -s, c
    return c, s


def random_cases(suite: Suite, rng: random.Random) -> None:
    for k in range(400):
        ci, si = rand_basis(rng)
        sq_i = (big_rational(rng, 1, 15), big_rational(rng, 1, 15), ci, si)
        basis_j = rand_basis(rng)
        tau = F(rng.randrange(-4 * 10**6, 4 * 10**6), 10**7)
        delta = DELTAS[k % 3]
        try:
            sq_j, factor = G.vertex_on_edge(sq_i, rng.randrange(2), rng.choice((1, -1)), basis_j, tau, delta)
        except ValueError:
            sq_j = G.side_by_side(sq_i, rng.randrange(2), rng.choice((1, -1)), rng.randrange(4), tau, delta)
            area = abs(delta) * (1 - abs(tau)) if delta < 0 else F(0)
            suite.pair(sq_i, sq_j, delta, area, f"random side-by-side {k}")
            continue
        area = factor * delta * delta if delta < 0 else F(0)
        suite.pair(sq_i, sq_j, delta, area, f"random vertex-edge {k}")
    # random pairs: both methods' classes, and A against the closed form of l153_geom
    for k in range(300):
        sq_i = (big_rational(rng, 2, 4), big_rational(rng, 2, 4), *rand_basis(rng))
        sq_j = (big_rational(rng, 2, 4), big_rational(rng, 2, 4), *rand_basis(rng))
        suite.cases += 1
        ei, ej = G.encode(sq_i), G.encode(sq_j)
        m = A.margin(A.prepare(ei), A.prepare(ej))
        if m != G.closed_form_margin(sq_i, sq_j):
            suite.fail(f"random pair {k}: A margin differs from the closed form")
        cls, area = B.pair(B.corners(ei), B.corners(ej), closed=not suite.broken_b)
        if suite.classify_a(m) != cls:
            suite.fail(f"random pair {k}: A {suite.classify_a(m)} B {cls}")
        if (area > 0) != (m < 0):
            suite.fail(f"random pair {k}: area {area} with margin sign {m < 0}")
    # random closings along the centre line: contact and 1e-30 past
    for k in range(200):
        sq_i = (big_rational(rng, 2, 4), big_rational(rng, 2, 4), *rand_basis(rng))
        sq_j = (big_rational(rng, 5, 7), big_rational(rng, 5, 7), *rand_basis(rng))
        info = G.closing(sq_i, sq_j)
        at = G.moved(sq_j, sq_i, info["t"])
        slow = min(info["rates"][b] for b in info["binding"])
        past = G.moved(sq_j, sq_i, info["t"] + TINY / slow)
        expected_past = max(g - (TINY / slow) * info["rates"][lab] for lab, g in info["gaps_at"].items())
        for sq_m, want, what in ((at, F(0), "at"), (past, expected_past, "past")):
            suite.cases += 1
            em, ei = G.encode(sq_m), G.encode(sq_i)
            m = A.margin(A.prepare(ei), A.prepare(em))
            if m != want:
                suite.fail(f"closing {k} {what}: A margin {m} != {want}")
            cls, _ = B.pair(B.corners(ei), B.corners(em), closed=not suite.broken_b)
            if cls != cls_of(want) or suite.classify_a(m) != cls_of(want):
                suite.fail(f"closing {k} {what}: classes A {suite.classify_a(m)} B {cls}")
    # random walls
    side = F(17)
    for k in range(200):
        c, s = rand_basis(rng)
        h = (abs(c) + abs(s)) / 2
        delta = DELTAS[k % 3]
        mid = big_rational(rng, 3, 14)
        suite.wall((delta + h, mid, c, s), side, "left", delta, f"random left {k}")
        suite.wall((side - delta - h, mid, c, s), side, "right", delta, f"random right {k}")
        suite.wall((mid, delta + h, c, s), side, "bottom", delta, f"random bottom {k}")
        suite.wall((mid, side - delta - h, c, s), side, "top", delta, f"random top {k}")


VALID_JSON = (
    '{"n": 2, "side": "5/2", "square_size": "1", "format": "f", "squares": '
    '[["1/2", "1/2", "1", "0"], ["3/2", "3/2", "3/5", "-4/5"]]}'
)
VALID_YAML = """softschema:
  contract: packing.squares:Witness/v2
  schema: s
  envelope: witness
  status: enforced
witness:
  id: W-x
  n: 2
  side: 5/2
  square_size: '1'
  representation: center-basis
  scalar:
    kind: rational
  coordinates:
    origin: lower-left
    axes: x-right-y-up
    angle_unit: not-applicable
  claim:
    coordinate_provenance: verified
    method: exact-algebraic
    limitations: none
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
    - 3/2
    basis:
    - 3/5
    - -4/5
"""


def json_cases() -> list[tuple[str, str]]:
    v = VALID_JSON
    return [
        ("float side", v.replace('"side": "5/2"', '"side": 2.5')),
        ("integer side", v.replace('"side": "5/2"', '"side": 3')),
        ("NaN", v.replace('"side": "5/2"', '"side": NaN')),
        ("duplicate key", v.replace('"format": "f"', '"format": "f", "format": "g"')),
        ("extra key", v.replace('"format": "f"', '"format": "f", "x": 1')),
        ("missing key", v.replace('"format": "f", ', "")),
        ("n too large", v.replace('"n": 2', '"n": 3')),
        ("n as string", v.replace('"n": 2', '"n": "2"')),
        ("n true", v.replace('"n": 2', '"n": true')),
        ("not lowest terms", v.replace('"5/2"', '"10/4"')),
        ("denominator 1", v.replace('"5/2"', '"5/1"')),
        ("leading zero", v.replace('"3/2", "3/2"', '"03/2", "3/2"')),
        ("plus sign", v.replace('"3/5"', '"+3/5"')),
        ("negative denominator", v.replace('"-4/5"', '"4/-5"')),
        ("signed zero", v.replace('"0"]', '"-0"]')),
        ("zero over q", v.replace('"0"]', '"0/5"]')),
        ("decimal scalar", v.replace('"3/5"', '"0.6"')),
        ("space", v.replace('"3/5"', '" 3/5"')),
        ("unicode minus", v.replace('"-4/5"', '"−4/5"')),
        ("number scalar", v.replace('"3/5"', "1")),
        ("three scalars", v.replace('["1/2", "1/2", "1", "0"]', '["1/2", "1/2", "1"]')),
        ("five scalars", v.replace('["1/2", "1/2", "1", "0"]', '["1/2", "1/2", "1", "0", "0"]')),
        ("square size 2", v.replace('"square_size": "1"', '"square_size": "2"')),
        ("zero side", v.replace('"5/2"', '"0"')),
        ("negative side", v.replace('"5/2"', '"-5/2"')),
        ("list top level", "[" + v + "]"),
        ("trailing garbage", v + "x"),
    ]


def yaml_cases() -> list[tuple[str, str]]:
    v = VALID_YAML
    return [
        ("anchor and alias", v.replace("    - 3/2\n    - 3/2", "    - &a 3/2\n    - *a")),
        ("explicit tag", v.replace("side: 5/2", "side: !!str 5/2")),
        ("non-specific tag", v.replace("side: 5/2", "side: ! 5/2")),
        ("duplicate key", v.replace("  n: 2\n", "  n: 2\n  n: 2\n")),
        ("second document", v + "---\nx: 1\n"),
        ("unknown witness key", v.replace("  n: 2\n", "  n: 2\n  extra: 1\n")),
        ("unknown square key", v.replace("  - id: 2\n", "  - id: 2\n    angle: '0'\n")),
        ("id out of order", v.replace("  - id: 2\n", "  - id: 3\n")),
        ("octal id", v.replace("  - id: 2\n", "  - id: 02\n")),
        ("hex n", v.replace("  n: 2\n", "  n: 0x2\n")),
        ("float scalar", v.replace("    - 3/2\n    - 3/2", "    - 1.5\n    - 3/2")),
        ("integer scalar", v.replace("    - '1'\n    - '0'", "    - 1\n    - '0'")),
        ("bool scalar", v.replace("  status: enforced", "  status: true")),
        ("corners representation", v.replace("center-basis", "corners")),
        ("container-center origin", v.replace("lower-left", "container-center")),
        ("decimal kind", v.replace("kind: rational", "kind: decimal")),
        ("wrong contract", v.replace("Witness/v2", "Witness/v1")),
        ("not lowest terms", v.replace("side: 5/2", "side: 10/4")),
        ("missing claim", v.replace("  claim:\n    coordinate_provenance: verified\n    method: exact-algebraic\n    limitations: none\n", "")),
    ]


def reader_cases(suite: Suite) -> None:
    def expect(ok: bool, fn, text: str, what: str) -> None:
        suite.cases += 1
        try:
            fn(text)
        except reader.ReadError:
            if ok:
                suite.fail(f"reader refuses a valid file: {what}")
            return
        if not ok:
            suite.fail(f"reader accepts: {what}")

    expect(True, reader.parse_json_text, VALID_JSON, "valid JSON")
    expect(True, reader.parse_yaml_text, VALID_YAML, "valid YAML")
    for what, text in json_cases():
        if text == VALID_JSON:
            suite.fail(f"JSON case did not change the file: {what}")
        expect(False, reader.parse_json_text, text, what)
    for what, text in yaml_cases():
        if text == VALID_YAML:
            suite.fail(f"YAML case did not change the file: {what}")
        expect(False, reader.parse_yaml_text, text, what)
    # twins
    with tempfile.TemporaryDirectory() as tmp:
        j = Path(tmp) / "c.json"
        y = Path(tmp) / "c.yaml"
        j.write_text(VALID_JSON)
        for what, text, ok in (
            ("twin equal", VALID_YAML, True),
            ("twin side differs", VALID_YAML.replace("side: 5/2", "side: 7/2"), False),
            ("twin basis differs", VALID_YAML.replace("    - -4/5", "    - 4/5"), False),
            ("twin centre differs", VALID_YAML.replace("    - 3/2\n    - 3/2", "    - 3/2\n    - 5/2"), False),
        ):
            y.write_text(text)
            suite.cases += 1
            try:
                reader.read(str(j), str(y))
            except reader.ReadError:
                if ok:
                    suite.fail(f"reader refuses: {what}")
                continue
            if not ok:
                suite.fail(f"reader accepts: {what}")
        y.write_bytes(b"\xff\xfe")
        suite.cases += 1
        try:
            reader.read(str(j), str(y))
            suite.fail("reader accepts a non-UTF-8 twin")
        except reader.ReadError:
            pass


def run(broken_a: bool = False, broken_b: bool = False) -> Suite:
    suite = Suite(broken_a, broken_b)
    fixed_cases(suite)
    random_cases(suite, random.Random(153))
    if not (broken_a or broken_b):
        reader_cases(suite)
    return suite


def main(argv: list[str]) -> int:
    good = run()
    broken_a = run(broken_a=True)
    broken_b = run(broken_b=True)
    passed = not good.failures and broken_a.failures and broken_b.failures
    receipt = {
        "program": "l153_selftest.py",
        "verdict": "PASSED" if passed else "FAILED",
        "cases": good.cases,
        "failures": len(good.failures),
        "failure_examples": [f for f in good.failures if f][:20],
        "broken_a_contact_as_apart": {
            "cases": broken_a.cases,
            "failures": len(broken_a.failures),
            "examples": [f for f in broken_a.failures if f][:3],
        },
        "broken_b_open_half_planes": {
            "cases": broken_b.cases,
            "failures": len(broken_b.failures),
            "examples": [f for f in broken_b.failures if f][:3],
        },
    }
    Path(argv[1]).write_text(json.dumps(receipt, indent=1) + "\n")
    print(receipt["verdict"], good.cases, "cases", len(good.failures), "failed;",
          "broken A fails", len(broken_a.failures), "broken B fails", len(broken_b.failures))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
