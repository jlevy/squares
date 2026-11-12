"""Test the issue's lineage counts against T-290. Written and run after the freeze.

Lane L127, clean room; decides nothing. Usage:

    python -I -B l127_lineage.py CERT.yaml TWIN.json HOUSE.yaml ISSUE.json OUT.json

The issue says: "Squares matched by assignment up to the symmetries of the square: 261 of
269 centres move by more than 1e-3, 137 by more than 0.05 (largest 1.879); 121 squares are
re-tilted by more than 1° (largest 44.4°)". This program applies each of the box's eight
symmetries to the house packing, anchors its box against this certificate's box at five
places (the four corners and the centre), assigns squares by least summed move and by
least summed squared move (scipy's linear_sum_assignment, binary64), and reports the five
numbers for each of the 80 combinations, and which reproduce the issue's at its precision.
A re-tilt is the turn between assigned squares folded to (-45, 45] degrees.
"""

from __future__ import annotations

import json
import math
import re
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from scipy.optimize import linear_sum_assignment

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_reader as rd  # noqa: E402


def fold(a: float) -> float:
    r = math.fmod(a + 45.0, 90.0)
    if r <= 0:
        r += 90.0
    return r - 45.0


def certificate_poses(doc: dict[str, Any]) -> list[tuple[float, float, float]]:
    out = []
    for c in doc["squares"]:
        p = [(F(*x), F(*y)) for x, y in c]
        cx = float((p[0][0] + p[2][0]) / 2)
        cy = float((p[0][1] + p[2][1]) / 2)
        ang = math.degrees(math.atan2(float(p[1][1] - p[0][1]), float(p[1][0] - p[0][0])))
        out.append((cx, cy, fold(ang)))
    return out


def house_poses(text: str) -> tuple[float, list[tuple[float, float, float]]]:
    w = yaml.safe_load(text)["witness"]
    assert w["representation"] == "center-basis"
    side = float(F(str(w["side"])))
    out = []
    for s in w["squares"]:
        cx, cy = (float(F(str(v))) for v in s["center"])
        c, sn = (float(F(str(v))) for v in s["basis"])
        out.append((cx, cy, fold(math.degrees(math.atan2(sn, c)))))
    return side, out


SYMS = {
    "identity": (lambda x, y, L: (x, y), 1),
    "turn 90": (lambda x, y, L: (L - y, x), 1),
    "turn 180": (lambda x, y, L: (L - x, L - y), 1),
    "turn 270": (lambda x, y, L: (y, L - x), 1),
    "reflect left-right": (lambda x, y, L: (L - x, y), -1),
    "reflect top-bottom": (lambda x, y, L: (x, L - y), -1),
    "transpose": (lambda x, y, L: (y, x), -1),
    "anti-transpose": (lambda x, y, L: (L - y, L - x), -1),
}


def main(argv: list[str]) -> int:
    cert, twin, house, issue, outp = (Path(a) for a in argv[1:6])
    doc = rd.read_certificate(cert.read_text(encoding="utf-8"), twin.read_text(encoding="utf-8"))
    new = certificate_poses(doc)
    s_new = float(F(*doc["side"]))
    L, old = house_poses(house.read_text(encoding="utf-8"))
    body = json.loads(issue.read_text(encoding="utf-8"))["issue"]["body"]
    m = re.search(
        r"(\d+) of 269 centres move by more than 1e-3, (\d+) by more than 0\.05 \(largest ([0-9.]+)\); "
        r"(\d+) squares are re-tilted by more than 1° \(largest ([0-9.]+)°\)",
        body,
    )
    assert m is not None
    want = (int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4)), m.group(5))
    dl = s_new - L
    anchors = {
        "lower-left": (0.0, 0.0),
        "lower-right": (dl, 0.0),
        "upper-left": (0.0, dl),
        "upper-right": (dl, dl),
        "centre": (dl / 2, dl / 2),
    }
    nx = np.array([p[0] for p in new])
    ny = np.array([p[1] for p in new])
    na = [p[2] for p in new]
    rows: list[dict[str, Any]] = []
    for sname, (fn, sense) in SYMS.items():
        moved = [fn(x, y, L) + (sense * a,) for x, y, a in old]
        for aname, (ax, ay) in anchors.items():
            ox = np.array([p[0] + ax for p in moved])
            oy = np.array([p[1] + ay for p in moved])
            d = np.hypot(nx[:, None] - ox[None, :], ny[:, None] - oy[None, :])
            for crit, cost in (("least summed move", d), ("least summed squared move", d * d)):
                r, c = linear_sum_assignment(cost)
                mv = d[r, c]
                rt = [abs(fold(na[i] - moved[j][2])) for i, j in zip(r, c, strict=True)]
                row = {
                    "symmetry": sname,
                    "anchor": aname,
                    "assignment": crit,
                    "beyond_1e-3": int((mv > 1e-3).sum()),
                    "beyond_0.05": int((mv > 0.05).sum()),
                    "largest_move": round(float(mv.max()), 4),
                    "retilted_beyond_1": sum(1 for t in rt if t > 1),
                    "largest_retilt": round(max(rt), 2),
                    "summed_move": round(float(mv.sum()), 3),
                }
                got = (
                    row["beyond_1e-3"],
                    row["beyond_0.05"],
                    f"{float(mv.max()):.3f}",
                    row["retilted_beyond_1"],
                    f"{max(rt):.1f}",
                )
                row["matches_issue"] = got == want
                row["matching_fields"] = sum(1 for a, b in zip(got, want, strict=True) if a == b)
                rows.append(row)
    best = min(rows, key=lambda r: r["summed_move"])
    out = {
        "program": "l127_lineage.py",
        "issue_numbers": {"beyond_1e-3": want[0], "beyond_0.05": want[1], "largest_move": want[2], "retilted_beyond_1": want[3], "largest_retilt": want[4]},
        "house_side": L,
        "tilted_beyond_0.5": {"certificate": sum(1 for a in na if abs(a) > 0.5), "house": sum(1 for p in old if abs(p[2]) > 0.5)},
        "exact_matches": [r for r in rows if r["matches_issue"]],
        "closest": sorted(rows, key=lambda r: -r["matching_fields"])[:6],
        "least_summed_move_overall": best,
        "rows": rows,
    }
    outp.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("issue_numbers", "tilted_beyond_0.5", "exact_matches", "closest", "least_summed_move_overall")}, indent=1)[:5000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
