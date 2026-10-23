#!/usr/bin/env python3
"""Exact newness of T-226, T-227 and T-228 in report order, and their status now.

Decides no geometry. Sides are read from the retained certificates' headers (this
review's reader) and from the retained exact files of the packings they are compared
with; houses from `main`'s case records (`git show`), at the 18 October ledger's freeze
(`804eff369`, before all three reports) and at the review's `main`.

For each certificate it checks, by exact arithmetic:
* the header side equals the register claim's fraction and `claims.json`'s exact side,
  and the issue's 12-place print is that side rounded up;
* the side is below every earlier member of its count's chain in report order (the
  house at the ledger's freeze and every earlier report), and above every later one;
* the side is below the verified and reported upper bound at every count m with
  n < m <= 324 on `main` (bounds only fall, so `main`'s are at most those of the
  report's day): deleting m - n squares of a packing of m leaves one of n.

Exact forms read: p/q, integers, and sums of rationals with at most one surd term
`B sqrt(k)` (B >= 0); a null form falls back to the print, decided only where the side
lies below print - 10^-places.

Usage: python -I margins_0nse.py REPO DATA_DIR OUT.json
DATA_DIR holds main-cases/n-NNN.md and start-cases/n-NNN.md with MAIN_COMMIT files.
"""

from __future__ import annotations

import gzip
import importlib.util
import json
import math
import re
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("review_0nse_check", HERE / "review_0nse_check.py")
check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check)

WEB = "packing/resources/web"


def header_side(path: Path) -> Fraction:
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    _, side, _, _ = check.read(data.decode("ascii"))
    return Fraction(*side)


def json_side(path: Path) -> Fraction:
    return Fraction(json.loads(gzip.decompress(path.read_bytes()))["side"])


class Form:
    """A + B sqrt(k), A and B rational, B >= 0."""

    def __init__(self, a: Fraction, b: Fraction = Fraction(0), k: int = 0, text: str = "") -> None:
        self.a, self.b, self.k, self.text = a, b, k, text

    def above(self, s: Fraction) -> bool:
        d = s - self.a
        if self.b == 0:
            return d < 0
        return d < 0 or d * d < self.b * self.b * self.k

    def below(self, s: Fraction) -> bool:
        d = s - self.a
        if self.b == 0:
            return d > 0
        return d > 0 and d * d > self.b * self.b * self.k

    def minus(self, s: Fraction) -> Decimal:
        with localcontext() as context:
            context.prec = 80
            value = Decimal(self.a.numerator) / Decimal(self.a.denominator) - Decimal(s.numerator) / Decimal(s.denominator)
            if self.b:
                value += Decimal(self.b.numerator) / Decimal(self.b.denominator) * Decimal(self.k).sqrt()
            return +value


_RATIONAL = r"\((\d+)/(\d+)\)|(\d+)/(\d+)|(\d+)"
_TERM = re.compile(rf"(?:{_RATIONAL})?(?:\s*\*?\s*sqrt\((\d+)\))?")


def _rational(groups) -> Fraction | None:
    p1, q1, p2, q2, whole = groups
    if p1 is not None:
        return Fraction(int(p1), int(q1))
    if p2 is not None:
        return Fraction(int(p2), int(q2))
    if whole is not None:
        return Fraction(int(whole))
    return None


def parse_form(text: str) -> Form | None:
    text = text.strip().strip("'")
    if text in ("", "null"):
        return None
    a, b, k = Fraction(0), Fraction(0), 0
    for term in text.split(" + "):
        match = _TERM.fullmatch(term.strip())
        if match is None or term.strip() == "":
            return None
        r = _rational(match.groups()[:5])
        surd = match.group(6)
        if surd is None:
            if r is None:
                return None
            a += r
        else:
            if k and int(surd) != k:
                return None
            k = int(surd)
            b += r if r is not None else Fraction(1)
    return Form(a, b, k, text)


def lane(md: str, name: str) -> tuple[Form | None, str | None]:
    block = re.search(rf"^  {name}:\n((?:    .*\n)+)", md, re.M)
    if block is None:
        return None, None
    value = re.search(r"^    value: '?([0-9.]+)'?", block.group(1), re.M)
    form = re.search(r"^    exact_form: (.*)$", block.group(1), re.M)
    return (parse_form(form.group(1)) if form else None), (value.group(1) if value else None)


def compare(side: Fraction, form: Form | None, value: str | None) -> dict:
    """Is side below the bound? Exact where a form is read, else by the print."""
    if form is not None:
        return {"below": form.above(side), "how": "exact", "bound_minus_side": f"{float(form.minus(side)):.6e}", "form": form.text[:80]}
    places = len(value.partition(".")[2])
    printed = Fraction(Decimal(value))
    return {"below": side < printed - Fraction(1, 10**places), "how": f"print {value}", "bound_minus_side": f"{float(printed - side):.6e}"}


def ceil_places(x: Fraction, places: int) -> str:
    c = math.ceil(x * 10**places)
    return f"{c // 10**places}.{c % 10**places:0{places}d}"


def main(argv: list[str]) -> int:
    repo, data, out = Path(argv[1]), Path(argv[2]), Path(argv[3])
    web = repo / WEB
    main_cases = {int(p.stem[2:]): p.read_text("utf-8") for p in (data / "main-cases").glob("n-*.md")}
    start_cases = {int(p.stem[2:]): p.read_text("utf-8") for p in (data / "start-cases").glob("n-*.md")}

    sides = {
        "T-226 (#670)": header_side(web / "couzo-issue670-2026-10-17/source/certificates/n204.cert"),
        "T-228 (#675)": header_side(web / "couzo-issue675-2026-10-18/source/certificates/best/n204.cert"),
        "T-227@227 (#672)": header_side(web / "couzo-issue672-2026-10-17/source/certificates/n227.cert"),
        "T-227@229 (#672)": header_side(web / "couzo-issue672-2026-10-17/source/certificates/n229.cert"),
        "T-223 (#678)@204": header_side(web / "couzo-issue678-2026-10-18/source/certificates/best/n204.cert"),
        "T-225@204": header_side(web / "evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-204.cert.gz"),
        "T-225@227": header_side(web / "evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-227.cert.gz"),
        "T-225@229": header_side(web / "evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-229.cert.gz"),
        "T-196 (#668)@227": json_side(web / "de-winter-upper-bounds-227-229-260-2026-10-17/source/n227/n227_exact.json.gz"),
        "T-196 (#668)@229": json_side(web / "de-winter-upper-bounds-227-229-260-2026-10-17/source/n229/n229_exact.json.gz"),
        "T-198 (#674 opening)": header_side(web / "evand-n229-dilation-2026-10-17/source/search/packer/candidates/s229.cert"),
        "T-199 (#674 update)": header_side(web / "evand-n229-dilation-update-2026-10-18/source/search/packer/candidates/s229_v2.cert"),
    }
    # The held register candidate of think-qdcc (20 October): T-196 solved 1.66e-8 lower by
    # Evan Daniel's driver; #672's issue prints it as the prior at 227. Not a report.
    held_227 = Fraction(486368646470642329014092781873, 31250000000000000000000000000)

    claims_text = {
        "T-226 (#670)": (Fraction(45044217780850246618141, 3041751595240000000000), "couzo-issue670-2026-10-17", 204),
        "T-228 (#675)": (Fraction(101859759444979981360793459, 6878398651426000000000000), "couzo-issue675-2026-10-18", 204),
        "T-227@227 (#672)": (Fraction(71427829379429597600111901507, 4589408083628500000000000000), "couzo-issue672-2026-10-17", 227),
        "T-227@229 (#672)": (Fraction(231170315041711399213831561, 14771101209934000000000000), "couzo-issue672-2026-10-17", 229),
    }

    def start(n: int) -> list[tuple[str, str, Form | None, str | None]]:
        rows = []
        for name in ("verified_upper_bound", "reported_upper_bound"):
            form, value = lane(start_cases[n], name)
            rows.append((f"house at 804eff369 ({name.split('_')[0]})", "2026-10-17T06:37:10Z (freeze)", form, value))
        return rows

    chains = {
        204: [
            ("T-226 (#670)", "2026-10-17T18:05:06Z"),
            ("T-228 (#675)", "2026-10-18T06:02:11Z"),
            ("T-223 (#678)@204", "2026-10-18T23:23:19Z"),
            ("T-225@204", "2026-10-20T02:36:12Z"),
        ],
        227: [
            ("T-196 (#668)@227", "2026-10-17T14:06:25Z"),
            ("T-227@227 (#672)", "2026-10-17T20:48:34Z"),
            ("T-225@227", "2026-10-20T02:36:12Z"),
        ],
        229: [
            ("T-196 (#668)@229", "2026-10-17T14:06:25Z"),
            ("T-227@229 (#672)", "2026-10-17T20:48:34Z"),
            ("T-198 (#674 opening)", "2026-10-17T23:10:59Z"),
            ("T-199 (#674 update)", "2026-10-18T01:36:21Z"),
            ("T-225@229", "2026-10-20T02:36:12Z"),
        ],
    }

    report: dict = {"main": (data / "main-cases/MAIN_COMMIT").read_text().strip(), "start": (data / "start-cases/MAIN_COMMIT").read_text().strip(), "rows": {}}
    ok = True
    for label, (claimed, packet, n) in claims_text.items():
        side = sides[label]
        claims = json.loads((web / packet / "acquisition/claims.json").read_text("utf-8"))
        row_claims = next(r for r in claims["results"] if r["n"] == n)
        row: dict = {
            "n": n,
            "side": f"{side.numerator}/{side.denominator}",
            "side_approx": f"{Decimal(side.numerator) / Decimal(side.denominator):.20f}",
            "equals_register_claim": side == claimed,
            "equals_claims_json_exact_side": side == Fraction(row_claims["exact_side"]),
            "issue_print": row_claims["offered_side"],
            "issue_print_is_ceiling_at_12": ceil_places(side, 12) == row_claims["offered_side"],
            "ceiling_at_16": ceil_places(side, 16),
            "claims_json_ceiling_equal": ceil_places(side, 16) == row_claims["ceiling"],
        }
        ok &= row["equals_register_claim"] and row["equals_claims_json_exact_side"] and row["issue_print_is_ceiling_at_12"]
        # report order
        chain = chains[n]
        position = [c[0] for c in chain].index(label)
        earlier = []
        for name, when, form, value in start(n):
            r = compare(side, form, value)
            earlier.append({"against": name, "reported": when, **r})
            ok &= r["below"]
        for name, when in chain[:position]:
            other = sides[name]
            earlier.append({"against": name, "reported": when, "below": side < other, "how": "exact", "bound_minus_side": f"{float(other - side):.6e}", "exact_difference": str(other - side)})
            ok &= side < other
        if n == 227:
            earlier.append({"against": "held candidate of think-qdcc (Daniel's driver on T-196, 20 October; #672's printed prior)", "reported": "not a report", "below": side < held_227, "how": "exact", "bound_minus_side": f"{float(held_227 - side):.6e}"})
        later = []
        for name, when in chain[position + 1 :]:
            other = sides[name]
            later.append({"by": name, "reported": when, "below_this": other < side, "side_minus_other": f"{float(side - other):.6e}", "exact_difference": str(side - other)})
        # the house now
        now = {}
        for name in ("verified_upper_bound", "reported_upper_bound"):
            form, value = lane(main_cases[n], name)
            now[name.split("_")[0]] = {"form": form.text[:80] if form else value, "this_minus_house": f"{float(-form.minus(side)):.6e}" if form else None, "house_below_this": form.below(side) if form else None}
        now["house_is_T-225"] = lane(main_cases[n], "verified_upper_bound")[0].a == sides[f"T-225@{n}"]
        # later counts on main
        later_counts = []
        for m in range(n + 1, 325):
            for name in ("verified_upper_bound", "reported_upper_bound"):
                form, value = lane(main_cases[m], name)
                if form is None and value is None:
                    continue
                r = compare(side, form, value)
                later_counts.append({"m": m, "lane": name.split("_")[0], **r})
        least = min(later_counts, key=lambda r: float(r["bound_minus_side"]))
        row |= {
            "earlier_in_report_order": earlier,
            "below_every_earlier": all(e["below"] for e in earlier),
            "later_in_report_order": later,
            "superseded_by_every_later": all(e["below_this"] for e in later),
            "house_on_main_now": now,
            "later_counts_compared": len(later_counts),
            "later_counts_decided_by_print": sum(1 for r in later_counts if r["how"] != "exact"),
            "below_every_later_count": all(r["below"] for r in later_counts),
            "least_later_margin": least,
        }
        ok &= row["below_every_later_count"] and row["superseded_by_every_later"]
        report["rows"][label] = row
        print(label, json.dumps({k: v for k, v in row.items() if k not in ("earlier_in_report_order", "later_in_report_order")})[:900])
        for e in earlier:
            print("   below", e["against"], e["below"], e["how"], e["bound_minus_side"])
        for e in later:
            print("   superseded by", e["by"], e["below_this"], e["side_minus_other"])
    out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print("margins", "all as the entries claim" if ok else "SOME NOT AS CLAIMED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
