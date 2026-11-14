"""Lane L159's custody record: read-only Git plumbing and the issue's times.

Written after the findings were frozen, for the stage 4 review of issue #983; decides
nothing. It runs `rev-parse`, `rev-list`, `log`, `ls-tree`, `hash-object` and `status`
on the clone made for this review and on this repository, and compares the commit's
time with the issue's, the timeline's events and the issues the filing names.

Usage: l159_custody.py CLONE REPO PIN ISSUE.json TIMELINE.json CONTEXT.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout


def when(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def main(argv: list[str]) -> int:
    clone, repo = Path(argv[1]), Path(argv[2])
    pin = argv[3]
    issue = json.loads(Path(argv[4]).read_text(encoding="utf-8"))
    timeline = json.loads(Path(argv[5]).read_text(encoding="utf-8"))
    context = json.loads(Path(argv[6]).read_text(encoding="utf-8"))
    out_path = Path(argv[7])
    out: dict[str, object] = {"program": "l159_custody.py"}
    head = git(clone, "rev-parse", "HEAD").strip()
    out["clone_head"] = head
    out["clone_head_is_pin"] = head == pin
    out["commits_reachable_from_pin"] = int(git(clone, "rev-list", "--count", pin).strip())
    out["branches_and_tags"] = git(clone, "for-each-ref", "--format=%(refname) %(objectname)").splitlines()
    fmt = "%H%n%P%n%an <%ae>%n%aI%n%cn <%ce>%n%cI%n%T%n%s"
    h, parents, author, adate, committer, cdate, tree, subject = git(clone, "log", "-1", f"--format={fmt}", pin).splitlines()[:8]
    out["commit"] = {"sha": h, "parents": parents.split(), "author": author, "authored": adate, "committer": committer, "committed": cdate, "tree": tree, "subject": subject}
    files = []
    all_equal = True
    for line in git(clone, "ls-tree", "-r", "-l", pin).splitlines():
        meta, path = line.split("\t", 1)
        _, _, blob, size = meta.split()
        work = git(clone, "hash-object", path).strip()
        all_equal &= work == blob
        digest = hashlib.sha256((clone / path).read_bytes()).hexdigest()
        files.append({"path": path, "blob": blob, "size": int(size), "sha256": digest, "working_tree_equal": work == blob})
    out["files"] = files
    out["every_working_file_equals_its_blob"] = all_equal
    out["clone_status_clean"] = git(clone, "status", "--porcelain").strip() == ""
    cert = clone / "n-228-candidate.yaml"
    twin = clone / "n228-witness.json"
    out["certificate_sha256"] = hashlib.sha256(cert.read_bytes()).hexdigest()
    out["twin_sha256"] = hashlib.sha256(twin.read_bytes()).hexdigest()
    # Retained copies here of the source's licence files and checker, by blob.
    tree_here = git(repo, "ls-tree", "-r", "HEAD").splitlines()
    retained = {}
    for f in files:
        if f["path"] in ("LICENSE.md", "LICENSE-evand-square-packing.txt", "verifier/sqcheck.py", "verifier/README.md", "n-228-candidate.yaml", "n228-witness.json"):
            paths = [ln.split("\t", 1)[1] for ln in tree_here if ln.split()[2] == f["blob"]]
            retained[f["path"]] = {"blob": f["blob"], "copies_here": len(paths), "first": paths[:3]}
    out["retained_here_by_blob"] = retained
    out["repo_head"] = git(repo, "rev-parse", "HEAD").strip()
    main_head = git(repo, "log", "-1", "--format=%H %cI %s", "fa980f8e7").strip()
    out["fa980f8e7"] = main_head
    # Times.
    committed = when(cdate)
    created = when(issue["created_at"])
    out["issue_created"] = issue["created_at"]
    out["issue_created_after_commit_seconds"] = (created - committed).total_seconds()
    out["fa980f8e7_committed_before_issue_seconds"] = (created - when(main_head.split()[1])).total_seconds()
    out["issue_updated_at"] = issue["updated_at"]
    out["timeline"] = timeline["timeline"]
    out["timeline_fetched_at"] = timeline["fetched_at"]
    out["issue_now"] = timeline["issue_now"]
    out["issues_named"] = [{k: v for k, v in i.items() if k in ("number", "state", "title", "is_pr")} for i in context["issues_named"]]
    out["evand_square_packing_head"] = context["evand_square_packing_head"]
    out_path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("clone_head_is_pin", "commits_reachable_from_pin", "commit", "every_working_file_equals_its_blob", "clone_status_clean", "retained_here_by_blob", "issue_created_after_commit_seconds", "fa980f8e7", "fa980f8e7_committed_before_issue_seconds")}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
