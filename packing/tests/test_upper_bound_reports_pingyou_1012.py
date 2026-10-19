"""PingYou Ltd's certificates of 12 October 2026 (#564, #566 to #569, and the refinements
posted on #503 and #504), imported by declaration.

Seven packets, one per issue: each pins its release, retains no upstream byte and keeps
the certificate as a derived exact fact, held there to the source's own corners
Witness/v2. The general importer's checks run on them through ``test_upper_bound_reports``;
these hold what is particular to them: the digests the issues state, the exact margins
the refinements of T-147 and T-148 claim, which report is smallest at each count, the
ceilings the n261 certificate and the n272 receipt needed raised, and n261's exact
contacts. Nothing here needs Git or the network.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports

N302 = "pingyou-n302-certificate-2026-10-12"
N153 = "pingyou-n153-refinement-2026-10-12"
N207 = "pingyou-n207-refinement-2026-10-12"
N146 = "pingyou-n146-refinement-2026-10-12"
N261 = "pingyou-n261-refinement-2026-10-12"
N105 = "pingyou-n105-refinement-2026-10-12"
N272 = "pingyou-n272-refinement-2026-10-12"
PACKETS = (N302, N153, N207, N146, N261, N105, N272)
COUNTS = {N302: 302, N153: 153, N207: 207, N146: 146, N261: 261, N105: 105, N272: 272}
#: The certificate digest each issue, or each comment's dated update, states.
STATED = {
    N302: "fc57b683ccd411660bb5d5f9758fb2ac013733220bf525936d73f2a11fd8d2cd",
    N153: "1ca754f0238f958597ecddc645aa16f5c44c3afc9cf2614b40ce2fd1f6dea670",
    N207: "94dc19ce0ab4e8c35de7a4a542ff2b46d0dafe717bb84ebf6d3fcd351a212a5c",
    N146: "a88ede7e2faa9d62fe8b6d0e46f7d38dde7df1f5a198d15bc6d6d726df77d13d",
    N261: "f850cb35c31e018d5f6fdde90940f3d55ad36ecdb88341b805af47639c7e16c2",
    N105: "8c684d15e87e772bec491f0c77db5b87c0246883875f5c0ad8b0c8a8ac8cd613",
    N272: "1bfe74e4af5dba4bfb6865ad953ff169620c2b85d91f919abd0ef5527cae21e0",
}
#: What each count's frozen comparison names smallest: this certificate, another report,
#: or the reports whose prints do not order them.
#: Read at the exact sides this record retains for each later report (review A1 of #602):
#: at 302 issues 583 and 586 state one certificate, and PR 574 refines every other count.
SMALLEST: dict[str, dict[str, Any]] = {
    N302: {"smallest": None, "tied": ["#583", "#586"]},
    N153: {"smallest": "PR #574"},
    N207: {"smallest": "PR #574"},
    N146: {"smallest": "PR #574"},
    N261: {"smallest": "PR #574"},
    N105: {"smallest": "PR #574"},
    N272: {"smallest": "PR #574"},
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _row(name: str) -> dict[str, Any]:
    (row,) = reports.check_claims(reports.packet_path(name))["results"]
    return row


@pytest.mark.parametrize("name", PACKETS)
def test_each_packet_pins_its_release_and_retains_no_upstream_byte(name: str) -> None:
    packet = reports.packet_path(name)
    (source,) = _json(packet / "acquisition/sources.json")["sources"]
    assert (source["retained_file_count"], source["retained_total_bytes"]) == (0, 0)
    n = COUNTS[name]
    pinned = {item["path"]: item["sha256"] for item in source["pinned_only"]}
    assert pinned[f"n{n}.cert.json"] == STATED[name]
    (row,) = reports.load_declaration(packet)["certificates"]
    assert row.get("fact") == f"facts/n-{n:03d}.yaml"
    witness = {"path": f"pingyou-n{n}-rational.yaml", "format": "witness-corners"}
    assert row.get("same_packing") == [witness]
    assert f"pingyou-n{n}-rational.yaml" in pinned


@pytest.mark.parametrize("name", PACKETS)
def test_each_fact_is_below_its_case_and_names_the_smallest_report(name: str) -> None:
    row = _row(name)
    assert row["case"]["relation"] == "below"
    expected = SMALLEST[name]
    assert {key: row.get(key) for key in expected} == expected
    # Every register entry the packets rebuild is above the certificate at its count.
    for other in row["pending"]:
        if "result" in other:
            assert other["relation"] == "below", other["report"]


def test_the_refinements_improve_t147_and_t148_by_the_margins_the_comments_state() -> None:
    margins = {
        N207: ("T-147", Fraction("1.4851194398617480221170501178639E-9")),
        N153: ("T-148", Fraction("1.0000000000002E-14")),
    }
    for name, (result, margin) in margins.items():
        case = _row(name)["case"]
        assert case["result"] == result
        assert Fraction(case["difference"]) == margin


def test_the_n105_side_is_below_its_case_by_the_scale_of_that_certificates_padding() -> None:
    case = _row(N105)["case"]
    assert case["result"] == "T-130"
    assert Fraction(1, 10**19) < Fraction(case["difference"]) < Fraction(11, 10**20)


def test_the_n261_certificate_needs_the_raised_ceilings() -> None:
    packet = reports.packet_path(N261)
    (source,) = _json(packet / "acquisition/sources.json")["sources"]
    sizes = {item["path"]: item["bytes"] for item in source["pinned_only"]}
    assert 1_000_000 < sizes["n261.cert.json"] <= reports.MAX_SOURCE_BYTES
    assert 1_000_000 < sizes["pingyou-n261-rational.yaml"] <= reports.MAX_SOURCE_BYTES
    side = reports.read_facts(packet)[261].side
    assert len(str(side.denominator)) == 913
    assert reports.MAX_LITERAL_CHARS == kernel.MAX_RATIONAL_CHARS >= 2522


def _certificate(literal: str) -> bytes:
    """A one-square PingYou certificate whose side is the given literal."""
    return json.dumps({"n": 1, "s_exact": literal, "squares": [["1/2", "1/2", "0"]]}).encode()


def test_a_literal_is_read_up_to_the_integer_limit_and_refused_beyond_it() -> None:
    # Each integer part may run to Python's integer-string limit, which every writer
    # downstream shares; one digit more is refused as it is read, never as a traceback
    # where it is written (review B5 of #602).
    at = "1" + "0" * (reports.MAX_INTEGER_DIGITS - 1)
    certificate = reports.parse_certificate(_certificate(f"{at}/{at[:-1]}"), 1, "pingyou-json")
    assert certificate.side == 10
    with pytest.raises(reports.ReportError, match="integer part longer"):
        reports.parse_certificate(_certificate(at + "0"), 1, "pingyou-json")
    with pytest.raises(reports.ReportError, match="bounded rational"):
        reports.parse_certificate(
            _certificate("1" * (reports.MAX_LITERAL_CHARS + 1)), 1, "pingyou-json"
        )
    with pytest.raises(kernel.ReportError, match="invalid exact diagnostic"):
        kernel._rational(at + "0")  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    assert kernel.to_witness(certificate)["side"] == "10"


def test_the_n272_receipt_states_a_pair_gap_longer_than_the_old_ceiling() -> None:
    positives = reports.check_certification(reports.packet_path(N272))
    margin = reports.margins(positives)[272]
    gap = margin["exact_verify_best_pair_gap"]
    assert gap == margin["independent_best_pair_gap"]
    assert 1024 < len(gap) == 1043 <= kernel.MAX_RATIONAL_CHARS
    assert 0 < Fraction(gap) < Fraction(1, 10**100)


def test_the_n261_certificate_has_exact_contacts_that_both_routes_admit() -> None:
    # The source permits boundary contacts; its exact repair and crop leave some square on
    # the wall and some pair touching, and each route certifies disjoint interiors.
    positives = reports.check_certification(reports.packet_path(N261))
    assert set(reports.margins(positives)[261].values()) == {"0"}
    for route in reports.ROUTES:
        assert positives[261][route]["verification_passed"] is True


def test_the_n261_outside_control_states_a_wall_clearance_longer_than_the_old_ceiling() -> None:
    packet = reports.packet_path(N261)
    _declaration, facts = reports.replayed_facts(packet)
    ((part, _),) = reports.receipt_parts(packet, facts)
    (row,) = [
        row for row in part["cases"] if row["control"] == "square-translated-outside-container"
    ]
    walls = {row[route]["minimum_containment_clearance"] for route in reports.ROUTES}
    (wall,) = walls
    assert 1024 < len(wall) == 2205 <= kernel.MAX_RATIONAL_CHARS
    assert Fraction(wall) < 0


@pytest.mark.parametrize("name", [N261, N272])
def test_the_old_diagnostic_ceiling_refuses_the_receipt(
    monkeypatch: pytest.MonkeyPatch, name: str
) -> None:
    monkeypatch.setattr(kernel, "MAX_RATIONAL_CHARS", 1024)
    with pytest.raises(kernel.ReportError, match="invalid exact diagnostic"):
        reports.check_certification(reports.packet_path(name))


def test_a_certificate_is_refused_beyond_the_byte_ceiling() -> None:
    with pytest.raises(reports.ReportError, match="invalid certificate JSON"):
        reports.parse_certificate(b" " * reports.MAX_SOURCE_BYTES, 1, "pingyou-json")
    with pytest.raises(reports.ReportError, match="byte ceiling"):
        reports.parse_certificate(b" " * (reports.MAX_SOURCE_BYTES + 1), 1, "pingyou-json")


@pytest.mark.parametrize("name", PACKETS)
def test_each_new_packet_is_a_house_reader_of_its_own_side(name: str) -> None:
    declaration = reports.load_declaration(reports.packet_path(name))
    n = COUNTS[name]
    side = reports.read_facts(reports.packet_path(name))[n].side
    assert reports.house_side(declaration["source_key"], n) == side
