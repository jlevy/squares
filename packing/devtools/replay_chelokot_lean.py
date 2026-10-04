#!/usr/bin/env python3
# ruff: noqa: RUF001 -- the Lean statement is matched as written, with its natural-number sign.
"""Replay chelokot's Lean proof that s(n^2 - 2) = n, and retain an axiom receipt.

After Karakuş (arXiv:2609.37410v1) showed Nagamochi 2005 Lemma 1 false, the register's
`s(k^2 - 2) = k` rests on one source: chelokot/square-packing-archive at commit 753079eb,
which states `Records.NearSquare.squareMinusTwo_isMinimumSide` for every `n >= 2` and whose
CI asserts that the proof uses only the standard axioms. Nobody here had built it, so the
claim sat at `V0`/`C0`. This tool is the replay, kept as a tool rather than a one-off
(OR-1): given a working directory outside the repository it clones the archive, checks out
the pinned commit, takes Mathlib's prebuilt cache, builds the library with the pinned
toolchain, runs the archive's own axiom assertions again, runs its policy test, prints the
axioms of the final theorem and of its instances, and writes a receipt.

Steps, in order; the first failure stops the run and is retained as a failure receipt
(which step, the error in the log), because a failed replay is a result:

  clone, checkout       the archive at the pinned commit
  pins                  the toolchain file, the manifest's Mathlib revision, the statement
                        text, and a scan of every `.lean` file for `sorry`, a custom
                        `axiom`, and `native_decide`
  toolchain             elan, lake and lean versions, which also installs the pinned Lean
  cache                 `lake exe cache get`: Mathlib's prebuilt oleans, never a source build
  build                 `lake build`, the whole library, which imports `ManifestEvidence`
                        (79 `assert_standard_axioms`) and `Audit` (its `#print axioms`)
  manifest-evidence     `lean ManifestEvidence.lean` again, on its own, so the assertions
                        ran in this replay and are not only a cached build artifact
  policy-test           the archive's `test_lean_axiom_policy.py`: the assertion command
                        rejects `sorryAx`, a custom axiom and `native_decide`
  axioms                `#print axioms` and `assert_standard_axioms` on the theorem and on
                        its instances, from a scratch file that imports the archive
  definitions           `#print` of the definitions the statement is made of

The receipt is `receipt.json` beside the trimmed `build.log` it hashes. `--check` validates
the retained pair offline: structure, commit, toolchain, the theorem name and statement, the
axiom list being exactly `propext`, `Classical.choice` and `Quot.sound` for the theorem and
every instance, and the log's sha256. It reads two small files and runs in milliseconds.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.replay_chelokot_lean \\
        --run --workdir /path/outside/the/repository [--fresh-build]
    uv run --frozen --all-extras --group dev python -m devtools.replay_chelokot_lean --check

`--fresh-build` removes only the archive's own `formal/.lake/build` first, so the timed build
is the archive's modules from source over the Mathlib cache.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RECEIPT_DIR = (
    ROOT / "campaign/series/series-000-smoke-and-calibration/results/chelokot-lean-replay"
)
RECEIPT_NAME = "receipt.json"
LOG_NAME = "build.log"

SCHEMA = "chelokot-lean-replay/1"
BEAD = "think-ym34"

ARCHIVE_URL = "https://github.com/chelokot/square-packing-archive"
ARCHIVE_COMMIT = "753079eb37d8d16225a5dc1f56e493a3c3b243f4"
ARCHIVE_COMMITTED = "2026-09-06T00:42:12+03:00"
TOOLCHAIN = "leanprover/lean4:v4.33.0"
MATHLIB_REV = "db584cd6d46c92f209a44c0f1c829460d327499d"
LEAN_VERSION = "4.33.0"

STANDARD_AXIOMS = ("Classical.choice", "Quot.sound", "propext")
"""Lean's three standard axioms, sorted, as `Lean.collectAxioms` reports them."""

THEOREM = "SquarePackingArchive.Records.NearSquare.squareMinusTwo_isMinimumSide"
THEOREM_FILE = "formal/SquarePackingArchive/NagamochiPackingTheorem.lean"
THEOREM_SOURCE = (
    "theorem Records.NearSquare.squareMinusTwo_isMinimumSide\n"
    "    {size : ℕ} (size_lower : 2 ≤ size) :\n"
    "    IsMinimumSide (size * size - 2) size"
)
"""The declaration header as written in the archive, up to `:= by`."""

THEOREM_ELABORATED = (
    "SquarePackingArchive.Records.NearSquare.squareMinusTwo_isMinimumSide {size : ℕ} "
    "(size_lower : 2 ≤ size) : SquarePackingArchive.IsMinimumSide (size * size - 2) ↑size"
)
"""What `#check` prints for the theorem, on one line, with the cast `↑size` made visible."""

GEOMETRY_FILE = "formal/SquarePackingArchive/Geometry.lean"
MANIFEST_FILE = "formal/SquarePackingArchive/ManifestEvidence.lean"
PINNED_BLOBS = {
    THEOREM_FILE: "da209bad1b6739f52f4b74c1af9b2ca6e788c6d1",
    GEOMETRY_FILE: "4398066bab5a90c9b65b403509b65941e89b5b3d",
}
"""Git blob ids of the two files whose text the statement-fidelity reading rests on."""

MANIFEST_ASSERTIONS = 79
"""`assert_standard_axioms` commands in the generated `ManifestEvidence.lean` at the pin."""

INSTANCE_DECLARATIONS = (
    "SquarePackingArchive.Records.NearSquare.s2_eq_two",
    "SquarePackingArchive.Records.Square7.s7_eq_three",
    "SquarePackingArchive.Records.NearSquare.s14_eq_four",
    "SquarePackingArchive.Records.NearSquare.s62_eq_eight",
    "SquarePackingArchive.Records.NearSquare.s79_eq_nine",
    "SquarePackingArchive.Records.NearSquare.s98_eq_ten",
    "replay_s23_eq_five",
    "replay_s34_eq_six",
    "replay_s47_eq_seven",
)
"""Instances whose axioms are printed: the archive's own, and the register's other values."""

REPLAY_INSTANCES = ((23, 5), (34, 6), (47, 7))
"""`(N, k)` with `N = k^2 - 2` for the register's consumers the archive names no theorem for."""

DEFINITIONS = (
    "SquarePackingArchive.IsMinimumSide",
    "SquarePackingArchive.IsLowerBound",
    "SquarePackingArchive.HasPacking",
    "SquarePackingArchive.Packing",
    "SquarePackingArchive.PlacedSquare",
    "SquarePackingArchive.Frame",
    "SquarePackingArchive.PlacedSquare.point",
    "SquarePackingArchive.PlacedSquare.Contains",
    "SquarePackingArchive.PlacedSquare.InteriorContains",
    "SquarePackingArchive.Container.Contains",
    "SquarePackingArchive.PlacedSquare.Fits",
    "SquarePackingArchive.PlacedSquare.InteriorDisjoint",
)

STEP_NAMES = (
    "clone",
    "checkout",
    "pins",
    "toolchain",
    "cache",
    "build",
    "manifest-evidence",
    "policy-test",
    "axioms",
    "definitions",
)

STATEMENT_READING = (
    "Read from Geometry.lean at the pinned commit. A PlacedSquare is a centre and a Frame "
    "(cosine, sine, cosine^2 + sine^2 = 1), so rotation is arbitrary; Contains is the "
    "closed unit square (|x'| <= 1/2, |y'| <= 1/2 in local coordinates); Container.Contains "
    "side is the closed square [0, side]^2; Packing n side is n placed squares indexed by "
    "Fin n, each Fits (every point of the closed unit square lies in the closed container) "
    "and any two distinct indices InteriorDisjoint (no common point of the open unit "
    "squares), so boundary contact is allowed; IsMinimumSide n s is HasPacking n s and "
    "s <= every side that has a packing. That is the register's s(N): the side of the "
    "smallest square holding N non-overlapping unit squares, rotations allowed. "
    "Differences that do not change the value: reals are Mathlib's, the container is "
    "axis-aligned at the origin (every square container is congruent to it), a Frame has "
    "no reflection (a square is symmetric under it), and the theorem's count "
    "`size * size - 2` is natural-number subtraction, exact for size >= 2. The theorem "
    "covers the closed-square container only, as the register's s(N) does. This is a "
    "reading of the definitions by the author of this receipt, not a human formalization "
    "review."
)

AXIOMS_REPORT = re.compile(r"'([^']+)' depends on axioms: \[([^\]]*)\]")
AXIOMS_NONE = re.compile(r"'([^']+)' does not depend on any axioms")
AXIOM_DECLARATION = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable|unsafe)\s+)*axiom\s+\S",
    re.MULTILINE,
)
ANSI = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
UNITTEST_RAN = re.compile(r"^Ran (\d+) tests? in ", re.MULTILINE)
LEAN_FILE_SKIP = {".lake"}

HEAD_LINES = 100
TAIL_LINES = 1500
STEP_TIMEOUT_SECONDS = {"clone": 900, "cache": 7200, "build": 4 * 3600}
DEFAULT_TIMEOUT_SECONDS = 3600


# --- Parsing -------------------------------------------------------------------------


def parse_print_axioms(text: str) -> dict[str, tuple[str, ...]]:
    """Map each declaration in `#print axioms` output to its sorted, de-duplicated axioms.

    Lean wraps long messages, so whitespace is collapsed before matching. A report that
    is present but not matched (truncated, or in a format this parser does not know) is
    an error rather than a missing entry, because a missed `sorryAx` must not read as a
    clean receipt.
    """
    flat = " ".join(text.split())
    reports: dict[str, tuple[str, ...]] = {}
    for match in AXIOMS_REPORT.finditer(flat):
        names = tuple(
            sorted({part.strip() for part in match.group(2).split(",") if part.strip()})
        )
        record(reports, match.group(1), names)
    for match in AXIOMS_NONE.finditer(flat):
        record(reports, match.group(1), ())
    seen = flat.count("depends on axioms") + flat.count("does not depend on any axioms")
    if seen != len(AXIOMS_REPORT.findall(flat)) + len(AXIOMS_NONE.findall(flat)):
        raise ValueError("an axiom report in the output did not match the expected format")
    return reports


def record(reports: dict[str, tuple[str, ...]], name: str, axioms: tuple[str, ...]) -> None:
    if reports.setdefault(name, axioms) != axioms:
        raise ValueError(f"{name} is reported twice with different axioms")


def format_axioms_report(declaration: str, axioms: Sequence[str]) -> str:
    """The line `#print axioms` prints, for building synthetic output in tests."""
    if not axioms:
        return f"'{declaration}' does not depend on any axioms"
    return f"'{declaration}' depends on axioms: [{', '.join(axioms)}]"


def tidy_output(text: str) -> str:
    """Strip ANSI escapes, keep the last state of each carriage-return progress line."""
    lines = []
    for raw in ANSI.sub("", text).split("\n"):
        segments = [part for part in raw.rstrip("\r").split("\r") if part.strip()]
        lines.append((segments[-1] if segments else "").rstrip())
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def trim_output(text: str, head: int = HEAD_LINES, tail: int = TAIL_LINES) -> str:
    """The output, tidied, with the middle elided when it is longer than head + tail."""
    lines = tidy_output(text).split("\n")
    if len(lines) <= head + tail:
        return "\n".join(lines)
    elided = len(lines) - head - tail
    return "\n".join([*lines[:head], f"[... {elided} lines elided ...]", *lines[-tail:]])


def elaborated_statement(output: str) -> str | None:
    """The `#check` text of the theorem in the axioms run's output, on one line, or None."""
    flat = tidy_output(output)
    start = flat.find(f"{THEOREM} {{")
    if start < 0:
        return None
    end = flat.find("\n'", start)
    return " ".join(flat[start : end if end >= 0 else len(flat)].split())


def source_statement(text: str) -> str | None:
    """The theorem's declaration header in the archive's source, up to `:=`."""
    marker = "theorem Records.NearSquare.squareMinusTwo_isMinimumSide\n"
    start = text.find(marker)
    if start < 0:
        return None
    end = text.find(" :=", start)
    return text[start:end].rstrip() if end >= 0 else None


# --- The scratch Lean files ----------------------------------------------------------


def axioms_source() -> str:
    """The scratch file for the `axioms` step: the theorem, the archive's own instances, and
    the register's other values, each with `#print axioms`, the theorem also asserted."""
    lines = [
        "import SquarePackingArchive",
        "import SquarePackingArchive.EvidenceAudit",
        "",
        f"#check {THEOREM}",
        f"#print axioms {THEOREM}",
        f"assert_standard_axioms {THEOREM}",
        "",
    ]
    for count, size in REPLAY_INSTANCES:
        lines += [
            f"theorem replay_s{count}_eq_{NUMBER_WORDS[size]} :",
            f"    SquarePackingArchive.IsMinimumSide {count} {size} := by",
            f"  simpa using ({THEOREM} (size := {size}) (by norm_num))",
            "",
        ]
    lines += [f"#print axioms {name}" for name in INSTANCE_DECLARATIONS]
    lines += [f"assert_standard_axioms {name}" for name in INSTANCE_DECLARATIONS]
    return "\n".join(lines) + "\n"


NUMBER_WORDS = {5: "five", 6: "six", 7: "seven"}


def definitions_source() -> str:
    """The scratch file for the `definitions` step: `#print` of the statement's definitions."""
    lines = ["import SquarePackingArchive", ""]
    lines += [f"#print {name}" for name in DEFINITIONS]
    return "\n".join(lines) + "\n"


# --- Running commands ----------------------------------------------------------------


@dataclass(frozen=True)
class CommandResult:
    argv: tuple[str, ...]
    returncode: int
    output: str
    seconds: float


type Runner = Callable[[Sequence[str], Path, float], CommandResult]


def tool_environment() -> dict[str, str]:
    """The environment for the Lean tools: elan's bin directory first, plain output."""
    environment = dict(os.environ)
    elan_bin = Path(environment.get("ELAN_HOME", str(Path.home() / ".elan"))) / "bin"
    if elan_bin.is_dir():
        environment["PATH"] = f"{elan_bin}{os.pathsep}{environment.get('PATH', '')}"
    environment["NO_COLOR"] = "1"
    return environment


def run_command(argv: Sequence[str], cwd: Path, timeout: float) -> CommandResult:
    """Run one command, echoing its lines to stderr as they arrive, killing it at timeout."""
    started = time.monotonic()
    try:
        process = subprocess.Popen(
            list(argv),
            cwd=cwd,
            env=tool_environment(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except OSError as error:
        return CommandResult(tuple(argv), 127, f"could not start {argv[0]}: {error}", 0.0)
    timer = threading.Timer(timeout, process.kill)
    timer.start()
    chunks: list[bytes] = []
    try:
        assert process.stdout is not None
        for chunk in iter(process.stdout.readline, b""):
            chunks.append(chunk)
            echo = tidy_output(chunk.decode("utf-8", "replace"))
            if echo:
                print(f"    {echo}", file=sys.stderr, flush=True)
        returncode = process.wait()
    finally:
        timer.cancel()
    return CommandResult(
        tuple(argv),
        returncode,
        b"".join(chunks).decode("utf-8", "replace"),
        time.monotonic() - started,
    )


# --- The replay ----------------------------------------------------------------------


@dataclass
class StepResult:
    commands: list[str]
    returncode: int
    output: str


@dataclass
class Replay:
    workdir: Path
    runner: Runner = run_command
    fresh_build: bool = False
    notes: Sequence[str] = ()
    rebuild: Sequence[str] = ()
    steps: list[dict[str, Any]] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)
    facts: dict[str, Any] = field(default_factory=dict)

    @property
    def repo(self) -> Path:
        return self.workdir / "square-packing-archive"

    @property
    def formal(self) -> Path:
        return self.repo / "formal"

    def run(self) -> dict[str, Any]:
        """Run the steps in order until one fails; return the receipt (log not yet written)."""
        actions: dict[str, Callable[[], StepResult]] = {
            "clone": self.clone,
            "checkout": self.checkout,
            "pins": self.pins,
            "toolchain": self.toolchain,
            "cache": self.cache,
            "build": self.build,
            "manifest-evidence": self.manifest_evidence,
            "policy-test": self.policy_test,
            "axioms": self.axioms,
            "definitions": self.definitions,
        }
        failed: str | None = None
        for name in STEP_NAMES:
            print(f"== {name}", file=sys.stderr, flush=True)
            started = time.monotonic()
            try:
                result = actions[name]()
            except OSError as error:
                result = StepResult([], 1, f"{type(error).__name__}: {error}")
            seconds = round(time.monotonic() - started, 1)
            self.steps.append(
                {
                    "name": name,
                    "commands": result.commands,
                    "returncode": result.returncode,
                    "seconds": seconds,
                }
            )
            self.sections.append(
                f"=== step: {name} ===\n"
                + "".join(f"$ {command}\n" for command in result.commands)
                + trim_output(result.output)
                + f"\n=== end: {name} returncode={result.returncode} seconds={seconds} ===\n"
            )
            if result.returncode != 0:
                failed = name
                break
        return self.receipt(failed)

    def sh(self, commands: Sequence[Sequence[str]], cwd: Path, name: str) -> StepResult:
        """Run commands in order, stop at the first failure, join their output."""
        timeout = STEP_TIMEOUT_SECONDS.get(name, DEFAULT_TIMEOUT_SECONDS)
        shown: list[str] = []
        output: list[str] = []
        for argv in commands:
            result = self.runner(argv, cwd, timeout)
            shown.append(shlex.join(argv))
            output.append(result.output)
            if result.returncode != 0:
                return StepResult(shown, result.returncode, "\n".join(output))
        return StepResult(shown, 0, "\n".join(output))

    def clone(self) -> StepResult:
        if (self.repo / ".git").is_dir():
            return StepResult([], 0, f"reusing the existing clone at {self.repo}")
        return self.sh([["git", "clone", ARCHIVE_URL, str(self.repo)]], self.workdir, "clone")

    def checkout(self) -> StepResult:
        return self.sh(
            [
                ["git", "checkout", "--detach", ARCHIVE_COMMIT],
                ["git", "rev-parse", "HEAD"],
                ["git", "status", "--porcelain", "--untracked-files=no"],
            ],
            self.repo,
            "checkout",
        )

    def pins(self) -> StepResult:
        """Check the pins the receipt rests on and scan the sources; no tool is run."""
        problems: list[str] = []
        head = self.runner(["git", "rev-parse", "HEAD"], self.repo, 60)
        if head.output.strip() != ARCHIVE_COMMIT:
            problems.append(f"HEAD is {head.output.strip()!r}, not {ARCHIVE_COMMIT}")
        status = self.runner(
            ["git", "status", "--porcelain", "--untracked-files=no"], self.repo, 60
        )
        if status.output.strip():
            problems.append(f"tracked files differ from the commit:\n{status.output.strip()}")
        toolchain = (self.formal / "lean-toolchain").read_text(encoding="utf-8").strip()
        if toolchain != TOOLCHAIN:
            problems.append(f"lean-toolchain is {toolchain!r}, not {TOOLCHAIN!r}")
        manifest = json.loads((self.formal / "lake-manifest.json").read_text(encoding="utf-8"))
        revisions = {package["name"]: package["rev"] for package in manifest["packages"]}
        if revisions.get("mathlib") != MATHLIB_REV:
            problems.append(f"Mathlib is at {revisions.get('mathlib')!r}, not {MATHLIB_REV}")
        blobs = {}
        for path in PINNED_BLOBS:
            blob = self.runner(["git", "rev-parse", f"{ARCHIVE_COMMIT}:{path}"], self.repo, 60)
            blobs[path] = blob.output.strip()
        theorem_text = (self.repo / THEOREM_FILE).read_text(encoding="utf-8")
        statement = source_statement(theorem_text)
        if statement != THEOREM_SOURCE:
            problems.append(f"the theorem's declaration header changed: {statement!r}")
        manifest_text = (self.repo / MANIFEST_FILE).read_text(encoding="utf-8")
        assertions = len(re.findall(r"^assert_standard_axioms ", manifest_text, re.MULTILINE))
        scan = scan_sources(self.formal)
        scan["manifest_assertions"] = assertions
        self.facts.update(
            blobs=blobs,
            statement_source=statement,
            source_scan=scan,
            mathlib_rev=revisions.get("mathlib"),
            toolchain_file=toolchain,
        )
        output = json.dumps(
            {"blobs": blobs, "source_scan": scan, "mathlib_rev": revisions.get("mathlib")},
            indent=2,
        )
        if assertions != MANIFEST_ASSERTIONS:
            problems.append(
                f"ManifestEvidence has {assertions} assertions, not {MANIFEST_ASSERTIONS}"
            )
        problems.extend(
            f"the sources contain {scan[key]} occurrence(s) of {key}"
            for key in ("sorry", "axiom_declarations", "native_decide")
            if scan[key]
        )
        return StepResult(
            ["internal: pins and source scan"],
            1 if problems else 0,
            "\n".join([*problems, output]),
        )

    def toolchain(self) -> StepResult:
        result = self.sh(
            [["elan", "--version"], ["lake", "--version"], ["lean", "--version"]],
            self.formal,
            "toolchain",
        )
        versions = [line for line in tidy_output(result.output).split("\n") if line.strip()]
        self.facts["tool_versions"] = versions
        return result

    def cache(self) -> StepResult:
        return self.sh([["lake", "exe", "cache", "get"]], self.formal, "cache")

    def build(self) -> StepResult:
        fresh = self.formal / ".lake" / "build"
        removed = ""
        if self.fresh_build and fresh.is_dir():
            shutil.rmtree(fresh)
            removed = f"removed {fresh} so the archive's modules build from source\n"
        for module in self.rebuild:
            products = module_products(self.formal, module)
            for product in products:
                product.unlink()
            removed += (
                f"removed {len(products)} build products of {module}, to elaborate it again\n"
            )
        self.facts["fresh_archive_build"] = self.fresh_build
        self.facts["rebuilt_modules"] = list(self.rebuild)
        result = self.sh([["lake", "build"]], self.formal, "build")
        result.output = removed + result.output
        return result

    def manifest_evidence(self) -> StepResult:
        result = self.sh(
            [["lake", "env", "lean", "SquarePackingArchive/ManifestEvidence.lean"]],
            self.formal,
            "manifest-evidence",
        )
        if result.returncode == 0 and tidy_output(result.output):
            result.returncode = 1
            result.output = "unexpected output from the assertions:\n" + result.output
        return result

    def policy_test(self) -> StepResult:
        result = self.sh(
            [
                [
                    sys.executable,
                    "-S",
                    "-m",
                    "unittest",
                    "discover",
                    "-v",
                    "-s",
                    "../scripts",
                    "-p",
                    "test_lean_axiom_policy.py",
                ]
            ],
            self.formal,
            "policy-test",
        )
        match = UNITTEST_RAN.search(result.output)
        self.facts["policy_tests_run"] = int(match.group(1)) if match else 0
        return result

    def axioms(self) -> StepResult:
        scratch = self.workdir / "ReplayAxioms.lean"
        scratch.write_text(axioms_source(), encoding="utf-8")
        result = self.sh([["lake", "env", "lean", str(scratch)]], self.formal, "axioms")
        self.facts["axioms_raw"] = tidy_output(result.output)
        return result

    def definitions(self) -> StepResult:
        scratch = self.workdir / "ReplayDefinitions.lean"
        scratch.write_text(definitions_source(), encoding="utf-8")
        return self.sh([["lake", "env", "lean", str(scratch)]], self.formal, "definitions")

    def receipt(self, failed: str | None) -> dict[str, Any]:
        """The receipt for the steps run so far; the log hash is filled in by `retain`."""
        axioms_raw = self.facts.get("axioms_raw", "")
        reported: dict[str, list[str]] = {}
        if failed is None:
            reported = {
                name: list(found) for name, found in parse_print_axioms(axioms_raw).items()
            }
        scan = self.facts.get("source_scan", {})
        return {
            "schema": SCHEMA,
            "bead": BEAD,
            "recorded_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "passed" if failed is None else "failed",
            "failed_step": failed,
            "archive": {
                "url": ARCHIVE_URL,
                "commit": ARCHIVE_COMMIT,
                "committed": ARCHIVE_COMMITTED,
                "blobs": self.facts.get("blobs", {}),
            },
            "toolchain": {
                "lean_toolchain": self.facts.get("toolchain_file", ""),
                "mathlib_rev": self.facts.get("mathlib_rev", ""),
                "tool_versions": self.facts.get("tool_versions", []),
            },
            "host": {"platform": platform.platform(), "cpus": os.cpu_count()},
            "fresh_archive_build": self.facts.get("fresh_archive_build", False),
            "rebuilt_modules": self.facts.get("rebuilt_modules", []),
            "steps": self.steps,
            "wall_seconds": round(sum(step["seconds"] for step in self.steps), 1),
            "theorem": {
                "name": THEOREM,
                "statement_source": self.facts.get("statement_source", ""),
                "statement_elaborated": elaborated_statement(axioms_raw) or "",
            },
            "axioms": {"raw": axioms_raw, "reported": reported},
            "archive_assertions": {
                "module": "SquarePackingArchive.ManifestEvidence",
                "assert_standard_axioms_count": scan.get("manifest_assertions", 0),
            },
            "policy_test": {"tests_run": self.facts.get("policy_tests_run", 0)},
            "source_scan": {
                key: scan.get(key, 0)
                for key in ("lean_files", "sorry", "axiom_declarations", "native_decide")
            },
            "notes": list(self.notes),
            "statement_reading": STATEMENT_READING,
        }


MODULE_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)*$")


def module_products(formal: Path, module: str) -> list[Path]:
    """The build products of one module under `.lake/build`, so Lake must elaborate it again.

    A module `A.B.C` leaves `C.olean`, `C.ilean`, `C.trace`, `C.hash` and friends in
    `lib/lean/A/B`, and its generated C in `ir/A/B`; the match is on the stem followed by
    a dot, so `Audit` never takes `AuditExtra`. The module's own directory is left alone.
    """
    if not MODULE_NAME.match(module):
        raise ValueError(f"{module!r} is not a Lean module name")
    *parents, stem = module.split(".")
    products: list[Path] = []
    for kind in ("lib/lean", "ir"):
        directory = formal / ".lake" / "build" / kind
        for part in parents:
            directory /= part
        if directory.is_dir():
            products += sorted(path for path in directory.glob(f"{stem}.*") if path.is_file())
    return products


def scan_sources(formal: Path) -> dict[str, int]:
    """Count `.lean` files and the words CI and the axiom policy forbid, outside `.lake`."""
    counts = {"lean_files": 0, "sorry": 0, "axiom_declarations": 0, "native_decide": 0}
    files = [formal / "SquarePackingArchive.lean"]
    files += sorted((formal / "SquarePackingArchive").rglob("*.lean"))
    for path in files:
        text = path.read_text(encoding="utf-8")
        counts["lean_files"] += 1
        counts["sorry"] += len(re.findall(r"\bsorry\b", text))
        counts["axiom_declarations"] += len(re.findall(AXIOM_DECLARATION, text))
        counts["native_decide"] += len(re.findall(r"\bnative_decide\b", text))
    return counts


def retain(receipt: dict[str, Any], sections: Sequence[str], out_dir: Path) -> None:
    """Write the trimmed log and the receipt that hashes it."""
    out_dir.mkdir(parents=True, exist_ok=True)
    log = "\n".join(sections).encode("utf-8")
    (out_dir / LOG_NAME).write_bytes(log)
    receipt["build_log"] = {
        "path": LOG_NAME,
        "sha256": hashlib.sha256(log).hexdigest(),
        "bytes": len(log),
        "lines": log.count(b"\n"),
    }
    (out_dir / RECEIPT_NAME).write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# --- The offline check ---------------------------------------------------------------


def expect(problems: list[str], condition: object, message: str) -> None:
    if not condition:
        problems.append(message)


def validate_receipt(receipt: Mapping[str, Any], log: bytes) -> list[str]:
    """Every problem with a receipt and the log it hashes; an empty list is a valid receipt."""
    problems: list[str] = []
    expect(problems, receipt.get("schema") == SCHEMA, f"schema is not {SCHEMA}")
    notes = receipt.get("notes", [])
    expect(
        problems,
        isinstance(notes, list) and all(isinstance(note, str) for note in notes),
        "notes is not a list of strings",
    )
    status = receipt.get("status")
    expect(
        problems, status in {"passed", "failed"}, f"status {status!r} is not passed or failed"
    )
    check_pins(receipt, problems)
    check_steps(receipt, problems)
    check_log(receipt, log, problems)
    if status == "passed":
        check_theorem(receipt, problems)
        check_axioms(receipt, problems)
        check_assertions(receipt, problems)
    elif status == "failed":
        steps = receipt.get("steps") or [{}]
        expect(
            problems,
            receipt.get("failed_step") == steps[-1].get("name"),
            "failed_step is not the last step",
        )
        expect(
            problems,
            steps[-1].get("returncode") not in (0, None),
            "the failed step has returncode 0",
        )
    return problems


def check_pins(receipt: Mapping[str, Any], problems: list[str]) -> None:
    archive = receipt.get("archive") or {}
    expect(problems, archive.get("url") == ARCHIVE_URL, f"archive url is not {ARCHIVE_URL}")
    expect(
        problems,
        archive.get("commit") == ARCHIVE_COMMIT,
        f"archive commit {archive.get('commit')!r} is not the pinned {ARCHIVE_COMMIT}",
    )
    expect(
        problems, archive.get("committed") == ARCHIVE_COMMITTED, "archive commit date differs"
    )
    if receipt.get("status") != "passed":
        return
    blobs = archive.get("blobs") or {}
    for path, blob in PINNED_BLOBS.items():
        expect(
            problems, blobs.get(path) == blob, f"git blob of {path} is not the pinned {blob}"
        )
    toolchain = receipt.get("toolchain") or {}
    expect(
        problems,
        toolchain.get("lean_toolchain") == TOOLCHAIN,
        f"toolchain {toolchain.get('lean_toolchain')!r} is not {TOOLCHAIN!r}",
    )
    expect(
        problems,
        toolchain.get("mathlib_rev") == MATHLIB_REV,
        f"Mathlib {toolchain.get('mathlib_rev')!r} is not the pinned {MATHLIB_REV}",
    )
    versions = " ".join(toolchain.get("tool_versions") or [])
    expect(
        problems,
        f"version {LEAN_VERSION}" in versions,
        f"no `Lean (version {LEAN_VERSION}` line",
    )
    scan = receipt.get("source_scan") or {}
    for key in ("sorry", "axiom_declarations", "native_decide"):
        expect(problems, scan.get(key) == 0, f"source scan: {key} is {scan.get(key)!r}, not 0")
    expect(problems, (scan.get("lean_files") or 0) > 0, "source scan saw no Lean files")
    expect(
        problems,
        (receipt.get("policy_test") or {}).get("tests_run", 0) > 0,
        "policy test ran no tests",
    )


def check_steps(receipt: Mapping[str, Any], problems: list[str]) -> None:
    steps = receipt.get("steps")
    if not isinstance(steps, list) or not steps:
        problems.append("steps is missing or empty")
        return
    names = [step.get("name") for step in steps]
    expect(
        problems,
        names == list(STEP_NAMES[: len(names)]),
        f"steps {names} are not a prefix of {list(STEP_NAMES)}",
    )
    for step in steps:
        expect(
            problems,
            isinstance(step.get("returncode"), int),
            f"step {step.get('name')} has no returncode",
        )
        expect(
            problems,
            isinstance(step.get("seconds"), int | float),
            f"step {step.get('name')} has no seconds",
        )
    if receipt.get("status") == "passed":
        expect(problems, names == list(STEP_NAMES), "a passed receipt must carry every step")
        expect(
            problems,
            all(step.get("returncode") == 0 for step in steps),
            "a passed receipt has a nonzero step",
        )
        expect(
            problems, receipt.get("failed_step") is None, "a passed receipt names a failed step"
        )
    wall = receipt.get("wall_seconds")
    expect(
        problems, isinstance(wall, int | float) and wall >= 0, "wall_seconds is not a number"
    )


def check_theorem(receipt: Mapping[str, Any], problems: list[str]) -> None:
    theorem = receipt.get("theorem") or {}
    expect(
        problems,
        theorem.get("name") == THEOREM,
        f"theorem is {theorem.get('name')!r}, not {THEOREM}",
    )
    expect(
        problems,
        theorem.get("statement_source") == THEOREM_SOURCE,
        "the theorem's source statement differs from the retained text",
    )
    expect(
        problems,
        theorem.get("statement_elaborated") == THEOREM_ELABORATED,
        "the theorem's elaborated statement differs from the retained text",
    )
    expect(
        problems, receipt.get("statement_reading"), "the statement-fidelity reading is missing"
    )


def check_axioms(receipt: Mapping[str, Any], problems: list[str]) -> None:
    axioms = receipt.get("axioms") or {}
    try:
        parsed = parse_print_axioms(str(axioms.get("raw", "")))
    except ValueError as error:
        problems.append(f"axiom output: {error}")
        return
    reported = {name: tuple(found) for name, found in (axioms.get("reported") or {}).items()}
    expect(
        problems, parsed == reported, "the reported axioms differ from the retained raw output"
    )
    for declaration in (THEOREM, *INSTANCE_DECLARATIONS):
        found = parsed.get(declaration)
        if found is None:
            problems.append(f"{declaration}: no axiom report in the retained output")
            continue
        extra = sorted(set(found) - set(STANDARD_AXIOMS))
        expect(problems, not extra, f"{declaration} depends on non-standard axioms {extra}")
        expect(
            problems,
            tuple(sorted(found)) == STANDARD_AXIOMS,
            f"{declaration}: axioms {list(found)} are not exactly {list(STANDARD_AXIOMS)}",
        )
    expect(
        problems,
        "sorryAx" not in " ".join(axioms.get("raw", "").split()),
        "sorryAx appears in the output",
    )


def check_assertions(receipt: Mapping[str, Any], problems: list[str]) -> None:
    assertions = receipt.get("archive_assertions") or {}
    expect(
        problems,
        assertions.get("assert_standard_axioms_count") == MANIFEST_ASSERTIONS,
        f"ManifestEvidence assertion count is not {MANIFEST_ASSERTIONS}",
    )


def check_log(receipt: Mapping[str, Any], log: bytes, problems: list[str]) -> None:
    entry = receipt.get("build_log") or {}
    expect(problems, entry.get("path") == LOG_NAME, f"build_log path is not {LOG_NAME}")
    expect(
        problems,
        entry.get("sha256") == hashlib.sha256(log).hexdigest(),
        "the retained build log does not match its recorded sha256",
    )
    expect(problems, entry.get("bytes") == len(log), "the retained build log's size differs")
    text = log.decode("utf-8", "replace")
    steps = receipt.get("steps") or []
    for step in steps:
        header = f"=== step: {step.get('name')} ===\n"
        expect(problems, header in text, f"the log has no section for step {step.get('name')}")
    if receipt.get("status") == "passed":
        expect(
            problems,
            "Build completed successfully" in text,
            "the log has no `Build completed successfully`",
        )


def check_retained(directory: Path = RECEIPT_DIR) -> list[str]:
    """Problems with the retained receipt in a directory, reading only its two files."""
    try:
        receipt = json.loads((directory / RECEIPT_NAME).read_text(encoding="utf-8"))
        log = (directory / LOG_NAME).read_bytes()
    except (OSError, ValueError) as error:
        return [f"cannot read the retained receipt: {error}"]
    return validate_receipt(receipt, log)


def summary(directory: Path = RECEIPT_DIR) -> str:
    receipt = json.loads((directory / RECEIPT_NAME).read_text(encoding="utf-8"))
    if receipt["status"] != "passed":
        return f"replay FAILED at step {receipt['failed_step']}"
    build = next(step for step in receipt["steps"] if step["name"] == "build")
    rebuilt = receipt.get("rebuilt_modules") or []
    scope = (
        "from source"
        if receipt.get("fresh_archive_build")
        else f"over an existing build, {len(rebuilt)} module(s) rebuilt"
    )
    return (
        f"replay passed: {THEOREM} depends only on {', '.join(STANDARD_AXIOMS)}; "
        f"build step {build['seconds']} s {scope}, at {receipt['archive']['commit'][:8]}"
    )


# --- Command line --------------------------------------------------------------------


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", maxsplit=1)[0])
    mode = cli.add_mutually_exclusive_group(required=True)
    mode.add_argument("--run", action="store_true", help="run the replay and write the receipt")
    mode.add_argument(
        "--check", action="store_true", help="validate the retained receipt offline"
    )
    cli.add_argument(
        "--workdir", type=Path, help="with --run: a directory outside the repository"
    )
    cli.add_argument(
        "--receipt-dir",
        type=Path,
        default=RECEIPT_DIR,
        help="where the receipt is retained, or read",
    )
    cli.add_argument(
        "--rebuild",
        action="append",
        default=[],
        metavar="MODULE",
        help="with --run: remove this module's build products so Lake elaborates it again "
        "(repeatable); a cheaper audit of the modules that matter than --fresh-build",
    )
    cli.add_argument(
        "--note",
        action="append",
        default=[],
        help="with --run: a sentence kept in the receipt's notes (repeatable)",
    )
    cli.add_argument(
        "--fresh-build",
        action="store_true",
        help="with --run: remove the archive's own build products first, keeping Mathlib's",
    )
    return cli


def main(argv: Sequence[str] | None = None) -> int:
    cli = parser()
    args = cli.parse_args(argv)
    if args.check:
        problems = check_retained(args.receipt_dir)
        if problems:
            for problem in problems:
                print(f"replay_chelokot_lean: {problem}", file=sys.stderr)
            return 1
        print(summary(args.receipt_dir))
        return 0
    if args.workdir is None:
        cli.error("--run needs --workdir")
    workdir = args.workdir.resolve()
    if REPO in (workdir, *workdir.parents):
        cli.error("--workdir must be outside the repository")
    workdir.mkdir(parents=True, exist_ok=True)
    replay = Replay(
        workdir, fresh_build=args.fresh_build, notes=args.note, rebuild=args.rebuild
    )
    receipt = replay.run()
    retain(receipt, replay.sections, args.receipt_dir)
    problems = validate_receipt(receipt, (args.receipt_dir / LOG_NAME).read_bytes())
    for problem in problems:
        print(f"replay_chelokot_lean: {problem}", file=sys.stderr)
    print(f"{receipt['status']}: receipt written to {args.receipt_dir / RECEIPT_NAME}")
    return 0 if receipt["status"] == "passed" and not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
