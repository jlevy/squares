#!/usr/bin/env python3
"""Pack deterministic checkpoint archives and verify frozen legacy manifests.

New archives retain the original receipts and their Git/path provenance without adding
checksum sidecars. Packing accepts a flat directory of regular files and excludes macOS
metadata. Legacy manifest checking remains available for already retained evidence.

Usage:
    python -m devtools.checkpoint_manifest check MANIFEST [MANIFEST ...]
    python -m devtools.checkpoint_manifest pack DIR ARCHIVE [--force]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import stat
import sys
import tarfile
from datetime import UTC, datetime
from pathlib import Path

from strif import atomic_output_file

# macOS metadata that must never appear in a checkpoint archive.
_JUNK_BASENAMES = frozenset({".DS_Store"})


def _is_junk(name: str) -> bool:
    """AppleDouble resource-fork files and `.DS_Store`."""
    basename = Path(name).name
    return basename.startswith("._") or basename in _JUNK_BASENAMES


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------


def _check_one(manifest_path: Path) -> list[str]:
    """Verify one manifest against its archive. Returns a list of problems."""
    problems: list[str] = []
    label = manifest_path.name

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{label}: cannot read manifest: {exc}"]

    archive_name = manifest.get("archive", "")
    archive_path = manifest_path.parent / archive_name
    if not archive_path.is_file():
        return [f"{label}: archive {archive_name!r} not found beside the manifest"]

    # archive_sha256
    archive_bytes = archive_path.read_bytes()
    actual_sha = hashlib.sha256(archive_bytes).hexdigest()
    if actual_sha != manifest.get("archive_sha256"):
        problems.append(
            f"{label}: archive SHA-256 mismatch: "
            f"manifest says {manifest.get('archive_sha256')}, actual {actual_sha}"
        )

    # Open the tar and collect members, checking for junk and unsafe paths.
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
            members = tar.getmembers()
            archive_files: dict[str, tuple[int, str]] = {}
            seen: set[str] = set()
            for member in members:
                root = member.isdir() and member.name in (".", "./")
                name = "." if root else member.name.removeprefix("./")
                if name in seen:
                    problems.append(f"{label}: duplicate normalized member name: {name!r}")
                    continue
                seen.add(name)
                if root:
                    continue
                if not member.isfile():
                    problems.append(f"{label}: nonregular member: {member.name!r}")
                    continue
                if not name or name in (".", "..") or "/" in name:
                    problems.append(f"{label}: member is not a flat filename: {member.name!r}")
                    continue
                if _is_junk(name):
                    problems.append(
                        f"{label}: archive contains macOS metadata: {member.name!r}"
                    )
                    continue
                reader = tar.extractfile(member)
                if reader is None:
                    problems.append(f"{label}: cannot read {member.name!r}")
                    continue
                data = reader.read()
                archive_files[name] = (len(data), hashlib.sha256(data).hexdigest())
    except (tarfile.TarError, OSError) as exc:
        return [*problems, f"{label}: cannot read archive: {exc}"]

    manifest_files: dict[str, dict[str, object]] = manifest.get("files", {})

    # file set equality
    manifest_names = set(manifest_files.keys())
    archive_names = set(archive_files.keys())
    problems.extend(
        f"{label}: manifest lists {m!r} but archive does not contain it"
        for m in sorted(manifest_names - archive_names)
    )
    problems.extend(
        f"{label}: archive contains {e!r} but manifest does not list it"
        for e in sorted(archive_names - manifest_names)
    )

    # per-file bytes and sha256
    for name in sorted(manifest_names & archive_names):
        expected = manifest_files[name]
        actual_bytes, actual_hash = archive_files[name]
        if expected.get("bytes") != actual_bytes:
            problems.append(
                f"{label}: {name}: bytes mismatch: "
                f"manifest {expected.get('bytes')}, actual {actual_bytes}"
            )
        if expected.get("sha256") != actual_hash:
            problems.append(
                f"{label}: {name}: sha256 mismatch: "
                f"manifest {expected.get('sha256')}, actual {actual_hash}"
            )

    # file_count and uncompressed_bytes
    if manifest.get("file_count") != len(archive_files):
        problems.append(
            f"{label}: file_count mismatch: "
            f"manifest {manifest.get('file_count')}, actual {len(archive_files)}"
        )
    total_bytes = sum(size for size, _ in archive_files.values())
    if manifest.get("uncompressed_bytes") != total_bytes:
        problems.append(
            f"{label}: uncompressed_bytes mismatch: "
            f"manifest {manifest.get('uncompressed_bytes')}, actual {total_bytes}"
        )

    return problems


def check(manifests: list[Path]) -> int:
    """Verify each manifest. Returns 0 on success, 1 on any problem."""
    all_ok = True
    for manifest_path in manifests:
        problems = _check_one(manifest_path)
        if problems:
            all_ok = False
            for problem in problems:
                print(f"FAIL {problem}", file=sys.stderr)
        else:
            print(f"  {manifest_path.name}: OK")
    return 0 if all_ok else 1


# ---------------------------------------------------------------------------
# pack
# ---------------------------------------------------------------------------


def _read_run_receipt(directory: Path) -> dict[str, object]:
    """Find and parse the single `run-*.json` in `directory`."""
    candidates = sorted(directory.glob("run-*.json"))
    if len(candidates) != 1:
        raise SystemExit(
            f"expected exactly one run-*.json in {directory}, found {len(candidates)}"
        )
    return json.loads(candidates[0].read_text(encoding="utf-8"))  # pyright: ignore[reportReturnType]


def pack(directory: Path, archive_path: Path, *, force: bool) -> None:
    """Build only a deterministic flat archive, preserving embedded receipts unchanged."""
    if not force and archive_path.exists():
        raise SystemExit(f"archive already exists (use --force to overwrite): {archive_path}")

    entries: list[Path] = []
    for entry in sorted(directory.iterdir()):
        # lstat rejects links rather than following them, including metadata links.
        if not stat.S_ISREG(entry.lstat().st_mode):
            raise SystemExit(f"checkpoint entry must be a regular file: {entry}")
        if not _is_junk(entry.name):
            entries.append(entry)

    run = _read_run_receipt(directory)
    started_at = str(run["started_at"])

    # Parse started_at into a Unix timestamp for deterministic mtime.
    dt = datetime.fromisoformat(started_at)
    mtime = int(dt.replace(tzinfo=UTC if dt.tzinfo is None else dt.tzinfo).timestamp())

    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        for entry in entries:
            data = entry.read_bytes()
            info = tarfile.TarInfo(name=entry.name)
            info.size, info.uid, info.gid = len(data), 0, 0
            info.uname, info.gname, info.mode, info.mtime = "", "", 0o644, mtime
            tar.addfile(info, io.BytesIO(data))

    # Deterministic gzip: mtime=0, no filename header.
    gz_buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=gz_buffer, mode="wb", mtime=0) as gz:
        gz.write(tar_buffer.getvalue())
    archive_bytes = gz_buffer.getvalue()

    with atomic_output_file(archive_path, force=force) as tmp:
        tmp.write_bytes(archive_bytes)

    print(f"  packed {len(entries)} files into {archive_path.name}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m devtools.checkpoint_manifest",
        description="Pack and verify validation checkpoint archives.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check_p = sub.add_parser("check", help="Verify manifests against their archives.")
    check_p.add_argument("manifests", nargs="+", type=Path, metavar="MANIFEST")

    pack_p = sub.add_parser(
        "pack", help="Build a deterministic archive without a checksum sidecar."
    )
    pack_p.add_argument("directory", type=Path, metavar="DIRECTORY")
    pack_p.add_argument("archive", type=Path, metavar="ARCHIVE")
    pack_p.add_argument("--force", action="store_true")

    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "check":
        return check(args.manifests)
    if args.command == "pack":
        pack(args.directory, args.archive, force=args.force)
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
