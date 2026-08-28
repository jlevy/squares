#!/usr/bin/env python3
"""Generate the exact-rational known-best n=11 robustification control."""

from __future__ import annotations

import argparse
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml
from strif import atomic_output_file

from sqpack.witness import load_witness, promote_rational, witness_document

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "witnesses/known-best/n-011.yaml"
OUTPUT = ROOT / "witnesses/known-best-n011-rational-control.yaml"
SOURCE_PATH = "witnesses/known-best/n-011.yaml"
REPLAY_PATH = "witnesses/known-best-n011-rational-control.yaml"
RATIONAL_DIGITS = 36
MAX_SIDE_INCREASE = "1e-8"
EXPECTED_LIMITATIONS = (
    "Exact feasible upper-bound witness derived by rational robustification; "
    "does not establish global optimality or certify the original decimal pose."
)


def expected_witness() -> dict[str, Any]:
    """Recompute the frozen rational control from the retained decimal source."""
    source = load_witness(SOURCE)
    result, promoted = promote_rational(
        source,
        rational_digits=RATIONAL_DIGITS,
        max_side_increase=MAX_SIDE_INCREASE,
        source_path=SOURCE_PATH,
        replay_path=REPLAY_PATH,
    )
    if result["status"] != "certificate-produced":
        raise AssertionError("n=11 robustification did not produce a certificate")
    if result["pairs_tested"] != 55:
        raise AssertionError("n=11 robustification did not test all 55 pairs")
    if [square["id"] for square in promoted["squares"]] != list(range(1, 12)):
        raise AssertionError("n=11 robustification did not retain ids 1..11")
    if promoted["claim"]["limitations"] != EXPECTED_LIMITATIONS:
        raise AssertionError("n=11 robustification widened its claim boundary")
    return promoted


def expected_text() -> str:
    """Return the byte-stable Witness/v2 control document."""
    return witness_document(expected_witness())


def validate_document(document: Mapping[str, Any]) -> None:
    """Reject stale content or any mutation of the frozen control contract."""
    expected = yaml.safe_load(expected_text())
    if document != expected:
        raise ValueError(
            "known-best n=11 rational control does not match its generated contract"
        )


def update() -> None:
    text = expected_text()
    validate_document(yaml.safe_load(text))
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(text, encoding="utf-8")
    print("known-best n=11 rational control updated")


def check() -> None:
    text = expected_text()
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != text:
        raise ValueError(f"{OUTPUT.relative_to(ROOT)} is stale")
    retained = yaml.safe_load(text)
    validate_document(retained)
    if load_witness(OUTPUT) != retained["witness"]:
        raise ValueError("known-best n=11 rational control failed Witness/v2 validation")
    print("known-best n=11 rational control check passed")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.update:
        update()
    else:
        check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
