"""Record one screened class with the native kernel, then verify every node.

Run from packing with its venv interpreter. The output directory must be new;
it holds certificate/, search.json, verification.json, logs, and run.json.
The native extension must already be built for the host Python/platform.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CLASSES = {
    "C1": "side-S0,side-N0,interior-SW,interior-NW,interior-W,interior-S,interior-SE",
    "C2": "side-S0,side-W0,interior-SW,interior-NW,interior-W,interior-S,interior-SE",
}


def _write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    temporary = path.with_suffix(".tmp")
    _ = temporary.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    _ = temporary.replace(path)


def _step(command: list[str], log: Path) -> dict[str, Any]:
    started = datetime.now(UTC).isoformat()
    clock = time.perf_counter()
    with log.open("w", encoding="utf-8") as stream:
        process = subprocess.run(
            command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=False
        )
    return {
        "command": command,
        "cwd": str(ROOT),
        "started_at": started,
        "finished_at": datetime.now(UTC).isoformat(),
        "wall_seconds": time.perf_counter() - clock,
        "returncode": process.returncode,
        "log": str(log),
    }


def run(label: str, native_dir: Path, output: Path, max_seconds: float) -> int:
    """Write durable stage receipts; succeed only on a full verifier PASS."""
    native_dir, output = native_dir.resolve(), output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    certificate = output / "certificate"
    receipt_path = output / "run.json"
    receipt: dict[str, Any] = {
        "class": label,
        "cells": CLASSES[label].split(","),
        "native_dir": str(native_dir),
        "status": "RUNNING",
        "started_at": datetime.now(UTC).isoformat(),
    }
    _write_receipt(receipt_path, receipt)
    clock = time.perf_counter()
    try:
        search = _step(
            [
                sys.executable,
                "-m",
                "devtools.n17_bb_native",
                "--native-dir",
                str(native_dir),
                "--cells",
                CLASSES[label],
                "--label",
                label,
                "--max-seconds",
                str(max_seconds),
                "--save-certificate",
                str(certificate),
                "--output",
                str(output / "search.json"),
                "--progress",
            ],
            output / "search.log",
        )
        receipt["search"] = search
        _write_receipt(receipt_path, receipt)
        if search["returncode"] != 0:
            receipt["status"] = "SEARCH_FAILED"
            return 1
        verification = _step(
            [
                sys.executable,
                "-m",
                "devtools.verify_n17_bb_certificate",
                str(certificate),
                "--output",
                str(output / "verification.json"),
                "--progress",
            ],
            output / "verification.log",
        )
        receipt["verification"] = verification
        if verification["returncode"] != 0:
            receipt["status"] = "VERIFICATION_FAILED"
            return 1
        checked = json.loads((output / "verification.json").read_text(encoding="utf-8"))
        if checked.get("status") != "PASS" or checked.get("mode") != "full":
            receipt["status"] = "VERIFICATION_FAILED"
            return 1
        receipt["certificate"] = checked["certificate"]
        receipt["status"] = "PASS"
    except (Exception, KeyboardInterrupt) as error:
        receipt["status"] = "ERROR"
        receipt["error"] = f"{type(error).__name__}: {error}"
        raise
    else:
        return 0
    finally:
        receipt["finished_at"] = datetime.now(UTC).isoformat()
        receipt["wall_seconds"] = time.perf_counter() - clock
        _write_receipt(receipt_path, receipt)
        print(json.dumps({"receipt": str(receipt_path), "status": receipt["status"]}))


def main(argv: list[str] | None = None) -> int:
    """Run C1 or C2 without silently accepting a budget-exhausted search."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("class_name", choices=CLASSES)
    _ = parser.add_argument("--native-dir", type=Path, required=True)
    _ = parser.add_argument("--output", type=Path, required=True, help="new run directory")
    _ = parser.add_argument("--max-seconds", type=float, default=86400.0)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("--max-seconds must be finite and positive")
    return run(args.class_name, args.native_dir, args.output, args.max_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
