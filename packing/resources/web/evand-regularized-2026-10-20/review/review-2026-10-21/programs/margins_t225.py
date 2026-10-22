"""Exact newness margins for T-225's four sides against the record on main.

Decides no geometry. For each count n in {204, 227, 229, 260} it reads the certificate's
header side with review_t225_check's reader and, by exact arithmetic:

* checks it equals the side T-225's claim states, as a fraction and as the claim's
  30-place decimal, and equals the JSON's S_cert; and that it is S_exact (the JSON's
  60-digit decimal) times 1 + 1e-20, rounded up at 30 places;
* compares it with the case's reported and verified upper bounds at n on main (the
  house best packing's side), and with #672's exact side at 227 (lineage);
* compares it with the verified and the reported upper bound at every count m with
  n < m <= 324 on main, since deleting m - n squares from any packing of m squares leaves
  a packing of n in the same box: the side is new only if it is below all of them.

Exact forms read: integers, p/q, `A + (p/q)`, and `A + B sqrt(k)` with A, B integers or
(p/q); a null form falls back to the record's `value`, compared as a print rounded up
(the side must lie below value - 10^-places to be decided below).

Usage: python -I margins_t225.py DATA_DIR OUT.json
DATA_DIR holds packet/, fetched-672/n227.cert and main-cases/n-NNN.md (git show of main).
"""

from __future__ import annotations

import gzip
import json
import math
import re
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import review_t225_check as check  # noqa: E402

CLAIM = {
    204: (Fraction(14808642840591493923068442871459, 10**30), "14.808642840591493923068442871459"),
    227: (Fraction(7781812826162574542396221861851, 5 * 10**29), "15.563625652325149084792443723702"),
    229: (Fraction(15650161513876431064009548865321, 10**30), "15.650161513876431064009548865321"),
    260: (Fraction(4161438312629953048686574163329, 25 * 10**28), "16.645753250519812194746296653316"),
}
HOUSES = {204: "T-223", 227: "T-196", 229: "T-199", 260: "T-223"}
RAT = r"(?:\((\d+)/(\d+)\)|(\d+))"
SURD = re.compile(rf"{RAT} \+ {RAT} ?sqrt\((\d+)\)")
SUM = re.compile(rf"{RAT} \+ \((\d+)/(\d+)\)")


def rat(groups: tuple) -> Fraction:
    p, q, whole = groups
    return Fraction(int(whole)) if whole is not None else Fraction(int(p), int(q))


class Exact:
    """A + B sqrt(k) with A, B rational, k a non-square positive integer (or B = 0)."""

    def __init__(self, a: Fraction, b: Fraction = Fraction(0), k: int = 0, text: str = "") -> None:
        self.a, self.b, self.k, self.text = a, b, k, text

    def above(self, s: Fraction) -> bool:
        """s < A + B sqrt(k), decided exactly (B >= 0)."""
        if self.b == 0:
            return s < self.a
        d = s - self.a
        return d < 0 or d * d < self.b * self.b * self.k

    def minus(self, s: Fraction) -> str:
        """(A + B sqrt(k)) - s to seven significant digits, from the exact difference."""
        if self.b == 0:
            return f"{float(self.a - s):.6e}"
        with localcontext() as context:
            context.prec = 60
            value = (Decimal(self.a.numerator) / Decimal(self.a.denominator) - Decimal(s.numerator) / Decimal(s.denominator)) + (
                Decimal(self.b.numerator) / Decimal(self.b.denominator)
            ) * Decimal(self.k).sqrt()
        return f"{float(value):.6e}"


def parse_form(text: str) -> Exact | None:
    text = text.strip().strip("'")
    if re.fullmatch(r"\d+(/\d+)?", text):
        return Exact(Fraction(text), text=text)
    m = SURD.fullmatch(text)
    if m:
        g = m.groups()
        return Exact(rat(g[0:3]), rat(g[3:6]), int(g[6]), text)
    m = SUM.fullmatch(text)
    if m:
        g = m.groups()
        return Exact(rat(g[0:3]) + Fraction(int(g[3]), int(g[4])), text=text)
    return None


def lane(md: str, name: str) -> tuple[Exact | None, str | None]:
    block = re.search(rf"^  {name}:\n((?:    .*\n)+)", md, re.M)
    if block is None:
        return None, None
    value = re.search(r"^    value: '?([0-9.]+)'?", block.group(1), re.M)
    form = re.search(r"^    exact_form: (.*)$", block.group(1), re.M)
    exact = parse_form(form.group(1)) if form and form.group(1).strip() not in ("null", "") else None
    return exact, value.group(1) if value else None


def below(side: Fraction, exact: Exact | None, value: str | None) -> tuple[bool, str, str]:
    """Whether side < the bound, how it was decided, and the margin (approx)."""
    if exact is not None:
        return exact.above(side), "exact", exact.minus(side)
    places = len(value.partition(".")[2])
    printed = Fraction(Decimal(value))
    lower = printed - Fraction(1, 10**places)
    return side < lower, f"print {value} rounded up", f"{float(printed - side):.6e}"


def main(argv: list[str]) -> int:
    data, out = Path(argv[1]), Path(argv[2])
    certs = data / "packet/source/search/regularize/lists/certs"
    cases = {int(p.stem[2:]): p.read_text("utf-8") for p in (data / "main-cases").glob("n-*.md")}
    p672_side, _rows = check.read_certificate((data / "fetched-672/n227.cert").read_text("ascii"), 227)
    p672 = Fraction(*p672_side)
    report = {"main": (data / "main-cases/MAIN_COMMIT").read_text().strip(), "counts": {}}
    ok_all = True
    for n, (claimed, decimal) in CLAIM.items():
        text = gzip.decompress((certs / f"n-{n:03d}.cert.gz").read_bytes()).decode("ascii")
        side = Fraction(*check.read_certificate(text, n)[0])
        document = json.loads(gzip.decompress((certs / f"n-{n:03d}.json.gz").read_bytes()))
        solved = Fraction(Decimal(document["S_exact"]))
        made = Fraction(math.ceil(solved * (1 + Fraction(1, 10**20)) * 10**30), 10**30)
        row = {
            "side": f"{side.numerator}/{side.denominator}",
            "ceiling_16": (lambda c: f"{c // 10**16}.{c % 10**16:016d}")(math.ceil(side * 10**16)),
            "equals_claim_fraction": side == claimed,
            "equals_claim_decimal": side == Fraction(Decimal(decimal)),
            "equals_json_S_cert": side == Fraction(document["S_cert"]),
            "is_S_exact_times_1e-20_rounded_up_at_30": side == made,
            "above_S_exact_by": f"{float(side - solved):.6e}",
        }
        md = cases[n]
        rep, rep_v = lane(md, "reported_upper_bound")
        ver, ver_v = lane(md, "verified_upper_bound")
        house = {}
        for name, (exact, value) in (("reported", (rep, rep_v)), ("verified", (ver, ver_v))):
            is_below, how, margin = below(side, exact, value)
            house[name] = {"form": exact.text if exact else None, "below": is_below, "how": how, "margin": margin}
            if exact is not None and exact.b == 0:
                house[name]["margin_exact"] = str(exact.a - side)
            ok_all &= is_below
        row["house_at_n"] = {"holder": HOUSES[n], **house}
        if n == 227:
            row["below_672_exact_side"] = {"below": side < p672, "margin": f"{float(p672 - side):.6e}", "margin_exact": str(p672 - side)}
        later = []
        for m in range(n + 1, 325):
            for name in ("verified_upper_bound", "reported_upper_bound"):
                exact, value = lane(cases[m], name)
                if exact is None and value is None:
                    continue
                is_below, how, margin = below(side, exact, value)
                later.append({"m": m, "lane": name.split("_")[0], "below": is_below, "how": how, "margin": float(margin), "form": exact.text[:60] if exact else value})
        nearest = min(later, key=lambda r: r["margin"])
        next_verified = next(r for r in later if r["m"] == n + 1 and r["lane"] == "verified")
        nv_exact, _ = lane(cases[n + 1], "verified_upper_bound")
        row["next_count_verified"] = {**next_verified, "margin_exact": str(nv_exact.a - side) if nv_exact and nv_exact.b == 0 else None}
        row["all_later_counts_below"] = all(r["below"] for r in later)
        row["later_bounds_compared"] = len(later)
        row["least_later_margin"] = nearest
        ok_all &= row["all_later_counts_below"] and row["equals_claim_fraction"] and row["equals_claim_decimal"]
        report["counts"][str(n)] = row
        print(n, json.dumps(row)[:1500], flush=True)
    out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print("margins", "all new" if ok_all else "NOT ALL NEW")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
