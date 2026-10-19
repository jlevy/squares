"""Read retained data stored as deterministic gzip, and check the packets that store it.

A packet under ``resources/web/`` keeps third-party bytes byte-identical at their upstream
paths. Large retained data files (certificates, ledgers, receipts and logs of more than
1,000 lines) are stored instead as ``X.gz``, made by ``gzip -9n`` so the archive carries
no file name and no timestamp and the same input always gives the same bytes. The
precedent is the R052 packet, whose source ships its certificate that way.

Readers go through `read_retained_bytes`, which takes the upstream path ``X`` and reads
``X`` or ``X.gz``, whichever is present, so a tree restored by ``gunzip -k`` and the
compressed tree read the same. Where both are present they must agree. Both reads are
bounded, before and after decompression.

Each packet that stores files this way lists them in a README section headed
``## Compressed Files``: every row names the stored ``.gz`` path relative to the packet,
the origin of the bytes (``upstream`` or ``receipt``), and the Git blob and SHA-256 of
the decompressed bytes. ``check`` re-derives every row from the stored files.
An explicitly retained upstream gzip belongs instead to ``## Original Gzip Files``:
its Git blob and SHA-256 name the original compressed bytes, including its header.
Readers still decompress gzip normally; only that separate custody table binds raw bytes.

Usage (from ``packing/``)::

    .venv/bin/python3 -m devtools.retained_data candidates PACKET...
    .venv/bin/python3 -m devtools.retained_data compress --origin upstream PACKET FILE...
    .venv/bin/python3 -m devtools.retained_data check PACKET...
"""

from __future__ import annotations

import argparse
import errno
import gzip
import hashlib
import io
import os
import subprocess
import sys
import zlib
from dataclasses import dataclass
from pathlib import Path

GZIP_SUFFIX = ".gz"
MAX_COMPRESSED = 16 * 1024 * 1024
MAX_DECOMPRESSED = 64 * 1024 * 1024
#: Data suffixes that are compressed above `LINE_THRESHOLD`; source code never is.
DATA_SUFFIXES = frozenset({".json", ".jsonl", ".txt", ".log"})
LINE_THRESHOLD = 1000
HEADING = "## Compressed Files"
ORIGINAL_GZIP_HEADING = "## Original Gzip Files"
ORIGINS = frozenset({"upstream", "receipt"})
#: A gzip member header with no optional fields (no name, comment or extra) and mtime 0.
_DETERMINISTIC_HEADER = b"\x1f\x8b\x08\x00\x00\x00\x00\x00"


def _bounded_read(path: Path, limit: int) -> bytes:
    with path.open("rb") as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError(f"{path} exceeds {limit} bytes")
    return data


def gunzip_bytes(data: bytes, *, limit: int = MAX_DECOMPRESSED, name: str = "data") -> bytes:
    """Decompress one gzip stream, refusing output past ``limit`` bytes."""
    with gzip.GzipFile(fileobj=io.BytesIO(data)) as stream:
        out = stream.read(limit + 1)
    if len(out) > limit:
        raise ValueError(f"decompressed {name} exceeds {limit} bytes")
    return out


def compressed_path(path: Path) -> Path:
    """The ``.gz`` sibling that stores ``path``."""
    return path.with_name(path.name + GZIP_SUFFIX)


def read_retained_bytes(path: Path, *, limit: int = MAX_DECOMPRESSED) -> bytes:
    """The upstream bytes of ``path``, read from ``path`` or from ``path.gz``.

    A path that itself ends in ``.gz`` is decompressed. Otherwise the plain file is read
    when present, and must equal its compressed sibling if that exists too (a tree
    restored with ``gunzip -k``); failing both, the sibling is decompressed.
    """
    if path.name.endswith(GZIP_SUFFIX):
        return gunzip_bytes(
            _bounded_read(path, min(limit, MAX_COMPRESSED)), limit=limit, name=str(path)
        )
    packed = compressed_path(path)
    if path.is_file():
        data = _bounded_read(path, limit)
        if packed.is_file() and read_retained_bytes(packed, limit=limit) != data:
            raise ValueError(f"{path} differs from its compressed copy {packed.name}")
        return data
    if packed.is_file():
        return read_retained_bytes(packed, limit=limit)
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(path))


def read_retained_text(path: Path, *, encoding: str = "utf-8") -> str:
    """`read_retained_bytes` decoded, strictly."""
    return read_retained_bytes(path).decode(encoding)


def retained_exists(path: Path) -> bool:
    """Whether ``path`` is present, plain or compressed."""
    return path.is_file() or compressed_path(path).is_file()


def git_blob(data: bytes) -> str:
    """The SHA-1 ``git hash-object`` gives these bytes."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data, usedforsecurity=False).hexdigest()


def is_deterministic_gzip(data: bytes) -> bool:
    """A single-member gzip header carrying no name, comment, extra field or timestamp."""
    return data[: len(_DETERMINISTIC_HEADER)] == _DETERMINISTIC_HEADER


def compress(path: Path) -> Path:
    """Replace ``path`` by ``path.gz`` made with ``gzip -9n``; return the stored path."""
    subprocess.run(["gzip", "-9n", "--", str(path)], check=True)
    stored = compressed_path(path)
    if not is_deterministic_gzip(stored.read_bytes()):
        raise ValueError(f"{stored} is not a deterministic gzip")
    return stored


@dataclass(frozen=True, slots=True)
class Row:
    stored: str
    origin: str
    blob: str
    sha256: str

    def markdown(self) -> str:
        return f"| `{self.stored}` | {self.origin} | `{self.blob}` | `{self.sha256}` |"


def describe(packet: Path, stored: Path, origin: str) -> Row:
    """The table row for one stored file, from its decompressed bytes."""
    if origin not in ORIGINS:
        raise ValueError(f"origin must be one of {sorted(ORIGINS)}: {origin}")
    data = read_retained_bytes(stored)
    return Row(
        str(stored.relative_to(packet)),
        origin,
        git_blob(data),
        hashlib.sha256(data).hexdigest(),
    )


def read_table(readme: Path, *, heading: str = HEADING) -> list[Row]:
    """The rows of the README's ``Compressed Files`` table, in order."""
    lines = readme.read_text(encoding="utf-8").splitlines()
    if heading not in lines:
        return []
    rows: list[Row] = []
    for line in lines[lines.index(heading) + 1 :]:
        if line.startswith("## "):
            break
        if not line.startswith("| `"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) != 4:
            raise ValueError(f"{readme}: malformed compressed-file row: {line}")
        rows.append(Row(*cells))
    return rows


def read_original_gzip_bytes(path: Path) -> bytes:
    """Read bounded original compressed bytes, without archive recompression."""
    return _bounded_read(path, MAX_COMPRESSED)


def describe_original_gzip(packet: Path, stored: Path, origin: str = "upstream") -> Row:
    """Bind an explicitly retained upstream gzip file's original compressed bytes."""
    if origin != "upstream":
        raise ValueError("original gzip files must be upstream bytes")
    data = read_original_gzip_bytes(stored)
    gunzip_bytes(data, name=str(stored))
    return Row(
        str(stored.relative_to(packet)),
        origin,
        git_blob(data),
        hashlib.sha256(data).hexdigest(),
    )


def check_packet(packet: Path) -> list[str]:
    """Every problem with the packet's compressed files against its README table."""
    problems: list[str] = []
    rows = read_table(packet / "README.md")
    originals = read_table(packet / "README.md", heading=ORIGINAL_GZIP_HEADING)
    listed = {row.stored for row in (*rows, *originals)}
    stored = {str(path.relative_to(packet)) for path in packet.rglob(f"*{GZIP_SUFFIX}")}
    problems.extend(f"{packet.name}: {name} is not in the table" for name in stored - listed)
    if len(listed) != len(rows) + len(originals):
        problems.append(f"{packet.name}: the table lists a file twice")
    for row in rows:
        path = packet / row.stored
        if row.stored not in stored:
            problems.append(f"{packet.name}: {row.stored} is listed but absent")
            continue
        if not is_deterministic_gzip(path.read_bytes()):
            problems.append(f"{packet.name}: {row.stored} carries a name or timestamp")
        if describe(packet, path, row.origin) != row:
            problems.append(f"{packet.name}: {row.stored} differs from its table row")
    for row in originals:
        if row.stored not in stored:
            problems.append(f"{packet.name}: {row.stored} is listed but absent")
            continue
        try:
            found = describe_original_gzip(packet, packet / row.stored, row.origin)
        except OSError, ValueError, EOFError, zlib.error:
            problems.append(f"{packet.name}: {row.stored} is not a valid original gzip")
            continue
        if found != row:
            problems.append(
                f"{packet.name}: {row.stored} differs from its original-gzip table row"
            )
    return problems


def candidates(packet: Path) -> list[Path]:
    """Plain data files in the packet over the line threshold, in path order."""
    return sorted(
        path
        for path in packet.rglob("*")
        if path.is_file()
        and path.suffix in DATA_SUFFIXES
        and path.read_bytes().count(b"\n") > LINE_THRESHOLD
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("candidates", help="list data files over the threshold")
    listing.add_argument("packets", type=Path, nargs="+")
    packing = commands.add_parser("compress", help="gzip files and print their table rows")
    packing.add_argument("--origin", choices=sorted(ORIGINS), required=True)
    packing.add_argument("packet", type=Path)
    packing.add_argument("files", type=Path, nargs="+")
    checking = commands.add_parser("check", help="re-derive every packet's table")
    checking.add_argument("packets", type=Path, nargs="+")
    args = parser.parse_args()
    if args.command == "candidates":
        for packet in args.packets:
            for path in candidates(packet):
                print(path)
        return 0
    if args.command == "compress":
        packet = args.packet.resolve()
        for path in args.files:
            print(describe(packet, compress(path.resolve()), args.origin).markdown())
        return 0
    problems = [problem for packet in args.packets for problem in check_packet(packet)]
    for problem in problems:
        print(problem, file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
