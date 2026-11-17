"""Hold the issues' printed numbers to the certificates' exact sides and to `main`'s rows.

L96 review program. Usage:
  python -I -B l96_claims.py ISSUES_JSON RECORD_ROWS_JSON OUT_JSON CHECK_DIR...
It parses the tables of #941, #942 and the #942 addendum comment, and for each row:
the printed new side against the side's 10-place ceiling; the printed record value
against `main`'s current beyond-horizon row (rounded to nearest and cut at 10 places);
the printed improvement or gain against the exact difference; and whether the exact side
lies below the current row and below the least current row at any count >= n.
"""

import glob
import json
import math
import os
import re
import sys
from fractions import Fraction as F

ROW = re.compile(r"^\|\s*(\d+)\s*\|(.*)\|\s*$")


def dec(s):
    return F(s.strip())


def floor_k(q, k):
    return F((q.numerator * 10**k) // q.denominator, 10**k)


def ceil_k(q, k):
    return -floor_k(-q, k)


def nearest_k(q, k):
    return floor_k(q + F(1, 2 * 10**k), k)


def fmt(q, k):
    v = int(q * 10**k)
    return f"{v // 10**k}.{v % 10**k:0{k}d}"


def sig2(q):
    """Two significant figures, half up, printed like 3.8e-04."""
    e = 0
    while q >= 10 ** (e + 1):
        e += 1
    while q < F(10) ** e:
        e -= 1
    m = math.floor(q / F(10) ** (e - 1) + F(1, 2))
    if m >= 100:
        m, e = m // 10, e + 1
    return f"{m // 10}.{m % 10}e{e:+03d}"


def tables(text):
    out = []
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if m:
            out.append([int(m.group(1))] + [c.strip() for c in m.group(2).split("|")])
    return out


def main():
    issues_path, rows_path, out_path = sys.argv[1:4]
    check_dirs = sys.argv[4:]
    sides = {}
    for d in check_dirs:
        for p in glob.glob(os.path.join(d, "check-n*.json")):
            with open(p) as fh:
                r = json.load(fh)
            sides[r["n"]] = (F(r["side"]["exact"]), r["file"], r["sha256"], r["verdict"])
    with open(issues_path) as fh:
        iss = json.load(fh)
    with open(rows_path) as fh:
        rows = json.load(fh)
    sources = [(f"#{i['number']}", i["body"]) for i in iss["issues"]] + [
        (f"#942 comment {c['id']}", c["body"]) for c in iss["comments"]
    ]
    results = []
    problems = []
    for where, body in sources:
        for t in tables(body):
            n = t[0]
            side, fname, sha, verdict = sides[n]
            item = {"where": where, "n": n, "file": fname, "sha256": sha, "check": verdict}
            item["printed_side"] = t[1]
            item["ceil_10"] = fmt(ceil_k(side, 10), 10)
            item["side_print_is_ceil_10"] = t[1] == item["ceil_10"]
            current = [
                r for r in rows["beyond_horizon_rows"].get(str(n), []) if r["disposition"] != "superseded"
            ]
            item["main_current_rows"] = [[r["source_id"], r["value"], r["disposition"]] for r in current]
            if where == "#941":
                rec_print, impr = t[2], t[3]
                item["printed_record"] = rec_print
                item["printed_improvement"] = impr
            else:
                item["printed_public"] = t[2]
                rec_print, impr = t[3], t[4]
                item["printed_record"] = rec_print
                item["printed_gain_over_public"] = impr
                gain = dec(t[2]) - side
                item["gain_over_public_exact_2sf"] = sig2(gain)
                item["gain_over_public_print_matches"] = sig2(gain) == impr
                item["public_print_above_side"] = gain > 0
            if current:
                val = min(dec(r["value"]) for r in current)
                near = fmt(nearest_k(val, 10), 10) == rec_print
                cut = fmt(floor_k(val, 10), 10) == rec_print
                item["record_print_rule"] = {(1, 1): "both", (1, 0): "nearest", (0, 1): "cut", (0, 0): "neither"}[
                    (int(near), int(cut))
                ]
                item["record_print_matches_row"] = near or cut
                item["below_current_row_by"] = f"{float(val - side):.6e}"
                item["below_current_row"] = side < val
                if where == "#941":
                    item["improvement_exact_6"] = fmt(nearest_k(val - side, 6), 6)
                    item["improvement_print_matches"] = item["improvement_exact_6"] == impr
            else:
                item["record_print_is_26"] = dec(rec_print) == 26
                item["below_26"] = side < 26
            mono = rows["monotone_least_current_row"].get(str(n))
            if mono:
                item["monotone_least_current_row"] = mono
                item["below_monotone_least"] = side < dec(mono["value"])
            for k, v in item.items():
                if isinstance(v, bool) and not v:
                    problems.append(f"{where} n={n}: {k} false")
            results.append(item)
    out = {"rows": results, "count": len(results), "not_as_printed": problems}
    with open(out_path, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(len(results), "rows;", len(problems), "not as printed")
    for p in problems:
        print(" ", p)


if __name__ == "__main__":
    main()
