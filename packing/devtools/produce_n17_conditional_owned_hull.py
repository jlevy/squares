"""Produce one explicit parent-relative, closed-guard ownership continuation.

Preparation belongs to the separate conditional checker. Each step is locally
certified before reuse; production alone is never a conditional exclusion receipt.
The original endpoint lies outside the guard and is not an update invariant.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import math
import sys
import time
from importlib import import_module
from pathlib import Path
from typing import Any

from devtools import pilot_n17_capture as pilot
from devtools.check_n17_capture_checkpoint import read_frame
from devtools.provenance import provenance
from sqpack import retained_json
from sqpack.hull_kernel import node
from sqpack.hull_kernel.geometry import Budget, IncompleteError, RefusalError, require
from sqpack.hull_kernel.induction import encode
from sqpack.hull_kernel.rational import Q, as_fraction

SCHEMA = "n17-conditional-owned-hull-production/v1"
CHILD_SCHEMA = "n17-parent-guard-owned-hull/v1"
DESCRIPTOR_SCHEMA = "n17-parent-guard-owned-hull-context/v1"
GUARD = {"kind": "closed_half_angle_guard", "owner": 0, "interval": ["13/32", "27/64"]}
SETTINGS = {"max_live": 64, "min_width": "1/4194304", "hull_limit": 48, "core": "octagon"}
CHILD_DECODED_LIMIT = 512 << 20
CHILD_COMPRESSED_LIMIT = REPORT_LIMIT = 64 << 20


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def identity(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def within(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise IncompleteError("conditional production wall ceiling")


def output_within(encoded: bytes) -> None:
    if len(encoded) > CHILD_DECODED_LIMIT:
        raise IncompleteError("conditional child decoded output ceiling")


def compressed_within(encoded: bytes) -> None:
    if len(encoded) > CHILD_COMPRESSED_LIMIT:
        raise IncompleteError("conditional child compressed output ceiling")


def initial_closure(groups: dict[int, Any]) -> dict[str, Any] | None:
    """Propose the shared pure exact all-hull scan, including points and segments."""
    checker = import_module("devtools.verify_n17_conditional_owned_hull")
    return checker.initial_closure(
        {
            owner: [(as_fraction(x), as_fraction(y)) for x, y in points]
            for owner, points in groups.items()
        }
    )


def guard_closure(rows: list[dict[str, Any]], step: int) -> dict[str, Any] | None:
    """Propose the checked complete closed-guard row-cover terminal."""
    checker = import_module("devtools.verify_n17_conditional_owned_hull")
    return checker.guard_closure(rows, step)


def owner_order(mask: list[int], coarse: int, parent_order: list[int]) -> list[int]:
    require(0 in mask and coarse in mask and coarse != 0, "conditional owner roster")
    require(
        len(parent_order) == 16
        and len(set(parent_order)) == 16
        and set(parent_order) == set(mask) - {coarse},
        "accepted parent full16 contracting roster",
    )
    return [owner for owner in parent_order if owner != 0] + [0]


def prepared_state(prepared: dict[str, Any]) -> tuple[Any, dict[int, Any], dict[int, Any]]:
    require(prepared["constraints"] == [GUARD], "closed conditional guard differs")
    require(
        prepared["parent"] is not None and prepared["guard_source"] is not None,
        "ancestry missing",
    )
    frame = read_frame(prepared["frame"])
    initial = prepared["initial_state"]
    mask = initial["mask"]
    require(mask == sorted(set(mask)) and len(mask) == 17, "full17 initial mask")
    require(
        set(initial["cells"]) == set(initial["groups"]) == set(map(str, mask)),
        "initial owner keys differ",
    )
    groups = {owner: node.points(initial["groups"][str(owner)]) for owner in mask}
    rows = {owner: copy.deepcopy(initial["cells"][str(owner)]) for owner in mask}
    return frame, groups, rows


def child_record(
    prepared: dict[str, Any],
    groups: dict[int, Any],
    rows: dict[int, Any],
    steps: list[dict[str, Any]],
    closure: dict[str, Any] | None,
) -> dict[str, Any]:
    initial = prepared["initial_state"]
    ancestry = {
        "parent": copy.deepcopy(prepared["parent"]),
        "guard_source": copy.deepcopy(prepared["guard_source"]),
        "constraints": copy.deepcopy(prepared["constraints"]),
    }
    source = {"conditional_initial_sha256": identity(initial)}
    return {
        "schema": CHILD_SCHEMA,
        "node_id": "n17-conditional-owned-hull",
        **ancestry,
        "mask_index": None,
        "mask": list(initial["mask"]),
        "U": prepared["frame"]["U"],
        "B": prepared["frame"]["B"],
        "source": source,
        "initial": copy.deepcopy(initial),
        "steps": copy.deepcopy(steps),
        "final_state": {
            "mask_index": None,
            "mask": list(initial["mask"]),
            "U": prepared["frame"]["U"],
            "B": prepared["frame"]["B"],
            **ancestry,
            "guard": copy.deepcopy(GUARD),
            "source": source,
            "world": copy.deepcopy(prepared["frame"]["cells"]),
            "groups": {str(owner): encode(value) for owner, value in groups.items()},
            "cells": {str(owner): copy.deepcopy(value) for owner, value in rows.items()},
        },
        "contradiction": copy.deepcopy(closure),
        "closed": closure is not None,
        "terminal": closure is not None,
        "mask_exclusion_proved": False,
        "conditional_exclusion_proved": False,
        "global_optimality_proved": False,
        "census_admission_proved": False,
    }


def produce(prepared: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    frozen = canonical(prepared)
    started, cpu_start = time.monotonic(), time.process_time()
    frame, groups, rows = prepared_state(prepared)
    mask = prepared["initial_state"]["mask"]
    coarse = prepared["custody"]["label_to_owner"]["6"]
    order = owner_order(mask, coarse, prepared["custody"]["parent_step_owners"])
    steps: list[dict[str, Any]] = []
    updates: list[dict[str, Any]] = []
    require(
        all(len(group) <= SETTINGS["hull_limit"] for group in groups.values()),
        "initial hull ceiling",
    )
    closure = None
    status, error = "production_stall_candidate", None
    try:
        within(deadline)
        proposed_closure = initial_closure(groups)
        within(deadline)
        closure = proposed_closure
        if closure is not None:
            status = "production_closed_candidate"
    except IncompleteError as exc:
        status, error = "incomplete", str(exc)
    cores: dict[Any, Any] = {}
    budget = Budget(deadline, pilot.MAX_EVENTS)
    for owner in [] if closure or status == "incomplete" else order:
        if time.monotonic() >= deadline:
            status, error = "incomplete", "production wall ceiling"
            break
        # Freeze the parent's complete partition. Passing its current live count
        # disables the pilot's optional bisection without changing the 64 ceiling.
        live = sum(bool(row["residual_polygons"]) for row in rows[owner])
        require(live <= SETTINGS["max_live"], "live-row ceiling exceeded")
        before = time.monotonic()
        try:
            step, stats, predicted = pilot.produce_step(
                frame,
                node_id="n17-conditional-owned-hull",
                step_index=len(steps),
                owner=owner,
                mask=mask,
                groups=groups,
                rows=rows,
                cores=cores,
                max_live=live,
                min_width=Q(SETTINGS["min_width"]),
                hull_limit=SETTINGS["hull_limit"],
                core_kind=SETTINGS["core"],
            )
            require(stats["splits"] == 0, "conditional continuation refined rows")
            within(deadline)
            trial_groups, trial_rows = copy.deepcopy(groups), copy.deepcopy(rows)
            checked = pilot.certify_step(
                frame,
                step,
                trial_groups,
                trial_rows,
                node_id="n17-conditional-owned-hull",
                mask=mask,
                budget=budget,
            )
            require(pilot.agree(predicted, trial_rows[owner]), "producer/checker state differs")
            require(
                [row["interval"] for row in rows[owner]]
                == [row["interval"] for row in trial_rows[owner]],
                "conditional update changed the closed partition",
            )
            require(
                all(len(group) <= SETTINGS["hull_limit"] for group in trial_groups.values()),
                "certified owned hull exceeds48; no implicit truncation",
            )
            require(
                all(
                    trial_groups[other] == groups[other] and trial_rows[other] == rows[other]
                    for other in mask
                    if other != owner
                ),
                "certified update altered another owner",
            )
            require(rows[coarse] == trial_rows[coarse], "coarse square6 rows changed")
            proposed_closure = checked["closure"]
            if proposed_closure is None and owner == 0:
                require(len(steps) + 1 == 16, "guard terminal before the owner0-last round")
                proposed_closure = guard_closure(trial_rows[owner], len(steps))
            within(deadline)
            groups, rows = trial_groups, trial_rows
            steps.append(step)
            closure = proposed_closure
            updates.append(
                {
                    "owner": owner,
                    "seconds": time.monotonic() - before,
                    **stats,
                    **checked,
                    "closure": closure,
                }
            )
            if closure is not None:
                status = "production_closed_candidate"
                break
        except IncompleteError as exc:
            status, error = "incomplete", str(exc)
            break
        except RefusalError as exc:
            status, error = "refused", str(exc)
            break
    require(canonical(prepared) == frozen, "prepared parent/guard changed")
    child = child_record(prepared, groups, rows, steps, closure)
    return {
        "schema": SCHEMA,
        "status": status,
        "error": error,
        "settings": dict(SETTINGS),
        "owner_order": order,
        "completed_owner_count": len(steps),
        "complete_round": len(steps) == 16,
        "updates": updates,
        "child": child,
        "child_sha256": identity(child),
        "custody": copy.deepcopy(prepared["custody"]),
        "elapsed_seconds": time.monotonic() - started,
        "cpu_seconds": time.process_time() - cpu_start,
        "endpoint_monitor_used": False,
        "initial_closure_scope": "all finite convex hulls, including points and segments",
        "fresh_conditional_replay_required": True,
        "conditional_exclusion_proved": False,
        "census_admission_proved": False,
        "global_optimality_proved": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--child-output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    checker = import_module("devtools.verify_n17_conditional_owned_hull")
    deadline = time.monotonic() + args.max_seconds
    result: dict[str, Any]
    try:
        raw, document = checker.read_json(args.descriptor)
        require(document["schema"] == DESCRIPTOR_SCHEMA, "conditional descriptor schema")
        prepared = checker.prepare(document, deadline=deadline)
        result = produce(prepared, deadline=deadline)
        require(
            checker.read_json(args.descriptor)[0] == raw, "descriptor changed during production"
        )
        child = result.pop("child")
        encoded = retained_json.dumps(child, sort_keys=True).encode()
        output_within(encoded)
        within(deadline)
        compressed = gzip.compress(encoded, mtime=0)
        compressed_within(compressed)
        within(deadline)
        args.child_output.parent.mkdir(parents=True, exist_ok=True)
        args.child_output.write_bytes(compressed)
        within(deadline)
        result["child_object"] = {
            "path": str(args.child_output),
            "canonical_sha256": identity(child),
            "compressed_sha256": hashlib.sha256(args.child_output.read_bytes()).hexdigest(),
        }
    except (IncompleteError, checker.IncompleteError) as exc:
        result = {"schema": SCHEMA, "status": "incomplete", "error": str(exc)}
    except (ValueError, KeyError, TypeError, OSError) as exc:
        result = {"schema": SCHEMA, "status": "refused", "error": str(exc)}
    result.update(
        conditional_exclusion_proved=False,
        census_admission_proved=False,
        global_optimality_proved=False,
        provenance=provenance(
            Path(__file__),
            Path(pilot.__file__),
            Path(node.__file__),
            Path(__file__).with_name("check_n17_capture_checkpoint.py"),
            Path(__file__).with_name("verify_n17_conditional_owned_hull.py"),
            *sorted(pilot.KERNEL_DIR.glob("*.py")),
        ),
        invocation={
            "argv": list(sys.argv if argv is None else argv),
            "interpreter": sys.executable,
        },
    )
    report = retained_json.dumps(result)
    if len(report.encode()) > REPORT_LIMIT:
        result = {"schema": SCHEMA, "status": "incomplete", "error": "report byte ceiling"}
        report = retained_json.dumps(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report + "\n")
    print(json.dumps({k: result.get(k) for k in ("schema", "status", "error", "child_sha256")}))
    return (
        0
        if result["status"] in {"production_stall_candidate", "production_closed_candidate"}
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
