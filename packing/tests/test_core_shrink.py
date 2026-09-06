"""A smaller core can remain usable below mass one, after exact normalization."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.core_shrink import evaluate, publish
from devtools.decide_certificate import decide, load

PACKING = Path(__file__).resolve().parents[1]


def source_bytes() -> bytes:
    record = {
        "id": "test-core-shrink",
        "n": 2,
        "claim": "s(2) >= 1",
        "outer_side": "1",
        "square_side": "7/10",
        "angle_limit": "1/2",
        "direction_steps": 2,
        "total_mass": "53/50",
        "least_cell_mass": "53/50",
        "symmetry": "D4",
        "atoms": [
            ["1/2", "1/2", "9/10"],
            ["2/5", "1/2", "1/25"],
            ["3/5", "1/2", "1/25"],
            ["1/2", "2/5", "1/25"],
            ["1/2", "3/5", "1/25"],
        ],
    }
    return json.dumps(record).encode()


def test_subunit_minimum_normalizes_to_a_standard_certificate(tmp_path: Path) -> None:
    result, candidate = evaluate(
        source_bytes(), square_side=Fraction(11, 20), factor=Fraction(6, 5), workers=1
    )
    assert result["outcome"] == "candidate_constructed"
    minimum = Fraction(str(result["minimum_mass"]))
    assert Fraction(53, 100) < minimum < 1
    assert candidate is not None
    assert Fraction(str(candidate["total_mass"])) == Fraction(53, 50) / minimum
    output = tmp_path / "result"
    publish(output, result, candidate)
    certificate, saved = load(output / "candidate.json")
    assert certificate.outer_side == Fraction(6, 5)
    assert certificate.square_side == Fraction(33, 50)
    assert saved["least_cell_mass"] == "1"
    assert decide(output / "candidate.json", quick=False)
    with pytest.raises(FileExistsError):
        publish(output, result, candidate)


def test_failure_keeps_a_witness_and_emits_no_certificate(tmp_path: Path) -> None:
    result, candidate = evaluate(
        source_bytes(), square_side=Fraction(2, 5), factor=Fraction(6, 5), workers=1
    )
    assert result["outcome"] == "criterion_missed"
    assert result["minimum_mass"] == "0"
    assert result["witness_closed_mass"] == "0"
    assert candidate is None
    output = tmp_path / "failed"
    publish(output, result, candidate)
    assert (output / "result.json").is_file()
    assert not (output / "candidate.json").exists()


def test_source_identity_and_declarations_are_checked() -> None:
    original = source_bytes()
    mutated = original.replace(b'"n": 2', b'"n": 1')
    with pytest.raises(ValueError, match="source"):
        evaluate(mutated, square_side=Fraction(11, 20), factor=Fraction(6, 5), workers=1)
    duplicate = original.replace(b'"n": 2', b'"n": 2, "n": 1')
    with pytest.raises(ValueError, match="duplicate"):
        evaluate(duplicate, square_side=Fraction(11, 20), factor=Fraction(6, 5), workers=1)
    stale = original.replace(b'"total_mass": "53/50"', b'"total_mass": "1"')
    with pytest.raises(ValueError, match="source declaration"):
        evaluate(stale, square_side=Fraction(11, 20), factor=Fraction(6, 5), workers=1)


def test_invalid_shrink_and_dilation_fail_before_replay() -> None:
    with pytest.raises(ValueError, match="strictly smaller"):
        evaluate(source_bytes(), square_side=Fraction(7, 10), factor=Fraction(1), workers=1)
    with pytest.raises(ValueError, match="containment"):
        evaluate(source_bytes(), square_side=Fraction(11, 20), factor=Fraction(2), workers=1)


def test_exp110_corner_obstruction_replays_without_the_sweep() -> None:
    receipt = json.loads(
        (
            PACKING / "campaign/series/series-000-smoke-and-calibration/results/"
            "exp-110-h-090-core-shrink/result.json"
        ).read_text()
    )
    raw = (PACKING / "cases/n11_fractional_certificate/certificate.json").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == receipt["source_sha256"]
    atoms = [tuple(map(Fraction, atom)) for atom in json.loads(raw)["atoms"]]
    edge = Fraction(receipt["witness_admissible_up_to_side"])
    center = edge / 2
    below = sum(
        (weight for x, y, weight in atoms if max(abs(x - center), abs(y - center)) < center),
        start=Fraction(0),
    )
    at = sum(
        (weight for x, y, weight in atoms if max(abs(x - center), abs(y - center)) <= center),
        start=Fraction(0),
    )
    assert below == Fraction(receipt["minimum_mass"]) == Fraction(85353, 100000)
    assert below < Fraction(receipt["threshold_mass"])
    assert at - below == Fraction(917, 6250)
    assert at == Fraction(receipt["source_minimum_mass"])
    squared = Fraction(receipt["source_refined_limit_squared"])
    proposed = Fraction(receipt["proposed_side"])
    assert proposed - Fraction(1, 100000) > 0
    assert (proposed - Fraction(1, 100000)) ** 2 > squared
