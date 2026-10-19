"""The tolerance that decides whether an animation frame is the record it names.

It is a matching tolerance, not packing validity: a frame that names a retained record is
drawn from that record's witness, so the frame's own side and poses have to be the
witness's. These tests pin where it refuses, and re-measure the precision argument that
sets it.
"""

from __future__ import annotations

import math
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from devtools import known_structure
from devtools.known_structure import WITNESSES, record
from sqpack.yamlio import safe_load
from workbench_tools.animation_records import ANIMATION_CONTRACT, decode_animation
from workbench_tools.animation_render import (
    RECORD_REFERENCE_TOLERANCE,
    trajectory_from_animation,
)
from workbench_tools.packing_contracts import DEFAULT_VALIDITY_TOLERANCE

#: The page's catalogue stores centres to 1e-6 and angles to 1e-4 degrees, so a catalogue
#: copy of a record can sit this far from its witness.
CATALOGUE_CENTRE_ROUNDING = 0.5e-6
CATALOGUE_ANGLE_ROUNDING = math.radians(0.5e-4)
#: Above anything binary64 conversion of a witness produces (2.4e-15 over all 324).
CONVERSION_SCALE = 1e-12
#: Every sixth retained witness, with n = 2 and 12, which are stored as corners.
SAMPLED_WITNESSES = sorted({*range(1, 325, 6), 2, 12, 199})


@pytest.mark.parametrize("representation", ["corners", "degrees", "radians"])
def test_record_decodes_exact_rational_scalars(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, representation: str
) -> None:
    """Exact packet fractions reach the diagnostic reader without changing units."""
    if representation == "corners":
        square = {"corners": [["1/3", "1/2"], ["4/3", "1/2"], ["4/3", "3/2"], ["1/3", "3/2"]]}
        expected_angle = 0.0
    else:
        square = {"center": ["5/6", "1/1"], "angle": "1/3"}
        expected_angle = math.radians(1 / 3) if representation == "degrees" else 1 / 3
    payload = {
        "witness": {
            "side": "9/4",
            "coordinates": {
                "angle_unit": "degrees" if representation == "corners" else representation
            },
            "squares": [square],
        }
    }
    (tmp_path / "n-001.yaml").write_text(yaml.safe_dump(payload), encoding="utf-8")
    monkeypatch.setattr(known_structure, "WITNESSES", tmp_path)
    poses, side = known_structure.record(1)
    assert side == 9 / 4
    assert poses[0, 0] == pytest.approx(5 / 6, abs=CONVERSION_SCALE, rel=0)
    assert poses[0, 1] == 1.0
    assert poses[0, 2] == expected_angle


@pytest.mark.parametrize("n", [51, 70])
def test_record_projects_complete_exact_bases_without_geometry_decisions(
    n: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The radical and rational houses retain every centre in diagnostic float poses."""
    from decimal import Decimal, localcontext  # noqa: PLC0415

    from sqpack import witness as witness_api  # noqa: PLC0415

    source = WITNESSES / f"n-{n:03d}.yaml"
    original = source.read_bytes()
    witness = safe_load(original.decode())["witness"]

    def forbidden(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError("a diagnostic reader must not decide feasibility")

    monkeypatch.setattr(witness_api, "verify_packing", forbidden)
    poses, side = record(n)
    with localcontext() as context:
        context.prec = 80

        def scalar(value: Any) -> float:
            if n == 70:
                return float(Fraction(str(value)))
            rational, root = (Fraction(str(part)) for part in value)
            return float(
                Decimal(rational.numerator) / Decimal(rational.denominator)
                + Decimal(root.numerator) / Decimal(root.denominator) * Decimal(2).sqrt()
            )

        assert side == scalar(witness["side"])
        assert poses.shape == (n, 3)
        for index, square in enumerate(witness["squares"]):
            for axis in (0, 1):
                assert poses[index, axis] == pytest.approx(
                    scalar(square["center"][axis]), abs=CONVERSION_SCALE, rel=0
                )
            angle = math.atan2(scalar(square["basis"][1]), scalar(square["basis"][0]))
            assert poses[index, 2] == pytest.approx(angle, abs=CONVERSION_SCALE, rel=0)
    assert source.read_bytes() == original


def _record_frame(*, lift: float = 0.0, grow: float = 0.0) -> dict[str, Any]:
    """The retained n = 2 record as an animation frame naming it, optionally moved."""
    poses, side = record(2)
    squares = [[float(x), float(y) + lift, float(angle)] for x, y, angle in poses]
    return {
        "contract": ANIMATION_CONTRACT,
        "name": "record-2",
        "n": 2,
        "frames": [
            {"t": 0.0, "side": side + grow, "squares": squares, "feasible": True, "record": 2}
        ],
    }


def _renders(document: dict[str, Any]) -> bool:
    trajectory_from_animation(decode_animation(document))
    return True


def test_a_pose_just_inside_the_tolerance_is_the_record() -> None:
    # n = 2 leaves a unit of room above the squares, so the lift stays a valid packing and
    # only the record match is under test.
    assert _renders(_record_frame(lift=0.9 * RECORD_REFERENCE_TOLERANCE))


def test_a_pose_just_outside_the_tolerance_is_a_different_arrangement() -> None:
    with pytest.raises(ValueError, match="record reference poses"):
        _renders(_record_frame(lift=1.1 * RECORD_REFERENCE_TOLERANCE))


def test_the_side_is_matched_relative_to_the_record_side() -> None:
    side = record(2)[1]
    allowed = RECORD_REFERENCE_TOLERANCE * max(1.0, side)
    assert _renders(_record_frame(grow=0.9 * allowed))
    with pytest.raises(ValueError, match="record reference side"):
        _renders(_record_frame(grow=1.1 * allowed))


def test_the_tolerance_sits_between_float_conversion_and_catalogue_rounding() -> None:
    """Reading the exact decimal witnesses as binary64 moves nothing near the tolerance, and
    a catalogue-precision copy moves further than it allows.

    All 324 were measured on 2026-09-14 (a centre moves at most 2.4e-15, a side 1.7e-15).
    This re-measures a spread of them, both representations included, to stay quick.
    """
    worst = 0.0
    for n in SAMPLED_WITNESSES:
        payload = safe_load((WITNESSES / f"n-{n:03d}.yaml").read_text(encoding="utf-8"))
        witness = payload["witness"]
        poses, side = record(n)
        worst = max(worst, float(abs(Fraction(str(witness["side"])) - Fraction(side))))
        for index, square in enumerate(witness["squares"]):
            if "center" in square:
                exact = [Fraction(str(value)) for value in square["center"]]
            else:
                corners = [
                    [Fraction(str(value)) for value in corner] for corner in square["corners"]
                ]
                exact = [sum(axis) / len(corners) for axis in zip(*corners, strict=True)]
            worst = max(
                worst,
                *(float(abs(exact[axis] - Fraction(poses[index, axis]))) for axis in (0, 1)),
            )
    assert worst < CONVERSION_SCALE


def test_a_copy_off_by_float_conversion_is_the_record() -> None:
    assert _renders(_record_frame(lift=CONVERSION_SCALE))


def test_a_copy_at_catalogue_precision_is_not_the_record() -> None:
    with pytest.raises(ValueError, match="record reference poses"):
        _renders(_record_frame(lift=CATALOGUE_CENTRE_ROUNDING))
    with pytest.raises(ValueError, match="record reference poses"):
        _renders(_record_frame(lift=CATALOGUE_ANGLE_ROUNDING))


def test_the_record_match_is_not_the_validity_tolerance() -> None:
    assert RECORD_REFERENCE_TOLERANCE > DEFAULT_VALIDITY_TOLERANCE
