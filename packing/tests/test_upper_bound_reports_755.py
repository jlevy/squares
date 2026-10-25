"""Amund Kristiansen's issue #755: the #755 lane of 23 October 2026.

One dilation certificate in Evan Daniel's text format, in a gist with no licence, so kept
as a derived exact fact and read by the `evand-cert` adapter: s(303) of #755 at
``511f56b``. The author's CC0 1.0 dedication of 24 October (issuecomment-6388401978) let
the packet retain the gist's three files at the same pin; the fact stays, since the
receipts are bound to it, and the importer holds it to the retained certificate. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it, as the stage 4 review
of 19 October asked of the imports before it (RV-1 of
docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md): the
digests the issue prints, that the derived fact names the certificate's, the side, that it
is below every report at 303 by the margin the records state, that the house reader
rebuilds it, the replay's margins, the sharp controls, and the identity measured against
T-230. Every test reads the packet only; none needs the network.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from sqpack.yamlio import load_yaml

PACKET = "amundsk-n303-2026-10-23"
N = 303
KEY = "[Kristiansen n303 2026-10-23]"
CERT = "s303_amund.cert"
SIDE = Fraction(223872029093440709529093216833, 125 * 10**26)
#: The SHA-256 digests issue #755 prints for the certificate and its binary64 input.
PRINTED_DIGESTS = {
    CERT: "9ec01059b35cc983cb28a1bb33bd215a2717228f7efd182e1724de6b22dc511b",
    "s303_amund.input.txt": "19fc5d171a26bf8d4a925c0457fa367b12127e8bd581d91c6dcd573108e4bba4",
}
#: The certificate's margin below T-230, the house it would replace, exactly.
MARGIN = ("T-230", Fraction(9889799071009889799071, 10**27))


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _row() -> dict[str, Any]:
    (row,) = (row for row in reports.check_claims(_packet())["results"] if row["n"] == N)
    return row


def _ceil_at(value: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(value * 10**places), 10**places)


def _manifest() -> dict[str, str]:
    text = (_packet() / "acquisition/upstream-subtree.sha256").read_text("utf-8")
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def test_the_packet_retains_the_gists_files_under_cc0_with_the_digests_the_issue_prints() -> None:
    """Derived-only on 23 October for want of a licence; on 24 October the author
    dedicated the three files to the public domain under CC0 1.0 and asked that they be
    kept, so the packet was acquired again at the same pin, every digest unchanged."""
    manifest = _manifest()
    for name, digest in PRINTED_DIGESTS.items():
        assert manifest[name] == digest
    record = json.loads((_packet() / "acquisition/sources.json").read_text("utf-8"))
    (source,) = record["sources"]
    assert source["source_commit"] == "511f56bf6e6afb4eb22f12d31371c2a2fe7b4767"
    assert source["retained_file_count"] == 3
    assert source["pinned_only"] == []
    assert source["license"].startswith("CC0 1.0")
    assert "issuecomment-6388401978" in source["license"]
    for name, digest in manifest.items():
        raw = (_packet() / "source" / name).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == digest
    answer = json.loads((_packet() / "acquisition/answer.json").read_text("utf-8"))
    assert answer["html_url"].endswith("#issuecomment-6388401978")
    assert answer["created_at"] == answer["updated_at"] == "2026-10-24T19:13:49Z"


def test_the_derived_fact_is_the_retained_certificate() -> None:
    """The row keeps its fact, which the receipts name; admitting it also reads the
    retained certificate and requires the same packing at the same side."""
    (row,) = reports.load_declaration(_packet())["certificates"]
    raw = (_packet() / "source" / CERT).read_bytes()
    retained = reports.parse_certificate(raw, N, row["format"], reports.row_options(row))
    assert reports.read_facts(_packet())[N] == retained


def test_the_derived_fact_names_the_certificates_digest_and_states_its_side() -> None:
    raw = gzip.decompress((_packet() / "facts/n-303.yaml.gz").read_bytes()).decode("utf-8")
    witness = load_yaml(raw)["witness"]
    assert witness["source"]["revision_sha256"] == PRINTED_DIGESTS[CERT]
    assert witness["source"]["revision"] == "511f56bf6e6afb4eb22f12d31371c2a2fe7b4767"
    assert Fraction(witness["side"]) == SIDE


def test_the_certificate_states_its_side_and_the_house_reader_rebuilds_it() -> None:
    (certificate,) = reports.read_facts(_packet()).values()
    assert (certificate.n, certificate.side) == (N, SIDE)
    assert reports.house_side(KEY, N) == SIDE
    (row,) = reports.load_declaration(_packet())["certificates"]
    assert (row["path"], row.get("fact")) == (CERT, "facts/n-303.yaml")
    assert row["offered"] == "17.909762327476"
    assert _ceil_at(SIDE, 12) == Fraction(Decimal(row["offered"]))


def test_the_issues_long_decimal_is_the_binary64_value_below_the_side() -> None:
    """The issue also prints the side as 17.909762327475256427..., which is the double
    nearest it, 3.35e-16 below the exact side, not its expansion; the record quotes the
    exact side or its 12-place ceiling."""
    printed = Fraction(Decimal("17.909762327475256427"))
    assert printed < SIDE
    assert Decimal(float(SIDE)).to_eng_string().startswith("17.909762327475256427")


def test_the_certificate_is_below_its_case_and_every_report_it_names() -> None:
    row = _row()
    assert row["smallest"] == reports.THIS
    assert row["case"]["relation"] == "below"
    assert {other["relation"] for other in row["pending"]} == {"below"}
    house, margin = MARGIN
    assert row["case"]["result"] == house
    assert Fraction(row["case"]["difference"]) == margin
    assert reports.house_side("[Daniel n303 2026-10-22]", N) - SIDE == margin


def test_the_replay_clears_walls_and_pairs_by_the_margins_its_construction_gives() -> None:
    positives = reports.check_certification(_packet())
    (margins,) = reports.margins(positives).values()
    for route in ("exact_verify", "independent"):
        assert Fraction(margins[f"{route}_containment_clearance"]) >= Fraction(6, 10**13)
        assert Fraction(margins[f"{route}_best_pair_gap"]) >= Fraction(12, 10**13)


def test_the_retained_sharp_controls_met_contact_and_refused_1e30_past_it() -> None:
    record = json.loads((_packet() / "replay/sharp-controls.json").read_text("utf-8"))
    assert record["all_as_expected"] is True
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    seen = set()
    for row in record["controls"]:
        past = row["where"] == "past-contact"
        seen.add((row["control"], past))
        assert set(row["routes"]) == set(kernel.ROUTES)
        for verdict in row["routes"].values():
            assert verdict["passed"] is not past
            assert Fraction(verdict[row["margin"]]) == (-kernel.SHARP_EPSILON if past else 0)
    assert seen == {
        (control, past) for control in kernel.SHARP_CONTROLS for past in (False, True)
    }


@pytest.mark.slow
@pytest.mark.parametrize("where", ["at-contact", "past-contact"])
@pytest.mark.parametrize("control", kernel.SHARP_CONTROLS)
def test_both_routes_meet_contact_and_refuse_1e30_past_it_at_755s_303(
    control: str, where: str
) -> None:
    """The receipt's two controls are gross (a duplicated square, gap -1, and a square
    moved outside), while #755's certificate clears every wall by about 6.0e-13 and every
    pair by about 1.2e-12. The kernel's two sharp controls on the derived fact, decided
    again: accepted by both maintained routes at exact contact with the margin exactly 0,
    and refused 1e-30 past it at exactly -1e-30, as replay/sharp-controls.json records.
    Each case runs both routes over 45,753 pairs, about ten seconds, so it runs in the deep
    surface."""
    certificate = reports.read_facts(_packet(), numbers=[N])[N]
    margin = "wall" if control == "side-lowered-past-wall-contact" else "gap"
    past = where == "past-contact"
    verdicts = kernel.run_sharp(certificate, control, past=past)
    for route in kernel.ROUTES:
        assert verdicts[route]["passed"] is not past, route
        assert verdicts[route][margin] == (-kernel.SHARP_EPSILON if past else 0), route


def test_the_identity_record_pairs_it_one_to_one_with_t230s_packing() -> None:
    """The measurement the register's notes cite (measure/identity.json): nearest centres
    pair it one to one with T-230's packing; the assignment moves 12 squares beyond a
    tenth, so it is no refinement by the record's word, and every one of T-230's 91 tilted
    squares pairs with a square tilted the same way."""
    record = json.loads((_packet() / "measure/identity.json").read_text("utf-8"))
    (house,) = (pair for pair in record["pairs"] if pair["against"].startswith("T-230"))
    assert house["nearest_centre"]["one_to_one"] is True
    assert house["assignment"]["moved_beyond"]["1e-1"] == 12
    assert house["assignment"]["moved_beyond"]["1e-2"] == 31
    assert Fraction(house["side_difference_exact"]) == -MARGIN[1]
    assert house["bands"]["tilted_paired_same_sign_within_1e-1"] == 91
    assert record["tilts"]["#755"]["tilted_beyond_1_degree"] == 96
    others = [pair for pair in record["pairs"] if not pair["against"].startswith("T-230")]
    assert all(pair["nearest_centre"]["one_to_one"] is False for pair in others)
    assert (
        record["dilation"]["input_side_times_1_plus_delta_rounded_up_at_30_places_equals_side"]
        is True
    )
