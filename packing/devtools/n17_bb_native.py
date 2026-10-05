"""Run the unchanged n=17 branch-and-bound pilot with its native kernel.

The native path replaces pair construction, interval dual bounds, the tiny LP step,
and bound tightening, returning proof events to the pilot's Python certificate recorder.
Taylor mode retains the pilot's Python implementations for its extra columns.
"""

from __future__ import annotations

import argparse
import importlib
import sys
import weakref
from collections.abc import Callable, Sequence
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import gmpy2

from devtools import pilot_n17_subpattern_bb as pilot

_installed: ModuleType | None = None


class _NativeCore(Protocol):
    def pair_term(
        self,
        first_angle: pilot.Iv,
        second_angle: pilot.Iv,
        window: pilot.Iv | None,
        first_box: pilot.Box,
        second_box: pilot.Box,
    ) -> tuple[
        str,
        list[pilot.Iv],
        list[tuple[float, float, float]],
        list[tuple[float, float, float]],
        list[tuple[float, float, float]],
    ]: ...


class _NativeLpSession(Protocol):
    def lp_step(
        self, lp_positive: float
    ) -> tuple[str, float, list[float], list[float], bool]: ...

    def tighten(self) -> list[pilot.Box] | None: ...

    def tighten_recorded(
        self,
    ) -> tuple[
        list[pilot.Box] | None,
        list[tuple[int, float, float, list[float]]],
        str | None,
    ]: ...


_CoreFactory = Callable[
    [
        Callable[[float], tuple[pilot.Iv, pilot.Iv]],
        dict[int, pilot.Iv],
        float,
    ],
    _NativeCore,
]
_LpFactory = Callable[..., _NativeLpSession]
_DualBound = Callable[
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


def _load_native(native_dir: Path) -> ModuleType:
    directory = native_dir.expanduser().resolve(strict=True)
    if not directory.is_dir():
        raise NotADirectoryError(directory)
    entry = str(directory)
    sys.path.insert(0, entry)
    importlib.invalidate_caches()
    try:
        module = importlib.import_module("n17bb_native")
    finally:
        sys.path.remove(entry)
    loaded_from = Path(module.__file__ or "").resolve()
    if loaded_from.parent != directory:
        raise ImportError(
            f"n17bb_native resolved to {loaded_from}, outside requested directory {directory}"
        )
    return module


def _row_args(
    rows: list[pilot.Row], boxes: tuple[pilot.Box, ...]
) -> tuple[
    list[tuple[int, ...]],
    list[tuple[float, ...]],
    list[float],
    list[float],
    list[tuple[pilot.Iv, ...]],
    list[pilot.Iv],
    list[pilot.Box],
]:
    return (
        [row.columns for row in rows],
        [row.values for row in rows],
        [row.rhs for row in rows],
        [row.norm for row in rows],
        [row.exact for row in rows],
        [row.exact_rhs for row in rows],
        list(boxes),
    )


def install(native_dir: str | Path) -> ModuleType:
    """Patch the pilot to use the extension loaded from ``native_dir``.

    Repeated calls return the already installed module.  Loading a second extension in
    one interpreter is refused because CPython caches extension modules by module name.
    """
    global _installed  # noqa: PLW0603
    requested = Path(native_dir).expanduser().resolve(strict=True)
    if _installed is not None:
        loaded_from = Path(_installed.__file__ or "").resolve()
        if loaded_from.parent != requested:
            raise RuntimeError(
                f"n17bb_native is already installed from {loaded_from.parent}, not {requested}"
            )
        return _installed

    native = _load_native(requested)
    for module in (pilot, pilot.cover):
        namespace = vars(module)
        if "Fraction" in namespace:
            namespace["Fraction"] = gmpy2.mpq
        if namespace.get("Q") is Fraction:
            namespace["Q"] = gmpy2.mpq
    core_factory = cast(_CoreFactory, vars(native)["Core"])
    lp_factory = cast(_LpFactory, vars(native)["LpSession"])
    native_dual_bound = cast(_DualBound, vars(native)["dual_bound"])
    core = core_factory(pilot.cos_sin, pilot.HALF_PI_MULTIPLES, 0.0)
    solver_type = pilot.Solver
    original_pair_term = solver_type.pair_term
    original_solve_lp = solver_type.solve_lp
    original_tighten = solver_type.tighten
    sessions: weakref.WeakKeyDictionary[pilot.Solver, _NativeLpSession] = (
        weakref.WeakKeyDictionary()
    )

    def use_python(solver: pilot.Solver) -> bool:
        return solver.settings.taylor or solver.taylor is not None

    def pair_term(
        self: pilot.Solver,
        node: pilot.Node,
        boxes: tuple[pilot.Box, ...],
        index: int,
    ) -> pilot.PairTerm:
        if use_python(self):
            return original_pair_term(self, node, boxes, index)
        if self.settings.merge_gap != 0.0:
            raise ValueError("the native kernel requires --merge-gap 0")
        i, j = self.pattern.pairs[index]
        key = (
            index,
            node.angles[i],
            node.angles[j],
            node.windows[index],
            boxes[i],
            boxes[j],
        )
        cached = self.pair_cache.get(key)
        if cached is not None:
            return cached
        kind, options, cuts, planes, pieces = core.pair_term(
            node.angles[i],
            node.angles[j],
            node.windows[index],
            boxes[i],
            boxes[j],
        )
        term = pilot.PairTerm(kind, options, cuts, planes, pieces, [])
        if len(self.pair_cache) > 400_000:
            self.pair_cache.clear()
        self.pair_cache[key] = term
        return term

    def dual_bound(
        rows: Sequence[pilot.Row],
        multipliers: Sequence[float],
        spans: Sequence[pilot.Iv],
        cost: tuple[int, float] | None,
    ) -> float:
        return native_dual_bound(
            [row.columns for row in rows],
            [row.exact for row in rows],
            [row.exact_rhs for row in rows],
            [row.norm for row in rows],
            list(multipliers),
            list(spans),
            cost,
        )

    def solve_lp(
        self: pilot.Solver, evaluation: pilot.Evaluation, rows: list[pilot.Row]
    ) -> None:
        if use_python(self):
            original_solve_lp(self, evaluation, rows)
            return
        session = lp_factory(*_row_args(rows, evaluation.boxes))
        sessions[self] = session
        status, value, point, duals, closed = session.lp_step(pilot.LP_POSITIVE)
        if status != "optimal":
            evaluation.farkas_failed = True
            return
        evaluation.lp_depth = value
        evaluation.point = point
        if value <= pilot.LP_POSITIVE:
            return
        if closed:
            evaluation.pruned = "lp"
            if self.recorder is not None:
                self.recorder.farkas(rows, duals)
            total = sum(duals) or 1.0
            for row, weight in zip(rows, duals, strict=True):
                if weight > 0.0:
                    evaluation.blame[row.owner] = (
                        evaluation.blame.get(row.owner, 0.0) + weight / total
                    )
        else:
            evaluation.farkas_failed = True

    def tighten(
        self: pilot.Solver, evaluation: pilot.Evaluation, rows: list[pilot.Row]
    ) -> tuple[pilot.Box, ...] | None:
        if use_python(self):
            return original_tighten(self, evaluation, rows)
        session = sessions[self]
        if self.recorder is None:
            bounds = session.tighten()
        else:
            bounds, events, empty_reason = session.tighten_recorded()
            for column, sign, bound, duals in events:
                self.recorder.bound(column, sign, bound, rows, duals)
            if empty_reason is not None:
                self.recorder.emptied(empty_reason)
        if bounds is None:
            return None
        boxes: list[pilot.Box] = []
        for index, bound in enumerate(bounds):
            clipped = pilot.clip_to_box(self.pattern.polygons[index], bound)
            if clipped is None:
                if self.recorder is not None:
                    self.recorder.emptied("cell")
                return None
            boxes.append(clipped)
        return tuple(boxes)

    solver_type.pair_term = pair_term
    solver_type.solve_lp = solve_lp
    solver_type.tighten = tighten
    pilot.dual_bound = dual_bound
    _installed = native
    return native


def main(argv: list[str] | None = None) -> int:
    """Install the extension, then forward all remaining arguments to the pilot."""
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    _ = parser.add_argument("--native-dir", type=Path, required=True)
    _ = parser.add_argument("-h", "--help", action="store_true")
    args, pilot_arguments = parser.parse_known_args(argv)
    if cast(bool, args.help):
        parser.print_help()
        print("\nPilot arguments:")
        return pilot.main(["--help"])
    _ = install(cast(Path, args.native_dir))
    return pilot.main(pilot_arguments)


if __name__ == "__main__":
    raise SystemExit(main())
