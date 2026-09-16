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


def _test_files() -> set[str]:
    """Every file pytest would collect as a test module under `tests`, repository-relative."""
    return {
        suite_files.repository_path(path)
        for path in (PROJECT_ROOT / "tests").rglob("test_*.py")
        if "__pycache__" not in path.parts
    }


def test_the_suite_shards_partition_every_test_file() -> None:
    """Each test file on disk is in exactly one shard, and every shard has files.

    This is the property that lets two runners divide the lane without a test running
    twice or not at all. It holds by construction -- a file's shard is a function of its
    path -- so what this checks is the construction against the real tree and the real
    record: that the recorded count is the one the CLI and the register use, and that
    the files each shard would collect are disjoint and add up to the whole lane.
    """
    costs = suite_files.load_costs()
    assert costs.shards == validate.SUITE_SHARDS
    packed = suite_files.pack(costs)
    files = _test_files()
    shards = [
        {name for name in files if suite_files.shard_of(name, costs, packed) == index}
        for index in range(1, costs.shards + 1)
    ]
    assert set().union(*shards) == files
    assert sum(len(shard) for shard in shards) == len(files)
    assert all(shards)


def test_the_packing_depends_only_on_the_record() -> None:
    """The same record in any order packs the same way, and a new file moves nothing."""
    costs = suite_files.load_costs()
    items = list(costs.seconds.items())
    random.Random(20260915).shuffle(items)
    shuffled = RecordedCosts(shards=costs.shards, seconds=dict(items))
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


@pytest.mark.parametrize("text", ["2", "0/2", "3/2", "a/b", "1/"])
def test_a_shard_is_written_k_of_n(text: str) -> None:
    with pytest.raises(SuiteFilesError):
        _ = Shard.parse(text)
    assert str(Shard.parse("2/2")) == "2/2"


def test_record_takes_each_files_geometric_mean_and_names_its_sources() -> None:
    reports = [
        suite_files.report_document(
            {"packing/tests/test_a.py": (3, 2.0), "packing/tests/test_b.py": (1, 0.0)},
            shard=Shard(1, 2),
            environment={"GITHUB_RUN_ID": "1", "GITHUB_JOB": "suite-1-of-2"},
        ),
        suite_files.report_document(
            {"packing/tests/test_a.py": (3, 8.0), "packing/tests/test_c.py": (2, 1.5)},
            shard=Shard(2, 2),
            environment={},
        ),
    ]
    document = suite_files.record(reports, shards=2)
    assert document["files"] == {
        "packing/tests/test_a.py": 4.0,
        "packing/tests/test_b.py": 0.0,
        "packing/tests/test_c.py": 1.5,
    }
    assert document["recorded_from"] == [
        "shard 1/2: GITHUB_JOB=suite-1-of-2, GITHUB_RUN_ID=1",
        "shard 2/2: no CI provenance",
    ]
    assert reports[0]["tests"] == 4
    assert reports[0]["seconds"] == 2.0


_PROBE_FILES = {
    "test_alpha.py": "def test_one():\n    pass\n\ndef test_two():\n    pass\n",
    "test_beta.py": "def test_one():\n    pass\n",
    "test_gamma.py": "import time\n\ndef test_sleeps():\n    time.sleep(0.05)\n",
    "test_delta.py": "def test_one():\n    pass\n",
    "sub/test_epsilon.py": "def test_one():\n    pass\n",
}


def _probe(tmp_path: Path, *arguments: str) -> subprocess.Popen[str]:
    """Start one pytest run under the plugin; the three runs below overlap to stay cheap."""
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
            str(tmp_path),
            "-c",
            os.devnull,
            str(tmp_path / "suite"),
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
    packing for recorded files and the path hash for the rest.
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
    collected: list[set[str]] = []
    for index, (run, report) in enumerate(zip(runs, reports, strict=True), start=1):
        status, output = _finish(run)
        assert status == 0, output
        document = json.loads(report.read_text(encoding="utf-8"))
        assert document["schema"] == suite_files.REPORT_SCHEMA
        assert document["shard"] == f"{index}/2"
        collected.append({row["file"] for row in document["files"]})
        for row in document["files"]:
            assert set(row) == {"file", "tests", "seconds"}
    everything = {suite_files.repository_path(suite / name) for name in _PROBE_FILES}
    assert collected[0] | collected[1] == everything
    assert not collected[0] & collected[1]
    # The two recorded files pack into different shards, longest first.
    assert alpha in collected[0]
    assert gamma in collected[1]

    status, output = _finish(refused)
    assert status != 0
    assert "re-record" in output


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (["--shard", "1/2"], "use it with --suite"),
        (["--suite", "--shard", "3/3"], "is not one of"),
        (["--suite", "--shard", "1/2", "--only", "fast"], "takes no --only"),
        (["--checks", "--typecheck"], "five parts"),
    ],
)
def test_the_cli_refuses_a_shard_it_has_no_ceiling_for(
    arguments: list[str], message: str, capsys: pytest.CaptureFixture[str]
) -> None:
    assert validate.main([*arguments, "--list"]) == 2
    assert message in capsys.readouterr().err
