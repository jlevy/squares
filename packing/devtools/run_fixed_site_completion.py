"""Retain one fixed-site row-completion attempt, including unsuccessful returns.

This adapter calls `solve_rows` once, then uses the covering bridge's helpers.
Candidates are unverified. No finite-site dual checker is implemented here.
Target execution requires a separately registered hypothesis and funded protocol.
The row deadline starts after input validation and initial matrix reconstruction;
the snapped LP and rationalization tail are outside that cooperative deadline.
No intermediate objective-threshold stop is added to the existing row solver.

An exclusively created output directory owns atomic receipt replacements and live
stdout/stderr streams. Caught failures preserve available rows and timings; vectors
are unavailable if the solver did not return. SIGKILL or a failed final publication
leaves the started receipt. Atomic visibility does not promise power-loss durability.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
import traceback
from collections.abc import Iterator, Sequence
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from dataclasses import asdict
from datetime import UTC, datetime
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import Any

import numpy as np
from strif import atomic_write_text

from devtools.freeze_cutting_primal import ROW_DENOMINATOR
from devtools.run_fractional_colgen import certificate_json
from sqpack.fractional.certificate import Certificate
from sqpack.fractional.colgen import (
    DEFAULT_SCALE,
    LpSolution,
    RoundTiming,
    Rows,
    SiteSet,
    rationalise_sites,
    site_set_from_points,
    solve_lp,
    solve_rows,
)
from sqpack.fractional.cutting import ExactRow, rebuild_rows, rows_from_exact, snap_centre
from sqpack.fractional.generate import direction_net, net_half_tangents


def _json_safe(value: Any) -> Any:
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    if isinstance(value, list | tuple):
        return [_json_safe(item) for item in value]
    return value


def _publish(path: Path, record: dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(_json_safe(record), indent=2, allow_nan=False) + "\n")


@contextmanager
def _streams(output: Path) -> Iterator[None]:
    # Native LP output uses file descriptors; Python redirection alone misses it.
    with (
        (output / "stdout.log").open("x", buffering=1) as stdout,
        (output / "stderr.log").open("x", buffering=1) as stderr,
    ):
        sys.stdout.flush()
        sys.stderr.flush()
        saved_out, saved_err = os.dup(1), os.dup(2)
        try:
            os.dup2(stdout.fileno(), 1)
            os.dup2(stderr.fileno(), 2)
            with redirect_stdout(stdout), redirect_stderr(stderr):
                yield
        finally:
            stdout.flush()
            stderr.flush()
            os.dup2(saved_out, 1)
            os.dup2(saved_err, 2)
            os.close(saved_out)
            os.close(saved_err)


def _inputs(
    state: Path,
    output: Path,
    record: dict[str, Any],
    *,
    side: Fraction,
    core: Fraction,
    half_tangents: tuple[Fraction, ...],
) -> tuple[SiteSet, list[ExactRow]]:
    source = state.read_text()
    atomic_write_text(output / "input.json", source)
    data = json.loads(source)
    record["input"] = {
        key: data.get(key)
        for key in ("outer_side", "square_side", "sites", "rows", "half_tangents")
    }
    if Fraction(data["outer_side"]) != side or Fraction(data["square_side"]) != core:
        raise ValueError("state side/core differs from the declared instance")
    declared_net = [str(value) for value in half_tangents]
    if "half_tangents" in data:
        if [str(Fraction(value)) for value in data["half_tangents"]] != declared_net:
            raise ValueError("state net differs from the declared net")
        record["net_binding"] = "matches source state"
    else:
        record["net_binding"] = "caller-declared; source state does not contain its net"
    points = [(Fraction(x), Fraction(y)) for x, y in data["sites"]]
    if not points or len(set(points)) != len(points):
        raise ValueError("the fixed site list must be nonempty and contain no duplicates")
    if any(not (0 <= x <= side and 0 <= y <= side) for x, y in points):
        raise ValueError("a fixed site lies outside the container")
    sites = site_set_from_points(side, set(points))
    if set(sites.positions()) != set(points):
        raise ValueError("closing the site set under D4 would change the fixed sites")
    directions = direction_net(half_tangents)
    exact_rows: list[ExactRow] = []
    for index, raw_x, raw_y in data["rows"]:
        if type(index) is not int or not 0 <= index < len(directions):
            raise ValueError("a row index is outside the declared net")
        x, y = Fraction(raw_x), Fraction(raw_y)
        direction = directions[index]
        extent = core * (direction.ux + direction.uy) / 2
        if not (extent <= x <= side - extent and extent <= y <= side - extent):
            raise ValueError("a retained placement is outside its exact centre domain")
        exact_rows.append((index, x, y))
    record["site_orbits"] = [[[str(x), str(y)] for x, y in orbit] for orbit in sites.orbits]
    record["initial_rows"] = len(exact_rows)
    return sites, exact_rows


def _solution(solution: LpSolution) -> dict[str, Any]:
    return {
        "primal": solution.weights.tolist(),
        "dual": solution.duals.tolist(),
        "dual_row_count": len(solution.duals),
        "objective": solution.objective,
        "finite": bool(
            np.isfinite(solution.weights).all()
            and np.isfinite(solution.duals).all()
            and math.isfinite(solution.objective)
        ),
        "converged": solution.converged,
        "stopped": solution.stopped,
        "rounds": solution.rounds,
        "least_covered": solution.least_covered,
        "basis": (
            "the first dual_row_count rows of the initial reconstructed rows plus "
            "unsnapped oracle rows; a failed later LP may leave a shorter prefix"
        ),
    }


def _snapshot_rows(
    rows: Rows,
    exact_rows: list[ExactRow],
    *,
    half_tangents: tuple[Fraction, ...],
    side: Fraction,
    core: Fraction,
    timings: list[RoundTiming],
    record: dict[str, Any],
) -> None:
    record["round_timings"] = [asdict(timing) for timing in timings]
    record["oracle_rows"] = [
        [index, cu, cv] for index, (cu, cv) in zip(rows.directions, rows.centres, strict=True)
    ]
    directions = direction_net(half_tangents)
    for position in range(len(exact_rows), len(rows)):
        index = rows.directions[position]
        x, y = snap_centre(
            directions[index], rows.centres[position], side, core, ROW_DENOMINATOR
        )
        exact_rows.append((index, x, y))
    record["exact_rows"] = [[index, str(x), str(y)] for index, x, y in exact_rows]
    record["additional_rows"] = len(exact_rows) - record["initial_rows"]


def _complete(
    state: Path,
    output: Path,
    record: dict[str, Any],
    *,
    n: int,
    side: Fraction,
    core: Fraction,
    half_tangents: tuple[Fraction, ...],
    rows_rounds: int,
    rows_per_direction: int,
    deadline_seconds: float,
    scale: int,
) -> int:
    if n < 1 or not 0 < core < side or rows_rounds < 1 or rows_per_direction < 1 or scale < 1:
        raise ValueError("n, side/core, row limits and rationalization scale must be positive")
    if not math.isfinite(deadline_seconds) or deadline_seconds < 0:
        raise ValueError("the cooperative deadline must be finite and nonnegative")
    if (
        len(half_tangents) < 2
        or half_tangents[0] != 0
        or any(not 0 <= left < right <= 1 for left, right in pairwise(half_tangents))
    ):
        raise ValueError("the declared net must be strictly increasing from zero")
    if half_tangents != net_half_tangents(half_tangents[-1], len(half_tangents) - 1):
        raise ValueError("the certificate serializer requires a uniformly spaced net")
    sites, exact_rows = _inputs(
        state, output, record, side=side, core=core, half_tangents=half_tangents
    )
    record["exact_rows"] = [[index, str(x), str(y)] for index, x, y in exact_rows]
    rows = rows_from_exact(exact_rows, sites, half_tangents, core)
    timings: list[RoundTiming] = []
    deadline = time.perf_counter() + deadline_seconds
    try:
        solution = solve_rows(
            sites,
            core,
            half_tangents,
            rows,
            max_rounds=rows_rounds,
            rows_per_direction=rows_per_direction,
            timings=timings,
            deadline=deadline,
        )
        record["row_solution"] = _solution(solution)
        record["vectors_unavailable_reason"] = None
    finally:
        _snapshot_rows(
            rows,
            exact_rows,
            half_tangents=half_tangents,
            side=side,
            core=core,
            timings=timings,
            record=record,
        )
    record["stop_reason"] = solution.stopped
    record["status"] = "unresolved"
    if not solution.converged:
        return 1
    if not record["row_solution"]["finite"]:
        raise ValueError("a converged solver returned nonfinite vectors or objective")
    rebuild_rows(rows, exact_rows, sites, half_tangents, core)
    solved = solve_lp(sites, rows)
    if solved is None:
        raise ValueError("the snapped-row LP refused")
    weights, duals, objective = solved
    snapped = _solution(LpSolution(weights, duals, objective))
    snapped["basis"] = "all exact rows reconstructed with the bridge coverage slack"
    record["snapped_solution"] = snapped
    if not snapped["finite"] or np.any(weights < 0) or np.any(duals < 0):
        raise ValueError("the snapped-row LP returned invalid numerical values")
    atoms = rationalise_sites(sites, weights, scale=scale)
    if not atoms:
        raise ValueError("all primal atom weights rounded to zero")
    candidate = Certificate(n, side, core, atoms, half_tangents)
    record["rational_mass"] = str(candidate.total_mass)
    if candidate.total_mass >= n:
        record["stop_reason"] = "rational mass is not below n; no exact negative decision"
        return 1
    atomic_write_text(output / "candidate.json", certificate_json(candidate, None))
    record["candidate"] = "candidate.json"
    record["status"] = "candidate-unverified"
    return 0


def run(
    state: Path,
    output: Path,
    *,
    n: int,
    side: Fraction,
    core: Fraction,
    half_tangents: tuple[Fraction, ...],
    rows_rounds: int,
    rows_per_direction: int,
    deadline_seconds: float,
    scale: int = DEFAULT_SCALE,
) -> int:
    """Publish one attempt in a new directory; zero means an unverified candidate."""
    started, cpu_started = time.perf_counter(), time.process_time()
    record: dict[str, Any] = {
        "version": 1,
        "status": "started",
        "stop_reason": "solver has not returned",
        "started_at": datetime.now(UTC).isoformat(),
        "source_state": str(state),
        "parameters": {
            "n": n,
            "outer_side": str(side),
            "square_side": str(core),
            "half_tangents": [str(value) for value in half_tangents],
            "rows_rounds": rows_rounds,
            "rows_per_direction": rows_per_direction,
            "deadline_seconds": deadline_seconds,
            "deadline_scope": (
                "one row-solver call, including its warm solve; "
                "excludes reconstruction and finalization"
            ),
            "scale": scale,
        },
        "row_solution": None,
        "snapped_solution": None,
        "round_timings": [],
        "vectors_unavailable_reason": "the row solver has not returned a solution",
        "exact_verification": "not-run",
        "finite_site_dual_verification": "not-implemented",
        "candidate": None,
        "streams": ["stdout.log", "stderr.log"],
    }
    try:
        output.mkdir()
    except OSError as error:
        print(f"refused before output ownership: {error}", file=sys.stderr)
        return 2
    try:
        _publish(output / "receipt.json", record)
        with _streams(output):
            try:
                code = _complete(
                    state,
                    output,
                    record,
                    n=n,
                    side=side,
                    core=core,
                    half_tangents=half_tangents,
                    rows_rounds=rows_rounds,
                    rows_per_direction=rows_per_direction,
                    deadline_seconds=deadline_seconds,
                    scale=scale,
                )
            except (ValueError, KeyError, TypeError, OSError) as error:
                record.update(status="refused", stop_reason=f"{type(error).__name__}: {error}")
                traceback.print_exc()
                code = 2
            except (Exception, KeyboardInterrupt) as error:  # noqa: BLE001 — retain unexpected tool failures.
                record.update(
                    status="technical-failure", stop_reason=f"{type(error).__name__}: {error}"
                )
                traceback.print_exc()
                code = 2
            record["finished_at"] = datetime.now(UTC).isoformat()
            record["timing"] = {
                "wall_seconds_before_publication": time.perf_counter() - started,
                "cpu_seconds_before_publication": time.process_time() - cpu_started,
                "scope": (
                    "run entry through before terminal publication; "
                    "excludes imports and CLI startup/teardown"
                ),
            }
            record["exit_code"] = code
            print(f"{record['status']}: {record['stop_reason']}")
            _publish(output / "receipt.json", record)
    except OSError as error:
        print(
            f"receipt publication failed; inspect the retained started receipt: {error}",
            file=sys.stderr,
        )
        return 2
    return code


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--side", type=Fraction, required=True)
    parser.add_argument("--core", type=Fraction, required=True)
    parser.add_argument("--angle-limit", type=Fraction, required=True)
    parser.add_argument("--steps", type=int, required=True)
    parser.add_argument("--rows-rounds", type=int, required=True)
    parser.add_argument("--rows-per-direction", type=int, required=True)
    parser.add_argument("--deadline-seconds", type=float, required=True)
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE)
    args = parser.parse_args(argv)
    return run(
        args.state,
        args.output,
        n=args.n,
        side=args.side,
        core=args.core,
        half_tangents=net_half_tangents(args.angle_limit, args.steps),
        rows_rounds=args.rows_rounds,
        rows_per_direction=args.rows_per_direction,
        deadline_seconds=args.deadline_seconds,
        scale=args.scale,
    )


if __name__ == "__main__":
    raise SystemExit(main())
