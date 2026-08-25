"""Behavioral tests for the self-documenting packing validation command."""

# These contracts deliberately exercise the CLI module's internal functional seams.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import io
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

from sqpack.cli import validate
from sqpack.cli.validate import main


def _invoke(*arguments: str) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        status = main(list(arguments))
    return status, stdout.getvalue(), stderr.getvalue()


def test_list_is_read_only_and_exposes_fast_and_full_check_groups() -> None:
    status, stdout, stderr = _invoke("--list")

    assert status == 0
    assert stderr == ""
    assert "fast behavioral tests [fast]" in stdout
    assert "soundness perimeter [full, engine]" in stdout


def test_list_applies_the_same_fast_and_name_filters_as_execution() -> None:
    status, stdout, stderr = _invoke("--list", "--fast")

    assert status == 0
    assert stderr == ""
    assert "fast behavioral tests [fast]" in stdout
    assert "soundness perimeter" not in stdout

    status, stdout, stderr = _invoke("--list", "--only", "negative control")

    assert status == 0
    assert stderr == ""
    assert stdout.splitlines() == ["negative controls [full]"]


def test_invalid_worker_count_and_unmatched_selection_are_actionable() -> None:
    status, _, stderr = _invoke("--jobs", "0", "--list")
    assert status == 2
    assert "--jobs must be a positive integer" in stderr

    status, _, stderr = _invoke("--only", "not-a-real-step")
    assert status == 2
    assert "matched no validation step" in stderr
    assert "packing-validate --list" in stderr


def test_strict_mode_refuses_a_partial_validation_surface() -> None:
    status, _, stderr = _invoke("--strict", "--only", "fast behavioral tests")

    assert status == 2
    assert "--strict cannot be combined with --only or --fast" in stderr


def test_strict_mode_enables_deep_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    observed: validate.Context | None = None

    def capture_context(
        selected: list[validate.Step], context: validate.Context, patterns: list[str]
    ) -> validate.RunSummary:
        del patterns
        nonlocal observed
        observed = context
        return validate.RunSummary(
            results=[],
            wall_seconds=0,
            selected_count=len(selected),
            total_count=len(validate.STEPS),
        )

    monkeypatch.setattr(validate, "_run_selected", capture_context)

    status, _, stderr = _invoke("--strict")

    assert status == 0
    assert stderr == ""
    assert observed is not None
    if not observed.deep:
        pytest.fail("strict mode did not enable deep validation")


def test_existing_activity_marker_explains_safe_recovery(tmp_path: Path) -> None:
    marker = tmp_path / ".gate-running"
    marker.mkdir()

    with (
        pytest.raises(validate.StepFailureError, match="Wait for it, or delete"),
        validate._validation_activity(marker),
    ):
        pytest.fail("an existing marker must prevent validation")


def test_missing_provenance_object_is_not_called_an_orphan() -> None:
    assert validate._commit_state("0" * 40) == "missing"


def test_annotated_lost_provenance_object_is_reported_unavailable() -> None:
    line = validate._provenance_line(
        "exp-001.md",
        "d6a1057",
        "## Annotation\n`engine_commit: d6a1057` is unreachable after a rebase.",
        "missing",
    )

    assert "UNAVAILABLE" in line
    assert "ORPHANED" not in line

    with pytest.raises(validate.StepFailureError, match="fetch complete history"):
        validate._provenance_line("unannotated.md", "deadbee", "", "missing")


def test_basin_event_archives_are_discovered_from_their_contract(tmp_path: Path) -> None:
    (tmp_path / "baseline.jsonl").write_text('{"kind": "result"}\n', encoding="utf-8")
    (tmp_path / "events-v2.jsonl").write_text(
        '{"contract": "packing.squares:BasinEvent/v2"}\n', encoding="utf-8"
    )
    (tmp_path / "events-v3.jsonl").write_text(
        '{"contract": "packing.squares:BasinEvent/v3"}\n', encoding="utf-8"
    )

    assert [path.name for path in validate._basin_event_archives(tmp_path)] == [
        "events-v2.jsonl",
        "events-v3.jsonl",
    ]


def test_failure_summary_uses_singular_step_for_one_failure() -> None:
    summary = validate.RunSummary(
        results=[validate.StepResult("broken", "failed", 0.1, reason="because")],
        wall_seconds=0.1,
        selected_count=1,
        total_count=1,
    )
    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        status = validate._render_text(summary, strict=False)

    assert status == 1
    assert "1 STEP FAILED:" in stdout.getvalue()


def test_frontier_contract_accepts_the_declared_schema_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # The full gate runs pytest while its real activity marker is present. Give this
    # deliberately nested CLI contract an isolated marker without weakening the
    # production exclusion between validation and campaign execution.
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    status, stdout, stderr = _invoke("--only", "frontier corpus", "--jobs", "1")

    assert status == 0
    assert stderr == ""
    assert "100 artifacts, n = 1..100, 35 proved, 65 open" in stdout
