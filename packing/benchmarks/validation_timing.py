"""Record repeated pytest runs with raw output, JUnit, and append-only receipts.

Example: python -m benchmarks.validation_timing --root . --label serial
--output-dir /tmp/validation-samples --repeats 3 tests -m exhaustive_exact

Allocated worker-seconds are wall time times the declared process allocation, not
measured CPU. Native thread limits and inner workers are recorded separately. Tests
that explicitly create their own pools can exceed the declared allocation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import signal
import subprocess
import sys
import time
import uuid
from collections.abc import Sequence
from contextlib import suppress
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from typing import Any

from strif import atomic_write_text

PHASE_EXPERIMENT_SECONDS = 300
PHASE_CLI_SECONDS = 45

NATIVE_THREAD_LIMITS = (
    "OPENBLAS_NUM_THREADS",
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "BLIS_NUM_THREADS",
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _append(output_dir: Path, event: dict[str, Any]) -> None:
    with (output_dir / "receipts.jsonl").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _stop(process: subprocess.Popen[bytes]) -> None:
    """Reap the process and terminate descendants in its private process group."""
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGTERM)
    with suppress(subprocess.TimeoutExpired):
        process.wait(timeout=1)
    # A parent can exit while a grandchild ignores SIGTERM and keeps running.
    with suppress(ProcessLookupError):
        os.killpg(process.pid, signal.SIGKILL)
    process.wait()


def _admit_phase_source(
    command: Sequence[str],
    root: Path,
    plugin: Path,
    metadata: dict[str, Any],
    expected: bytes | None,
) -> bytes:
    """Admit the currently requested child plugin before starting pytest."""
    if tuple(command[:3]) != (sys.executable, "-m", "pytest"):
        raise ValueError("phase timings require the maintained pytest command")
    if not plugin.is_relative_to(root.resolve()):
        raise ValueError("phase plugin resolves outside the selected root")
    source = plugin.read_bytes()
    if expected is not None and source != expected:
        raise ValueError("phase plugin changed during this invocation")
    if re.fullmatch(r"[0-9a-f]{40}", str(metadata.get("commit", ""))) is None:
        raise ValueError("phase timings require current source provenance")
    return source


def run_sample(
    command: Sequence[str],
    *,
    root: Path,
    output_dir: Path,
    metadata: dict[str, Any],
    timeout: float | None,
    environment: dict[str, str] | None = None,
    phase_timings: bool = False,
    expected_phase_source: bytes | None = None,
) -> dict[str, Any]:
    """Write a start receipt before launch and an end receipt after cleanup.

    Output is streamed directly to files, including before an interrupt or timeout.
    A hard kill of this recorder leaves the durable start receipt unmatched; consumers
    must treat that as incomplete. JUnit is best effort because pytest writes it on exit.
    """
    if phase_timings:
        source_root = Path(_git(root, "rev-parse", "--show-toplevel") or root).resolve()
        if not output_dir.is_absolute() or output_dir.resolve().is_relative_to(source_root):
            raise ValueError("phase journals must be absolute and outside source")
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex
    stdout_path = output_dir / f"{run_id}.stdout.log"
    stderr_path = output_dir / f"{run_id}.stderr.log"
    junit_path = output_dir / f"{run_id}.junit.xml"
    argv = [part.replace("{junit}", str(junit_path)) for part in command]
    if phase_timings:
        argv.extend(
            (
                "-p",
                "devtools.reachable_progress",
                "--reachable-phase-timings=pytest-report-duration-v1",
            )
        )
    receipt = {
        **metadata,
        "run_id": run_id,
        "command": argv,
        "root": str(root),
        "started_at": _now(),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "junit_path": str(junit_path),
        "timeout_seconds": timeout,
    }
    if phase_timings:
        receipt["phase_timings"] = {
            "capability": "pytest-report-duration-v1",
            "stem": str(output_dir / run_id),
        }
    _append(output_dir, {**receipt, "event": "start"})
    started = time.perf_counter()
    status = "failed"
    returncode: int | None = None
    error = ""
    process: subprocess.Popen[bytes] | None = None
    plugin = (root / "devtools/reachable_progress.py").resolve()
    phase_before: bytes | None = None
    try:
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            if phase_timings:
                phase_before = _admit_phase_source(
                    command, root, plugin, metadata, expected_phase_source
                )
                environment = dict(os.environ if environment is None else environment)
                for name in tuple(environment):
                    if name.startswith("PACKING_REACHABLE_TEST_"):
                        environment.pop(name)
                environment.pop("PACKING_VALIDATION_ARTIFACT_DIR", None)
                environment.pop("PYTEST_ADDOPTS", None)
                environment.update(
                    {
                        "PACKING_REACHABLE_TEST_ARTIFACT_STEM": str(output_dir / run_id),
                        "PACKING_REACHABLE_TEST_RUN_ID": run_id,
                        "PACKING_REACHABLE_TEST_SOURCE_COMMIT": str(metadata["commit"]),
                        "PACKING_REACHABLE_TEST_PHASES": "1",
                        "PACKING_REACHABLE_TEST_PHASE_PLUGIN_PATH": str(plugin),
                        "PACKING_REACHABLE_TEST_LANE": "validation-timing",
                        "PACKING_REACHABLE_TEST_MARKER": str(metadata.get("marker") or ""),
                        "PACKING_REACHABLE_TEST_EXCLUSIONS": "explicit timing selection",
                        "PYTHONPATH": os.pathsep.join((str(root / "src"), str(root))),
                    }
                )
            process = subprocess.Popen(
                argv,
                cwd=root,
                env=environment,
                stdout=stdout,
                stderr=stderr,
                start_new_session=True,
            )
            try:
                returncode = process.wait(timeout=timeout)
                status = "passed" if returncode == 0 else "failed"
            except subprocess.TimeoutExpired:
                status = "timeout"
            except KeyboardInterrupt:
                status = "interrupted"
            finally:
                _stop(process)
                returncode = process.returncode
    except OSError as exc:
        error = str(exc)
    except ValueError as exc:
        if not phase_timings:
            raise
        error = str(exc)
    if phase_before is not None:
        try:
            if plugin.read_bytes() != phase_before:
                status, error = "failed", "phase plugin changed during this invocation"
        except OSError as exc:
            status, error = "failed", str(exc)
    elapsed = time.perf_counter() - started
    result = {
        **receipt,
        "event": "end",
        "finished_at": _now(),
        "status": status,
        "returncode": returncode,
        "wall_seconds": elapsed,
        "allocated_worker_seconds": elapsed * int(metadata["allocated_workers"]),
        "error": error,
    }
    if phase_timings:
        result["phase_journals"] = [
            str(path) for path in sorted(output_dir.glob(f"{run_id}.progress-*.jsonl"))
        ]
    _append(output_dir, result)
    return result


def _git_bytes(root: Path, *arguments: str, required: bool = False) -> bytes:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    result = subprocess.run(
        ["git", "-C", str(root), *arguments],
        capture_output=True,
        check=False,
        env=environment,
        timeout=10,
    )
    if required and result.returncode != 0:
        raise ValueError(f"current Git provenance unavailable: {' '.join(arguments)}")
    return result.stdout if result.returncode == 0 else b""


def _git(root: Path, *arguments: str, required: bool = False) -> str:
    return (
        _git_bytes(root, *arguments, required=required)
        .decode("utf-8", errors="replace")
        .strip()
    )


def _untracked_hashes(root: Path, output_dir: Path) -> dict[str, str]:
    """Hash untracked inputs throughout the checkout, excluding timing outputs."""
    repository = _git(root, "rev-parse", "--show-toplevel")
    if not repository:
        return {}
    repo = Path(repository)
    output_dir = output_dir.resolve()
    hashes: dict[str, str] = {}
    for name in _git_bytes(repo, "ls-files", "--others", "--exclude-standard", "-z").split(
        b"\0"
    ):
        if not name:
            continue
        relative = os.fsdecode(name)
        path = repo / relative
        if path.is_file() and not path.resolve().is_relative_to(output_dir):
            hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def _sources(root: Path, targets: Sequence[str]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for target in targets:
        path = (root / target.split("::", 1)[0]).resolve()
        paths = sorted(path.rglob("*.py")) if path.is_dir() else [path]
        for source in paths:
            if source.is_file():
                hashes[str(source)] = hashlib.sha256(source.read_bytes()).hexdigest()
    return hashes


def main(argv: Sequence[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv[:1] == ["phase-overhead"]:
        return phase_overhead_main(argv[1:])
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, required=True, help="packing root or repository root"
    )
    parser.add_argument("--label", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--timeout", type=float)
    parser.add_argument("--phase-timings", action="store_true")
    parser.add_argument("--workers", type=int, default=0, help="xdist workers; 0 is in-process")
    parser.add_argument(
        "--inner-workers", type=int, default=1, help="PACK_JOBS cap per pytest worker"
    )
    parser.add_argument("--native-threads", type=int, default=1)
    parser.add_argument("-m", "--marker")
    parser.add_argument("-k", "--match")
    parser.add_argument("targets", nargs="+")
    args = parser.parse_args(argv)
    if (
        args.repeats < 1
        or args.workers < 0
        or args.inner_workers < 1
        or args.native_threads < 1
    ):
        parser.error("repeats and worker limits must be positive (xdist workers may be zero)")
    if args.timeout is not None and not (0 < args.timeout < float("inf")):
        parser.error("timeout must be finite and positive")
    root = args.root.resolve()
    if (root / "packing/pyproject.toml").is_file():
        root /= "packing"
    output_dir = args.output_dir.resolve()
    if args.phase_timings and not args.output_dir.is_absolute():
        parser.error("--phase-timings requires an absolute output directory")
    environment = os.environ.copy()
    environment.update({name: str(args.native_threads) for name in NATIVE_THREAD_LIMITS})
    environment.update(
        {
            "PACK_JOBS": str(args.inner_workers),
            "UV_NO_SYNC": "1",
            "PYTHONPATH": os.pathsep.join((str(root / "src"), str(root))),
            "PYTHONUNBUFFERED": "1",
        }
    )
    # Ambient pytest switches could select different tests or overwrite our JUnit path.
    environment.pop("PYTEST_ADDOPTS", None)
    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        *args.targets,
        "--durations=0",
        "--durations-min=0",
        "--junitxml={junit}",
    ]
    if args.workers:
        command.extend(("-n", str(args.workers)))
    if args.marker:
        command.extend(("-m", args.marker))
    if args.match:
        command.extend(("-k", args.match))
    dirty_diff = _git_bytes(root, "diff", "HEAD", "--binary")
    metadata = {
        "label": args.label,
        "commit": _git(root, "rev-parse", "HEAD"),
        "git_status": _git(root, "status", "--porcelain"),
        "dirty_diff_sha256": hashlib.sha256(dirty_diff).hexdigest(),
        "dirty_diff_hash_kind": "exact_git_diff_bytes",
        "untracked_sha256": _untracked_hashes(root, output_dir),
        "source_hashes": _sources(root, args.targets),
        "platform": platform.platform(),
        "python": sys.version,
        "interpreter": sys.executable,
        "available_cpus": os.process_cpu_count(),
        "pytest_workers": args.workers,
        "inner_workers": args.inner_workers,
        "native_threads": args.native_threads,
        "allocated_workers": max(1, args.workers) * args.inner_workers,
        "allocation_note": "wall times declared workers; not CPU or enforced process count",
        "environment": {
            name: environment[name]
            for name in (*NATIVE_THREAD_LIMITS, "PACK_JOBS", "PYTHONPATH", "UV_NO_SYNC")
        },
        "pytest_configuration": {
            name: environment.get(name, "")
            for name in (
                "PYTEST_DISABLE_PLUGIN_AUTOLOAD",
                "PYTHONPYCACHEPREFIX",
                "PYTHONUNBUFFERED",
            )
        },
    }
    phase_source: bytes | None = None
    if args.phase_timings:
        metadata["marker"] = args.marker
        metadata["phase_plugin_path"] = str((root / "devtools/reachable_progress.py").resolve())
        # run_sample retains any setup refusal with its requested receipt.
        with suppress(OSError):
            phase_source = (root / "devtools/reachable_progress.py").read_bytes()
    passed = True
    for repeat in range(1, args.repeats + 1):
        result = run_sample(
            command,
            root=root,
            output_dir=output_dir,
            metadata={**metadata, "repeat": repeat},
            timeout=args.timeout,
            environment=environment,
            phase_timings=args.phase_timings,
            expected_phase_source=phase_source,
        )
        print(json.dumps(result, sort_keys=True), flush=True)
        passed = passed and result["status"] == "passed"
        if result["status"] == "interrupted":
            return 130
        if args.phase_timings and result["status"] != "passed":
            break
    return 0 if passed else 1


def _check_phase_inputs(
    root: Path,
    fixture: Path,
    fixture_text: str,
    contents: dict[str, bytes],
    source: dict[str, Any],
    *,
    started: float,
    before: bool,
) -> None:
    """Keep one live comparison's fixture, source and runtime regime unchanged."""
    if before and time.monotonic() - started > PHASE_EXPERIMENT_SECONDS - PHASE_CLI_SECONDS:
        raise ValueError("comparison cannot fit its next 45-second command")
    changed = (
        fixture.read_bytes() != fixture_text.encode("utf-8")
        if before
        else fixture.read_text() != fixture_text
    )
    if changed:
        raise ValueError(
            "comparison fixture changed before observation"
            if before
            else "comparison fixture changed"
        )
    if contents != {name: (root / name).read_bytes() for name in contents}:
        raise ValueError("current comparison inputs changed")
    if (
        _git(root, "status", "--porcelain", required=True) != source["git_status"]
        or _git(root, "rev-parse", "HEAD", required=True) != source["commit"]
    ):
        raise ValueError("current source state changed during comparison")
    if source["versions"] != {
        name: version(name) for name in ("pytest", "pytest-xdist", "execnet")
    }:
        raise ValueError("runtime package versions changed during comparison")


def _require_phase_observation(index: int, result: dict[str, Any]) -> None:
    if result["status"] != "passed":
        raise ValueError(f"observation {index} was {result['status']}")


def phase_overhead_main(argv: Sequence[str]) -> int:
    """Run the fixed small v2 comparison through the existing whole-CLI recorder."""
    # Keep report dependencies off ordinary capture startup.
    from benchmarks import (  # noqa: PLC0415
        validation_report,
    )

    if (
        Path(validation_report.__file__).resolve()
        != Path(__file__).with_name("validation_report.py").resolve()
    ):
        raise ValueError("current report helper is outside the active instrument package")
    parser = argparse.ArgumentParser(description=phase_overhead_main.__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    root, output = args.root.resolve(), args.output_dir
    if (root / "packing/pyproject.toml").is_file():
        root /= "packing"
    if (
        Path(__file__).resolve() != root / "benchmarks/validation_timing.py"
        or Path(validation_report.__file__).resolve()
        != root / "benchmarks/validation_report.py"
    ):
        raise ValueError("active timing/report modules differ from the selected root")
    if not output.is_absolute() or output.resolve().is_relative_to(root.parent):
        parser.error("comparison output must be absolute and outside source")
    output = output.resolve()
    commit, dirty = (
        _git(root, "rev-parse", "HEAD", required=True),
        _git(root, "status", "--porcelain", required=True),
    )
    if not commit or dirty:
        parser.error("formal comparison requires clean current Git source")
    inputs = (
        "benchmarks/validation_timing.py",
        "benchmarks/validation_report.py",
        "devtools/reachable_progress.py",
        "pyproject.toml",
        "uv.lock",
        ".python-version",
    )
    contents = {name: (root / name).read_bytes() for name in inputs}
    output.mkdir()  # Exclusive: never replace or add target samples to old evidence.
    fixture = output / "fixture/test_phase_timing_work.py"
    fixture.parent.mkdir()
    fixture.write_text(validation_report.PHASE_FIXTURE, encoding="utf-8")
    environment = os.environ.copy()
    environment.update(
        {
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "PYTHONPYCACHEPREFIX": str(output / "python-cache"),
            "PYTHONPATH": os.pathsep.join((str(root / "src"), str(root))),
        }
    )
    environment.pop("PYTEST_ADDOPTS", None)
    environment.pop("PYTEST_DEBUG_TEMPROOT", None)
    environment.pop("PYTEST_PLUGINS", None)
    environment.pop("PACKING_VALIDATION_ARTIFACT_DIR", None)
    for name in tuple(environment):
        if name.startswith("PACKING_REACHABLE_TEST_"):
            environment.pop(name)
    protocol = {
        "protocol": "phase-overhead-v2",
        "order": list(validation_report.PHASE_ORDER),
        "source": {
            "commit": commit,
            "root": str(root),
            "git_status": dirty,
            "interpreter": sys.executable,
            "python": sys.version,
            "platform": platform.platform(),
            "available_cpus": os.process_cpu_count(),
            "versions": {name: version(name) for name in ("pytest", "pytest-xdist", "execnet")},
        },
        "output_root": str(output),
        "null_config": os.devnull,
        "started_at": _now(),
    }
    atomic_write_text(output / "protocol.json", json.dumps(protocol, indent=2) + "\n")
    started = time.monotonic()
    error = "capture did not finish"
    complete = False
    try:
        for index, arm in enumerate(validation_report.PHASE_ORDER):
            _check_phase_inputs(
                root,
                fixture,
                validation_report.PHASE_FIXTURE,
                contents,
                protocol["source"],
                started=started,
                before=True,
            )
            command = validation_report.phase_command(protocol, index, arm)
            result = run_sample(
                command,
                root=root,
                output_dir=output / "outer",
                metadata={"label": arm, "observation": index, "allocated_workers": 2},
                timeout=PHASE_CLI_SECONDS,
                environment=environment,
            )
            _require_phase_observation(index, result)
            _check_phase_inputs(
                root,
                fixture,
                validation_report.PHASE_FIXTURE,
                contents,
                protocol["source"],
                started=started,
                before=False,
            )
            validation_report.phase_observation(output, protocol, index, arm, result)
        atomic_write_text(
            output / "completion.json", json.dumps({"complete": True, "error": ""}) + "\n"
        )
        summary = validation_report.phase_overhead(output)
        atomic_write_text(output / "summary.json", json.dumps(summary, indent=2) + "\n")
        complete, error = True, ""
        return 0 if summary["accepted"] else 1
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        error = str(exc)
        return 1
    finally:
        atomic_write_text(
            output / "completion.json",
            json.dumps({"complete": complete, "error": error, "finished_at": _now()}) + "\n",
        )


if __name__ == "__main__":
    raise SystemExit(main())
