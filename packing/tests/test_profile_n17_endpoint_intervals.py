"""Target-free controls for the selected arithmetic experiment."""

import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any

import pytest

from devtools import profile_n17_endpoint_intervals as probe
from devtools.check_n17_core_stress import Dyadic
from devtools.check_n17_endpoint_feasibility import Box
from sqpack.hull_kernel.geometry import Budget, IncompleteError


@pytest.mark.parametrize(("lo", "hi"), [(Q(1, 3), Q(2, 3)), (Q(-4, 3), Q(-2, 3))])
def test_existing_operations_enclose_independent_exact_values(lo: Q, hi: Q) -> None:
    value = Dyadic.enclose(lo, hi)
    result = (value + Q(2, 7)) * Q(-3, 5) / Q(11, 13)
    expected = Box((hi + Q(2, 7)) * Q(-3, 5) / Q(11, 13), (lo + Q(2, 7)) * Q(-3, 5) / Q(11, 13))
    probe.check_enclosure(expected, result)
    assert type(result) is Dyadic
    assert all((endpoint * 2**256).denominator == 1 for endpoint in (result.lo, result.hi))


def test_deliberately_narrow_interval_refuses() -> None:
    with pytest.raises(ValueError, match="narrowed"):
        probe.check_enclosure(Box(Q(1), Q(3)), Box(Q(2), Q(3)))


def test_zero_denominator_refuses_and_straddle_stays_unresolved() -> None:
    straddle = Dyadic.enclose(Q(-1, 3), Q(2, 3))
    assert probe.disposition(straddle) == "unresolved"
    with pytest.raises(ValueError, match="includes zero"):
        _ = Dyadic.point(Q(1)) / straddle
    with pytest.raises(ValueError, match="sign was lost"):
        probe.check_enclosure(Box(Q(1, 3), Q(2, 3)), straddle)


def test_output_observation_does_not_assume_intermediate_types() -> None:
    stats = probe.interval_stats(
        {"mixed": (Dyadic.point(Q(1)), Box.point(Q(1, 3))), "scalar": 3}
    )
    assert stats["types"] == ["Box", "Dyadic"]
    assert stats["off_grid_endpoints"] == 2
    assert stats["interval_count"] == 2


@pytest.mark.parametrize(
    ("exact", "dyadic", "expected"), [(1.0, 0.8, True), (0.1, 0.01, False), (1.0, 0.81, False)]
)
def test_preregistered_dual_performance_threshold(
    exact: float, dyadic: float, *, expected: bool
) -> None:
    assert probe.pair_gate(exact, dyadic) is expected


def test_ab_then_ba_uses_fresh_passes_and_requires_both_gates(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls = []
    times = iter((1.0, 0.5, 0.9, 1.0))

    def fake_pass(backend: str, *_: Any) -> tuple[dict[str, Any], tuple[Box, ...]]:
        calls.append(backend)
        constructor = Box if backend == "exact" else Dyadic
        values = tuple(constructor.point(Q(1)) for _ in probe.FIXTURE)
        return {"seconds": {"fresh_fixture_total": next(times)}, "rows": [1]}, values

    monkeypatch.setattr(probe, "run_pass", fake_pass)
    monkeypatch.setattr(probe, "check_budget", lambda *_, **__: None)
    packet = probe.profile((Q(1), Q(2)), (Q(1, 100), Q(1, 100)), Budget(1e20, 0))
    assert calls == ["exact", "dyadic", "dyadic", "exact"]
    assert packet["pair_performance_gates"] == [True, False]
    assert packet["selected_fixture_adoption_interest"] is False


def test_postquery_guard_cannot_return_success(monkeypatch: pytest.MonkeyPatch) -> None:
    checks = iter((None, IncompleteError("postquery cap")))

    def guard(*_: Any, **__: Any) -> None:
        error = next(checks)
        if error is not None:
            raise error

    monkeypatch.setattr(probe, "check_budget", guard)
    with pytest.raises(IncompleteError, match="postquery"):
        probe.timed(Budget(1e20, 0), lambda: "completed")


def test_unknown_backend_refuses() -> None:
    with pytest.raises(ValueError, match="unknown backend"):
        probe.build_layout("float", (Q(1), Q(2)), (Q(1, 10), Q(1, 10)))


def test_real_mixed_operator_layout_observes_types_and_encloses(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(probe, "check_budget", lambda *_, **__: None)
    midpoint = Q(365, 1000), Q(337, 1000)
    radii = Q(1, 2**60), Q(1, 2**60)
    exact, exact_values = probe.run_pass("exact", midpoint, radii, Budget(1e20, 0))
    dyadic, dyadic_values = probe.run_pass("dyadic", midpoint, radii, Budget(1e20, 0))
    assert exact["returned_objects"]["types"] == ["Box"]
    assert dyadic["returned_objects"]["types"] == ["Dyadic"]
    assert dyadic["returned_objects"]["off_grid_endpoints"] == 0
    for reference, candidate in zip(exact_values, dyadic_values, strict=True):
        probe.check_enclosure(reference, candidate)


def test_later_refusal_preserves_completed_passes_without_acceptance(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    root = {"box": {"midpoint": ["1", "2"]}, "inclusion_bounds": ["1/100", "1/100"]}
    monkeypatch.setattr(probe, "require_retained_path", lambda *_: None)
    monkeypatch.setattr(probe, "_read_limited", lambda *_: json.dumps(root).encode())
    monkeypatch.setattr(probe, "check_root", lambda *_: {"verification_passed": True})
    monkeypatch.setattr(probe, "check_budget", lambda *_, **__: None)

    def stop_after_ab(*args: Any) -> dict[str, Any]:
        args[3].extend([{"backend": "exact"}, {"backend": "dyadic"}])
        raise IncompleteError("BA resource cap")

    monkeypatch.setattr(probe, "profile", stop_after_ab)
    output = tmp_path / "partial.json"
    assert probe.main(["--out", str(output)]) == 2
    packet = json.loads(output.read_text())
    assert packet["completed_passes"] == [{"backend": "exact"}, {"backend": "dyadic"}]
    assert packet["partial_evidence_accepted"] is False
    assert packet["selected_fixture_adoption_interest"] is False


def test_existing_output_is_preserved_before_any_input_read(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    output = tmp_path / "retained.json"
    output.write_bytes(b"original evidence")

    def refuse_input(*_: Any) -> bytes:
        raise AssertionError("input read before output preservation check")

    monkeypatch.setattr(probe, "_read_limited", refuse_input)
    with pytest.raises(SystemExit) as error:
        probe.main(["--out", str(output)])
    assert error.value.code == 2
    assert output.read_bytes() == b"original evidence"


def test_grid_rounding_can_lose_a_positive_sign_without_proving_negative() -> None:
    tiny = Q(1, 2**300)
    rounded = Dyadic.point(tiny)
    assert probe.disposition(rounded) == "unresolved"
    with pytest.raises(ValueError, match="sign was lost"):
        probe.check_enclosure(Box.point(tiny), rounded)


def test_completed_ab_is_checkpointed_before_a_later_stop(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    calls = []

    def fake_pass(backend: str, *_: Any) -> tuple[dict[str, Any], tuple[Box, ...]]:
        calls.append(backend)
        if len(calls) == 3:
            raise IncompleteError("later stop")
        return {"backend": backend}, tuple(Box.point(Q(1)) for _ in probe.FIXTURE)

    monkeypatch.setattr(probe, "run_pass", fake_pass)
    output = tmp_path / "checkpoint.json"
    with pytest.raises(IncompleteError, match="later stop"):
        probe.profile((Q(1), Q(2)), (Q(1, 100), Q(1, 100)), Budget(1e20, 0), checkpoint=output)
    packet = json.loads(output.read_text())
    assert packet["completed_passes"] == [{"backend": "exact"}, {"backend": "dyadic"}]
    assert packet["partial_evidence_accepted"] is False
