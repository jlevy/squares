"""Reconcile the retained native n11 receipt, journal, premises and Git provenance.

This is not an interval-coverage replay or another confirmation method. The
receipt and journal are related outputs of one historical execution; matching
them cannot authenticate coordinated invented data. Git identity establishes
which unchanged proof implementation the retained run can be reused with.

Run from packing with ``python -m devtools.audit_kleddamag_n11_native``. The
normal quick test lane performs the same reconciliation. ``--output`` retains
its findings without changing the immutable coverage receipt or row journal.
"""

from __future__ import annotations

import argparse
import ast
import json
import math
import subprocess
from dataclasses import dataclass
from math import ceil
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools.verify_kleddamag_n11_native import REPO, REVIEWED_SHA256, SOURCE
from sqpack.fractional.parent_core import load_kleddamag_parent_core, validate_parent_core
from sqpack.fractional.threshold_interval import ThresholdAtomData

PROOF_COMMIT = "c183cc9abe93eedcb268a5390cdd1cdc6e7bbb39"
RECEIPT = REPO / "packing/campaign/agent-sessions/session-153-native-full.json"
JOURNAL = RECEIPT.with_suffix(".rows.jsonl")
RECONCILIATION = RECEIPT.with_name("session-153-native-reconciliation.json")
MAX_DOCUMENT_BYTES = 16 * 1024 * 1024

# The frozen CLI's complete local import closure, including package initializers.
# certificate.py imports sweep.py for other APIs; native coverage does not call
# that sweep. Keeping the whole imported file is a conservative reuse boundary.
# Third-party and interpreter requirements are bound through the locked project.
PROOF_INPUTS = (
    "packing/devtools/__init__.py",
    "packing/devtools/verify_kleddamag_n11_native.py",
    "packing/src/sqpack/__init__.py",
    "packing/src/sqpack/field.py",
    "packing/src/sqpack/verify.py",
    "packing/src/sqpack/workers.py",
    "packing/src/sqpack/fractional/__init__.py",
    "packing/src/sqpack/fractional/certificate.py",
    "packing/src/sqpack/fractional/corner_clip.py",
    "packing/src/sqpack/fractional/model.py",
    "packing/src/sqpack/fractional/sweep.py",
    "packing/src/sqpack/fractional/threshold.py",
    "packing/src/sqpack/fractional/interval.py",
    "packing/src/sqpack/fractional/threshold_interval.py",
    "packing/src/sqpack/fractional/parent_core.py",
    "packing/src/sqpack/fractional/parent_core_interval.py",
    "packing/.python-version",
    "packing/pyproject.toml",
    "packing/uv.lock",
)


def _require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def _git(repository: Path, *arguments: str) -> bytes:
    return subprocess.run(
        ["git", *arguments], cwd=repository, check=True, capture_output=True
    ).stdout


def check_proof_code(
    repository: Path = REPO,
    *,
    revision: str = PROOF_COMMIT,
    paths: tuple[str, ...] = PROOF_INPUTS,
) -> tuple[dict[str, str], ...]:
    """Compare current proof inputs to their historical Git blobs, including dirt."""
    _git(repository, "merge-base", "--is-ancestor", revision, "HEAD")
    manifest: list[dict[str, str]] = []
    for relative in paths:
        frozen = _git(repository, "cat-file", "blob", f"{revision}:{relative}")
        _require(
            (repository / relative).read_bytes() == frozen,
            f"proof input differs from frozen Git blob: {relative}",
        )
        blob = _git(repository, "rev-parse", f"{revision}:{relative}").decode().strip()
        manifest.append({"path": relative, "git_blob": blob})
    return tuple(manifest)


def check_import_inventory(repository: Path = REPO) -> None:
    """Refuse an omitted local import or package initializer in the frozen inventory."""
    paths = set(PROOF_INPUTS)
    for relative in PROOF_INPUTS:
        if not relative.endswith(".py"):
            continue
        source = _git(repository, "cat-file", "blob", f"{PROOF_COMMIT}:{relative}")
        for node in ast.walk(ast.parse(source)):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                _require(
                    node.level == 0, "frozen import inventory needs relative-import review"
                )
                if node.module is not None:
                    names = [node.module]
            for name in names:
                package = name.split(".")[0]
                if package not in ("sqpack", "devtools"):
                    continue
                prefix = "packing/src/" if package == "sqpack" else "packing/"
                module = prefix + name.replace(".", "/")
                _require(
                    module + ".py" in paths or module + "/__init__.py" in paths,
                    f"local import missing from frozen inventory: {name}",
                )
                parent = Path(module).parent
                while parent.as_posix() != prefix.rstrip("/"):
                    _require(
                        (parent / "__init__.py").as_posix() in paths,
                        f"package initializer missing from frozen inventory: {parent}",
                    )
                    parent = parent.parent


@dataclass(frozen=True, slots=True)
class ReceiptContext:
    expected: dict[str, Any]
    proof_inputs: tuple[dict[str, str], ...]
    python_version: str
    counting_gap: str


def prepare_context(repository: Path = REPO) -> ReceiptContext:
    """Recompute exact premises and resource dimensions without any coverage search."""
    manifest = check_proof_code(repository)
    check_import_inventory(repository)
    source = repository / SOURCE.relative_to(REPO)
    certificate = load_kleddamag_parent_core(source, expected_sha256=REVIEWED_SHA256)
    premises = validate_parent_core(certificate)
    data = ThresholdAtomData.of(certificate, batch_size=2048)
    return ReceiptContext(
        expected={
            "schema": "NativeParentCoreIntervalReceipt/v1",
            "method": "directed-rounding box branch-and-bound with direct threshold counts",
            "bound": str(certificate.outer_side / certificate.parent_side),
            "parent_side": str(certificate.parent_side),
            "minimum_charge": str(certificate.minimum_charge),
            "budget": str(certificate.budget),
            "scale": data.scale,
            "threshold_units": ceil(certificate.minimum_charge * data.scale),
            "catalogue_rows": len(certificate.rows),
            "premises": {
                "budget": str(premises.budget),
                "minimum_containment_numerator": str(premises.minimum_containment_numerator),
                "final_half_tangent": str(premises.final_half_tangent),
                "rows": premises.rows,
            },
            "batch": {
                "boxes": 2048,
                "workers": 2,
                "sites": len(data.sites.xlo),
                "features": len(data.members),
                "member_slots": data.members.size,
                "site_mask_bytes": 2048 * len(data.sites.xlo),
                "gathered_member_bytes": 2048 * data.members.size,
                "int16_count_bytes": 2048 * len(data.members) * 2,
            },
        },
        proof_inputs=manifest,
        python_version=(repository / "packing/.python-version").read_text().strip(),
        counting_gap=str(certificate.n * certificate.minimum_charge - certificate.budget),
    )


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        _require(key not in result, f"duplicate receipt key: {key}")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def _read(path: Path) -> str:
    with path.open("rb") as stream:
        data = stream.read(MAX_DOCUMENT_BYTES + 1)
    _require(len(data) <= MAX_DOCUMENT_BYTES, "receipt or journal exceeds 16 MiB")
    return data.decode("utf-8")


def read_documents(
    receipt: Path = RECEIPT, journal: Path = JOURNAL
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Read bounded, duplicate-free JSON artifacts without interpreting their claims."""
    document = json.loads(
        _read(receipt), object_pairs_hook=_unique_object, parse_constant=_invalid_constant
    )
    entries = [
        json.loads(line, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
        for line in _read(journal).splitlines()
    ]
    if not isinstance(document, dict):
        raise TypeError("receipt must be an object")
    if not entries or not all(isinstance(row, dict) for row in entries):
        raise ValueError("invalid journal")
    return document, entries


def _same_json(left: object, right: object) -> bool:
    # Python equality conflates bool/int and int/float; JSON preserves those types.
    return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(
        right, sort_keys=True, allow_nan=False
    )


def _integer(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be a nonnegative exact integer")
    return value


def reconcile(
    receipt: dict[str, Any], journal: list[dict[str, Any]], context: ReceiptContext
) -> dict[str, Any]:
    """Check agreement and complete recorded coverage; never rerun or authenticate it."""
    for field, expected in context.expected.items():
        _require(
            _same_json(receipt.get(field), expected), f"receipt {field} disagrees with source"
        )
    _require(receipt.get("status") == "PASS_COMPLETE", "receipt is not PASS_COMPLETE")
    _require(
        receipt.get("complete") is True and receipt.get("accepted") is True, "not accepted"
    )
    _require(receipt.get("refutations") == [], "receipt contains refutations")
    provenance = receipt.get("provenance")
    if not isinstance(provenance, dict):
        raise TypeError("missing provenance")
    _require(provenance.get("git_commit") == PROOF_COMMIT, "unexpected proof commit")
    _require(provenance.get("dirty") is False, "proof source was dirty")
    _require(provenance.get("certificate_sha256") == REVIEWED_SHA256, "wrong source identity")
    python = provenance.get("python")
    _require(
        isinstance(python, str) and python.startswith(context.python_version + " "),
        "proof interpreter disagrees with frozen pin",
    )
    count = context.expected["catalogue_rows"]
    rows = receipt.get("rows")
    if not isinstance(rows, list) or len(rows) != count:
        raise ValueError("incomplete row inventory")
    threshold = context.expected["threshold_units"]
    boxes = 0
    least: int | None = None
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise TypeError("row must be an object")
        _require(
            _integer(row.get("index"), "row index") == index, "wrong row order or identity"
        )
        _require(row.get("label") == str(index), "wrong row label")
        _require(row.get("status") == "certified", f"row {index} is not certified")
        _require(_integer(row.get("stalled"), "stalled") == 0, f"row {index} has stalls")
        _require(row.get("budget_exhausted") is False, f"row {index} exhausted its budget")
        lower = _integer(row.get("lower"), "lower bound")
        _require(lower >= threshold, f"row {index} is below Gamma")
        least = lower if least is None else min(least, lower)
        boxes += _integer(row.get("boxes"), "box count")
        seconds = row.get("seconds")
        _require(
            isinstance(seconds, (int, float))
            and not isinstance(seconds, bool)
            and math.isfinite(seconds)
            and seconds >= 0,
            f"row {index} has invalid elapsed time",
        )
    _require(len(journal) == count + 1, "incomplete row journal")
    header = journal[0]
    _require(
        header.get("schema") == "NativeParentCoreRowJournal/v1"
        and header.get("status") == "INCOMPLETE_ROW_JOURNAL",
        "invalid journal header",
    )
    _require(_same_json(header.get("provenance"), provenance), "journal provenance mismatch")
    _require(
        _same_json(header.get("selected_rows"), list(range(count))),
        "journal did not select every row",
    )
    _require(
        _same_json(header.get("batch_size"), 2048) and _same_json(header.get("workers"), 2),
        "journal resource configuration mismatch",
    )
    _require(_same_json(rows, journal[1:]), "journal rows differ from final receipt")
    return {
        "schema": "NativeParentCoreReceiptReconciliation/v1",
        "status": "RECONCILED_RECEIPT_NOT_COVERAGE_REPLAY",
        "coverage_replayed": False,
        "additional_confirmation_method": False,
        "proof_commit": PROOF_COMMIT,
        "certificate_sha256": REVIEWED_SHA256,
        "proof_inputs": context.proof_inputs,
        "rows_reconciled": count,
        "minimum_recorded_lower_units": least,
        "threshold_units": threshold,
        "total_recorded_boxes": boxes,
        "counting_gap": context.counting_gap,
        "exact_premises": context.expected["premises"],
        "limitations": [
            (
                "Receipt and journal are related outputs of one historical execution; "
                "matching cannot authenticate coordinated invented data."
            ),
            (
                "Git identity establishes unchanged proof inputs, not historical execution. "
                "Coverage evidence remains the original complete run and its reviewed method."
            ),
            (
                "The pinned runtime describes the original run; this reconciliation may run "
                "on another supported host and does not reproduce its memory or timing."
            ),
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, default=RECEIPT)
    parser.add_argument("--journal", type=Path, default=JOURNAL)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        context = prepare_context()
        result = reconcile(*read_documents(args.receipt, args.journal), context)
        if args.output is not None:
            with atomic_output_file(args.output, make_parents=True) as temporary:
                temporary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"receipt reconciliation refused: {error}\n")
    print(
        f"{result['status']}: {result['rows_reconciled']} rows; exact premises and "
        f"{len(context.proof_inputs)} frozen Git inputs agree"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
