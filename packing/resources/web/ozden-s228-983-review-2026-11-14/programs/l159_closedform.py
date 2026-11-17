"""Lane L159's closed-form check: is the side s(m) + k for a registry value?

Written after the findings were frozen, for the stage 4 review of issue #983; decides
nothing. It reads the reported upper bound printed at every count m below 228 in
packing/frontier/n-NNN.md and computes S - (s(m) + k) for k = 0, ..., 16, exactly in
the printed decimals. Nothing further is searched.

Usage: l159_closedform.py CERT.yaml TWIN.json FRONTIER_DIR OUT.json
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml  # noqa: E402

from l159_geom import sci  # noqa: E402
from l159_reader import read_paths  # noqa: E402


def main(argv: list[str]) -> int:
    cert, twin, frontier, out_path = (Path(a) for a in argv[1:5])
    w = read_paths(cert, twin)
    s = Fraction(*w.side)
    rows = []
    read = 0
    for m in range(1, 228):
        path = frontier / f"n-{m:03d}.md"
        if not path.exists():
            continue
        front = yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1])
        value = front["packing"]["reported_upper_bound"]["value"]
        read += 1
        v = Fraction(str(value))
        for k in range(17):
            rows.append((abs(s - (v + k)), m, k, str(value)))
    rows.sort()
    out = {
        "program": "l159_closedform.py",
        "counts_read": read,
        "within_1e-9": [[m, k, val] for d, m, k, val in rows if d < Fraction(1, 10**9)],
        "nearest": [[m, k, val, sci(d, 4)] for d, m, k, val in rows[:8]],
    }
    out_path.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("read", read, "| within 1e-9:", out["within_1e-9"], "| nearest:", out["nearest"][:4])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
