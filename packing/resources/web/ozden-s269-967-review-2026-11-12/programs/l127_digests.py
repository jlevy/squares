"""Check every frozen digest against the kept bytes, and list every file's digest.

Lane L127, clean room; decides nothing. Usage: python -I -B l127_digests.py PACKET_DIR OUT.json

Each line `HEX  PATH` of the three lists under frozen/ is checked: PATH relative to the
packet, or to programs/ for the checker list, whose paths are bare file names.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(argv: list[str]) -> int:
    root, outp = Path(argv[1]), Path(argv[2])
    checks = []
    for name in ("checker-frozen-digests.txt", "controls-plan-digest.txt", "findings-frozen-digest.txt"):
        for line in (root / "frozen" / name).read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            hexd, path = line.split(None, 1)
            p = root / path
            if not p.exists():
                p = root / "programs" / path
            checks.append({"list": name, "path": path, "holds": p.exists() and sha(p) == hexd})
    files = {
        str(p.relative_to(root)): sha(p)
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.name != outp.name and "__pycache__" not in p.parts
    }
    ok = all(c["holds"] for c in checks)
    out = {
        "program": "l127_digests.py",
        "verdict": "ALL_FROZEN_DIGESTS_HOLD" if ok else "A_FROZEN_DIGEST_DOES_NOT_HOLD",
        "checked": len(checks),
        "failures": [c for c in checks if not c["holds"]],
        "files": files,
    }
    outp.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(out["verdict"], len(checks), "digests checked,", len(files), "files listed")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
