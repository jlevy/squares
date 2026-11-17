"""Compare two files that are said to hold one packing.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

    python -I -B r1_twin.py FILE_A FORM_A FILE_B FORM_B OUT.json

Each file is read strictly (r1_read).  A square is taken as the set of its four
corners, exact rationals; for a centre-and-direction file the corners are
c + (+-u +- v)/2 with v = (-sin, cos), computed here in fractions.  The files hold
one packing square for square when n and the side are equal and the k-th squares'
corner sets are equal for every k.  Where they are not, the squares are also
compared as an unordered collection.

For a corners file against a centre-and-direction file the receipt says where the
corners file starts each square's listing and in which sense, relative to the
counterclockwise listing from c + (-u - v)/2.

It decides no certificate.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_fmt  # noqa: E402
import r1_read  # noqa: E402


def corner_list(form, square):
    """The square's corners in order: as listed, or counterclockwise from c - (u+v)/2."""
    if form == "corners":
        return list(square)
    cx, cy, ux, uy = square
    vx, vy = -uy, ux
    out = []
    for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        out.append((cx + (su * ux + sv * vx) / 2, cy + (su * uy + sv * vy) / 2))
    return out


def compare(pa, pb):
    """The relation of two packings the reader handed on."""
    out = {
        "n": [pa.n, pb.n],
        "n_equal": pa.n == pb.n,
        "side_equal": pa.side == pb.side,
        "side_a_less_side_b": r1_fmt.frac(pa.side - pb.side),
    }
    la = [corner_list(pa.form, s) for s in pa.squares]
    lb = [corner_list(pb.form, s) for s in pb.squares]
    sa = [frozenset(c) for c in la]
    sb = [frozenset(c) for c in lb]
    out["squares_with_four_distinct_corners"] = [
        sum(1 for s in sa if len(s) == 4),
        sum(1 for s in sb if len(s) == 4),
    ]
    unequal = [k + 1 for k in range(min(pa.n, pb.n)) if sa[k] != sb[k]]
    out["unequal_in_file_order"] = {"count": len(unequal), "first": unequal[:40]}
    out["equal_square_for_square"] = pa.n == pb.n and not unequal
    out["equal_as_collections"] = Counter(sa) == Counter(sb)
    listing = Counter()
    for k in range(min(pa.n, pb.n)):
        if sa[k] != sb[k] or len(sa[k]) != 4:
            continue
        ref, other = la[k], lb[k]
        start = ref.index(other[0])
        if all(other[m] == ref[(start + m) % 4] for m in range(4)):
            listing[f"same sense, from corner {start} of the first file's listing"] += 1
        elif all(other[m] == ref[(start - m) % 4] for m in range(4)):
            listing[f"opposite sense, from corner {start} of the first file's listing"] += 1
        else:
            listing["not a cyclic listing of the same corners"] += 1
    out["second_file_listing_relative_to_first"] = dict(sorted(listing.items()))
    out["same_packing"] = (
        out["n_equal"] and out["side_equal"] and out["equal_square_for_square"]
    )
    return out


def main(argv):
    if len(argv) != 6:
        raise SystemExit(__doc__)
    path_a, form_a, path_b, form_b, out_path = argv[1:]
    receipt = {
        "program": "r1_twin.py",
        "lane": "R1 (c-review-1005-1117)",
        "first": {"file": os.path.basename(path_a), "form": form_a},
        "second": {"file": os.path.basename(path_b), "form": form_b},
    }
    pa, _ = r1_read.read_file(path_a, form_a)
    pb, _ = r1_read.read_file(path_b, form_b)
    receipt.update(compare(pa, pb))
    if pa.form == "corners" and pb.form == "corners":
        keys = ("softschema", "witness_id", "claim", "source", "certificate", "id_form")
        receipt["records_equal_outside_the_geometry"] = {
            key: pa.notes.get(key) == pb.notes.get(key) for key in keys
        }
        receipt["ids_equal"] = pa.ids == pb.ids
    with open(out_path, "w") as handle:
        json.dump(receipt, handle, indent=1)
        handle.write("\n")
    print("SAME_PACKING" if receipt["same_packing"] else "DIFFERENT", receipt["first"]["file"],
          receipt["second"]["file"])
    return 0 if receipt["same_packing"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
