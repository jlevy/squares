#!/usr/bin/env python3
"""Behavior and regression checks for the generic Witness/v2 command boundary."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import yaml

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
    validate_witness_document,
    witness_document,
    witness_envelope,
)
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
WITNESSES = ROOT / "witnesses"


def main() -> int:
    grid = load_witness(WITNESSES / "grid-n004.yaml")
    grid_result, grid_report = exact_verify(grid)
    assert grid_report.valid
    assert grid_result["coordinate_provenance"] == "verified"

    algebraic = load_witness(WITNESSES / "rotated-n001-sqrt2.yaml")
    algebraic_result, algebraic_report = exact_verify(algebraic)
    assert algebraic_report.valid
    assert algebraic_result["coordinate_provenance"] == "verified"
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
    assert algebraic_numeric["coordinate_provenance"] == "numerically-checked"

    overlap = load_witness(WITNESSES / "overlap-negative-control.yaml")
    overlap_result, overlap_report = exact_verify(overlap)
    assert not overlap_report.valid
    assert overlap_result["coordinate_provenance"] == "not-established"
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
    mislabeled_decimal["claim"]["coordinate_provenance"] = "verified"
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
    assert numeric_report.valid
    assert numeric["coordinate_provenance"] == "numerically-checked"
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
        rational_digits=36,
        max_side_increase="0.000001",
        source_path="witnesses/schadt-n029-2025-decimal.yaml",
        replay_path="witnesses/schadt-n029-2025-rational.yaml",
    )
    retained = load_witness(WITNESSES / "schadt-n029-2025-rational.yaml")
    assert generated == retained
    assert promoted_result["coordinate_provenance"] == "verified"
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

        retired_name = Path(directory) / "retired-assurance.yaml"
        retired_name.write_text(
            (WITNESSES / "grid-n004.yaml")
            .read_text(encoding="utf-8")
            .replace("    coordinate_provenance:", "    assurance:", 1),
            encoding="utf-8",
        )
        try:
            load_witness(retired_name, fallback_schema=WITNESSES / "witness.schema.yaml")
        except WitnessError as error:
            assert error.kind == "schema-invalid"
            assert str(error).startswith("claim:")
        else:
            raise AssertionError("witness loader accepted the retired claim.assurance name")

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


@pytest.mark.parametrize(
    "name", ["grid-n004.yaml", "rotated-n001-sqrt2.yaml", "schadt-n029-2025-decimal.yaml"]
)
def test_parsed_document_preserves_typed_file_admission(tmp_path: Path, name: str) -> None:
    retained = load_witness(WITNESSES / name)
    retained.setdefault("certificate", {})["typed_payload"] = {
        "boolean": True,
        "integer": 4,
        "float": 4.25,
        "null": None,
        "sequence": ["1/2", False, 0],
    }
    schema = (WITNESSES / "witness.schema.yaml").as_posix()
    document = witness_envelope(retained, schema=schema)
    path = tmp_path / name
    path.write_text(witness_document(retained, schema=schema))
    serialized = load_yaml(path.read_text())
    assert serialized == document
    assert validate_witness_document(document, path=path) == load_witness(path) == retained
    document["witness"]["certificate"]["typed_payload"]["sequence"].append("changed")
    assert retained["certificate"]["typed_payload"]["sequence"] == ["1/2", False, 0]


@pytest.mark.parametrize(
    "mutation",
    [
        "document-type",
        "witness-type",
        "contract",
        "boolean-n",
        "string-n",
        "numeric-side",
        "numeric-coordinate",
        "retired-claim",
        "duplicate-id",
        "wrong-count",
        "angle-unit",
        "unsupported-field",
    ],
)
def test_parsed_document_rejects_the_same_invalid_file(tmp_path: Path, mutation: str) -> None:
    schema = (WITNESSES / "witness.schema.yaml").as_posix()
    document = witness_envelope(load_witness(WITNESSES / "grid-n004.yaml"), schema=schema)
    witness = document["witness"]
    if mutation == "document-type":
        document = None
    elif mutation == "witness-type":
        document["witness"] = []
    elif mutation == "contract":
        document["softschema"]["contract"] = "retired-contract"
    elif mutation == "boolean-n":
        witness["n"] = True
    elif mutation == "string-n":
        witness["n"] = "4"
    elif mutation == "numeric-side":
        witness["side"] = 2.0
    elif mutation == "numeric-coordinate":
        witness["squares"][0]["corners"][0][0] = 0.0
    elif mutation == "retired-claim":
        witness["claim"]["assurance"] = witness["claim"].pop("coordinate_provenance")
    elif mutation == "duplicate-id":
        witness["squares"][1]["id"] = witness["squares"][0]["id"]
    elif mutation == "wrong-count":
        witness["n"] = 3
    elif mutation == "angle-unit":
        witness["coordinates"]["angle_unit"] = "radians"
    else:
        witness["unexpected"] = "not part of Witness/v2"
    path = tmp_path / "invalid.yaml"
    path.write_text(yaml.safe_dump(document, sort_keys=False))
    with pytest.raises(WitnessError) as direct:
        validate_witness_document(document, path=path)
    with pytest.raises(WitnessError) as loaded:
        load_witness(path)
    assert (direct.value.kind, str(direct.value)) == (loaded.value.kind, str(loaded.value))


def test_parsed_document_keeps_schema_fallback_and_strict_file_duplicates(
    tmp_path: Path,
) -> None:
    schema = WITNESSES / "witness.schema.yaml"
    witness = load_witness(WITNESSES / "grid-n004.yaml")
    document = witness_envelope(witness, schema="absent.schema.yaml")
    path = tmp_path / "fallback.yaml"
    path.write_text(witness_document(witness, schema="absent.schema.yaml"))
    assert validate_witness_document(document, path=path, fallback_schema=schema) == witness
    assert load_witness(path, fallback_schema=schema) == witness
    path.write_text(path.read_text().replace("  n: 4\n", "  n: 4\n  n: 5\n", 1))
    with pytest.raises(WitnessError, match="duplicate key 'n'") as failure:
        load_witness(path, fallback_schema=schema)
    assert failure.value.kind == "malformed-input"
