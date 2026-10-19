"""Bounded, manual forwarder observations with raw Playwright and pytest evidence.

These two fixed selections diagnose a failure; neither replaces a required CI owner.
The native validator retains raw output, partial progress and process-group cleanup.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from pathlib import Path

from sqpack.cli import validate

FORWARDER_MODULE = "tests/test_site_forwarders.py"
FORWARDER_NODE = f"{FORWARDER_MODULE}::test_the_deployed_site_check_follows_the_same_forwarders"
PRESETS = {
    "forwarder-node": (FORWARDER_NODE, 120),
    "forwarder-module": (FORWARDER_MODULE, 180),
}

# Share the gate's artifact and process-group boundaries instead of implementing a
# second subprocess supervisor for this manual observation.
_begin_artifacts = validate._begin_artifacts  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
_run = validate._run  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=tuple(PRESETS), required=True)
    parser.add_argument("--artifacts", type=Path, required=True)
    arguments = parser.parse_args(argv)
    requested: Path = arguments.artifacts
    artifacts = requested.resolve()
    if not requested.is_absolute() or artifacts.is_relative_to(
        validate.REPOSITORY_ROOT.resolve()
    ):
        parser.error("--artifacts must be an absolute directory outside the source checkout")
    target, seconds = PRESETS[arguments.mode]
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("GIT_", "PACKING_REACHABLE_TEST_"))
        and key not in {"SQPACK_SITE_PREVIEW_URL", "PYTEST_DEBUG_TEMPROOT", "PYTEST_PLUGINS"}
    }
    environment.update(
        {
            "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts),
            "PACK_JOBS": "1",
            "PYTHONUNBUFFERED": "1",
            # Unlike pw:api, wire diagnostics include newPage/close and their replies.
            "DEBUGP": "1",
            "DEBUG": "pw:api",
            validate.REQUIRE_CHROMIUM: "1",
            "PYTEST_ADDOPTS": (
                "-o tmp_path_retention_policy=failed -o tmp_path_retention_count=1"
            ),
        }
    )
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=environment,
        timeout_seconds=seconds,
        timeout_is_explicit=True,
        step_name=f"manual browser diagnostic: {arguments.mode}",
    )
    command = (
        sys.executable,
        "-m",
        "pytest",
        "-n",
        "0",
        "-s",
        "-vv",
        "-x",
        "-p",
        "no:cacheprovider",
        "-o",
        "faulthandler_timeout=45",
        target,
    )
    try:
        _begin_artifacts(context, [])
        _run(
            context,
            command,
            pytest_progress=("browser-diagnostic", "all tests outside the fixed preset"),
        )
    except validate.StepFailureError as error:
        print(str(error).splitlines()[0], file=sys.stderr)
        print(f"Raw diagnostic evidence: {artifacts}", file=sys.stderr)
        return 1
    print(f"Manual browser diagnostic passed; no required CI credit. Evidence: {artifacts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
