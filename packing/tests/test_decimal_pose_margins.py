"""`devtools.decimal_pose_margins` measures decimal poses rigorously and refuses the rest."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import decimal_pose_margins as margins
from devtools.decimal_pose_margins import (
    PoseError,
    ceiling,
    check,
    decimal_text,
    measure,
    parse_pose,
)

#: Four axis-aligned unit squares filling a box of side 2: every pair touches.
GRID = """s: 2.0

Square 1: x=-0.5, y=-0.5, deg=0.0
Square 2: x=0.5, y=-0.5, deg=0.0
Square 3: x=-0.5, y=0.5, deg=0.0
Square 4: x=0.5, y=0.5, deg=0.0
"""


def _pair(overlap: str, side: str = "2.0") -> str:
    """Two axis-aligned squares whose interiors overlap by ``overlap`` along x."""
    half = Fraction(overlap) / 2
    left, right = Fraction(-1, 2) + half, Fraction(1, 2) - half
    return (
        f"s: {side}\n"
        f"Square 1: x={decimal_text(left, 20)}, y=0, deg=0\n"
        f"Square 2: x={decimal_text(right, 20)}, y=0, deg=0\n"
    )


def _write(tmp_path: Path, name: str, text: str) -> str:
    (tmp_path / name).write_text(text, encoding="utf-8")
    return name


def _row(tmp_path: Path, text: str, **target: Any) -> dict[str, Any]:
    name = _write(tmp_path, "pose.txt", text)
    receipt = measure(tmp_path, [name], **target)
    return receipt["files"][0]


def test_parses_both_export_variants() -> None:
    pose = parse_pose(
        "Final s: 3.5\n\nSquare 0: x=-1.25 y=0.5 deg=-12.5\nSquare 1: x=1, y=-1e-3, deg=45,\n"
    )
    assert pose.side == Fraction(7, 2)
    assert [square.label for square in pose.squares] == [0, 1]
    assert pose.squares[1].y == Fraction(-1, 1000)
    assert pose.squares[0].degrees == Fraction(-25, 2)


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("Square 1: x=0, y=0, deg=0\n", "states no side"),
        ("s: 2\n", "states no square"),
        ("s: 0\nSquare 1: x=0, y=0, deg=0\n", "must be positive"),
        ("s: 2\nSquare 1: x=0, y=0, deg=0\nSquare 1: x=1, y=0, deg=0\n", "appears twice"),
        ("s: 2\nSquare 1: x=0, y=nan, deg=0\n", "neither the side nor a square"),
        ("s: 2\nSquare 1: x=0, y=0, deg=0\ns: 3\n", "a second side line"),
        ("s: 2\n# a comment\nSquare 1: x=0, y=0, deg=0\n", "neither the side nor a square"),
    ],
)
def test_refuses_malformed_poses(text: str, reason: str) -> None:
    with pytest.raises(PoseError, match=reason):
        parse_pose(text)


def test_ceiling_rounds_up_only() -> None:
    assert ceiling(Fraction("9.6979347990169860"), 12) == Fraction("9.697934799017")
    assert ceiling(Fraction("2.5"), 12) == Fraction("2.5")


def test_touching_grid_is_a_packing_with_exact_zero_margins(tmp_path: Path) -> None:
    row = _row(tmp_path, GRID, places=12)
    printed = row["at_printed_side"]
    assert printed["verdict"] == "packing"
    assert printed["least_pair_separation"] == ["0", "0"]
    assert printed["least_wall_clearance"] == ["0", "0"]
    assert printed["pairs_touching"] == 6
    assert row["near_pairs"] == 6
    assert row["dilation"] == "1"


def test_shallow_overlap_is_refuted_and_paid_for_by_the_declared_dilation(
    tmp_path: Path,
) -> None:
    row = _row(tmp_path, _pair("0.0000000000001"), explicit="2.000000001")
    printed, declared = row["at_printed_side"], row["at_target_side"]
    assert printed["verdict"] == "not-a-packing"
    assert printed["pairs_overlapping"] == 1
    low, high = (Fraction(value) for value in printed["least_pair_separation"])
    assert low <= Fraction("-1e-13") <= high < 0
    assert declared["verdict"] == "packing"
    assert Fraction(declared["least_pair_separation"][0]) > 0


def test_deep_overlap_survives_no_small_dilation(tmp_path: Path) -> None:
    row = _row(tmp_path, _pair("0.000001"), explicit="2.000000001")
    declared = row["at_target_side"]
    assert declared["verdict"] == "not-a-packing"
    assert declared["deepest_overlaps"][0]["squares"] == [1, 2]


def test_rotated_square_clearance_is_enclosed(tmp_path: Path) -> None:
    fits = _row(tmp_path, "s: 1.5\nSquare 1: x=0, y=0, deg=45\n", places=0)
    printed = fits["at_printed_side"]
    low, high = (Fraction(value) for value in printed["least_wall_clearance"])
    exact = 0.75 - 2**0.5 / 2
    assert low <= Fraction(exact) + Fraction(1, 10**12)
    assert high >= Fraction(exact) - Fraction(1, 10**12)
    assert high - low < Fraction(1, 10**6)
    assert printed["verdict"] == "packing"
    assert fits["target_side"] == "2"
    tight = _row(tmp_path, "s: 1.4\nSquare 1: x=0, y=0, deg=45\n", explicit="1.4")
    assert tight["at_printed_side"]["verdict"] == "not-a-packing"


def test_far_pairs_are_not_measured(tmp_path: Path) -> None:
    row = _row(
        tmp_path, "s: 5\nSquare 1: x=-1.5, y=0, deg=10\nSquare 2: x=1.5, y=0, deg=0\n", places=0
    )
    assert row["near_pairs"] == 0
    assert "least_pair_separation" not in row["at_printed_side"]


@pytest.mark.parametrize(
    ("target", "reason"),
    [({"explicit": "1.999"}, "below the printed side"), ({}, "exactly one")],
)
def test_refuses_an_undeclared_or_shrinking_target(
    tmp_path: Path, target: dict[str, Any], reason: str
) -> None:
    name = _write(tmp_path, "grid.txt", GRID)
    with pytest.raises(PoseError, match=reason):
        measure(tmp_path, [name], **target)


def test_refuses_paths_outside_the_root(tmp_path: Path) -> None:
    with pytest.raises(PoseError, match="plain path"):
        measure(tmp_path, ["../grid.txt"], places=12)


def test_receipt_reproduces_and_refuses_tampering(tmp_path: Path) -> None:
    first = _write(tmp_path, "grid.txt", GRID)
    second = _write(tmp_path, "pair.txt", _pair("0.0000000000001", side="2.0000000000002"))
    receipt = measure(tmp_path, [first, second], places=12, source="test")
    assert check(receipt, tmp_path) == []
    edited = json.loads(json.dumps(receipt))
    edited["files"][1]["at_target_side"]["verdict"] = "packing-claimed"
    assert any("at_target_side" in problem for problem in check(edited, tmp_path))
    (tmp_path / "grid.txt").write_text(GRID.replace("0.5, y=0.5", "0.5, y=0.6"), "utf-8")
    assert any("bytes are not" in problem for problem in check(receipt, tmp_path))


def test_command_writes_a_receipt_that_check_admits(tmp_path: Path) -> None:
    name = _write(tmp_path, "grid.txt", GRID)
    output = tmp_path / "receipt.json"
    assert (
        margins.main(
            [
                "measure",
                "--root",
                str(tmp_path),
                "--target-places",
                "12",
                "--output",
                str(output),
                name,
            ]
        )
        == 0
    )
    assert margins.main(["check", str(output), "--root", str(tmp_path)]) == 0
    assert margins.main(["measure", "--root", str(tmp_path), "--target", "1", name]) == 2
