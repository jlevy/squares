"""Fresh synthetic checkout provenance and private-worker isolation controls."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from devtools import check_checkout_imports as preflight


def checkout(root: Path) -> None:
    for directory in preflight.MODULES.values():
        p = root / directory
        p.mkdir(parents=True, exist_ok=True)
        (p / "__init__.py").write_text("")
    (root / "packing/src/sqpack/cli/validate.py").write_text("")


def test_binding_is_child_local_and_clears_stale_parent_override(tmp_path: Path) -> None:
    inherited = {
        "PYTHONPATH": "old-parent",
        "PACKING_PROJECT_ROOT": "old-parent",
        "PATH": "unchanged",
    }
    first = preflight.environment_for(tmp_path / "parent", inherited)
    private = preflight.environment_for(tmp_path / "private", first)
    assert inherited["PACKING_PROJECT_ROOT"] == "old-parent"
    assert "PACKING_PROJECT_ROOT" not in first
    assert "parent" not in private["PYTHONPATH"]
    assert first["PATH"] == private["PATH"] == "unchanged"


def test_fresh_check_refuses_contamination_and_accepts_explicit_private_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent, private = tmp_path / "parent", tmp_path / "private"
    checkout(parent)
    checkout(private)
    monkeypatch.setenv("PYTHONPATH", preflight.environment_for(parent, {})["PYTHONPATH"])
    assert preflight.check(private)["status"] == "REFUSED"
    assert preflight.check(private, bind_paths=True)["status"] == "PASS"
    assert os.environ["PYTHONPATH"] == preflight.environment_for(parent, {})["PYTHONPATH"]


def test_stale_project_root_refuses_without_binding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    checkout(tmp_path)
    monkeypatch.setenv("PYTHONPATH", preflight.environment_for(tmp_path, {})["PYTHONPATH"])
    monkeypatch.setenv("PACKING_PROJECT_ROOT", "stale")
    assert preflight.check(tmp_path)["status"] == "REFUSED"
    assert preflight.check(tmp_path, bind_paths=True)["status"] == "PASS"


def test_missing_workbench_refuses_before_long_gate(tmp_path: Path) -> None:
    checkout(tmp_path)
    (tmp_path / "packages/workbench/tools/workbench_tools/__init__.py").unlink()
    # An empty namespace at the expected path remains a valid location, so remove it.
    (tmp_path / "packages/workbench/tools/workbench_tools").rmdir()
    assert preflight.check(tmp_path, bind_paths=True)["status"] == "REFUSED"
