"""Replay native certificates against Python proof loops using the same tinylp LPs."""

from __future__ import annotations

import argparse
import json
from collections.abc import Iterator, Sequence
from contextlib import ExitStack, contextmanager
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import cast
from unittest.mock import patch

import gmpy2

from devtools import n17_bb_native as wiring
from devtools import pilot_n17_subpattern_bb as pilot
from devtools import verify_n17_bb_certificate as verifier

A_CELLS = "interior-SW,interior-NW,interior-W,interior-S,interior-N,interior-SE"


@contextmanager
def python_tinylp(native: ModuleType) -> Iterator[None]:
    """Keep Python proof loops and replace only their numerical LP backend."""
    if vars(wiring)["_installed"] is not None:
        raise RuntimeError("Python reference requires the pilot before native installation")
    original_init = pilot.Solver.__init__

    class Adapter:
        def __init__(self) -> None:
            self.lp = native._TinyLP()  # noqa: SLF001

        def changeColBounds(self, column: int, lower: float, upper: float) -> None:  # noqa: N802
            self.lp.set_col_bounds(column, lower, upper)

        def changeColsCost(  # noqa: N802
            self, count: int, columns: Sequence[int], cost: Sequence[float]
        ) -> None:
            del count, columns
            self.lp.set_cost(list(cost))

        def setOptionValue(self, *_arguments: object) -> None:  # noqa: N802
            return

    def initialize(
        self: pilot.Solver, pattern: pilot.Pattern, settings: pilot.Settings
    ) -> None:
        original_init(self, pattern, settings)
        self.highs = Adapter()  # type: ignore[assignment]

    def load(self: pilot.Solver, rows: list[pilot.Row], boxes: tuple[pilot.Box, ...]) -> None:
        columns = self.columns()
        matrix = [[0.0] * columns for _ in rows]
        for index, row in enumerate(rows):
            for column, value in zip(row.columns, row.values, strict=True):
                matrix[index][column] += value
            matrix[index][-1] -= 1.0
        lower = [*(bound for box in boxes for bound in (box[0], box[2])), -1.0]
        upper = [*(bound for box in boxes for bound in (box[1], box[3])), float("inf")]
        cost = [0.0] * columns
        cost[-1] = 1.0
        cast(Adapter, self.highs).lp.load(matrix, [row.rhs for row in rows], lower, upper, cost)

    def run(self: pilot.Solver) -> tuple[float, list[float], list[float]] | None:
        status, value, point, duals = cast(Adapter, self.highs).lp.solve()
        if status != "optimal":
            return None
        return value, point, [max(0.0, dual) for dual in duals]

    def forbidden_backend(*_arguments: object) -> None:
        raise AssertionError("reference proof must use Python loops and only tinylp numerics")

    with ExitStack() as patches:
        for name in ("Core", "LpSession", "dual_bound"):
            patches.enter_context(patch.object(native, name, forbidden_backend))
        highs_type = vars(pilot.highs)["_Highs"]
        patches.enter_context(patch.object(highs_type, "run", forbidden_backend))
        patches.enter_context(patch.object(pilot.Solver, "__init__", initialize))
        patches.enter_context(patch.object(pilot.Solver, "load", load))
        patches.enter_context(patch.object(pilot.Solver, "run", run))
        for module in (pilot, pilot.cover):
            namespace = vars(module)
            if "Fraction" in namespace:
                patches.enter_context(patch.dict(namespace, {"Fraction": gmpy2.mpq}))
            if namespace.get("Q") is Fraction:
                patches.enter_context(patch.dict(namespace, {"Q": gmpy2.mpq}))
        yield


def certificate_files(directory: Path) -> set[Path]:
    """List all certificate artifacts, including their descriptive README."""
    return {path.relative_to(directory) for path in directory.rglob("*") if path.is_file()}


def compare_certificates(expected: Path, observed: Path) -> tuple[int, int]:
    """Compare every byte with bounded memory and return file and byte counts."""
    names = certificate_files(expected)
    if names != certificate_files(observed):
        raise RuntimeError("certificate file sets differ")
    total = 0
    for name in sorted(names):
        with (expected / name).open("rb") as first, (observed / name).open("rb") as second:
            while True:
                content = first.read(1024 * 1024)
                if content != second.read(1024 * 1024):
                    raise RuntimeError(f"certificate bytes differ: {name}")
                total += len(content)
                if not content:
                    break
    return len(names), total


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--native-dir", type=Path, required=True)
    _ = parser.add_argument("--output-dir", type=Path, required=True)
    arguments = parser.parse_args(argv)
    directory = cast(Path, arguments.output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    native_dir = cast(Path, arguments.native_dir)
    # Import without installing the native pair/dual/tighten implementations.
    native = wiring._load_native(native_dir)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    for name in ("python", "native"):
        target = directory / name
        if target.exists():
            parser.error(f"refusing existing certificate directory: {target}")
    settings = pilot.Settings(max_seconds=3600.0, max_nodes=None)
    with python_tinylp(native):
        pattern = pilot.cover_pattern(A_CELLS.split(","))
        reference = pilot.search(
            pattern, settings, certificate=directory / "python", progress=True
        )
    (directory / "python-search.json").write_text(json.dumps(reference, indent=2) + "\n")
    _ = wiring.install(native_dir)
    actual = pilot.search(pattern, settings, certificate=directory / "native", progress=True)
    (directory / "native-search.json").write_text(json.dumps(actual, indent=2) + "\n")
    if (
        reference["verdict"] != "certified-infeasible"
        or actual["verdict"] != "certified-infeasible"
    ):
        raise RuntimeError("A did not close completely")
    files, size = compare_certificates(directory / "python", directory / "native")
    comparison = {
        "equal": True,
        "files": files,
        "bytes_per_certificate": size,
        "manifest_sha256": actual["certificate_manifest"],
    }
    (directory / "comparison.json").write_text(json.dumps(comparison, indent=2) + "\n")
    print(json.dumps(comparison), flush=True)
    for name in ("python", "native"):
        status = verifier.main(
            [str(directory / name), "--output", str(directory / f"{name}-verification.json")]
        )
        if status:
            return status
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
