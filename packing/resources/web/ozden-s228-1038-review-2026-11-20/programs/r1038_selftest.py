"""Lane r1038's self-test: the reader, both methods and the corner formulation, against
answers derived by hand. It reads no certificate.

Usage: python -I -B r1038_selftest.py OUT_JSON

- The reader: one valid synthetic text, its non-canonical scalars, and 34 malformed
  variants, each refused for the stated reason.
- Pairs of equal orientation: with square j at c_i + s u + r v, the margin is
  max(|s|, |r|) - 1 exactly and, when |s| < 1 and |r| < 1, the overlap area is
  (1 - |s|)(1 - |r|). Over rational bases, offsets and rational rigid motions.
- An axis-aligned square and a turned one at (x, 0): the margin is |x| - (1 + |a| + |b|)/2,
  under rational rigid motions.
- Walls: the clearances c - (|a| + |b|)/2 and S - c - (|a| + |b|)/2; for axis-aligned
  squares the area inside is the product of the two overlaps.
- Unit squares: bases on the unit circle accepted, others refused by both methods.
- Moves: closing a pair to 0 and to -eps, and moving a square to a wall and past.
- Small packings: a 2 x 2 grid and a packing with a turned square accepted; three broken
  copies refused for the stated reason.
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1038_clip as clip  # noqa: E402
import r1038_decide as decide  # noqa: E402
import r1038_geom as geom  # noqa: E402
import r1038_reader as reader  # noqa: E402
import r1038_sat as sat  # noqa: E402

EPS = Fraction(1, 10**30)
F = Fraction
CHECKS = {"passed": 0, "failed": []}


def check(condition: bool, label: str) -> None:
    if condition:
        CHECKS["passed"] += 1
    else:
        CHECKS["failed"].append(label)


def unit_from_t(t: Fraction) -> tuple[Fraction, Fraction]:
    return ((1 - t * t) / (1 + t * t), 2 * t / (1 + t * t))


BASES = [unit_from_t(F(t)) for t in ("0", "1/2", "1/3", "2/7", "3/4", "-1/5", "5/3", "-7/11", "123456789/987654321")]
BASES += [(F(0), F(1)), (F(-1), F(0)), (F(-3, 5), F(-4, 5))]
OFFSETS = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1), 1 - EPS, 1 + EPS, F(5, 4), F(3, 2), F(2)]
OFFSETS = OFFSETS + [-v for v in OFFSETS if v != 0]
MOTIONS = [((F(1), F(0)), (F(0), F(0))), (unit_from_t(F(2, 3)), (F(7, 3), F(-5, 2))), (unit_from_t(F(-9, 13)), (F(1, 10**20), F(11, 7)))]


def rotate(vector: tuple[Fraction, Fraction], unit: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    return (unit[0] * vector[0] - unit[1] * vector[1], unit[1] * vector[0] + unit[0] * vector[1])


def moved(center, basis, motion):
    unit, shift = motion
    c = rotate(center, unit)
    return (c[0] + shift[0], c[1] + shift[1]), rotate(basis, unit)


def b_pair(ci, bi, cj, bj):
    pi = clip.counterclockwise(clip.corners(*(clip.to_mpq(v) for v in (*ci, *bi))))[0]
    pj = clip.counterclockwise(clip.corners(*(clip.to_mpq(v) for v in (*cj, *bj))))[0]
    kind, area, agree = clip.pair(pi, pj)
    return kind, Fraction(int(area.numerator), int(area.denominator)), agree


def a_margin(ci, bi, cj, bj) -> Fraction:
    return sat.as_fraction(sat.margin(sat.integer_square(*ci, *bi), sat.integer_square(*cj, *bj)))


def expected_class(value: Fraction) -> str:
    return "apart" if value > 0 else "contact" if value == 0 else "overlap"


def pair_checks() -> None:
    origin = (F(0), F(0))
    for basis in BASES:
        v = (-basis[1], basis[0])
        for s in OFFSETS:
            for r in OFFSETS:
                cj = (s * basis[0] + r * v[0], s * basis[1] + r * v[1])
                expected = max(abs(s), abs(r)) - 1
                area = (1 - abs(s)) * (1 - abs(r)) if abs(s) < 1 and abs(r) < 1 else F(0)
                for motion in MOTIONS[:2]:
                    ci2, bi2 = moved(origin, basis, motion)
                    cj2, bj2 = moved(cj, basis, motion)
                    label = f"same {basis} {s} {r} {motion[0]}"
                    check(a_margin(ci2, bi2, cj2, bj2) == expected, "A " + label)
                    check(geom.corner_margin(ci2, bi2, cj2, bj2) == expected, "corners " + label)
                    kind, got, agree = b_pair(ci2, bi2, cj2, bj2)
                    check(agree and kind == expected_class(expected), "B class " + label)
                    check(got == area, "B area " + label)
    axis = (F(1), F(0))
    for basis in BASES:
        reach = (1 + abs(basis[0]) + abs(basis[1])) / 2
        for x in (reach, reach + EPS, reach - EPS, reach + F(1, 7), reach - F(1, 7), -reach, -reach - EPS, F(0)):
            expected = abs(x) - reach
            for motion in MOTIONS:
                ci2, bi2 = moved((F(0), F(0)), axis, motion)
                cj2, bj2 = moved((x, F(0)), basis, motion)
                label = f"turned {basis} {x} {motion[0]}"
                check(a_margin(ci2, bi2, cj2, bj2) == expected, "A " + label)
                check(a_margin(cj2, bj2, ci2, bi2) == expected, "A swapped " + label)
                check(geom.corner_margin(ci2, bi2, cj2, bj2) == expected, "corners " + label)
                kind, _, agree = b_pair(ci2, bi2, cj2, bj2)
                check(agree and kind == expected_class(expected), "B class " + label)


def wall_checks() -> None:
    side = F(5, 2)
    for basis in BASES:
        reach = (abs(basis[0]) + abs(basis[1])) / 2
        for cx in (reach, reach - EPS, reach + F(1, 3), side - reach, side - reach + EPS, F(5, 4)):
            for cy in (reach, side - reach - F(1, 9), side - reach + F(1, 9)):
                expected = [cx - reach, cy - reach, side - cx - reach, side - cy - reach]
                square = sat.integer_square(cx, cy, basis[0], basis[1])
                got = [sat.as_fraction(v) for v in sat.clearances(square, side)]
                label = f"walls {basis} {cx} {cy}"
                check(got == expected, "A " + label)
                check(geom.corner_clearances((cx, cy), basis, side) == expected, "corners " + label)
                points = clip.counterclockwise(clip.corners(*(clip.to_mpq(v) for v in (cx, cy, *basis))))[0]
                classes, area = clip.walls(points, clip.to_mpq(side))
                names = ["clear" if v > 0 else "touching" if v == 0 else "crossing" for v in expected]
                check(classes == names, "B classes " + label)
                if all(v >= 0 for v in expected):
                    check(area == 1, "B area inside " + label)
                else:
                    check(area < 1, "B area below 1 " + label)
                if basis[1] == 0 or basis[0] == 0:
                    over_x = max(F(0), min(cx + F(1, 2), side) - max(cx - F(1, 2), F(0)))
                    over_y = max(F(0), min(cy + F(1, 2), side) - max(cy - F(1, 2), F(0)))
                    check(Fraction(int(area.numerator), int(area.denominator)) == over_x * over_y, "B area " + label)


def unit_checks() -> None:
    for basis in BASES:
        square = sat.integer_square(F(1), F(1), *basis)
        check(sat.is_unit(square), f"A unit {basis}")
        check(clip.unit_square(clip.corners(*(clip.to_mpq(v) for v in (F(1), F(1), *basis)))), f"B unit {basis}")
    for basis in ((F(1), F(1)), (F(3, 5), F(4, 5) + EPS), (F(1, 2), F(1, 2)), (F(0), F(0)), (F(1) + EPS, F(0)), (F(-3, 5), F(4, 5) - EPS)):
        square = sat.integer_square(F(1), F(1), *basis)
        check(not sat.is_unit(square), f"A not unit {basis}")
        check(not clip.unit_square(clip.corners(*(clip.to_mpq(v) for v in (F(1), F(1), *basis)))), f"B not unit {basis}")


def move_checks() -> None:
    side = F(9)
    cases = [((F(3), F(3)), BASES[1], (F(5), F(4)), BASES[4]), ((F(2), F(6)), BASES[0], (F(3), F(6)), BASES[2]), ((F(4), F(4)), BASES[5], (F(6), F(7, 3)), BASES[8])]
    for ci, bi, cj, bj in cases:
        for target, name in ((F(0), "contact"), (-EPS, "overlap"), (F(1, 10**20), "apart")):
            new = geom.close_pair(ci, bi, cj, bj, target)
            check(a_margin(ci, bi, new, bj) == target, f"A close {target}")
            check(geom.corner_margin(ci, bi, new, bj) == target, f"corners close {target}")
            kind, _, agree = b_pair(ci, bi, new, bj)
            check(agree and kind == name, f"B close {target}")
        for wall in range(4):
            for target, name in ((F(0), "touching"), (-EPS, "crossing")):
                new = geom.to_wall(cj, bj, side, wall, target)
                got = sat.as_fraction(sat.clearances(sat.integer_square(*new, *bj), side)[wall])
                check(got == target, f"A wall {wall} {target}")
                check(geom.corner_clearances(new, bj, side)[wall] == target, f"corners wall {wall} {target}")
                points = clip.counterclockwise(clip.corners(*(clip.to_mpq(v) for v in (*new, *bj))))[0]
                classes, area = clip.walls(points, clip.to_mpq(side))
                check(classes[wall] == name and ((area == 1) if target == 0 else (area < 1)), f"B wall {wall} {target}")


def packing_checks() -> None:
    axis = (F(1), F(0))
    grid = [(F(1, 2), F(1, 2)), (F(3, 2), F(1, 2)), (F(1, 2), F(3, 2)), (F(3, 2), F(3, 2))]
    result = decide.decide(F(2), grid, [axis] * 4)
    facts = decide.summary(result)
    check(result.verdict == "ACCEPT", "grid accepted")
    check(facts["pair_classes_A"] == {"apart": 0, "contact": 6, "overlap": 0}, "grid six contacts")
    check(len(facts["wall_contacts"]) == 8, "grid eight wall contacts")
    turned = decide.decide(F(3), [(F(1, 2), F(1, 2)), (F(2), F(2))], [axis, (F(3, 5), F(4, 5))])
    check(turned.verdict == "ACCEPT" and not turned.disagreements, "turned packing accepted")
    shifted = list(grid)
    shifted[1] = (F(3, 2) - F(1, 10), F(1, 2))
    broken = decide.decide(F(2), shifted, [axis] * 4)
    check(broken.verdict == "REFUSE" and broken.pair_b[(1, 2)] == ("overlap", F(1, 10)), "broken: overlap of area 1/10")
    check(broken.margins[(1, 2)] == F(-1, 10), "broken: margin -1/10")
    outside = list(grid)
    outside[3] = (F(3, 2) + F(1, 10), F(3, 2))
    broken = decide.decide(F(2), outside, [axis] * 4)
    check(broken.verdict == "REFUSE" and broken.inside_b[3] == F(9, 10), "broken: square 4 crossing, 9/10 inside")
    check(broken.wall_a[3][2] == "crossing" and broken.clear_a[3][2] == F(-1, 10), "broken: right clearance -1/10")
    skewed = decide.decide(F(2), grid, [axis, axis, axis, (F(3, 5), F(4, 5) + EPS)])
    check(skewed.verdict == "REFUSE" and skewed.unit_a == [True, True, True, False] and skewed.unit_b == [True, True, True, False], "broken: square 4 not unit")


def valid_text(**edits: str) -> str:
    values = {
        "contract": "packing.squares:Witness/v2",
        "wid": "W-selftest",
        "n": "2",
        "side": "'5/2'",
        "size": "'1'",
        "rep": "center-basis",
        "kind": "rational",
        "origin": "lower-left",
        "s1": "    center:\n    - '1/2'\n    - 1/2\n    basis:\n    - '1'\n    - '0'\n",
        "s2": "    center:\n    - 7/4\n    - '7/4'\n    basis:\n    - 3/5\n    - -4/5\n",
        "id2": "2",
        "extra": "",
    }
    values.update(edits)
    return (
        "softschema:\n"
        f"  contract: {values['contract']}\n"
        "  schema: witness.schema.yaml\n"
        "  envelope: witness\n"
        "witness:\n"
        f"  id: {values['wid']}\n"
        f"  n: {values['n']}\n"
        f"  side: {values['side']}\n"
        f"  square_size: {values['size']}\n"
        f"  representation: {values['rep']}\n"
        "  scalar:\n"
        f"    kind: {values['kind']}\n"
        "  coordinates:\n"
        f"    origin: {values['origin']}\n"
        "    axes: x-right-y-up\n"
        "    angle_unit: not-applicable\n"
        f"{values['extra']}"
        "  squares:\n"
        "  - id: 1\n"
        f"{values['s1']}"
        f"  - id: {values['id2']}\n"
        f"{values['s2']}"
        "  claim:\n"
        "    coordinate_provenance: reported\n"
        "    method: exact-algebraic\n"
        "    limitations: a synthetic self-test text\n"
    )


def reader_checks() -> None:
    cert = reader.read_text(valid_text())
    check(cert.n == 2 and cert.side == F(5, 2), "valid read")
    check(cert.centers == [(F(1, 2), F(1, 2)), (F(7, 4), F(7, 4))], "valid centres")
    check(cert.bases == [(F(1), F(0)), (F(3, 5), F(-4, 5))], "valid bases")
    check(cert.noncanonical == [], "valid canonical")
    odd = reader.read_text(valid_text(side="'10/4'", s2="    center:\n    - '-0'\n    - '0/3'\n    basis:\n    - '4/1'\n    - '0'\n"))
    check(odd.noncanonical == ["side", "square 2.center.x", "square 2.center.y", "square 2.basis.x"], "non-canonical recorded")
    check(odd.side == F(5, 2) and odd.centers[1] == (F(0), F(0)) and odd.bases[1] == (F(4), F(0)), "non-canonical values")
    refusals = [
        ("two documents", valid_text() + "---\n" + valid_text(), "documents"),
        ("anchor", valid_text(side="&s '5/2'"), "an anchor"),
        ("alias", valid_text(extra="  source: *x\n"), "alias"),
        ("explicit tag", valid_text(side="!!str 5/2"), "explicit tag"),
        ("duplicate key", valid_text(extra="  side: '5/2'\n"), "twice"),
        ("tab", valid_text().replace("  n: 2", "  n:\t2"), "a tab"),
        ("carriage return", valid_text().replace("\n", "\r\n"), "carriage return"),
        ("byte-order mark", "\ufeff" + valid_text(), "byte-order mark"),
        ("float side", valid_text(side="2.5"), "float"),
        ("bool size", valid_text(size="yes"), "bool"),
        ("null n", valid_text(n=""), "null"),
        ("plus", valid_text(side="'+5/2'"), "is not p or p/q"),
        ("leading zero", valid_text(side="'05/2'"), "is not p or p/q"),
        ("zero denominator", valid_text(side="'5/0'"), "is not p or p/q"),
        ("negative denominator", valid_text(side="'5/-2'"), "is not p or p/q"),
        ("quoted decimal", valid_text(side="'2.5'"), "is not p or p/q"),
        ("missing claim", valid_text().split("  claim:")[0], "missing ['claim']"),
        ("extra witness key", valid_text(extra="  angle: '0'\n"), "extra ['angle']"),
        ("corners", valid_text(rep="corners"), "not center-basis"),
        ("decimal kind", valid_text(kind="decimal"), "not exactly kind rational"),
        ("container centre", valid_text(origin="container-center"), "not lower-left"),
        ("ids out of order", valid_text(id2="3"), "out of order"),
        ("string id", valid_text(id2="'2'"), "out of order"),
        ("n mismatch", valid_text(n="3"), "squares are listed"),
        ("three centre scalars", valid_text(s1="    center:\n    - '1/2'\n    - '1/2'\n    - '0'\n    basis:\n    - '1'\n    - '0'\n"), "not a list of two scalars"),
        ("square extra key", valid_text(s1="    center:\n    - '1/2'\n    - '1/2'\n    basis:\n    - '1'\n    - '0'\n    angle: '0'\n"), "keys"),
        ("size two", valid_text(size="'2'"), "square_size"),
        ("contract v1", valid_text(contract="packing.squares:Witness/v1"), "contract"),
        ("hex n", valid_text(n="0x2"), "scalar of type"),
        ("underscore n", valid_text(n="0_2"), "scalar of type"),
        ("sexagesimal n", valid_text(n="1:30"), "scalar of type"),
        ("directive", "%YAML 1.1\n---\n" + valid_text(), "directive"),
        ("witness id", valid_text(wid="W-Self"), "witness id"),
        ("merge key", valid_text(extra="  <<: {a: '1'}\n"), "not a string"),
    ]
    for label, text, needle in refusals:
        try:
            reader.read_text(text)
        except reader.ReadRefused as error:
            check(needle in str(error), f"reader {label}: {error}")
        except Exception as error:  # any other failure is not the stated refusal
            check(False, f"reader {label}: raised {type(error).__name__} {error}")
        else:
            check(False, f"reader {label}: read")


def main(argv: list[str]) -> int:
    started = time.process_time()
    reader_checks()
    pair_checks()
    wall_checks()
    unit_checks()
    move_checks()
    packing_checks()
    failed = CHECKS["failed"]
    receipt = {
        "program": "r1038_selftest.py",
        "outcome": "PASSED" if not failed else "FAILED",
        "checks": CHECKS["passed"] + len(failed),
        "passed": CHECKS["passed"],
        "failed": failed[:40],
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    with open(argv[1], "w", encoding="utf-8") as handle:
        json.dump(receipt, handle, indent=1)
    print(receipt["outcome"], receipt["passed"], "of", receipt["checks"])
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
