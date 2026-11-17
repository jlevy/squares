"""Print the review's tables from the receipts.  It decides nothing.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

    python -I -B r1_tables.py OUT_DIR

Written after the checker and the controls plan were frozen.  It reads this lane's
own receipts in OUT_DIR (check-*.json and controls-*.json) and prints the facts the
review quotes, so that every number in the review's tables can be traced.
"""

from __future__ import annotations

import json
import os
import sys

LABELS = (
    "1005-n292-yaml", "1005-n292-json", "1006-n292-exact", "1006-n292-witness",
    "1007-n262-exact", "1007-n262-witness", "1007-n295-exact", "1007-n295-witness",
    "derived-n262-exact", "derived-n262-witness",
)


def load(out_dir, name):
    path = os.path.join(out_dir, name)
    if not os.path.exists(path):
        return None
    with open(path) as handle:
        return json.load(handle)


def main(argv):
    if len(argv) != 2:
        raise SystemExit(__doc__)
    out_dir = argv[1]
    total_controls = total_stated = 0
    for label in LABELS:
        check = load(out_dir, f"check-{label}.json")
        if check is None:
            continue
        pairs, walls = check["pairs"], check["walls"]
        print(f"== {label}: {check['file']} ({check['bytes']} bytes) {check['verdict']}")
        print(f"   sha256 {check['sha256']}")
        print(f"   side {check['side']['to_40_places'][:33]} digits "
              f"{check['side']['numerator_digits']}/{check['side']['denominator_digits']}")
        print(f"   scalars {check['reading']['scalars']} in lowest terms "
              f"{check['reading']['scalars_in_lowest_terms']}")
        print(f"   squares unit {check['squares']['unit_by_a']}/{check['squares']['unit_by_b']}"
              f" ccw {check['squares']['counterclockwise_by_a']}")
        print(f"   pairs {pairs['decided']} A {pairs['by_a']} B {pairs['by_b']}"
              f" area {pairs['sum_of_overlap_areas_by_b']}")
        print(f"   least margin {pairs['least_margin']['about']} at {pairs['least_margin_pairs']}")
        print(f"   below {pairs['positive_margins_below']}")
        print(f"   below 1e-9 {pairs['positive_below_1e-9']}")
        for wall in ("left", "bottom", "right", "top"):
            w = walls[wall]
            low = w["least_positive_clearance"]
            print(f"   {wall}: touching {w['touching_squares']} least {w['least_clearance']['about']}"
                  f" at {w['least_clearance_squares'][:8]}; least positive"
                  f" {low['about'] if low else None} at {w['least_positive_clearance_squares'][:8]};"
                  f" positive below 1e-9: {w['positive_clearances_below_1e-9']}")
        ext = check["extent"]
        print(f"   side less width {ext['side_less_width']['about']}, less height"
              f" {ext['side_less_height']['about']}")
        claim = check["claim"]
        print(f"   claim {claim['claimed']} less side {claim['claim_less_side']['about']}"
              f" ceiling {claim['claim_is_that_ceiling']}; cpu {check['cpu_seconds']} s")
        controls = load(out_dir, f"controls-{label}.json")
        if controls is None:
            continue
        total_controls += controls["of"]
        total_stated += controls["as_stated"]
        print(f"   controls {controls['summary']} {controls['as_stated']} of {controls['of']}"
              f" tier {controls['tier']} cpu {controls['cpu_seconds']} s")
        by_id = {c["id"]: c for c in controls["controls"]}
        for key in ("S0", "S1a", "S1b", "S1c", "S1d", "S1e", "S1f", "S2c", "S2p"):
            c = by_id[key]
            crossing = c.get("crossing", {})
            lowering = c.get("lowering", {}).get("about")
            print(f"     {key}: {c['verdict']} lowering {lowering} crossing"
                  f" {crossing.get('count')} {crossing.get('first', [])[:6]}"
                  f" contacts {c.get('contacts_left_bottom_right_top')}")
        for key in ("P0p", "P1c", "P1p"):
            c = by_id[key]
            print(f"     {key}: pair {c.get('pair')} moved {c.get('square_moved')} eligible"
                  f" {c.get('eligible')} rank {c.get('rank_among_positive_margins')} margin"
                  f" {c.get('margin_in_the_certificate', {}).get('about')} ->"
                  f" {c.get('margin')} {c.get('verdict')} {c.get('no_subject', '')}")
        for wall in ("left", "bottom", "right", "top"):
            c = by_id[f"W1c-{wall}"]
            print(f"     W1 {wall}: square {c.get('square')} clearance"
                  f" {c.get('clearance_in_the_certificate', {}).get('about')}"
                  f" {c.get('no_subject', '')}")
        for key in ("G9", "G10", "PALL", "WALL"):
            if key in by_id:
                c = by_id[key]
                keep = {k: c[k] for k in ("verdict", "overlapping_pairs", "least_margin", "pairs",
                                           "closings", "moves", "failures") if k in c}
                print(f"     {key}: {keep} cpu {c['cpu_seconds']} s")
    print(f"controls as stated: {total_stated} of {total_controls}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
