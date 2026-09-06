"""Replay strict pair witnesses or separating axes, never global depth feasibility.

Candidate-pair replay does not call producer SAT or intersection routines. Source
reconstruction still uses the accepted packing validator. Target replay requires the
separately accepted exp-113 parent packet; it does not re-solve that LP.
"""

from __future__ import annotations

import argparse
import json
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.trump11.packing import U_INTERVAL, U_MIN_POLY
from devtools.check_full_size_density_support_ceiling import (
    RATIONAL_TEXT,
    load_packet,
    load_source,
    reconstruct_source,
)
from sqpack.field import NumberField
from sqpack.full_size_density.pair_separator import PAIR_CAP, PairFamily, make_family
from sqpack.full_size_density.support_ceiling import (
    Point,
    SupportError,
    axis_square,
    checked_rational,
)

WALL_CAP_SECONDS = 30
CANDIDATE_SOURCE = "exp-113-candidate-v1"
CANDIDATE_WEIGHTS = (
    Fraction(1),
    Fraction(0),
    Fraction(2, 5),
    Fraction(1, 10),
    Fraction(0),
    Fraction(1, 10),
    Fraction(3, 10),
    Fraction(0),
)
CONTROLS = (
    "toy-overlap-v1",
    "toy-edge-v1",
    "toy-corner-v1",
    "toy-gap-v1",
    "toy-equal-v1",
    "toy-triple-v1",
    "toy-prefix-v1",
    "toy-narrow-overlap-v1",
    "toy-algebraic-v1",
    "toy-rotated-algebraic-v1",
    "trump-original-control-v1",
    "trump-uniform-control-v1",
)


def _source_control_family(source: str) -> PairFamily:
    if source == "trump-original-control-v1":
        seeds, side = load_source("trump11-v1")
        return make_family(seeds, side, (Fraction(1),) * len(seeds))
    if source == "trump-uniform-control-v1":
        _, support, metadata = reconstruct_source("trump11-v1")
        weights = [Fraction(value) for value in metadata["uniform_weights"]]
        return make_family(
            tuple(square for orbit in support.orbits for square in orbit),
            support.side,
            tuple(
                weight
                for orbit, weight in zip(support.orbits, weights, strict=True)
                for _ in orbit
            ),
        )
    raise SupportError("unknown exact source control")


def control_family(source: str) -> PairFamily:
    """Construct only a named, predeclared source or toy control."""
    if source in ("trump-original-control-v1", "trump-uniform-control-v1"):
        return _source_control_family(source)
    if source not in CONTROLS:
        raise SupportError("unknown pair control; target is not a control")
    field = (
        NumberField(U_MIN_POLY, U_INTERVAL)
        if source in ("toy-algebraic-v1", "toy-rotated-algebraic-v1")
        else NumberField((1, 0), ("-1", "1"))
    )
    q = field.rational
    if source == "toy-narrow-overlap-v1":
        width = Fraction(1, 10**30)
        squares = (axis_square(q(1), q(1)), axis_square(q(2 - width), q(1)))
        return make_family(squares, q(3), (Fraction(1), Fraction(1, 2)))
    if source == "toy-prefix-v1":
        squares = tuple(axis_square(q(x), q(1)) for x in ("1", "5/2", "3"))
        return make_family(squares, q(4), (Fraction(3, 5),) * 3)
    if source == "toy-rotated-algebraic-v1":
        u = field.alpha
        cosine, sine = (1 - u * u) / (1 + u * u), 2 * u / (1 + u * u)
        center = q("3/2")
        first = axis_square(center, center)
        second = tuple(
            (
                center + cosine * (x - center) - sine * (y - center),
                center + sine * (x - center) + cosine * (y - center),
            )
            for x, y in first
        )
        return make_family((first, second), q(3), (Fraction(1), Fraction(1, 2)))
    if source == "toy-algebraic-v1":
        squares = (
            axis_square(q("3/4") + field.alpha / 100, q("3/4")),
            axis_square(q("5/4"), q("3/4")),
        )
        return make_family(squares, q(2), (Fraction(1), Fraction(1, 2)))
    centers = {
        "toy-overlap-v1": (("1", "1"), ("3/2", "1")),
        "toy-edge-v1": (("1", "1"), ("2", "1")),
        "toy-corner-v1": (("1", "1"), ("2", "2")),
        "toy-gap-v1": (("1", "1"), ("9/4", "1")),
        "toy-equal-v1": (("1", "1"), ("3/2", "1")),
        "toy-triple-v1": (("1", "1"), ("3/2", "1"), ("5/4", "5/4")),
    }[source]
    squares = tuple(axis_square(q(x), q(y)) for x, y in centers)
    weights = (Fraction(1), Fraction(1, 2))
    if source == "toy-equal-v1":
        weights = (Fraction(1, 2),) * 2
    elif source == "toy-triple-v1":
        weights = (Fraction(2, 5),) * 3
    return make_family(squares, q(3), weights)


def _equal(actual: Any, expected: Any, label: str) -> None:
    if json.dumps(actual, sort_keys=True) != json.dumps(expected, sort_keys=True):
        raise SupportError(f"{label} differs from the exact frozen binding")


def bind_parent(parent: Any, metadata: dict[str, Any]) -> None:
    """Bind the accepted parent's source and fixed primal, not its LP proof/history."""
    data = _keys(
        parent,
        {
            "version",
            "source",
            "support",
            "rows",
            "dispositions",
            "primal",
            "multipliers",
            "bound",
            "solve_pivots",
        },
    )
    _equal(data["version"], 1, "parent version")
    _equal(data["source"], "trump11-v1", "parent source")
    _equal(data["support"], metadata, "parent support")
    _equal(data["primal"], [str(weight) for weight in CANDIDATE_WEIGHTS], "parent primal")
    _equal(data["bound"], "56/5", "parent finite-row ceiling")


def candidate_family(parent: Any) -> PairFamily:
    """Explicit target-only reconstruction; never used by control mode."""
    _, support, metadata = reconstruct_source("trump11-v1")
    bind_parent(parent, metadata)
    return make_family(
        tuple(square for orbit in support.orbits for square in orbit),
        support.side,
        tuple(
            weight
            for orbit, weight in zip(support.orbits, CANDIDATE_WEIGHTS, strict=True)
            for _ in orbit
        ),
    )


def family_signature(family: PairFamily) -> dict[str, Any]:
    return {
        "side": [str(value) for value in family.side.coeffs],
        "placements": [
            {
                "key": [
                    [[str(value) for value in coordinate] for coordinate in corner]
                    for corner in item.key
                ],
                "weight": str(item.weight),
            }
            for item in family.placements
        ],
    }


def _keys(value: Any, expected: set[str]) -> dict[str, Any]:
    if type(value) is not dict or set(value) != expected:
        raise SupportError("packet object has missing or unexpected keys")
    return value


def parse_rational(value: Any) -> Fraction:
    """Apply the existing bounded lexical contract before rational conversion."""
    if type(value) is not str or len(value) > 4096 or RATIONAL_TEXT.fullmatch(value) is None:
        raise SupportError("pair rational must be a bounded canonical string")
    result = checked_rational(value)
    if str(result) != value:
        raise SupportError("pair rational is not canonical")
    return result


def _point(value: Any, field: NumberField) -> Point:
    if type(value) is not list or len(value) != 2:
        raise SupportError("point needs two exact coordinates")
    coordinates = []
    for coordinate in value:
        if type(coordinate) is not list or len(coordinate) != field.degree:
            raise SupportError("coordinate has wrong exact-field degree")
        coordinates.append(field.element([parse_rational(item) for item in coordinate]))
    return coordinates[0], coordinates[1]


def _pair(value: Any, expected: tuple[int, int]) -> None:
    if (
        type(value) is not list
        or len(value) != 2
        or any(type(index) is not int for index in value)
        or tuple(value) != expected
    ):
        raise SupportError("pair is not the next canonical eligible pair")


def _check_axis(family: PairFamily, pair: tuple[int, int], axis: Point) -> None:
    ax, ay = axis
    if ax * ax + ay * ay != 1:
        raise SupportError("separation axis must be exactly unit length")
    first, second = (family.placements[index].square for index in pair)
    # A linear functional is extremal at a polygon vertex. This checks the claimed
    # separating halfplanes directly, without producer SAT or edge-axis selection.
    left = [ax * x + ay * y for x, y in first]
    right = [ax * x + ay * y for x, y in second]
    if any((high - low).sign() < 0 for low in left for high in right):
        raise SupportError("axis does not separate the two closed squares")


def _check_witness(family: PairFamily, pair: tuple[int, int], data: dict[str, Any]) -> None:
    point = _point(data["point"], family.side.field)
    radius, excess = parse_rational(data["radius"]), parse_rational(data["excess"])
    first, second = (family.placements[index] for index in pair)
    if radius <= 0 or excess != first.weight + second.weight - 1 or excess <= 0:
        raise SupportError("witness radius or strict overweight is invalid")
    px, py = point
    margins = [px, py, family.side - px, family.side - py]
    for entry in (first, second):
        square = entry.square
        ex, ey = square[1][0] - square[0][0], square[1][1] - square[0][1]
        fx, fy = square[2][0] - square[1][0], square[2][1] - square[1][1]
        orientation = (ex * fy - ey * fx).sign()
        if not orientation:
            raise SupportError("witness square is degenerate")
        for index, (x, y) in enumerate(square):
            nx, ny = square[(index + 1) % 4]
            margins.append(orientation * ((nx - x) * (py - y) - (ny - y) * (px - x)))
    # A unit edge normal has L1 norm <= sqrt(2) < 2. These strict margins
    # therefore certify the whole open L-infinity box, of area 4 radius^2.
    if any((margin - 2 * radius).sign() <= 0 for margin in margins):
        raise SupportError("positive-area common-interior box was not certified")


def replay_packet(packet: Any, *, parent: Any = None) -> str:
    """Check a complete no-pair certificate or the first positive-area pair witness."""
    data = _keys(packet, {"version", "source", "family", "eligible", "separations", "witness"})
    _equal(data["version"], 1, "version")
    if type(data["source"]) is not str:
        raise SupportError("source must be a fixed identifier")
    if data["source"] == CANDIDATE_SOURCE:
        if parent is None:
            raise SupportError("target replay requires the accepted parent packet")
        family = candidate_family(parent)
    else:
        if parent is not None:
            raise SupportError("controls do not accept target parent packets")
        family = control_family(data["source"])
    _equal(data["family"], family_signature(family), "pair family")
    # Deliberately independent of the producer's eligible_pairs helper.
    expected = [
        (i, j)
        for i in range(len(family.placements))
        for j in range(i + 1, len(family.placements))
        if family.placements[i].weight + family.placements[j].weight > 1
    ]
    if (
        len(expected) > PAIR_CAP
        or type(data["eligible"]) is not int
        or data["eligible"] != len(expected)
    ):
        raise SupportError("eligible-pair count or cap is invalid")
    if data["source"] == CANDIDATE_SOURCE and len(expected) != PAIR_CAP:
        raise SupportError("frozen candidate must have exactly 134 eligible pairs")
    records = data["separations"]
    if type(records) is not list or len(records) > len(expected):
        raise SupportError("separation list is invalid")
    for record, pair in zip(records, expected, strict=False):
        entry = _keys(record, {"pair", "axis"})
        _pair(entry["pair"], pair)
        _check_axis(family, pair, _point(entry["axis"], family.side.field))
    if data["witness"] is None:
        if len(records) != len(expected):
            raise SupportError("no-pair result omits an eligible pair")
        return "no-pair-obstruction"
    if len(records) >= len(expected):
        raise SupportError("witness does not name a remaining eligible pair")
    witness = _keys(data["witness"], {"pair", "point", "radius", "excess"})
    pair = expected[len(records)]
    _pair(witness["pair"], pair)
    _check_witness(family, pair, witness)
    return "candidate-refuted"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--parent", type=Path)
    parser.add_argument("--timeout-seconds", type=int, default=WALL_CAP_SECONDS)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    if not 1 <= args.timeout_seconds <= WALL_CAP_SECONDS:
        parser.error("timeout must be an integer from 1 to 30 seconds")
    if not args.worker:
        command = [
            sys.executable,
            "-m",
            "devtools.check_full_size_density_pair_separator",
            str(args.certificate),
            "--worker",
            "--timeout-seconds",
            str(args.timeout_seconds),
        ]
        if args.parent is not None:
            command.extend(["--parent", str(args.parent)])
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=args.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired:
            print("unresolved: fixed process wall cap expired", file=sys.stderr)
            return 1
        except OSError as error:
            print(f"refused: {error}", file=sys.stderr)
            return 2
        sys.stderr.write(completed.stderr)
        if completed.returncode == 0:
            sys.stdout.write(completed.stdout)
        return completed.returncode

    def expired(_signal, _frame):
        raise TimeoutError("pair replay reached its fixed process wall cap")

    started, cpu = time.monotonic(), time.process_time()
    previous = signal.signal(signal.SIGALRM, expired)
    signal.alarm(args.timeout_seconds)
    try:
        parent = None if args.parent is None else load_packet(args.parent)
        verdict = replay_packet(load_packet(args.certificate), parent=parent)
    except TimeoutError as error:
        print(f"unresolved: {error}", file=sys.stderr)
        return 1
    except (SupportError, OSError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 2
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    print(
        json.dumps(
            {
                "verdict": verdict,
                "scope": "fixed candidate only; H099 unresolved; no-hit is not feasibility",
            },
            sort_keys=True,
        )
    )
    print(
        json.dumps(
            {
                "wall_seconds": time.monotonic() - started,
                "cpu_seconds": time.process_time() - cpu,
            },
            sort_keys=True,
        ),
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
