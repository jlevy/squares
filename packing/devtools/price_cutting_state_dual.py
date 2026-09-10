"""Price one retained cutting state with paired 32-row and full-dual support."""

from __future__ import annotations

import argparse
import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from devtools.transport_ceiling_family import source_binding
from sqpack.cover import write_text_atomic
from sqpack.fractional.ceiling import CeilingCertificate, arrangement_lines
from sqpack.fractional.colgen import site_set_from_points, solve_lp
from sqpack.fractional.cutting import (
    Separation,
    family_record,
    load_state,
    rows_from_exact,
    screened_separation,
    support_entries,
    symmetric_placements,
)
from sqpack.fractional.cutting import exact_membership as _exact_membership

WEIGHT_DENOMINATOR = 10**9
DEFAULT_MAX_LINE_PAIRS = 5_000_000


def _write_new(path: Path, record: dict[str, Any]) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    write_text_atomic(path, json.dumps(record, indent=1) + "\n")


def _separation_record(separation: Separation, seconds: float) -> dict[str, Any]:
    return {
        "max_depth": str(separation.max_depth),
        "vertices": separation.vertices,
        "decided_exactly": separation.decided,
        "violating_screen_count": separation.violating,
        "qualifying_new_points": [
            {
                "depth": str(depth),
                "point": [str(value) for value in orbit[0]],
                "orbit": [[str(value) for value in point] for point in orbit],
            }
            for depth, orbit in separation.chosen
        ],
        "seconds": seconds,
    }


def price_state(
    state_path: Path,
    solved_path: Path,
    priced_path: Path,
    *,
    max_line_pairs: int = DEFAULT_MAX_LINE_PAIRS,
) -> dict[str, Any]:
    """Solve once, retain the full support, then price both support arms."""
    if solved_path.resolve() == priced_path.resolve():
        raise ValueError("solved and priced receipts need distinct paths")
    for path in (solved_path, priced_path):
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {path}")
    if max_line_pairs < 0:
        raise ValueError("the line-pair guard must be non-negative")

    started = time.perf_counter()
    state = json.loads(state_path.read_text())
    outer_side, points, exact_rows = load_state(state_path)
    source_family = CeilingCertificate.from_record(state["best_family"])
    net = tuple(Fraction(value) for value in state.get("half_tangents", []))
    net = net or source_family.half_tangents
    if (
        source_family.outer_side != outer_side
        or source_family.square_side != Fraction(state["square_side"])
        or source_family.half_tangents != net
    ):
        raise ValueError("state geometry and best_family disagree")
    if any(direction >= len(net) for direction, _x, _y in exact_rows):
        raise ValueError("state row has an invalid direction index")
    sites = site_set_from_points(outer_side, set(points))
    rows = rows_from_exact(exact_rows, sites, net, source_family.square_side)
    solved = solve_lp(sites, rows)
    if solved is None:
        raise RuntimeError("the transported state linear program is infeasible")
    _weights, duals, objective = solved
    solve_seconds = time.perf_counter() - started
    full_entries = support_entries(
        exact_rows, duals, net, support_cap=None, weight_denominator=WEIGHT_DENOMINATOR
    )
    control_entries = full_entries[:32]
    positive = [int(index) for index in np.argsort(-duals) if duals[index] > 1e-9]
    if len(positive) != len(full_entries):
        raise RuntimeError("positive dual support did not survive rationalization")

    def make_family(entries: Any) -> CeilingCertificate:
        return CeilingCertificate(
            source_family.n,
            outer_side,
            source_family.square_side,
            net,
            symmetric_placements(entries, outer_side, source_family.square_side),
        )

    full_family = make_family(full_entries)
    binding = source_binding(state_path)
    receipt = {
        "schema": "paired-cutting-dual-support-v1",
        "stage": "solved_support",
        "source": binding,
        "source_transport": state.get("transport"),
        "settings": {"control_cap": 32, "weight_denominator": WEIGHT_DENOMINATOR},
        "lp": {
            "objective": objective,
            "seconds": solve_seconds,
            "sites": sites.size,
            "rows": len(exact_rows),
            "raw_duals_hex": [float(value).hex() for value in duals],
        },
        "positive_support": [
            {
                "row_index": index,
                "row": [entry.direction, str(entry.centre_x), str(entry.centre_y)],
                "half_tangent": str(entry.half_tangent),
                "raw_dual_hex": float(duals[index]).hex(),
                "rational_weight": str(entry.weight),
            }
            for index, entry in zip(positive, full_entries, strict=True)
        ],
        "full_family": family_record(full_family),
    }
    _write_new(solved_path, receipt)

    control_family = make_family(control_entries)
    line_started = time.perf_counter()
    arm_data: dict[str, dict[str, Any]] = {}
    lines_by_arm = {}
    for name, family in (("paired32", control_family), ("full", full_family)):
        lines = arrangement_lines(family)
        pairs = len(lines) * (len(lines) - 1) // 2
        lines_by_arm[name] = lines
        arm_data[name] = {
            "support_rows": len(family.placements) // 8,
            "lines": len(lines),
            "candidate_line_pairs": pairs,
            "dual_source": "solved_support.lp.raw_duals_hex",
            "rational_support_source": "solved_support.positive_support",
            "rational_support_selection": "first 32" if name == "paired32" else "all",
        }
    line_seconds = time.perf_counter() - line_started
    priced: dict[str, Any] = {
        "schema": "paired-cutting-dual-pricing-v1",
        "source": binding,
        "solved_support": source_binding(solved_path)["path"],
        "max_line_pairs": max_line_pairs,
        "line_construction_seconds": line_seconds,
        "arms": arm_data,
    }
    if any(arm["candidate_line_pairs"] > max_line_pairs for arm in arm_data.values()):
        priced.update(
            classification="guard_refused",
            evidence_of_paired_32_row_miss=False,
            reason="candidate line-pair estimate exceeds the declared guard",
        )
        _write_new(priced_path, priced)
        return priced

    separations: dict[str, Separation] = {}
    for name, family in (("paired32", control_family), ("full", full_family)):
        separation_started = time.perf_counter()
        separation = screened_separation(
            family, lines_by_arm[name], sites, cap=1, select_above=Fraction(1)
        )
        separations[name] = separation
        arm_data[name]["separation"] = _separation_record(
            separation, time.perf_counter() - separation_started
        )
    full = separations["full"]
    held = {point for orbit in sites.orbits for point in orbit}
    witness_checks = []
    miss = False
    for reported_depth, orbit in full.chosen:
        point = orbit[0]
        paired_depth, paired_members = _exact_membership(control_family, point)
        full_depth, full_members = _exact_membership(full_family, point)
        if full_depth != reported_depth:
            raise RuntimeError("full separation witness disagrees with exact membership")
        absent = all(member not in held for member in orbit)
        if not absent:
            raise RuntimeError("full separation returned an orbit already held by the state")
        witness_checks.append(
            {
                "point": [str(value) for value in point],
                "orbit": [[str(value) for value in member] for member in orbit],
                "orbit_absent_from_state": absent,
                "paired32": {
                    "depth": str(paired_depth),
                    "placement_indices": paired_members,
                },
                "full": {
                    "depth": str(full_depth),
                    "placement_indices": full_members,
                },
            }
        )
        miss = miss or paired_depth <= Fraction(1) < full_depth
    priced.update(
        classification="paired_32_row_miss" if miss else "unresolved",
        evidence_of_paired_32_row_miss=miss,
        witness_checks=witness_checks,
        reason=(
            "full support found an exact qualifying new state point with "
            "paired32 depth at most one"
            if miss
            else "paired pricing did not establish an exact same-point 32-row support miss"
        ),
    )
    _write_new(priced_path, priced)
    return priced


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("--solved", type=Path, required=True)
    parser.add_argument("--priced", type=Path, required=True)
    parser.add_argument("--max-line-pairs", type=int, default=DEFAULT_MAX_LINE_PAIRS)
    args = parser.parse_args(argv)
    result = price_state(
        args.state, args.solved, args.priced, max_line_pairs=args.max_line_pairs
    )
    print(json.dumps({"priced": str(args.priced), "classification": result["classification"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
