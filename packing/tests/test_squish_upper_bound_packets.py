"""Trust-boundary and geometry controls for the exact SQUISH packet adapter."""

from __future__ import annotations

import copy
import functools
import gzip
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

import pytest
import yaml

from devtools import squish_followup_packets as first
from devtools import squish_followup_packets as update
from devtools import squish_second_update_packets as second
from devtools import squish_upper_bound_packets as original
from devtools import squish_upper_bound_packets as packet
from sqpack.yamlio import safe_load


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
    fact, raw = packet.parse_source(path, n)
    assert packet.parse_source_bytes(raw, n) == (fact, raw)
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
    with pytest.raises(ValueError, match=r"source|square|exact|roster|required"):
        packet.parse_source_bytes(json.dumps({**source_data(), **mutation}).encode(), 2)


def test_duplicate_json_and_bounded_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "source.json"
    path.write_text('{"n":2,"n":2}')
    with pytest.raises(ValueError, match="duplicate"):
        packet.parse_source(path, 2)
    with pytest.raises(ValueError, match="duplicate"):
        packet.parse_source_bytes(path.read_bytes(), 2)
    path.write_text(json.dumps(source_data()))
    monkeypatch.setattr(packet, "MAX_SOURCE_BYTES", 16)
    with pytest.raises(ValueError, match="byte ceiling"):
        packet.parse_source(path, 2)
    with pytest.raises(ValueError, match="admission"):
        packet.parse_source(path, 325)
    with pytest.raises(ValueError, match="byte ceiling"):
        packet.parse_source_bytes(path.read_bytes(), 2)
    for expected in (True, 0, 325):
        with pytest.raises(ValueError, match="admission"):
            packet.parse_source_bytes(path.read_bytes(), expected)


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


def second_source_data(n: int = 1) -> dict[str, object]:
    return {
        "n": n,
        "s_exact": str(n),
        "s_decimal": f"{n}.0000",
        "note": "fixture",
        "squares": [[str(i), "0", "0"] for i in range(n)],
    }


def second_parse(tmp_path: Path, data: object, n: int = 1) -> dict[str, object]:
    path = tmp_path / "source.json"
    path.write_text(json.dumps(data))
    return original.parse_source(path, n)[0]


@pytest.mark.parametrize("squeezed", [True, False])
@pytest.mark.parametrize("phase", [None, 3])
def test_squeezed_boolean_is_metadata_only(
    tmp_path: Path, squeezed: object, phase: int | None
) -> None:
    plain = second_source_data()
    marked = {**plain, "squeezed": squeezed}
    if phase is not None:
        marked["phase"] = phase
    assert second_parse(tmp_path, marked) == second_parse(tmp_path, plain)


@pytest.mark.parametrize("squeezed", [0, 1, "true", "false", None, [], {}])
def test_nonboolean_squeezed_is_refused(tmp_path: Path, squeezed: object) -> None:
    with pytest.raises(original.PacketError, match="squeezed"):
        second_parse(tmp_path, {**second_source_data(), "squeezed": squeezed})


@pytest.mark.parametrize("missing", ["n", "s_exact", "s_decimal", "note", "squares"])
def test_squeezed_does_not_allow_missing_required_fields(tmp_path: Path, missing: str) -> None:
    data = {**second_source_data(), "squeezed": True}
    del data[missing]
    with pytest.raises(original.PacketError, match="required"):
        second_parse(tmp_path, data)


@pytest.mark.parametrize(
    "mutation",
    [
        {"unexpected_metadata": True},
        {"n": True},
        {"n": 2},
        {"phase": True},
        {"phase": 0},
        {"phase": 101},
        {"phase": "3"},
        {"s_exact": 1},
        {"s_exact": "1/0"},
        {"s_exact": "1" * 257},
        {"s_exact": "0"},
        {"s_decimal": "NaN"},
        {"squares": []},
        {"squares": [["0", "0", 0]]},
        {"squares": [["0", "0", "1e-3"]]},
        {"squares": [["0", "0"]]},
        {"squares": [["0", "0", "0", "0"]]},
        {"squares": [["0" * 257, "0", "0"]]},
    ],
)
def test_metadata_allowance_keeps_existing_guards(
    tmp_path: Path, mutation: dict[str, object]
) -> None:
    with pytest.raises(ValueError, match=r"source|square|rational|side|literal"):
        second_parse(tmp_path, {**second_source_data(), "squeezed": True, **mutation})


def test_duplicate_squeezed_byte_and_expected_count_guards(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "source.json"
    valid = json.dumps({**second_source_data(), "squeezed": True})
    path.write_text(valid[:-1] + ', "squeezed": false}')
    with pytest.raises(ValueError, match="duplicate"):
        original.parse_source(path, 1)
    path.write_text(valid)
    for expected in (True, 0, 325):
        with pytest.raises(original.PacketError, match="admission"):
            original.parse_source(path, expected)
    monkeypatch.setattr(original, "MAX_SOURCE_BYTES", len(valid.encode()) - 1)
    with pytest.raises(original.PacketError, match="byte ceiling"):
        original.parse_source(path, 1)


def test_n263_sourceprint_is_distinct_from_safe_ceiling() -> None:
    exact = Fraction("9424018478849569/562949953421312")
    printed = "16.7404196795387747"
    ceiling = first.display(str(exact))
    assert ceiling == "16.7404196795387766"
    assert Fraction(printed) < exact <= Fraction(ceiling)
    assert Fraction(ceiling) - exact < Fraction(1, 10**16)


def test_second_update_has_distinct_revision_identity() -> None:
    assert second.NUMBERS == (88, 108, 179, 180, 199, 207, 236, 263, 302)
    assert second.REVISION != first.REVISION
    assert second.SOURCE_KEY != first.SOURCE_KEY
    assert second.PACKET != first.PACKET
    assert second.source_url(88).endswith("/n088/n088.cert.json")
    assert second.witness_id(263) == "W-squish-422-n263"
    with pytest.raises(original.PacketError):
        second.source_url(123)


def test_acquisition_binds_all_nine_before_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    destination = tmp_path / "packet"
    monkeypatch.setattr(second, "REPO", tmp_path)
    monkeypatch.setattr(second, "PACKET", destination)
    for n in second.NUMBERS:
        path = source / f"n{n:03d}/n{n:03d}.cert.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps({**second_source_data(n), "phase": 3, "squeezed": n == 263}))
    last = source / "n302/n302.cert.json"
    last.write_text(json.dumps({**second_source_data(302), "unknown": True}))
    with pytest.raises(original.PacketError):
        second.acquire(source)
    assert not destination.exists()
    last.write_text(json.dumps(second_source_data(302)))
    second.acquire(source)
    acquisition = json.loads((destination / "acquisition/sources.json").read_bytes())
    assert [row["n"] for row in acquisition["cases"]] == list(second.NUMBERS)
    assert acquisition["source_commit"] == second.REVISION
    assert acquisition["feasibility_checked"] is False
    assert acquisition["producer_checker_replayed"] is False
    for row in acquisition["cases"]:
        n = row["n"]
        raw = (source / f"n{n:03d}/n{n:03d}.cert.json").read_bytes()
        assert row["source_sha256"] == hashlib.sha256(raw).hexdigest()
        assert row["source_bytes"] == len(raw)
        assert row["reported_seed"] == second.SEEDS[n]
        fact = json.loads(gzip.decompress((tmp_path / row["facts"]).read_bytes()))
        assert len(fact["squares"]) == n
        assert row["safe_ceiling_16"] == first.display(fact["side"])
        assert row["side"] == fact["printed_side"]
    assert acquisition["cases"][-2]["reported_metadata"]["squeezed"] is True


@functools.cache
def previous_source_case(n: int) -> str:
    """Retain the complete SQUISH source state displaced by the Gupta intake."""
    from devtools import register_gupta_reports as gupta  # noqa: PLC0415

    if gupta.HISTORY.exists():
        for row in gupta.read_history():
            if row["n"] == n:
                return row["frontier"]
    return (second.REPO / f"packing/frontier/n-{n:03d}.md").read_text()


def historical_second_report(n: int) -> str:
    """Project the historical source report and earlier ceiling without publishing it."""
    current = previous_source_case(n)
    _, front, body = current.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    fact = second.read_fact(n)
    case["reported_upper_bound"].update(
        value=first.display(fact["side"]),
        exact_form=fact["side"],
        source_key=second.SOURCE_KEY,
        evidence=[second.EVIDENCE_ID],
    )
    case["verified_upper_bound"] = copy.deepcopy(second.prior_lanes()[n]["prior_verified"])
    projected = "---\n" + yaml.safe_dump(document, sort_keys=False) + "---\n" + body
    return second.adopt_report(n, projected)


@pytest.mark.parametrize("n", second.NUMBERS)
def test_second_update_reconstructs_report_without_replacing_prior_verified_lane(
    n: int,
) -> None:
    current = historical_second_report(n)
    expected = second.adopt_report(n, current)
    _, front, body = current.split("---\n", 2)
    document = safe_load(front)
    case = document["packing"]
    previous = second.prior_lanes()[n]
    fact = second.read_fact(n)
    assert case["verified_upper_bound"] == previous["prior_verified"]
    assert case["reported_upper_bound"]["value"] == first.display(fact["side"])
    assert case["reported_upper_bound"]["exact_form"] == fact["side"]
    assert case["reported_upper_bound"]["source_key"] == second.SOURCE_KEY
    assert case["reported_upper_bound"]["evidence"] == [second.EVIDENCE_ID]
    retained_fields = {
        key: copy.deepcopy(case[key])
        for key in ("evidence", "resources", "priority_notes", "blockers")
    }
    case["reported_upper_bound"].update(value="999.0", exact_form="999")
    case["verified_upper_bound"].update(value="888.0", exact_form="888")
    body = body.replace(f"$s({n}) \\le {first.display(fact['side'])}$", f"$s({n}) \\le 999.0$")
    body = body.replace(f"with exact side ${fact['side']}$", "with exact side $999$")
    body = body.replace(f"source print ${fact['printed_side']}$", "source print $777.0$")
    damaged = (
        "---\n"
        + yaml.safe_dump(document, sort_keys=False, allow_unicode=True, width=98)
        + "---\n"
        + body
    )
    repaired = second.adopt_report(n, damaged)
    assert repaired == expected
    assert second.adopt_report(n, repaired) == repaired
    payload = safe_load(repaired.split("---\n", 2)[1])["packing"]
    assert payload["verified_upper_bound"] == previous["prior_verified"]
    for key, value in retained_fields.items():
        assert payload[key] == value


def test_second_update_refuses_unknown_confirmation_and_output_escape(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    text = previous_source_case(179)
    _, front, body = text.split("---\n", 2)
    document = safe_load(front)
    document["packing"]["verified_upper_bound"]["evidence"] = [
        "E-squish-second-update-2026-10-07-exact-replay"
    ]
    confirmed = "---\n" + yaml.safe_dump(document, sort_keys=False) + "---\n" + body
    with pytest.raises(packet.PacketError, match="confirmation adapter"):
        second.adopt_report(179, confirmed)
    private = tmp_path / "private"
    outside = tmp_path / "outside"
    private.mkdir()
    outside.mkdir()
    (private / "linked").symlink_to(outside, target_is_directory=True)
    monkeypatch.setattr(second, "REPO", private)
    with pytest.raises(packet.PacketError, match="escapes"):
        second.save(private / "linked/facts.json", b"{}")
    assert not (outside / "facts.json").exists()


def test_second_update_adoption_keeps_title_and_leads_with_current_report() -> None:
    """Temporal qualification belongs to a paragraph, never to the Markdown title."""
    text = historical_second_report(88)
    _, front, body = text.split("---\n", 2)
    body = re.sub(
        rf"\n{second.HEADING}\n.*?{re.escape(second.REPORT_END)}\n",
        "",
        body,
        flags=re.DOTALL,
    )
    body = body.replace("Previously, **Exact certificate", "**Exact certificate", 1)
    adopted = second.adopt_report(88, "---\n" + front + "---\n" + body)
    assert "\n# `s(88)` — open\n" in adopted
    assert "Previously, #" not in adopted
    assert adopted.index(second.HEADING) < adopted.index("**Exact certificate")
