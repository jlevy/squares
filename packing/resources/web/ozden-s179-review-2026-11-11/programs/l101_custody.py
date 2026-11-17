"""Custody of the source repository, after the freeze. Read-only Git plumbing.

Usage: python -I -B l101_custody.py SOURCE_DIR REPO_DIR ISSUE.json OUT.json

On the clone: the pin, its parents, author and committer, the commit time, the tree, every
committed blob and whether each working file hashes to it. On this repository: which
tracked files hold the same blobs as the source's licence and verifier files, and whether
the commit the issue names for the promotion and the verify run is on main.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def blob_id(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main() -> int:
    src, repo, issue_path, out = (Path(a) for a in sys.argv[1:5])
    issue = json.loads(issue_path.read_text(encoding="utf-8"))
    head = git(src, "rev-parse", "HEAD")
    log = git(src, "log", "-1", "--format=%H%n%P%n%an <%ae>%n%cn <%ce>%n%aI%n%cI%n%T")
    commit, parents, author, committer, authored, committed, tree = log.split("\n")
    all_commits = git(src, "rev-list", "--all").split()
    files = {}
    for line in git(src, "ls-tree", "-r", "-l", "HEAD").splitlines():
        meta, name = line.split("\t")
        _, _, blob, size = meta.split()
        files[name] = {"blob": blob, "size": int(size),
                       "working_file_matches": blob_id(src / name) == blob,
                       "sha256": hashlib.sha256((src / name).read_bytes()).hexdigest()}
    repo_blobs: dict[str, list[str]] = {}
    for line in git(repo, "ls-tree", "-r", "HEAD").splitlines():
        meta, name = line.split("\t")
        repo_blobs.setdefault(meta.split()[2], []).append(name)
    shared = {name: repo_blobs.get(info["blob"], []) for name, info in files.items()
              if name in {"LICENSE.md", "LICENSE-evand-square-packing.txt", "verifier/sqcheck.py",
                          "verifier/README.md"}}
    promote = "591644a9"
    try:
        full = git(repo, "rev-parse", "--verify", f"{promote}^{{commit}}")
        on_main = subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", full, "HEAD"],
                                 check=False).returncode == 0
        promote_info = {"commit": full, "on_main": on_main,
                        "committed": git(repo, "log", "-1", "--format=%cI", full)}
    except subprocess.CalledProcessError:
        promote_info = {"commit": None}
    receipt = {
        "program": "l101_custody.py",
        "head": head,
        "issue_pin": "bd262d8ba2966000e827547597fe6da24d0e118c",
        "head_is_pin": head == "bd262d8ba2966000e827547597fe6da24d0e118c",
        "commits_in_clone": len(all_commits),
        "parents": parents.split() if parents else [],
        "author": author,
        "committer": committer,
        "authored": authored,
        "committed": committed,
        "issue_opened": issue["created_at"],
        "tree": tree,
        "files": files,
        "same_blob_in_this_repository": shared,
        "promotion_commit": promote_info,
        "main_head": git(repo, "rev-parse", "HEAD"),
    }
    Path(out).write_text(json.dumps(receipt, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in receipt.items() if k != "files"}, indent=1, ensure_ascii=False))
    print({k: (v["blob"][:8], v["working_file_matches"]) for k, v in files.items()})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
