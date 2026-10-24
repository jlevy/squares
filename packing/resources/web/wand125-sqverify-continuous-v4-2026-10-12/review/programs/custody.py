"""Custody of wand125's sqverify_continuous: digests, shared files and the v3-to-v4 change.

Reads the retained crate trees as data (never builds or runs them) and prints one JSON
receipt with:

- ``source_sha256`` of each version by the rule its ``build.rs`` states: SHA-256 over,
  for ``Cargo.toml``, ``Cargo.lock``, ``build.rs`` and every ``src/*.rs`` in sorted
  order, the file's relative name, a zero byte, its bytes and a zero byte;
- every crate file's Git blob id, beside the blob id of the same path in this
  repository's ``packing/sqverify_fast`` at the revisions named on the command line
  (read with ``git ls-tree``), so that "byte for byte" is a measured statement;
- the top-level Rust items of ``src/slab.rs`` and ``src/main.rs`` whose text differs
  between the two versions, found by splitting each file at column-0 item heads and
  matching braces, so that "the search is unchanged" is measured too.

It decides nothing about the claim; it is the custody record the review cites.

The v3 packet retains only the files v4 changes and pins the rest to the v4 packet's
identical copies, so ``--v3-base`` names the v4 crate whose files fill in what the v3
directory lacks; the overlay is the v3 tree exactly when the v3 packet's manifest says so
(``devtools.acquire_source --check`` decides that).

Usage, from the repository root::

    packing/.venv/bin/python3 -I PATH/custody.py --v3 V3_CRATE --v3-base V4_CRATE \
        --v4 V4_CRATE --repo . --rev origin/main --rev dee22b88 > custody.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

DIGEST_FILES = ("Cargo.toml", "Cargo.lock", "build.rs")
ITEM_HEAD = re.compile(r"^(pub(\([a-z]+\))? )?(fn|struct|enum|impl|const|static|mod|type|use)\b")


def tree(crate: Path, base: Path | None = None) -> dict[str, bytes]:
    """The crate's files by relative path, ``crate`` over ``base`` where both hold one."""
    out: dict[str, bytes] = {}
    for root in (base, crate):
        if root is None:
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and "target" not in path.relative_to(root).parts:
                out[path.relative_to(root).as_posix()] = path.read_bytes()
    return out


def source_sha256(files: dict[str, bytes]) -> str:
    """The digest build.rs embeds: names and bytes, each followed by a zero byte."""
    names = list(DIGEST_FILES)
    names += sorted(n for n in files if n.startswith("src/") and n.count("/") == 1 and n.endswith(".rs"))
    digest = hashlib.sha256()
    for name in names:
        digest.update(name.encode())
        digest.update(b"\0")
        digest.update(files[name])
        digest.update(b"\0")
    return digest.hexdigest()


def git_blob(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def crate_files(files: dict[str, bytes]) -> dict[str, str]:
    return {name: git_blob(data) for name, data in sorted(files.items())}


def upstream_blobs(repo: Path, rev: str) -> dict[str, str]:
    listing = subprocess.run(
        ["git", "-C", str(repo), "ls-tree", "-r", rev, "packing/sqverify_fast"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    out = {}
    for line in listing.splitlines():
        meta, path = line.split("\t", 1)
        out[path.removeprefix("packing/sqverify_fast/")] = meta.split()[2]
    return out


def items(text: str) -> dict[str, str]:
    """Top-level items keyed by their head line, with their full text.

    An item starts at a column-0 head (doc comments and attributes above it are
    attached to it) and ends where its braces close or at its semicolon.
    """
    lines = text.splitlines()
    out: dict[str, str] = {}
    pending: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith(("///", "#[", "//!")) or not line.strip():
            if line.startswith(("///", "#[")):
                pending.append(line)
            index += 1
            continue
        if ITEM_HEAD.match(line):
            body = [*pending, line]
            depth = line.count("{") - line.count("}")
            ends = line.rstrip().endswith(";") and depth == 0
            index += 1
            while not ends and index < len(lines):
                body.append(lines[index])
                depth += lines[index].count("{") - lines[index].count("}")
                if depth <= 0 and ("}" in lines[index] or lines[index].rstrip().endswith(";")):
                    ends = True
                index += 1
            key = line.split("{")[0].strip()
            out[key] = "\n".join(body)
            pending = []
            continue
        pending = []
        index += 1
    return out


def changed_items(old: bytes, new: bytes) -> dict[str, list[str]]:
    a, b = items(old.decode()), items(new.decode())
    return {
        "changed": sorted(k for k in a.keys() & b.keys() if a[k] != b[k]),
        "added": sorted(b.keys() - a.keys()),
        "removed": sorted(a.keys() - b.keys()),
        "unchanged": sorted(k for k in a.keys() & b.keys() if a[k] == b[k]),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v3", type=Path, required=True, help="crate directory of v3")
    parser.add_argument("--v3-base", type=Path, default=None, help="crate filling in v3's pinned files")
    parser.add_argument("--v4", type=Path, required=True, help="crate directory of v4")
    parser.add_argument("--repo", type=Path, required=True, help="this repository's root")
    parser.add_argument("--rev", action="append", default=[], help="revisions to compare")
    args = parser.parse_args()
    t3, t4 = tree(args.v3, args.v3_base), tree(args.v4)
    v3, v4 = crate_files(t3), crate_files(t4)
    receipt: dict[str, object] = {
        "source_sha256": {"v3": source_sha256(t3), "v4": source_sha256(t4)},
        "files": {"v3": v3, "v4": v4},
        "v3_to_v4_changed_files": sorted(k for k in v3.keys() | v4.keys() if v3.get(k) != v4.get(k)),
    }
    comparisons = {}
    for rev in args.rev:
        up = upstream_blobs(args.repo, rev)
        comparisons[rev] = {
            name: ("same" if up.get(name) == blob else ("absent" if name not in up else "differs"))
            for name, blob in v4.items()
        }
    receipt["v4_against_upstream"] = comparisons
    receipt["slab_rs_items_v3_to_v4"] = changed_items(t3["src/slab.rs"], t4["src/slab.rs"])
    receipt["main_rs_items_v3_to_v4"] = changed_items(t3["src/main.rs"], t4["src/main.rs"])
    json.dump(receipt, sys.stdout, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
