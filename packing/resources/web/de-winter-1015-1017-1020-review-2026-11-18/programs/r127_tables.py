"""Tabulate the control receipts against the plan; it decides nothing.

Lane r127-1118.  Written after the checker was frozen and before the findings were
frozen.  It reads the plan and the receipts only, and checks the plan's statement about
the two constant checkers: under always-accept every must_refuse control that ran is not
as stated, and under always-refuse every must_accept control that ran is not as stated.

    python -I -B r127_tables.py --plan programs/controls-plan.json --out out/tables.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys


def base(cid: str) -> str:
    return cid.split("-")[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--dir", default="out")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    plan = json.load(open(a.plan))
    must_refuse, must_accept = set(plan["must_refuse"]), set(plan["must_accept"])
    tiers = {x["id"]: set(x["tiers"]) for x in plan["controls"]}
    rows = []
    for k in ("1015", "1017", "1020"):
        for form, tier in (("exact", "first"), ("witness", "twin")):
            path = os.path.join(a.dir, f"controls-{k}-{form}.json")
            r = json.load(open(path))
            outside = sorted({base(x["id"]) for x in r["results"]} - {c for c, t in tiers.items() if tier in t})
            no_subject = [x["id"] for x in r["results"] if x["verdict"] == "NO_SUBJECT"]
            rows.append({"report": k, "file": form, "controls": r["controls"], "as_stated": r["as_stated"],
                         "not_as_stated": r["not_as_stated"], "no_subject": no_subject,
                         "outside_the_plans_tier": outside, "verdict": r["verdict"],
                         "cpu_seconds": r["cpu_seconds"]})
        for ck in ("always-accept", "always-refuse"):
            path = os.path.join(a.dir, f"controls-{k}-exact-{ck}.json")
            r = json.load(open(path))
            failed = {base(x["id"]) for x in r["results"] if not x["as_stated"]}
            ran = {base(x["id"]) for x in r["results"]}
            target = must_refuse if ck == "always-accept" else must_accept
            # P0p has no subject when no pair touches, as the plan allows
            target_ran = {c for c in target & ran if not (c == "P0p" and all(
                x["verdict"] == "NO_SUBJECT" for x in r["results"] if base(x["id"]) == "P0p"))}
            rows.append({"report": k, "file": f"exact, {ck}", "controls": r["controls"],
                         "as_stated": r["as_stated"], "not_as_stated": r["not_as_stated"],
                         "plan_targets_that_ran": sorted(target_ran),
                         "plan_targets_failed": sorted(target_ran & failed),
                         "plan_statement_holds": target_ran <= failed and r["verdict"] != "EVERY_CONTROL_AS_STATED",
                         "skipped": r["missing_from_run"], "cpu_seconds": r["cpu_seconds"]})
    out = {"program": "r127_tables.py", "decides": "nothing", "rows": rows,
           "real_controls": sum(x["controls"] for x in rows if x["file"] in ("exact", "witness")),
           "real_as_stated": sum(x["as_stated"] for x in rows if x["file"] in ("exact", "witness")),
           "cpu_seconds": round(sum(x["cpu_seconds"] for x in rows), 1)}
    json.dump(out, open(a.out, "w"), indent=1)
    for x in rows:
        print(json.dumps(x))
    print(f"real controls {out['real_as_stated']}/{out['real_controls']} as stated; cpu {out['cpu_seconds']} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
