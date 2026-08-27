"""Run the packing project's refactor, evidence, and infrastructure checks.

The command is read-only. Checks run concurrently, but their captured output is
replayed in the declared order so two runs remain comparable. Use `--fast` while
editing, `--only TEXT` for one named surface, the default command before a commit, and
`--strict` before an unattended research session or merge.
"""

from __future__ import annotations

import argparse
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
from dataclasses import asdict, dataclass, field
from pathlib import Path
from threading import Lock
from typing import Literal, Never, override

import yaml

from sqpack.project import (
    ProjectLayoutError,
    configured_project_root,
    require_project_root,
)

PROJECT_ROOT = configured_project_root()
REPOSITORY_ROOT = PROJECT_ROOT.parents[1]
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
        ),
    )
    _require_text(
        output,
        "known-best atlas check passed: 100 sources/plans, witnesses, renders, and links",
        "chunk census check passed: components, contacts, and bounded lattice partitions "
        "for 100 records",
        "known-best contact overlay check passed: 5 house-rendered calibration strata",
        "known-best chunk evidence profile check passed: 36 non-grid calibration cases",
        "contact enumeration pricing check passed",
        "contact full-cell control check passed",
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
        "prospective source map check passed: 224 cases, availability only",
        "prospective atlas seed check passed: 101 witnesses and 101 house renderings",
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
        data = yaml.safe_load(path.read_text(encoding="utf-8").split("---\n")[1])
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
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
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
    return _module(context, "sqpack.campaign.ledger", "check")


STEPS: tuple[Step, ...] = (
    Step("soundness perimeter", _soundness_perimeter, needs_engine=True),
    Step("lint floor (python)", _python_quality, fast=True),
    Step("basin atlas", _basin_atlas),
    Step("basin event record and replay", _basin_events),
    Step("historical regressions", _historical_regressions),
    Step("small-n exact models and local geometry", _small_n),
    Step("deterministic SVG rendering", _svg_rendering),
    Step("known-best n=1..100 atlas", _known_best_atlas),
    Step("prospective n=101..324 source map and safe seed", _prospective_atlas),
    Step("abstract size-five contact-scaffold atlas", _contact_scaffold_atlas),
    Step("negative controls", _negative_controls),
    Step("fixed-angle cell is an LP, rebuilt independently", _independent_lp),
    Step("fast behavioral tests", _fast_tests, fast=True),
    Step("exhaustive exact behavioral tests", _exhaustive_exact_tests),
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
    Step("verifier perturbation limits", _verifier_limits, fast=True),
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
            f"--only {summary.partial_pattern!r}" if summary.partial_pattern else "--fast"
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


def _validate_invocation(*, strict: bool, only: list[str], fast: bool) -> None:
    if strict and (only or fast):
        raise UsageError("--strict cannot be combined with --only or --fast")


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
        _validate_invocation(strict=strict, only=namespace.only, fast=namespace.fast)
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
        timeout_seconds = (
            _positive_seconds(timeout_name, timeout_value)
            if timeout_value is not None
            else DEFAULT_TIMEOUT_SECONDS
        )
        _validate_runtime()
        require_project_root(PROJECT_ROOT)
        selected = _select_steps(only=namespace.only, fast=namespace.fast)
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
