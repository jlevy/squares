"""What does the JSON's 303 'max_relative_center_change_exact' measure? (L70; decides nothing)

Compares Yim's 303 (546928a) with T-278 square by square under the identity, exactly:
for each choice of reference square r, the largest change of c_i - c_r over i, in the
L-infinity norm, the squared Euclidean norm and the L1 norm, and reports which (if any)
equals the JSON's exact value.

Usage: python -I l70_relative303.py --src SRC --repo REPO --out relative303.json
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import l70_check as C  # noqa: E402
import l70_identity as I  # noqa: E402
import l70_reader as R  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out", required=True)
    ns = ap.parse_args()
    src = Path(ns.src)
    meta = json.loads((src / "ac14112" / "packing-certificates.json").read_text())
    rg = next(c for c in meta["certificates"] if c["n"] == 303)["relative_geometry"]
    target = F(rg["max_relative_center_change_exact"])
    new = I.exact_poses(R.read_cert(src / "ac14112" / "n303.cert"))
    old = I.exact_poses(R.read_corners_yaml(Path(ns.repo) / "packing/resources/web/ozden-s303-upper-bound-2026-11-09/source/n-303-candidate.yaml"))
    disp = [(a[0] - b[0], a[1] - b[1]) for a, b in zip(new, old, strict=True)]
    hits = []
    best = {}
    for r, (rx, ry) in enumerate(disp):
        rel = [(dx - rx, dy - ry) for dx, dy in disp]
        linf = max(max(abs(x), abs(y)) for x, y in rel)
        l1 = max(abs(x) + abs(y) for x, y in rel)
        l2sq = max(x * x + y * y for x, y in rel)
        changed = sum(1 for x, y in rel if (x, y) != (0, 0))
        for name, v in (("Linf", linf), ("L1", l1), ("L2 squared", l2sq)):
            if v == target:
                hits.append({"reference_square": r + 1, "norm": name, "changed": changed})
        if r == 0:
            best = {"Linf": float(linf), "L1": float(l1), "L2": float(l2sq) ** 0.5, "changed": changed}
    out = {
        "program": "l70_relative303.py",
        "program_digests": C.file_digests(C.CHECKER_FILES + ("l70_identity.py", "l70_relative303.py")),
        "json_value": rg["max_relative_center_change_exact"],
        "json_float": float(target),
        "json_changed": rg["nonreference_relative_centers_changed"],
        "relative_to_square_1": best,
        "exact_matches": hits[:20],
    }
    Path(ns.out).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k != "program_digests"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
