"""Lane L169 custody (after the freeze): the source clone, its dates, digests and twin.

Usage: l169_custody.py CLONE PIN ISSUE_JSON OUT_JSON

It decides nothing. Read-only Git plumbing on the clone (rev-parse, log, ls-tree, show,
diff --name-status, status) records each commit's author name, dates and subject, and
the files at each commit; no e-mail address is read or written. It checks the pin's
SHA256SUMS against the files, compares the decimal CSV with the certificate (centres to
the CSV's printed precision, angles as 2 atan t in degrees), and sets the issue's
opening time against the pin's commit time.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import os
import subprocess
import sys
from datetime import datetime
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # -I leaves it off

import l169_reader as rd


def git(clone: str, *args: str) -> str:
    return subprocess.run(["git", "-C", clone, *args], check=True, capture_output=True, text=True).stdout


def main(argv: list[str]) -> int:
    clone, pin, issue_path, out_path = argv[1:5]
    out: dict = {"program": "l169_custody.py", "pin": pin}
    out["head"] = git(clone, "rev-parse", "HEAD").strip()
    out["working_tree_clean"] = git(clone, "status", "--porcelain") == ""
    log = git(clone, "log", "--format=%H%x09%an%x09%aI%x09%cI%x09%s", pin)
    commits = []
    for line in log.strip().splitlines():
        h, an, ad, cd, subj = line.split("\t", 4)
        files = git(clone, "ls-tree", "-r", "--format=%(objectname) %(objectsize) %(path)", h).strip().splitlines()
        commits.append({"commit": h, "author_name": an, "author_date": ad, "commit_date": cd, "subject": subj,
                         "files": files})
    out["commits"] = commits
    if len(commits) >= 2:
        out["pin_changes_from_parent"] = git(clone, "diff", "--name-status", f"{pin}~1", pin).strip().splitlines()
        out["pin_parent_readme_changed_lines"] = [
            ln for ln in git(clone, "diff", "--unified=0", f"{pin}~1", pin, "--", "README.md").splitlines()
            if ln.startswith(("+", "-")) and not ln.startswith(("+++", "---"))
        ]
    # SHA256SUMS at the pin.
    sums = git(clone, "show", f"{pin}:SHA256SUMS")
    checks = []
    for line in sums.strip().splitlines():
        digest, name = line.split(None, 1)
        data = subprocess.run(["git", "-C", clone, "show", f"{pin}:{name}"], check=True, capture_output=True).stdout
        checks.append({"file": name, "stated": digest, "actual": hashlib.sha256(data).hexdigest(),
                       "holds": hashlib.sha256(data).hexdigest() == digest})
    out["sha256sums"] = checks
    out["licence_files"] = [f.split()[-1] for f in commits[0]["files"] if "LICEN" in f.split()[-1].upper()]
    # The CSV twin.
    cert_bytes = subprocess.run(["git", "-C", clone, "show", f"{pin}:n90.cert"], check=True, capture_output=True).stdout
    rdg = rd.read_text(cert_bytes)
    rows = list(csv.reader(io.StringIO(git(clone, "show", f"{pin}:n90.csv"))))
    header, body = rows[0], rows[1:]
    worst_c, worst_a = F(0), 0.0
    ids_in_order = True
    for k, (row, sq) in enumerate(zip(body, rdg["squares"], strict=True)):
        ids_in_order &= int(row[0]) == k + 1
        for col, v in ((1, sq[0]), (2, sq[1])):
            worst_c = max(worst_c, abs(F(row[col]) - F(*v)))
        ang = math.degrees(2 * math.atan(F(*sq[2])))
        worst_a = max(worst_a, abs(float(row[3]) - ang))
    out["csv"] = {"header": header, "rows": len(body), "ids_in_certificate_order": ids_in_order,
                  "largest_centre_difference": float(worst_c), "largest_angle_difference_deg": worst_a}
    issue = json.load(open(issue_path))
    t_issue = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
    t_pin = datetime.fromisoformat(commits[0]["commit_date"])
    out["issue"] = {"number": issue.get("number"), "created_at": issue["created_at"],
                    "seconds_after_pin_commit": (t_issue - t_pin).total_seconds(),
                    "labels": issue.get("labels"), "comments": issue.get("comments")}
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for c in commits:
        print(c["commit"][:9], c["author_name"], c["commit_date"], c["subject"], len(c["files"]), "files")
    print("changes from parent", out.get("pin_changes_from_parent"))
    print("readme lines changed", out.get("pin_parent_readme_changed_lines"))
    print("sha256sums hold", all(c["holds"] for c in checks), "licence files", out["licence_files"])
    print("csv", out["csv"])
    print("issue", out["issue"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
