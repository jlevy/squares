"""Regression checks for the generated n=11 robust-rational control."""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from pathlib import Path

import pytest
import yaml

from devtools.check_rational_witness_independent import check as independent_check
from devtools.check_rational_witness_independent import parse as independent_parse
from devtools.generate_known_best_n011_rational_control import (
    EXPECTED_LIMITATIONS,
    MAX_SIDE_INCREASE,
    OUTPUT,
    RATIONAL_DIGITS,
    SOURCE,
    expected_text,
    validate_document,
)
from sqpack.witness import WitnessError, exact_verify, load_witness, promote_rational


def _write_document(path: Path, document: dict[str, object]) -> None:
    path.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")


def test_retained_control_is_current_and_exactly_replayable() -> None:
    assert OUTPUT.read_text(encoding="utf-8") == expected_text()
    witness = load_witness(OUTPUT)
    result, report = exact_verify(witness)
    independent = independent_check(OUTPUT)

    assert report.valid
    assert result["verification_passed"]
    assert result["n"] == 11
    assert result["pairs_tested"] == 55
    assert independent["verification_passed"]
    assert independent["n"] == 11
    assert independent["pairs_tested"] == 55
    assert [square["id"] for square in witness["squares"]] == list(range(1, 12))


def test_relaxation_and_claim_boundary_are_frozen() -> None:
    source = load_witness(SOURCE)
    witness = load_witness(OUTPUT)
    source_side = Fraction(source["side"])
    promoted_side = Fraction(witness["side"])

    assert source_side < promoted_side <= source_side + Fraction(MAX_SIDE_INCREASE)
    assert witness["certificate"]["rational_digits"] == RATIONAL_DIGITS
    assert witness["certificate"]["pairs_tested"] == 55
    assert witness["certificate"]["derived_from"] == source["id"]
    assert witness["certificate"]["replay"] == (
        "uv run --frozen packing-witness verify witnesses/known-best-n011-rational-control.yaml"
    )
    assert witness["claim"]["limitations"] == EXPECTED_LIMITATIONS


def test_zero_relaxation_is_a_typed_refusal() -> None:
    source = load_witness(SOURCE)
    with pytest.raises(WitnessError, match="no exact rational candidate") as caught:
        promote_rational(
            source,
            rational_digits=RATIONAL_DIGITS,
            max_side_increase="0",
            source_path="witnesses/known-best/n-011.yaml",
            replay_path="unused.yaml",
        )
    assert caught.value.kind == "robustification-failed"


def test_incomplete_and_overlapping_mutations_reject(tmp_path: Path) -> None:
    document = yaml.safe_load(OUTPUT.read_text(encoding="utf-8"))
    incomplete = deepcopy(document)
    incomplete["witness"]["squares"].pop()
    incomplete_path = tmp_path / "incomplete.yaml"
    _write_document(incomplete_path, incomplete)
    with pytest.raises(ValueError, match="complete square list"):
        independent_parse(incomplete_path)
    with pytest.raises(WitnessError, match="artifact contains 10 squares"):
        load_witness(incomplete_path, fallback_schema=OUTPUT.parent / "witness.schema.yaml")

    overlapping = deepcopy(document)
    overlapping["witness"]["squares"][1]["corners"] = deepcopy(
        overlapping["witness"]["squares"][0]["corners"]
    )
    overlapping_path = tmp_path / "overlapping.yaml"
    _write_document(overlapping_path, overlapping)
    assert not independent_check(overlapping_path)["verification_passed"]
    overlap_witness = load_witness(
        overlapping_path, fallback_schema=OUTPUT.parent / "witness.schema.yaml"
    )
    assert not exact_verify(overlap_witness)[1].valid


def test_shape_and_containment_mutations_reject(tmp_path: Path) -> None:
    document = yaml.safe_load(OUTPUT.read_text(encoding="utf-8"))
    malformed = deepcopy(document)
    malformed["witness"]["squares"][0]["corners"][1][0] = "1000001/1000000"
    malformed_path = tmp_path / "malformed-square.yaml"
    _write_document(malformed_path, malformed)
    assert not independent_check(malformed_path)["verification_passed"]
    malformed_witness = load_witness(
        malformed_path, fallback_schema=OUTPUT.parent / "witness.schema.yaml"
    )
    assert not exact_verify(malformed_witness)[1].valid

    too_small = deepcopy(document)
    too_small["witness"]["side"] = str(Fraction(too_small["witness"]["side"]) - 1)
    too_small_path = tmp_path / "too-small.yaml"
    _write_document(too_small_path, too_small)
    assert not independent_check(too_small_path)["verification_passed"]
    too_small_witness = load_witness(
        too_small_path, fallback_schema=OUTPUT.parent / "witness.schema.yaml"
    )
    assert not exact_verify(too_small_witness)[1].valid


def test_claim_widening_is_stale_generated_content() -> None:
    document = yaml.safe_load(OUTPUT.read_text(encoding="utf-8"))
    document["witness"]["claim"]["limitations"] = "Proves the source pose optimal."
    with pytest.raises(ValueError, match="generated contract"):
        validate_document(document)


def test_scope_and_certificate_mutations_are_stale_generated_content() -> None:
    document = yaml.safe_load(OUTPUT.read_text(encoding="utf-8"))
    smaller = deepcopy(document)
    smaller["witness"]["squares"].pop()
    smaller["witness"]["n"] = 10
    smaller["witness"]["certificate"]["pairs_tested"] = 45
    with pytest.raises(ValueError, match="generated contract"):
        validate_document(smaller)

    wrong_derivation = deepcopy(document)
    wrong_derivation["witness"]["certificate"]["derived_from"] = "W-trump-algebraic"
    with pytest.raises(ValueError, match="generated contract"):
        validate_document(wrong_derivation)
