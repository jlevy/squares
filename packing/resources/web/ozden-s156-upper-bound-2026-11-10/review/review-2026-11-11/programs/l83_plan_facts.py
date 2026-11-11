"""Facts the controls are stated from; decides no modified file (review L83).

Usage: python -I -B l83_plan_facts.py CERT.yaml CHECK.json OUT.json
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402
import l83_geom as G  # noqa: E402
import l83_reader as R  # noqa: E402
import l83_sat as A  # noqa: E402


def places(x: Fraction, k: int, up: bool) -> Fraction:
    s = x * 10**k
    q = s.numerator // s.denominator
    if up and q * s.denominator != s.numerator:
        q += 1
    return Fraction(q, 10**k)


def main(argv: list[str]) -> int:
    w = R.read_files(Path(argv[1])).witness
    chk = json.loads(Path(argv[2]).read_text())
    S = Fraction(*w.side)
    floor12, ceil12 = places(S, 12, False), places(S, 12, True)
    drop = S - floor12
    clear = {w.ids[i]: A.wall_clearances(A.points(w.corners[i]), S) for i in range(w.n)}
    far_contacts = sorted((i, wl) for i, c in clear.items() for wl in ("right", "top") if c[wl] == 0)
    s1c = sorted({i for i, c in clear.items() if c["right"] < drop or c["top"] < drop})
    positive = [v for c in clear.values() for v in c.values() if v > 0]
    least_pos = min(positive)
    lp = chk["least_pair_margin"]["ids"]
    a, b = A.points(w.corners[lp[0] - 1]), A.points(w.corners[lp[1] - 1])
    t = G.closing_parameter(a, b)
    ca, cb = G.centre(a), G.centre(b)
    dist = float(((ca[0] - cb[0]) ** 2 + (ca[1] - cb[1]) ** 2)) ** 0.5
    sb = A.Square(b)
    others = sorted(
        A.pair_margin(sb, A.Square(A.points(w.corners[k]))) for k in range(w.n) if k not in (lp[0] - 1, lp[1] - 1)
    )
    moved_least_other_margin = float(others[0])
    moved_least_wall = float(min(clear[lp[1]].values()))
    dx, dy = t * (ca[0] - cb[0]), t * (ca[1] - cb[1])
    cw = clear[lp[1]]
    after = {"left": cw["left"] + dx, "right": cw["right"] - dx, "bottom": cw["bottom"] + dy, "top": cw["top"] - dy}
    moved_walls = {k: {"before": float(cw[k]), "after_contact_move": float(v)} for k, v in after.items()}
    t_past = t + Fraction(1, 10**30)
    after_past = {"left": cw["left"] + t_past * (ca[0] - cb[0]), "right": cw["right"] - t_past * (ca[0] - cb[0]), "bottom": cw["bottom"] + t_past * (ca[1] - cb[1]), "top": cw["top"] - t_past * (ca[1] - cb[1])}
    moved_out_at_contact = sorted(k for k, v in after.items() if v < 0)
    moved_out_past = sorted(k for k, v in after_past.items() if v < 0)
    sq1 = clear[1]
    right_contacts = [i for i, c in clear.items() if c["right"] == 0]
    out = {
        "n": w.n,
        "side": f"{w.side[0]}/{w.side[1]}",
        "side_denominator_digits": len(str(w.side[1])),
        "ceil12": str(ceil12),
        "floor12": str(floor12),
        "drop_to_floor12": float(drop),
        "s1c_squares_below_drop": s1c,
        "far_wall_contacts": far_contacts,
        "all_contacts": chk["wall_contacts"],
        "least_positive_clearance": float(least_pos),
        "any_positive_clearance_below_1e-30": least_pos < Fraction(1, 10**30),
        "square1_contacts": [wl for wl, v in sq1.items() if v == 0],
        "right_wall_contacts": right_contacts,
        "least_pair": lp,
        "least_pair_margin": chk["least_pair_margin"]["float"],
        "least_pair_closing_parameter": float(t),
        "least_pair_closing_move": float(t) * dist,
        "moved_square": lp[1],
        "moved_square_least_other_margin": moved_least_other_margin,
        "moved_square_least_wall_clearance": moved_least_wall,
        "moved_square_walls": moved_walls,
        "moved_square_outside_at_contact": moved_out_at_contact,
        "moved_square_outside_past": moved_out_past,
        "pairs_below_1e-12": chk["pairs_below_1e-12"],
        "programs": C.program_digests(),
    }
    Path(argv[3]).write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({k: v for k, v in out.items() if k not in ("side", "programs")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
