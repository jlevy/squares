"""Fast contracts for reusable numerical research helpers."""

from __future__ import annotations

import base64
import math
from pathlib import Path
from typing import cast

import numpy as np
import pytest
import yaml
from scipy.optimize import OptimizeResult, linprog

from sqpack.research import quench
from sqpack.research.closed_form import recognise

N4_STATUS4_FIXTURE = Path(__file__).parent / "fixtures/n4_seed0_highs_status4.yaml"
Cell = list[tuple[int, int, float, float, float, float]]
LPCall = tuple[
    str,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    list[tuple[float | None, float | None]],
    dict[str, float],
]


def _unhex(value: str | None) -> float | None:
    return None if value is None else float.fromhex(value)


def _mapping(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    return cast(dict[str, object], value)


def _items(value: object) -> list[object]:
    assert isinstance(value, list)
    return value


def _hex_float(value: object) -> float:
    assert isinstance(value, str)
    return float.fromhex(value)


def _integer(value: object) -> int:
    assert isinstance(value, int)
    return value


def _float(value: object) -> float:
    assert isinstance(value, (float, int, str))
    return float(value)


def _f64_le(encoded: str, shape: tuple[int, ...]) -> np.ndarray:
    values = np.frombuffer(base64.b64decode(encoded), dtype="<f8")
    return values.reshape(shape)


def _rebuild_n4_lp(
    data: dict[str, object], cell: list[dict[str, object]] | None = None
) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[tuple[float | None, float | None]]]:
    """Independently reconstruct the fixed-cell LP; do not call ``solve_cell``."""
    inputs = _mapping(data["input_hex"])
    theta = [_hex_float(value) for value in _items(inputs["theta"])]
    raw_cell = [_mapping(value) for value in _items(inputs["cell"])] if cell is None else cell
    n, nv = 4, 9
    obj = np.zeros(nv)
    obj[0] = 1.0
    rows: list[np.ndarray] = []
    rhs: list[float] = []
    for k, angle in enumerate(theta):
        cosine, sine = math.cos(angle), math.sin(angle)
        extent_x = 0.5 * (abs(cosine) + abs(sine))
        extent_y = 0.5 * (abs(sine) + abs(cosine))
        for coord, half in ((1 + k, extent_x), (1 + n + k, extent_y)):
            lo = np.zeros(nv)
            lo[coord] = -1.0
            rows.append(lo)
            rhs.append(-half)
            hi = np.zeros(nv)
            hi[coord] = 1.0
            hi[0] = -1.0
            rows.append(hi)
            rhs.append(-half)
    for record in raw_cell:
        i, j = _integer(record["i"]), _integer(record["j"])
        ax, ay, h, sign = (_hex_float(record[key]) for key in ("ax", "ay", "h", "sign"))
        row = np.zeros(nv)
        row[1 + i], row[1 + j] = -sign * ax, sign * ax
        row[1 + n + i], row[1 + n + j] = -sign * ay, sign * ay
        rows.append(row)
        rhs.append(-h)
    lower_bounded: tuple[float | None, float | None] = (0.0, None)
    unbounded: tuple[float | None, float | None] = (None, None)
    bounds: list[tuple[float | None, float | None]] = []
    bounds.append(lower_bounded)
    bounds.extend([unbounded] * 8)
    return obj, np.array(rows), np.array(rhs), bounds


def test_closed_form_recognises_simple_surd_without_overclaiming() -> None:
    form = recognise(2 + math.sqrt(2) / 2)

    assert form is not None
    assert (form.p, form.q, form.d, form.r) == (4, 1, 2, 2)
    assert recognise(math.pi, tol=1e-14) is None


def test_n4_seed0_highs_failure_fixture_is_replayable() -> None:
    data = _mapping(yaml.safe_load(N4_STATUS4_FIXTURE.read_text()))
    obj, a_ub, b_ub, bounds = _rebuild_n4_lp(data)
    recorded = _mapping(data["linprog"])
    assert np.array_equal(obj, _f64_le(cast(str, recorded["obj_f64_le_base64"]), (9,)))
    expected_a_ub = np.vstack(
        [_f64_le(cast(str, row), (9,)) for row in _items(recorded["a_ub_rows_f64_le_base64"])]
    )
    assert np.array_equal(a_ub, expected_a_ub)
    assert np.array_equal(b_ub, _f64_le(cast(str, recorded["b_ub_f64_le_base64"]), (22,)))
    assert bounds == [
        tuple(_unhex(cast(str | None, value)) for value in _items(pair))
        for pair in _items(recorded["bounds"])
    ]

    options = {key: _float(value) for key, value in _mapping(recorded["options"]).items()}
    receipt = _mapping(recorded["receipt"])
    assert receipt == {
        "success": False,
        "status": 4,
        "message": "(HiGHS Status 4: Solve error)",
    }
    result = linprog(
        obj,
        A_ub=a_ub,
        b_ub=b_ub,
        bounds=bounds,
        method=cast(str, recorded["method"]),
        options=options,
    )
    if result.status == 4:
        assert result.success is False
        assert str(result.message) == "(HiGHS Status 4: Solve error)"
    else:
        assert result.success, (result.status, result.message)
        assert result.x is not None and result.x.shape == (9,)
        assert np.isfinite(result.x).all()
        assert np.max(a_ub @ result.x - b_ub) <= 1e-10

    inputs = _mapping(data["input_hex"])
    mutated = [dict(_mapping(entry)) for entry in _items(inputs["cell"])]
    mutated[0]["ax"] = "0x1.0000000000000p-1"
    _, bad_a_ub, _, _ = _rebuild_n4_lp(data, mutated)
    assert not np.array_equal(bad_a_ub, a_ub)


def _n4_fixture_cell(data: dict[str, object]) -> tuple[list[float], Cell]:
    """Decode the captured cell without routing through cell selection."""
    inputs = _mapping(data["input_hex"])
    theta = [_hex_float(value) for value in _items(inputs["theta"])]
    cell: Cell = []
    for entry in _items(inputs["cell"]):
        record = _mapping(entry)
        cell.append(
            (
                _integer(record["i"]),
                _integer(record["j"]),
                _hex_float(record["ax"]),
                _hex_float(record["ay"]),
                _hex_float(record["h"]),
                _hex_float(record["sign"]),
            )
        )
    return theta, cell


def _valid_n2_cell() -> tuple[list[float], Cell, np.ndarray]:
    """A fixed horizontal two-square LP with a known feasible optimum."""
    theta = [0.0, 0.0]
    cell = [(0, 1, 1.0, 0.0, 1.0, -1.0)]
    return theta, cell, np.array([2.0, 0.5, 1.5, 0.5, 0.5])


def _result(*, status: int, success: bool, x: np.ndarray | None = None) -> OptimizeResult:
    return OptimizeResult(
        status=status,
        success=success,
        message=f"scripted status {status}",
        x=x,
    )


def _assert_attempt_indices(result: quench.CellSolveResult) -> None:
    assert [receipt.solver_call for receipt in result.attempt_receipts] == list(
        range(1, len(result.attempt_receipts) + 1)
    )


def test_n4_status4_fixture_is_recovered_or_primary_optimal() -> None:
    """The captured LP is portable: HiGHS or its scoped IPM fallback must certify it."""
    data = _mapping(yaml.safe_load(N4_STATUS4_FIXTURE.read_text()))
    theta, cell = _n4_fixture_cell(data)
    _, a_ub, b_ub, _ = _rebuild_n4_lp(data)

    result = quench.solve_cell(theta, cell, 4)

    assert result.outcome == "optimal"
    assert result.side is not None
    candidate = np.array([result.side, *result.x, *result.y])
    assert candidate.shape == (9,)
    assert np.isfinite(candidate).all()
    assert np.max(a_ub @ candidate - b_ub) <= quench.LP_FEASIBLE_EPS
    assert result.solver_calls == len(result.attempt_receipts)
    _assert_attempt_indices(result)
    assert [receipt.method for receipt in result.attempt_receipts] in (
        ["highs"],
        ["highs", "highs-ipm"],
    )
    assert result.attempt_receipts[0].method == "highs"
    if len(result.attempt_receipts) == 2:
        primary, fallback = result.attempt_receipts
        assert (primary.status, primary.success, fallback.method, fallback.success) == (
            4,
            False,
            "highs-ipm",
            True,
        )


def test_solve_cell_status4_uses_one_ipm_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    theta, cell, solution = _valid_n2_cell()
    calls: list[LPCall] = []

    def scripted(
        obj: np.ndarray,
        *,
        A_ub: np.ndarray,  # noqa: N803 - mirrors scipy.optimize.linprog's keyword
        b_ub: np.ndarray,
        bounds: list[tuple[float | None, float | None]],
        method: str,
        options: dict[str, float],
    ) -> OptimizeResult:
        calls.append(
            (method, obj.copy(), A_ub.copy(), b_ub.copy(), list(bounds), dict(options))
        )
        return (
            _result(status=4, success=False)
            if method == "highs"
            else _result(status=0, success=True, x=solution)
        )

    monkeypatch.setattr(quench, "linprog", scripted)

    result = quench.solve_cell(theta, cell, 2)

    assert result.outcome == "optimal"
    assert [call[0] for call in calls] == ["highs", "highs-ipm"]
    first, fallback = calls
    assert np.array_equal(first[1], fallback[1])
    assert np.array_equal(first[2], fallback[2])
    assert np.array_equal(first[3], fallback[3])
    assert first[4:] == fallback[4:]
    assert [receipt.method for receipt in result.attempt_receipts] == [
        call[0] for call in calls
    ]
    assert [(receipt.status, receipt.success) for receipt in result.attempt_receipts] == [
        (4, False),
        (0, True),
    ]
    assert result.solver_calls == 2
    _assert_attempt_indices(result)
    assert result.max_violation is not None and result.max_violation <= quench.LP_FEASIBLE_EPS


def test_solve_cell_status4_ipm_failure_stays_typed(monkeypatch: pytest.MonkeyPatch) -> None:
    theta, cell, _ = _valid_n2_cell()
    calls: list[str] = []

    def scripted(*_args: object, method: str, **_kwargs: object) -> OptimizeResult:
        calls.append(method)
        if method == "highs":
            return _result(status=4, success=False)
        return _result(status=1, success=False)

    monkeypatch.setattr(quench, "linprog", scripted)

    result = quench.solve_cell(theta, cell, 2)

    assert result.outcome == "solver_failure"
    assert calls == ["highs", "highs-ipm"]
    assert [receipt.method for receipt in result.attempt_receipts] == calls
    assert [(receipt.status, receipt.success) for receipt in result.attempt_receipts] == [
        (4, False),
        (1, False),
    ]
    assert result.solver_calls == 2
    _assert_attempt_indices(result)


def test_solve_cell_status4_ipm_status2_stays_solver_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    theta, cell, _ = _valid_n2_cell()
    calls: list[str] = []

    def scripted(*_args: object, method: str, **_kwargs: object) -> OptimizeResult:
        calls.append(method)
        return (
            _result(status=4, success=False)
            if method == "highs"
            else _result(status=2, success=False)
        )

    monkeypatch.setattr(quench, "linprog", scripted)

    result = quench.solve_cell(theta, cell, 2)

    assert result.outcome == "solver_failure"
    assert calls == ["highs", "highs-ipm"]
    assert [(receipt.status, receipt.success) for receipt in result.attempt_receipts] == [
        (4, False),
        (2, False),
    ]
    assert result.solver_calls == 2
    _assert_attempt_indices(result)


@pytest.mark.parametrize(
    ("status", "outcome"),
    [(1, "solver_failure"), (2, "infeasible")],
)
def test_solve_cell_non_status4_primary_failure_never_falls_back(
    monkeypatch: pytest.MonkeyPatch,
    status: int,
    outcome: str,
) -> None:
    theta, cell, _ = _valid_n2_cell()
    calls: list[str] = []

    def scripted(*_args: object, method: str, **_kwargs: object) -> OptimizeResult:
        calls.append(method)
        return _result(status=status, success=False)

    monkeypatch.setattr(quench, "linprog", scripted)

    result = quench.solve_cell(theta, cell, 2)

    assert result.outcome == outcome
    assert calls == ["highs"]
    assert [
        (receipt.method, receipt.status, receipt.success) for receipt in result.attempt_receipts
    ] == [
        ("highs", status, False),
    ]
    assert result.solver_calls == 1
    _assert_attempt_indices(result)


def test_solve_cell_nonfinite_successful_ipm_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    theta, cell, _ = _valid_n2_cell()

    def scripted(*_args: object, method: str, **_kwargs: object) -> OptimizeResult:
        if method == "highs":
            return _result(status=4, success=False)
        return _result(status=0, success=True, x=np.full(5, np.nan))

    monkeypatch.setattr(quench, "linprog", scripted)

    result = quench.solve_cell(theta, cell, 2)

    assert result.outcome == "postcheck_rejection"
    assert result.solver_calls == 2
    assert [receipt.method for receipt in result.attempt_receipts] == ["highs", "highs-ipm"]
    _assert_attempt_indices(result)


def test_solve_cell_ipm_bad_residual_refuses_at_total_cap(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    theta, cell, _ = _valid_n2_cell()
    calls: list[str] = []

    def scripted(*_args: object, method: str, **_kwargs: object) -> OptimizeResult:
        calls.append(method)
        if method == "highs":
            return _result(status=4, success=False)
        return _result(status=0, success=True, x=np.zeros(5))

    monkeypatch.setattr(quench, "linprog", scripted)

    result = quench.solve_cell(theta, cell, 2)

    assert result.outcome == "postcheck_rejection"
    assert result.max_violation is not None and result.max_violation > quench.LP_FEASIBLE_EPS
    assert calls == ["highs", "highs-ipm", "highs-ipm", "highs-ipm"]
    assert [receipt.method for receipt in result.attempt_receipts] == calls
    assert result.solver_calls == len(calls) == quench.MAX_RESIDUAL_SOLVER_CALLS
    _assert_attempt_indices(result)
