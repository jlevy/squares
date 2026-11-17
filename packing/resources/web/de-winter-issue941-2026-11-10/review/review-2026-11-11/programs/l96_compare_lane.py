"""After the freeze: hold the import lane's ledger and manifests to this review's receipts.

L96 review program, written after the findings were frozen. Usage:
  python -I -B l96_compare_lane.py OUT_JSON LEDGER_JSON OUT_DIR MANIFEST_941 MANIFEST_942 MANIFEST_A0C LICENSE_COPY
LEDGER_JSON is the lane's `ledger.json`; the manifests are its three
`acquisition/upstream-subtree.sha256`; LICENSE_COPY is the copy `main` keeps in the
227/229/260 packet. It compares, exactly: each ledger side with the certificate's side
(the ledger prints 12 places, so the check is that the print is the exact side's 12-place
ceiling); each ledger start with `main`'s current row as `record-rows.json` lists it; each
retained file's SHA-256 with the manifests; and the manifests' LICENSE with the copy.
"""

import glob
import hashlib
import json
import os
import sys
from fractions import Fraction as F


def ceil12(q):
    v = -((-q.numerator * 10**12) // q.denominator)
    return f"{v // 10**12}.{v % 10**12:012d}"


def main():
    out_path, ledger_path, out_dir, m1, m2, m3, lic = sys.argv[1:8]
    with open(ledger_path) as fh:
        ledger = json.load(fh)
    sides = {}
    for p in glob.glob(os.path.join(out_dir, "..", "..", "..", "..", "de-winter-*", "review", "review-2026-11-11", "out", "check-n*.json")):
        with open(p) as fh:
            r = json.load(fh)
        sides[r["n"]] = F(r["side"]["exact"])
    with open(os.path.join(out_dir, "record-rows.json")) as fh:
        rows = json.load(fh)
    problems = []
    for c in ledger["counts"]:
        n = c["n"]
        step = c["steps"][0]
        if step["side"] != ceil12(sides[n]):
            problems.append(f"{n}: ledger side {step['side']} is not the 12-place ceiling {ceil12(sides[n])}")
        if step["verdict"] != "recorded":
            problems.append(f"{n}: ledger verdict {step['verdict']}")
        cur = [r["value"] for r in rows["beyond_horizon_rows"].get(str(n), []) if r["disposition"] != "superseded"]
        starts = [s["side"] for s in c["start"]]
        if cur and starts != cur:
            problems.append(f"{n}: ledger start {starts}, main's current row {cur}")
        if not cur and starts != ["26"]:
            problems.append(f"{n}: no row on main, ledger start {starts}")
    with open(os.path.join(out_dir, "custody.json")) as fh:
        cust = json.load(fh)
    lic_sha = hashlib.sha256(open(lic, "rb").read()).hexdigest()
    manifests = {}
    for key, m in (("941@71da0d5", m1), ("942@a9486ed", m2), ("addendum@a0c4fc8", m3)):
        with open(m) as fh:
            text = fh.read()
        hashes = {line.split()[0] for line in text.splitlines() if line.strip()}
        missing = [f for f, d in cust["packets"][key]["files"].items() if d["sha256"] not in hashes]
        licence = [line.split()[0] for line in text.splitlines() if line.endswith("/LICENSE")]
        manifests[key] = {"retained_files_missing_from_manifest": missing, "licence_sha256": sorted(set(licence))}
        if missing:
            problems.append(f"{key}: {missing} not in the lane's manifest")
        if set(licence) != {lic_sha}:
            problems.append(f"{key}: LICENSE {licence} differs from main's copy {lic_sha}")
    out = {
        "ledger_counts": len(ledger["counts"]),
        "ledger_read_at_main": ledger["read_at_main"],
        "main_licence_copy_sha256": lic_sha,
        "manifests": manifests,
        "problems": problems,
        "result": "LANE_AGREES" if not problems else "DIFFERS",
    }
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(out["result"], out["ledger_counts"], problems[:5])


if __name__ == "__main__":
    main()
