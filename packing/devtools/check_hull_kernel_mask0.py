"""Replay n11's mask-0 field packet through `sqpack.hull_kernel` on the n11 frame.

The method control for the hull-kernel adaptation (BC-418, slice 1a). The frozen
checker `check_n11_optimality_field_mask0` loads every input under its SHA-256 pins
and admits it; this tool then builds the n11 frame and the counting packet through the
library's adapters, replays all 55 ownership proofs, all 136 rows and the half-turn
transfer through the library, runs the frozen checker's own `all_geometry` on the same
inputs (in a second process with `--workers 2`), and compares both, field by field and
`Fraction` string by string, with the retained receipt
`receipts/field-mask0/result.json`, itself pinned by its SHA-256. Any difference
refuses, and the refusal names the first differing path.

`--sample` replays owner 0's points, the first row of each positive cell and the
transfer, against the frozen per-item functions and the receipt's entries at the same
positions; it is a partial check and claims nothing.

`--n17-frame` builds and validates the n17 frame instead: the H-266 unique-state design
`ring-3-voronoi-8-tabbed-unique` at cap 1169/250 with D4, checked against the cover
tool's cells, permutations and Burnside count. No n17 exclusion is run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Any

from devtools import check_n11_optimality_field_mask0 as frozen
from devtools import check_n17_capacity_one_cover as n17_cover
from sqpack.hull_kernel import counting, n11, n17
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError
from sqpack.hull_kernel.rational import as_fraction

RECEIPT_DIR = frozen.PACKET / "receipts/field-mask0"
RECEIPT = RECEIPT_DIR / "result.json"
RECEIPT_SHA = "821274111e6eb50d47e20882da083e3e23d25ee37e6725a18b18d133ab798663"
OBJECTS = RECEIPT_DIR / "objects"
COVER = frozen.PACKET / "receipts/d4-independent/objects" / f"{frozen.COVER_SHA}.gz"
FROZEN_SHA = "75fc0238f2ac91af9dc9cf57bd00792343dcf3321c395adddebf0f3465113ce5"
# SHA-256 of the canonical JSON (sorted keys, no spaces) of each object the frozen loader
# admits, so that the library adapters are refused any input but those exact contents.
CONTENT_SHA = {
    "packet": "eb6b7413933ef77a6d36e1c3701485ff532a1c5a387ab4112ec9f4c420ed8f48",
    "audit": "b0544e5ebd15dfb86986b04bfda57aea88667df7593c876476c851b97cc8f831",
    "cover": "883f21ed4b666724dfdfa85eefdab4252db6be0a74b95e3b6e958a7c37a1171b",
}
KERNEL_DIR = Path(counting.__file__).resolve().parent
# n11's published inventory for mask 0: owners and points, rows per positive cell, cases.
OWNER_POINTS = {0: 11, 1: 10, 2: 12, 3: 12, 6: 10}
ROWS_PER_CELL = {1: 67, 2: 69}
DIRECT_CASES = 453
TRANSFERRED_CASES = 459
SHARED_FIELDS = (
    "ownership_checked",
    "rows_checked",
    "transfer",
    "work_units",
    "ownership_points",
    "positive_cell_rows",
    "canonical_cases_excluded",
    "geometry_verified",
)
FROZEN_PASS = "PASS_ONE_FIELD_MASK0_GEOMETRY_AND_TRANSFER"
N17_DESIGN = n17_cover.UNIQUE_24
N17_CELLS = 24
N17_ORBITS = 43593

type Sources = tuple[dict[str, Any], dict[str, Any], dict[str, Any]]


class _Absent:
    """Marks a key present on one side of a comparison only."""

    def __repr__(self) -> str:
        return "<absent>"


_ABSENT = _Absent()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def first_difference(left: Any, right: Any, path: str = "") -> str | None:
    """The first path at which two JSON values differ, or None if they are equal."""
    if isinstance(left, dict) and isinstance(right, dict):
        pairs = [
            (f"{path}.{key}", left.get(key, _ABSENT), right.get(key, _ABSENT))
            for key in sorted(set(left) | set(right))
        ]
    elif isinstance(left, list) and isinstance(right, list):
        if len(left) != len(right):
            return f"{path} (lengths {len(left)} and {len(right)})"
        pairs = [
            (f"{path}[{n}]", a, b) for n, (a, b) in enumerate(zip(left, right, strict=True))
        ]
    else:
        same = type(left) is type(right) and left == right
        return None if same else f"{path} ({left!r} against {right!r})"
    for where, a, b in pairs:
        found = first_difference(a, b, where)
        if found is not None:
            return found
    return None


def require_same(left: Any, right: Any, what: str) -> None:
    found = first_difference(left, right)
    if found is not None:
        raise RefusalError(f"{what} differ at {found or 'the root'}")


def load_sources(objects: Path = OBJECTS, cover: Path = COVER) -> Sources:
    """The pinned packet, audit and cover, admitted by the frozen checker itself."""
    packet, audit, cover_object = frozen.load_sources(objects, cover)
    frozen.admit(packet, audit, cover_object)
    frozen.admit_d4_receipt()
    return packet, audit, cover_object


def load_baseline() -> dict[str, Any]:
    return frozen.pinned_gzip(
        frozen.PACKET / "receipts/case-census/objects" / f"{frozen.A1_SHA}.gz",
        packed_bytes=26100,
        packed_sha=frozen.A1_LFS_SHA,
        raw_bytes=122029,
        raw_sha=frozen.A1_SHA,
    )


def load_receipt(path: Path = RECEIPT) -> dict[str, Any]:
    raw = path.read_bytes()
    if sha(raw) != RECEIPT_SHA:
        raise RefusalError("retained mask-0 receipt changed")
    receipt = frozen.strict_json(raw)
    if receipt.get("checker_sha256") != FROZEN_SHA or receipt.get("status") != FROZEN_PASS:
        raise RefusalError("retained mask-0 receipt identity changed")
    return receipt


def admit_frozen_source() -> None:
    if sha(Path(frozen.__file__).read_bytes()) != FROZEN_SHA:
        raise RefusalError("the frozen mask-0 checker changed")


def a1_cases(baseline: dict[str, Any]) -> set[int]:
    entries = [
        row
        for row in baseline["certificates"]
        if row.get("family") == "field" and row.get("source_sha256") == frozen.FIELD_SHA
    ]
    if len(entries) != 1:
        raise RefusalError("A1 mask-0 certificate identity changed")
    return set(entries[0]["cases"])


def content_digest(value: dict[str, Any]) -> str:
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":")).encode())


def admit_content(sources: Sources) -> None:
    """Refuse any packet, audit or cover whose content is not the pinned object's."""
    for name, value in zip(("packet", "audit", "cover"), sources, strict=True):
        if content_digest(value) != CONTENT_SHA[name]:
            raise RefusalError(f"{name} content differs from the pinned object")


def library_inputs(
    sources: Sources,
) -> tuple[Frame, counting.CountingPacket, list[counting.Row]]:
    """The n11 frame, packet and ordered rows, through the library adapters only."""
    admit_content(sources)
    packet, audit, cover = sources
    frame = n11.frame_from_cover(cover, provenance=f"n11 cover {frozen.COVER_SHA}")
    library_packet = n11.packet_from_field(frame, packet)
    if {owner: len(library_packet.owned_points[owner]) for owner in library_packet.owners} != (
        OWNER_POINTS
    ):
        raise RefusalError("mask-0 owner inventory changed")
    rows = counting.partition_rows(n11.rows_from_audit(audit), library_packet.positive_cells)
    per_cell = {cell: sum(1 for row in rows if row[0] == cell) for cell in ROWS_PER_CELL}
    if per_cell != ROWS_PER_CELL or len(rows) != sum(ROWS_PER_CELL.values()):
        raise RefusalError("positive-cell row counts changed")
    return frame, library_packet, rows


def pin_transfer(transfer: dict[str, list[int]] | None, baseline: dict[str, Any]) -> None:
    if transfer is None:
        raise RefusalError("no transfer was computed")
    if len(transfer["direct_case_ids"]) != DIRECT_CASES:
        raise RefusalError("direct case count changed")
    if len(transfer["transferred_case_ids"]) != TRANSFERRED_CASES:
        raise RefusalError("transferred case count changed")
    if set(transfer["transferred_case_ids"]) != a1_cases(baseline):
        raise RefusalError("transferred cases differ from the A1 list")


def frozen_full(objects: str, cover: str, max_seconds: float, max_nodes: int) -> dict[str, Any]:
    """The frozen checker's own complete run; a top-level function so a worker can run it."""
    start = time.monotonic()
    packet, audit, cover_object = load_sources(Path(objects), Path(cover))
    result = frozen.all_geometry(
        packet,
        audit,
        cover_object,
        load_baseline(),
        budget=frozen.Budget(start + max_seconds, max_nodes),
    )
    result["wall_seconds"] = time.monotonic() - start
    return result


def full_replay(
    sources: Sources,
    *,
    max_seconds: float,
    max_nodes: int,
    workers: int = 2,
    objects: Path = OBJECTS,
    cover: Path = COVER,
) -> dict[str, Any]:
    """The whole packet through the library and the frozen checker, against the receipt."""
    admit_frozen_source()
    receipt = load_receipt()
    baseline = load_baseline()
    frame, packet, rows = library_inputs(sources)
    arguments = (str(objects), str(cover), max_seconds, max_nodes)

    def run_library() -> tuple[dict[str, Any], float]:
        start = time.monotonic()
        result = counting.replay_counting_packet(
            frame, packet, rows, budget=Budget(start + max_seconds, max_nodes)
        )
        return result, time.monotonic() - start

    if workers > 1:
        with ProcessPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(frozen_full, *arguments)
            library, library_seconds = run_library()
            reference = pending.result()
    else:
        library, library_seconds = run_library()
        reference = frozen_full(*arguments)
    if library["status"] != "PASS_COUNTING_PACKET":
        raise RefusalError(f"library replay did not pass: {library.get('reason')}")
    if reference["status"] != FROZEN_PASS:
        raise RefusalError(f"frozen replay did not pass: {reference.get('reason')}")
    pin_transfer(library["transfer"], baseline)
    for field in SHARED_FIELDS:
        require_same(library[field], reference[field], f"library and frozen {field}")
        require_same(library[field], receipt[field], f"library and receipt {field}")
    return {
        "status": "PASS_LIBRARY_REPRODUCES_MASK0",
        "frame": frame.name,
        "ownership_points": library["ownership_points"],
        "positive_cell_rows": library["positive_cell_rows"],
        "rows_by_cell": ROWS_PER_CELL,
        "direct_cases": len(library["transfer"]["direct_case_ids"]),
        "transferred_cases": len(library["transfer"]["transferred_case_ids"]),
        "work_units": library["work_units"],
        "receipt_counts": {
            "ownership_points": receipt["ownership_points"],
            "positive_cell_rows": receipt["positive_cell_rows"],
            "direct_cases": len(receipt["transfer"]["direct_case_ids"]),
            "transferred_cases": len(receipt["transfer"]["transferred_case_ids"]),
            "work_units": receipt["work_units"],
        },
        "compared_fields": list(SHARED_FIELDS),
        "library_wall_seconds": library_seconds,
        "frozen_wall_seconds": reference["wall_seconds"],
        "geometry_verified": True,
    }


def sample_replay(
    sources: Sources,
    *,
    points: Sequence[tuple[int, int]],
    row_positions: Sequence[int],
    max_seconds: float,
    max_nodes: int,
) -> dict[str, Any]:
    """A partial replay against the frozen per-item functions and the receipt's entries."""
    admit_frozen_source()
    receipt = load_receipt()
    baseline = load_baseline()
    packet_json, _, cover = sources
    frame, packet, rows = library_inputs(sources)
    selected = [rows[position] for position in row_positions]
    start = time.monotonic()
    library = counting.replay_counting_packet(
        frame,
        packet,
        selected,
        budget=Budget(start + max_seconds, max_nodes),
        points=points,
    )
    if library["status"] != "PASS_PARTIAL_REPLAY":
        raise RefusalError(f"library replay did not pass: {library.get('reason')}")
    budget = frozen.Budget(time.monotonic() + max_seconds, max_nodes)
    point_reference = [
        {
            "owner": owner,
            "point_index": index,
            **frozen.ownership(
                frozen.cell_vertices(cover, owner),
                frozen.point(packet_json["ownership_points_field"][owner][index]),
                budget=budget,
            ),
        }
        for owner, index in points
    ]
    row_reference = [
        {
            "row_index": index,
            **frozen.row_geometry(
                packet_json,
                cover,
                cell,
                (as_fraction(interval[0]), as_fraction(interval[1])),
                budget=budget,
            ),
        }
        for cell, index, interval in selected
    ]
    transfer_reference = frozen.transferred_cases(packet_json, cover, baseline)
    positions = {key: number for number, key in enumerate(_receipt_point_keys(receipt))}
    require_same(library["ownership_checked"], point_reference, "library and frozen points")
    require_same(
        library["ownership_checked"],
        [receipt["ownership_checked"][positions[key]] for key in points],
        "library and receipt points",
    )
    require_same(library["rows_checked"], row_reference, "library and frozen rows")
    require_same(
        library["rows_checked"],
        [receipt["rows_checked"][position] for position in row_positions],
        "library and receipt rows",
    )
    pin_transfer(library["transfer"], baseline)
    require_same(library["transfer"], transfer_reference, "library and frozen transfer")
    require_same(library["transfer"], receipt["transfer"], "library and receipt transfer")
    return {
        "status": "PASS_PARTIAL_SAMPLE",
        "frame": frame.name,
        "points_checked": len(points),
        "rows_checked": len(selected),
        "direct_cases": len(library["transfer"]["direct_case_ids"]),
        "transferred_cases": len(library["transfer"]["transferred_case_ids"]),
        "geometry_verified": False,
    }


def _receipt_point_keys(receipt: dict[str, Any]) -> list[tuple[int, int]]:
    return [(entry["owner"], entry["point_index"]) for entry in receipt["ownership_checked"]]


def n17_unique_frame() -> Frame:
    """The n17 frame on H-266's unique-state cover, cross-checked against the cover tool."""
    cells = n17_cover.build_cover(N17_DESIGN)
    frame = n17.frame_from_cells(
        [(cell.name, cell.vertices) for cell in cells],
        design=N17_DESIGN.name,
        provenance=(
            "devtools/check_n17_capacity_one_cover.py build_cover("
            f"{N17_DESIGN.name}), module {sha(Path(n17_cover.__file__).read_bytes())}"
        ),
    )
    permutations = n17_cover.d4_permutations(cells)
    if permutations is None:
        raise RefusalError("the cover tool finds the design not D4-invariant")
    if any(list(action.permutation) != permutations[action.name] for action in frame.actions):
        raise RefusalError("frame permutations differ from the cover tool's")
    if [cell.vertices for cell in cells] != list(frame.cells):
        raise RefusalError("frame cells differ from the cover tool's")
    if len(frame.cells) != N17_CELLS or frame.scale != 1 or frame.cap != n17_cover.U:
        raise RefusalError("the n17 frame must have 24 cells, B = 1 and the cover's cap")
    return frame


def n17_frame_summary(frame: Frame) -> dict[str, Any]:
    census = n17_cover.burnside(
        {action.name: list(action.permutation) for action in frame.actions}
    )
    representatives = frame.representatives
    if len(representatives) != census["orbits"] or len(representatives) != N17_ORBITS:
        raise RefusalError("orbit representatives differ from the Burnside count")
    return {
        "status": "PASS_N17_FRAME_BUILT_NO_EXCLUSION",
        "frame": frame.name,
        "cap": str(frame.cap),
        "scale": str(frame.scale),
        "cells": len(frame.cells),
        "cell_names": list(frame.cell_names),
        "actions": {action.name: list(action.permutation) for action in frame.actions},
        "states": census["states"],
        "orbit_representatives": len(representatives),
        "burnside_orbits": census["orbits"],
        "first_representative": [frame.cell_names[i] for i in representatives[0]],
        "cells_reaching_diameter_one": list(frame.cells_reaching_diameter_one()),
        "provenance": frame.provenance,
    }


def kernel_digests() -> dict[str, str]:
    return {path.name: sha(path.read_bytes()) for path in sorted(KERNEL_DIR.glob("*.py"))}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--sample", action="store_true", help="a partial replay; claims nothing")
    mode.add_argument("--n17-frame", action="store_true", help="build the n17 frame only")
    parser.add_argument("--objects", type=Path, default=OBJECTS)
    parser.add_argument("--cover", type=Path, default=COVER)
    parser.add_argument("--workers", type=int, choices=(1, 2), default=2)
    parser.add_argument("--max-seconds", type=float, default=120.0)
    parser.add_argument("--max-nodes", type=int, default=100000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0 or args.max_nodes <= 0:
        parser.error("ceilings must be positive and finite")
    start, cpu = time.monotonic(), time.process_time()
    try:
        if args.n17_frame:
            result = n17_frame_summary(n17_unique_frame())
        else:
            sources = load_sources(args.objects, args.cover)
            if args.sample:
                result = sample_replay(
                    sources,
                    points=[(0, index) for index in range(OWNER_POINTS[0])],
                    row_positions=[0, ROWS_PER_CELL[1]],
                    max_seconds=args.max_seconds,
                    max_nodes=args.max_nodes,
                )
            else:
                result = full_replay(
                    sources,
                    max_seconds=args.max_seconds,
                    max_nodes=args.max_nodes,
                    workers=args.workers,
                    objects=args.objects,
                    cover=args.cover,
                )
    except IncompleteError as error:
        result = {"status": "INCOMPLETE", "reason": str(error), "geometry_verified": False}
    except (ValueError, KeyError, IndexError, TypeError, OSError) as error:
        result = {"status": "REFUSED", "reason": str(error), "geometry_verified": False}
    result.update(
        kernel_sha256=kernel_digests(),
        frozen_checker_sha256=FROZEN_SHA,
        receipt_sha256=RECEIPT_SHA,
        tool_sha256=sha(Path(__file__).read_bytes()),
        wall_seconds=time.monotonic() - start,
        process_cpu_seconds=time.process_time() - cpu,
        wall_ceiling_seconds=args.max_seconds,
    )
    encoded = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0 if str(result["status"]).startswith("PASS") else 2


if __name__ == "__main__":
    sys.exit(main())
