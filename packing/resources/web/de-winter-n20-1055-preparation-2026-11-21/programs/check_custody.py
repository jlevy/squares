"""Read archive members as bytes; never import or execute submitted programs."""

from __future__ import annotations

import argparse
import hashlib
import json
import signal
import sys
import time
import zipfile
from pathlib import Path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--original", type=Path, help="Optional original lower_n20 directory")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assert __debug__, "Assertions must be enabled."
    signal.alarm(120)
    start = time.monotonic()
    packet = Path(__file__).resolve().parents[1]
    manifest = json.loads((packet / "acquisition/manifest.json").read_text())
    raw = args.archive.read_bytes()
    assert len(raw) == manifest["archive"]["bytes"]
    assert sha256(raw) == manifest["archive"]["sha256"]
    with zipfile.ZipFile(args.archive) as archive:
        names = [info.filename for info in archive.infolist() if not info.is_dir()]
        assert len(names) == len(set(names))
        entries = {}
        for line in archive.read("SHA256SUMS").decode().splitlines():
            digest, name = line.split(maxsplit=1)
            assert name not in entries
            entries[name] = digest
            assert sha256(archive.read(name)) == digest, name
        assert set(names) == set(entries) | {"SHA256SUMS"}
        for row in manifest["retained_members"]:
            data = archive.read(row["member"])
            assert len(data) == row["bytes"]
            assert sha256(data) == row["sha256"]
            assert data == (packet / row["retained_as"]).read_bytes()
        upstream = json.loads((packet / "acquisition/upstream-blobs.json").read_text())
        for name, expected in upstream["files"].items():
            data = archive.read("base496/upstream/" + name)
            blob = b"blob " + str(len(data)).encode() + b"\0" + data
            assert hashlib.sha1(blob).hexdigest() == expected, name
        result = {
            "format": "n20-custody-check-v1",
            "archive_sha256": sha256(raw),
            "archive_bytes": len(raw),
            "archive_files": len(names),
            "manifest_members_checked": len(entries),
            "upstream_git_blobs_checked": len(upstream["files"]),
            "retained_members_identical": len(manifest["retained_members"]),
        }
    if args.original:
        original = {}
        for line in (args.original / "SHA256SUMS").read_text().splitlines():
            digest, name = line.split(maxsplit=1)
            assert sha256((args.original / name).read_bytes()) == digest, name
            original[name] = digest
        result["original_495_members_checked"] = original
    result["elapsed_seconds"] = round(time.monotonic() - start, 6)
    with args.output.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    sys.stdout.write(json.dumps(result) + "\n")


if __name__ == "__main__":
    main()
