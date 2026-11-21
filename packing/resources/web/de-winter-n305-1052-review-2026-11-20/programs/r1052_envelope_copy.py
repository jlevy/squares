"""Lane r1052, written after the checker's freeze: a reading copy of form C. It decides
nothing.

Usage: r1052_envelope_copy.py C_FILE COPY_OUT RECEIPT_JSON

The published n305_witness.yaml has a softschema block with only ``contract`` and a
witness record with no ``claim`` block, which the Witness/v2 schema requires; the frozen
reader refuses it there. This program writes a scratch copy that inserts exactly two
things and changes nothing else: the line ``  envelope: witness`` after the ``contract``
line, and a three-line ``claim`` block before the ``squares`` key, saying that it was
inserted. It then proves the copy is the original plus those lines: deleting the
inserted lines from the copy gives the original bytes exactly. The frozen check and
controls then read the copy, and the receipt names both digests.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ENVELOPE = b"  envelope: witness\n"
CLAIM = (
    b"  claim:\n"
    b"    coordinate_provenance: reported\n"
    b"    method: exact-algebraic\n"
    b"    limitations: inserted by lane r1052 into a reading copy; the published file has no claim block\n"
)


def main(argv: list[str]) -> int:
    src, dst, receipt_path = argv[1:4]
    data = Path(src).read_bytes()
    lines = data.splitlines(keepends=True)
    if lines[:2] != [b"softschema:\n", b"  contract: packing.squares:Witness/v2\n"]:
        raise SystemExit("unexpected envelope")
    squares_at = [k for k, line in enumerate(lines) if line == b"  squares:\n"]
    if len(squares_at) != 1 or any(line.startswith(b"  claim:") for line in lines):
        raise SystemExit("unexpected layout")
    k = squares_at[0]
    out = [*lines[:2], ENVELOPE, *lines[2:k], CLAIM, *lines[k:]]
    copy = b"".join(out)
    restored = copy.replace(ENVELOPE, b"", 1).replace(CLAIM, b"", 1)
    same = restored == data
    Path(dst).write_bytes(copy)
    receipt = {
        "program": "r1052_envelope_copy.py",
        "original_sha256": hashlib.sha256(data).hexdigest(),
        "copy_sha256": hashlib.sha256(copy).hexdigest(),
        "inserted_lines": [ENVELOPE.decode(), *CLAIM.decode().splitlines(keepends=True)],
        "inserted_after_line": {"envelope": 2, "claim": k},
        "copy_minus_insertions_is_original": same,
        "original_bytes": len(data),
        "copy_bytes": len(copy),
    }
    Path(receipt_path).write_text(json.dumps(receipt, indent=1) + "\n")
    print(f"copy written; deleting the inserted lines restores the original: {same}")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
