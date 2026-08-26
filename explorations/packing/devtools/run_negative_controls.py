#!/usr/bin/env python3
"""Negative-control harness: prove a check fails when it should.

A check nobody has watched fail is not a check. Every guard in this directory was
negative-controlled by hand at least once -- corrupt a field, run the gate, confirm it
complains, put the field back -- and every one of those controls was then thrown away,
so the next person has only a claim that it was done.

This runs them from a file instead, so they are checked in, repeatable, and part of the
suite. It also removes the way the hand version goes wrong: restoring with
`git checkout` reverts to HEAD, which silently discards uncommitted work in the same
file.

Each control runs in a throwaway source snapshot, and the working tree is never touched.
------------------------------------------------------------------------------------
The first version of this file corrupted tracked files IN PLACE and restored them
afterwards. That worked, and it cost more than it looked like it did:

  * Anything reading those files meanwhile saw the corruption. Seen once as
    the campaign runner failing on a dead link to a hypothesis that never existed. A
    spurious failure is the good outcome; a spurious pass is the other one. The
    `.gate-running` marker existed to narrow that window, and narrowing is not closing:
    an editor, a language server, a second agent or a second gate run could still read
    a half-corrupted tree.
  * The thirty controls had to run strictly one at a time, and so did the whole rest of
    the gate around them, because any concurrent step might read a corrupted file. That
    made this the gate's longest step at ~34s of a ~170s run -- on a ten-core machine
    where twenty-nine of the thirty controls are pure subprocess wait.
  * A crash between mutate and restore left the tree corrupt. `finally` covers
    exceptions; it does not cover SIGKILL or a power cut.

On APFS a snapshot uses copy-on-write cloning. Elsewhere it falls back to a plain copy
of a bounded source surface: the packing tree without the literature archive or build
products, plus the root formatter ignore file. One snapshot per worker is reused across
controls; `.venv` and the cargo target are symlinked back so nothing is rebuilt.

The gate can now run this step concurrently with every other step, and a control can no
longer corrupt anyone's checkout.

Control file format (YAML):

    controls:
    - name: outstanding defect without a bead
      file: defects.yaml
      replace: ["  bead: think-lksm\\n", ""]     # literal, must appear exactly once
      run: python3 -m devtools.validate_schemas
      expect: "outstanding without a bead"
      timeout_seconds: 120                         # optional; 120 is the default

Usage:
    uv run --frozen python -m devtools.run_negative_controls
    uv run --frozen python -m devtools.run_negative_controls -k bead
    uv run --frozen python -m devtools.run_negative_controls -j 1
"""

from __future__ import annotations

import argparse
import math
import os
import queue
import shutil
import signal
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

import yaml

from sqpack.workers import worker_count

ROOT = Path(__file__).resolve().parent.parent
# The REPOSITORY root, not this directory: one control targets ../../.flowmarkignore,
# because "is the generated view exempt from the Markdown formatter?" is a question
# about a file two levels up (D-027). Cloning only `explorations/packing` would put
# that control's target outside the sandbox and back in the real working tree, which
# is the one thing this file now exists to prevent. Clone the repo, work in the
# corresponding subdirectory.
REPO = ROOT.parent.parent
HERE = ROOT.relative_to(REPO)

# Controls need the packing source, not the literature archive, the rest of the
# repository, or build products. `resources/README.md` is copied separately because the
# README link checker requires that one path. The virtualenv and cargo target are
# symlinked back so nothing is rebuilt or resolved again.
PRUNE = frozenset(
    {
        # The gate's own marker. A clone that carried it would make the campaign runner
        # refuse to start, and four controls drive the runner expecting a DIFFERENT
        # refusal -- so the control would "fire" for the wrong reason and prove nothing.
        ROOT / ".gate-running",
        ROOT / ".venv",
        # Large, generator-owned prospective outputs are replayed by their dedicated
        # validation step and are never mutation targets. Copying 101 witnesses and 101
        # renderings into every private worker would exceed the portable snapshot cap.
        ROOT / "atlas/prospective/rendering",
        ROOT / "resources",
        ROOT / "sqsearch/target",
        ROOT / "witnesses/prospective",
    }
)
LINK_BACK = (Path(".venv"), Path("sqsearch/target"))
COPY_SEPARATELY = (ROOT / "resources/README.md", REPO / ".flowmarkignore")
# Keep a bounded portable fallback with enough headroom for source, schemas, and
# manifests after generator-owned prospective geometry is pruned above.
SNAPSHOT_MAX_BYTES = 40 * 1024 * 1024
DEFAULT_CONTROL_TIMEOUT_SECONDS = 120.0
TERMINATION_GRACE_SECONDS = 1.0
# Directories that must be walked into rather than bulk-copied, because something
# below them is pruned. Computed from PRUNE so the two cannot drift.
DESCEND = frozenset(a for p in PRUNE for a in p.parents if ROOT in (a, *a.parents))


@dataclass(frozen=True)
class CommandOutcome:
    """Complete captured state from one bounded control command."""

    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


def _stop_process_group(
    process: subprocess.Popen[str], *, grace_seconds: float
) -> tuple[str, str]:
    """Terminate and reap a control's complete process group."""
    if process.poll() is None:
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGTERM)
    try:
        return process.communicate(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
        return process.communicate()


def run_control_command(
    command: str,
    *,
    cwd: Path | None = None,
    environment: dict[str, str] | None = None,
    timeout_seconds: float = DEFAULT_CONTROL_TIMEOUT_SECONDS,
    termination_grace_seconds: float = TERMINATION_GRACE_SECONDS,
) -> CommandOutcome:
    """Run one registry command with captured output and bounded group cleanup."""
    process = subprocess.Popen(
        command,
        shell=True,
        cwd=cwd,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        stdout, stderr = _stop_process_group(process, grace_seconds=termination_grace_seconds)
        return CommandOutcome(
            returncode=process.returncode,
            stdout=stdout,
            stderr=stderr,
            timed_out=True,
        )
    except BaseException:
        _stop_process_group(process, grace_seconds=termination_grace_seconds)
        raise
    return CommandOutcome(process.returncode, stdout, stderr)


def _clone_into(src: Path, dst: Path) -> None:
    """Clone `src` to `dst`, descending only where a prune target lives below.

    Everything else goes in one `cp -Rc`, which asks APFS for a copy-on-write clone:
    near-instant, and it costs no disk until a block is written. `-c` is macOS-specific
    and fails loudly where the filesystem cannot clone, so the plain copy is the
    fallback rather than the default.
    """
    dst.mkdir(parents=True, exist_ok=True)
    bulk: list[str] = []
    for entry in src.iterdir():
        if entry in PRUNE:
            continue
        if entry in DESCEND:
            _clone_into(entry, dst / entry.name)
        else:
            bulk.append(str(entry))
    if not bulk:
        return
    if subprocess.run(
        ["cp", "-Rc", *bulk, str(dst)], capture_output=True, check=False
    ).returncode:
        subprocess.run(["cp", "-R", *bulk, str(dst)], capture_output=True, check=True)


def snapshot_source_bytes() -> int:
    """Bytes copied by the portable fallback, excluding linked build products."""
    total = sum(path.stat().st_size for path in COPY_SEPARATELY)
    for directory, names, files in os.walk(ROOT):
        parent = Path(directory)
        names[:] = [name for name in names if parent / name not in PRUNE]
        for name in files:
            path = parent / name
            if path in PRUNE or path.is_symlink():
                continue
            total += path.stat().st_size
    return total


def clone_tree(dest: Path) -> None:
    """A private, writable source snapshot for one worker to corrupt."""
    work = dest / HERE
    _clone_into(ROOT, work)

    resource_readme = work / "resources/README.md"
    resource_readme.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "resources/README.md", resource_readme)
    shutil.copy2(REPO / ".flowmarkignore", dest / ".flowmarkignore")

    for rel in LINK_BACK:
        source = ROOT / rel
        if not source.exists():
            continue
        link = work / rel
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(source)


def resolve_control_target(control_file: object, *, tree: Path, work: Path) -> Path:
    """Resolve one mutation target without allowing it to leave the private snapshot."""
    if not isinstance(control_file, str) or not control_file:
        raise ValueError("control file must be a non-empty path string")
    try:
        target = (work / control_file).resolve(strict=True)
    except OSError as error:
        raise ValueError(f"control target does not exist: {control_file!r}") from error
    if not target.is_relative_to(tree.resolve()):
        raise ValueError(f"control target escapes private snapshot: {control_file!r}")
    if not target.is_file():
        raise ValueError(f"control target is not a regular file: {control_file!r}")
    return target


def run_one(c: dict, tree: Path) -> tuple[bool, str]:
    """Apply the mutation inside `tree`, run the command there, restore. (passed, why)."""
    work = tree / HERE
    try:
        target = resolve_control_target(c.get("file"), tree=tree, work=work)
    except ValueError as error:
        return False, str(error)
    original = target.read_bytes()
    old, new = c["replace"]
    try:
        text = original.decode("utf-8")
        if text.count(old) != 1:
            return False, f"anchor appears {text.count(old)} times, expected exactly 1"
        target.write_text(text.replace(old, new, 1), encoding="utf-8")
        # check=False deliberately: a non-zero exit is the EXPECTED outcome here, and
        # inspecting it is this function's whole job.
        env = os.environ.copy()
        # Every worker links the already-synced environment to avoid reinstalling the
        # scientific stack. Letting `uv run` sync that shared environment installs the
        # editable project from a temporary snapshot, which disappears after this run
        # and leaves the developer environment broken. Snapshot imports must still win.
        env["UV_NO_SYNC"] = "1"
        import_roots = (str(work / "src"), str(work))
        env["PYTHONPATH"] = os.pathsep.join(
            (*import_roots, env["PYTHONPATH"]) if env.get("PYTHONPATH") else import_roots
        )
        try:
            timeout_seconds = float(c.get("timeout_seconds", DEFAULT_CONTROL_TIMEOUT_SECONDS))
        except TypeError, ValueError:
            return False, "timeout_seconds is not a number"
        if not math.isfinite(timeout_seconds) or timeout_seconds <= 0:
            return False, "timeout_seconds must be finite and positive"
        # Two controls can make same-size edits to one module inside the same filesystem
        # timestamp tick. Python's normal timestamp-and-size bytecode cache would then
        # let the second command execute the first control's mutation. Give every
        # command a fresh cache root so the source under test is always recompiled.
        with tempfile.TemporaryDirectory(prefix="negctl-pycache-", dir=tree) as pycache:
            env["PYTHONPYCACHEPREFIX"] = pycache
            outcome = run_control_command(
                c["run"],
                cwd=work,
                environment=env,
                timeout_seconds=timeout_seconds,
            )
        output = outcome.stdout + outcome.stderr
        detail = ""
        if outcome.timed_out:
            detail = f"timed out after {timeout_seconds:g} seconds"
        elif outcome.returncode == 0:
            detail = "command SUCCEEDED; the check did not fire"
        elif c["expect"] not in output:
            detail = f"failed, but not with the expected message: {output.strip()[:120]}"
        return not detail, detail
    finally:
        # Restore inside the clone anyway: one worker runs several controls, and the
        # next one must not see the previous one's corruption.
        target.write_bytes(original)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "spec",
        nargs="?",
        type=Path,
        default=Path("devtools/controls.yaml"),
        help="control registry, relative to the packing project root",
    )
    parser.add_argument("-k", "--match", help="run controls whose names contain TEXT")
    parser.add_argument("-j", "--jobs", type=int, default=0, help="worker count (0 = auto)")
    return parser


def main(arguments: list[str] | None = None) -> int:
    """Run selected controls in isolated source snapshots."""
    options = _parser().parse_args(arguments)
    spec_path = options.spec if options.spec.is_absolute() else ROOT / options.spec
    spec = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    only = options.match
    controls = [c for c in spec["controls"] if not only or only in c["name"]]
    if not controls:
        print("  no controls matched", file=sys.stderr)
        return 1

    requested = options.jobs
    if requested < 0:
        _parser().error("--jobs must be non-negative")
    workers = requested or worker_count(len(controls))

    source_bytes = snapshot_source_bytes()
    if source_bytes > SNAPSHOT_MAX_BYTES:
        print(
            f"negative-control snapshot source is {source_bytes} bytes; "
            f"cap is {SNAPSHOT_MAX_BYTES}",
            file=sys.stderr,
        )
        return 1
    print(
        f"  snapshot source {source_bytes / (1024 * 1024):.1f} MiB; "
        f"{workers} private worker trees"
    )

    failures: list[tuple[str, str]] = []
    with tempfile.TemporaryDirectory(prefix="negctl-") as tmp:
        trees = [Path(tmp) / f"w{i}" for i in range(workers)]
        with ThreadPoolExecutor(max_workers=workers) as pool:
            list(pool.map(clone_tree, trees))

            # A tree is CHECKED OUT for the duration of one control and returned
            # afterwards, so no two running controls can ever share one.
            #
            # The obvious thing -- hand control i the tree at index i % workers -- is
            # wrong, and wrong in the way that only shows up under load: a pool does
            # not promise that item i runs on worker i % workers. It promises that
            # some free thread takes the next item. One slow control is enough for
            # item i and item i + workers to be in flight at the same moment, both
            # claiming the same tree, one restoring the file the other just corrupted.
            # Caught by running the gate at --jobs 10: the "defect log - count
            # disagreeing with the list" control stopped firing, because a neighbour
            # had already put defects.yaml back.
            available: queue.Queue[Path] = queue.Queue()
            for t in trees:
                available.put(t)

            def work(c: dict) -> tuple[dict, bool, str]:
                tree = available.get()
                try:
                    passed, detail = run_one(c, tree)
                finally:
                    available.put(tree)
                return c, passed, detail

            # `pool.map` preserves order, so the report reads the same however the
            # work happened to be split across trees.
            for c, passed, detail in pool.map(work, controls):
                if not passed:
                    failures.append((c["name"], detail))

    for name, detail in failures:
        print(f"  CONTROL FAILED  {name}: {detail}", file=sys.stderr)
    if failures:
        print(
            f"{len(failures)} of {len(controls)} negative controls did not fire",
            file=sys.stderr,
        )
        return 1
    print(f"  {len(controls)} negative controls fire as expected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
