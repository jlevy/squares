"""Lane L117, after the freeze: every frozen digest against the kept bytes. Decides nothing.

Reads the three frozen digest lists, checks each listed SHA-256 against the file it
names (the checker list names programs relative to programs/, the others relative to
this directory), and lists the SHA-256 of every file in the directory.

Usage: python -I -B l117_digests.py PACKET_DIR OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import sys


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main(argv: list[str]) -> int:
    root, opath = argv[1], argv[2]
    checks = []
    for name, base in (("checker-frozen-digests.txt", "programs"), ("controls-plan-digest.txt", "."),
                       ("findings-frozen-digest.txt", ".")):
        with open(os.path.join(root, "frozen", name), encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("#") or not line.strip():
                    continue
                digest, rel = line.split()
                path = os.path.join(root, rel) if "/" in rel else os.path.join(root, base, rel)
                checks.append({"list": name, "file": os.path.relpath(path, root), "holds": sha(path) == digest})
    files = {}
    for d, _, fs in os.walk(root):
        for f in sorted(fs):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, root)
            if rel != os.path.relpath(opath, root):
                files[rel] = sha(p)
    ok = all(c["holds"] for c in checks)
    out = {"program": "l117_digests.py", "verdict": "ALL_FROZEN_DIGESTS_HOLD" if ok else "A_FROZEN_DIGEST_FAILS",
           "checked": len(checks), "checks": checks, "files": dict(sorted(files.items()))}
    with open(opath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(out["verdict"], len(checks), "digests checked,", len(files), "files listed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
