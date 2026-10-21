"""The exact replay of issue #678: its rows, its pair filter, its controls and its receipts.

`devtools.couzo_678_replay` decides Francisco Couzo's 85 claimed upper bounds from the
83 certificates the ``couzo-issue678-2026-10-18`` packet retains. These tests hold the
smallest certificate, n = 204, to the outcomes the receipt records: both exact routes
accept it, and both refuse each of its five mutants. They hold the pair filter to its
lemma, that no pair whose centres are closer than sqrt 2 is skipped, and the committed
receipts to the issue's table and the packet's manifest.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

from devtools import acquire_source, upper_bound_reports
from devtools import couzo_678_replay as replay

N204 = 0


def test_the_rows_are_the_issue_table() -> None:
    rows = replay.claims()
    assert len(rows) == replay.ROWS
    assert len({row.path for row in rows}) == replay.CERTIFICATES
    deleted = {row.n: (row.certificate_n, row.deleted) for row in rows if row.deleted}
    assert deleted == {545: (546, 1), 641: (642, 1)}
    assert rows[N204].n == 204


def test_the_filter_skips_only_pairs_at_least_sqrt2_apart() -> None:
    half = Fraction(1, 2)
    assert replay.candidate_pairs([(half, half), (half + 1, half + 1)]) == []
    nearly = Fraction(99, 100)
    assert replay.candidate_pairs([(half, half), (half + 1, half + nearly)]) == [(0, 1)]
    cert = replay.certificate(replay.claims()[N204], replay.manifest())
    centres = [(pose.x, pose.y) for pose in cert.poses]
    kept = set(replay.candidate_pairs(centres))
    for left in range(len(centres)):
        for right in range(left + 1, len(centres)):
            dx = centres[right][0] - centres[left][0]
            dy = centres[right][1] - centres[left][1]
            assert ((left, right) in kept) == (dx * dx + dy * dy < 2)


def test_n204_is_verified_and_every_control_is_refused() -> None:
    row = replay.decide_row(replay.claims()[N204])
    assert row["verified"]
    assert row["printed_is_upward_rounding"]
    assert row["decision"]["sqpack"]["passed"]
    assert row["decision"]["independent"]["passed"]
    assert [control["control"] for control in row["controls"]] == list(replay.CONTROLS)
    for control in row["controls"]:
        assert control["refused_by_sqpack"], control["control"]
        assert control["refused_by_independent"], control["control"]


def test_a_deletion_row_is_its_parent_less_one_square() -> None:
    rows = {row.n: row for row in replay.claims()}
    digests = replay.manifest()
    parent = replay.certificate(rows[546], digests)
    derived = replay.certificate(rows[545], digests)
    assert derived.n == 545
    assert derived.side == parent.side
    assert derived.poses == parent.poses[:545]


def test_a_print_must_round_the_side_up() -> None:
    side = Fraction(14808642841981247, 10**15)
    assert replay.rounds_up_to(side, "14.808642841982")
    assert not replay.rounds_up_to(side, "14.808642841981")
    assert not replay.rounds_up_to(side, "14.808642841983")


def test_the_packet_custody_holds() -> None:
    assert acquire_source.check(replay.PACKET, replay.REPO) == []
    assert "verify_bound_certificate.py" in replay.manifest()


def test_the_source_checker_refuses_a_duplicate_square(tmp_path: Path) -> None:
    rows = replay.claims()
    cert = replay.certificate(rows[N204], replay.manifest())
    assert replay.source_run(replay.SOURCE / rows[N204].path)["valid"] is True
    mutant = tmp_path / "duplicate.cert"
    mutant.write_text(
        replay.legacy.serialize(replay.mutant_certificate(cert, "duplicate-square")),
        encoding="utf-8",
    )
    outcome = replay.source_run(mutant)
    assert outcome["exit"] == 1
    assert outcome["valid"] is False


def test_the_committed_receipts_hold() -> None:
    assert replay.check(replay=False) == []


def test_the_claims_record_holds_the_rows_beyond_the_corpus() -> None:
    record = replay.beyond_horizon_claims()
    rows = {row.n: row for row in replay.claims()}
    counts = [entry["n"] for entry in record["results"]]
    assert counts == sorted(n for n in rows if n > replay.HORIZON)
    assert len(counts) == replay.ROWS - 2
    assert 204 not in counts
    assert 260 not in counts
    for entry in record["results"]:
        assert entry["offered_side"] == rows[entry["n"]].printed
        assert replay.rounds_up_to(Fraction(entry["exact_side"]), entry["offered_side"])
    # The two deletion rows are the only ones the builder takes from another count's
    # certificate: each names its parent's file, deletes one square and shares its side.
    by_n = {entry["n"]: entry for entry in record["results"]}
    for n, parent in ((545, 546), (641, 642)):
        assert by_n[n]["certificate"] == f"certificates/best/n{parent}.cert"
        assert by_n[n]["deleted"] == 1
        assert by_n[n]["exact_side"] == by_n[parent]["exact_side"]
    assert {n for n, entry in by_n.items() if entry["deleted"]} == {545, 641}
    assert record["format"] == upper_bound_reports.BEYOND_FORMAT
    assert record["horizon"] == upper_bound_reports.HORIZON
