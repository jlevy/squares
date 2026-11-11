"""Hold every L96 receipt to the kept programs, and the checker to its frozen digests.

L96 review program. Usage: python -I -B l96_digests.py OUT_JSON PROGRAM_DIR FROZEN_DIR RECEIPT_DIR...
Every receipt that records `programs` must name the digests of the files kept in
PROGRAM_DIR; the five files in frozen/checker-frozen-digests.txt must still have those
digests; the controls plan must have the digest frozen/controls-plan-digest.txt states,
and every controls receipt must name it.
"""

import glob
import hashlib
import json
import os
import sys


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def frozen_list(path):
    out = {}
    with open(path) as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            h, name = line.split()
            out[name] = h
    return out


def main():
    out_path, pdir, fdir = sys.argv[1:4]
    progs = {os.path.basename(p): sha(p) for p in sorted(glob.glob(os.path.join(pdir, "l96_*.py")))}
    problems = []
    frozen = frozen_list(os.path.join(fdir, "checker-frozen-digests.txt"))
    for name, h in frozen.items():
        if progs.get(name) != h:
            problems.append(f"frozen checker file changed: {name}")
    plan = frozen_list(os.path.join(fdir, "controls-plan-digest.txt"))
    plan_sha = sha(os.path.join(fdir, "controls-plan.json"))
    if plan.get("frozen/controls-plan.json") != plan_sha:
        problems.append("controls plan differs from its stated digest")
    receipts = {}
    for d in sys.argv[4:]:
        for p in sorted(glob.glob(os.path.join(d, "*.json"))):
            with open(p) as fh:
                r = json.load(fh)
            receipts[os.path.relpath(p, os.path.join(d, "..", "..", "..", ".."))] = sha(p)
            for name, h in (r.get("programs") or {}).items():
                if progs.get(name) != h:
                    problems.append(f"{p}: names {name} at {h[:12]}, kept {str(progs.get(name))[:12]}")
            if "plan_sha256" in r and r["plan_sha256"] != plan_sha:
                problems.append(f"{p}: names another plan")
    out = {
        "programs": progs,
        "frozen_checker": frozen,
        "controls_plan_sha256": plan_sha,
        "receipts": receipts,
        "problems": problems,
        "result": "ALL_RECEIPTS_MATCH" if not problems else "MISMATCH",
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(out["result"], len(receipts), "receipts", problems[:5])


if __name__ == "__main__":
    main()
