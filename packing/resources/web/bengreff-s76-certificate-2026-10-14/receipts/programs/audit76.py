"""Triage diagnostic for #594: the repository's own audit_cover on the s(76) cover, with the
total and counts the issue states, so the 'as stated' flags are meaningful.

usage: python -I audit76.py PACKING_DIR COVER
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

packing, cover = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(packing))
from devtools.audit_evand_mixed_covers import Case, audit_cover  # noqa: E402

case = Case(n=76, side=9, bundle="s76", cover=cover.name, total=Fraction(3788361049, 50000000),
            points=41633, segments=9744, directory=cover.parent)
r = audit_cover(case)
r["cover"] = cover.name
print(json.dumps(r, indent=1))
