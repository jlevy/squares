"""Hold every receipt to the kept programs, and the frozen files to their digests (review L83).

Usage: python -I -B l83_digests.py REVIEW_DIR OUT.json

REVIEW_DIR holds programs/, frozen/ and out*/ directories. Each receipt records the
SHA-256 of every l83_*.py beside the program that wrote it; each must equal the kept
bytes. The plan facts were written before the plan and are held to the plan's frozen
list instead.
"""

import hashlib
import json
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def frozen(path: Path) -> dict:
    out = {}
    for line in path.read_text().splitlines():
        if line and not line.startswith("#"):
            digest, name = line.split()
            out[name] = digest
    return out


def main(argv):
    root, out = Path(argv[1]), Path(argv[2])
    progs = root / "programs"
    kept = {p.name: sha(p) for p in sorted(progs.glob("l83_*.py"))}
    problems = []
    checker = frozen(root / "frozen/checker-frozen-digests.txt")
    for name, digest in checker.items():
        if kept.get(name) != digest:
            problems.append(f"checker file {name} differs from its frozen digest")
    plan = frozen(root / "frozen/controls-plan-digest.txt")
    receipts = sorted(p for p in root.glob("out*/*.json") if p.name != out.name)
    for name, digest in plan.items():
        hits = [p for p in [progs / name, *receipts] if p.name == name and p.exists()]
        if not hits or any(sha(p) != digest for p in hits):
            problems.append(f"plan file {name} differs from its frozen digest")
    held = 0
    for p in receipts:
        if p.name.startswith("plan-facts-"):
            continue
        doc = json.loads(p.read_text())
        recorded = doc.get("programs")
        if not recorded:
            problems.append(f"{p.parent.name}/{p.name} records no program digests")
            continue
        for name, digest in recorded.items():
            if kept.get(name) != digest:
                problems.append(f"{p.parent.name}/{p.name}: {name} recorded {digest[:12]}, kept {kept.get(name, 'missing')[:12]}")
        held += 1
    doc = {
        "verdict": "ALL_RECEIPTS_MATCH" if not problems else "MISMATCH",
        "receipts_held": held,
        "kept_programs": kept,
        "problems": problems,
    }
    out.write_text(json.dumps(doc, indent=1) + "\n")
    print(doc["verdict"], "receipts", held, "problems", len(problems))
    for line in problems[:20]:
        print(" ", line)
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
