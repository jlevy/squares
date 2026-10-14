"""The author's nested verifier archive, read as data: digests, build digest and diff.

Usage::

    python3 -I nested_crate.py ARCHIVE.tar.gz ARCHIVE_SHA256 EXPECTED_BUILD_SHA256 \\
        LABEL=REFERENCE_CRATE_DIR [LABEL=REFERENCE_CRATE_DIR ...]

Unpacks the archive into a fresh directory beside it (refusing any member outside the
archive's own root), lists its members with their digests, recomputes the ``source_sha256``
a build of it embeds by ``build.rs``'s rule (``Cargo.toml``, ``Cargo.lock``, ``build.rs``,
then ``src/*.rs`` sorted, each as name, NUL, bytes, NUL), and for each reference crate
directory reports which files are byte-identical and how many lines differ in the rest.
It prints no line of the archive, and it builds and runs nothing.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import shutil
import sys
import tarfile
from pathlib import Path, PurePosixPath

RULE = ("Cargo.toml", "Cargo.lock", "build.rs")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def unpack(archive: Path) -> Path:
    into = archive.with_name(archive.name + ".unpacked")
    if into.exists():
        shutil.rmtree(into)
    into.mkdir()
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            name = PurePosixPath(member.name)
            if (
                name.is_absolute()
                or ".." in name.parts
                or not (member.isfile() or member.isdir())
            ):
                msg = f"refusing member {member.name}"
                raise SystemExit(msg)
        tar.extractall(into, filter="data")
    roots = list(into.iterdir())
    if len(roots) != 1 or not roots[0].is_dir():
        msg = "the archive does not hold one root directory"
        raise SystemExit(msg)
    return roots[0]


def build_digest(crate: Path) -> str:
    names = list(RULE) + sorted(
        f"src/{p.name}" for p in (crate / "src").iterdir() if p.suffix == ".rs"
    )
    digest = hashlib.sha256()
    for name in names:
        digest.update(name.encode() + b"\0" + (crate / name).read_bytes() + b"\0")
    return digest.hexdigest()


def compare(crate: Path, reference: Path) -> dict[str, object]:
    ours = {p.relative_to(crate).as_posix(): p for p in crate.rglob("*") if p.is_file()}
    theirs = {
        p.relative_to(reference).as_posix(): p
        for p in reference.rglob("*")
        if p.is_file() and "target" not in p.parts
    }
    report: dict[str, object] = {}
    for name in sorted(set(ours) | set(theirs)):
        if name not in ours:
            report[name] = "only in the reference"
        elif name not in theirs:
            report[name] = "only in the archive"
        elif ours[name].read_bytes() == theirs[name].read_bytes():
            report[name] = "identical"
        else:
            a = theirs[name].read_text(encoding="utf-8", errors="replace").splitlines()
            b = ours[name].read_text(encoding="utf-8", errors="replace").splitlines()
            added = sum(
                1
                for line in difflib.unified_diff(a, b, lineterm="", n=0)
                if line.startswith("+") and not line.startswith("+++")
            )
            removed = sum(
                1
                for line in difflib.unified_diff(a, b, lineterm="", n=0)
                if line.startswith("-") and not line.startswith("---")
            )
            report[name] = f"differs: +{added} -{removed} lines against the reference"
    return report


def main(argv: list[str]) -> int:
    archive, expected, expected_build = Path(argv[1]), argv[2], argv[3]
    data = archive.read_bytes()
    if sha256(data) != expected:
        msg = f"{archive} hashes to {sha256(data)}, not {expected}"
        raise SystemExit(msg)
    crate = unpack(archive)
    members = {
        p.relative_to(crate).as_posix(): {
            "bytes": p.stat().st_size,
            "sha256": sha256(p.read_bytes()),
        }
        for p in sorted(crate.rglob("*"))
        if p.is_file()
    }
    digest = build_digest(crate)
    references = {}
    for spec in argv[4:]:
        label, path = spec.split("=", 1)
        references[label] = compare(crate, Path(path))
    report = {
        "archive_sha256": expected,
        "archive_bytes": len(data),
        "root": crate.name,
        "members": members,
        "build_source_sha256": digest,
        "build_source_sha256_is_expected": digest == expected_build,
        "against": references,
    }
    shutil.rmtree(crate.parent)
    sys.stdout.write(json.dumps(report, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
