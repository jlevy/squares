"""Lane L117, after the freeze: custody, licence and dating. Decides nothing.

Runs read-only Git plumbing (rev-parse, rev-list, log -1, ls-tree, hash-object, status)
on the clone made for this review and on this repository, hashes the clone's files, and
compares the commit's and the issue's times.

Usage: python -I -B l117_custody.py CLONE_DIR REPO_DIR ISSUE.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime


def git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout.strip()


def t(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def main(argv: list[str]) -> int:
    clone, repo, ipath, opath = argv[1:5]
    with open(ipath, encoding="utf-8") as fh:
        issue = json.load(fh)
    head = git(clone, "rev-parse", "HEAD")
    fmt = "%H%n%P%n%an <%ae>%n%aI%n%cn <%ce>%n%cI%n%T"
    h, parents, author, adate, committer, cdate, tree = git(clone, "log", "-1", f"--format={fmt}").split("\n")
    entries = []
    for line in git(clone, "ls-tree", "-r", "HEAD").splitlines():
        meta, path = line.split("\t", 1)
        _, _, blob = meta.split()
        work = git(clone, "hash-object", path)
        with open(os.path.join(clone, path), "rb") as fh:
            sha = hashlib.sha256(fh.read()).hexdigest()
        entries.append({"path": path, "blob": blob, "worktree_equals_blob": work == blob, "sha256": sha})
    repo_tree = git(repo, "ls-tree", "-r", "HEAD").splitlines()
    by_blob: dict[str, list[str]] = {}
    for line in repo_tree:
        meta, path = line.split("\t", 1)
        by_blob.setdefault(meta.split()[2], []).append(path)
    for e in entries:
        paths = by_blob.get(e["blob"], [])
        e["copies_in_repository"] = len(paths)
        e["example_copies"] = sorted(paths)[:3]
    created = issue["issue"]["created_at"]
    c947 = issue["comment_947"]["created_at"]
    main_at = git(repo, "log", "-1", "--format=%H %cI", "0af33d85")
    nxt = git(repo, "log", "--first-parent", "--format=%h %cI", "--reverse", "0af33d85..2fe557598").splitlines()
    out = {
        "program": "l117_custody.py",
        "clone": {
            "head": head,
            "commits": int(git(clone, "rev-list", "--count", "HEAD")),
            "parents": parents,
            "author": author,
            "author_date": adate,
            "committer": committer,
            "commit_date": cdate,
            "tree": tree,
            "status_clean": git(clone, "status", "--porcelain") == "",
            "files": entries,
        },
        "issue_created": created,
        "seconds_commit_to_issue": (t(created) - t(cdate)).total_seconds(),
        "comment_947_created": c947,
        "seconds_issue_to_comment": (t(c947) - t(created)).total_seconds(),
        "main_0af33d85": main_at,
        "next_main_first_parent": nxt[:1],
        "issue_search_time_stated": "2026-11-11 15:35 PST = 2026-11-11T23:35Z",
    }
    with open(opath, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: v for k, v in out.items() if k != "clone"}, indent=1))
    for e in entries:
        print(e["path"], e["blob"][:8], e["worktree_equals_blob"], e["copies_in_repository"], e["example_copies"][:2], e["sha256"][:8])
    print({k: v for k, v in out["clone"].items() if k != "files"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
