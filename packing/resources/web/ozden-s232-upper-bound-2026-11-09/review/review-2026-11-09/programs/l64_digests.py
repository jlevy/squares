"""Hold every receipt's program digests to the frozen checker and to the bytes kept here.

Usage: python -I -B l64_digests.py FROZEN_DIGESTS.txt OUT_DIR OUT.json

Lane L64. Decides nothing about any certificate. For each receipt in OUT_DIR it compares
the SHA-256 it records for every program with the program's bytes in this directory, and
for the six checker files also with the frozen digests. A receipt whose digests differ
from the bytes kept here was written by an earlier version and is named as such.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from l64_util import program_digests, sha256_file, write_receipt  # noqa: E402

HERE = Path(__file__).resolve().parent


def main(argv: list[str]) -> int:
    if len(argv) != 4:
        print(__doc__)
        return 2
    frozen_path, out_dir, out = Path(argv[1]), Path(argv[2]), argv[3]
    frozen = {}
    for line in frozen_path.read_text().splitlines():
        if line and not line.startswith("#"):
            digest, name = line.split()
            frozen[name] = digest
    current = {p.name: sha256_file(p) for p in sorted(HERE.glob("*.py"))}
    checker_frozen_equal = all(current.get(name) == d for name, d in frozen.items())
    receipts = {}
    for path in sorted(out_dir.glob("*.json")):
        data = json.loads(path.read_text())
        recorded = data.get("programs_sha256", {})
        receipts[path.name] = {
            "program": data.get("program"),
            "all_programs_match_kept_bytes": all(current.get(k) == v for k, v in recorded.items()),
            "checker_files_match_frozen": all(frozen[k] == v for k, v in recorded.items() if k in frozen),
            "differs": sorted(k for k, v in recorded.items() if current.get(k) != v),
        }
    ok = checker_frozen_equal and all(
        r["all_programs_match_kept_bytes"] and r["checker_files_match_frozen"] for r in receipts.values()
    )
    receipt = {
        "program": "l64_digests.py",
        "programs_sha256": program_digests([HERE / "l64_digests.py", HERE / "l64_util.py"]),
        "frozen_digests_file_sha256": sha256_file(frozen_path),
        "checker_files_equal_frozen": checker_frozen_equal,
        "current_programs": current,
        "receipts": receipts,
        "verdict": "ALL_RECEIPTS_MATCH" if ok else "SOME_RECEIPTS_DIFFER",
    }
    write_receipt(out, receipt)
    print(receipt["verdict"], "checker == frozen:", checker_frozen_equal)
    for name, r in receipts.items():
        if not (r["all_programs_match_kept_bytes"] and r["checker_files_match_frozen"]):
            print("  differs:", name, r["differs"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
