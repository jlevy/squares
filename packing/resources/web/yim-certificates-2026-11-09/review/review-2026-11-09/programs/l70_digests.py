"""Hold every L70 receipt to the programs that wrote it, and the checker to its freeze.

* Each receipt in out/ records program_digests; each must equal the program's
  current SHA-256 in programs/.
* The five checker files must equal the digests in frozen/checker-frozen-digests.txt.
* The controls plan(s) must equal the digests in frozen/controls-plan-digests.txt.
* Writes out/program-digests.json: the SHA-256 of every program, receipt and frozen file.

Usage: python -I l70_digests.py --root REVIEW_DIR
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def frozen_list(path: Path) -> dict[str, str]:
    out = {}
    if not path.exists():
        return out
    for line in path.read_text().splitlines():
        parts = line.split()
        if len(parts) == 2 and len(parts[0]) == 64:
            out[parts[1]] = parts[0]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ns = ap.parse_args()
    root = Path(ns.root)
    progs = {p.name: sha(p) for p in sorted((root / "programs").iterdir()) if p.is_file()}
    problems = []
    receipts = {}
    for r in sorted((root / "out").glob("*.json")):
        if r.name == "program-digests.json":
            continue
        receipts[r.name] = sha(r)
        try:
            d = json.loads(r.read_text())
        except json.JSONDecodeError:
            problems.append(f"{r.name}: not JSON")
            continue
        for name, digest in (d.get("program_digests") or {}).items():
            if progs.get(name) != digest:
                problems.append(f"{r.name}: {name} recorded {digest[:12]}, now {str(progs.get(name))[:12]}")
    for fl in ("checker-frozen-digests.txt", "controls-plan-digests.txt"):
        for rel, digest in frozen_list(root / "frozen" / fl).items():
            p = root / rel
            if not p.exists() or sha(p) != digest:
                problems.append(f"{fl}: {rel} differs from its frozen digest")
    frozen = {p.name: sha(p) for p in sorted((root / "frozen").iterdir()) if p.is_file()}
    out = {
        "program": "l70_digests.py",
        "programs": progs,
        "receipts": receipts,
        "frozen": frozen,
        "problems": problems,
        "verdict": "ALL_RECEIPTS_MATCH" if not problems else "MISMATCH",
    }
    (root / "out" / "program-digests.json").write_text(json.dumps(out, indent=1) + "\n")
    print(out["verdict"], len(receipts), "receipts", len(progs), "programs")
    for p in problems:
        print("  ", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
