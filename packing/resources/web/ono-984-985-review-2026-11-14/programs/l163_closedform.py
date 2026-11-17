"""Lane L163 closed forms, after the freeze: is a side s(m) + k, and does an L step carry it?

Usage: l163_closedform.py FRONTIER_DIR OUT.json LABEL=CERT.json [LABEL=CERT.json ...]

For each certificate's side S at count n it computes S - (s(m) + k) for every count m
below n with a reported upper bound in `FRONTIER_DIR/n-NNN.md` and every k from 0 to 16,
and lists any within 1e-9 and the nearest three. It then takes the standard L step of
width k = 1..4 (k rows of floor(S + k) squares above, k columns of floor(S) beside) to the
count n + k floor(S + k) + k floor(S) at side S + k, and compares it with that count's
reported value where the record has a case. Decides nothing.
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys
from decimal import Decimal
from fractions import Fraction as F
from math import floor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import l163_geom as geom  # noqa: E402
import yaml  # noqa: E402
from l163_reader import read_json  # noqa: E402


def reported(frontier: str) -> dict[int, F]:
    out: dict[int, F] = {}
    for path in glob.glob(os.path.join(frontier, "n-*.md")):
        m = re.search(r"n-(\d+)\.md$", path)
        if not m:
            continue
        text = open(path, encoding="utf-8").read()
        try:
            pk = yaml.safe_load(text.split("---", 2)[1])["packing"]
            v = pk["reported_upper_bound"]["value"]
        except (KeyError, TypeError, IndexError, yaml.YAMLError):
            continue
        if v is not None:
            out[int(m.group(1))] = F(Decimal(str(v)))
    return out


def main() -> None:
    frontier, out = sys.argv[1:3]
    rep = reported(frontier)
    rec: dict[str, object] = {"lane": "L163", "program": "l163_closedform.py", "counts_read": len(rep), "largest_count": max(rep)}
    for spec in sys.argv[3:]:
        label, path = spec.split("=", 1)
        c = read_json(path)
        s = F(*c.side)
        n = c.n
        diffs = [(abs(s - (v + k)), m, k, s - (v + k)) for m, v in rep.items() if m < n for k in range(17)]
        diffs.sort()
        within = [[m, k, geom.sci(d)] for a, m, k, d in diffs if a < F(1, 10**9)]
        nearest = [[m, k, geom.sci(d)] for _, m, k, d in diffs[:3]]
        steps = []
        for k in range(1, 5):
            add = k * floor(s + k) + k * floor(s)
            n2 = n + add
            entry: dict[str, object] = {"k": k, "count": n2, "side": geom.ceil_places(s + k, 12)}
            if n2 in rep:
                entry["reported"] = str(Decimal(rep[n2].numerator) / Decimal(rep[n2].denominator))
                entry["side_less_reported_sci"] = geom.sci(s + k - rep[n2])
                entry["improves"] = s + k < rep[n2]
            else:
                entry["reported"] = None
            steps.append(entry)
        rec[label] = {"n": n, "within_1e-9": within, "nearest_three": nearest, "l_steps": steps}
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(rec, fh, indent=1)
    print(json.dumps(rec)[:2000])


if __name__ == "__main__":
    main()
