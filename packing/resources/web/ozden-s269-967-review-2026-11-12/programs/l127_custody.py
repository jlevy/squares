"""Custody, licence and dating, by read-only Git plumbing. Written and run after the freeze.

Lane L127, clean room; decides nothing. Usage:

    python -I -B l127_custody.py CLONE_DIR REPO_DIR PIN ISSUE.json TIMELINE.json OUT.json

Runs only rev-parse, rev-list, log, ls-tree, hash-object and status on the clone of the
source and on this repository (whose `origin/main` is read), and the issue's times.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(UTC)


def main(argv: list[str]) -> int:
    clone, repo, pin = Path(argv[1]), Path(argv[2]), argv[3]
    issue = json.loads(Path(argv[4]).read_text(encoding="utf-8"))
    timeline = json.loads(Path(argv[5]).read_text(encoding="utf-8"))
    outp = Path(argv[6])
    head = git(clone, "rev-parse", "HEAD")
    commits = git(clone, "rev-list", "--all").split()
    meta = git(clone, "log", "-1", "--format=%H%n%P%n%an <%ae>%n%aI%n%cn <%ce>%n%cI%n%T", pin).split("\n")
    tree = [line.split(None, 3) for line in git(clone, "ls-tree", "-r", "-l", pin).split("\n")]
    files = {t[3].split("\t", 1)[1] if "\t" in t[3] else t[3]: t[2] for t in tree}
    sizes = {}
    for t in tree:
        size, path = t[3].split("\t", 1)
        sizes[path] = int(size)
    worktree_equal = {p: git(clone, "hash-object", p) == b for p, b in files.items()}
    status = git(clone, "status", "--porcelain")
    # blobs this repository already retains on main
    main_tree = git(repo, "ls-tree", "-r", "origin/main")
    retained: dict[str, list[str]] = {}
    by_blob: dict[str, list[str]] = {}
    for line in main_tree.split("\n"):
        info, path = line.split("\t", 1)
        by_blob.setdefault(info.split()[2], []).append(path)
    for p, b in files.items():
        retained[p] = by_blob.get(b, [])
    # main's head over the issue's window
    first_parent = git(repo, "log", "--first-parent", "--format=%H %cI", "origin/main", "-6").split("\n")
    main_log = [{"commit": h[:10], "committed": ts(t).isoformat()} for h, t in (x.split() for x in first_parent)]
    stated = git(repo, "log", "-1", "--format=%H %cI", "0352d755")
    stated_commit, stated_time = stated.split()
    created = ts(issue["issue"]["created_at"])
    comment = ts(issue["comment_on_947"]["created_at"])
    committed = ts(meta[5])
    # the issue's dating: "checked 0352d755, 2026-11-11 19:10 PST"
    checked = datetime(2026, 11, 12, 3, 10, tzinfo=UTC)
    out: dict[str, Any] = {
        "program": "l127_custody.py",
        "clone_head": head,
        "head_is_pin": head == pin,
        "commits_in_clone": len(commits),
        "pin": {
            "commit": meta[0],
            "parents": meta[1].split(),
            "author": meta[2],
            "authored": ts(meta[3]).isoformat(),
            "committer": meta[4],
            "committed": committed.isoformat(),
            "tree": meta[6],
        },
        "files": {p: {"blob": b, "bytes": sizes[p], "worktree_equals_blob": worktree_equal[p], "retained_on_main": len(retained[p]), "retained_examples": retained[p][:3]} for p, b in sorted(files.items())},
        "worktree_clean": status == "",
        "times": {
            "commit_to_issue_seconds": (created - committed).total_seconds(),
            "issue_to_947_comment_seconds": (comment - created).total_seconds(),
            "issue_created": created.isoformat(),
            "stated_check_time_utc": checked.isoformat(),
            "stated_check_after_issue_seconds": (checked - created).total_seconds(),
        },
        "stated_commit": {"commit": stated_commit, "committed": ts(stated_time).isoformat(), "is_main_head_now": main_log[0]["commit"] == stated_commit[:10]},
        "main_first_parent": main_log,
        "timeline": timeline["timeline"],
    }
    outp.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1)[:5000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
