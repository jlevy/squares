"""Triage diagnostic for #610: the repository's own audit_cover on a mixed cover, with the
total and counts the source states, so the 'as stated' flags are meaningful. The #594
triage's audit76.py with the case as arguments.

usage: python -I audit_stated.py PACKING_DIR COVER N SIDE TOTAL POINTS SEGMENTS
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

packing, cover = Path(sys.argv[1]), Path(sys.argv[2])
n, side, total, points, segments = (
    int(sys.argv[3]),
    int(sys.argv[4]),
    Fraction(sys.argv[5]),
    int(sys.argv[6]),
    int(sys.argv[7]),
)
sys.path.insert(0, str(packing))
from devtools.audit_evand_mixed_covers import Case, audit_cover  # noqa: E402

case = Case(
    n=n,
    side=side,
    bundle=f"s{n}",
    cover=cover.name,
    total=total,
    points=points,
    segments=segments,
    directory=cover.parent,
)
r = audit_cover(case)
r["cover"] = cover.name
print(json.dumps(r, indent=1))
sys.exit(0 if not r.get("problems") else 1)
