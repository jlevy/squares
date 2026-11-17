"""The squares inside a certificate's L-shaped border, decided as a packing of their own.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

    python -I -B r1_inner.py FILE_OUTER FORM_OUTER FILE_INNER FORM_INNER OUT.json [DIR]

With DIR, the derived packing is also written there in two forms, as
``derived_exact.json`` (centres and directions) and ``derived_witness.yaml``
(corners), so that r1_check.py, r1_twin.py and r1_controls.py can be run on it.

Issue #1007 says its 295 packing is its 262 packing with an L-shaped border of 33
axis-aligned squares.  This program takes the 295 file (FILE_OUTER), tries each of
the four corners, naming as border the squares whose centres lie within 1 of the two
walls that meet there, and keeps the corner that leaves as many squares as the 262
file has and whose remaining squares have the least extent.  It treats those
squares as a packing of their own: it translates them so that their bounding box
starts at the origin, sets the side to the larger extent of that box, writes the
result in the outer file's form, reads it back and hands it to the decision
(r1_decide), both methods on every square, wall and pair.  It then compares those
squares, one to one by nearest centre, with the squares of the 262 file (FILE_INNER).

Written after the checker and the controls plan were frozen and before the findings
were frozen; it is not in the checker's digest list.  It selects and translates
squares and decides nothing itself: the decision is the frozen one.
"""

from __future__ import annotations

import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_axes  # noqa: E402
import r1_decide  # noqa: E402
import r1_fmt  # noqa: E402
import r1_frame  # noqa: E402
import r1_read  # noqa: E402

CORNERS = {
    "left-bottom": ("left", "bottom"),
    "right-bottom": ("right", "bottom"),
    "left-top": ("left", "top"),
    "right-top": ("right", "top"),
}


def near_wall(centre, wall, side):
    x, y = centre
    return {"left": x < 1, "right": x > side - 1, "bottom": y < 1, "top": y > side - 1}[wall]


def box(squares_a):
    xs = [Fraction(q[0], a.D) for a in squares_a for q in a.Q]
    ys = [Fraction(q[1], a.D) for a in squares_a for q in a.Q]
    return min(xs), min(ys), max(xs), max(ys)


def upright(frame):
    u = frame.u
    return (u[0] == 0 and abs(u[1]) == 1) or (u[1] == 0 and abs(u[0]) == 1)


def main(argv):
    if len(argv) not in (6, 7):
        raise SystemExit(__doc__)
    outer_path, outer_form, inner_path, inner_form, out_path = argv[1:6]
    derived_dir = argv[6] if len(argv) == 7 else None
    outer, _ = r1_read.read_file(outer_path, outer_form)
    small, _ = r1_read.read_file(inner_path, inner_form)
    side = outer.side
    frames = r1_frame.of_packing(outer)
    sq_a = r1_axes.of_packing(outer)
    receipt = {
        "program": "r1_inner.py",
        "lane": "R1 (c-review-1005-1117)",
        "outer": {"file": os.path.basename(outer_path), "n": outer.n, "side": r1_fmt.frac(side)},
        "inner_file": {
            "file": os.path.basename(inner_path), "n": small.n, "side": r1_fmt.frac(small.side),
        },
        "outer_side_less_1_less_inner_file_side": r1_fmt.exact_and_sci(side - 1 - small.side),
        "corners_tried": {},
    }
    chosen = None
    for name, (wall_a, wall_b) in CORNERS.items():
        border = [
            k for k in range(outer.n)
            if near_wall(frames[k].c, wall_a, side) or near_wall(frames[k].c, wall_b, side)
        ]
        in_border = set(border)
        rest = [sq_a[k] for k in range(outer.n) if k not in in_border]
        rx0, ry0, rx1, ry1 = box(rest)
        rest_extent = max(rx1 - rx0, ry1 - ry0)
        receipt["corners_tried"][name] = {
            "border_squares": len(border),
            "other_squares": outer.n - len(border),
            "border_squares_exactly_upright": sum(1 for k in border if upright(frames[k])),
            "larger_extent_of_the_other_squares": r1_fmt.dec(rest_extent, 20),
        }
        # among the corners that leave as many squares as the inner file has, the one
        # whose remaining squares have the least extent
        if outer.n - len(border) == small.n and (chosen is None or rest_extent < chosen[2]):
            chosen = (name, border, rest_extent)
    if chosen is None:
        receipt["verdict"] = "NO_BORDER_FOUND"
        r1_fmt.write_json(out_path, receipt)
        print("NO_BORDER_FOUND")
        return 1
    name, border, _ = chosen
    border_set = set(border)
    keep = [k for k in range(outer.n) if k not in border_set]
    x0, y0, x1, y1 = box([sq_a[k] for k in keep])
    width, height = x1 - x0, y1 - y0
    extent = max(width, height)
    bx0, by0, bx1, by1 = box([sq_a[k] for k in border])
    moved = [r1_frame.translate_square(outer.form, outer.squares[k], (-x0, -y0)) for k in keep]
    kind = {"corners": "witness-yaml", "centre": "centre-json"}[outer.form]
    raw = r1_read.WRITERS[kind](len(moved), extent, moved)
    packing = r1_read.READERS[kind](raw)
    if packing.side != extent or [tuple(s) for s in packing.squares] != [tuple(s) for s in moved]:
        raise SystemExit("the inner packing did not read back as written")
    dec, _, _ = r1_decide.decide(packing)
    verdict, reasons = dec.verdict()
    positive = sorted(v for v in dec.margin.values() if v > 0)
    receipt["corner"] = name
    receipt["border"] = {
        "squares": [k + 1 for k in border],
        "count": len(border),
        "exactly_upright": sum(1 for k in border if upright(frames[k])),
        "bounding_box": [r1_fmt.dec(v, 20) for v in (bx0, by0, bx1, by1)],
    }
    receipt["inner"] = {
        "squares": len(keep),
        "bounding_box_in_the_outer_file": [r1_fmt.dec(v, 20) for v in (x0, y0, x1, y1)],
        "lower_left_exact": [r1_fmt.frac(x0), r1_fmt.frac(y0)],
        "width": r1_fmt.exact_and_sci(width, 20),
        "height": r1_fmt.exact_and_sci(height, 20),
        "larger_extent": r1_fmt.exact_and_sci(extent, 20),
        "larger_extent_to_30_places": r1_fmt.dec(extent, 30),
        "outer_side_less_1_less_extent": r1_fmt.exact_and_sci(side - 1 - extent),
        "inner_file_side_less_extent": r1_fmt.exact_and_sci(small.side - extent),
        "twelve_place_ceiling_of_extent": r1_fmt.dec(r1_fmt.ceil_places(extent, 12), 12),
    }
    receipt["decision_of_the_inner_squares_in_their_own_box"] = {
        "side": r1_fmt.frac(extent),
        "verdict": verdict,
        "reasons": [{"kind": k, "count": len(v), "first": v[:12]} for k, v in reasons],
        "pairs": len(dec.margin),
        "pairs_apart_touching_overlapping_by_a": [
            sum(1 for v in dec.margin.values() if v > 0),
            sum(1 for v in dec.margin.values() if v == 0),
            sum(1 for v in dec.margin.values() if v < 0),
        ],
        "classes_by_b": {
            cls: sum(1 for c in dec.class_b.values() if c == cls)
            for cls in ("apart", "touching", "overlapping")
        },
        "least_positive_margin": r1_fmt.sci(positive[0]) if positive else None,
        "methods_disagree": len(dec.disagreements()),
        "wall_contacts_left_bottom_right_top": [
            sum(1 for c in dec.clear if c[w] == 0) for w in range(4)
        ],
        "least_clearance_left_bottom_right_top": [
            r1_fmt.sci(min(c[w] for c in dec.clear)) for w in range(4)
        ],
    }
    # the inner squares against the squares of the inner file, by nearest centre after
    # the two bounding boxes' lower-left corners are brought together
    small_frames = r1_frame.of_packing(small)
    sx0, sy0, sx1, sy1 = box(r1_axes.of_packing(small))
    pairs = []
    used = set()
    one_to_one = True
    for idx, k in enumerate(keep):
        cx, cy = frames[k].c[0] - x0, frames[k].c[1] - y0
        best = None
        for m, f in enumerate(small_frames):
            dx, dy = f.c[0] - sx0 - cx, f.c[1] - sy0 - cy
            d2 = dx * dx + dy * dy
            if best is None or d2 < best[0]:
                best = (d2, m, dx, dy)
        if best[1] in used:
            one_to_one = False
        used.add(best[1])
        pairs.append((idx, k, best))
    worst = max(pairs, key=lambda p: p[2][0])
    same_direction = sum(
        1 for _, k, b in pairs if (frames[k].u == small_frames[b[1]].u)
    )
    same_index = sum(1 for idx, _, b in pairs if idx == b[1])
    receipt["against_the_inner_file"] = {
        "inner_file_bounding_box": [r1_fmt.dec(v, 20) for v in (sx0, sy0, sx1, sy1)],
        "nearest_centres_one_to_one": one_to_one,
        "paired_in_the_same_order": same_index,
        "largest_centre_distance": f"{math.sqrt(float(worst[2][0])):.6e}",
        "largest_centre_distance_at": [worst[1] + 1, worst[2][1] + 1],
        "centre_distances_below_1e-9_1e-6_1e-3": [
            sum(1 for p in pairs if p[2][0] < Fraction(1, 10**18)),
            sum(1 for p in pairs if p[2][0] < Fraction(1, 10**12)),
            sum(1 for p in pairs if p[2][0] < Fraction(1, 10**6)),
        ],
        "exactly_equal_centres": sum(1 for p in pairs if p[2][0] == 0),
        "exactly_equal_directions": same_direction,
    }
    if derived_dir is not None:
        import hashlib

        import r1_twin

        if outer.form == "centre":
            centre_form = moved
            corner_form = [tuple(r1_twin.corner_list("centre", sq)) for sq in moved]
            written = {
                "derived_exact.json": r1_read.write_centre_json(len(moved), extent, centre_form),
                "derived_witness.yaml": r1_read.write_witness_yaml(
                    len(moved), extent, corner_form, witness_id="W-r1-derived"
                ),
            }
        else:
            written = {
                "derived_witness.yaml": r1_read.write_witness_yaml(
                    len(moved), extent, moved, witness_id="W-r1-derived"
                ),
            }
        receipt["derived_files"] = {}
        for name_out, raw_out in written.items():
            with open(os.path.join(derived_dir, name_out), "wb") as handle:
                handle.write(raw_out)
            receipt["derived_files"][name_out] = {
                "bytes": len(raw_out), "sha256": hashlib.sha256(raw_out).hexdigest(),
            }
    receipt["verdict"] = verdict
    r1_fmt.write_json(out_path, receipt)
    print(verdict, name, "inner", len(keep), "extent", r1_fmt.dec(extent, 20),
          "inner-file side less extent", r1_fmt.sci(small.side - extent))
    return 0 if verdict == "ACCEPT" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
