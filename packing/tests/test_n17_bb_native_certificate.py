"""Fast certificate replay against Python proof decisions with embedded tinylp."""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from types import ModuleType

import pytest

from devtools import n17_bb_native as wiring
from devtools import pilot_n17_subpattern_bb as pilot
from devtools.n17_bb_certificate_replay import compare_certificates, python_tinylp

A_CELLS = "interior-SW,interior-NW,interior-W,interior-S,interior-N,interior-SE"


def _native_or_skip(monkeypatch: pytest.MonkeyPatch) -> tuple[Path, ModuleType]:
    configured = os.environ.get("N17BB_NATIVE_DIR")
    if configured is None or not Path(configured).expanduser().is_dir():
        if os.environ.get("N17BB_NATIVE_REQUIRED") == "1":
            pytest.fail("N17BB_NATIVE_DIR must name the native extension directory")
        pytest.skip("N17BB_NATIVE_DIR is unset or absent; build n17bb_native first")
    directory = Path(configured).expanduser().resolve()
    monkeypatch.syspath_prepend(str(directory))
    importlib.invalidate_caches()
    try:
        native = importlib.import_module("n17bb_native")
    except ImportError as error:
        if os.environ.get("N17BB_NATIVE_REQUIRED") == "1":
            pytest.fail(str(error))
        pytest.skip(str(error))
    assert Path(native.__file__ or "").resolve().parent == directory
    return directory, native


def test_certificate_bytes_and_no_python_fallback(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every recorded byte agrees, and all three old fallback entry points fail hard."""
    native_was_loaded = "n17bb_native" in sys.modules
    directory, native = _native_or_skip(monkeypatch)
    settings = pilot.Settings(max_nodes=4, max_seconds=60.0)
    with python_tinylp(native):
        pattern = pilot.cover_pattern(A_CELLS.split(","))
        reference = pilot.search(pattern, settings, certificate=tmp_path / "python")

    def forbidden_fallback(*_arguments: object) -> None:
        pytest.fail("recording used a Python pair/LP/tighten fallback")

    with pytest.MonkeyPatch.context() as patches:
        for method in ("pair_term", "solve_lp", "tighten"):
            patches.setattr(pilot.Solver, method, forbidden_fallback)
        patches.setattr(pilot, "dual_bound", pilot.dual_bound)
        patches.setitem(vars(wiring), "_installed", None)
        for module in (pilot, pilot.cover):
            for name in ("Fraction", "Q"):
                if name in vars(module):
                    patches.setitem(vars(module), name, vars(module)[name])
        _ = wiring.install(directory)
        actual = pilot.search(pattern, settings, certificate=tmp_path / "native")
    if not native_was_loaded:
        _ = sys.modules.pop("n17bb_native", None)

    assert reference["nodes"] == actual["nodes"] == 4
    assert reference["verdict"] == actual["verdict"] == "unresolved-at-budget"
    files, size = compare_certificates(tmp_path / "python", tmp_path / "native")
    assert files > 0
    assert size > 0
