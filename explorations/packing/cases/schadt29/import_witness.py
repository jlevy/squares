#!/usr/bin/env python3
"""Convert the Schadt n=29 text format into the generic Witness/v2 boundary."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from strif import atomic_output_file

from sqpack.witness import witness_document

SIDE_RE = re.compile(r"^Final s:\s*(\S+)\s*$", re.MULTILINE)
SQUARE_RE = re.compile(
    r"^Square\s+(?P<id>\d+):\s*x=(?P<x>[^,]+),\s*"
    r"y=(?P<y>[^,]+),\s*deg=(?P<angle>\S+)\s*$",
    re.MULTILINE,
)
SOURCE_URL = "https://github.com/BalthasarStrauss/Squares-packing_S-29-_New-Record"


def parse_source(path: Path) -> dict:
    """Parse the complete first-party source and reject incomplete or duplicate input."""
    text = path.read_text(encoding="utf-8")
    side_match = SIDE_RE.search(text)
    if side_match is None:
        raise ValueError("source has no Final s value")
    squares = [
        {
            "id": int(match.group("id")),
            "center": [match.group("x").strip(), match.group("y").strip()],
            "angle": match.group("angle").strip(),
        }
        for match in SQUARE_RE.finditer(text)
    ]
    ids = [square["id"] for square in squares]
    if len(squares) != 29 or sorted(ids) != list(range(1, 30)):
        raise ValueError(f"expected ids 1..29 exactly once, found {ids}")
    return {
        "id": "W-schadt-n029-2025-decimal",
        "n": 29,
        "side": side_match.group(1),
        "square_size": "1",
        "representation": "center-angle",
        "scalar": {"kind": "decimal"},
        "coordinates": {
            "origin": "container-center",
            "axes": "x-right-y-up",
            "angle_unit": "degrees",
        },
        "squares": squares,
        "claim": {
            "coordinate_provenance": "reported",
            "method": "numerical-multiprecision",
            "precision": {"decimal_digits": 300, "rounding": "decimal-context"},
            "tolerance": "1e-100",
            "limitations": (
                "The source checker accepts overlaps within 1e-100 and does not enforce "
                "the square count. This serialized pose is numerical evidence, not a "
                "formal feasibility or optimality certificate."
            ),
        },
        "source": {
            "key": "[Schadt n=29 repository]",
            "path": str(path),
            "url": SOURCE_URL,
            "retrieved": "2026-08-25",
        },
        "certificate": None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    with atomic_output_file(args.output) as temporary:
        temporary.write_text(witness_document(parse_source(args.source)), encoding="utf-8")
    print(f"imported complete n=29 source geometry to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
