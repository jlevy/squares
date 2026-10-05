"""Fail-safe boundaries for the optional native n=17 kernel."""

from __future__ import annotations

import importlib
import math
import os
import struct
import sys
from pathlib import Path
from types import ModuleType

import pytest


@pytest.fixture(scope="module")
def native() -> ModuleType:
    """Import the explicitly selected native build or skip with its build remedy."""
    configured = os.environ.get("N17BB_NATIVE_DIR")
    if configured is None:
        pytest.skip("N17BB_NATIVE_DIR is unset; build n17bb_native before edge tests")
    directory = Path(configured).expanduser().resolve()
    if not directory.is_dir():
        pytest.skip(f"native module directory does not exist: {directory}")
    sys.path.insert(0, str(directory))
    importlib.invalidate_caches()
    try:
        module = importlib.import_module("n17bb_native")
    except ImportError as error:
        pytest.skip(f"n17bb_native is not importable from {directory}: {error}")
    finally:
        sys.path.remove(str(directory))
    loaded_from = Path(module.__file__ or "").resolve()
    assert loaded_from.parent == directory
    return module


def _boxes(count: int) -> list[tuple[float, float, float, float]]:
    return [(0.0, 1.0, -0.0, 1.0)] * count


@pytest.mark.parametrize("count", [1, 7, 15])
def test_empty_rows_admit_supported_box_limits(native: ModuleType, count: int) -> None:
    session = native.LpSession([], [], [], [], [], [], _boxes(count))
    status, value, point, duals, closed = session.lp_step(1.0e-9)
    assert status == "optimal"
    assert value == -1.0
    assert point == [0.0] * (2 * count)
    assert duals == []
    assert closed is False
    assert session.tighten() == _boxes(count)


@pytest.mark.parametrize(
    ("arguments", "message"),
    [
        (([], [], [], [], [], [], []), "expected 1..15 boxes"),
        (([], [], [], [], [], [], _boxes(16)), "expected 1..15 boxes"),
        (
            (
                [[]] * 513,
                [[]] * 513,
                [0.0] * 513,
                [1.0] * 513,
                [[]] * 513,
                [(0.0, 0.0)] * 513,
                _boxes(1),
            ),
            "<=512 rows",
        ),
        (
            ([[2]], [[1.0]], [0.0], [1.0], [[(1.0, 1.0)]], [(0.0, 0.0)], _boxes(1)),
            "invalid row columns",
        ),
        (([[]], [], [], [], [], [], _boxes(1)), "matching row dimensions"),
    ],
)
def test_session_rejects_invalid_dimensions(
    native: ModuleType, arguments: tuple[object, ...], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        native.LpSession(*arguments)


def test_session_call_order_is_enforced(native: ModuleType) -> None:
    before = native.LpSession([], [], [], [], [], [], _boxes(1))
    with pytest.raises(ValueError, match="preceding lp_step"):
        before.tighten()

    session = native.LpSession([], [], [], [], [], [], _boxes(1))
    session.lp_step(1.0e-9)
    with pytest.raises(ValueError, match="called once"):
        session.lp_step(1.0e-9)
    assert session.tighten() == _boxes(1)
    with pytest.raises(ValueError, match="called once"):
        session.tighten()


def test_inverted_bounds_report_infeasible_without_panicking(native: ModuleType) -> None:
    boxes = [(1.0, 0.0, 0.0, 1.0)]
    session = native.LpSession([], [], [], [], [], [], boxes)
    status, value, point, duals, closed = session.lp_step(1.0e-9)
    assert status == "infeasible"
    assert value == math.inf
    assert point == [0.0, 0.0]
    assert duals == []
    assert closed is False
    assert session.tighten() == boxes


def test_tiny_lp_preserves_negative_zero(native: ModuleType) -> None:
    lp = native._TinyLP()  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    lp.load([], [], [-0.0], [-0.0], [1.0])
    status, value, point, duals = lp.solve()
    assert status == "optimal"
    assert struct.pack("!d", value) == struct.pack("!d", -0.0)
    assert struct.pack("!d", point[0]) == struct.pack("!d", -0.0)
    assert duals == []


def test_pair_core_rejects_unsupported_merging(native: ModuleType) -> None:
    multiples = {index: (index * math.pi / 2.0,) * 2 for index in range(5)}

    def trig(angle: float) -> tuple[tuple[float, float], tuple[float, float]]:
        cosine = math.cos(angle)
        sine = math.sin(angle)
        return (cosine, cosine), (sine, sine)

    with pytest.raises(ValueError, match="merge_gap=0"):
        native.Core(trig, multiples, 0.1)
    core = native.Core(trig, multiples, -0.0)
    assert core.pair_term(
        (-0.0, 0.0),
        (0.0, 0.0),
        None,
        (0.0, 0.0, 0.0, 0.0),
        (2.0, 2.0, 0.0, 0.0),
    ) == ("separated", [], [], [], [])
