# pyright: reportPrivateUsage=false
"""The pre-push tier can only ever run too many tests, never too few (BC-086).

Every case here is one of the conservative promises `devtools.reachable_tests` makes.
The two regression cases at the top are 2026-08-30's red pushes replayed: a change to
`validate.py` must select the two test files that pinned it (D-381, D-393), and a
change nobody can attribute must select everything.
"""

from __future__ import annotations

import pytest

from devtools.reachable_tests import select_tests
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
