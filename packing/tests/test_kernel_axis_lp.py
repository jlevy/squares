"""Source-free controls; the scientific factory is forbidden in this suite."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import combinations
from types import SimpleNamespace
from typing import Any

import pytest

from devtools import kernel_axis_lp as kernel


@pytest.fixture(autouse=True)
def forbid_scientific_source(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden() -> object:
        raise AssertionError("scientific source construction is forbidden in controls")

    monkeypatch.setattr(kernel, "scientific_source", forbidden)


def grid() -> tuple[tuple[Fraction, Fraction], ...]:
    return tuple((Fraction(x, 2), Fraction(y, 2)) for x in (1, 3, 5) for y in (1, 3, 5))


def test_exact_nine_clique_objective_certificate() -> None:
    packet = kernel.make_certificate(
        Fraction(3),
        grid(),
        [Fraction(1, 9)] * 9,
        [(i, j, Fraction(2, 9)) for i, j in combinations(range(9), 2)],
    )
    assert packet["bound"] == "9"
    assert packet["alpha"] == ["1/9"] * 9
    assert len(packet["beta"]) == 36
    assert set(packet) == {"format", "source", "side", "poses", "alpha", "beta", "bound"}


def test_unrelated_five_grid_rule_and_closed_walls() -> None:
    poses = kernel.five_grid_poses(Fraction(4))
    assert len(poses) == 25
    assert poses == tuple(sorted(set(poses)))
    kernel.validate_poses(Fraction(4), poses, kernel.SYNTHETIC_SOURCE)
    assert (Fraction(1, 2), Fraction(7, 2)) in poses
    assert (Fraction(2), Fraction(2)) in poses


def test_touching_and_exact_sliver_compatibility() -> None:
    origin = (Fraction(1), Fraction(1))
    assert kernel.compatible(origin, (Fraction(2), Fraction(1)))
    assert kernel.compatible(origin, (Fraction(2), Fraction(2)))
    assert not kernel.compatible(origin, (Fraction(2) - Fraction(1, 2**80), Fraction(1)))


def test_source_admission_refuses_before_solver(monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(**_kwargs: object) -> object:
        raise AssertionError("invalid sources must not enter a solver")

    monkeypatch.setattr(kernel, "linprog", forbidden)
    for side, poses, source in (
        (Fraction(3), grid()[::-1], kernel.SYNTHETIC_SOURCE),
        (Fraction(3), (*grid(), grid()[0]), kernel.SYNTHETIC_SOURCE),
        (Fraction(2), grid(), kernel.SYNTHETIC_SOURCE),
        (Fraction(3), grid(), "foreign"),
        (Fraction(3), grid(), kernel.SCIENTIFIC_SOURCE),
        (Fraction(3), (), kernel.SYNTHETIC_SOURCE),
        (Fraction(1, 2**129), grid(), kernel.SYNTHETIC_SOURCE),
    ):
        with pytest.raises(kernel.GuardError):
            kernel.propose(side, poses, source=source)
    with pytest.raises(kernel.GuardError, match="Fraction"):
        kernel.bounded(1.0)


def test_feature_pair_form_and_joint_quarter_turn() -> None:
    side = Fraction(4)
    left = (Fraction(1), Fraction(3, 2))
    right = (Fraction(5, 2), Fraction(3))
    features = kernel.axis_features(side, left)
    assert features == tuple(
        map(
            Fraction,
            (
                1,
                Fraction(5, 4),
                Fraction(1, 4),
                1,
                0,
                Fraction(3, 4),
                Fraction(1, 2),
                -1,
                Fraction(-1, 2),
                Fraction(-1, 4),
                Fraction(-1, 2),
            ),
        )
    )
    original = kernel.pair_coefficients(features, kernel.axis_features(side, right))
    rotated = kernel.pair_coefficients(
        kernel.axis_features(side, (side - left[1], left[0])),
        kernel.axis_features(side, (side - right[1], right[0])),
    )
    assert original == rotated
    assert original[1] == features[0] * kernel.axis_features(side, right)[1] + features[1]


def test_fixed_psd_directions_and_lp_row_signs() -> None:
    directions = kernel.psd_directions()
    assert len(directions) == 23
    assert len(set(directions)) == 23
    problem = kernel.build_problem(Fraction(3), grid())
    assert len(problem.pairs) == 36
    assert len(problem.rows) == 9 + 36 + 23
    assert problem.rhs == (-Fraction(1),) * 45 + (Fraction(0),) * 23
    for row in problem.rows[:9]:
        assert row[0] == -1
    for row, direction in zip(problem.rows[-23:], directions, strict=True):
        assert row == (Fraction(0), *(-value for value in direction))
    # The A01 test-vector directions must contain both off-diagonal signs.
    assert (Fraction(1), Fraction(-2), Fraction(0), Fraction(0), Fraction(1)) == directions[4][
        :5
    ]
    assert (Fraction(1), Fraction(2), Fraction(0), Fraction(0), Fraction(1)) == directions[5][
        :5
    ]


def test_exact_psd_zero_pivots_and_schur_complements() -> None:
    def matrix(rows: list[list[int]]) -> kernel.Matrix:
        return [[Fraction(value) for value in row] for row in rows]

    assert kernel.is_psd(matrix([[0, 0], [0, 1]]))
    assert kernel.is_psd(matrix([[1, -2], [-2, 4]]))
    assert not kernel.is_psd(matrix([[0, 1], [1, 0]]))
    assert not kernel.is_psd(matrix([[1, 2], [2, 3]]))
    assert not kernel.is_psd(matrix([[-1, 0], [0, 1]]))
    with pytest.raises(kernel.GuardError, match="symmetric"):
        kernel.is_psd(matrix([[1, 0], [1, 1]]))


def test_objective_mutations_are_refused() -> None:
    alpha = [Fraction(1, 9)] * 9
    beta = [(i, j, Fraction(2, 9)) for i, j in combinations(range(9), 2)]
    for bad_alpha, bad_beta in (
        (alpha[:-1], beta),
        ([Fraction(1)] * 9, beta),
        ([Fraction(-1), Fraction(2), *([Fraction(0)] * 7)], beta),
        (alpha, [beta[0], *beta]),
        (alpha, beta[::-1]),
        (alpha, [(0, 0, Fraction(1))]),
        (alpha, [(True, 2, Fraction(1))]),
        (alpha, [(0, 1, Fraction(-1))]),
        (alpha, [(0, 1, Fraction(0))]),
    ):
        with pytest.raises(kernel.GuardError):
            kernel.make_certificate(Fraction(3), grid(), bad_alpha, bad_beta)
    with pytest.raises(kernel.GuardError, match="compatible"):
        kernel.make_certificate(
            Fraction(3),
            ((Fraction(1), Fraction(1)), (Fraction(3, 2), Fraction(1))),
            [Fraction(1, 2)] * 2,
            [(0, 1, Fraction(1))],
        )
    with pytest.raises(kernel.GuardError, match="PSD"):
        kernel.make_certificate(
            Fraction(3), grid()[:2], [Fraction(1, 2)] * 2, [(0, 1, Fraction(2))]
        )


def test_certificate_bit_and_output_caps(monkeypatch: pytest.MonkeyPatch) -> None:
    with pytest.raises(kernel.GuardError, match="bit limit"):
        kernel.make_certificate(
            Fraction(3), grid(), [Fraction(1, 9)] * 9, [(0, 1, Fraction(1, 2**4097))]
        )
    monkeypatch.setattr(kernel, "MAX_PACKET_BYTES", 1)
    with pytest.raises(kernel.GuardError, match="output cap"):
        kernel.make_certificate(Fraction(3), grid(), [Fraction(1, 9)] * 9, [])


def test_intermediate_denominator_growth_is_bounded() -> None:
    with pytest.raises(kernel.GuardError, match="bit limit"):
        kernel.bounded_sum((Fraction(1, 2**4095), Fraction(1, 3)))


def nine_marginals(problem: kernel.Problem) -> list[float]:
    return [-2 / 9] * len(problem.poses) + [-4 / 9] * len(problem.pairs) + [0.0] * 23


def test_one_pass_rationalization_normalizes_and_checks_exactly() -> None:
    problem = kernel.build_problem(Fraction(3), grid())
    packet = kernel.reconstruct(problem, nine_marginals(problem))
    assert packet["bound"] == "9"
    assert packet["alpha"] == ["1/9"] * 9
    assert {item["weight"] for item in packet["beta"]} == {"2/9"}
    for bad in (
        [],
        [0.0] * len(problem.rows),
        [float("nan")] * len(problem.rows),
        [float("inf")] * len(problem.rows),
        [float(2**40)] * len(problem.rows),
        [1.0] * len(problem.rows),
        ["-1/9"] * len(problem.rows),
    ):
        with pytest.raises(kernel.GuardError):
            kernel.reconstruct(problem, bad)


def test_single_solver_call_and_exact_certificate(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict[str, Any]] = []
    problem = kernel.build_problem(Fraction(3), grid())

    def solver(**kwargs: Any) -> SimpleNamespace:
        calls.append(kwargs)
        return SimpleNamespace(
            success=True, status=0, ineqlin=SimpleNamespace(marginals=nine_marginals(problem))
        )

    monkeypatch.setattr(kernel, "linprog", solver)
    outcome = kernel.propose(Fraction(3), grid())
    assert outcome.packet is not None
    assert outcome.packet["bound"] == "9"
    assert len(calls) == 1
    assert calls[0]["c"] == [1.0] + [0.0] * 16
    assert calls[0]["bounds"] == [(None, None)] * 17
    assert calls[0]["options"] == {"time_limit": 30.0, "maxiter": 10_000}
    assert calls[0]["A_ub"] == [[float(value) for value in row] for row in problem.rows]


def test_solver_failures_never_produce_certificates(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = 0

    def solver(**_kwargs: object) -> SimpleNamespace:
        nonlocal calls
        calls += 1
        return SimpleNamespace(success=False, status=1)

    monkeypatch.setattr(kernel, "linprog", solver)
    outcome = kernel.propose(Fraction(3), grid())
    assert outcome.packet is None
    assert outcome.solver_status == 1
    assert calls == 1


def test_bad_solver_receipts_and_exact_failure_are_inconclusive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    problem = kernel.build_problem(Fraction(3), grid())
    bad_psd = [-1 / 2, -1 / 2, *([0.0] * 7), -2.0, *([0.0] * (len(problem.rows) - 10))]
    receipts = (
        SimpleNamespace(success=True, status=None),
        SimpleNamespace(success=True, status=0),
        SimpleNamespace(success=True, status=0, ineqlin=SimpleNamespace(marginals=[])),
        SimpleNamespace(success=True, status=0, ineqlin=SimpleNamespace(marginals=bad_psd)),
    )
    for receipt in receipts:
        calls = []

        def solver(
            *,
            _receipt: SimpleNamespace = receipt,
            _calls: list[dict[str, Any]] = calls,
            **kwargs: Any,
        ) -> SimpleNamespace:
            _calls.append(kwargs)
            return _receipt

        monkeypatch.setattr(kernel, "linprog", solver)
        outcome = kernel.propose(Fraction(3), grid())
        assert outcome.packet is None
        assert "inconclusive" in outcome.reason
        assert len(calls) == 1

    def raising_solver(**_kwargs: Any) -> SimpleNamespace:
        raise RuntimeError("injected solver failure")

    monkeypatch.setattr(kernel, "linprog", raising_solver)
    outcome = kernel.propose(Fraction(3), grid())
    assert outcome.packet is None
    assert "injected solver failure" in outcome.reason


def test_valid_small_bound_is_not_a_family_obstruction() -> None:
    packet = kernel.make_certificate(Fraction(3), grid(), [Fraction(1, 9)] * 9, [])
    assert packet["bound"] == "1"
    assert "obstruction" not in packet
    assert "proved" not in packet


def test_real_solver_on_unrelated_one_pose_control() -> None:
    outcome = kernel.propose(Fraction(2), ((Fraction(1), Fraction(1)),))
    assert outcome.packet is not None
    assert outcome.packet["bound"] == "1"
    assert outcome.packet["alpha"] == ["1"]
    assert outcome.packet["beta"] == []


def test_cli_streams_and_statuses(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    packet = kernel.make_certificate(Fraction(3), grid(), [Fraction(1, 9)] * 9, [])
    monkeypatch.setattr(
        kernel, "propose_scientific", lambda: kernel.Outcome(packet, "exact", 0)
    )
    assert kernel.main(["--target-five-grids"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out) == packet
    assert captured.err == ""
    monkeypatch.setattr(
        kernel, "propose_scientific", lambda: kernel.Outcome(None, "solver limit", 1)
    )
    assert kernel.main(["--target-five-grids"]) == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "inconclusive" in captured.err
    with pytest.raises(SystemExit) as stopped:
        kernel.main([])
    assert stopped.value.code == 2
    capsys.readouterr()

    def refused() -> kernel.Outcome:
        raise kernel.GuardError("injected guard failure")

    monkeypatch.setattr(kernel, "propose_scientific", refused)
    assert kernel.main(["--target-five-grids"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "refused" in captured.err
