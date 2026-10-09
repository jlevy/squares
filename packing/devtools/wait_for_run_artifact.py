"""Wait for one exact-attempt producer artifact to become visible.

The Pages workflow schedules prepared-page consumers after their producer with
``needs:``. This tool then joins the current run attempt to its artifact, whose API
listing may become visible after the producer completes.

This tool makes that join explicit and bounded. It polls only the named workflow run,
accepts only a non-expired artifact with the exact name, and fails immediately when the
named producer completes without success. Polling backs off while the producer is
pending, and explicit API quota responses wait for the advertised retry window within
the same deadline. Other API failures and timeouts are errors. A consumer therefore
cannot continue on a missing, stale, or failed producer artifact.

Usage, from ``packing/``::

    python -m devtools.wait_for_run_artifact \
        --repository "$GITHUB_REPOSITORY" --run-id "$GITHUB_RUN_ID" \
        --run-attempt "$GITHUB_RUN_ATTEMPT" --name prepared-page \
        --producer prepare --github-output "$GITHUB_OUTPUT" --timeout 600
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence

type Api = Callable[[str], Any]
type Clock = Callable[[], float]
type Sleep = Callable[[float], None]


class RateLimitError(OSError):
    """An explicit API quota response and its minimum retry delay."""

    def __init__(self, message: str, *, retry_after: float) -> None:
        super().__init__(message)
        self.retry_after = retry_after


@dataclass(frozen=True)
class Ready:
    """The exact artifact and how many observations made it available."""

    attempts: int
    artifact_id: int


def _artifacts_path(repository: str, run_id: int) -> str:
    return f"repos/{repository}/actions/runs/{run_id}/artifacts?per_page=100"


def _jobs_path(repository: str, run_id: int, run_attempt: int) -> str:
    return f"repos/{repository}/actions/runs/{run_id}/attempts/{run_attempt}/jobs?per_page=100"


def _timestamp(value: object, *, what: str) -> datetime:
    if not isinstance(value, str):
        raise TypeError(f"{what} has no timestamp")
    try:
        return datetime.fromisoformat(value)
    except ValueError as error:
        raise RuntimeError(f"{what} has invalid timestamp {value!r}") from error


def _artifact_from_attempt(
    document: Mapping[str, Any], *, name: str, producer_started_at: str
) -> int | None:
    started = _timestamp(producer_started_at, what="producer")
    candidates: list[int] = []
    for artifact in document.get("artifacts", []):
        if artifact.get("name") != name or artifact.get("expired") is not False:
            continue
        created = _timestamp(artifact.get("created_at"), what=f"artifact {name!r}")
        artifact_id = artifact.get("id")
        if not isinstance(artifact_id, int) or artifact_id <= 0:
            raise RuntimeError(f"artifact {name!r} has invalid id {artifact_id!r}")
        # GitHub timestamps have one-second precision.  Strictly newer avoids accepting
        # an artifact from a prior attempt that finished in the same displayed second
        # this attempt's producer started; this producer renders for many seconds, so its
        # own artifact cannot legitimately share the start timestamp.
        if created > started:
            candidates.append(artifact_id)
    if len(candidates) > 1:
        raise RuntimeError(
            f"artifact {name!r} is ambiguous in this attempt: ids {sorted(candidates)}"
        )
    return candidates[0] if candidates else None


def _producer_job(document: Mapping[str, Any], *, producer: str) -> Mapping[str, Any] | None:
    producers = [job for job in document.get("jobs", []) if job.get("name") == producer]
    if len(producers) > 1:
        raise RuntimeError(f"producer {producer!r} is ambiguous in this attempt")
    return producers[0] if producers else None


def _producer_failure(job: Mapping[str, Any] | None, *, producer: str) -> str | None:
    if job is None or job.get("status") != "completed" or job.get("conclusion") == "success":
        return None
    return f"producer {producer!r} completed without success ({job.get('conclusion')!r})"


def wait_for_artifact(
    *,
    repository: str,
    run_id: int,
    run_attempt: int,
    name: str,
    producer: str,
    timeout: float,
    interval: float,
    api: Api,
    clock: Clock = time.monotonic,
    sleep: Sleep = time.sleep,
) -> Ready:
    """Return when ``name`` is finalized, or raise on a failed or bounded-out join."""
    if timeout < 0:
        raise ValueError("timeout must be non-negative")
    if interval <= 0:
        raise ValueError("interval must be positive")
    if run_attempt < 1:
        raise ValueError("run_attempt must be positive")
    deadline = clock() + timeout
    timeout_message = (
        f"artifact {name!r} was not available from {producer!r} after {timeout:g} seconds"
    )
    attempts = 0
    poll_interval = interval
    quota_interval = 60.0
    while True:
        attempts += 1
        delay = poll_interval
        try:
            jobs = api(_jobs_path(repository, run_id, run_attempt))
            if clock() >= deadline:
                raise TimeoutError(timeout_message)
            job = _producer_job(jobs, producer=producer)
            failure = _producer_failure(job, producer=producer)
            if failure is not None:
                raise RuntimeError(failure)
            active = job is not None and job.get("status") in {"in_progress", "completed"}
            started_at = None if job is None else job.get("started_at")
            if active and started_at is not None:
                artifacts = api(_artifacts_path(repository, run_id))
                if clock() >= deadline:
                    raise TimeoutError(timeout_message)
                artifact_id = _artifact_from_attempt(
                    artifacts, name=name, producer_started_at=str(started_at)
                )
                if artifact_id is not None:
                    return Ready(attempts, artifact_id)

            # Queued jobs can have started_at set before a runner picks them up.
            # Listing artifacts then adds requests without any possible new artifact.
            delay = min(poll_interval, 30.0 if active else 60.0)
            poll_interval = min(delay * 2, 30.0 if active else 60.0)
        except RateLimitError as error:
            delay = max(quota_interval, error.retry_after)
            quota_interval *= 2

        now = clock()
        if now >= deadline:
            raise TimeoutError(timeout_message)
        sleep(min(delay, deadline - now))
        # Do not spend another API request once a retry window reaches the deadline.
        if clock() >= deadline:
            raise TimeoutError(timeout_message)


def gh_api(path: str) -> Any:
    """Decode one API response, carrying explicit quota retry windows to the waiter."""
    completed = subprocess.run(
        ("gh", "api", "--include", path),
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    header_block, separator, body = completed.stdout.replace("\r\n", "\n").partition("\n\n")
    if completed.returncode != 0:
        message = completed.stderr.strip() or f"gh api {path} exited {completed.returncode}"
        lines = header_block.splitlines()
        status = lines[0].split()[1] if lines and len(lines[0].split()) > 1 else ""
        headers = {
            key.strip().lower(): value.strip()
            for line in lines[1:]
            for key, colon, value in [line.partition(":")]
            if colon
        }
        limited = status in {"403", "429"} and (
            status == "429"
            or "rate limit" in message.lower()
            or headers.get("x-ratelimit-remaining") == "0"
        )
        if limited:
            delays = [60.0]
            if "retry-after" in headers:
                delays.append(float(headers["retry-after"]))
            if headers.get("x-ratelimit-remaining") == "0" and "x-ratelimit-reset" in headers:
                delays.append(float(headers["x-ratelimit-reset"]) - time.time() + 1)
            if not all(math.isfinite(delay) for delay in delays):
                raise ValueError("API quota response has a non-finite retry window")
            raise RateLimitError(message, retry_after=max(delays))
        raise OSError(message)
    if not separator:
        raise RuntimeError("gh api response has no header/body separator")
    return json.loads(body)


def main(argv: Sequence[str] | None = None, *, api: Api = gh_api) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m devtools.wait_for_run_artifact",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    _ = parser.add_argument("--repository", required=True, help="OWNER/NAME")
    _ = parser.add_argument("--run-id", required=True, type=int)
    _ = parser.add_argument("--run-attempt", required=True, type=int)
    _ = parser.add_argument("--name", required=True)
    _ = parser.add_argument("--producer", required=True)
    _ = parser.add_argument("--github-output", type=Path)
    _ = parser.add_argument("--timeout", type=float, default=600)
    _ = parser.add_argument("--interval", type=float, default=5)
    arguments = parser.parse_args(argv)
    try:
        ready = wait_for_artifact(
            repository=str(arguments.repository),
            run_id=int(arguments.run_id),
            run_attempt=int(arguments.run_attempt),
            name=str(arguments.name),
            producer=str(arguments.producer),
            timeout=float(arguments.timeout),
            interval=float(arguments.interval),
            api=api,
        )
    except (OSError, TypeError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"artifact join failed: {error}", file=sys.stderr)
        return 1
    if arguments.github_output is not None:
        with arguments.github_output.open("a", encoding="utf-8") as output:
            _ = output.write(f"artifact_id={ready.artifact_id}\n")
    print(
        f"artifact {arguments.name!r} id {ready.artifact_id} is ready after "
        f"{ready.attempts} observation(s)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
