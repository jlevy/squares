#!/usr/bin/env python3
"""Pack a validation checkpoint into a deterministic tar.gz and verify it with a manifest.

Validation checkpoint archives are retained timing evidence (OR-14). They must be
byte-reproducible, free of macOS metadata (AppleDouble `._*`, `.DS_Store`), and paired
with a SHA-256 manifest so that drift is machine-checkable. The 2026-09-06 integrated-fast
archive was committed with 410 AppleDouble resource-fork entries and no manifest; this
tool closes both gaps.

The manifest shape matches the sibling
`2026-09-06-pre-main-integration.manifest.json`: top-level keys `archive`,
`archive_sha256`, `file_count`, `files`, `outcome`, `provenance`, `scope`, and
`uncompressed_bytes`.

Usage:
    python -m devtools.checkpoint_manifest check MANIFEST [MANIFEST ...]
    python -m devtools.checkpoint_manifest pack DIR ARCHIVE --scope TEXT \\
        --wall-seconds N --wall-seconds-source TEXT [--failure TEXT] [--force]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
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


def _is_unsafe(name: str) -> bool:
    """Absolute paths, `..` components, or directory entries other than `.`."""
    return name.startswith("/") or ".." in name.split("/")


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
            for member in members:
                if member.isdir():
                    if member.name not in (".", "./"):
                        problems.append(f"{label}: directory other than `.`: {member.name!r}")
                    continue
                if not member.isfile():
                    continue
                if _is_junk(member.name):
                    problems.append(
                        f"{label}: archive contains macOS metadata: {member.name!r}"
                    )
                    continue
                if _is_unsafe(member.name):
                    problems.append(f"{label}: unsafe member name: {member.name!r}")
                    continue
                reader = tar.extractfile(member)
                if reader is None:
                    problems.append(f"{label}: cannot read {member.name!r}")
                    continue
                data = reader.read()
                basename = Path(member.name).name
                archive_files[basename] = (len(data), hashlib.sha256(data).hexdigest())
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


def _read_step_receipts(directory: Path) -> list[dict[str, object]]:
    """Read every `step-*.json`."""
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(directory.glob("step-*.json"))
    ]


_PROVENANCE_KEYS = (
    "available_cpus",
    "commit",
    "dirty_diff_sha256",
    "inner_jobs",
    "jobs",
    "platform",
    "python",
    "run_id",
    "started_at",
)


def _provenance_from_run(run: dict[str, object]) -> dict[str, object]:
    """Extract the nine provenance keys from the run receipt."""
    return {k: run[k] for k in _PROVENANCE_KEYS}


def _outcome_from_steps(
    steps: list[dict[str, object]],
    wall_seconds: float,
    wall_seconds_source: str,
    failure: str | None,
) -> dict[str, object]:
    """Build the outcome object from step receipts."""
    passed = sum(1 for s in steps if s.get("status") == "passed")
    failed = len(steps) - passed
    outcome: dict[str, object] = {
        "failed": failed,
        "passed": passed,
        "steps": len(steps),
        "wall_seconds": wall_seconds,
        "wall_seconds_source": wall_seconds_source,
    }
    if failure is not None:
        outcome["failure"] = failure
    return outcome


def pack(
    directory: Path,
    archive_path: Path,
    *,
    scope: str,
    wall_seconds: float,
    wall_seconds_source: str,
    failure: str | None,
    force: bool,
) -> None:
    """Build a deterministic flat tar.gz and its SHA-256 manifest."""
    manifest_path = archive_path.parent / archive_path.name.replace(".tar.gz", ".manifest.json")
    if not force:
        if archive_path.exists():
            raise SystemExit(
                f"archive already exists (use --force to overwrite): {archive_path}"
            )
        if manifest_path.exists():
            raise SystemExit(
                f"manifest already exists (use --force to overwrite): {manifest_path}"
            )

    # Collect regular files, skipping junk.
    entries = [c for c in sorted(directory.iterdir()) if c.is_file() and not _is_junk(c.name)]

    run = _read_run_receipt(directory)
    started_at = str(run["started_at"])

    # Parse started_at into a Unix timestamp for deterministic mtime.
    dt = datetime.fromisoformat(started_at)
    mtime = int(dt.replace(tzinfo=UTC if dt.tzinfo is None else dt.tzinfo).timestamp())

    # Build file manifest while collecting tar members.
    files: dict[str, dict[str, object]] = {}
    sizes: list[int] = []
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        for entry in entries:
            data = entry.read_bytes()
            sizes.append(len(data))
            files[entry.name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            info = tarfile.TarInfo(name=entry.name)
            info.size, info.uid, info.gid = len(data), 0, 0
            info.uname, info.gname, info.mode, info.mtime = "", "", 0o644, mtime
            tar.addfile(info, io.BytesIO(data))

    # Deterministic gzip: mtime=0, no filename header.
    gz_buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=gz_buffer, mode="wb", mtime=0) as gz:
        gz.write(tar_buffer.getvalue())
    archive_bytes = gz_buffer.getvalue()

    steps = _read_step_receipts(directory)
    manifest: dict[str, object] = {
        "archive": archive_path.name,
        "archive_sha256": hashlib.sha256(archive_bytes).hexdigest(),
        "file_count": len(files),
        "files": dict(sorted(files.items())),
        "outcome": _outcome_from_steps(steps, wall_seconds, wall_seconds_source, failure),
        "provenance": _provenance_from_run(run),
        "scope": scope,
        "uncompressed_bytes": sum(sizes),
    }

    manifest_text = json.dumps(manifest, sort_keys=True, indent=2) + "\n"

    # Write both atomically; they are retained evidence.
    with atomic_output_file(archive_path, force=force) as tmp:
        tmp.write_bytes(archive_bytes)
    with atomic_output_file(manifest_path, force=force) as tmp:
        tmp.write_text(manifest_text, encoding="utf-8")

    print(f"  packed {len(entries)} files into {archive_path.name}")
    print(f"  manifest written to {manifest_path.name}")


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

    pack_p = sub.add_parser("pack", help="Build a deterministic archive and manifest.")
    pack_p.add_argument("directory", type=Path, metavar="DIRECTORY")
    pack_p.add_argument("archive", type=Path, metavar="ARCHIVE")
    pack_p.add_argument("--scope", required=True)
    pack_p.add_argument("--wall-seconds", required=True, type=float)
    pack_p.add_argument("--wall-seconds-source", required=True)
    pack_p.add_argument("--failure", default=None)
    pack_p.add_argument("--force", action="store_true")

    return parser


def main() -> int:
    args = _parser().parse_args()
    if args.command == "check":
        return check(args.manifests)
    if args.command == "pack":
        pack(
            args.directory,
            args.archive,
            scope=args.scope,
            wall_seconds=args.wall_seconds,
            wall_seconds_source=args.wall_seconds_source,
            failure=args.failure,
            force=args.force,
        )
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
