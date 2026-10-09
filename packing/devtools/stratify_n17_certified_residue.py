"""Partition the current admitted n17 residue without searching or admitting anything.

The census validates the ledger and defines the population; only admitted patterns
exclude states. Composition and distance strata reuse the historical survey's helpers,
but its historical selector populations are never inputs here.

Optional producer receipts describe attempts, not exclusions. They join only when they
name the whole state, this cover's frame and its cap. Missing identity remains explicit:
filenames, incomplete receipts and missing nodes cannot establish a tested orbit.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np
from strif import atomic_write_text

from devtools import census_n17_certified as census
from devtools import select_n17_sub_patterns as selector
from devtools import survey_n17_residue as survey
from devtools.check_n17_capacity_one_cover import U
from devtools.provenance import provenance, repository_path
from sqpack import retained_json

SCHEMA = "n17-certified-residue-stratification/v1"
PROVENANCE = provenance(Path(__file__))
TIMINGS = ("producer_seconds", "checker_seconds", "process_cpu_seconds", "wall_seconds")
OUTCOMES = {"stalled": "fixed_point", "round_cap": "round_cap", "time_cap": "time_cap"}


def partition(cover: census.Cover, entries: list[census.Entry]) -> dict[str, Any]:
    """Exact admitted-ledger population, with one row per canonical surviving orbit."""
    admitted = [entry.mask for entry in entries if entry.status == "admitted"]
    expected = census.count(cover, admitted)
    if not expected["endpoint_survives"]:
        raise census.RefusedError("the admitted ledger excludes the endpoint")
    group = cover.geometry.group
    forbidden = sorted({image for mask in admitted for image in selector.orbit(mask, group)})
    alive = selector.survivors(cover.states, forbidden)
    images = np.stack([selector.apply_permutation(alive, permutation) for permutation in group])
    representatives = [int(mask) for mask in np.unique(images.min(axis=0))]
    endpoint_images = sorted(selector.orbit(cover.endpoint_state, group))
    endpoint = min(endpoint_images)
    rows: list[dict[str, Any]] = []
    strata: dict[str, dict[str, Any]] = {}
    for mask in representatives:
        composition = survey.composition(cover.geometry.names, mask)
        distance = survey.distance(mask, endpoint_images)
        key = (
            survey.ENDPOINT_STRATUM
            if mask == endpoint
            else survey.stratum_of(composition, distance)
        )
        orbit_size = len(selector.orbit(mask, group))
        rows.append(
            {
                "mask": mask,
                "cells": [cover.geometry.names[index] for index in selector.cells_of(mask)],
                "composition": composition,
                "distance": distance,
                "orbit_size": orbit_size,
                "stratum": key,
                "attempts": [],
                "unjoined_receipts": [],
            }
        )
        stratum = strata.setdefault(key, {"orbits": 0, "states": 0, "masks": []})
        stratum["orbits"] += 1
        stratum["states"] += orbit_size
        stratum["masks"].append(mask)
    measured = {"surviving_states": sum(row["orbit_size"] for row in rows), "orbits": len(rows)}
    if (
        measured != {key: expected[key] for key in measured}
        or int(alive.size) != measured["surviving_states"]
    ):
        raise census.RefusedError("orbit roster does not partition the certified census")
    if sum(row["orbits"] for row in strata.values()) != len(rows):
        raise census.RefusedError("strata do not partition the orbit roster")
    return {
        "certified": {"admitted": len(admitted), **expected},
        "strata": dict(sorted(strata.items())),
        "orbits": rows,
    }


def receipt_identity(
    cover: census.Cover, receipt: dict[str, Any]
) -> tuple[int | None, list[str]]:
    """A canonical full-state mask, with every missing or mismatched identity premise."""
    problems: list[str] = []
    cells = receipt.get("cells")
    mask = None
    if not isinstance(cells, list) or len(cells) != cover.endpoint_state.bit_count():
        problems.append("missing_or_non_full_state_cells")
    elif any(
        not isinstance(cell, str) or cell not in cover.geometry.names for cell in cells
    ) or len(set(cells)) != len(cells):
        problems.append("invalid_cells")
    else:
        mask = selector.canonical(
            selector.mask_of([cover.geometry.names.index(cell) for cell in cells]),
            cover.geometry.group,
        )
    if receipt.get("frame") != census.KERNEL_FRAME:
        problems.append("missing_frame" if "frame" not in receipt else "different_frame")
    try:
        cap = Fraction(str(receipt["cap"]))
    except KeyError, ValueError, ZeroDivisionError:
        problems.append("missing_or_invalid_cap")
    else:
        if cap != U:
            problems.append("different_cap")
    return mask, problems


def attempt(receipt: dict[str, Any], path: Path) -> dict[str, Any]:
    """Read the producer's disposition and costs; no stall is an exclusion."""
    status = receipt.get("status")
    if not isinstance(status, str):
        outcome = "outcome_unavailable"
    elif status in census.KERNEL_CLOSED:
        outcome = "closed_unadmitted"
    elif status == "INCOMPLETE":
        outcome = "incomplete"
    elif status in {"PASS_CERTIFIED_STALL", "PASS_SAVED_STALL", "PASS_CONTROL_STALLED"}:
        reported = receipt.get("producer_outcome")
        outcome = (
            OUTCOMES.get(reported, "stall_reason_unavailable")
            if isinstance(reported, str)
            else "stall_reason_unavailable"
        )
    elif isinstance(status, str) and status.startswith("REFUSED"):
        outcome = "refused"
    else:
        outcome = "outcome_unavailable"
    timings = {}
    for key in TIMINGS:
        value = receipt.get(key)
        timings[key] = (
            float(value)
            if isinstance(value, (int, float))
            and not isinstance(value, bool)
            and math.isfinite(value)
            and value >= 0
            else None
        )
    extents = receipt.get("final_extents")
    return {
        "receipt": repository_path(path),
        "status": status,
        "outcome": outcome,
        "producer_outcome": receipt.get("producer_outcome"),
        "timings": timings,
        "owner_extents": extents if isinstance(extents, list) and extents else None,
        "owner_support": "unavailable",
        "node_available": "not_checked",
        "provenance": receipt.get("provenance"),
    }


def join_receipts(record: dict[str, Any], cover: census.Cover, paths: list[Path]) -> None:
    """Join only identified receipts; preserve rejected inputs and their possible orbit."""
    by_mask = {row["mask"]: row for row in record["orbits"]}
    unjoined: list[dict[str, Any]] = []
    for path in sorted({path.resolve() for path in paths}):
        receipt = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(receipt, dict):
            raise census.RefusedError(f"{path}: producer receipt is not an object")
        mask, problems = receipt_identity(cover, receipt)
        if mask is not None and mask not in by_mask:
            problems.append("outside_current_residue")
        if problems:
            row = {
                "receipt": repository_path(path),
                "candidate_mask": mask,
                "reasons": problems,
                "reported_attempt": attempt(receipt, path),
            }
            unjoined.append(row)
            if mask in by_mask:
                by_mask[mask]["unjoined_receipts"].append(row)
        else:
            by_mask[mask]["attempts"].append(attempt(receipt, path))
    record["unjoined_inputs"] = unjoined
    for row in record["orbits"]:
        row["test_status"] = (
            "tested_in_supplied_receipts"
            if any(item["outcome"] != "outcome_unavailable" for item in row["attempts"])
            else "outcome_unavailable"
            if row["attempts"] or row["unjoined_receipts"]
            else "untested_in_supplied_receipts"
        )
        row["owner_diagnostics"] = (
            "extents_available_support_unavailable"
            if any(item["owner_extents"] is not None for item in row["attempts"])
            else "unavailable"
        )
    for stratum in record["strata"].values():
        members = [by_mask[mask] for mask in stratum["masks"]]
        stratum["test_status"] = dict(
            sorted(Counter(row["test_status"] for row in members).items())
        )
        stratum["owner_diagnostics"] = dict(
            sorted(Counter(row["owner_diagnostics"] for row in members).items())
        )
        stratum["attempt_outcomes"] = dict(
            sorted(
                Counter(item["outcome"] for row in members for item in row["attempts"]).items()
            )
        )
        attempts = [item for row in members for item in row["attempts"]]
        stratum["attempt_costs"] = {}
        for key in TIMINGS:
            known = [
                item["timings"][key] for item in attempts if item["timings"][key] is not None
            ]
            stratum["attempt_costs"][key] = {
                "measured_attempts": len(known),
                "missing_attempts": len(attempts) - len(known),
                "total_seconds": sum(known) if known else None,
            }


def stratify(
    ledger: Path, *, root: Path = census.REPO, receipts: list[Path] | None = None
) -> dict[str, Any]:
    """Validate the ledger before reporting its exact residue and supplied diagnostics."""
    started = time.monotonic()
    cover = census.cover_context()
    entries, _ = census.load_ledger(cover, ledger, root)
    record = partition(cover, entries)
    paths = sorted({path.resolve() for path in receipts or []})
    join_receipts(record, cover, paths)
    return {
        "schema": SCHEMA,
        "status": (
            "exact admitted-ledger partition; "
            "supplied attempt diagnostics do not admit exclusions"
        ),
        "design": census.DESIGN,
        "cap": str(U),
        "state_semantics": "all closed-cell assignment masks, quotiented only by D4",
        "ledger": ledger.relative_to(root).as_posix()
        if ledger.is_relative_to(root)
        else str(ledger),
        "diagnostics_scope": (
            "only explicitly supplied receipts; absence does not establish "
            "that an orbit was never tested"
        ),
        "outcome_scope": (
            "producer-reported fixed points describe extents; no box compatibility, "
            "rounding-loss or row-resolution diagnosis is inferred"
        ),
        "producer_receipts": [repository_path(path) for path in sorted(set(paths))],
        **record,
        "provenance": {"tool": PROVENANCE, "ledger": provenance(ledger)},
        "seconds": round(time.monotonic() - started, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", default=census.DEFAULT_LEDGER, help="repository-relative")
    parser.add_argument("--root", type=Path, default=census.REPO)
    parser.add_argument("--producer-receipt", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        record = stratify(
            args.root / args.ledger, root=args.root, receipts=args.producer_receipt
        )
    except (census.RefusedError, OSError, ValueError) as error:
        print(json.dumps({"refused": str(error)}))
        return 2
    text = retained_json.dumps(record, sort_keys=True)
    if args.output is not None:
        atomic_write_text(args.output, text)
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
