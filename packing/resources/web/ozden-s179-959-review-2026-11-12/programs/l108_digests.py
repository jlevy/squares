"""Hold every program and receipt to the kept bytes and to the frozen digest lists.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen; decides nothing. Checks each line of the three frozen lists against the file it
names, then writes the SHA-256 of every file under programs/, out/ and frozen/.

Usage: python -I -B l108_digests.py PACKET_DIR OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str]) -> int:
    root = Path(argv[1])
    checks = []
    for listing, base in (
        ("frozen/checker-frozen-digests.txt", "programs"),
        ("frozen/controls-plan-digest.txt", "."),
        ("frozen/findings-frozen-digest.txt", "."),
    ):
        section_base = base
        for line in (root / listing).read_text(encoding="utf-8").splitlines():
            if line.startswith("# receipts written by the frozen checker"):
                section_base = "."
            if not line or line.startswith("#"):
                continue
            digest, name = line.split(maxsplit=1)
            path = root / section_base / name
            checks.append({"list": listing, "file": str(Path(section_base) / name), "holds": path.exists() and sha(path) == digest})
    files = {str(p.relative_to(root)): sha(p) for p in sorted(root.rglob("*")) if p.is_file() and p.name != Path(argv[2]).name}
    ok = all(c["holds"] for c in checks)
    out = {"program": "l108_digests.py", "frozen_lines_checked": len(checks), "every_frozen_digest_holds": ok, "checks": checks, "files": files}
    Path(argv[2]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("ALL_FROZEN_DIGESTS_HOLD" if ok else "SOME_FROZEN_DIGEST_DIFFERS", len(checks), "lines;", len(files), "files listed")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
