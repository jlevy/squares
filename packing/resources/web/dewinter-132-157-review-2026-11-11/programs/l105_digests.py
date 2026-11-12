"""Lane L105: hold every program and receipt to the kept bytes and the frozen lists.

Usage: python -I -B l105_digests.py PACKET_DIR OUT_JSON

Decides nothing. For each receipt in out/ that names programs (`program_sha256`), it
checks that each named program's kept bytes have that digest. It checks every line of
frozen/checker-frozen-digests.txt, frozen/controls-plan-digest.txt and
frozen/findings-frozen-digest.txt against the kept files: the checker files and the plan
must be unchanged; a receipt listed at the findings freeze must be unchanged unless it is
one a later program rewrote (none of the frozen deciders' receipts may be).
Prints ALL_RECEIPTS_MATCH or the mismatches.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def frozen_lines(path: Path) -> list[tuple[str, str]]:
    out = []
    for line in path.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        digest, name = line.split(None, 1)
        out.append((digest, name.strip()))
    return out


def main() -> None:
    root, outp = Path(sys.argv[1]), Path(sys.argv[2])
    problems: list[str] = []
    receipts = {}
    for r in sorted((root / "out").glob("*.json")):
        if r.name == outp.name:
            continue
        data = json.loads(r.read_text())
        named = data.get("program_sha256") or {}
        ok = all(sha(root / "programs" / p) == d for p, d in named.items())
        receipts[r.name] = {"sha256": sha(r), "programs_named": len(named), "programs_match": ok}
        if not ok:
            problems.append(f"{r.name}: a named program changed")
    frozen = {}
    for name, base in (
        ("checker-frozen-digests.txt", root / "programs"),
        ("controls-plan-digest.txt", root),
        ("findings-frozen-digest.txt", root),
    ):
        rows = []
        for digest, rel in frozen_lines(root / "frozen" / name):
            p = base / rel
            now = sha(p) if p.exists() else None
            rows.append({"file": rel, "frozen": digest, "now_equal": now == digest})
            if now != digest:
                problems.append(f"{name}: {rel} differs from its frozen digest")
        frozen[name] = {"sha256": sha(root / "frozen" / name), "lines": len(rows), "all_equal": all(r["now_equal"] for r in rows), "rows": rows}
    programs = {q.name: sha(q) for q in sorted((root / "programs").iterdir()) if q.is_file()}
    out = {
        "program": "l105_digests.py",
        "programs": programs,
        "receipts": receipts,
        "frozen_lists": frozen,
        "status": "ALL_RECEIPTS_MATCH" if not problems else "MISMATCH",
        "problems": problems,
    }
    outp.write_text(json.dumps(out, indent=1) + "\n")
    print(out["status"], len(receipts), "receipts", problems)


if __name__ == "__main__":
    main()
