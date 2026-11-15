"""Lane L163 custody, after the freeze: read-only Git plumbing on the clone of the source.

Usage: l163_custody.py CLONE PIN ISSUES.json OUT.json

Runs `rev-parse`, `log`, `merge-base --is-ancestor`, `ls-tree`, `show`, `status` and
`hash-object` only. Records commit times, the first commit of the files the issues name,
VERIFIER.sha256 against the digests of what it names, the licence's first lines, the run's
stated start and end, and the issues' times. Author e-mail addresses are not recorded.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import UTC, datetime

RUN = "runs/2026-11-11_fable-5.2"
FILES = [
    "VERIFIER.sha256",
    "verify.py",
    "tests/test_verify.py",
    "LICENSE",
    f"{RUN}/RUN.md",
    f"{RUN}/search/attack.py",
    f"{RUN}/search/opt.py",
    f"{RUN}/search/indep_check.py",
    f"{RUN}/search/fu_strict_check.py",
    f"{RUN}/certificates/n228_S59604312.json",
    f"{RUN}/certificates/n147_S65104355.json",
    f"{RUN}/evidence/registration/n228.cert",
    f"{RUN}/evidence/registration/n147.cert",
    f"{RUN}/evidence/registration/n228.strict.cert",
    f"{RUN}/evidence/registration/n147.strict.cert",
]


def git(clone: str, *args: str) -> str:
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True, text=True).stdout


def utc(stamp: str) -> str:
    return datetime.fromisoformat(stamp).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    clone, pin, issues_path, out = sys.argv[1:5]
    rec: dict[str, object] = {"lane": "L163", "program": "l163_custody.py", "pin": pin}
    rows = git(clone, "log", "--all", "--format=%H%x09%an%x09%aI%x09%cI%x09%P%x09%s").strip().split("\n")
    commits = []
    for r in rows:
        h, an, ad, cd, parents, subj = r.split("\t")
        commits.append({"commit": h[:12], "author": an, "authored": utc(ad), "committed": utc(cd), "parents": [p[:12] for p in parents.split()], "subject": subj})
    rec["commits"] = commits
    rec["pin_on_origin_main"] = subprocess.run(["git", "-C", clone, "merge-base", "--is-ancestor", pin, "origin/main"]).returncode == 0
    rec["origin_main"] = git(clone, "rev-parse", "origin/main").strip()[:12]
    rec["working_tree_clean_at_pin"] = git(clone, "rev-parse", "HEAD").strip() == pin and git(clone, "status", "--porcelain").strip() == ""
    rec["tree_files_at_pin"] = len(git(clone, "ls-tree", "-r", "--name-only", pin).split())
    first = {}
    for f in FILES:
        added = git(clone, "log", "--diff-filter=A", "--format=%h %cI", pin, "--", f).strip().split("\n")[-1]
        changed = git(clone, "log", "--format=%h", pin, "--", f).split()
        h, d = added.split(" ")
        first[f] = {"first_commit": h, "committed": utc(d), "commits_touching": changed}
    rec["files"] = first
    vc = git(clone, "log", "--diff-filter=A", "--format=%H", pin, "--", "VERIFIER.sha256").strip().split("\n")[-1]
    listed = {}
    for line in git(clone, "show", f"{vc}:VERIFIER.sha256").strip().split("\n"):
        digest, name = line.split()
        at_commit = hashlib.sha256(subprocess.run(["git", "-C", clone, "show", f"{vc}:{name}"], check=True, capture_output=True).stdout).hexdigest()
        at_pin = hashlib.sha256(subprocess.run(["git", "-C", clone, "show", f"{pin}:{name}"], check=True, capture_output=True).stdout).hexdigest()
        listed[name] = {"listed": digest, "equals_at_its_commit": digest == at_commit, "equals_at_pin": digest == at_pin}
    rec["verifier_sha256"] = {"commit": vc[:12], "entries": listed}
    lic = git(clone, "show", f"{pin}:LICENSE").split("\n")
    rec["licence_first_lines"] = [s for s in lic[:4] if s.strip()]
    runmd = git(clone, "show", f"{pin}:{RUN}/RUN.md")
    stamps = {}
    for key in ("started", "ended"):
        m = re.search(rf"\|\s*{key}\s*\|\s*([0-9T:+\-]+)\s*\|", runmd)
        stamps[key] = utc(m.group(1)[:-2] + ":" + m.group(1)[-2:]) if m else None
    rec["run_stated"] = stamps
    with open(issues_path, encoding="utf-8") as fh:
        issues = json.load(fh)
    pin_time = next(c["committed"] for c in commits if pin.startswith(c["commit"]))
    t_pin = datetime.fromisoformat(pin_time.replace("Z", "+00:00"))
    rec["issues"] = [
        {"number": i["number"], "created": i["created_at"], "seconds_after_pin_commit": int((datetime.fromisoformat(i["created_at"].replace("Z", "+00:00")) - t_pin).total_seconds())}
        for i in issues["issues"]
    ]
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)
    print(json.dumps({k: rec[k] for k in ("pin_on_origin_main", "working_tree_clean_at_pin", "verifier_sha256", "run_stated", "issues", "licence_first_lines")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
