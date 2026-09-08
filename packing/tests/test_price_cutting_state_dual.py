"""Focused controls for paired pricing of one retained cutting state."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from devtools import price_cutting_state_dual as pricing
from sqpack.fractional.cutting import Separation


@pytest.fixture(autouse=True)
def stable_source_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pricing, "source_binding", lambda path: {"path": path.name})


def _state(path: Path, rows: int = 40) -> None:
    path.write_text(
        json.dumps(
            {
                "outer_side": "2",
                "square_side": "1",
                "half_tangents": ["0", "1/3"],
                "sites": [["1", "1"]],
                "rows": [[0, str(Fraction(50 + index, 100)), "1"] for index in range(rows)],
                "best_family": {
                    "n": 11,
                    "outer_side": "2",
                    "square_side": "1",
                    "half_tangents": ["0", "1/3"],
                    "placements": [["0", "1", "1", "1", "1"]],
                },
            }
        )
        + "\n"
    )


def _solve(rows: int = 40) -> tuple[np.ndarray, np.ndarray, float]:
    return np.ones(1), np.array([1 - index / 100 for index in range(rows)]), 10.0


def test_positive_control_retains_more_than_32_rows_from_one_solve(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    solved = tmp_path / "solved.json"
    priced = tmp_path / "priced.json"
    _state(state)
    solve_calls = 0

    def fake_solve(*_args: Any) -> tuple[np.ndarray, np.ndarray, float]:
        nonlocal solve_calls
        solve_calls += 1
        return _solve()

    def fake_lines(_family: Any) -> list[Any]:
        assert solved.exists(), "support receipt must precede geometry"
        return []

    orbit = ((Fraction(1, 3), Fraction(1, 4)),)
    separation_calls = 0

    def fake_separation(*_args: Any, **_kwargs: Any) -> Separation:
        nonlocal separation_calls
        separation_calls += 1
        if separation_calls == 1:
            return Separation(Fraction(1), 2, 3, 0, [])
        return Separation(Fraction(3, 2), 4, 5, 1, [(Fraction(3, 2), orbit)])

    def fake_membership(
        family: Any, _point: tuple[Fraction, Fraction]
    ) -> tuple[Fraction, list[int]]:
        if len(family.placements) == 32 * 8:
            return Fraction(1), [0]
        return Fraction(3, 2), [0, 32 * 8]

    monkeypatch.setattr(pricing, "solve_lp", fake_solve)
    monkeypatch.setattr(pricing, "arrangement_lines", fake_lines)
    monkeypatch.setattr(pricing, "screened_separation", fake_separation)
    monkeypatch.setattr(pricing, "_exact_membership", fake_membership)
    result = pricing.price_state(state, solved, priced)
    support = json.loads(solved.read_text())

    assert solve_calls == 1
    assert separation_calls == 2
    assert len(support["positive_support"]) == 40
    assert len(support["full_family"]["placements"]) == 40 * 8
    assert result["arms"]["paired32"]["support_rows"] == 32
    assert result["arms"]["full"]["support_rows"] == 40
    assert result["arms"]["paired32"]["dual_source"] == result["arms"]["full"]["dual_source"]
    assert result["solved_support"] == "solved.json"
    assert result["classification"] == "paired_32_row_miss"
    assert result["witness_checks"][0] == {
        "point": ["1/3", "1/4"],
        "orbit": [["1/3", "1/4"]],
        "orbit_absent_from_state": True,
        "paired32": {"depth": "1", "placement_indices": [0]},
        "full": {"depth": "3/2", "placement_indices": [0, 256]},
    }
    assert result["arms"]["full"]["separation"]["qualifying_new_points"][0]["point"] == [
        "1/3",
        "1/4",
    ]


def test_empty_paired_chosen_does_not_claim_a_miss_at_the_full_witness(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A held paired violation can leave ``chosen`` empty without clearing the witness."""
    state = tmp_path / "state.json"
    _state(state)
    monkeypatch.setattr(pricing, "solve_lp", lambda *_args: _solve())
    monkeypatch.setattr(pricing, "arrangement_lines", lambda _family: [])
    orbit = ((Fraction(1, 3), Fraction(1, 4)),)
    calls = 0

    def fake_separation(*_args: Any, **_kwargs: Any) -> Separation:
        nonlocal calls
        calls += 1
        if calls == 1:
            return Separation(Fraction(3, 2), 1, 1, 1, [])
        return Separation(Fraction(3, 2), 1, 1, 1, [(Fraction(3, 2), orbit)])

    def fake_membership(
        family: Any, _point: tuple[Fraction, Fraction]
    ) -> tuple[Fraction, list[int]]:
        depth = Fraction(5, 4) if len(family.placements) == 32 * 8 else Fraction(3, 2)
        return depth, [0]

    monkeypatch.setattr(pricing, "screened_separation", fake_separation)
    monkeypatch.setattr(pricing, "_exact_membership", fake_membership)
    result = pricing.price_state(state, tmp_path / "solved.json", tmp_path / "priced.json")

    assert result["classification"] == "unresolved"
    assert not result["evidence_of_paired_32_row_miss"]
    assert result["witness_checks"][0]["paired32"]["depth"] == "5/4"


def test_line_pair_guard_writes_receipts_without_separation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    solved = tmp_path / "solved.json"
    priced = tmp_path / "priced.json"
    _state(state)
    monkeypatch.setattr(pricing, "solve_lp", lambda *_args: _solve())
    monkeypatch.setattr(pricing, "arrangement_lines", lambda _family: [()] * 6)

    def forbidden(*_args: Any, **_kwargs: Any) -> Separation:
        raise AssertionError("guarded pricing must not materialize candidate pairs")

    monkeypatch.setattr(pricing, "screened_separation", forbidden)
    result = pricing.price_state(state, solved, priced, max_line_pairs=10)

    assert solved.exists()
    assert priced.exists()
    assert result["classification"] == "guard_refused"
    assert not result["evidence_of_paired_32_row_miss"]
    assert result["arms"]["full"]["candidate_line_pairs"] == 15


def test_no_new_geometry_is_unresolved(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    state = tmp_path / "state.json"
    _state(state)
    monkeypatch.setattr(pricing, "solve_lp", lambda *_args: _solve())
    monkeypatch.setattr(pricing, "arrangement_lines", lambda _family: [])
    monkeypatch.setattr(
        pricing,
        "screened_separation",
        lambda *_args, **_kwargs: Separation(Fraction(1), 0, 0, 0, []),
    )
    result = pricing.price_state(state, tmp_path / "solved.json", tmp_path / "priced.json")
    assert result["classification"] == "unresolved"
    assert not result["evidence_of_paired_32_row_miss"]


def test_existing_receipt_refuses_before_solving(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state = tmp_path / "state.json"
    solved = tmp_path / "solved.json"
    _state(state)
    solved.write_text("old\n")

    def forbidden(*_args: Any) -> None:
        raise AssertionError("an existing receipt must refuse before solving")

    monkeypatch.setattr(pricing, "solve_lp", forbidden)
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        pricing.price_state(state, solved, tmp_path / "priced.json")
    assert solved.read_text() == "old\n"
