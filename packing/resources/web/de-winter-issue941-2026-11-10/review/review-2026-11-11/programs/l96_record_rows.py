"""List what `main` records at the 37 counts: register entries and beyond-horizon rows.

L96 review program. Usage:
  python -I l96_record_rows.py SOURCE_COVERAGE_YAML RESULTS_YAML MAIN_SHA OUT_JSON
It reads the two files as data (exported with `git show MAIN:...`) and decides nothing
about any certificate; it answers whether a count is inside the case corpus and whether
a row already stands there.
"""

import json
from fractions import Fraction
import sys

import yaml

COUNTS_941 = [413, 494, 539, 543, 547, 590, 738, 739, 753, 794, 809, 810, 851, 867, 910]
COUNTS_942 = [632, 637, 655, 684, 685, 744, 750, 756, 805, 814, 918, 921, 924, 935, 970, 989]
COUNTS_A0C = [597, 754, 864, 865, 869, 991]
ALL = sorted(COUNTS_941 + COUNTS_942 + COUNTS_A0C)


def load(path):
    with open(path, "rb") as fh:
        return yaml.load(fh, Loader=getattr(yaml, "CSafeLoader", yaml.SafeLoader))


def main():
    cov_path, res_path, sha, out = sys.argv[1:5]
    cov = load(cov_path)
    res = load(res_path)
    corpus = cov["case_corpus"]
    rows = {n: [] for n in ALL}
    current = []
    dispositions = {}
    for row in cov.get("beyond_horizon_claims", []):
        disp = row.get("disposition")
        dispositions[str(disp)] = dispositions.get(str(disp), 0) + 1
        if disp != "superseded" and row.get("claim") == "upper-bound":
            current.append((Fraction(str(row["value"])), row["n"], row["source_id"], str(row["value"])))
        if row.get("n") in rows:
            rows[row["n"]].append(
                {k: row.get(k) for k in ("source_id", "claim", "value", "assurance", "disposition", "superseded_by")}
            )
    entries = {n: [] for n in ALL}
    results = res["results"] if isinstance(res, dict) and "results" in res else res
    for entry in results:
        scope = entry.get("scope") or {}
        for n in scope.get("n_values") or []:
            if n in entries:
                entries[n].append({"id": entry.get("id"), "kind": entry.get("kind")})
    # Monotonicity: s(n) <= s(m) for m >= n, so every current row at a count m >= n bounds
    # s(n). The least such row is a lower envelope of the record's start at n; Goebel's
    # constructions and border consequences, which the import lane's start also holds,
    # are not computed here.
    monotone = {}
    for n in ALL:
        best = min((r for r in current if r[1] >= n), default=None)
        if best is not None:
            monotone[str(n)] = {"value": best[3], "at_n": best[1], "source_id": best[2]}
    report = {
        "main": sha,
        "case_corpus": corpus,
        "dispositions": dispositions,
        "monotone_least_current_row": monotone,
        "counts": ALL,
        "inside_corpus": [n for n in ALL if corpus["n_min"] <= n <= corpus["n_max"]],
        "register_entries": {str(n): entries[n] for n in ALL if entries[n]},
        "beyond_horizon_rows": {str(n): rows[n] for n in ALL if rows[n]},
        "counts_with_no_row": [n for n in ALL if not rows[n] and not entries[n]],
    }
    with open(out, "w") as fh:
        json.dump(report, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: report[k] for k in ("inside_corpus", "register_entries", "counts_with_no_row", "dispositions")}))
    for n in ALL:
        print("monotone", n, report["monotone_least_current_row"].get(str(n)))
    for n in ALL:
        for r in rows[n]:
            print(n, r["source_id"], r["value"], r["assurance"], r.get("disposition"))


if __name__ == "__main__":
    main()
