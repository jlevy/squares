"""Target-free controls for the deterministic n17 common-core stress."""

# ruff: noqa: SLF001
# pyright: reportPrivateUsage=false

from __future__ import annotations

import time
from fractions import Fraction as Q
from pathlib import Path

import pytest

from devtools import check_n17_core_stress as stress
from devtools.check_n17_contact_chart import ANCHORS, CONTACTS
from devtools.check_n17_endpoint_feasibility import _layout

FORMAL_WALL_BOUND_SECONDS = 30.0
SUBSTITUTED_WALL_BOUND_SECONDS = 120.0


def test_complete_original_order_matrix_and_exact_unrelated_residuals() -> None:
    t, b, half = Q(1, 3), Q(1, 5), Q(1, 2)
    rows, weights, scales, residuals = stress.complete_stress(t, b, half)
    assert len(rows) == len(weights) == 58
    assert all(len(row) == 52 for row in rows.values())
    assert list(rows)[:2] == [("wall", *ANCHORS[0], 0), ("wall", *ANCHORS[0], 1)]
    assert list(rows)[-1] == ("pair", *CONTACTS[-1][:2], 0)
    assert residuals[51] == 0
    side, aux, _ = _layout(t, b, half)
    f2 = aux["d"] * (side - aux["X"] - Q(3, 2)) - aux["e"] * (aux["Y"] - side + Q(3, 2)) - 1
    expected = aux["gamma"] * scales["rho"] * f2 / scales["K"]
    assert residuals[stress._coordinate(12, "angle")] == expected
    assert residuals[stress._coordinate(16, "angle")] == -expected
    assert all(
        residual == 0
        for index, residual in enumerate(residuals)
        if index not in {stress._coordinate(12, "angle"), stress._coordinate(16, "angle")}
    )


def test_prescribed_zero_rows_and_mutated_moment_refusal() -> None:
    rows, weights, _, _ = stress.complete_stress(Q(1, 3), Q(1, 5), Q(1, 2))
    zero_keys = {
        ("wall", 5, "right", 0),
        ("wall", 5, "right", 1),
        ("wall", 6, "bottom", 0),
        ("wall", 6, "bottom", 1),
        ("pair", 9, 11, 0),
        ("pair", 9, 11, 1),
    }
    assert all(weights[key] == 0 for key in zero_keys)
    altered = weights.copy()
    altered["pair", 9, 10, 0] += Q(1, 100)
    assert any(
        sum(altered[key] * row[column] for key, row in rows.items())
        != sum(weights[key] * row[column] for key, row in rows.items())
        for column in range(52)
    )


def test_formal_ring_identity_completes_within_wall_bound() -> None:
    started = time.monotonic()
    proof = stress.ring_residual_proofs(substituted=False)
    elapsed = time.monotonic() - started
    assert elapsed < FORMAL_WALL_BOUND_SECONDS
    summary = proof.summary
    assert summary["passed"] is True
    assert summary["block_residual_failures"] == []
    assert summary["formal_full_matrix_failures"] == []
    assert summary["formal_zero_weight_failures"] == []
    assert summary["load_balance_identities"] == [True, True]
    assert summary["f2_to_h255_pi2_binding"] is True
    assert summary["tied_row_shapes"] == 23
    assert summary["denominators_outside_t_b"] == []


@pytest.mark.slow
def test_substituted_normalized_identity_completes_within_wall_bound() -> None:
    started = time.monotonic()
    proof = stress.ring_residual_proofs(substituted=True)
    assert time.monotonic() - started < SUBSTITUTED_WALL_BOUND_SECONDS
    assert proof.summary["substituted_full_matrix_failures"] == []
    assert proof.summary["substituted_zero_weight_failures"] == []


def test_ring_zero_test_and_derivative_are_exact() -> None:
    field = stress.ExactField()
    t = field.generator("t")
    value = (1 - t * t) / (1 + t * t)
    assert (value * (1 + t * t) / (1 - t * t) - 1).is_zero
    assert not (value - 1).is_zero
    expected = -4 * t / ((1 + t * t) * (1 + t * t))
    assert (value.derivative("t") - expected).is_zero


def test_synthetic_controls_refuse_every_mutation() -> None:
    controls = stress.synthetic_controls()
    sections = controls["sections"]
    assert all(section["passed"] is True for section in sections.values())
    mutations = sections["mutations"]["mutations"]
    assert len(mutations) == 9
    assert all(case["refused"] and case["failing_columns"] for case in mutations.values())
    assert sections["row_derivatives"]["checks"] == 18
    assert all(
        sections["load_derivatives"]["differentiate_after_substitution_refused"].values()
    )


def test_dyadic_intervals_round_outward_on_the_fixed_grid() -> None:
    third = stress.Dyadic.point(Q(1, 3))
    assert third.lo < Q(1, 3) < third.hi
    assert third.hi - third.lo == Q(1, stress.GRID)
    quotient = stress.Dyadic.enclose(Q(-1, 3), Q(2, 3)) / stress.Dyadic.point(Q(3))
    assert quotient.lo <= Q(-1, 9)
    assert Q(2, 9) <= quotient.hi
    with pytest.raises(ValueError, match="includes zero"):
        _ = stress.Dyadic.point(Q(1)) / stress.Dyadic.enclose(Q(-1), Q(1))
    with pytest.raises(ValueError, match="grid"):
        stress.Dyadic(Q(1, 3), Q(1, 3))


def test_sign_disposition_separates_rejection_from_unresolved() -> None:
    positive = stress.Dyadic.enclose(Q(1, 10), Q(1, 5))
    straddle = stress.Dyadic.enclose(Q(-1, 10), Q(1, 5))
    negative = stress.Dyadic.enclose(Q(-1, 5), Q(-1, 10))
    assert stress.classify_signs({"a": positive})[0] == "confirmed_fixed_stress"
    assert stress.classify_signs({"a": straddle})[0] == "unresolved_interval_sign"
    assert stress.classify_signs({"a": straddle, "b": negative})[0] == (
        "rejected_fixed_candidate"
    )


def _refusing_reader(_path: Path) -> bytes:
    raise AssertionError("CLI attempted target input read")


def test_failed_controls_refuse_before_any_target_io(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    paths = [
        tmp_path / name for name in ("root.json", "endpoint.json", "feature.json", "source")
    ]
    for path in paths:
        path.write_bytes(b"{}")

    def failing_controls() -> dict[str, object]:
        raise ValueError("synthetic controls failed: ['mutations']")

    monkeypatch.setattr(stress, "_read_limited", _refusing_reader)
    monkeypatch.setattr(stress, "synthetic_controls", failing_controls)
    assert stress.main([*(str(path) for path in paths[:3]), "--source", str(paths[3])]) == 2
    output = capsys.readouterr().out
    assert '"criterion_passed": false' in output
    assert "synthetic controls failed" in output


def test_unready_flag_still_refuses_before_any_target_io(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(stress, "INSTRUMENT_READY", False)
    monkeypatch.setattr(stress, "_read_limited", _refusing_reader)
    assert stress.main([str(tmp_path / "root.json")]) == 2
    assert '"error": "instrument_unready"' in capsys.readouterr().out


def test_missing_required_input_is_refused(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(stress, "synthetic_controls", lambda: {"passed": True, "seconds": 0})
    monkeypatch.setattr(stress, "_read_limited", _refusing_reader)
    assert stress.main([]) == 2
    assert "all required" in capsys.readouterr().out


def test_tampered_input_is_refused_by_frozen_blob_binding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(stress, "synthetic_controls", lambda: {"passed": True, "seconds": 0})
    paths = [
        tmp_path / name for name in ("root.json", "endpoint.json", "feature.json", "source")
    ]
    for path in paths:
        path.write_bytes(b"{}")
    assert stress.main([*(str(path) for path in paths[:3]), "--source", str(paths[3])]) == 2
    assert "frozen" in capsys.readouterr().out
