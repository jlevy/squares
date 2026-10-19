"""Which files the SHA-256 column of ``theorem/PIECES.md`` identifies.

    python3 -I -B pieces_digests.py PIECES.md NAME=PATH [NAME=PATH ...]

Each ``NAME=PATH`` names a piece of the table and the file retained for it. For each
piece the program prints whether the table's digest is the digest of the retained
file's bytes, of its bytes with the ``#`` comment lines removed, or of neither. It
decides a question of provenance, not of geometry: whether the inventory's piece list
binds to the files the release ships. Exit status 0 when every piece is identified one
way or the other. Written for the review of 14 October 2026; see ../README.md.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def say(line: str) -> None:
    sys.stdout.write(line + "\n")


def table_digests(pieces: Path) -> dict[str, str]:
    digests: dict[str, str] = {}
    for line in pieces.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 10 and cells[-1].startswith("`") and cells[2].isdigit():
            digests[cells[0]] = cells[-1].strip("`")
    return digests


def without_comments(data: bytes) -> bytes:
    return b"".join(
        line for line in data.splitlines(keepends=True) if not line.lstrip().startswith(b"#")
    )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    digests = table_digests(Path(args[0]))
    unidentified = 0
    counts = {"the retained file": 0, "the file without its comment lines": 0, "neither": 0}
    for item in args[1:]:
        name, _, path = item.partition("=")
        data = Path(path).read_bytes()
        full = hashlib.sha256(data).hexdigest()
        stripped = hashlib.sha256(without_comments(data)).hexdigest()
        stated = digests.get(name)
        if stated is None:
            say(f"{name}: not in the table")
            unidentified += 1
            continue
        if stated == full:
            verdict = "the retained file"
        elif stated == stripped:
            verdict = "the file without its comment lines"
        else:
            verdict = "neither"
            unidentified += 1
        counts[verdict] += 1
        say(f"{name}: the table's digest {stated[:12]} is the digest of {verdict}")
    say(
        f"{counts['the retained file']} identify the retained file, "
        f"{counts['the file without its comment lines']} its comment-stripped bytes, "
        f"{counts['neither']} neither"
    )
    say("PIECES_DIGESTS_IDENTIFIED" if not unidentified else "PIECES_DIGESTS_UNIDENTIFIED")
    return 0 if not unidentified else 1


if __name__ == "__main__":
    sys.exit(main())
