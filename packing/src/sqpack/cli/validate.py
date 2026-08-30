"""Run the packing project's refactor, evidence, and infrastructure checks.

The command is read-only. Checks run concurrently, but their captured output is
replayed in the declared order so two runs remain comparable. Use `--fast` while
editing, `--records` before a push, `--only TEXT` for one named surface, the default
command before a commit, and `--strict` before an unattended research session or merge.

`--records` exists because of what breaks. Every CI failure on this branch was a
registry, generated view, or declared contract going stale, and none was a test; the
record steps run in about seventy seconds against the fast tier's eight minutes, which
is what made pushing without them the cheaper-looking move.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import math
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import traceback
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import contextmanager, suppress
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from threading import Lock
from typing import Literal, Never, override

from sqpack.project import (
    ProjectLayoutError,
    configured_project_root,
    require_project_root,
)
from sqpack.yamlio import safe_load

PROJECT_ROOT = configured_project_root()
REPOSITORY_ROOT = PROJECT_ROOT.parent
ENGINE = PROJECT_ROOT / "sqsearch/target/release/sqsearch"
RESULTS = Path("campaign/series/series-000-smoke-and-calibration/results")
ACTIVITY_MARKER = PROJECT_ROOT / ".gate-running"
DEFAULT_CPU_COUNT = 4
INNER_JOB_DIVISOR = 3
NEGATIVE_CONTROL_WORKERS = 2
TOP_TIMING_COUNT = 8
SUPPORTED_PYTHON = (3, 14)
BASIN_EVENT_CONTRACT_PREFIX = "packing.squares:BasinEvent/"
PROCESS_TERMINATION_GRACE_SECONDS = 1.0
DEFAULT_TIMEOUT_SECONDS = 900.0


class _ProcessRegistry:
    """Process groups owned by one validation run."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._pids: set[int] = set()
        self._stopping = False

    def register(self, pid: int) -> None:
        with self._lock:
            if self._stopping:
                with suppress(ProcessLookupError):
                    os.killpg(pid, signal.SIGKILL)
                raise StepFailureError("validation is stopping; rejected new subprocess")
            self._pids.add(pid)

    def discard(self, pid: int) -> None:
        with self._lock:
            self._pids.discard(pid)

    def stop(self) -> None:
        with self._lock:
            self._stopping = True
            pids = tuple(self._pids)
        if not pids:
            return
        for pid in pids:
            with suppress(ProcessLookupError):
                os.killpg(pid, signal.SIGTERM)
        time.sleep(PROCESS_TERMINATION_GRACE_SECONDS)
        for pid in pids:
            with suppress(ProcessLookupError):
                os.killpg(pid, signal.SIGKILL)


type CommitState = Literal["reachable", "orphaned", "missing"]


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
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
    timeout_is_explicit: bool = False
    """True when an operator named the cap through `--timeout-seconds` or the
    environment variable, rather than taking the default.

    A step's `budget_seconds` may raise the default cap, because the default is a
    project-wide guess and one step is known to exceed it. It may not raise a number a
    person typed: someone tightening the cap is deliberately bounding this run, and a
    step quietly opting out of that is the bug, not the feature."""

    processes: _ProcessRegistry = field(
        default_factory=_ProcessRegistry, compare=False, repr=False
    )


StepAction = Callable[[Context], str]


@dataclass(frozen=True)
class Step:
    """One independently runnable, read-only validation contract."""

    name: str
    action: StepAction
    fast: bool = False
    needs_engine: bool = False
    records: bool = False
    """Checks the record rather than the mathematics: registries, generated views, and
    declared contracts. Every CI failure on the 2026-08-29 branch was one of these and
    none was a test, so they are selectable without paying for the test step (D-369)."""

    broad: bool = False
    """Excluded from `--edit` because its cost is breadth rather than what it uniquely
    catches.

    Measured on 2026-08-30: `--fast` is 499s and `fast behavioral tests` is 499s of it,
    so the other seventeen fast steps together cost about 48 seconds. A tier priced at
    the cost of its widest step is a tier people skip, which is the mechanism `D-369`
    records -- seven CI failures, every one a record check, none a behavioural test.

    **The default is the safe direction on purpose.** A new step is in the edit tier
    unless it says otherwise, so forgetting this flag makes the tier slower rather than
    blinder. Marking a step `broad` is the change that needs an argument, and
    `test_the_edit_tier_cannot_under_run` is where it has to be made.

    Being excluded from `--edit` is not being excluded from the gate. Every broad step
    still runs in `--fast` and above, and CI runs the full gate on every push."""

    touches: tuple[str, ...] = ()
    """Repo-relative path globs whose change can affect this step's verdict.

    Empty means *unattributed*, and an unattributed step is selected by every change. The
    default is therefore the safe direction, exactly as `broad` is: forgetting to attribute
    a step costs time, never coverage.

    Selection is conservative on both sides, which is the whole design (`BC-084`):

    - a changed path matching no step's patterns selects the **entire gate**, never the
      empty set, so a file nobody thought about cannot silently skip everything;
    - a step with no patterns is always selected;
    - `test_every_step_is_reachable_from_a_declared_pattern` requires each step to be
      selected by at least one path under `PATTERN_PROBES`, so a pattern set that has
      drifted into selecting nothing is caught rather than trusted.

    **Do not over-trust the first of those.** `fnmatch` crosses separators, so `*.py` and
    `*.md` claim every Python and Markdown file in the repository: measured over the 1312
    tracked files, 953 are claimed and only 359 can still reach the escape hatch. No `.py`
    or `.md` change ever triggers it. For those two extensions the narrow steps' own
    patterns are the *only* protection, and five were measurably too narrow when first
    written -- the SVG step reads every Markdown file in the repo and claimed none of
    them, and `frontier corpus` claimed a module it never runs while missing the one it
    does. The escape hatch is a backstop for unfamiliar file types, not for careless
    attribution of familiar ones.

    This is the commit-boundary instrument, not the edit-loop one. `BC-079` already made
    the edit loop cheap -- `--records` is 5.7s and `--edit` 43s -- so the cost this
    addresses is the full gate, where `D-355` measured a two-file edit to the rigidity
    assessor verified by a 979.79s run whose two reachable steps take 12.06s together.

    Measured on 2026-08-30 over the 42 steps: an edit to the rigidity assessor selects 11,
    one root document 9, one agenda 10, the Rust engine 12, and one unrecognised file
    still selects all 42. Six steps are deliberately unattributed because their true input
    set is the repository's whole path space -- `negative controls` runs 148 declared shell
    commands against a snapshot of nearly everything, `fast behavioral tests` walks
    `REPO.rglob("*")`, and `synopsis`, `README`, `soft-schema validation` and the
    exhaustive test step each resolve or enumerate arbitrary paths. Attributing those would
    make a data file the load-bearing contract, which is the trade this field exists to
    refuse."""

    budget_seconds: float | None = None
    """This step's own declared ceiling, for the rare step that legitimately costs more
    than the shared per-step cap.

    The shared cap exists to stop a hung step consuming the run, and it should stay tight
    for the forty steps that do not need it. `D-366` is the case that motivated an
    exception: the control suite is killed at 900 seconds and completes in about 1270,
    with nothing wrong with it -- it simply grew. Raising the shared cap would have bought
    that one step a pass by weakening the guard on every other step at once, which is the
    trade this field exists to refuse.

    A budget is a declaration, not a waiver. It is per step, it is written next to the
    step that claims it with the measurement that justifies it, and a step that exceeds
    its own budget still fails. An explicit `--timeout-seconds` on the command line still
    wins, so an operator can always tighten what a step asked for."""

    def reachable_from(self, path: str) -> bool:
        """Can a change to `path` affect this step?

        An unattributed step answers yes to everything, which is what makes forgetting to
        attribute one safe.
        """
        if not self.touches:
            return True
        return any(fnmatch.fnmatch(path, pattern) for pattern in self.touches)

    @property
    def tags(self) -> str:
        tags = ["fast" if self.fast else "full"]
        if self.fast and not self.broad:
            tags.append("edit")
        if self.records:
            tags.append("records")
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


def _timeout_output(error: subprocess.TimeoutExpired) -> str:
    output = error.output
    if isinstance(output, bytes):
        return output.decode(errors="replace")
    return output or ""


def _stop_process_group(process: subprocess.Popen[str]) -> str:
    """Stop one POSIX group and reap its parent.

    Deliberately detached descendants are outside this group-scoped guarantee.
    """
    grace_deadline = time.monotonic() + PROCESS_TERMINATION_GRACE_SECONDS
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGTERM)
    try:
        stdout, _ = process.communicate(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
        output = stdout or ""
    except subprocess.TimeoutExpired as error:
        output = _timeout_output(error)

    # communicate() can return as soon as the parent exits even though a descendant
    # ignores TERM and no longer holds the parent's output pipe. Preserve the complete
    # grace interval before escalating the whole group.
    remaining = grace_deadline - time.monotonic()
    if remaining > 0:
        time.sleep(remaining)
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)

    try:
        stdout, _ = process.communicate(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
    except subprocess.TimeoutExpired as error:
        if process.stdout is not None:
            process.stdout.close()
        try:
            process.wait(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
        except subprocess.TimeoutExpired as reap_error:
            raise StepFailureError(
                "timed-out command did not exit after process-group SIGKILL"
            ) from reap_error
        return _timeout_output(error) or output
    else:
        return stdout or output


def _run(
    context: Context,
    command: Sequence[str],
    *,
    cwd: Path = PROJECT_ROOT,
    timeout_seconds: float | None = None,
) -> str:
    effective_timeout = (
        context.timeout_seconds
        if timeout_seconds is None
        else min(timeout_seconds, context.timeout_seconds)
    )

    if os.name == "nt":
        raise StepFailureError(
            "bounded validation subprocesses require verified process-tree cleanup; "
            "Windows support is not yet implemented"
        )

    process = subprocess.Popen(
        list(command),
        cwd=cwd,
        env=context.environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    )
    try:
        context.processes.register(process.pid)
    except StepFailureError:
        try:
            process.communicate(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
        except subprocess.TimeoutExpired as error:
            if process.stdout is not None:
                process.stdout.close()
            raise StepFailureError(
                "rejected validation subprocess did not exit after SIGKILL"
            ) from error
        raise
    try:
        stdout, _ = process.communicate(timeout=effective_timeout)
    except subprocess.TimeoutExpired:
        output = _stop_process_group(process).rstrip()
        rendered = " ".join(command)
        detail = f"command timed out after {effective_timeout:g} seconds: {rendered}"
        if output:
            detail += f"\n{output}"
        raise StepFailureError(detail) from None
    except BaseException:
        _stop_process_group(process)
        raise
    finally:
        context.processes.discard(process.pid)
    output = (stdout or "").rstrip()
    if process.returncode:
        rendered = " ".join(command)
        detail = f"command exited {process.returncode}: {rendered}"
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
    return _run(
        context,
        (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "tests",
            "-m",
            "not exhaustive_exact",
        ),
    )


def _exhaustive_exact_tests(context: Context) -> str:
    return _run(
        context,
        (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "tests",
            "-m",
            "exhaustive_exact",
        ),
    )


def _soundness_perimeter(context: Context) -> str:
    output = _module(context, "devtools.check_soundness_perimeter")
    if "skipping engine cells" in output:
        raise StepSkippedError(
            "soundness perimeter did not exercise sqsearch cells",
            output=output,
        )
    return output


def _lint_floor(context: Context) -> str:
    """Ruff alone, because it is the half that is instant and the half that caught a
    registry bug: the duplicated declared-consumer key behind one of D-369's CI
    failures was an `F601`. Measured under a second against basedpyright's 36."""
    ruff = _required_tool(context, "ruff")
    return _commands(context, ((ruff, "check", "."), (ruff, "format", "--check", ".")))


def _type_floor(context: Context) -> str:
    basedpyright = _required_tool(context, "basedpyright")
    output = _commands(context, ((basedpyright,),))
    _require_text(output, "0 errors, 0 warnings, 0 notes")
    return output


def _basin_atlas(context: Context) -> str:
    return _module(context, "devtools.check_atlas")


def _basin_event_archives(results: Path) -> list[Path]:
    """Discover retained event journals by their versioned record contract."""
    archives: list[Path] = []
    for path in sorted(results.glob("*.jsonl")):
        first_line = next(
            (line for line in path.read_text().splitlines() if line.strip()), None
        )
        if first_line is None:
            continue
        try:
            first_record = json.loads(first_line)
        except json.JSONDecodeError as error:
            message = f"cannot classify malformed result archive {path}"
            raise StepFailureError(message) from error
        contract = first_record.get("contract") if isinstance(first_record, dict) else None
        if isinstance(contract, str) and contract.startswith(BASIN_EVENT_CONTRACT_PREFIX):
            archives.append(path)
    return archives


def _basin_events(context: Context) -> str:
    module = "cases.campaign_smoke.basin_events"
    archives = _basin_event_archives(PROJECT_ROOT / RESULTS)
    if not archives:
        raise StepFailureError(f"no basin-event archives found below {RESULTS}")
    outputs = [_module(context, module, "--selftest")]
    outputs.extend(
        _module(context, module, "replay", str(archive.relative_to(PROJECT_ROOT)))
        for archive in archives
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
        (
            sys.executable,
            "-m",
            "cases.n5.tangent_inventory",
            "--replay",
            str(RESULTS / "exp-038-h-023-n5-tangent-inventory.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.fixed_angle_polytope",
            "--replay",
            str(RESULTS / "exp-039-h-023-n5-fixed-angle-polytope.json"),
        ),
        (
            sys.executable,
            "-m",
            "cases.n5.rotating_release_paths",
            "--replay",
            str(RESULTS / "exp-042-h-023-n5-endpoint-aware-rotating-paths.json"),
        ),
    )
    return _commands(context, commands)


def _svg_rendering(context: Context) -> str:
    output = _module(context, "devtools.check_svg_rendering", "--check")
    _require_text(output, "SVG RENDERING CHECKS PASSED")
    return output


def _known_best_atlas(context: Context) -> str:
    output = _commands(
        context,
        (
            (sys.executable, "-m", "devtools.build_known_best_atlas", "--check"),
            (sys.executable, "-m", "devtools.build_composite_figure_data", "--check"),
            (sys.executable, "-m", "devtools.render_composite_pdf", "--check"),
            (sys.executable, "-m", "devtools.census_known_best_chunks", "--check"),
            (
                sys.executable,
                "-m",
                "devtools.render_known_best_contact_overlays",
                "--check",
            ),
            (
                sys.executable,
                "-m",
                "devtools.profile_known_best_chunks",
                "--check",
            ),
            (sys.executable, "-m", "devtools.price_contact_enumeration", "--check"),
            (
                sys.executable,
                "-m",
                "devtools.generate_contact_full_cell_control",
                "--check",
            ),
            (
                sys.executable,
                "-m",
                "devtools.generate_contact_structures",
                "--check",
            ),
        ),
    )
    _require_text(
        output,
        "known-best atlas check passed: 100 sources/plans, witnesses, renders, "
        "1 composite, and links",
        "chunk census check passed: components, contacts, and bounded lattice partitions "
        "for 100 records",
        "known-best contact overlay check passed: 5 house-rendered calibration strata",
        "known-best chunk evidence profile check passed: 36 non-grid calibration cases",
        "contact enumeration pricing check passed",
        "contact full-cell control check passed",
        "contact structures check passed",
    )
    return output


def _prospective_atlas(context: Context) -> str:
    output = _commands(
        context,
        (
            (sys.executable, "-m", "devtools.map_prospective_sources", "--check"),
            (sys.executable, "-m", "devtools.build_prospective_atlas", "--check"),
        ),
    )
    _require_text(
        output,
        "prospective source map check passed: 224 cases, availability and SVG",
        "prospective atlas seed check passed: 101 witnesses and 101 house renderings",
    )
    return output


def _frontier_rigidity(context: Context) -> str:
    """Every rigidity block still follows from the screen and the tiling argument.

    The counts are pinned because they are the finding: 84 records are NOT rigid on a
    replayable certificate, ten are rigid by an exact tiling with no slack, and five are
    assessed and unsettled. `undetermined` is a result and is not the same as the field
    being null; n=11 is excluded here because a stronger first-party argument owns it.
    """
    output = _module(context, "devtools.assess_frontier_rigidity", "--check")
    _require_text(output, "frontier rigidity check passed")
    review = _module(context, "devtools.assess_frontier_rigidity", "--review")
    _require_text(
        review,
        "assessed: 10 locally-rigid, 84 not-rigid, 5 undetermined, "
        "1 left to a stronger argument",
    )
    _require_text(review, "left to a stronger argument: n = [11]")
    return output + review


def _translation_escape_screen(context: Context) -> str:
    """The single-square translation screen, rebuilt from the witnesses every run.

    The counts are pinned here because they are the finding: 25 records hold a square
    that can be pushed clear of everything it touches, and the two records whose witness
    geometry is too coarse to read contacts from are excluded rather than reported on.
    A miss is not rigidity, so nothing here may be restated as one.
    """
    output = _module(context, "devtools.screen_translation_escape", "--check")
    _require_text(
        output,
        "translation escape screen check passed: 98 records screened, "
        "25 with a square that separates (76 squares), "
        "84 with a square that translates at all (496 squares), "
        "excluded: n=68, n=69",
    )
    return output


def _contact_scaffold_atlas(context: Context) -> str:
    output = _module(context, "devtools.build_contact_scaffold_atlas", "--check")
    _require_text(
        output,
        "contact scaffold atlas check passed: 21 topologies, 11013 abstract orbits",
    )
    return output


def _negative_controls(context: Context) -> str:
    workers = min(NEGATIVE_CONTROL_WORKERS, context.inner_jobs)
    return _module(
        context,
        "devtools.run_negative_controls",
        "devtools/controls.yaml",
        "-j",
        str(workers),
    )


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
    return _commands(
        context,
        (
            (sys.executable, "-m", "devtools.validate_schemas"),
            (sys.executable, "-m", "devtools.check_source_coverage"),
        ),
    )


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
    output = _commands(
        context,
        (
            (
                sys.executable,
                "-m",
                "devtools.generate_known_best_n011_rational_control",
                "--check",
            ),
            # The exact rational grid replay. It ran inside `soft-schema validation`
            # until D-370, where it was 3.58s of that step and where nobody would look
            # for exact geometry. Same cases, same predicate, same verdict; only the
            # step reporting it changed.
            (sys.executable, "-m", "devtools.check_basic_bounds"),
            (sys.executable, "-m", "cases.trump11.verify_exact"),
            (sys.executable, "-m", "cases.gobel5.verify_exact"),
            (sys.executable, "-m", "cases.gobel10.verify_exact"),
            (
                sys.executable,
                "-m",
                "sqpack.cli.witness",
                "verify",
                "witnesses/known-best-n011-rational-control.yaml",
            ),
            (
                sys.executable,
                "-m",
                "devtools.check_rational_witness_independent",
                "witnesses/known-best-n011-rational-control.yaml",
            ),
            (
                sys.executable,
                "-m",
                "sqpack.cli.witness",
                "verify",
                "witnesses/schadt-n029-2025-rational.yaml",
            ),
            (
                sys.executable,
                "-m",
                "devtools.check_rational_witness_independent",
                "witnesses/schadt-n029-2025-rational.yaml",
            ),
        ),
    )
    _require_text(
        output,
        "known-best n=11 rational control check passed",
        "VALID: 11 squares, 55 pairs tested",
        "14 separated with zero gap, 41 strictly",
        "20 corner coordinates exactly on the boundary",
        "P(s) == 0 for the published degree-8 polynomial: True",
        "s = 3.87708359002281417730789706010096",
        "VALID: 5 squares, 10 pairs tested",
        "VALID: 10 squares, 45 pairs tested",
        "VERIFIED\n  id: W-known-best-n011-rational",
        "VERIFIED: 11 squares, 55 pairs",
        "VERIFIED\n  id: W-schadt-n029-2025-decimal-rational",
        "VERIFIED: 29 squares, 406 pairs",
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
    formal_open = 0
    reported_open = 0
    nagamochi_count = 0
    for path in files:
        data = safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
        softschema = data["softschema"]
        packing = data["packing"]
        if softschema != {
            "contract": "packing.squares:SquarePackingCase/v2",
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
        if packing["status"] == "open":
            formal_open += 1
            nagamochi_count += (
                "E-nagamochi-lower" in packing["verified_lower_bound"]["evidence"]
            )
        reported_open += packing["reported_status"] == "open"
        values.add(n)
    expected_values = set(range(1, 101))
    if values != expected_values:
        missing = sorted(expected_values - values)
        extra = sorted(values - expected_values)
        raise StepFailureError(
            f"frontier n coverage drifted: missing {missing}, unexpected {extra}"
        )
    if (formal_open, reported_open, nagamochi_count) != (65, 65, 63):
        raise StepFailureError(
            "frontier corpus counts drifted: expected 65 formal-open, 65 reported-open, "
            f"and 63 Nagamochi-bounded; observed {formal_open}, {reported_open}, "
            f"and {nagamochi_count}"
        )

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
        f"  100 artifacts, n = 1..100; formal lane: {100 - formal_open} proved, "
        f"{formal_open} open\n"
        f"  reported lane: {100 - reported_open} proved, {reported_open} open; "
        f"{nagamochi_count} formal-open cases use Nagamochi\n"
        "  n=29 source numerically checked: 29 squares, 406 pairs, six classes\n"
        "  named-source reconciliation is enforced by soft-schema validation"
    )


def _generated_tables(context: Context) -> str:
    return _module(context, "devtools.render_research_tables", "--check")


def _strategy_catalogues(_context: Context) -> str:
    lines: list[str] = []
    for kind, field_name, expected in (("search", "outcome", 20), ("proof", "status", 30)):
        path = PROJECT_ROOT / "frontier" / f"{kind}-strategies.yaml"
        data = safe_load(path.read_text(encoding="utf-8"))
        strategies = data["strategies"]
        observed_kind = data.get("kind")
        if observed_kind != kind:
            raise StepFailureError(
                f"{kind} catalogue: expected kind {kind!r}, observed {observed_kind!r}"
            )
        declared_count = data.get("count")
        observed_count = len(strategies)
        if declared_count != observed_count or observed_count != expected:
            raise StepFailureError(
                f"{kind} catalogue: expected {expected} strategies; "
                f"declared {declared_count!r}, observed {observed_count} records"
            )
        observed_ids = [item["id"] for item in strategies]
        expected_ids = list(range(1, expected + 1))
        if observed_ids != expected_ids:
            raise StepFailureError(
                f"{kind} catalogue: expected ids {expected_ids}, observed {observed_ids}"
            )
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
    return _commands(
        context,
        (
            (sys.executable, "-m", "devtools.check_documentation"),
            (sys.executable, "-m", "devtools.check_synopsis"),
        ),
    )


def _readme(context: Context) -> str:
    return _module(context, "devtools.check_readme")


def _operating_rules(context: Context) -> str:
    return _module(context, "devtools.render_operating_rules", "--check")


def _agenda_map(context: Context) -> str:
    return _module(context, "devtools.render_agenda_map", "--check")


def _n5_identity_pair(context: Context) -> str:
    # Re-runs the six-seed n=5 census, so ~28s: too slow for --edit and too important to
    # leave unreplayed. D-034's pair is the only prospective control the identity work
    # has, and a census that stopped reproducing it would invalidate the control without
    # changing any file.
    return _module(context, "devtools.build_n5_identity_pair", "--check")


def _differential(context: Context) -> str:
    if not ENGINE.is_file():
        raise StepSkippedError(
            "sqsearch binary is absent; differential geometry was not checked"
        )
    return _module(context, "devtools.check_search_differential", "20000")


def _run_returncode(context: Context, command: Sequence[str]) -> int:
    """Run a quiet command through the same bounded process-group path as _run."""
    if os.name == "nt":
        raise StepFailureError(
            "bounded validation subprocesses require verified process-tree cleanup; "
            "Windows support is not yet implemented"
        )
    process = subprocess.Popen(
        list(command),
        cwd=PROJECT_ROOT,
        env=context.environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
        start_new_session=True,
    )
    try:
        context.processes.register(process.pid)
    except StepFailureError:
        try:
            process.wait(timeout=PROCESS_TERMINATION_GRACE_SECONDS)
        except subprocess.TimeoutExpired as error:
            raise StepFailureError(
                "rejected validation subprocess did not exit after SIGKILL"
            ) from error
        raise
    try:
        process.wait(timeout=context.timeout_seconds)
    except subprocess.TimeoutExpired:
        _stop_process_group(process)
        rendered = " ".join(command)
        raise StepFailureError(
            f"command timed out after {context.timeout_seconds:g} seconds: {rendered}"
        ) from None
    except BaseException:
        _stop_process_group(process)
        raise
    finally:
        context.processes.discard(process.pid)
    return process.returncode


def _commit_state(context: Context, commit: str) -> CommitState:
    available = _run_returncode(
        context,
        ("git", "cat-file", "-e", f"{commit}^{{commit}}"),
    )
    if available != 0:
        return "missing"
    ancestry = _run_returncode(
        context,
        ("git", "merge-base", "--is-ancestor", commit, "HEAD"),
    )
    if ancestry not in {0, 1}:
        raise StepFailureError(
            f"git could not compare engine commit {commit} with HEAD (exit {ancestry})"
        )
    return "reachable" if ancestry == 0 else "orphaned"


def _provenance_line(name: str, commit: str, text: str, state: CommitState) -> str:
    annotation = text.split("## Annotation", 1)[1] if "## Annotation" in text else ""
    loss_is_annotated = commit in annotation and "unreachable" in annotation.lower()
    if state == "reachable":
        return f"  ok          {name} -> {commit}"
    if state == "missing":
        if loss_is_annotated:
            return f"  UNAVAILABLE {name} -> {commit} (historical loss is annotated)"
        raise StepFailureError(
            f"{name}: engine commit {commit} is unavailable in local history; "
            "fetch complete history (`git fetch --unshallow` for a shallow clone, "
            "otherwise `git fetch --all`) and rerun"
        )
    if not loss_is_annotated:
        raise StepFailureError(f"{name}: orphaned engine commit has no explicit annotation")
    return f"  ORPHANED    {name} -> {commit} (historical loss is annotated)"


def _provenance(context: Context) -> str:
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
        state = _commit_state(context, commit)
        lines.append(_provenance_line(path.name, commit, text, state))
    if checked != declared:
        raise StepFailureError(f"checked {checked} of {declared} declared engine commits")
    lines.append(f"  checked all {checked} declared engine commits")
    return "\n".join(lines)


def _campaign_record(context: Context) -> str:
    return _commands(
        context,
        (
            (sys.executable, "-m", "sqpack.campaign.ledger", "check"),
            # A phase's validation_command is its declared falsifier. Nothing checked
            # that the command could run, so two phases once carried a flag that exits
            # 2 (think-ldy8).
            (sys.executable, "-m", "devtools.check_declared_commands"),
        ),
    )


# Attribution groups for `Step.touches`, deliberately generous. A pattern that is too
# wide costs a step that need not have run; one that is too narrow costs a verdict nobody
# checked, and only the second is a soundness failure.
#
# `fnmatch` is not a path glob -- its `*` crosses separators -- so `packing/src/sqpack/*`
# covers the whole subtree, and every pattern here is repo-relative.
_TOOLCHAIN = ("packing/pyproject.toml", "packing/uv.lock", "packing/.python-version")
# `devtools/__init__.py` is imported by every devtools-invoking step and is covered by no
# per-file devtools pattern, so it belongs with the shared core rather than repeated.
_CORE = ("packing/src/sqpack/*", "packing/devtools/__init__.py", *_TOOLCHAIN)
_ENGINE_SRC = ("packing/sqsearch/*",)
_ANY_PYTHON = ("*.py", "*.pyi", *_TOOLCHAIN)
_CASES = ("packing/cases/*",)
# The retained replay archives. Whole subtree, not the named files: several steps
# discover which archives to replay by globbing, so adding one changes what runs.
_RESULTS = ("packing/campaign/series/*",)

STEPS: tuple[Step, ...] = (
    Step(
        "soundness perimeter",
        _soundness_perimeter,
        needs_engine=True,
        touches=(*_CORE, *_ENGINE_SRC, "packing/devtools/check_soundness_perimeter.py"),
    ),
    Step("lint floor (ruff)", _lint_floor, fast=True, records=True, touches=_ANY_PYTHON),
    Step("type floor (basedpyright)", _type_floor, fast=True, touches=_ANY_PYTHON),
    Step(
        "basin atlas",
        _basin_atlas,
        touches=(*_CORE, "packing/atlas/*", "packing/devtools/check_atlas.py"),
    ),
    Step(
        "basin event record and replay",
        _basin_events,
        touches=(*_CORE, *_CASES, *_RESULTS, "packing/frontier/*"),
    ),
    Step(
        "historical regressions",
        _historical_regressions,
        touches=(
            *_CORE,
            *_ENGINE_SRC,
            *_CASES,
            *_RESULTS,
            "packing/devtools/check_regressions.py",
        ),
    ),
    Step(
        "small-n exact models and local geometry",
        _small_n,
        touches=(*_CORE, *_CASES, *_RESULTS, "packing/atlas/*"),
    ),
    Step(
        "deterministic SVG rendering",
        _svg_rendering,
        touches=(
            *_CORE,
            "packing/atlas/*",
            "packing/devtools/*",
            "packing/cases/*",
            # It asserts facts about every Markdown file in the repository:
            # `surface_expectations` pins examples in TUTORIAL.md and SYNOPSIS.md, and
            # three checks walk `REPO.rglob("*.md")` for inline SVG targets.
            "*.md",
        ),
    ),
    Step(
        "known-best n=1..100 atlas",
        _known_best_atlas,
        touches=(
            *_CORE,
            *_CASES,
            "packing/devtools/*",
            "packing/atlas/*",
            "packing/witnesses/*",
            "packing/frontier/*",
            "packing/resources/*",
        ),
    ),
    Step(
        "prospective n=101..324 source map and safe seed",
        _prospective_atlas,
        touches=(
            *_CORE,
            "packing/atlas/prospective/*",
            # The generated witnesses declare a schema one level up, so the whole tree.
            "packing/witnesses/*",
            "packing/resources/web/*",
            "packing/devtools/map_prospective_sources.py",
            "packing/devtools/build_prospective_atlas.py",
        ),
    ),
    Step(
        "single-square translation escape screen",
        _translation_escape_screen,
        touches=(
            *_CORE,
            "packing/atlas/known-best/*",
            "packing/witnesses/*",
            "packing/devtools/screen_translation_escape.py",
        ),
    ),
    Step(
        "abstract size-five contact-scaffold atlas",
        _contact_scaffold_atlas,
        touches=(
            *_CORE,
            "packing/atlas/enumerated/*",
            "packing/devtools/build_contact_scaffold_atlas.py",
        ),
    ),
    # 1268s measured uncapped at 137 controls (D-366), and the suite only grows. The
    # budget is that measurement plus room for the growth, not a number chosen to make
    # today's run pass; a control suite that doubles again should be re-argued, not
    # re-padded.
    Step("negative controls", _negative_controls, budget_seconds=1800),
    Step(
        "fixed-angle cell is an LP, rebuilt independently",
        _independent_lp,
        touches=(*_CORE, "packing/cases/trump11/*"),
    ),
    Step("fast behavioral tests", _fast_tests, fast=True, broad=True),
    Step("exhaustive exact behavioral tests", _exhaustive_exact_tests),
    Step(
        "bead tree",
        _bead_tree,
        fast=True,
        records=True,
        # The bead data lives in a sync worktree, not the tracked tree, so a bead-only
        # change produces no changed path at all -- which selects the whole gate.
        touches=(*_CORE, ".tbd/*", "packing/devtools/check_bead_tree.py"),
    ),
    Step(
        "golden basin maps (proved cases, checked against mathematics)",
        _golden_basins,
        touches=(
            *_CORE,
            *_ENGINE_SRC,
            "packing/golden/*",
            "packing/frontier/*",
            "packing/devtools/check_golden_basins.py",
        ),
    ),
    Step(
        "basin identity",
        _canonical_identity,
        touches=(
            *_CORE,
            "packing/cases/trump11/*",
            *_RESULTS,
            "packing/devtools/check_canonical.py",
        ),
    ),
    Step("soft-schema validation", _schemas, fast=True, records=True),
    Step(
        "derivation (needs sympy)",
        _derivation,
        fast=True,
        touches=(*_CORE, "packing/cases/trump11/*"),
    ),
    Step("search engine (sqsearch)", _search_engine, needs_engine=True, touches=_ENGINE_SRC),
    Step("lint floor (rust)", _rust_quality, touches=_ENGINE_SRC),
    Step(
        "Trump exact branchwise linearized cones",
        _trump_cones,
        touches=(*_CORE, "packing/cases/trump11/*", *_RESULTS),
    ),
    Step(
        "H-041 Stromquist repaired-cover exact certificate",
        _stromquist_repair,
        touches=(
            *_CORE,
            "packing/cases/stromquist/*",
            *_RESULTS,
            "packing/resources/papers/*",
        ),
    ),
    Step(
        "H-010 Stromquist printed-cover exact rejection",
        _stromquist_rejection,
        touches=(
            *_CORE,
            "packing/cases/stromquist/*",
            *_RESULTS,
            "packing/resources/papers/*",
        ),
    ),
    Step(
        "exact verification",
        _exact_verification,
        fast=True,
        touches=(
            *_CORE,
            *_CASES,
            "packing/witnesses/*",
            "packing/frontier/*",
            "packing/devtools/check_basic_bounds.py",
            "packing/devtools/generate_known_best_n011_rational_control.py",
            "packing/devtools/check_rational_witness_independent.py",
        ),
    ),
    Step(
        "verifier perturbation limits",
        _verifier_limits,
        fast=True,
        touches=(*_CORE, "packing/cases/trump11/*"),
    ),
    # D-355's measured case: a two-file edit to the rigidity assessor was verified with a
    # 979.79s full gate, and these three are what such an edit can reach.
    Step(
        "frontier corpus",
        _frontier_corpus,
        touches=(
            *_CORE,
            "packing/frontier/*",
            "packing/cases/kingbird29/*",
            "packing/resources/papers/*",
        ),
    ),
    Step(
        "frontier rigidity assessed here",
        _frontier_rigidity,
        fast=True,
        touches=(
            *_CORE,
            "packing/frontier/*",
            "packing/devtools/assess_frontier_rigidity.py",
            # `SCREEN` is atlas/known-best/translation-escape-screen.json, and the pinned
            # rigid/not-rigid/undetermined counts are exactly what changing it moves.
            "packing/atlas/known-best/*",
        ),
    ),
    Step(
        "generated tables in sync with frontier/",
        _generated_tables,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/frontier/*",
            "packing/devtools/render_research_tables.py",
            # `MAIN` is the n=11 research report, read and compared cell by cell; the
            # step exists to catch a hand-edited table in exactly that file.
            "docs/*",
        ),
    ),
    Step(
        "strategy catalogues",
        _strategy_catalogues,
        fast=True,
        records=True,
        touches=(*_CORE, "packing/frontier/*"),
    ),
    Step(
        "defect log",
        _defect_log,
        fast=True,
        records=True,
        touches=(
            "packing/defects.yaml",
            "packing/defects.schema.yaml",
            "defects.md",
            *_CORE,
            "packing/devtools/render_defects.py",
            "packing/devtools/check_generated_markdown.py",
            ".flowmarkignore",
            "*.md",
        ),
    ),
    Step(
        "skills mirrored between .agents and .claude",
        _skills_mirrored,
        fast=True,
        records=True,
        # The mirrored list is a Make variable, so the Makefile is part of the contract.
        touches=("Makefile", ".agents/*", ".claude/*"),
    ),
    Step("synopsis agrees with the artifacts", _synopsis, fast=True, records=True),
    Step("README agrees with the directory", _readme, fast=True, records=True),
    Step(
        "AGENTS.md mirrors the operating rules",
        _operating_rules,
        fast=True,
        records=True,
        touches=(
            "AGENTS.md",
            "CLAUDE.md",
            "operating-rules.md",
            "packing/devtools/render_operating_rules.py",
        ),
    ),
    Step(
        "agenda map agrees with the agendas",
        _agenda_map,
        fast=True,
        records=True,
        touches=(
            "packing/campaign/agendas/*",
            "packing/campaign/agenda-map.md",
            "packing/campaign/schemas/agenda.schema.yaml",
            "packing/devtools/render_agenda_map.py",
            *_CORE,
        ),
    ),
    # 28s, so it stays out of `--edit` -- but that follows from `fast=False` alone, since
    # `_select_steps` filters to the fast steps before `broad` is consulted. The flag was
    # set here and did nothing; a step is excluded from `--edit` by not being fast.
    Step(
        "D-034's n=5 identity pair still reproduces",
        _n5_identity_pair,
        touches=(
            *_CORE,
            "packing/devtools/build_n5_identity_pair.py",
            "packing/devtools/check_golden_basins.py",
            "packing/devtools/check_soundness_perimeter.py",
            "packing/campaign/series/*/results/bc-083-n5-identity-pair.json",
        ),
    ),
    Step(
        "differential: search energy vs validity oracle",
        _differential,
        needs_engine=True,
        touches=(*_CORE, *_ENGINE_SRC, "packing/devtools/check_search_differential.py"),
    ),
    Step(
        "provenance: recorded commits are reachable",
        _provenance,
        fast=True,
        # Also depends on git history and where HEAD points, which no path expresses. An
        # empty changed-path set already selects the whole gate, so that is bounded.
        touches=(*_CORE, *_RESULTS),
    ),
    Step(
        "campaign record",
        _campaign_record,
        fast=True,
        records=True,
        touches=(
            *_CORE,
            "packing/campaign/*",
            "packing/frontier/*",
            "packing/defects.yaml",
            "packing/devtools/check_declared_commands.py",
        ),
    ),
)


def _positive_integer(name: str, value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise UsageError(f"{name} must be a positive integer, got {value!r}") from error
    if parsed <= 0:
        raise UsageError(f"{name} must be a positive integer, got {value!r}")
    return parsed


def _positive_seconds(name: str, value: str) -> float:
    try:
        parsed = float(value)
    except ValueError as error:
        raise UsageError(
            f"{name} must be a positive number of seconds, got {value!r}"
        ) from error
    if not math.isfinite(parsed) or parsed <= 0:
        raise UsageError(f"{name} must be a positive number of seconds, got {value!r}")
    return parsed


def _environment_flag(name: str) -> bool:
    value = os.environ.get(name, "0")
    if value not in {"0", "1"}:
        raise UsageError(f"{name} must be 0 or 1, got {value!r}")
    return value == "1"


@dataclass(frozen=True)
class Selection:
    """Which steps a set of changed paths reaches, and why."""

    steps: tuple[Step, ...]
    unattributed_paths: tuple[str, ...]
    """Changed paths no step claims. Non-empty means the whole selection was returned."""

    universe_size: int
    """How many steps were offered. Not `len(STEPS)`: `--since` narrows whatever tier
    preceded it, so "everything" means everything in that tier."""

    @property
    def is_whole_gate(self) -> bool:
        return len(self.steps) == self.universe_size


def select_for_paths(paths: Sequence[str], steps: Sequence[Step] | None = None) -> Selection:
    """The steps a change to `paths` can affect, erring toward running too much.

    Two refusals rather than one, because under-selection is the failure that costs
    coverage and it can arrive from either direction:

    - a path no step claims means the attribution is incomplete for this change, so the
      whole gate runs. Returning the steps that happened to match would be an answer
      derived from an admittedly incomplete map.
    - a step that claims nothing is claimed by everything.

    An empty `paths` is not "nothing changed"; it is "nothing was determined", and it
    also selects the whole gate.
    """
    universe = STEPS if steps is None else tuple(steps)
    if not paths:
        return Selection(steps=universe, unattributed_paths=(), universe_size=len(universe))

    attributed = {
        path
        for path in paths
        if any(step.touches and step.reachable_from(path) for step in universe)
    }
    unclaimed = tuple(sorted(set(paths) - attributed))
    if unclaimed:
        return Selection(
            steps=universe, unattributed_paths=unclaimed, universe_size=len(universe)
        )

    reached = tuple(
        step for step in universe if any(step.reachable_from(path) for path in paths)
    )
    return Selection(steps=reached, unattributed_paths=(), universe_size=len(universe))


def _git(*args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=REPOSITORY_ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        raise UsageError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def changed_paths(since: str) -> list[str]:
    """Repo-relative paths changed against a git ref, including uncommitted work.

    Uncommitted changes are included deliberately: the question is "what do I need to run
    before pushing this", and a working tree the diff ignored would be exactly the change
    nobody checked.

    Four details, each of which silently under-reported before it was fixed, and an
    under-reported path is a step that does not run:

    - **`--no-renames`.** Rename detection reports only the destination, so moving a file
      out of an attributed subtree drops the path that named the steps it used to reach.
      Renaming `devtools/assess_frontier_rigidity.py` left the step that imports it by
      name unselected, and that step would then die with `ModuleNotFoundError`.
    - **The merge base, not the ref tip.** A two-dot diff compares against the tip, so a
      file this branch changed disappears from the answer once the base converges on the
      same content. The question is what this branch did, which is the three-dot one.
    - **`rev-parse --verify` and `--`.** Without them a `--since` value naming an existing
      path is taken as a pathspec: `--since packing` exits 0 and returns a pathspec-limited
      unstaged diff, dropping every committed change. Silent exactly when the argument
      looks plausible.
    - **`-z`.** With `core.quotePath` at its default a non-ASCII path arrives C-quoted,
      quotes included, and matches no pattern. That fails safe -- an unmatched path selects
      the whole gate -- but it defeats the feature for anyone with such a filename, and
      splitting on NUL fixes the leading/trailing-whitespace corruption at the same time.
    """
    resolved = _git("rev-parse", "--verify", "--quiet", f"{since}^{{commit}}").strip()
    if not resolved:
        raise UsageError(f"--since {since!r} does not name a commit")
    base = _git("merge-base", resolved, "HEAD").strip() or resolved

    out: set[str] = set()
    for args in (
        ("diff", "--name-only", "--no-renames", "-z", base, "--"),
        ("diff", "--name-only", "--no-renames", "-z"),
        ("diff", "--name-only", "--no-renames", "-z", "--cached"),
        ("ls-files", "--others", "--exclude-standard", "-z"),
    ):
        out |= {entry for entry in _git(*args).split("\0") if entry}
    return sorted(out)


def _select_steps(
    *, only: list[str], fast: bool, records: bool = False, edit: bool = False
) -> list[Step]:
    selected = [step for step in STEPS if not (fast or edit) or step.fast]
    if edit:
        selected = [step for step in selected if not step.broad]
    if records:
        selected = [step for step in selected if step.records]
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
    if (
        step.budget_seconds is not None
        and not context.timeout_is_explicit
        and step.budget_seconds > context.timeout_seconds
    ):
        context = replace(context, timeout_seconds=step.budget_seconds)
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
def _validation_activity(marker: Path) -> Iterator[None]:
    try:
        marker.mkdir()
    except FileExistsError as error:
        raise StepFailureError(
            f"validation marker already exists at {marker}; another gate may be running. "
            f"Wait for it, or delete {marker.name} if a crash left it behind."
        ) from error
    try:
        yield
    finally:
        marker.rmdir()


def _run_selected(
    selected: Sequence[Step], context: Context, patterns: list[str]
) -> RunSummary:
    started = time.perf_counter()
    with _validation_activity(ACTIVITY_MARKER):
        setup_output = _build_engine(context, selected)
        by_name: dict[str, StepResult] = {}
        with ThreadPoolExecutor(max_workers=context.jobs) as pool:
            futures = {
                pool.submit(_execute_step, step, context): step.name for step in selected
            }
            try:
                for future in as_completed(futures):
                    result = future.result()
                    by_name[result.name] = result
            except BaseException:
                for future in futures:
                    future.cancel()
                context.processes.stop()
                raise
    ordered = [by_name[step.name] for step in selected]
    return RunSummary(
        results=ordered,
        wall_seconds=time.perf_counter() - started,
        setup_output=setup_output,
        selected_count=len(selected),
        total_count=len(STEPS),
        partial_pattern=patterns,
    )


def _summary_status(summary: RunSummary, *, strict: bool) -> int:
    failed = any(result.status == "failed" for result in summary.results)
    skipped = any(result.status == "skipped" for result in summary.results)
    return 1 if failed or (strict and skipped) else 0


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
        noun = "STEP" if len(failed) == 1 else "STEPS"
        print(f"{len(failed)} {noun} FAILED:")
        for result in failed:
            print(f"  - {result.name}")
        return _summary_status(summary, strict=strict)
    if skipped:
        print(f"VALIDATION COMPLETED, BUT {len(skipped)} CHECKS WERE SKIPPED:")
        for result in skipped:
            print(f"  - {result.name}: {result.reason}")
        if strict:
            print("strict mode: a skipped check is not a passed check", file=sys.stderr)
            return _summary_status(summary, strict=strict)
    if summary.selected_count != summary.total_count:
        qualifier = (
            f"--only {summary.partial_pattern!r}" if summary.partial_pattern else "a named tier"
        )
        print(
            f"{summary.selected_count} of {summary.total_count} STEPS PASSED "
            f"({qualifier}; this is not the full gate)"
        )
    else:
        print("ALL CHECKS PASSED")
    return _summary_status(summary, strict=strict)


def _parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="packing-validate",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--edit",
        action="store_true",
        help="run the edit-loop checks: everything in --fast except the broad test suite",
    )
    parser.add_argument("--fast", action="store_true", help="run the fast edit-loop checks")
    parser.add_argument(
        "--records",
        action="store_true",
        help="run only the record checks: registries, generated views, declared contracts",
    )
    parser.add_argument(
        "--since",
        metavar="REF",
        help=(
            "run only the steps a change against REF can affect, including uncommitted "
            "work; a path no step claims selects the whole gate"
        ),
    )
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
        "--timeout-seconds",
        metavar="SECONDS",
        help=(
            "maximum time for each validation subprocess (default: 900; also "
            "PACKING_VALIDATE_TIMEOUT_SECONDS)"
        ),
    )
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


def _validate_invocation(
    *,
    strict: bool,
    only: list[str],
    fast: bool,
    records: bool = False,
    edit: bool = False,
    since: str | None = None,
) -> None:
    if strict and (only or fast or records or edit or since):
        raise UsageError(
            "--strict cannot be combined with --only, --fast, --records, --edit, or --since"
        )
    if edit and fast:
        raise UsageError(
            "--edit and --fast select different tiers; --fast is the wider of the two"
        )


def _validate_runtime() -> None:
    if sys.version_info[:2] != SUPPORTED_PYTHON:
        raise UsageError(f"Python 3.14 is required, running {sys.version.split()[0]}")


def main(arguments: list[str] | None = None) -> int:
    """Run validation and return a process-compatible status code."""
    parser = _parser()
    try:
        namespace = parser.parse_args(arguments)
        strict = namespace.strict or _environment_flag("PACKING_VALIDATE_STRICT")
        deep = namespace.deep or _environment_flag("PACKING_VALIDATE_DEEP") or strict
        _validate_invocation(
            strict=strict,
            only=namespace.only,
            fast=namespace.fast,
            records=namespace.records,
            edit=namespace.edit,
            since=namespace.since,
        )
        jobs_value = namespace.jobs or os.environ.get("PACKING_VALIDATE_JOBS")
        jobs = (
            _positive_integer("--jobs", jobs_value)
            if jobs_value is not None
            else (os.process_cpu_count() or DEFAULT_CPU_COUNT)
        )
        inner_value = namespace.inner_jobs or os.environ.get("PACKING_VALIDATE_INNER_JOBS")
        inner_jobs = (
            _positive_integer("--inner-jobs", inner_value)
            if inner_value is not None
            else max(1, jobs // INNER_JOB_DIVISOR)
        )
        if namespace.timeout_seconds is not None:
            timeout_name = "--timeout-seconds"
            timeout_value = namespace.timeout_seconds
        else:
            timeout_name = "PACKING_VALIDATE_TIMEOUT_SECONDS"
            timeout_value = os.environ.get(timeout_name)
        timeout_is_explicit = timeout_value is not None
        timeout_seconds = (
            _positive_seconds(timeout_name, timeout_value)
            if timeout_value is not None
            else DEFAULT_TIMEOUT_SECONDS
        )
        _validate_runtime()
        require_project_root(PROJECT_ROOT)
        selected = _select_steps(
            only=namespace.only,
            fast=namespace.fast,
            records=namespace.records,
            edit=namespace.edit,
        )
        if namespace.since:
            paths = changed_paths(namespace.since)
            selection = select_for_paths(paths, selected)
            selected = list(selection.steps)
            print(f"== change-scoped against {namespace.since}: {len(paths)} paths ==")
            if selection.unattributed_paths:
                shown = ", ".join(selection.unattributed_paths[:5])
                more = (
                    f" (+{len(selection.unattributed_paths) - 5} more)"
                    if len(selection.unattributed_paths) > 5
                    else ""
                )
                print(f"  no step claims {shown}{more}; running the whole selection")
            else:
                print(f"  {len(selected)} steps reachable from those paths")
            print()
        if namespace.list:
            records = [{"name": step.name, "tags": step.tags} for step in selected]
            if namespace.format == "json":
                print(json.dumps(records, indent=2))
            else:
                for step in selected:
                    print(f"{step.name} [{step.tags}]")
            return 0
        environment = os.environ.copy()
        environment["PACK_JOBS"] = str(inner_jobs)
        context = Context(
            deep=deep,
            strict=strict,
            jobs=jobs,
            inner_jobs=inner_jobs,
            environment=environment,
            timeout_seconds=timeout_seconds,
            timeout_is_explicit=timeout_is_explicit,
        )
        summary = _run_selected(selected, context, namespace.only)
    except ParserExitError as error:
        if error.message:
            stream = sys.stdout if error.status == 0 else sys.stderr
            print(error.message, end="", file=stream)
        return error.status
    except (UsageError, StepFailureError, ProjectLayoutError) as error:
        print(f"packing-validate: error: {error}", file=sys.stderr)
        return 2 if isinstance(error, (UsageError, ProjectLayoutError)) else 1

    if namespace.format == "json":
        print(json.dumps(asdict(summary), indent=2))
        return _summary_status(summary, strict=strict)
    return _render_text(summary, strict=strict)


if __name__ == "__main__":
    raise SystemExit(main())
