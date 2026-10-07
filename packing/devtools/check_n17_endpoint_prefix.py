"""Retain and replay a bounded full-17 exact endpoint-preservation control.

Current producer logic is observed through its StepLog interface. Each complete owner
step is independently checked before its prefix is retained. All seventeen exact-root
poses must remain in accepted closed row domains after seed and every accepted update.
A new interpreter replays the saved prefix without importing the producer. Nothing in
this readiness control admits an exclusion, a capture tree or a census change.
Importing the module reads no scientific inputs.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devtools import audit_n17_endpoint_receipt as exact
from devtools import check_hull_kernel_mask0 as mask0
from devtools import check_n17_capacity_one_cover as cover
from devtools import check_n17_endpoint_feasibility as endpoint_geometry
from devtools import check_n17_subpattern as saved
from devtools import check_n17_widened_features as forcing
from devtools import pilot_n17_capture as pilot
from devtools.check_n17_endpoint_feasibility import THETA_LABELS, Box
from devtools.provenance import provenance
from sqpack import retained_json
from sqpack.hull_kernel import frame as frame_geometry
from sqpack.hull_kernel import geometry, induction, node, producer, sequential
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import (
    Budget,
    IncompleteError,
    Polygon,
    RefusalError,
    intersect,
    require,
)
from sqpack.hull_kernel.induction import encode, same, wall_lines
from sqpack.hull_kernel.rational import Q

SCHEMA = "n17-endpoint-prefix-control/v1"
LABELS = tuple(range(1, 18))
SETTINGS: dict[str, Any] = {
    "bins": 64,
    "max_rounds": 24,
    "hull_limit": 16,
    "core": "envelope",
    "split": {"floor": 512, "max_rows": 1152, "patience": 1},
}
NODE_ID = "n17-full-endpoint-readiness-prefix"


@dataclass(frozen=True)
class EndpointPose:
    label: int
    owner: int
    centre: tuple[Box, Box]
    charts: tuple[tuple[Q, Q], ...]


class PrefixStopError(Exception):
    """A declared prefix boundary; retained complete steps remain independently replayable."""


def endpoint_witness(
    pose: EndpointPose, rows: Sequence[Mapping[str, Any]]
) -> dict[str, Any] | None:
    corners = [
        (Q(x), Q(y))
        for x in (pose.centre[0].lo, pose.centre[0].hi)
        for y in (pose.centre[1].lo, pose.centre[1].hi)
    ]
    for index, row in enumerate(rows):
        lo, hi = (Q(value) for value in row["interval"])
        if not any(lo <= low <= high <= hi for low, high in pose.charts):
            continue
        for piece, polygon in enumerate(row["residual_polygons"]):
            if all(pilot.in_convex(node.points(polygon), corner) for corner in corners):
                return {
                    "row": index,
                    "piece": piece,
                    "reference": row["reference"],
                    "interval": list(row["interval"]),
                }
    return None


def endpoint_check(
    poses: tuple[EndpointPose, ...], rows: Mapping[int, Sequence[Mapping[str, Any]]]
) -> dict[str, Any]:
    require(
        tuple(sorted(pose.label for pose in poses)) == LABELS
        and len({pose.owner for pose in poses}) == 17
        and set(rows) == {pose.owner for pose in poses},
        "full seventeen endpoint/owner roster required",
    )
    witnesses = [
        {
            "label": pose.label,
            "owner": pose.owner,
            "witness": endpoint_witness(pose, rows[pose.owner]),
        }
        for pose in sorted(poses, key=lambda value: value.label)
    ]
    lost = [entry["label"] for entry in witnesses if entry["witness"] is None]
    return {"held": not lost, "lost_labels": lost, "owners": witnesses}


def load_endpoint() -> tuple[Frame, tuple[EndpointPose, ...], dict[str, Any]]:
    frame = mask0.n17_unique_frame()
    require(
        str(frame.cap) == "1169/250" and frame.scale == 1 and frame.capture_cap is None,
        "endpoint control frame/cap changed",
    )
    root_inputs, _, _ = forcing.load_root()
    t, beta = (
        Box(*exact.read_interval(value)) for value in root_inputs["root_inclusion_box_used"]
    )
    endpoint = cover.endpoint(t, beta)
    cells = cover.build_cover(cover.UNIQUE_24)
    require(
        tuple(cell.name for cell in cells) == frame.cell_names
        and all(
            same([(Q(x), Q(y)) for x, y in cell.vertices], frame.cell(i))
            for i, cell in enumerate(cells)
        ),
        "endpoint cover/frame geometry changed",
    )
    assignment = cover.family_state(cells, endpoint, cover.ENDPOINT)
    require(assignment["one_state"], "endpoint has no supported named state")
    owners = {
        item["label"]: frame.cell_names.index(item["cell"]) for item in assignment["squares"]
    }
    sixteen = (Q((1 - beta.hi) / (1 + beta.hi)), Q((1 - beta.lo) / (1 + beta.lo)))
    poses = tuple(
        EndpointPose(
            label,
            owners[label],
            endpoint.centres[label - 1],
            ((Q(t.lo), Q(t.hi)),)
            if label in THETA_LABELS
            else (sixteen,)
            if label == 16
            else ((Q(0), Q(0)), (Q(1), Q(1))),
        )
        for label in LABELS
    )
    require(len({pose.owner for pose in poses}) == 17, "endpoint assignment is not bijective")
    return (
        frame,
        poses,
        {
            "root": root_inputs,
            "frame": frame.name,
            "cap": str(frame.cap),
            "B": str(frame.scale),
            "state_encoding": "sorted-cell-indices/v1",
            "state": sorted(owners.values()),
            "label_to_owner": {str(label): owner for label, owner in owners.items()},
            "cells": [frame.cell_names[owner] for owner in sorted(owners.values())],
            "endpoint_poses": [
                {
                    "label": pose.label,
                    "owner": pose.owner,
                    "centre": [value.as_json() for value in pose.centre],
                    "charts": [[str(lo), str(hi)] for lo, hi in pose.charts],
                }
                for pose in poses
            ],
        },
    )


def seed_from_first_step(
    frame: Frame, mask: list[int], step: Mapping[str, Any]
) -> dict[str, Any]:
    """Reconstruct the exact initial wall rows; initial owned points come from the step."""
    cells = {}
    for owner in mask:
        rows = []
        for index in range(SETTINGS["bins"]):
            lo, hi = Q(index, SETTINGS["bins"]), Q(index + 1, SETTINGS["bins"])
            domain = intersect(frame.world(owner), wall_lines(frame, lo, hi))
            rows.append(
                {
                    "interval": [str(lo), str(hi)],
                    "residual_polygons": [encode(domain)] if domain else [],
                    "outer_domain": encode(domain),
                    "outer_bounds": [],
                    "reference": {"kind": "wall_seed", "owner": owner, "row": index},
                }
            )
        cells[str(owner)] = rows
    return {
        "schema": "generic_wall_seed_v1",
        "mask_index": None,
        "mask": mask,
        "U": str(frame.cap),
        "B": str(frame.scale),
        "bins": SETTINGS["bins"],
        "groups": dict(step["prior_owned_hulls"]),
        "cells": cells,
        "world": [encode(frame.world(i)) for i in range(len(frame.cells))],
    }


class PrefixMonitor:
    """Independent acceptance at the current producer's complete-step append boundary."""

    def __init__(
        self,
        frame: Frame,
        poses: tuple[EndpointPose, ...],
        directory: Path,
        deadline: float,
        max_updates: int | None,
    ) -> None:
        self.frame, self.poses = frame, poses
        self.mask = sorted(pose.owner for pose in poses)
        self.budget = Budget(deadline, 200000)
        self.max_updates = max_updates
        self.steps = saved.SpilledSteps(directory / ".accepted-prefix-steps.json.gz")
        self.seed: dict[str, Any] | None = None
        self.groups: dict[int, Polygon] = {}
        self.rows: dict[int, list[dict[str, Any]]] = {}
        self.endpoint_checks: list[dict[str, Any]] = []
        self.step_checks: list[dict[str, Any]] = []
        self.closure: dict[str, Any] | None = None

    def __len__(self) -> int:
        return len(self.steps)

    def append(self, step: dict[str, Any], /) -> None:
        require(
            step["index"] == len(self) and step["complete"] is True,
            "prefix owner step is not complete/ordered",
        )
        node.remaining(self.budget)
        if self.seed is None:
            self.seed = seed_from_first_step(self.frame, self.mask, step)
            admitted = node.admit_seed(
                self.frame,
                self.seed,
                mask=self.mask,
                bins=SETTINGS["bins"],
                budget=self.budget,
                allow_empty_groups=True,
            )
            self.groups = dict(admitted.groups)
            self.rows = {owner: list(rows) for owner, rows in admitted.rows.items()}
            control = {"phase": "seed", **endpoint_check(self.poses, self.rows)}
            self.endpoint_checks.append(control)
            if not control["held"]:
                raise PrefixStopError("endpoint_lost_at_seed")
        next_groups, next_rows = dict(self.groups), dict(self.rows)
        checked = pilot.certify_step(
            self.frame,
            step,
            next_groups,
            next_rows,
            node_id=NODE_ID,
            mask=self.mask,
            budget=self.budget,
        )
        self.groups, self.rows = next_groups, next_rows
        self.steps.append(step)
        self.step_checks.append({"index": step["index"], "owner": step["owner"], **checked})
        self.closure = checked["closure"]
        control = {
            "phase": "owner_update",
            "step": step["index"],
            **endpoint_check(self.poses, self.rows),
        }
        self.endpoint_checks.append(control)
        if not control["held"]:
            raise PrefixStopError("endpoint_lost_after_update")
        if self.closure is not None:
            raise PrefixStopError("unexpected_endpoint_closure")
        if self.max_updates is not None and len(self) >= self.max_updates:
            raise PrefixStopError("declared_update_prefix")

    def node_object(self) -> dict[str, Any]:
        require(
            self.seed is not None and len(self) > 0, "no accepted complete prefix to retain"
        )
        assert self.seed is not None
        source = {"sha256": saved.content_sha256(self.seed)}
        common = {
            "mask_index": None,
            "mask": self.mask,
            "U": str(self.frame.cap),
            "B": str(self.frame.scale),
            "constraints": [],
            "guard_source": None,
            "source": source,
        }
        return {
            "schema": "exact_generic_owned_hull_v1",
            "node_id": NODE_ID,
            "parent": None,
            **common,
            "initial": {
                "groups": self.seed["groups"],
                "cell_references": {
                    str(owner): [row["reference"] for row in self.seed["cells"][str(owner)]]
                    for owner in self.mask
                },
            },
            "steps": self.steps,
            "final_state": {
                **common,
                "guard": {},
                "world": self.seed["world"],
                "groups": {str(owner): encode(self.groups[owner]) for owner in self.mask},
                "cells": {str(owner): self.rows[owner] for owner in self.mask},
            },
            "contradiction": self.closure,
            "closed": self.closure is not None,
            "terminal": self.closure is not None,
            "mask_exclusion_proved": False,
            "global_optimality_proved": False,
        }


def fresh_replay(directory: Path, output: Path, seconds: float) -> dict[str, Any]:
    command = [
        sys.executable,
        "-m",
        "devtools.check_n17_subpattern",
        "--check-saved",
        str(directory),
        "--cover",
        "indexed",
        "--max-seconds",
        str(seconds),
        "--output",
        str(output),
    ]
    try:
        completed = subprocess.run(
            command, capture_output=True, text=True, timeout=seconds, check=False
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "INCOMPLETE",
            "reason": "fresh full replay process ceiling",
            "command": command,
        }
    if not output.is_file():
        return {
            "status": "REFUSED",
            "reason": "fresh full replay produced no receipt",
            "exit_code": completed.returncode,
            "stderr": completed.stderr[-4000:],
            "command": command,
        }
    result = json.loads(output.read_text())
    return {"command": command, "exit_code": completed.returncode, "receipt": result}


def run(
    directory: Path,
    *,
    prefix_seconds: float = 120,
    replay_seconds: float = 60,
    max_updates: int = 1,
) -> dict[str, Any]:
    require(
        all(math.isfinite(value) and value > 0 for value in (prefix_seconds, replay_seconds))
        and type(max_updates) is int
        and max_updates == 1,
        "invalid prefix/replay budget or changed first-update criterion",
    )
    require(not directory.exists(), "prefix objects need a new unique directory")
    directory.mkdir(parents=True)
    started = time.monotonic()
    frame, poses, inputs = load_endpoint()
    monitor = PrefixMonitor(frame, poses, directory, started + prefix_seconds, max_updates)
    outcome, refusal = "producer_returned", None
    try:
        production = producer.produce(
            frame,
            monitor.mask,
            bins=SETTINGS["bins"],
            max_rounds=SETTINGS["max_rounds"],
            budget=monitor.budget,
            node_id=NODE_ID,
            collision=True,
            hull_limit=SETTINGS["hull_limit"],
            stop_at=monitor.budget.deadline,
            core=SETTINGS["core"],
            split=producer.SplitPolicy(**SETTINGS["split"]),
            step_log=monitor,
        )
        outcome = production.outcome
        if len(monitor):
            require(
                monitor.seed is not None
                and saved.content_sha256(production.seed)
                == saved.content_sha256(monitor.seed),
                "observed producer seed differs from admitted prefix seed",
            )
            node.admit_final_state(
                frame, production.node, monitor.groups, monitor.rows, mask=monitor.mask
            )
        else:
            require(
                not production.node["steps"], "producer returned unobserved complete updates"
            )
    except PrefixStopError as error:
        outcome = str(error)
    except IncompleteError as error:
        outcome, refusal = "prefix_incomplete", str(error)
    except (RefusalError, ValueError, KeyError, TypeError, IndexError) as error:
        outcome, refusal = "prefix_refused", str(error)
    replay, seed_sha, node_sha = None, None, None
    if monitor.seed is not None and len(monitor):
        prefix = monitor.node_object()
        saved.save_certificate(directory, monitor.seed, prefix)
        seed_sha, node_sha = saved.content_sha256(monitor.seed), saved.content_sha256(prefix)
        replay = fresh_replay(directory, directory / "fresh-full-replay.json", replay_seconds)
    receipt = replay.get("receipt", {}) if replay else {}
    endpoint_held = bool(monitor.endpoint_checks) and all(
        item["held"] for item in monitor.endpoint_checks
    )
    replayed = (
        receipt.get("status") == "PASS_SAVED_STALL"
        and replay is not None
        and replay.get("exit_code") == 0
        and receipt.get("producer_imported") is False
        and receipt.get("closure") is None
        and receipt.get("node_sha256") == node_sha
        and receipt.get("seed_sha256") == seed_sha
        and receipt.get("steps_checked") == len(monitor)
        and receipt.get("mask") == monitor.mask
        and receipt.get("bins") == SETTINGS["bins"]
        and receipt.get("cover_backend") == "indexed"
        and receipt.get("frame") == frame.name
        and set(receipt.get("cells", [])) == set(inputs["cells"])
    )
    replay_incomplete = replay is not None and (
        replay.get("status") == "INCOMPLETE" or receipt.get("status") == "INCOMPLETE"
    )
    replay_refused = replay is not None and not replayed and not replay_incomplete
    passed = (
        endpoint_held
        and len(monitor) >= 1
        and monitor.closure is None
        and replayed
        and outcome
        not in {
            "prefix_refused",
            "endpoint_lost_at_seed",
            "endpoint_lost_after_update",
            "unexpected_endpoint_closure",
        }
    )
    return {
        "schema": SCHEMA,
        "status": "PASS_ENDPOINT_PREFIX"
        if passed
        else "REFUSED_ENDPOINT_CONTROL"
        if (monitor.endpoint_checks and not endpoint_held)
        or monitor.closure is not None
        or outcome == "prefix_refused"
        or replay_refused
        else "INCOMPLETE",
        "control_passed": passed,
        "inputs": inputs,
        "settings": SETTINGS,
        "prefix_seconds": prefix_seconds,
        "replay_seconds": replay_seconds,
        "checker_event_ceiling": monitor.budget.max_nodes,
        "max_updates": max_updates,
        "prefix_outcome": outcome,
        "refusal": refusal,
        "complete_owner_updates": len(monitor),
        "endpoint_checks": monitor.endpoint_checks,
        "step_checks": monitor.step_checks,
        "seed_sha256": seed_sha,
        "node_sha256": node_sha,
        "fresh_full_replay": replay,
        "replay_refused": replay_refused,
        "closure": monitor.closure,
        "global_admission_proved": False,
        "capture_tree_proved": False,
        "excluded_orbits": 0,
        "wall_seconds": time.monotonic() - started,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objects", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prefix-seconds", type=float, default=120)
    parser.add_argument("--replay-seconds", type=float, default=60)
    parser.add_argument("--max-updates", type=int, default=1)
    args = parser.parse_args(argv)
    try:
        result = run(
            args.objects,
            prefix_seconds=args.prefix_seconds,
            replay_seconds=args.replay_seconds,
            max_updates=args.max_updates,
        )
    except (ValueError, OSError, KeyError, TypeError, IndexError, IncompleteError) as error:
        result = {
            "schema": SCHEMA,
            "status": "INCOMPLETE" if isinstance(error, IncompleteError) else "REFUSED",
            "control_passed": False,
            "reason": str(error),
            "excluded_orbits": 0,
            "global_admission_proved": False,
            "capture_tree_proved": False,
        }
    result["provenance"] = provenance(
        Path(__file__),
        Path(producer.__file__),
        Path(pilot.__file__),
        Path(node.__file__),
        Path(saved.__file__),
        Path(forcing.__file__),
        Path(forcing.root.__file__),
        Path(exact.__file__),
        Path(cover.__file__),
        Path(endpoint_geometry.__file__),
        Path(frame_geometry.__file__),
        Path(geometry.__file__),
        Path(induction.__file__),
        Path(sequential.__file__),
    )
    result["execution"] = {
        "argv": list(argv) if argv is not None else sys.argv[1:],
        "interpreter": sys.executable,
        "objects": str(args.objects.resolve()),
        "output": str(args.output.resolve()),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(retained_json.dumps(result))
    print(
        json.dumps(
            {
                key: result.get(key)
                for key in (
                    "status",
                    "control_passed",
                    "complete_owner_updates",
                    "prefix_outcome",
                    "refusal",
                    "reason",
                )
            }
        )
    )
    return 0 if result["control_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
