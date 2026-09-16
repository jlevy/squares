"""The quick behavioural lane by test file: a stable shard partition and a cost report.

A pytest plugin with two options, and a small command that records the costs the first
one partitions on. Both exist because the lane outgrew one runner by accretion rather
than by any one test: on 2026-09-15 the pull request's `suite` job took 300 s on the
workbench stack and 284 s on PRs into `main`, over 6,095 and 5,664 tests, with no test
above the per-test ceiling and four red runs in a day with every test passing. Nothing
said which files the growth came from when it landed, and no worker count on a four-cpu
runner divides 870 test-seconds under that job's ceiling.

`--suite-shard K/N` collects only the test files the partition assigns to shard K. The
partition is a function of a file's repository-relative path and nothing else, so every
file lands in exactly one shard by construction:

* a file named in `suite-file-costs.json` takes the shard a greedy longest-first packing
  of the recorded costs gives it. The packing reads only the record, so it moves when
  someone re-records and never because a file elsewhere was added or removed;
* a file the record does not name -- a new test, or a renamed one -- takes
  `crc32(path) mod N`. That is stable across runs and machines, needs no edit to land,
  and spreads new files as a uniform hash does rather than piling them on one side.

The filter runs in `pytest_ignore_collect`, before a module is imported, so each shard
pays for collecting its own half rather than all of it; the CI audit measured collection
at 10-16 s per process, most of the lane's fixed cost.

`--test-file-costs PATH` writes one JSON document per run: for every test file that
reported, its repository-relative path, how many tests it ran, and the sum of their
setup, call and teardown seconds -- the quantity a junit `time` attribute carries.
`sqpack.cli.validate` asks for it beside the junit file in the gate's timing artifact, so
growth in the lane is priced by file on the run that introduced it. Under xdist the
controller receives every worker's reports, and only the controller writes.

Record the partition's costs from those reports, never by hand:

    uv run --frozen --all-extras --group dev python -m devtools.suite_files record \\
        REPORT.json [REPORT.json ...]
    uv run --frozen --all-extras --group dev python -m devtools.suite_files show
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import zlib
from collections import defaultdict
from dataclasses import dataclass
from fnmatch import fnmatch
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Any, Final

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
#: The recorded per-file costs the partition packs, keyed by repository-relative path.
COSTS = Path(__file__).with_name("suite-file-costs.json")
COSTS_SCHEMA: Final = "packing.squares:SuiteFileCosts/1"
REPORT_SCHEMA: Final = "packing.squares:TestFileCosts/1"
#: The GitHub environment a report carries, so a record can name the runs it came from.
_PROVENANCE_ENVIRONMENT: Final = (
    "GITHUB_RUN_ID",
    "GITHUB_RUN_ATTEMPT",
    "GITHUB_JOB",
    "GITHUB_SHA",
)


class SuiteFilesError(ValueError):
    """A shard, a record, or a report that cannot be read as declared."""


@dataclass(frozen=True)
class Shard:
    """Shard `index` of `count`, one-based as it is written on a command line."""

    index: int
    count: int

    @classmethod
    def parse(cls, text: str) -> Shard:
        head, separator, tail = text.partition("/")
        if not separator or not head.isdigit() or not tail.isdigit():
            raise SuiteFilesError(f"a shard is written K/N, not {text!r}")
        shard = cls(int(head), int(tail))
        if not 1 <= shard.index <= shard.count:
            raise SuiteFilesError(f"shard {text!r} is not one of 1/{tail} .. {tail}/{tail}")
        return shard

    def __str__(self) -> str:
        return f"{self.index}/{self.count}"


@dataclass(frozen=True)
class RecordedCosts:
    """Seconds per repository-relative test file, and the shard count they pack into."""

    shards: int
    seconds: Mapping[str, float]
    recorded_from: tuple[str, ...] = ()


def load_costs(path: Path = COSTS) -> RecordedCosts:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SuiteFilesError(f"{path}: {error}") from error
    if not isinstance(document, dict) or document.get("schema") != COSTS_SCHEMA:
        raise SuiteFilesError(f"{path} is not a {COSTS_SCHEMA} document")
    shards = document.get("shards")
    files = document.get("files")
    if not isinstance(shards, int) or shards < 1 or not isinstance(files, dict):
        raise SuiteFilesError(f"{path} needs a positive `shards` and a `files` mapping")
    seconds: dict[str, float] = {}
    for name, value in files.items():
        if not isinstance(value, int | float) or value < 0 or not math.isfinite(value):
            raise SuiteFilesError(f"{path}: {name} records {value!r}, not seconds")
        seconds[str(name)] = float(value)
    sources = document.get("recorded_from", [])
    return RecordedCosts(
        shards=shards,
        seconds=seconds,
        recorded_from=tuple(str(source) for source in sources),
    )


def pack(costs: RecordedCosts) -> dict[str, int]:
    """The recorded files' shards: longest first, each into the lightest shard so far.

    Ties break on path and then on the lower shard, so the answer depends on the record's
    contents and on nothing about the order it was read in.
    """
    totals = [0.0] * costs.shards
    assigned: dict[str, int] = {}
    for name, seconds in sorted(costs.seconds.items(), key=lambda item: (-item[1], item[0])):
        lightest = min(range(costs.shards), key=lambda shard: (totals[shard], shard))
        totals[lightest] += seconds
        assigned[name] = lightest + 1
    return assigned


def unrecorded_shard(path: str, count: int) -> int:
    return zlib.crc32(path.encode("utf-8")) % count + 1


def shard_of(path: str, costs: RecordedCosts, packed: Mapping[str, int] | None = None) -> int:
    """The one shard `path` belongs to, recorded or not."""
    assignments = pack(costs) if packed is None else packed
    recorded = assignments.get(path)
    return recorded if recorded is not None else unrecorded_shard(path, costs.shards)


def shard_totals(costs: RecordedCosts) -> list[float]:
    """Recorded seconds per shard, in shard order."""
    totals = [0.0] * costs.shards
    for name, shard in pack(costs).items():
        totals[shard - 1] += costs.seconds[name]
    return totals


def repository_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO).as_posix()
    except ValueError:
        return resolved.as_posix()


@cache
def _packed(path: Path) -> tuple[RecordedCosts, dict[str, int]]:
    costs = load_costs(path)
    return costs, pack(costs)


# --- the pytest plugin -------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("suite files")
    _ = group.addoption(
        "--suite-shard",
        action="store",
        default=None,
        metavar="K/N",
        help="collect only the test files the recorded partition assigns to shard K of N",
    )
    _ = group.addoption(
        "--suite-file-costs",
        action="store",
        default=str(COSTS),
        metavar="PATH",
        help="the recorded per-file costs the shard partition packs",
    )
    _ = group.addoption(
        "--test-file-costs",
        action="store",
        default=None,
        metavar="PATH",
        help="write each test file's test count and setup+call+teardown seconds as JSON",
    )


_SHARD: Final = pytest.StashKey[Shard | None]()


def _costs_option(config: pytest.Config) -> Path:
    return Path(str(config.getoption("--suite-file-costs"))).resolve()


def pytest_configure(config: pytest.Config) -> None:
    option = config.getoption("--suite-shard", default=None)
    try:
        shard = None if option is None else Shard.parse(str(option))
        costs = None if shard is None else _packed(_costs_option(config))[0]
    except SuiteFilesError as error:
        raise pytest.UsageError(str(error)) from error
    if shard is not None and costs is not None and costs.shards != shard.count:
        raise pytest.UsageError(
            f"--suite-shard {shard} asks for {shard.count} shards, but the recorded "
            f"partition packs {costs.shards}; re-record it with `python -m "
            "devtools.suite_files record` rather than dividing a record made for another "
            "count"
        )
    config.stash[_SHARD] = shard
    target = config.getoption("--test-file-costs", default=None)
    if target is not None and not hasattr(config, "workerinput"):
        config.pluginmanager.register(FileCostReport(Path(str(target)), shard), "file-costs")


def pytest_ignore_collect(collection_path: Path, config: pytest.Config) -> bool | None:
    """Leave out a test module another shard owns, and say nothing about anything else.

    `None` rather than `False` for a kept path: `False` would override every other
    plugin's and every conftest's decision to ignore it.
    """
    shard = config.stash.get(_SHARD, None)
    if shard is None or not collection_path.is_file():
        return None
    patterns = [str(pattern) for pattern in config.getini("python_files")]
    if not any(fnmatch(collection_path.name, pattern) for pattern in patterns):
        return None
    costs, packed = _packed(_costs_option(config))
    if shard_of(repository_path(collection_path), costs, packed) == shard.index:
        return None
    return True


class FileCostReport:
    """Sums each file's phase durations on the controller and writes them at the end."""

    def __init__(self, target: Path, shard: Shard | None) -> None:
        self.target = target
        self.shard = shard
        self.seconds: defaultdict[str, float] = defaultdict(float)
        self.tests: defaultdict[str, set[str]] = defaultdict(set)
        self.rootpath = Path.cwd()

    def pytest_sessionstart(self, session: pytest.Session) -> None:
        self.rootpath = session.config.rootpath

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when not in {"setup", "call", "teardown"}:
            return
        name = repository_path(self.rootpath / report.nodeid.split("::", 1)[0])
        self.seconds[name] += report.duration
        self.tests[name].add(report.nodeid)

    def pytest_sessionfinish(self) -> None:
        document = report_document(
            {name: (len(self.tests[name]), seconds) for name, seconds in self.seconds.items()},
            shard=self.shard,
            environment=os.environ,
        )
        self.target.parent.mkdir(parents=True, exist_ok=True)
        self.target.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def report_document(
    files: Mapping[str, tuple[int, float]],
    *,
    shard: Shard | None,
    environment: Mapping[str, str],
) -> dict[str, Any]:
    """The report's one shape: `files` is a list of `{file, tests, seconds}` rows."""
    rows = [
        {"file": name, "tests": tests, "seconds": round(seconds, 3)}
        for name, (tests, seconds) in sorted(files.items())
    ]
    return {
        "schema": REPORT_SCHEMA,
        "shard": None if shard is None else str(shard),
        "provenance": {
            key: environment[key] for key in _PROVENANCE_ENVIRONMENT if key in environment
        },
        "tests": sum(int(row["tests"]) for row in rows),
        "seconds": round(sum(float(row["seconds"]) for row in rows), 3),
        "files": rows,
    }


# --- recording ---------------------------------------------------------------------


def read_report(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SuiteFilesError(f"{path}: {error}") from error
    if not isinstance(document, dict) or document.get("schema") != REPORT_SCHEMA:
        raise SuiteFilesError(f"{path} is not a {REPORT_SCHEMA} report")
    return document


def record(reports: Iterable[Mapping[str, Any]], *, shards: int) -> dict[str, Any]:
    """Combine reports into a record: each file's geometric mean over the reports naming it.

    A geometric mean because hosted runners differ by a factor rather than an offset --
    the audit measured a 1.8x spread applied evenly across files -- so the record is the
    centre of that spread rather than whichever runner drew last. A file that reported no
    time at all is recorded at zero and packs last.
    """
    observed: defaultdict[str, list[float]] = defaultdict(list)
    sources: list[str] = []
    for report in reports:
        provenance = report.get("provenance") or {}
        label = ", ".join(f"{key}={value}" for key, value in sorted(provenance.items()))
        part = f"shard {report['shard']}" if report.get("shard") else "the whole lane"
        sources.append(f"{part}: {label or 'no CI provenance'}")
        for row in report["files"]:
            observed[str(row["file"])].append(float(row["seconds"]))
    files = {
        name: round(math.exp(sum(math.log(value) for value in values) / len(values)), 3)
        if all(value > 0 for value in values)
        else 0.0
        for name, values in sorted(observed.items())
    }
    return {"schema": COSTS_SCHEMA, "shards": shards, "recorded_from": sources, "files": files}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m devtools.suite_files",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    recording = commands.add_parser("record", help="write the record from cost reports")
    _ = recording.add_argument("reports", nargs="+", type=Path)
    _ = recording.add_argument("--shards", type=int, default=None)
    _ = recording.add_argument("--output", type=Path, default=COSTS)
    _ = commands.add_parser("show", help="print the recorded partition's shard totals")
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "record":
            shards = int(arguments.shards or load_costs().shards)
            document = record([read_report(path) for path in arguments.reports], shards=shards)
            output = Path(arguments.output)
            _ = output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
            costs = load_costs(output)
        else:
            costs = load_costs()
    except SuiteFilesError as error:
        print(f"suite_files: error: {error}", file=sys.stderr)
        return 2
    print(f"{len(costs.seconds)} recorded files packed into {costs.shards} shards:")
    for index, total in enumerate(shard_totals(costs), start=1):
        print(f"  shard {index}/{costs.shards}: {total:8.2f}s recorded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
