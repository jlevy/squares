"""n-parameterised threshold-atom covering producer (think-qqzs G4).

Builds a tiny D4 site grid, solves the point-only restricted covering LP with scipy
HiGHS, and separates violated 2-of-3 threshold atoms against the dual using the in-tree
``FamilyGeometry``. It is not H-216's instrument (H-216 is point-atom). It does not
freeze a scientific candidate, does not run the n=11 181-net or n=6 at 299/100, and
does not import agenda-034 scratch.

Usage, from packing/::

    uv run --frozen --all-extras --group dev python -m devtools.produce_threshold_certificate \\
        --n 2 --outer-side 5/2 --square-side 1 --grid-counts 3 --max-atom-rounds 1 \\
        --max-row-rounds 0 --output-dir DIR
    uv run --frozen --all-extras --group dev python -m devtools.produce_threshold_certificate \\
        --n 2 --check
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any, TextIO

import numpy as np
from scipy import sparse
from scipy.optimize import linprog
from strif import atomic_write_text

from sqpack.fractional.ceiling import CeilingCertificate, Placement
from sqpack.fractional.colgen import Rows, site_set_from_grids, solve_lp, solve_rows
from sqpack.fractional.cutting import ExactRow, coverage_matrix, rows_from_exact, snap_centre
from sqpack.fractional.generate import build_site_grid, direction_net, net_half_tangents
from sqpack.fractional.model import Atom
from sqpack.fractional.threshold import (
    ThresholdAtom,
    least_charged_slabs,
    rectangle_terms,
    sweep_slabs,
    threshold_weight_scale,
)
from sqpack.fractional.threshold_separation import (
    FamilyGeometry,
    TwoOfThreeViolation,
    atom_columns,
    class_summary,
    family_from_dual,
)

DEFAULT_OUTER = Fraction(5, 2)
DEFAULT_SQUARE = Fraction(9977, 10000)
DEFAULT_ANGLE_LIMIT = Fraction(1, 10)
DEFAULT_GRID_COUNTS = (3,)
ROW_DENOMINATOR = 10**6
WEIGHT_DENOMINATOR = 10**9
INITIAL_ROW_ROUNDS = 8
SCIENTIFIC_N11_STEPS = 180
SCIENTIFIC_N6_SIDE = Fraction(299, 100)

_FORBIDDEN_MODULE_MARKERS = ("sepcore", "lp383")


@dataclass(frozen=True, slots=True)
class CoveringSolve:
    """HiGHS covering-LP outcome. Timeout is unresolved, not infeasible."""

    status: str
    weights: np.ndarray | None = None
    duals: np.ndarray | None = None
    objective: float | None = None


@dataclass(frozen=True, slots=True)
class ProducerSettings:
    """Search knobs. Defaults stay tiny so a test run finishes in seconds."""

    n: int
    outer_side: Fraction = DEFAULT_OUTER
    square_side: Fraction = DEFAULT_SQUARE
    grid_counts: tuple[int, ...] = DEFAULT_GRID_COUNTS
    inset: Fraction = Fraction(1, 2)
    angle_limit: Fraction = DEFAULT_ANGLE_LIMIT
    direction_steps: int = 1
    max_atom_rounds: int = 1
    max_row_rounds: int = 0
    atoms_per_round: int = 8
    rows_per_direction: int = 2
    min_violation: float = 0.0
    vertex_cap: int = 0


def _grid_counts(text: str) -> tuple[int, ...]:
    parts = tuple(int(piece) for piece in text.split(",") if piece)
    if not parts or any(count < 2 for count in parts):
        raise argparse.ArgumentTypeError("each grid count must be an integer >= 2")
    return parts


def refuse_scratch_imports(modules: dict[str, object] | None = None) -> None:
    """Refuse a process that has loaded agenda-034 scratch or a ``.py.txt`` module."""

    loaded = sys.modules if modules is None else modules
    for name in loaded:
        lowered = name.lower()
        if any(marker in lowered for marker in _FORBIDDEN_MODULE_MARKERS):
            raise RuntimeError(f"refusing scratch module {name}")
        if lowered.endswith(".txt") or ".py.txt" in lowered:
            raise RuntimeError(f"refusing .py.txt module {name}")


def scientific_refuse(settings: ProducerSettings) -> str | None:
    """This producer is not a scientific freeze of H-216 or the n=11 181-net."""

    if settings.n == 11 and settings.direction_steps >= SCIENTIFIC_N11_STEPS:
        return (
            "refusing the n=11 181-net; this producer is the n-parameterised instrument, "
            "not a scientific freeze"
        )
    if settings.n == 6 and settings.outer_side == SCIENTIFIC_N6_SIDE:
        return "refusing n=6 at 299/100; that target belongs to H-216's point-atom instrument"
    return None


def check_in_tree_apis() -> dict[str, str]:
    """Touch the in-tree APIs the producer needs. Writes nothing."""

    refuse_scratch_imports()
    grid = build_site_grid(DEFAULT_OUTER, 3, Fraction(1, 2))
    atom = ThresholdAtom(
        (
            (Fraction(1), Fraction(1)),
            (Fraction(1, 2), Fraction(1)),
            (Fraction(1), Fraction(1, 2)),
        ),
        2,
        Fraction(1),
    )
    family = CeilingCertificate(
        2,
        Fraction(4),
        Fraction(1),
        (Fraction(0), Fraction(1, 5)),
        (Placement(Fraction(0), Fraction(2), Fraction(2), Fraction(1, 4), Fraction(1)),),
    )
    geometry = FamilyGeometry(family)
    violations = geometry.violated_2of3(outer_side=family.outer_side)
    empty_columns, empty_costs = atom_columns((), [], family.half_tangents, family.square_side)
    return {
        "build_site_grid": str(grid.size),
        "ThresholdAtom.size": str(atom.size),
        "FamilyGeometry.placements": str(geometry.placement_count),
        "violated_2of3": str(len(violations)),
        "atom_columns": (
            f"{int(empty_columns.get_shape()[0])}x{int(empty_columns.get_shape()[1])}"
        ),
        "atom_costs": str(len(empty_costs)),
        "coverage_matrix": coverage_matrix.__name__,
        "family_from_dual": family_from_dual.__name__,
    }


def _snap_exact_rows(
    rows: Rows,
    outer_side: Fraction,
    square_side: Fraction,
    half_tangents: tuple[Fraction, ...],
) -> list[ExactRow]:
    directions = direction_net(half_tangents)
    snapped: list[ExactRow] = []
    for direction_index, centre in zip(rows.directions, rows.centres, strict=True):
        x, y = snap_centre(
            directions[direction_index], centre, outer_side, square_side, ROW_DENOMINATOR
        )
        snapped.append((direction_index, x, y))
    return snapped


def _csr(matrix: object) -> sparse.csr_matrix:
    return sparse.csr_matrix(matrix)


def _matrix_rows(matrix: sparse.csr_matrix) -> int:
    return int(matrix.get_shape()[0])


def _matrix_cols(matrix: sparse.csr_matrix) -> int:
    return int(matrix.get_shape()[1])


def solve_covering(matrix: sparse.csr_matrix, costs: np.ndarray) -> CoveringSolve:
    """Point-or-atom covering LP: minimise cost, every row covered at least once."""

    n_rows = _matrix_rows(matrix)
    if n_rows == 0:
        return CoveringSolve("infeasible")
    result = linprog(
        c=costs,
        A_ub=-matrix,
        b_ub=-np.ones(n_rows),
        bounds=(0.0, None),
        method="highs",
    )
    if int(result.status) == 1:
        return CoveringSolve("unresolved")
    if not result.success or result.ineqlin is None or result.x is None:
        return CoveringSolve("infeasible")
    duals = np.maximum(-np.asarray(result.ineqlin.marginals, dtype=float), 0.0)
    return CoveringSolve(
        "ok",
        np.asarray(result.x, dtype=float),
        duals,
        float(result.fun),
    )


def _receipt(
    *,
    n: int,
    status: str,
    covering_ran: bool,
    objective: float | None,
    reason: str | None = None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "n": n,
        "objective": objective,
        "covering_ran": covering_ran,
        "candidate_created": False,
        "h216_verdict": None,
        "scientific_target": None,
        "status": status,
        "reason": reason,
        "exact_gate_routes": [],
    }
    if extra:
        payload.update(extra)
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(payload, indent=1) + "\n", make_parents=True)


def _log(handle: TextIO, message: str) -> None:
    print(message, file=handle, flush=True)


def _add_violations(
    found: Sequence[TwoOfThreeViolation],
    *,
    outer_side: Fraction,
    keys: set[object],
    cap: int,
) -> list[tuple[tuple[ThresholdAtom, ...], TwoOfThreeViolation]]:
    added: list[tuple[tuple[ThresholdAtom, ...], TwoOfThreeViolation]] = []
    for violation in found:
        atom = violation.atom()
        key = min(image.key for image in atom.images(outer_side))
        if key in keys:
            continue
        keys.add(key)
        added.append((atom.orbit(outer_side), violation))
        if len(added) >= cap:
            break
    return added


def produce(
    settings: ProducerSettings,
    output_dir: Path,
    *,
    log: TextIO = sys.stdout,
) -> dict[str, Any]:
    """Run the point covering LP and 2-of-3 separation. Never a scientific freeze."""

    refuse_scratch_imports()
    blocked = scientific_refuse(settings)
    if blocked is not None:
        receipt = _receipt(
            n=settings.n, status="refused", covering_ran=False, objective=None, reason=blocked
        )
        _write_json(output_dir / "receipt.json", receipt)
        _log(log, f"REFUSED: {blocked}")
        return receipt
    if settings.n < 2:
        receipt = _receipt(
            n=settings.n,
            status="refused",
            covering_ran=False,
            objective=None,
            reason="n must be an integer >= 2",
        )
        _write_json(output_dir / "receipt.json", receipt)
        _log(log, "REFUSED: n must be an integer >= 2")
        return receipt

    started = time.perf_counter()
    half_tangents = net_half_tangents(settings.angle_limit, settings.direction_steps)
    sites = site_set_from_grids(settings.outer_side, settings.grid_counts, settings.inset)
    rows = Rows()
    seed = solve_rows(
        sites,
        settings.square_side,
        half_tangents,
        rows,
        max_rounds=INITIAL_ROW_ROUNDS,
        rows_per_direction=settings.rows_per_direction,
    )
    extra = {
        "outer_side": str(settings.outer_side),
        "square_side": str(settings.square_side),
        "angle_limit": str(settings.angle_limit),
        "direction_steps": settings.direction_steps,
        "grid_counts": list(settings.grid_counts),
        "site_orbits": len(sites.orbits),
        "sites": sites.size,
    }
    if len(rows) == 0:
        reason = seed.stopped or "point-only covering produced no placement rows"
        receipt = _receipt(
            n=settings.n,
            status="refused",
            covering_ran=False,
            objective=None,
            reason=reason,
            extra=extra,
        )
        _write_json(output_dir / "receipt.json", receipt)
        _log(log, f"REFUSED: {reason}")
        return receipt

    exact_rows = _snap_exact_rows(
        rows, settings.outer_side, settings.square_side, half_tangents
    )
    held = rows_from_exact(exact_rows, sites, half_tangents, settings.square_side)
    solved = solve_lp(sites, held)
    if solved is None:
        reason = "point-only covering LP is infeasible on the snapped rows"
        receipt = _receipt(
            n=settings.n,
            status="refused",
            covering_ran=False,
            objective=None,
            reason=reason,
            extra={**extra, "rows": len(exact_rows)},
        )
        _write_json(output_dir / "receipt.json", receipt)
        _log(log, f"REFUSED: {reason}")
        return receipt

    weights, duals, objective = solved
    covering_ran = True
    a_sites = _csr(held.matrix)
    sizes = sites.sizes()
    n_site_orbits = len(sites.orbits)
    _log(
        log,
        f"control: n={settings.n} sites {sites.size}/{n_site_orbits} orbits, "
        f"{len(exact_rows)} rows, objective {objective:.9f}, {seed.stopped}",
    )
    trajectory: list[dict[str, Any]] = [
        {
            "stage": "control",
            "objective": objective,
            "rows": len(exact_rows),
            "atom_orbits": 0,
            "site_support": int((weights > 1e-12).sum()),
            "seconds": time.perf_counter() - started,
        }
    ]
    orbits: list[tuple[ThresholdAtom, ...]] = []
    keys: set[object] = set()
    atom_meta: list[dict[str, Any]] = []
    a_atoms = _csr((len(exact_rows), 0))
    atom_costs = np.zeros(0)
    x = weights
    unresolved_note = "no 2-of-3 violation this generator sees; unresolved, not a refute"

    def checkpoint(note: str) -> None:
        _write_json(
            output_dir / "trajectory.json",
            {"trajectory": trajectory, "note": note, "n": settings.n},
        )
        _write_json(
            output_dir / "atoms.json",
            {
                "n": settings.n,
                "outer_side": str(settings.outer_side),
                "square_side": str(settings.square_side),
                "angle_limit": str(settings.angle_limit),
                "direction_steps": settings.direction_steps,
                "candidate_created": False,
                "h216_verdict": None,
                "scientific_target": None,
                "atoms": [
                    {
                        "points": [[str(px), str(py)] for px, py in orbit[0].points],
                        "threshold": orbit[0].threshold,
                        "orbit_size": len(orbit),
                        **atom_meta[index],
                    }
                    for index, orbit in enumerate(orbits)
                ],
            },
        )

    def resolve(stage: str) -> str | None:
        nonlocal x, duals, objective
        atom_width = _matrix_cols(a_atoms)
        matrix = _csr(sparse.hstack([a_sites, a_atoms])) if atom_width else a_sites
        costs = np.concatenate([sizes, atom_costs]) if atom_width else sizes
        solved_round = solve_covering(matrix, costs)
        if solved_round.status == "unresolved":
            return "unresolved:covering LP hit a HiGHS time or iteration limit"
        if (
            solved_round.status != "ok"
            or solved_round.weights is None
            or solved_round.duals is None
            or solved_round.objective is None
        ):
            return "covering LP is infeasible after adding threshold-atom columns"
        x, duals, objective = (
            solved_round.weights,
            solved_round.duals,
            solved_round.objective,
        )
        atom_mass = float(atom_costs @ x[n_site_orbits:]) if _matrix_cols(a_atoms) else 0.0
        trajectory.append(
            {
                "stage": stage,
                "objective": objective,
                "rows": len(exact_rows),
                "atom_orbits": _matrix_cols(a_atoms),
                "atom_budget": atom_mass,
                "positive_atoms": (
                    int((x[n_site_orbits:] > 1e-12).sum()) if _matrix_cols(a_atoms) else 0
                ),
                "site_support": int((x[:n_site_orbits] > 1e-12).sum()),
                "seconds": time.perf_counter() - started,
            }
        )
        checkpoint(stage)
        _log(
            log,
            f"[{stage}] objective {objective:.9f} atom orbits {_matrix_cols(a_atoms)} "
            f"rows {len(exact_rows)}",
        )
        return None

    checkpoint("control")
    stop_reason: str | None = None
    for round_index in range(settings.max_atom_rounds):
        family = family_from_dual(
            exact_rows,
            duals,
            half_tangents=half_tangents,
            outer_side=settings.outer_side,
            square_side=settings.square_side,
            n=settings.n,
        )
        if family is None:
            unresolved_note = "empty dual; unresolved, not a refute"
            _log(log, unresolved_note)
            break
        _log(
            log,
            f"  dual family: {len(family.placements)} placements, "
            f"total {float(family.total_weight):.6f}",
        )
        geometry = FamilyGeometry(family)
        found = geometry.violated_2of3(
            outer_side=settings.outer_side,
            min_violation=settings.min_violation,
            vertex_cap=settings.vertex_cap,
        )
        added = _add_violations(
            found, outer_side=settings.outer_side, keys=keys, cap=settings.atoms_per_round
        )
        if found:
            _log(
                log,
                f"  top violation {float(found[0].charge) - 1:.6f}; "
                f"classes {class_summary(found)}",
            )
        if not added:
            _log(log, unresolved_note)
            trajectory.append(
                {
                    "stage": f"atoms-{round_index}-none",
                    "objective": objective,
                    "rows": len(exact_rows),
                    "atom_orbits": _matrix_cols(a_atoms),
                    "seconds": time.perf_counter() - started,
                }
            )
            checkpoint("no-new-atom")
            break
        new_orbits = tuple(orbit for orbit, _ in added)
        columns, costs = atom_columns(
            new_orbits, exact_rows, half_tangents, settings.square_side
        )
        for orbit, violation in added:
            orbits.append(orbit)
            atom_meta.append(
                {
                    "charge_at_separation": float(violation.charge),
                    "classes": list(violation.classes),
                    "angles": [round(angle, 2) for angle in violation.angles],
                }
            )
        a_atoms = _csr(sparse.hstack([a_atoms, columns]))
        atom_costs = np.concatenate([atom_costs, costs])
        _log(log, f"  added {len(added)} atom orbits")
        stop_reason = resolve(f"atoms-{round_index}")
        if stop_reason is not None:
            break

    if stop_reason is None and settings.max_row_rounds > 0 and _matrix_cols(a_atoms):
        directions = direction_net(half_tangents)
        for round_index in range(settings.max_row_rounds):
            site_weights, atom_weights = x[:n_site_orbits], x[n_site_orbits:]
            point_atoms = tuple(
                atom
                for atom in (
                    Atom(
                        f"{orbit_index}:{member_index}",
                        px,
                        py,
                        Fraction(math.ceil(weight * WEIGHT_DENOMINATOR), WEIGHT_DENOMINATOR),
                    )
                    for orbit_index, weight in enumerate(site_weights)
                    if weight > 1e-12
                    for member_index, (px, py) in enumerate(sites.orbits[orbit_index])
                )
                if atom.weight > 0
            )
            threshold_atoms = tuple(
                atom
                for atom in (
                    ThresholdAtom(
                        image.points,
                        image.threshold,
                        Fraction(math.ceil(weight * WEIGHT_DENOMINATOR), WEIGHT_DENOMINATOR),
                    )
                    for orbit_index, weight in enumerate(atom_weights)
                    if weight > 1e-12
                    for image in orbits[orbit_index]
                )
                if atom.weight > 0
            )
            scale = threshold_weight_scale(point_atoms, threshold_atoms)
            new_rows: list[ExactRow] = []
            least: Fraction | None = None
            for direction_index, direction in enumerate(directions):
                terms = rectangle_terms(
                    point_atoms,
                    threshold_atoms,
                    direction,
                    settings.outer_side,
                    settings.square_side,
                    scale=scale,
                )
                scores, _ = sweep_slabs(terms)
                charge = Fraction(int(scores.min()), scale)
                if least is None or charge < least:
                    least = charge
                for _, (u, v) in least_charged_slabs(
                    terms,
                    direction,
                    settings.outer_side,
                    settings.square_side,
                    keep=settings.rows_per_direction,
                    below=Fraction(1) - Fraction(1, 10**6),
                ):
                    new_rows.append(
                        (
                            direction_index,
                            direction.ux * u - direction.uy * v,
                            direction.uy * u + direction.ux * v,
                        )
                    )
            trajectory.append(
                {
                    "stage": f"sweep-{round_index}",
                    "least_charge": None if least is None else float(least),
                    "violated_cells": len(new_rows),
                    "seconds": time.perf_counter() - started,
                }
            )
            if not new_rows:
                checkpoint("rows-complete")
                break
            exact_rows.extend(new_rows)
            a_sites = _csr(
                sparse.vstack(
                    [
                        a_sites,
                        _csr(
                            coverage_matrix(
                                new_rows, sites, half_tangents, settings.square_side
                            )
                        ),
                    ]
                )
            )
            extra_columns, _ = atom_columns(
                orbits, new_rows, half_tangents, settings.square_side
            )
            a_atoms = _csr(sparse.vstack([a_atoms, extra_columns]))
            stop_reason = resolve(f"rows-{round_index}")
            if stop_reason is not None:
                break

    if stop_reason is not None:
        unresolved = stop_reason.startswith("unresolved:")
        reason = stop_reason.removeprefix("unresolved:") if unresolved else stop_reason
        receipt = _receipt(
            n=settings.n,
            status="unresolved" if unresolved else "refused",
            covering_ran=covering_ran,
            objective=objective,
            reason=reason,
            extra={**extra, "rows": len(exact_rows), "atom_orbits": len(orbits)},
        )
        _write_json(output_dir / "receipt.json", receipt)
        _log(log, f"{'UNRESOLVED' if unresolved else 'REFUSED'}: {reason}")
        return receipt

    checkpoint("final")
    receipt = _receipt(
        n=settings.n,
        status="unresolved",
        covering_ran=covering_ran,
        objective=objective,
        reason=unresolved_note if not orbits else None,
        extra={
            **extra,
            "rows": len(exact_rows),
            "atom_orbits": len(orbits),
            "seconds": time.perf_counter() - started,
            "seed_stopped": seed.stopped,
        },
    )
    _write_json(output_dir / "receipt.json", receipt)
    _log(
        log,
        f"unresolved n={settings.n} objective {objective:.9f} "
        f"rows {len(exact_rows)} atom orbits {len(orbits)}; not a refute",
    )
    return receipt


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=(__doc__ or "").split("\n\n")[0],
        allow_abbrev=False,
    )
    command.add_argument("--n", type=int, required=True, help="packing n, integer >= 2")
    command.add_argument("--outer-side", type=Fraction, default=DEFAULT_OUTER)
    command.add_argument("--square-side", type=Fraction, default=DEFAULT_SQUARE)
    command.add_argument("--grid-counts", type=_grid_counts, default=DEFAULT_GRID_COUNTS)
    command.add_argument("--inset", type=Fraction, default=Fraction(1, 2))
    command.add_argument("--angle-limit", type=Fraction, default=DEFAULT_ANGLE_LIMIT)
    command.add_argument("--direction-steps", type=int, default=1)
    command.add_argument("--max-atom-rounds", type=int, default=1)
    command.add_argument("--max-row-rounds", type=int, default=0)
    command.add_argument("--atoms-per-round", type=int, default=8)
    command.add_argument("--rows-per-direction", type=int, default=2)
    command.add_argument("--output-dir", type=Path, default=None)
    command.add_argument(
        "--check",
        action="store_true",
        help="validate flags and in-tree APIs; write nothing",
    )
    return command


def _settings_from(args: argparse.Namespace) -> ProducerSettings | str:
    if args.n < 2:
        return "n must be an integer >= 2"
    if args.direction_steps < 1:
        return "direction-steps must be >= 1"
    if args.max_atom_rounds < 0 or args.max_row_rounds < 0:
        return "round counts must be >= 0"
    return ProducerSettings(
        n=args.n,
        outer_side=args.outer_side,
        square_side=args.square_side,
        grid_counts=tuple(args.grid_counts),
        inset=args.inset,
        angle_limit=args.angle_limit,
        direction_steps=args.direction_steps,
        max_atom_rounds=args.max_atom_rounds,
        max_row_rounds=args.max_row_rounds,
        atoms_per_round=args.atoms_per_round,
        rows_per_direction=args.rows_per_direction,
    )


def main(argv: list[str] | None = None) -> int:
    refuse_scratch_imports()
    args = parser().parse_args(argv)
    settings = _settings_from(args)
    if isinstance(settings, str):
        print(f"REFUSED: {settings}", file=sys.stderr)
        return 2
    blocked = scientific_refuse(settings)
    if args.check:
        if blocked is not None:
            print(f"REFUSED: {blocked}", file=sys.stderr)
            return 2
        apis = check_in_tree_apis()
        print(
            json.dumps(
                {
                    "status": "checked",
                    "n": settings.n,
                    "apis": apis,
                    "candidate_created": False,
                }
            )
        )
        return 0
    if args.output_dir is None:
        print("REFUSED: --output-dir is required unless --check", file=sys.stderr)
        return 2
    receipt = produce(settings, args.output_dir)
    if receipt["status"] == "refused":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
