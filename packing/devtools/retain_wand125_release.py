"""Retain what a stage 4 replay reads from a wand125 certificate kept outside Git.

The 10 October packets of ``wand125/square-packing`` (``resources/web/wand125-fine-net-*``
and ``wand125-linear-n122-2026-10-10``) were written as authored facts and hash
references. Each ``source-manifest.json`` pins the certificate's release asset by size
and SHA-256, every member of that asset and every document of the pinned commit by
SHA-256. A complete replay reads its certificate from the packet, where the stage 4 tools
look for it: `devtools.sqverify_fast_census` reads
``square-packing-bounds/certificates/NAME/candidate.json.gz``, and
`devtools.audit_wand125_linear` reads a linear certificate's five small files beside the
two acquisition pins. This command writes those files from a local copy of the asset and
from the pinned commit, and refuses any byte whose digest is not the manifest's.
Nothing else of the asset is written: its run logs, its sealed bundles, its proof bundle
and the adapted verifier's source stay with their author.

- ``PACKET NAME --asset ASSET --members candidate.json`` writes the chosen asset members
  under ``PACKET/square-packing-bounds/certificates/NAME/`` at their upstream names; a
  data file of more than 1,000 lines is stored as deterministic gzip
  (`devtools.retained_data`). ``--documents README.md ...`` adds documents of the pinned
  commit, fetched by their raw address. It prints the README's Compressed Files rows.
- ``--acquisition`` also writes the pins `devtools.audit_wand125_linear` reads, for a
  linear certificate: ``acquisition/upstream-subtree.sha256``, every file of the
  certificate directory, documents and asset members alike, and the project notice, by
  SHA-256 with paths relative to ``problems/square-lower-bounds/``; and
  ``acquisition/sources.json`` (`FORMAT`): the commit, the retained files, every other
  file pinned only, with its size, digest and reason, and the release asset with the
  members it holds, from which ``--via release`` fetches the proof bundle.

``square-packing-bounds/`` is the directory name the earlier ``wand125/square-packing-bounds``
packets archive under and the census and the linear tools read; here it stands for
``problems/square-lower-bounds/`` of ``wand125/square-packing``.

From ``packing/``::

    .venv/bin/python3 -m devtools.retain_wand125_release \\
        resources/web/wand125-fine-net-n29-2026-10-10 mixed_n29_L582 \\
        --asset ASSET.tar.gz --members candidate.json
    .venv/bin/python3 -m devtools.retain_wand125_release \\
        resources/web/wand125-linear-n122-2026-10-10 mixed_n122_L1126 \\
        --asset ASSET.tar.gz --members candidate.json certificate.json \\
        --documents README.md manifest.json completion-audit.json --acquisition
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tarfile
import urllib.request
from collections.abc import Callable
from pathlib import Path, PurePosixPath
from typing import Any

from devtools.retained_data import (
    DATA_SUFFIXES,
    LINE_THRESHOLD,
    compress,
    describe,
    git_blob,
)
from sqpack import retained_json

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent
#: The archived directory the census and the linear tools read under a packet.
ARCHIVED = "square-packing-bounds"
#: The source directory that ``ARCHIVED`` stands for in ``wand125/square-packing``.
UPSTREAM_ROOT = PurePosixPath("problems/square-lower-bounds")
#: The format of the ``acquisition/sources.json`` this command writes.
FORMAT = "release-asset-retention-v1"
#: The project notice every certificate directory sits under, and its retained copy.
NOTICE = "LICENSE"
NOTICE_COPY = (
    PROJECT
    / "resources/web/wand125-rectangle-certificates-2026-09-27/wand125-rectangles/LICENSE"
)
#: Bounds on the asset and on the one member read at a time.
MAX_ASSET_BYTES = 64 * 1024 * 1024
MAX_MEMBER_BYTES = 64 * 1024 * 1024

Fetch = Callable[[str], bytes]


def require(condition: object, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_url(url: str) -> bytes:
    """A document of the pinned commit, by its raw address."""
    with urllib.request.urlopen(url, timeout=120) as response:
        data: bytes = response.read(MAX_MEMBER_BYTES + 1)
    require(len(data) <= MAX_MEMBER_BYTES, f"{url} exceeds {MAX_MEMBER_BYTES} bytes")
    return data


def certificate_entry(manifest: dict[str, Any], name: str) -> dict[str, Any]:
    """The manifest's entry for one certificate: the whole manifest for a packet of one,
    or the ``certificates`` row named ``name``."""
    if "certificates" in manifest:
        rows = [row for row in manifest["certificates"] if row.get("certificate") == name]
        require(len(rows) == 1, f"the manifest has {len(rows)} entries for {name}")
        entry = dict(rows[0])
        entry.setdefault("source_repository", manifest["source_repository"])
        entry.setdefault("license", manifest.get("license"))
        return entry
    asset = str(manifest["release"]["asset"])
    require(asset == f"certificates__{name}.tar.gz", f"the manifest pins {asset}, not {name}")
    return manifest


def raw_url(repository: str, revision: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{repository}/{revision}/{path}"


def asset_members(asset: Path, entry: dict[str, Any], name: str) -> dict[str, bytes]:
    """Every member of the pinned asset the manifest lists, read from the asset after its
    size and SHA-256 are the manifest's, each refused unless it has its listed digest and
    the asset holds nothing else but plain files and directories under the certificate."""
    pin = entry["release"]
    size = asset.stat().st_size
    require(size == pin["bytes"] <= MAX_ASSET_BYTES, f"{asset} is not {pin['bytes']} bytes")
    require(sha256(asset.read_bytes()) == pin["sha256"], f"{asset} is not the pinned asset")
    listed = {str(row["path"]): str(row["sha256"]) for row in entry["asset_members"]}
    root = PurePosixPath("certificates", name)
    found: dict[str, bytes] = {}
    with tarfile.open(asset, "r:gz") as archive:
        for member in archive.getmembers():
            path = PurePosixPath(member.name)
            require(
                path.parts[: len(root.parts)] == root.parts
                and ".." not in path.parts
                and not path.is_absolute()
                and (member.isfile() or member.isdir())
                and member.size <= MAX_MEMBER_BYTES,
                f"unexpected archive member: {member.name}",
            )
            if not member.isfile():
                continue
            relative = path.relative_to(root).as_posix()
            stream = archive.extractfile(member)
            require(stream is not None, f"{member.name} cannot be read")
            assert stream is not None
            data = stream.read()
            require(
                listed.get(relative) == sha256(data), f"{relative} is not the listed member"
            )
            found[relative] = data
    require(set(found) == set(listed), f"the asset lacks {sorted(set(listed) - set(found))}")
    return found


def documents_of(entry: dict[str, Any], name: str) -> dict[str, dict[str, Any]]:
    """The manifest's pinned documents of the certificate directory, by relative path,
    with the raw address each is fetched from."""
    prefix = f"{UPSTREAM_ROOT}/certificates/{name}/"
    rows: dict[str, dict[str, Any]] = {}
    for row in entry["source_documents"]:
        path = str(row["path"])
        if path.startswith(prefix):
            raw = raw_url(entry["source_repository"], entry["source_revision"], path)
            rows[path.removeprefix(prefix)] = row | {"raw": raw}
    return rows


def compressed(name: str, data: bytes) -> bool:
    """Whether a retained file is stored as deterministic gzip: a data file of more than
    `LINE_THRESHOLD` lines, the archive's rule."""
    return PurePosixPath(name).suffix in DATA_SUFFIXES and data.count(b"\n") > LINE_THRESHOLD


def write_retained(directory: Path, name: str, data: bytes) -> Path:
    """One upstream file at its upstream name, compressed where the archive's rule says."""
    target = directory / name
    target.parent.mkdir(parents=True, exist_ok=True)
    stale = target.with_name(target.name + ".gz")
    for path in (target, stale):
        path.unlink(missing_ok=True)
    target.write_bytes(data)
    return compress(target) if compressed(name, data) else target


def notice_pin(entry: dict[str, Any]) -> dict[str, Any]:
    """The project notice, bound to the retained copy by its Git blob."""
    notice = (entry.get("license") or {}).get("project_notice") or {}
    data = NOTICE_COPY.read_bytes()
    require(
        notice.get("path") == f"{UPSTREAM_ROOT}/{NOTICE}"
        and notice.get("git_blob") == git_blob(data)
        and notice.get("bytes") == len(data),
        "the project notice is not the retained MIT notice",
    )
    return {
        "path": NOTICE,
        "bytes": len(data),
        "sha256": sha256(data),
        "reason": "the MIT notice the certificate directory sits under, retained byte-identical"
        " by the 2026-09-27 rectangle packet",
        "identical_to": NOTICE_COPY.relative_to(REPO).as_posix(),
    }


def pinned_reason(relative: str, row: dict[str, Any], *, in_asset: bool) -> dict[str, Any]:
    """Why one file of the directory is pinned and not retained."""
    if in_asset:
        reason = (
            "a member of the release asset below, which stays with its author; "
            "audit_wand125_linear --via release fetches it and refuses other bytes"
        )
    elif row.get("byte_identical_to_retained"):
        reason = "byte-identical to the retained copy named, which the linear tools read"
    else:
        reason = "a document the replay does not read"
    pinned = {"reason": reason}
    if row.get("byte_identical_to_retained"):
        copy = REPO / str(row["byte_identical_to_retained"])
        require(sha256(copy.read_bytes()) == row["sha256"], f"{relative}'s copy differs")
        pinned["identical_to"] = str(row["byte_identical_to_retained"])
    return pinned


def acquisition(
    packet: Path,
    entry: dict[str, Any],
    name: str,
    *,
    retained: dict[str, Path],
    members: dict[str, bytes],
    documents: dict[str, dict[str, Any]],
) -> tuple[str, dict[str, Any]]:
    """The subtree pins and the acquisition record of a linear certificate's packet."""
    directory = f"certificates/{name}"
    files: dict[str, dict[str, Any]] = {}
    for relative, row in documents.items():
        files[f"{directory}/{relative}"] = {"bytes": row["bytes"], "sha256": row["sha256"]}
    for relative, data in members.items():
        files[f"{directory}/{relative}"] = {"bytes": len(data), "sha256": sha256(data)}
    notice = notice_pin(entry)
    files[NOTICE] = {"bytes": notice["bytes"], "sha256": notice["sha256"]}
    subtree = "".join(f"{files[path]['sha256']}  ./{path}\n" for path in sorted(files))
    kept = {f"{directory}/{relative}" for relative in retained}
    pinned: list[dict[str, Any]] = [notice]
    for path in sorted(set(files) - kept - {NOTICE}):
        relative = path.removeprefix(f"{directory}/")
        row = documents.get(relative, {})
        pinned.append(
            {"path": path, **files[path]}
            | pinned_reason(relative, row, in_asset=relative in members)
        )
    pin = entry["release"]
    root = (packet.relative_to(REPO) if packet.is_relative_to(REPO) else packet).as_posix()
    record = {
        "format": FORMAT,
        "written_by": "devtools.retain_wand125_release",
        "source_manifest": f"{root}/source-manifest.json",
        "sources": [
            {
                "id": f"wand125-square-packing-{name}",
                "source_url": f"https://github.com/{entry['source_repository']}",
                "source_commit": entry["source_revision"],
                "committed_utc": entry["source_revision_date"],
                "upstream_root": str(UPSTREAM_ROOT),
                "archived_path": f"{root}/{ARCHIVED}",
                "subtree_manifest": f"{root}/acquisition/upstream-subtree.sha256",
                "subtree_scope": [NOTICE, directory],
                "subtree_file_count": len(files),
                "subtree_total_bytes": sum(row["bytes"] for row in files.values()),
                "retained": [
                    {
                        "path": f"{directory}/{relative}",
                        "stored": path.relative_to(packet).as_posix(),
                        **files[f"{directory}/{relative}"],
                    }
                    for relative, path in sorted(retained.items())
                ],
                "pinned_only": pinned,
                "release_assets": [
                    {
                        "repository": pin["repository"],
                        "tag": pin["tag"],
                        "asset": pin["asset"],
                        "url": pin["url"],
                        "bytes": pin["bytes"],
                        "sha256": pin["sha256"],
                        "members": [
                            {
                                "member": f"{directory}/{relative}",
                                "path": f"{directory}/{relative}",
                                **files[f"{directory}/{relative}"],
                            }
                            for relative in sorted(members)
                        ],
                    }
                ],
            }
        ],
    }
    return subtree, record


def retain(
    packet: Path,
    name: str,
    asset: Path,
    *,
    members: list[str],
    documents: list[str],
    write_acquisition: bool,
    fetch: Fetch = fetch_url,
) -> dict[str, Any]:
    """Write the chosen members and documents, and the acquisition pins if asked."""
    manifest = json.loads((packet / "source-manifest.json").read_text(encoding="utf-8"))
    entry = certificate_entry(manifest, name)
    found = asset_members(asset, entry, name)
    pinned = documents_of(entry, name)
    require(
        set(members) <= set(found), f"not members of the asset: {set(members) - set(found)}"
    )
    require(
        set(documents) <= set(pinned), f"not pinned documents: {set(documents) - set(pinned)}"
    )
    directory = packet / ARCHIVED / "certificates" / name
    chosen: dict[str, bytes] = {relative: found[relative] for relative in members}
    for relative in documents:
        data = fetch(pinned[relative]["raw"])
        require(sha256(data) == pinned[relative]["sha256"], f"{relative} is not the pinned one")
        chosen[relative] = data
    retained = {
        relative: write_retained(directory, relative, data)
        for relative, data in sorted(chosen.items())
    }
    rows = [
        describe(packet, path, "upstream").markdown()
        for path in retained.values()
        if path.suffix == ".gz"
    ]
    if write_acquisition:
        subtree, record = acquisition(
            packet, entry, name, retained=retained, members=found, documents=pinned
        )
        (packet / "acquisition").mkdir(exist_ok=True)
        (packet / "acquisition/upstream-subtree.sha256").write_text(subtree, encoding="utf-8")
        text = retained_json.dumps(record)
        (packet / "acquisition/sources.json").write_text(text, encoding="utf-8")
    return {
        "certificate": name,
        "retained": {
            relative: path.relative_to(packet).as_posix() for relative, path in retained.items()
        },
        "compressed_rows": rows,
        "acquisition": write_acquisition,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("packet", type=Path, help="the packet directory")
    parser.add_argument("name", help="the certificate directory's name, mixed_nN_LX")
    parser.add_argument("--asset", type=Path, required=True, help="a local copy of the asset")
    parser.add_argument("--members", nargs="+", default=["candidate.json"])
    parser.add_argument("--documents", nargs="*", default=[])
    parser.add_argument(
        "--acquisition",
        action="store_true",
        help="also write acquisition/upstream-subtree.sha256 and acquisition/sources.json",
    )
    args = parser.parse_args(argv)
    try:
        result = retain(
            args.packet.resolve(),
            args.name,
            args.asset,
            members=args.members,
            documents=args.documents,
            write_acquisition=args.acquisition,
        )
    except (ValueError, OSError, tarfile.TarError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
