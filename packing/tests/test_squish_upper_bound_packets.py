"""Trust-boundary and geometry controls for the exact SQUISH packet adapter."""

from __future__ import annotations

import copy
import gzip
import json
from fractions import Fraction
from pathlib import Path

import pytest

from devtools import squish_followup_packets as update
from devtools import squish_upper_bound_packets as packet


def source_data(n: int = 2) -> dict[str, object]:
    return {
        "n": n,
        "s_exact": str(n),
        "s_decimal": f"{n}.0000",
        "note": "fixture",
        "squares": [[str(Fraction(2 * i + 1, 2)), "1/2", "0"] for i in range(n)],
    }


def parse(tmp_path: Path, data: object, n: int = 2) -> dict[str, object]:
    path = tmp_path / "source.json"
    path.write_text(json.dumps(data))
    fact, _raw = packet.parse_source(path, n)
    return fact


def test_complete_grid_above_old_admission_cap(tmp_path: Path) -> None:
    fact = parse(tmp_path, source_data(108), 108)
    witness = packet.to_witness(fact)
    verdict = packet.decide(witness)
    for result in verdict.values():
        assert result["verification_passed"]
        assert result["pairs_tested"] == 5778


def test_exact_rotated_conversion_and_both_control_refusals(tmp_path: Path) -> None:
    fact = parse(tmp_path, source_data())
    witness = packet.to_witness(fact)
    assert all(row["verification_passed"] for row in packet.decide(witness).values())
    overlap = copy.deepcopy(witness)
    overlap["squares"][1]["corners"] = copy.deepcopy(overlap["squares"][0]["corners"])
    outside = copy.deepcopy(witness)
    for point in outside["squares"][0]["corners"]:
        point[0] = str(Fraction(point[0]) - 4)
    for control in (overlap, outside):
        assert all(not row["verification_passed"] for row in packet.decide(control).values())
    rotated = parse(
        tmp_path,
        {
            **source_data(1),
            "s_exact": "2",
            "s_decimal": "2.0000",
            "squares": [["1", "1", "1/2"]],
        },
        1,
    )
    witness = packet.to_witness(rotated)
    assert witness["squares"][0]["corners"] == [
        ["11/10", "3/10"],
        ["17/10", "11/10"],
        ["9/10", "17/10"],
        ["3/10", "9/10"],
    ]
    assert all(row["verification_passed"] for row in packet.decide(witness).values())


@pytest.mark.parametrize(
    "mutation",
    [
        {"n": True},
        {"n": 3},
        {"s_exact": 2},
        {"s_exact": "1/0"},
        {"s_exact": "0"},
        {"s_exact": "1" * 257},
        {"s_decimal": "NaN"},
        {"unknown": "field"},
        {"squares": [["1/2", "1/2", 0]]},
        {"squares": [["1/2", "1/2", "0"], ["3/2", "1/2"]]},
    ],
)
def test_malformed_source_is_refused(tmp_path: Path, mutation: dict[str, object]) -> None:
    with pytest.raises(ValueError, match=r"source|square|exact|roster|required"):
        parse(tmp_path, {**source_data(), **mutation})


def test_duplicate_json_and_bounded_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "source.json"
    path.write_text('{"n":2,"n":2}')
    with pytest.raises(ValueError, match="duplicate"):
        packet.parse_source(path, 2)
    path.write_text(json.dumps(source_data()))
    monkeypatch.setattr(packet, "MAX_SOURCE_BYTES", 16)
    with pytest.raises(ValueError, match="byte ceiling"):
        packet.parse_source(path, 2)
    with pytest.raises(ValueError, match="admission"):
        packet.parse_source(path, 325)


def test_integer_decimal_ceiling_never_understates_exact_bound() -> None:
    assert packet.verified_value(Fraction(20001, 10000), "2.000") == "2.001"
    assert packet.verified_value(Fraction(2), "2.000") == "2.000"
    assert Fraction(
        packet.verified_value(
            Fraction(6147784441267127, 562949953421312), "10.9206589394033085"
        )
    ) >= Fraction(6147784441267127, 562949953421312)


def test_exact_contact_and_tiny_overlap_have_opposite_verdicts(tmp_path: Path) -> None:
    witness = packet.to_witness(parse(tmp_path, source_data()))
    assert all(row["verification_passed"] for row in packet.decide(witness).values())
    for point in witness["squares"][1]["corners"]:
        point[0] = str(Fraction(point[0]) - Fraction(1, 10**30))
    for result in packet.decide(witness).values():
        assert result["verification_passed"] is False
        assert result["pairs_tested"] == 1
        assert result["failures"]


def test_negative_controls_match_their_json_receipt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fact = parse(tmp_path, source_data())
    monkeypatch.setattr(packet, "NUMBERS", (2,))
    monkeypatch.setattr(packet, "read_fact", lambda _n: fact)
    receipt = packet.negative_controls()
    assert json.loads(json.dumps(receipt)) == receipt


def test_update_side_display_is_a_ceiling() -> None:
    for literal in (
        "1/3",
        "100000000000000001/100000000000000000",
        "3",
        "7250614903299225/562949953421312",
    ):
        rendered = Fraction(update.display(literal))
        exact = Fraction(literal)
        assert exact <= rendered < exact + Fraction(1, 10**16)


def test_update_packet_geometry_and_prior_evidence_are_distinct() -> None:
    update.check()
    prior = packet.read_fact(153)
    current = update.read_fact(153)
    assert current == prior
    assert update.fact_path(153) != packet.fact_path(153)
    for n in update.REPLACEMENTS:
        assert Fraction(update.read_fact(n)["side"]) < Fraction(packet.read_fact(n)["side"])


def test_update_retained_noncanonical_facts_are_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    fact = update.read_fact(123)
    fact["squares"][0]["x"] = "2/2"
    target = tmp_path / "facts/n-123.json.gz"
    target.parent.mkdir()
    target.write_bytes(gzip.compress(update.json_bytes(fact), mtime=0))
    monkeypatch.setattr(update, "PACKET", tmp_path)
    with pytest.raises(packet.PacketError, match="not normalized"):
        update.read_fact(123)
