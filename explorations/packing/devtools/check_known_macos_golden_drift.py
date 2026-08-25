"""Require the one known macOS deep-golden failure and reject every other outcome.

This is a temporary CI contract for D-203. It keeps the known numerical drift visible
without allowing ``continue-on-error`` to hide a crash, a different basin-map change,
or a future fix that should remove this expected-failure check.
"""

from __future__ import annotations

import subprocess
import sys

from sqpack.project import require_project_root

KNOWN_DRIFT_FRAGMENTS = (
    "GOLDEN DRIFT — the map changed",
    "n= 4   2 endpoint rows from  4 proposals (3 converged)",
    "-    converged: 4",
    "-    distinct_basins: 1",
    "+    converged: 3",
    "+    distinct_basins: 2",
    "ORACLE FAILURES:",
    "the rebuilt map differs from the committed golden",
    "GOLDEN BASIN CHECKS FAILED",
)


class ProbeMismatchError(RuntimeError):
    """The deep-golden probe no longer has its one documented outcome."""


def validate_probe_result(returncode: int, transcript: str) -> None:
    """Accept only D-203's captured failure signature."""
    if returncode == 0:
        raise ProbeMismatchError(
            "the macOS deep-golden probe unexpectedly passed; remove this D-203 "
            "expected-failure contract and make the deep check blocking"
        )
    missing = [fragment for fragment in KNOWN_DRIFT_FRAGMENTS if fragment not in transcript]
    if returncode != 1 or missing:
        raise ProbeMismatchError(
            "the macOS deep-golden probe had an unexpected failure: "
            f"exit {returncode}, missing expected fragments {missing!r}"
        )


def main() -> int:
    """Run the focused reconstruction and classify its complete transcript."""
    project_root = require_project_root()
    command = (
        sys.executable,
        "-m",
        "sqpack.cli.validate",
        "--deep",
        "--only",
        "golden basin maps",
        "--jobs",
        "1",
        "--inner-jobs",
        "1",
    )
    completed = subprocess.run(
        command,
        cwd=project_root,
        capture_output=True,
        text=True,
        check=False,
    )
    print(completed.stdout, end="")
    print(completed.stderr, end="", file=sys.stderr)
    transcript = f"{completed.stdout}\n{completed.stderr}"
    try:
        validate_probe_result(completed.returncode, transcript)
    except ProbeMismatchError as error:
        print(f"macOS deep-golden contract failed: {error}", file=sys.stderr)
        return 1
    print("KNOWN D-203 MACOS GOLDEN DRIFT CONFIRMED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
