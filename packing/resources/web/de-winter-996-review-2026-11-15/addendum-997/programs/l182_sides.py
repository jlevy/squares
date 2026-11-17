"""Lane L182: the arithmetic of #997's claim, its step from #996, and both against the padding.

Written for the addendum to lane L180's blind stage 4 review of issue #996, after the
controls on #997's certificate were run. It decides nothing about the bound. Every
number is exact (fractions); the contraction margins are read from the receipts of
``devtools.contraction_margin``, which this program does not recompute. It reuses
``l180_sides``'s helpers and ``l180_reader``, unchanged.

Usage: l182_sides.py JSON_997 JSON_996 DESCRIBE_997 FRONTIER_DIR HOUSE_WITNESS
       CONTRACTION_T303 CONTRACTION_997 CONTRACTION_996_AGAINST_997 OUT
"""

from __future__ import annotations

import json
import os
import sys
from fractions import Fraction as F
from typing import Any

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
L180 = os.path.normpath(os.path.join(HERE, "..", "..", "programs"))
sys.path.insert(0, L180)

import l180_reader as R  # noqa: E402
from l180_decide import fstr, sci  # noqa: E402
from l180_sides import case_bounds, dec, places  # noqa: E402

CLAIM_997 = F(9994038766610, 10**12)
CLAIM_996 = F(9994038857546, 10**12)
T303_PRINT = F(9998277166926, 10**12)


def margin(path: str) -> tuple[F, dict[str, Any]]:
    with open(path, encoding="utf-8") as fh:
        rec = json.load(fh)
    return F(rec["margin"]), rec


def main(argv: list[str]) -> int:
    if len(argv) != 10:
        print(__doc__)
        return 2
    j7, j6, desc, frontier, house_path, ct, c7, c67, out = argv[1:]
    r7 = R.read_json(j7)
    r6 = R.read_json(j6)
    S, S6 = r7.side, r6.side
    with open(desc, encoding="utf-8") as fh:
        width = F(json.load(fh)["extent"]["width_x"])
    with open(house_path, encoding="utf-8") as fh:
        t303 = R.scalar(str(yaml.safe_load(fh)["witness"]["side"]))
    m_t303, rec_t = margin(ct)
    m_997, rec_7 = margin(c7)
    m_996, rec_67 = margin(c67)
    res: dict[str, Any] = {"program": "l182_sides.py", "lane": "L182"}
    res["side"] = {
        "exact": fstr(S),
        "places_30": dec(S, 30),
        "ceil_12": dec(places(S, 12, True), 12),
        "floor_12": dec(places(S, 12, False), 12),
        "claim": dec(CLAIM_997, 12),
        "claim_is_ceil_12": CLAIM_997 == places(S, 12, True),
        "claim_minus_side": sci(CLAIM_997 - S),
        "side_minus_floor_12": sci(S - places(S, 12, False)),
        "extent": fstr(width),
        "side_minus_extent": sci(S - width),
        "side_is_extent_rounded_up_at_19_places": places(width, 19, True) == S,
        "side_is_extent_rounded_up_at_20_places": places(width, 20, True) == S,
    }
    step = S6 - S
    res["step_from_996"] = {
        "side_996": fstr(S6),
        "exact": fstr(step),
        "decimal": dec(step, 25),
        "approx": sci(step),
        "issue_print_9e-8_is_one_figure": f"{float(step):.0e}" == "9e-08",
        "claim_to_claim": dec(CLAIM_996 - CLAIM_997, 12),
        "below_996_floor_12": sci(places(S6, 12, False) - S),
        "996_claim_minus_996_side": sci(CLAIM_996 - S6),
    }
    gain = t303 - S
    res["gain_on_t303"] = {
        "t303_side": fstr(t303),
        "exact": fstr(gain),
        "decimal": dec(gain, 20),
        "approx": sci(gain),
        "relative": sci(gain / t303),
        "claim_to_claim": dec(T303_PRINT - CLAIM_997, 12),
        "three_figures": f"{float(gain):.3g}",
        "gain_996_exact": fstr(t303 - S6),
        "gain_997_less_gain_996": fstr(gain - (t303 - S6)),
        "on_grid_10": dec(10 - S, 20),
    }
    res["padding"] = {
        "t303_margin": {"exact": fstr(m_t303), "approx": sci(m_t303), "first_contact": rec_t["one_minus_lambda_star"], "pair": rec_t["binding_pair"]},
        "996_margin": {"exact": fstr(m_996), "approx": sci(m_996), "first_contact": rec_67["one_minus_lambda_star"], "pair": rec_67["binding_pair"]},
        "997_margin": {"exact": fstr(m_997), "approx": sci(m_997), "first_contact": rec_7["one_minus_lambda_star"], "pair": rec_7["binding_pair"]},
        "gain_on_t303_over_t303_margin": f"{float(gain / m_t303):.6g}",
        "gain_within_t303_margin": gain <= m_t303,
        "step_over_996_margin": f"{float(step / m_996):.6g}",
        "step_within_996_margin": step <= m_996,
        "step_over_997_margin": f"{float(step / m_997):.6g}",
        "996_margin_over_step": sci(m_996 / step),
        "step_over_gain_on_t303": sci(step / gain),
        "devtools_against": {"t303_vs_997": rec_t["against"], "996_vs_997": rec_67["against"]},
    }
    close = 0
    for i in range(r7.n):
        for k in range(i + 1, r7.n):
            dx = r7.poses[i].x - r7.poses[k].x
            dy = r7.poses[i].y - r7.poses[k].y
            if dx * dx + dy * dy < 2:
                close += 1
    res["pairs_with_centres_closer_than_sqrt2"] = close
    cases = case_bounds(frontier)
    near = []
    best: tuple[F, int, int] | None = None
    for m, c in cases.items():
        if m >= 90:
            continue
        j = max(0, round(float(S - c["side"])))
        for jj in (j - 1, j, j + 1):
            if jj < 0:
                continue
            d = S - (c["side"] + jj)
            if best is None or abs(d) < abs(best[0]):
                best = (d, m, jj)
            if abs(d) < F(1, 1000):
                near.append({"m": m, "j": jj, "difference": sci(d)})
    res["closed_forms"] = {"within_1e-3": near, "nearest": {"m": best[1], "j": best[2], "difference": sci(best[0])} if best else None, "cases_read": len(cases)}
    fl = S.numerator // S.denominator
    steps = []
    for w in range(1, 9):
        m = 90 + w * (2 * fl + w)
        c = cases.get(m)
        steps.append({"width": w, "count": m, "side": dec(S + w, 12), "reported": dec(c["side"], 12) if c else None, "improves": bool(c and S + w < c["side"]), "above_record_by": sci(S + w - c["side"]) if c else None})
    res["l_steps"] = steps
    res["monotonicity"] = {
        "below_90_reported_above_S": sorted(m for m, c in cases.items() if m < 90 and c["side"] > S),
        "above_90_reported_below_S": sorted(m for m, c in cases.items() if m > 90 and c["side"] < S),
    }
    res["record_90"] = {k: (fstr(v) if isinstance(v, F) else v) for k, v in cases.get(90, {}).items()}
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
        fh.write("\n")
    p = res["padding"]
    print(
        f"claim ceil12 {res['side']['claim_is_ceil_12']}; step {res['step_from_996']['approx']}; gain {res['gain_on_t303']['approx']}; "
        f"margins T-303 {p['t303_margin']['approx']}, #996 {p['996_margin']['approx']}, #997 {p['997_margin']['approx']}; "
        f"step/#996 margin {p['step_over_996_margin']}; close pairs {close}; closed forms {len(near)}; "
        f"L steps improving {[s['count'] for s in steps if s['improves']]}; monotonicity {res['monotonicity']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
