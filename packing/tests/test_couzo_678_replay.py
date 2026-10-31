"""The exact replay of issue #678: its rows, its pair filter, its controls and its receipts.

`devtools.couzo_678_replay` decides Francisco Couzo's 85 claimed upper bounds from the
83 certificates the ``couzo-issue678-2026-10-18`` packet retains. These tests hold the
smallest certificate, n = 204, to the outcomes the receipt records: both exact routes
accept it, and both refuse each of its six mutants. They hold the near-contact mutant to
its edge, the pair accepted in exact contact and refused 10^-30 past it, the pair filter to
its lemma, that no pair whose centres are closer than sqrt 2 is skipped, and the committed
receipts to the issue's table and the packet's manifest.
"""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

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


def test_the_near_contact_control_is_refused_at_the_least_gap_scale() -> None:
    """RF-2 of the 20 October review: the overlap controls were gross, gap -1 and centres
    within 7e-9, while the least gaps are 1e-11 to 1e-13. At 204 the near-contact pair is
    the receipt's least-gap pair, 5.56e-11 apart. Translated by the exact vector between its
    closest points it touches, and both routes accept it with that one contact; pushed
    10^-30 of its centre distance further, both refuse it on that pair, and on nothing
    else, at a depth no tolerance above 10^-29 would see."""
    cert = replay.certificate(replay.claims()[N204], replay.manifest())
    left, right, (dx, dy), squared = replay.near_contact_translation(cert)
    assert (left + 1, right + 1) == (115, 124)
    assert Fraction(1, 10**22) < squared < Fraction(1, 10**20)
    first, second = cert.poses[left], cert.poses[right]
    poses = list(cert.poses)
    poses[right] = replace(
        second,
        x=second.x + dx - replay.PAIR_PUSH * (first.x - second.x),
        y=second.y + dy - replay.PAIR_PUSH * (first.y - second.y),
    )
    touching = replay.decide(replay.geometry(replace(cert, poses=tuple(poses))))
    assert touching["passed"]
    assert touching["sqpack"]["touching_pairs"] == 1
    assert touching["independent"]["least_pair_gap"] == "0"
    assert touching["independent"]["least_pair"] == [115, 124]
    pushed = replay.decide(replay.control_geometry(cert, "near-contact-overlap"))
    assert not pushed["sqpack"]["passed"]
    assert not pushed["independent"]["passed"]
    assert pushed["sqpack"]["failures"] == ["squares 115 and 124 overlap"]
    [failure] = pushed["independent"]["failures"]
    assert failure.startswith("1 overlapping pairs; worst -")
    assert failure.endswith(" at 115, 124")
    depth = -Fraction(failure.split("worst ")[1].split(" at ")[0])
    assert Fraction(1, 10**31) < depth < Fraction(1, 10**29)


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


#: The review's own checker, which accepted 204 and 260 (`outputs/out-204-260.json`).
REVIEW_CHECKER = replay.PACKET / "review/programs/review_678_check.py"


@pytest.mark.parametrize(
    ("control", "pair"), [("duplicate-square", [1, 2]), ("near-contact-overlap", [115, 124])]
)
def test_the_review_checker_refuses_the_packet_mutants(
    tmp_path: Path, control: str, pair: list[int]
) -> None:
    """Stage 4's two mutated certificates, refused by the review's checker too, which the
    confirming entry E-couzo-678-review-exact-feasibility cites (review A2 of #706).

    The checker reads `certificates/best/n204.cert` under the source root it is given, so
    the mutant takes that place in a scratch root, and it decides every pair at 204: one
    pair overlaps by separating axes and by exact area, and the row is refused.
    """
    rows = replay.claims()
    cert = replay.certificate(rows[N204], replay.manifest())
    best = tmp_path / "source/certificates/best"
    best.mkdir(parents=True)
    (best / "n204.cert").write_text(
        replay.legacy.serialize(replay.mutant_certificate(cert, control)), encoding="utf-8"
    )
    out = tmp_path / "out.json"
    shown = subprocess.run(
        (
            sys.executable,
            "-I",
            str(REVIEW_CHECKER),
            str(tmp_path / "source"),
            str(replay.ISSUE),
            str(replay.FILTERED),
            str(out),
            "--only",
            "204",
            "--all-pairs",
            "204",
            "--workers",
            "1",
        ),
        capture_output=True,
        text=True,
        check=False,
        timeout=600,
    )
    assert shown.returncode == 1, shown.stderr
    (row,) = json.loads(out.read_text(encoding="utf-8"))["rows"]
    assert row["n"] == 204
    assert row["all_pairs"] is True
    assert row["passed"] is False
    assert (row["sat_overlaps"], row["area_overlaps"]) == (1, 1)
    assert row["least_pair"] == pair


def test_the_committed_receipts_hold() -> None:
    assert replay.check(replay=False) == []


def test_a_goebel_receipt_that_is_not_its_rebuild_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """think-llit (#793's review A, A13): ``check`` holds the committed Göbel receipt to
    its writer's rebuild byte for byte, so the families sentence it carried until it was
    rebuilt, one word longer than the writer's, is refused; the comparison is unchanged."""
    committed = replay.GOEBEL.read_text(encoding="utf-8")
    old = committed.replace("corner-touching strips", "corner-touching G\\u00f6bel strips")
    assert old != committed
    assert json.loads(old)["comparison"] == json.loads(committed)["comparison"]
    receipt = tmp_path / "goebel-comparison.json"
    receipt.write_text(old, encoding="utf-8")
    monkeypatch.setattr(replay, "GOEBEL", receipt)
    assert replay.check(replay=False) == ["the Göbel receipt differs from its rebuild"]


def test_the_claims_record_holds_the_rows_beyond_the_corpus() -> None:
    record = replay.beyond_horizon_claims()
    rows = {row.n: row for row in replay.claims()}
    counts = [entry["n"] for entry in record["results"]]
    assert counts == sorted(n for n in rows if n > upper_bound_reports.HORIZON)
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
