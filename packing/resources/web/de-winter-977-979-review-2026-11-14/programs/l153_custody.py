"""Lane L153, after the freeze: custody and dating, by read-only Git plumbing.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review. It decides nothing about the bounds.

On the clone of JoostdeWinter/square-packing it runs `rev-parse`, `log`, `ls-tree`,
`rev-list` and `status` (read-only), and on the pins' worktrees `hash-object`; it
compares the commit times with the issues' creation times, and records the licence
file's blob, first line and the commit that added it.

Usage: l153_custody.py CLONE PIN297_WORKTREE PIN979_WORKTREE ISSUES.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PIN_977 = "7b4701f35e815301e4f467d214fab4205ded5eb1"
PIN_979 = "c70defaf39af47db220d1e7c2922590637ffb664"


def git(repo: str, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", repo, *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def when(text: str) -> datetime:
    return datetime.fromisoformat(text.replace("Z", "+00:00"))


def main(argv: list[str]) -> int:
    clone, wt977, wt979, issues_path, out_path = argv[1:6]
    issues = {i["number"]: i for i in json.loads(Path(issues_path).read_text())["issues"]}
    log = git(clone, "log", "--format=%H|%P|%an <%ae>|%aI|%cn <%ce>|%cI|%s", "--all")
    commits = []
    for line in log.splitlines():
        h, parents, author, adate, committer, cdate, subject = line.split("|", 6)
        commits.append(
            {
                "sha": h,
                "parents": parents.split(),
                "author": author,
                "authored": adate,
                "committer": committer,
                "committed": cdate,
                "subject": subject,
            }
        )
    by_sha = {c["sha"]: c for c in commits}
    out: dict = {"program": "l153_custody.py", "commits_in_clone": len(commits)}
    out["head"] = git(clone, "rev-parse", "HEAD")
    out["branches"] = git(clone, "branch", "-r").split()
    for number, pin, wt, files in (
        (977, PIN_977, wt977, ["n297/n297_exact.json", "n297/n297_witness.yaml"]),
        (
            979,
            PIN_979,
            wt979,
            ["above324_from_n297/n332_exact.json", "above324_from_n297/n409_exact.json"],
        ),
    ):
        c = by_sha[pin]
        created = when(issues[number]["created_at"])
        committed = when(c["committed"])
        entry = {
            "commit": c,
            "issue_created": issues[number]["created_at"],
            "seconds_from_commit_to_issue": (created - committed).total_seconds(),
            "commits_after_pin_before_issue": [
                d["sha"][:12] + " " + d["committed"] + " " + d["subject"]
                for d in commits
                if committed < when(d["committed"]) <= created
            ],
            "on_default_branch": pin
            in git(clone, "rev-list", "origin/HEAD").split(),
            "worktree_clean": git(wt, "status", "--porcelain") == "",
            "files": {},
        }
        for f in files:
            blob = git(clone, "rev-parse", f"{pin}:{f}")
            data = (Path(wt) / f).read_bytes()
            entry["files"][f] = {
                "blob": blob,
                "worktree_blob": git(wt, "hash-object", f),
                "sha256": hashlib.sha256(data).hexdigest(),
                "first_commit": git(clone, "log", "--format=%h %cI", "--diff-filter=A", "--", f).splitlines()[-1:],
            }
        out[str(number)] = entry
    # Licence.
    lic_blob = git(clone, "rev-parse", f"{PIN_979}:LICENSE")
    lic_text = git(clone, "show", f"{PIN_979}:LICENSE")
    out["licence"] = {
        "blob_at_979_pin": lic_blob,
        "blob_at_977_pin": git(clone, "rev-parse", f"{PIN_977}:LICENSE"),
        "first_line": lic_text.splitlines()[0],
        "copyright_line": next((ln for ln in lic_text.splitlines() if "Copyright" in ln), None),
        "added_in": git(clone, "log", "--format=%h %cI %s", "--diff-filter=A", "--", "LICENSE"),
        "sha256": hashlib.sha256((lic_text + "\n").encode()).hexdigest(),
    }
    out["all_commits"] = [
        f"{c['sha'][:12]} {c['committed']} {c['subject']}" for c in commits
    ]
    Path(out_path).write_text(json.dumps(out, indent=1) + "\n")
    for number in (977, 979):
        e = out[str(number)]
        print(number, e["commit"]["committed"], "issue", e["issue_created"],
              "seconds", e["seconds_from_commit_to_issue"], "on default", e["on_default_branch"],
              "clean", e["worktree_clean"])
    print("licence", out["licence"]["first_line"], "|", out["licence"]["copyright_line"], "|", out["licence"]["added_in"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
