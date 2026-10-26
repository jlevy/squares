"""Audit the root names of the Lean kernel proof of Valid7 against its certificates.

wand125's kernel proof of Evan Daniel's ``Bentz.Valid7`` (merged into evand/square-packing
at ``060c1a1``, issue #537) glues one generated Lean module per root cell of the k2m3
``qx2_zm`` run V3 into ``Sqpack/V7/Main.lean``: ``scripts/gen_main.py`` names root ``i``
``Sqpack.V7.R{i:05d}``, numbering the roots in the order of the run's leaves file, and
asserts that they fill the grid of the D4 root. Neither the root modules nor ``Main.lean``
are stored in Git: version 1 builds them from the release ``data/valid7-lean-certs-v1``
(``v7cert.tar.zst``, one pickle per root and ``v7cert.sha256``), and version 2
(wand125/square-packing ``649a920``) publishes them in the release ``valid7-lean-v2`` with
``generated-sources.sha256``, one line per generated file. This command checks that the
names agree, and writes ``receipts/root-names.json`` in the #537 packet:

- **leaves**: the run's leaves file, as the 1 October evand packet retains it (the blob
  ``060c1a1`` holds), has as many roots as the grid ``gen_main.py`` asserts, the product
  of its distinct cuts in x, y and u;
- **version 1**: every member of ``v7cert.tar.zst`` is ``v7cert/R{i:05d}.pkl`` for exactly
  the indices of those roots, plus ``v7cert.sha256``, which lists each pickle once with
  the SHA-256 of its bytes. The pickles are hashed and never loaded;
- **version 2**: ``generated-sources.sha256`` names ``Sqpack/V7/R{i:05d}.lean`` for exactly
  those indices, every other generated file but ``Main.lean`` lies under a root's own
  ``Sqpack/V7/R{i:05d}/`` directory and is named for it; a root may have no directory,
  and the audit counts the roots that do without reading why;
- **X mode**: ``scripts/v7_xroots.txt``, the roots version 1 emitted in X mode, names
  distinct indices among them.

It decides nothing about the proof: a name that agrees says which module a root's
certificate becomes, not that the module checks. ``scan`` reads the release archive and
the version 2 list, which the repository does not retain, from local copies held to the
SHA-256 pinned at review (the archive's here, the list's in the v2 packet's manifest),
and writes the receipt; ``check`` re-derives the leaves and X-mode parts from the
retained files, which Git identifies, and compares them with the receipt.

From ``packing/``::

    python -m devtools.audit_valid7_roots scan --certs ARCHIVE --generated LISTING
    python -m devtools.audit_valid7_roots check
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
import tarfile
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

from strif import atomic_write_text

from devtools.retained_data import read_retained_bytes

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "resources" / "web"
LEAVES = (
    WEB
    / "evand-square-packing-2026-10-01/source/s12/certificates/k2m3/qx2_zm"
    / "runV3_6294052a_leaves.jsonl.gz"
)
V1_PACKET = WEB / "evand-valid7-lean-2026-10-11"
V2_PACKET = WEB / "wand125-valid7-lean-v2-2026-10-17"
XROOTS = V1_PACKET / "square-packing/lean/scripts/v7_xroots.txt"
RECEIPT = V1_PACKET / "receipts/root-names.json"
#: The release asset of version 1 as downloaded for #537 on 26 October 2026; no file in
#: either repository states its digest, so the receipt is where it is pinned.
CERTS_SHA256 = "be50c2ed65b9214515930f8ab235d036684d571f51a7beecbee7e290c6ed4a75"
GENERATED = "lean/valid7/generated-sources.sha256"
FORMAT = "valid7-root-names-v1"
PICKLE = re.compile(r"v7cert/R(\d{5})\.pkl")
MODULE = re.compile(r"Sqpack/V7/R(\d{5})\.lean")
LEAF = re.compile(r"Sqpack/V7/R(\d{5})/[^/]+\.lean")


class AuditError(ValueError):
    pass


def _require(condition: object, message: str) -> None:
    if not condition:
        raise AuditError(message)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _span(indices: Sequence[int]) -> str:
    return f"R{min(indices):05d} to R{max(indices):05d}" if indices else "none"


def leaves() -> dict[str, Any]:
    """The run's roots and the grid ``gen_main.py`` asserts they fill."""
    with gzip.open(LEAVES, "rt", encoding="utf-8") as handle:
        handle.readline()
        roots = [tuple(Fraction(x) for x in json.loads(line)["root"]) for line in handle]
    cuts = [len({r[k] for r in roots} | {r[k + 1] for r in roots}) - 1 for k in (0, 2, 4)]
    cells = {(r[0], r[2], r[4]) for r in roots}
    _require(len(cells) == len(roots), "two roots share a lower corner")
    _require(cuts[0] * cuts[1] * cuts[2] == len(roots), "the roots do not fill the grid")
    return {
        "path": LEAVES.relative_to(ROOT.parent).as_posix(),
        "roots": len(roots),
        "grid": cuts,
    }


def xroots(count: int) -> dict[str, Any]:
    raw = read_retained_bytes(XROOTS)
    names = [int(line) for line in raw.decode("ascii").split()]
    _require(len(set(names)) == len(names), "v7_xroots.txt repeats a root")
    _require(all(0 <= i < count for i in names), "v7_xroots.txt names a root out of range")
    return {
        "path": XROOTS.relative_to(ROOT.parent).as_posix(),
        "roots": len(names),
    }


def certificates(path: Path, count: int) -> dict[str, Any]:
    """Version 1's archive: one pickle per root, each matching its line in the list."""
    _require(_sha256(path) == CERTS_SHA256, f"{path}: not the pinned v7cert.tar.zst")
    by_root: dict[int, str] = {}
    listed: dict[str, str] = {}
    others: list[str] = []
    with tarfile.open(path, "r:zst") as archive:
        for member in archive:
            if member.isdir():
                others.append(member.name)
                continue
            handle = archive.extractfile(member)
            _require(handle is not None, f"{member.name}: not a regular file")
            assert handle is not None
            data = handle.read()
            if member.name == "v7cert.sha256":
                for line in data.decode("ascii").splitlines():
                    digest, name = line.split(maxsplit=1)
                    _require(name not in listed, f"v7cert.sha256 repeats {name}")
                    listed[name] = digest
                continue
            match = PICKLE.fullmatch(member.name)
            _require(match is not None, f"{member.name}: not a root's pickle")
            assert match is not None
            index = int(match.group(1))
            _require(index not in by_root, f"{member.name}: twice")
            by_root[index] = hashlib.sha256(data).hexdigest()
    _require(sorted(by_root) == list(range(count)), "the pickles are not one per root")
    by_name = {Path(name).name: digest for name, digest in listed.items()}
    _require(
        by_name == {f"R{i:05d}.pkl": value for i, value in by_root.items()},
        "v7cert.sha256 does not list each pickle once with its digest",
    )
    return {
        "asset": "v7cert.tar.zst",
        "sha256": CERTS_SHA256,
        "bytes": path.stat().st_size,
        "pickles": len(by_root),
        "names": _span(sorted(by_root)),
        "listed": len(listed),
        "every_pickle_matches_its_line": True,
        "directories": others,
    }


def _pinned_generated() -> str:
    for line in (V2_PACKET / "acquisition/upstream-subtree.sha256").read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        if name == f"./{GENERATED}":
            return digest
    raise AuditError(f"the v2 packet does not pin {GENERATED}")


def generated(path: Path, count: int) -> dict[str, Any]:
    """Version 2's list: one root module per root, every leaf under its root."""
    pinned = _pinned_generated()
    _require(_sha256(path) == pinned, f"{path}: not the pinned {GENERATED}")
    modules: set[int] = set()
    leaf_roots: set[int] = set()
    leaf_files = 0
    others: list[str] = []
    for line in path.read_text("utf-8").splitlines():
        _digest, name = line.split(maxsplit=1)
        if match := MODULE.fullmatch(name):
            index = int(match.group(1))
            _require(index not in modules, f"{name}: twice")
            modules.add(index)
        elif match := LEAF.fullmatch(name):
            index = int(match.group(1))
            _require(
                PurePosixPath(name).name.startswith(f"r{index:05d}"),
                f"{name}: a leaf named for another root",
            )
            leaf_roots.add(index)
            leaf_files += 1
        else:
            others.append(name)
    _require(sorted(modules) == list(range(count)), "the root modules are not one per root")
    _require(leaf_roots <= modules, "a leaf directory names no root")
    _require(others == ["Sqpack/V7/Main.lean"], f"unexpected generated files: {others}")
    return {
        "path": GENERATED,
        "sha256": pinned,
        "lines": len(modules) + leaf_files + len(others),
        "root_modules": len(modules),
        "names": _span(sorted(modules)),
        "leaf_files": leaf_files,
        "roots_with_leaves": len(leaf_roots),
        "others": others,
    }


def scan(certs: Path, listing: Path) -> dict[str, Any]:
    grid = leaves()
    count = grid["roots"]
    return {
        "format": FORMAT,
        "leaves": grid,
        "xroots": xroots(count),
        "version_1": certificates(certs, count),
        "version_2": generated(listing, count),
        "agree": True,
    }


def check() -> list[str]:
    record = json.loads(RECEIPT.read_text("utf-8"))
    problems: list[str] = []
    if record.get("format") != FORMAT or record.get("agree") is not True:
        problems.append("the receipt is not an agreeing valid7-root-names-v1 receipt")
    grid = leaves()
    if record.get("leaves") != grid:
        problems.append("the leaves part does not re-derive")
    if record.get("xroots") != xroots(grid["roots"]):
        problems.append("the X-mode part does not re-derive")
    for part in ("version_1", "version_2"):
        names = record.get(part, {}).get("names")
        if names != _span(range(grid["roots"])):
            problems.append(f"{part} does not name every root")
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)
    scan_parser = sub.add_parser("scan")
    scan_parser.add_argument("--certs", type=Path, required=True)
    scan_parser.add_argument("--generated", type=Path, required=True)
    sub.add_parser("check")
    args = parser.parse_args(argv)
    try:
        if args.command == "scan":
            record = scan(args.certs, args.generated)
            RECEIPT.parent.mkdir(parents=True, exist_ok=True)
            atomic_write_text(RECEIPT, json.dumps(record, indent=2) + "\n")
            print(json.dumps(record, indent=2))
            return 0
        problems = check()
    except (AuditError, OSError, tarfile.TarError) as error:
        print(f"audit_valid7_roots: {error}", file=sys.stderr)
        return 1
    for problem in problems:
        print(problem, file=sys.stderr)
    if not problems:
        print("ROOT_NAMES_AGREE")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
