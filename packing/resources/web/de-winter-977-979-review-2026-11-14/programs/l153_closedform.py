"""Lane L153, after the freeze: is a side s(m) + k for a registry value s(m)?

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review. It decides nothing about the bounds.

It reads the reported upper bound of every case record `frontier/n-NNN.md` below the
largest count asked (the exact form where it is rational, else the printed value), and
for each certificate side S computes S - (s(m) + k) for k = 0 .. 16; it lists the
nearest few and every one within 1e-9.

Usage: l153_closedform.py FRONTIER_DIR OUT.json N=CERT.json [N=CERT.json ...]
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_reader as reader  # noqa: E402
from l153_check import sci  # noqa: E402

RATIONAL = re.compile(r"-?\d+(/\d+)?")


def registry(frontier: Path, below: int) -> dict[int, tuple[Fraction, str]]:
    out = {}
    for m in range(1, below):
        path = frontier / f"n-{m:03d}.md"
        if not path.exists():
            continue
        front = yaml.safe_load(path.read_text().split("---")[1])
        rub = front["packing"]["reported_upper_bound"]
        exact = rub.get("exact_form")
        if isinstance(exact, str) and RATIONAL.fullmatch(exact):
            out[m] = (Fraction(exact), "exact")
        else:
            out[m] = (Fraction(str(rub["value"])), "printed")
    return out


def main(argv: list[str]) -> int:
    frontier = Path(argv[1])
    out_path = Path(argv[2])
    specs = [(int(a.split("=", 1)[0]), a.split("=", 1)[1]) for a in argv[3:]]
    reg = registry(frontier, max(n for n, _ in specs))
    out: dict = {"program": "l153_closedform.py", "registry_counts": len(reg), "sides": {}}
    for n, path in specs:
        side = Fraction(*reader.read(path)["side"])
        rows = []
        for m, (value, kind) in reg.items():
            if m >= n:
                continue
            for k in range(17):
                rows.append((abs(side - value - k), m, k, kind, side - value - k))
        rows.sort()
        out["sides"][str(n)] = {
            "nearest": [
                {"m": m, "k": k, "kind": kind, "difference": sci(d, 6)} for _, m, k, kind, d in rows[:6]
            ],
            "within_1e-9": [{"m": m, "k": k} for a, m, k, _, _ in rows if a < Fraction(1, 10**9)],
        }
        print(n, out["sides"][str(n)]["nearest"][:3], "within 1e-9:", out["sides"][str(n)]["within_1e-9"])
    out_path.write_text(json.dumps(out, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
