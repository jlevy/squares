"""Compare the n259 submission and T-193 using the maintained identity measures."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import measure_identity
from devtools.check_rational_witness_independent import parse
from sqpack.field import FieldElement
from sqpack.witness import load_witness, materialize_exact_witness

PACKET = Path(__file__).resolve().parent
REPO = PACKET.parents[3]
HOUSE = REPO / "packing/witnesses/known-best/n-259.yaml"
CANDIDATE = PACKET / "source/upper/n259/witness.yaml"


def midpoint(value: Any) -> Fraction:
    """Project a field element by the midpoint of its refined rational enclosure."""
    if isinstance(value, FieldElement):
        low, high = value.field.enclose(value)
        return (low + high) / 2
    return Fraction(value)


def placed(square: Any) -> measure_identity.Placed:
    points = [(midpoint(x), midpoint(y)) for x, y in square]
    return (
        sum((x for x, _ in points), Fraction(0)) / 4,
        sum((y for _, y in points), Fraction(0)) / 4,
        points[1][0] - points[0][0],
        points[1][1] - points[0][1],
    )


def source(path: Path, method: str) -> dict[str, str]:
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "geometry": method,
    }


def main() -> None:
    house_squares, house_side = materialize_exact_witness(load_witness(HOUSE))
    candidate_squares, candidate_side = parse(CANDIDATE)
    candidate = measure_identity.Packing(
        "issue-1040",
        source(CANDIDATE, "Exact rational corners"),
        candidate_side,
        tuple(map(placed, candidate_squares)),
    )
    projections = {}
    for digits in (40, 60):
        if not isinstance(house_side, FieldElement):
            raise TypeError("This comparison expects the pinned number-field house")
        house_side.field.refine_to(digits)
        house = measure_identity.Packing(
            "T-193",
            source(HOUSE, f"Rational interval midpoint after refinement to {digits} places"),
            midpoint(house_side),
            tuple(map(placed, house_squares)),
        )
        projections[str(digits)] = measure_identity.receipt(259, candidate, [house])
    exact_tilts = {
        label: sum(
            square[0][0] != square[1][0] and square[0][1] != square[1][1] for square in squares
        )
        for label, squares in (("issue-1040", candidate_squares), ("T-193", house_squares))
    }
    result = {
        "format": "issue-1040-house-identity-v1",
        "exact_non_axis_counts": exact_tilts,
        "projection_comparisons": projections,
    }
    (PACKET / "receipts/identity-t193.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
