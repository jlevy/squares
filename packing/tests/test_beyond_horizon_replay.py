"""The beyond-horizon rows of issues #666, #670, #672, #675, #719 and #732, and of the
publications no issue reports, in report order.

`devtools.beyond_horizon_replay` decides the rows at or below 1024 of five reports from
their packets: Joost de Winter's #666 (11 of its 19 rows; the 8 above 1024 wait on the
owner), the rows beyond the corpus of Francisco Couzo's #670, #672 and #675, whose in-corpus
rows T-226 to T-228 register, and Mykhailo Polkovskyi's #719, whose packet keeps derived
facts and no upstream byte. These tests hold what is particular to the import:
each issue table's rows and the certificate each reads, the receipts and records against the
packets, the first commit of every certificate, each row's place in the backlog ledger's
report order and the coverage register's rows that follow from it, each walked count as
one chain in report order, and the forged receipts a check must refuse. Mykhailo
Polkovskyi's #732 has no table of rows: its packet declares the 77 its walk records, from
the history of his own repository, which the walk reads beside every watched publication.
Every test reads
the retained packets, the ledger and the source register only; none needs the network.
"""

from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import os
import subprocess
from collections import Counter
from fractions import Fraction
from pathlib import Path
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
#: Since the history walk, #719's other 49 rows follow Couzo's own, his 4e4c8ce index's at
#: 38 counts and his 5a299b4 reconciliation's at 11, which that walk plans.
SUPERSEDED_BY_719 = {
    "muglich-issue686-2026-10-19": 33,
    "couzo-issue715-2026-10-21": 16,
    "couzo-issue678-2026-10-18": 7,
    "couzo-issue670-2026-10-17": 3,
    "couzo-verified-bounds-2026-10-14": 2,
    "couzo-certificates-2026-10-14": 1,
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
        commits = _read(chosen.path(replay.FIRST_COMMITS))
        assert commits["retained_commit"] == chosen.retained
        for row in commits["rows"]:
            assert (row["first_commit"], row["committed"]) == chosen.first_commit_of(row["n"])
        record = _read(chosen.path(replay.RECORD))
        for row in record["results"]:
            assert row["first_committed"] == chosen.first_commit_of(row["n"])[1]
    later = replay.release(719)
    assert {row["n"] for row in _read(later.directory / replay.FIRST_COMMITS)["rows"]} >= {447}
    assert later.first_commit_of(447) == (later.retained, "2026-10-22T06:05:07Z")
    assert later.first_commit_of(330) == (later.first_commit, "2026-10-22T05:29:48Z")


def test_each_receipt_decided_every_row_and_refused_every_control() -> None:
    for chosen in replay.RELEASES.values():
        receipt = _read(chosen.path(replay.FILTERED))
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
    backlog = {replay.release(issue).source for issue in BACKLOG}
    rows = [row for row in replay.planned_rows() if row["source_id"] in backlog]
    current = {row["n"]: row["source_id"] for row in rows if "superseded_by" not in row}
    assert current == dict.fromkeys(CURRENT_670, "couzo-issue670-2026-10-17")
    found: dict[str, Counter[str]] = {}
    for row in rows:
        if "superseded_by" in row:
            found.setdefault(row["source_id"], Counter())[row["superseded_by"]] += 1
    assert {source: dict(counts) for source, counts in found.items()} == SUCCESSORS
    supersessions = [item for item in replay.planned_supersessions() if item[2] in backlog]
    assert [(n, earlier, by) for n, earlier, by in supersessions if n in current] == [
        (n, earlier, "couzo-issue670-2026-10-17") for n, earlier in CURRENT_670.items()
    ]
    assert dict(Counter((earlier, by) for _, earlier, by in supersessions)) == FIRST_BEATEN


def test_each_walked_count_is_one_chain_in_report_order() -> None:
    """At 464 Couzo's 4e4c8ce row, which the history walk records, is beaten first by #666,
    reported before #678; a row naming #678 there is out of report order for the history
    walk, and the backlog walk can no longer lead from the 14 October row to #666."""
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    assert replay.chain_problems(coverage) == []
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    rows[464, "couzo-index-2026-10-15"]["superseded_by"] = "couzo-issue678-2026-10-18"
    from_index = (
        "n=464 from couzo-index-2026-10-15: superseded naming "
        "couzo-issue678-2026-10-18, not superseded by de-winter-issue666-2026-10-17"
    )
    from_14_october = (
        "n=464 from couzo-verified-bounds-2026-10-14: superseded naming "
        "couzo-index-2026-10-15, not superseded by de-winter-issue666-2026-10-17"
    )
    assert replay.chain_problems(coverage) == [from_14_october, from_index]
    del rows[464, "couzo-issue675-2026-10-18"]["superseded_by"]
    rows[464, "couzo-issue675-2026-10-18"]["disposition"] = "tracked-outside-case-corpus"
    assert replay.chain_problems(coverage) == [
        from_14_october,
        (
            "n=464 from couzo-issue675-2026-10-18: tracked-outside-case-corpus naming None, "
            "not superseded by couzo-issue678-2026-10-18"
        ),
        from_index,
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
        source = sources[chosen.source]
        record = replay.ROOT / source["claims_record"]
        assert record == chosen.path(replay.RECORD)
        claims = coverage_check.load_claims(record)
        rows = {
            row["n"]: row["value"]
            for row in coverage["beyond_horizon_claims"]
            if row["source_id"] == chosen.source
        }
        assert rows == claims
        assert set(rows) <= set(source["scope"]["n_values"])


def _successor_at_682(
    successor: str,
    added: tuple[str, str] | None = None,
    *,
    kind: str = "upper-bound",
    **changed: str,
) -> tuple[list[str], list[str]]:
    """#719's row at 682 held superseded by ``successor``, with ``added`` (a value and a
    date) as that source's row claiming ``kind``, and what the plan and
    `check_source_coverage` say there."""
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    held = rows[682, MISHAPOLK]
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
            {**mine, "id": successor, "source_date": dated, "scope": {"n_values": [682]}}
        )
        coverage["beyond_horizon_claims"].append(
            {
                "n": 682,
                "source_id": successor,
                "claim": kind,
                "value": value,
                "assurance": "reported",
                "disposition": "tracked-outside-case-corpus",
                "bead": "think-xyhn",
            }
        )
        claims[successor] = {682: value}
    plan = [problem for problem in replay.coverage_problems(coverage) if "n=682 " in problem]
    gate = [
        error
        for error in coverage_check.beyond_horizon_errors(coverage, claims)[0]
        if "682" in error
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
    refused = "n=682 from mishapolk-issue719-2026-10-22: the register's row is not the plan's"
    smaller, larger = "26.6568542495000000", "26.6568542496000000"
    equal = rows[682, MISHAPOLK]["value"]
    assert Fraction(smaller) < Fraction(equal) < Fraction(larger)
    later = _successor_at_682("x-later-2026-10-23", (smaller, "2026-10-23"))
    assert later == ([], [])
    same_day = _successor_at_682("x-same-2026-10-22", (smaller, "2026-10-22"))
    assert same_day == ([], [])
    for successor, added, kind in (
        ("couzo-issue715-2026-10-21", None, "upper-bound"),
        ("a-later-import-2026-10-23", None, "upper-bound"),
        ("x-early-2026-10-21", (smaller, "2026-10-21"), "upper-bound"),
        ("x-big-2026-10-23", (larger, "2026-10-23"), "upper-bound"),
        ("x-equal-2026-10-23", (equal, "2026-10-23"), "upper-bound"),
        ("x-lower-2026-10-23", (smaller, "2026-10-23"), "lower-bound"),
    ):
        plan, gate = _successor_at_682(successor, added, kind=kind)
        assert plan == [refused], successor
        assert gate, successor
    changed, _ = _successor_at_682(
        "x-later-2026-10-23", (smaller, "2026-10-23"), assurance="verified"
    )
    assert changed == [refused]


def test_a_source_the_walk_reaches_is_never_a_later_successor() -> None:
    """#722's review B, B2: at 631 #719's walk reaches Couzo's verified bounds of 14
    October. Dated a day after #719 and smaller there, that source's row would pass the
    row, date and strictness checks, so only the reach check refuses it as #719's
    successor: the walk already ordered the two. Both walks record Couzo's 4e4c8ce
    index between them (#715's re-certification is held), so the 14 October row names
    the index's, which names #719's."""
    reached = "couzo-verified-bounds-2026-10-14"
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    sources = {source["id"]: source for source in coverage["sources"]}
    assert rows[631, reached]["superseded_by"] == "couzo-index-2026-10-15"
    assert rows[631, "couzo-index-2026-10-15"]["superseded_by"] == MISHAPOLK
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


def test_a_re_certification_held_for_a_decision_is_passed_over_in_the_chain() -> None:
    """At 631 the #719 walk records Couzo's 4e4c8ce certificate, #715's re-certification of
    it and #719. 4e4c8ce's row is the history walk's; #715's is held for a decision
    (think-fwa9), not awaiting an import, so the chain passes over it and 4e4c8ce's row
    names #719."""
    walk = replay.WALKS[replay.ISSUE_719]
    (count,) = [item for item in _read(walk.ledger)["counts"] if item["n"] == 631]
    assert [step["report"] for step in count["steps"] if step["verdict"] == "recorded"] == [
        "franciscouzo/square-packing@4e4c8ce",
        "#715",
        "#719",
    ]
    assert replay.recorded_reports(walk, count) == [
        "franciscouzo/square-packing@4e4c8ce",
        "#719",
    ]
    assert walk.later["franciscouzo/square-packing@4e4c8ce"] == "couzo-index-2026-10-15"
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    rows = {(row["n"], row["source_id"]): row for row in coverage["beyond_horizon_claims"]}
    assert rows[631, "couzo-index-2026-10-15"]["superseded_by"] == MISHAPOLK
    assert (631, "couzo-issue715-2026-10-21") not in rows
    assert walk.awaiting == {}
    held = walk.holds("#715", 631)
    assert held is not None
    assert (held.kind, held.bead) == (replay.SUB_PRINT, "think-fwa9")
    assert walk.holds("#715", 417) is None


#: The 19 counts at which the #719 walk records #715's held re-certifications, below 1024.
HELD_715_IN_719 = {535, 582, 591, 631, 633, 640, 682, 684, 691, 695}
HELD_715_IN_719 |= {735, 737, 742, 745, 790, 791, 797, 798, 799}


def test_the_719_walk_holds_715_s_re_certifications_and_names_what_rests_on_them() -> None:
    """Review A of #730, A6: #715's re-certifications wait on think-fwa9's decision, so the
    #719 walk holds them as the history walk does, and 5a299b4's verdicts at those 19 counts
    rest on them; left out, the walk records each again as a re-certification."""
    walk = replay.WALKS[replay.ISSUE_719]
    (held,) = walk.held["#715"]
    assert held.counts == HELD_715_IN_719
    assert held.counts <= replay.HISTORY_HELD["#715"][0].counts
    resting = {(item.report, item.kinds): item.counts for item in walk.resting}
    assert resting[("franciscouzo/square-packing@5a299b4", (replay.SUB_PRINT,))] == (
        HELD_715_IN_719
    )
    assert replay.resting_problems() == []
    flips = replay.refusal_flips(walk, (replay.SUB_PRINT,))
    assert {n for n, _, _ in flips} == HELD_715_IN_719
    assert {falls for _, _, falls in flips} == {replay.SUB_PRINT}


def test_a_single_hold_or_resting_verdict_is_counted_in_the_singular() -> None:
    """Review A of #730, A7: "at 1 count", not "at 1 counts"."""
    walk = replay.WALKS[replay.HISTORY]
    text = replay.held_sentence(walk, "evand/square-packing@41fc9ec")
    assert "verdicts at 1 count are decided" in text
    assert "1 counts" not in text
    sources = (HISTORY_LEDGER / "sources.yaml").read_text(encoding="utf-8")
    assert "at 1 counts" not in sources


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


def test_the_719_ledger_takes_its_commits_least_side_at_204() -> None:
    """#722's review A, A2, at #719's own commit: 1851c2c published both 204 files, the
    issue names certificates/n-204.cert (T-229), and the ledger keeps one claim of a report
    a count, the least side its commit states, certificates/n204.cert (T-231), which the
    author claimed on 22 October after T-229 was registered (think-h01y). Only 204 is
    transcribed so; 105, whose other file is above the named one, is not."""
    chosen = replay.release(719)
    assert set(chosen.same_commit_least or {}) == {204}
    sources = safe_load((LEDGER_719 / "sources.yaml").read_text(encoding="utf-8"))
    (own,) = (report for report in sources["reports"] if report["report"] == "#719")
    claims = {claim["n"]: claim for claim in own["claims"]}
    lower = Fraction(14808642830513087197802415708703, 10**30)
    named = Fraction(882663895519250432, 59604644775390625)
    assert Fraction(claims[204]["exact"]) == lower
    assert claims[204]["exact_from"].startswith("certificates/n204.cert at 12fc4667")
    assert (
        "beside certificates/n-204.cert, the file the issue names"
        in (claims[204]["exact_from"])
    )
    assert "T-231 registers the lower file" in own["note"]
    assert claims[105]["exact_from"].endswith(
        "certificates/n-105.cert at 12fc4667 (its header)"
    )
    ledger = _read(LEDGER_719 / "ledger.json")
    (count,) = (row for row in ledger["counts"] if row["n"] == 204)
    (step,) = count["steps"]
    assert (step["report"], step["verdict"], step["side"]) == (
        "#719",
        "recorded",
        "14.808642830514",
    )
    row = next(row for row in replay.claims(chosen) if row.n == 204)
    other = (chosen.same_commit_least or {})[204]
    with pytest.raises(replay.ReplayError, match="not below the file the issue names"):
        replay.same_commit_claim(chosen, row, lower, other)
    assert Fraction(replay.same_commit_claim(chosen, row, named, other)["exact"]) == lower


def _watched(**changed: Any) -> replay.Release:
    """A publication no issue reports, shaped like #670's release (`Release`)."""
    return dataclasses.replace(
        replay.release(670),
        issue=None,
        pin="23aff0c6f992271e1ad13a148d44f392c4b386c0",
        read=replay.read_declared_rows,
        **changed,
    )


def test_a_release_is_named_by_its_issue_or_by_its_publication() -> None:
    """An issue's release is ``#N``; a publication no issue reports is the ledger's label,
    ``owner/name@commit``, and its address is its tree at the commit."""
    assert replay.release(670) is replay.release("#670") is replay.release("670")
    with pytest.raises(replay.ReplayError, match="#1: no declared release"):
        replay.release(1)
    watched = _watched()
    assert watched.label == "franciscouzo/square-packing@23aff0c"
    assert watched.described == watched.label
    assert watched.issue_url == f"{replay.COUZO_URL}/tree/{watched.pin}"
    assert watched.report_key == "publication"
    assert replay.release(670).report_key == "issue"
    assert watched.reported == watched.committed
    assert _watched(published="2026-10-21T22:56:37Z").reported == "2026-10-21T22:56:37Z"
    with pytest.raises(replay.ReplayError, match="not a GitHub repository"):
        replay.repository_of("https://example.org/a/b")


def test_a_second_report_in_one_packet_has_its_own_source_record_and_receipts() -> None:
    """A packet may retain two reports of one commit, as Couzo's 23aff0c holds #670's
    certificates and others no issue claims: each has its own coverage source, claims
    record and receipts, and the first keeps the packet's defaults."""
    issue = replay.release(670)
    assert issue.source == issue.packet
    assert issue.path(replay.FILTERED) == issue.directory / replay.FILTERED
    assert issue.path(replay.RECORD) == issue.directory / replay.RECORD
    second = _watched(
        source_id="couzo-23aff0c-2026-10-17",
        record=Path("acquisition/beyond-horizon-rows-23aff0c.json"),
        receipts=Path("receipts/23aff0c"),
    )
    assert second.source == "couzo-23aff0c-2026-10-17"
    assert second.path(replay.FILTERED) == (
        second.directory / "receipts/23aff0c/filtered-exact-replay.json"
    )
    assert second.path(replay.RECORD) == (
        second.directory / "acquisition/beyond-horizon-rows-23aff0c.json"
    )
    assert second.path(replay.ISSUE) == second.directory / replay.ISSUE


def test_a_publication_reads_the_rows_its_packet_declares() -> None:
    """The declaration names the publication's commit, address and walk, and each row's
    count, certificate and print; one that names another commit or walk is refused."""
    watched = _watched()
    declared = {
        "format": replay.WATCHED_FORMAT,
        "publication": watched.issue_url,
        "commit": watched.pin,
        "walk": watched.walk,
        "rows": [{"n": 547, "certificate": "certificates/best/n547.cert", "printed": "23.9"}],
    }
    (row,) = watched.read(json.dumps(declared), watched)
    assert (row.n, row.path, row.printed, row.certificate_n, row.deleted) == (
        547,
        "certificates/best/n547.cert",
        "23.9",
        547,
        0,
    )
    for key, value in (("commit", "0" * 40), ("walk", "elsewhere"), ("format", "v0")):
        with pytest.raises(replay.ReplayError):
            watched.read(json.dumps(declared | {key: value}), watched)


def _holding(monkeypatch: pytest.MonkeyPatch, **held: tuple[replay.Held, ...]) -> replay.Walk:
    """#719's walk with Couzo's 5a299b4 held where ``held`` says, in place of awaiting its
    import, as the only walk the checks read."""
    walk = replay.WALKS[replay.ISSUE_719]
    awaiting = {
        report: item
        for report, item in walk.awaiting.items()
        if report != "franciscouzo/square-packing@5a299b4"
    }
    changed = dataclasses.replace(walk, awaiting=awaiting, held=held)
    monkeypatch.setattr(replay, "WALKS", {replay.ISSUE_719: changed})
    return changed


def test_a_held_publication_is_passed_over_and_held_to_the_walk(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """At 366 and 372 the walk records Couzo's 5a299b4 below 4e4c8ce by 2e-23, the same
    12-place print: held for the owner's answer (think-fwa9), it has no row, so the chain
    passes over it, and the hold names a class, a decision's bead and a publication the
    walk records there."""
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    label = "franciscouzo/square-packing@5a299b4"
    walk = _holding(
        monkeypatch,
        **{label: (replay.Held(replay.SUB_PRINT, "think-fwa9", frozenset({366, 372})),)},
    )
    assert replay.held_problems(coverage) == []
    assert walk.holds(label, 372) is not None
    counts = {count["n"]: count for count in _read(walk.ledger)["counts"]}
    assert label not in replay.recorded_reports(walk, counts[372])
    assert label in replay.recorded_reports(walk, counts[409])
    assert replay.held_plan() == [
        {
            "walk": replay.ISSUE_719,
            "report": label,
            "n": n,
            "class": "sub-print",
            "bead": "think-fwa9",
        }
        for n in (366, 372)
    ]
    _holding(
        monkeypatch, **{label: (replay.Held(replay.SUB_PRINT, "think-fwa9", frozenset({371})),)}
    )
    assert replay.held_problems(coverage) == [
        f"{replay.ISSUE_719}: {label} n=371: the walk does not record it, so it holds nothing"
    ]
    _holding(
        monkeypatch,
        **{
            label: (
                replay.Held("rounding", "fwa9", frozenset({366})),
                replay.Held(replay.SUB_PRINT, "think-fwa9", frozenset({366})),
            )
        },
    )
    assert replay.held_problems(coverage) == [
        f"{replay.ISSUE_719}: {label}: no such class of hold, 'rounding'",
        f"{replay.ISSUE_719}: {label}: 'fwa9' is not a decision's bead",
        f"{replay.ISSUE_719}: {label}: holds n=[366] twice",
    ]


def test_a_hold_on_a_count_a_row_holds_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    """#719's own row at 372 is a declared row with a register row: it cannot be held."""
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    _holding(
        monkeypatch,
        **{"#719": (replay.Held(replay.SUB_PRINT, "think-fwa9", frozenset({372})),)},
    )
    assert replay.held_problems(coverage) == [
        (
            f"{replay.ISSUE_719}: #719 n=372: held for think-fwa9, yet "
            "mishapolk-issue719-2026-10-22 has a row there"
        ),
        f"{replay.ISSUE_719}: #719 n=372: held and declared as a row",
    ]


def _commit(repo: Path, when: str, files: dict[str, str | None]) -> None:
    """Commit ``files`` at ``when``: each path with its text, or removed where it is None."""
    for name, text in files.items():
        if text is None:
            (repo / name).unlink()
            continue
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text, encoding="utf-8")
    env = {"GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when, "PATH": os.environ["PATH"]}
    for args in (["add", "-A"], ["commit", "-q", "-m", when]):
        subprocess.run(["git", "-C", str(repo), *args], check=True, env=env)


def _repository(path: Path, commits: list[tuple[str, dict[str, str | None]]]) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    for key, value in (("user.name", "t"), ("user.email", "t@t"), ("commit.gpgsign", "false")):
        subprocess.run(["git", "-C", str(path), "config", key, value], check=True)
    for when, files in commits:
        _commit(path, when, files)
    return path


def test_the_history_scan_keeps_each_side_at_its_first_publication(tmp_path: Path) -> None:
    """Every certificate header, index bound and table row at 325 to 1024 is a publication
    from the first commit of any watched repository that stated it, below the frozen start;
    a copy in a later commit or another repository is none."""
    index = {
        "entries": {
            "400": {"verified": {"bound": "39/2"}},
            "401": {"verified": {"bound": "19.9"}},
        }
    }
    evand = _repository(
        tmp_path / "evand",
        [
            (
                "2026-10-10T00:00:00Z",
                {
                    "certificates/n400.cert": "400 39/2\n",
                    "upper_bounds.json": json.dumps(index),
                },
            ),
            (
                "2026-10-11T00:00:00Z",
                {
                    "certificates/best/n400.cert": "400 39/2\n",
                    "certificates/n402.cert": "# a comment\n402 20\n",
                    "composites/table.csv": (
                        "count,side_rounded_up_15,id\n403,20.123456789012345,x\n"
                    ),
                },
            ),
        ],
    )
    fang = _repository(
        tmp_path / "fang", [("2026-10-09T00:00:00Z", {"n0400/n0400.cert": "400 39/2\n"})]
    )
    found = replay.first_publications("evand/square-packing", evand)
    assert [(item["n"], item["side"], item["kind"], item["path"]) for item in found] == [
        (400, "39/2", "certificate", "certificates/n400.cert"),
        (401, "199/10", "index", "upper_bounds.json"),
        (402, "20", "certificate", "certificates/n402.cert"),
        (403, "4024691357802469/200000000000000", "table", "composites/table.csv:x"),
    ]
    start = tmp_path / "source-coverage.yaml"
    start.write_text(
        "beyond_horizon_claims:\n- n: 401\n  source_id: s\n  value: '19.5'\n"
        "  disposition: tracked-outside-case-corpus\n",
        encoding="utf-8",
    )
    scan = replay.history_publications(
        {"evand/square-packing": evand, "TheSnakeFang/squarepack-certs": fang}, start
    )
    assert [(item["n"], item["repository"]) for item in scan["publications"]] == [
        (400, "TheSnakeFang/squarepack-certs"),
        (402, "evand/square-packing"),
        (403, "evand/square-packing"),
    ]
    assert scan["read_at_main"] == replay.HISTORY_READ_AT_MAIN


def test_the_history_starts_are_frozen_from_the_register_named(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The starts come from the coverage register of a checkout of the frozen ``main``,
    read by its path: its current row at a count, else the grid."""
    monkeypatch.setattr(replay, "INTAKE", tmp_path)
    start = tmp_path / "source-coverage.yaml"
    start.write_text(
        "beyond_horizon_claims:\n- n: 401\n  source_id: s\n  value: '19.5'\n"
        "  disposition: tracked-outside-case-corpus\n",
        encoding="utf-8",
    )
    assert replay.write_history_starts(start, [400, 401]) == 2
    starts = safe_load((tmp_path / replay.HISTORY / "starts.yaml").read_text(encoding="utf-8"))
    assert starts["read_at_main"] == replay.HISTORY_READ_AT_MAIN
    labels = {count["n"]: count["members"][0]["label"] for count in starts["counts"]}
    assert labels == {400: "the grid", 401: "beyond-horizon row s"}
    assert replay.history_label("couzo-issue670-2026-10-17") == "#670"
    assert (
        replay.history_label("couzo-verified-bounds-2026-10-14")
        == "couzo-verified-bounds-2026-10-14"
    )


def test_an_earlier_walk_s_pair_may_be_bridged_by_a_report_a_later_walk_orders(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A walk whose starts were frozen later may lack an earlier publication another walk
    inserts between two of its reports; the register may lead through it only where the
    first walk does not reach it and another walk does."""
    first = replay.Walk("first", later={}, awaiting={})
    other = replay.Walk("other", later={}, awaiting={})
    reached = {"first": {"a", "c"}, "other": {"a", "b", "c"}}
    monkeypatch.setattr(replay, "WALKS", {"first": first, "other": other})
    monkeypatch.setattr(replay, "_reached", lambda walk, _n: reached[walk.name])
    rows = {
        (500, "a"): {"disposition": "superseded", "superseded_by": "b"},
        (500, "b"): {"disposition": "superseded", "superseded_by": "c"},
    }
    assert replay.bridged(rows, 500, "a", "c", first)
    assert not replay.bridged(rows, 500, "a", "b", first)
    reached["other"] = {"a", "c"}
    assert not replay.bridged(rows, 500, "a", "c", first)
    reached["other"] = {"a", "b", "c"}
    reached["first"] = {"a", "b", "c"}
    assert not replay.bridged(rows, 500, "a", "c", first)


HISTORY_LEDGER = replay.ROOT / f"campaign/issue-intake/{replay.HISTORY}"
#: Each publication the history walk records as rows: its rows, and how many are current.
HISTORY_ROWS = {
    "franciscouzo/square-packing@02f9690": (12, 6),
    "evand/square-packing@f7a2325": (1, 0),
    "franciscouzo/square-packing@3ef7634": (2, 0),
    "franciscouzo/square-packing@f311f08": (4, 1),
    "franciscouzo/square-packing@a7067d7": (1, 0),
    "TheSnakeFang/squarepack-certs@bef5c42": (2, 0),
    "franciscouzo/square-packing@93570ef": (2, 0),
    "franciscouzo/square-packing@4596670": (1, 0),
    "franciscouzo/square-packing@4e4c8ce": (253, 91),
    "franciscouzo/square-packing@23aff0c": (21, 0),
    "franciscouzo/square-packing@5a299b4": (20, 9),
}
#: What the history walk holds back, by class: (publications, decision's bead).
HISTORY_HOLDS = {
    "goebel": (148, "think-8krd"),
    "sub-print": (74, "think-fwa9"),
    "consequence": (54, "think-f2io"),
    "recipe": (64, "think-f2io"),
}


def test_the_history_walk_records_each_publication_s_rows() -> None:
    """319 rows of 11 publications no issue reports: 107 current, 212 superseded on entry,
    each certificate first committed at its publication's commit and below Göbel."""
    found = {}
    rows = [row for row in replay.planned_rows() if row["bead"]]
    for label, chosen in replay.RELEASES.items():
        if chosen.walk != replay.HISTORY:
            continue
        assert chosen.issue is None
        mine = [row for row in rows if row["source_id"] == chosen.source]
        current = sum(1 for row in mine if "superseded_by" not in row)
        found[label] = (len(mine), current)
        assert len(replay.decided_claims(chosen)) == chosen.decided == len(mine)
    assert found == HISTORY_ROWS
    assert sum(rows for rows, _ in found.values()) == 319
    assert sum(current for _, current in found.values()) == 107


def test_each_publication_declares_the_rows_its_walk_records() -> None:
    """The packet's declaration is what `declared_rows` writes from the ledger and the
    scan; dropping a row or declaring one the walk holds is refused."""
    assert replay.declaration_problems() == []
    for chosen in replay.RELEASES.values():
        if replay.declares_rows(chosen):
            assert replay.declared_rows(chosen) == _read(chosen.directory / chosen.declared)


def test_the_history_walk_holds_back_what_waits_on_a_decision() -> None:
    """Göbel-above, sub-print, deletion-bound and recipe publications have no row; each is
    held with its decision's bead, and the plan lists every hold."""
    held = [item for item in replay.held_plan() if item["walk"] == replay.HISTORY]
    by_class = Counter(item["class"] for item in held)
    beads = {item["class"]: item["bead"] for item in held}
    assert {kind: (by_class[kind], beads[kind]) for kind in by_class} == HISTORY_HOLDS
    assert sum(by_class.values()) == 340
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    assert replay.held_problems(coverage) == []


#: 23aff0c's held constructions and deletions from them, all classical (#722's review of
#: #730, A1): they wait on #613 (think-8krd) as well as on D2 and D6 (think-f2io).
CLASSICAL_23AFF0C = {"consequence": 15, "recipe": 46}
#: The steps a rerun history walk would record if an answer left a class of hold out
#: (review A of #730, A2): new records at deletion bounds and recipes, and at Göbel and
#: sub-print holds only publications the same decision holds again.
LEFT_OUT = {
    "consequence": {"record": 9},
    "recipe": {"record": 47},
    "goebel": {"goebel": 66},
    "sub-print": {"sub-print": 8},
}


def test_23aff0c_s_classical_holds_wait_on_613_too() -> None:
    """Its 15 deletion bounds and 46 constructions are Göbel's and Friedman's, so each hold
    names think-8krd beside think-f2io, says what it is, and the class says it too."""
    held = replay.HISTORY_HELD["franciscouzo/square-packing@23aff0c"]
    classical = {item.kind: item for item in held if item.also}
    assert {kind: len(item.counts) for kind, item in classical.items()} == CLASSICAL_23AFF0C
    assert all(
        item.bead == "think-f2io" and item.also == ("think-8krd",) for item in held if item.also
    )
    assert "Friedman" in classical["consequence"].note
    assert "Göbel's squares" in classical["recipe"].note
    assert "classical construction" in replay.HELD_CLASSES[replay.RECIPE]
    assert "construction the index states" in replay.HELD_CLASSES[replay.CONSEQUENCE]
    plan = [
        item
        for item in replay.held_plan()
        if item["walk"] == replay.HISTORY and item["report"].endswith("@23aff0c")
    ]
    assert sum(1 for item in plan if item.get("also") == ["think-8krd"]) == 61


def test_a_hold_s_further_decision_is_a_bead(monkeypatch: pytest.MonkeyPatch) -> None:
    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    label = "franciscouzo/square-packing@5a299b4"
    _holding(
        monkeypatch,
        **{
            label: (
                replay.Held(replay.SUB_PRINT, "think-fwa9", frozenset({366, 372}), ("613",)),
            )
        },
    )
    assert replay.held_problems(coverage) == [
        f"{replay.ISSUE_719}: {label}: '613' is not a decision's bead"
    ]


def test_each_verdict_resting_on_a_hold_is_declared(monkeypatch: pytest.MonkeyPatch) -> None:
    """131 history verdicts and 2 of #719's are decided only against held publications;
    each is declared (`Resting`), and one the ledger rests or does not rest is named."""
    assert replay.resting_problems() == []
    history = replay.WALKS[replay.HISTORY]
    assert sum(len(item.counts) for item in history.resting) == 131
    assert replay.resting_on_holds(history) == history.resting
    first, *rest = history.resting
    dropped = dataclasses.replace(
        history,
        resting=(
            dataclasses.replace(first, counts=first.counts - {757}),
            dataclasses.replace(rest[0], counts=rest[0].counts | {376}),
            *rest[1:],
        ),
    )
    monkeypatch.setattr(replay, "WALKS", {replay.HISTORY: dropped})
    assert replay.resting_problems() == [
        (
            f"{replay.HISTORY}: {first.report} not recorded on recipe holds: rests at "
            "n=[757], undeclared"
        ),
        (
            f"{replay.HISTORY}: {rest[0].report} not recorded on goebel holds: declared at "
            "n=[376], not in the ledger"
        ),
    ]


def test_an_answer_leaving_a_hold_out_reopens_the_verdicts_resting_on_it() -> None:
    """Run again without each class of hold, the history walk records 9 of 5a299b4's
    certificates at the deletion bounds' counts and 47 publications at the recipes', each
    a new record with no row and no hold; at Göbel and sub-print holds every step it would
    record is held again by the same decision. Each step it would record rests on that
    class alone; a verdict also resting on another standing hold stays."""
    history = replay.WALKS[replay.HISTORY]
    found = {}
    for kind in LEFT_OUT:
        flips = replay.refusal_flips(history, (kind,))
        found[kind] = dict(Counter(falls for _, _, falls in flips))
        resting = {
            (n, item.report)
            for item in history.resting
            if item.kinds == (kind,)
            for n in item.counts
        }
        assert {(n, report) for n, report, _ in flips} <= resting
    assert found == LEFT_OUT
    deletions = replay.refusal_flips(history, (replay.CONSEQUENCE,))
    assert [n for n, _, _ in deletions] == [406, 447, 588, 589, 638, 906, 907, 967, 968]
    assert {report for _, report, _ in deletions} == {"franciscouzo/square-packing@5a299b4"}


def test_the_history_ledger_transcribes_the_scan_and_the_register() -> None:
    """sources.yaml is what `history_sources` writes from the scan and the register; the
    starts are frozen at a97b712b9, where the 8 October rows or the grid stood."""
    sources = safe_load((HISTORY_LEDGER / "sources.yaml").read_text(encoding="utf-8"))
    assert sources == replay.history_sources(str(sources["read_on"]))
    starts = safe_load((HISTORY_LEDGER / "starts.yaml").read_text(encoding="utf-8"))
    assert starts["read_at_main"] == replay.HISTORY_READ_AT_MAIN
    labels = {member["label"] for count in starts["counts"] for member in count["members"]}
    assert labels == {"the grid"} | {
        f"beyond-horizon row {source}" for source in replay.HISTORY_START_SOURCES
    }


ISSUE_732 = replay.ROOT / "campaign/issue-intake/upper-bounds-issue732-20261023"
#: The SHA-256 issue #732 states for the manifest that indexes its certificates.
MANIFEST_732 = "5dff6ae3b8b4b5adbb44dd64cb907361a7fe5f323500b472007375f11ace47d5"
#: The first commit that published each side the source holds at 325 to 1024 at the pin.
FIRST_PUBLISHED_732 = {"8a488a1": 246, "1851c2c": 82, "3285fac": 61, "12fc466": 1}
#: The rows #732 supersedes on entry, by the source that held each count.
SUPERSEDED_BY_732 = {
    "couzo-issue715-2026-10-21": 30,
    "mishapolk-issue719-2026-10-22": 29,
    "couzo-index-2026-10-15": 14,
    "couzo-verified-bounds-2026-10-14": 4,
}
#: #732's verdicts that rest on held publications, by the class of hold.
RESTING_732 = {"consequence": 14, "goebel": 43, "recipe": 41, "sub-print": 31}


def test_a_count_named_outside_the_band_is_never_read() -> None:
    """The source-history scan reads only certificate files whose paths name a count from
    325 to 1024, under every layout of certificate files the source has used, so a blobless
    clone fetches nothing above. Decimal poses and indexes name no count to it."""
    named = {
        "certificates/0000-0999/n372.cert": 372,
        "certificates/n-411.cert": 411,
        "certificates/n-133_breakthrough.cert": 133,
        "certificates/square-27.cert": 27,
        "certificates/1000-1999/n1061.cert": 1061,
        "README.md": None,
        "certificates/manifest.json": None,
        "certificates/square-343.txt": None,
        "upper_bounds.json": None,
    }
    assert {path: replay.named_count(path) for path in named} == named
    assert 1061 not in replay.HISTORY_COUNTS
    assert 133 not in replay.HISTORY_COUNTS


def test_the_732_source_history_holds_each_certificate_to_the_manifest() -> None:
    """At 17cc220 the source holds 390 certificates beyond the corpus at or below 1024, each
    the file, digest and exact bound its manifest states; the manifest has the SHA-256 the
    issue states and the packet pins, and each side's first publication is dated."""
    chosen = replay.release(732)
    history = _read(chosen.path(replay.SOURCE_HISTORY))
    rows = history["at_commit"]
    assert history["retained_commit"] == chosen.retained
    assert len(rows) == 390
    assert all(325 <= row["n"] <= replay.LIMIT for row in rows)
    assert history["manifest_sha256"] == MANIFEST_732
    assert replay.manifest(chosen)[replay.SOURCE_MANIFEST] == MANIFEST_732
    pinned = replay.manifest(chosen)
    assert all(pinned[row["certificate"]] == row["sha256"] for row in rows)
    found = Counter(row["side_first_commit"][:7] for row in rows)
    assert found == FIRST_PUBLISHED_732
    sides = {(item["n"], item["side"]) for item in history["publications"]}
    assert all((row["n"], row["side"]) in sides for row in rows)


#: A certificate the #732 source-history fixture moves, a lower side it publishes later,
#: and files outside the band whose headers would be refused if they were read.
SOURCE_400 = "# N=400, src=cert_n-399, layers=1, del=0\n400 39/2\n0 0 0\n"
SOURCE_401 = ("401 20\n", "401 199/10\n")
OUTSIDE_BAND = {
    "certificates/n-133_tight.cert": "not a certificate\n",
    "certificates/1000-1999/n1061.cert": "not a certificate\n",
    "certificates/square-400.txt": "decimal poses, not a certificate\n",
}


def _source_history(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    witnesses: Any = None,
    early: dict[str, str | None] | None = None,
) -> tuple[dict[str, Any], list[str], dict[str, str]]:
    """`source_history` over a three-commit source: an ``n-N.cert`` at 400 (with a tight
    copy) and 401; the 400 blob moved to ``0000-0999/nN.cert`` beside a lower 401; then
    files outside the band and the manifest. ``witnesses`` edits the manifest's entries and
    ``early`` adds files to the first commit. Returns the receipt, the three commits and
    the blob of each path at the last."""
    moved = "certificates/0000-0999/n400.cert"
    lower = "certificates/0000-0999/n401.cert"
    stated = {
        "400": {
            "certificate": moved,
            "certificate_sha256": hashlib.sha256(SOURCE_400.encode()).hexdigest(),
            "bound": "19.5",
        },
        "401": {
            "certificate": lower,
            "certificate_sha256": hashlib.sha256(SOURCE_401[1].encode()).hexdigest(),
            "bound": "199/10",
        },
        "1061": {"certificate": "certificates/1000-1999/n1061.cert", "bound": "33"},
    }
    if witnesses is not None:
        witnesses(stated)
    first: dict[str, str | None] = {
        "certificates/n-400.cert": SOURCE_400,
        "certificates/n-400_tight.cert": SOURCE_400,
        "certificates/n-401.cert": SOURCE_401[0],
        **(early or {}),
    }
    tmp_path.mkdir(parents=True, exist_ok=True)
    repo = _repository(
        tmp_path / "source",
        [
            ("2026-10-10T00:00:00Z", first),
            (
                "2026-10-11T00:00:00Z",
                {
                    "certificates/n-400.cert": None,
                    "certificates/n-400_tight.cert": None,
                    "certificates/n-401.cert": None,
                    moved: SOURCE_400,
                    lower: SOURCE_401[1],
                },
            ),
            (
                "2026-10-12T00:00:00Z",
                {
                    **OUTSIDE_BAND,
                    replay.SOURCE_MANIFEST: json.dumps({"witnesses": stated}),
                },
            ),
        ],
    )

    def git(*args: str) -> str:
        found = subprocess.run(
            ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
        )
        return found.stdout.strip()

    commits = git("rev-list", "--reverse", "HEAD").split()
    blobs = {path: git("rev-parse", f"HEAD:{path}") for path in (moved, lower)}
    chosen = dataclasses.replace(replay.release(732), retained=commits[-1])
    monkeypatch.setitem(replay.RELEASES, "#732", chosen)
    return replay.source_history(732, repo), commits, blobs


def test_the_source_history_dates_each_side_by_its_first_commit_across_renames(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`source_history` reads only certificate paths naming a count from 325 to 1024: the
    files outside the band, whose headers it would refuse, are never opened, and decimal
    poses are not certificates. A side is first published by the first commit,
    in topological order and then by path, that holds it under any name, so a moved file
    keeps its first commit, and each side a count ever had is a publication. At the last
    commit each count's file is held to the manifest (#742's review A, A2)."""
    history, (first, second, last), blobs = _source_history(tmp_path, monkeypatch)
    moved, lower = "certificates/0000-0999/n400.cert", "certificates/0000-0999/n401.cert"
    assert (history["retained_commit"], history["history_commits"]) == (last, 3)
    assert history["counts"] == [325, 1024]
    assert history["at_commit"] == [
        {
            "n": 400,
            "certificate": moved,
            "blob": blobs[moved],
            "sha256": hashlib.sha256(SOURCE_400.encode()).hexdigest(),
            "side": "39/2",
            "ceiling_12": "19.500000000000",
            "side_first_commit": first,
            "side_first_published": "2026-10-10T00:00:00Z",
            "side_first_path": "certificates/n-400.cert",
            "blob_first_commit": first,
            "blob_first_published": "2026-10-10T00:00:00Z",
        },
        {
            "n": 401,
            "certificate": lower,
            "blob": blobs[lower],
            "sha256": hashlib.sha256(SOURCE_401[1].encode()).hexdigest(),
            "side": "199/10",
            "ceiling_12": "19.900000000000",
            "side_first_commit": second,
            "side_first_published": "2026-10-11T00:00:00Z",
            "side_first_path": lower,
            "blob_first_commit": second,
            "blob_first_published": "2026-10-11T00:00:00Z",
        },
    ]
    assert [
        (item["n"], item["side"], item["commit"], item["path"])
        for item in history["publications"]
    ] == [
        (400, "39/2", first, "certificates/n-400.cert"),
        (401, "20", first, "certificates/n-401.cert"),
        (401, "199/10", second, lower),
    ]
    assert {item["path"] for item in history["publications"]}.isdisjoint(OUTSIDE_BAND)


def test_the_source_history_refuses_a_header_or_a_manifest_that_disagrees(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A file in the band whose header states another count is refused, in any commit of
    the history, as is a manifest whose path, digest or exact bound for a count is not the
    file's, or which states another set of counts in the band than the commit holds."""
    with pytest.raises(replay.ReplayError, match=r"n-402\.cert .*header does not state"):
        _source_history(
            tmp_path / "header", monkeypatch, early={"certificates/n-402.cert": "403 20\n"}
        )
    edits = {
        "path": lambda stated: stated["400"].update(certificate="certificates/n-400.cert"),
        "digest": lambda stated: stated["400"].update(certificate_sha256="0" * 64),
        "bound": lambda stated: stated["400"].update(bound="39/2" + "1"),
        "absent": lambda stated: stated.pop("400"),
    }
    for name, edit in edits.items():
        with pytest.raises(replay.ReplayError, match=r"n=400: .* is not the certificate"):
            _source_history(tmp_path / name, monkeypatch, edit)
    with pytest.raises(replay.ReplayError, match="states other counts at or below 1024"):
        _source_history(
            tmp_path / "extra",
            monkeypatch,
            lambda stated: stated.update({"402": dict(stated["401"])}),
        )
    with pytest.raises(replay.ReplayError, match="n=400: the commit holds 2 files"):
        _source_history(
            tmp_path / "two",
            monkeypatch,
            early={"certificates/0000-0999/n400_tight.cert": SOURCE_400},
        )


def test_the_replay_reads_a_row_s_exact_side_as_the_ledger_s_starts_do(
    tmp_path: Path,
) -> None:
    """One reader for both (`devtools.intake_ledger.stated_exact_side`): at every current
    beyond-horizon row the replay's side is the ledger's exact side, or its print where the
    source states none, and an unclear record is refused as a `ReplayError` (#742's review
    A, A3)."""
    from devtools import intake_ledger  # noqa: PLC0415

    coverage = safe_load(replay.COVERAGE.read_text(encoding="utf-8"))
    sources = {source["id"]: source for source in coverage["sources"]}
    rows = {
        row["n"]: row
        for row in coverage["beyond_horizon_claims"]
        if "superseded_by" not in row and row["n"] in replay.HISTORY_COUNTS
    }
    exact = intake_ledger.beyond_exact_sides(coverage, rows)
    assert len(exact) > 300
    for n, row in rows.items():
        side = replay.row_side(sources[row["source_id"]], n, str(row["value"]))
        assert side == exact.get(n, Fraction(str(row["value"]))), n
    absent = {"id": "absent", "claims_record": str(tmp_path / "absent.json")}
    with pytest.raises(replay.ReplayError, match="does not exist"):
        replay.row_side(absent, 400, "20")
    printed_only = tmp_path / "sources.json"
    printed_only.write_text(json.dumps({"sources": []}), encoding="utf-8")
    printed = {"id": "printed", "claims_record": str(printed_only)}
    assert replay.row_side(printed, 400, "19.99") == Fraction("19.99")
    with pytest.raises(replay.ReplayError, match="states no one exact side"):
        replay.exact_row_side(printed, 400)


def test_732_declares_the_77_rows_its_walk_records_and_holds_499() -> None:
    """The issue has no table: the packet declares the rows the walk records and does not
    hold, each the certificate the source holds at the pin, printed rounded up at 12 places.
    499, 8.66e-13 below #719's row at the same print, is recorded and held (think-fwa9)."""
    chosen = replay.release(732)
    assert replay.declares_rows(chosen)
    assert chosen.issue == 732
    rows = replay.decided_claims(chosen)
    assert len(rows) == len(replay.claims(chosen)) == chosen.decided == 77
    walk = replay.WALKS[replay.ISSUE_732]
    ledger = _read(ISSUE_732 / "ledger.json")
    recorded = {
        count["n"]
        for count in ledger["counts"]
        for step in count["steps"]
        if step["report"] == "#732" and step["verdict"] == replay.RECORDED
    }
    assert recorded == {row.n for row in rows} | {499}
    held = walk.holds("#732", 499)
    assert held is not None
    assert (held.kind, held.bead) == (replay.SUB_PRINT, "think-fwa9")
    history = {row["n"]: row for row in _read(chosen.path(replay.SOURCE_HISTORY))["at_commit"]}
    for row in rows:
        assert row.path == history[row.n]["certificate"]
        assert row.printed == history[row.n]["ceiling_12"]
    first = Counter(history[row.n]["side_first_commit"][:7] for row in rows)
    assert first == {"8a488a1": 76, "1851c2c": 1}
    assert history[539]["side_first_commit"].startswith("1851c2c")


def test_732_s_rows_are_current_and_supersede_the_rows_they_beat() -> None:
    rows = [row for row in replay.planned_rows() if row["bead"] == "think-0gp6"]
    assert len(rows) == 77
    assert all("superseded_by" not in row for row in rows)
    beaten = Counter(
        start
        for _, start, source in replay.planned_supersessions()
        if source == "mishapolk-issue732-2026-10-22"
    )
    assert beaten == SUPERSEDED_BY_732


def test_the_732_walk_holds_the_withdrawn_files_and_names_what_rests_on_holds() -> None:
    """The author's 1851c2c files at the nine counts #719's edit withdrew are below every
    earlier report, and #732's later files below them: held for think-8m4k. 369 and 376 are
    above 58a7833's held bound, itself above Göbel's construction; 985 equals 4e4c8ce's
    deletion bound. Only a deletion-bound answer would make one of #732's a new record."""
    walk = replay.WALKS[replay.ISSUE_732]
    (withdrawn,) = walk.held["Mishapolk/square-packing-records@1851c2c"]
    assert (withdrawn.kind, withdrawn.bead) == (replay.WITHDRAWN, "think-8m4k")
    assert sorted(withdrawn.counts) == [411, 451, 494, 495, 540, 583, 587, 632, 683]
    assert withdrawn.kind in replay.HELD_CLASSES
    mine = {item.kinds: item.counts for item in walk.resting if item.report == "#732"}
    assert {kinds[0]: len(counts) for kinds, counts in mine.items()} == RESTING_732
    assert {369, 376} <= mine[(replay.GOEBEL_ABOVE,)]
    assert 985 in mine[(replay.CONSEQUENCE,)]
    flips = replay.refusal_flips(walk, (replay.CONSEQUENCE,))
    assert [(n, falls) for n, report, falls in flips if report == "#732"] == [
        (985, replay.NEW_RECORD)
    ]
    assert replay.refusal_flips(walk, (replay.WITHDRAWN,)) == []


def test_the_732_ledger_transcribes_the_source_history_and_the_scan() -> None:
    """sources.yaml is what `release_walk_sources` writes from the packet's source history,
    the history scan and #715's held re-certifications, each publication strictly below
    the starts frozen at main fcf2f96a5, which read each row at its exact side."""
    sources = safe_load((ISSUE_732 / "sources.yaml").read_text(encoding="utf-8"))
    assert sources == replay.release_walk_sources(732, str(sources["read_on"]))
    starts = safe_load((ISSUE_732 / "starts.yaml").read_text(encoding="utf-8"))
    assert starts["read_at_main"] == replay.ISSUE_732_READ_AT_MAIN
    models = Counter(
        member["model"] for count in starts["counts"] for member in count["members"]
    )
    assert set(models) == {"exact", "print"}
    assert models["print"] < 5
