"""Measure #470's sixteen witnesses pose by pose against every packing published before it.

Written for review A3 of #747 (23 October 2026). Issue 470 credits the discoverers of the
packings its poses started from, Stenlund, Friedman, Ellsworth, SQUISH (Nate
Chaoweeraprasit), Francisco Couzo and Ryan Xu, without saying which count started from
which; the confirmation of 12 October asked the author, and the question waited. The
10 October review had measured 103 as Ryan Xu's packing and 258 as SQUISH's. This
measures the rest, so that the question is settled here rather than held open. A
measurement for credit; it decides nothing.

Each witness is T-138's at its count, read by the third route's import reader
(`check_half_angle_area.import_packing("#470")`). It is measured against every register
entry the third route can read a packing of (`CREDITED_READERS`) whose source was
published before #470's, on 9 October 2026, at every count of T-138 the entry's scope
holds. For each pair it records `arrangement_gap`: under each of the box's eight
symmetries, every square matched to the nearest centre of the other packing, kept only
where one to one, and for the best such symmetry the largest move, the squares moved
beyond each of 1e-9 to 1e-1 and the squares turned by a sine above 1e-6; and `unmoved`,
the symmetry that keeps most squares where they were. Both are exact over the rationals.
A packing an entry's reader cannot produce at a count is recorded with the reason.

Usage, from packing/ with the project interpreter, about a minute of CPU:
    python resources/web/mishapolk-decimal-poses-2026-10-09/measure/identity.py \
        --out resources/web/mishapolk-decimal-poses-2026-10-09/measure/identity.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path[:0] = [str(Path.cwd()), str(Path.cwd() / "src")]

from devtools import check_half_angle_area as area  # noqa: E402
from sqpack.yamlio import safe_load  # noqa: E402

RESULTS = Path("frontier/results.yaml")
WITNESS = "T-138"
ISSUE = "#470"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    register = {
        str(entry["id"]): entry
        for entry in safe_load(RESULTS.read_text(encoding="utf-8"))["results"]
    }
    published = str(register[WITNESS]["attribution"]["published"])
    counts = [int(n) for n in register[WITNESS]["scope"]["n_values"]]
    earlier = sorted(
        key
        for key in area.CREDITED_READERS
        if key in register
        and str((register[key].get("attribution") or {}).get("published", "9999")) < published
    )
    rows: list[dict[str, object]] = []
    for n in counts:
        mine = area.import_packing(ISSUE)(n)
        for key in earlier:
            if n not in {int(m) for m in register[key]["scope"]["n_values"]}:
                continue
            row: dict[str, object] = {
                "n": n,
                "against": key,
                "published": str(register[key]["attribution"]["published"]),
            }
            try:
                other = area.parent_packing(key, n)
            except Exception as error:  # noqa: BLE001 -- recorded, not hidden
                row["unreadable"] = f"{type(error).__name__}: {error}"[:200]
                rows.append(row)
                continue
            try:
                row["gap"] = area.arrangement_gap(mine, other)
            except area.AreaRouteError as error:
                row["gap"] = {"unmatched": str(error)}
            row["unmoved"] = area.unmoved(mine, other)
            rows.append(row)
            gap = row["gap"]
            assert isinstance(gap, dict)
            moved = gap.get("moved_beyond") or {}
            print(
                f"{n:>4} {key:<6} symmetry {gap.get('symmetry', '-')} "
                f"largest {gap.get('largest_displacement', '-')} "
                f"beyond 1e-9 {moved.get('1e-9', '-')} 1e-3 {moved.get('1e-3', '-')} "
                f"turned {gap.get('turned_beyond_1e-6', '-')} {gap.get('unmatched', '')}"
            )
    document = {
        "format": "mishapolk-470-identity-v1",
        "witness": f"{WITNESS} ({ISSUE}), published {published}",
        "counts": counts,
        "against": earlier,
        "rows": rows,
    }
    args.out.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
