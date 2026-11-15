"""Price a Lean build's disk before anything is written: size a toolchain, then test the plan.

A Lean build here needs the toolchain and a Mathlib cache on disk before the first module
compiles, and the record's Lean replays have stopped on disk more often than on CPU. This
tool answers the disk question first, writing nothing but its receipt.

``toolchain SOURCE``
    Read a ``.tar.zst`` toolchain archive as a stream (``-`` for standard input, so that
    ``curl -sSL URL |`` can feed it), and report its compressed bytes and SHA-256 and the
    unpacked bytes of its regular files, in total and by directory. Nothing is unpacked.
    It refuses (exit 1) an archive that does not decompress or list to its end, and a
    stream whose length or digest is not the one ``--expect-bytes`` or ``--expect-sha256``
    names, so a cut-off download cannot pass for a small toolchain.
``plan --item LABEL=BYTES|LABEL=@RECEIPT ... --cap BYTES --disk PATH``
    Add the items, each a stated figure or a ``toolchain`` receipt's measured unpacked
    bytes, and compare the total with the cap and with the free bytes of the filesystem
    holding ``PATH``. It prints ``FITS`` (exit 0) or ``DOES-NOT-FIT`` (exit 2) with both
    margins, and records which items were measured and which stated.

Usage, from ``packing/``::

    URL=https://github.com/leanprover/lean4/releases/download/v4.33.1
    curl -sSL $URL/lean-4.33.1-linux.tar.zst \\
      | .venv/bin/python3 -m devtools.lean_disk_price toolchain - \\
          --label leanprover/lean4:v4.33.1 --expect-bytes 570405234 --json R/toolchain.json
    .venv/bin/python3 -m devtools.lean_disk_price plan --item toolchain=@R/toolchain.json \\
        --item mathlib-cache=6500000000 --cap 9000000000 --disk SCRATCH --json R/plan.json
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import sys
import tarfile
from collections import Counter
from collections.abc import Buffer, Sequence
from compression import zstd
from datetime import UTC, datetime
from pathlib import Path
from typing import BinaryIO

from strif import atomic_write_text

TOOLCHAIN_KIND = "lean-disk-price-toolchain/1"
PLAN_KIND = "lean-disk-price-plan/1"
_CHUNK = 1 << 20


class PriceRefusedError(Exception):
    """The input cannot support a price: a truncated or unreadable archive, or a bad item."""


class _Counted(io.RawIOBase):
    """A read-only raw stream that hashes and counts every byte read through it."""

    def __init__(self, raw: BinaryIO) -> None:
        super().__init__()
        self._raw = raw
        self.digest = hashlib.sha256()
        self.count = 0

    def readable(self) -> bool:
        return True

    def readinto(self, buffer: Buffer, /) -> int:
        view = memoryview(buffer).cast("B")
        data = self._raw.read(len(view))
        view[: len(data)] = data
        self.digest.update(data)
        self.count += len(data)
        return len(data)


def _directory(name: str) -> str:
    """The archive member's directory two levels below the archive's root folder."""
    parts = name.split("/")[1:-1]
    return "/".join(parts[:2]) or "."


def measure_toolchain(
    raw: BinaryIO,
    *,
    label: str,
    expect_bytes: int | None = None,
    expect_sha256: str | None = None,
) -> dict[str, object]:
    """Stream a ``.tar.zst`` archive and return its sizes; refuse a short or unreadable one."""
    counted = _Counted(raw)
    stream = io.BufferedReader(counted, _CHUNK)
    by_directory: Counter[str] = Counter()
    files = 0
    try:
        with tarfile.open(fileobj=stream, mode="r|zst") as archive:
            for member in archive:
                if member.isfile():
                    by_directory[_directory(member.name)] += member.size
                    files += 1
    except (tarfile.TarError, EOFError, zstd.ZstdError) as error:
        raise PriceRefusedError(f"archive does not read to its end: {error}") from error
    while stream.read(_CHUNK):
        pass
    sha256 = counted.digest.hexdigest()
    if expect_bytes is not None and counted.count != expect_bytes:
        raise PriceRefusedError(f"stream is {counted.count} bytes, expected {expect_bytes}")
    if expect_sha256 is not None and sha256 != expect_sha256.lower():
        raise PriceRefusedError(f"stream SHA-256 is {sha256}, expected {expect_sha256}")
    if files == 0:
        raise PriceRefusedError("archive lists no regular file")
    return {
        "kind": TOOLCHAIN_KIND,
        "label": label,
        "compressed_bytes": counted.count,
        "sha256": sha256,
        "files": files,
        "unpacked_bytes": sum(by_directory.values()),
        "by_directory": dict(sorted(by_directory.items(), key=lambda kv: (-kv[1], kv[0]))),
        "measured": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def parse_item(text: str) -> tuple[str, int, str]:
    """``LABEL=BYTES`` (a stated figure) or ``LABEL=@RECEIPT`` (a measured toolchain)."""
    label, sep, value = text.partition("=")
    if not sep or not label:
        raise PriceRefusedError(f"item {text!r} is not LABEL=BYTES or LABEL=@RECEIPT")
    if value.startswith("@"):
        receipt = json.loads(Path(value[1:]).read_text(encoding="utf-8"))
        if receipt.get("kind") != TOOLCHAIN_KIND:
            raise PriceRefusedError(f"{value[1:]} is not a {TOOLCHAIN_KIND} receipt")
        basis = f"measured: {receipt.get('label', '?')}, sha256 {receipt.get('sha256', '?')}"
        return label, int(receipt["unpacked_bytes"]), basis
    try:
        size = int(value)
    except ValueError as error:
        raise PriceRefusedError(
            f"item {text!r}: {value!r} is not a whole number of bytes"
        ) from error
    if size < 0:
        raise PriceRefusedError(f"item {text!r} is negative")
    return label, size, "stated"


def price_plan(
    items: Sequence[tuple[str, int, str]], *, cap: int, free: int
) -> dict[str, object]:
    """The plan's total against the cap and the free bytes, and its verdict."""
    total = sum(size for _, size, _ in items)
    fits = total <= cap and total <= free
    return {
        "kind": PLAN_KIND,
        "items": [
            {"label": label, "bytes": size, "basis": basis} for label, size, basis in items
        ],
        "total_bytes": total,
        "cap_bytes": cap,
        "free_bytes": free,
        "margin_to_cap_bytes": cap - total,
        "margin_to_free_bytes": free - total,
        "verdict": "FITS" if fits else "DOES-NOT-FIT",
    }


def _gb(size: int) -> str:
    return f"{size / 1e9:.2f} GB"


def _write(path: Path | None, record: dict[str, object]) -> None:
    if path is not None:
        atomic_write_text(path, json.dumps(record, indent=2) + "\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    tool = commands.add_parser("toolchain", help="size a .tar.zst toolchain stream")
    tool.add_argument("source", help="the archive's path, or - for standard input")
    tool.add_argument("--label", required=True, help="what the archive is, for the receipt")
    tool.add_argument("--expect-bytes", type=int, help="refuse a stream of another length")
    tool.add_argument("--expect-sha256", help="refuse a stream with another digest")
    tool.add_argument("--json", type=Path, help="write the receipt here")
    plan = commands.add_parser("plan", help="test a build's disk plan against a cap")
    plan.add_argument(
        "--item", action="append", required=True, help="LABEL=BYTES or LABEL=@RECEIPT"
    )
    plan.add_argument(
        "--cap", type=int, required=True, help="the most the build may use, in bytes"
    )
    plan.add_argument(
        "--disk", type=Path, required=True, help="a path on the build's filesystem"
    )
    plan.add_argument(
        "--disk-label", help="what --disk is, for the verdict (default: the path)"
    )
    plan.add_argument("--json", type=Path, help="write the verdict here")
    args = parser.parse_args(argv)
    try:
        if args.command == "toolchain":
            if args.source == "-":
                record = measure_toolchain(
                    sys.stdin.buffer,
                    label=args.label,
                    expect_bytes=args.expect_bytes,
                    expect_sha256=args.expect_sha256,
                )
            else:
                with Path(args.source).open("rb") as raw:
                    record = measure_toolchain(
                        raw,
                        label=args.label,
                        expect_bytes=args.expect_bytes,
                        expect_sha256=args.expect_sha256,
                    )
            _write(args.json, record)
            print(
                f"{record['label']}: {record['compressed_bytes']} bytes compressed, "
                f"sha256 {record['sha256']}, {record['files']} files, "
                f"{record['unpacked_bytes']} bytes unpacked"
            )
            return 0
        items = [parse_item(text) for text in args.item]
        record = price_plan(items, cap=args.cap, free=shutil.disk_usage(args.disk).free)
        record["disk"] = args.disk_label or str(args.disk)
        record["priced"] = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
        _write(args.json, record)
        for label, size, basis in items:
            print(f"  {label}: {_gb(size)} ({basis})")
        total, cap, free = (
            int(str(record[k])) for k in ("total_bytes", "cap_bytes", "free_bytes")
        )
        print(f"{record['verdict']}: total {_gb(total)}, cap {_gb(cap)}, free {_gb(free)}")
        return 0 if record["verdict"] == "FITS" else 2
    except PriceRefusedError as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
