"""Replay the frozen exact n = 19 Q(sqrt(2)) control for BC-118.

The control calls the retained builder and exact-sign verifier unchanged. It has no
n = 50 source, witness, geometry, or reconstruction dependency.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from cases.lifted_q2.packing import build
from sqpack.verify import exact_sign, verify_packing

PACKING_ROOT = Path(__file__).resolve().parents[2]
CONTROL_N = 19
EXPECTED_PAIR_COUNT = CONTROL_N * (CONTROL_N - 1) // 2
MUTATED_N = CONTROL_N + 1
EXPECTED_MUTATION_PAIR_COUNT = MUTATED_N * (MUTATED_N - 1) // 2
EXPECTED_SIDE_TEXT = "poly[3,4/3]"
CONTROL_INPUTS = (
    (
        "cases/lifted_q2/packing.py",
        "0e1cbf5b7eacb9e9c354aa9dab7f835097885c0b8ddc54ff6ad0eb62febc8a78",
    ),
    (
        "cases/lifted_q2/verify_exact.py",
        "8019f856856be7d81a9a0a6b9aa2afd1aa9faabb3aa270677e3123eadfb7f2f3",
    ),
)


class ControlError(RuntimeError):
    """The frozen control or its duplicate-square mutation failed."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verify_inputs() -> None:
    for relative, expected in CONTROL_INPUTS:
        observed = _sha256(PACKING_ROOT / relative)
        if observed != expected:
            raise ControlError(
                f"frozen control input changed: {relative}: expected {expected}, got {observed}"
            )


def run_control() -> dict[str, Any]:
    """Run the n = 19 exact control and duplicate-square rejection once."""

    _verify_inputs()
    squares, side, field = build(CONTROL_N)
    expected_side = field.rational(3) + field.rational(Fraction(4, 3)) * field.alpha
    if len(squares) != CONTROL_N:
        raise ControlError(f"build(19) returned {len(squares)} squares")
    if side != expected_side or side.text() != EXPECTED_SIDE_TEXT:
        raise ControlError(f"side mismatch: expected {EXPECTED_SIDE_TEXT}, got {side.text()}")

    report = verify_packing(squares, side, sign=exact_sign)
    if not report.valid or report.n != CONTROL_N:
        raise ControlError("exact-sign verifier rejected the n = 19 control")
    if report.pairs_tested != EXPECTED_PAIR_COUNT:
        raise ControlError(
            f"expected {EXPECTED_PAIR_COUNT} unordered pairs, got {report.pairs_tested}"
        )

    duplicate = verify_packing([*squares, squares[0]], side, sign=exact_sign)
    if duplicate.valid:
        raise ControlError("exact-sign verifier accepted the duplicated first square")
    if duplicate.n != MUTATED_N or duplicate.pairs_tested != EXPECTED_MUTATION_PAIR_COUNT:
        raise ControlError("duplicate-square mutation did not test every unordered pair")

    return {
        "schema_version": 1,
        "control": "lifted-q2-n19-exact-sign",
        "control_inputs": [
            {"path": relative, "sha256": expected} for relative, expected in CONTROL_INPUTS
        ],
        "requested_n": CONTROL_N,
        "build_call": "build(19)",
        "expected_side": {
            "field": "Q(sqrt(2))",
            "power_basis_coefficients": ["3", "4/3"],
            "serialized": EXPECTED_SIDE_TEXT,
        },
        "observed_side": {
            "power_basis_coefficients": [str(coefficient) for coefficient in side.coeffs],
            "serialized": side.text(),
            "equals_expected": side == expected_side,
        },
        "verification": {
            "assurance": "exact-sign",
            "valid": report.valid,
            "observed_n": report.n,
            "pair_semantics": "all-unordered-pairs",
            "expected_pairs": EXPECTED_PAIR_COUNT,
            "observed_pairs": report.pairs_tested,
        },
        "mutation": {
            "kind": "append-duplicate-of-square-1",
            "duplicated_index_one_based": 1,
            "expected_valid": False,
            "observed_valid": duplicate.valid,
            "observed_n": duplicate.n,
            "expected_pairs": EXPECTED_MUTATION_PAIR_COUNT,
            "observed_pairs": duplicate.pairs_tested,
            "failure_kinds": sorted({kind for kind, _detail in duplicate.failures}),
        },
        "skip_count": 0,
    }


def _canonical_receipt(receipt: dict[str, Any]) -> str:
    return json.dumps(receipt, indent=2, sort_keys=True) + "\n"


def write_new_receipt(path: Path, receipt: dict[str, Any]) -> None:
    """Atomically create a receipt without replacing an existing artifact."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(_canonical_receipt(receipt))
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError as error:
            raise ControlError(f"receipt already exists: {path}") from error
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        temporary.unlink(missing_ok=True)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True)
    arguments = parser.parse_args(argv)
    write_new_receipt(arguments.record, run_control())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
