"""Screen a bounded exact sample from an immutable paired-pricing support receipt.

Only an absent D4 orbit whose exact paired32 depth is at most one and whose exact
full-support depth exceeds one is positive evidence. Every guard or exhausted
sample is unresolved; this tool makes no complete geometric or packing claim.
"""

from __future__ import annotations

import argparse
import heapq
import json
import re
import subprocess
from collections.abc import Iterator, Mapping, Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools.transport_ceiling_family import REPO, source_binding
from sqpack.cover import write_text_atomic
from sqpack.fractional.ceiling import (
    CeilingCertificate,
    Line,
    arrangement_lines,
    exact_intersection,
)
from sqpack.fractional.colgen import d4_orbit, site_set_from_points
from sqpack.fractional.cutting import (
    ExactRow,
    SupportEntry,
    exact_membership,
    load_state,
    symmetric_placements,
)

CONTROL_ROWS = 32
COMMIT_ID = re.compile(r"[0-9a-fA-F]{40}")


def _write_new(path: Path, record: dict[str, Any]) -> dict[str, Any]:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    write_text_atomic(path, json.dumps(record, indent=1) + "\n")
    return record


def _mapping(value: object, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{field} is not a mapping")
    return value


def _fraction(value: object, field: str) -> Fraction:
    if not isinstance(value, str):
        raise TypeError(f"{field} is not an exact rational string")
    return Fraction(value)


def _entries(
    support: Mapping[str, Any],
    exact_rows: list[ExactRow],
    family: CeilingCertificate,
) -> tuple[SupportEntry, ...]:
    raw_entries = support.get("positive_support")
    if not isinstance(raw_entries, list):
        raise TypeError("positive_support is not a list")
    entries: list[SupportEntry] = []
    row_indices: set[int] = set()
    for offset, raw in enumerate(raw_entries):
        item = _mapping(raw, f"positive_support[{offset}]")
        row = item.get("row")
        row_index = item.get("row_index")
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError(f"positive_support[{offset}].row is not a three-item list")
        if type(row_index) is not int or not 0 <= row_index < len(exact_rows):
            raise ValueError(f"positive_support[{offset}].row_index is invalid")
        if row_index in row_indices:
            raise ValueError("positive_support repeats a row_index")
        row_indices.add(row_index)
        direction = row[0]
        if type(direction) is not int or not 0 <= direction < len(family.half_tangents):
            raise ValueError(f"positive_support[{offset}].row direction is invalid")
        exact_row = (
            direction,
            _fraction(row[1], f"positive_support[{offset}].row[1]"),
            _fraction(row[2], f"positive_support[{offset}].row[2]"),
        )
        if exact_row != exact_rows[row_index]:
            raise ValueError(f"positive_support[{offset}] disagrees with the source state")
        tangent = _fraction(
            item.get("half_tangent"), f"positive_support[{offset}].half_tangent"
        )
        weight = _fraction(
            item.get("rational_weight"), f"positive_support[{offset}].rational_weight"
        )
        if tangent != family.half_tangents[direction] or weight <= 0:
            raise ValueError(f"positive_support[{offset}] has invalid exact support data")
        entries.append(SupportEntry(direction, tangent, exact_row[1], exact_row[2], weight))
    return tuple(entries)


def _line_record(index: int, line: Line) -> dict[str, Any]:
    return {"line_index": index, "coefficients": [str(value) for value in line]}


def _git_blob(commit: str, path: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "show", f"{commit}:{path}"],
            cwd=REPO,
            check=True,
            capture_output=True,
        ).stdout
    except subprocess.CalledProcessError as error:
        raise ValueError("recorded state Git blob is unavailable") from error


def _verify_state_binding(state_path: Path, raw: object) -> dict[str, Any]:
    recorded = _mapping(raw, "solved support source binding")
    required = {
        "source_in_worktree": True,
        "source_tracked": True,
        "source_dirty": False,
    }
    if any(recorded.get(key) != value for key, value in required.items()):
        raise ValueError("recorded state binding is untracked, dirty, or outside the worktree")
    path, commit = recorded.get("path"), recorded.get("git_commit")
    if not isinstance(path, str) or not isinstance(commit, str):
        raise TypeError("recorded state binding lacks Git path or commit identity")
    if COMMIT_ID.fullmatch(commit) is None:
        raise ValueError("recorded state commit is not a full 40-character hexadecimal id")
    observed = source_binding(state_path)
    if observed.get("path") != path or any(
        observed.get(key) != value for key, value in required.items()
    ):
        raise ValueError("current state path is missing, dirty, untracked, or rebound")
    if _git_blob(commit, path) != state_path.read_bytes():
        raise ValueError("current state bytes differ from the recorded Git blob")
    return {"recorded": dict(recorded), "observed": observed, "git_blob_match": True}


def incident_pairs(count: int, selected: set[int]) -> Iterator[tuple[int, int]]:
    """Selected-incident pairs in lexicographic order, without visiting other pairs."""

    def stream(chosen: int) -> Iterator[tuple[int, int]]:
        yield from ((index, chosen) for index in range(chosen))
        yield from ((chosen, index) for index in range(chosen + 1, count))

    previous: tuple[int, int] | None = None
    for pair in heapq.merge(*(stream(chosen) for chosen in sorted(selected))):
        if pair != previous:
            yield pair
            previous = pair


def screen_candidates(
    state_path: Path,
    solved_path: Path,
    output_path: Path,
    *,
    tail_line_limit: int,
    max_line_pairs: int,
    max_unique_points: int,
) -> dict[str, Any]:
    """Evaluate one deterministic tail-boundary sample without solving another LP."""
    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite {output_path}")
    if min(tail_line_limit, max_line_pairs, max_unique_points) < 0:
        raise ValueError("sampling limits must be non-negative")

    state = _mapping(json.loads(state_path.read_text()), "state")
    support = _mapping(json.loads(solved_path.read_text()), "solved support")
    if support.get("schema") != "paired-cutting-dual-support-v1":
        raise ValueError("solved support has the wrong schema")
    if support.get("stage") != "solved_support":
        raise ValueError("solved support has the wrong stage")
    settings = _mapping(support.get("settings"), "solved support settings")
    if settings.get("control_cap") != CONTROL_ROWS:
        raise ValueError("solved support does not declare the paired32 control")
    state_binding = _verify_state_binding(state_path, support.get("source"))
    if support.get("source_transport") != state.get("transport"):
        raise ValueError("solved support transport binding does not match the state")

    outer_side, points, exact_rows = load_state(state_path)
    state_family = CeilingCertificate.from_record(
        _mapping(state.get("best_family"), "state best_family")
    )
    full_family = CeilingCertificate.from_record(
        _mapping(support.get("full_family"), "solved support full_family")
    )
    state_net = tuple(Fraction(value) for value in state.get("half_tangents", []))
    state_net = state_net or state_family.half_tangents
    geometry = (
        outer_side,
        _fraction(state.get("square_side"), "state square_side"),
        state_net,
    )
    if geometry != (
        state_family.outer_side,
        state_family.square_side,
        state_family.half_tangents,
    ) or geometry != (
        full_family.outer_side,
        full_family.square_side,
        full_family.half_tangents,
    ):
        raise ValueError("state and solved-support geometry disagree")
    if state_family.n != full_family.n:
        raise ValueError("state and solved-support instance disagree")
    sites = site_set_from_points(outer_side, set(points))
    lp = _mapping(support.get("lp"), "solved support lp")
    if lp.get("rows") != len(exact_rows) or lp.get("sites") != sites.size:
        raise ValueError("solved support dimensions disagree with the state")
    entries = _entries(support, exact_rows, full_family)
    rebuilt = symmetric_placements(entries, outer_side, full_family.square_side)
    if rebuilt != full_family.placements:
        raise ValueError("full_family is not the recorded positive support in order")

    control_count = min(CONTROL_ROWS * 8, len(full_family.placements))
    paired_family = CeilingCertificate(
        full_family.n,
        outer_side,
        full_family.square_side,
        full_family.half_tangents,
        full_family.placements[:control_count],
    )
    all_lines = arrangement_lines(full_family)
    line_indices = {line: index for index, line in enumerate(all_lines)}
    tail_lines: list[Line] = []
    seen_tail: set[Line] = set()
    for placement in full_family.placements[control_count:]:
        for line in placement.lines():
            if line not in seen_tail:
                seen_tail.add(line)
                tail_lines.append(line)
    selected_lines = tail_lines[:tail_line_limit]
    selected_indices = {line_indices[line] for line in selected_lines}
    selected_count = len(selected_indices)
    line_pair_estimate = (
        selected_count * len(all_lines) - selected_count * (selected_count + 1) // 2
    )
    receipt: dict[str, Any] = {
        "schema": "paired-cutting-dual-candidate-screen-v1",
        "source_state": state_binding,
        "source_solved_support": source_binding(solved_path),
        "settings": {
            "control_rows": CONTROL_ROWS,
            "tail_line_limit": tail_line_limit,
            "max_line_pairs": max_line_pairs,
            "max_unique_points": max_unique_points,
        },
        "support_rows": len(entries),
        "all_lines": len(all_lines),
        "tail_lines_available": len(tail_lines),
        "selected_tail_lines": [
            _line_record(line_indices[line], line) for line in selected_lines
        ],
        "candidate_line_pair_estimate": line_pair_estimate,
        "sampling": {
            "line_pairs_examined": 0,
            "unique_points_examined": 0,
            "parallel_pairs": 0,
            "outside_points": 0,
            "duplicate_points": 0,
            "held_orbit_points": 0,
        },
        "classification": "unresolved",
        "evidence_of_paired_32_row_miss": False,
    }
    if line_pair_estimate > max_line_pairs:
        receipt.update(
            stop_reason="line_pair_guard",
            reason="selected line-pair estimate exceeds the declared guard",
        )
        return _write_new(output_path, receipt)
    if line_pair_estimate and max_unique_points == 0:
        receipt.update(
            stop_reason="unique_point_guard",
            reason="the declared unique-point guard permits no candidate",
        )
        return _write_new(output_path, receipt)

    held = {point for orbit in sites.orbits for point in orbit}
    seen_points: set[tuple[Fraction, Fraction]] = set()
    sampling = receipt["sampling"]
    assert isinstance(sampling, dict)
    for first_index, second_index in incident_pairs(len(all_lines), selected_indices):
        first = all_lines[first_index]
        sampling["line_pairs_examined"] += 1
        point = exact_intersection(first, all_lines[second_index])
        if point is None:
            sampling["parallel_pairs"] += 1
            continue
        if not (0 <= point[0] <= outer_side and 0 <= point[1] <= outer_side):
            sampling["outside_points"] += 1
            continue
        if point in seen_points:
            sampling["duplicate_points"] += 1
            continue
        if len(seen_points) >= max_unique_points:
            receipt.update(
                stop_reason="unique_point_guard",
                reason="the deterministic sample reached the declared unique-point guard",
            )
            return _write_new(output_path, receipt)
        seen_points.add(point)
        sampling["unique_points_examined"] += 1
        paired_depth, paired_members = exact_membership(paired_family, point)
        full_depth, full_members = exact_membership(full_family, point)
        orbit = d4_orbit(*point, outer_side)
        absent = all(member not in held for member in orbit)
        if not absent:
            sampling["held_orbit_points"] += 1
        if absent and paired_depth <= 1 < full_depth:
            receipt.update(
                classification="paired_32_row_miss",
                evidence_of_paired_32_row_miss=True,
                stop_reason="exact_witness",
                reason=(
                    "a selected exact point has paired32 depth at most one and "
                    "full-support depth above one on an absent state orbit"
                ),
                witness={
                    "point": [str(value) for value in point],
                    "orbit": [[str(value) for value in member] for member in orbit],
                    "orbit_absent_from_state": True,
                    "source_lines": [
                        _line_record(first_index, first),
                        _line_record(second_index, all_lines[second_index]),
                    ],
                    "paired32": {
                        "depth": str(paired_depth),
                        "placement_indices": paired_members,
                    },
                    "full": {
                        "depth": str(full_depth),
                        "placement_indices": full_members,
                    },
                },
            )
            return _write_new(output_path, receipt)
    receipt.update(
        stop_reason="selected_sample_exhausted",
        reason="the selected candidate sample was exhausted without an exact witness",
    )
    return _write_new(output_path, receipt)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    parser.add_argument("solved", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--tail-lines", type=int, required=True)
    parser.add_argument("--max-line-pairs", type=int, required=True)
    parser.add_argument("--max-unique-points", type=int, required=True)
    args = parser.parse_args(argv)
    result = screen_candidates(
        args.state,
        args.solved,
        args.out,
        tail_line_limit=args.tail_lines,
        max_line_pairs=args.max_line_pairs,
        max_unique_points=args.max_unique_points,
    )
    print(json.dumps({"output": str(args.out), "classification": result["classification"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
