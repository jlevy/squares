"""Check a separate centered-target standing context without changing the U ledger.

The parent binds the accepted algebraic root/cap and original cell world. Its
clean child checks the supplied rational centered container with the independent
standing verifier only. The first scientific control requires a complete stall.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import subprocess
import sys
import tempfile
import time
from fractions import Fraction as Q
from importlib import import_module
from pathlib import Path
from typing import Any

from devtools.provenance import provenance
from sqpack import retained_json

REPO = Path(__file__).resolve().parents[2]
SCHEMA = "n17-centered-cap-standing-context/v1"
U = Q(1169, 250)
V = Q(935106018721, 200000000000)
JSON_LIMIT = 10 << 20
SEED_LIMIT = 10 << 20
NODE_LIMIT = 512 << 20
DECODED_LIMIT = 2 << 30
OUTPUT_LIMIT = 64 << 20
FORBIDDEN = (
    "sqpack.hull_kernel",
    "devtools.check_n17_subpattern",
    "devtools.check_n17_capture_cap",
    "devtools.check_n17_widened_features",
    "devtools.check_n17_root_certificate",
)


class IncompleteError(Exception):
    """A resource ceiling was reached without a complete verdict."""


class ChildRefusalError(ValueError):
    """Retain a bounded failed child receipt and process diagnostics."""

    def __init__(self, diagnostics: dict[str, Any]) -> None:
        super().__init__("fresh standing child refused")
        self.diagnostics = diagnostics


class ChildIncompleteError(IncompleteError):
    """Retain bounded diagnostics without promoting an unfinished replay."""

    def __init__(self, message: str, diagnostics: dict[str, Any]) -> None:
        super().__init__(message)
        self.diagnostics = diagnostics


def require(condition: bool, message: str) -> None:  # noqa: FBT001
    if not condition:
        raise ValueError(message)


def within(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise IncompleteError("centered standing wall ceiling")


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def identity(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON member")
        result[key] = value
    return result


def integer(value: str) -> int:
    require(len(value) <= 1024, "oversized JSON integer")
    return int(value)


def nonfinite(_value: str) -> Any:
    raise ValueError("nonfinite JSON number")


def read_json(path: Path) -> tuple[bytes, dict[str, Any]]:
    with path.open("rb") as stream:
        raw = stream.read(JSON_LIMIT + 1)
    if len(raw) > JSON_LIMIT:
        raise IncompleteError("descriptor/input JSON byte ceiling")
    data = json.loads(
        raw, object_pairs_hook=unique, parse_int=integer, parse_constant=nonfinite
    )
    require(type(data) is dict, "JSON object required")
    return raw, data


def retained_path(value: Any) -> Path:
    require(type(value) is str and not Path(value).is_absolute(), "invalid retained path")
    path = (REPO / value).resolve()
    require(path.is_relative_to(REPO), "retained path escapes repository")
    return path


def context_record() -> dict[str, str]:
    return {
        "outer_U": str(U),
        "inner_V": str(V),
        "offset": str((U - V) / 2),
        "B": "1",
        "target_T": str(V),
    }


def world_record(frame: Any) -> dict[str, Any]:
    return {
        "U": str(frame.cap),
        "L": str(frame.length),
        "B": str(frame.scale),
        "names": list(frame.cell_names),
        "polygons": [[[str(x), str(y)] for x, y in cell] for cell in frame.cells],
        "occupancy": frame.occupancy,
        "actions": [
            {"name": a.name, "matrix": list(a.matrix), "permutation": list(a.permutation)}
            for a in frame.actions
        ],
        "core_slack": str(frame.core_slack),
    }


def validate_descriptor(document: dict[str, Any]) -> None:
    require(
        document["schema"] == SCHEMA and document["context"] == context_record(),
        "centered schema or frozen container/target differs",
    )
    world = document["world"]
    require(
        world["U"] == str(U)
        and world["L"] == str(U)
        and world["B"] == "1"
        and world["occupancy"] == 17
        and len(world["names"]) == len(world["polygons"]),
        "outer world or scale differs",
    )
    require(document["world_sha256"] == identity(world), "world identity differs")
    mask = document["mask"]
    require(
        type(mask) is list
        and len(mask) == 17
        and all(type(i) is int and 0 <= i < len(world["names"]) for i in mask)
        and mask == sorted(set(mask)),
        "complete17 mask differs",
    )
    require(document["expected_status"] == "PASS_STALL", "first control requires stall")


def gzip_size(path: Path, limit: int, deadline: float) -> int:
    count = 0
    with gzip.open(path, "rb") as stream:
        while True:
            within(deadline)
            chunk = stream.read(min(1 << 20, limit - count + 1))
            if not chunk:
                return count
            count += len(chunk)
            if count > limit:
                raise IncompleteError("saved gzip decoded byte ceiling")


def copy_bounded(source: Path, target: Path, limit: int, deadline: float) -> str:
    count, digest = 0, hashlib.sha256()
    with source.open("rb") as reader, target.open("wb") as writer:
        while True:
            within(deadline)
            chunk = reader.read(min(1 << 20, limit - count + 1))
            if not chunk:
                return digest.hexdigest()
            count += len(chunk)
            if count > limit:
                raise IncompleteError("saved gzip compressed byte ceiling")
            digest.update(chunk)
            writer.write(chunk)


def bounded_digest(source: Path, limit: int, deadline: float) -> str:
    count, digest = 0, hashlib.sha256()
    with source.open("rb") as stream:
        while True:
            within(deadline)
            chunk = stream.read(min(1 << 20, limit - count + 1))
            if not chunk:
                return digest.hexdigest()
            count += len(chunk)
            if count > limit:
                raise IncompleteError("saved gzip compressed byte ceiling")
            digest.update(chunk)


def bounded_output(report: dict[str, Any]) -> None:
    if len(retained_json.dumps(report).encode()) > OUTPUT_LIMIT:
        raise IncompleteError("standing report byte ceiling")


def no_science_imports() -> None:
    require(
        not any(
            name == prefix or name.startswith(prefix + ".")
            for name in sys.modules
            for prefix in FORBIDDEN
        ),
        "independent standing child imported forbidden science/producer module",
    )


def relative_replay(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    no_science_imports()
    validate_descriptor(document)
    verifier = import_module("devtools.verify_n17_kernel_certificate")
    world = document["world"]
    cells = verifier.Cells(
        tuple(world["names"]),
        tuple(tuple((Q(x), Q(y)) for x, y in cell) for cell in world["polygons"]),
        U,
        {"kind": "centered-descriptor", "world_sha256": identity(world)},
    )
    directory = retained_path(document["saved_objects"])
    originals = []
    for kind in ("seed", "node"):
        files = list(directory.glob(kind + "-*.json.gz"))
        require(len(files) == 1, "exactly one saved seed/node required")
        originals.append(files[0])
    # The independent verifier receives only bounded private copies. Original
    # gzip bytes and canonical identities remain explicit custody boundaries.
    with tempfile.TemporaryDirectory(prefix="centered-standing-") as temporary:
        target_dir = Path(temporary)
        compressed = {}
        for kind, source in zip(("seed", "node"), originals, strict=True):
            target = target_dir / (kind + "-bounded.json.gz")
            compressed[kind] = copy_bounded(
                source, target, SEED_LIMIT if kind == "seed" else NODE_LIMIT, deadline
            )
            gzip_size(target, SEED_LIMIT if kind == "seed" else DECODED_LIMIT, deadline)
        require(
            compressed == document["compressed_sha256"],
            "registered compressed saved identities differ",
        )
        within(deadline)
        result = verifier.verify(
            target_dir, cells, container=verifier.CenteredContainer(U, V), sample=None
        )
        within(deadline)
        for kind, source in zip(("seed", "node"), originals, strict=True):
            require(
                bounded_digest(source, SEED_LIMIT if kind == "seed" else NODE_LIMIT, deadline)
                == compressed[kind],
                "original saved compressed objects changed",
            )
    no_science_imports()
    require(
        result["schema"] == verifier.CENTERED_SCHEMA
        and result["mode"] == "full"
        and result["status"] in ("PASS_STALL", "PASS_CLOSED"),
        "full centered standing replay failed: " + str(result.get("failure")),
    )
    require(
        result["container"] == {k: v for k, v in context_record().items() if k != "target_T"}
        and result["root_cap_join_checked"] is False,
        "standing result rational container identity differs",
    )
    require(
        result["certificate"]
        == {"seed_sha256": document["seed_sha256"], "node_sha256": document["node_sha256"]}
        and result["mask"] == document["mask"]
        and result["cells"] == [world["names"][i] for i in document["mask"]],
        "canonical saved identity or named mask differs",
    )
    result.update(
        context=context_record(),
        world=world,
        world_sha256=identity(world),
        compressed_sha256=compressed,
        independent_modules=True,
        root_cap_join_checked=False,
        existing_U_census_admission=False,
    )
    return result


def accepted_context(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    # Scientific imports are confined to the parent; no saved object is loaded.
    cap = import_module("devtools.check_n17_capture_cap")
    mask0 = import_module("devtools.check_hull_kernel_mask0")
    validate_descriptor(document)
    root_path = retained_path(document["root_path"])
    cap_path = retained_path(document["cap_certificate"])
    root_raw, _root_packet = read_json(root_path)
    cap_raw, cap_packet = read_json(cap_path)
    within(deadline)
    checked = cap.check(cap_packet, root_path)
    require(
        checked["verification_passed"] is True and checked["cap_certified"] is True,
        "fresh root/cap prerequisite refused",
    )
    root, _layout, _nominal = cap.root_loader.load_root(root_path)
    require(cap.exact.exact_structure(document["root"], root), "accepted root custody differs")
    frame = mask0.n17_unique_frame()
    require(
        len(frame.cells) == 24
        and canonical(document["world"]) == canonical(world_record(frame)),
        "original24 closed cells or D4 context differs",
    )
    endpoint_join = accepted_endpoint(document, root)
    within(deadline)
    require(
        root_raw == read_json(root_path)[0] and cap_raw == read_json(cap_path)[0],
        "root/cap inputs changed across context loading",
    )
    return {
        "root": root,
        "fresh_cap_check": checked,
        "context": context_record(),
        "world_sha256": identity(document["world"]),
        "root_sha256": hashlib.sha256(root_raw).hexdigest(),
        "cap_sha256": hashlib.sha256(cap_raw).hexdigest(),
        "accepted_endpoint": endpoint_join,
    }


def accepted_endpoint(document: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    # This is an explicit accepted-receipt premise join, not another leaf evaluation.
    raw, receipt = read_json(retained_path(document["endpoint_receipt"]))
    require(
        hashlib.sha256(raw).hexdigest() == document["endpoint_receipt_sha256"],
        "accepted endpoint receipt bytes differ",
    )
    require(
        receipt["schema"] == "n17-numeric-cap-checkpoint/v1"
        and receipt["verification_passed"] is True
        and receipt["readiness_passed"] is True
        and receipt["saved_checkpoint_replayed"] is True
        and receipt["root"] == root,
        "accepted full-root numeric endpoint premise differs",
    )
    replay = receipt["custody"]["parent_replay"]
    frame = replay["frame"]
    world = document["world"]
    require(
        frame["U"] == str(U)
        and frame["L"] == str(U)
        and frame["B"] == "1"
        and frame["capture_cap"] == str(V)
        and frame["cells"] == world["polygons"]
        and frame["cell_names"] == world["names"]
        and frame["actions"] == world["actions"]
        and frame["occupancy"] == 17
        and frame["core_slack"] == world["core_slack"]
        and replay["mask"] == document["mask"]
        and replay["steps_checked"] == 16
        and replay["seed_sha256"] == document["seed_sha256"]
        and replay["node_sha256"] == document["node_sha256"]
        and replay["closure"] is None,
        "accepted endpoint original frame/objects differ",
    )
    retention = receipt["custody"]["endpoint_retention"]
    require(
        retention["held"] is True
        and retention["lost_labels"] == []
        and [p["label"] for p in retention["owners"]] == list(range(1, 18))
        and {str(p["label"]): p["owner"] for p in retention["owners"]}
        == document["label_to_owner"]
        and set(document["label_to_owner"].values()) == set(document["mask"])
        and all(p["witness"] is not None for p in retention["owners"]),
        "accepted all17 endpoint retention differs",
    )
    return {
        "receipt": document["endpoint_receipt"],
        "sha256": document["endpoint_receipt_sha256"],
        "scope": "accepted H290 endpoint-retention premise; no new leaf evaluation",
    }


def fresh_replay(path: Path, seconds: float) -> dict[str, Any]:
    require(math.isfinite(seconds) and seconds > 0, "invalid child lease")
    command = [
        sys.executable,
        "-m",
        "devtools.check_n17_centered_cap_standing",
        "--relative-child",
        str(path),
        "--max-seconds",
        str(seconds),
    ]
    with tempfile.TemporaryDirectory(prefix="centered-child-") as temporary:
        output = Path(temporary) / "receipt.json"
        command += ["--output", str(output)]
        try:
            execution = subprocess.run(
                command, cwd=REPO / "packing", timeout=seconds, capture_output=True, check=False
            )
        except subprocess.TimeoutExpired as error:
            diagnostics = child_diagnostics(command, None, error.stdout, error.stderr, output)
            raise ChildIncompleteError(
                "fresh standing child wall ceiling", diagnostics
            ) from error
        diagnostics = child_diagnostics(
            command, execution.returncode, execution.stdout, execution.stderr, output
        )
        if diagnostics.get("receipt_byte_ceiling"):
            raise ChildIncompleteError("fresh standing child receipt byte ceiling", diagnostics)
        receipt = diagnostics.get("receipt")
        if type(receipt) is not dict:
            raise ChildRefusalError(diagnostics)
        if receipt.get("status") == "incomplete":
            raise ChildIncompleteError("fresh standing child incomplete", diagnostics)
        failed_child(execution.returncode, receipt, diagnostics)
    return {"argv": command, "exit_code": execution.returncode, "receipt": receipt}


def child_diagnostics(
    command: list[str],
    code: int | None,
    stdout: bytes | None,
    stderr: bytes | None,
    output: Path,
) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {
        "argv": command,
        "exit_code": code,
        "stdout_tail": (stdout or b"")[-8192:].decode(errors="replace"),
        "stderr_tail": (stderr or b"")[-8192:].decode(errors="replace"),
        "scope": "failed child evidence only; no replay or exclusion accepted",
    }
    try:
        _raw, diagnostics["receipt"] = read_json(output)
    except IncompleteError as error:
        diagnostics["receipt_byte_ceiling"] = True
        diagnostics["receipt_error"] = str(error)
    except (ValueError, OSError, TypeError) as error:
        diagnostics["receipt_error"] = str(error)
    return diagnostics


def failed_child(code: int, receipt: dict[str, Any], diagnostics: dict[str, Any]) -> None:
    if code != 0 or receipt.get("independent_modules") is not True:
        raise ChildRefusalError(diagnostics)


def consume(path: Path, *, deadline: float, child_seconds: float) -> dict[str, Any]:
    raw, document = read_json(path)
    context = accepted_context(document, deadline=deadline)
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise IncompleteError("parent ceiling before independent standing child")
    fresh = fresh_replay(path, min(remaining, child_seconds))
    result = fresh["receipt"]
    require(
        result["context"] == context["context"]
        and result["world"] == document["world"]
        and result["world_sha256"] == context["world_sha256"]
        and result["certificate"]
        == {"seed_sha256": document["seed_sha256"], "node_sha256": document["node_sha256"]}
        and result["mask"] == document["mask"]
        and result["mode"] == "full"
        and result["schema"] == "n17-centered-cap-certificate-verification/v1"
        and result["container"]
        == {k: v for k, v in context_record().items() if k != "target_T"}
        and result["root_cap_join_checked"] is False
        and result["counts"]["steps"] == 16
        and result["compressed_sha256"] == document["compressed_sha256"],
        "fresh context/world/content/complete mask differs",
    )
    require(
        result["status"] == document["expected_status"]
        and result["closure"] is None
        and result["closed"] is False
        and result["centered_exclusion_proved"] is False,
        "numeric endpoint stall control unexpectedly closed",
    )
    require(raw == read_json(path)[0], "standing descriptor changed")
    for field, digest in (
        ("root_path", context["root_sha256"]),
        ("cap_certificate", context["cap_sha256"]),
        ("endpoint_receipt", context["accepted_endpoint"]["sha256"]),
    ):
        require(
            hashlib.sha256(read_json(retained_path(document[field]))[0]).hexdigest() == digest,
            "standing premise inputs changed across child replay",
        )
    within(deadline)
    return {
        "schema": SCHEMA,
        "status": "centered_stall_control_checked",
        "verification_passed": True,
        "readiness_passed": True,
        "accepted_context": context,
        "fresh_standing": fresh,
        "root_cap_join_checked": True,
        "target_T": str(V),
        "centered_exclusion_proved": False,
        "existing_U_census_admission": False,
        "new_target_admission_proved": False,
        "global_optimality_proved": False,
        "scope": "full numeric-centered stall control; no exclusion or admission",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--descriptor", type=Path)
    mode.add_argument("--relative-child", type=Path)
    parser.add_argument("--max-seconds", type=float, default=600)
    parser.add_argument("--child-seconds", type=float, default=300)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        require(
            math.isfinite(args.max_seconds)
            and 0 < args.max_seconds <= (300 if args.relative_child else 600)
            and math.isfinite(args.child_seconds)
            and 0 < args.child_seconds <= 300,
            "invalid or enlarged standing wall ceiling",
        )
        deadline = time.monotonic() + args.max_seconds
        if args.relative_child:
            _raw, document = read_json(args.relative_child)
            report = relative_replay(document, deadline=deadline)
        else:
            report = consume(
                args.descriptor, deadline=deadline, child_seconds=args.child_seconds
            )
        report["execution"] = {
            "argv": list(argv) if argv is not None else sys.argv[1:],
            "python": sys.version,
            "executable": sys.executable,
            "max_seconds": args.max_seconds,
            "child_seconds": args.child_seconds,
            "rss_scope": "external sampled currentRSS; no peak claim",
        }
        report["wrapper_provenance"] = provenance(Path(__file__))
        within(deadline)
        bounded_output(report)
    except IncompleteError as error:
        report = {
            "schema": SCHEMA,
            "status": "incomplete",
            "error": str(error),
            "readiness_passed": False,
            "verification_passed": False,
        }
        if isinstance(error, ChildIncompleteError):
            report["failed_child"] = error.diagnostics
    except (ValueError, OSError, EOFError, KeyError, TypeError, IndexError) as error:
        report = {
            "schema": SCHEMA,
            "status": "refused",
            "error": str(error),
            "readiness_passed": False,
            "verification_passed": False,
        }
        if isinstance(error, ChildRefusalError):
            report["failed_child"] = error.diagnostics
    for flag in (
        "existing_U_census_admission",
        "new_target_admission_proved",
        "global_optimality_proved",
    ):
        report[flag] = False
    args.output.write_text(retained_json.dumps(report))
    print(json.dumps({k: report[k] for k in ("status", "error") if k in report}))
    return (
        0
        if report.get("readiness_passed")
        or report.get("status") in ("PASS_STALL", "PASS_CLOSED")
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
