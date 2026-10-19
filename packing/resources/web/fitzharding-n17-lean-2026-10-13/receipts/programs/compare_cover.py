"""Compare sq17-lean's cell cover and excluded patterns with this repository's n = 17 data.

Reads, as text, the packet's retained ``Sq17Lean/ExactCellCoverData.lean`` (the 24 cells,
each a list of rational vertices under a ``-- name`` comment) and
``Sq17Lean/RepresentativeCaseData.lean`` (the 35 patterns, each a list of cell indices),
and this repository's own: the four cover designs of ``devtools.check_n17_capacity_one_cover``
(H-266; exp-247's ``ring-3-voronoi-8-tabbed-unique`` is ``UNIQUE_24``) and the certified
sub-pattern ledger ``certified-sub-patterns.yaml``. Nothing from the source is executed:
its numbers and indices are parsed by regular expressions, and every comparison is
exact. Prints one JSON object:

- ``cells``: for each design, how many of the Lean's 24 cells equal one of its cells
  vertex for vertex (as sets of exact points), and whether the matches keep the Lean's
  order and names;
- ``patterns``: each Lean pattern by the Lean's cell names, the admitted ledger entries
  equal to it under one of the eight symmetries of the cover
  (``check_n17_capacity_one_cover.d4_permutations``), the entries that strictly contain an
  image of it, and a count of the equal ones by the record that admitted them.

Usage, from ``packing/``, with the project interpreter and ``-I``::

    .venv/bin/python3 -I PACKET/receipts/programs/compare_cover.py PACKET REPO

``PACKET`` is the packet directory and ``REPO`` the repository root; the output is the
packet's ``receipts/cover-comparison.json``.
"""

from __future__ import annotations

import collections
import json
import re
import sys
from fractions import Fraction as Q
from pathlib import Path

import yaml

packet, repo = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "packing"))

from devtools.check_n17_capacity_one_cover import (  # noqa: E402
    DESIGNS,
    UNIQUE_24,
    build_cover,
    d4_permutations,
)

LEAN = packet / "sq17-lean" / "Sq17Lean"
LEDGER = repo / "packing/campaign/explorations/X048-session-168-pilots/certified-sub-patterns.yaml"
POINT = re.compile(r"\((-?\d+(?:/\d+)?), (-?\d+(?:/\d+)?)\)")

cover_text = (LEAN / "ExactCellCoverData.lean").read_text(encoding="utf-8")
block = re.search(
    r"def vertices : Fin 24 → List \(ℚ × ℚ\) := !\[(.*?)\]\n\ndef xBreaks", cover_text, re.S
)
if block is None:
    raise SystemExit("no vertices block in ExactCellCoverData.lean")
lean_cells: list[tuple[str, frozenset[tuple[Q, Q]]]] = []
name = None
for line in block.group(1).splitlines():
    line = line.strip()
    if line.startswith("--"):
        name = line[2:].strip()
    elif line.startswith("["):
        if name is None:
            raise SystemExit("a cell with no name comment")
        points = [(Q(x), Q(y)) for x, y in POINT.findall(line)]
        lean_cells.append((name, frozenset(points)))
        name = None
if len(lean_cells) != 24:
    raise SystemExit(f"{len(lean_cells)} cells, not 24")
lean_names = [cell_name for cell_name, _ in lean_cells]

cells: dict[str, object] = {}
for design_name, design in DESIGNS.items():
    ours = build_cover(design)
    index = {frozenset(cell.vertices): (k, cell.name) for k, cell in enumerate(ours)}
    matched = [(k, index.get(points)) for k, (_, points) in enumerate(lean_cells)]
    cells[design_name] = {
        "cells": len(ours),
        "lean_cells_equal_vertex_for_vertex": sum(hit is not None for _, hit in matched),
        "same_order": all(hit is not None and hit[0] == k for k, hit in matched),
        "same_names": all(
            hit is not None and hit[1] == lean_names[k] for k, hit in matched
        ),
    }

pattern_text = (LEAN / "RepresentativeCaseData.lean").read_text(encoding="utf-8")
head = pattern_text.split("noncomputable def fullRosters", 1)[0]
lean_patterns = {
    int(k): frozenset(int(c) for c in members.split(","))
    for k, members in re.findall(r"\|\s*(\d+)\s*=>\s*\[([\d,]+)\]", head)
}
if sorted(lean_patterns) != list(range(35)):
    raise SystemExit(f"patterns {sorted(lean_patterns)}, not 0..34")

unique = build_cover(UNIQUE_24)
names = [cell.name for cell in unique]
if names != lean_names:
    raise SystemExit("the Lean cells are not UNIQUE_24's in order; patterns cannot be read")
permutations = d4_permutations(unique)
if permutations is None:
    raise SystemExit("UNIQUE_24 is not closed under D4")
position = {cell_name: k for k, cell_name in enumerate(names)}
ledger = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
entries = {
    str(entry["name"]): (
        frozenset(position[cell] for cell in entry["cells"]),
        str(entry.get("evidence", "")),
    )
    for entry in ledger["entries"]
    if entry.get("status") == "admitted"
}

rows = []
admitted_by: collections.Counter[str] = collections.Counter()
for k, pattern in sorted(lean_patterns.items()):
    images = {frozenset(permutation[c] for c in pattern) for permutation in permutations.values()}
    equal = sorted(entry for entry, (occupied, _) in entries.items() if occupied in images)
    inside = sorted(
        entry
        for entry, (occupied, _) in entries.items()
        if occupied not in images and any(image < occupied for image in images)
    )
    for entry in equal:
        admitted_by[entries[entry][1]] += 1
    rows.append(
        {
            "pattern": k,
            "occupied": len(pattern),
            "cells": [names[c] for c in sorted(pattern)],
            "equal_to_admitted": equal,
            "strictly_inside_admitted": inside,
        }
    )

print(
    json.dumps(
        {
            "format": "sq17-lean-cover-comparison-v1",
            "inputs": {
                "lean": [
                    "sq17-lean/Sq17Lean/ExactCellCoverData.lean",
                    "sq17-lean/Sq17Lean/RepresentativeCaseData.lean",
                ],
                "record": [
                    "packing/devtools/check_n17_capacity_one_cover.py",
                    str(LEDGER.relative_to(repo)),
                ],
            },
            "lean_cell_names": lean_names,
            "cells": cells,
            "patterns": {
                "lean_patterns": len(lean_patterns),
                "admitted_entries": len(entries),
                "equal_to_an_admitted_entry": sum(bool(row["equal_to_admitted"]) for row in rows),
                "strictly_inside_an_admitted_entry_only": sum(
                    not row["equal_to_admitted"] and bool(row["strictly_inside_admitted"])
                    for row in rows
                ),
                "neither": [
                    row["pattern"]
                    for row in rows
                    if not row["equal_to_admitted"] and not row["strictly_inside_admitted"]
                ],
                "equal_ones_by_admitting_record": dict(sorted(admitted_by.items())),
                "rows": rows,
            },
        },
        indent=2,
        ensure_ascii=False,
    )
)
