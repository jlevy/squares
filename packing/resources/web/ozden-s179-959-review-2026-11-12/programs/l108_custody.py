"""Custody: read-only Git plumbing on the review's clone and on this repository.

Lane L108, blind stage 4 review of jlevy/squares#959. Written after the findings were
frozen; decides nothing. Runs rev-parse, rev-list, log -1, ls-tree and hash-object only.

Usage: python -I -B l108_custody.py CLONE_DIR REPO_DIR ISSUE.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def main(argv: list[str]) -> int:
    clone, repo, issue_path = Path(argv[1]), Path(argv[2]), Path(argv[3])
    head = git(clone, "rev-parse", "HEAD").strip()
    parents = git(clone, "rev-list", "--parents", "-n", "1", "HEAD").split()[1:]
    count = int(git(clone, "rev-list", "--count", "HEAD").strip())
    fmt = git(clone, "log", "-1", "--format=%an%n%ae%n%aI%n%cn%n%ce%n%cI%n%T").splitlines()
    files: dict[str, Any] = {}
    for line in git(clone, "ls-tree", "-r", "HEAD").splitlines():
        meta, path = line.split("\t", 1)
        _mode, _kind, blob = meta.split()
        on_disk = git(clone, "hash-object", path).strip()
        files[path] = {
            "blob": blob,
            "working_tree_equals_blob": on_disk == blob,
            "sha256": hashlib.sha256((clone / path).read_bytes()).hexdigest(),
        }
    # Retained copies in this repository's tree (main) with the same blob ids.
    by_blob: dict[str, list[str]] = {}
    for line in git(repo, "ls-tree", "-r", "HEAD").splitlines():
        meta, path = line.split("\t", 1)
        blob = meta.split()[2]
        by_blob.setdefault(blob, []).append(path)
    for info in files.values():
        hits = by_blob.get(info["blob"], [])
        info["copies_in_repo"] = len(hits)
        info["copies_in_repo_first"] = sorted(hits)[:4]
    issue = json.loads(issue_path.read_text(encoding="utf-8"))
    created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
    committed = datetime.fromisoformat(fmt[5])
    out = {
        "program": "l108_custody.py",
        "repo_head": git(repo, "rev-parse", "HEAD").strip(),
        "clone_head": head,
        "commits": count,
        "parents": parents,
        "author": f"{fmt[0]} <{fmt[1]}>",
        "authored": fmt[2],
        "committer": f"{fmt[3]} <{fmt[4]}>",
        "committed": fmt[5],
        "tree": fmt[6],
        "issue_created": issue["created_at"],
        "issue_after_commit_seconds": (created - committed).total_seconds(),
        "files": files,
    }
    Path(argv[4]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
