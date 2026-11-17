"""Hold every receipt and program to the kept bytes and to the digests frozen before them.

Usage: python -I -B l101_digests.py REVIEW_DIR OUT.json

Checks the six checker files against frozen/checker-frozen-digests.txt; the plan, its
facts, the base check receipt and the plan's two programs against
frozen/controls-plan-digest.txt; the frozen review text and the receipts at the freeze
against frozen/findings-frozen-digest.txt; and the programs_sha256 the check and controls
receipts record against the programs kept. Records the digest of every file it finds.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def listed(path: Path) -> dict[str, str]:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#") or not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        out[name.strip()] = digest
    return out


def main() -> int:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    problems = []
    checks = []

    def expect(label: str, path: Path, digest: str) -> None:
        actual = sha(path) if path.is_file() else None
        checks.append({"what": label, "file": str(path.relative_to(root)), "ok": actual == digest})
        if actual != digest:
            problems.append(f"{label}: {path.relative_to(root)}")

    for name, digest in listed(root / "frozen/checker-frozen-digests.txt").items():
        expect("checker frozen", root / "programs" / name, digest)
    for name, digest in listed(root / "frozen/controls-plan-digest.txt").items():
        expect("plan stated", root / name, digest)
    for name, digest in listed(root / "frozen/findings-frozen-digest.txt").items():
        if name.startswith("frozen/") and name != "frozen/review-2026-11-11-ozden-954.frozen.md":
            expect("list at the freeze", root / name, digest)
        else:
            expect("findings frozen", root / name, digest)
    for receipt in ("out/check-n179.json", "out/controls-n179.json"):
        recorded = json.loads((root / receipt).read_text(encoding="utf-8"))["programs_sha256"]
        for name, digest in recorded.items():
            expect(f"recorded by {receipt}", root / "programs" / name, digest)
    files = {
        str(p.relative_to(root)): sha(p)
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.name != Path(out).name and "__pycache__" not in p.parts
    }
    receipt = {
        "program": "l101_digests.py",
        "checks": checks,
        "problems": problems,
        "files": files,
        "verdict": "ALL_RECEIPTS_MATCH" if not problems else "MISMATCH",
    }
    Path(out).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
    print(receipt["verdict"], len(checks), "checks", problems)
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
