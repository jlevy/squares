"""Bind numeric-cap inputs or consume an independently replayed saved checkpoint.

The default input mode produces no seed or leaf bound. Checkpoint mode checks
conditional leaf readiness; its clean child replays the supplied exact Frame
without importing the producer. Neither mode admits a state to the census.
"""

from __future__ import annotations

import argparse
import codecs
import copy
import gzip
import hashlib
import inspect
import json
import math
import subprocess
import sys
import tempfile
import time
from importlib import import_module
from pathlib import Path
from typing import Any, cast

from devtools import audit_n17_endpoint_receipt as exact
from devtools.provenance import provenance
from sqpack import retained_json
from sqpack.hull_kernel.frame import Frame, make_frame
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
CHECKPOINT_SCHEMA = "n17-numeric-cap-checkpoint/v1"
SEED_LIMIT = 10 << 20
NODE_COMPRESSED_LIMIT = 512 << 20
NODE_DECODED_LIMIT = 2 << 30
OUTPUT_LIMIT = 64 << 20
EVENT_LIMIT = 200000
LIMITS = {
    "seed_bytes": SEED_LIMIT,
    "node_bytes": NODE_COMPRESSED_LIMIT,
    "decoded_node_bytes": NODE_DECODED_LIMIT,
    "output_bytes": OUTPUT_LIMIT,
}


def retained_path(value: Any) -> Path:
    exact.require(type(value) is str and not Path(value).is_absolute(), "invalid retained path")
    path = (exact.REPO / value).resolve()
    exact.require(path.is_relative_to(exact.REPO), "retained path escapes repository")
    return path


def frame_record(frame: Frame) -> dict[str, Any]:
    return {
        "name": frame.name,
        "U": str(frame.cap),
        "L": str(frame.length),
        "B": str(frame.scale),
        "capture_cap": str(frame.capture_cap),
        "cells": [[[str(x), str(y)] for x, y in cell] for cell in frame.cells],
        "cell_names": list(frame.cell_names),
        "occupancy": frame.occupancy,
        "actions": [
            {"name": a.name, "matrix": list(a.matrix), "permutation": list(a.permutation)}
            for a in frame.actions
        ],
        "core_slack": str(frame.core_slack),
        "provenance": frame.provenance,
    }


def read_frame(record: dict[str, Any]) -> Frame:
    # This clean reconstruction proves only the supplied exact frame. Parent mode
    # additionally binds it to the freshly accepted 24-cell/root/cap context.
    frame = make_frame(
        name=record["name"],
        cap=Q(exact.rational(record["U"])),
        length=Q(exact.rational(record["L"])),
        cells=[
            [(Q(exact.rational(x)), Q(exact.rational(y))) for x, y in cell]
            for cell in record["cells"]
        ],
        cell_names=record["cell_names"],
        occupancy=record["occupancy"],
        action_names=[a["name"] for a in record["actions"]],
        core_slack=Q(exact.rational(record["core_slack"])),
        provenance=record["provenance"],
        capture_cap=Q(exact.rational(record["capture_cap"])),
    )
    exact.require(
        exact.exact_structure(frame_record(frame), record), "serialized numeric frame differs"
    )
    exact.require(
        frame.scale == 1 and frame.occupancy == 17 and 0 < frame.inner_cap <= frame.cap,
        "unsupported numeric replay frame",
    )
    return frame


def bounded_gzip(path: Path, limit: int, *, deadline: float, retain: bool = False) -> bytes:
    pieces, count = [], 0
    with gzip.open(path, "rb") as stream:
        while True:
            within(deadline)
            chunk = stream.read(min(1 << 20, limit - count + 1))
            if not chunk:
                break
            count += len(chunk)
            if count > limit:
                raise IncompleteError("saved-object decoded byte ceiling")
            if retain:
                pieces.append(chunk)
    return b"".join(pieces)


def compressed_digest(path: Path, limit: int, *, deadline: float) -> str:
    digest, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        while True:
            within(deadline)
            chunk = stream.read(min(1 << 20, limit - count + 1))
            if not chunk:
                return digest.hexdigest()
            count += len(chunk)
            if count > limit:
                raise IncompleteError("saved-object compressed byte ceiling")
            digest.update(chunk)


def bounded_node(saved: Any, path: Path, limit: int, *, deadline: float) -> tuple[Any, Any]:
    # Keep the existing streaming grammar/canonical EOF identity, enforcing the
    # decoded ceiling again during the replay rather than trusting a prior pass.
    def pieces() -> Any:
        decoder, count = codecs.getincrementaldecoder("utf-8")(), 0
        with gzip.open(path, "rb") as stream:
            while True:
                within(deadline)
                chunk = stream.read(min(saved.STREAM_CHUNK, limit - count + 1))
                if not chunk:
                    break
                count += len(chunk)
                if count > limit:
                    raise IncompleteError("saved-node streaming decoded byte ceiling")
                yield decoder.decode(chunk)
        yield decoder.decode(b"", final=True)

    text = saved.GzipJsonText(path)
    text._pieces = pieces()  # noqa: SLF001 — bounded input for the retained streaming parser.
    text.take("{", "a saved node is a JSON object")
    header: dict[str, Any] = {}
    if text.peek() != "}":
        while True:
            name = saved._member_name(text, header)  # noqa: SLF001 — preserve duplicate grammar.
            if name == "steps":
                text.take("[", "a node's steps are an array")
                steps = saved.SavedSteps(text, header)
                header[name] = steps
                return header, steps
            header[name] = text.value()
            if text.take(",}", "a node's members are separated by commas") == "}":
                break
    raise ValueError("the saved node has no steps")


def output_within(report: dict[str, Any], limit: int) -> None:
    if len(retained_json.dumps(report).encode()) > limit:
        raise IncompleteError("checkpoint output byte ceiling")


def saved_replay(
    document: dict[str, Any],
    frame: Frame,
    *,
    deadline: float,
    limits: dict[str, int] | None = None,
) -> tuple[Any, dict[str, Any]]:
    limits = dict(LIMITS) if limits is None else limits
    exact.require(
        document["schema"] == CHECKPOINT_SCHEMA and document["action"] == "r0",
        "saved descriptor schema/action differs",
    )
    saved = import_module("devtools.check_n17_subpattern")
    node = import_module("sqpack.hull_kernel.node")
    sequential = import_module("sqpack.hull_kernel.sequential")
    geometry = import_module("sqpack.hull_kernel.geometry")
    directory = retained_path(document["saved_objects"])
    seed_path, node_path = saved.saved_files(directory)
    within(deadline)
    if (
        seed_path.stat().st_size > limits["seed_bytes"]
        or node_path.stat().st_size > limits["node_bytes"]
    ):
        raise IncompleteError("saved-object compressed byte ceiling")
    compressed_limits = {seed_path: limits["seed_bytes"], node_path: limits["node_bytes"]}
    frozen = {
        path: compressed_digest(path, ceiling, deadline=deadline)
        for path, ceiling in compressed_limits.items()
    }
    seed_packet = exact.decode(
        bounded_gzip(seed_path, limits["seed_bytes"], deadline=deadline, retain=True)
    )
    bounded_gzip(node_path, limits["decoded_node_bytes"], deadline=deadline)
    seed_id = saved.content_sha256(seed_packet)
    exact.require(seed_id == document["seed_sha256"], "saved seed identity differs")
    state, roles, step_owners = (
        document["state"],
        document["label_to_owner"],
        document["step_owners"],
    )
    exact.require(
        type(state) is list
        and len(state) == 17
        and all(type(i) is int and 0 <= i < len(frame.cells) for i in state)
        and state == sorted(set(state)),
        "full17 saved state differs",
    )
    state = cast(list[int], state)
    exact.require(
        set(roles) == set(map(str, LABELS))
        and all(type(i) is int for i in roles.values())
        and set(roles.values()) == set(state)
        and len(step_owners) == 16
        and set(step_owners) == set(state) - {roles["6"]}
        and all(type(i) is int for i in step_owners),
        "saved step/owner roster differs",
    )
    exact.require(seed_packet["bins"] == 32, "saved seed bins differ")
    packet, steps = bounded_node(
        saved, node_path, limits["decoded_node_bytes"], deadline=deadline
    )
    exact.require(
        packet.get("parent") is None
        and packet.get("guard_source") is None
        and packet.get("constraints") == [],
        "unsupported saved ancestry or guard",
    )
    budget = geometry.Budget(deadline, EVENT_LIMIT)
    admitted = node.admit_seed(
        frame, seed_packet, mask=state, bins=32, budget=budget, allow_empty_groups=True
    )
    # admit_seed checks every actual legal wall row and full world/owner inventory.
    trace = sequential.replay_sequential(
        frame, packet, admitted, mask=state, seed_sha256=seed_id, budget=budget, cover="indexed"
    )
    exact.require(
        steps.content_sha256 == document["node_sha256"]
        and [s["owner"] for s in trace.steps] == step_owners
        and trace.closure is None,
        "saved EOF identity, step order or closure differs",
    )
    for path in (seed_path, node_path):
        within(deadline)
        exact.require(
            compressed_digest(path, compressed_limits[path], deadline=deadline) == frozen[path],
            "saved compressed objects changed",
        )
    return trace, {
        "status": "PASS_SAVED_STALL",
        "frame": frame_record(frame),
        "mask": state,
        "cells": [frame.cell_names[i] for i in state],
        "bins": 32,
        "step_owners": step_owners,
        "steps_checked": len(trace.steps),
        "actual_seed_rows_checked": 17 * 32,
        "seed_sha256": seed_id,
        "node_sha256": steps.content_sha256,
        "closure": None,
        "cover_backend": "indexed",
        "compressed_object_sha256": {
            str(p.relative_to(exact.REPO)): digest for p, digest in frozen.items()
        },
        "scope": "complete supplied-Frame replay; parent binds accepted root/cap",
        "root_cap_independently_checked": False,
        "producer_imported": saved.PRODUCER in sys.modules,
        "limits": dict(limits),
        "checker_event_ceiling": EVENT_LIMIT,
        "python": sys.version,
        "executable": sys.executable,
    }


def fresh_child(
    document_path: Path, *, seconds: float, limits: dict[str, int]
) -> dict[str, Any]:
    exact.require(math.isfinite(seconds) and seconds > 0, "invalid fresh child lease")
    command = [
        sys.executable,
        "-m",
        "devtools.check_n17_capture_checkpoint",
        "--fresh-saved",
        str(document_path),
        "--max-seconds",
        str(seconds),
    ]
    for name, value in limits.items():
        command += ["--max-" + name.replace("_", "-"), str(value)]
    with tempfile.TemporaryDirectory(prefix="numeric-checkpoint-") as scratch:
        output = Path(scratch) / "child.json"
        command += ["--output", str(output)]
        try:
            execution = subprocess.run(
                command,
                cwd=exact.REPO / "packing",
                capture_output=True,
                timeout=seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as error:
            raise IncompleteError("fresh numeric replay wall ceiling") from error
        result = exact.decode(exact.read_bytes(output))
        if result.get("status") == "incomplete":
            raise IncompleteError("fresh numeric replay incomplete")
        exact.require(
            execution.returncode == 0 and result["producer_imported"] is False,
            "fresh numeric replay refused or producer imported",
        )
    return {"command": command, "exit_code": execution.returncode, "receipt": result}


def phase_receipts(document: dict[str, Any], input_control: dict[str, Any]) -> dict[str, Any]:
    production, fresh = [
        exact.decode(exact.read_bytes(retained_path(document[key])))
        for key in ("production_receipt", "fresh_replay_receipt")
    ]
    supplied_input = exact.decode(exact.read_bytes(retained_path(document["input_control"])))
    payload = {k: v for k, v in supplied_input.items() if k not in {"execution", "provenance"}}
    exact.require(
        exact.exact_structure(payload, input_control), "registered input receipt differs"
    )
    for receipt in (production, fresh):
        exact.require(
            receipt["status"] == "PASS_PILOT_MEASURED"
            and receipt["system"] == "n17"
            and receipt["cap"] == "capture"
            and receipt["inner_cap"] == str(CAP)
            and receipt["frame"] == document["frame"]["name"]
            and receipt["U"] == str(OUTER)
            and receipt["seed_sha256"] == document["seed_sha256"]
            and receipt["node_sha256"] == document["node_sha256"]
            and receipt["endpoint_control"]["held"] is True
            and receipt["closure"] is None
            and receipt["refusal"] is None,
            "H289 phase receipt refused or custody differs",
        )
        expected_owners = [
            {
                "label": p["label"],
                "owner": p["owner"],
                "cell": p["cell"],
                "coarse": p["label"] == 6,
            }
            for p in input_control["endpoint_roster"]
        ]
        actual_owners = [
            {k: p[k] for k in ("label", "owner", "cell", "coarse")} for p in receipt["owners"]
        ]
        exact.require(
            exact.exact_structure(actual_owners, expected_owners)
            and all(
                receipt["endpoint"][k] == input_control["pilot_root_boxes"][k]
                for k in ("t_box", "b_box")
            ),
            "H289 endpoint/frame owner custody differs",
        )
        settings = receipt["settings"]
        exact.require(
            settings["box"] is None
            and settings["max_rounds"] == 1
            and settings["bins"] == 32
            and settings["max_live"] == 64
            and settings["min_width"] == "1/4194304"
            and settings["hull_limit"] == 48
            and settings["core"] == "octagon"
            and settings["seed_grid"] == 0,
            "H289 scientific settings differ",
        )
        exact.require(
            receipt["rounds"][-1]["round"] == 1
            and receipt["rounds"][-1]["complete"] is True
            and len(receipt["updates"]) == 16,
            "H289 complete round differs",
        )
    roles = document["label_to_owner"]
    exact.require(
        [roles[str(u["label"])] for u in production["updates"]] == document["step_owners"]
        and production["endpoint_control"]["checked_after"] == 17
        and production["resumed"] is None
        and production["settings"]["replay_share"] == 0
        and fresh["settings"]["replay_share"] == 0.5
        and all(
            u["round"] == 1 and type(u["step"]) is int and u["step"] == i
            for i, u in enumerate(production["updates"])
        )
        and fresh["resumed"]["round"] == 1
        and fresh["resumed"]["changed_since"] == []
        and fresh["updates"] == production["updates"]
        and fresh["rounds"] == production["rounds"]
        and fresh["replay"]["status"] == "PASS_REPLAYED"
        and fresh["replay"]["steps"] == 16
        and fresh["replay"]["final_state_agrees"] is True,
        "H289 zero-production fresh replay differs",
    )
    return {
        "production_receipt": document["production_receipt"],
        "fresh_replay_receipt": document["fresh_replay_receipt"],
        "production_endpoint_checks": 17,
        "fresh_endpoint_scope": "one final-state check; full16-step replay",
    }


def consume_checkpoint(
    document_path: Path, *, deadline: float, child_seconds: float, limits: dict[str, int]
) -> dict[str, Any]:
    consumer = import_module("devtools.check_n17_capture_leaf")
    cap, prefix, _pilot = scientific_modules()
    descriptor_raw = exact.read_bytes(document_path)
    document = exact.decode(descriptor_raw)
    exact.require(
        document["schema"] == CHECKPOINT_SCHEMA
        and document["action"] == "r0"
        and document["original_container_premise"] == "centred-C(S*)"
        and document["composition_premise"] == consumer.COMPOSITION,
        "checkpoint descriptor or conditional premises differ",
    )
    context = load_context(
        retained_path(document["root_path"]),
        retained_path(document["cap_certificate"]),
        retained_path(document["geometry"]),
        deadline,
    )
    checked_inputs = input_packet(context, deadline=deadline)
    exact.require(
        exact.exact_structure(document["root"], context["root"])
        and exact.exact_structure(document["frame"], frame_record(context["numeric"]))
        and exact.exact_structure(
            document["label_to_owner"], {str(p.label): p.owner for p in context["poses"]}
        )
        and len(context["numeric"].cells) == 24,
        "checkpoint root/frame/label custody differs",
    )
    phases = phase_receipts(document, checked_inputs)
    frame = context["numeric"]
    trace, replay = saved_replay(document, frame, deadline=deadline, limits=limits)
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise IncompleteError("parent ceiling before fresh numeric replay")
    fresh = fresh_child(document_path, seconds=min(child_seconds, remaining), limits=limits)
    child = fresh["receipt"]
    exact.require(
        exact.exact_structure(
            {k: child[k] for k in replay if k != "producer_imported"},
            {k: v for k, v in replay.items() if k != "producer_imported"},
        ),
        "fresh numeric full-frame replay differs",
    )
    exact.require(
        descriptor_raw == exact.read_bytes(document_path), "checkpoint descriptor changed"
    )
    held = prefix.endpoint_check(context["poses"], trace.rows)
    exact.require(held["held"] is True, "full17 accepted-root endpoint lost")
    root_loader = cap.root_loader
    root_inputs, layout, _nominal = root_loader.load_root(retained_path(document["root_path"]))
    exact.require(exact.exact_structure(root_inputs, context["root"]), "bounds root changed")
    roles = {int(label): owner for label, owner in document["label_to_owner"].items()}
    leaf = consumer.Leaf(
        frame,
        layout,
        trace.rows,
        roles,
        roles,
        "r0",
        {
            "fresh_replay": True,
            "original_container_premise": "centred-C(S*)",
            "root_layout_x5_identity": "x5*=S*-1/2",
        },
    )
    bounded = consumer.bounds(leaf, deadline=deadline)
    exact.require(
        bounded["status"] == "bounded"
        and len(bounded["intervals"]) == 49
        and all(
            lo <= 0 <= hi for lo, hi in map(exact.read_interval, bounded["intervals"].values())
        ),
        "complete49 zero-containing endpoint bounds required",
    )
    return {
        "schema": CHECKPOINT_SCHEMA,
        "verification_passed": True,
        "readiness_passed": True,
        **consumer.predicates(bounded),
        "root": root_inputs,
        "custody": {
            "input_control": checked_inputs,
            "phases": phases,
            "parent_replay": replay,
            "fresh_replay": fresh,
            "endpoint_retention": held,
        },
        "saved_checkpoint_replayed": True,
        "producer_run": False,
        "exclusion_proved": False,
        "census_admission_proved": False,
        "global_admission_proved": False,
        "capture_tree_proved": False,
        "scope": "conditional leaf readiness; original C(S*)/composition inherited",
    }


def checkpoint_main(argv: list[str], *, clean: bool) -> int:
    parser = argparse.ArgumentParser(description="Bounded numeric-frame saved replay/consumer")
    parser.add_argument("--fresh-saved" if clean else "--checkpoint", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=300 if clean else 600)
    parser.add_argument("--fresh-replay-seconds", type=float, default=300)
    parser.add_argument("--output", type=Path, required=True)
    for name, value in LIMITS.items():
        parser.add_argument("--max-" + name.replace("_", "-"), type=int, default=value)
    args = parser.parse_args(argv)
    started = time.monotonic()
    try:
        exact.require(
            math.isfinite(args.max_seconds)
            and args.max_seconds > 0
            and args.max_seconds <= (300 if clean else 600)
            and math.isfinite(args.fresh_replay_seconds)
            and args.fresh_replay_seconds > 0,
            "invalid checkpoint ceiling",
        )
        exact.require(
            args.fresh_replay_seconds <= 300, "fresh child ceiling exceeds frozen maximum"
        )
        limits = {name: getattr(args, "max_" + name) for name in LIMITS}
        exact.require(
            all(0 < value <= LIMITS[name] for name, value in limits.items()),
            "invalid or enlarged byte ceiling",
        )
        deadline = time.monotonic() + args.max_seconds
        if clean:
            exact.require(
                "sqpack.hull_kernel.producer" not in sys.modules, "producer already imported"
            )
            document = exact.decode(exact.read_bytes(args.fresh_saved))
            _trace, report = saved_replay(
                document, read_frame(document["frame"]), deadline=deadline, limits=limits
            )
            exact.require(
                report["producer_imported"] is False, "producer imported during saved replay"
            )
        else:
            report = consume_checkpoint(
                args.checkpoint,
                deadline=deadline,
                child_seconds=args.fresh_replay_seconds,
                limits=limits,
            )
        report["execution"] = {
            "argv": list(argv),
            "python": sys.version,
            "executable": sys.executable,
            "max_seconds": args.max_seconds,
            "fresh_child_max_seconds": args.fresh_replay_seconds,
            "elapsed_seconds": time.monotonic() - started,
            "limits": limits,
            "rss_scope": "external sampled current-RSS supervisor; no internal peak claim",
        }
        dependencies = [Path(__file__), Path(exact.__file__)]
        dependencies += [
            Path(cast(str, module.__file__))
            for name, module in sorted(sys.modules.items())
            if name.startswith("sqpack.hull_kernel") and getattr(module, "__file__", None)
        ]
        if not clean:
            dependencies += [
                Path(cast(str, sys.modules[name].__file__))
                for name in (
                    "devtools.check_n17_capture_cap",
                    "devtools.check_n17_capture_leaf",
                    "devtools.check_n17_endpoint_prefix",
                    "devtools.pilot_n17_capture",
                )
            ]
        report["provenance"] = provenance(*dependencies)
        within(deadline)
        output_within(report, limits["output_bytes"])
    except IncompleteError as error:
        report = {
            "schema": CHECKPOINT_SCHEMA,
            "status": "incomplete",
            "readiness_passed": False,
            "verification_passed": False,
            "error": str(error),
        }
    except (ValueError, OSError, EOFError, KeyError, TypeError, IndexError) as error:
        report = {
            "schema": CHECKPOINT_SCHEMA,
            "status": "refused",
            "readiness_passed": False,
            "verification_passed": False,
            "error": str(error),
        }
    report.setdefault("global_admission_proved", False)
    report.setdefault("capture_tree_proved", False)
    report.setdefault("census_admission_proved", False)
    report.setdefault("exclusion_proved", False)
    args.output.write_text(retained_json.dumps(report))
    print(
        json.dumps(
            {k: report[k] for k in ("status", "readiness_passed", "error") if k in report}
        )
    )
    return (
        0 if report.get("readiness_passed") or report.get("status") == "PASS_SAVED_STALL" else 1
    )


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
    arguments = list(argv) if argv is not None else sys.argv[1:]
    if any(arg.split("=", 1)[0] == "--fresh-saved" for arg in arguments):
        return checkpoint_main(arguments, clean=True)
    if any(arg.split("=", 1)[0] == "--checkpoint" for arg in arguments):
        return checkpoint_main(arguments, clean=False)
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
