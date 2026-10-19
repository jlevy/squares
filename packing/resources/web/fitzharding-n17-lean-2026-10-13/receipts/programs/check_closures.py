"""Read the import closures of sq17-lean's statement and upper bound for native evaluation.

Reads, as data, the packet's retained ``manifest.json.gz`` (every source module with its
imports, archive, size and SHA-256), a checkout of ``ofitzharding/sq17-lean`` at the pin,
and the release archive ``generated-sources.tar.gz``, streamed without extracting it. Runs
nothing from any of them. For each closure below it holds every module's bytes to the
size and SHA-256 ``manifest.json`` gives, the archive to the size and SHA-256 it gives,
and counts in each module's code, with comments, strings and character literals blanked,
the tokens ``devtools.audit_n11_lean`` counts: ``native_decide``, ``decide +native``,
``ofReduceBool``, ``implemented_by``, ``extern``, ``axiom``, ``sorry`` and the rest of
its ``TOKENS``. A raw ``native_decide`` that is not in code is listed with its line.

- ``Sq17Lean.PackingStatement``: ``PlainPacking``, ``feasible_iff_plainPacking`` and
  ``endpoint_plainPacking``, the existence half's statement and proof;
- ``Sq17Lean.EndpointPacking``: ``EndpointGeometry.endpoint_packing``, which
  ``endpoint_plainPacking`` wraps;
- ``Sq17Lean.EndpointGeometry``: the definition of ``side``;
- ``Sq17Lean.Square17Optimality``: the theorem, counted and not read.

Usage, from ``packing/``, with the project interpreter and ``-I``::

    .venv/bin/python3 -I PACKET/receipts/programs/check_closures.py PACKET CHECKOUT ARCHIVE

``PACKET`` is the packet directory, ``CHECKOUT`` a clone at the pin and ``ARCHIVE`` the
release's ``generated-sources.tar.gz``; the output is the packet's
``receipts/closures.json``. The repository root is found from this file's path, for
``devtools.audit_n11_lean``.
"""

from __future__ import annotations

import collections
import gzip
import hashlib
import json
import re
import sys
import tarfile
from pathlib import Path
from typing import BinaryIO

packet, checkout, archive = (Path(arg).resolve() for arg in sys.argv[1:4])
repo = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(repo / "packing"))

from devtools.audit_n11_lean import TOKENS, strip_code, token_counts  # noqa: E402

ARCHIVE_KEY = "certificates/generated-sources.tar.gz"
ROOTS = (
    "Sq17Lean.PackingStatement",
    "Sq17Lean.EndpointPacking",
    "Sq17Lean.EndpointGeometry",
)
THEOREM = "Sq17Lean.Square17Optimality"
NATIVE = re.compile(TOKENS["native_decide"])

manifest = json.loads(gzip.decompress((packet / "sq17-lean/manifest.json.gz").read_bytes()))
modules = {entry["module"]: (path, entry) for path, entry in manifest["sources"].items()}


def closure(root: str) -> set[str]:
    seen: set[str] = set()
    stack = [root]
    while stack:
        module = stack.pop()
        if module in seen or module not in modules:
            continue
        seen.add(module)
        stack.extend(modules[module][1]["imports"])
    return seen


closures = {root: closure(root) for root in ROOTS}
wanted = set().union(*closures.values())
texts: dict[str, bytes] = {}
mismatched: list[str] = []


def admit(module: str, data: bytes) -> None:
    entry = modules[module][1]
    if hashlib.sha256(data).hexdigest() != entry["sha256"] or len(data) != entry["bytes"]:
        mismatched.append(module)
    texts[module] = data


for module in sorted(wanted):
    path, entry = modules[module]
    if entry["archive"] is None:
        admit(module, (checkout / path).read_bytes())


class Hashing:
    """A read-only stream that hashes and counts every byte read through it."""

    def __init__(self, stream: BinaryIO) -> None:
        self.stream, self.digest, self.size = stream, hashlib.sha256(), 0

    def read(self, size: int = -1) -> bytes:
        data = self.stream.read(size)
        self.digest.update(data)
        self.size += len(data)
        return data


by_path = {path: module for module, (path, _) in modules.items() if module in wanted}
unsafe: list[str] = []
with archive.open("rb") as raw:
    stream = Hashing(raw)
    with tarfile.open(fileobj=stream, mode="r|gz") as tar:
        for member in tar:
            name = member.name.removeprefix("./")
            if name.startswith("/") or ".." in Path(name).parts or member.issym() or member.islnk():
                unsafe.append(name)
                continue
            if member.isfile() and name in by_path:
                handle = tar.extractfile(member)
                if handle is not None:
                    admit(by_path[name], handle.read())
    while stream.read(1 << 20):
        pass
recorded = manifest["archives"][ARCHIVE_KEY]


def lines(text: str, pattern: re.Pattern[str]) -> list[int]:
    return [text.count("\n", 0, match.start()) + 1 for match in pattern.finditer(text)]


def report(root: str) -> dict[str, object]:
    members = closures[root]
    per_archive = collections.Counter(modules[m][1]["archive"] or "tree" for m in members)
    totals: collections.Counter[str] = collections.Counter()
    outside_code: list[str] = []
    for module in sorted(members):
        text = texts[module].decode("utf-8")
        totals.update(token_counts(text))
        code = strip_code(text)
        in_code = set(lines(code, NATIVE))
        outside_code += [
            f"{modules[module][0]}:{line}" for line in lines(text, NATIVE) if line not in in_code
        ]
    return {
        "modules": len(members),
        "by_archive": dict(sorted(per_archive.items())),
        "archived_modules": sorted(m for m in members if modules[m][1]["archive"]),
        "read": all(m in texts for m in members),
        "mismatched": sorted(m for m in members if m in mismatched),
        "tokens_in_code": {name: totals[name] for name in TOKENS},
        "native_decide_outside_code": outside_code,
    }


print(
    json.dumps(
        {
            "format": "sq17-lean-closures-v1",
            "archive": {
                "name": ARCHIVE_KEY,
                "bytes": stream.size,
                "sha256": stream.digest.hexdigest(),
                "matches_manifest": stream.size == recorded["bytes"]
                and stream.digest.hexdigest() == recorded["sha256"],
                "unsafe_members": unsafe,
            },
            "theorem_closure_modules": len(closure(THEOREM)),
            "closures": {root: report(root) for root in ROOTS},
            "endpoint_packing_within_statement": closures["Sq17Lean.EndpointPacking"]
            <= closures["Sq17Lean.PackingStatement"],
        },
        indent=2,
        ensure_ascii=False,
    )
)
