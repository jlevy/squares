"""Run the controls of controls-plan.json and compare each outcome with its stated rule.

Usage: python -I -B r1038_controls.py CERTIFICATE PLAN_JSON CLAIM_DECIMAL OUT_JSON

Every rule is evaluated exactly over the original certificate's facts by method A, and
compared with what both methods decide on the modified packing. A decision in which the
methods disagree anywhere fails its control. Whole-file controls write the modified
packing as Witness/v2 text with this program's own writer and read it back through the
reader. The receipt gives each control's outcome and whether it came out as stated, and
the program prints EVERY_CONTROL_AS_STATED or SOME_CONTROL_NOT_AS_STATED.
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections.abc import Callable
from decimal import Decimal
from fractions import Fraction
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1038_clip as clip  # noqa: E402
import r1038_decide as decide  # noqa: E402
import r1038_geom as geom  # noqa: E402
import r1038_reader as reader  # noqa: E402
import r1038_sat as sat  # noqa: E402

EPS = Fraction(1, 10**30)
WALLS = decide.WALLS
HEADER = 18
Vec = tuple[Fraction, Fraction]


def canonical(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def write_lines(side_text: str, texts: list[tuple[str, str, str, str]], n: int | None = None) -> list[str]:
    """This program's Witness/v2 writer: a fixed header, seven lines a square, a claim."""
    count = len(texts) if n is None else n
    lines = [
        "softschema:",
        "  contract: packing.squares:Witness/v2",
        "  schema: witness.schema.yaml",
        "  envelope: witness",
        "  status: enforced",
        "witness:",
        "  id: W-r1038-control",
        f"  n: {count}",
        f"  side: '{side_text}'",
        "  square_size: '1'",
        "  representation: center-basis",
        "  scalar:",
        "    kind: rational",
        "  coordinates:",
        "    origin: lower-left",
        "    axes: x-right-y-up",
        "    angle_unit: not-applicable",
        "  squares:",
    ]
    assert len(lines) == HEADER
    for index, (x, y, a, b) in enumerate(texts, start=1):
        lines += [f"  - id: {index}", "    center:", f"    - '{x}'", f"    - '{y}'", "    basis:", f"    - '{a}'", f"    - '{b}'"]
    lines += [
        "  claim:",
        "    coordinate_provenance: reported",
        "    method: exact-algebraic",
        "    limitations: a control copy written by lane r1038's controls program",
    ]
    return lines


def text_of(lines: list[str]) -> str:
    return "\n".join(lines) + "\n"


def line_of(square: int, offset: int) -> int:
    """The index of a square's line: 0 id, 1 center, 2 x, 3 y, 4 basis, 5 a, 6 b."""
    return HEADER + 7 * (square - 1) + offset


class Controls:
    def __init__(self, cert: reader.Certificate, claim: Fraction) -> None:
        self.cert = cert
        self.claim = claim
        self.n = cert.n
        self.side = cert.side
        self.c: list[Vec] = list(cert.centers)
        self.b: list[Vec] = list(cert.bases)
        self.orig = decide.decide(self.side, self.c, self.b)
        self.m = self.orig.margins
        self.cl = self.orig.clear_a
        self.by_square: dict[int, list[tuple[int, Fraction]]] = {k: [] for k in range(1, self.n + 1)}
        for (i, j), value in self.m.items():
            self.by_square[i].append((j, value))
            self.by_square[j].append((i, value))
        self.decides = 1

    # -- writing and reading back -------------------------------------------------------
    def texts_for(self, centers: list[Vec], bases: list[Vec]) -> list[tuple[str, str, str, str]]:
        out = []
        for k in range(len(centers)):
            values = (centers[k][0], centers[k][1], bases[k][0], bases[k][1])
            if k < self.n:
                original = (self.c[k][0], self.c[k][1], self.b[k][0], self.b[k][1])
                written = self.cert.texts[k]
                out.append(tuple(written[q] if values[q] == original[q] else canonical(values[q]) for q in range(4)))
            else:
                out.append(tuple(canonical(v) for v in values))
        return out  # type: ignore[return-value]

    def whole(self, side: Fraction, centers: list[Vec], bases: list[Vec]) -> decide.Decision:
        side_text = self.cert.side_text if side == self.side else canonical(side)
        back = reader.read_text(text_of(write_lines(side_text, self.texts_for(centers, bases))))
        if back.side != side or back.centers != centers or back.bases != bases:
            raise AssertionError("the writer and reader do not round-trip")
        self.decides += 1
        return decide.decide(back.side, back.centers, back.bases)

    @staticmethod
    def overlapping(result: decide.Decision) -> set[tuple[int, int]]:
        return {key for key, value in result.margins.items() if value < 0}

    @staticmethod
    def crossings(result: decide.Decision) -> set[tuple[int, int]]:
        return {(k, w) for k, values in enumerate(result.clear_a, start=1) for w, v in enumerate(values) if v < 0}

    @staticmethod
    def contacts(result: decide.Decision) -> set[tuple[int, int]]:
        return {(k, w) for k, values in enumerate(result.clear_a, start=1) for w, v in enumerate(values) if v == 0}

    # -- C0 and the reader --------------------------------------------------------------
    def c0(self) -> tuple[bool, dict[str, Any]]:
        mismatches = 0
        for (i, j), value in self.m.items():
            if geom.corner_margin(self.c[i - 1], self.b[i - 1], self.c[j - 1], self.b[j - 1]) != value:
                mismatches += 1
        for k in range(self.n):
            if geom.corner_clearances(self.c[k], self.b[k], self.side) != self.cl[k]:
                mismatches += 1
        return mismatches == 0, {"pairs": len(self.m), "squares": self.n, "mismatches": mismatches}

    def base_lines(self) -> list[str]:
        return write_lines(self.cert.side_text, list(self.cert.texts))

    def refused(self, lines: list[str], needle: str) -> tuple[bool, dict[str, Any]]:
        try:
            reader.read_text(text_of(lines))
        except reader.ReadRefused as error:
            return needle in str(error), {"refused": str(error)}
        return False, {"refused": None}

    def r1(self) -> tuple[bool, dict[str, Any]]:
        lines = write_lines(self.cert.side_text, list(self.cert.texts[:-1]), n=self.n)
        return self.refused(lines, "squares are listed")

    def r2(self) -> tuple[bool, dict[str, Any]]:
        p, q = self.side.numerator, self.side.denominator
        lines = self.base_lines()
        lines[8] = f"  side: '{2 * p}/{2 * q}'"
        back = reader.read_text(text_of(lines))
        same = back.side == self.side and back.centers == self.c and back.bases == self.b
        expected = sorted(set(self.cert.noncanonical) | {"side"})
        ok = same and sorted(back.noncanonical) == expected
        return ok, {"values_equal": same, "noncanonical": back.noncanonical[:10]}

    def r3(self) -> tuple[bool, dict[str, Any]]:
        lines = self.base_lines()
        lines[line_of(1, 0)] = "  - id: 2"
        lines[line_of(2, 0)] = "  - id: 1"
        return self.refused(lines, "out of order")

    def r4(self) -> tuple[bool, dict[str, Any]]:
        lines = self.base_lines()
        lines[8] = f"  side: {decide.fixed(self.side, 40)}"
        return self.refused(lines, "float")

    def r5(self) -> tuple[bool, dict[str, Any]]:
        lines = self.base_lines()
        lines[line_of(1, 2)] = f"    - '+{self.cert.texts[0][0]}'"
        return self.refused(lines, "is not p or p/q")

    def r6(self) -> tuple[bool, dict[str, Any]]:
        lines = self.base_lines()
        lines.insert(line_of(1, 6) + 1, "    - '0'")
        return self.refused(lines, "not a list of two scalars")

    def r7(self) -> tuple[bool, dict[str, Any]]:
        lines = self.base_lines()
        lines.insert(9, lines[8])
        return self.refused(lines, "twice")

    def r8(self) -> tuple[bool, dict[str, Any]]:
        lines = self.base_lines()
        lines[line_of(1, 1)] = "    center: &c1"
        start = line_of(2, 1)
        lines[start : start + 3] = ["    center: *c1"]
        return self.refused(lines, "an anchor")

    def r9(self) -> tuple[bool, dict[str, Any]]:
        lines = self.base_lines()
        lines[10] = "  representation: corners"
        return self.refused(lines, "not center-basis")

    # -- geometry -------------------------------------------------------------------------
    def g1(self) -> tuple[bool, dict[str, Any]]:
        n = self.n
        centers, bases = list(self.c), list(self.b)
        centers[n - 1], bases[n - 1] = self.c[0], self.b[0]
        result = self.whole(self.side, centers, bases)
        expected: dict[tuple[int, int], Fraction] = {}
        for (i, j), value in self.m.items():
            if j != n:
                expected[(i, j)] = value
        expected[(1, n)] = Fraction(-1)
        for k in range(2, n):
            expected[(k, n)] = self.m[(1, k)]
        clears = [list(v) for v in self.cl]
        clears[n - 1] = list(self.cl[0])
        over = {(1, n)} | {(k, n) for k in range(2, n) if self.m[(1, k)] < 0}
        over |= {key for key in self.overlapping(self.orig) if n not in key}
        ok = (
            result.verdict == "REFUSE"
            and result.margins == expected
            and result.clear_a == clears
            and self.overlapping(result) == over
            and result.pair_b[(1, n)] == ("overlap", Fraction(1))
            and not result.disagreements
        )
        return ok, {"verdict": result.verdict, "overlapping": sorted(self.overlapping(result))[:10], "area_1n_B": str(result.pair_b[(1, n)][1])}

    def g2(self) -> tuple[bool, dict[str, Any]]:
        centers = list(self.c)
        centers[0] = (self.c[0][0] + self.side, self.c[0][1])
        result = self.whole(self.side, centers, self.b)
        left, bottom, right, top = self.cl[0]
        clears = [list(v) for v in self.cl]
        clears[0] = [left + self.side, bottom, right - self.side, top]
        cross = {(1, 2)} | {key for key in self.crossings(self.orig) if key[0] != 1}
        unchanged = all(result.margins[key] == value for key, value in self.m.items() if 1 not in key)
        area_ok = result.inside_b[0] == 0 if left >= 0 else True
        ok = (
            result.verdict == "REFUSE"
            and result.clear_a == clears
            and self.crossings(result) == cross
            and area_ok
            and self.overlapping(result) == {key for key in self.overlapping(self.orig) if 1 not in key}
            and unchanged
            and not result.disagreements
        )
        return ok, {"verdict": result.verdict, "crossings": sorted(self.crossings(result))[:10], "right_clearance_1": decide.decimal(clears[0][2]), "inside_area_1_B": str(result.inside_b[0])}

    def g3(self) -> tuple[bool, dict[str, Any]]:
        bases = list(self.b)
        bases[0] = (self.b[0][0] + EPS, self.b[0][1])
        result = self.whole(self.side, self.c, bases)
        still_unit = self.b[0][0] == -EPS / 2
        bad_a = [k + 1 for k, flag in enumerate(result.unit_a) if not flag]
        bad_b = [k + 1 for k, flag in enumerate(result.unit_b) if not flag]
        expected = [] if still_unit else [1]
        ok = result.verdict == "REFUSE" and bad_a == expected and bad_b == expected and not result.disagreements
        return ok, {"verdict": result.verdict, "not_unit_A": bad_a, "not_unit_B": bad_b}

    def symmetric(self, centers: list[Vec], bases: list[Vec], order: tuple[int, int, int, int]) -> tuple[bool, dict[str, Any]]:
        result = self.whole(self.side, centers, bases)
        clears = [[v[order[w]] for w in range(4)] for v in self.cl]
        ok = (
            result.verdict == self.orig.verdict
            and result.margins == self.m
            and result.clear_a == clears
            and not result.disagreements
        )
        senses = {"ccw": result.sense_b.count(1), "cw": result.sense_b.count(-1)}
        return ok, {"verdict": result.verdict, "senses_B": senses}

    def g4(self) -> tuple[bool, dict[str, Any]]:
        return self.symmetric(self.c, [(-b, a) for a, b in self.b], (0, 1, 2, 3))

    def g5(self) -> tuple[bool, dict[str, Any]]:
        return self.symmetric(self.c, [(-a, -b) for a, b in self.b], (0, 1, 2, 3))

    def g6(self) -> tuple[bool, dict[str, Any]]:
        return self.symmetric([(y, x) for x, y in self.c], [(b, a) for a, b in self.b], (1, 0, 3, 2))

    def g7(self) -> tuple[bool, dict[str, Any]]:
        s = self.side
        return self.symmetric([(s - y, x) for x, y in self.c], [(-b, a) for a, b in self.b], (3, 0, 1, 2))

    def g8(self) -> tuple[bool, dict[str, Any]]:
        s = self.side
        return self.symmetric([(s - x, y) for x, y in self.c], [(-a, b) for a, b in self.b], (2, 1, 0, 3))

    # -- the side -------------------------------------------------------------------------
    def least_far(self) -> Fraction:
        return min(min(v[2], v[3]) for v in self.cl)

    def side_rule(self, delta: Fraction, stated_verdict: str | None = None) -> tuple[bool, dict[str, Any]]:
        result = self.whole(self.side - delta, self.c, self.b)
        clears = [[v[0], v[1], v[2] - delta, v[3] - delta] for v in self.cl]
        cross = {(k, w) for k, values in enumerate(clears, start=1) for w, v in enumerate(values) if v < 0}
        touch = {(k, w) for k, values in enumerate(clears, start=1) for w, v in enumerate(values) if v == 0}
        verdict = "ACCEPT" if not cross and self.orig.verdict == "ACCEPT" else "REFUSE"
        ok = (
            result.clear_a == clears
            and result.margins == self.m
            and self.crossings(result) == cross
            and self.contacts(result) == touch
            and result.verdict == verdict
            and (stated_verdict is None or result.verdict == stated_verdict)
            and not result.disagreements
        )
        crossing_squares = sorted({k for k, _ in cross})
        return ok, {
            "delta": decide.decimal(delta),
            "verdict": result.verdict,
            "square_walls_crossing": len(cross),
            "crossing_squares": crossing_squares[:20],
            "contacts": sorted(touch)[:20],
        }

    def s1a(self) -> tuple[bool, dict[str, Any]]:
        return self.side_rule(EPS)

    def s1b(self) -> tuple[bool, dict[str, Any]]:
        return self.side_rule(Fraction(1, self.side.denominator))

    def s1c(self) -> tuple[bool, dict[str, Any]]:
        return self.side_rule(self.least_far(), "ACCEPT")

    def s1d(self) -> tuple[bool, dict[str, Any]]:
        return self.side_rule(self.least_far() + EPS, "REFUSE")

    def s1e(self) -> tuple[bool, dict[str, Any]]:
        return self.side_rule(self.side - self.claim)

    def s1f(self) -> tuple[bool, dict[str, Any]]:
        return self.side_rule(self.side - self.claim + Fraction(1, 10**12))

    # -- pair and wall moves ----------------------------------------------------------------
    def p1_choice(self) -> tuple[tuple[int, int], int, int] | None:
        order = sorted((value, key) for key, value in self.m.items() if value >= 0)
        for _, (i, j) in order:
            for mover, anchor in ((j, i), (i, j)):
                moved = geom.close_pair(self.c[anchor - 1], self.b[anchor - 1], self.c[mover - 1], self.b[mover - 1], -EPS)
                old = self.c[mover - 1]
                length = abs(moved[0] - old[0]) + abs(moved[1] - old[1])
                others = [value for other, value in self.by_square[mover] if other != anchor]
                if all(value > length for value in others) and all(v > length for v in self.cl[mover - 1]):
                    return (i, j), mover, anchor
        return None

    def p1(self, target: Fraction) -> tuple[bool, dict[str, Any]]:
        choice = self.p1_choice()
        if choice is None:
            return False, {"eligible": None}
        key, mover, anchor = choice
        centers = list(self.c)
        centers[mover - 1] = geom.close_pair(self.c[anchor - 1], self.b[anchor - 1], self.c[mover - 1], self.b[mover - 1], target)
        result = self.whole(self.side, centers, self.b)
        corner = geom.corner_margin(centers[key[0] - 1], self.b[key[0] - 1], centers[key[1] - 1], self.b[key[1] - 1])
        unchanged = all(result.margins[k] == v for k, v in self.m.items() if mover not in k)
        details = {"pair": list(key), "moved": mover, "original_margin": decide.decimal(self.m[key]), "verdict": result.verdict}
        if target == 0:
            others_apart = all(result.margins[k] > 0 for k in result.margins if mover in k and k != key)
            ok = (
                result.verdict == self.orig.verdict
                and result.margins[key] == 0
                and corner == 0
                and result.pair_b[key][0] == "contact"
                and unchanged
                and others_apart
                and all(v > 0 for v in result.clear_a[mover - 1])
                and not result.disagreements
            )
        else:
            ok = (
                result.verdict == "REFUSE"
                and self.overlapping(result) == {key}
                and result.margins[key] == -EPS
                and corner == -EPS
                and result.pair_b[key][0] == "overlap"
                and not self.crossings(result)
                and unchanged
                and not result.disagreements
            )
        return ok, details

    def p1c(self) -> tuple[bool, dict[str, Any]]:
        return self.p1(Fraction(0))

    def p1p(self) -> tuple[bool, dict[str, Any]]:
        return self.p1(-EPS)

    def w1_choice(self, wall: int) -> int | None:
        for value, k in sorted((v[wall], k) for k, v in enumerate(self.cl, start=1)):
            if all(m > value + EPS for _, m in self.by_square[k]):
                return k
        return None

    def w1(self, wall: int, target: Fraction) -> tuple[bool, dict[str, Any]]:
        k = self.w1_choice(wall)
        opposite = (wall + 2) % 4
        if k is None:
            least = min(v[wall] for v in self.cl)
            shift = least - target
            step = {0: (-shift, Fraction(0)), 1: (Fraction(0), -shift), 2: (shift, Fraction(0)), 3: (Fraction(0), shift)}[wall]
            centers = [(x + step[0], y + step[1]) for x, y in self.c]
            result = self.whole(self.side, centers, self.b)
            clears = []
            for v in self.cl:
                row = list(v)
                row[wall] = v[wall] - shift
                row[opposite] = v[opposite] + shift
                clears.append(row)
            ok = result.margins == self.m and result.clear_a == clears and not result.disagreements
            if target == 0:
                ok = ok and result.verdict == self.orig.verdict
            else:
                expected = {(q, wall) for q, v in enumerate(self.cl, start=1) if v[wall] == least}
                ok = ok and result.verdict == "REFUSE" and self.crossings(result) == expected
            return ok, {"fallback": True, "least": decide.decimal(least), "verdict": result.verdict}
        centers = list(self.c)
        centers[k - 1] = geom.to_wall(self.c[k - 1], self.b[k - 1], self.side, wall, target)
        result = self.whole(self.side, centers, self.b)
        original = self.cl[k - 1][wall]
        row = list(self.cl[k - 1])
        row[wall] = target
        row[opposite] = self.cl[k - 1][opposite] + (original - target)
        clears = [list(v) for v in self.cl]
        clears[k - 1] = row
        unchanged = all(result.margins[key] == v for key, v in self.m.items() if k not in key)
        apart = all(result.margins[key] > 0 for key in result.margins if k in key)
        details = {"square": k, "original_clearance": decide.decimal(original), "verdict": result.verdict}
        if target == 0:
            ok = result.verdict == self.orig.verdict and result.clear_a == clears and unchanged and apart and not result.disagreements
        else:
            ok = (
                result.verdict == "REFUSE"
                and result.clear_a == clears
                and self.crossings(result) == {(k, wall)}
                and not self.overlapping(result)
                and unchanged
                and not result.disagreements
            )
        return ok, details

    # -- every square and every pair ------------------------------------------------------
    def wall_all(self) -> tuple[bool, dict[str, Any]]:
        failures = []
        side_q = clip.to_mpq(self.side)
        for k in range(self.n):
            wall = min(range(4), key=lambda q: (self.cl[k][q], q))
            for target, name, below in ((Fraction(0), "touching", False), (-EPS, "crossing", True)):
                moved = geom.to_wall(self.c[k], self.b[k], self.side, wall, target)
                a_value = sat.as_fraction(sat.clearances(sat.integer_square(moved[0], moved[1], self.b[k][0], self.b[k][1]), self.side)[wall])
                corner_value = geom.corner_clearances(moved, self.b[k], self.side)[wall]
                points = clip.corners(clip.to_mpq(moved[0]), clip.to_mpq(moved[1]), clip.to_mpq(self.b[k][0]), clip.to_mpq(self.b[k][1]))
                classes, area = clip.walls(clip.counterclockwise(points)[0], side_q)
                area_ok = area < 1 if below else area == 1
                if not (a_value == target and corner_value == target and classes[wall] == name and area_ok):
                    failures.append([k + 1, WALLS[wall], str(target)])
        return not failures, {"moves": 2 * self.n, "failures": failures[:10]}

    def pair_all(self) -> tuple[bool, dict[str, Any]]:
        failures = []
        ints = [sat.integer_square(c[0], c[1], u[0], u[1]) for c, u in zip(self.c, self.b)]
        polys = [
            clip.counterclockwise(clip.corners(clip.to_mpq(c[0]), clip.to_mpq(c[1]), clip.to_mpq(u[0]), clip.to_mpq(u[1])))[0]
            for c, u in zip(self.c, self.b)
        ]
        for i, j in self.m:
            ci, bi, cj, bj = self.c[i - 1], self.b[i - 1], self.c[j - 1], self.b[j - 1]
            for target, name in ((Fraction(0), "contact"), (-EPS, "overlap")):
                moved = geom.close_pair(ci, bi, cj, bj, target)
                a_value = sat.as_fraction(sat.margin(ints[i - 1], sat.integer_square(moved[0], moved[1], bj[0], bj[1])))
                corner_value = geom.corner_margin(ci, bi, moved, bj)
                poly = clip.counterclockwise(clip.corners(clip.to_mpq(moved[0]), clip.to_mpq(moved[1]), clip.to_mpq(bj[0]), clip.to_mpq(bj[1])))[0]
                kind, _, agree = clip.pair(polys[i - 1], poly)
                if not (a_value == target and corner_value == target and kind == name and agree):
                    failures.append([i, j, str(target)])
        return not failures, {"closings": 2 * len(self.m), "failures": failures[:10]}


def main(argv: list[str]) -> int:
    path, plan_path, claim_text, out_path = argv[1:5]
    started = time.process_time()
    with open(plan_path, encoding="utf-8") as handle:
        plan = json.load(handle)
    cert = reader.read_path(path)
    runner = Controls(cert, Fraction(Decimal(claim_text)))
    table: dict[str, Callable[[], tuple[bool, dict[str, Any]]]] = {
        "C0": runner.c0,
        "R1": runner.r1,
        "R2": runner.r2,
        "R3": runner.r3,
        "R4": runner.r4,
        "R5": runner.r5,
        "R6": runner.r6,
        "R7": runner.r7,
        "R8": runner.r8,
        "R9": runner.r9,
        "G1": runner.g1,
        "G2": runner.g2,
        "G3": runner.g3,
        "G4": runner.g4,
        "G5": runner.g5,
        "G6": runner.g6,
        "G7": runner.g7,
        "G8": runner.g8,
        "S1a": runner.s1a,
        "S1b": runner.s1b,
        "S1c": runner.s1c,
        "S1d": runner.s1d,
        "S1e": runner.s1e,
        "S1f": runner.s1f,
        "P1c": runner.p1c,
        "P1p": runner.p1p,
        "WALL": runner.wall_all,
        "PALL": runner.pair_all,
    }
    for wall, name in enumerate(WALLS):
        table[f"W1c-{name}"] = lambda wall=wall: runner.w1(wall, Fraction(0))
        table[f"W1p-{name}"] = lambda wall=wall: runner.w1(wall, -EPS)
    results = []
    for control in plan["controls"]:
        ident = control["id"]
        clock = time.process_time()
        try:
            ok, details = table[ident]()
        except Exception as error:  # a control that raises did not come out as stated
            ok, details = False, {"raised": f"{type(error).__name__}: {error}"}
        results.append({"id": ident, "stated": control["stated"], "as_stated": ok, "outcome": details, "cpu_seconds": round(time.process_time() - clock, 2)})
        print(ident, "as stated" if ok else "NOT AS STATED", flush=True)
    every = all(item["as_stated"] for item in results)
    receipt = {
        "program": "r1038_controls.py",
        "certificate": os.path.basename(path),
        "original_verdict": runner.orig.verdict,
        "controls": results,
        "as_stated": sum(1 for item in results if item["as_stated"]),
        "of": len(results),
        "outcome": "EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_NOT_AS_STATED",
        "whole_file_decisions": runner.decides,
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=1)
    print(receipt["outcome"], f"{receipt['as_stated']} of {receipt['of']}")
    return 0 if every else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
