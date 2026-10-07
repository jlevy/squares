"""The quick lane's shard partition and its per-file cost report (`devtools.suite_files`)."""

from __future__ import annotations

import json
import os
import random
import subprocess
import sys
from pathlib import Path

import pytest

from devtools import suite_files
from devtools.suite_files import RecordedCosts, Shard, SuiteFilesError
from sqpack.cli import validate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO = PROJECT_ROOT.parent
TEST_ROOTS = (PROJECT_ROOT / "tests", REPO / "packages/workbench/tests")
EXHAUSTIVE_COSTS = PROJECT_ROOT / "devtools/exhaustive-file-costs.json"


def _test_files() -> set[str]:
    """Every file in either behavioural root, repository-relative."""
    return {
        suite_files.repository_path(path)
        for root in TEST_ROOTS
        for path in root.rglob("test_*.py")
        if "__pycache__" not in path.parts
    }


def test_the_suite_shards_partition_every_test_file() -> None:
    """Each test file on disk is in exactly one shard, and every shard has files.

    This is the property that lets the runners divide the lane without a test running
    twice or not at all. It holds by construction -- a file's shard is a function of its
    path -- so what this checks is the construction against the real tree and the real
    record: that the recorded count is the one the CLI and the register use, and that
    the files each shard would collect are disjoint and add up to the whole lane.
    """
    costs = suite_files.load_costs()
    assert costs.shards == validate.SUITE_SHARDS
    packed = suite_files.pack(costs)
    files = _test_files()
    assert any(name.startswith("packages/workbench/tests/") for name in files)
    shards = [
        {name for name in files if suite_files.shard_of(name, costs, packed) == index}
        for index in range(1, costs.shards + 1)
    ]
    assert set().union(*shards) == files
    assert sum(len(shard) for shard in shards) == len(files)
    assert all(shards)


def test_the_exhaustive_shards_partition_current_files_and_new_arrivals() -> None:
    """Three runners cover every eligible test file once before marker selection.

    Pytest applies ``-m exhaustive_exact`` after the file partition. Partitioning the
    complete discovery roots therefore preserves module, class, parametrized, inherited
    and dynamically applied marker forms without guessing how the mark is expressed.
    """
    costs = suite_files.load_costs(EXHAUSTIVE_COSTS)
    assert costs.shards == 3
    packed = suite_files.pack(costs)
    files = _test_files()
    assert set(costs.seconds) <= files
    shards = [
        {name for name in files if suite_files.shard_of(name, costs, packed) == index}
        for index in range(1, costs.shards + 1)
    ]
    assert set().union(*shards) == files
    assert sum(len(shard) for shard in shards) == len(files)
    assert all(shards)

    arrival = "packing/tests/test_new_exhaustive_decision.py"
    assert arrival not in costs.seconds
    assigned = suite_files.shard_of(arrival, costs, packed)
    assert assigned == suite_files.unrecorded_shard(arrival, costs.shards)
    assert 1 <= assigned <= costs.shards


def test_the_record_names_only_files_under_the_behavioural_roots() -> None:
    """A recorded path outside both roots matches no collected file and still takes weight.

    Schema-v1 reports derived the file from a nodeid relative to `packing/`, so the
    workbench tests were recorded as `packing/test_*.py`: sixteen entries and 15.05
    recorded seconds that the packing balanced while the real files fell back to their
    path hash. A rename or a deletion may still leave a stale row, which the design
    tolerates; a row under no behavioural root is a mislabelled report.
    """
    roots = tuple(f"{suite_files.repository_path(root)}/" for root in TEST_ROOTS)
    costs = suite_files.load_costs()
    assert sorted(name for name in costs.seconds if not name.startswith(roots)) == []


def test_the_packing_depends_only_on_the_record() -> None:
    """The same record in any order packs the same way, and a new file moves nothing."""
    costs = suite_files.load_costs()
    items = list(costs.seconds.items())
    random.Random(20260915).shuffle(items)
    shuffled = RecordedCosts(
        shards=costs.shards,
        seconds=dict(items),
        target_ceiling_seconds=costs.target_ceiling_seconds,
    )
    assert suite_files.pack(shuffled) == suite_files.pack(costs)

    packed = suite_files.pack(costs)
    arrival = "packing/tests/test_a_file_nobody_has_recorded_yet.py"
    assert arrival not in costs.seconds
    shard = suite_files.shard_of(arrival, costs, packed)
    assert shard == suite_files.unrecorded_shard(arrival, costs.shards)
    assert 1 <= shard <= costs.shards
    # Nothing recorded changes shard because a file arrived.
    assert {name: suite_files.shard_of(name, costs, packed) for name in costs.seconds} == packed


def test_the_greedy_packing_balances_within_its_largest_file() -> None:
    costs = RecordedCosts(
        shards=2, seconds={"a.py": 9.0, "b.py": 5.0, "c.py": 4.0, "d.py": 3.0, "e.py": 1.0}
    )
    assert suite_files.pack(costs) == {"a.py": 1, "b.py": 2, "c.py": 2, "d.py": 1, "e.py": 2}
    totals = suite_files.shard_totals(costs)
    assert totals == [12.0, 10.0]
    assert max(totals) - min(totals) <= max(costs.seconds.values())


def test_capacity_weighted_packing_preserves_the_measured_assignment() -> None:
    """Historical capacities retain the reviewed partition as live ceilings evolve."""
    costs = suite_files.load_costs()
    assert costs.target_ceiling_seconds == (131.0, 154.0, 154.0, 131.0)
    totals = suite_files.shard_totals(costs)
    assert costs.target_ceiling_seconds is not None
    normalized = [
        total / ceiling
        for total, ceiling in zip(totals, costs.target_ceiling_seconds, strict=True)
    ]
    assert max(normalized) / min(normalized) <= 1.01
    weighted = RecordedCosts(
        shards=2,
        seconds={"a.py": 9.0, "b.py": 5.0, "c.py": 4.0, "d.py": 3.0, "e.py": 1.0},
        target_ceiling_seconds=(2.0, 1.0),
    )
    assert suite_files.pack(weighted) == {
        "a.py": 1,
        "b.py": 2,
        "c.py": 1,
        "d.py": 2,
        "e.py": 1,
    }
    assert suite_files.shard_totals(weighted) == [14.0, 8.0]


@pytest.mark.parametrize(
    "targets",
    [(0.0, 1.0), (-1.0, 1.0), (float("nan"), 1.0), (float("inf"), 1.0), (1.0,)],
)
def test_invalid_capacity_targets_refuse(targets: tuple[float, ...]) -> None:
    with pytest.raises(SuiteFilesError, match="target ceilings"):
        suite_files.pack(
            RecordedCosts(shards=2, seconds={"a.py": 1.0}, target_ceiling_seconds=targets)
        )


def test_json_boolean_capacity_refuses(tmp_path: Path) -> None:
    path = tmp_path / "costs.json"
    path.write_text(
        json.dumps(
            {
                "schema": suite_files.COSTS_SCHEMA,
                "shards": 2,
                "target_ceiling_seconds": [True, 154],
                "files": {"packing/tests/test_a.py": 1.0},
            }
        )
    )
    with pytest.raises(SuiteFilesError, match="target ceilings"):
        suite_files.load_costs(path)


@pytest.mark.parametrize("text", ["2", "0/2", "3/2", "a/b", "1/"])
def test_a_shard_is_written_k_of_n(text: str) -> None:
    with pytest.raises(SuiteFilesError):
        _ = Shard.parse(text)
    assert str(Shard.parse("2/2")) == "2/2"


def test_record_takes_each_files_geometric_mean_and_names_its_sources() -> None:
    reports = [
        suite_files.report_document(
            {"packing/tests/test_a.py": (3, 2.0), "packing/tests/test_b.py": (1, 0.0)},
            shard=None,
            environment={"GITHUB_RUN_ID": "1", "GITHUB_JOB": "suite-1-of-2"},
            exit_status=0,
        ),
        suite_files.report_document(
            {"packing/tests/test_a.py": (3, 8.0), "packing/tests/test_b.py": (1, 0.0)},
            shard=None,
            environment={},
            exit_status=0,
        ),
    ]
    document = suite_files.record(reports, shards=2)
    assert document["files"] == {
        "packing/tests/test_a.py": 4.0,
        "packing/tests/test_b.py": 0.0,
    }
    assert document["recorded_from"] == [
        "the whole lane: GITHUB_JOB=suite-1-of-2, GITHUB_RUN_ID=1",
        "the whole lane: no CI provenance",
    ]
    assert reports[0]["tests"] == 4
    assert reports[0]["seconds"] == 2.0


def test_a_report_records_the_resolved_validated_tree() -> None:
    report = suite_files.report_document(
        {"packing/tests/test_a.py": (1, 0.25)},
        shard=Shard(1, 3),
        environment={
            "PACKING_VALIDATED_SHA": "resolved-merge-sha",
            "GITHUB_SHA": "dispatch-ref-sha",
        },
        exit_status=0,
    )

    assert report["provenance"] == {
        "PACKING_VALIDATED_SHA": "resolved-merge-sha",
        "GITHUB_SHA": "dispatch-ref-sha",
    }


def _shard_report(
    index: int,
    *,
    run: str = "1",
    attempt: str = "1",
    sha: str = "abc",
    seconds: float | None = None,
    exit_status: int = 0,
    file: str | None = None,
    count: int = 2,
) -> dict[str, object]:
    return suite_files.report_document(
        {
            file or f"packing/tests/test_{index}.py": (
                1,
                float(index) if seconds is None else seconds,
            )
        },
        shard=Shard(index, count),
        environment={
            "GITHUB_RUN_ID": run,
            "GITHUB_RUN_ATTEMPT": attempt,
            "GITHUB_JOB": f"suite-{index}",
            "GITHUB_SHA": sha,
        },
        exit_status=exit_status,
    )


def test_record_requires_one_complete_coherent_shard_cohort() -> None:
    complete = [_shard_report(1), _shard_report(2)]
    assert suite_files.record(complete, shards=2)["files"] == {
        "packing/tests/test_1.py": 1.0,
        "packing/tests/test_2.py": 2.0,
    }
    with pytest.raises(SuiteFilesError, match="each shard exactly once"):
        suite_files.record(complete[:1], shards=2)
    with pytest.raises(SuiteFilesError, match="each shard exactly once"):
        suite_files.record([complete[0], complete[0]], shards=2)
    with pytest.raises(SuiteFilesError, match="each sharded cohort"):
        suite_files.record([complete[0], _shard_report(2, run="2")], shards=2)
    with pytest.raises(SuiteFilesError, match="each sharded cohort"):
        suite_files.record([complete[0], _shard_report(2, attempt="2")], shards=2)
    with pytest.raises(SuiteFilesError, match="each sharded cohort"):
        suite_files.record([complete[0], _shard_report(2, sha="def")], shards=2)


def test_three_shard_record_requires_all_three_reports() -> None:
    complete = [_shard_report(index, count=3) for index in (1, 2, 3)]
    document = suite_files.record(complete, shards=3, target_ceiling_seconds=(168, 154, 154))
    assert len(document["files"]) == 3
    assert document["target_ceiling_seconds"] == [168, 154, 154]
    with pytest.raises(SuiteFilesError, match="each shard exactly once"):
        suite_files.record(complete[:2], shards=3)
    # Two of three is incomplete by the count the reports were cut at, so asking to pack
    # into two does not turn `1/3` and `2/3` into a complete cohort of two.
    with pytest.raises(SuiteFilesError, match="each shard exactly once"):
        suite_files.record(complete[:2], shards=2)


def test_record_packs_a_complete_cohort_into_another_shard_count() -> None:
    """A repartition: the cohort's count is provenance and the requested count is the record's.

    The lane's costs are per file, so a complete two-shard cohort says everything a
    three-shard record needs. Before this was allowed, the three-shard record was made by
    editing `shards` by hand on a two-shard cohort's output.
    """
    complete = [_shard_report(1), _shard_report(2)]
    same = suite_files.record(complete, shards=2)
    repacked = suite_files.record(complete, shards=3, target_ceiling_seconds=(168, 154, 154))
    assert same["shards"] == 2
    assert repacked["shards"] == 3
    assert repacked["files"] == same["files"]
    assert repacked["target_ceiling_seconds"] == [168, 154, 154]
    # The sources still say what the reports were: shards of two.
    assert repacked["recorded_from"] == same["recorded_from"]
    assert [source.split(":")[0] for source in repacked["recorded_from"]] == [
        "shard 1/2",
        "shard 2/2",
    ]
    # Capacities are per packed shard, so the cohort's count does not excuse a short list.
    with pytest.raises(SuiteFilesError, match="target ceilings"):
        suite_files.record(complete, shards=3, target_ceiling_seconds=(168, 154))


def test_record_refuses_reports_cut_for_different_shard_counts() -> None:
    """Shards `1/2` and `2/3` would otherwise pass as one complete cohort of two."""
    mixed = [_shard_report(1), _shard_report(2, count=3)]
    for requested in (2, 3, 4):
        with pytest.raises(SuiteFilesError, match=r"shard count\(s\) \[2, 3\], not one count"):
            suite_files.record(mixed, shards=requested)


def test_the_record_command_repacks_a_cohort_and_the_result_loads(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The command a repartition runs: three reports in, a four-shard record out."""
    paths: list[str] = []
    for index in (1, 2, 3):
        path = tmp_path / f"report-{index}.json"
        path.write_text(json.dumps(_shard_report(index, count=3)), encoding="utf-8")
        paths.append(str(path))
    output = tmp_path / "costs.json"
    arguments = ["record", *paths, "--shards", "4", "--output", str(output)]
    assert suite_files.main([*arguments, "--target-ceilings", "131,154,154,131"]) == 0
    costs = suite_files.load_costs(output)
    assert costs.shards == 4
    assert costs.target_ceiling_seconds == (131.0, 154.0, 154.0, 131.0)
    assert costs.seconds == {
        f"packing/tests/test_{index}.py": float(index) for index in (1, 2, 3)
    }
    assert set(suite_files.pack(costs).values()) <= {1, 2, 3, 4}
    printed = capsys.readouterr().out
    assert "3 recorded files packed into 4 shards" in printed
    assert all(f"shard {index}/4:" in printed for index in (1, 2, 3, 4))
    # Two of the three reports are refused whatever count is asked for.
    assert (
        suite_files.main(["record", *paths[:2], "--shards", "2", "--output", str(output)]) == 2
    )
    assert "each shard exactly once" in capsys.readouterr().err


def test_record_combines_complete_sharded_cohorts() -> None:
    reports = [
        _shard_report(1, run="1", seconds=2.0),
        _shard_report(2, run="1", seconds=8.0),
        _shard_report(1, run="2", seconds=8.0),
        _shard_report(2, run="2", seconds=2.0),
    ]
    document = suite_files.record(reports, shards=2)
    assert document["files"] == {
        "packing/tests/test_1.py": 4.0,
        "packing/tests/test_2.py": 4.0,
    }
    assert len(document["recorded_from"]) == 4


def test_record_refuses_an_incomplete_second_sharded_cohort() -> None:
    reports = [_shard_report(1), _shard_report(2), _shard_report(1, run="2", sha="def")]
    with pytest.raises(SuiteFilesError, match="each sharded cohort"):
        suite_files.record(reports, shards=2)


def test_record_refuses_complete_cohorts_from_different_source_revisions() -> None:
    reports = [
        _shard_report(1, run="1", sha="abc"),
        _shard_report(2, run="1", sha="abc"),
        _shard_report(1, run="2", sha="def"),
        _shard_report(2, run="2", sha="def"),
    ]
    with pytest.raises(SuiteFilesError, match="one GITHUB_SHA"):
        suite_files.record(reports, shards=2)


def test_record_refuses_unsuccessful_or_legacy_reports() -> None:
    unsuccessful = _shard_report(1, exit_status=int(pytest.ExitCode.TESTS_FAILED))
    with pytest.raises(SuiteFilesError, match="not successful"):
        suite_files.record([unsuccessful, _shard_report(2)], shards=2)

    legacy = _shard_report(1)
    del legacy["exit_status"]
    with pytest.raises(SuiteFilesError, match="exit_status"):
        suite_files.record([legacy, _shard_report(2)], shards=2)


def test_record_refuses_malformed_file_rows_and_totals() -> None:
    duplicate = _shard_report(1)
    duplicate["files"] = [*duplicate["files"], *duplicate["files"]]  # type: ignore[index]
    duplicate["tests"] = 2
    duplicate["seconds"] = 2.0
    with pytest.raises(SuiteFilesError, match="duplicate file"):
        suite_files.record([duplicate, _shard_report(2)], shards=2)

    invalid_seconds = _shard_report(1)
    invalid_seconds["files"][0]["seconds"] = -1.0  # type: ignore[index]
    with pytest.raises(SuiteFilesError, match="not finite seconds"):
        suite_files.record([invalid_seconds, _shard_report(2)], shards=2)

    wrong_total = _shard_report(1)
    wrong_total["tests"] = 2
    with pytest.raises(SuiteFilesError, match="rows total"):
        suite_files.record([wrong_total, _shard_report(2)], shards=2)


def test_record_refuses_overlapping_shards_and_inconsistent_cohort_coverage() -> None:
    overlap = [
        _shard_report(1, file="packing/tests/test_shared.py"),
        _shard_report(2, file="packing/tests/test_shared.py"),
    ]
    with pytest.raises(SuiteFilesError, match="more than one shard"):
        suite_files.record(overlap, shards=2)

    inconsistent = [
        _shard_report(1),
        _shard_report(2),
        _shard_report(1, run="2"),
        _shard_report(2, run="2", file="packing/tests/test_3.py"),
    ]
    with pytest.raises(SuiteFilesError, match="same file coverage"):
        suite_files.record(inconsistent, shards=2)


def test_record_refuses_mixed_whole_lane_and_sharded_reports() -> None:
    whole = suite_files.report_document(
        {"packing/tests/test_whole.py": (1, 1.0)},
        shard=None,
        environment={},
        exit_status=0,
    )
    with pytest.raises(SuiteFilesError, match="cannot mix"):
        suite_files.record([whole, _shard_report(1)], shards=2)


def test_unrecorded_files_are_counted_in_the_shard_their_hash_gives_them() -> None:
    """Per shard: what it is assigned, and the part of that the packing never weighed."""
    costs = RecordedCosts(shards=2, seconds={"a.py": 9.0, "b.py": 5.0, "c.py": 4.0})
    assert suite_files.pack(costs) == {"a.py": 1, "b.py": 2, "c.py": 2}
    # `c.py` is recorded and no longer on disk: a stale row is not a file in any shard.
    files = ["a.py", "b.py", "d.py", "e.py", "f.py", "g.py", "h.py"]
    assert [suite_files.unrecorded_shard(name, 2) for name in files[2:]] == [1, 2, 2, 1, 1]
    assert suite_files.unrecorded_by_shard(costs, files) == [(4, 3), (3, 2)]
    assert suite_files.unrecorded_by_shard(costs, files, suite_files.pack(costs)) == [
        (4, 3),
        (3, 2),
    ]
    assert suite_files.unrecorded_by_shard(costs, ["a.py", "b.py", "c.py"]) == [(1, 0), (2, 0)]
    assert suite_files.unrecorded_by_shard(costs, []) == [(0, 0), (0, 0)]


def test_explicit_unknown_owners_keep_unknown_costs_and_recorded_weights_take_precedence() -> (
    None
):
    names = tuple(suite_files.UNKNOWN_FOUR_SHARD_OWNERS)
    unknown = RecordedCosts(shards=4, seconds={})
    assert [suite_files.shard_of(name, unknown) for name in names] == [3, 1, 3]
    assert suite_files.shard_totals(unknown) == [0, 0, 0, 0]
    assert sum(row[1] for row in suite_files.unrecorded_by_shard(unknown, names)) == 3
    assert sum(row[0] for row in suite_files.unrecorded_by_shard(unknown, names)) == 3
    # A hosted cost, once recorded, owns the assignment instead of the unknown overlay.
    recorded = RecordedCosts(shards=4, seconds={names[0]: 1.0})
    assert suite_files.shard_of(names[0], recorded) == suite_files.pack(recorded)[names[0]]
    assert suite_files.shard_of(names[0], recorded) == 1
    assert sum(row[1] for row in suite_files.unrecorded_by_shard(recorded, names)) == 2
    # Other shard topologies retain their existing hash assignment and all coverage.
    for count in (2, 3, 5):
        for name in names:
            assert (
                suite_files.unrecorded_shard(name, count)
                == suite_files.zlib.crc32(name.encode("utf-8")) % count + 1
            )


def test_the_unrecorded_share_warns_above_its_threshold_and_not_at_it() -> None:
    record = Path("devtools/suite-file-costs.json")
    message = suite_files.unrecorded_share_warning(
        Shard(1, 2), 4, 3, threshold=suite_files.UNRECORDED_SHARE_WARNING, record=record
    )
    assert message is not None
    assert message.startswith(
        "suite shard 1/2: 3 of the 4 test files it is assigned (75.0%) are not named in "
        "suite-file-costs.json, over the 10% threshold."
    )
    assert "`python -m devtools.suite_files record REPORT.json ...`" in message
    assert "\n" not in message
    for assigned, unrecorded in ((10, 1), (10, 0), (0, 0)):
        assert (
            suite_files.unrecorded_share_warning(
                Shard(1, 2), assigned, unrecorded, threshold=0.10, record=record
            )
            is None
        )
    assert suite_files.unrecorded_share_warning(
        Shard(2, 2), 10, 2, threshold=0.10, record=record
    )
    assert (
        suite_files.unrecorded_share_warning(Shard(2, 2), 4, 4, threshold=1.0, record=record)
        is None
    )


def test_check_prices_every_shard_and_fails_only_over_the_threshold(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Twelve files the record has never seen: every one is unrecorded wherever it hashes."""
    lane = tmp_path / "lane"
    names = [f"sub/test_arrival_{index}.py" for index in range(11)]
    for name in names:
        (lane / name).parent.mkdir(parents=True, exist_ok=True)
        (lane / name).write_text("", encoding="utf-8")
    # Neither a helper beside the tests nor a stale cache entry is a test file.
    (lane / "sub/helper.py").write_text("", encoding="utf-8")
    (lane / "__pycache__").mkdir()
    (lane / "__pycache__/test_cached.py").write_text("", encoding="utf-8")
    # A root that is a file counts as itself.
    alone = tmp_path / "test_alone.py"
    alone.write_text("", encoding="utf-8")
    arguments = ["check", "--root", str(lane), str(alone)]
    files = [suite_files.repository_path(path) for path in (*(lane / n for n in names), alone)]
    assert suite_files.lane_files([lane, alone]) == sorted(files)

    costs = suite_files.load_costs()
    rows = suite_files.unrecorded_by_shard(costs, files)
    assert sum(assigned for assigned, _unrecorded in rows) == 12
    assert all(assigned == unrecorded for assigned, unrecorded in rows)

    assert suite_files.main(arguments) == 1
    printed = capsys.readouterr().out
    assert (
        "12 test files, 12 not named in the record; a shard may be 10% unrecorded:" in printed
    )
    for index, (assigned, unrecorded) in enumerate(rows, start=1):
        share = "100.0%" if assigned else " 0.0%"
        line = (
            f"  shard {index}/{costs.shards}: {assigned:4d} files, {unrecorded:3d} unrecorded "
            f"({share})" + (" -- over the threshold" if assigned else "")
        )
        assert line in printed.splitlines()
    assert all(f"      {name}" in printed.splitlines() for name in files)
    assert "helper.py" not in printed
    assert "test_cached.py" not in printed
    assert "`python -m devtools.suite_files record REPORT.json ...`" in printed

    assert suite_files.main([*arguments, "--max-unrecorded-share", "1"]) == 0
    printed = capsys.readouterr().out
    assert (
        "12 test files, 12 not named in the record; a shard may be 100% unrecorded:" in printed
    )
    assert all(f"      {name}" in printed.splitlines() for name in files)
    assert "over the threshold" not in printed

    assert suite_files.main([*arguments, "--max-unrecorded-share", "1.5"]) == 2
    assert "a fraction from 0 to 1" in capsys.readouterr().err


def test_check_passes_on_the_real_tree(capsys: pytest.CaptureFixture[str]) -> None:
    """The record names the lane: no shard of the real tree is over the threshold.

    The files a quick-lane report can never name -- those whose tests are all `slow` or
    `exhaustive_exact`, and the one the lane ignores -- stay unrecorded after any rebuild.
    They were 10 of 499 on 2026-10-01, at most 3.4 per cent of a shard. A failure here says
    enough new test files have landed since the record was made that some shard's cost is
    no longer the one it balanced, and the remedy is the one the output names.
    """
    assert suite_files.main(["check"]) == 0, capsys.readouterr().out
    printed = capsys.readouterr().out
    costs = suite_files.load_costs()
    assert f"{len(_test_files())} test files, " in printed
    rows = suite_files.unrecorded_by_shard(costs, _test_files())
    assert all(assigned for assigned, _unrecorded in rows)
    for index, (assigned, unrecorded) in enumerate(rows, start=1):
        assert unrecorded / assigned <= suite_files.UNRECORDED_SHARE_WARNING
        assert f"  shard {index}/{costs.shards}: {assigned:4d} files," in printed


_PROBE_FILES = {
    "test_alpha.py": "def test_one():\n    pass\n\ndef test_two():\n    pass\n",
    "test_beta.py": "def test_one():\n    pass\n",
    "test_gamma.py": "import time\n\ndef test_sleeps():\n    time.sleep(0.05)\n",
    "test_delta.py": "def test_one():\n    pass\n",
    "sub/test_epsilon.py": "def test_one():\n    pass\n",
}


def _probe(
    tmp_path: Path,
    *arguments: str,
    rootdir: Path | None = None,
    test_root: Path | None = None,
) -> subprocess.Popen[str]:
    """Start one pytest run under the plugin; the runs below overlap to stay cheap."""
    rootdir = tmp_path if rootdir is None else rootdir
    test_root = tmp_path / "suite" if test_root is None else test_root
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "-p",
            "devtools.suite_files",
            "--rootdir",
            str(rootdir),
            "-c",
            os.devnull,
            str(test_root),
            *arguments,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=PROJECT_ROOT,
        env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
    )


def _finish(process: subprocess.Popen[str]) -> tuple[int, str]:
    output, _ = process.communicate(timeout=60)
    return process.returncode, output


def test_the_plugin_collects_each_file_in_exactly_one_shard_and_reports_its_cost(
    tmp_path: Path,
) -> None:
    """End to end through pytest: collection filtered per shard, and the report written.

    Two of the five files are recorded, so the run exercises both rules at once: the
    packing for recorded files and the path hash for the rest. Three unrecorded files in
    two shards also put at least one shard over the unrecorded-share threshold, whichever
    way the hash sends them: that shard has to say so and still pass, and the same shard
    run with the threshold raised to 1 has to say nothing.
    """
    suite = tmp_path / "suite"
    for name, body in _PROBE_FILES.items():
        (suite / name).parent.mkdir(parents=True, exist_ok=True)
        (suite / name).write_text(body, encoding="utf-8")
    record = tmp_path / "costs.json"
    alpha = suite_files.repository_path(suite / "test_alpha.py")
    gamma = suite_files.repository_path(suite / "test_gamma.py")
    record.write_text(
        json.dumps(
            {
                "schema": suite_files.COSTS_SCHEMA,
                "shards": 2,
                "files": {alpha: 10.0, gamma: 9.0},
            }
        ),
        encoding="utf-8",
    )
    reports = [tmp_path / f"report-{index}.json" for index in (1, 2)]
    runs = [
        _probe(
            tmp_path,
            f"--suite-shard={index}/2",
            f"--suite-file-costs={record}",
            f"--test-file-costs={report}",
        )
        for index, report in zip((1, 2), reports, strict=True)
    ]
    refused = _probe(tmp_path, "--suite-shard=1/3", f"--suite-file-costs={record}")
    everything = {suite_files.repository_path(suite / name) for name in _PROBE_FILES}
    shares = suite_files.unrecorded_by_shard(suite_files.load_costs(record), everything)
    assert [unrecorded for _assigned, unrecorded in shares] in ([0, 3], [1, 2], [2, 1], [3, 0])
    loudest = max((1, 2), key=lambda index: shares[index - 1][1])
    silenced = _probe(
        tmp_path,
        f"--suite-shard={loudest}/2",
        f"--suite-file-costs={record}",
        "--suite-unrecorded-share=1",
    )
    collected: list[set[str]] = []
    warned: list[int] = []
    for index, (run, report) in enumerate(zip(runs, reports, strict=True), start=1):
        status, output = _finish(run)
        # A warning, never a failure: the lane keeps running when files land.
        assert status == 0, output
        document = json.loads(report.read_text(encoding="utf-8"))
        assert document["schema"] == suite_files.REPORT_SCHEMA
        assert document["shard"] == f"{index}/2"
        assert document["exit_status"] == 0
        collected.append({row["file"] for row in document["files"]})
        for row in document["files"]:
            assert set(row) == {"file", "tests", "seconds"}
        assigned, unrecorded = shares[index - 1]
        assert len(collected[-1]) == assigned
        if unrecorded / assigned > suite_files.UNRECORDED_SHARE_WARNING:
            warned.append(index)
            assert "PytestConfigWarning" in output, output
            assert (
                f"suite shard {index}/2: {unrecorded} of the {assigned} test files it is "
                f"assigned ({unrecorded / assigned:.1%}) are not named in costs.json, over "
                "the 10% threshold"
            ) in output, output
            assert "`python -m devtools.suite_files record REPORT.json ...`" in output
        else:
            assert "not named in" not in output, output
    assert loudest in warned
    assert collected[0] | collected[1] == everything
    assert not collected[0] & collected[1]
    # The two recorded files pack into different shards, longest first.
    assert alpha in collected[0]
    assert gamma in collected[1]

    status, output = _finish(refused)
    assert status != 0
    assert "re-record" in output

    status, output = _finish(silenced)
    assert status == 0, output
    assert "not named in" not in output, output
    assert "PytestConfigWarning" not in output, output


def test_the_report_uses_the_actual_location_for_a_test_outside_rootdir(tmp_path: Path) -> None:
    rootdir = tmp_path / "root"
    rootdir.mkdir()
    external = tmp_path / "external/test_external.py"
    external.parent.mkdir()
    external.write_text("def test_external():\n    pass\n", encoding="utf-8")
    report = tmp_path / "external-report.json"

    run = _probe(
        tmp_path,
        f"--test-file-costs={report}",
        rootdir=rootdir,
        test_root=external,
    )
    status, output = _finish(run)

    assert status == 0, output
    document = json.loads(report.read_text(encoding="utf-8"))
    assert document["exit_status"] == 0
    assert [row["file"] for row in document["files"]] == [suite_files.repository_path(external)]


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (["--suite-a", "--suite-b"], "ten parts"),
        (["--checks", "--typecheck"], "ten parts"),
    ],
)
def test_the_cli_refuses_more_than_one_public_fast_part(
    arguments: list[str], message: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert validate.main([*arguments, "--list"]) == 2
    assert message in capsys.readouterr().err
