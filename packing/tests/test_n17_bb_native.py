"""Differential and integration checks for the native n=17 BB kernel."""

from __future__ import annotations

import importlib
import json
import os
import struct
import sys
from collections import Counter
from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import gmpy2
import pytest

from devtools import n17_bb_native as wiring
from devtools import pilot_n17_subpattern_bb as pilot

A_CELLS = "interior-SW,interior-NW,interior-W,interior-S,interior-N,interior-SE"
F7_CELLS = "corner-SW,corner-NW,side-S0,side-N0,side-W0,side-W2,interior-W"

Plane = tuple[float, float, float]
PairResult = tuple[str, list[pilot.Iv], list[Plane], list[Plane], list[Plane]]
RowArgs = tuple[
    list[tuple[int, ...]],
    list[tuple[float, ...]],
    list[float],
    list[float],
    list[tuple[pilot.Iv, ...]],
    list[pilot.Iv],
    list[pilot.Box],
]
LpResult = tuple[str, float, list[float], list[float], bool]


class _TinyLp(Protocol):
    def load(
        self,
        matrix: list[list[float]],
        right: list[float],
        lower: list[float],
        upper: list[float],
        cost: list[float],
    ) -> None: ...

    def set_col_bounds(self, column: int, lower: float, upper: float) -> None: ...

    def set_cost(self, cost: list[float]) -> None: ...

    def solve(self) -> tuple[str, float, list[float], list[float]]: ...


class _NativeCore(Protocol):
    def pair_term(
        self,
        first_angle: pilot.Iv,
        second_angle: pilot.Iv,
        window: pilot.Iv | None,
        first_box: pilot.Box,
        second_box: pilot.Box,
    ) -> PairResult: ...


class _NativeLpSession(Protocol):
    def lp_step(self, lp_positive: float) -> LpResult: ...

    def tighten(self) -> list[pilot.Box] | None: ...


_TinyLpFactory = Callable[[], _TinyLp]
_CoreFactory = Callable[
    [Callable[[float], tuple[pilot.Iv, pilot.Iv]], dict[int, pilot.Iv], float],
    _NativeCore,
]
_LpFactory = Callable[..., _NativeLpSession]
_NativeDual = Callable[
    [
        list[tuple[int, ...]],
        list[tuple[pilot.Iv, ...]],
        list[pilot.Iv],
        list[float],
        list[float],
        list[pilot.Iv],
        tuple[int, float] | None,
    ],
    float,
]


@dataclass(frozen=True)
class _PairCall:
    arguments: tuple[pilot.Iv, pilot.Iv, pilot.Iv | None, pilot.Box, pilot.Box]
    expected: PairResult


@dataclass(frozen=True)
class _DualCall:
    arguments: tuple[
        list[tuple[int, ...]],
        list[tuple[pilot.Iv, ...]],
        list[pilot.Iv],
        list[float],
        list[float],
        list[pilot.Iv],
        tuple[int, float] | None,
    ]
    expected: float


@dataclass(frozen=True)
class _LpCall:
    arguments: RowArgs
    expected: LpResult


@dataclass(frozen=True)
class _TightenCall:
    arguments: RowArgs
    expected: list[pilot.Box] | None


@dataclass(frozen=True)
class _Evidence:
    native: ModuleType
    pairs: list[_PairCall]
    duals: list[_DualCall]
    lp_steps: list[_LpCall]
    tightenings: list[_TightenCall]
    highs_divergence: tuple[LpResult, LpResult]
    fallback_calls: Counter[tuple[str, str]]
    reference_summary: dict[str, object]
    native_summary: dict[str, object]
    f7_summary: dict[str, object]
    certificate: dict[str, object]
    taylor_summary: dict[str, object]


class _Adapter:
    """The four calls made by the pilot's Python LP and tightening loops."""

    def __init__(self, factory: _TinyLpFactory) -> None:
        self.lp = factory()
        self.lower: list[float] = []
        self.upper: list[float] = []
        self.last_outcome: tuple[str, float, list[float], list[float]] | None = None

    def load(
        self,
        matrix: list[list[float]],
        right: list[float],
        lower: list[float],
        upper: list[float],
        cost: list[float],
    ) -> None:
        self.lower = list(lower)
        self.upper = list(upper)
        self.lp.load(matrix, right, lower, upper, cost)

    def changeColBounds(self, column: int, lower: float, upper: float) -> None:  # noqa: N802
        self.lower[column] = lower
        self.upper[column] = upper
        self.lp.set_col_bounds(column, lower, upper)

    def changeColsCost(  # noqa: N802
        self, count: int, columns: Sequence[int], cost: Sequence[float]
    ) -> None:
        del count, columns
        self.lp.set_cost(list(cost))

    def setOptionValue(self, *_arguments: object) -> None:  # noqa: N802
        return

    def solve(self) -> tuple[str, float, list[float], list[float]]:
        self.last_outcome = self.lp.solve()
        return self.last_outcome

    def centre_bounds(self, squares: int) -> list[pilot.Box]:
        return [
            (
                self.lower[2 * square],
                self.upper[2 * square],
                self.lower[2 * square + 1],
                self.upper[2 * square + 1],
            )
            for square in range(squares)
        ]


def _native_or_skip() -> tuple[Path, ModuleType]:
    configured = os.environ.get("N17BB_NATIVE_DIR")
    required = os.environ.get("N17BB_NATIVE_REQUIRED") == "1"
    if configured is None:
        message = "N17BB_NATIVE_DIR is unset; build the n17bb_native extension first"
        if required:
            pytest.fail(message)
        pytest.skip(message)
    directory = Path(configured).expanduser().resolve()
    if not directory.is_dir():
        message = f"native module directory does not exist: {directory}"
        if required:
            pytest.fail(message)
        pytest.skip(message)
    entry = str(directory)
    sys.path.insert(0, entry)
    importlib.invalidate_caches()
    try:
        native = importlib.import_module("n17bb_native")
    except ImportError as error:
        message = f"n17bb_native is not importable from {directory}: {error}"
        if required:
            pytest.fail(message)
        pytest.skip(message)
    finally:
        sys.path.remove(entry)
    loaded_from = Path(native.__file__ or "").resolve()
    if loaded_from.parent != directory:
        pytest.fail(f"n17bb_native loaded from {loaded_from}, not {directory}")
    return directory, native


def _row_args(rows: list[pilot.Row], boxes: tuple[pilot.Box, ...]) -> RowArgs:
    return (
        [row.columns for row in rows],
        [row.values for row in rows],
        [row.rhs for row in rows],
        [row.norm for row in rows],
        [row.exact for row in rows],
        [row.exact_rhs for row in rows],
        list(boxes),
    )


def _pair_result(term: pilot.PairTerm) -> PairResult:
    return term.kind, term.options, term.cuts, term.planes, term.pieces


def _run_receipt(arguments: list[str], output: Path) -> tuple[int, dict[str, object]]:
    status = pilot.main([*arguments, "--output", str(output)])
    return status, cast(dict[str, object], json.loads(output.read_text(encoding="utf-8")))


def _highs_lp_step(arguments: RowArgs) -> LpResult:
    columns, values, rhs, norms, exact, exact_rhs, raw_boxes = arguments
    boxes = tuple(raw_boxes)
    rows = [
        pilot.Row(column, value, right, norm, coefficients, exact_right)
        for column, value, right, norm, coefficients, exact_right in zip(
            columns, values, rhs, norms, exact, exact_rhs, strict=True
        )
    ]
    pattern = pilot.cover_pattern(A_CELLS.split(","))
    solver = pilot.Solver(pattern, pilot.Settings())
    solver.load(rows, boxes)
    outcome = solver.run()
    assert outcome is not None
    value, point, duals = outcome
    closed = (
        value > pilot.LP_POSITIVE
        and pilot.dual_bound(rows, duals, solver.spans(boxes), None) > 0.0
    )
    return "optimal", value, point[: 2 * pattern.k], duals, closed


def _same_bits(expected: object, actual: object) -> bool:
    if isinstance(expected, float):
        return isinstance(actual, float) and struct.pack("!d", expected) == struct.pack(
            "!d", actual
        )
    if isinstance(expected, (list, tuple)):
        if type(actual) is not type(expected):
            return False
        actual_sequence = cast(Sequence[object], actual)
        return len(expected) == len(actual_sequence) and all(
            _same_bits(expected_item, actual_item)
            for expected_item, actual_item in zip(expected, actual_sequence, strict=True)
        )
    return type(actual) is type(expected) and actual == expected


def _reference_run(
    native: ModuleType, directory: Path
) -> tuple[
    list[_PairCall],
    list[_DualCall],
    list[_LpCall],
    list[_TightenCall],
    dict[str, object],
]:
    tiny_factory = cast(_TinyLpFactory, vars(native)["_TinyLP"])
    solver_type = pilot.Solver
    original_init = solver_type.__init__
    original_load = solver_type.load
    original_run = solver_type.run
    original_pair = solver_type.pair_term
    original_solve = solver_type.solve_lp
    original_tighten = solver_type.tighten
    original_dual = pilot.dual_bound
    rational_bindings = [
        (module, vars(module).get("Fraction"), vars(module).get("Q"))
        for module in (pilot, pilot.cover)
    ]
    for module, _, _ in rational_bindings:
        namespace = vars(module)
        if "Fraction" in namespace:
            namespace["Fraction"] = gmpy2.mpq
        if namespace.get("Q") is Fraction:
            namespace["Q"] = gmpy2.mpq
    pairs: list[_PairCall] = []
    duals: list[_DualCall] = []
    lp_steps: list[_LpCall] = []
    tightenings: list[_TightenCall] = []

    def reference_init(
        self: pilot.Solver, pattern: pilot.Pattern, settings: pilot.Settings
    ) -> None:
        original_init(self, pattern, settings)
        self.highs = _Adapter(tiny_factory)  # type: ignore[assignment]

    def reference_load(
        self: pilot.Solver, rows: list[pilot.Row], boxes: tuple[pilot.Box, ...]
    ) -> None:
        columns = self.columns()
        matrix = [[0.0] * columns for _ in rows]
        for row_index, row in enumerate(rows):
            for column, value in zip(row.columns, row.values, strict=True):
                matrix[row_index][column] += value
            matrix[row_index][columns - 1] -= 1.0
        offsets = self.taylor.offsets if self.taylor is not None else ()
        lower = [
            *(bound for box in boxes for bound in (box[0], box[2])),
            *(offset[0] for offset in offsets),
            -1.0,
        ]
        upper = [
            *(bound for box in boxes for bound in (box[1], box[3])),
            *(offset[1] for offset in offsets),
            float("inf"),
        ]
        cost = [0.0] * columns
        cost[-1] = 1.0
        cast(_Adapter, self.highs).load(matrix, [row.rhs for row in rows], lower, upper, cost)

    def reference_run(self: pilot.Solver) -> tuple[float, list[float], list[float]] | None:
        status, value, point, row_duals = cast(_Adapter, self.highs).solve()
        if status != "optimal":
            return None
        return value, point, [max(0.0, dual) for dual in row_duals]

    def record_pair(
        self: pilot.Solver,
        node: pilot.Node,
        boxes: tuple[pilot.Box, ...],
        index: int,
    ) -> pilot.PairTerm:
        term = original_pair(self, node, boxes, index)
        i, j = self.pattern.pairs[index]
        pairs.append(
            _PairCall(
                (node.angles[i], node.angles[j], node.windows[index], boxes[i], boxes[j]),
                _pair_result(term),
            )
        )
        return term

    def record_dual(
        rows: Sequence[pilot.Row],
        multipliers: Sequence[float],
        spans: Sequence[pilot.Iv],
        cost: tuple[int, float] | None,
    ) -> float:
        value = original_dual(rows, multipliers, spans, cost)
        arguments = (
            [row.columns for row in rows],
            [row.exact for row in rows],
            [row.exact_rhs for row in rows],
            [row.norm for row in rows],
            list(multipliers),
            list(spans),
            cost,
        )
        duals.append(_DualCall(arguments, value))
        return value

    def record_solve(
        self: pilot.Solver, evaluation: pilot.Evaluation, rows: list[pilot.Row]
    ) -> None:
        arguments = _row_args(rows, evaluation.boxes)
        original_solve(self, evaluation, rows)
        outcome = cast(_Adapter, self.highs).last_outcome
        assert outcome is not None
        status, value, point, row_duals = outcome
        expected = (
            status,
            value,
            point[: 2 * self.pattern.k],
            [max(0.0, dual) for dual in row_duals],
            evaluation.pruned == "lp",
        )
        lp_steps.append(_LpCall(arguments, expected))

    def record_tighten(
        self: pilot.Solver, evaluation: pilot.Evaluation, rows: list[pilot.Row]
    ) -> tuple[pilot.Box, ...] | None:
        arguments = _row_args(rows, evaluation.boxes)
        result = original_tighten(self, evaluation, rows)
        bounds = cast(_Adapter, self.highs).centre_bounds(self.pattern.k)
        tightenings.append(_TightenCall(arguments, bounds))
        return result

    solver_type.__init__ = reference_init
    solver_type.load = reference_load
    solver_type.run = reference_run
    solver_type.pair_term = record_pair
    solver_type.solve_lp = record_solve
    solver_type.tighten = record_tighten
    pilot.dual_bound = record_dual
    try:
        pattern = pilot.cover_pattern(A_CELLS.split(","))
        differential = pilot.search(
            pattern,
            pilot.Settings(max_seconds=60.0, max_nodes=24),
        )
        assert differential["verdict"] == "unresolved-at-budget"

        solver_type.pair_term = original_pair
        solver_type.solve_lp = original_solve
        solver_type.tighten = original_tighten
        pilot.dual_bound = original_dual
        status, summary = _run_receipt(
            [
                "--cells",
                A_CELLS,
                "--label",
                "A-summary",
                "--max-seconds",
                "60",
                "--max-nodes",
                "500",
            ],
            directory / "reference-summary.json",
        )
        assert status == 0
    finally:
        solver_type.__init__ = original_init
        solver_type.load = original_load
        solver_type.run = original_run
        solver_type.pair_term = original_pair
        solver_type.solve_lp = original_solve
        solver_type.tighten = original_tighten
        pilot.dual_bound = original_dual
        for module, fraction, rational in rational_bindings:
            namespace = vars(module)
            if fraction is not None:
                namespace["Fraction"] = fraction
            if rational is not None:
                namespace["Q"] = rational
    return pairs, duals, lp_steps, tightenings, summary


@pytest.fixture(scope="module")
def evidence(tmp_path_factory: pytest.TempPathFactory) -> Iterator[_Evidence]:
    native_was_loaded = "n17bb_native" in sys.modules
    native_dir, native = _native_or_skip()
    temporary = tmp_path_factory.mktemp("n17-bb-native")
    solver_type = pilot.Solver
    original_pair = solver_type.pair_term
    original_solve = solver_type.solve_lp
    original_tighten = solver_type.tighten
    original_dual = pilot.dual_bound
    original_installed = vars(wiring)["_installed"]
    rational_bindings = [
        (module, vars(module).get("Fraction"), vars(module).get("Q"))
        for module in (pilot, pilot.cover)
    ]
    fallback_calls: Counter[tuple[str, str]] = Counter()

    def fallback_kind(self: pilot.Solver) -> str:
        if self.recorder is not None:
            return "certificate"
        if self.settings.taylor or self.taylor is not None:
            return "taylor"
        return "unexpected"

    def counted_pair(
        self: pilot.Solver,
        node: pilot.Node,
        boxes: tuple[pilot.Box, ...],
        index: int,
    ) -> pilot.PairTerm:
        fallback_calls[(fallback_kind(self), "pair_term")] += 1
        return original_pair(self, node, boxes, index)

    def counted_solve(
        self: pilot.Solver, evaluation: pilot.Evaluation, rows: list[pilot.Row]
    ) -> None:
        fallback_calls[(fallback_kind(self), "solve_lp")] += 1
        original_solve(self, evaluation, rows)

    def counted_tighten(
        self: pilot.Solver, evaluation: pilot.Evaluation, rows: list[pilot.Row]
    ) -> tuple[pilot.Box, ...] | None:
        fallback_calls[(fallback_kind(self), "tighten")] += 1
        return original_tighten(self, evaluation, rows)

    try:
        pairs, duals, lp_steps, tightenings, reference_summary = _reference_run(
            native, temporary
        )
        highs_divergence = next(
            (
                (call.expected, highs)
                for call in lp_steps
                if (highs := _highs_lp_step(call.arguments))[0] == call.expected[0]
                and highs[4] == call.expected[4]
                and not _same_bits(call.expected, highs)
            ),
            None,
        )
        assert highs_divergence is not None
        solver_type.pair_term = counted_pair
        solver_type.solve_lp = counted_solve
        solver_type.tighten = counted_tighten
        _ = wiring.install(native_dir)
        status, native_summary = _run_receipt(
            [
                "--cells",
                A_CELLS,
                "--label",
                "A-summary",
                "--max-seconds",
                "60",
                "--max-nodes",
                "500",
            ],
            temporary / "native-summary.json",
        )
        assert status == 0
        f7_status, f7_summary = _run_receipt(
            [
                "--cells",
                F7_CELLS,
                "--label",
                "F7",
                "--control",
                "--max-seconds",
                "60",
                "--max-nodes",
                "100",
            ],
            temporary / "f7.json",
        )
        assert f7_status == 0

        certificate_dir = temporary / "certificate"
        certificate_status, certificate_summary = _run_receipt(
            [
                "--cells",
                A_CELLS,
                "--label",
                "certificate-native",
                "--max-seconds",
                "60",
                "--max-nodes",
                "2",
                "--save-certificate",
                str(certificate_dir),
            ],
            temporary / "certificate.json",
        )
        assert certificate_status == 0
        manifest = cast(str, certificate_summary["certificate_manifest"])
        certificate = cast(dict[str, object], pilot.load_certificate(certificate_dir, manifest))

        taylor_status, taylor_summary = _run_receipt(
            [
                "--cells",
                A_CELLS,
                "--label",
                "taylor-fallback",
                "--max-seconds",
                "60",
                "--max-nodes",
                "2",
                "--taylor",
            ],
            temporary / "taylor.json",
        )
        assert taylor_status == 0
        yield _Evidence(
            native,
            pairs,
            duals,
            lp_steps,
            tightenings,
            highs_divergence,
            fallback_calls,
            reference_summary,
            native_summary,
            f7_summary,
            certificate,
            taylor_summary,
        )
    finally:
        solver_type.pair_term = original_pair
        solver_type.solve_lp = original_solve
        solver_type.tighten = original_tighten
        pilot.dual_bound = original_dual
        wiring.__dict__["_installed"] = original_installed
        for module, fraction, rational in rational_bindings:
            namespace = vars(module)
            if fraction is not None:
                namespace["Fraction"] = fraction
            if rational is not None:
                namespace["Q"] = rational
        if not native_was_loaded:
            _ = sys.modules.pop("n17bb_native", None)


def _assert_bits(expected: object, actual: object) -> None:
    assert _same_bits(expected, actual)


def test_differential_replay_is_bitwise_for_all_four_call_types(
    evidence: _Evidence,
) -> None:
    core_factory = cast(_CoreFactory, vars(evidence.native)["Core"])
    lp_factory = cast(_LpFactory, vars(evidence.native)["LpSession"])
    native_dual = cast(_NativeDual, vars(evidence.native)["dual_bound"])
    core = core_factory(pilot.cos_sin, pilot.HALF_PI_MULTIPLES, 0.0)
    for call in evidence.pairs:
        _assert_bits(call.expected, core.pair_term(*call.arguments))
    for call in evidence.duals:
        _assert_bits(call.expected, native_dual(*call.arguments))
    for call in evidence.lp_steps:
        session = lp_factory(*call.arguments)
        _assert_bits(call.expected, session.lp_step(pilot.LP_POSITIVE))
    for call in evidence.tightenings:
        session = lp_factory(*call.arguments)
        _ = session.lp_step(pilot.LP_POSITIVE)
        _assert_bits(call.expected, session.tighten())
    assert len(evidence.pairs) > 100
    assert len(evidence.duals) > 100
    assert len(evidence.lp_steps) > 10
    assert len(evidence.tightenings) > 10


def test_a_summary_equals_the_python_tinylp_path(evidence: _Evidence) -> None:
    ignored = {"wall_seconds", "cpu_seconds", "module_sha256"}
    reference = {
        key: value for key, value in evidence.reference_summary.items() if key not in ignored
    }
    native = {
        key: value for key, value in evidence.native_summary.items() if key not in ignored
    }
    assert native == reference


def test_highs_is_a_distinct_numerical_baseline(evidence: _Evidence) -> None:
    """The unmodified pilot agrees on closure but does not produce tiny-LP's bits."""
    tinylp, highs = evidence.highs_divergence
    assert tinylp[0] == highs[0] == "optimal"
    assert tinylp[4] == highs[4]
    assert not _same_bits(tinylp, highs)
    print(f"same closure, distinct LP bits: tinylp={tinylp!r}; highs={highs!r}")


def test_f7_control_is_not_certified(evidence: _Evidence) -> None:
    assert evidence.f7_summary["verdict"] != "certified-infeasible"
    assert "soundness_failure" not in evidence.f7_summary


def test_certificate_is_native_and_taylor_uses_python_fallbacks(
    evidence: _Evidence,
) -> None:
    nodes = cast(list[object], evidence.certificate["nodes"])
    assert nodes
    parameters = cast(dict[str, object], evidence.taylor_summary["parameters"])
    assert parameters["taylor"] is True
    for method in ("pair_term", "solve_lp", "tighten"):
        assert evidence.fallback_calls[("certificate", method)] == 0
        assert evidence.fallback_calls[("taylor", method)] > 0
