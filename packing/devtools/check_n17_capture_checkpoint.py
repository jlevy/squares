"""Bind numeric-cap capture inputs before a registered producer run.

This first instrument checks inputs only. It produces no seed, owner update,
checkpoint, leaf bound, terminal result or census admission. Scientific loaders
are lazy so a later producer-free replay entry can remain isolated.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import inspect
import json
import math
import sys
import time
from importlib import import_module
from pathlib import Path
from typing import Any

from devtools import audit_n17_endpoint_receipt as exact
from devtools.provenance import provenance
from sqpack import retained_json
from sqpack.hull_kernel.frame import Frame
from sqpack.hull_kernel.geometry import IncompleteError, trig
from sqpack.hull_kernel.induction import wall_lines
from sqpack.hull_kernel.rational import Q

SCHEMA = "n17-numeric-cap-checkpoint-inputs/v1"
CAP = Q(935106018721, 200000000000)
OUTER = Q(1169, 250)
LABELS = tuple(range(1, 18))
FALSE_FLAGS = {
    "producer_run": False,
    "saved_checkpoint_replayed": False,
    "capture_proved": False,
    "terminal_predicate_checked": False,
    "global_admission": False,
    "existing_objects_relabelled": False,
}


def within(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise IncompleteError("numeric-cap input wall ceiling")


def contained(outer: Any, inner: Any) -> bool:
    a, b = exact.read_interval(outer), exact.read_interval(inner)
    return a[0] <= b[0] <= b[1] <= a[1]


def frame_walls(base: Frame, numeric: Frame, *, bins: int, deadline: float) -> dict[str, Any]:
    exact.require(type(bins) is int and bins == 32, "frozen bins differ")
    exact.require(
        base.capture_cap is None
        and base.cap == OUTER
        and base.length == OUTER
        and base.scale == 1
        and base.occupancy == 17,
        "original full17 frame differs",
    )
    exact.require(
        numeric.name == f"{base.name}-capture"
        and numeric.capture_cap == CAP
        and numeric.cap == base.cap
        and numeric.length == base.length
        and numeric.cells == base.cells
        and numeric.cell_names == base.cell_names
        and numeric.actions == base.actions
        and numeric.occupancy == base.occupancy
        and numeric.core_slack == base.core_slack
        and numeric.provenance == base.provenance,
        "numeric frame custody differs",
    )

    def expected(h: Q) -> tuple[Q, Q]:
        return numeric.scale * ((OUTER - CAP) / 2 + h), numeric.scale * ((OUTER + CAP) / 2 - h)

    exact.require(
        all(numeric.field_centre_bounds(h) == expected(h) for h in (Q(0), Q(1))),
        "numeric affine field-wall coefficients differ",
    )
    prototypes = []
    for index in range(bins):
        within(deadline)
        lo, hi = Q(index, bins), Q(index + 1, bins)
        width = min(sum(trig(t), Q()) for t in (lo, hi))
        low, high = expected(width / 2)
        expected_lines = [
            (Q(1), Q(0), high),
            (Q(-1), Q(0), -low),
            (Q(0), Q(1), high),
            (Q(0), Q(-1), -low),
        ]
        actual = wall_lines(numeric, lo, hi)
        exact.require(actual == expected_lines, "numeric row wall coefficients differ")
        prototypes.append(
            {
                "interval": [str(lo), str(hi)],
                "walls": [[str(value) for value in line] for line in actual],
            }
        )
    return {
        "U": str(OUTER),
        "L": str(numeric.length),
        "B": str(numeric.scale),
        "capture_cap": str(CAP),
        "name": numeric.name,
        "affine_formula": "B*((U-Uprime)/2+h), B*((U+Uprime)/2-h)",
        "row_prototypes": prototypes,
        "seed_generated": False,
    }


def scientific_modules() -> tuple[Any, Any, Any]:
    """Delay modules that import the producer until input-control execution."""
    return (
        import_module("devtools.check_n17_capture_cap"),
        import_module("devtools.check_n17_endpoint_prefix"),
        import_module("devtools.pilot_n17_capture"),
    )


def load_context(
    root_path: Path, cap_path: Path, geometry_path: Path, deadline: float
) -> dict[str, Any]:
    # Only registered control execution calls these scientific loaders.
    cap, prefix, pilot = scientific_modules()

    within(deadline)
    root_raw = exact.read_bytes(root_path)
    geometry_raw = exact.read_bytes(geometry_path)
    cap_raw = exact.read_bytes(cap_path)
    cap_document = exact.decode(cap_raw)
    checked_cap = cap.check(cap_document, root_path)
    exact.require(
        checked_cap["verification_passed"] and checked_cap["cap_certified"],
        "fresh cap prerequisite refused",
    )
    within(deadline)
    root_document = exact.decode(root_raw)
    root_checked = cap.root_loader.root.check(
        root_document, exact.read_bytes(exact.REPO / cap.root_loader.root.SOURCE_PATH)
    )
    exact.require(root_checked["verification_passed"], "fresh root prerequisite refused")
    geometry_document = exact.decode(geometry_raw)
    exact.require(geometry_document["criterion_passed"] is True, "endpoint geometry refused")
    expected_box = {
        "midpoint": root_document["box"]["midpoint"],
        "inclusion_bounds": root_checked["inclusion_bounds"],
    }
    exact.require(
        exact.exact_structure(geometry_document["geometry"]["box"], expected_box),
        "exp238/root exact box binding differs",
    )
    exact.require(
        geometry_path.resolve() == pilot.cover.CERTIFICATE.resolve(),
        "pilot reads a different geometry source",
    )
    within(deadline)
    base = pilot.capture_frame(None)
    endpoint = pilot.load_endpoint(base)
    numeric = pilot.capture_frame(endpoint.capture_cap)
    within(deadline)
    endpoint_frame, poses, endpoint_inputs = prefix.load_endpoint()
    exact.require(endpoint_frame == base, "independent endpoint frame differs")
    exact.require(
        geometry_raw == exact.read_bytes(geometry_path)
        and root_raw == exact.read_bytes(root_path)
        and cap_raw == exact.read_bytes(cap_path),
        "input changed across loading",
    )
    return {
        "root": cap_document["inputs"],
        "root_box": expected_box,
        "cap_check": checked_cap,
        "base": base,
        "numeric": numeric,
        "endpoint": endpoint,
        "poses": poses,
        "endpoint_inputs": endpoint_inputs,
        "source_bytes": {
            "root": hashlib.sha256(root_raw).hexdigest(),
            "geometry": hashlib.sha256(geometry_raw).hexdigest(),
            "cap_certificate": hashlib.sha256(cap_raw).hexdigest(),
        },
    }


def input_packet(context: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    within(deadline)
    endpoint, poses = context["endpoint"], context["poses"]
    root = context["root"]
    exact.require(
        context["cap_check"]["verification_passed"] is True
        and context["cap_check"]["cap_certified"] is True
        and root["root_verification_passed"] is True,
        "fresh root/cap prerequisite refused",
    )
    exact.require(
        exact.exact_structure(context["endpoint_inputs"]["root"], root),
        "full-root endpoint custody differs",
    )
    exact.require(endpoint.capture_cap == CAP, "pilot cap differs from accepted frozen cap")
    exact.require(
        endpoint.coarse == 6 and endpoint.system == "n17" and endpoint.scale == 1,
        "pilot system or coarse-owner scope differs",
    )
    for key, interval in zip(("t_box", "b_box"), root["root_inclusion_box_used"], strict=True):
        exact.require(
            contained(endpoint.provenance[key], interval), "pilot root enclosure too narrow"
        )
    exact.require(
        CAP - endpoint.side.hi > 0 and CAP - endpoint.side.lo <= Q(1, 10**12),
        "pilot own side all-root excess fails",
    )
    targets = {target.label: target for target in endpoint.targets}
    exact.require(
        tuple(sorted(targets)) == LABELS
        and len(endpoint.targets) == 17
        and len({target.owner for target in endpoint.targets}) == 17
        and all(
            type(t.owner) is int and 0 <= t.owner < len(context["base"].cells)
            for t in endpoint.targets
        ),
        "full17 pilot target roster differs",
    )
    exact.require(
        tuple(sorted(pose.label for pose in poses)) == LABELS,
        "full17 independent endpoint roster differs",
    )
    roster = []
    for pose in poses:
        within(deadline)
        target = targets[pose.label]
        exact.require(
            target.owner == pose.owner
            and target.cell == context["base"].cell_names[pose.owner],
            "endpoint label/owner/cell mapping differs",
        )
        exact.require(
            all(
                a.lo <= b.lo <= b.hi <= a.hi
                for a, b in zip(target.centre, pose.centre, strict=True)
            )
            and all(
                any(lo <= a <= b <= hi for lo, hi in target.charts) for a, b in pose.charts
            ),
            "pilot pose does not contain full accepted-root pose",
        )
        roster.append(
            {
                "label": pose.label,
                "owner": pose.owner,
                "cell": target.cell,
                "centre": [[str(v.lo), str(v.hi)] for v in pose.centre],
                "charts": [[str(a), str(b)] for a, b in pose.charts],
            }
        )
    exact.require(targets[6].cell == "side-S2", "square6 cell differs")
    frame = frame_walls(context["base"], context["numeric"], bins=32, deadline=deadline)
    return {
        "schema": SCHEMA,
        "input_join_passed": True,
        "status": "numeric_cap_inputs_checked",
        "root": copy.deepcopy(root),
        "root_box": copy.deepcopy(context["root_box"]),
        "source_bytes": dict(context["source_bytes"]),
        "fresh_cap_check": copy.deepcopy(context["cap_check"]),
        "pilot_root_boxes": {k: list(endpoint.provenance[k]) for k in ("t_box", "b_box")},
        "pilot_side": [str(endpoint.side.lo), str(endpoint.side.hi)],
        "frame": frame,
        "endpoint_roster": roster,
        "state": sorted(t.owner for t in endpoint.targets),
        "row_wall_prototypes_checked": 32,
        "prospective_owner_seed_rows": 17 * 32,
        "actual_seed_rows_checked": 0,
        "scope": "numeric-cap input control only; no production or saved-node acceptance",
        **FALSE_FLAGS,
    }


def main(argv: list[str] | None = None) -> int:
    cap, prefix, pilot = scientific_modules()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=cap.root_loader.ROOT_PATH)
    parser.add_argument("--cap-certificate", type=Path, required=True)
    parser.add_argument("--geometry", type=Path, default=pilot.cover.CERTIFICATE)
    parser.add_argument("--max-seconds", type=float, default=60)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        exact.require(
            math.isfinite(args.max_seconds) and args.max_seconds > 0, "invalid wall ceiling"
        )
        deadline = time.monotonic() + args.max_seconds
        packet = input_packet(
            load_context(args.root, args.cap_certificate, args.geometry, deadline),
            deadline=deadline,
        )
        packet["execution"] = {
            "argv": list(argv) if argv is not None else sys.argv[1:],
            "max_seconds": args.max_seconds,
            "python": sys.version,
        }
        packet["provenance"] = provenance(
            Path(__file__),
            Path(cap.__file__),
            Path(pilot.__file__),
            Path(prefix.__file__),
            Path(cap.root_loader.__file__),
            Path(cap.root_loader.root.__file__),
            Path(pilot.cover.__file__),
            Path(exact.__file__),
            Path(inspect.getfile(Frame)),
            Path(inspect.getfile(wall_lines)),
            Path(inspect.getfile(trig)),
        )
    except IncompleteError as error:
        packet = {
            "schema": SCHEMA,
            "status": "incomplete",
            "input_join_passed": False,
            "error": str(error),
            **FALSE_FLAGS,
        }
    except (ValueError, OSError, KeyError, TypeError, IndexError) as error:
        packet = {
            "schema": SCHEMA,
            "status": "refused",
            "input_join_passed": False,
            "error": str(error),
            **FALSE_FLAGS,
        }
    args.output.write_text(retained_json.dumps(packet))
    print(
        json.dumps(
            {k: v for k, v in packet.items() if k in {"status", "input_join_passed", "error"}}
        )
    )
    return 0 if packet["input_join_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
