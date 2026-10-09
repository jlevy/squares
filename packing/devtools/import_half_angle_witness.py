"""Import an exact centre/half-angle packing as a checked rational Witness/v2.

The input has a rational-string ``side`` and a complete ``squares`` list of
``{x, y, t}`` objects, where ``t`` is the tangent of half the rotation angle.
The independent corner checker decides feasibility before the output is published.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
import re
import shlex
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.check_rational_witness_independent import pair_gap, square_failures
from sqpack.witness import witness_document

MAX_SOURCE_BYTES = 1_000_000
"""Input ceiling that keeps this small adapter from consuming an unbounded source."""
MAX_SQUARES = 64
"""Admission ceiling for exact pairwise checking."""
MAX_LITERAL_CHARS = 256
"""Maximum decimal digits and punctuation in one exact rational source literal."""
RATIONAL = re.compile(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")
REPO = Path(__file__).resolve().parents[2]
WITNESS_SCHEMA = REPO / "packing/witnesses/witness.schema.yaml"


class HalfAngleImportError(ValueError):
    """A source or feasibility refusal; the final output is not written."""


def _object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HalfAngleImportError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _fraction(raw: Any, label: str) -> Fraction:
    if type(raw) is not str or len(raw) > MAX_LITERAL_CHARS or RATIONAL.fullmatch(raw) is None:
        raise HalfAngleImportError(f"{label} must be a bounded exact rational string")
    return Fraction(raw)


def _literal(value: Fraction) -> str:
    return str(value)


def _source_path(source: Path) -> str:
    resolved = source.resolve()
    try:
        return str(resolved.relative_to(REPO))
    except ValueError:
        return str(resolved)


def _corners(x: Fraction, y: Fraction, t: Fraction) -> list[tuple[Fraction, Fraction]]:
    denominator = 1 + t * t
    u = ((1 - t * t) / denominator, 2 * t / denominator)
    v = (-u[1], u[0])
    return [
        (x - u[0] / 2 - v[0] / 2, y - u[1] / 2 - v[1] / 2),
        (x + u[0] / 2 - v[0] / 2, y + u[1] / 2 - v[1] / 2),
        (x + u[0] / 2 + v[0] / 2, y + u[1] / 2 + v[1] / 2),
        (x - u[0] / 2 + v[0] / 2, y - u[1] / 2 + v[1] / 2),
    ]


def rational_literal(raw: Any, label: str) -> Fraction:
    """Parse the adapter's bounded exact rational-string input contract."""
    return _fraction(raw, label)


def unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Build an untrusted JSON object while refusing duplicate keys."""
    return _object(pairs)


def half_angle_corners(
    x: Fraction, y: Fraction, t: Fraction
) -> list[tuple[Fraction, Fraction]]:
    """Expose the exact conversion for bounded packet adapters."""
    return _corners(x, y, t)


def import_source(source: Path, *, expected_n: int, expected_side: str) -> dict[str, Any]:
    """Convert only a complete, independently feasible rational source roster."""
    if not 1 <= expected_n <= MAX_SQUARES:
        raise HalfAngleImportError(f"expected_n must be between 1 and {MAX_SQUARES}")
    side = _fraction(expected_side, "expected side")
    if side <= 0:
        raise HalfAngleImportError("expected side must be positive")
    with source.open("rb") as stream:
        raw = stream.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES:
        raise HalfAngleImportError("source exceeds the input byte ceiling")
    try:
        data = json.loads(raw, object_pairs_hook=_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise HalfAngleImportError(f"invalid JSON source: {error}") from error
    if type(data) is not dict or _fraction(data.get("side"), "source side") != side:
        raise HalfAngleImportError("source side differs from the expected side")
    entries = data.get("squares")
    if type(entries) is not list or len(entries) != expected_n:
        raise HalfAngleImportError("source square count differs from expected_n")

    squares: list[list[tuple[Fraction, Fraction]]] = []
    for index, entry in enumerate(entries, start=1):
        if type(entry) is not dict or set(entry) != {"x", "y", "t"}:
            raise HalfAngleImportError(f"square {index} must contain exactly x, y, t")
        x = _fraction(entry["x"], f"square {index} x")
        y = _fraction(entry["y"], f"square {index} y")
        t = _fraction(entry["t"], f"square {index} t")
        squares.append(_corners(x, y, t))

    failures = [
        failure
        for index, square in enumerate(squares, start=1)
        for failure in square_failures(square, index)
    ]
    if any(
        coordinate < 0 or coordinate > side
        for square in squares
        for point in square
        for coordinate in point
    ):
        failures.append("square outside container")
    if any(pair_gap(left, right) < 0 for left, right in itertools.combinations(squares, 2)):
        failures.append("squares overlap")
    if failures:
        raise HalfAngleImportError(
            "independent corner check failed: " + "; ".join(failures[:3])
        )

    return {
        "id": f"W-imported-half-angle-n{expected_n:03d}",
        "n": expected_n,
        "side": _literal(side),
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": index,
                "corners": [[_literal(x), _literal(y)] for x, y in square],
            }
            for index, square in enumerate(squares, start=1)
        ],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": (
                "Exact feasible upper bound only; no optimality or algebraic endpoint claim."
            ),
        },
        "source": {"path": _source_path(source)},
        "certificate": {
            "kind": "exact-rational-sat",
            "replay": "Run the independent rational-corner checker on this witness.",
        },
    }


def _validate_paths(source: Path, output: Path) -> None:
    if source.resolve() == output.resolve():
        raise HalfAngleImportError("source and output paths must differ")
    if output.exists():
        raise HalfAngleImportError("output already exists")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("source", type=Path)
    parser.add_argument("--expected-n", type=int, required=True)
    parser.add_argument("--expected-side", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        _validate_paths(args.source, args.output)
        witness = import_source(
            args.source, expected_n=args.expected_n, expected_side=args.expected_side
        )
        witness["certificate"]["replay"] = (
            ".venv/bin/python3 -m devtools.check_rational_witness_independent "
            + shlex.quote(str(args.output))
        )
        schema = Path(os.path.relpath(WITNESS_SCHEMA, args.output.parent.resolve())).as_posix()
        with atomic_output_file(args.output) as temporary:
            temporary.write_text(witness_document(witness, schema=schema), encoding="utf-8")
    except (HalfAngleImportError, OSError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(f"IMPORTED: {witness['n']} exact unit squares at side {witness['side']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
