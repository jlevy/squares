"""Evan Daniel's issue #824: the #824 import lane of 26 October 2026 (think-3xn9).

One rational centre/half-angle certificate in Evan Daniel's text format, first committed
at ``1be69ca`` and retained under the source's MIT licence at ``6067db5``, the head, with
the five other files of its ``s299-1025`` set, and read by the ``evand-cert`` adapter:
s(299) of #824. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it, as the stage 4 review
of 19 October asked of the imports before it (RV-1 of
docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md): the
digest the issue prints, the checkers pinned against the n183 packet's copies, the side
and its print, that it is below the case's ceiling by the margin the records state, that
the house reader rebuilds it, the replay's margins, the sharp controls, and the identity
measured against T-101. Every test reads the packet only; none needs the network.
"""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

PACKET = "evand-n299-2026-10-26"
N = 299
KEY = "[Daniel n299 2026-10-26]"
HOUSE = "[evand exact optima 2026-10-05]"
COMMIT = "6067db5bf4d41dab7f0e1475e9fa845c0c6d2133"
CANDIDATES = "search/packer/candidates"
CERT = f"{CANDIDATES}/s299-1025.cert"
SIDE = Fraction(8901847717666168847717657266821, 5 * 10**29)
#: The SHA-256 digest issue #824 prints for the certificate.
PRINTED_DIGEST = "1ad65a494df088a86890abf3a2d593152df2439be39f1beaacf5a7e5c102bb71"
#: The six files of the s299-1025 set at the pin, 129,275 bytes upstream.
SET = (
    "s299-1025.cert",
    "s299-1025.exact.txt",
    "s299-1025.input.txt",
    "s299-1025.json",
    "s299-1025.predescent.txt",
    "s299-1025_prior.json",
)
#: The sides two Kaggle per-puzzle entries the issue quotes list, with no packing.
KAGGLE_SIDE_ONLY = (Fraction(Decimal("17.802718854399")), Fraction(Decimal("17.798169713703")))


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _row() -> dict[str, Any]:
    (row,) = reports.check_claims(_packet())["results"]
    return row


def _manifest() -> dict[str, str]:
    text = (_packet() / "acquisition/upstream-subtree.sha256").read_text("utf-8")
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def test_the_packet_retains_the_set_at_the_pin_with_the_digest_the_issue_prints() -> None:
    """All six files of the set, the licence and the credits are retained at 6067db5; the
    two checkers the certificate's header names are pinned against the identical copies
    the n183 packet retains, and never run."""
    manifest = _manifest()
    assert manifest[CERT] == PRINTED_DIGEST
    record = _json(_packet() / "acquisition/sources.json")
    (source,) = record["sources"]
    assert source["source_commit"] == COMMIT
    assert source["committed_utc"] == "2026-10-26T03:47:41Z"
    assert source["retained_file_count"] == 8
    assert source["license"].startswith("MIT, copyright (c) 2026 Evan Daniel")
    upstream = (
        sum(item["bytes"] for item in source["pinned_only"]) + source["retained_total_bytes"]
    )
    assert upstream == source["subtree_total_bytes"]
    assert source["retained_total_bytes"] - 1068 - 7501 == 129_275
    assert {f"{CANDIDATES}/{name}" for name in SET} | {"LICENSE", "CREDITS.md"} == {
        path for path in manifest if not path.startswith("search/exact/")
    }
    twins = {item["path"]: item["identical_to"] for item in source["pinned_only"]}
    n183 = "packing/resources/web/evand-n183-subgrid-2026-10-19/source/search/exact"
    assert twins == {
        "search/exact/verify_cert.py": f"{n183}/verify_cert.py",
        "search/exact/verify_cert2.py": f"{n183}/verify_cert2.py",
    }
    for path, twin in twins.items():
        raw = (reports.REPO / twin).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == manifest[path]
    raw = (_packet() / "source" / CERT).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PRINTED_DIGEST


def test_the_certificate_states_its_side_and_the_house_reader_rebuilds_it() -> None:
    (certificate,) = reports.read_facts(_packet()).values()
    assert (certificate.n, certificate.side, len(certificate.poses)) == (N, SIDE, N)
    assert reports.house_side(KEY, N) == SIDE
    (row,) = reports.load_declaration(_packet())["certificates"]
    assert (row["path"], row["format"]) == (CERT, "evand-cert")
    assert "fact" not in row
    assert row["first_committed"] == "2026-10-26T03:30:38Z"
    header = (_packet() / "source" / CERT).read_text("ascii").splitlines()[1]
    assert header == f"{N} {SIDE.numerator}/{SIDE.denominator}"


def test_the_issues_print_is_the_side_rounded_up_at_12_places() -> None:
    assert Fraction(math.ceil(SIDE * 10**12), 10**12) == Fraction(Decimal("17.803695435333"))
    assert _row()["ceiling"] == "17.8036954353323377"


def test_the_certificate_is_below_its_case_by_the_margin_the_records_state() -> None:
    """1.92e-2 below the case's ceiling, T-101's exact certificate of the Kingbird
    catalogue's 33/2 + sqrt(7)/2, and below the closed form itself; no other report at 299
    is pending."""
    row = _row()
    assert row["smallest"] == reports.THIS
    assert (row["case"]["result"], row["case"]["relation"]) == ("T-101", "below")
    margin = reports.house_side(HOUSE, N) - SIDE
    assert Fraction(row["case"]["difference"]) == margin
    assert Fraction(1918, 10**5) < margin < Fraction(1919, 10**5)
    assert row["pending"] == []
    # 33/2 + sqrt(7)/2 > SIDE  <=>  sqrt(7) > 2 * SIDE - 33  <=>  7 > (2 * SIDE - 33)^2.
    assert 2 * SIDE - 33 > 0
    assert (2 * SIDE - 33) ** 2 < 7


def test_the_side_only_kaggle_entries_are_below_the_certificate() -> None:
    """The two listed sides the issue quotes state no packing and are no report; both lie
    below this side, as the issue says."""
    for listed in KAGGLE_SIDE_ONLY:
        assert listed < SIDE


def test_the_replay_clears_walls_and_pairs_by_the_margins_the_records_state() -> None:
    positives = reports.check_certification(_packet())
    (margins,) = reports.margins(positives).values()
    for route in kernel.ROUTES:
        wall = Fraction(margins[f"{route}_containment_clearance"])
        assert Fraction(499, 10**15) < wall < Fraction(5, 10**13)
        gap = Fraction(margins[f"{route}_best_pair_gap"])
        assert Fraction(999, 10**15) < gap < Fraction(1, 10**12)


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    """Every control of `devtools.upper_bound_sharp_controls` as expected on both routes:
    each translation accepted at exact contact with margin 0 and refused 1e-30 past it,
    each enlargement refused at contact for its shape alone and past it for the overlap or
    the wall too, and the duplicated square refused."""
    record = _json(_packet() / "receipts/sharp-controls.json")
    assert (record["packet"], record["n"], record["all_as_expected"]) == (PACKET, N, True)
    assert Fraction(record["side"]) == SIDE
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    rows = {(row["control"], row["where"]): row for row in record["controls"]}
    for control in sharp.CONTROLS:
        wheres = ("gross",) if control == sharp.DUPLICATE else ("at-contact", "past-contact")
        for where in wheres:
            row = rows.pop((control, where))
            assert row["as_expected"] is True
            assert set(row["routes"]) == set(kernel.ROUTES)
            translated = control in {sharp.SIDE_LOWERED, sharp.TIGHTEST_PAIR, sharp.NEAR_WALL}
            accepted = translated and where == "at-contact"
            for verdict in row["routes"].values():
                assert verdict["passed"] is accepted
                if where == "at-contact":
                    assert Fraction(verdict[row["margin"]]) == 0
                elif where == "past-contact":
                    assert Fraction(verdict[row["margin"]]) <= -kernel.SHARP_EPSILON
    assert rows == {}


def test_the_identity_record_pairs_it_with_no_symmetry_of_the_houses_packing() -> None:
    """The measurement the register's notes cite (measure/identity.json): no symmetry
    pairs it one to one with T-101's certificate of the house's packing by nearest
    centres; the optimal assignment moves 124 squares beyond a tenth. Against the
    source's binary64 input it is one to one, none beyond 1e-9."""
    record = _json(_packet() / "measure/identity.json")
    assert record["n"] == N
    pairs = {pair["against"]: pair for pair in record["pairs"]}
    assert set(pairs) == {"T-101", "input"}
    house = pairs["T-101"]
    assert house["nearest_centre"]["one_to_one"] is False
    assert house["assignment"]["moved_beyond"]["1e-1"] == 124
    assert house["assignment"]["moved_beyond"]["1e-2"] == 243
    assert Fraction(house["side_difference_exact"]) == SIDE - reports.house_side(HOUSE, N)
    given = pairs["input"]["nearest_centre"]
    assert (given["one_to_one"], given["symmetry"], given["moved_beyond"]["1e-9"]) == (
        True,
        0,
        0,
    )
    assert record["tilts"]["#824"]["tilted_beyond_1_degree"] == 83
    assert record["tilts"]["T-101"]["tilted_beyond_1_degree"] == 38
