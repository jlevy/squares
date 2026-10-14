"""Hold sq17-lean's own manifest and receipts to each other and to a checkout of the pin.

Reads, as data, the packet's retained ``manifest.json.gz``, ``clean-build-receipt.json``
and verification logs, and a checkout of ``ofitzharding/sq17-lean`` at the pin; runs
nothing from either. Prints one JSON object:

- every source module ``manifest.json`` lists outside the release archives, and every
  root file it lists, compared by size and SHA-256 with the checkout's file;
- the three release archives, with the size, SHA-256 and member count it records, and how
  many modules it assigns to each: both counts are ``manifest.json``'s own, and no
  archive is opened here;
- the axiom report: its SHA-256 against the receipt's ``final_log_sha256``, the theorem it
  is for, the standard axioms, the count of ``native_decide`` facts against the receipt's,
  and whether ``sorryAx`` or any other axiom appears;
- the two control logs against the receipt's digests.

Usage, with the project interpreter and ``-I``::

    python3 -I check_source_manifest.py PACKET CHECKOUT
"""

from __future__ import annotations

import collections
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

STANDARD = ("propext", "Classical.choice", "Quot.sound")
NATIVE = re.compile(r"\._native\.native_decide\.ax_\d+_\d+$")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def axiom_report(log: bytes) -> dict[str, object]:
    text = log.decode("utf-8")
    head, _, rest = text.partition(" depends on axioms: [")
    listed, _, tail = rest.partition("]")
    axioms = [name.strip() for name in listed.split(",") if name.strip()]
    native = [name for name in axioms if NATIVE.search(name)]
    other = [name for name in axioms if name not in STANDARD and not NATIVE.search(name)]
    return {
        "theorem": head.strip().strip("'"),
        "axioms_listed": len(axioms),
        "standard_axioms": [name for name in STANDARD if name in axioms],
        "native_decide_facts": len(native),
        "distinct_native_decide_facts": len(set(native)),
        "other_axioms": other,
        "sorryAx_anywhere": "sorryAx" in text,
        "statement_line": tail.strip(),
    }


def main(packet: Path, checkout: Path) -> dict[str, object]:
    source = packet / "sq17-lean"
    manifest = json.loads(gzip.decompress((source / "manifest.json.gz").read_bytes()))
    receipt = json.loads((source / "verification/clean-build-receipt.json").read_bytes())
    log = gzip.decompress((source / "verification/Square17Optimality.log.gz").read_bytes())

    in_tree = {path: entry for path, entry in manifest["sources"].items() if entry["archive"] is None}
    mismatched = [
        path
        for path, entry in sorted(in_tree.items())
        if not (checkout / path).is_file()
        or sha256(data := (checkout / path).read_bytes()) != entry["sha256"]
        or len(data) != entry["bytes"]
    ]
    root_mismatched = [
        path
        for path, entry in sorted(manifest["files"].items())
        if sha256(data := (checkout / path).read_bytes()) != entry["sha256"]
        or len(data) != entry["bytes"]
    ]
    tracked = sorted(
        path.relative_to(checkout).as_posix()
        for path in (checkout / "Sq17Lean").rglob("*.lean")
    )
    per_archive = collections.Counter(entry["archive"] for entry in manifest["sources"].values())
    archives = [
        {
            "name": name,
            "bytes": entry["bytes"],
            "sha256": entry["sha256"],
            "format": entry["format"],
            "members": entry["members"],
            "modules_assigned": per_archive[name],
            "module_bytes": sum(
                item["bytes"] for item in manifest["sources"].values() if item["archive"] == name
            ),
        }
        for name, entry in sorted(manifest["archives"].items())
    ]
    controls = {
        name: {
            "exit_code": value["exit_code"],
            "log_sha256_matches_receipt": sha256(
                (source / f"verification/{name}.log").read_bytes()
            )
            == value["log_sha256"],
        }
        for name, value in sorted(receipt["controls"].items())
    }
    report = axiom_report(log)
    return {
        "format": "sq17-lean-source-consistency-v1",
        "manifest_schema": manifest["schema"],
        "manifest_status": manifest["status"],
        "manifest_entry": manifest["entry"],
        "manifest_counts": manifest["counts"],
        "source_modules_listed": len(manifest["sources"]),
        "validation_only": sorted(
            path for path, entry in manifest["sources"].items() if entry.get("validationOnly")
        ),
        "in_tree_modules_listed": len(in_tree),
        "lean_files_in_checkout": len(tracked),
        "in_tree_listed_equals_checkout_lean_files": sorted(in_tree) == tracked,
        "in_tree_modules_mismatched": mismatched,
        "root_files_listed": sorted(manifest["files"]),
        "root_files_mismatched": root_mismatched,
        "archives": archives,
        "archive_bytes_total": sum(entry["bytes"] for entry in archives),
        "axiom_report": {
            **report,
            "log_sha256": sha256(log),
            "log_sha256_matches_receipt": sha256(log) == receipt["final_log_sha256"],
            "native_decide_facts_match_receipt": report["native_decide_facts"]
            == receipt["native_decide_facts"],
            "standard_axioms_match_receipt": report["standard_axioms"]
            == receipt["standard_axioms"],
        },
        "receipt_status": receipt["status"],
        "receipt_modules_rebuilt": receipt["project_modules_rebuilt"],
        "controls": controls,
    }


if __name__ == "__main__":
    print(json.dumps(main(Path(sys.argv[1]), Path(sys.argv[2])), indent=2, ensure_ascii=False))
