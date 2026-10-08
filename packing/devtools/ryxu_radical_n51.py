"""Independently decide the undilated issue432 n51 construction in Q(sqrt(2)).

The independent route uses rational pairs and direct axis/diamond corners;
it shares no number-field or geometry implementation with the native route.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import ryxu_arrangement_reports as rational
from sqpack.witness import exact_verify

SOURCE_SHA256 = "93130ffb2f9da1b15ba5e8e491e60509192d6fb21108aa2adc86d29c4f071e5d"
RECORD_SHA256 = "bf744f8b9b41776cabe43eb46c2e45293fbfe3803eb47578de878c61509357e0"
# Frozen complete deciding outcomes, retained across the private-worker custody boundary.
OUTCOME_SHA256 = {
    "positive": "2170142ecd3e1065a038ad5d1eb38c7f53951d7f9fad6851a34f729ba9b249a2",
    "duplicate-square-overlap": (
        "65dfc3caaf99e148f0a49dfd61702c8b95397cd5e88a17d9413899f83685dc4e"
    ),
    "square-translated-outside-container": (
        "02a31fcac9651ffbc3b0a6dab329675c1e2cdecdf263d92c5327b37331a6c0cc"
    ),
}


@dataclass(frozen=True)
class Q2:
    """a+b sqrt(2), with order decided by exact rational comparisons."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other: Q2) -> Q2:
        return Q2(self.a + other.a, self.b + other.b)

    def __neg__(self) -> Q2:
        return Q2(-self.a, -self.b)

    def __sub__(self, other: Q2) -> Q2:
        return self + -other

    def __mul__(self, other: Q2) -> Q2:
        return Q2(self.a * other.a + 2 * self.b * other.b, self.a * other.b + self.b * other.a)

    def sign(self) -> int:
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a == 0 or (self.a > 0) == (self.b > 0):
            return (self.b > 0) - (self.b < 0)
        difference = self.a * self.a - 2 * self.b * self.b
        return ((difference > 0) - (difference < 0)) * ((self.a > 0) - (self.a < 0))

    def scalar(self) -> list[str]:
        return [str(self.a), str(self.b)]


def parse(value: object) -> Q2:
    if type(value) is not str or len(value) > 128:
        raise ValueError("bounded exact radical expression required")
    if re.fullmatch(r"-?[0-9]+(?:/[1-9][0-9]*)?", value):
        return Q2(Fraction(value))
    normalized = value.replace("\u2212", "-")
    match = re.fullmatch(r"\((-?[0-9]+) ([+-]) ([0-9]+)√2\)/([1-9][0-9]*)", normalized)
    if match is not None:
        a, sign, b, denominator = match.groups()
        return Q2(
            Fraction(int(a), int(denominator)),
            Fraction(int(b) * (1 if sign == "+" else -1), int(denominator)),
        )
    match = re.fullmatch(r"(-?[0-9]+) ([+-]) ([0-9]+)√2", normalized)
    if match is not None:
        a, sign, b = match.groups()
        return Q2(Fraction(a), Fraction(int(b) * (1 if sign == "+" else -1)))
    raise ValueError("unsupported exact radical expression")


def fact_path() -> Path:
    return rational.PACKET / "facts/n051-undilated-record.json.xz"


def acquire(path: Path) -> None:
    data = path.read_bytes()
    if len(data) > 1_000_000 or hashlib.sha256(data).hexdigest() != SOURCE_SHA256:
        raise ValueError("undilated source blob differs from acquired bytes")
    record = json.loads(data, object_pairs_hook=rational.unique_json_keys)
    if type(record) is not dict or set(record) != {"records"}:
        raise ValueError("unexpected upstream records envelope")
    matches = [row for row in record["records"] if row.get("n") == 51]
    if len(matches) != 1:
        raise ValueError("missing or repeated n51 source record")
    row = matches[0]
    if hashlib.sha256(rational.canonical_json(row)).hexdigest() != RECORD_SHA256:
        raise ValueError("n51 extraction differs from frozen source record")
    rational.save(fact_path(), row)


def read_fact() -> dict[str, Any]:
    rational.ensure_private(fact_path())
    row = rational.kernel.read_xz(fact_path())
    if hashlib.sha256(rational.canonical_json(row)).hexdigest() != RECORD_SHA256:
        raise ValueError("undilated complete source record changed")
    if (
        type(row) is not dict
        or set(row) != {"n", "side", "side_exact", "squares"}
        or type(row["n"]) is not int
        or row["n"] != 51
        or len(row["squares"]) != 51
    ):
        raise ValueError("incomplete n51 radical source roster")
    for square in row["squares"]:
        if set(square) != {"x", "y", "angle", "x_exact", "y_exact", "angle_exact"} or square[
            "angle_exact"
        ] not in {"0", "π/4"}:
            raise ValueError("unsupported complete radical square")
        parse(square["x_exact"])
        parse(square["y_exact"])
    if parse(row["side_exact"]) != Q2(Fraction(16, 3), Fraction(5, 3)):
        raise ValueError("wrong undilated algebraic side")
    return row


def inputs(control: str) -> tuple[Q2, list[tuple[Q2, Q2, str]]]:
    if control not in rational.JOBS:
        raise ValueError("unknown radical control")
    row = read_fact()
    side = parse(row["side_exact"])
    poses = [
        (parse(s["x_exact"]), parse(s["y_exact"]), s["angle_exact"]) for s in row["squares"]
    ]
    if control == "duplicate-square-overlap":
        poses[1] = poses[0]
    elif control == "square-translated-outside-container":
        x, y, angle = poses[0]
        poses[0] = (x + side + Q2(Fraction(2)), y, angle)
    return side, poses


def witness(side: Q2, poses: list[tuple[Q2, Q2, str]]) -> dict[str, Any]:
    zero, one, diagonal = Q2(), Q2(Fraction(1)), Q2(b=Fraction(1, 2))
    return {
        "id": "W-ryxu-432-n051-radical",
        "n": len(poses),
        "side": side.scalar(),
        "square_size": one.scalar(),
        "representation": "center-basis",
        "scalar": {
            "kind": "algebraic-number-field",
            "minimal_polynomial": ["1", "0", "-2"],
            "isolating_interval": ["1", "2"],
        },
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": i,
                "center": [x.scalar(), y.scalar()],
                "basis": [one.scalar(), zero.scalar()]
                if angle == "0"
                else [diagonal.scalar(), diagonal.scalar()],
            }
            for i, (x, y, angle) in enumerate(poses, start=1)
        ],
        "claim": {
            "coordinate_provenance": "reported",
            "method": "exact-algebraic",
            "limitations": (
                "Undilated n51 source construction: feasibility only, "
                "no global optimality claim."
            ),
        },
    }


def independent(side: Q2, poses: list[tuple[Q2, Q2, str]]) -> dict[str, Any]:
    half, diagonal, one = Q2(Fraction(1, 2)), Q2(b=Fraction(1, 2)), Q2(Fraction(1))
    polygons = []
    failures: list[str] = []
    for i, (x, y, angle) in enumerate(poses):
        corners = (
            [
                (x - half, y - half),
                (x + half, y - half),
                (x + half, y + half),
                (x - half, y + half),
            ]
            if angle == "0"
            else [(x, y - diagonal), (x + diagonal, y), (x, y + diagonal), (x - diagonal, y)]
        )
        edges = [
            (corners[(j + 1) % 4][0] - cx, corners[(j + 1) % 4][1] - cy)
            for j, (cx, cy) in enumerate(corners)
        ]
        if (
            any(dx * dx + dy * dy != one for dx, dy in edges)
            or edges[0][0] * edges[1][1] - edges[0][1] * edges[1][0] != one
        ):
            failures.append(f"square {i}: non-unit or non-oriented corners")
        if any(
            min(cx.sign(), cy.sign(), (side - cx).sign(), (side - cy).sign()) < 0
            for cx, cy in corners
        ):
            failures.append(f"square {i}: outside container")
        polygons.append((corners, edges))
    pairs = 0
    touching = 0

    def extreme(values: list[Q2], *, maximum: bool) -> Q2:
        result = values[0]
        for value in values[1:]:
            if (value - result).sign() == (1 if maximum else -1):
                result = value
        return result

    for i, (left, left_edges) in enumerate(polygons):
        for j in range(i + 1, len(polygons)):
            pairs += 1
            right, right_edges = polygons[j]
            gaps = []
            for dx, dy in left_edges + right_edges:
                axis = (-dy, dx)
                lp = [cx * axis[0] + cy * axis[1] for cx, cy in left]
                rp = [cx * axis[0] + cy * axis[1] for cx, cy in right]
                gaps.extend(
                    [
                        extreme(rp, maximum=False) - extreme(lp, maximum=True),
                        extreme(lp, maximum=False) - extreme(rp, maximum=True),
                    ]
                )
            best = extreme(gaps, maximum=True)
            if best.sign() < 0:
                failures.append(f"pair {i},{j}: interior overlap")
            elif best.sign() == 0:
                touching += 1
    return {
        "route": "independent-rational-pairs-Q-sqrt2-direct-corners-SAT",
        "n": len(poses),
        "pairs_tested": pairs,
        "touching_pairs": touching,
        "verification_passed": not failures,
        "failures": failures,
        "side": side.scalar(),
        "field": "Q(sqrt(2)), positive root; order by a² versus 2b²",
        "limitations": "Complete feasibility only; no global optimality.",
    }


def run_case(control: str) -> dict[str, Any]:
    side, poses = inputs(control)
    native_input = witness(side, poses)
    native, _ = exact_verify(native_input)
    other = independent(side, poses)
    expected = control == "positive"
    if (
        native["verification_passed"] is not expected
        or other["verification_passed"] is not expected
        or native["pairs_tested"] != 1275
        or other["pairs_tested"] != 1275
    ):
        raise ValueError("complete radical deciding routes disagree or control escaped")
    return {
        "control": control,
        "native_input": native_input,
        "exact_verify": native,
        "independent": other,
    }


def check_certification(*, replay: bool = False) -> dict[str, Any]:
    """Bind complete retained native inputs and outcomes to source and all controls."""
    rows = {}
    for control in rational.JOBS:
        path = rational.PACKET / f"receipts/n051-radical-{control}.json.xz"
        rational.ensure_private(path)
        row = rational.kernel.read_xz(path)
        if hashlib.sha256(rational.canonical_json(row)).hexdigest() != OUTCOME_SHA256[control]:
            raise ValueError("complete frozen radical native outcome changed")
        side, poses = inputs(control)
        if (
            type(row) is not dict
            or set(row) != {"control", "native_input", "exact_verify", "independent"}
            or row["control"] != control
            or row["native_input"] != witness(side, poses)
        ):
            raise ValueError("radical receipt complete source input or namespace mismatch")
        native = row["exact_verify"]
        other = row["independent"]
        expected = control == "positive"
        if (
            type(native) is not dict
            or type(other) is not dict
            or native.get("verification_passed") is not expected
            or other.get("verification_passed") is not expected
            or type(native.get("pairs_tested")) is not int
            or native["pairs_tested"] != 1275
            or type(other.get("pairs_tested")) is not int
            or other["pairs_tested"] != 1275
        ):
            raise ValueError("radical receipt incomplete native verdict")
        if replay and row != run_case(control):
            raise ValueError("fresh full radical outcome differs from retained receipt")
        rows[control] = row
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("acquire", "certify", "check"))
    parser.add_argument("--source", type=Path)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    if args.command == "acquire":
        if args.source is None:
            parser.error("acquire requires --source")
        acquire(args.source)
    elif args.command == "certify":
        started = time.monotonic()
        for control in rational.JOBS:
            row = run_case(control)
            rational.save(rational.PACKET / f"receipts/n051-radical-{control}.json.xz", row)
        rational.save(
            rational.PACKET / "receipts/n051-radical-measurement.json.xz",
            {
                "actual_wall_seconds": time.monotonic() - started,
                "full_roster_jobs": 3,
                "routes": 2,
                "pair_decisions": 7650,
            },
        )
        check_certification()
    else:
        check_certification(replay=args.replay)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
