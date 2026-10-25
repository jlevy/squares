"""Amund Kristiansen's issue #798: the #798 import lane of 24 October 2026.

Fourteen dilation certificates in Evan Daniel's text format, retained under the author's
CC0 1.0 dedication (#755, issuecomment-6388401978) and read by the `evand-cert` adapter,
all beyond the ``n <= 324`` case corpus: twelve are beyond-horizon rows of the source
register, and 372 and 412 are above Francisco Couzo's 43f666c, an earlier publication, so
not recorded. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digests and sides
the issue prints, the requested roster the walk records, the comparison in report order,
the rows and what they supersede, the replay's margins, the sharp controls, and the
identity measured against the packings the issue says each was found from. Every test
reads the retained packet, the walk and the source register only; none needs the network.
"""

from __future__ import annotations

import hashlib
import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_source_coverage as coverage_check
from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from sqpack.yamlio import safe_load

PACKET = "amundsk-issue798-2026-10-24"
WALK = reports.ROOT / "campaign/issue-intake/upper-bounds-issue798-20261024"
COVERAGE = reports.REPO / "packing/frontier/source-coverage.yaml"
#: Each count's side as the issue prints it, rounded up at 12 places, and the exact side
#: S' its certificate table prints.
ISSUE = {
    334: (
        "18.786944251907",
        "18786944251906076944251887289623/1000000000000000000000000000000",
    ),
    338: (
        "18.887926955871",
        "18887926955870337926955851449621/1000000000000000000000000000000",
    ),
    343: (
        "18.976291436857",
        "18976291436856010291436837033619/1000000000000000000000000000000",
    ),
    372: ("19.806121548598", "9903060774298500560774288597301/500000000000000000000000000000"),
    376: (
        "19.884256884304",
        "19884256884303024256884283139601/1000000000000000000000000000000",
    ),
    377: ("19.906977592561", "99534887962803649887962704113/5000000000000000000000000000"),
    379: (
        "19.950579117727",
        "19950579117726400579117706449599/1000000000000000000000000000000",
    ),
    382: ("19.987567257068", "9993783628533528783628523534799/500000000000000000000000000000"),
    412: ("20.822875656790", "10411437828394813437828384401791/500000000000000000000000000000"),
    416: ("20.889554050378", "1044477702518860877702517816379/50000000000000000000000000000"),
    457: ("21.887025665808", "68396955205649731330205581333/3125000000000000000000000000"),
    458: ("21.888719382533", "547217984563320717984562773489/25000000000000000000000000000"),
    502: ("22.891715605670", "1144585780283463585780282318977/50000000000000000000000000000"),
    504: (
        "22.921326029542",
        "22921326029541371326029518449539/1000000000000000000000000000000",
    ),
}
#: The two counts where Couzo's 43f666c, pushed at 2026-10-24T06:10:44Z, is below the issue.
ABOVE_43F = (372, 412)
RECORDED = tuple(n for n in ISSUE if n not in ABOVE_43F)
#: The row each recorded count supersedes, the current row on main 2ed0ea740.
SUPERSEDED = {
    334: "couzo-issue763-2026-10-23",
    338: "alexchilton-fault-line-2026-10-23",
    343: "couzo-issue763-2026-10-23",
    376: "tymchishin-22-3662-2026-10-23",
    377: "kyleluecke-inos-2026-10-23",
    379: "couzo-964ee2b-2026-10-23",
    382: "couzo-issue670-2026-10-17",
    416: "couzo-issue763-2026-10-23",
    457: "couzo-issue763-2026-10-23",
    458: "couzo-issue763-2026-10-23",
    502: "couzo-issue763-2026-10-23",
    504: "alexchilton-fault-line-2026-10-23",
}
#: The one report that may stand between a count's row on main and this packet's: Couzo's
#: 43f666c, the earlier publication at 376, 377, 416, 458, 502 and 504, whose import
#: (think-gn29) supersedes those rows in turn once it lands.
BETWEEN = frozenset({"couzo-43f666c-2026-10-24"})
#: The issue's lineage table: squares moved beyond 0.1 against #763's packing at the count.
LINEAGE_BEYOND_TENTH = {
    334: 20,
    338: 5,
    343: 5,
    372: 0,
    376: 19,
    377: 29,
    379: 3,
    382: 1,
    412: 0,
    416: 8,
    457: 26,
    458: 11,
    502: 8,
    504: 29,
}


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _manifest() -> dict[str, str]:
    text = (_packet() / "acquisition/upstream-subtree.sha256").read_text("utf-8")
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _ceil_at(value: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(value * 10**places), 10**places)


def _claims() -> dict[int, dict[str, Any]]:
    return {row["n"]: row for row in reports.check_claims(_packet())["results"]}


def test_the_packet_retains_all_29_files_under_the_authors_cc0_dedication() -> None:
    manifest = _manifest()
    assert len(manifest) == 29
    record = json.loads((_packet() / "acquisition/sources.json").read_text("utf-8"))
    (source,) = record["sources"]
    assert source["source_commit"] == "c9be7b70e2220c2eccb2c5ea746094bc85dda405"
    assert source["retained_file_count"] == 29
    assert source["pinned_only"] == []
    assert source["license"].startswith("CC0 1.0")
    assert "issuecomment-6388401978" in source["license"]
    folder = reports.REPO / source["archived_path"]
    for name, digest in manifest.items():
        assert hashlib.sha256((folder / name).read_bytes()).hexdigest() == digest
    answer = json.loads((_packet() / "acquisition/licence-answer.json").read_text("utf-8"))
    assert answer["html_url"].endswith("#issuecomment-6388401978")
    assert "CC0 1.0" in answer["body"]
    assert "c9be7b70e2220c2eccb2c5ea746094bc85dda405" in answer["body"]


def test_each_certificate_has_the_digest_and_the_side_the_issue_prints() -> None:
    body = json.loads((_packet() / "acquisition/issue.json").read_text("utf-8"))["body"]
    manifest = _manifest()
    certificates = reports.read_facts(_packet())
    assert sorted(certificates) == sorted(ISSUE)
    for n, (printed, exact) in ISSUE.items():
        assert manifest[f"s{n}_amund.cert"] in body
        assert manifest[f"s{n}_amund.input.txt"] in body
        assert exact in body
        assert certificates[n].side == Fraction(exact)
        assert _ceil_at(Fraction(exact), 12) == Fraction(Decimal(printed))


def test_the_requested_roster_is_what_the_walk_records() -> None:
    declaration = reports.load_declaration(_packet())
    assert declaration["requested"] == declaration["replayed"] == list(RECORDED)
    assert declaration["houses"] == []
    ledger = json.loads((WALK / "ledger.json").read_text("utf-8"))
    verdicts = {
        count["n"]: step["verdict"]
        for count in ledger["counts"]
        for step in count["steps"]
        if step["report"] == "#798"
    }
    assert verdicts == {n: "not recorded" if n in ABOVE_43F else "recorded" for n in ISSUE}
    assert ledger["summary"]["undecided"] == 0


def test_the_comparison_finds_43f666c_below_only_at_372_and_412() -> None:
    claims = _claims()
    for n, row in claims.items():
        assert row["case"] is None
        assert row["construction"]["relation"] == "below"
        couzo = [other for other in row["pending"] if other["report"].endswith("@43f666c")]
        if n in ABOVE_43F:
            assert row["smallest"] == "franciscouzo/square-packing@43f666c"
            assert [other["relation"] for other in couzo] == ["above"]
            assert not row["requested"]
        else:
            assert row["smallest"] == reports.THIS
            assert {other["relation"] for other in row["pending"]} == {"below"}
            assert row["requested"]


def test_the_rows_supersede_each_counts_row_and_read_their_claims_record() -> None:
    """Each count's row on main 2ed0ea740 leads to this packet's row in report order:
    directly, or through Couzo's 43f666c row where that import has landed (`BETWEEN`),
    since 43f666c is the earlier report at six of the counts."""
    claims = coverage_check.load_claims(_packet() / reports.BEYOND)
    assert claims == {n: ISSUE[n][0] for n in RECORDED}
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    current = coverage_check.current_beyond_horizon(coverage)
    for n in RECORDED:
        assert current[n]["source_id"] == PACKET
        assert current[n]["value"] == ISSUE[n][0]
        rows = {
            row["source_id"]: row for row in coverage["beyond_horizon_claims"] if row["n"] == n
        }
        link = SUPERSEDED[n]
        while rows[link]["superseded_by"] != PACKET:
            assert rows[link]["disposition"] == "superseded"
            link = rows[link]["superseded_by"]
            assert link in BETWEEN, (n, link)
        assert rows[link]["disposition"] == "superseded"
    assert not any(
        row["source_id"] == PACKET and row["n"] in ABOVE_43F
        for row in coverage["beyond_horizon_claims"]
    )


def test_the_replay_clears_walls_and_pairs_by_the_margins_a_dilation_gives() -> None:
    positives = reports.check_certification(_packet())
    margins = reports.margins(positives)
    assert sorted(int(n) for n in margins) == list(RECORDED)
    for values in margins.values():
        for route in ("exact_verify", "independent"):
            assert Fraction(values[f"{route}_containment_clearance"]) >= Fraction(598, 10**15)
            assert Fraction(values[f"{route}_best_pair_gap"]) >= Fraction(119, 10**14)


@pytest.mark.parametrize("n", RECORDED)
def test_the_retained_sharp_controls_are_as_expected(n: int) -> None:
    record = json.loads(
        (_packet() / f"receipts/sharp-controls-n{n:03d}.json").read_text("utf-8")
    )
    assert record["all_as_expected"] is True
    assert Fraction(record["epsilon"]) == kernel.SHARP_EPSILON
    assert (record["packet"], record["n"]) == (PACKET, n)


@pytest.mark.parametrize("n", sorted(ISSUE))
def test_the_identity_reproduces_the_issues_lineage_table(n: int) -> None:
    """The issue matches each packing one to one with #763's at the count by an optimal
    assignment on centres, best of the eight symmetries; measured here, the squares moved
    beyond a tenth are its figures, so 372 and 412 are refinements and the rest new
    arrangements found from those packings."""
    record = json.loads((_packet() / f"measure/identity-n{n:03d}.json").read_text("utf-8"))
    (start,) = (pair for pair in record["pairs"] if pair["against"].startswith("964ee2b"))
    assert start["assignment"]["moved_beyond"]["1e-1"] == LINEAGE_BEYOND_TENTH[n]
