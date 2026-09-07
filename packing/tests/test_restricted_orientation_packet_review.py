"""Independent packet-reader controls; target construction is never invoked."""

from __future__ import annotations

import json
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_restricted_orientation_discriminator as check
from devtools import run_restricted_orientation_discriminator as producer


@pytest.fixture(scope="module")
def source_packet() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    producer.run_geometry("source-control", rows.append)
    return producer.collect_receipts(
        "".join(json.dumps(row) + "\n" for row in rows),
        "source-control",
        worker_succeeded=True,
    )


def test_independent_source_formulas_and_complete_receipt(
    source_packet: dict[str, Any],
) -> None:
    result = check.check_packet(source_packet, "source-control", 0)
    assert result["decision"] == "accepted"
    assert result["standalone_exhaustive_certificate"] is False
    assert result["h036_outcome"] == "unresolved"
    for change in ("point", "unchecked", "false", "exit"):
        packet = deepcopy(source_packet)
        exit_code = 0
        if change == "point":
            packet["inputs"]["twelve_points_power_basis"][0][0] = "poly[0,0]"
        elif change == "unchecked":
            packet["unchecked_obligations"] = ["forced_A1"]
        elif change == "false":
            packet["obligations"]["forced_A1"] = False
        else:
            exit_code = 1
        with pytest.raises(ValueError, match=r"disagree|requires"):
            check.check_packet(packet, "source-control", exit_code)


@pytest.mark.parametrize("name", check.NAMES)
def test_source_distinct_witness_geometry_on_side_four_toys(name: str) -> None:
    side = check.rational(4)
    ten = tuple((check.rational(3 + Fraction(i, 100)), check.rational(3)) for i in range(10))
    twelve = tuple((check.rational(3 + Fraction(i, 100)), check.rational(3)) for i in range(12))
    angle = 0 if name in check.BY_ANGLE[0] else 45
    center = "poly[2,0]" if name == "localization" else "poly[1,0]" if angle else "poly[1/2,0]"
    row = {
        "obligation": name,
        "angle_degrees": angle,
        "center_power_basis": [center, center],
        "square_side": "1",
        "square_semantics": "closed",
        "ten_membership_mask": 0,
        "twelve_membership_mask": 0,
        "strict_box_counterexample_established": False,
    }
    assert check.check_escape(side, ten, twelve, row) == name
    assert (
        check.membership(
            (check.rational("1/2"), check.rational("1/2")),
            ((check.rational(1), check.rational(1)),),
            0,
        )
        == 1
    )
    row["center_power_basis"] = ["poly[0,0]", "poly[0,0]"]
    with pytest.raises(ValueError, match="containment"):
        check.check_escape(side, ten, twelve, row)


def test_exact_signs_and_packet_loader_refusals(tmp_path: Path) -> None:
    p, q = 1, 0
    for _ in range(25):
        p, q = 3 * p + 4 * q, 2 * p + 3 * q
    assert check.sign((Fraction(p), Fraction(-q))) == 1
    assert check.sign((Fraction(p) - Fraction(1, p), Fraction(-q))) == -1
    for value in ("poly[1e1000000000,0]", "poly[01,0]", "poly[1/1,0]"):
        with pytest.raises(ValueError, match="coefficient"):
            check.coordinate(value)
    path = tmp_path / "packet.json"
    for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":1e9999}', " " * (check.LIMIT + 1)):
        path.write_text(text)
        with pytest.raises(ValueError, match=r"duplicate|nonfinite|byte limit"):
            check.load_packet(path)
