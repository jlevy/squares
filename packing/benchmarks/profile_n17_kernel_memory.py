"""Peak memory and time of the n17 kernel's three checks of a certificate, step by step.

Runs one of them in this process and records its resident set:

- `produce` is `check_n17_subpattern` producing a certificate and then checking it in the
  same process, with the tool's own arguments in `--producer-arguments`;
- `check-saved` is `check_n17_subpattern.check_saved` on a saved certificate directory,
  the checker alone, as `--check-saved` runs it;
- `verify` is `verify_n17_kernel_certificate.verify` on one, the standing verifier, in
  full.

Each step is marked: a produced one through the producer's progress callback, a checked
one through the function both checkers call once per step before its rows
(`sequential.admit_partner_covers`, `verify_n17_kernel_certificate.check_partners`), and
`produce` also marks the end of the production and of the save. A mark reads `VmRSS`
from `/proc/self/status`. The peaks are the kernel's own high-water mark, `VmHWM`, read
at the first checked step and reset there through `/proc/self/clear_refs`, so the report
gives the peak before the check and the peak in it exactly, with no sampling. A sampling
thread was tried first and dropped: on a loaded machine its contention for the GIL cost
the measured process most of its share of a CPU.

The report is JSON: the verdict and its counts, as the run states them, the wall and
process CPU time (the second is the one to compare on a shared machine), the peaks and
the resident set at every mark. `--rss-ceiling-mb` starts a thread that ends the process
with status 3 once a once-a-second sample exceeds it: a shared machine's memory is the
reason this tool exists, and a measurement must not become the job the OOM killer picks.
An allocation that passes the ceiling between two samples still can; for a hard limit
run under `ulimit -v` as well.

From `packing/`:

    .venv/bin/python3 -m benchmarks.profile_n17_kernel_memory check-saved DIR \\
        --rss-ceiling-mb 4000 --output saved-memory.json
    .venv/bin/python3 -m benchmarks.profile_n17_kernel_memory produce \\
        --producer-arguments "--pattern W7 --bins 64 --save-objects OUT" --output run.json
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

CEILING_SECONDS = 1.0


def status_mb(field: str) -> int:
    """A `/proc/self/status` field in MiB, or -1 where there is none."""
    try:
        lines = Path("/proc/self/status").read_text(encoding="ascii").splitlines()
    except OSError:
        return -1
    for line in lines:
        if line.startswith(f"{field}:"):
            return int(line.split()[1]) // 1024
    return -1


def reset_peak() -> bool:
    """Reset `VmHWM` to the current resident set; False where the kernel does not allow it."""
    try:
        _ = Path("/proc/self/clear_refs").write_text("5", encoding="ascii")
    except OSError:
        return False
    return True


class Recorder:
    """Marks steps and phases with the resident set, and keeps the peak before the first
    checked step apart from the peak from it on."""

    def __init__(self, ceiling_mb: int | None) -> None:
        self.started = time.monotonic()
        self.cpu_started = time.process_time()
        self.ceiling_mb = ceiling_mb
        self.steps: list[dict[str, Any]] = []
        self.phases: dict[str, dict[str, float]] = {}
        self.peak_before_check_mb: int | None = None
        self.peak_was_reset = False

    def seconds(self) -> float:
        return round(time.monotonic() - self.started, 2)

    def sample(self) -> int:
        rss = status_mb("VmRSS")
        if self.ceiling_mb is not None and rss > self.ceiling_mb:
            stopped = {"stopped": "rss ceiling", "rss_mb": rss, "seconds": self.seconds()}
            print(json.dumps(stopped), flush=True)
            os._exit(3)
        return rss

    def watch(self) -> None:
        """With a ceiling, check it once a second from a thread."""
        if self.ceiling_mb is None:
            return

        def loop() -> None:
            while True:
                _ = self.sample()
                time.sleep(CEILING_SECONDS)

        threading.Thread(target=loop, daemon=True).start()

    def step(self, phase: str, index: object, rows: int) -> None:
        if phase == "check" and self.peak_before_check_mb is None:
            self.peak_before_check_mb = status_mb("VmHWM")
            self.peak_was_reset = reset_peak()
        self.steps.append(
            {
                "phase": phase,
                "step": index,
                "rows": rows,
                "rss_mb": self.sample(),
                "seconds": self.seconds(),
            }
        )

    def phase(self, name: str) -> None:
        self.phases[name] = {"rss_mb": self.sample(), "seconds": self.seconds()}

    def report(self) -> dict[str, Any]:
        checked = [step["rss_mb"] for step in self.steps if step["phase"] == "check"]
        high = status_mb("VmHWM")
        before = self.peak_before_check_mb
        return {
            "wall_seconds": self.seconds(),
            "process_cpu_seconds": round(time.process_time() - self.cpu_started, 2),
            "peak_rss_mb": high if before is None else max(before, high),
            "peak_before_check_mb": before,
            "peak_in_check_mb": high if self.peak_was_reset else None,
            "rss_at_first_check_step_mb": checked[0] if checked else None,
            "max_check_step_rss_mb": max(checked, default=None),
            "phases": self.phases,
            "steps": self.steps,
        }


def mark_checked_steps(recorder: Recorder) -> Callable[[], None]:
    """Mark the start of each step `sequential.replay_sequential` checks; returns the undo."""
    from sqpack.hull_kernel import sequential  # noqa: PLC0415

    admit = sequential.admit_partner_covers

    def marked(frame: Any, step: Any, rows: Any, *, mask: Any) -> Any:
        recorder.step("check", step["index"], len(step["rows"]))
        return admit(frame, step, rows, mask=mask)

    sequential.admit_partner_covers = marked

    def undo() -> None:
        sequential.admit_partner_covers = admit

    return undo


def profile_saved(
    directory: Path,
    recorder: Recorder,
    max_seconds: float,
    frame: Any = None,
    *,
    require_no_producer: bool = True,
) -> dict[str, Any]:
    """`check_saved`'s result less its timing, on the n17 frame unless `frame` is given;
    `require_no_producer` is passed on, and only a test that produced its certificate in
    this process turns it off."""
    from devtools import check_n17_subpattern as tool  # noqa: PLC0415

    undo = mark_checked_steps(recorder)
    try:
        result = tool.check_saved(
            directory, frame, max_seconds=max_seconds, require_no_producer=require_no_producer
        )
    finally:
        undo()
    volatile = ("check_seconds", "checker_modules_sha256")
    return {key: value for key, value in result.items() if key not in volatile}


def profile_verifier(directory: Path, recorder: Recorder, cells: Any = None) -> dict[str, Any]:
    """The verifier's receipt, on the n17 cover's cells unless `cells` are given."""
    from devtools import verify_n17_kernel_certificate as verifier  # noqa: PLC0415

    check: Callable[..., Any] = verifier.check_partners

    def marked(state: Any, step: Any, si: int) -> Any:
        recorder.step("check", si, len(step["rows"]))
        return check(state, step, si)

    verifier.check_partners = marked
    try:
        receipt = verifier.verify(directory, cells or verifier.cover_cells())
    finally:
        verifier.check_partners = check
    volatile = ("seconds", "provenance")
    return {key: value for key, value in receipt.items() if key not in volatile}


def profile_produce(arguments: list[str], recorder: Recorder) -> dict[str, Any]:
    """`check_n17_subpattern`'s result for these arguments, less its timing and provenance:
    production, the save if asked, and the in-process check."""
    from devtools import check_n17_subpattern as tool  # noqa: PLC0415
    from sqpack.hull_kernel import producer  # noqa: PLC0415

    produce, save, run = producer.produce, tool.save_certificate, tool.run
    results: list[dict[str, Any]] = []

    def produced(*args: Any, **kwargs: Any) -> Any:
        progress = kwargs.get("progress")

        def marked(event: dict[str, Any]) -> None:
            recorder.step("produce", event.get("step"), int(event.get("rows", 0)))
            if progress is not None:
                progress(event)

        kwargs["progress"] = marked
        production = produce(*args, **kwargs)
        recorder.phase("produced")
        return production

    def saved(*args: Any, **kwargs: Any) -> Any:
        path = save(*args, **kwargs)
        recorder.phase("saved")
        return path

    def ran(*args: Any, **kwargs: Any) -> dict[str, Any]:
        result = run(*args, **kwargs)
        results.append(result)
        return result

    producer.produce, tool.save_certificate, tool.run = produced, saved, ran
    undo = mark_checked_steps(recorder)
    try:
        _ = tool.main(arguments)
    finally:
        producer.produce, tool.save_certificate, tool.run = produce, save, run
        undo()
    volatile = ("producer_seconds", "checker_seconds", "wall_seconds", "process_cpu_seconds")
    return {
        key: value
        for key, value in (results[0] if results else {}).items()
        if key not in (*volatile, "provenance", "wall_ceiling_seconds")
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("checker", choices=("produce", "check-saved", "verify"))
    _ = parser.add_argument(
        "directory", type=Path, nargs="?", help="holds seed-*.json.gz, node-*.json.gz"
    )
    _ = parser.add_argument(
        "--producer-arguments", default="", help="with produce: check_n17_subpattern's"
    )
    _ = parser.add_argument("--rss-ceiling-mb", type=int, default=None)
    _ = parser.add_argument("--max-seconds", type=float, default=9000.0)
    _ = parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    if arguments.checker != "produce" and arguments.directory is None:
        parser.error("check-saved and verify need a certificate directory")
    recorder = Recorder(arguments.rss_ceiling_mb)
    recorder.watch()
    if arguments.checker == "produce":
        verdict = profile_produce(shlex.split(arguments.producer_arguments), recorder)
    elif arguments.checker == "check-saved":
        verdict = profile_saved(arguments.directory, recorder, arguments.max_seconds)
    else:
        verdict = profile_verifier(arguments.directory, recorder)
    report = {
        "checker": arguments.checker,
        "directory": None if arguments.directory is None else str(arguments.directory),
        "producer_arguments": arguments.producer_arguments or None,
        "verdict": verdict,
        **recorder.report(),
    }
    encoded = json.dumps(report, indent=1, default=str) + "\n"
    if arguments.output is not None:
        _ = arguments.output.write_text(encoded, encoding="utf-8")
    summary = {key: report[key] for key in ("checker", "wall_seconds", "peak_rss_mb")}
    print(json.dumps({**summary, "status": verdict.get("status")}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
