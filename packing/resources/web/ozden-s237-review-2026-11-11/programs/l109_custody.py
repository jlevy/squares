"""Lane L109's custody, licence and dating facts, after the findings were frozen.

Usage: python -I -B l109_custody.py SOURCE_DIR REPO_DIR ISSUE.json OUT.json

Decides nothing about the packing. Runs read-only Git plumbing (rev-parse, rev-list,
log -1, ls-tree, cat-file) on the clone made for this review and on this repository;
computes every file's Git blob id and SHA-256 itself and compares the blob ids with
Git's; finds the retained copies of the licence files and the author's verifier in this
repository's tree by blob id; and sets the commit's and the issue's times beside the
times the issue states.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l109_check as C  # noqa: E402

PROGRAMS = ["l109_check.py", "l109_custody.py"]
PIN = "13c4b231bb16437a6ee3751e75113ef95113b235"
MAIN = "c8448724e"


def git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout.strip()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main() -> int:
    src, repo, issue_path, out = sys.argv[1:5]
    with open(issue_path, encoding="utf-8") as f:
        issue = json.load(f)
    head = git(src, "rev-parse", "HEAD")
    commits = git(src, "rev-list", "--all").split()
    meta = git(src, "log", "-1", "--format=%H%n%P%n%T%n%an <%ae>%n%aI%n%cn <%ce>%n%cI%n%s", PIN).split("\n")
    tree = [line.split(None, 4) for line in git(src, "ls-tree", "-r", "-l", PIN).split("\n")]
    files = {}
    for mode, typ, oid, size, path in tree:
        with open(os.path.join(src, path), "rb") as f:
            data = f.read()
        files[path] = {
            "blob": oid,
            "blob_computed_equal": blob_id(data) == oid,
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
            "mode": mode,
            "type": typ,
            "size_listed": int(size),
        }
    repo_tree = git(repo, "ls-tree", "-r", MAIN)
    by_blob: dict[str, list[str]] = {}
    for line in repo_tree.split("\n"):
        left, path = line.split("\t", 1)
        oid = left.split()[2]
        by_blob.setdefault(oid, []).append(path)
    retained = {}
    for name in ("LICENSE.md", "LICENSE-evand-square-packing.txt", "verifier/sqcheck.py", "verifier/README.md"):
        paths = by_blob.get(files[name]["blob"], [])
        retained[name] = {"copies_on_main": len(paths), "examples": sorted(paths)[:6]}
    main_meta = git(repo, "log", "-1", "--format=%H%n%cI%n%s", MAIN).split("\n")
    receipt = {
        "program": "l109_custody.py",
        "programs_sha256": C.program_digests(PROGRAMS),
        "decides": "nothing",
        "clone_head": head,
        "head_is_pin": head == PIN,
        "commits_in_clone": len(commits),
        "commit": {
            "sha": meta[0],
            "parents": meta[1],
            "tree": meta[2],
            "author": meta[3],
            "authored": meta[4],
            "committer": meta[5],
            "committed": meta[6],
            "subject": meta[7],
        },
        "files": files,
        "retained_copies_on_main_by_blob": retained,
        "main": {"sha": main_meta[0], "committed": main_meta[1], "subject": main_meta[2]},
        "issue": {
            "created_at": issue["created_at"],
            "updated_at": issue["updated_at"],
            "author": issue["user"]["login"],
            "comments": issue["comments"],
            "states_check_time": "2026-11-11 13:50 PST" in issue["body"],
        },
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=1)
        f.write("\n")
    print(json.dumps(receipt, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
