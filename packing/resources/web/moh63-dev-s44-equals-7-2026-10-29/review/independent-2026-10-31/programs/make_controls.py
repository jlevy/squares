"""Reviewer controls for the s(44) cover (bold-ritchie-rev3), written for this review only.

Reads the decompressed cover and writes three mutants, each differing from the original in
the rows stated, with their SHA-256 and what changed:

  scale99    W row 100000000 -> 101010102: every mass scaled exactly by 10^8/101010102
             (about 0.99); D4 invariance is preserved because only the denominator moves.
  drop1pt    the first point row removed (only that point, not its D4 orbit), np - 1:
             the point measure is no longer D4-invariant.
  drop1seg   the first segment row removed (only that segment, not its orbit), ns - 1:
             the line measure is no longer D4-invariant; the point measure is untouched.

Usage: python -I make_controls.py COVER OUTDIR
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def rows(lines: list[str]) -> list[int]:
    """Indices of lines that carry tokens once the # comment is removed."""
    return [i for i, line in enumerate(lines) if line.split("#", 1)[0].split()]


def main(cover: Path, out: Path) -> int:
    text = cover.read_text(encoding="ascii")
    lines = text.splitlines(keepends=True)
    r = rows(lines)
    tok = lambda k: lines[r[k]].split("#", 1)[0].split()  # noqa: E731
    assert tok(0) == ["mixed", "1"], tok(0)
    assert tok(1) == ["7", "1"], tok(1)
    assert tok(2) == ["1000"], tok(2)
    assert tok(3) == ["100000000"], tok(3)
    np_ = int(tok(4)[0])
    first_point = 5
    ns_row = first_point + np_
    ns = int(tok(ns_row)[0])
    first_seg = ns_row + 1
    out.mkdir(parents=True, exist_ok=True)

    def emit(name: str, new_lines: list[str], what: str) -> None:
        data = "".join(new_lines).encode("ascii")
        path = out / f"s44_cover_7_{name}.txt"
        path.write_bytes(data)
        print(f"{name}: sha256 {hashlib.sha256(data).hexdigest()}  {what}")

    a = list(lines)
    a[r[3]] = "101010102\n"
    emit("scale99", a, "W 100000000 -> 101010102 (exact uniform scale 10^8/101010102)")

    b = list(lines)
    dropped = b[r[first_point]].strip()
    b[r[first_point]] = ""
    b[r[4]] = f"{np_ - 1}\n"
    emit("drop1pt", b, f"dropped point row '{dropped}' alone; np {np_} -> {np_ - 1}")

    c = list(lines)
    dropped = c[r[first_seg]].strip()
    c[r[first_seg]] = ""
    c[r[ns_row]] = f"{ns - 1}\n"
    emit("drop1seg", c, f"dropped segment row '{dropped}' alone; ns {ns} -> {ns - 1}")
    print(f"original: sha256 {hashlib.sha256(text.encode('ascii')).hexdigest()}; np {np_}, ns {ns}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
