#!/usr/bin/env python3
"""The side of #728's certificate, its print, and its margins against the record at 303.

A measurement for the review of #728 (lane c-review-728-math), run after
review_728_check.py had decided the certificate. It decides no feasibility. It reads
the certificate with review_728_check.py's reader and the record with PyYAML (a
third-party library in the project environment); it imports no repository code.

It establishes, by exact rational arithmetic:
  1. the header side equals the claimed fraction, and the issue's prints of it;
  2. the house at 303 on main (the witness, the case record's two upper lanes), and the
     margin below it;
  3. the margin below every earlier report at 303 that the record retains with a side:
     the packets' claims (exact sides), the facts and certificates of the older imports,
     the case record's printed priority notes, and the Kingbird (Ellsworth) catalogue
     captures, the printed ones with a 10^-places allowance;
  4. that the side is below the verified and reported upper bounds at every count m with
     303 < m <= 324 on main (s(303) <= s(m)); beyond 324 every bound is at least
     sqrt(m) > 18 by area;
  5. the f64 input's side and the dilation the issue states (1 + 1e-12), if given.

Usage:
    python3 -I margins_728.py CERT --repo /path/to/squares [--input F64.txt] --out FILE.json
"""

from __future__ import annotations

import argparse
import glob
import gzip
import json
import math
import os
import re
import sys
from fractions import Fraction as F

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review_728_check as chk  # noqa: E402

CLAIM = F(447744305431858194305431410441, 25000000000000000000000000000)
ISSUE_PRINT = "17.909772217275"
ISSUE_LONG = "17.909772217274327772"  # printed with a trailing ellipsis
ISSUE_BEST_BEFORE = "17.909958291070"
ISSUE_IMPROVEMENT = "1.86e-4"


def ceil_print(x: F, places: int) -> str:
    q = -((-x.numerator * 10**places) // x.denominator)
    s = str(q).rjust(places + 1, "0")
    return f"{s[:-places]}.{s[-places:]}"


def trunc_print(x: F, places: int) -> str:
    q = (x.numerator * 10**places) // x.denominator
    s = str(q).rjust(places + 1, "0")
    return f"{s[:-places]}.{s[-places:]}"


def dec(text: str) -> tuple[F, F]:
    """A printed decimal and its allowance 10^-places."""
    places = len(text.partition(".")[2])
    return F(text), F(1, 10**places)


def sci(x: F, digits: int = 7) -> str:
    return chk.sci(x.numerator, x.denominator, digits)


def front_matter(path: str) -> dict:
    text = open(path, encoding="utf-8").read()
    _, fm, _ = text.split("---", 2)
    return yaml.safe_load(fm)


def bound_value(entry: dict | None) -> tuple[F, F, str] | None:
    """(value, allowance, how): exact where exact_form is a rational literal."""
    if not entry:
        return None
    ef = entry.get("exact_form")
    if isinstance(ef, str) and re.fullmatch(r"-?[0-9]+(/[0-9]+)?", ef):
        return F(ef), F(0), "exact"
    v, a = dec(str(entry["value"]))
    return v, a, f"printed {entry['value']} ({ef or 'no exact form'})"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--input")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    P = os.path.join(args.repo, "packing")
    cert = chk.read_certificate(open(args.cert, "rb").read())
    S = F(*cert["side"])
    out: dict = {"side": str(S), "side_sci": sci(S, 25)}

    # 1. the side and its prints
    out["side_equals_claim"] = S == CLAIM
    out["ceil_12"] = ceil_print(S, 12)
    out["ceil_12_equals_issue_print"] = ceil_print(S, 12) == ISSUE_PRINT
    out["issue_long_print_is_truncation"] = trunc_print(S, len(ISSUE_LONG.partition(".")[2])) == ISSUE_LONG
    out["side_is_not_a_12_place_decimal"] = S * 10**12 != int(S * 10**12)

    # 2. the house on main
    fm = front_matter(os.path.join(P, "frontier/n-303.md"))["packing"]
    wit = yaml.safe_load(open(os.path.join(P, "witnesses/known-best/n-303.yaml")))["witness"]
    house_w = F(wit["side"])
    ver = bound_value(fm["verified_upper_bound"])
    rep = bound_value(fm["reported_upper_bound"])
    out["house"] = {
        "witness_id": wit["id"],
        "witness_side": str(house_w),
        "witness_side_sci": sci(house_w, 20),
        "verified_exact_equals_witness": ver[0] == house_w and ver[2] == "exact",
        "reported_exact_equals_witness": rep[0] == house_w and rep[2] == "exact",
        "verified_value_print": fm["verified_upper_bound"]["value"],
        "verified_value_is_ceiling_of_witness_side": fm["verified_upper_bound"]["value"]
        == ceil_print(house_w, len(fm["verified_upper_bound"]["value"].partition(".")[2])),
        "evidence": fm["verified_upper_bound"]["evidence"],
        "margin": str(house_w - S),
        "margin_sci": sci(house_w - S, 13),
        "issue_best_before_is_ceil12_of_house": ceil_print(house_w, 12) == ISSUE_BEST_BEFORE,
        "issue_improvement_print": ISSUE_IMPROVEMENT,
        "improvement_rounds_to_issue": f"{float(house_w - S):.2e}" == "1.86e-04",
    }

    # 3. earlier reports at 303 that the record retains with a side
    reports = []

    def add(label, when, value, allowance, source):
        reports.append(
            {
                "report": label,
                "when": when,
                "side": str(value) if allowance == 0 else f"{value} (printed, +/- {allowance})",
                "margin_lower": str(value - allowance - S),
                "margin_sci": sci(value - S, 7),
                "below": value - allowance > S,
                "how": "exact" if allowance == 0 else "printed",
                "source": source,
            }
        )

    case_text = open(os.path.join(P, "frontier/n-303.md"), encoding="utf-8").read()
    for note in fm["priority_notes"]:
        m = re.match(r"s\(303\) <= ([0-9.]+)", note["claim"])
        if m:
            v, a = dec(m.group(1))
            add(", ".join(note["claimed_by"]), note["published"], v, a, "frontier/n-303.md priority_notes")
    for name, rel in (
        ("Couzo 2026-09-27 packet (T-056)", "resources/web/franciscouzo-square-packing-2026-09-27/facts/n-303.yaml"),
        ("Couzo 2026-10-03 packet (T-092)", "resources/web/franciscouzo-square-packing-2026-10-03/facts/n-303.yaml"),
    ):
        side = yaml.safe_load(open(os.path.join(P, rel)))
        side = side.get("side") or side.get("witness", {}).get("side")
        add(name, rel.split("/")[2][-10:], F(str(side)), F(0), rel + " (side as the packet states it)")
    rel = "resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-303.cert"
    add("Daniel exact optima (T-098)", "2026-10-05", F(*chk.read_certificate(open(os.path.join(P, rel), "rb").read())["side"]), F(0), rel)
    rel = "resources/web/squish-401-2026-10-07/facts/n-303.json.gz"
    add("SQUISH #401 (T-113)", "2026-10-07", F(json.load(gzip.open(os.path.join(P, rel)))["side"]), F(0), rel)
    for path in sorted(glob.glob(os.path.join(P, "resources/web/*/acquisition/claims.json"))):
        d = json.load(open(path))
        for row in d.get("results", []):
            if str(row.get("n")) == "303" and row.get("exact_side"):
                add(
                    f"{os.path.basename(os.path.dirname(os.path.dirname(path)))} ({d.get('issue')})",
                    row.get("first_committed"),
                    F(row["exact_side"]),
                    F(0),
                    os.path.relpath(path, P),
                )
    for cap in sorted(glob.glob(os.path.join(args.repo, "attic/intake/kingbird-*/kingbird-squares-in-squares.md"))) + [
        os.path.join(P, "resources/web/kingbird-squares-in-squares.md")
    ]:
        text = open(cap, encoding="utf-8").read()
        m = re.search(r"\n303 *\n.*?\n\$s = \\Nn\{([0-9.]+)\}\$", text, re.S)
        if m:
            v, a = dec(m.group(1))
            add("Kingbird (David Ellsworth's catalogue)", os.path.basename(os.path.dirname(cap)) if "attic" in cap else "retained 2026-09-30", v, a, os.path.relpath(cap, args.repo))
    for path in sorted(glob.glob(os.path.join(P, "campaign/issue-intake/**/ledger.yaml"), recursive=True)):
        d = yaml.safe_load(open(path))
        for rep_ in d.get("reports", []):
            for c in rep_.get("claims", []):
                if c.get("n") == 303 and c.get("exact"):
                    add(f"ledger: {rep_['report']}", rep_.get("reported_at"), F(c["exact"]), F(0), os.path.relpath(path, P))
    out["earlier_reports"] = reports
    out["every_earlier_report_above"] = all(r["below"] for r in reports)
    least = min(reports, key=lambda r: F(r["margin_lower"]))
    out["least_margin_report"] = least
    out["case_record_mentions_no_lower_report"] = "17.9097" not in case_text

    # 4. later counts
    later = []
    for m in range(304, 325):
        path = os.path.join(P, f"frontier/n-{m}.md")
        f = front_matter(path)["packing"]
        for lane in ("verified_upper_bound", "reported_upper_bound"):
            b = bound_value(f.get(lane))
            if b is None:
                continue
            v, a, how = b
            later.append({"n": m, "lane": lane, "how": how, "margin_lower": str(v - a - S), "margin_sci": sci(v - a - S, 7), "below": v - a > S})
    out["later_counts"] = {
        "bounds": len(later),
        "all_below": all(x["below"] for x in later),
        "exact": sum(1 for x in later if x["how"] == "exact"),
        "printed": [x for x in later if x["how"] != "exact"],
        "least": min(later, key=lambda x: F(x["margin_lower"])),
        "beyond_324": "every bound at m >= 325 is at least sqrt(m) > 18 > S by area",
    }

    # 5. the f64 input and the dilation
    if args.input:
        head = open(args.input).readline().split()
        s64 = float(head[1])
        e = F(s64)
        dil = e * (1 + F(1, 10**12))
        out["f64"] = {
            "header": head,
            "binary64_side_exact": str(e),
            "dilated_by_1e-12": sci(dil, 30),
            "certificate_minus_dilated": sci(S - dil, 6),
            "certificate_is_dilated_side_rounded_to_29_places": S == F(round(dil * 10**29), 10**29),
            "certificate_over_binary64_side_minus_1": sci(S / e - 1, 10),
        }

    open(args.out, "w").write(json.dumps(out, indent=1) + "\n")
    show = {k: v for k, v in out.items() if k not in ("earlier_reports", "later_counts")}
    show["later_counts"] = {k: v for k, v in out["later_counts"].items() if k != "printed"}
    show["later_counts"]["printed_count"] = len(out["later_counts"]["printed"])
    print(json.dumps(show, indent=1))
    print("earlier reports at 303:")
    for r in sorted(reports, key=lambda r: F(r["margin_lower"])):
        print(f"  {r['margin_sci']:>16}  {r['how']:7} {str(r['when'])[:20]:20} {r['report'][:70]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
