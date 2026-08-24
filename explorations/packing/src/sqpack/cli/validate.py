"""Run the packing project's refactor, evidence, and infrastructure checks.

The command is read-only. Checks run concurrently, but their captured output is
replayed in the declared order so two runs remain comparable. Use `--fast` while
editing, `--only TEXT` for one named surface, the default command before a commit, and
`--strict` before an unattended research session or merge.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Literal, Never, override

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
REPOSITORY_ROOT = PROJECT_ROOT.parents[1]
ENGINE = PROJECT_ROOT / "sqsearch/target/release/sqsearch"
RESULTS = Path("campaign/series/series-000-smoke-and-calibration/results")
ACTIVITY_MARKER = PROJECT_ROOT / ".gate-running"
DEFAULT_CPU_COUNT = 4
INNER_JOB_DIVISOR = 3
TOP_TIMING_COUNT = 8


class UsageError(ValueError):
    """The requested validation surface is internally inconsistent."""


class StepFailureError(RuntimeError):
    """A check ran and did not establish its contract."""


class StepSkippedError(RuntimeError):
    """A check could not run because an optional local tool is unavailable."""

    def __init__(self, reason: str, *, output: str = "") -> None:
        super().__init__(reason)
        self.output = output


class ParserExitError(Exception):
    """An argparse exit represented as a return value for programmatic callers."""

    def __init__(self, status: int, message: str | None = None) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


class ArgumentParser(argparse.ArgumentParser):
    """Argument parser that never terminates an embedding Python process."""

    @override
    def exit(self, status: int = 0, message: str | None = None) -> Never:
        raise ParserExitError(status, message)

    @override
    def error(self, message: str) -> Never:
        raise UsageError(message)


@dataclass(frozen=True)
class Context:
    """Resolved settings shared by every validation step."""

    deep: bool
    strict: bool
    jobs: int
    inner_jobs: int
    environment: dict[str, str]


StepAction = Callable[[Context], str]


@dataclass(frozen=True)
class Step:
    """One independently runnable, read-only validation contract."""

    name: str
    action: StepAction
    fast: bool = False
    needs_engine: bool = False

    @property
    def tags(self) -> str:
        tags = ["fast" if self.fast else "full"]
        if self.needs_engine:
            tags.append("engine")
        return ", ".join(tags)


@dataclass(frozen=True)
class StepResult:
    """The complete observable outcome of one step."""

    name: str
    status: Literal["passed", "failed", "skipped"]
    seconds: float
    output: str = ""
    reason: str = ""


@dataclass
class RunSummary:
    """Ordered validation results plus setup output."""

    results: list[StepResult]
    wall_seconds: float
    setup_output: str = ""
    selected_count: int = 0
    total_count: int = 0
    partial_pattern: list[str] = field(default_factory=list)


def _run(
    context: Context,
    command: Sequence[str],
    *,
    cwd: Path = PROJECT_ROOT,
) -> str:
    completed = subprocess.run(
        list(command),
        cwd=cwd,
        env=context.environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    output = completed.stdout.rstrip()
    if completed.returncode:
        rendered = " ".join(command)
        detail = f"command exited {completed.returncode}: {rendered}"
        if output:
            detail += f"\n{output}"
        raise StepFailureError(detail)
    return output


def _module(context: Context, module: str, *arguments: str) -> str:
    return _run(context, (sys.executable, "-m", module, *arguments))


def _commands(
    context: Context, commands: Sequence[Sequence[str]], *, cwd: Path = PROJECT_ROOT
) -> str:
    outputs = [_run(context, command, cwd=cwd) for command in commands]
    return "\n".join(output for output in outputs if output)


def _require_text(output: str, *needles: str) -> None:
    missing = [needle for needle in needles if needle not in output]
    if missing:
        raise StepFailureError(f"output omitted required text: {missing!r}\n{output}")


def _required_tool(context: Context, name: str) -> str:
    found = shutil.which(name, path=context.environment.get("PATH"))
    if found is None:
        raise StepFailureError(
            f"required development tool is unavailable: {name}; run `uv sync --group dev`"
        )
    return found


def _optional_tool(context: Context, name: str) -> str:
    found = shutil.which(name, path=context.environment.get("PATH"))
    if found is None:
        raise StepSkippedError(f"{name} is unavailable")
    return found


def _fast_tests(context: Context) -> str:
    return _run(context, (sys.executable, "-m", "pytest", "-q", "tests"))


def _soundness_perimeter(context: Context) -> str:
    output = _module(context, "devtools.check_soundness_perimeter")
    if "skipping engine cells" in output:
        raise StepSkippedError(
            "soundness perimeter did not exercise sqsearch cells",
            output=output,
        )
    return output


def _python_quality(context: Context) -> str:
    ruff = _required_tool(context, "ruff")
    basedpyright = _required_tool(context, "basedpyright")
    output = _commands(
        context,
        (
            (ruff, "check", "."),
            (ruff, "format", "--check", "."),
            (basedpyright,),
        ),
    )
    _require_text(output, "0 errors, 0 warnings, 0 notes")
    return output


def _basin_atlas(context: Context) -> str:
    return _module(context, "devtools.check_atlas")


def _basin_events(context: Context) -> str:
    module = "cases.campaign_smoke.basin_events"
    archives = (
        "exp-018-h-021-n3-basin-events.jsonl",
        "exp-021-h-021-n3-basin-event-v3.jsonl",
        "exp-022-h-021-n3-basin-event-v3-completion.jsonl",
        "exp-023-h-021-n4-basin-event-v3.jsonl",
        "exp-024-h-021-n4-basin-event-v3-repair.jsonl",
        "exp-025-h-021-n5-basin-event-v3.jsonl",
        "exp-026-h-021-n6-basin-event-v3.jsonl",
        "exp-027-h-021-n6-basin-event-v3-retention.jsonl",
        "exp-028-h-021-n7-basin-event-v3.jsonl",
        "exp-029-h-021-n8-basin-event-v3.jsonl",
        "exp-030-h-021-n9-basin-event-v3.jsonl",
        "exp-031-h-002-n10-source-return.jsonl",
    )
    outputs = [_module(context, module, "--selftest")]
    outputs.extend(
        _module(context, module, "replay", str(RESULTS / archive)) for archive in archives
    )
    return "\n".join(outputs)


def _historical_regressions(context: Context) -> str:
    return _module(context, "devtools.check_regressions")


def _small_n(context: Context) -> str:
    commands = (
        (
            sys.executable,
            "-m",
            "cases.small_n.optimal_moduli",
            "--n",
            "3",
            "--replay",
            str(RESULTS / "exp-014-h-032-n3-optimal-moduli.json"),
            "--check-svg",
            "atlas/n-003-optimal-moduli.svg",
        ),
        (
            sys.executable,
            "-m",
            "cases.small_n.optimal_moduli",
            "--n",
            "4",
            "--replay",
            str(RESULTS / "exp-015-h-032-n4-optimal-moduli.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.small_n.terminal_components",
            "--replay",
            str(RESULTS / "exp-032-h-021-terminal-component-controls.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.equal_side_face",
            "--replay",
            str(RESULTS / "exp-033-h-023-n5-equal-side-face.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.angle_sheet",
            "--replay",
            str(RESULTS / "exp-034-h-023-n5-angle-sheet.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.tangent_cones",
            "--replay",
            str(RESULTS / "exp-035-h-023-n5-tangent-cones.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.second_order_obstruction",
            "--replay",
            str(RESULTS / "exp-036-h-023-n5-second-order-obstruction.json"),
        ),
    )
    return _commands(context, commands)


def _negative_controls(context: Context) -> str:
    return _module(context, "devtools.run_negative_controls", "devtools/controls.yaml")


def _independent_lp(context: Context) -> str:
    output = _module(context, "cases.trump11.independent_lp_cell")
    _require_text(output, "23 variables, 1056 constraints", "ALL CHECKS PASSED")
    return output


def _bead_tree(context: Context) -> str:
    output = _module(context, "devtools.check_bead_tree")
    if output.startswith("SKIP"):
        raise StepSkippedError("no bead store is reachable", output=output)
    return output


def _golden_basins(context: Context) -> str:
    arguments = ("--deep",) if context.deep else ()
    output = _module(context, "devtools.check_golden_basins", *arguments)
    if not context.deep:
        output += "\n  (fast path; `packing-validate --deep` rebuilds and compares the map)"
    return output


def _canonical_identity(context: Context) -> str:
    return _module(context, "devtools.check_canonical")


def _schemas(context: Context) -> str:
    return _module(context, "devtools.validate_schemas")


def _derivation(context: Context) -> str:
    output = _module(context, "cases.trump11.derive_field")
    _require_text(output, "matches cases.trump11.packing.U_MIN_POLY: True")
    return output


def _search_engine(context: Context) -> str:
    if not ENGINE.is_file():
        raise StepSkippedError("sqsearch binary is absent")
    output = _run(context, (str(ENGINE), "--selftest"))
    _require_text(output, "SELFTEST PASSED")
    if "FAIL" in output:
        raise StepFailureError(output)
    return output


def _rust_quality(context: Context) -> str:
    cargo = _optional_tool(context, "cargo")
    output = _commands(
        context,
        (
            (cargo, "clippy", "--release", "--all-targets", "--quiet", "--", "-D", "warnings"),
            (cargo, "fmt", "--check"),
        ),
        cwd=PROJECT_ROOT / "sqsearch",
    )
    return f"{output}\n  clippy clean at warnings-as-errors; rustfmt clean".strip()


def _trump_cones(context: Context) -> str:
    return _module(
        context,
        "cases.trump11.tangent_cones",
        "--replay",
        str(RESULTS / "exp-013-h-026-trump-tangent.json"),
    )


def _stromquist_repair(context: Context) -> str:
    return _module(
        context,
        "cases.stromquist.repaired_cover",
        "--replay",
        str(RESULTS / "exp-017-h-041-stromquist-repaired-figure14.json"),
    )


def _stromquist_rejection(context: Context) -> str:
    return _module(
        context,
        "cases.stromquist.printed_cover",
        "--replay",
        str(RESULTS / "exp-016-h-010-stromquist-printed-figure14.json"),
    )


def _exact_verification(context: Context) -> str:
    output = _module(context, "cases.trump11.verify_exact")
    _require_text(
        output,
        "VALID: 11 squares, 55 pairs tested",
        "14 separated with zero gap, 41 strictly",
        "20 corner coordinates exactly on the boundary",
        "P(s) == 0 for the published degree-8 polynomial: True",
        "s = 3.87708359002281417730789706010096",
    )
    return output


def _verifier_limits(context: Context) -> str:
    output = _module(context, "cases.trump11.verifier_limits")
    _require_text(output, "delta = 1e-100  REJECT", "tol=1e-09")
    if re.search(r"delta = 1e-[0-9]+ +accept", output):
        raise StepFailureError("the exact verifier accepted a perturbed packing")
    line = next((value for value in output.splitlines() if value.startswith("  tol=1e-09")), "")
    _require_text(line, "1e-12: accept")
    return output


def _frontier_corpus(context: Context) -> str:
    files = sorted((PROJECT_ROOT / "frontier").glob("n-*.md"))
    if len(files) != 100:
        raise StepFailureError(f"expected 100 frontier artifacts, found {len(files)}")
    values: set[int] = set()
    open_count = 0
    nagamochi_count = 0
    for path in files:
        data = yaml.safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
        softschema = data["softschema"]
        packing = data["packing"]
        if softschema != {
            "contract": "packing.squares:SquarePackingCase/v1",
            "schema": "square-packing-case.schema.yaml",
            "envelope": "packing",
            "status": "enforced",
        }:
            raise StepFailureError(
                f"unexpected softschema declaration: {path.relative_to(PROJECT_ROOT)}"
            )
        n = int(path.stem.split("-")[1])
        if n != packing["n"] or packing["status"] not in {"proved", "open"}:
            raise StepFailureError(
                f"inconsistent frontier identity: {path.relative_to(PROJECT_ROOT)}"
            )
        if packing["upper_bound"]["value"] < packing["lower_bound"]["value"] - 1e-9:
            raise StepFailureError(f"negative frontier gap: {path.relative_to(PROJECT_ROOT)}")
        if packing["status"] == "proved" and abs(packing["gap"]) >= 1e-9:
            raise StepFailureError(
                f"proved frontier case retains a gap: {path.relative_to(PROJECT_ROOT)}"
            )
        if packing["status"] == "open":
            open_count += 1
            nagamochi_count += packing["lower_bound"]["kind"] == "nagamochi"
        values.add(n)
    if values != set(range(1, 101)) or (open_count, nagamochi_count) != (65, 63):
        raise StepFailureError("frontier coverage or documented corpus counts drifted")

    kingbird = _module(
        context,
        "cases.kingbird29.verify_svg",
        "resources/papers/kingbird-square-29-provenance.svg",
    )
    result = json.loads(kingbird)
    if not (
        result["packing"]["valid"]
        and result["packing"]["n"] == 29
        and result["packing"]["pairs_tested"] == 406
        and result["orientation_class_count"] == 6
        and [item["count"] for item in result["orientation_classes"]] == [15, 1, 9, 1, 2, 1]
        and all(result["selftests"].values())
    ):
        raise StepFailureError("the Kingbird n=29 replay contract changed")
    return (
        f"  100 artifacts, n = 1..100, {100 - open_count} proved, {open_count} open\n"
        f"  {nagamochi_count} of {open_count} open cases bounded below by Nagamochi's theorem\n"
        "  n=29 source: 29 squares, 406 pairs, six classes, source equations replayed"
    )


def _generated_tables(context: Context) -> str:
    return _module(context, "devtools.render_research_tables", "--check")


def _strategy_catalogues(_context: Context) -> str:
    lines: list[str] = []
    for kind, field_name, expected in (("search", "outcome", 20), ("proof", "status", 30)):
        path = PROJECT_ROOT / "frontier" / f"{kind}-strategies.yaml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        strategies = data["strategies"]
        if (
            data["kind"] != kind
            or data["count"] != len(strategies)
            or len(strategies) != expected
        ):
            raise StepFailureError(f"{kind}: expected {expected} strategies")
        if [item["id"] for item in strategies] != list(range(1, expected + 1)):
            raise StepFailureError(f"{kind}: ids are not contiguous")
        families = set(data["families"])
        for item in strategies:
            required = (item[field_name], item["name"], item["mechanism"], item["note"])
            if item["family"] not in families or not all(required):
                raise StepFailureError(f"{kind} #{item['id']}: invalid family or empty field")
        lines.append(
            f"  {kind}: {expected} strategies, {len(families)} families, all fields populated"
        )
    return "\n".join(lines)


def _defect_log(context: Context) -> str:
    return _commands(
        context,
        (
            (sys.executable, "-m", "devtools.render_defects", "--check"),
            (sys.executable, "-m", "devtools.check_generated_markdown"),
        ),
    )


def _skills_mirrored(context: Context) -> str:
    make = shutil.which("make", path=context.environment.get("PATH"))
    if make is None:
        raise StepSkippedError("make is unavailable; skill mirrors were not compared")
    return _run(context, (make, "--no-print-directory", "skills-check"), cwd=REPOSITORY_ROOT)


def _synopsis(context: Context) -> str:
    return _module(context, "devtools.check_synopsis")


def _readme(context: Context) -> str:
    return _module(context, "devtools.check_readme")


def _differential(context: Context) -> str:
    if not ENGINE.is_file():
        raise StepSkippedError(
            "sqsearch binary is absent; differential geometry was not checked"
        )
    return _module(context, "devtools.check_search_differential", "20000")


def _provenance(context: Context) -> str:
    del context
    lines: list[str] = []
    checked = 0
    declared = 0
    paths = sorted((PROJECT_ROOT / "campaign/series").glob("*/experiments/*.md"))
    for path in paths:
        text = path.read_text(encoding="utf-8")
        matches = re.findall(r"^[ \t]*engine_commit:[ \t]*(.*)$", text, re.MULTILINE)
        declared += len(matches)
        if not matches:
            continue
        raw = matches[0].split("#", 1)[0]
        commit = raw.strip().strip("'\"").strip()
        if re.fullmatch(r"[0-9a-fA-F]{7,40}", commit) is None:
            raise StepFailureError(f"invalid {path.name} engine_commit: {raw}")
        checked += 1
        reachable = (
            subprocess.run(
                ("git", "merge-base", "--is-ancestor", commit, "HEAD"),
                cwd=PROJECT_ROOT,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            ).returncode
            == 0
        )
        if reachable:
            lines.append(f"  ok       {path.name} -> {commit}")
        else:
            lines.append(f"  ORPHANED {path.name} -> {commit} (must carry an annotation)")
            if "## Annotation" not in text:
                raise StepFailureError(f"{path.name}: orphaned engine commit has no annotation")
    if checked != declared:
        raise StepFailureError(f"checked {checked} of {declared} declared engine commits")
    lines.append(f"  checked all {checked} declared engine commits")
    return "\n".join(lines)


def _campaign_record(context: Context) -> str:
    return _module(context, "sqpack.campaign.ledger", "check")


STEPS: tuple[Step, ...] = (
    Step("soundness perimeter", _soundness_perimeter, needs_engine=True),
    Step("lint floor (python)", _python_quality, fast=True),
    Step("basin atlas", _basin_atlas),
    Step("basin event record and replay", _basin_events),
    Step("historical regressions", _historical_regressions),
    Step("small-n optimal moduli", _small_n),
    Step("negative controls", _negative_controls),
    Step("fixed-angle cell is an LP, rebuilt independently", _independent_lp),
    Step("fast behavioral tests", _fast_tests, fast=True),
    Step("bead tree", _bead_tree, fast=True),
    Step("golden basin maps (proved cases, checked against mathematics)", _golden_basins),
    Step("basin identity", _canonical_identity),
    Step("soft-schema validation", _schemas, fast=True),
    Step("derivation (needs sympy)", _derivation, fast=True),
    Step("search engine (sqsearch)", _search_engine, needs_engine=True),
    Step("lint floor (rust)", _rust_quality),
    Step("Trump exact branchwise linearized cones", _trump_cones),
    Step("H-041 Stromquist repaired-cover exact certificate", _stromquist_repair),
    Step("H-010 Stromquist printed-cover exact rejection", _stromquist_rejection),
    Step("exact verification", _exact_verification, fast=True),
    Step("negative control", _verifier_limits, fast=True),
    Step("frontier corpus", _frontier_corpus),
    Step("generated tables in sync with frontier/", _generated_tables, fast=True),
    Step("strategy catalogues", _strategy_catalogues, fast=True),
    Step("defect log", _defect_log, fast=True),
    Step("skills mirrored between .agents and .claude", _skills_mirrored, fast=True),
    Step("synopsis agrees with the artifacts", _synopsis, fast=True),
    Step("README agrees with the directory", _readme, fast=True),
    Step("differential: search energy vs validity oracle", _differential, needs_engine=True),
    Step("provenance: recorded commits are reachable", _provenance, fast=True),
    Step("campaign record", _campaign_record, fast=True),
)


def _positive_integer(name: str, value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise UsageError(f"{name} must be a positive integer, got {value!r}") from error
    if parsed <= 0:
        raise UsageError(f"{name} must be a positive integer, got {value!r}")
    return parsed


def _environment_flag(name: str) -> bool:
    value = os.environ.get(name, "0")
    if value not in {"0", "1"}:
        raise UsageError(f"{name} must be 0 or 1, got {value!r}")
    return value == "1"


def _select_steps(*, only: list[str], fast: bool) -> list[Step]:
    selected = [step for step in STEPS if not fast or step.fast]
    if only:
        selected = [step for step in selected if any(pattern in step.name for pattern in only)]
    if not selected:
        patterns = ", ".join(repr(pattern) for pattern in only)
        message = (
            f"--only {patterns} matched no validation step; "
            "`packing-validate --list` shows names"
        )
        raise UsageError(message)
    return selected


def _execute_step(step: Step, context: Context) -> StepResult:
    started = time.perf_counter()
    try:
        output = step.action(context)
    except StepSkippedError as error:
        return StepResult(
            name=step.name,
            status="skipped",
            seconds=time.perf_counter() - started,
            output=error.output,
            reason=str(error),
        )
    except StepFailureError as error:
        return StepResult(
            name=step.name,
            status="failed",
            seconds=time.perf_counter() - started,
            reason=str(error),
        )
    except Exception:
        return StepResult(
            name=step.name,
            status="failed",
            seconds=time.perf_counter() - started,
            reason=traceback.format_exc().rstrip(),
        )
    return StepResult(
        name=step.name,
        status="passed",
        seconds=time.perf_counter() - started,
        output=output,
    )


def _build_engine(context: Context, selected: Sequence[Step]) -> str:
    if not any(step.needs_engine for step in selected):
        return ""
    cargo = shutil.which("cargo", path=context.environment.get("PATH"))
    if cargo is None:
        return "  SKIP: cargo is unavailable; sqsearch-dependent checks cannot run"
    output = _run(
        context,
        (cargo, "build", "--locked", "--release", "--quiet"),
        cwd=PROJECT_ROOT / "sqsearch",
    )
    suffix = "  built sqsearch/target/release/sqsearch"
    return f"{output}\n{suffix}".strip()


@contextmanager
def _validation_activity() -> Iterator[None]:
    try:
        ACTIVITY_MARKER.mkdir()
    except FileExistsError as error:
        raise StepFailureError(
            "validation marker already exists at "
            f"{ACTIVITY_MARKER}; another gate may be running"
        ) from error
    try:
        yield
    finally:
        ACTIVITY_MARKER.rmdir()


def _run_selected(
    selected: Sequence[Step], context: Context, patterns: list[str]
) -> RunSummary:
    started = time.perf_counter()
    with _validation_activity():
        setup_output = _build_engine(context, selected)
        by_name: dict[str, StepResult] = {}
        with ThreadPoolExecutor(max_workers=context.jobs) as pool:
            futures = {
                pool.submit(_execute_step, step, context): step.name for step in selected
            }
            for future in as_completed(futures):
                result = future.result()
                by_name[result.name] = result
    ordered = [by_name[step.name] for step in selected]
    return RunSummary(
        results=ordered,
        wall_seconds=time.perf_counter() - started,
        setup_output=setup_output,
        selected_count=len(selected),
        total_count=len(STEPS),
        partial_pattern=patterns,
    )


def _render_text(summary: RunSummary, *, strict: bool) -> int:
    if summary.setup_output:
        print("\n== building sqsearch ==")
        print(summary.setup_output)
    for result in summary.results:
        print(f"\n== {result.name} ==")
        if result.output:
            print(result.output)
        if result.status == "skipped":
            print(f"  SKIP: {result.reason}")
        elif result.status == "failed":
            print(result.reason, file=sys.stderr)

    print("\n== where the time went ==")
    for result in sorted(summary.results, key=lambda item: item.seconds, reverse=True)[
        :TOP_TIMING_COUNT
    ]:
        print(f"  {result.seconds:7.2f}s  {result.name}")
    print(f"  {summary.wall_seconds:7.2f}s  TOTAL (wall)")

    failed = [result for result in summary.results if result.status == "failed"]
    skipped = [result for result in summary.results if result.status == "skipped"]
    print()
    if failed:
        print(f"{len(failed)} STEPS FAILED:")
        for result in failed:
            print(f"  - {result.name}")
        return 1
    if skipped:
        print(f"VALIDATION COMPLETED, BUT {len(skipped)} CHECKS WERE SKIPPED:")
        for result in skipped:
            print(f"  - {result.name}: {result.reason}")
        if strict:
            print("strict mode: a skipped check is not a passed check", file=sys.stderr)
            return 1
    if summary.selected_count != summary.total_count:
        qualifier = (
            f"--only {summary.partial_pattern!r}" if summary.partial_pattern else "--fast"
        )
        print(
            f"{summary.selected_count} of {summary.total_count} STEPS PASSED "
            f"({qualifier}; this is not the full gate)"
        )
    else:
        print("ALL CHECKS PASSED")
    return 0


def _parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="packing-validate",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--fast", action="store_true", help="run the fast edit-loop checks")
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="TEXT",
        help="run step names containing TEXT; repeat for more than one pattern",
    )
    parser.add_argument(
        "--strict", action="store_true", help="run deep checks and fail on skips"
    )
    parser.add_argument(
        "--deep", action="store_true", help="rebuild expensive golden producers"
    )
    parser.add_argument("--jobs", metavar="N", help="maximum concurrent validation steps")
    parser.add_argument("--inner-jobs", metavar="N", help="worker cap exported to each step")
    parser.add_argument(
        "--list", action="store_true", help="list check names and tiers, then exit"
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="render a human transcript or one machine-readable summary",
    )
    return parser


def _validate_invocation(*, strict: bool, deep: bool, only: list[str], fast: bool) -> None:
    if strict and (only or fast):
        raise UsageError("--strict cannot be combined with --only or --fast")
    if strict and not deep:
        raise StepFailureError("strict mode did not enable deep validation")


def _validate_runtime() -> None:
    if sys.version_info[:2] != (3, 14):
        raise UsageError(f"Python 3.14 is required, running {sys.version.split()[0]}")


def main(arguments: list[str] | None = None) -> int:
    """Run validation and return a process-compatible status code."""
    parser = _parser()
    try:
        namespace = parser.parse_args(arguments)
        strict = namespace.strict or _environment_flag("PACKING_VALIDATE_STRICT")
        deep = namespace.deep or _environment_flag("PACKING_VALIDATE_DEEP") or strict
        _validate_invocation(strict=strict, deep=deep, only=namespace.only, fast=namespace.fast)
        jobs_value = namespace.jobs or os.environ.get("PACKING_VALIDATE_JOBS")
        jobs = (
            _positive_integer("--jobs", jobs_value)
            if jobs_value is not None
            else (os.cpu_count() or DEFAULT_CPU_COUNT)
        )
        inner_value = namespace.inner_jobs or os.environ.get("PACKING_VALIDATE_INNER_JOBS")
        inner_jobs = (
            _positive_integer("--inner-jobs", inner_value)
            if inner_value is not None
            else max(1, jobs // INNER_JOB_DIVISOR)
        )
        _validate_runtime()
        if namespace.list:
            records = [{"name": step.name, "tags": step.tags} for step in STEPS]
            if namespace.format == "json":
                print(json.dumps(records, indent=2))
            else:
                for step in STEPS:
                    print(f"{step.name} [{step.tags}]")
            return 0
        selected = _select_steps(only=namespace.only, fast=namespace.fast)
        environment = os.environ.copy()
        environment["PACK_JOBS"] = str(inner_jobs)
        context = Context(
            deep=deep,
            strict=strict,
            jobs=jobs,
            inner_jobs=inner_jobs,
            environment=environment,
        )
        summary = _run_selected(selected, context, namespace.only)
    except ParserExitError as error:
        if error.message:
            stream = sys.stdout if error.status == 0 else sys.stderr
            print(error.message, end="", file=stream)
        return error.status
    except (UsageError, StepFailureError) as error:
        print(f"packing-validate: error: {error}", file=sys.stderr)
        return 2 if isinstance(error, UsageError) else 1

    if namespace.format == "json":
        print(json.dumps(asdict(summary), indent=2))
        failed = any(result.status == "failed" for result in summary.results)
        skipped = any(result.status == "skipped" for result in summary.results)
        return 1 if failed or (strict and skipped) else 0
    return _render_text(summary, strict=strict)


if __name__ == "__main__":
    raise SystemExit(main())
