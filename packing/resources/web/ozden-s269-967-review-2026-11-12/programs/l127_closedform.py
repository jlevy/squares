"""Does the side sit at a registry value plus an integer, s(m) + k? Written after the freeze.

Lane L127, clean room; decides nothing. Usage:

    python -I -B l127_closedform.py CERT.yaml TWIN.json FRONTIER_DIR OUT.json

Reads `reported_upper_bound.value` from each `n-NNN.md` in FRONTIER_DIR (main's register)
and, for every count m < 269 and integer k from 0 to 16, the gap S - (s(m) + k). The
review of #959 found that certificate's side at s(70) + 5; this asks the same of 269 and
no more: a hit closer than 1e-9 would be reported for an exact check.
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_reader as rd  # noqa: E402


def main(argv: list[str]) -> int:
    cert, twin, fdir, outp = Path(argv[1]), Path(argv[2]), Path(argv[3]), Path(argv[4])
    doc = rd.read_certificate(cert.read_text(encoding="utf-8"), twin.read_text(encoding="utf-8"))
    s = F(*doc["side"])
    vals: dict[int, F] = {}
    for p in sorted(fdir.glob("n-[0-9][0-9][0-9].md")):
        m = int(p.stem[2:])
        t = p.read_text(encoding="utf-8")
        mm = re.search(r"reported_upper_bound:\n\s+value: '?([0-9]+(?:\.[0-9]+)?)'?", t)
        if mm and m < 269:
            vals[m] = F(mm.group(1))
    hits = []
    for m, v in vals.items():
        for k in range(17):
            d = s - (v + k)
            hits.append((abs(d), m, k, d))
    hits.sort()
    out = {
        "program": "l127_closedform.py",
        "values_read": len(vals),
        "counts_range": [min(vals), max(vals)],
        "below_1e-9": [{"m": m, "k": k, "gap": f"{float(d):.3e}"} for a, m, k, d in hits if a < F(1, 10**9)],
        "nearest_ten": [{"m": m, "k": k, "s(m)": f"{float(vals[m]):.15f}", "gap": f"{float(d):.3e}"} for _, m, k, d in hits[:10]],
        "side_minus_16": f"{float(s - 16):.15f}",
    }
    outp.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
