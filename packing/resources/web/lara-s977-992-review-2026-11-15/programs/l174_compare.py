"""Lane L174: compare each control's two-method receipt with the outcome the plan stated.

Usage: ``python -I -B l174_compare.py PLAN.json RECEIPT_DIR OUT.json``

Reads ``RECEIPT_DIR/decide-<name>.json`` for every control in the plan.  For each stated
quantity it checks method A's and method B's values, requires the two methods to agree
on every pair class, wall class and unit test, and prints one line per control.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

COUNT_KEYS = (
    "apart",
    "touching",
    "overlapping",
    "wall_touching",
    "wall_touching_squares",
    "wall_crossing",
    "wall_crossing_squares",
)


def pairset(pairs: list[list[str]]) -> set[tuple[str, str]]:
    return {(min(a, b), max(a, b)) for a, b in pairs}


def compare(name: str, stated: dict[str, object], rec: dict[str, object]) -> dict[str, object]:
    diffs: list[str] = []
    if stated["n"] != rec["n"]:
        diffs.append(f"n {rec['n']} != {stated['n']}")
    if "angles" in stated and stated["angles"] != rec["angles"]:
        diffs.append(f"angles {rec['angles']} != {stated['angles']}")
    if not rec["all_agree"]:
        diffs.append(f"methods disagree: {rec['agree']}")
    for m in ("A", "B"):
        got: dict[str, object] = rec[m]  # pyright: ignore[reportAssignmentType]
        for key in COUNT_KEYS:
            if key in stated and stated[key] != got[key]:
                diffs.append(f"{m}.{key} {got[key]} != {stated[key]}")
        if "non_unit" in stated and stated["non_unit"] != len(got["non_unit"]):  # pyright: ignore[reportArgumentType]
            diffs.append(f"{m}.non_unit {len(got['non_unit'])} != {stated['non_unit']}")  # pyright: ignore[reportArgumentType]
        if "overlapping_pairs" in stated:
            want = pairset(stated["overlapping_pairs"])  # pyright: ignore[reportArgumentType]
            have = pairset(got["overlapping_pairs"])  # pyright: ignore[reportArgumentType]
            if want != have:
                diffs.append(
                    f"{m}.overlapping_pairs: missing {sorted(want - have)[:6]} extra {sorted(have - want)[:6]}"
                )
        if "wall_crossing_walls" in stated:
            bad = [w for w in got["wall_crossing_list"] if not w.endswith((":right", ":top"))]  # pyright: ignore[reportGeneralTypeIssues]
            if bad:
                diffs.append(f"{m}: crossings not at right/top: {bad[:6]}")
        verdict = rec[f"verdict_{m}"]
        if verdict != stated["verdict"]:
            diffs.append(f"verdict_{m} {verdict} != {stated['verdict']}")
    return {"control": name, "as_stated": not diffs, "differences": diffs}


def main(argv: list[str]) -> int:
    plan = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    rdir = Path(argv[2])
    results = []
    for name, stated in plan["controls"].items():
        rec = json.loads((rdir / f"decide-{name}.json").read_text(encoding="utf-8"))
        res = compare(name, stated, rec)
        res["receipt_sha256_file"] = rec["file_sha256"]
        results.append(res)
        status = "AS STATED" if res["as_stated"] else "DIFFERS: " + "; ".join(res["differences"])
        print(f"{name}: {status}")
    every = all(r["as_stated"] for r in results)
    out = {"results": results, "every_control_as_stated": every}
    Path(argv[3]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("EVERY_CONTROL_AS_STATED" if every else "SOME_CONTROL_DIFFERS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
