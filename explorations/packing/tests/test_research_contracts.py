"""Fast contracts for reusable numerical research helpers."""

from __future__ import annotations

import base64
import math
from pathlib import Path
from typing import cast

import numpy as np
import yaml
from scipy.optimize import linprog

from sqpack.research.closed_form import recognise

N4_STATUS4_FIXTURE = Path(__file__).parent / "fixtures/n4_seed0_highs_status4.yaml"


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
