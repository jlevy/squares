#!/usr/bin/env python3
"""Source-bound exact replay of one endpoint owner-footprint covering receipt.

The wrapper never solves an LP or reconstructs lost binary64 weights.  It accepts the
rationalized atoms retained by a completed numerical receipt, rebuilds the declared
support and footprint geometry, and evaluates exact event cells on either the retained
nine directions or the full 361-direction net.  Even a full-net result has no
continuum-angle transfer and is not a packing certificate.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools.owner_footprints import CORE_SIDE, OUTER_SIDE, Point
from devtools.run_owner_footprint_cover import (
    Arm,
    build_four_owner_arms,
    build_receipt,
    exact_minimum_covered_mass_on_pieces,
)
from sqpack.fractional.model import Atom, Direction, require_nonnegative_atom_weights


@dataclass(frozen=True, slots=True)
class BoundSource:
    """A clean tracked numerical receipt and its reconstructed endpoint arm."""

    path: Path
    git_commit: str
    git_blob: str
    receipt: dict[str, Any]
    arm: Arm
    retained_directions: tuple[Direction, ...]
    atoms: tuple[Atom, ...]
    total_mass: Fraction
    owner_count: int


def _git(*args: str, root: Path) -> str:
    result = subprocess.run(
        ("git", *args),
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ValueError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def bind_clean_tracked_source(path: Path, expected_blob: str) -> tuple[Path, str, str]:
    """Require the exact working bytes to be clean, tracked, and blob-bound."""

    root = Path(_git("rev-parse", "--show-toplevel", root=Path.cwd()))
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError as error:
        raise ValueError("source receipt is outside the Git repository") from error
    relative_text = relative.as_posix()
    _git("ls-files", "--error-unmatch", "--", relative_text, root=root)
    if _git("status", "--porcelain", "--", relative_text, root=root):
        raise ValueError("source receipt has uncommitted or untracked changes")
    blob = _git("hash-object", "--", relative_text, root=root)
    if blob != expected_blob:
        raise ValueError(f"source blob {blob} does not match expected {expected_blob}")
    commit = _git("rev-parse", "HEAD", root=root)
    return root, commit, blob


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be an object")
    return value


def _sequence(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise TypeError(f"{label} must be an array")
    return value


def _fraction(value: object, label: str) -> Fraction:
    if not isinstance(value, (str, int)):
        raise TypeError(f"{label} must be an exact rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise ValueError(f"{label} is not an exact rational") from error


def _source_configuration(
    receipt: dict[str, Any],
) -> tuple[dict[str, Any], tuple[Arm, ...], tuple[Direction, ...], int]:
    if receipt.get("schema") != "owner-footprint-cover/v1":
        raise ValueError("source receipt has the wrong schema")
    if receipt.get("status") != "complete":
        raise ValueError("source receipt is not a completed four-arm comparison")
    settings = _mapping(receipt.get("settings"), "settings")
    if _fraction(settings.get("outer_side"), "outer_side") != OUTER_SIDE:
        raise ValueError("source receipt changes the outer side")
    if _fraction(settings.get("square_side"), "square_side") != CORE_SIDE:
        raise ValueError("source receipt changes the core side")
    owner_count = settings.get("owner_count")
    if owner_count not in (1, 4):
        raise ValueError("source owner_count must be 1 or 4")
    class_record = _mapping(receipt.get("class"), "class")
    class_id = class_record.get("id")
    if not isinstance(class_id, str):
        raise TypeError("source class id is missing")
    folded = tuple(
        int(value)
        for value in _sequence(settings.get("folded_source_indices"), "folded indices")
    )
    grid_count = settings.get("grid_count")
    if not isinstance(grid_count, int):
        raise TypeError("grid_count must be an integer")
    inset = _fraction(settings.get("inset"), "inset")
    expected, arms, directions = build_receipt(
        class_id=class_id,
        grid_count=grid_count,
        inset=inset,
        folded_indices=folded,
        owner_count=owner_count,
    )
    for key in ("class", "direction_provenance", "available_support"):
        if receipt.get(key) != expected.get(key):
            raise ValueError(f"source {key} does not match reconstructed geometry")
    expected_settings = _mapping(expected.get("settings"), "reconstructed settings")
    for key, value in expected_settings.items():
        if settings.get(key) != value:
            raise ValueError(f"source settings.{key} does not match reconstruction")
    execution = _mapping(settings.get("execution"), "settings.execution")
    if any(
        not isinstance(execution.get(key), (int, float)) or execution[key] <= 0
        for key in (
            "max_rounds_per_arm",
            "rows_per_direction",
            "deadline_seconds_per_arm",
            "max_dense_event_cells_per_direction",
            "max_dense_event_cells_per_round",
            "rationalisation_scale",
        )
    ):
        raise ValueError("source execution settings are incomplete or nonpositive")
    expected_arms = _mapping(expected.get("arms"), "reconstructed arms")
    source_arms = _mapping(receipt.get("arms"), "source arms")
    for label in ("unrestricted", "point", "triangle", "endpoint"):
        expected_arm = _mapping(expected_arms.get(label), f"reconstructed {label}")
        source_arm = _mapping(source_arms.get(label), f"source {label}")
        for key in (
            "footprint",
            "footprint_union",
            "available_sites",
            "retained_singleton_variables",
            "removed_inside_closed_footprint",
            "component_counts",
        ):
            if source_arm.get(key) != expected_arm.get(key):
                raise ValueError(f"source {label}.{key} does not match reconstruction")
    return expected, arms, directions, owner_count


def _endpoint_atoms(receipt: dict[str, Any], arm: Arm) -> tuple[tuple[Atom, ...], Fraction]:
    arm_record = _mapping(_mapping(receipt.get("arms"), "arms").get("endpoint"), "endpoint")
    proposal = _mapping(arm_record.get("proposal"), "endpoint proposal")
    if proposal.get("converged") is not True:
        raise ValueError("endpoint proposal did not converge")
    scale = proposal.get("rationalisation_scale")
    if not isinstance(scale, int) or scale < 1:
        raise ValueError("endpoint rationalisation scale is invalid")
    raw_atoms = _sequence(proposal.get("rationalised_atoms"), "endpoint atoms")
    atoms: list[Atom] = []
    seen: set[Point] = set()
    available = set(arm.sites.positions())
    for index, raw in enumerate(raw_atoms):
        values = _sequence(raw, f"endpoint atom {index}")
        if len(values) != 3:
            raise ValueError("each endpoint atom must be [x,y,weight]")
        point = (
            _fraction(values[0], f"atom {index} x"),
            _fraction(values[1], f"atom {index} y"),
        )
        weight = _fraction(values[2], f"atom {index} weight")
        if point not in available:
            raise ValueError(f"endpoint atom {index} is outside reconstructed support")
        if point in seen:
            raise ValueError(f"endpoint atom {index} duplicates a support position")
        if weight <= 0:
            raise ValueError(f"endpoint atom {index} has nonpositive weight")
        if weight.denominator > scale:
            raise ValueError(
                f"endpoint atom {index} exceeds the declared rationalisation scale"
            )
        seen.add(point)
        atoms.append(Atom(f"endpoint-{index}", point[0], point[1], weight))
    result = tuple(atoms)
    require_nonnegative_atom_weights(result)
    if not result:
        raise ValueError("endpoint proposal has no positive rationalized atoms")
    total = sum((atom.weight for atom in result), start=Fraction(0))
    if total != _fraction(proposal.get("rationalised_total_mass"), "endpoint total mass"):
        raise ValueError("endpoint rationalized total does not equal the atom sum")
    return result, total


def load_bound_source(path: Path, expected_blob: str) -> BoundSource:
    """Load and reconstruct a clean committed numerical endpoint receipt."""

    _, commit, blob = bind_clean_tracked_source(path, expected_blob)
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"could not read source receipt: {error}") from error
    if not isinstance(receipt, dict):
        raise TypeError("source receipt root must be an object")
    _, arms, directions, owner_count = _source_configuration(receipt)
    endpoint = next(arm for arm in arms if arm.label == "endpoint")
    atoms, total = _endpoint_atoms(receipt, endpoint)
    return BoundSource(
        path, commit, blob, receipt, endpoint, directions, atoms, total, owner_count
    )


def replay_directions(
    source: BoundSource,
    scope: str,
) -> tuple[Arm, tuple[Direction, ...]]:
    """Rebuild either the retained endpoint arm or the full-361 endpoint arm."""

    if scope == "retained":
        return source.arm, source.retained_directions
    if scope != "full":
        raise ValueError("scope must be retained or full")
    from devtools.owner_footprints import full_owner_direction_manifest  # noqa: PLC0415

    directions = full_owner_direction_manifest().directions
    settings = _mapping(source.receipt.get("settings"), "settings")
    class_record = _mapping(source.receipt.get("class"), "class")
    expected, arms, _ = build_receipt(
        class_id=str(class_record["id"]),
        grid_count=int(settings["grid_count"]),
        inset=_fraction(settings["inset"], "inset"),
        folded_indices=tuple(int(value) for value in settings["folded_source_indices"]),
        owner_count=source.owner_count,
    )
    del expected
    sites = next(arm for arm in arms if arm.label == "unrestricted").sites
    if source.owner_count == 4:
        full_arms = build_four_owner_arms(sites, directions)
    else:
        # Rebuild with a synthetic full-index selection is impossible because the
        # selection interface names folded sources.  Use the already reconstructed
        # class and public arm constructor directly.
        from devtools.owner_footprints import owner_branch_manifest  # noqa: PLC0415
        from devtools.run_owner_footprint_cover import build_arms  # noqa: PLC0415

        manifest = owner_branch_manifest()
        owner_class = next(
            entry for entry in manifest.classes if entry.class_id == class_record["id"]
        )
        full_arms = build_arms(
            owner_class,
            sites,
            directions,
            direction_manifest=manifest,
        )
    return next(arm for arm in full_arms if arm.label == "endpoint"), directions


def exact_event_cell_count(
    atoms: tuple[Atom, ...],
    arm: Arm,
    direction: Direction,
    direction_index: int,
) -> int:
    """Count the exact reader's dense cells without allocating its array."""

    pieces = arm.pieces_by_direction[direction_index]
    if not pieces:
        return 0
    half = CORE_SIDE / 2
    projected = tuple(
        (
            direction.ux * atom.x + direction.uy * atom.y,
            direction.vx * atom.x + direction.vy * atom.y,
        )
        for atom in atoms
    )
    u_events = {u + offset for u, _ in projected for offset in (-half, half)} | {
        u for polygon in pieces for u, _ in polygon
    }
    v_events = {v + offset for _, v in projected for offset in (-half, half)} | {
        v for polygon in pieces for _, v in polygon
    }
    return (len(u_events) - 1) * (len(v_events) - 1)


def exact_replay(
    source: BoundSource,
    *,
    scope: str,
    max_atoms: int,
    max_event_cells: int,
    max_total_event_cells: int,
    deadline_seconds: float,
    checkpoint: Path | None = None,
) -> dict[str, Any]:
    """Replay every declared direction exactly, with guards and progress receipts."""

    if len(source.atoms) > max_atoms:
        raise ValueError("the endpoint proposal exceeds the atom-count guard")
    arm, directions = replay_directions(source, scope)
    counts = tuple(
        exact_event_cell_count(source.atoms, arm, direction, index)
        for index, direction in enumerate(directions)
    )
    if max(counts, default=0) > max_event_cells:
        raise ValueError("one direction exceeds the exact event-cell guard")
    if sum(counts) > max_total_event_cells:
        raise ValueError("the replay exceeds the total exact event-cell guard")
    threshold = Fraction(10 if source.owner_count == 1 else 7)
    result: dict[str, Any] = {
        "schema": "owner-footprint-exact-replay/v1",
        "status": "running",
        "scientific_target_run": True,
        "source": {
            "path": source.path.as_posix(),
            "git_commit": source.git_commit,
            "git_blob": source.git_blob,
            "owner_count": source.owner_count,
            "endpoint_atoms": len(source.atoms),
            "rationalised_total_mass": str(source.total_mass),
        },
        "scope": {
            "directions": scope,
            "direction_count": len(directions),
            "continuum_angle_transfer_checked": False,
            "claim_limit": "exact selected-net replay only; no all-angle or packing claim",
        },
        "guards": {
            "max_atoms": max_atoms,
            "max_event_cells": max_event_cells,
            "max_total_event_cells": max_total_event_cells,
            "observed_max_event_cells": max(counts, default=0),
            "observed_total_event_cells": sum(counts),
            "deadline_seconds": deadline_seconds,
        },
        "directions": [],
        "summary": None,
    }
    started = time.perf_counter()
    if checkpoint is not None:
        atomic_write_text(checkpoint, json.dumps(result, indent=1) + "\n", make_parents=True)
    records = result["directions"]
    assert isinstance(records, list)
    minima: list[Fraction] = []
    for index, (direction, pieces) in enumerate(
        zip(directions, arm.pieces_by_direction, strict=True)
    ):
        if time.perf_counter() - started >= deadline_seconds:
            result["status"] = "partial"
            least_so_far = min(minima) if minima else None
            result["summary"] = {
                "completed_direction_count": len(minima),
                "minimum_covered_mass_so_far": (
                    None if least_so_far is None else str(least_so_far)
                ),
                "normalised_total_mass_lower_bound": (
                    None
                    if least_so_far is None or least_so_far == 0
                    else str(source.total_mass / least_so_far)
                ),
                "conditional_threshold": str(threshold),
                "criterion_readable": False,
            }
            break
        if not pieces:
            continue
        minimum = exact_minimum_covered_mass_on_pieces(
            source.atoms, direction, CORE_SIDE, pieces
        )
        minima.append(minimum.mass)
        records.append(
            {
                "index": index,
                "label": direction.label,
                "minimum_covered_mass": str(minimum.mass),
                "reachable_cells": minimum.reachable_cells,
                "dense_event_cells": counts[index],
            }
        )
        if checkpoint is not None:
            atomic_write_text(checkpoint, json.dumps(result, indent=1) + "\n")
    else:
        if not minima:
            raise ValueError("exact replay has no nonempty residual direction")
        least = min(minima)
        normalised = source.total_mass / least if least > 0 else None
        result["status"] = "complete"
        result["summary"] = {
            "minimum_covered_mass": str(least),
            "normalised_total_mass": None if normalised is None else str(normalised),
            "conditional_threshold": str(threshold),
            "normalised_mass_below_threshold": (
                normalised is not None and normalised < threshold
            ),
            "scope_is_not_continuum": True,
        }
    result["wall_seconds"] = time.perf_counter() - started
    if checkpoint is not None:
        atomic_write_text(checkpoint, json.dumps(result, indent=1) + "\n")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--expect-receipt-blob", required=True)
    parser.add_argument("--scope", choices=("retained", "full"), default="retained")
    parser.add_argument("--max-atoms", type=int, default=1_000)
    parser.add_argument("--max-event-cells", type=int, default=5_000_000)
    parser.add_argument("--max-total-event-cells", type=int, default=10_000_000)
    parser.add_argument("--deadline-seconds", type=float, default=240)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if min(args.max_atoms, args.max_event_cells, args.max_total_event_cells) < 1:
        parser.error("atom and event-cell guards must be positive")
    if args.deadline_seconds <= 0:
        parser.error("deadline-seconds must be positive")
    source = load_bound_source(args.receipt, args.expect_receipt_blob)
    result = exact_replay(
        source,
        scope=args.scope,
        max_atoms=args.max_atoms,
        max_event_cells=args.max_event_cells,
        max_total_event_cells=args.max_total_event_cells,
        deadline_seconds=args.deadline_seconds,
        checkpoint=args.output,
    )
    print(json.dumps(result, indent=1), flush=True)
    return 0 if result["status"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
