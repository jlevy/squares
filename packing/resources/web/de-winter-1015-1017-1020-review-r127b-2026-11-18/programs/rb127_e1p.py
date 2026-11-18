"""Control E1p with its rule restated, after the freeze (lane r127b-1118).

Written after the checker's freeze, when E1p at #1020 came out other than stated. The
frozen rule said that with the side lowered to X - 1e-40, X the packing's extent,
exactly the squares at the wall of the larger extent cross. That holds only where the
other extent falls short of X by more than 1e-40; at #1020 the height falls short of
the width by less than that, so squares at the top wall cross as well. The restated rule
is the side rule applied to E1c's packing: exactly the squares whose right or top
clearance in E1c's packing is below 1e-40 cross.

Usage, as rb127_controls.py's modes:

    python -I -B rb127_e1p.py pair LABEL EXACT.json WITNESS.yaml OUT.json
    python -I -B rb127_e1p.py house LABEL CANDIDATE.yaml OUT.json

It imports the frozen modules unchanged and decides E1p's packing again by both methods.
It is a restated control, not one stated in advance, and is reported as such.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rb127_controls as CT  # noqa: E402
import rb127_fmt as F  # noqa: E402


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "pair" and len(argv) == 6:
        label, jp, cp, out = argv[2:6]
        run = CT.Runner(label, "pair", Path(jp).read_bytes(), Path(cp).read_bytes(), "0.0")
    elif len(argv) >= 2 and argv[1] == "house" and len(argv) == 5:
        label, cp, out = argv[2:5]
        run = CT.Runner(label, "house", None, Path(cp).read_bytes(), "0.0")
    else:
        print(__doc__)
        return 2
    c = run.cert
    Lmin = min(cl[0] for cl in c.clear)
    Bmin = min(cl[1] for cl in c.clear)
    lo_x = min(c.cen[k][0] - c.h[k] for k in range(c.n))
    lo_y = min(c.cen[k][1] - c.h[k] for k in range(c.n))
    width = max(c.cen[k][0] + c.h[k] for k in range(c.n)) - lo_x
    height = max(c.cen[k][1] + c.h[k] for k in range(c.n)) - lo_y
    X = max(width, height)
    rows = [(CT.pq(CT.fr(r[0]) - Lmin), CT.pq(CT.fr(r[1]) - Bmin), r[2], r[3]) for r in c.rows]
    tiny = Fr(1, 10**40)
    dec = run.decide_rows(rows, CT.pq(X - tiny), squares=list(range(c.n)), pairs=[])
    _, cross = CT.wall_sets(dec)
    got = sorted(set(cross["right"]) | set(cross["top"]))
    right = {k + 1: X - (c.cen[k][0] - Lmin) - c.h[k] for k in range(c.n)}
    top = {k + 1: X - (c.cen[k][1] - Bmin) - c.h[k] for k in range(c.n)}
    restated = sorted(k for k in right if right[k] < tiny or top[k] < tiny)
    frozen_rule = sorted(k for k in right if (width == X and right[k] == 0) or (height == X and top[k] == 0))
    rec = {
        "program": "rb127_e1p.py",
        "label": label,
        "verdict": dec["verdict"],
        "width_less_height_sci": F.sci(width - height, 8),
        "crossing": got,
        "restated_rule": restated,
        "frozen_rule": frozen_rule,
        "as_restated": dec["verdict"] == "REFUSE" and got == restated and CT.classes_agree(dec),
        "as_frozen": dec["verdict"] == "REFUSE" and got == frozen_rule,
        "least_E1c_top_clearance_sci": F.sci(min(top.values()), 8),
        "least_E1c_right_clearance_sci": F.sci(min(right.values()), 8),
    }
    Path(out).write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(label, rec["verdict"], "as restated:", rec["as_restated"], "as frozen:", rec["as_frozen"],
          len(got), "crossing")
    return 0 if rec["as_restated"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
