"""Hold every receipt in out/ to the kept programs, the checker to its frozen digests, and
the controls plan to the digest recorded when it was stated.

Run: python -I -B l77_digests.py OUT.json
"""

from __future__ import annotations

import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def sha(p: str) -> str:
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main() -> int:
    out = sys.argv[1]
    problems = []
    frozen = {}
    for line in open(os.path.join(HERE, "frozen/checker-frozen-digests.txt")):
        if line.startswith("#") or not line.strip():
            continue
        d, name = line.split()
        frozen[name] = d
        if sha(os.path.join(HERE, name)) != d:
            problems.append(f"{name} differs from its frozen digest")
    plan_line = [x for x in open(os.path.join(HERE, "frozen/controls-plan-digest.txt")) if not x.startswith("#")][0]
    if sha(os.path.join(HERE, "controls-plan.json")) != plan_line.split()[0]:
        problems.append("controls-plan.json differs from its stated digest")
    programs = {os.path.basename(p): sha(p) for p in sorted(glob.glob(os.path.join(HERE, "*.py")))}
    receipts = {}
    for p in sorted(glob.glob(os.path.join(HERE, "out", "*.json"))):
        name = os.path.basename(p)
        if name == os.path.basename(out):
            continue
        r = json.load(open(p))
        prog = r.get("program")
        rec = {"sha256": sha(p), "program": prog}
        if prog is None or prog not in programs:
            problems.append(f"{name}: names no kept program")
        elif r.get("program_sha256") != programs[prog]:
            problems.append(f"{name}: program digest differs from kept {prog}")
        if "checker_sha256" in r and r["checker_sha256"] != frozen["l77_checker.py"]:
            problems.append(f"{name}: checker digest differs from frozen")
        if "plan_sha256" in r and r["plan_sha256"] != plan_line.split()[0]:
            problems.append(f"{name}: plan digest differs")
        receipts[name] = rec
    res = {"program": "l77_digests.py", "program_sha256": programs["l77_digests.py"],
           "frozen_checker": frozen, "programs": programs, "receipts": receipts,
           "verdict": "ALL_RECEIPTS_MATCH" if not problems else "MISMATCH", "problems": problems}
    with open(out, "w") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    print(res["verdict"], problems)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
