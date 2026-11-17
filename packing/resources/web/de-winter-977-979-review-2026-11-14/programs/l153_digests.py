"""Lane L153, after the freeze: every frozen digest against the kept bytes.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review. It decides nothing about the bounds.

It reads each list in `frozen/`, checks every digest whose file is in this directory,
and lists the SHA-256 of every file here.

Usage: l153_digests.py PACKET_DIR OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    root = Path(argv[1])
    out_path = Path(argv[2])
    checked = []
    bad = []
    skipped = []
    for lst in sorted((root / "frozen").glob("*.txt")):
        for line in lst.read_text().splitlines():
            if not line or line.startswith("#"):
                continue
            digest, name = line.split(None, 1)
            name = name.strip()
            candidates = [root / name, root / "programs" / name]
            path = next((p for p in candidates if p.is_file()), None)
            if path is None:
                skipped.append([lst.name, name])
                continue
            ok = hashlib.sha256(path.read_bytes()).hexdigest() == digest
            checked.append([lst.name, name, ok])
            if not ok:
                bad.append([lst.name, name])
    files = {
        str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file() and p != out_path and "__pycache__" not in p.parts
    }
    verdict = "ALL_FROZEN_DIGESTS_HOLD" if not bad else "SOME_FROZEN_DIGEST_DIFFERS"
    out_path.write_text(
        json.dumps(
            {
                "program": "l153_digests.py",
                "verdict": verdict,
                "checked": checked,
                "not_in_this_directory": skipped,
                "files": files,
            },
            indent=1,
        )
        + "\n"
    )
    print(verdict, len(checked), "checked,", len(skipped), "outside this directory")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
