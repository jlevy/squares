"""Lane L159's digest check: every frozen digest against the kept bytes.

Written after the findings were frozen, for the stage 4 review of issue #983; decides
nothing about the certificate. It reads the three frozen digest lists of this packet,
checks every digest they hold against the file it names, lists the SHA-256 of every
file here, and, given a directory where the frozen chain was rerun, compares each
rerun receipt with the kept one, key for key except CPU seconds, and the rerun plan
with the kept plan byte for byte.

Usage: l159_digests.py PACKET OUT.json [RERUN_DIR]
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

LISTS = ("frozen/checker-frozen-digests.txt", "frozen/controls-plan-digest.txt", "frozen/findings-frozen-digest.txt")
RECEIPTS = ("selftest.json", "check-n228.json", "plan-facts-n228.json", "controls-n228.json", "describe-n228.json")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strip_cpu(value: object) -> object:
    if isinstance(value, dict):
        return {k: strip_cpu(v) for k, v in value.items() if k != "cpu_seconds"}
    if isinstance(value, list):
        return [strip_cpu(v) for v in value]
    return value


def main(argv: list[str]) -> int:
    root = Path(argv[1])
    out_path = Path(argv[2])
    rerun = Path(argv[3]) if len(argv) > 3 else None
    checked = []
    ok = True
    for name in LISTS:
        for line in (root / name).read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            digest, rel = line.split(maxsplit=1)
            target = root / rel
            if not target.exists():
                target = root / "programs" / rel
            holds = target.exists() and sha(target) == digest
            ok &= holds
            checked.append({"list": name, "file": rel, "holds": holds})
    out: dict[str, object] = {
        "program": "l159_digests.py",
        "verdict": "ALL_FROZEN_DIGESTS_HOLD" if ok else "SOME_FROZEN_DIGEST_DIFFERS",
        "checked": checked,
        "files": {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file() and p.name != out_path.name},
    }
    if rerun is not None:
        same = {}
        for name in RECEIPTS:
            kept = json.loads((root / "out" / name).read_text(encoding="utf-8"))
            again = json.loads((rerun / name).read_text(encoding="utf-8"))
            same[name] = strip_cpu(kept) == strip_cpu(again)
        same["controls-plan.json (bytes)"] = sha(root / "programs" / "controls-plan.json") == sha(rerun / "controls-plan.json")
        out["rerun_reproduces"] = same
        out["rerun_verdict"] = "RERUN_REPRODUCES_EVERY_RECEIPT" if all(same.values()) else "RERUN_DIFFERS"
    out_path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(out["verdict"], len(checked), "digests;", out.get("rerun_verdict"), out.get("rerun_reproduces"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
