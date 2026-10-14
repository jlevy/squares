"""A real-event quick checkpoint enforces the canonical suites without silent omissions."""

from __future__ import annotations

import io
import itertools
import os
import re
import shlex
import subprocess
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from typing import Any, cast

import pytest

from devtools import check_enforced_quick as coverage
from sqpack.cli import validate
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
WORKFLOW = REPO / ".github/workflows/enforced-quick.yml"


def workflow() -> dict[str, Any]:
    return cast(dict[str, Any], safe_load(WORKFLOW.read_text()))


def test_checkpoint_self_changes_bootstrap_on_a_real_push_and_can_be_dispatched() -> None:
    document = workflow()
    assert set(document["on"]) == {"push", "workflow_dispatch"}
    assert document["on"]["push"] == {
        "paths": [
            ".github/workflows/enforced-quick.yml",
            "packing/tests/test_enforced_quick_workflow.py",
        ]
    }
    assert "branches" not in document["on"]["push"]
    assert document["permissions"] == {"contents": "read"}
    assert document["concurrency"]["cancel-in-progress"] is False
    normal = safe_load((REPO / ".github/workflows/packing-validation.yml").read_text())
    assert normal["on"]["pull_request"] == {}
    assert normal["on"]["push"] == {"branches": ["main"]}
    assert "schedule" in normal["on"]
    assert normal["jobs"]["packing-required"]["if"] == (
        "!cancelled() && github.event_name == 'pull_request'"
    )
    assert "enforced-quick-required" not in normal["jobs"]


def test_checkpoint_retains_exact_identity_browser_floor_and_pinned_setup() -> None:
    document = workflow()
    assert document["env"]["SQPACK_REQUIRE_CHROMIUM"] == "1"
    assert document["env"]["PACKING_VALIDATION_ARTIFACT_DIR"].startswith(
        "${{ github.workspace }}-"
    )
    references = [
        safe_load((REPO / ".github/workflows" / name).read_text())
        for name in ("packing-validation.yml", "pages.yml")
    ]
    pinned = {
        step["uses"]
        for reference in references
        for job in reference["jobs"].values()
        for step in job.get("steps", [])
        if "uses" in step
    }
    for job in document["jobs"].values():
        assert job.get("permissions", document["permissions"]).get("contents") == "read"
        for environment in (
            job.get("env", {}),
            *(step.get("env", {}) for step in job["steps"]),
        ):
            assert not {"GITHUB_EVENT_NAME", "GITHUB_ACTIONS"} & set(environment)
        for step in job["steps"]:
            if "uses" in step:
                assert re.fullmatch(r"[^@]+@[0-9a-f]{40}", step["uses"])
                assert step["uses"] in pinned
                if step["uses"].startswith("actions/checkout@"):
                    assert step["with"] == {
                        "ref": "${{ github.sha }}",
                        "fetch-depth": 0,
                        "submodules": True,
                        "persist-credentials": False,
                    }
                elif step["uses"].startswith("astral-sh/setup-uv@"):
                    assert step["with"]["version"] == "0.12.8"
                    assert step["with"]["python-version"] == "3.14.7"
    steps = document["jobs"]["suite"]["steps"]
    runs = "\n".join(step.get("run", "") for step in steps)
    assert 'test "$(git rev-parse HEAD)" = "$GITHUB_SHA"' in runs
    assert "source-sha.txt" in runs
    assert "tree-sha.txt" in runs
    assert "npm ci --ignore-scripts" in runs
    assert "playwright install --with-deps --only-shell chromium" in runs
    assert (
        next(step for step in steps if step.get("uses", "").startswith("actions/setup-node@"))[
            "with"
        ]["node-version"]
        == "24.18.0"
    )
    upload = next(
        step for step in steps if step.get("uses", "").startswith("actions/upload-artifact@")
    )
    assert upload["if"] == "always()"
    assert upload["with"]["if-no-files-found"] == "error"
    assert "${{ matrix.suite }}" in upload["with"]["name"]


def test_the_four_matrix_commands_select_the_four_canonical_enforced_suites() -> None:
    job = workflow()["jobs"]["suite"]
    assert job["strategy"] == {"fail-fast": False, "matrix": {"suite": list("abcd")}}
    command = next(step["run"] for step in job["steps"] if step.get("id") == "quick")
    selected: set[str] = set()
    for suite in "abcd":
        tokens = shlex.split(command.replace("${{ matrix.suite }}", suite))
        arguments = tokens[tokens.index("packing-validate") + 1 :]
        assert arguments == [f"--suite-{suite}", "--jobs", "1", "--inner-jobs", "1"]
        output = io.StringIO()
        with redirect_stdout(output):
            assert validate.main(["--list", "--format", "json", *arguments]) == 0
        import json  # noqa: PLC0415

        names = {row["name"] for row in json.loads(output.getvalue())}
        assert names == {f"fast behavioral tests, shard {suite.upper()}"}
        assert not names & selected
        selected |= names
    assert len(selected) == 4
    assert validate.QUICK_TEST_WALL_BACKSTOP_SECONDS == 12


@pytest.mark.parametrize(
    ("suite", "controls"),
    itertools.product(("success", "failure", "cancelled", "skipped"), repeat=2),
)
def test_aggregate_rejects_any_failed_cancelled_or_skipped_prerequisite(
    suite: str, controls: str
) -> None:
    aggregate = workflow()["jobs"]["enforced-quick-required"]
    assert aggregate["if"] == "always()"
    assert aggregate["needs"] == ["suite", "negative-controls"]
    step = aggregate["steps"][0]
    assert step["env"] == {
        "SUITE_RESULT": "${{ needs.suite.result }}",
        "CONTROLS_RESULT": "${{ needs.negative-controls.result }}",
    }
    result = subprocess.run(
        ("bash", "-e", "-c", step["run"]),
        check=False,
        env={**os.environ, "SUITE_RESULT": suite, "CONTROLS_RESULT": controls},
        capture_output=True,
    )
    assert (result.returncode == 0) == (suite == controls == "success")
    assert any("--aggregate" in item.get("run", "") for item in aggregate["steps"])


def test_execution_receipts_refuse_missing_skipped_duplicate_or_foreign_cases() -> None:
    node = "tests.test_site_forwarders::test_arrival[plain]"
    assert coverage.execution_problems({node}, {node: "passed"}, set()) == []
    assert coverage.execution_problems({node}, {}, set())
    assert coverage.execution_problems({node}, {node: "skipped"}, set())
    assert coverage.execution_problems(set(), {node: "skipped"}, set())
    optional = next(iter(coverage.KNOWN_OMISSIONS))
    assert coverage.execution_problems(set(), {optional: "skipped"}, set()) == []
    module = "packing/" + optional.split("::", 1)[0].replace(".", "/") + ".py"
    assert coverage.execution_problems(set(), {optional: "skipped"}, {module})
    xml = (
        '<testsuites><testsuite><testcase classname="tests.test_site_forwarders" '
        'name="test_arrival[plain]"/></testsuite></testsuites>'
    )
    assert coverage.junit_nodes([xml]) == {node: "passed"}
    with pytest.raises(coverage.CoverageError, match="repeated"):
        coverage.junit_nodes([xml, xml])
    with pytest.raises(coverage.CoverageError, match="no actual"):
        coverage.junit_nodes(["<testsuites/>"])


def test_complete_aggregate_requires_five_distinct_successful_source_bound_receipts() -> None:
    sha = "a" * 40
    receipts = [
        {"suite": suite, "source_sha": sha, "status": "success", "passed_cases": 1}
        for suite in [*"abcd", "negative-controls"]
    ]
    receipts[-1]["passed_cases"] = 10
    receipts[-1]["selected_controls"] = sorted(coverage.NEGATIVE_CONTROL_NAMES)
    assert coverage.aggregate_problems(receipts, sha) == []
    assert coverage.aggregate_problems(receipts[:4], sha)
    for changed in ("status", "source_sha", "passed_cases", "suite"):
        bad = deepcopy(receipts)
        bad[0][changed] = {
            "status": "cancelled",
            "source_sha": "b" * 40,
            "passed_cases": 0,
            "suite": "b",
        }[changed]
        assert coverage.aggregate_problems(bad, sha)


def test_schema_control_selection_and_journal_require_exact_ten_current_controls() -> None:
    registry = safe_load((REPO / "packing/devtools/controls.yaml").read_text())
    controls = coverage.select_negative_controls(registry)
    assert len(controls) == 10
    assert all("devtools.validate_schemas" in row["run"] for row in controls)
    with pytest.raises(coverage.CoverageError, match="ten"):
        coverage.select_negative_controls({"controls": controls[:-1]})
    with pytest.raises(coverage.CoverageError, match="ten"):
        coverage.select_negative_controls({"controls": [*controls, controls[0]]})
    events = [
        {"event": "run_started", "selected_controls": sorted(coverage.NEGATIVE_CONTROL_NAMES)},
        *(
            {"event": "control_finished", "name": name, "status": "passed"}
            for name in coverage.NEGATIVE_CONTROL_NAMES
        ),
        {"event": "run_finished", "status": "passed", "completed": 10},
    ]
    assert coverage.negative_control_problems(events) == []
    assert coverage.negative_control_problems(events[:-2] + events[-1:])
    bad = deepcopy(events)
    bad[1]["status"] = "failed"
    assert coverage.negative_control_problems(bad)
    job = workflow()["jobs"]["negative-controls"]
    assert any("--negative-controls" in step.get("run", "") for step in job["steps"])
    assert any(
        step.get("if") == "always()" and "upload-artifact@" in step.get("uses", "")
        for step in job["steps"]
    )


def test_required_collection_uses_physical_paths_and_actual_junit_names(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import json  # noqa: PLC0415

    paths = ["packing/tests/test_one.py", "packages/workbench/tests/test_poster.py"]
    rows = [
        {"path": paths[0], "key": "tests.test_one.TestGroup::test_case[a::b]"},
        {"path": paths[1], "key": "test_poster::test_poster[a::b]"},
        {"path": "packing/tests/test_other.py", "key": "tests.test_other::test_case"},
    ]
    calls: list[tuple[str, ...]] = []

    def collected(command: tuple[str, ...], **_kwargs: Any) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        return subprocess.CompletedProcess(
            command, 0, coverage.COLLECTION_PREFIX + json.dumps(rows), ""
        )

    monkeypatch.setattr(coverage.subprocess, "run", collected)
    assert coverage.collect_nodes(paths) == {rows[0]["key"], rows[1]["key"]}
    assert calls[0][-2:] == validate.BEHAVIORAL_TEST_ROOTS
    assert "devtools.check_enforced_quick" in calls[0]
    with pytest.raises(coverage.CoverageError, match="no quick cases"):
        coverage.collect_nodes(["packages/workbench/tests/test_missing.py"])
    skipped = "test_poster::test_ffmpeg_returns_the_frame_asked_for"
    assert coverage.execution_problems(set(), {skipped: "skipped"}, {paths[1]})


def test_collection_hook_preserves_workbench_path_class_and_parameter_identity(
    capsys: pytest.CaptureFixture[str],
) -> None:
    import json  # noqa: PLC0415
    from types import SimpleNamespace  # noqa: PLC0415

    session = cast(
        pytest.Session,
        SimpleNamespace(
            items=[
                SimpleNamespace(
                    path=REPO / "packages/workbench/tests/test_poster.py",
                    nodeid="test_poster.py::TestGroup::test_poster[a::b]",
                )
            ]
        ),
    )
    coverage.pytest_collection_finish(session)
    output = capsys.readouterr().out.strip().removeprefix(coverage.COLLECTION_PREFIX)
    assert json.loads(output) == [
        {
            "path": "packages/workbench/tests/test_poster.py",
            "key": "test_poster.TestGroup::test_poster[a::b]",
        }
    ]
