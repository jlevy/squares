"""The upper-bound imports of the intake pass's lane L71 of 9 November 2026 (think-3guf).

Two packets, each read by the ``witness-corners`` adapter: Doğa Özden's #935 at 172
(kenaznia-doga/s172-upper-bound 2ce1f7c) and #936 at 270 (s270-upper-bound 78ab8ce). Each
witness was promoted to exact rationals by this repository's ``packing-witness promote
--strategy robust-rational`` from a decimal pose the source retains, so its side is a
fraction of about 90 and 190 digits, and each issue prints it rounded up at 12 places. The
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

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-935-936-20261109"

#: Each packet with its issue, its count, the house it is compared with, that house's
#: register entry, the issue's 12-place print and the improvement the issue states.
PACKETS: dict[str, tuple[int, int, str, str, str, str]] = {
    "ozden-s172-upper-bound-2026-11-09": (
        935,
        172,
        "[Daniel issue 845 2026-10-29]",
        "T-257",
        "13.614689853287",
        "3.246e-03",
    ),
    "ozden-s270-upper-bound-2026-11-09": (
        936,
        270,
        "[Daniel n270 sweep 2026-10-20]",
        "T-224",
        "16.928148603343",
        "1.365e-05",
    ),
}
#: The SHA-256 digests the issues (the witness) and the READMEs (both files) print, by count:
#: the candidate YAML's, then its JSON copy's.
PRINTED_DIGESTS = {
    172: (
        "0df5ae7936950b9a1fe06832cb8f8bdc21dbae9e0d009c6b87302a14c452b2af",
        "311a83339e86d503954c8f423b0c6e0ca3c2c5bfb6e80c37d53ec064667aa2bf",
    ),
    270: (
        "f2b62bf0f89eabe4c9872cb2c37cca9a24a3926e939cb017278c0e5d16fa9386",
        "1d01092fa384d09035eb7103d7494bff48c80880574a97d13240e143874c854b",
    ),
}
#: Each certificate's side rounded up at 16 places, as its claim record prints it.
CEILINGS = {
    172: "13.6146898532862152",
    270: "16.9281486033428544",
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
    # The decimal pose the witness's source.path names is retained beside it.
    assert f"n-{n}-decimal-pose.yaml" in manifest


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
    assert recorded == {172: ["#935"], 270: ["#936"]}


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
        ("ozden-s172-upper-bound-2026-11-09", False, 15, (49, 49)),
        ("ozden-s270-upper-bound-2026-11-09", True, 1, (66, 67)),
    ],
)
def test_the_identity_measurement_the_notes_cite(
    name: str, *, one_to_one: bool, beyond_tenth: int, tilted: tuple[int, int]
) -> None:
    """Measured against the house's packet first, then the house witness (and the
    regularized view the source says it started from)."""
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
