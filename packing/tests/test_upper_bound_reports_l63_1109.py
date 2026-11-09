"""The upper-bound imports of the intake pass's lane L63 of 9 November 2026 (think-3guf).

Five packets, each read by the ``witness-corners`` adapter: Doğa Özden's #927 at 232
(kenaznia-doga/s232-upper-bound 09e324f), #928 at 268 (s268-upper-bound a40a15d), #929 at
299 (s299-upper-bound-17801004 a042eab), #930 at 303 (s303-upper-bound b43ca09) and #931 at
307 (s307-upper-bound dbe8838). Each witness was promoted to exact rationals by this
repository's ``packing-witness promote --strategy robust-rational``, so its side is a
fraction of more than 150 digits, and each issue prints it rounded up at 12 places. The
general importer's checks run on each packet through ``test_upper_bound_reports``; these
hold what is particular to them: the digests the issues and READMEs print, each print
against its exact side, the house each is compared with and the improvement the issue
states, the ledger's verdicts, the retained sharp controls and the identity measurements
the register's notes cite. Every test reads the packets and the ledger only; none needs
the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-927-931-20261109"

#: Each packet with its issue, its count, the house it is compared with, that house's
#: register entry, the issue's 12-place print and the improvement the issue states.
PACKETS: dict[str, tuple[int, int, str, str, str, str]] = {
    "ozden-s232-upper-bound-2026-11-09": (
        927,
        232,
        "[Couzo issue 844 2026-10-28]",
        "T-256",
        "15.761409644882",
        "2.521e-04",
    ),
    "ozden-s268-upper-bound-2026-11-09": (
        928,
        268,
        "[Daniel issue 914 2026-11-05]",
        "T-270",
        "16.872469897837",
        "2.962e-05",
    ),
    "ozden-s299-upper-bound-2026-11-09": (
        929,
        299,
        "[Özden s299 upper bound 2026-11-03]",
        "T-263",
        "17.801004434256",
        "2.341e-04",
    ),
    "ozden-s303-upper-bound-2026-11-09": (
        930,
        303,
        "[Daniel issue 914 2026-11-05]",
        "T-272",
        "17.901789273157",
        "4.348e-05",
    ),
    "ozden-s307-upper-bound-2026-11-09": (
        931,
        307,
        "[Couzo issue 844 2026-10-28]",
        "T-256",
        "17.979230960388",
        "2.032e-05",
    ),
}
#: The SHA-256 digests the issues (the witness) and the READMEs (both files) print, by count:
#: the candidate YAML's, then its JSON copy's.
PRINTED_DIGESTS = {
    232: (
        "22b3809ec29efbb3555d3eb2eaee89aa47901696b7c2578ccf8ff688d07f13e8",
        "51a17e96f1e6aa4989c295c1b235a51515165a88da57d4b904f748a0460aaf9b",
    ),
    268: (
        "74c0e5d4927ec57468f0cae71636ba46833230ceea4d1dd0cd5ddc1ed76421b3",
        "fcd07b9ff77e7e9be86fcf78eebee721bcfd1c4e5d6ffa2c8164847a4dd0d180",
    ),
    299: (
        "dfb0ccf71474a276a52ce768cc38e799d30ff6373a22b8ae318f58f278025d9d",
        "e2f178e7586729e3aa7ba5ad9c44eb8a406dbd1ca069a98b20ff367174036929",
    ),
    303: (
        "9cbeb7a8198ef9f3316f9e4dd0a998b879133a2e31e12c82c3fbe9882e0f2f3e",
        "0fd9f9dce219b250e21eb60a95e62c042df1baff4553dd7c4397fb397114c3a2",
    ),
    307: (
        "cb78adf88737718e4efe855bf5870879eef90ad30c386728d2ba64bb7f4e81e8",
        "612e97b1220ff5016e88c57d19293047da18d2e7775a8f99b0974cda1a6c706c",
    ),
}
#: Each certificate's side rounded up at 16 places, as its claim record prints it.
CEILINGS = {
    232: "15.7614096448817244",
    268: "16.8724698978362125",
    299: "17.8010044342552937",
    303: "17.9017892731564904",
    307: "17.9792309603873628",
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest(name: str) -> dict[str, str]:
    text = (reports.packet_path(name) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


@pytest.mark.parametrize("n", sorted(PRINTED_DIGESTS))
def test_the_packets_hold_the_files_whose_digests_the_issues_print(n: int) -> None:
    manifest = _manifest(f"ozden-s{n}-upper-bound-2026-11-09")
    candidate, copy = PRINTED_DIGESTS[n]
    assert manifest[f"n-{n}-candidate.yaml"] == candidate
    assert manifest[f"n{n}-witness.json"] == copy


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_print_is_its_exact_side_rounded_up_and_its_reader_rebuilds_it(name: str) -> None:
    """Each issue's 12-place print is the side rounded up, and the JSON states the same
    packing as the YAML (the declaration's ``same_packing``, which ``read_facts`` holds)."""
    issue, n, _house, _result, printed, _gain = PACKETS[name]
    declaration = reports.load_declaration(reports.packet_path(name))
    assert declaration["source_key"] == f"[Özden s{n} upper bound 2026-11-09]"
    assert declaration["issue"].endswith(f"/issues/{issue}")
    assert (declaration["requested"], declaration["replayed"]) == ([n], [n])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (n, "witness-corners", printed)
    assert [other["path"] for other in row.get("same_packing", [])] == [f"n{n}-witness.json"]
    side = reports.read_facts(reports.packet_path(name))[n].side
    assert _up(side, 12) == Fraction(Decimal(printed))
    assert _up(side, 16) == Fraction(Decimal(CEILINGS[n]))
    assert reports.house_side(declaration["source_key"], n) == side


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_certificate_is_below_its_house_by_the_improvement_the_issue_states(
    name: str,
) -> None:
    _issue, n, house, result, _printed, gain = PACKETS[name]
    side = reports.read_facts(reports.packet_path(name))[n].side
    difference = reports.house_side(house, n) - side
    assert difference > 0
    assert f"{float(difference):.3e}" == gain
    (row,) = reports.check_claims(reports.packet_path(name))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (n, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["result"]) == (house, result)
    assert Fraction(row["case"]["difference"]) == difference


def test_the_ledger_records_each_claim() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
    assert recorded == {
        232: ["#927"],
        268: ["#928"],
        299: ["#929"],
        303: ["#930"],
        307: ["#931"],
    }


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(name: str) -> None:
    _issue, n, _house, _result, _printed, _gain = PACKETS[name]
    record = _json(reports.packet_path(name) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, name, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)


@pytest.mark.parametrize(
    ("name", "one_to_one", "beyond_tenth", "tilted"),
    [
        ("ozden-s232-upper-bound-2026-11-09", True, 6, (80, 81)),
        ("ozden-s268-upper-bound-2026-11-09", True, 4, (99, 98)),
        ("ozden-s299-upper-bound-2026-11-09", False, 12, (85, 85)),
        ("ozden-s303-upper-bound-2026-11-09", True, 5, (111, 112)),
        ("ozden-s307-upper-bound-2026-11-09", True, 5, (112, 107)),
    ],
)
def test_the_identity_measurement_the_notes_cite(
    name: str, *, one_to_one: bool, beyond_tenth: int, tilted: tuple[int, int]
) -> None:
    """Measured against the house's packet first, then the house witness (and, where the
    adapter reads it, the regularized view the source says it started from)."""
    _issue, n, _house, result, _printed, _gain = PACKETS[name]
    record = _json(reports.packet_path(name) / "measure/identity.json")
    assert record["n"] == n
    pair = record["pairs"][0]
    assert (pair["view"], pair["against"]) == ("OZDEN", result)
    assert pair["nearest_centre"]["one_to_one"] is one_to_one
    assert pair["assignment"]["symmetry"] == 0
    assert pair["assignment"]["moved_beyond"]["1e-1"] == beyond_tenth
    tilts = record["tilts"]
    assert (
        tilts["OZDEN"]["tilted_beyond_1_degree"],
        tilts[result]["tilted_beyond_1_degree"],
    ) == tilted
    witness = next(other for other in record["pairs"] if other["against"] == "house-witness")
    assert witness["assignment"]["moved_beyond"] == pair["assignment"]["moved_beyond"]
