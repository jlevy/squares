"""Is #1018's measure T-216's measure with every coordinate times 1063/1062 and every mass kept?

Lane r108-1118, blind review of jlevy/squares#1018. Compares, in exact rationals, the
source's `evidence/n108_measure.json.gz` with T-216's retained candidate
(`mixed_n108_L1062/candidate.json.gz`), and the source's copy of T-216's file with the
retained one byte for byte:

- n and total mass equal, the new side the old times the factor;
- row by row in file order: every coordinate the old one times the factor, every mass equal
  (as a number, and as the same string);
- the same as multisets, so a permutation would be reported as such;
- the merged D4 expansions: the new one the old one scaled, densities divided by the factor
  squared, so the new measure is the push-forward of the old under x -> factor x.

Imports nothing from jlevy/squares or the source.

Usage: python -I rv1018_measure.py --base T216.json.gz --new N108.json.gz
         [--source-copy Hosono_n108.json.gz] [--factor 1063/1062] --out OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1018_common as cm  # noqa: E402


def compare(base: dict, new: dict, lam: Fraction) -> dict:
    fails: list[str] = []
    if base["n"] != new["n"]:
        fails.append("n differs")
    if base["total_mass"] != new["total_mass"]:
        fails.append("total mass differs")
    if new["L"] != base["L"] * lam:
        fails.append("new side is not the old side times the factor")
    rb, rn = base["rows"], new["rows"]
    first_bad = None
    ordered = len(rb) == len(rn)
    if not ordered:
        fails.append(f"row counts differ: {len(rb)} and {len(rn)}")
    else:
        for i, (a, b) in enumerate(zip(rb, rn)):
            if any(b[k] != a[k] * lam for k in range(4)) or b[4] != a[4]:
                ordered = False
                first_bad = i
                break
            if base["raw_strings"][i]["mass"] != new["raw_strings"][i]["mass"]:
                ordered = False
                first_bad = i
                break
    scaled = Counter(tuple(a[k] * lam for k in range(4)) + (a[4],) for a in rb)
    as_sets = scaled == Counter(tuple(b) for b in rn)
    if not as_sets:
        fails.append("rows are not the scaled rows even as a multiset")
    elif not ordered:
        fails.append("rows are the scaled rows in another order")
    eb = cm.expand(rb, base["L"])
    en = cm.expand(rn, new["L"])
    push = sorted(
        (a * lam, b * lam, c * lam, d * lam, m, g / (lam * lam)) for (a, b, c, d, m, g) in eb
    )
    pushforward = push == en
    if not pushforward:
        fails.append("the new expansion is not the push-forward of the old")
    return {
        "factor": str(lam),
        "n": [base["n"], new["n"]],
        "L": [str(base["L"]), str(new["L"])],
        "B": [str(base["B"]), str(new["B"])],
        "proof_net": [
            {"step": str(base["step"]), "last": base["last"]},
            {"step": str(new["step"]), "last": new["last"]},
        ],
        "total_mass": [str(base["total_mass"]), str(new["total_mass"])],
        "rows": [len(rb), len(rn)],
        "rows_scaled_in_file_order": ordered,
        "first_row_that_differs": first_bad,
        "rows_scaled_as_multiset": as_sets,
        "expanded_distinct": [len(eb), len(en)],
        "new_is_pushforward_of_old": pushforward,
        "failures": fails,
        "verdict": "SCALED_COPY" if not fails else "NOT_A_SCALED_COPY",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--new", required=True)
    ap.add_argument("--source-copy")
    ap.add_argument("--factor", default="1063/1062")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    base = cm.read_measure(args.base)
    new = cm.read_measure(args.new)
    res = compare(base, new, Fraction(args.factor))
    res["program"] = "rv1018_measure.py"
    res["base_digests"] = {
        "stored": base["stored_sha256"],
        "json": base["json_sha256"],
        "canonical": base["canonical_sha256"],
    }
    res["new_digests"] = {
        "stored": new["stored_sha256"],
        "json": new["json_sha256"],
        "canonical": new["canonical_sha256"],
    }
    if args.source_copy:
        raw = Path(args.source_copy).read_bytes()
        res["source_copy_sha256"] = cm.sha256_bytes(raw)
        res["source_copy_is_retained_base"] = cm.sha256_bytes(raw) == base["stored_sha256"]
        if not res["source_copy_is_retained_base"]:
            res["failures"].append("the source's copy of T-216's file is not the retained one")
            res["verdict"] = "NOT_A_SCALED_COPY"
    Path(args.out).write_text(json.dumps(res, indent=1) + "\n")
    print(res["verdict"], res["failures"])
    return 0 if res["verdict"] == "SCALED_COPY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
