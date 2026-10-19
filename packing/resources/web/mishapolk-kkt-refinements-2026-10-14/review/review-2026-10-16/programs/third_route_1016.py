"""Run the third exact route on the six packets of T-185 to T-190 (review lane C, 16 October).

``devtools.check_half_angle_area`` (unchanged since ``e1fc548d9``) decides only the
imports its tables name. This driver, written for the review in scratch space and kept
here since the review's fix round, adds the six packets to those tables in this process
and then runs the route's
own ``decide-imports`` unchanged: its readers, its decisions and six controls, its
comparison with the maintained routes' retained positives and frozen claim records, its
hold of each certificate to the side the citing register entry's claim prints, its
upstream checks, and its credit measurements (`arrangement_gap`, `unmoved`). It adds no
reader and changes no decision; it writes only the ``--json`` report it is given.

Keys, one packet each, decided at the counts the entries cite:

- ``#506-n175``: ``couzo-certificates-2026-10-11`` at 175 (T-185);
- ``70a033f``: ``mishapolk-kkt-refinements-2026-10-14`` at T-186's twelve counts;
- ``#606``: ``evand-n146-2026-10-14`` at 146 (T-187);
- ``487b058``: ``couzo-verified-bounds-2026-10-14`` at 211 (T-188);
- ``#607``: ``couzo-certificates-2026-10-14`` at 237 (T-189);
- ``4e4c8ce``: ``couzo-n237-2026-10-15`` at 237 (T-190).

Usage, from ``packing/`` with the project interpreter, isolated since the upstream copies it
reads are downloaded data::

    python -I resources/web/mishapolk-kkt-refinements-2026-10-14/review/review-2026-10-16/programs/third_route_1016.py \
        --workers 1 --json OUT.json \
        --upstream PACKET DIR ...
"""

from __future__ import annotations

import sys
from pathlib import Path

#: `packing/`, six levels up from this file in the packet's review directory.
PACKING = Path(__file__).resolve().parents[6]
if str(PACKING) not in sys.path:
    sys.path.insert(0, str(PACKING))

from devtools import check_half_angle_area as route  # noqa: E402

NEW = {
    "#506-n175": "couzo-certificates-2026-10-11",
    "70a033f": "mishapolk-kkt-refinements-2026-10-14",
    "#606": "evand-n146-2026-10-14",
    "487b058": "couzo-verified-bounds-2026-10-14",
    "#607": "couzo-certificates-2026-10-14",
    "4e4c8ce": "couzo-n237-2026-10-15",
}
T186 = (129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304)
ROSTERS = {
    "#506-n175": (175,),
    "70a033f": T186,
    "#606": (146,),
    "487b058": (211,),
    "#607": (237,),
    "4e4c8ce": (237,),
}
# Each certificate against the packing its entry's `regularizations` names first, then
# the packing the record credits as first found, and the case's house where different.
CREDITED = {
    ("#506-n175", 175): ("T-140", "T-125", "T-130", "T-158"),
    ("70a033f", 129): ("T-174", "T-162"),
    ("70a033f", 154): ("T-182", "T-172", "T-160"),
    ("70a033f", 156): ("T-174", "T-161", "T-149"),
    ("70a033f", 175): ("T-174", "T-158"),
    ("70a033f", 176): ("T-174", "#575"),
    ("70a033f", 204): ("T-174", "T-162"),
    ("70a033f", 232): ("T-174", "T-158"),
    ("70a033f", 264): ("T-174", "T-158"),
    ("70a033f", 271): ("T-174", "T-161", "T-151"),
    ("70a033f", 302): ("T-181", "T-164"),
    ("70a033f", 303): ("T-174", "T-162"),
    ("70a033f", 304): ("T-175",),
    ("#606", 146): ("T-150", "T-168", "T-174", "T-125", "T-146"),
    ("487b058", 211): ("T-182", "T-181", "T-175", "T-149"),
    ("#607", 237): ("T-183", "T-161", "T-140"),
    ("4e4c8ce", 237): ("T-183", "T-189", "T-161"),
}
READERS = {
    "T-182": route.import_packing("#586"),
    "T-183": route.import_packing("#593"),
    "T-189": route.import_packing("#607"),
}


def extend() -> None:
    """Name the six packets in the route's tables, as a roster commit would."""
    route.ALL_IMPORTS.update(NEW)
    route.IMPORTS_1014.update(NEW)
    route.REGISTERED = frozenset(route.IMPORTS_1014)
    route.ROSTERS.update(ROSTERS)
    route.CREDITED.update(CREDITED)
    route.CREDITED_READERS.update(READERS)
    # Each against Mykhailo Polkovskyi's #593 at its count where #593 declares one and no
    # credit line already names it, as the 14 October review measured its imports.
    for key in ("#506-n175", "70a033f", "#606", "487b058"):
        route.ALSO_MEASURED[key] = ("#593",)


def main(argv: list[str]) -> int:
    extend()
    return route.main(["decide-imports", "--imports", *NEW, *argv])


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
