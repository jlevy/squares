# pyright: reportPrivateUsage=false
"""The pre-push tier can only ever run too many tests, never too few (BC-086).

Every case here is one of the conservative promises `devtools.reachable_tests` makes.
The two regression cases at the top are 2026-08-30's red pushes replayed: a change to
`validate.py` must select the two test files that pinned it (D-381, D-393), and a
change nobody can attribute must select everything.
"""

from __future__ import annotations

import os
import subprocess
from collections.abc import Sequence
from types import SimpleNamespace

import pytest

from devtools import reachable_tests
from devtools.reachable_tests import pytest_command, select_tests
from sqpack.cli import validate


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


def test_a_changed_test_file_selects_itself() -> None:
    selection = select_tests(["packing/tests/test_reachable_tests.py"])
    assert not selection.everything
    assert "packing/tests/test_reachable_tests.py" in selection.tests


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
        ".github/workflows/packing-validation.yml",
        "pyproject.toml",
    ],
)
def test_suite_configuration_selects_everything(path: str) -> None:
    assert select_tests([path]).everything


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
    assert serial[-2:] == ("-m", "not exhaustive_exact")

    parallel = pytest_command(["tests"], 4)
    assert parallel[-2:] == ("-n", "4")
    assert parallel[: len(serial)] == serial


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

    def context(jobs: int) -> validate.Context:
        return validate.Context(
            deep=False, strict=False, jobs=jobs, inner_jobs=1, environment=dict(os.environ)
        )

    step.action(context(1))
    step.action(context(4))

    assert seen[0][-2:] == ("-n", "7"), seen[0]
    assert "-n" not in seen[1], seen[1]
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

    assert seen[0][-2:] == ("-n", "3"), seen[0]
    assert "-n" not in seen[1], seen[1]
