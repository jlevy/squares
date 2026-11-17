"""Lane L180, after the freeze: custody, dating and licence, by read-only Git plumbing.

Written for the blind stage 4 review of issue #996. It decides nothing about the bound.
It runs only ``git rev-parse``, ``log``, ``ls-tree``, ``show`` and ``status`` on the clone
made for this review, records author names and times but no addresses, checks the
author's ``SHA256SUMS`` at the head against the head's bytes, and dates the issue
against the commits.

Usage: l180_custody.py CLONE PIN HEAD ISSUE_JSON OUT
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from typing import Any


def git(clone: str, *args: str) -> bytes:
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True).stdout


def when(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    clone, pin, head, issue_path, out = argv[1:]
    with open(issue_path, encoding="utf-8") as fh:
        issue = json.load(fh)
    res: dict[str, Any] = {"program": "l180_custody.py", "lane": "L180"}
    res["checked_out"] = git(clone, "rev-parse", "HEAD").decode().strip()
    res["working_tree_clean"] = git(clone, "status", "--porcelain").decode().strip() == ""
    res["remote_head"] = git(clone, "rev-parse", "origin/main").decode().strip()
    log = git(clone, "log", "--format=%H%x09%aI%x09%cI%x09%an%x09%s", "origin/main").decode().splitlines()
    commits = [dict(zip(("sha", "authored", "committed", "author", "subject"), line.split("\t"), strict=True)) for line in log]
    res["commit_count"] = len(commits)
    res["authors"] = sorted({c["author"] for c in commits})
    res["commits_of_15_november"] = [c for c in commits if c["authored"].startswith("2026-11-15")]
    res["pin_is_ancestor_of_head"] = subprocess.run(["git", "-C", clone, "merge-base", "--is-ancestor", pin, head], check=False).returncode == 0
    trees = {}
    for name, rev in (("pin", pin), ("head", head)):
        rows = git(clone, "ls-tree", "-l", rev, "n90/").decode().splitlines()
        trees[name] = {r.split("\t")[1]: r.split()[2] for r in rows}
    res["n90_blobs"] = trees
    res["certificate_blobs_unchanged"] = all(trees["pin"][f] == trees["head"][f] for f in ("n90/n90_exact.json", "n90/n90_witness.yaml"))
    res["changed_pin_to_head"] = git(clone, "diff", "--name-only", pin, head).decode().split()
    sums = git(clone, "show", f"{head}:n90/SHA256SUMS").decode().splitlines()
    checks = {}
    for line in sums:
        digest, name = line.split()
        data = git(clone, "show", f"{head}:n90/{name}")
        checks[name] = hashlib.sha256(data).hexdigest() == digest
    res["sha256sums_at_head"] = checks
    res["sha256sums_hold"] = all(checks.values())
    pin_time = when(git(clone, "log", "-1", "--format=%cI", pin).decode().strip())
    head_time = when(git(clone, "log", "-1", "--format=%cI", head).decode().strip())
    opened = when(issue["created_at"])
    res["dating"] = {
        "issue_opened": issue["created_at"],
        "pin_committed": pin_time.isoformat(),
        "head_committed": head_time.isoformat(),
        "issue_after_pin_seconds": int((opened - pin_time).total_seconds()),
        "issue_after_head_seconds": int((opened - head_time).total_seconds()),
        "issue_labels": issue.get("labels"),
        "issue_comments": issue.get("comments"),
    }
    lic = git(clone, "show", f"{pin}:LICENSE").decode()
    readme = git(clone, "show", f"{pin}:README.md").decode()
    res["licence"] = {
        "blob": git(clone, "rev-parse", f"{pin}:LICENSE").decode().strip(),
        "blob_at_head": git(clone, "rev-parse", f"{head}:LICENSE").decode().strip(),
        "first_line": lic.splitlines()[0],
        "copyright": next((ln for ln in lic.splitlines() if ln.startswith("Copyright")), None),
        "readme_statement": next((ln for ln in readme.splitlines() if "licen" in ln.lower()), None),
        "added_in": git(clone, "log", "--format=%h %aI", "--", "LICENSE").decode().split("\n")[-2],
    }
    credit = {}
    for name, rev in (("pin", pin), ("head", head)):
        text = git(clone, "show", f"{rev}:n90/README.md").decode()
        credit[name] = next((ln for ln in text.splitlines() if "local search" in ln and "run with" in ln), None)
    res["n90_readme_search_credit"] = credit
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: res[k] for k in ("certificate_blobs_unchanged", "sha256sums_hold", "dating", "licence", "n90_readme_search_credit")})[:2000])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
