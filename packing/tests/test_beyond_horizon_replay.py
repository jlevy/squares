"""The beyond-horizon rows of issues #666, #670, #672, #675 and #719, recorded on 22 October.

`devtools.beyond_horizon_replay` decides the rows at or below 1024 of five reports from
their packets: Joost de Winter's #666 (11 of its 19 rows; the 8 above 1024 wait on the
owner), the rows beyond the corpus of Francisco Couzo's #670, #672 and #675, whose in-corpus
rows T-226 to T-228 register, and Mykhailo Polkovskyi's #719, whose packet keeps derived
facts and no upstream byte. These tests hold what is particular to the import:
each issue table's rows and the certificate each reads, the receipts and records against the
packets, the first commit of every certificate, each row's place in the backlog ledger's
report order and the coverage register's rows that follow from it, each walked count as
one chain in report order, and the forged receipts a check must refuse. Every test reads
the retained packets, the ledger and the source register only; none needs the network.
"""

from __future__ import annotations

import copy
import json
from collections import Counter
from fractions import Fraction
from typing import Any

import pytest

from devtools import beyond_horizon_replay as replay
from devtools import check_source_coverage as coverage_check
from devtools.retained_data import read_retained_bytes
from sqpack.yamlio import safe_load

LEDGER = replay.ROOT / "campaign/issue-intake/upper-bounds-backlog-20261022"
LEDGER_719 = replay.ROOT / "campaign/issue-intake/upper-bounds-issue719-20261022"
MISHAPOLK = "mishapolk-issue719-2026-10-22"
#: The four reports the backlog ledger walks.
BACKLOG = (666, 670, 672, 675)
#: Each report's rows: the table's, the decided (beyond the corpus to 1024) and the held.
ROWS = {666: (19, 11, 8), 670: (73, 72, 0), 672: (46, 44, 0), 675: (79, 78, 0)}
#: The rows #719 supersedes on entry, by the source that held each count.
SUPERSEDED_BY_719 = {
    "muglich-issue686-2026-10-19": 42,
    "couzo-verified-bounds-2026-10-14": 39,
    "couzo-issue715-2026-10-21": 16,
    "couzo-issue678-2026-10-18": 7,
    "couzo-certificates-2026-10-14": 3,
    "couzo-issue670-2026-10-17": 3,
    "couzo-extended-range-reports-2026-10-08": 1,
}
#: #670's rows that are the current row at their count, and the rows they supersede.
CURRENT_670 = {
    364: "evand-compositions-2026-10-13",
    370: "couzo-verified-bounds-2026-10-14",
    382: "couzo-certificates-2026-10-14",
    403: "couzo-verified-bounds-2026-10-14",
    444: "couzo-verified-bounds-2026-10-14",
    452: "couzo-verified-bounds-2026-10-14",
    536: "couzo-verified-bounds-2026-10-14",
    922: "couzo-verified-bounds-2026-10-14",
}
#: The starts each report's rows beat first in report order, by the start's source; eight
#: are #670's current rows above, and the rest name the report that beat them first, not
#: the later #678, #686 or #715 row that superseded them on ``main``.
FIRST_BEATEN = {
    ("couzo-verified-bounds-2026-10-14", "couzo-issue670-2026-10-17"): 56,
    ("couzo-verified-bounds-2026-10-14", "couzo-issue675-2026-10-18"): 10,
    ("couzo-verified-bounds-2026-10-14", "couzo-issue672-2026-10-17"): 8,
    ("couzo-verified-bounds-2026-10-14", "de-winter-issue666-2026-10-17"): 1,
    ("couzo-certificates-2026-10-14", "couzo-issue670-2026-10-17"): 7,
    ("evand-compositions-2026-10-13", "couzo-issue670-2026-10-17"): 1,
    ("evand-fresh-compositions-2026-10-14", "couzo-issue670-2026-10-17"): 1,
    ("fang-excess-theorem-2026-10-13", "couzo-issue672-2026-10-17"): 1,
}
#: Each report's superseded rows, by the source of the next report the walk records.
SUCCESSORS = {
    "de-winter-issue666-2026-10-17": {
        "couzo-issue675-2026-10-18": 6,
        "couzo-issue672-2026-10-17": 2,
        "couzo-issue678-2026-10-18": 1,
        "muglich-issue686-2026-10-19": 1,
        "couzo-issue715-2026-10-21": 1,
    },
    "couzo-issue670-2026-10-17": {
        "couzo-issue675-2026-10-18": 25,
        "couzo-issue672-2026-10-17": 19,
        "muglich-issue686-2026-10-19": 9,
        "couzo-issue678-2026-10-18": 9,
        "couzo-issue715-2026-10-21": 2,
    },
    "couzo-issue672-2026-10-17": {
        "couzo-issue675-2026-10-18": 32,
        "couzo-issue678-2026-10-18": 7,
        "muglich-issue686-2026-10-19": 4,
        "couzo-issue715-2026-10-21": 1,
    },
    "couzo-issue675-2026-10-18": {
        "couzo-issue678-2026-10-18": 54,
        "muglich-issue686-2026-10-19": 18,
        "couzo-issue715-2026-10-21": 6,
    },
}


def _read(path: Any) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def test_each_issue_table_reads_its_rows_and_the_certificate_each_names() -> None:
    for issue, (rows, decided, held) in ROWS.items():
        chosen = replay.release(issue)
        assert len(replay.claims(chosen)) == rows
        assert len(replay.decided_claims(chosen)) == decided == chosen.decided
        assert len(replay.held_claims(chosen)) == held
        digests = replay.manifest(chosen)
        for row in [*replay.decided_claims(chosen), *replay.held_claims(chosen)]:
            assert row.path in digests, (issue, row.n)
            assert read_retained_bytes(replay.archive(chosen) / row.path), (issue, row.n)
    deletions = [
        (row.n, row.certificate_n, row.deleted)
        for row in replay.decided_claims(replay.release(675))
        if row.deleted
    ]
    assert deletions == [(992, 993, 1), (995, 996, 1)]
    above = [row.n for row in replay.held_claims(replay.release(666))]
    assert above == [1061, 1128, 1196, 1266, 1339, 1413, 1489, 1568]


def test_a_table_that_links_another_commit_or_folder_is_refused() -> None:
    couzo = replay.release(670)
    body = json.loads((couzo.directory / replay.ISSUE).read_text(encoding="utf-8"))["body"]
    with pytest.raises(replay.ReplayError, match="links another commit"):
        couzo.read(body.replace(couzo.pin, "0" * 40), couzo)
    de_winter = replay.release(666)
    text = json.loads((de_winter.directory / replay.ISSUE).read_text(encoding="utf-8"))["body"]
    with pytest.raises(replay.ReplayError, match="another folder"):
        de_winter.read(text.replace(de_winter.pin, de_winter.retained), de_winter)


def test_the_receipts_records_and_coverage_rows_hold() -> None:
    assert replay.check(replay=False) == []


def test_every_certificate_was_first_committed_at_the_commit_the_record_states() -> None:
    """Couzo's at each issue's own pin, minutes before the issue; de Winter's at b9cdc16b,
    whose time the issue's off-branch pin b3152f52 shares, three minutes before the issue."""
    for chosen in replay.RELEASES.values():
        commits = _read(chosen.directory / replay.FIRST_COMMITS)
        assert commits["retained_commit"] == chosen.retained
        for row in commits["rows"]:
            assert (row["first_commit"], row["committed"]) == chosen.first_commit_of(row["n"])
        record = _read(chosen.directory / replay.RECORD)
        for row in record["results"]:
            assert row["first_committed"] == chosen.first_commit_of(row["n"])[1]
    later = replay.release(719)
    assert {row["n"] for row in _read(later.directory / replay.FIRST_COMMITS)["rows"]} >= {447}
    assert later.first_commit_of(447) == (later.retained, "2026-10-22T06:05:07Z")
    assert later.first_commit_of(330) == (later.first_commit, "2026-10-22T05:29:48Z")


def test_each_receipt_decided_every_row_and_refused_every_control() -> None:
    for chosen in replay.RELEASES.values():
        receipt = _read(chosen.directory / replay.FILTERED)
        summary = receipt["summary"]
        assert summary["rows"] == summary["verified"] == chosen.decided
        assert summary["refused"] == []
        whole = sum(1 for row in replay.decided_claims(chosen) if not row.deleted)
        assert summary["controls"] == summary["controls_refused_by_both"] == 6 * whole
        assert receipt["source_commit"] == chosen.retained
        assert receipt["issue_pin"] == chosen.pin


def test_a_forged_receipt_row_is_refused() -> None:
    chosen = replay.release(672)
    row = replay.decided_claims(chosen)[0]
    kept = _read(chosen.directory / replay.FILTERED)["rows"][0]
    assert replay.row_problems(chosen, row, kept) == []
    accepted = copy.deepcopy(kept)
    accepted["controls"][5]["refused_by_independent"] = False
    assert replay.row_problems(chosen, row, accepted) == [
        f"#672 n={row.n}: near-contact-overlap was accepted"
    ]
    unverified = copy.deepcopy(kept)
    unverified["verified"] = False
    assert replay.row_problems(chosen, row, unverified) == [f"#672 n={row.n}: not verified"]
    moved = copy.deepcopy(kept)
    moved["printed"] = "18.692698795115"
    assert replay.row_problems(chosen, row, moved) == [
        f"#672 n={row.n}: receipt row differs from the issue"
    ]
    dropped = copy.deepcopy(kept)
    dropped["controls"] = dropped["controls"][:5]
    assert replay.row_problems(chosen, row, dropped) == [
        f"#672 n={row.n}: the controls are not the declared six"
    ]


def test_an_empty_or_disagreeing_all_pairs_sample_is_refused() -> None:
    chosen = replay.release(670)
    rows = replay.decided_claims(chosen)
    sample = _read(chosen.directory / replay.EXHAUSTIVE)["rows"]
    assert replay.sample_problems(chosen, rows, sample) == []
    assert replay.sample_problems(chosen, rows, []) == [
        "#670: the all-pairs sample decides [], not the declared [922]"
    ]
    disagreeing = copy.deepcopy(sample)
    disagreeing[0]["equals_filtered_least_gap"] = False
    assert replay.sample_problems(chosen, rows, disagreeing) == [
        "#670 n=922: the all-pairs sample disagrees with the filtered one"
    ]


def test_a_deletion_row_needs_its_certificate_read_whole() -> None:
    """#675's 992 and 995 delete from the 993 and 996 certificates, whose own rows carry
    the controls; without such a row the certificate would have none."""
    chosen = replay.release(675)
    rows = replay.decided_claims(chosen)
    assert replay.deletion_problems(chosen, rows) == []
    assert replay.deletion_problems(chosen, [row for row in rows if row.n != 993]) == [
        (
            "#675 n=992: deletes from n993, which no row of the release reads whole, so no "
            "control decides its certificate"
        )
    ]


def test_check_for_one_issue_reports_that_issue(capsys: pytest.CaptureFixture[str]) -> None:
    assert replay.main(["check", "--issue", "672"]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == (
        "OK: 44 rows of #672 verified, controls refused; "
        "the coverage plan and report order hold"
    )


def test_each_side_rounds_up_to_its_print_and_the_ledger_reads_the_same_side() -> None:
    sources = safe_load((LEDGER / "sources.yaml").read_text(encoding="utf-8"))
    transcribed = {
        (report["report"], claim["n"]): Fraction(claim["exact"])
        for report in sources["reports"]
        for claim in report["claims"]
        if "exact" in claim
    }
    for issue in BACKLOG:
        chosen = replay.release(issue)
        for row in _read(chosen.directory / replay.RECORD)["results"]:
            side = Fraction(row["exact_side"])
            printed = Fraction(row["offered_side"])
            assert printed - Fraction(1, 10**12) < side <= printed, (issue, row["n"])
            assert transcribed[f"#{issue}", row["n"]] == side, (issue, row["n"])


def test_the_ledger_records_every_row_and_the_plan_reads_its_dispositions() -> None:
    verdicts = _read(LEDGER / "ledger.json")
    ours = {f"#{issue}" for issue in BACKLOG}
    steps = [
        step
        for count in verdicts["counts"]
        for step in count["steps"]
        if step["report"] in ours and count["n"] > 324
    ]
    assert len(steps) == sum(replay.release(issue).decided for issue in BACKLOG)
    assert {step["verdict"] for step in steps} == {"recorded"}
    rows = [row for row in replay.planned_rows() if row["source_id"] != MISHAPOLK]
    current = {row["n"]: row["source_id"] for row in rows if "superseded_by" not in row}
    assert current == dict.fromkeys(CURRENT_670, "couzo-issue670-2026-10-17")
    found: dict[str, Counter[str]] = {}
    for row in rows:
        if "superseded_by" in row:
            found.setdefault(row["source_id"], Counter())[row["superseded_by"]] += 1
    assert {source: dict(counts) for source, counts in found.items()} == SUCCESSORS
    supersessions = [item for item in replay.planned_supersessions() if item[2] != MISHAPOLK]
    assert [(n, earlier, by) for n, earlier, by in supersessions if n in current] == [
        (n, earlier, "couzo-issue670-2026-10-17") for n, earlier in CURRENT_670.items()
    ]
    assert dict(Counter((earlier, by) for _, earlier, by in supersessions)) == FIRST_BEATEN


def test_each_walked_count_is_one_chain_in_report_order() -> None:
    """At 464 the 14 October row named #678 on ``main``; #666, reported first, beat it."""
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    assert replay.chain_problems(coverage) == []
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    rows[464, "couzo-verified-bounds-2026-10-14"]["superseded_by"] = "couzo-issue678-2026-10-18"
    assert replay.chain_problems(coverage) == [
        (
            "n=464 from couzo-verified-bounds-2026-10-14: superseded naming "
            "couzo-issue678-2026-10-18, not superseded by de-winter-issue666-2026-10-17"
        )
    ]
    del rows[464, "couzo-issue675-2026-10-18"]["superseded_by"]
    rows[464, "couzo-issue675-2026-10-18"]["disposition"] = "tracked-outside-case-corpus"
    assert replay.chain_problems(coverage)[1:] == [
        (
            "n=464 from couzo-issue675-2026-10-18: tracked-outside-case-corpus naming None, "
            "not superseded by couzo-issue678-2026-10-18"
        )
    ]


def test_a_right_successor_under_a_wrong_disposition_is_named_once() -> None:
    """#720's review B, B4: the message names the disposition, not the successor twice."""
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    rows[330, "couzo-issue670-2026-10-17"]["disposition"] = "tracked-outside-case-corpus"
    assert replay.chain_problems(coverage) == [
        (
            "n=330 from couzo-issue670-2026-10-17: tracked-outside-case-corpus naming "
            "couzo-issue672-2026-10-17, not superseded by couzo-issue672-2026-10-17"
        )
    ]


def test_the_coverage_register_reads_each_source_claims_record() -> None:
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    sources = {source["id"]: source for source in coverage["sources"]}
    for chosen in replay.RELEASES.values():
        source = sources[chosen.packet]
        record = replay.ROOT / source["claims_record"]
        assert record == chosen.directory / replay.RECORD
        claims = coverage_check.load_claims(record)
        rows = {
            row["n"]: row["value"]
            for row in coverage["beyond_horizon_claims"]
            if row["source_id"] == chosen.packet
        }
        assert rows == claims
        assert set(rows) <= set(source["scope"]["n_values"])


def _successor_at_631(
    successor: str,
    added: tuple[str, str] | None = None,
    *,
    kind: str = "upper-bound",
    **changed: str,
) -> tuple[list[str], list[str]]:
    """#719's row at 631 held superseded by ``successor``, with ``added`` (a value and a
    date) as that source's row claiming ``kind``, and what the plan and
    `check_source_coverage` say there."""
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    held = rows[631, MISHAPOLK]
    held.update(disposition="superseded", superseded_by=successor, **changed)
    claims = {
        source["id"]: coverage_check.load_claims(coverage_check.ROOT / source["claims_record"])
        for source in coverage["sources"]
        if source.get("claims_record")
    }
    if added is not None:
        value, dated = added
        mine = next(source for source in coverage["sources"] if source["id"] == MISHAPOLK)
        coverage["sources"].append(
            {**mine, "id": successor, "source_date": dated, "scope": {"n_values": [631]}}
        )
        coverage["beyond_horizon_claims"].append(
            {
                "n": 631,
                "source_id": successor,
                "claim": kind,
                "value": value,
                "assurance": "reported",
                "disposition": "tracked-outside-case-corpus",
                "bead": "think-xyhn",
            }
        )
        claims[successor] = {631: value}
    plan = [problem for problem in replay.coverage_problems(coverage) if "n=631 " in problem]
    gate = [
        error
        for error in coverage_check.beyond_horizon_errors(coverage, claims)[0]
        if "631" in error
    ]
    return plan, gate


def test_a_successor_outside_the_walk_holds_the_plan_only_with_a_later_smaller_row() -> None:
    """#720's review B, B1: a later import may supersede a row the plan calls current, as
    #719 supersedes #670's at 370, 452 and 536. #722's review A, A5: the plan accepts such
    a successor only where it holds a row at the count strictly below, dated no earlier,
    with the held row otherwise as planned, so it does not rest on the coverage gate; a
    same-day successor is not ordered by either. #722's review B: an equal row is not
    below (B2), and a smaller row of another claim is not the successor's (B3)."""
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    for n in (370, 452, 536):
        assert rows[n, "couzo-issue670-2026-10-17"]["superseded_by"] == MISHAPOLK
    assert replay.coverage_problems(coverage) == []
    refused = "n=631 from mishapolk-issue719-2026-10-22: the register's row is not the plan's"
    smaller, larger = "25.6568542495100000", "25.6568542496000000"
    equal = rows[631, MISHAPOLK]["value"]
    assert Fraction(smaller) < Fraction(equal) < Fraction(larger)
    later = _successor_at_631("x-later-2026-10-23", (smaller, "2026-10-23"))
    assert later == ([], [])
    same_day = _successor_at_631("x-same-2026-10-22", (smaller, "2026-10-22"))
    assert same_day == ([], [])
    for successor, added, kind in (
        ("couzo-issue715-2026-10-21", None, "upper-bound"),
        ("a-later-import-2026-10-23", None, "upper-bound"),
        ("x-early-2026-10-21", (smaller, "2026-10-21"), "upper-bound"),
        ("x-big-2026-10-23", (larger, "2026-10-23"), "upper-bound"),
        ("x-equal-2026-10-23", (equal, "2026-10-23"), "upper-bound"),
        ("x-lower-2026-10-23", (smaller, "2026-10-23"), "lower-bound"),
    ):
        plan, gate = _successor_at_631(successor, added, kind=kind)
        assert plan == [refused], successor
        assert gate, successor
    changed, _ = _successor_at_631(
        "x-later-2026-10-23", (smaller, "2026-10-23"), assurance="verified"
    )
    assert changed == [refused]


def test_a_source_the_walk_reaches_is_never_a_later_successor() -> None:
    """#722's review B, B2: at 631 #719's walk reaches Couzo's verified bounds of 14
    October. Dated a day after #719 and smaller there, that source's row would pass the
    row, date and strictness checks, so only the reach check refuses it as #719's
    successor: the walk already ordered the two."""
    reached = "couzo-verified-bounds-2026-10-14"
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    sources = {source["id"]: source for source in coverage["sources"]}
    assert rows[631, reached]["superseded_by"] == MISHAPOLK
    sources[reached]["source_date"] = "2026-10-23"
    rows[631, reached]["value"] = "25.6568542495100000"
    assert Fraction(rows[631, reached]["value"]) < Fraction(rows[631, MISHAPOLK]["value"])
    rows[631, MISHAPOLK].update(disposition="superseded", superseded_by=reached)
    refused = "n=631 from mishapolk-issue719-2026-10-22: the register's row is not the plan's"
    assert refused in replay.coverage_problems(coverage)


def test_a_commit_stating_two_sides_at_a_count_is_walked_at_its_least() -> None:
    """#722's review A, A2: 4e4c8ce states 450 twice and 5a299b4 six counts above 1024
    twice (`best/` and `parents/`); the ledger walks each commit's least side there, naming
    the other file, so 5a299b4 ties #715 above 1024 rather than lying above it. A4: 366 and
    447 are #719's from the 06:05:31Z edit that first claimed them."""
    sources = safe_load((replay.WALKS[replay.ISSUE_719].directory / "sources.yaml").read_text())
    reports = {report["report"]: report for report in sources["reports"]}
    for report in reports.values():
        counted = Counter(claim["n"] for claim in report["claims"])
        assert max(counted.values()) == 1, report["report"]
    couzo = reports["franciscouzo/square-packing@4e4c8ce"]
    at_450 = next(claim for claim in couzo["claims"] if claim["n"] == 450)
    assert at_450["printed"] == "21.767428349966"
    assert "the least of the 2 sides" in at_450["exact_from"]
    later = reports["franciscouzo/square-packing@5a299b4"]
    held_715 = {claim["n"]: claim["exact"] for claim in reports["#715"]["claims"]}
    for n in (1061, 1266, 1339, 1413, 1489, 1568):
        claim = next(claim for claim in later["claims"] if claim["n"] == n)
        assert claim["exact"] == held_715[n], n
    own = {claim["n"]: claim for claim in reports["#719"]["claims"]}
    assert {n for n, claim in own.items() if "reported_at" in claim} == {366, 447}
    assert own[447]["reported_at"] == "2026-10-22T06:05:31Z"


def test_719_reads_both_tables_and_holds_each_file_to_its_pinned_digest() -> None:
    chosen = replay.release(719)
    assert chosen.derived
    assert (
        chosen.rows,
        len(replay.decided_claims(chosen)),
        len(replay.held_claims(chosen)),
    ) == (
        122,
        112,
        8,
    )
    pinned = replay.manifest(chosen)
    for row in replay.claims(chosen):
        assert row.path == f"certificates/n-{row.n}.cert"
        assert row.path in pinned
        assert len(row.printed.partition(".")[2]) == 16
    body = json.loads((chosen.directory / replay.ISSUE).read_text(encoding="utf-8"))["body"]
    digest = pinned["certificates/n-330.cert"]
    with pytest.raises(replay.ReplayError, match="n=330: not the pinned digest"):
        chosen.read(body.replace(digest, "0" * 64), chosen)
    with pytest.raises(replay.ReplayError, match="links another commit"):
        chosen.read(body.replace(chosen.pin, "0" * 40), chosen)


def test_719_prints_the_binary64_side_and_its_rows_round_the_side_up_at_16_places() -> None:
    """76 of the issue's 16-place prints lie below the exact side, so the rows record the
    side rounded up at 16 places; at 631 that is what tells #719 from Couzo's 4e4c8ce and
    5a299b4 certificates, which round up to the same 12 places."""
    chosen = replay.release(719)
    record = {row["n"]: row for row in _read(chosen.directory / replay.RECORD)["results"]}
    below = 0
    for row in replay.decided_claims(chosen):
        if row.n not in record:
            continue
        side = Fraction(record[row.n]["exact_side"])
        assert replay.print_holds(chosen, side, row.printed)
        assert record[row.n]["issue_print"] == row.printed
        assert record[row.n]["offered_side"] == replay.ceiling(side, 16)
        below += Fraction(row.printed) < side
    assert below > 0
    assert not replay.print_holds(
        chosen, Fraction(record[330]["exact_side"]), "18.692672444455"
    )
    earlier = _read(chosen.directory / replay.EARLIER)
    (at_631,) = [row for row in earlier["rows"] if row["n"] == 631]
    ours = Fraction(record[631]["exact_side"])
    for item in at_631["publications"]:
        assert item["ceiling_12"] == replay.ceiling(ours)
        assert Fraction(item["side"]) > Fraction(record[631]["offered_side"]) > ours


def test_719_leaves_366_unrecorded_and_supersedes_the_row_at_each_other_count() -> None:
    """Couzo's 4e4c8ce certificate of 15 October is below #719's 366, so the walk does not
    record it: the receipt decides it, and no row or record entry holds it."""
    chosen = replay.release(719)
    assert replay.unrecorded_rows() == [(366, MISHAPOLK)]
    receipt = {row["n"]: row for row in _read(chosen.directory / replay.FILTERED)["rows"]}
    assert receipt[366]["verified"]
    assert 366 not in {row["n"] for row in _read(chosen.directory / replay.RECORD)["results"]}
    verdicts = _read(LEDGER_719 / "ledger.json")
    own = Counter(
        step["verdict"]
        for count in verdicts["counts"]
        for step in count["steps"]
        if step["report"] == "#719"
    )
    assert own == {"recorded": 121, "not recorded": 1}
    rows = [row for row in replay.planned_rows() if row["source_id"] == MISHAPOLK]
    assert len(rows) == 111
    assert {row["disposition"] for row in rows} == {"tracked-outside-case-corpus"}
    flips = [item for item in replay.planned_supersessions() if item[2] == MISHAPOLK]
    assert dict(Counter(earlier for _, earlier, _ in flips)) == SUPERSEDED_BY_719


def test_a_report_awaiting_its_own_import_is_passed_over_in_the_chain() -> None:
    """At 410 the walk records Couzo's 4e4c8ce certificate, then #719; 4e4c8ce has no row
    until think-yfoo lands, so main's row names #719, and a row naming 4e4c8ce's would not
    be the chain."""
    walk = replay.WALKS[replay.ISSUE_719]
    (count,) = [item for item in _read(walk.ledger)["counts"] if item["n"] == 410]
    assert [step["report"] for step in count["steps"] if step["verdict"] == "recorded"] == [
        "franciscouzo/square-packing@4e4c8ce",
        "#719",
    ]
    assert replay.recorded_reports(walk, count) == ["#719"]
    assert (
        410,
        "couzo-verified-bounds-2026-10-14",
        MISHAPOLK,
    ) in replay.planned_supersessions()
    held = walk.awaiting["#715"].counts
    assert held is not None
    assert 631 in held
    assert 417 not in held


def test_the_719_ledger_transcribes_the_packets_receipts() -> None:
    """sources.yaml is what `ledger_sources` writes from the earlier-publications receipt,
    the facts' claim record and the #666 and #715 packets."""
    sources = safe_load((LEDGER_719 / "sources.yaml").read_text(encoding="utf-8"))
    assert sources == replay.ledger_sources(
        719, sources["read_at_main"], str(sources["read_on"])
    )
    earlier = _read(replay.release(719).directory / replay.EARLIER)
    assert earlier["pushed_later"]["franciscouzo/square-packing"]["pushed"] == (
        "2026-10-21T22:56:37Z"
    )
    counts = {row["n"] for row in earlier["rows"] if row["publications"]}
    assert len(counts) == 60
    assert {n for n in counts if n > replay.LIMIT} == {
        1061,
        1128,
        1196,
        1266,
        1339,
        1413,
        1489,
        1568,
    }
