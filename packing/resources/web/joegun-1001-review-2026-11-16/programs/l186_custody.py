"""Lane L186, after the freeze: custody of the five certificates. Decides nothing.

Usage: python -I -B l186_custody.py CLONE PIN ISSUE.json OUT.json

Runs read-only Git plumbing on the clone (rev-parse, log, ls-tree, cat-file,
merge-base, diff) and records: the commits (hash, author and committer times,
subject; no names or e-mail addresses), the pin's tree with blob ids and sizes, the
SHA-256 of each candidate blob at the pin and at every later commit, the files that
differ between the pin and the head, and the issue's stated digests and times.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from typing import Any

COUNTS = ("127", "204", "232", "264", "305")


def git(clone: str, *args: str) -> str:
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True, text=True).stdout


def blob_sha256(clone: str, rev: str, path: str) -> str | None:
    try:
        data = subprocess.run(
            ["git", "-C", clone, "cat-file", "blob", f"{rev}:{path}"], check=True, capture_output=True
        ).stdout
    except subprocess.CalledProcessError:
        return None
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    clone, pin, issue_path, out_path = sys.argv[1:5]
    with open(issue_path) as fh:
        issue = json.load(fh)
    head = git(clone, "rev-parse", "HEAD").strip()
    remote_head = git(clone, "rev-parse", "refs/remotes/origin/HEAD").strip()
    log = [
        dict(zip(("hash", "author_time", "committer_time", "subject"), line.split("\x1f"), strict=True))
        for line in git(clone, "log", "--all", "--format=%H\x1f%aI\x1f%cI\x1f%s").splitlines()
    ]
    tree = []
    for line in git(clone, "ls-tree", "-r", "-l", pin).splitlines():
        meta, path = line.split("\t", 1)
        _, kind, blob, size = meta.split()
        tree.append({"path": path, "kind": kind, "blob": blob, "size": int(size)})
    stated = issue["stated_sha256"]
    cand: dict[str, Any] = {}
    for n in COUNTS:
        path = f"n-{n}-candidate.yaml"
        at_pin = blob_sha256(clone, pin, path)
        later = {c["hash"][:12]: blob_sha256(clone, c["hash"], path) for c in log}
        cand[n] = {
            "path": path,
            "sha256_at_pin": at_pin,
            "issue_sha256": stated[n],
            "matches_issue": at_pin == stated[n],
            "sha256_at_every_commit": later,
            "unchanged_at_every_commit": all(v == at_pin for v in later.values()),
        }
    diff_names = git(clone, "diff", "--name-only", pin, remote_head).split()
    rec = {
        "pin": pin,
        "head": head,
        "remote_head": remote_head,
        "pin_is_remote_head": pin == remote_head,
        "pin_is_ancestor_of_remote_head": git(clone, "merge-base", pin, remote_head).strip() == pin,
        "commits": log,
        "tree_at_pin": tree,
        "files_differing_pin_to_remote_head": diff_names,
        "candidates": cand,
        "issue": {k: issue[k] for k in ("number", "created_at", "fetched_at", "comments", "labels")},
    }
    with open(out_path, "w") as fh:
        json.dump(rec, fh, indent=1)
        fh.write("\n")
    print(
        "pin is remote head:",
        rec["pin_is_remote_head"],
        "commits:",
        len(log),
        "all match issue:",
        all(c["matches_issue"] for c in cand.values()),
        "unchanged:",
        all(c["unchanged_at_every_commit"] for c in cand.values()),
    )


if __name__ == "__main__":
    main()
