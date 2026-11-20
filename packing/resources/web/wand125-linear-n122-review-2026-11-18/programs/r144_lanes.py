"""Which lanes of the record would 563/50 raise at n = 122 to 127? Exact comparisons.

Usage: r144_lanes.py --frontier REPO/packing/frontier --out OUT.json

Reads, as data, the front matter of the case records n-122.md to n-127.md (their
reported and verified lower bounds, values and exact forms) and compares L = 563/50 with
each lane exactly: a decimal value as the rational it writes, an exact form p/q as
itself, the Karakus strip form 1/2 + sqrt(N - floor(sqrt(N)) + 1/4) by squaring, and the
other closed forms by rational bounds on their square roots. Written after the review's
controls plan (a disclosed addition); imports nothing from jlevy/squares or the source.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from fractions import Fraction as F

import yaml

L = F(563, 50)


def front_matter(path):
    text = open(path).read()
    parts = text.split("---\n")
    return yaml.safe_load(parts[1])["packing"]


def sqrt_bounds(q: F, digits: int = 60):
    N = q.numerator * 10 ** (2 * digits)
    r = math.isqrt(N * q.denominator)
    lo = F(r, q.denominator * 10**digits)
    hi = F(r + 1, q.denominator * 10**digits)
    return lo, hi


def compare(n: int, lane: dict) -> dict:
    v = F(str(lane["value"]))
    ef = str(lane.get("exact_form") or "")
    out = {"value": str(lane["value"]), "exact_form": ef, "source_key": lane.get("source_key"), "evidence": lane.get("evidence")}
    out["L_above_value"] = L > v
    m = re.fullmatch(r"1/2 \+ sqrt\((\d+) - floor\(sqrt\((\d+)\)\) \+ 1/4\)", ef)
    if re.fullmatch(r"\d+/\d+", ef):
        out["L_above_exact"] = L > F(ef)
        out["exact_method"] = "rational"
    elif m:
        N = int(m.group(1))
        k = math.isqrt(N)
        # L > 1/2 + sqrt(N - k + 1/4)  iff  (L - 1/2)^2 > N - k + 1/4 (both sides positive)
        out["L_above_exact"] = (L - F(1, 2)) ** 2 > N - k + F(1, 4)
        out["exact_method"] = "Karakus strip form, by squaring"
    else:
        out["L_above_exact"] = None
        out["exact_method"] = "none (decimal value only)"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frontier", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rows = []
    for n in range(122, 128):
        pk = front_matter(os.path.join(a.frontier, f"n-{n:03d}.md"))
        rep = compare(n, pk["reported_lower_bound"])
        ver = compare(n, pk["verified_lower_bound"])
        rows.append({"n": n, "reported_lower": rep, "verified_lower": ver, "raises_reported": rep["L_above_value"], "raises_verified": ver["L_above_value"]})
    # Green's G_11 and Nagamochi's 1 + sqrt(105), as the claim states them
    lo2, hi2 = sqrt_bounds(F(2))
    lo22, hi22 = sqrt_bounds(F(22))
    green = (F(489, 61) + 2 * lo2 + F(5, 61) * lo22, F(489, 61) + 2 * hi2 + F(5, 61) * hi22)
    res = {
        "program": "r144_lanes.py",
        "L": "563/50",
        "rows": rows,
        "raises_reported_at": [r["n"] for r in rows if r["raises_reported"]],
        "raises_verified_at": [r["n"] for r in rows if r["raises_verified"]],
        "green_G11_decimal": f"{float(green[0]):.12f}",
        "L_minus_green_lower": f"{float(L - green[1]):.12f}",
        "L_above_1_plus_sqrt105": (L - 1) ** 2 > 105,
        "L_minus_1_plus_sqrt105": f"{float(L - 1 - sqrt_bounds(F(105))[1]):.12f}",
    }
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1)
        f.write("\n")
    print("raises reported at", res["raises_reported_at"], "raises verified at", res["raises_verified_at"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
