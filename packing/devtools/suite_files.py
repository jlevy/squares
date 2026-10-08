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
  of the recorded costs gives it. The record's `target_ceiling_seconds` are historical
  planning capacities for this measured assignment, separate from the gate's live
  enforcement ceilings. Packing balances cost divided by those capacities; a generic
  record without them balances raw cost. The packing reads only the record, so it moves
  when someone re-records and never because a file elsewhere was added or removed;
* a file the record does not name -- a new test, or a renamed one -- takes
  `crc32(path) mod N`, except for the explicit four-shard unknown owners below.
  These owners balance unknown file counts, carry no cost weight, and are superseded
  when a complete hosted cohort records the file. Every file remains in one shard.

The filter runs in `pytest_ignore_collect`, before a module is imported, so each shard
pays for collecting only its assigned files. The CI audit measured collection at 10-16 s
per process, most of the lane's fixed cost.

`--test-file-costs PATH` writes one JSON document per run: for every test file that
reported, its repository-relative path, how many tests it ran, and the sum of their
setup, call and teardown seconds -- the quantity a junit `time` attribute carries.
`sqpack.cli.validate` asks for it beside the junit file in the gate's timing artifact, so
growth in the lane is priced by file on the run that introduced it. Under xdist the
controller receives every worker's reports, and only the controller writes.

Record the partition's costs from those reports, never by hand. Each hosted cohort must
include all of its shards, and every cohort passed must have been cut at one shard count.
That count need not be the one the record packs: the costs are per file, so a cohort
recorded at N shards may be packed into M with `--shards M`, which is how the lane is
repartitioned without editing the record. Passing several complete cohorts makes the
record use each file's geometric mean across them rather than chase one runner's
assignment:

    uv run --frozen --all-extras --group dev python -m devtools.suite_files record \\
        [--shards M] [--target-ceilings SECONDS,...] REPORT.json [REPORT.json ...]
    uv run --frozen --all-extras --group dev python -m devtools.suite_files show
    uv run --frozen --all-extras --group dev python -m devtools.suite_files check

For newly added modules, `admit-local REPORT.json ... --files PATH ...` adds only
their measured costs to the existing record. Reports must come from successful,
unsharded, unfiltered runs of exactly those whole modules. Keep the raw reports beside
the record's admission provenance. This local subset is recorded separately from the
historical hosted cohorts; their weights, sources and planning capacities are preserved.

A file the record does not name carries no weight in the packing, so when many land the
partition is unbalanced and nothing says so. A sharded run therefore warns when more than
`UNRECORDED_SHARE_WARNING` of the test files its shard is assigned are unrecorded. It
warns rather than fails, because the lane has to keep running when files land. `check`
prints the same count for every shard beside the unrecorded file names, and exits 1 when
any shard is over the threshold. The count is of files under the roots the run was given
and takes no account of `-m` or `--ignore`, so a record that is sparse by design is over
it always: the exhaustive lane's names only the files that carry an `exhaustive_exact`
test. `--suite-unrecorded-share=1` turns the warning off for such a run.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import zlib
from collections import defaultdict
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass
from fnmatch import fnmatch
from functools import cache
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any, Final

import pytest
from strif import atomic_write_text

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
#: The recorded per-file costs the partition packs, keyed by repository-relative path.
COSTS = Path(__file__).with_name("suite-file-costs.json")
#: The two behavioural test roots the quick lane collects, which `check` walks by default.
DEFAULT_ROOTS: Final = (ROOT / "tests", REPO / "packages/workbench/tests")
COSTS_SCHEMA: Final = "packing.squares:SuiteFileCosts/1"
REPORT_SCHEMA: Final = "packing.squares:TestFileCosts/2"
#: The share of a shard's assigned test files the record may leave unnamed before a
#: sharded run warns and `check` exits 1. An unrecorded file takes its owner or hash and no
#: weight in the packing, so above this share the shard's cost is no longer the one the
#: record balanced. A tenth leaves room for the files a quick-lane report can never name
#: -- those whose tests are all `slow` or `exhaustive_exact`, and the one the lane
#: ignores -- and for the new files that land between two recordings.
UNRECORDED_SHARE_WARNING: Final = 0.10
# 2026-10-07 real-tree check: 53/634 files had unknown costs, but hash imbalance
# assigned 17/151 (11.3%) to shard 4. These three scheduling-only owners give
# unknown counts 13/13/13/14 without inventing weights or changing the 10% guard.
# Only the four-shard topology uses them; recorded cohort weights take precedence.
# The two centered-standing controls explicitly keep their current hash owners.
# At 56/637 unknown files, the real tree has 14 unknown files in each shard; these
# controls retain unknown cost status until a complete hosted cohort records them.
# The conditional-hull file brought shard 4 to 15/149 (10.1%) at 57/638 overall.
# Giving only that new unknown file to shard 2 keeps counts 14/15/14/14 without weights.
UNKNOWN_FOUR_SHARD_OWNERS: Final = {
    "packing/tests/test_check_n17_capture_cap.py": 3,
    "packing/tests/test_check_n17_capture_leaf.py": 1,
    "packing/tests/test_check_n17_widened_positive_cone.py": 3,
    "packing/tests/test_check_n17_centered_cap_standing.py": 1,
    "packing/tests/test_verify_n17_centered_cap.py": 3,
    "packing/tests/test_probe_n17_conditional_owned_hull.py": 2,
    # 681 files / 66 unknown after two measured complete-module admissions:
    # 15/18/18/15 unknowns fit the unchanged 10% guard, with no assigned weights.
    "packing/tests/test_check_n17_regional_row_coverage.py": 2,
    "packing/tests/test_check_n17_n11_envelope_representation.py": 2,
    "packing/tests/test_check_n17_case_preserving_owned_propagation.py": 2,
    "packing/tests/test_check_n17_full_square_partner_coupling.py": 2,
    "packing/tests/test_check_n17_normalized_contact_rank_filter.py": 2,
    "packing/tests/test_check_n17_incircle_disk_projection.py": 3,
}
#: What a test file is called where no pytest configuration says otherwise.
_PYTHON_FILES: Final = ("test_*.py",)
#: The behavioural lane's configured file pattern and pytest's class/function defaults.
#: Alternate rules can hide tests before pytest emits any deselection event.
_LOCAL_COLLECTION_PATTERNS: Final = {
    "python_files": ["test_*.py"],
    "python_classes": ["Test"],
    "python_functions": ["test"],
}
_LOCAL_COLLECTION_CONTROLS: Final = {
    "ignore": [],
    "ignore_glob": [],
    "deselect": [],
    "confcutdir": None,
    "noconftest": False,
    "pyargs": False,
    "keepduplicates": False,
    "lf": False,
    "stepwise": False,
    "stepwise_skip": False,
    "setuponly": False,
    "setupplan": False,
    "collectonly": False,
}
#: The GitHub environment a report carries, so a record can name the runs it came from.
_PROVENANCE_ENVIRONMENT: Final = (
    "PACKING_VALIDATED_SHA",
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
    """Seconds per test file and optional historical shard planning capacities."""

    shards: int
    seconds: Mapping[str, float]
    recorded_from: tuple[str, ...] = ()
    target_ceiling_seconds: tuple[float, ...] | None = None


def _targets(targets: tuple[float, ...] | None, shards: int) -> tuple[float, ...]:
    """A valid capacity vector, with equal capacities for a generic record."""
    if targets is None:
        return (1.0,) * shards
    if len(targets) != shards or any(
        isinstance(x, bool) or not math.isfinite(x) or x <= 0 for x in targets
    ):
        raise SuiteFilesError("target ceilings must be positive finite seconds for every shard")
    return targets


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
    raw_targets = document.get("target_ceiling_seconds")
    if raw_targets is not None and (
        not isinstance(raw_targets, list)
        or any(
            isinstance(value, bool) or not isinstance(value, int | float)
            for value in raw_targets
        )
    ):
        raise SuiteFilesError(f"{path}: target ceilings must be a numeric list")
    targets = None if raw_targets is None else tuple(float(value) for value in raw_targets)
    _ = _targets(targets, shards)
    return RecordedCosts(
        shards=shards,
        seconds=seconds,
        recorded_from=tuple(str(source) for source in sources),
        target_ceiling_seconds=targets,
    )


def pack(costs: RecordedCosts) -> dict[str, int]:
    """The recorded files' shards: longest first, each into the least-loaded capacity.

    Ties break on path and then on the lower shard, so the answer depends on the record's
    contents and on nothing about the order it was read in.
    """
    targets = _targets(costs.target_ceiling_seconds, costs.shards)
    totals = [0.0] * costs.shards
    assigned: dict[str, int] = {}
    for name, seconds in sorted(costs.seconds.items(), key=lambda item: (-item[1], item[0])):
        lightest = min(
            range(costs.shards), key=lambda shard: (totals[shard] / targets[shard], shard)
        )
        totals[lightest] += seconds
        assigned[name] = lightest + 1
    return assigned


def unrecorded_shard(path: str, count: int) -> int:
    if count == 4 and path in UNKNOWN_FOUR_SHARD_OWNERS:
        return UNKNOWN_FOUR_SHARD_OWNERS[path]
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


def lane_files(roots: Iterable[Path], patterns: Sequence[str] = _PYTHON_FILES) -> list[str]:
    """The test files under `roots`, repository-relative: one walk, `__pycache__` pruned.

    A root that is itself a file counts as that file whatever it is called, since a run
    pointed at one module collects that module.
    """
    found: set[str] = set()
    for root in roots:
        if root.is_file():
            found.add(repository_path(root))
            continue
        for directory, names, files in os.walk(root):
            names[:] = [name for name in names if name != "__pycache__"]
            found.update(
                repository_path(Path(directory, name))
                for name in files
                if any(fnmatch(name, pattern) for pattern in patterns)
            )
    return sorted(found)


def unrecorded_by_shard(
    costs: RecordedCosts, files: Iterable[str], packed: Mapping[str, int] | None = None
) -> list[tuple[int, int]]:
    """Per shard, in order: the files assigned, and how many the record does not name.

    `files` are repository-relative paths. The second number is the part of the shard the
    packing never weighed: their scheduling owner or path hash assigns them, but neither
    supplies a measured cost.
    """
    assignments = pack(costs) if packed is None else packed
    assigned = [0] * costs.shards
    unrecorded = [0] * costs.shards
    for path in files:
        recorded = assignments.get(path)
        shard = unrecorded_shard(path, costs.shards) if recorded is None else recorded
        assigned[shard - 1] += 1
        unrecorded[shard - 1] += recorded is None
    return list(zip(assigned, unrecorded, strict=True))


def _share(assigned: int, unrecorded: int) -> float:
    return unrecorded / assigned if assigned else 0.0


def _percent(fraction: float) -> str:
    return f"{fraction * 100:g}%"


def _share_threshold(value: object) -> float:
    """A fraction of a shard, or a refusal: 1 never warns, 0 warns on any unrecorded file."""
    if isinstance(value, bool) or not isinstance(value, int | float) or not 0 <= value <= 1:
        raise SuiteFilesError(f"an unrecorded share is a fraction from 0 to 1, not {value!r}")
    return float(value)


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
        "--suite-unrecorded-share",
        action="store",
        type=float,
        default=UNRECORDED_SHARE_WARNING,
        metavar="FRACTION",
        help=(
            "warn when more than this fraction of the shard's test files is not named in "
            "the record; 1 never warns, for a record that is sparse by design"
        ),
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


def unrecorded_share_warning(
    shard: Shard, assigned: int, unrecorded: int, *, threshold: float, record: Path
) -> str | None:
    """What a sharded run says when too much of its shard was never weighed, or `None`."""
    share = _share(assigned, unrecorded)
    if share <= threshold:
        return None
    return (
        f"suite shard {shard}: {unrecorded} of the {assigned} test files it is assigned "
        f"({share:.1%}) are not named in {record.name}, over the {_percent(threshold)} "
        "threshold. An unrecorded file takes its owner or path hash and no cost weight, "
        "so this shard's cost is not the one the record balanced. Rebuild the record from "
        "the reports of a complete hosted cohort: `python -m devtools.suite_files record "
        "REPORT.json ...`"
    )


def _warn_of_unrecorded_share(config: pytest.Config, shard: Shard) -> None:
    """One walk of the roots this run was pointed at, priced against the record."""
    threshold = _share_threshold(config.getoption("--suite-unrecorded-share"))
    record = _costs_option(config)
    costs, packed = _packed(record)
    base = config.invocation_params.dir
    roots = [base / str(argument).partition("::")[0] for argument in config.args]
    patterns = [str(pattern) for pattern in config.getini("python_files")]
    assigned, unrecorded = unrecorded_by_shard(costs, lane_files(roots, patterns), packed)[
        shard.index - 1
    ]
    message = unrecorded_share_warning(
        shard, assigned, unrecorded, threshold=threshold, record=record
    )
    if message is not None:
        config.issue_config_time_warning(pytest.PytestConfigWarning(message), stacklevel=2)


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
            f"devtools.suite_files record --shards {shard.count}` rather than dividing a "
            "record made for another count"
        )
    config.stash[_SHARD] = shard
    controller = not hasattr(config, "workerinput")
    if shard is not None and controller:
        # The controller alone, so an xdist run says it once rather than once per worker.
        try:
            _warn_of_unrecorded_share(config, shard)
        except SuiteFilesError as error:
            raise pytest.UsageError(str(error)) from error
    target = config.getoption("--test-file-costs", default=None)
    if target is not None and controller:
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
        self.module_scope: dict[str, Any] = {}
        self.collected: defaultdict[str, int] = defaultdict(int)
        self.deselected = 0

    def pytest_sessionstart(self, session: pytest.Session) -> None:
        self.rootpath = session.config.rootpath
        config = session.config
        invocation = config.invocation_params.dir
        self.module_scope = {
            "requested_files": [repository_path(invocation / name) for name in config.args],
            "keyword": config.getoption("keyword"),
            "markexpr": config.getoption("markexpr"),
            "collection_patterns": {
                name: config.getini(name) for name in _LOCAL_COLLECTION_PATTERNS
            },
            "collection_overrides": [
                value
                for value in config.getoption("override_ini", default=[]) or []
                if value.split("=", 1)[0].strip() in _LOCAL_COLLECTION_PATTERNS
            ],
            "collection_controls": {
                name: config.getoption(name, default=default) or default
                for name, default in _LOCAL_COLLECTION_CONTROLS.items()
            },
        }

    def pytest_collection_finish(self, session: pytest.Session) -> None:
        for item in session.items:
            self.collected[repository_path(item.path)] += 1

    def pytest_deselected(self, items: list[pytest.Item]) -> None:
        self.deselected += len(items)

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.when not in {"setup", "call", "teardown"}:
            return
        location = Path(report.location[0])
        if not location.is_absolute():
            location = self.rootpath / location
        name = repository_path(location)
        self.seconds[name] += report.duration
        self.tests[name].add(report.nodeid)

    def pytest_sessionfinish(self, exitstatus: int | pytest.ExitCode) -> None:
        document = report_document(
            {name: (len(self.tests[name]), seconds) for name, seconds in self.seconds.items()},
            shard=self.shard,
            environment=os.environ,
            exit_status=int(exitstatus),
        )
        document["module_scope"] = {
            **self.module_scope,
            "collected_tests": dict(sorted(self.collected.items())),
            "deselected_tests": self.deselected,
        }
        self.target.parent.mkdir(parents=True, exist_ok=True)
        self.target.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")


def report_document(
    files: Mapping[str, tuple[int, float]],
    *,
    shard: Shard | None,
    environment: Mapping[str, str],
    exit_status: int,
) -> dict[str, Any]:
    """The report's one shape, including pytest's process exit status."""
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
        "exit_status": exit_status,
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


def _validated_files(report: Mapping[str, Any], *, position: int) -> dict[str, float]:
    """Return a report's unique file costs or refuse a report that cannot be evidence."""
    label = f"cost report {position}"
    if report.get("schema") != REPORT_SCHEMA:
        raise SuiteFilesError(f"{label} is not a {REPORT_SCHEMA} report")
    exit_status = report.get("exit_status")
    if not isinstance(exit_status, int) or isinstance(exit_status, bool):
        raise SuiteFilesError(f"{label} has no integer pytest exit_status")
    if exit_status != int(pytest.ExitCode.OK):
        raise SuiteFilesError(
            f"{label} is not successful: pytest exit_status is {exit_status}, not 0"
        )
    provenance = report.get("provenance")
    if not isinstance(provenance, Mapping) or any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in provenance.items()
    ):
        raise SuiteFilesError(f"{label} has no string-to-string provenance mapping")
    rows = report.get("files")
    if not isinstance(rows, list) or not rows:
        raise SuiteFilesError(f"{label} has no non-empty files list")

    files: dict[str, float] = {}
    total_tests = 0
    total_seconds = 0.0
    for row_position, row in enumerate(rows, start=1):
        row_label = f"{label} file row {row_position}"
        if not isinstance(row, Mapping):
            raise SuiteFilesError(f"{row_label} is not a mapping")
        name = row.get("file")
        tests = row.get("tests")
        seconds = row.get("seconds")
        if not isinstance(name, str) or not name:
            raise SuiteFilesError(f"{row_label} has no file path")
        if name in files:
            raise SuiteFilesError(f"{label} contains duplicate file {name!r}")
        if not isinstance(tests, int) or isinstance(tests, bool) or tests < 1:
            raise SuiteFilesError(f"{row_label} records {tests!r}, not a positive test count")
        if (
            not isinstance(seconds, int | float)
            or isinstance(seconds, bool)
            or seconds < 0
            or not math.isfinite(seconds)
        ):
            raise SuiteFilesError(f"{row_label} records {seconds!r}, not finite seconds")
        files[name] = float(seconds)
        total_tests += tests
        total_seconds += float(seconds)

    reported_tests = report.get("tests")
    if (
        not isinstance(reported_tests, int)
        or isinstance(reported_tests, bool)
        or reported_tests != total_tests
    ):
        raise SuiteFilesError(
            f"{label} reports {reported_tests!r} tests but its rows total {total_tests}"
        )
    reported_seconds = report.get("seconds")
    if (
        not isinstance(reported_seconds, int | float)
        or isinstance(reported_seconds, bool)
        or not math.isfinite(reported_seconds)
        or round(float(reported_seconds), 3) != round(total_seconds, 3)
    ):
        raise SuiteFilesError(
            f"{label} reports {reported_seconds!r} seconds but its rows total "
            f"{round(total_seconds, 3)!r}"
        )
    return files


def _require_same_coverage(coverages: Sequence[tuple[str, set[str]]]) -> None:
    """Refuse cohorts that would give some files fewer observations than others."""
    if not coverages:
        return
    reference_label, reference = coverages[0]
    for label, files in coverages[1:]:
        if files == reference:
            continue
        missing = sorted(reference - files)
        unexpected = sorted(files - reference)
        raise SuiteFilesError(
            f"{label} does not have the same file coverage as {reference_label}: "
            f"missing {missing[:5]}, unexpected {unexpected[:5]}"
        )


def record(
    reports: Iterable[Mapping[str, Any]],
    *,
    shards: int,
    target_ceiling_seconds: tuple[float, ...] | None = None,
) -> dict[str, Any]:
    """Combine reports into a record: each file's geometric mean over the reports naming it.

    A geometric mean because hosted runners differ by a factor rather than an offset --
    the audit measured a 1.8x spread applied evenly across files -- so the record is the
    centre of that spread rather than whichever runner drew last. A file that reported no
    time at all is recorded at zero and packs last.

    `shards` is the count the record packs into, and it is written to the record as asked.
    The count the reports were cut at is a separate fact, read from the reports: every
    sharded report must name the same one, and a cohort is complete when it holds each
    shard of that count exactly once. So a complete cohort of N packs into M, while `1/2`
    and `2/3` together are still refused as no cohort at all.
    """
    reports = list(reports)
    if not reports:
        raise SuiteFilesError("record needs at least one cost report")
    if shards < 1:
        raise SuiteFilesError(f"record needs a positive shard count, found {shards}")
    _ = _targets(target_ceiling_seconds, shards)
    validated = [
        _validated_files(report, position=position)
        for position, report in enumerate(reports, start=1)
    ]
    raw_shards = [report.get("shard") for report in reports]
    if any(part is None for part in raw_shards) and not all(
        part is None for part in raw_shards
    ):
        raise SuiteFilesError("cannot mix whole-lane and sharded cost reports")
    if all(part is not None for part in raw_shards):
        parsed = [Shard.parse(str(part)) for part in raw_shards]
        counts = {part.count for part in parsed}
        if len(counts) != 1:
            raise SuiteFilesError(
                f"reports describe shard count(s) {sorted(counts)}, not one count; a record "
                "is made from complete cohorts cut at a single shard count, whatever "
                f"--shards ({shards}) packs them into"
            )
        (cohort_shards,) = counts
        expected = set(range(1, cohort_shards + 1))
        cohort_keys = ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_SHA")
        cohorts: defaultdict[tuple[str, ...], list[tuple[int, set[str]]]] = defaultdict(list)
        for report, part, files in zip(reports, parsed, validated, strict=True):
            provenance = report.get("provenance")
            if not isinstance(provenance, dict):
                raise SuiteFilesError("a sharded report has no provenance mapping")
            missing = [key for key in cohort_keys if not provenance.get(key)]
            if missing:
                raise SuiteFilesError(
                    "a sharded report is missing cohort provenance: " + ", ".join(missing)
                )
            cohort = tuple(str(provenance[key]) for key in cohort_keys)
            cohorts[cohort].append((part.index, set(files)))
        incomplete: list[tuple[tuple[str, ...], list[int]]] = []
        for cohort, parts in cohorts.items():
            indexes = [index for index, _files in parts]
            if set(indexes) != expected or len(indexes) != cohort_shards:
                incomplete.append((cohort, indexes))
        if incomplete:
            cohort, indexes = incomplete[0]
            identity = ", ".join(
                f"{key}={value}" for key, value in zip(cohort_keys, cohort, strict=True)
            )
            raise SuiteFilesError(
                "each sharded cohort must contain each shard exactly once; "
                f"{identity} has {indexes}, expected {sorted(expected)}"
            )
        source_shas = {cohort[2] for cohort in cohorts}
        if len(source_shas) != 1:
            raise SuiteFilesError(
                f"sharded cohorts must all describe one GITHUB_SHA; found {sorted(source_shas)}"
            )
        coverages: list[tuple[str, set[str]]] = []
        for cohort, parts in cohorts.items():
            identity = ", ".join(
                f"{key}={value}" for key, value in zip(cohort_keys, cohort, strict=True)
            )
            coverage: set[str] = set()
            for index, files in parts:
                overlap = coverage & files
                if overlap:
                    raise SuiteFilesError(
                        f"sharded cohort {identity} records files in more than one shard: "
                        f"{sorted(overlap)[:5]} (including shard {index})"
                    )
                coverage.update(files)
            coverages.append((f"sharded cohort {identity}", coverage))
        _require_same_coverage(coverages)
    else:
        _require_same_coverage(
            [
                (f"whole-lane report {position}", set(files))
                for position, files in enumerate(validated, start=1)
            ]
        )

    observed: defaultdict[str, list[float]] = defaultdict(list)
    sources: list[str] = []
    for report, files in zip(reports, validated, strict=True):
        provenance = report.get("provenance") or {}
        label = ", ".join(f"{key}={value}" for key, value in sorted(provenance.items()))
        part = f"shard {report['shard']}" if report.get("shard") else "the whole lane"
        sources.append(f"{part}: {label or 'no CI provenance'}")
        for name, seconds in files.items():
            observed[name].append(seconds)
    files = {
        name: round(math.exp(sum(math.log(value) for value in values) / len(values)), 3)
        if all(value > 0 for value in values)
        else 0.0
        for name, values in sorted(observed.items())
    }
    document = {
        "schema": COSTS_SCHEMA,
        "shards": shards,
        "recorded_from": sources,
        "files": files,
    }
    if target_ceiling_seconds is not None:
        document["target_ceiling_seconds"] = list(target_ceiling_seconds)
    return document


def _local_module_names(names: Sequence[str]) -> set[str]:
    """An explicit, unique roster of whole test modules under the behavioural roots."""
    roots = tuple(repository_path(root) + "/" for root in DEFAULT_ROOTS)
    result: set[str] = set()
    for name in names:
        path = PurePosixPath(name)
        if (
            not name.startswith(roots)
            or path.as_posix() != name
            or any(part in {".", ".."} for part in path.parts)
            or "::" in name
            or path.suffix != ".py"
            or not path.name.startswith("test_")
        ):
            raise SuiteFilesError(
                f"local admission needs whole behavioural test modules: {name!r}"
            )
        if name in result:
            raise SuiteFilesError(f"local admission repeats module {name!r}")
        result.add(name)
    if not result:
        raise SuiteFilesError("local admission needs an explicit non-empty module roster")
    return result


def admit_local(
    existing: Mapping[str, Any],
    reports: Sequence[Mapping[str, Any]],
    *,
    files: Sequence[str],
    report_sources: Sequence[str],
) -> dict[str, Any]:
    """Append measured new modules, preserving every historical record field and weight.

    Collection metadata is required on this route: an exit code alone cannot distinguish
    a whole-module run from a successful filtered selection. Hosted and sharded reports
    belong to `record`, never to an incremental local admission.
    """
    names = _local_module_names(files)
    if existing.get("schema") != COSTS_SCHEMA or not isinstance(existing.get("files"), dict):
        raise SuiteFilesError("local admission needs an existing cost record")
    overlap = names & set(existing["files"])
    if overlap:
        raise SuiteFilesError(
            f"local admission cannot replace recorded modules: {sorted(overlap)}"
        )
    if not reports or len(reports) != len(report_sources):
        raise SuiteFilesError("local admission needs a source path for every report")
    if len(set(report_sources)) != len(report_sources):
        raise SuiteFilesError("local admission repeats a report source")
    observations: defaultdict[str, list[float]] = defaultdict(list)
    sources: list[dict[str, Any]] = []
    for position, (report, source) in enumerate(zip(reports, report_sources, strict=True), 1):
        observed = _validated_files(report, position=position)
        if "shard" not in report or report["shard"] is not None:
            raise SuiteFilesError("local admission requires explicitly unsharded reports")
        if any(key.startswith("GITHUB_") for key in report["provenance"]):
            raise SuiteFilesError("local admission refuses hosted provenance")
        if set(observed) != names:
            raise SuiteFilesError(
                "local admission report does not cover exactly the explicit module roster"
            )
        scope = report.get("module_scope")
        if not isinstance(scope, Mapping):
            raise SuiteFilesError(
                "local admission report has no whole-module collection metadata"
            )
        requested = scope.get("requested_files")
        if (
            not isinstance(requested, list)
            or any(not isinstance(name, str) for name in requested)
            or _local_module_names(requested) != names
        ):
            raise SuiteFilesError(
                "local admission requested files do not match its module roster"
            )
        if scope.get("keyword") != "" or scope.get("markexpr") != "":
            raise SuiteFilesError("local admission refuses keyword or marker filtering")
        controls = scope.get("collection_controls")
        if (
            scope.get("collection_patterns") != _LOCAL_COLLECTION_PATTERNS
            or scope.get("collection_overrides") != []
            or not isinstance(controls, Mapping)
            or set(controls) != set(_LOCAL_COLLECTION_CONTROLS)
            or any(
                type(controls[name]) is not type(default) or controls[name] != default
                for name, default in _LOCAL_COLLECTION_CONTROLS.items()
            )
        ):
            raise SuiteFilesError(
                "local admission refuses missing or nonstandard collection rules"
            )
        deselected = scope.get("deselected_tests")
        if type(deselected) is not int or deselected != 0:
            raise SuiteFilesError("local admission refuses missing or deselected tests")
        collected = scope.get("collected_tests")
        expected_counts = {row["file"]: row["tests"] for row in report["files"]}
        if (
            not isinstance(collected, Mapping)
            or any(type(count) is not int or count < 1 for count in collected.values())
            or dict(collected) != expected_counts
        ):
            raise SuiteFilesError(
                "local admission reported tests do not match whole-module collection"
            )
        for name, seconds in observed.items():
            observations[name].append(seconds)
        sources.append(
            {
                "report": source,
                "provenance": dict(report["provenance"]),
                "tests": report["tests"],
            }
        )
    additions = {
        name: round(math.exp(sum(math.log(value) for value in values) / len(values)), 3)
        if all(value > 0 for value in values)
        else 0.0
        for name, values in sorted(observations.items())
    }
    document = deepcopy(dict(existing))
    document["files"].update(additions)
    document["files"] = dict(sorted(document["files"].items()))
    admissions = document.setdefault("local_admissions", [])
    if not isinstance(admissions, list):
        raise SuiteFilesError("existing local_admissions is not a list")
    admissions.append(
        {
            "method": "successful-unsharded-unfiltered-whole-module-local-reports",
            "aggregation": "per-file-geometric-mean",
            "files": sorted(names),
            "reports": sources,
        }
    )
    return document


def read_local_admission(
    costs_path: Path, report_paths: Sequence[Path], module_paths: Sequence[Path]
) -> dict[str, Any]:
    """Read validated inputs before an admission command may replace its output."""
    _ = load_costs(costs_path)
    missing = [str(path) for path in module_paths if not path.is_file()]
    if missing:
        raise SuiteFilesError(f"local admission module paths do not exist: {missing}")
    return admit_local(
        json.loads(costs_path.read_text(encoding="utf-8")),
        [read_report(path) for path in report_paths],
        files=[repository_path(path) for path in module_paths],
        report_sources=[repository_path(path) for path in report_paths],
    )


def _check(costs: RecordedCosts, roots: Iterable[Path], threshold: float) -> int:
    """Print every shard's unrecorded share and files; 1 when any is over `threshold`."""
    files = lane_files(roots)
    packed = pack(costs)
    names: defaultdict[int, list[str]] = defaultdict(list)
    for name in files:
        if name not in packed:
            names[unrecorded_shard(name, costs.shards)].append(name)
    rows = unrecorded_by_shard(costs, files, packed)
    print(
        f"{len(files)} test files, {sum(unrecorded for _assigned, unrecorded in rows)} not "
        f"named in the record; a shard may be {_percent(threshold)} unrecorded:"
    )
    over: list[str] = []
    for index, (assigned, unrecorded) in enumerate(rows, start=1):
        share = _share(assigned, unrecorded)
        excess = share > threshold
        if excess:
            over.append(f"{index}/{costs.shards}")
        print(
            f"  shard {index}/{costs.shards}: {assigned:4d} files, {unrecorded:3d} unrecorded "
            f"({share:5.1%})" + (" -- over the threshold" if excess else "")
        )
        for name in names[index]:
            print(f"      {name}")
    if not over:
        return 0
    print(
        f"shard(s) {', '.join(over)} over the threshold: those files took an owner or hash "
        "and no weight in the packing. Rebuild the record from the reports of a complete "
        "hosted cohort: `python -m devtools.suite_files record REPORT.json ...`"
    )
    return 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m devtools.suite_files",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    recording = commands.add_parser("record", help="write the record from cost reports")
    _ = recording.add_argument("reports", nargs="+", type=Path)
    _ = recording.add_argument(
        "--shards",
        type=int,
        default=None,
        help=(
            "the count to pack into, whatever count the reports were cut at; omit to keep "
            "the current record's"
        ),
    )
    admitting = commands.add_parser(
        "admit-local", help="append measured new modules without replacing hosted costs"
    )
    _ = admitting.add_argument("reports", nargs="+", type=Path)
    _ = admitting.add_argument("--files", nargs="+", type=Path, required=True)
    _ = admitting.add_argument("--costs", type=Path, default=COSTS)
    _ = admitting.add_argument("--output", type=Path, default=None)
    _ = recording.add_argument("--output", type=Path, default=COSTS)
    _ = recording.add_argument(
        "--target-ceilings",
        metavar="SECONDS,...",
        help=(
            "positive wall ceilings, one per packed shard, e.g. 131,154,154,131; omit for "
            "equal capacities"
        ),
    )
    _ = commands.add_parser("show", help="print the recorded partition's shard totals")
    checking = commands.add_parser(
        "check", help="print each shard's unrecorded files; exit 1 over the threshold"
    )
    _ = checking.add_argument(
        "--root",
        action="extend",
        nargs="+",
        type=Path,
        default=None,
        metavar="DIR",
        help="a directory of test files; default: both behavioural test roots",
    )
    _ = checking.add_argument(
        "--max-unrecorded-share",
        type=float,
        default=UNRECORDED_SHARE_WARNING,
        metavar="FRACTION",
        help=f"the share of a shard that may be unrecorded; default {UNRECORDED_SHARE_WARNING}",
    )
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "check":
            return _check(
                load_costs(),
                arguments.root or DEFAULT_ROOTS,
                _share_threshold(arguments.max_unrecorded_share),
            )
        if arguments.command == "admit-local":
            document = read_local_admission(arguments.costs, arguments.reports, arguments.files)
            output = arguments.output or arguments.costs
            atomic_write_text(output, json.dumps(document, indent=2) + "\n", encoding="utf-8")
            costs = load_costs(output)
        elif arguments.command == "record":
            shards = int(arguments.shards or load_costs().shards)
            try:
                targets = (
                    None
                    if arguments.target_ceilings is None
                    else tuple(float(part) for part in arguments.target_ceilings.split(","))
                )
            except ValueError as error:
                raise SuiteFilesError("target ceilings must be numeric seconds") from error
            document = record(
                [read_report(path) for path in arguments.reports],
                shards=shards,
                target_ceiling_seconds=targets,
            )
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
