"""Facts the controls plan states its outcomes from. Decides no modified file.

Usage: python -I -B l101_plan_facts.py WITNESS.yaml TWIN.json N CHECK.json OUT.json

From the accepted base it computes, exactly: the side's 12-place floor and ceiling and
the drop to the floor; every square's four wall clearances (its own min / max of corner
coordinates); the far-wall contacts and the least positive far-wall clearance against
1/q and 1e-30; the squares a side at the floor would cut; for the least pair and every
pair below 1e-12, the closing time along the line of centres, the move it makes and,
for the least pair, the moved square's other margins (by l101_geom's own projections)
and its wall clearances after the move; each square's nearest wall.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l101_geom as geom  # noqa: E402
import l101_reader as reader  # noqa: E402
from l101_check import frac_str, sci, sha256_file  # noqa: E402

WALLS = ("left", "bottom", "right", "top")
D30 = F(1, 10**30)


def clearances(points: list, side: F) -> dict[str, F]:
    p = geom.to_fracs(points)
    xs = [x for x, _ in p]
    ys = [y for _, y in p]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


def margin(a: list, b: list) -> F:
    best = None
    for ax in geom.axes(a) + geom.axes(b):
        lo_a, hi_a = geom.interval(a, ax)
        lo_b, hi_b = geom.interval(b, ax)
        gap = max(lo_b - hi_a, lo_a - hi_b)
        best = gap if best is None or gap > best else best
    assert best is not None
    return best


def floor_places(x: F, places: int) -> F:
    scale = 10**places
    return F((x.numerator * scale) // x.denominator, scale)


def main() -> int:
    yaml_path, json_path, n_text, check_path, out_path = sys.argv[1:6]
    w = reader.read_files(Path(yaml_path), Path(json_path), int(n_text))
    check = json.loads(Path(check_path).read_text(encoding="utf-8"))
    side = F(*w.side)
    q = w.side[1]
    floor12 = floor_places(side, 12)
    ceil12 = floor12 if floor12 == side else floor12 + F(1, 10**12)
    drop = side - floor12
    rows = [clearances(sq, side) for sq in w.squares]
    far_contacts = [[i + 1, wl] for i, r in enumerate(rows) for wl in ("right", "top") if r[wl] == 0]
    near_contacts = [[i + 1, wl] for i, r in enumerate(rows) for wl in ("left", "bottom") if r[wl] == 0]
    far_positive = [(r[wl], i + 1, wl) for i, r in enumerate(rows) for wl in ("right", "top") if r[wl] > 0]
    least_far = min(far_positive)
    cut_by_floor = sorted({i + 1 for i, r in enumerate(rows) for wl in ("right", "top") if r[wl] < drop})
    nearest = []
    for i, r in enumerate(rows):
        best = min(r[wl] for wl in WALLS)
        ties = [wl for wl in WALLS if r[wl] == best]
        nearest.append({"square": i + 1, "wall": ties[0], "ties": ties, "clearance": frac_str(best)})

    # The least pair: move one square toward the other along the line of centres. A
    # translation by d changes every projection gap on a unit axis by at most |d|, so the
    # moved square's other pairs stay apart when |d|^2 < (least other margin)^2. The square
    # moved is the higher id unless only the lower one passes that test.
    a0, b0 = (k - 1 for k in check["least_pair_margin"]["pair"])
    choices = {}
    for fixed, moving in ((a0, b0), (b0, a0)):
        c = geom.closing(w.squares[fixed], w.squares[moving])
        least_o = min(margin(w.squares[moving], w.squares[k]) for k in range(w.n) if k not in (a0, b0))
        d2 = c["move"][0] ** 2 + c["move"][1] ** 2
        choices[moving + 1] = {"info": c, "least_other": least_o, "euclid_ok": d2 < least_o**2,
                               "move_euclid_sq": d2}
    j0 = b0 if choices[b0 + 1]["euclid_ok"] or not choices[a0 + 1]["euclid_ok"] else a0
    i0 = a0 if j0 == b0 else b0
    info = choices[j0 + 1]["info"]
    least_other = choices[j0 + 1]["least_other"]
    moved_contact = geom.moved(w.squares[j0], info["w"], info["t_contact"])
    moved_past = geom.moved(w.squares[j0], info["w"], info["t_past"])
    least_pair = {
        "fixed": i0 + 1,
        "moved": j0 + 1,
        "margin": check["least_pair_margin"]["value"],
        "t_contact": frac_str(info["t_contact"]),
        "t_past": frac_str(info["t_past"]),
        "active_all_decreasing": info["active_all_decreasing"],
        "move_l1": sci(info["move_l1"]),
        "least_other_margin_of_moved": sci(least_other),
        "move_l1_below_every_other_margin": info["move_l1"] < least_other,
        "move_euclid_below_every_other_margin": choices[j0 + 1]["euclid_ok"],
        "move_euclid_approx": sci(F(int(float(choices[j0 + 1]["move_euclid_sq"]) ** 0.5 * 10**30), 10**30), 6),
        "choices": {str(k): {"euclid_ok": v["euclid_ok"], "least_other": sci(v["least_other"]),
                             "move_l1": sci(v["info"]["move_l1"])} for k, v in choices.items()},
        "moved_clearances_at_contact": {k: sci(v) for k, v in clearances(moved_contact, side).items()},
        "moved_clearances_past": {k: sci(v) for k, v in clearances(moved_past, side).items()},
        "moved_inside_at_contact": min(clearances(moved_contact, side).values()) > 0,
        "moved_inside_past": min(clearances(moved_past, side).values()) > 0,
    }

    near_pairs = []
    for entry in check["near_pairs_exact"]:
        a, b = (k - 1 for k in entry["pair"])
        c = geom.closing(w.squares[a], w.squares[b])
        near_pairs.append({
            "pair": entry["pair"],
            "t_contact": frac_str(c["t_contact"]),
            "t_past": frac_str(c["t_past"]) if c["t_past"] is not None else None,
            "active_all_decreasing": c["active_all_decreasing"],
            "move_l1": sci(c["move_l1"]),
        })

    facts = {
        "program": "l101_plan_facts.py",
        "input_yaml_sha256": sha256_file(Path(yaml_path)),
        "check_receipt_sha256": sha256_file(Path(check_path)),
        "side": frac_str(side),
        "side_denominator_digits": len(str(q)),
        "side_terminates": floor_places(side, 200) == side,
        "floor12": frac_str(floor12),
        "ceil12": frac_str(ceil12),
        "ceil12_decimal": f"{ceil12.numerator // ceil12.denominator}.{(ceil12.numerator * 10**12 // ceil12.denominator) % 10**12:012d}",
        "drop_to_floor12": sci(drop),
        "claim_less_side": sci(ceil12 - side),
        "far_wall_contacts": far_contacts,
        "near_wall_contacts": near_contacts,
        "least_positive_far_clearance": {"value": sci(least_far[0]), "square": least_far[1], "wall": least_far[2]},
        "least_positive_far_clearance_above_1_over_q": least_far[0] > F(1, q),
        "least_positive_far_clearance_above_1e-30": least_far[0] > D30,
        "cut_by_floor12": cut_by_floor,
        "square1_left_clearance": sci(rows[0]["left"]),
        "square1_left_clearance_positive": rows[0]["left"] > 0,
        "least_pair": least_pair,
        "near_pairs": near_pairs,
        "near_pairs_all_decreasing": all(p["active_all_decreasing"] for p in near_pairs),
        "nearest_walls": nearest,
        "nearest_wall_ties": [r for r in nearest if len(r["ties"]) > 1],
    }
    Path(out_path).write_text(json.dumps(facts, indent=1) + "\n", encoding="utf-8")
    print("cut_by_floor12", cut_by_floor)
    print("least_pair", {k: v for k, v in least_pair.items() if k not in {"t_contact", "t_past", "margin"}})
    print("far", far_contacts, "near", near_contacts, "least far", facts["least_positive_far_clearance"])
    print("near pairs", len(near_pairs), "all decreasing", facts["near_pairs_all_decreasing"])
    print("ties", facts["nearest_wall_ties"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
