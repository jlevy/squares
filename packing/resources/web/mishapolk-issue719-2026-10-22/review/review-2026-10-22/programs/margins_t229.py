#!/usr/bin/env python3
"""Exact margins of T-229's two sides in report order, at later counts, and their prints.

Standard library only; decides no certificate. For each of #719's two sides it computes:

* the margin below every earlier report at the count, in report order: exactly where a
  retained file states the report's side (a certificate's header, a fact's side), and
  conservatively where only a print exists (the print less one unit in its last place);
* the margin below the house when #719 was reported, exactly;
* the margin below the reported and verified upper bounds of every later count through
  324 on main (deleting squares from a packing of m gives one of n < m, so a side is new
  only if it is below every bound at every later count), exactly where the case record
  states a rational exact form and from the print otherwise;
* the side's exact decimal expansion, its ceilings at 12 and 16 places, its binary64
  value at 16 places, and how the issue's printed side and the packet's ceiling stand
  to it.

Usage: margins_t229.py REPO DATA PIN OUT.json
    REPO  the repository checkout whose packets are read (the worktree at 56d6d0d6d)
    DATA  this lane's data directory: main-cases/ (main's case records 105 to 324, with
          MAIN_COMMIT) and couzo/ (Couzo's watched-repository files, as data)
    PIN   the source's certificates directory at 12fc466, read as data, or - to skip the
          two checks that need it (the claimed files' headers, and the source's other files)
"""

import gzip
import json
import os
import re
import sys
from decimal import Decimal
from fractions import Fraction

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

RAT = re.compile(r"-?[0-9]+(?:/[0-9]+)?\Z")
DEC = re.compile(r"-?[0-9]+\.[0-9]+\Z")

PACKET = "packing/resources/web/mishapolk-issue719-2026-10-22"
W = "packing/resources/web"

# Each earlier report at the count, in report order: (label, reported, kind, value or path).
# kind "print": a printed decimal; "repo": a retained file in REPO; "data": DATA/couzo.
EARLIER = {
    105: [
        ("Kingbird catalogue", "before 2026-08-22", "print", "10.80789399144854"),
        ("Griffin Casson, griffcass/square-packing 82661bc", "2026-09-24T04:45:20Z", "print",
         "10.80758853319602153"),
        ("Francisco Couzo, franciscouzo/square-packing 3bfc47e", "2026-09-26T03:27:13Z", "print",
         "10.807588532111675"),
        ("Francisco Couzo, 27 September ceiling", "2026-09-27", "print", "10.806077865540567"),
        ("T-117, Rehwaldt and Couzo refinements", "2026-10-07", "print",
         "10.80607786551970463257490535044771520398745274"),
        ("T-125, Ryan Xu", "2026-10-08", "print", "10.7906765754107907"),
        ("T-128", "before 2026-10-13", "print", "10.7906182681071446"),
        ("T-138", "before 2026-10-13", "print", "10.789303783751"),
        ("T-130, Couzo's refinement of Xu's packing", "2026-10-08", "repo",
         f"{W}/couzo-followup-refinements-2026-10-08/facts/n-105.yaml"),
        ("T-170, PingYou Ltd #568", "2026-10-12", "repo",
         f"{W}/pingyou-n105-refinement-2026-10-12/facts/n-105.yaml.gz"),
        ("T-174, PingYou Ltd PR #574, the house when #719 was reported", "2026-10-13", "repo",
         f"{W}/pingyou-pr574-certificates-2026-10-13/facts/n-105.yaml.gz"),
        ("T-183, Polkovskyi #593", "2026-10-14T01:40Z", "repo",
         f"{W}/mishapolk-records-2026-10-14/facts/n-105.yaml.gz"),
        ("Couzo 4e4c8ce certificates/best/n105.cert", "2026-10-15T00:31:53Z", "data",
         "couzo/4e4c8ce-certificates-best-n105.cert"),
        ("Couzo 4e4c8ce certificates/n105.cert", "2026-10-15T00:31:53Z", "data",
         "couzo/4e4c8ce-certificates-n105.cert"),
        ("Couzo 5a299b4 certificates/best/n105.cert", "2026-10-21T22:56:37Z (pushed)", "data",
         "couzo/5a299b4-certificates-best-n105.cert"),
    ],
    204: [
        ("Kingbird catalogue", "before 2026-08-22", "print", "14.82287565553229"),
        ("T-162, Daniil Ostashev #562", "2026-10-12", "repo",
         f"{W}/dostashev-compositions-2026-10-12/source/records/n0204.sqcert"),
        ("PingYou Ltd PR #574", "2026-10-13", "repo",
         f"{W}/pingyou-pr574-certificates-2026-10-13/facts/n-204.yaml.gz"),
        ("T-183, Polkovskyi #593", "2026-10-14T01:40Z", "repo",
         f"{W}/mishapolk-records-2026-10-14/facts/n-204.yaml.gz"),
        ("T-186, Polkovskyi 70a033f KKT refinement", "2026-10-14T16:11:31Z", "repo",
         f"{W}/mishapolk-kkt-refinements-2026-10-14/facts/n-204.yaml.gz"),
        ("Couzo 4e4c8ce certificates/best/n204.cert", "2026-10-15T00:31:53Z", "data",
         "couzo/4e4c8ce-certificates-best-n204.cert"),
        ("Couzo 4e4c8ce certificates/n204.cert", "2026-10-15T00:31:53Z", "data",
         "couzo/4e4c8ce-certificates-n204.cert"),
        ("Evan Daniel #639 (the ledger's print, rounded up at 12)", "2026-10-16T03:37:13Z",
         "print", "14.808663234387"),
        ("T-226, Couzo #670", "2026-10-17T18:05:06Z", "repo",
         f"{W}/couzo-issue670-2026-10-17/source/certificates/n204.cert"),
        ("T-228, Couzo #675", "2026-10-18T06:02:11Z", "repo",
         f"{W}/couzo-issue675-2026-10-18/source/certificates/best/n204.cert"),
        ("T-223, Couzo #678", "2026-10-18T23:23:19Z", "repo",
         f"{W}/couzo-issue678-2026-10-18/source/certificates/best/n204.cert"),
        ("T-225, Evan Daniel evand/square-packing@0075967, the house when #719 was reported",
         "2026-10-20T02:36:12Z", "repo",
         f"{W}/evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-204.cert.gz"),
        ("Couzo 5a299b4 certificates/best/n204.cert", "2026-10-21T22:56:37Z (pushed)", "data",
         "couzo/5a299b4-certificates-best-n204.cert"),
    ],
}
HOUSE = {105: "T-174", 204: "T-225"}
ISSUE_PRINT = {105: ("10.7893037837429748", "10.7893037837481582"),
               204: ("14.8086428305278961", "14.8086428405914940")}
CLAIM_MARGINS = {105: {"T-174": "5.18e-12", "T-183": "5.18e-12"},
                 204: {"T-225": "1.006e-8", "T-223": "1.145e-8", "T-228": "1.537e-6",
                       "T-226": "1.587e-6", "T-186": "2.040e-5"}}
OTHER_FILES = {105: "n105.cert", 204: "n204.cert"}


def text(path):
    raw = open(path, "rb").read()
    if raw[:2] == b"\x1f\x8b":
        raw = gzip.decompress(raw)
    return raw.decode("utf-8")


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "'\"":
        return v[1:-1]
    return v


def frac(tok):
    if not RAT.match(tok):
        raise ValueError(f"not a rational: {tok[:60]!r}")
    return Fraction(tok)


def side_of(path):
    """The side a certificate, sqcert or witness fact states, exactly."""
    t = text(path)
    if "\nwitness:" in "\n" + t:
        for line in t.split("\n"):
            if line.startswith("  side: "):
                return frac(unquote(line[len("  side: "):])), "witness side"
        raise ValueError("no side")
    lines = [ln.strip() for ln in t.split("\n") if ln.strip() and not ln.strip().startswith("#")]
    first = lines[0].split()
    if first[0] == "n" and lines[1].split()[0] == "s":
        return frac(lines[1].split()[1]), "sqcert s line"
    return frac(first[1]), "certificate header"


def low_of_print(p):
    """The least value a decimal print may stand for: the print less one unit in its last place."""
    places = len(p.partition(".")[2])
    return Fraction(Decimal(p)) - Fraction(1, 10**places), places


def ceil_places(x, places):
    q = 10**places
    v = -((-x.numerator * q) // x.denominator)
    s = str(v).rjust(places + 1, "0")
    return s[:-places] + "." + s[-places:]


def exact_decimal(x):
    d = x.denominator
    two = five = 0
    while d % 2 == 0:
        d //= 2
        two += 1
    while d % 5 == 0:
        d //= 5
        five += 1
    if d != 1:
        return None
    places = max(two, five)
    v = x.numerator * 10**places // x.denominator
    s = str(v).rjust(places + 1, "0")
    return s[:-places] + "." + s[-places:]


def sci(x):
    return f"{float(x):.10e}"


def case_bounds(path):
    """The reported and verified upper bounds of a case record: value and exact form."""
    out = {}
    lane = None
    inside = False
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line == "---":
            if inside:
                break
            inside = True
            continue
        m = re.match(r"  ([a-z_]+):\s*$", line)
        if m:
            lane = m.group(1) if m.group(1) in ("reported_upper_bound", "verified_upper_bound") else None
            continue
        if re.match(r"  [a-z_]+:", line):
            lane = None
            continue
        if lane:
            m = re.match(r"    (value|exact_form): (.*)$", line)
            if m:
                out.setdefault(lane, {})[m.group(1)] = unquote(m.group(2))
    return out


def main(argv):
    repo, data, pin, out_path = argv
    sides = {}
    for n in (105, 204):
        sides[n] = side_of(os.path.join(repo, PACKET, f"facts/n-{n:03d}.yaml.gz"))[0]
        if pin != "-":
            assert side_of(os.path.join(pin, f"n-{n}.cert"))[0] == sides[n]
    report = {"main": open(os.path.join(data, "main-cases/MAIN_COMMIT")).read().strip(),
              "counts": []}
    ok_all = True
    for n in (105, 204):
        S = sides[n]
        entry = {"n": n, "side": f"{S.numerator}/{S.denominator}", "earlier": [],
                 "later_counts": {}, "prints": {}}
        found = {}
        for label, when, kind, val in EARLIER[n]:
            row = {"report": label, "reported": when, "kind": kind}
            if kind == "print":
                low, places = low_of_print(val)
                row.update({"print": val, "margin_at_least": sci(low - S), "below": low > S})
            else:
                path = os.path.join(repo if kind == "repo" else data, val)
                other, how = side_of(path)
                d = other - S
                row.update({"source": val, "read_from": how,
                            "side": f"{other.numerator}/{other.denominator}" if len(str(other.denominator)) < 60
                            else f"{str(other.numerator)[:30]}…/{str(other.denominator)[:30]}… ({len(str(other.numerator))} and {len(str(other.denominator))} digits)",
                            "margin": sci(d), "margin_exact": f"{d.numerator}/{d.denominator}" if len(str(d.denominator)) < 120 else None,
                            "below": d > 0})
                tag = label.split(",")[0]
                found[tag] = (other, d)
            ok_all = ok_all and row["below"]
            entry["earlier"].append(row)
        # The house on main, from the case record, equals the house's retained file.
        cb = case_bounds(os.path.join(data, f"main-cases/n-{n:03d}.md"))
        house_main = frac(cb["verified_upper_bound"]["exact_form"])
        hside, hmargin = found[HOUSE[n]]
        entry["house"] = {"result": HOUSE[n], "case_record_exact_form_equals_file": house_main == hside,
                          "reported_lane_equals_verified": cb["reported_upper_bound"]["exact_form"]
                          == cb["verified_upper_bound"]["exact_form"],
                          "margin": sci(hmargin), "margin_exact": f"{hmargin.numerator}/{hmargin.denominator}"
                          if len(str(hmargin.denominator)) < 120 else None}
        # The claim's and notes' printed margins, each a truncation of the exact margin.
        checks = {}
        for tag, printed in CLAIM_MARGINS[n].items():
            d = found[tag][1]
            p = Fraction(Decimal(printed))
            mant = printed.split("e")[0]
            unit = Fraction(Decimal("1" + "e" + printed.split("e")[1])) / 10 ** len(mant.partition(".")[2])
            checks[tag] = {"printed": printed, "exact": sci(d), "printed_at_most_exact": p <= d,
                           "within_one_unit": d - p < unit}
        entry["printed_margins"] = checks
        # Every later count through 324 on main.
        least = None
        decided = 0
        for m in range(n + 1, 325):
            cb = case_bounds(os.path.join(data, f"main-cases/n-{m:03d}.md"))
            for lane, v in cb.items():
                ef = v.get("exact_form", "")
                if ef and RAT.match(ef):
                    margin, how = frac(ef) - S, "exact"
                elif v.get("value") and DEC.match(v["value"]):
                    low, _ = low_of_print(v["value"])
                    margin, how = low - S, "print"
                elif v.get("value") and RAT.match(v["value"]):
                    margin, how = frac(v["value"]) - S, "exact"
                else:
                    raise ValueError(f"n={m} {lane}: no usable bound")
                decided += 1
                if margin <= 0:
                    ok_all = False
                if least is None or margin < least[0]:
                    least = (margin, m, lane, how)
        entry["later_counts"] = {"bounds_decided": decided, "all_below": least[0] > 0,
                                 "least_margin": sci(least[0]), "at": least[1], "lane": least[2],
                                 "how": least[3]}
        # Prints and rounding.
        issue_print, issue_baseline = ISSUE_PRINT[n]
        packet_ceiling = None
        for r in json.load(open(os.path.join(repo, PACKET, "acquisition/claims.json")))["results"]:
            if r["n"] == n:
                packet_ceiling = r["ceiling"]
                offered = r["offered_side"]
        entry["prints"] = {
            "exact_decimal": exact_decimal(S),
            "ceiling_12": ceil_places(S, 12), "ceiling_16": ceil_places(S, 16),
            "binary64_at_16": f"{float(S):.16f}",
            "issue_print": issue_print,
            "issue_print_is_binary64_at_16": issue_print == f"{float(S):.16f}",
            "issue_print_below_exact_side": Fraction(Decimal(issue_print)) < S,
            "packet_ceiling": packet_ceiling, "packet_ceiling_is_ceiling_16": packet_ceiling == ceil_places(S, 16),
            "offered_side": offered, "offered_side_is_exact": Fraction(Decimal(offered)) == S,
            "issue_baseline": issue_baseline,
            "issue_baseline_minus_house": sci(Fraction(Decimal(issue_baseline)) - hside),
        }
        if pin != "-":
            other, _ = side_of(os.path.join(pin, OTHER_FILES[n]))
            entry["source_other_file"] = {"file": OTHER_FILES[n],
                                          "side_minus_claimed": sci(other - S)}
        report["counts"].append(entry)
        print(f"n={n}: side {float(S):.16f}; below every earlier report: "
              f"{all(r['below'] for r in entry['earlier'])} ({len(entry['earlier'])}); "
              f"house {HOUSE[n]} by {entry['house']['margin']}; later counts all below: "
              f"{entry['later_counts']['all_below']} (least {entry['later_counts']['least_margin']} "
              f"at {entry['later_counts']['at']}, {entry['later_counts']['bounds_decided']} bounds)")
        for r in entry["earlier"]:
            print(f"    {r['reported']:<32} {r['report'][:70]:<70} "
                  f"{r.get('margin', r.get('margin_at_least')):>18} {'below' if r['below'] else 'NOT BELOW'}")
        print(f"    prints: {json.dumps(entry['prints'])}")
        print(f"    printed margins: {json.dumps(checks)}")
        if "source_other_file" in entry:
            print(f"    other file {OTHER_FILES[n]}: side - claimed = "
                  f"{entry['source_other_file']['side_minus_claimed']}")
    report["all_as_claimed"] = ok_all
    with open(out_path, "w") as fh:
        json.dump(report, fh, indent=1)
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
