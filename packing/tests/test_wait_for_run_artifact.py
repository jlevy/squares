"""The concurrent Actions artifact join is exact, bounded, and fail-closed."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from devtools import wait_for_run_artifact as tool

REPOSITORY = "jlevy/squares"
RUN_ID = 77
RUN_ATTEMPT = 2
STARTED = "2026-09-16T12:00:01Z"
CREATED = "2026-09-16T12:00:02Z"
OLD_CREATED = "2026-09-16T11:59:59Z"
START_SECOND = STARTED


def _artifact(
    *,
    artifact_id: int = 91,
    name: str = "prepared-page",
    expired: bool = False,
    created_at: str = CREATED,
) -> dict[str, Any]:
    return {"id": artifact_id, "name": name, "expired": expired, "created_at": created_at}


def _job(
    *,
    name: str = "prepare",
    status: str = "in_progress",
    conclusion: str | None = None,
    started_at: str | None = STARTED,
) -> dict[str, Any]:
    return {
        "name": name,
        "status": status,
        "conclusion": conclusion,
        "started_at": started_at,
    }


class Responses:
    def __init__(
        self,
        artifacts: list[list[dict[str, Any]]],
        jobs: list[list[dict[str, Any]]] | None = None,
    ) -> None:
        self.artifacts = iter(artifacts)
        self.jobs = iter(jobs or [[_job()] for _ in artifacts])
        self.paths: list[str] = []

    def __call__(self, path: str) -> dict[str, Any]:
        self.paths.append(path)
        if "/artifacts?" in path:
            return {"artifacts": next(self.artifacts)}
        assert "/jobs?" in path
        assert f"/attempts/{RUN_ATTEMPT}/" in path
        return {"jobs": next(self.jobs)}


def wait(api: tool.Api, **overrides: Any) -> tool.Ready:
    observations = overrides.pop("clock_values", [0.0, 0.0])
    clock_values = iter(observations)
    arguments = {
        "run_attempt": RUN_ATTEMPT,
        "timeout": 10,
        "interval": 1,
        **overrides,
    }
    return tool.wait_for_artifact(
        repository=REPOSITORY,
        run_id=RUN_ID,
        name="prepared-page",
        producer="prepare",
        api=api,
        **{
            "clock": lambda: next(clock_values, observations[-1]),
            "sleep": lambda _seconds: None,
            **arguments,
        },
    )


def test_an_exact_nonexpired_artifact_from_this_attempt_is_ready() -> None:
    api = Responses([[_artifact()]])
    assert wait(api) == tool.Ready(attempts=1, artifact_id=91)
    assert api.paths == [
        f"repos/{REPOSITORY}/actions/runs/{RUN_ID}/attempts/{RUN_ATTEMPT}/jobs?per_page=100",
        f"repos/{REPOSITORY}/actions/runs/{RUN_ID}/artifacts?per_page=100",
    ]


def test_an_expired_or_differently_named_artifact_is_not_accepted() -> None:
    api = Responses(
        [[_artifact(expired=True), _artifact(name="another")]],
        [[_job(status="completed", conclusion="failure")]],
    )
    with pytest.raises(RuntimeError, match="completed without success"):
        wait(api)


def test_the_join_polls_until_the_artifact_is_finalized() -> None:
    api = Responses([[], [_artifact()]])
    assert wait(api, clock_values=[0.0, 0.0, 1.0]) == tool.Ready(2, 91)
    assert sum("/artifacts?" in path for path in api.paths) == 2
    assert sum("/jobs?" in path for path in api.paths) == 2


def test_a_failed_producer_refuses_immediately() -> None:
    api = Responses([[]], [[_job(status="completed", conclusion="cancelled")]])
    with pytest.raises(RuntimeError, match="'cancelled'"):
        wait(api)
    assert not any("/artifacts?" in path for path in api.paths)


def test_a_rerun_ignores_the_previous_attempts_same_named_artifact() -> None:
    api = Responses(
        [[_artifact(artifact_id=80, created_at=OLD_CREATED)], [_artifact(artifact_id=92)]],
    )
    assert wait(api, clock_values=[0.0, 0.0, 1.0]) == tool.Ready(2, 92)


def test_a_same_second_artifact_is_not_attributed_to_this_attempt() -> None:
    api = Responses(
        [[_artifact(artifact_id=80, created_at=START_SECOND)], [_artifact(artifact_id=92)]],
    )
    assert wait(api, clock_values=[0.0, 0.0, 1.0]) == tool.Ready(2, 92)


def test_a_missing_artifact_times_out_at_the_declared_boundary() -> None:
    api = Responses([[], []])
    with pytest.raises(TimeoutError, match="after 10 seconds"):
        wait(api, clock_values=[0.0, 0.0, 10.0])


def test_api_errors_and_invalid_bounds_fail_closed() -> None:
    def broken(_path: str) -> Any:
        raise OSError("HTTP 403")

    with pytest.raises(OSError, match="403"):
        wait(broken)
    with pytest.raises(ValueError, match="timeout"):
        wait(broken, timeout=-1)
    with pytest.raises(ValueError, match="interval"):
        wait(broken, interval=0)
    with pytest.raises(ValueError, match="run_attempt"):
        wait(broken, run_attempt=0)


def test_main_reports_api_failure_as_a_failed_join(capsys: pytest.CaptureFixture[str]) -> None:
    def broken(_path: str) -> Any:
        raise OSError("API unavailable")

    assert (
        tool.main(
            [
                "--repository",
                REPOSITORY,
                "--run-id",
                str(RUN_ID),
                "--run-attempt",
                str(RUN_ATTEMPT),
                "--name",
                "prepared-page",
                "--producer",
                "prepare",
                "--timeout",
                "0",
            ],
            api=broken,
        )
        == 1
    )
    assert "artifact join failed: API unavailable" in capsys.readouterr().err


def test_main_writes_the_exact_artifact_id_for_the_download_step(tmp_path: Path) -> None:
    output = tmp_path / "github-output"
    api = Responses([[_artifact(artifact_id=93)]])
    assert (
        tool.main(
            [
                "--repository",
                REPOSITORY,
                "--run-id",
                str(RUN_ID),
                "--run-attempt",
                str(RUN_ATTEMPT),
                "--name",
                "prepared-page",
                "--producer",
                "prepare",
                "--github-output",
                str(output),
            ],
            api=api,
        )
        == 0
    )
    assert output.read_text(encoding="utf-8") == "artifact_id=93\n"


class FakeClock:
    def __init__(self) -> None:
        self.now = 0.0
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.sleeps.append(seconds)
        self.now += seconds


def test_queued_producer_uses_at_most_fourteen_requests_in_ten_minutes() -> None:
    clock = FakeClock()
    paths: list[str] = []

    def queued(path: str) -> dict[str, Any]:
        paths.append(path)
        assert "/jobs?" in path
        return {"jobs": [_job(status="queued")]}

    with pytest.raises(TimeoutError, match="after 600 seconds"):
        wait(queued, timeout=600, interval=5, clock=clock, sleep=clock.sleep)
    assert len(paths) <= 14
    assert clock.now == 600
    assert max(clock.sleeps) <= 60


def test_rate_limit_recovery_respects_retry_after_before_accepting_artifact() -> None:
    clock = FakeClock()
    responses = Responses([[_artifact()]])
    calls = 0

    def limited(path: str) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise tool.RateLimitError("HTTP 403 rate limit", retry_after=90)
        assert clock.now >= 90
        return responses(path)

    assert wait(limited, timeout=100, clock=clock, sleep=clock.sleep) == tool.Ready(2, 91)
    assert clock.sleeps == [90]


def test_rate_limit_longer_than_deadline_makes_no_retry() -> None:
    clock = FakeClock()
    calls = 0

    def limited(_path: str) -> Any:
        nonlocal calls
        calls += 1
        raise tool.RateLimitError("HTTP 403 rate limit", retry_after=3600)

    with pytest.raises(TimeoutError, match="after 10 seconds"):
        wait(limited, clock=clock, sleep=clock.sleep)
    assert calls == 1
    assert clock.now == 10


def test_repeated_rate_limits_back_off_within_original_deadline() -> None:
    clock = FakeClock()
    calls = 0

    def limited(_path: str) -> Any:
        nonlocal calls
        calls += 1
        raise tool.RateLimitError("HTTP 429 rate limit", retry_after=0)

    with pytest.raises(TimeoutError, match="after 200 seconds"):
        wait(limited, timeout=200, clock=clock, sleep=clock.sleep)
    assert clock.sleeps == [60, 120, 20]
    assert calls == 3


def test_active_missing_artifact_uses_at_most_forty_six_requests_in_ten_minutes() -> None:
    clock = FakeClock()
    paths: list[str] = []

    def missing(path: str) -> dict[str, Any]:
        paths.append(path)
        if "/jobs?" in path:
            return {"jobs": [_job()]}
        return {"artifacts": []}

    with pytest.raises(TimeoutError, match="after 600 seconds"):
        wait(missing, timeout=600, interval=5, clock=clock, sleep=clock.sleep)
    assert len(paths) <= 46
    assert clock.now == 600
    assert max(clock.sleeps) <= 30


def test_quota_recovery_still_refuses_a_previous_attempt_artifact() -> None:
    clock = FakeClock()
    calls = 0

    def stale(path: str) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        if calls == 1:
            raise tool.RateLimitError("HTTP 403 rate limit", retry_after=60)
        if "/jobs?" in path:
            return {"jobs": [_job()]}
        return {"artifacts": [_artifact(created_at=OLD_CREATED)]}

    with pytest.raises(TimeoutError, match="after 65 seconds"):
        wait(stale, timeout=65, clock=clock, sleep=clock.sleep)
    assert clock.now == 65


def test_gh_api_honors_quota_headers_and_default_secondary_backoff(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tool.time, "time", lambda: 1000.0)
    for status, headers, expected in [
        (
            "403 Forbidden",
            "Retry-After: 90\r\nX-RateLimit-Remaining: 0\r\nX-RateLimit-Reset: 1100",
            101,
        ),
        ("403 Forbidden", "Retry-After: 90", 90),
        ("429 Too Many Requests", "", 60),
    ]:

        def limited(
            _args: tuple[str, ...],
            _status: str = status,
            _headers: str = headers,
            **_kwargs: Any,
        ) -> subprocess.CompletedProcess[str]:
            return subprocess.CompletedProcess(
                [],
                1,
                stdout=f"HTTP/2.0 {_status}\r\n{_headers}\r\n\r\n{{}}",
                stderr=f"gh: API rate limit exceeded (HTTP {_status})",
            )

        monkeypatch.setattr(tool.subprocess, "run", limited)
        with pytest.raises(tool.RateLimitError) as error:
            tool.gh_api("repos/jlevy/squares/actions/runs/77/artifacts")
        assert error.value.retry_after == expected


def test_gh_api_permission_denial_is_not_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    def denied(_args: tuple[str, ...], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            [],
            1,
            stdout="HTTP/2.0 403 Forbidden\nX-RateLimit-Remaining: 4500\n\n{}",
            stderr="gh: Resource not accessible by integration (HTTP 403)",
        )

    monkeypatch.setattr(tool.subprocess, "run", denied)
    with pytest.raises(OSError, match="Resource not accessible") as error:
        tool.gh_api("repos/jlevy/squares/actions/runs/77/artifacts")
    assert type(error.value) is OSError


def test_gh_api_decodes_included_response_and_rejects_invalid_retry_window(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def success(_args: tuple[str, ...], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            [],
            0,
            stdout='HTTP/2.0 200 OK\r\nContent-Type: application/json\r\n\r\n{"jobs": []}',
            stderr="",
        )

    monkeypatch.setattr(tool.subprocess, "run", success)
    assert tool.gh_api("repos/jlevy/squares/actions/runs/77/jobs") == {"jobs": []}

    def invalid(_args: tuple[str, ...], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            [],
            1,
            stdout="HTTP/2.0 429 Too Many Requests\nRetry-After: nan\n\n{}",
            stderr="gh: API rate limit exceeded (HTTP 429)",
        )

    monkeypatch.setattr(tool.subprocess, "run", invalid)
    with pytest.raises(ValueError, match="non-finite retry window"):
        tool.gh_api("repos/jlevy/squares/actions/runs/77/jobs")


@pytest.mark.parametrize("finished_at", [10.0, 11.0])
def test_jobs_response_consuming_deadline_starts_no_artifact_request(
    finished_at: float,
) -> None:
    clock = FakeClock()
    paths: list[str] = []

    def slow_jobs(path: str) -> dict[str, Any]:
        paths.append(path)
        clock.now = finished_at
        if "/jobs?" in path:
            return {"jobs": [_job()]}
        return {"artifacts": [_artifact()]}

    with pytest.raises(TimeoutError, match="after 10 seconds"):
        wait(slow_jobs, clock=clock, sleep=clock.sleep)
    assert len(paths) == 1
    assert "/jobs?" in paths[0]
    assert clock.sleeps == []


@pytest.mark.parametrize("finished_at", [10.0, 11.0])
def test_successful_artifact_response_arriving_after_deadline_is_refused(
    finished_at: float,
) -> None:
    clock = FakeClock()
    paths: list[str] = []

    def slow_artifact(path: str) -> dict[str, Any]:
        paths.append(path)
        if "/jobs?" in path:
            clock.now = 9
            return {"jobs": [_job()]}
        clock.now = finished_at
        return {"artifacts": [_artifact()]}

    with pytest.raises(TimeoutError, match="after 10 seconds"):
        wait(slow_artifact, clock=clock, sleep=clock.sleep)
    assert len(paths) == 2
    assert clock.sleeps == []
