"""Lane L153 plan facts: the exact facts the controls plan states its outcomes from.

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

It decides no modified file. From the certificate (through the frozen reader), the
frozen check receipt, and the closed forms of `l153_geom`, it computes: the side's
12-place floor and ceiling and one unit of its last place; the exact clearances and
which squares each lowered side pushes out; square 1's and square n's contacts; the
closing move of the S4 pair, chosen as the tightest positive pair whose move, past
contact, is shorter than every other margin and clearance of the moved square; each
near pair's closing time and its exact closed-form margin past contact; and each
square's nearest wall.

PAST = 10^-90, thirty orders below the certificate's least gaps (about 10^-60).

Usage: l153_plan_facts.py LABEL CERT.json [TWIN.yaml] CHECK.json OUT.json
"""

from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l153_geom as G  # noqa: E402
import l153_reader as reader  # noqa: E402
from l153_check import floor_places, sci  # noqa: E402

PAST = Fraction(1, 10**90)
NEAR = Fraction(1, 10**12)
WALL_ORDER = ("left", "right", "bottom", "top")


def clearances(sq: G.FSquare, side: Fraction) -> dict[str, Fraction]:
    cx, cy, c, s = sq
    h = (abs(c) + abs(s)) / 2
    return {"left": cx - h, "right": side - cx - h, "bottom": cy - h, "top": side - cy - h}


def ceil_places(value: Fraction, places: int) -> Fraction:
    scale = 10**places
    return Fraction(-((-value.numerator * scale) // value.denominator), scale)


def main(argv: list[str]) -> int:
    label = argv[1]
    cert = argv[2]
    twin = argv[3] if len(argv) == 6 else None
    check_path = argv[-2]
    out_path = argv[-1]
    data = reader.read(cert, twin)
    check = json.loads(Path(check_path).read_text())
    n = data["n"]
    side = Fraction(*data["side"])
    sq = [G.decode(s) for s in data["squares"]]
    q = side.denominator
    floor12 = Fraction(side.numerator * 10**12 // side.denominator, 10**12)
    ceil12 = ceil_places(side, 12)
    clear = [clearances(s, side) for s in sq]
    facts: dict = {
        "program": "l153_plan_facts.py",
        "label": label,
        "n": n,
        "past": "1/10^90",
        "side_floor_30": floor_places(side, 30),
        "floor12": floor_places(floor12, 12),
        "ceil12": floor_places(ceil12, 12),
        "side_minus_floor12": sci(side - floor12, 8),
        "ceil12_minus_side": sci(ceil12 - side, 8),
        "one_unit_last_place": f"1/{q}",
        "check_receipt_sha256": hashlib.sha256(Path(check_path).read_bytes()).hexdigest(),
    }
    # Walls: which squares a lowered side pushes out (right or top clearance below the drop).
    def pushed(drop: Fraction) -> list[list]:
        return [
            [k + 1, w]
            for k in range(n)
            for w in ("right", "top")
            if clear[k][w] < drop
        ]

    def touching(drop: Fraction) -> list[list]:
        return [
            [k + 1, w]
            for k in range(n)
            for w in ("right", "top")
            if clear[k][w] == drop
        ]

    facts["S1a_pushed"] = pushed(Fraction(1, q))
    facts["S1b_pushed"] = pushed(PAST)
    facts["S1c_pushed"] = pushed(side - floor12)
    facts["S1a_touching"] = touching(Fraction(1, q))
    facts["S1b_touching"] = touching(PAST)
    facts["S1c_touching"] = touching(side - floor12)
    facts["least_positive_right_or_top_clearance"] = sci(
        min(clear[k][w] for k in range(n) for w in ("right", "top") if clear[k][w] > 0), 8
    )
    facts["S1d_contacts"] = [
        [k + 1, w] for k in range(n) for w in ("left", "bottom") if clear[k][w] == 0
    ]
    facts["wall_contacts"] = [
        [k + 1, w] for k in range(n) for w in WALL_ORDER if clear[k][w] == 0
    ]
    if facts["wall_contacts"] != check["walls"]["contacts"]:
        raise SystemExit("plan facts disagree with the check receipt on wall contacts")
    # G1 and G2.
    contacts = [tuple(p) for p in check["pairs"]["contacts"]]
    facts["square_1_pair_contacts"] = [list(p) for p in contacts if 1 in p]
    facts["square_n_pair_contacts"] = [list(p) for p in contacts if n in p]
    facts["square_1_wall_contacts"] = [[1, w] for w in WALL_ORDER if clear[0][w] == 0]
    facts["square_n_wall_contacts"] = [[n, w] for w in WALL_ORDER if clear[n - 1][w] == 0]
    facts["square_1_upright"] = sq[0][2] in (1, -1, 0) and sq[0][3] in (1, -1, 0)
    facts["square_1_left_clearance"] = sci(clear[0]["left"], 8)
    facts["square_1_after_G2"] = {
        w: sci(v, 8) for w, v in clearances((sq[0][0] + side, sq[0][1], sq[0][2], sq[0][3]), side).items()
    }
    facts["G2_no_touch"] = facts["square_1_upright"] and clear[0]["left"] > 0
    # Near pairs, exact, by the closed form.
    near = []
    for p in check["pairs"]["near_below_1e-9"]:
        i, j = p[0], p[1]
        m = G.closed_form_margin(sq[i - 1], sq[j - 1])
        if 0 < m < NEAR:
            near.append((m, i, j))
    near.sort()
    facts["near_pairs_below_1e-12"] = len(near)
    # S4: the tightest positive pair whose closing move, past contact, is shorter than
    # every other margin and every clearance of the moved square.
    s4 = None
    tried = 0
    for m, i, j in near:
        for mover, other in ((j, i), (i, j)):
            tried += 1
            info = G.closing(sq[other - 1], sq[mover - 1])
            slow = min(info["rates"][b] for b in info["binding"])
            tau = PAST / slow
            dx = sq[other - 1][0] - sq[mover - 1][0]
            dy = sq[other - 1][1] - sq[mover - 1][1]
            length2_past = (info["t"] + tau) ** 2 * (dx * dx + dy * dy)
            others = [
                G.closed_form_margin(sq[mover - 1], sq[k])
                for k in range(n)
                if k + 1 not in (mover, other)
            ]
            nearest_other = min(others)
            nearest_wall = min(clear[mover - 1].values())
            if nearest_other > 0 and nearest_wall > 0 and length2_past < nearest_other**2 and length2_past < nearest_wall**2:
                past_margin = max(
                    g - tau * info["rates"][lab] for lab, g in info["gaps_at"].items()
                )
                s4 = {
                    "pair": [min(i, j), max(i, j)],
                    "mover": mover,
                    "toward": other,
                    "margin": sci(m, 15),
                    "t_contact": str(info["t"]),
                    "t_past": str(info["t"] + tau),
                    "binding": info["binding"],
                    "move_length_past_squared": sci(length2_past, 6),
                    "mover_next_margin": sci(nearest_other, 8),
                    "mover_least_clearance": sci(nearest_wall, 8),
                    "margin_past": str(past_margin),
                    "margin_past_approx": sci(past_margin, 8),
                    "candidates_tried": tried,
                }
                break
        if s4 is not None:
            break
    facts["S4"] = s4
    # S5: every near pair closed along its centre line, moving the second square.
    s5 = []
    digest = hashlib.sha256()
    for m, i, j in near:
        info = G.closing(sq[i - 1], sq[j - 1])
        slow = min(info["rates"][b] for b in info["binding"])
        tau = PAST / slow
        past_margin = max(g - tau * info["rates"][lab] for lab, g in info["gaps_at"].items())
        s5.append([i, j, len(info["binding"]), sci(past_margin, 8)])
        digest.update(f"{i} {j} {info['t']} {info['t'] + tau} {past_margin}\n".encode())
    facts["S5"] = {
        "pairs": len(s5),
        "binding_axes_count": {
            str(b): sum(1 for x in s5 if x[2] == b) for b in sorted({x[2] for x in s5})
        },
        "past_margin_minus_1e90_exactly": sum(1 for x in s5 if x[3] == "-1.0000000e-90"),
        "digest_times_and_past_margins": digest.hexdigest(),
        "list": s5,
    }
    # S6: each square's nearest wall (ties in the order left, right, bottom, top).
    s6 = []
    for k in range(n):
        value, wall = min((clear[k][w], idx, w) for idx, w in enumerate(WALL_ORDER))[0::2]
        s6.append([k + 1, wall, sci(value, 6)])
    facts["S6"] = {
        "squares": n,
        "by_wall": {w: sum(1 for x in s6 if x[1] == w) for w in WALL_ORDER},
        "list": s6,
    }
    Path(out_path).write_text(json.dumps(facts, indent=1) + "\n")
    print(
        label,
        "S1a", len(facts["S1a_pushed"]),
        "S1b", len(facts["S1b_pushed"]),
        "S1c", len(facts["S1c_pushed"]),
        "S1d contacts", len(facts["S1d_contacts"]),
        "near", len(near),
        "S4", s4 and (s4["pair"], s4["mover"], s4["candidates_tried"]),
        "S5 past exactly -1e-90:", facts["S5"]["past_margin_minus_1e90_exactly"],
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
