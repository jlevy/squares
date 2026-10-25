"""Evan Daniel's issue #806: the #806 import lane of 25 October 2026 (think-2lzo).

One rational centre/half-angle certificate in Evan Daniel's text format, retained under
the source's MIT licence at ``d99925d`` with the seven other files of its ``s182-1024``
set, and read by the ``evand-cert`` adapter: s(182) of #806. The general importer's checks
run on the packet through ``test_upper_bound_reports``; these hold what is particular to
it, as the stage 4 review of 19 October asked of the imports before it (RV-1 of
docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md): the
digests the issue prints, the checkers pinned against the n183 packet's copies, the side
and its print, that it is below every report at 182 by the margin the records state, that
the house reader rebuilds it, the replay's margins, the sharp controls, and the identity
measured against T-174. Every test reads the packet only; none needs the network.
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

PACKET = "evand-n182-2026-10-25"
N = 182
KEY = "[Daniel n182 2026-10-25]"
HOUSE = "[PingYou PR 574 certificates 2026-10-13]"
COMMIT = "d99925d1298262c4ddb81c95abbb6f45adca8d3d"
CANDIDATES = "search/packer/candidates"
CERT = f"{CANDIDATES}/s182-1024.cert"
SIDE = Fraction(13970916436214678735385725854133, 10**30)
#: The SHA-256 digests issue #806 prints for the certificate and its regularized view.
PRINTED_DIGESTS = {
    CERT: "9e12e0a42b05c4fcd2181c5255a4a19ab1aeb9a9f8c95f9943a20998a415fe97",
    f"{CANDIDATES}/s182-1024_regularized.cert": (
        "f1ec415a194b9c0d01d86d23d917a90375779dbd0739966287f189109fd2fabf"
    ),
}
#: The eight files of the s182-1024 set, 167,915 bytes upstream.
SET = (
    "s182-1024.cert",
    "s182-1024.exact.txt",
    "s182-1024.input.txt",
    "s182-1024.json",
    "s182-1024_prior.json",
    "s182-1024_regularized.cert",
    "s182-1024_regularized.json",
    "s182-1024_vs_prior.json",
)
#: The side Subramanya N's Kaggle per-puzzle entry of 24 October lists, with no packing.
KAGGLE_SIDE_ONLY = Fraction(Decimal("13.9709164362306"))


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


def test_the_packet_retains_the_set_at_the_pin_with_the_digests_the_issue_prints() -> None:
    """All eight files of the set, the licence and the credits are retained at d99925d;
    the two checkers the certificate's header names are pinned against the identical
    copies the n183 packet retains, and never run."""
    manifest = _manifest()
    for path, digest in PRINTED_DIGESTS.items():
        assert manifest[path] == digest
    record = _json(_packet() / "acquisition/sources.json")
    (source,) = record["sources"]
    assert source["source_commit"] == COMMIT
    assert source["committed_utc"] == "2026-10-25T04:11:15Z"
    assert source["retained_file_count"] == 10
    assert source["license"].startswith("MIT, copyright (c) 2026 Evan Daniel")
    upstream = (
        sum(item["bytes"] for item in source["pinned_only"]) + source["retained_total_bytes"]
    )
    assert upstream == source["subtree_total_bytes"]
    assert source["retained_total_bytes"] - 1068 - 7501 == 167_915
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
    assert hashlib.sha256(raw).hexdigest() == PRINTED_DIGESTS[CERT]


def test_the_certificate_states_its_side_and_the_house_reader_rebuilds_it() -> None:
    (certificate,) = reports.read_facts(_packet()).values()
    assert (certificate.n, certificate.side, len(certificate.poses)) == (N, SIDE, N)
    assert reports.house_side(KEY, N) == SIDE
    (row,) = reports.load_declaration(_packet())["certificates"]
    assert (row["path"], row["format"]) == (CERT, "evand-cert")
    assert "fact" not in row
    assert Fraction(Decimal(row["offered"])) == SIDE
    header = (_packet() / "source" / CERT).read_text("ascii").splitlines()[1]
    assert header == f"{N} {SIDE.numerator}/{SIDE.denominator}"


def test_the_issues_print_is_the_side_rounded_up_at_12_places() -> None:
    assert Fraction(math.ceil(SIDE * 10**12), 10**12) == Fraction(Decimal("13.970916436215"))
    assert _row()["ceiling"] == "13.9709164362146788"


def test_the_certificate_is_below_its_case_and_every_report_it_names() -> None:
    """3.17e-3 below T-174, the house, and below T-098, #476, #593 and T-056; the margin
    to the house is the house reader's side less this one, exactly."""
    row = _row()
    assert row["smallest"] == reports.THIS
    assert (row["case"]["result"], row["case"]["relation"]) == ("T-174", "below")
    margin = reports.house_side(HOUSE, N) - SIDE
    assert Fraction(row["case"]["difference"]) == margin
    assert Fraction(3174, 10**6) < margin < Fraction(3175, 10**6)
    assert [other["report"] for other in row["pending"]] == [
        "T-098 (#375)",
        "#476 (unnamed)",
        "#593",
        "T-056",
    ]
    assert {other["relation"] for other in row["pending"]} == {"below"}


def test_the_side_only_kaggle_entry_is_above_the_certificate() -> None:
    """Subramanya N's listed side, which the issue quotes and calls very likely the same
    local minimum, states no packing and is no report; it is 1.59e-11 above this side."""
    above = KAGGLE_SIDE_ONLY - SIDE
    assert Fraction(159, 10**13) < above < Fraction(160, 10**13)


def test_the_replay_clears_walls_and_pairs_by_the_margins_the_records_state() -> None:
    positives = reports.check_certification(_packet())
    (margins,) = reports.margins(positives).values()
    for route in kernel.ROUTES:
        assert Fraction(margins[f"{route}_containment_clearance"]) == Fraction(5, 10**21)
        gap = Fraction(margins[f"{route}_best_pair_gap"])
        assert Fraction(999, 10**23) < gap < Fraction(1, 10**20)


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


def test_the_identity_record_pairs_it_with_no_symmetry_of_t174s_packing() -> None:
    """The measurement the register's notes cite (measure/identity.json): no symmetry
    pairs it one to one with T-174's packing, the house witness or T-098's by nearest
    centres; the optimal assignment moves 44 squares beyond a tenth and shares no tilt
    angle. Against the source's binary64 input it is one to one, none beyond 1e-6, and
    against the regularized view one to one at the same side, 5 beyond a tenth."""
    record = _json(_packet() / "measure/identity.json")
    assert record["n"] == N
    pairs = {pair["against"]: pair for pair in record["pairs"]}
    assert set(pairs) == {"T-174", "house-witness", "T-098", "input", "regularized"}
    for label in ("T-174", "house-witness", "T-098"):
        pair = pairs[label]
        assert pair["nearest_centre"]["one_to_one"] is False
        assert pair["assignment"]["moved_beyond"]["1e-1"] == 44
        assert pair["assignment"]["moved_beyond"]["1e-2"] == 79
        assert pair["bands"]["tilt_angles_shared_within_1e-4_degrees"] == 0
        assert pair["bands"]["tilted_paired_opposite_sign"] == 16
    assert Fraction(pairs["T-098"]["side_difference_exact"]) == -(
        Fraction(3493522678280359751787532508193, 25 * 10**28) - SIDE
    )
    given = pairs["input"]["nearest_centre"]
    assert (given["one_to_one"], given["symmetry"], given["moved_beyond"]["1e-6"]) == (
        True,
        0,
        0,
    )
    view = pairs["regularized"]
    assert Fraction(view["side_difference_exact"]) == 0
    assert view["nearest_centre"]["one_to_one"] is True
    assert view["nearest_centre"]["moved_beyond"]["1e-9"] == 49
    assert view["nearest_centre"]["moved_beyond"]["1e-1"] == 5
    assert record["tilts"]["#806"]["tilted_beyond_1_degree"] == 68
    assert record["tilts"]["T-174"]["tilted_beyond_1_degree"] == 59
