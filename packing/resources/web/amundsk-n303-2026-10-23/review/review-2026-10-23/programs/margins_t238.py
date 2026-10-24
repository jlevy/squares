#!/usr/bin/env python3
"""The side of the issue 755 certificate, its prints, and its margins against the record.

Written for the stage 4 review of T-238 (bead think-jdz0). Decides nothing: it measures.

It reads the certificate's header side exactly, prints it rounded up at 12, 16 and 30
places, and compares it with the issue's statements: the bound 17.909762327476, the
improvement 9.89e-6, and the decimal expansion 17.909762327475256427 that the issue and
the gist README give for it. It reads the exact side of every earlier report at 303 from
its retained file in the repository at REF (a certificate header, a derived fact's
`side`, a SQUISH JSON `side` or an `sqcert` `s` line; where the record keeps only a
print, the print, as for the Kingbird catalogue's two retained captures), in report order, and gives the certificate's margin below each. It then
reads every case record from 304 to 320 at REF and compares the side with each reported
and verified upper bound, since s(303) <= s(m) for m > 303; from 321 on every bound is at
least sqrt(m) >= sqrt(321) > 17.916 by area.

Usage:
  python3 -I margins_t238.py CERT --repo /home/user/squares --ref origin/main --out OUT.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import subprocess
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path

getcontext().prec = 120

WEB = "packing/resources/web/"

#: Every report at 303 the record holds, in report order: label, date (UTC, as the record
#: keys it), how its side is read, and where.
REPORTS = [
    ("the basic grid", "", "value", "18"),
    ("Kingbird, David Ellsworth's catalogue (the capture of 22 August, a print)", "2026-08-22", "kingbird",
     WEB + "kingbird-squares-in-squares-2026-08-22.md"),
    ("Kingbird, the same catalogue (the capture of 30 September, page of 24 September, a print)", "2026-09-24",
     "kingbird", WEB + "kingbird-squares-in-squares.md"),
    ("Griffin Casson, griffcass/square-packing 82661bc", "2026-09-24", "casson",
     WEB + "casson-square-packing-2026-09-23/griffcass-square-packing/results/packings/n303.txt"),
    ("Francisco Couzo's first, franciscouzo/square-packing 801915f (a priority note)", "2026-09-24", "print",
     "17.928562541013548"),
    ("T-056, Couzo", "2026-09-27", "fact", WEB + "franciscouzo-square-packing-2026-09-27/facts/n-303.yaml"),
    ("T-092, Couzo", "2026-10-03", "fact", WEB + "franciscouzo-square-packing-2026-10-03/facts/n-303.yaml"),
    ("T-098, Daniel's exact optima (#375)", "2026-10-05", "cert",
     WEB + "evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-303.cert"),
    ("T-113, Chaoweeraprasit's SQUISH (#401)", "2026-10-07", "json", WEB + "squish-401-2026-10-07/facts/n-303.json.gz"),
    ("T-134, Couzo (#476)", "2026-10-09", "cert", WEB + "couzo-exact-certificates-2026-10-09/source/certificates/n303.cert"),
    ("T-136, Chaoweeraprasit's SQUISH (#481)", "2026-10-09", "fact", WEB + "squish-481-third-request-2026-10-09/facts/n-303.yaml.gz"),
    ("T-138, Polkovskyi's decimal poses (#470)", "2026-10-09", "fact", WEB + "mishapolk-decimal-poses-2026-10-09/facts/n-303.yaml.gz"),
    ("T-146, Daniel's regularized lists", "2026-10-10", "cert",
     WEB + "evand-regularized-2026-10-10/source/search/regularize/lists/certs/n-303.cert.gz"),
    ("#488, Couzo", "2026-10-10", "cert", WEB + "couzo-certificates-2026-10-10/source/certificates/n303.cert"),
    ("T-162, Ostashev (#562)", "2026-10-12", "sqcert", WEB + "dostashev-compositions-2026-10-12/source/records/n0303.sqcert"),
    ("#573, Polkovskyi", "2026-10-12", "fact", WEB + "mishapolk-exact-certificates-2026-10-12/facts/n-303.yaml.gz"),
    ("T-174, PingYou Ltd (PR #574)", "2026-10-13", "fact", WEB + "pingyou-pr574-certificates-2026-10-13/facts/n-303.yaml.gz"),
    ("#593, Polkovskyi", "2026-10-14", "fact", WEB + "mishapolk-records-2026-10-14/facts/n-303.yaml.gz"),
    ("T-186, Polkovskyi's KKT refinements (70a033f)", "2026-10-14", "fact",
     WEB + "mishapolk-kkt-refinements-2026-10-14/facts/n-303.yaml.gz"),
    ("T-230, Daniel (#728), the house", "2026-10-22", "cert",
     WEB + "evand-n303-2026-10-22/source/search/packer/candidates/s303_r303w0.cert"),
]


def show(repo: str, ref: str, path: str) -> bytes:
    data = subprocess.run(["git", "-C", repo, "show", f"{ref}:{path}"], check=True, capture_output=True).stdout
    return gzip.decompress(data) if path.endswith(".gz") else data


def ceil_places(value: Q, places: int) -> str:
    scaled = value * 10**places
    up = -((-scaled.numerator) // scaled.denominator)
    s = str(up).rjust(places + 1, "0")
    return s[:-places] + "." + s[-places:]


def floor_places(value: Q, places: int) -> str:
    scaled = value * 10**places
    down = scaled.numerator // scaled.denominator
    s = str(down).rjust(places + 1, "0")
    return s[:-places] + "." + s[-places:]


def terminating(value: Q) -> str | None:
    den = value.denominator
    k = 0
    while den % 2 == 0 or den % 5 == 0:
        den //= 2 if den % 2 == 0 else 5
        k += 1
    if den != 1:
        return None
    return floor_places(value, max(k, 1))


def sci(value: Q, digits: int = 12) -> str:
    if value == 0:
        return "0"
    d = Decimal(value.numerator) / Decimal(value.denominator)
    return f"{d:.{digits}e}"


def side_of(kind: str, raw: bytes) -> tuple[Q, str]:
    text = raw.decode("utf-8")
    if kind == "cert":
        for line in text.splitlines():
            if line.strip() and not line.startswith("#"):
                n, s = line.split()
                assert n == "303"
                return Q(s), "the certificate's header side"
    if kind == "sqcert":
        lines = [ln for ln in text.splitlines() if ln and not ln.startswith("#")]
        assert lines[0] == "n 303"
        assert lines[1].startswith("s ")
        return Q(lines[1][2:]), "the sqcert's s line"
    if kind == "json":
        d = json.loads(text)
        assert d["n"] == 303
        return Q(d["side"]), "the SQUISH fact's side"
    if kind == "fact":
        for line in text.splitlines():
            if line.startswith("  n: "):
                assert line.strip() == "n: 303"
            if line.startswith("  side: "):
                value = line[len("  side: ") :].strip().strip("'")
                return Q(value), "the derived fact's side" + (" (a decimal print)" if "." in value else "")
    if kind == "kingbird":
        lines = text.splitlines()
        for k, line in enumerate(lines):
            if line.strip() == "303":
                for follow in lines[k + 1 : k + 6]:
                    if "\\Nn{" in follow:
                        value = follow.split("\\Nn{", 1)[1].split("}", 1)[0]
                        return Q(value), "the catalogue's printed side at 303 (a decimal print)"
        raise ValueError("no entry at 303 in the catalogue capture")
    if kind == "casson":
        first = text.splitlines()[0]
        assert first.startswith("s: ")
        return Q(first[3:].strip()), "the retained packing's s: line (a decimal print)"
    raise ValueError(kind)


def case_bounds(repo: str, ref: str, n: int) -> dict:
    text = show(repo, ref, f"packing/frontier/n-{n}.md").decode()
    out = {}
    block = None
    for line in text.splitlines():
        if line.startswith("  reported_upper_bound:"):
            block = "reported"
        elif line.startswith("  verified_upper_bound:"):
            block = "verified"
        elif line.startswith("  ") and not line.startswith("    "):
            block = None
        if block and line.startswith("    value:"):
            out.setdefault(block, {})["value"] = line.split(":", 1)[1].strip().strip("'")
        if block and line.startswith("    exact_form:"):
            out.setdefault(block, {})["exact_form"] = line.split(":", 1)[1].strip().strip("'")
        if line.startswith("---") and out:
            break
    return out


def exact_of(entry: dict) -> tuple[Q | None, str]:
    form = entry.get("exact_form")
    if form and all(ch in "0123456789/" for ch in form):
        return Q(form), "exact_form"
    value = entry.get("value")
    if value:
        return Q(value), "value (a print)"
    return None, "none"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    data = Path(args.cert).read_bytes()
    header = [ln for ln in data.decode("ascii").splitlines() if not ln.startswith("#")][0]
    n_text, s_text = header.split(" ")
    assert n_text == "303"
    side = Q(s_text)
    rev = subprocess.run(["git", "-C", args.repo, "rev-parse", args.ref], check=True, capture_output=True, text=True).stdout.strip()
    out: dict = {
        "program": "margins_t238.py",
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_sha256": hashlib.sha256(data).hexdigest(),
        "ref": args.ref,
        "ref_commit": rev,
        "side": f"{side.numerator}/{side.denominator}",
        "side_terminating_decimal": terminating(side),
        "prints_rounded_up": {str(k): ceil_places(side, k) for k in (12, 16, 30)},
        "binary64_nearest": repr(float(side)),
        "binary64_nearest_exact": terminating(Q(float(side))),
    }
    issue_bound = Q("17.909762327476")
    out["issue_bound"] = {
        "printed": "17.909762327476",
        "is_side_rounded_up_at_12": ceil_places(side, 12) == "17.909762327476",
        "above_side_by": sci(issue_bound - side),
    }
    readme_expansion = "17.909762327475256427"
    out["issue_expansion"] = {
        "printed": readme_expansion + "...",
        "side_truncated_at_18": floor_places(side, 18),
        "agrees_with_side_to_places": next(
            (k - 1 for k in range(1, 30) if floor_places(side, k) != floor_places(Q(readme_expansion), k)), 29
        ),
        "agrees_with_binary64_nearest_to_places": next(
            (k - 1 for k in range(1, 30) if floor_places(Q(float(side)), k) != floor_places(Q(readme_expansion), k)), 29
        ),
    }
    rows = []
    for label, date, kind, where in REPORTS:
        if kind == "value":
            other, how = Q(where), "the grid side"
        elif kind == "print":
            other, how = Q(where), "the case record's priority note (a decimal print)"
        else:
            other, how = side_of(kind, show(args.repo, args.ref, where))
        rows.append(
            {
                "report": label,
                "date": date,
                "read_from": where if kind not in ("value", "print") else how,
                "how": how,
                "side": f"{other.numerator}/{other.denominator}" if len(str(other.denominator)) < 120 else None,
                "side_rounded_up_16": ceil_places(other, 16),
                "certificate_below_by": sci(other - side, 12),
                "certificate_below_by_exact": f"{(other - side).numerator}/{(other - side).denominator}"
                if len(str((other - side).denominator)) < 400
                else None,
                "below": side < other,
            }
        )
    out["reports_at_303"] = rows
    out["below_every_report_at_303"] = all(r["below"] for r in rows)
    t230 = next(r for r in rows if r["report"].startswith("T-230"))
    out["improvement_over_t230"] = t230["certificate_below_by"]
    later = []
    for m in range(304, 321):
        bounds = case_bounds(args.repo, args.ref, m)
        row = {"n": m}
        for which in ("reported", "verified"):
            if which in bounds:
                value, how = exact_of(bounds[which])
                row[which] = {
                    "value": bounds[which].get("value"),
                    "read_as": how,
                    "certificate_below_by": sci(value - side, 12) if value is not None else None,
                    "below": value is not None and side < value,
                }
        later.append(row)
    out["later_counts"] = later
    out["below_every_bound_304_to_320"] = all(
        all(r[w]["below"] for w in ("reported", "verified") if w in r) for r in later
    )
    margins = []
    for r in later:
        for w in ("reported", "verified"):
            if w in r and r[w]["certificate_below_by"] is not None:
                margins.append((Decimal(r[w]["certificate_below_by"]), r["n"], w))
    margins.sort()
    out["least_margin_304_to_320"] = {"margin": f"{margins[0][0]:.12e}", "n": margins[0][1], "bound": margins[0][2]}
    out["area_floor_from_321"] = f"{math.sqrt(321):.6f}"
    Path(args.out).write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("reports_at_303", "later_counts")}, indent=2))
    for r in rows:
        print(f"  {r['date']:10} {r['report'][:60]:60} {r['side_rounded_up_16']:>22} below by {r['certificate_below_by']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
