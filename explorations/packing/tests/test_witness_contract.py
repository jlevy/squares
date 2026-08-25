#!/usr/bin/env python3
"""Behavior and regression checks for the generic Witness/v1 command boundary."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory

from cases.schadt29.import_witness import parse_source
from devtools.check_rational_witness_independent import check as independent_check
from sqpack.witness import (
    WitnessError,
    check_witness_semantics,
    exact_verify,
    inspect_witness,
    load_witness,
    numerical_check,
    promote_rational,
)

ROOT = Path(__file__).resolve().parent.parent
WITNESSES = ROOT / "witnesses"


def main() -> int:
    grid = load_witness(WITNESSES / "grid-n004.yaml")
    grid_result, grid_report = exact_verify(grid)
    assert grid_report.valid and grid_result["assurance"] == "verified"

    algebraic = load_witness(WITNESSES / "rotated-n001-sqrt2.yaml")
    algebraic_result, algebraic_report = exact_verify(algebraic)
    assert algebraic_report.valid and algebraic_result["assurance"] == "verified"
    assert algebraic_result["field_certificate"]["irreducible_over_q"] is True
    inspected = inspect_witness(algebraic)
    assert inspected["assurance_conclusion"] == "none"
    assert inspected["bounding_box"]["min_x"] == "0.0"
    algebraic_numeric, algebraic_numeric_report = numerical_check(
        algebraic,
        method="numerical-multiprecision",
        precision=80,
        tolerance="1e-70",
    )
    assert algebraic_numeric_report.valid
    assert algebraic_numeric["assurance"] == "numerically-checked"

    overlap = load_witness(WITNESSES / "overlap-negative-control.yaml")
    overlap_result, overlap_report = exact_verify(overlap)
    assert not overlap_report.valid and overlap_result["assurance"] == "not-established"
    assert not independent_check(WITNESSES / "overlap-negative-control.yaml")[
        "verification_passed"
    ]

    incomplete = deepcopy(grid)
    incomplete["squares"] = incomplete["squares"][:-1]
    assert any(
        "artifact contains 3 squares" in problem
        for problem in check_witness_semantics(incomplete)
    )
    duplicated = deepcopy(grid)
    duplicated["squares"][1]["id"] = duplicated["squares"][0]["id"]
    assert "square ids must be unique" in check_witness_semantics(duplicated)

    decimal = load_witness(WITNESSES / "schadt-n029-2025-decimal.yaml")
    mislabeled_decimal = deepcopy(decimal)
    mislabeled_decimal["claim"]["assurance"] = "verified"
    mislabeled_decimal["claim"]["method"] = "exact-algebraic"
    assert any(
        "require rational or algebraic scalar data" in problem
        for problem in check_witness_semantics(mislabeled_decimal)
    )
    numeric, numeric_report = numerical_check(
        decimal,
        method="numerical-multiprecision",
        precision=300,
        tolerance="1e-100",
    )
    assert numeric_report.valid and numeric["assurance"] == "numerically-checked"
    minimum_gap = Fraction(numeric["minimum_best_pair_gap"])
    assert Fraction(-1, 10**100) < minimum_gap < 0
    try:
        exact_verify(decimal)
    except WitnessError as error:
        assert error.kind == "formal-certificate-missing"
    else:
        raise AssertionError("decimal witness was accepted as formal evidence")

    for method, precision, tolerance in (
        ("numerical-f64", 64, "1e-12"),
        ("numerical-f64", 53, "-1e-12"),
        ("numerical-multiprecision", 0, "1e-12"),
    ):
        try:
            numerical_check(
                decimal,
                method=method,
                precision=precision,
                tolerance=tolerance,
            )
        except WitnessError as error:
            assert error.kind == "malformed-option"
        else:
            raise AssertionError(f"accepted invalid numerical profile {method}")

    promoted_result, generated = promote_rational(
        decimal,
        rational_digits=16,
        max_side_increase="0.000001",
        source_path="witnesses/schadt-n029-2025-decimal.yaml",
        replay_path="witnesses/schadt-n029-2025-rational.yaml",
    )
    retained = load_witness(WITNESSES / "schadt-n029-2025-rational.yaml")
    assert generated == retained
    assert promoted_result["assurance"] == "verified"
    promoted_side = Fraction(generated["side"])
    assert Fraction(decimal["side"]) < promoted_side < Fraction("5.9343418049")
    assert independent_check(WITNESSES / "schadt-n029-2025-rational.yaml")[
        "verification_passed"
    ]
    assert generated["certificate"]["replay"].endswith(
        "witnesses/schadt-n029-2025-rational.yaml"
    )

    with TemporaryDirectory() as directory:
        duplicated_yaml = Path(directory) / "duplicate-key.yaml"
        duplicated_yaml.write_text(
            (WITNESSES / "grid-n004.yaml")
            .read_text(encoding="utf-8")
            .replace("  n: 4\n", "  n: 4\n  n: 5\n", 1),
            encoding="utf-8",
        )
        try:
            load_witness(duplicated_yaml)
        except WitnessError as error:
            assert error.kind == "malformed-input"
            assert "duplicate key 'n'" in str(error)
        else:
            raise AssertionError("witness loader silently overwrote a duplicate key")

        truncated = Path(directory) / "truncated.txt"
        source_lines = (ROOT / "resources/web/schadt-s29-2025/squares.txt").read_text(
            encoding="utf-8"
        )
        truncated.write_text("\n".join(source_lines.splitlines()[:3]), encoding="utf-8")
        try:
            parse_source(truncated)
        except ValueError as error:
            assert "expected ids 1..29" in str(error)
        else:
            raise AssertionError("source adapter accepted incomplete geometry")

    print("witness interchange and promotion contract selftest passed")
    return 0


def test_witness_contract() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
