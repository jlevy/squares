"""`devtools.verified_merge_tree`: a post-merge skip is licensed by a tree, never by a label."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import pytest

from devtools import verified_merge_tree as tool

REPOSITORY = "jlevy/squares"
TREE = "eddcb83517dc9280d217fc9411659af5dbad8b87"


def _run(run_id: int, **overrides: Any) -> dict[str, Any]:
    run: dict[str, Any] = {
        "id": run_id,
        "event": "pull_request",
        "path": tool.WORKFLOW_PATH,
        "status": "completed",
        "conclusion": "success",
        "repository": {"full_name": REPOSITORY},
        "head_repository": {"full_name": REPOSITORY},
    }
    run.update(overrides)
    return run


def _api(runs: list[dict[str, Any]], *, expired: frozenset[int] = frozenset()) -> tool.Api:
    artifacts = [
        {
            "name": tool.artifact_name(TREE),
            "expired": run["id"] in expired,
            "workflow_run": {"id": run["id"]},
        }
        for run in runs
    ]
    by_id = {run["id"]: run for run in runs}

    def api(path: str) -> Any:
        if path.startswith(f"repos/{REPOSITORY}/actions/artifacts?"):
            assert f"name={tool.artifact_name(TREE)}" in path
            return {"artifacts": artifacts}
        return by_id[int(path.rsplit("/", 1)[-1])]

    return api


def test_a_successful_pull_request_run_of_this_workflow_licenses_the_tree() -> None:
    verdict = tool.verify(TREE, repository=REPOSITORY, api=_api([_run(7), _run(9)]))
    assert verdict.run_id == 9, "the newest proving run is named"


@pytest.mark.parametrize(
    ("override", "reason"),
    [
        ({"conclusion": "failure"}, "conclusion is 'failure'"),
        ({"conclusion": "cancelled"}, "conclusion is 'cancelled'"),
        ({"status": "in_progress", "conclusion": None}, "status is 'in_progress'"),
        ({"event": "push"}, "event is 'push'"),
        ({"path": ".github/workflows/pages.yml"}, "workflow is"),
        ({"head_repository": {"full_name": "someone/fork"}}, "a fork's run is not accepted"),
    ],
)
def test_anything_short_of_a_successful_same_repository_run_names_nothing(
    override: dict[str, Any], reason: str
) -> None:
    verdict = tool.verify(TREE, repository=REPOSITORY, api=_api([_run(5, **override)]))
    assert verdict.run_id is None
    assert any(reason in line for line in verdict.reasons), verdict.reasons


def test_a_refused_newer_run_does_not_hide_an_older_proof() -> None:
    runs = [_run(4), _run(8, conclusion="failure")]
    verdict = tool.verify(TREE, repository=REPOSITORY, api=_api(runs))
    assert verdict.run_id == 4


def test_no_artifact_an_expired_one_or_an_api_error_all_fail_toward_the_full_surface() -> None:
    assert tool.verify(TREE, repository=REPOSITORY, api=_api([])).run_id is None
    expired = tool.verify(
        TREE, repository=REPOSITORY, api=_api([_run(3)], expired=frozenset({3}))
    )
    assert expired.run_id is None

    def broken(_path: str) -> Any:
        raise OSError("HTTP 403: Resource not accessible by integration")

    failed = tool.verify(TREE, repository=REPOSITORY, api=broken)
    assert failed.run_id is None
    assert "artifact lookup failed" in failed.reasons[0]


def test_main_writes_the_named_run_or_an_empty_one_to_the_step_output(
    tmp_path: Path,
) -> None:
    head = subprocess.run(
        ("git", "rev-parse", "HEAD"), capture_output=True, text=True, check=True, cwd=tool.REPO
    ).stdout.strip()
    tree = tool.tree_of(head)
    output = tmp_path / "github-output"

    def api(path: str) -> Any:
        if "artifacts?" in path:
            assert f"name={tool.artifact_name(tree)}" in path
            return {
                "artifacts": [
                    {
                        "name": tool.artifact_name(tree),
                        "expired": False,
                        "workflow_run": {"id": 42},
                    }
                ]
            }
        return _run(42)

    assert (
        tool.main(
            ["--sha", head, "--repository", REPOSITORY, "--github-output", str(output)], api=api
        )
        == 0
    )
    assert (
        tool.main(
            ["--sha", "0" * 40, "--repository", REPOSITORY, "--github-output", str(output)],
            api=api,
        )
        == 0
    )
    assert output.read_text(encoding="utf-8").splitlines() == ["run=42", "run="]
