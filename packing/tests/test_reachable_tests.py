# pyright: reportPrivateUsage=false
"""The pre-push tier can only ever run too many tests, never too few (BC-086).

Every case here is one of the conservative promises `devtools.reachable_tests` makes.
The two regression cases at the top are 2026-08-30's red pushes replayed: a change to
`validate.py` must select the two test files that pinned it (D-381, D-393), and a
change nobody can attribute must select everything.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest

from devtools import pages_scope, reachable_tests
from devtools.reachable_tests import pytest_command, select_tests
from sqpack.cli import validate


@pytest.fixture(autouse=True)
def _isolate_parent_reachable_receipt(monkeypatch: pytest.MonkeyPatch) -> None:
    """Unit runner mocks must not inherit the enclosing validation command's receipt."""
    monkeypatch.delenv("PACKING_REACHABLE_TEST_ARTIFACT_STEM", raising=False)
    monkeypatch.delenv("PACKING_REACHABLE_TEST_RUN_ID", raising=False)


@pytest.fixture(scope="module", autouse=True)
def _one_static_tree() -> None:
    """Every question here is put to one static tree, whose parse `select_tests` memoizes
    for the life of the process. Pay that parse once, in this module's setup, rather than
    in whichever test happens to run first: on jlevy/squares#353 it pushed the first one
    past the 12 s per-test rule while the call itself takes well under a second."""
    select_tests(["packing/src/sqpack/cli/validate.py"])
    select_tests([".github/workflows/pages.yml"])


def test_a_change_to_validate_selects_the_tests_that_pinned_it() -> None:
    """The D-381 pair: both stale-pin failures lived in these two files."""
    selection = select_tests(["packing/src/sqpack/cli/validate.py"])
    assert not selection.everything
    assert "packing/tests/test_validation_cli.py" in selection.tests
    assert "packing/tests/test_module_boundaries.py" in selection.tests


def test_a_changed_data_file_selects_the_test_that_names_it() -> None:
    selection = select_tests(["packing/devtools/controls.yaml"])
    assert not selection.everything
    assert "packing/tests/test_control_anchors.py" in selection.tests


def test_changed_release_data_selects_the_release_contract() -> None:
    selection = select_tests(["packing/frontier/results.yaml"])
    assert not selection.everything
    assert "packing/tests/test_release.py" in selection.tests


def test_a_changed_test_file_selects_itself() -> None:
    selection = select_tests(["packing/tests/test_reachable_tests.py"])
    assert not selection.everything
    assert "packing/tests/test_reachable_tests.py" in selection.tests


def test_a_workbench_tool_change_selects_its_package_tests() -> None:
    selection = select_tests(["packages/workbench/tools/workbench_tools/packing_contracts.py"])
    assert not selection.everything
    assert "packages/workbench/tests/test_python_contract_repairs.py" in selection.tests


def test_a_changed_workbench_test_file_selects_itself() -> None:
    path = "packages/workbench/tests/test_benchmark_admission.py"
    selection = select_tests([path])
    assert not selection.everything
    assert path in selection.tests


def test_nothing_determined_selects_everything() -> None:
    assert select_tests([]).everything


def test_python_outside_the_mapped_roots_selects_everything() -> None:
    assert select_tests(["docs/scripts/mystery.py"]).everything


def test_a_benchmark_only_change_selects_its_reachable_tests() -> None:
    """BC-142: the agenda-014 push tier ran all 1,302 tests for a change whose only
    Python was `benchmarks/n17_weighted_certificate_parallel.py`, because that root was
    unmapped. Mapped, the change reaches the test that names it and not the suite."""
    selection = select_tests(["packing/benchmarks/n17_weighted_certificate_parallel.py"])
    assert not selection.everything
    assert "packing/tests/test_n17_weighted_certificate_parallel.py" in selection.tests
    assert "packing/tests/test_reachable_tests.py" not in selection.tests


def test_an_unmapped_python_root_is_still_refused_into_everything() -> None:
    """Mapping one more root must not weaken the refusal for the next unmapped one."""
    assert select_tests(["packing/scripts/unmapped.py"]).everything


@pytest.mark.parametrize(
    "path",
    [
        "packing/pyproject.toml",
        "packing/uv.lock",
        "packing/tests/conftest.py",
        "packing/.python-version",
        "packages/workbench/pyproject.toml",
        ".github/workflows/packing-validation.yml",
        ".github/workflows/unknown.yml",
        "pyproject.toml",
    ],
)
def test_suite_configuration_selects_everything(path: str) -> None:
    assert select_tests([path]).everything


def test_pages_workflow_selects_every_declared_publication_test() -> None:
    selection = select_tests([".github/workflows/pages.yml"])
    assert not selection.everything, selection.reason
    expected = {
        "packing/tests/test_pages_workflow.py",
        "packing/tests/test_pages_scope.py",
        "packing/tests/test_site_rendering.py",
        "packing/tests/test_check_published_site.py",
    }
    for job in pages_scope.load_workflow()["jobs"].values():
        for step in job.get("steps", []):
            expected.update(
                f"packing/{target}"
                for target in re.findall(r"\btests/[\w/.-]+\.py\b", str(step.get("run", "")))
            )
    assert expected <= set(selection.tests)


def test_pages_selection_keeps_real_unmapped_python_fallback() -> None:
    selection = select_tests([".github/workflows/pages.yml", "docs/scripts/unmapped.py"])
    assert selection.everything
    assert "unmapped.py" in selection.reason


def test_pages_selection_refuses_missing_workflow_entrypoint(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        pages_scope,
        "load_workflow",
        lambda: {
            "jobs": {"check": {"steps": [{"run": "python -m devtools.missing_pages_tool"}]}}
        },
    )
    selection = select_tests([".github/workflows/pages.yml"])
    assert selection.everything
    assert "missing_pages_tool" in selection.reason


@pytest.mark.parametrize("module", ["sqpack.some_tool", "cases.some_tool", "$PAGE_TOOL"])
def test_pages_selection_refuses_unknown_python_entrypoints(
    monkeypatch: pytest.MonkeyPatch, module: str
) -> None:
    monkeypatch.setattr(
        pages_scope,
        "load_workflow",
        lambda: {"jobs": {"check": {"steps": [{"run": f"python -m {module}"}]}}},
    )
    selection = select_tests([".github/workflows/pages.yml"])
    assert selection.everything
    assert "unknown Pages Python entrypoint" in selection.reason


@pytest.mark.parametrize("extra", ["tests", "tests/test_*.py", "$TEST_TARGETS"])
def test_pages_selection_refuses_mixed_unknown_pytest_targets(
    monkeypatch: pytest.MonkeyPatch, extra: str
) -> None:
    monkeypatch.setattr(
        pages_scope,
        "load_workflow",
        lambda: {
            "jobs": {
                "check": {"steps": [{"run": f"pytest -q tests/test_pages_workflow.py {extra}"}]}
            }
        },
    )
    selection = select_tests([".github/workflows/pages.yml"])
    assert selection.everything
    assert "unknown selection" in selection.reason


def test_pages_selection_refuses_unreadable_workflow(monkeypatch: pytest.MonkeyPatch) -> None:
    def unreadable() -> dict[str, object]:
        raise OSError("unreadable Pages workflow")

    monkeypatch.setattr(pages_scope, "load_workflow", unreadable)
    selection = select_tests([".github/workflows/pages.yml"])
    assert selection.everything
    assert "unreadable Pages workflow" in selection.reason


def test_pages_selection_refuses_malformed_workflow(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    path = tmp_path / "pages.yml"
    path.write_text("jobs: [unterminated", encoding="utf-8")
    load_workflow = pages_scope.load_workflow
    monkeypatch.setattr(pages_scope, "load_workflow", lambda: load_workflow(path))
    selection = select_tests([".github/workflows/pages.yml"])
    assert selection.everything
    assert "Pages invocation inputs could not be resolved" in selection.reason


@pytest.mark.parametrize("everything", [False, True])
@pytest.mark.parametrize("workers", [1, 4])
def test_running_selected_tests_preserves_coverage_and_uses_requested_workers(
    monkeypatch: pytest.MonkeyPatch, *, everything: bool, workers: int
) -> None:
    selection = reachable_tests.TestSelection(
        everything=everything,
        reason="fixture selection",
        tests=(
            "packing/tests/test_reachable_tests.py",
            "packing/tests/test_validation_cli.py",
            "packages/workbench/tests/test_benchmark_admission.py",
        ),
    )
    monkeypatch.setattr(reachable_tests, "changed_paths", lambda _since: ["changed"])
    monkeypatch.setattr(reachable_tests, "select_tests", lambda _changed: selection)
    commands: list[tuple[str, ...]] = []

    def capture(
        command: tuple[str, ...], *, cwd: Path, check: bool
    ) -> subprocess.CompletedProcess[str]:
        assert cwd == reachable_tests.ROOT
        assert not check
        commands.append(command)
        return subprocess.CompletedProcess(command, returncode=7)

    monkeypatch.setattr(reachable_tests.subprocess, "run", capture)
    assert reachable_tests.main(["--run", "--numprocesses", str(workers)]) == 7
    targets = (
        reachable_tests.BEHAVIORAL_TEST_ROOTS
        if everything
        else (
            "tests/test_reachable_tests.py",
            "tests/test_validation_cli.py",
            "../packages/workbench/tests/test_benchmark_admission.py",
        )
    )
    assert commands == [
        (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            *targets,
            "-m",
            "not exhaustive_exact",
            *(("-n", "4") if workers == 4 else ()),
            "--durations=0",
            "--durations-min=0",
        )
    ]


@pytest.mark.parametrize("workers", ["0", "-1"])
def test_invalid_worker_counts_are_refused_before_selection(
    monkeypatch: pytest.MonkeyPatch, workers: str
) -> None:
    monkeypatch.setattr(
        reachable_tests, "changed_paths", lambda _since: pytest.fail("must not select")
    )
    with pytest.raises(SystemExit) as error:
        reachable_tests.main(["--run", "--numprocesses", workers])
    assert error.value.code == 2


def test_repository_walkers_run_for_any_change() -> None:
    """A test that enumerates the repository has the whole path space as input."""
    selection = select_tests(["packing/frontier/n-011.md"])
    assert selection.everything or (
        "packing/tests/test_verified_upper_bound_contract.py" in selection.tests
    )


def test_the_floor_tiers_need_no_marker() -> None:
    """A lock held by one's own gate must not talk an operator out of the floor."""
    records = validate._select_steps(only=[], fast=True, records=True)
    edit = validate._select_steps(only=[], fast=False, edit=True)
    assert not validate._selection_needs_marker(records)
    assert not validate._selection_needs_marker(edit)


def test_the_heavy_tiers_still_take_the_marker() -> None:
    fast = validate._select_steps(only=[], fast=True)
    full = validate._select_steps(only=[], fast=False)
    assert validate._selection_needs_marker(fast)
    assert validate._selection_needs_marker(full)


def test_push_is_its_own_tier() -> None:
    try:
        validate._validate_invocation(
            strict=False, only=[], fast=True, records=False, edit=False, push=True
        )
    except validate.UsageError as error:
        assert "--push is its own tier" in str(error)
    else:  # pragma: no cover - the refusal is the contract
        raise AssertionError("--push combined with --fast must be refused")


def test_the_selection_runs_under_the_workers_the_caller_asks_for() -> None:
    """`D-488`: the runner carried no distribution, so every push ran its tests serially.

    The number is the caller's to choose -- `cpus - jobs + 1` is about how many outer
    slots are already busy, which this module cannot see -- so what is pinned here is
    that the caller's answer reaches pytest, and that one worker asks for nothing rather
    than paying for an xdist protocol with no concurrency behind it.
    """
    serial = pytest_command(["tests"], 1)
    assert "-n" not in serial
    assert serial[-4:] == ("-m", "not exhaustive_exact", "--durations=0", "--durations-min=0")

    parallel = pytest_command(["tests"], 4)
    assert parallel[-4:] == ("-n", "4", "--durations=0", "--durations-min=0")
    assert parallel[: parallel.index("-n")] == serial[: serial.index("--durations=0")]


def test_the_push_step_forwards_the_distribution_both_lanes_use(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The step the pre-push tier builds must carry the flag, not merely accept one.

    `D-488` lived in the gap between those two: `devtools.reachable_tests` grew no
    distribution and `sqpack.cli.validate` passed none, so the rule `_xdist_distribution`
    documents -- four workers at `--jobs 1` on a four-cpu box -- was silently not applied
    on the one tier a contributor runs before every push. Pinning the caller's side as
    well as the runner's is what stops the flag from being dropped again on one side.

    `_pytest_workers` is pinned rather than read, so the assertion does not restate the
    formula under test and does not depend on how many cpus the box running it has.
    """

    def probe(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        del args, kwargs
        return subprocess.CompletedProcess(
            args=("reachable-tests",), returncode=0, stdout="everything\n", stderr=""
        )

    monkeypatch.setattr(validate.subprocess, "run", probe)
    step = validate._push_test_step("origin/main")

    seen: list[tuple[str, ...]] = []

    def capture(_context: validate.Context, command: tuple[str, ...]) -> str:
        seen.append(tuple(command))
        return ""

    monkeypatch.setattr(validate, "_run", capture)
    monkeypatch.setattr(validate, "_pytest_workers", lambda jobs: 7 if jobs == 1 else 1)

    def context(jobs: int, inner_jobs: int) -> validate.Context:
        return validate.Context(
            deep=False,
            strict=False,
            jobs=jobs,
            inner_jobs=inner_jobs,
            environment=dict(os.environ),
        )

    step.action(context(1, 3))
    step.action(context(4, 2))

    assert seen[0][seen[0].index("-n") :][:2] == ("-n", "7"), seen[0]
    assert "-n" not in seen[1], seen[1]
    assert seen[0][seen[0].index("--pool-workers") :][:2] == ("--pool-workers", "3")
    assert seen[1][seen[1].index("--pool-workers") :][:2] == ("--pool-workers", "2")
    assert "--run" in seen[0]
    assert "--since" in seen[0]


def test_the_runner_wires_its_argument_to_the_command_it_builds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The join between the two halves, which the other two tests leave unpinned.

    Both of them can pass while `main` builds its command with a literal instead of
    `namespace.numprocesses` -- the CLI would accept `-n` and silently drop it, which is
    D-488's own shape one layer in: an argument that exists and does not arrive. This
    reads the argv the runner actually hands to `subprocess.run`.
    """
    selection = SimpleNamespace(everything=True, tests=(), reason="everything here")
    monkeypatch.setattr(reachable_tests, "changed_paths", lambda _since: ["x"])
    monkeypatch.setattr(reachable_tests, "select_tests", lambda _paths: selection)

    seen: list[tuple[str, ...]] = []

    def capture(command: Sequence[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        del kwargs
        seen.append(tuple(command))
        return subprocess.CompletedProcess(args=tuple(command), returncode=0)

    monkeypatch.setattr(reachable_tests.subprocess, "run", capture)

    assert reachable_tests.main(["--run", "--since", "origin/main", "-n", "3"]) == 0
    assert reachable_tests.main(["--run", "--since", "origin/main"]) == 0

    assert seen[0][seen[0].index("-n") :][:2] == ("-n", "3"), seen[0]
    assert "-n" not in seen[1], seen[1]


@pytest.mark.parametrize(
    ("normal_status", "normal_probe", "pool_status", "pool_probe", "expected", "phases"),
    [
        (0, None, 0, None, 0, ("normal", "pool")),
        (5, 5, 0, None, 0, ("normal", "probe", "pool")),
        (0, None, 5, 5, 0, ("normal", "pool", "probe")),
        (5, 5, 5, 5, 5, ("normal", "probe", "pool", "probe")),
        (1, None, 0, None, 1, ("normal",)),
        (-15, None, 0, None, -15, ("normal",)),
        (5, 0, 0, None, 5, ("normal", "probe")),
        (0, None, 5, 2, 5, ("normal", "pool", "probe")),
    ],
)
def test_pool_phases_preserve_complements_failures_and_proved_empty_lanes(
    monkeypatch: pytest.MonkeyPatch,
    *,
    normal_status: int,
    normal_probe: int | None,
    pool_status: int,
    pool_probe: int | None,
    expected: int,
    phases: tuple[str, ...],
) -> None:
    selection = reachable_tests.TestSelection(
        everything=False,
        reason="fixture",
        tests=("packing/tests/test_reachable_tests.py",),
    )
    monkeypatch.setattr(reachable_tests, "changed_paths", lambda _since: ["changed"])
    monkeypatch.setattr(reachable_tests, "select_tests", lambda _changed: selection)
    seen: list[str] = []

    def capture(command: tuple[str, ...], **kwargs: object) -> subprocess.CompletedProcess[str]:
        assert kwargs["cwd"] == reachable_tests.ROOT
        marker = command[command.index("-m", 2) + 1]
        assert "tests/test_reachable_tests.py" in command
        if "--collect-only" in command:
            seen.append("probe")
            status = normal_probe if "not pool_heavy" in marker else pool_probe
            assert status is not None
            assert "-n" not in command
            return subprocess.CompletedProcess(command, status)
        environment = cast("dict[str, str]", kwargs["env"])
        if "not pool_heavy" in marker:
            seen.append("normal")
            assert command[command.index("-n") :][:2] == ("-n", "4")
            assert environment["PACK_JOBS"] == "1"
            return subprocess.CompletedProcess(command, normal_status)
        seen.append("pool")
        assert marker == "not exhaustive_exact and pool_heavy"
        assert "-n" not in command
        assert environment["PACK_JOBS"] == "4"
        return subprocess.CompletedProcess(command, pool_status)

    monkeypatch.setattr(reachable_tests.subprocess, "run", capture)
    assert reachable_tests.main(["--run", "-n", "4", "--pool-workers", "4"]) == expected
    assert tuple(seen) == phases


def test_pool_interruption_does_not_launch_the_second_phase(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(reachable_tests, "changed_paths", lambda _since: ["changed"])
    monkeypatch.setattr(
        reachable_tests,
        "select_tests",
        lambda _changed: reachable_tests.TestSelection(
            everything=False,
            reason="fixture",
            tests=("packing/tests/test_reachable_tests.py",),
        ),
    )
    seen: list[tuple[str, ...]] = []

    def interrupted(
        command: tuple[str, ...], **_kwargs: object
    ) -> subprocess.CompletedProcess[str]:
        seen.append(command)
        raise KeyboardInterrupt

    monkeypatch.setattr(reachable_tests.subprocess, "run", interrupted)
    with pytest.raises(KeyboardInterrupt):
        reachable_tests.main(["--run", "--pool-workers", "2"])
    assert len(seen) == 1
    assert "not pool_heavy" in seen[0][seen[0].index("-m", 2) + 1]


@pytest.mark.parametrize("workers", ["0", "-1"])
def test_invalid_pool_worker_counts_refuse_before_selection(
    monkeypatch: pytest.MonkeyPatch, workers: str
) -> None:
    monkeypatch.setattr(
        reachable_tests, "changed_paths", lambda _since: pytest.fail("must not select")
    )
    with pytest.raises(SystemExit) as error:
        reachable_tests.main(["--run", "--pool-workers", workers])
    assert error.value.code == 2


def test_pool_split_executes_the_exact_selected_tests_once_each(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    test_file = tmp_path / "test_pool_split.py"
    test_file.write_text(
        "import os\n"
        "from pathlib import Path\n"
        "import pytest\n"
        "def test_normal():\n"
        "    Path(os.environ['SPLIT_OUTPUT']).joinpath('normal')"
        ".write_text(os.environ['PACK_JOBS'])\n"
        "@pytest.mark.pool_heavy\n"
        "def test_pool():\n"
        "    Path(os.environ['SPLIT_OUTPUT']).joinpath('pool')"
        ".write_text(os.environ['PACK_JOBS'])\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("SPLIT_OUTPUT", str(tmp_path))
    monkeypatch.delenv("PACKING_REACHABLE_TEST_ARTIFACT_STEM", raising=False)
    monkeypatch.setattr(reachable_tests, "REPO", tmp_path)
    monkeypatch.setattr(reachable_tests, "changed_paths", lambda _since: ["changed"])
    monkeypatch.setattr(
        reachable_tests,
        "select_tests",
        lambda _changed: reachable_tests.TestSelection(
            everything=False, reason="fixture", tests=("test_pool_split.py",)
        ),
    )
    assert reachable_tests.main(["--run", "-n", "2", "--pool-workers", "2"]) == 0
    assert (tmp_path / "normal").read_text(encoding="utf-8") == "1"
    assert (tmp_path / "pool").read_text(encoding="utf-8") == "2"


def test_whole_atlas_pool_heavy_collection_is_one_canonical_node() -> None:
    command = (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "--collect-only",
        "-m",
        "pool_heavy",
        "tests/test_known_best_atlas.py",
    )
    result = subprocess.run(
        command, cwd=reachable_tests.ROOT, check=False, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr
    collected = {line for line in result.stdout.splitlines() if "::test_" in line}
    assert collected == {
        "tests/test_known_best_atlas.py::test_known_best_composite_contains_every_case_and_square"
    }
