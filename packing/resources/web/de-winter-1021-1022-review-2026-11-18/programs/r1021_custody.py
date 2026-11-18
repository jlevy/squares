"""Custody of the four source files of #1021 and #1022 (lane r1021-1118).  Decides no bound.

Usage: python -I -B r1021_custody.py CLONE PIN OUT.json FETCH_DIR [FETCH_DIR ...] [--activity ACTIVITY.json]

CLONE is a full clone of JoostdeWinter/square-packing; PIN the commit the issues pin.
Each FETCH_DIR holds the four files fetched one way (git show at the pin, the contents
API, raw.githubusercontent.com, at stated times in its fetched-at.txt).  It gives each
file's SHA-256 and Git blob id per route, the blob ids in the pin's tree and the head's,
the commits that touch n268/ and n270/, the source's own SHA256SUMS where it has one,
and, with --activity, the pushes in GitHub's activity log for the repository.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

FILES = ["n268/n268_exact.json", "n268/n268_witness.yaml", "n270/n270_exact.json", "n270/n270_witness.yaml"]


def git(clone: str, *args: str) -> str:
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True, text=True).stdout


def blob_id(raw: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()


def tree_blobs(clone: str, rev: str) -> dict:
    out = {}
    for line in git(clone, "ls-tree", "-r", "-l", rev, "n268/", "n270/").splitlines():
        meta, path = line.split("\t")
        _mode, _kind, blob, size = meta.split()
        out[path] = {"blob": blob, "bytes": int(size)}
    return out


def main(argv: list[str]) -> int:
    activity = None
    if "--activity" in argv:
        k = argv.index("--activity")
        activity = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
    clone, pin, out, *fetches = argv
    head = git(clone, "rev-parse", "HEAD").strip()
    rec: dict = {"pin": pin, "head": head, "routes": {}}
    rec["pin_tree"] = tree_blobs(clone, pin)
    rec["head_tree"] = tree_blobs(clone, "HEAD")
    for d in fetches:
        route = {}
        for path in FILES:
            raw = open(os.path.join(d, os.path.basename(path)), "rb").read()
            route[path] = {"sha256": hashlib.sha256(raw).hexdigest(), "blob": blob_id(raw), "bytes": len(raw)}
        stamp = os.path.join(d, "fetched-at.txt")
        rec["routes"][os.path.basename(d.rstrip("/"))] = {
            "fetched_at": open(stamp).read().split() if os.path.exists(stamp) else None, "files": route}
    agree = True
    for path in FILES:
        digests = {r["files"][path]["sha256"] for r in rec["routes"].values()}
        blobs = {r["files"][path]["blob"] for r in rec["routes"].values()}
        if len(digests) != 1 or blobs != {rec["pin_tree"][path]["blob"]} or rec["head_tree"][path]["blob"] != rec["pin_tree"][path]["blob"]:
            agree = False
    rec["all_routes_equal_pin_and_head"] = agree
    rec["commits"] = git(clone, "log", "--format=%H %cI %s", "--", "n268", "n270").splitlines()
    rec["all_commits"] = git(clone, "log", "--format=%H %cI %s").splitlines()[:12]
    sums = {}
    for rev in (pin, "HEAD"):
        for folder in ("n268", "n270"):
            try:
                text = git(clone, "show", f"{rev}:{folder}/SHA256SUMS")
            except subprocess.CalledProcessError:
                sums[f"{rev[:7]}:{folder}"] = None
                continue
            listed = dict(reversed(line.split("  ", 1)) for line in text.splitlines() if line.strip())
            sums[f"{rev[:7]}:{folder}"] = listed
    rec["sha256sums"] = sums
    checks = {}
    for key, listed in sums.items():
        if listed is None:
            continue
        folder = key.split(":")[1]
        first = next(iter(rec["routes"].values()))["files"]
        for path in FILES:
            if path.startswith(folder):
                name = os.path.basename(path)
                checks[f"{key}:{name}"] = listed.get(name) == first[path]["sha256"]
    rec["sha256sums_match"] = checks
    if activity:
        events = json.load(open(activity))
        rec["pushes"] = [{"before": e.get("before", "")[:7], "after": e.get("after", "")[:7], "at": e.get("timestamp"),
                          "type": e.get("activity_type"), "ref": e.get("ref")} for e in events]
    with open(out, "w") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    print("routes", list(rec["routes"]), "agree", agree, "sums", checks)
    return 0 if agree else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
