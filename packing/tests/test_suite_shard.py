"""Contracts for deterministic whole-module pull-request suite sharding."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import cast

import pytest

from devtools import suite_shard


def _run_real_collection(tmp_path: Path, shard: int | None) -> tuple[set[str], set[str]]:
    report = tmp_path / f"collection-{shard}.json"
    environment = os.environ.copy()
    packing = Path(__file__).parents[1]
    old_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        str(packing)
        if old_pythonpath is None
        else os.pathsep.join((str(packing), old_pythonpath))
    )
    environment["SUITE_SHARD_REPORT"] = str(report)
    command = [
        sys.executable,
        "-m",
        "pytest",
        "--collect-only",
        "-q",
        "-m",
        "not excluded",
    ]
    if shard is not None:
        command.extend(("-p", "devtools.suite_shard", f"--suite-shard={shard}"))

    completed = subprocess.run(
        command,
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    payload = json.loads(report.read_text(encoding="utf-8"))
    return set(payload["selected"]), set(payload["deselected"])


def test_assignment_is_deterministic_complete_and_disjoint() -> None:
    counts = {
        "tests/test_large.py": 11,
        "tests/test_medium.py": 7,
        "../packages/workbench/tests/test_browser.py": 5,
        "tests/test_small.py": 2,
    }

    forward = suite_shard.assign_modules(counts)
    reverse = suite_shard.assign_modules(dict(reversed(counts.items())))

    assert forward == reverse
    assert set().union(*forward) == set(counts)
    assert forward[0].isdisjoint(forward[1])

    loads = [sum(counts[module] for module in shard) for shard in forward]
    assert max(loads) - min(loads) <= max(counts.values())


def test_a_new_module_enters_exactly_one_shard_without_a_registry() -> None:
    original = suite_shard.assign_modules({"tests/test_a.py": 9, "tests/test_b.py": 4})
    expanded_counts = {
        "tests/test_a.py": 9,
        "tests/test_b.py": 4,
        "tests/test_new.py": 3,
    }
    expanded = suite_shard.assign_modules(expanded_counts)

    assert set().union(*original) == {"tests/test_a.py", "tests/test_b.py"}
    assert sum("tests/test_new.py" in shard for shard in expanded) == 1
    assert set().union(*expanded) == set(expanded_counts)


def test_parametrizations_and_classes_stay_with_their_module() -> None:
    nodeids = [
        "tests/test_one.py::test_plain",
        "tests/test_one.py::TestCase::test_param[value::with:colons]",
        "../packages/workbench/tests/test_two.py::test_other",
    ]

    assert suite_shard.count_modules(nodeids) == {
        "tests/test_one.py": 2,
        "../packages/workbench/tests/test_two.py": 1,
    }


def test_collection_hook_runs_after_marker_and_third_party_selectors() -> None:
    implementation = cast(
        dict[str, object],
        vars(suite_shard.pytest_collection_modifyitems)["pytest_impl"],
    )

    assert implementation["trylast"] is True
    assert implementation["tryfirst"] is False


def test_real_pytest_collection_shards_the_post_marker_selection(tmp_path: Path) -> None:
    """Real marker deselection precedes a complete, disjoint whole-module split."""
    (tmp_path / "conftest.py").write_text(
        textwrap.dedent(
            """
            import json
            import os
            from pathlib import Path

            deselected = []

            def pytest_configure(config):
                config.addinivalue_line("markers", "excluded: omitted from the quick lane")

            def pytest_deselected(items):
                deselected.extend(item.nodeid for item in items)

            def pytest_collection_finish(session):
                Path(os.environ["SUITE_SHARD_REPORT"]).write_text(
                    json.dumps({
                        "selected": [item.nodeid for item in session.items],
                        "deselected": deselected,
                    }),
                    encoding="utf-8",
                )
            """
        ),
        encoding="utf-8",
    )
    (tmp_path / "test_alpha.py").write_text(
        "def test_a1(): pass\ndef test_a2(): pass\ndef test_a3(): pass\n",
        encoding="utf-8",
    )
    (tmp_path / "test_beta.py").write_text(
        textwrap.dedent(
            """
            import pytest

            def test_b1(): pass
            def test_b2(): pass
            @pytest.mark.excluded
            def test_excluded_1(): pass
            @pytest.mark.excluded
            def test_excluded_2(): pass
            @pytest.mark.excluded
            def test_excluded_3(): pass
            @pytest.mark.excluded
            def test_excluded_4(): pass
            """
        ),
        encoding="utf-8",
    )
    (tmp_path / "test_gamma.py").write_text("def test_c1(): pass\n", encoding="utf-8")

    baseline, baseline_deselected = _run_real_collection(tmp_path, None)
    shard_runs = [_run_real_collection(tmp_path, shard) for shard in range(2)]
    selected = [run[0] for run in shard_runs]
    deselected = [run[1] for run in shard_runs]

    assert len(baseline) == 6
    assert len(baseline_deselected) == 4
    assert selected[0] | selected[1] == baseline
    assert selected[0].isdisjoint(selected[1])
    assert selected[0] == {
        "test_alpha.py::test_a1",
        "test_alpha.py::test_a2",
        "test_alpha.py::test_a3",
    }
    assert selected[1] == {
        "test_beta.py::test_b1",
        "test_beta.py::test_b2",
        "test_gamma.py::test_c1",
    }
    excluded = {f"test_beta.py::test_excluded_{index}" for index in range(1, 5)}
    assert excluded == baseline_deselected
    assert all(excluded <= nodes for nodes in deselected)
    assert all(len(nodes) == 7 for nodes in deselected)


@dataclass
class _Hook:
    deselected: list[object] = field(default_factory=list)

    def pytest_deselected(self, *, items: list[object]) -> None:
        self.deselected.extend(items)


@dataclass
class _Config:
    shard: int
    hook: _Hook = field(default_factory=_Hook)

    def getoption(self, name: str) -> int:
        assert name == "suite_shard"
        return self.shard


@dataclass(frozen=True)
class _Item:
    nodeid: str


def test_collection_hook_selects_complementary_whole_module_shards() -> None:
    nodeids = [
        "tests/test_large.py::test_one",
        "tests/test_large.py::test_two",
        "tests/test_large.py::test_three",
        "tests/test_medium.py::test_one",
        "tests/test_medium.py::test_two",
        "../packages/workbench/tests/test_small.py::test_one",
    ]
    selected: list[set[str]] = []
    deselected: list[set[str]] = []

    for shard in range(suite_shard.SHARD_COUNT):
        config = _Config(shard)
        items = [_Item(nodeid) for nodeid in nodeids]
        suite_shard.pytest_collection_modifyitems(
            cast(pytest.Config, config), cast(list[pytest.Item], items)
        )
        selected.append({item.nodeid for item in items})
        deselected.append({cast(_Item, item).nodeid for item in config.hook.deselected})

    assert selected[0].isdisjoint(selected[1])
    assert selected[0] | selected[1] == set(nodeids)
    assert selected[0] == deselected[1]
    assert selected[1] == deselected[0]
    for module in {suite_shard.module_id(nodeid) for nodeid in nodeids}:
        owners = [
            index
            for index, nodes in enumerate(selected)
            if any(suite_shard.module_id(nodeid) == module for nodeid in nodes)
        ]
        assert len(owners) == 1


def test_invalid_assignment_inputs_are_refused() -> None:
    try:
        suite_shard.assign_modules({}, shard_count=0)
    except ValueError as error:
        assert str(error) == "shard_count must be positive"
    else:
        raise AssertionError("a zero-shard assignment was accepted")

    try:
        suite_shard.assign_modules({"tests/test_empty.py": 0})
    except ValueError as error:
        assert str(error) == "module item counts must be positive"
    else:
        raise AssertionError("an empty collected module was accepted")
