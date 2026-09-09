#!/usr/bin/env python3
"""Replay residual-cover proposals exactly without solving or changing weights."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from devtools.run_residual_cover_pilot import (
    ANGLE_LIMIT,
    exact_minimum_covered_mass,
    residual_domain_pieces,
    unrestricted_domain_pieces,
)
from sqpack.fractional.colgen import SiteSet, rationalise_sites, site_set_from_grids
from sqpack.fractional.generate import direction_net, net_half_tangents
from sqpack.fractional.model import Atom, Direction

REPO = Path(__file__).resolve().parents[2]
OUTER_SIDE = Fraction(96, 25)
SQUARE_SIDE = Fraction(9977, 10000)
RETAINED_INDICES = (0, 23, 45, 68, 90, 113, 135, 158, 180)
DIRECTION_STEPS = 180
GRID_COUNTS = (19,)
GRID_INSET = Fraction(1, 2)
RATIONALISATION_SCALE = 4_000_000


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a JSON object")
    return value


def source_identity(path: Path, expected_git_blob: str) -> dict[str, object]:
    """Bind clean tracked source bytes to the preregistered Git blob and HEAD."""

    resolved = path.resolve()
    if not resolved.is_relative_to(REPO):
        raise ValueError("raw proposal must be inside the repository")
    relative = resolved.relative_to(REPO).as_posix()

    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=REPO, check=True, capture_output=True, text=True
        ).stdout.strip()

    if git("ls-files", "--error-unmatch", "--", relative) != relative:
        raise ValueError("raw proposal is not tracked")
    if git("status", "--porcelain", "--", relative):
        raise ValueError("raw proposal is dirty")
    observed_blob = git("hash-object", "--", relative)
    commit_blob = git("rev-parse", f"HEAD:{relative}")
    if observed_blob != expected_git_blob or commit_blob != expected_git_blob:
        raise ValueError("raw proposal does not match the expected Git blob")
    return {
        "path": relative,
        "git_commit": git("rev-parse", "HEAD"),
        "git_blob": observed_blob,
        "clean_tracked_blob_match": True,
    }


def _expected_support() -> tuple[SiteSet, dict[str, object]]:
    sites = site_set_from_grids(OUTER_SIDE, GRID_COUNTS, GRID_INSET)
    coordinates = [[[str(x), str(y)] for x, y in orbit] for orbit in sites.orbits]
    canonical = json.dumps(coordinates, separators=(",", ":")).encode()
    return sites, {
        "source": "grids=(19,);inset=1/2",
        "sha256": hashlib.sha256(canonical).hexdigest(),
        "orbits": len(sites.orbits),
        "sites": sites.size,
        "coordinates": coordinates,
    }


def validate_source_record(
    record: dict[str, Any],
) -> tuple[SiteSet, dict[str, tuple[Atom, ...]]]:
    """Refuse wrong settings, support confusion, and altered rationalized atoms."""

    if record.get("schema") != "residual-cover-pilot/v1" or record.get("status") != "complete":
        raise ValueError("source is not a completed residual-cover pilot")
    settings = _mapping(record.get("settings"), "settings")
    required_settings: dict[str, object] = {
        "outer_side": str(OUTER_SIDE),
        "square_side": str(SQUARE_SIDE),
        "direction_indices": list(RETAINED_INDICES),
        "directions": len(RETAINED_INDICES),
        "full_181_direction_net": False,
        "max_rounds_per_arm": 60,
        "rows_per_direction": 4,
        "deadline_seconds_per_arm": 120.0,
        "max_dense_event_cells_per_direction": 2_000_000,
        "max_dense_event_cells_per_round": 15_000_000,
        "rationalisation_scale": RATIONALISATION_SCALE,
    }
    for key, expected in required_settings.items():
        if settings.get(key) != expected:
            raise ValueError(f"source setting {key} is not the exp-136 setting")
    sites, expected_support = _expected_support()
    if _mapping(record.get("support"), "support") != expected_support:
        raise ValueError("source support does not match the exact 19-by-19 grid receipt")
    arms = _mapping(record.get("arms"), "arms")
    if set(arms) != {"unrestricted", "residual"}:
        raise ValueError("source must retain both matched arms")
    proposals: dict[str, tuple[Atom, ...]] = {}
    for label in ("unrestricted", "residual"):
        arm = _mapping(arms[label], f"arm {label}")
        if arm.get("converged") is not True:
            raise ValueError(f"source arm {label} did not converge")
        if arm.get("rationalisation_scale") != RATIONALISATION_SCALE:
            raise ValueError(f"source arm {label} changed the rationalisation scale")
        raw_weights = arm.get("orbit_weights")
        if not isinstance(raw_weights, list) or len(raw_weights) != len(sites.orbits):
            raise ValueError(f"source arm {label} has the wrong orbit-weight vector")
        weights = np.asarray(raw_weights, dtype=float)
        if not np.isfinite(weights).all() or (weights < 0).any():
            raise ValueError(f"source arm {label} has invalid numerical weights")
        expected_atoms = rationalise_sites(sites, weights, scale=RATIONALISATION_SCALE)
        expected_rows = [
            [str(atom.x), str(atom.y), str(atom.weight)] for atom in expected_atoms
        ]
        if arm.get("rationalised_atoms") != expected_rows:
            raise ValueError(f"source arm {label} rationalized atoms disagree with raw weights")
        expected_total = sum((atom.weight for atom in expected_atoms), Fraction(0))
        if arm.get("rationalised_total_mass") != str(expected_total):
            raise ValueError(f"source arm {label} has an inconsistent rationalized total")
        proposals[label] = expected_atoms
    return sites, proposals


def exact_event_cell_count(
    atoms: tuple[Atom, ...],
    direction: Direction,
    *,
    residual: bool,
) -> int:
    """Count the exact dense grid before allocation in the retained exact reader."""

    pieces = (
        residual_domain_pieces(OUTER_SIDE, SQUARE_SIDE, direction)
        if residual
        else unrestricted_domain_pieces(OUTER_SIDE, SQUARE_SIDE, direction)
    )
    half = SQUARE_SIDE / 2
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
    return max(0, len(u_events) - 1) * max(0, len(v_events) - 1)


def arm_summary(
    atoms: tuple[Atom, ...],
    rows: list[dict[str, object]],
    *,
    scope: str,
    label: str,
) -> dict[str, object]:
    """Summarize completed exact rows and conditionally scale a valid full-net cover."""

    if not rows:
        raise ValueError("an exact arm summary requires completed direction rows")
    least = min(Fraction(str(row["minimum_covered_mass"])) for row in rows)
    total = sum((atom.weight for atom in atoms), Fraction(0))
    result: dict[str, object] = {
        "atom_count": len(atoms),
        "unchanged_rationalised_total_mass": str(total),
        "minimum_over_directions": str(least),
        "covers_one_everywhere_checked": least >= 1,
        "directions": rows,
    }
    if scope == "full-net" and label == "residual" and least > 0:
        result["normalized_mass"] = str(total / least)
        result["normalization"] = (
            "exact total/minimum over the complete 181-direction replay; no optimum-gap claim"
        )
    return result


def replay(
    record: dict[str, Any],
    *,
    source: dict[str, object],
    scope: str,
    arm_mode: str,
    max_atoms: int,
    max_event_cells: int,
) -> dict[str, Any]:
    """Run the bounded exact reader and stream one progress receipt per direction."""

    _, proposals = validate_source_record(record)
    full_directions = direction_net(net_half_tangents(ANGLE_LIMIT, DIRECTION_STEPS))
    indices = RETAINED_INDICES if scope == "subset" else tuple(range(181))
    labels = ("residual",) if arm_mode == "residual" else ("unrestricted", "residual")
    started = time.perf_counter()
    results: dict[str, object] = {}
    for label in labels:
        atoms = proposals[label]
        if len(atoms) > max_atoms:
            raise ValueError(f"arm {label} has {len(atoms)} atoms above guard {max_atoms}")
        rows: list[dict[str, object]] = []
        for ordinal, index in enumerate(indices, 1):
            direction = full_directions[index]
            residual = label == "residual"
            event_cells = exact_event_cell_count(atoms, direction, residual=residual)
            if event_cells > max_event_cells:
                raise ValueError(
                    f"arm {label} direction {index} needs {event_cells} exact event cells, "
                    f"above guard {max_event_cells}"
                )
            minimum, reachable = exact_minimum_covered_mass(
                atoms, direction, OUTER_SIDE, SQUARE_SIDE, residual=residual
            )
            row = {
                "direction_index": index,
                "minimum_covered_mass": str(minimum),
                "event_cells": event_cells,
                "reachable_cells": reachable,
                "covers_one": minimum >= 1,
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "progress": "direction-complete",
                        "arm": label,
                        "ordinal": ordinal,
                        "directions": len(indices),
                        **row,
                    }
                ),
                flush=True,
            )
        summary = arm_summary(atoms, rows, scope=scope, label=label)
        results[label] = summary
        least = Fraction(str(summary["minimum_over_directions"]))
        print(
            json.dumps(
                {
                    "progress": "arm-complete",
                    "arm": label,
                    "minimum_over_directions": str(least),
                    "covers_one_everywhere_checked": least >= 1,
                }
            ),
            flush=True,
        )
    return {
        "schema": "residual-cover-exact-replay/v1",
        "status": "complete",
        "evidence_tier": "exact finite-direction replay of unchanged rationalized proposals",
        "claim_limit": (
            "No packing bound; retained mode checks nine directions and full181 checks the "
            "finite 181-direction net only."
        ),
        "source": source,
        "settings": {
            "outer_side": str(OUTER_SIDE),
            "square_side": str(SQUARE_SIDE),
            "scope": scope,
            "direction_indices": list(indices),
            "arm_mode": arm_mode,
            "max_atoms_per_arm": max_atoms,
            "max_event_cells_per_direction": max_event_cells,
            "weight_transform": "none; source rationalised_atoms replayed unchanged",
        },
        "arms": results,
        "seconds": time.perf_counter() - started,
    }


def write_exclusive_atomic(path: Path, record: dict[str, object]) -> None:
    """Publish through a same-directory hard link so an existing file wins."""

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
        ) as temporary:
            json.dump(record, temporary, indent=1)
            temporary.write("\n")
            temporary.flush()
            temporary_name = temporary.name
        os.link(temporary_name, path)
    finally:
        if temporary_name is not None:
            temporary = Path(temporary_name)
            if temporary.exists():
                temporary.unlink()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("source", type=Path)
    parser.add_argument("--expect-source-blob", required=True)
    parser.add_argument("--scope", choices=("subset", "full-net"), required=True)
    parser.add_argument("--arms", choices=("residual", "both"), required=True)
    parser.add_argument("--max-atoms", type=int, default=1_000)
    parser.add_argument("--max-event-cells", type=int, default=2_000_000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if min(args.max_atoms, args.max_event_cells) < 1:
        parser.error("atom and event-cell guards must be positive")
    if args.out.exists():
        parser.error(f"refusing to overwrite {args.out}")
    source = source_identity(args.source, args.expect_source_blob)
    raw = json.loads(args.source.read_text())
    result = replay(
        _mapping(raw, "source"),
        source=source,
        scope=args.scope,
        arm_mode=args.arms,
        max_atoms=args.max_atoms,
        max_event_cells=args.max_event_cells,
    )
    write_exclusive_atomic(args.out, result)
    print(json.dumps({"output": str(args.out), "status": "complete"}), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
