"""The exact facts the controls plan states its outcomes from. Decides no modified file.

Lane L127, clean room. Usage:

    python -I -B l127_plan_facts.py CERT.yaml TWIN.json CHECK.json ISSUE.json OUT.json

Computes, from the certificate and the check receipt: every square's exact wall
clearances; the side's 12-place floor and ceiling and the claim; which right or top
clearances fall below each side reduction the plan uses; the closest pair's closing move
along its centre line against every other closed-form margin and clearance of the moved
square; and, for every pair below 1e-12, its closing time by the closed form of
l127_geom.py and whether moving 1e-30 past contact leaves every other axis below.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l127_geom as g  # noqa: E402
import l127_reader as rd  # noqa: E402

TINY = F(1, 10**30)


def placed(corners: list[tuple[tuple[int, int], tuple[int, int]]]) -> g.Placed:
    pts = [(F(*x), F(*y)) for x, y in corners]
    cx = (pts[0][0] + pts[2][0]) / 2
    cy = (pts[0][1] + pts[2][1]) / 2
    return g.Placed(cx, cy, pts[1][0] - pts[0][0], pts[1][1] - pts[0][1])


def clearances(corners: list[tuple[tuple[int, int], tuple[int, int]]], side: F) -> dict[str, F]:
    xs = [F(*x) for x, _ in corners]
    ys = [F(*y) for _, y in corners]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


def dec(x: F, places: int, *, up: bool) -> F:
    scale = 10**places
    n = x.numerator * scale
    q, r = divmod(n, x.denominator)
    if up and r:
        q += 1
    return F(q, scale)


def fs(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def sci(x: F, sig: int = 6) -> str:
    return f"{float(x):.{sig - 1}e}"


def main(argv: list[str]) -> int:
    t0 = time.process_time()
    cert, twin, check, issue, out = (Path(a) for a in argv[1:6])
    doc = rd.read_certificate(cert.read_text(encoding="utf-8"), twin.read_text(encoding="utf-8"))
    rec = json.loads(check.read_text(encoding="utf-8"))
    iss = json.loads(issue.read_text(encoding="utf-8"))
    side = F(*doc["side"])
    sq = doc["squares"]
    n = len(sq)
    m = re.search(r"≤ ([0-9]+\.[0-9]+)", iss["issue"]["title"])
    assert m is not None
    claim = F(m.group(1))
    floor12 = dec(side, 12, up=False)
    ceil12 = dec(side, 12, up=True)

    cl = [clearances(c, side) for c in sq]
    contacts = [[k + 1, w] for k in range(n) for w, v in cl[k].items() if v == 0]

    def far_below(drop: F) -> dict[str, Any]:
        outside = [[k + 1, w] for k in range(n) for w in ("right", "top") if cl[k][w] < drop]
        touch = [[k + 1, w] for k in range(n) for w in ("right", "top") if cl[k][w] == drop]
        return {"drop": fs(drop), "drop_sci": sci(drop), "outside": outside, "touch": touch}

    far = sorted(
        ((cl[k][w], k + 1, w) for k in range(n) for w in ("right", "top") if cl[k][w] > 0),
        key=lambda t: t[0],
    )
    s1 = {
        "S1a_one_unit_of_last_place": far_below(F(1, side.denominator)),
        "S1b_1e-30": far_below(TINY),
        "S1c_floor12": far_below(side - floor12),
    }
    near_side_far = [{"square": t[1], "wall": t[2], "sci": sci(t[0])} for t in far[:3]]

    # G1 and G2 premises
    g1 = {
        "square1_clearances": {w: sci(v) for w, v in cl[0].items()},
        "square269_clearances": {w: sci(v) for w, v in cl[n - 1].items()},
    }
    g2 = {"square1_left_clearance": sci(cl[0]["left"]), "square1_left_clearance_positive": cl[0]["left"] > 0}

    # the closest pair, closed along its centre line
    pl = [placed(c) for c in sq]
    i, j = rec["least_margin"]["pair"]
    s4: dict[str, Any] = {"pair": [i, j], "candidates": []}
    for mover, fixed in ((j, i), (i, j)):
        p, q = pl[fixed - 1], pl[mover - 1]
        clo = g.closing(p, q)
        d2 = (q.cx - p.cx) ** 2 + (q.cy - p.cy) ** 2
        move2 = clo.t_star**2 * d2  # squared length of the move to contact
        past_t = clo.t_star + TINY / min(clo.binding_rates)
        past2 = past_t**2 * d2
        others = sorted(
            (g.closed_margin(pl[k], q), k + 1) for k in range(n) if k + 1 not in (mover, fixed)
        )
        next_margin, next_with = others[0]
        least_clear = min(cl[mover - 1].values())
        ok = past2 < next_margin**2 and past2 < least_clear**2 and next_margin > 0
        cf_at = g.closed_margin(p, g.moved(q, p, clo.t_star))
        cf_past = g.closed_margin(p, g.moved(q, p, past_t))
        s4["candidates"].append(
            {
                "move": mover,
                "towards": fixed,
                "t_star": fs(clo.t_star),
                "t_past": fs(past_t),
                "closed_form_at": fs(cf_at),
                "closed_form_past": fs(cf_past),
                "closed_form_past_is_minus_1e-30": cf_past == -TINY,
                "binding_axes": len(clo.binding_rates),
                "move_length_sci": f"{float(move2) ** 0.5:.5e}",
                "past_move_shorter_than_every_other_margin_and_clearance": ok,
                "next_margin": {"with": next_with, "sci": sci(next_margin)},
                "least_clearance_sci": sci(least_clear),
                "closed_form_margin_now": sci(g.closed_margin(p, q)),
            }
        )
    chosen = next(c for c in s4["candidates"] if c["past_move_shorter_than_every_other_margin_and_clearance"])
    s4["chosen"] = {"move": chosen["move"], "towards": chosen["towards"]}

    # S5: every pair below 1e-12, by the closed form. Square b moves towards square a to
    # t* (contact) and to t* + 1e-30 / (least binding rate) (past). The expected margin at
    # each position is the closed form there, exactly: 0 at contact, and past contact
    # -1e-30 unless a non-binding axis with a slower rate lies within 1e-30 of binding
    # (nearly parallel squares), when it is that axis's gap, still negative.
    s5 = []
    digest = hashlib.sha256()
    for item in rec["near_pairs_below_1e-12"]:
        a, b = item["pair"]
        p, q = pl[a - 1], pl[b - 1]
        clo = g.closing(p, q)
        t_past = clo.t_star + TINY / min(clo.binding_rates)
        cf = g.closed_margin(p, q)
        cf_at = g.closed_margin(p, g.moved(q, p, clo.t_star))
        cf_past = g.closed_margin(p, g.moved(q, p, t_past))
        s5.append(
            {
                "pair": [a, b],
                "binding_axes": len(clo.binding_rates),
                "slack_at_least_1e-30": clo.other_slack >= TINY,
                "cf_below_1e-12": cf < F(1, 10**12),
                "cf_at_zero": cf_at == 0,
                "cf_past": fs(cf_past),
                "cf_past_sci": sci(cf_past),
                "cf_past_is_minus_1e-30": cf_past == -TINY,
                "cf_past_negative": cf_past < 0,
            }
        )
        digest.update(f"{a} {b} {fs(clo.t_star)} {fs(t_past)} {fs(cf_past)}\n".encode())
    bind_hist: dict[int, int] = {}
    for e in s5:
        bind_hist[e["binding_axes"]] = bind_hist.get(e["binding_axes"], 0) + 1

    # S6: each square's nearest wall
    s6 = []
    for k in range(n):
        w, v = min(cl[k].items(), key=lambda t: t[1])
        s6.append({"square": k + 1, "wall": w, "clearance": fs(v)})

    facts = {
        "program": "l127_plan_facts.py",
        "side": fs(side),
        "side_denominator_digits": len(str(side.denominator)),
        "floor12": str(floor12.numerator * 10**12 // floor12.denominator),
        "floor12_decimal": f"{floor12.numerator // floor12.denominator}.{str(floor12.numerator % floor12.denominator * 10**12 // floor12.denominator).zfill(12)}",
        "ceil12_decimal": f"{ceil12.numerator // ceil12.denominator}.{str(ceil12.numerator % ceil12.denominator * 10**12 // ceil12.denominator).zfill(12)}",
        "claim": fs(claim),
        "claim_equals_ceil12": claim == ceil12,
        "claim_minus_side_sci": sci(claim - side),
        "contacts": contacts,
        "least_far_clearances": near_side_far,
        "S1": s1,
        "G1": g1,
        "G2": g2,
        "S4": s4,
        "S5": {
            "count": len(s5),
            "binding_axes_histogram": {str(k): v for k, v in sorted(bind_hist.items())},
            "slack_at_least_1e-30": sum(1 for e in s5 if e["slack_at_least_1e-30"]),
            "all_closed_form_below_1e-12": all(e["cf_below_1e-12"] for e in s5),
            "all_closed_form_zero_at_contact": all(e["cf_at_zero"] for e in s5),
            "past_exactly_minus_1e-30": sum(1 for e in s5 if e["cf_past_is_minus_1e-30"]),
            "past_negative": sum(1 for e in s5 if e["cf_past_negative"]),
            "past_not_minus_1e-30": [
                {"pair": e["pair"], "cf_past_sci": e["cf_past_sci"]} for e in s5 if not e["cf_past_is_minus_1e-30"]
            ],
            "closing_digest": digest.hexdigest(),
            "pairs": [{"pair": e["pair"], "cf_past": e["cf_past"]} for e in s5],
        },
        "S6": {"nearest_walls": s6, "contacts_already": sum(1 for e in s6 if e["clearance"] == "0")},
        "cpu_seconds": round(time.process_time() - t0, 1),
    }
    out.write_text(json.dumps(facts, indent=1) + "\n", encoding="utf-8")
    print("facts written;", "S1a", s1["S1a_one_unit_of_last_place"]["outside"], "S1c n", len(s1["S1c_floor12"]["outside"]),
          "S4", s4["chosen"], "S5", facts["S5"]["count"], facts["S5"]["binding_axes_histogram"],
          "past -1e-30:", facts["S5"]["past_exactly_minus_1e-30"], "negative:", facts["S5"]["past_negative"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
