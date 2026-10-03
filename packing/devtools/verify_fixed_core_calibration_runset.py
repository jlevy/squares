"""Verify retained, target-free three-profile calibration run-set evidence.

The source-distinct reader owns scientific checks. This module binds its three
accepted proofs to the coordinator, preserves the run root, and checks that every
receipt's source manifest names the execution revision's import closure.

The run set is a fact about that revision. What has changed in its source closure
since -- code, `pyproject.toml`, `uv.lock` or `.python-version` -- is reported as
`drift` for whoever commits the evidence, and is never a reason to refuse it or to
run the profiles again (development.md, Hashes and Repository-Owned Artifacts).
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import io
import json
import math
import os
import re
import stat
import subprocess
import sys
import tarfile
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path, PurePosixPath
from typing import Never, cast

INVENTORY_SCHEMA = "fixed-core-calibration-run-root-inventory/v1"
COMMAND_SCHEMA = "fixed-core-calibration-source-distinct-command/v1"
ADMISSION_SCHEMA = "fixed-core-calibration-run-set-reader-admission/v1"
CLOSURE_SCHEMA = "fixed-core-calibration-source-closure-check/v2"
SUMMARY_SCHEMA = "fixed-core-calibration-three-profile-summary/v1"
READER_SCHEMA = "fixed-core-calibration-source-distinct-readback/v1"
RUN_ORDERS = (1, 2, 3)
INVENTORY_NAME = "run-root-inventory.json"
ADMISSION_NAME = "run-set-reader-admission.json"
SUMMARY_NAME = "three-profile-summary.json"
COORDINATOR_TOP_LEVEL_FILES = frozenset(
    {
        SUMMARY_NAME,
        *(f"profile-{order}-run.json" for order in RUN_ORDERS),
        *(
            f"profile-{order}{suffix}.{stream}.log"
            for order in RUN_ORDERS
            for suffix in ("", "-producer-readback", "-inventory-readback")
            for stream in ("stdout", "stderr")
        ),
    }
)
FIXTURE_PATH = "packing/cases/n02_fixed_core_packet_calibration/fixture.json"
RUNTIME_PATHS = ("packing/.python-version", "packing/pyproject.toml", "packing/uv.lock")
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
SUMMARY_KEYS = {
    "schema",
    "evidence_scope",
    "execution_revision",
    "frozen_tuple",
    "settings",
    "runs",
    "metrics",
}
RUN_KEYS = {
    "run_order",
    "profile_directory",
    "invocation_identity",
    "calibration_receipt",
    "command_wall_seconds",
    "inventory",
}
IDENTITY_KEYS = {
    "implementation_revision",
    "requested_workers",
    "calibration_seconds",
    "external_seconds",
    "termination_grace_seconds",
    "monotonic_origin",
    "calibration_deadline_monotonic",
    "external_deadline_monotonic",
    "run_order",
    "cache_observation",
    "background_load",
}
PROOF_KEYS = {
    "schema",
    "status",
    "evidence_scope",
    "execution_revision",
    "reader_revision",
    "run_order",
    "profile_directory",
    "invocation_identity",
    "receipt",
    "fixture",
    "route_digests",
    "interval_boxes_observed",
    "resources",
    "worker_topology",
    "artifacts",
    "limitations",
}
REVIEW_NAMES = (
    "pre-series-processes.txt",
    "pre-series-uptime.txt",
    "coordinator.stdout.log",
    "coordinator.stderr.log",
    "coordinator.status",
    INVENTORY_NAME,
    ADMISSION_NAME,
    *(
        f"profile-{order}-source-distinct.{suffix}"
        for order in RUN_ORDERS
        for suffix in ("command.json", "stdout.json", "stderr.log", "status")
    ),
)


class RunSetRefusalError(ValueError):
    """A run-set input, retained byte, command, or source closure is inadmissible."""


def _refuse(message: str) -> Never:
    raise RunSetRefusalError(message)


def _revision(value: object, label: str) -> str:
    if type(value) is not str or HEX40.fullmatch(value) is None:
        _refuse(f"{label} must be 40 lowercase hexadecimal characters")
    return value


def _digest(value: object, label: str) -> str:
    if type(value) is not str or HEX64.fullmatch(value) is None:
        _refuse(f"{label} must be a SHA-256 digest")
    return value


def _object(value: object, keys: set[str], label: str) -> dict[str, object]:
    if type(value) is not dict or set(value) != keys:
        _refuse(f"{label} fields differ from the expected schema")
    return cast(dict[str, object], value)


def _array(value: object, label: str) -> list[object]:
    if type(value) is not list:
        _refuse(f"{label} must be an array")
    return cast(list[object], value)


def _integer(value: object, label: str, *, positive: bool = False) -> int:
    if type(value) is not int or (value <= 0 if positive else value < 0):
        _refuse(f"{label} must be a {'positive' if positive else 'nonnegative'} integer")
    return value


def _finite_number(value: object, label: str, *, positive: bool = False) -> int | float:
    if type(value) not in (int, float):
        _refuse(f"{label} must be a finite number")
    typed_value = cast(int | float, value)
    try:
        number = float(typed_value)
    except (OverflowError, ValueError) as error:
        raise RunSetRefusalError(f"{label} must be a finite number") from error
    if not math.isfinite(number) or (number <= 0 if positive else number < 0):
        _refuse(f"{label} must be a finite {'positive' if positive else 'nonnegative'} number")
    return typed_value


def _identity(value: object, revision: str, order: int, label: str) -> dict[str, object]:
    identity = _object(value, IDENTITY_KEYS, label)
    if identity["implementation_revision"] != revision or identity["run_order"] != order:
        _refuse(f"{label} revision or order differs")
    workers = _integer(
        identity["requested_workers"], f"{label} requested workers", positive=True
    )
    if workers > 4 or type(identity["run_order"]) is not int:
        _refuse(f"{label} workers or run order is malformed")
    calibration = _finite_number(
        identity["calibration_seconds"], f"{label} calibration", positive=True
    )
    external = _finite_number(identity["external_seconds"], f"{label} external", positive=True)
    _finite_number(identity["termination_grace_seconds"], f"{label} grace", positive=True)
    origin = _finite_number(identity["monotonic_origin"], f"{label} origin")
    calibration_deadline = _finite_number(
        identity["calibration_deadline_monotonic"], f"{label} calibration deadline"
    )
    external_deadline = _finite_number(
        identity["external_deadline_monotonic"], f"{label} external deadline"
    )
    if (
        calibration >= external
        or calibration_deadline != origin + calibration
        or external_deadline != origin + external
    ):
        _refuse(f"{label} deadlines are incoherent")
    for field in ("cache_observation", "background_load"):
        text = identity[field]
        if type(text) is not str or not text.strip():
            _refuse(f"{label} {field} must be nonempty text")
    return identity


def _pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            _refuse(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _constant(value: str) -> Never:
    _refuse(f"non-finite JSON constant: {value}")


def _finite_tree(value: object) -> None:
    if type(value) is float and not math.isfinite(value):
        _refuse("non-finite JSON number")
    if type(value) is dict:
        for nested in cast(dict[str, object], value).values():
            _finite_tree(nested)
    elif type(value) is list:
        for nested in cast(list[object], value):
            _finite_tree(nested)


def _json_bytes(data: bytes, label: str) -> dict[str, object]:
    try:
        value: object = json.loads(
            data.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_constant
        )
        if type(value) is not dict:
            _refuse(f"{label} must be a JSON object")
        _finite_tree(value)
    except RunSetRefusalError:
        raise
    except (ValueError, RecursionError) as error:
        raise RunSetRefusalError(f"{label} is not one UTF-8 JSON object") from error
    return cast(dict[str, object], value)


def _regular_bytes(path: Path, label: str) -> bytes:
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        _refuse(f"{label} is not a unique regular file: {path}")
    with path.open("rb") as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino):
            _refuse(f"{label} changed while opening: {path}")
        data = stream.read()
        after = os.fstat(stream.fileno())
    current = path.lstat()

    def signature(item: os.stat_result) -> tuple[int, ...]:
        return (
            item.st_dev,
            item.st_ino,
            item.st_mode,
            item.st_nlink,
            item.st_size,
            item.st_mtime_ns,
            item.st_ctime_ns,
        )

    if signature(before) != signature(after) or signature(after) != signature(current):
        _refuse(f"{label} changed while reading: {path}")
    if len(data) != before.st_size:
        _refuse(f"{label} has an inconsistent size: {path}")
    return data


def _json_file(path: Path, label: str) -> tuple[bytes, dict[str, object]]:
    data = _regular_bytes(path, label)
    return data, _json_bytes(data, label)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _atomic_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    staged = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            path.hardlink_to(staged)
        except FileExistsError as error:
            raise RunSetRefusalError(f"output already exists: {path}") from error
    finally:
        staged.unlink(missing_ok=True)


def _atomic_replace(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary).replace(path)
    finally:
        if Path(temporary).exists():
            Path(temporary).unlink()


def _publish_json(path: Path, record: dict[str, object], *, replace: bool = False) -> None:
    data = (
        json.dumps(record, sort_keys=True, allow_nan=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    if replace:
        _atomic_replace(path, data)
    else:
        _atomic_new(path, data)
    if _json_file(path, path.name)[0] != data:
        _refuse(f"published JSON changed on reread: {path}")


def _canonical_dir(path: Path, label: str) -> Path:
    if not path.is_absolute() or path != path.resolve(strict=True):
        _refuse(f"{label} must be a canonical absolute directory")
    if not stat.S_ISDIR(path.lstat().st_mode):
        _refuse(f"{label} must be a real directory")
    return path


def _roots(run_root: Path, review_root: Path) -> tuple[Path, Path]:
    run_root = _canonical_dir(run_root, "run root")
    review_root = _canonical_dir(review_root, "review root")
    if (
        run_root == review_root
        or run_root.is_relative_to(review_root)
        or review_root.is_relative_to(run_root)
    ):
        _refuse("run and review roots must be separate")
    return run_root, review_root


def _relative(value: object, label: str) -> str:
    if (
        type(value) is not str
        or not value
        or "\\" in value
        or PurePosixPath(value).is_absolute()
        or PurePosixPath(value).as_posix() != value
        or any(part in ("", ".", "..") for part in value.split("/"))
    ):
        _refuse(f"{label} is not a canonical relative POSIX path")
    return value


def _binding(value: object, label: str, *, path: str | None = None) -> dict[str, object]:
    row = _object(value, {"path", "bytes", "sha256"}, label)
    relative = _relative(row["path"], f"{label} path")
    if path is not None and relative != path:
        _refuse(f"{label} path differs from {path}")
    _integer(row["bytes"], f"{label} bytes")
    _digest(row["sha256"], f"{label} digest")
    return row


def _summary(
    run_root: Path, revision: str
) -> tuple[bytes, dict[str, object], list[dict[str, object]]]:
    data, summary = _json_file(run_root / SUMMARY_NAME, "coordinator summary")
    _object(summary, SUMMARY_KEYS, "coordinator summary")
    if summary["schema"] != SUMMARY_SCHEMA or summary["execution_revision"] != revision:
        _refuse("coordinator summary schema or execution revision differs")
    runs = _array(summary["runs"], "coordinator runs")
    if len(runs) != len(RUN_ORDERS):
        _refuse("coordinator summary requires exactly three runs")
    typed_runs: list[dict[str, object]] = []
    for order, value in zip(RUN_ORDERS, runs, strict=True):
        run = _object(value, RUN_KEYS, "coordinator run")
        if type(run["run_order"]) is not int or run["run_order"] != order:
            _refuse("coordinator runs are out of order")
        if run["profile_directory"] != str(run_root / f"profile-{order}"):
            _refuse("coordinator profile path differs from the run root")
        _identity(
            run["invocation_identity"], revision, order, "coordinator invocation identity"
        )
        _binding(run["calibration_receipt"], "coordinator receipt", path="result.json")
        if type(run["inventory"]) is not dict:
            _refuse("coordinator run inventory must be an object")
        typed_runs.append(run)
    return data, summary, typed_runs


def _scan(root: Path) -> tuple[list[str], list[dict[str, object]]]:
    directories: list[str] = []
    files: list[dict[str, object]] = []

    def walk(directory: Path, prefix: str) -> None:
        entries = sorted(os.scandir(directory), key=lambda entry: entry.name)
        if prefix and not entries:
            _refuse(f"empty run-root directory: {prefix}")
        for entry in entries:
            relative = _relative(
                f"{prefix}/{entry.name}" if prefix else entry.name, "run-root path"
            )
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                directories.append(relative)
                walk(Path(entry.path), relative)
            elif stat.S_ISREG(mode):
                data = _regular_bytes(Path(entry.path), "run-root artifact")
                files.append(
                    {
                        "path": relative,
                        "type": "regular-file",
                        "bytes": len(data),
                        "sha256": _sha(data),
                    }
                )
            else:
                _refuse(f"run root contains link or special file: {relative}")

    walk(root, "")
    directories.sort()
    files.sort(key=lambda row: cast(str, row["path"]))
    return directories, files


def _inventory(run_root: Path, revision: str) -> dict[str, object]:
    directories, files = _scan(run_root)
    if {name for name in directories if "/" not in name} != {
        f"profile-{order}" for order in RUN_ORDERS
    }:
        _refuse("run root does not contain exactly three profile directories")
    # The coordinator writes three command pairs and a run record per profile.
    # Producer artifacts are confined to the three profile directories.
    top_level = {cast(str, row["path"]) for row in files if "/" not in cast(str, row["path"])}
    if top_level != COORDINATOR_TOP_LEVEL_FILES:
        _refuse("run root top-level files differ from the coordinator output set")
    _summary(run_root, revision)
    return {
        "schema": INVENTORY_SCHEMA,
        "execution_revision": revision,
        "run_root": str(run_root),
        "directories": directories,
        "files": files,
    }


def _baseline(
    run_root: Path, review_root: Path, revision: str
) -> tuple[bytes, dict[str, object]]:
    data, record = _json_file(review_root / INVENTORY_NAME, "run-root inventory")
    _object(
        record,
        {"schema", "execution_revision", "run_root", "directories", "files"},
        "run-root inventory",
    )
    if (
        record["schema"] != INVENTORY_SCHEMA
        or record["execution_revision"] != revision
        or record["run_root"] != str(run_root)
    ):
        _refuse("run-root inventory identity differs")
    directories = _array(record["directories"], "inventory directories")
    files = _array(record["files"], "inventory files")
    paths = [_relative(item, "inventory directory") for item in directories]
    if paths != sorted(set(paths)):
        _refuse("inventory directories are unsorted or duplicated")
    file_paths: list[str] = []
    for item in files:
        row = _object(item, {"path", "type", "bytes", "sha256"}, "inventory file")
        file_paths.append(_relative(row["path"], "inventory file path"))
        if row["type"] != "regular-file":
            _refuse("inventory has a nonregular file")
        _integer(row["bytes"], "inventory file bytes")
        _digest(row["sha256"], "inventory file digest")
    if file_paths != sorted(set(file_paths)) or set(file_paths) & set(paths):
        _refuse("inventory paths are unsorted or duplicated")
    if record != _inventory(run_root, revision):
        _refuse("run root differs from coordinator-return inventory")
    return data, record


def snapshot_run_root(
    *, run_root: Path, review_root: Path, execution_revision: str
) -> dict[str, object]:
    """Record the first complete byte/type observation after coordinator return."""
    run_root, review_root = _roots(run_root, review_root)
    revision = _revision(execution_revision, "execution revision")
    if _regular_bytes(review_root / "coordinator.status", "coordinator status") != b"0\n":
        _refuse("coordinator did not return status zero")
    record = _inventory(run_root, revision)
    _publish_json(review_root / INVENTORY_NAME, record)
    _baseline(run_root, review_root, revision)
    return record


def _reader_names(order: int) -> tuple[str, str, str, str]:
    stem = f"profile-{order}-source-distinct"
    return (
        f"{stem}.command.json",
        f"{stem}.stdout.json",
        f"{stem}.stderr.log",
        f"{stem}.status",
    )


def _reader_argv(
    repository: Path, run_root: Path, execution_revision: str, reader_revision: str, order: int
) -> list[str]:
    return [
        sys.executable,
        "-m",
        "devtools.read_fixed_core_calibration_profile",
        "--repository",
        str(repository),
        "--expect-execution-revision",
        execution_revision,
        "--expect-reader-revision",
        reader_revision,
        "--output-dir",
        str(run_root / f"profile-{order}"),
        "--run-order",
        str(order),
    ]


def run_reader(
    *,
    repository: Path,
    run_root: Path,
    review_root: Path,
    execution_revision: str,
    reader_revision: str,
    run_order: int,
    runner: Callable[[Sequence[str]], subprocess.CompletedProcess[bytes]] | None = None,
) -> int:
    """Launch one reader with the exact retained argv and capture refusal evidence."""
    repository = _canonical_dir(repository, "repository")
    run_root, review_root = _roots(run_root, review_root)
    revision = _revision(execution_revision, "execution revision")
    reader_revision = _revision(reader_revision, "reader revision")
    if type(run_order) is not int or run_order not in RUN_ORDERS:
        _refuse("reader run order must be 1, 2, or 3")
    if run_root.is_relative_to(repository) or review_root.is_relative_to(repository):
        _refuse("run and review roots must be outside the repository")
    _baseline(run_root, review_root, revision)
    command_name, stdout_name, stderr_name, status_name = _reader_names(run_order)
    for name in (command_name, stdout_name, stderr_name, status_name):
        if (review_root / name).exists() or (review_root / name).is_symlink():
            _refuse(f"reader output already exists: {name}")
    argv = _reader_argv(repository, run_root, revision, reader_revision, run_order)
    record: dict[str, object] = {
        "schema": COMMAND_SCHEMA,
        "run_order": run_order,
        "argv": argv,
        "exit_status": None,
        "stdout": None,
        "stderr": None,
    }
    command_path = review_root / command_name
    _publish_json(command_path, record)
    try:
        result = (
            runner
            or (lambda arguments: subprocess.run(arguments, check=False, capture_output=True))
        )(argv)
    except OSError as error:
        raise RunSetRefusalError(
            f"reader launch failed; pending command retained: {error}"
        ) from error
    if (
        type(result.returncode) is not int
        or type(result.stdout) is not bytes
        or type(result.stderr) is not bytes
    ):
        _refuse("reader process returned malformed streams or status")
    _atomic_new(review_root / stdout_name, result.stdout)
    _atomic_new(review_root / stderr_name, result.stderr)
    _atomic_new(review_root / status_name, f"{result.returncode}\n".encode("ascii"))
    record["exit_status"] = result.returncode
    record["stdout"] = {
        "path": stdout_name,
        "bytes": len(result.stdout),
        "sha256": _sha(result.stdout),
    }
    record["stderr"] = {
        "path": stderr_name,
        "bytes": len(result.stderr),
        "sha256": _sha(result.stderr),
    }
    _publish_json(command_path, record, replace=True)
    if result.returncode == 0:
        _command(
            review_root=review_root,
            run_root=run_root,
            repository=repository,
            revision=revision,
            reader_revision=reader_revision,
            order=run_order,
        )
    _baseline(run_root, review_root, revision)
    return result.returncode or 0


def _command(
    *,
    review_root: Path,
    run_root: Path,
    repository: Path,
    revision: str,
    reader_revision: str,
    order: int,
) -> tuple[bytes, bytes, dict[str, object]]:
    command_name, stdout_name, stderr_name, status_name = _reader_names(order)
    command_data, record = _json_file(review_root / command_name, "reader command")
    _object(
        record,
        {"schema", "run_order", "argv", "exit_status", "stdout", "stderr"},
        "reader command",
    )
    if (
        record["schema"] != COMMAND_SCHEMA
        or type(record["run_order"]) is not int
        or record["run_order"] != order
        or record["argv"]
        != _reader_argv(repository, run_root, revision, reader_revision, order)
        or type(record["exit_status"]) is not int
        or record["exit_status"] != 0
    ):
        _refuse(f"reader {order} command, order, or status differs")
    if _regular_bytes(review_root / status_name, "reader status") != b"0\n":
        _refuse(f"reader {order} status file differs")
    for field, name in (("stdout", stdout_name), ("stderr", stderr_name)):
        binding = _binding(record[field], f"reader {order} {field}", path=name)
        stream = _regular_bytes(review_root / name, f"reader {order} {field}")
        if binding["bytes"] != len(stream) or binding["sha256"] != _sha(stream):
            _refuse(f"reader {order} {field} binding differs")
    return command_data, _regular_bytes(review_root / stdout_name, "reader proof"), record


def _admission(
    run_root: Path,
    review_root: Path,
    repository: Path,
    revision: str,
    reader_revision: str,
    *,
    copied_review: bool = False,
) -> dict[str, object]:
    if run_root.is_relative_to(repository) or (
        not copied_review and review_root.is_relative_to(repository)
    ):
        _refuse("run and review roots must be outside the repository")
    inventory_data, _ = _baseline(run_root, review_root, revision)
    summary_data, _, runs = _summary(run_root, revision)
    expected_reader_names = {name for order in RUN_ORDERS for name in _reader_names(order)}
    observed_reader_names = {
        entry.name
        for entry in os.scandir(review_root)
        if entry.name.startswith("profile-") and "source-distinct" in entry.name
    }
    if observed_reader_names != expected_reader_names:
        _refuse("reader proofs or command records are missing or extra")
    accepted: list[dict[str, object]] = []
    for order, run in zip(RUN_ORDERS, runs, strict=True):
        command_data, proof_data, _ = _command(
            review_root=review_root,
            run_root=run_root,
            repository=repository,
            revision=revision,
            reader_revision=reader_revision,
            order=order,
        )
        proof = _json_bytes(proof_data, f"reader {order} proof")
        _object(proof, PROOF_KEYS, f"reader {order} proof")
        proof_identity = _identity(
            proof["invocation_identity"], revision, order, f"reader {order} identity"
        )
        if (
            proof["schema"] != READER_SCHEMA
            or proof["status"] != "accepted"
            or proof["execution_revision"] != revision
            or proof["reader_revision"] != reader_revision
            or type(proof["run_order"]) is not int
            or proof["run_order"] != order
            or proof["profile_directory"] != run["profile_directory"]
            or not _same_typed(proof_identity, run["invocation_identity"])
        ):
            _refuse(f"reader {order} proof does not bind its coordinator run")
        receipt = _binding(proof["receipt"], f"reader {order} receipt", path="result.json")
        summary_receipt = _binding(
            run["calibration_receipt"], "summary receipt", path="result.json"
        )
        if receipt != summary_receipt:
            _refuse(f"reader {order} receipt differs from coordinator summary")
        profile_receipt = _regular_bytes(
            run_root / f"profile-{order}" / "result.json", "profile receipt"
        )
        if receipt["bytes"] != len(profile_receipt) or receipt["sha256"] != _sha(
            profile_receipt
        ):
            _refuse(f"reader {order} receipt bytes differ")
        accepted.append(
            {
                "run_order": order,
                "profile_directory": run["profile_directory"],
                "command_sha256": _sha(command_data),
                "proof_sha256": _sha(proof_data),
                "receipt_sha256": receipt["sha256"],
            }
        )
    return {
        "schema": ADMISSION_SCHEMA,
        "status": "accepted",
        "execution_revision": revision,
        "reader_revision": reader_revision,
        "run_root_inventory_sha256": _sha(inventory_data),
        "summary_sha256": _sha(summary_data),
        "runs": accepted,
    }


def _same_typed(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        lhs, rhs = cast(dict[str, object], left), cast(dict[str, object], right)
        return lhs.keys() == rhs.keys() and all(_same_typed(lhs[key], rhs[key]) for key in lhs)
    if type(left) is list:
        lhs, rhs = cast(list[object], left), cast(list[object], right)
        return len(lhs) == len(rhs) and all(
            _same_typed(a, b) for a, b in zip(lhs, rhs, strict=True)
        )
    return left == right


def join_reader_proofs(
    *,
    run_root: Path,
    review_root: Path,
    execution_revision: str,
    reader_revision: str,
    repository: Path | None = None,
) -> dict[str, object]:
    """Join three accepted reader proofs to the immutable coordinator summary."""
    run_root, review_root = _roots(run_root, review_root)
    revision = _revision(execution_revision, "execution revision")
    reader_revision = _revision(reader_revision, "reader revision")
    # The reader argv binds its repository. Its path is recovered exactly from
    # the first command, then checked against every command below.
    if repository is None:
        _, first = _json_file(review_root / _reader_names(1)[0], "first reader command")
        argv = _array(first.get("argv"), "first reader argv")
        if len(argv) != 13 or argv[3] != "--repository" or type(argv[4]) is not str:
            _refuse("first reader argv is malformed")
        repository = Path(cast(str, argv[4]))
    repository = _canonical_dir(repository, "repository")
    record = _admission(run_root, review_root, repository, revision, reader_revision)
    _publish_json(review_root / ADMISSION_NAME, record)
    return record


def _verify_archive(path: Path, run_root: Path, baseline: dict[str, object]) -> list[str]:
    expected_dirs = set(cast(list[str], baseline["directories"]))
    expected_files = {
        cast(str, row["path"]): row for row in cast(list[dict[str, object]], baseline["files"])
    }
    seen_dirs: set[str] = set()
    seen_files: set[str] = set()
    names: list[str] = []
    prefix = run_root.name
    with tarfile.open(path, "r:gz") as archive:
        for member in archive:
            name = member.name.rstrip("/")
            names.append(member.name)
            if name == prefix:
                if not member.isdir() or "" in seen_dirs:
                    _refuse("archive root is duplicated or not a directory")
                seen_dirs.add("")
                continue
            if not name.startswith(f"{prefix}/"):
                _refuse("archive member escapes the run-root prefix")
            relative = _relative(name[len(prefix) + 1 :], "archive member")
            if member.isdir():
                if (
                    relative not in expected_dirs
                    or relative in seen_dirs
                    or relative in seen_files
                ):
                    _refuse(f"archive directory differs or repeats: {relative}")
                seen_dirs.add(relative)
            elif member.isfile():
                if (
                    relative not in expected_files
                    or relative in seen_files
                    or relative in seen_dirs
                ):
                    _refuse(f"archive file differs or repeats: {relative}")
                stream = archive.extractfile(member)
                if stream is None:
                    _refuse(f"archive file cannot be read: {relative}")
                data = stream.read()
                row = expected_files[relative]
                if (
                    member.size != len(data)
                    or row["bytes"] != len(data)
                    or row["sha256"] != _sha(data)
                ):
                    _refuse(f"archive file bytes differ: {relative}")
                seen_files.add(relative)
            else:
                _refuse(f"archive has link or special member: {relative}")
    if seen_dirs != expected_dirs | {""} or seen_files != set(expected_files):
        _refuse("archive path/type set differs from the baseline")
    return names


def retain_run_root(
    *, run_root: Path, review_root: Path, evidence_root: Path, execution_revision: str
) -> dict[str, object]:
    """Copy review evidence and archive only bytes matching the first inventory."""
    run_root, review_root = _roots(run_root, review_root)
    revision = _revision(execution_revision, "execution revision")
    if (
        not evidence_root.is_absolute()
        or evidence_root.exists()
        or evidence_root.is_symlink()
        or evidence_root.parent != evidence_root.parent.resolve(strict=True)
    ):
        _refuse("evidence root must be a fresh canonical absolute path")
    if evidence_root.is_relative_to(run_root) or evidence_root.is_relative_to(review_root):
        _refuse("evidence root must be separate from external run and review roots")
    inventory_data, baseline = _baseline(run_root, review_root, revision)
    admission_data, admission = _json_file(review_root / ADMISSION_NAME, "reader admission")
    _object(
        admission,
        {
            "schema",
            "status",
            "execution_revision",
            "reader_revision",
            "run_root_inventory_sha256",
            "summary_sha256",
            "runs",
        },
        "reader admission",
    )
    reader_revision = _revision(admission["reader_revision"], "reader revision")
    _, first = _json_file(review_root / _reader_names(1)[0], "first reader command")
    argv = _array(first.get("argv"), "first reader argv")
    if len(argv) != 13 or argv[3] != "--repository" or type(argv[4]) is not str:
        _refuse("first reader argv is malformed")
    repository = _canonical_dir(Path(cast(str, argv[4])), "repository")
    if admission != _admission(run_root, review_root, repository, revision, reader_revision):
        _refuse("retained reader admission differs from current proofs")
    observed_review = {entry.name for entry in os.scandir(review_root)}
    if observed_review != set(REVIEW_NAMES):
        _refuse("review root file set differs from the retention whitelist")
    if _regular_bytes(review_root / "coordinator.status", "coordinator status") != b"0\n":
        _refuse("coordinator status changed after snapshot")
    review_digests = {
        name: _sha(_regular_bytes(review_root / name, "review artifact"))
        for name in REVIEW_NAMES
    }
    if review_digests["coordinator.status"] != _sha(b"0\n"):
        _refuse("coordinator status changed before retention copy")
    if review_digests[ADMISSION_NAME] != _sha(admission_data):
        _refuse("review artifact changed after admission check")
    evidence_root.mkdir()
    for name in REVIEW_NAMES:
        data = _regular_bytes(review_root / name, "review artifact")
        if _sha(data) != review_digests[name]:
            _refuse(f"review artifact changed during retention: {name}")
        _atomic_new(evidence_root / name, data)
    summary_data = _regular_bytes(run_root / SUMMARY_NAME, "coordinator summary")
    _atomic_new(evidence_root / SUMMARY_NAME, summary_data)
    _atomic_new(evidence_root / "execution-revision.txt", f"{revision}\n".encode())
    _atomic_new(evidence_root / "reader-revision.txt", f"{reader_revision}\n".encode())
    archive_path = evidence_root / "run-root.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        for relative in ("", *cast(list[str], baseline["directories"])):
            name = f"{run_root.name}/{relative}" if relative else run_root.name
            info = tarfile.TarInfo(name)
            info.type = tarfile.DIRTYPE
            info.mode = 0o755
            archive.addfile(info)
        for row in cast(list[dict[str, object]], baseline["files"]):
            relative = cast(str, row["path"])
            data = _regular_bytes(run_root / relative, "run-root archive source")
            if row["bytes"] != len(data) or row["sha256"] != _sha(data):
                _refuse(f"run-root artifact changed during archiving: {relative}")
            info = tarfile.TarInfo(f"{run_root.name}/{relative}")
            info.size = len(data)
            info.mode = 0o644
            archive.addfile(info, io.BytesIO(data))
    names = _verify_archive(archive_path, run_root, baseline)
    _baseline(run_root, review_root, revision)
    if {entry.name for entry in os.scandir(review_root)} != set(REVIEW_NAMES):
        _refuse("review artifact set changed during retention")
    for name, digest in review_digests.items():
        if (
            _sha(_regular_bytes(review_root / name, "review artifact")) != digest
            or _sha(_regular_bytes(evidence_root / name, "copied review artifact")) != digest
        ):
            _refuse(f"review artifact changed or copied inconsistently: {name}")
    if _regular_bytes(evidence_root / SUMMARY_NAME, "copied summary") != summary_data:
        _refuse("copied summary, inventory, or admission differs")
    if admission != _admission(
        run_root,
        evidence_root,
        repository,
        revision,
        reader_revision,
        copied_review=True,
    ):
        _refuse("copied review artifacts disagree with retained admission")
    archive_data = _regular_bytes(archive_path, "run-root archive")
    archive_digest = _sha(archive_data)
    _atomic_new(evidence_root / "run-root-contents.txt", ("\n".join(names) + "\n").encode())
    _atomic_new(
        evidence_root / "run-root.tar.gz.sha256",
        f"{archive_digest}  run-root.tar.gz\n".encode(),
    )
    if _sha(_regular_bytes(archive_path, "run-root archive")) != archive_digest:
        _refuse("archive digest changed on reread")
    if (
        _regular_bytes(review_root / "coordinator.status", "coordinator status") != b"0\n"
        or _regular_bytes(evidence_root / "coordinator.status", "copied coordinator status")
        != b"0\n"
    ):
        _refuse("coordinator status changed during retention")
    return {
        "schema": "fixed-core-calibration-run-root-retention/v1",
        "status": "accepted",
        "execution_revision": revision,
        "archive_sha256": archive_digest,
        "inventory_sha256": _sha(inventory_data),
        "files": len(cast(list[object], baseline["files"])),
    }


def _git(repository: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ("git", *arguments), cwd=repository, check=False, capture_output=True
    )
    if result.returncode:
        reason = result.stderr.decode(errors="replace").strip()
        _refuse(f"Git command failed: {' '.join(arguments)}: {reason}")
    return result.stdout


def _tree(repository: Path, treeish: str) -> dict[str, tuple[str, str]]:
    rows = _git(repository, "ls-tree", "-r", "-z", treeish).split(b"\0")
    result: dict[str, tuple[str, str]] = {}
    for row in rows:
        if not row:
            continue
        try:
            header, raw_path = row.split(b"\t", 1)
            mode, kind, oid = header.decode("ascii").split(" ")
            path = raw_path.decode("utf-8")
        except (UnicodeDecodeError, ValueError) as error:
            raise RunSetRefusalError("Git tree entry is malformed") from error
        _relative(path, "Git source path")
        if path in result:
            _refuse(f"Git tree has duplicate path: {path}")
        # Submodules elsewhere in the repository do not enter the Python closure.
        if kind == "commit":
            continue
        if kind != "blob":
            _refuse(f"Git tree has unexpected object type: {path}")
        result[path] = (mode, _revision(oid, "Git blob ID"))
    return result


def _closure(repository: Path, entries: dict[str, tuple[str, str]]) -> tuple[str, ...]:
    roots = {
        "cases": "packing/cases",
        "devtools": "packing/devtools",
        "sqpack": "packing/src/sqpack",
    }

    def module_path(module: str) -> str | None:
        parts = module.split(".")
        root = roots.get(parts[0])
        if root is None:
            return None
        stem = "/".join((root, *parts[1:]))
        for candidate in (f"{stem}.py", f"{stem}/__init__.py"):
            if candidate in entries:
                return candidate
        return None

    pending = ["devtools.calibrate_fixed_core_packet"]
    visited: set[str] = set()
    paths = {FIXTURE_PATH, *RUNTIME_PATHS}
    while pending:
        module = pending.pop()
        if module in visited:
            continue
        path = module_path(module)
        if path is None:
            continue
        visited.add(module)
        paths.add(path)
        data = _git(repository, "cat-file", "blob", entries[path][1])
        try:
            tree = ast.parse(data.decode("utf-8"), filename=path)
        except (UnicodeDecodeError, SyntaxError) as error:
            raise RunSetRefusalError(f"source cannot be parsed: {path}") from error
        package = module if path.endswith("/__init__.py") else module.rpartition(".")[0]
        pending.extend(
            ".".join(module.split(".")[:length]) for length in range(1, len(module.split(".")))
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                pending.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    try:
                        base = importlib.util.resolve_name(f"{'.' * node.level}{base}", package)
                    except ImportError as error:
                        raise RunSetRefusalError(
                            f"invalid relative import in {path}"
                        ) from error
                if base:
                    pending.append(base)
                    pending.extend(f"{base}.{alias.name}" for alias in node.names)
    if not paths.issubset(entries):
        _refuse("Git tree omits required source or runtime declaration")
    return tuple(sorted(paths))


def verify_source_closure(
    *,
    repository: Path,
    run_root: Path,
    review_root: Path,
    execution_revision: str,
    candidate_tree: str,
) -> dict[str, object]:
    """Check the three receipts name one source closure; report candidate drift.

    The manifests must agree with each other and name exactly the execution
    revision's import closure. Their blob ids and digests are the runs' own record and
    are kept, not compared. Paths whose mode or blob differ between that revision's
    closure and `candidate_tree`'s, or that only one closure holds, are returned as
    `drift`: information for the evidence commit, never a refusal.
    """
    repository = _canonical_dir(repository, "repository")
    run_root, review_root = _roots(run_root, review_root)
    revision = _revision(execution_revision, "execution revision")
    candidate_tree = _revision(candidate_tree, "candidate tree")
    if run_root.is_relative_to(repository) or review_root.is_relative_to(repository):
        _refuse("external roots must be outside the repository")
    _baseline(run_root, review_root, revision)
    if (
        _git(repository, "rev-parse", "--verify", f"{revision}^{{commit}}").strip().decode()
        != revision
    ):
        _refuse("execution revision is not an exact commit")
    candidate_oid = (
        _git(repository, "rev-parse", "--verify", f"{candidate_tree}^{{tree}}").strip().decode()
    )
    _revision(candidate_oid, "candidate tree object")
    # These name the tree the evidence is committed as; they check the arguments, not
    # what changed since execution, which `drift` reports below.
    candidate_kind = _git(repository, "cat-file", "-t", candidate_tree).strip()
    if candidate_kind == b"commit":
        if _git(repository, "rev-parse", "HEAD").strip().decode() != candidate_tree:
            _refuse("committed candidate is not the current HEAD")
    elif candidate_kind != b"tree":
        _refuse("candidate must be a staged tree or committed revision")
    index_tree = _git(repository, "write-tree").strip().decode()
    if _revision(index_tree, "staged index tree") != candidate_oid:
        _refuse("candidate tree differs from the current staged index")
    execution_entries = _tree(repository, revision)
    candidate_entries = _tree(repository, candidate_oid)
    execution_paths = _closure(repository, execution_entries)
    candidate_paths = _closure(repository, candidate_entries)
    _, _, summary_runs = _summary(run_root, revision)
    manifests: list[list[dict[str, object]]] = []
    for order in RUN_ORDERS:
        receipt_data, receipt = _json_file(
            run_root / f"profile-{order}" / "result.json", "calibration receipt"
        )
        binding = _binding(
            summary_runs[order - 1]["calibration_receipt"],
            f"profile {order} summary receipt",
            path="result.json",
        )
        if binding["bytes"] != len(receipt_data) or binding["sha256"] != _sha(receipt_data):
            _refuse(f"profile {order} receipt differs from coordinator summary")
        sources = _object(
            receipt.get("sources"),
            {"implementation_revision", "manifest", "runtime"},
            "receipt sources",
        )
        if sources["implementation_revision"] != revision:
            _refuse(f"profile {order} source revision differs")
        rows = _array(sources["manifest"], "source manifest")
        manifest: list[dict[str, object]] = []
        for value in rows:
            row = _object(value, {"path", "git_blob", "sha256"}, "source manifest row")
            _relative(row["path"], "source manifest path")
            _revision(row["git_blob"], "source blob")
            _digest(row["sha256"], "source digest")
            manifest.append(row)
        if [row["path"] for row in manifest] != list(execution_paths):
            _refuse(f"profile {order} manifest differs from complete source closure")
        manifests.append(manifest)
    if manifests[0] != manifests[1] or manifests[0] != manifests[2]:
        _refuse("three profile source manifests disagree")
    drift = sorted(
        path
        for path in {*execution_paths, *candidate_paths}
        if execution_entries.get(path) != candidate_entries.get(path)
        or (path in execution_paths) != (path in candidate_paths)
    )
    return {
        "schema": CLOSURE_SCHEMA,
        "status": "accepted",
        "execution_revision": revision,
        "candidate_tree": candidate_oid,
        "sources": manifests[0],
        "drift": drift,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("snapshot", "read", "join", "retain", "source-closure"):
        command = commands.add_parser(name)
        command.add_argument("--run-root", required=True, type=Path)
        command.add_argument("--review-root", required=True, type=Path)
        command.add_argument("--expect-execution-revision", required=True)
        if name in ("read", "source-closure"):
            command.add_argument("--repository", required=True, type=Path)
        if name in ("read", "join"):
            command.add_argument("--expect-reader-revision", required=True)
        if name == "read":
            command.add_argument("--run-order", required=True, type=int, choices=RUN_ORDERS)
        if name == "retain":
            command.add_argument("--evidence-root", required=True, type=Path)
        if name == "source-closure":
            command.add_argument("--candidate-tree", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        common = {
            "run_root": args.run_root,
            "review_root": args.review_root,
            "execution_revision": args.expect_execution_revision,
        }
        if args.command == "snapshot":
            snapshot_run_root(**common)
            result: object = {
                "status": "accepted",
                "inventory_path": str(args.review_root / INVENTORY_NAME),
                "inventory_sha256": _sha(
                    _regular_bytes(args.review_root / INVENTORY_NAME, "run-root inventory")
                ),
            }
        elif args.command == "read":
            status = run_reader(
                **common,
                repository=args.repository,
                reader_revision=args.expect_reader_revision,
                run_order=args.run_order,
            )
            return 0 if status == 0 else 2
        elif args.command == "join":
            result = join_reader_proofs(**common, reader_revision=args.expect_reader_revision)
        elif args.command == "retain":
            result = retain_run_root(**common, evidence_root=args.evidence_root)
        else:
            result = verify_source_closure(
                **common, repository=args.repository, candidate_tree=args.candidate_tree
            )
    except (OSError, EOFError, tarfile.TarError, RunSetRefusalError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
