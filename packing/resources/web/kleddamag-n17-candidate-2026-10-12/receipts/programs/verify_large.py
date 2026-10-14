"""Verify the 12 large files independently of the author's fetch_large.py.

Reads LARGE_FILES.tsv and the release metadata (gh release view JSON), hashes each file under
_large/ with hashlib, and prints one JSON receipt. Standard library only.

Usage: python -I verify_large.py EDITION_ROOT RELEASE_JSON
"""

import csv
import hashlib
import json
import os
import sys


def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    root, release_path = sys.argv[1], sys.argv[2]
    with open(os.path.join(root, "LARGE_FILES.tsv"), encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    with open(release_path, encoding="utf-8") as f:
        release = json.load(f)
    assets = {a["name"]: a for a in release["assets"]}
    out = []
    ok = True
    for r in rows:
        path = os.path.join(root, "_large", *r["path"].split("/"))
        got = sha256(path)
        size = os.path.getsize(path)
        asset = assets.get(os.path.basename(r["path"]), {})
        asset_digest = str(asset.get("digest", "")).removeprefix("sha256:")
        good = got == r["sha256"] == asset_digest and size == int(r["bytes"]) == asset.get("size")
        ok &= good
        out.append(
            {
                "path": r["path"],
                "bytes": size,
                "sha256": got,
                "matches_large_files_tsv": got == r["sha256"] and size == int(r["bytes"]),
                "matches_release_asset_digest": got == asset_digest and size == asset.get("size"),
            }
        )
    body = release["body"]
    receipt = {
        "release": {
            "tag": release["tagName"],
            "published_at": release["publishedAt"],
            "created_at": release["createdAt"],
            "target": release["targetCommitish"],
            "notes_manifest_sha256": body.split("sha256 of MANIFEST.sha256: ")[1].split()[0],
            "notes_check_py_sha256": body.split("sha256 of check.py: ")[1].split()[0],
        },
        "local": {
            "manifest_sha256": sha256(os.path.join(root, "MANIFEST.sha256")),
            "check_py_sha256": sha256(os.path.join(root, "check.py")),
            "large_files_tsv_sha256": sha256(os.path.join(root, "LARGE_FILES.tsv")),
        },
        "files": out,
        "total_bytes": sum(x["bytes"] for x in out),
        "all_match": ok,
    }
    receipt["local"]["manifest_matches_notes"] = (
        receipt["local"]["manifest_sha256"] == receipt["release"]["notes_manifest_sha256"]
    )
    receipt["local"]["check_py_matches_notes"] = (
        receipt["local"]["check_py_sha256"] == receipt["release"]["notes_check_py_sha256"]
    )
    print(json.dumps(receipt, indent=2))
    return 0 if ok and receipt["local"]["manifest_matches_notes"] else 1


if __name__ == "__main__":
    sys.exit(main())
