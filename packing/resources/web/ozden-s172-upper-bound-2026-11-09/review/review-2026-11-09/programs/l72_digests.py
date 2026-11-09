"""Hold every receipt to the kept programs and the checker to its freeze (lane L72, bead think-qqyg).

Usage: python -I -B l72_digests.py REVIEW_DIR_172 REVIEW_DIR_270 OUT.json

Checks that the six checker files in REVIEW_DIR_172/programs equal the digests in
frozen/checker-frozen-digests.txt, that controls-plan.json equals the digest recorded when
it was stated, and that every program digest a receipt records equals the kept file of that
name. Lists the SHA-256 of every receipt. Decides no bound.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l72_util as util  # noqa: E402

PLAN_SHA256_STATED = "1826043aaa43b13652f8f9ab378b13a5ea61b225a137616e1af3126385d807cd"


def recorded_digests(obj):
    """Every {basename: sha256} map a receipt records about the programs that wrote it."""
    out = {}
    for key in ("checker_digests", "program_digests"):
        if isinstance(obj.get(key), dict):
            out.update(obj[key])
    return out


def main(argv):
    r172, r270, out = argv[1], argv[2], argv[3]
    progs = os.path.join(r172, "programs")
    problems = []
    frozen = {}
    with open(os.path.join(r172, "frozen", "checker-frozen-digests.txt"), encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            digest, name = line.split()
            frozen[name] = digest
    checker = {}
    for name, digest in frozen.items():
        kept = util.sha256_file(os.path.join(progs, name))
        checker[name] = {"frozen": digest, "kept": kept, "equal": kept == digest}
        if kept != digest:
            problems.append(f"{name} differs from its frozen digest")
    plan = util.sha256_file(os.path.join(progs, "controls-plan.json"))
    if plan != PLAN_SHA256_STATED:
        problems.append("controls-plan.json differs from the digest recorded when it was stated")
    receipts = []
    for d in (r172, r270):
        od = os.path.join(d, "out")
        for name in sorted(os.listdir(od)):
            if not name.endswith(".json") or name == os.path.basename(out):
                continue
            path = os.path.join(od, name)
            with open(path, encoding="utf-8") as fh:
                obj = json.load(fh)
            rec = recorded_digests(obj)
            mismatched = []
            for prog, digest in rec.items():
                kept_path = os.path.join(progs, prog)
                if not os.path.exists(kept_path):
                    mismatched.append(f"{prog}: not kept")
                elif util.sha256_file(kept_path) != digest:
                    mismatched.append(f"{prog}: differs")
            if mismatched:
                problems.append(f"{name}: {mismatched}")
            receipts.append(
                {
                    "receipt": os.path.relpath(path, os.path.dirname(r172)),
                    "sha256": util.sha256_file(path),
                    "programs_recorded": len(rec),
                    "programs_match": not mismatched,
                }
            )
    report = {
        "program": "l72_digests.py",
        "lane": "L72",
        "bead": "think-qqyg",
        "environment": util.environment(),
        "program_digests": util.program_digests([os.path.join(progs, "l72_digests.py"), os.path.join(progs, "l72_util.py")]),
        "checker_against_freeze": checker,
        "controls_plan": {"sha256": plan, "stated": PLAN_SHA256_STATED, "equal": plan == PLAN_SHA256_STATED},
        "receipts": receipts,
        "problems": problems,
        "verdict": "ALL_RECEIPTS_MATCH" if not problems else "MISMATCH",
    }
    util.write_receipt(out, report)
    print(report["verdict"], problems)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
