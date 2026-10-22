"""The beyond-horizon rows of issues #666, #670, #672 and #675, recorded on 22 October 2026.

`devtools.beyond_horizon_replay` decides the rows at or below 1024 of four reports from
their retained packets: Joost de Winter's #666 (11 of its 19 rows; the 8 above 1024 wait on
the owner) and the rows beyond the corpus of Francisco Couzo's #670, #672 and #675, whose
in-corpus rows T-226 to T-228 register. These tests hold what is particular to the import:
each issue table's rows and the certificate each reads, the receipts and records against the
packets, the first commit of every certificate, each row's place in the backlog ledger's
report order and the coverage register's rows that follow from it, and the forged receipt
rows a check must refuse. Every test reads the retained packets, the ledger and the source
register only; none needs the network.
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
from sqpack.yamlio import safe_load

LEDGER = replay.ROOT / "campaign/issue-intake/upper-bounds-backlog-20261022"
#: Each report's rows: the table's, the decided (beyond the corpus to 1024) and the held.
ROWS = {666: (19, 11, 8), 670: (73, 72, 0), 672: (46, 44, 0), 675: (79, 78, 0)}
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
            assert (replay.archive(chosen) / row.path).is_file(), (issue, row.n)
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
        assert {(row["first_commit"], row["committed"]) for row in commits["rows"]} == {
            (chosen.first_commit, chosen.committed)
        }
        record = _read(chosen.directory / replay.RECORD)
        assert {row["first_committed"] for row in record["results"]} == {chosen.committed}


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


def test_each_side_rounds_up_to_its_print_and_the_ledger_reads_the_same_side() -> None:
    sources = safe_load((LEDGER / "sources.yaml").read_text(encoding="utf-8"))
    transcribed = {
        (report["report"], claim["n"]): Fraction(claim["exact"])
        for report in sources["reports"]
        for claim in report["claims"]
        if "exact" in claim
    }
    for issue, chosen in replay.RELEASES.items():
        for row in _read(chosen.directory / replay.RECORD)["results"]:
            side = Fraction(row["exact_side"])
            printed = Fraction(row["offered_side"])
            assert printed - Fraction(1, 10**12) < side <= printed, (issue, row["n"])
            assert transcribed[f"#{issue}", row["n"]] == side, (issue, row["n"])


def test_the_ledger_records_every_row_and_the_plan_reads_its_dispositions() -> None:
    verdicts = _read(LEDGER / "ledger.json")
    ours = {f"#{issue}" for issue in replay.RELEASES}
    steps = [
        step
        for count in verdicts["counts"]
        for step in count["steps"]
        if step["report"] in ours and count["n"] > 324
    ]
    assert len(steps) == sum(chosen.decided for chosen in replay.RELEASES.values())
    assert {step["verdict"] for step in steps} == {"recorded"}
    rows = replay.planned_rows()
    current = {row["n"]: row["source_id"] for row in rows if "superseded_by" not in row}
    assert current == dict.fromkeys(CURRENT_670, "couzo-issue670-2026-10-17")
    found: dict[str, Counter[str]] = {}
    for row in rows:
        if "superseded_by" in row:
            found.setdefault(row["source_id"], Counter())[row["superseded_by"]] += 1
    assert {source: dict(counts) for source, counts in found.items()} == SUCCESSORS
    assert replay.planned_supersessions() == [
        (n, earlier, "couzo-issue670-2026-10-17") for n, earlier in CURRENT_670.items()
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
