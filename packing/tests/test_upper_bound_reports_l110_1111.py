"""The upper-bound import of the intake pass's lane L110 of 11 November 2026 (think-3guf).

One packet, read by the ``witness-corners`` adapter: Doğa Özden's #960 at 237
(kenaznia-doga/s237-upper-bound 13c4b23). The witness was promoted to exact rationals by
this repository's ``packing-witness promote --strategy robust-rational`` from a decimal
pose the source retains, so its side is a fraction of about 186 places, and the issue
prints it rounded up at 12 places. The issue names the record T-189 but prints T-190's
side, the case's house, which the comparison reads. The general importer's checks run on
the packet through ``test_upper_bound_reports``; these hold what is particular to it: the
digests the issue and README print, the print against the exact side, the house it is
compared with and the improvement the issue states, the pending re-certification it is
also below, the ledger's verdict, the retained sharp controls, the identity measurement,
the contraction margins and the L-step scan the register's notes cite. Every test reads
the packet and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-960-20261111"
NAME = "ozden-s237-upper-bound-2026-11-11"
ISSUE = 960
N = 237
#: The house the certificate is compared with, its register entry, the issue's 12-place
#: print, the side rounded up at 16 places as the claim record prints it, and the
#: improvement the issue states.
HOUSE = "[Couzo n237 2026-10-15]"
RESULT = "T-190"
PRINTED = "15.893805580573"
CEILING = "15.8938055805725742"
GAIN = "8.798e-03"
#: The record the issue names, Couzo's issue-607 certificate, whose side is not the one
#: the issue prints, and the 16-place side the issue prints, below the exact side.
NAMED = "[Couzo certificates 2026-10-14]"
PRINTED_16 = "15.8938055805725735"
#: The re-certification of T-190's packing pending adoption at 237, which the claim
#: record compares the certificate with as well.
PENDING = "T-253, Polkovskyi of 23 October (no issue)"
#: The SHA-256 digests the issue (the witness) and the README (both files) print: the
#: candidate YAML's, then its JSON copy's.
PRINTED_DIGESTS = (
    "80687bdceef5780f907c7f47a181802fbfb76a026d077aa18f7bb3eaa3ec3833",
    "98f55b8ea9a5ae030fbdabc2c21b37e1a72f09a0eb656a6872d48e47ac573ca7",
)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest() -> dict[str, str]:
    text = (reports.packet_path(NAME) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


def _side() -> Fraction:
    return reports.read_facts(reports.packet_path(NAME))[N].side


def test_the_packet_holds_the_files_whose_digests_the_issue_prints() -> None:
    manifest = _manifest()
    candidate, copy = PRINTED_DIGESTS
    assert manifest[f"n-{N}-candidate.yaml"] == candidate
    assert manifest[f"n{N}-witness.json"] == copy
    # The decimal pose the witness's source.path names is retained beside it.
    assert f"n-{N}-decimal-pose.yaml" in manifest


def test_the_print_is_its_exact_side_rounded_up_and_its_reader_rebuilds_it() -> None:
    """The issue's 12-place print is the side rounded up, and the JSON states the same
    packing as the YAML (the declaration's ``same_packing``, which ``read_facts`` holds).
    The 16-place side the issue also prints lies below the exact side."""
    declaration = reports.load_declaration(reports.packet_path(NAME))
    assert declaration["source_key"] == f"[Özden s{N} upper bound {NAME[-10:]}]"
    assert declaration["issue"].endswith(f"/issues/{ISSUE}")
    assert (declaration["requested"], declaration["replayed"]) == ([N], [N])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (N, "witness-corners", PRINTED)
    assert [other["path"] for other in row.get("same_packing", [])] == [f"n{N}-witness.json"]
    side = _side()
    assert _up(side, 12) == Fraction(Decimal(PRINTED))
    assert _up(side, 16) == Fraction(Decimal(CEILING))
    assert Fraction(Decimal(PRINTED_16)) < side
    assert reports.house_side(declaration["source_key"], N) == side


def test_the_certificate_is_below_its_house_by_the_improvement_the_issue_states() -> None:
    """The gain is measured against T-190, whose side the issue prints; the T-189 it names
    is 2.40e-11 above T-190, so the 4-figure gain is the same against either."""
    side = _side()
    difference = reports.house_side(HOUSE, N) - side
    assert difference > 0
    assert f"{float(difference):.3e}" == GAIN
    named = reports.house_side(NAMED, N) - reports.house_side(HOUSE, N)
    assert f"{float(named):.2e}" == "2.40e-11"
    (row,) = reports.check_claims(reports.packet_path(NAME))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (N, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["result"]) == (HOUSE, RESULT)
    assert Fraction(row["case"]["difference"]) == difference
    (pending,) = row["pending"]
    assert (pending["report"], pending["relation"]) == (PENDING, "below")


def test_the_ledger_records_the_claim() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
    assert recorded == {N: [f"#{ISSUE}"]}


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    record = _json(reports.packet_path(NAME) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (N, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)


def test_the_identity_measurement_the_notes_cite() -> None:
    """Measured against T-190's packet first, then T-189's, the regularized view and the
    house witness, which measure the same: no symmetry pairs the two one to one, the
    optimal assignment moves 72 squares beyond a tenth, and 42 squares are tilted beyond
    a degree here against T-190's 49."""
    record = _json(reports.packet_path(NAME) / "measure/identity.json")
    assert record["n"] == N
    pair = record["pairs"][0]
    assert (pair["view"], pair["against"]) == ("OZDEN", RESULT)
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 72
    assert pair["centred"]["turned_beyond_1_degree"] == 73
    tilts = record["tilts"]
    assert (
        tilts["OZDEN"]["tilted_beyond_1_degree"],
        tilts[RESULT]["tilted_beyond_1_degree"],
    ) == (42, 49)
    for against in ("T-189", "regularized", "house-witness"):
        other = next(row for row in record["pairs"] if row["against"] == against)
        assert other["nearest_centre"]["one_to_one"] is False
        assert other["assignment"]["moved_beyond"] == pair["assignment"]["moved_beyond"]


def test_the_gain_is_far_above_both_certificates_contraction_margins() -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. T-190's
    certificate at 237 has 1.59e-19 of padding and T-189's 2.39e-11, so no part of the gain
    is padding and the entry is not held for it."""
    gain = reports.house_side(HOUSE, N) - _side()
    receipts = (
        (f"contraction-n{N}", RESULT, HOUSE),
        (f"contraction-n{N}-t189", "T-189", NAMED),
    )
    for receipt, label, key in receipts:
        record = _json(reports.packet_path(NAME) / f"measure/{receipt}.json")
        assert (record["n"], record["certificate"]["label"]) == (N, label)
        assert record["routes_accept"] is True
        assert 0 < Fraction(record["margin"]) < Fraction(1, 10**10)
        assert record["against"]["within_margin"] is False
        assert Fraction(record["against"]["gain"]) == reports.house_side(key, N) - _side()
    own = _json(reports.packet_path(NAME) / f"measure/contraction-n{N}-own.json")
    assert own["routes_accept"] is True
    assert gain > 10**6 * Fraction(own["margin"])


def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere() -> None:
    record = _json(reports.packet_path(NAME) / "measure/l-step-scan.json")
    assert Fraction(record["with"][str(N)]) == _side()
    improved = {row["n"] for row in record["l_step"]["improves"]}
    assert all(row["from"] != N for row in record["l_step"]["improves"])
    assert N not in improved
    assert record["monotonicity"]["improves"] == []
