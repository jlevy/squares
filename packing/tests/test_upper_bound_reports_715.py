"""Francisco Couzo's issue #715: the rows at or below n = 1024, recorded on 22 October 2026.

`devtools.couzo_715_replay` decides the issue's rows at or below 1024 from the 139
certificates the ``couzo-issue715-2026-10-21`` packet retains. Every count is beyond the
``n <= 324`` case corpus, so the recorded rows are beyond-horizon rows of the source register
and no register entry. These tests hold what is particular to the import, as the stage 4
review of 19 October asked of the imports before it (RV-1 of
docs/project/reviews/review-2026-10-19-upper-bound-imports-659-664-669-674.md): which counts
are the issue's own reports and which restate or re-certify earlier publications, that each
recorded row supersedes the row that stood at its count in report order, that the explicit
files realize the source index's constructions, that the receipts hold, and that the 22
October ledger decides each count as the record does. Every test reads the retained packet,
the ledger and the source register only; none needs the network.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import check_source_coverage as coverage_check
from devtools import couzo_715_replay as replay
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_bytes
from sqpack.yamlio import safe_load

SOURCE = "couzo-issue715-2026-10-21"
COVERAGE = reports.REPO / "packing/frontier/source-coverage.yaml"
LEDGER = replay.ROOT / "campaign/issue-intake/upper-bounds-20261022"
#: The row each recorded count superseded, by source, and the counts that held none. The
#: backlog rows of #666, #670, #672 and #675, recorded on 22 October after this import,
#: stand before it in report order: ten of them are the rows its rows supersede, and at
#: eight of those counts the 14 October row now names the backlog report that beat it
#: first, so 21 of its 29 rows remain here. 509 and 931 no longer hold this import's row
#: alone.
#: Since the history walk of 22 October, 20 of the rows here beat Couzo's 4e4c8ce index
#: first, which had beaten 487b058's.
SUPERSEDED = {
    "muglich-issue686-2026-10-19": 50,
    "couzo-verified-bounds-2026-10-14": 1,
    "couzo-index-2026-10-15": 20,
    "couzo-issue678-2026-10-18": 26,
    "evand-n343-sweep-2026-10-20": 1,
    "de-winter-issue666-2026-10-17": 1,
    "couzo-issue670-2026-10-17": 2,
    "couzo-issue672-2026-10-17": 1,
    "couzo-issue675-2026-10-18": 6,
}
GRID_COUNTS = [860]
#: The rows of this import that issue 719's rows, reported on 22 October, supersede.
LATER = "mishapolk-issue719-2026-10-22"
SUPERSEDED_BY_LATER = (
    417,
    456,
    499,
    553,
    601,
    652,
    705,
    758,
    868,
    869,
    872,
    927,
    928,
    932,
    994,
    996,
)
#: Issue 702's exact side at 343, which this import's row supersedes in report order.
SIDE_702 = Fraction(18977682482404124568634475670459, 10**30)
#: The certificates the issue restates that earlier packets already retain, byte for byte.
RETAINED_ELSEWHERE = {
    335: "couzo-exact-certificates-2026-10-09",
    336: "couzo-exact-certificates-2026-10-09",
    337: "couzo-exact-certificates-2026-10-09",
    338: "couzo-certificates-2026-10-12",
    340: "couzo-certificates-2026-10-11",
    341: "couzo-exact-certificates-2026-10-09",
    373: "couzo-exact-certificates-2026-10-09",
    374: "couzo-exact-certificates-2026-10-09",
}


def _coverage() -> Any:
    return safe_load(COVERAGE.read_text(encoding="utf-8"))


def _rows_at(coverage: Any, n: int) -> dict[str, Any]:
    return {row["source_id"]: row for row in coverage["beyond_horizon_claims"] if row["n"] == n}


def test_the_issue_table_splits_into_the_three_sets_and_retention_follows_them() -> None:
    assert len(replay.claims()) == replay.ROWS
    decided = replay.decided_claims()
    assert len(decided) == replay.DECIDED
    sets = {name: replay.counts_in(name) for name in replay.SET_SIZES}
    assert {name: len(counts) for name, counts in sets.items()} == replay.SET_SIZES
    assert sorted(n for counts in sets.values() for n in counts) == [row.n for row in decided]
    for row in decided:
        assert replay.retained(row.n) == (row.n not in sets[replay.RESTATED])
    assert replay.publication_problems() == []


def test_every_new_certificate_reached_the_repository_through_the_issue() -> None:
    record = replay.publications()
    assert (record["public_head"], record["revision"]) == (replay.PUBLIC_HEAD, replay.PIN)
    assert record["issue_filed"] < record["public_until"]
    rewritten = []
    for row in record["rows"]:
        # Newness is reachability from the public head, never a committer date.
        if row["set"] != replay.RESTATED:
            assert not row["first_commit_public"]
            continue
        assert row["below_earlier_by"] == "0"
        if not row["first_commit_public"]:
            rewritten.append(row["n"])
    # Two restated deletions were written out again at the same side as the 4e4c8ce
    # index's deletion bound; the other 32 restated files are the earlier bytes.
    assert rewritten == [743, 985]


def test_the_held_counts_are_below_an_earlier_publication_only_under_the_print() -> None:
    for row in replay.publications()["rows"]:
        margin = Fraction(row["below_earlier_by"])
        if row["set"] == replay.HELD:
            assert Fraction(236, 10**25) < margin < Fraction(32, 10**24)
            assert row["earlier"]["ceiling_12"] == row["printed"]
            assert row["earlier"]["commit"].startswith("4e4c8ce")
        elif row["set"] == replay.RECORDED:
            assert margin > Fraction(29, 10**8)
            assert row["earlier"]["ceiling_12"] > row["printed"]


def test_the_restated_certificates_are_pinned_against_their_earlier_packets() -> None:
    digests = replay.manifest()
    for n, packet in RETAINED_ELSEWHERE.items():
        copy = reports.REPO / f"packing/resources/web/{packet}/source/certificates/n{n}.cert"
        assert (
            hashlib.sha256(read_retained_bytes(copy)).hexdigest()
            == digests[f"certificates/n{n}.cert"]
        )
    assert set(RETAINED_ELSEWHERE) <= set(replay.counts_in(replay.RESTATED))


def test_the_recorded_rows_are_the_claims_record_and_supersede_the_rows_before_them() -> None:
    claims = coverage_check.load_claims(replay.BEYOND)
    recorded = replay.counts_in(replay.RECORDED)
    assert sorted(claims) == recorded
    coverage = _coverage()
    current = coverage_check.current_beyond_horizon(coverage)
    before: Counter[str] = Counter()
    for n in recorded:
        rows = _rows_at(coverage, n)
        assert rows[SOURCE]["value"] == claims[n]
        before.update(
            source for source, row in rows.items() if row.get("superseded_by") == SOURCE
        )
        if n in SUPERSEDED_BY_LATER:
            assert rows[SOURCE]["disposition"] == "superseded"
            assert rows[SOURCE]["superseded_by"] == LATER
            assert current[n]["source_id"] == LATER
            continue
        assert rows[SOURCE]["disposition"] == "tracked-outside-case-corpus"
        assert current[n]["source_id"] == SOURCE
    assert dict(before) == SUPERSEDED
    assert [n for n in recorded if len(_rows_at(coverage, n)) == 1] == GRID_COUNTS
    for n in replay.counts_in(replay.HELD) + replay.counts_in(replay.RESTATED):
        assert SOURCE not in _rows_at(coverage, n)


def test_343_is_recorded_after_678_and_702_each_below_the_last() -> None:
    rows = _rows_at(_coverage(), 343)
    assert rows["couzo-issue678-2026-10-18"]["superseded_by"] == "evand-n343-sweep-2026-10-20"
    assert rows["evand-n343-sweep-2026-10-20"]["superseded_by"] == SOURCE
    (claim,) = [row for row in replay.decided_claims() if row.n == 343]
    side = replay.certificate(claim).side
    assert side == Fraction(3993049794861220561760624561, 210408851936750000000000000)
    assert Fraction(10735, 10**8) < SIDE_702 - side < Fraction(10736, 10**8)


def test_the_explicit_files_realize_the_index_constructions() -> None:
    """At 365 the index states the 328 certificate with one L-border layer: the explicit
    file is the 328 packing's poses, then 37 axis-aligned squares, at side + 1. At 500 it
    states a deletion from 501: the file is the 501 packing's first 500 poses."""
    rows = {row.n: row for row in replay.decided_claims()}
    parent, border = replay.certificate(rows[328]), replay.certificate(rows[365])
    assert border.poses[:328] == parent.poses
    assert all(pose.t == 0 for pose in border.poses[328:])
    assert border.side == parent.side + 1
    full, deleted = replay.certificate(rows[501]), replay.certificate(rows[500])
    assert deleted.poses == full.poses[:500]
    assert deleted.side == full.side
    stored = json.loads(replay.FILTERED.read_text(encoding="utf-8"))["rows"]
    relations = [row["source_index"] for row in stored]
    assert Counter(relation["kind"] for relation in relations) == {
        "certificate": 80,
        "construction": 59,
    }
    for relation in relations:
        assert relation["bound_equals_header"]
        assert relation.get("parent_poses_lead", True)
        assert relation.get("added_squares_axis_aligned", True)
        assert relation.get("side_is_parent_side_plus_layers", True)


def test_the_receipts_hold_and_328_decides_again_as_recorded() -> None:
    assert replay.check(replay=False) == []
    stored = {row["n"]: row for row in json.loads(replay.FILTERED.read_text("utf-8"))["rows"]}
    (claim,) = [row for row in replay.decided_claims() if row.n == 328]
    again = replay.decide_row(claim)
    assert again["verified"]
    keep = {key: again[key] for key in ("exact_side", "printed", "controls")}
    assert keep == {key: stored[328][key] for key in keep}


def test_the_22_october_ledger_decides_each_count_as_the_record_does() -> None:
    ledger = json.loads((LEDGER / "ledger.json").read_text(encoding="utf-8"))
    verdicts = {
        count["n"]: step["verdict"]
        for count in ledger["counts"]
        for step in count["steps"]
        if step["report"] == "#715"
    }
    recorded = set(replay.counts_in(replay.RECORDED))
    held = set(replay.counts_in(replay.HELD))
    assert {n for n, verdict in verdicts.items() if verdict == "recorded"} == recorded
    # 338's start is the identical certificate, read by its print: undecided, a tie.
    assert {n for n, verdict in verdicts.items() if verdict == "undecided"} == held | {338}
    assert {n for n, verdict in verdicts.items() if verdict == "not recorded"} == (
        set(replay.counts_in(replay.RESTATED)) - {338}
    )
    assert ledger["read_at_main"] == "d588ad987bd8de53361d087b8961a7f2bf157c41"


def test_the_ledger_reads_the_exact_sides_the_publications_receipt_holds() -> None:
    """Each exact side the 22 October ledger's sources give #715 or a watched-repository
    publication is the side the packet's publications receipt read from the certificate."""
    sources = safe_load((LEDGER / "sources.yaml").read_text(encoding="utf-8"))
    rows = {row["n"]: row for row in replay.publications()["rows"]}
    checked = 0
    for report in sources["reports"]:
        for claim in report["claims"]:
            if "exact" not in claim:
                continue
            if report["report"] == "#715":
                assert claim["exact"] == rows[claim["n"]]["exact_side"]
                checked += 1
            elif report["report"].startswith("franciscouzo/square-packing@"):
                earlier = rows[claim["n"]]["earlier"]
                assert report["report"].endswith(earlier["commit"][:7])
                assert claim["exact"] == earlier["exact_side"]
                checked += 1
    held = set(replay.counts_in(replay.HELD))
    assert checked == (replay.DECIDED - len(held)) + (len(held) + 34 - 1)


@pytest.mark.parametrize(
    ("side", "printed", "earlier", "expected"),
    [
        (Fraction(1, 3), "0.333333333334", Fraction(1, 3), replay.RESTATED),
        (Fraction(1, 3), "0.333333333334", Fraction(1, 3) + Fraction(1, 10**20), replay.HELD),
        (
            Fraction(1, 3),
            "0.333333333334",
            Fraction(1, 3) + Fraction(1, 10**9),
            replay.RECORDED,
        ),
    ],
)
def test_classify_reads_equal_sub_print_and_print_margins(
    side: Fraction, printed: str, earlier: Fraction, expected: str
) -> None:
    assert replay.classify(side, printed, earlier) == expected


@pytest.mark.parametrize(
    ("side", "printed", "earlier", "refusal"),
    [
        (Fraction(1, 3), "0.333333333334", Fraction(1, 3) - Fraction(1, 10**20), "above"),
        (Fraction(1, 3), "0.333333333333", Fraction(1, 3), "rounded up"),
        (Fraction(1, 3), "0.333333333335", Fraction(1, 3), "rounded up"),
    ],
)
def test_classify_refuses_a_side_above_its_earlier_one_or_off_its_print(
    side: Fraction, printed: str, earlier: Fraction, refusal: str
) -> None:
    with pytest.raises(replay.ReplayError, match=refusal):
        replay.classify(side, printed, earlier)


def _forge(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, name: str, edit: Any) -> Path:
    """A copy of one receipt under ``tmp_path``, edited, that the module then reads."""
    source = {"filtered": replay.FILTERED, "publications": replay.PUBLICATIONS}[name]
    value = json.loads(source.read_text(encoding="utf-8"))
    edit(value)
    copy = tmp_path / source.name
    copy.write_text(json.dumps(value), encoding="utf-8")
    monkeypatch.setattr(
        replay, {"filtered": "FILTERED", "publications": "PUBLICATIONS"}[name], copy
    )
    return copy


def _filtered_check(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, edit: Any) -> list[str]:
    """`check` on a forged filtered receipt, the publications and claims records held."""
    _forge(monkeypatch, tmp_path, "filtered", edit)
    record = json.loads(replay.BEYOND.read_text(encoding="utf-8"))
    monkeypatch.setattr(replay, "custody", lambda: None)
    monkeypatch.setattr(replay, "publication_problems", list)
    monkeypatch.setattr(replay, "beyond_horizon_claims", lambda: record)
    return replay.check(replay=False)


def test_a_control_forged_as_accepted_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def edit(value: Any) -> None:
        value["rows"][0]["controls"][2]["refused_by_independent"] = False

    problems = _filtered_check(monkeypatch, tmp_path, edit)
    assert any("side-below-least-clearance was accepted" in problem for problem in problems)


def test_an_index_relation_forged_false_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def edit(value: Any) -> None:
        (row,) = [row for row in value["rows"] if row["n"] == 365]
        row["source_index"]["parent_poses_lead"] = False

    problems = _filtered_check(monkeypatch, tmp_path, edit)
    assert problems == ["n=365: the file does not realize the index's entry"]


def test_a_receipt_row_moved_to_another_count_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def edit(value: Any) -> None:
        value["rows"][0]["n"] = 327

    problems = _filtered_check(monkeypatch, tmp_path, edit)
    assert problems == ["the filtered receipt's rows are not the retained certificates"]


def test_a_held_row_relabelled_recorded_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def edit(value: Any) -> None:
        (row,) = [row for row in value["rows"] if row["n"] == 535]
        row["set"] = replay.RECORDED

    _forge(monkeypatch, tmp_path, "publications", edit)
    problems = replay.publication_problems()
    assert "n=535: the set is held, not recorded" in problems


def test_a_recorded_row_made_equal_to_its_earlier_side_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def edit(value: Any) -> None:
        (row,) = [row for row in value["rows"] if row["n"] == 328]
        row["earlier"]["exact_side"] = row["exact_side"]

    _forge(monkeypatch, tmp_path, "publications", edit)
    problems = replay.publication_problems()
    assert "n=328: the margin is not the sides' difference" in problems
    assert "n=328: the set is restated, not recorded" in problems


def test_a_new_row_marked_public_before_the_issue_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def edit(value: Any) -> None:
        (row,) = [row for row in value["rows"] if row["n"] == 343]
        row["first_commit_public"] = True

    _forge(monkeypatch, tmp_path, "publications", edit)
    assert "n=343: first committed while public, yet new" in replay.publication_problems()
