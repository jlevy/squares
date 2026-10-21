"""Exact ordering of T-196's three sides against every side registered or pending at
227, 229 and 260. Standard library only; every input is a literal read from the record
or from a certificate header. Run with `python -I margins_704.py WORKTREE OUT_JSON`.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction
from pathlib import Path

EVAND = "packing/resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs"
DEWINTER = "packing/resources/web/de-winter-upper-bounds-227-229-260-2026-10-17/source"


def header_side(path: Path) -> Fraction:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.lstrip().startswith("#"):
            n, side = line.split()
            return Fraction(side)
    raise ValueError(path)


def sci(value: Fraction) -> str:
    if value == 0:
        return "0"
    sign = "-" if value < 0 else ""
    value = abs(value)
    e = math.floor(math.log10(value.numerator) - math.log10(value.denominator))
    m = value / Fraction(10) ** e
    while m >= 10:
        m /= 10
        e += 1
    while m < 1:
        m *= 10
        e -= 1
    return f"{sign}{float(m):.4f}e{e:+03d}"


def below_sqrt2_form(side: Fraction, a: Fraction, b: Fraction) -> str:
    """Decide side <, =, > a + b*sqrt(2) exactly, for b > 0: compare ((side - a)/b)^2 with 2."""
    r = (side - a) / b
    if r < 0:
        return "below"
    r2 = r * r
    return "below" if r2 < 2 else ("equal" if r2 == 2 else "above")


def approx_gap_sqrt2(side: Fraction, a: Fraction, b: Fraction) -> float:
    return float(a) + float(b) * math.sqrt(2) - float(side)


def main(argv: list[str]) -> int:
    root = Path(argv[1])
    out = Path(argv[2])
    t196 = {}
    for n in (227, 229, 260):
        rec = json.loads((root / DEWINTER / f"n{n}" / "records.json").read_text())["records"][0]
        assert rec["n"] == n
        t196[n] = Fraction(rec["certified_side_exact"])
        printed = rec["decimal_upper_bound"]
        assert Fraction(printed) == Fraction(math.ceil(t196[n] * 10**12), 10**12), n
    t101 = {n: header_side(root / EVAND / f"n-{n}.cert") for n in (227, 229, 260)}
    # Exact sides read from the frozen comparison (claims.json on the branch) and the record.
    t155 = {
        227: Fraction("19463834764831844055010554526310613/1250000000000000000000000000000000"),
        260: Fraction("416421356237309504880168872421/25000000000000000000000000000"),
    }
    t199 = Fraction("7825080756947776580756939951343/500000000000000000000000000000")
    t198 = Fraction("7825081627429265081627421439843/500000000000000000000000000000")
    t223_260 = Fraction("146417594016514621500994169/8796093022208000000000000")  # Couzo #678, PR #701
    couzo672_print = {227: Fraction("15.563625652343"), 229: Fraction("15.650174740273")}  # rounded up
    kingbird = {  # the catalogue's closed forms, a + b*sqrt(2)
        227: (Fraction(17, 2), Fraction(5)),
        229: (Fraction(10), Fraction(4)),
        260: (Fraction(11), Fraction(4)),
    }
    kingbird_print = {227: "15.57106781186547", 229: "15.65685424949238", 260: "16.65685424949238"}
    results = {}
    for n in (227, 229, 260):
        S = t196[n]
        row = {"T-196": str(S), "T-196_float": f"{float(S):.16f}", "print_12": str(Fraction(math.ceil(S * 10**12), 10**12))}
        others = {"T-101": t101[n]}
        if n in t155:
            others["T-155"] = t155[n]
        if n == 229:
            others["T-199"] = t199
            others["T-198"] = t198
        if n == 260:
            others["T-223 (Couzo #678, PR #701)"] = t223_260
        for name, other in others.items():
            d = other - S
            row[name] = {"side": str(other), "minus_T196": str(d), "approx": sci(d), "T-196 is": "below" if d > 0 else ("equal" if d == 0 else "above")}
        a, b = kingbird[n]
        rel = below_sqrt2_form(S, a, b)
        row["Kingbird closed form"] = {"form": f"{a} + {b}*sqrt(2)", "print": kingbird_print[n], "relation_of_T196": rel, "approx_gap": f"{approx_gap_sqrt2(S, a, b):.6e}"}
        if n in couzo672_print:
            p = couzo672_print[n]
            # the print is rounded up at 12 places, so the exact side lies in (p - 1e-12, p]
            lo = p - Fraction(1, 10**12)
            row["Couzo #672 (print, rounded up)"] = {"print": str(p), "T196_minus_print": str(S - p), "approx": sci(S - p), "decided": "T-196 above #672's exact side" if S > p else ("undecided within 1e-12" if S > lo else "T-196 below #672")}
        results[n] = row
    # 229: T-199 is also the house; order of everything at 229
    order229 = sorted([("T-199", t199), ("T-198", t198), ("T-196", t196[229]), ("T-101", t101[229])], key=lambda kv: kv[1])
    results["order_229"] = [k for k, _ in order229]
    order260 = sorted([("T-223", t223_260), ("T-196", t196[260]), ("T-155", t155[260]), ("T-101", t101[260])], key=lambda kv: kv[1])
    results["order_260"] = [k for k, _ in order260]
    order227 = sorted([("T-196", t196[227]), ("T-155", t155[227]), ("T-101", t101[227])], key=lambda kv: kv[1])
    results["order_227"] = [k for k, _ in order227]
    # T-155 at 229 is not in the frozen comparison; record T-101 vs Kingbird for context
    out.write_text(json.dumps(results, indent=1), encoding="utf-8")
    print(json.dumps(results, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
