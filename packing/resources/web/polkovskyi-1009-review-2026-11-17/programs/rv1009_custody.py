"""Custody of the 26 certificate files in the source's history. Decides nothing.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Written and run after the
findings were frozen.

    python -I -B rv1009_custody.py CLONE PIN ISSUE.json OUT.json

Read-only Git plumbing on a blobless clone of the source: the commits (ids and times, no
names or addresses), the remote head, and for each certificate path every commit that
changed it with the blob it held there. The SHA-256 of each file at the pin is taken from
the checked-out bytes and compared with the issue's list.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1009_issue as issue  # noqa: E402

COUNTS = (147, 156, 180, 210, 260, 262, 268, 270, 272, 292, 295, 299, 307)


def git(clone: str, *args: str) -> str:
    done = subprocess.run(  # noqa: S603
        ["git", "-C", clone, *args],  # noqa: S607
        check=True,
        capture_output=True,
        text=True,
    )
    return done.stdout


def main(argv: list[str]) -> int:
    clone, pin, issue_path, out_path = argv[1:5]
    stated = issue.read_issue(issue_path)
    commits = []
    for line in git(clone, "log", "--format=%H %cI %aI", pin).splitlines():
        sha, committed, authored = line.split(" ")
        commits.append({"commit": sha, "committed": committed, "authored": authored})
    head = git(clone, "rev-parse", "HEAD").strip()
    remote = git(clone, "ls-remote", "origin", "HEAD").split()[0] if "--offline" not in argv else None
    files = {}
    for n in COUNTS:
        for kind, path in (
            ("cert", f"certificates/0000-0999/n{n}.cert"),
            ("yaml", f"witnesses/2026-11-16/n-{n}.yaml"),
        ):
            history = []
            for line in git(clone, "log", "--format=%H %cI", pin, "--", path).splitlines():
                sha, committed = line.split(" ")
                blob = git(clone, "rev-parse", f"{sha}:{path}").strip()
                history.append({"commit": sha, "committed": committed, "blob": blob})
            data = subprocess.run(  # noqa: S603
                ["git", "-C", clone, "cat-file", "blob", f"{pin}:{path}"],  # noqa: S607
                check=True,
                capture_output=True,
            ).stdout
            digest = hashlib.sha256(data).hexdigest()
            want = stated["files"][n][f"{kind}_sha256"]
            files[path] = {
                "n": n,
                "bytes": len(data),
                "sha256_at_pin": digest,
                "issue_sha256": want,
                "equal": digest == want,
                "commits_that_changed_it": history,
                "first_committed": history[-1]["committed"] if history else None,
                "versions": len({h["blob"] for h in history}),
            }
    receipt = {
        "program": "rv1009_custody.py",
        "lane": "c-review-1009-1117",
        "decides": "nothing",
        "pin": pin,
        "pin_is_clone_head": head == pin,
        "remote_head": remote,
        "pin_is_remote_head": remote == pin if remote else None,
        "commits": len(commits),
        "pin_commit": commits[0],
        "first_commit": commits[-1],
        "issue": {"created_at": stated["created_at"], "author": stated["author"]},
        "all_digests_equal": all(f["equal"] for f in files.values()),
        "files_new_at_pin": sorted(
            p for p, f in files.items() if [h["commit"] for h in f["commits_that_changed_it"]] == [pin]
        ),
        "files_with_earlier_versions": sorted(
            p for p, f in files.items() if len(f["commits_that_changed_it"]) > 1
        ),
        "files": files,
        "recent_commits": commits[:12],
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n", encoding="ascii")
    sys.stdout.write(
        f"commits={len(commits)} pin_is_head={head == pin} remote_head_is_pin={receipt['pin_is_remote_head']} "
        f"digests_equal={receipt['all_digests_equal']} new_at_pin={len(receipt['files_new_at_pin'])} "
        f"earlier_versions={len(receipt['files_with_earlier_versions'])}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
