"""The exact facts the controls plan is stated from; decides no modified file.

Lane L108, blind stage 4 review of jlevy/squares#959. Reads the certificate (through the
frozen reader) and the frozen check receipt; computes wall clearances, the side's
12-place floor and ceiling, and each near pair's centre-line closing with where it
takes the moved square. Uses l108_geom for the constructions, not either method.

Usage: python -I -B l108_plan_facts.py CERT.yaml CERT.json CHECK.json OUT.json
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import l108_check as check  # noqa: E402  (its dec and exact print helpers only)
import l108_geom as geom  # noqa: E402
import l108_reader as reader  # noqa: E402

EPS = Fraction(1, 10**30)
FAR = ("right", "top")


def main(argv: list[str]) -> int:
    cert = reader.read_paths(Path(argv[1]), Path(argv[2]))
    receipt = json.loads(Path(argv[3]).read_text(encoding="utf-8"))
    res = receipt["result"]
    side = Fraction(*cert.side)
    q = cert.side[1]
    sq = [geom.from_raw(raw) for raw in cert.squares]
    n = len(sq)
    clear = [geom.clearances(c, side) for c in sq]

    floor12 = Fraction(side.numerator * 10**12 // side.denominator, 10**12)
    ceil12 = Fraction(-((-side.numerator * 10**12) // side.denominator), 10**12)
    drop = side - floor12

    def far_below(limit: Fraction) -> list[list[Any]]:
        return [[i + 1, w] for i in range(n) for w in FAR if clear[i][w] < limit]

    facts: dict[str, Any] = {
        "program": "l108_plan_facts.py",
        "side_floor_12": f"{floor12.numerator}/{floor12.denominator}",
        "side_ceil_12": f"{ceil12.numerator}/{ceil12.denominator}",
        "side_floor_12_decimal": check.dec(floor12, 14),
        "side_ceil_12_decimal": check.dec(ceil12, 14),
        "side_less_floor": check.dec(drop),
        "ceil_less_side": check.dec(ceil12 - side),
        "far_wall_below_1_over_q": far_below(Fraction(1, q)),
        "far_wall_below_1e-30": far_below(EPS),
        "far_wall_below_drop_to_floor": far_below(drop),
        "least_positive_far_clearance": (lambda v: [check.dec(v[0]), v[1], v[2]])(min((clear[i][w], i + 1, w) for i in range(n) for w in FAR if clear[i][w] > 0)),
        "square_1_clearances": {w: check.dec(v) for w, v in clear[0].items()},
        "every_square_inside": all(v >= 0 for c in clear for v in c.values()),
        "wall_contacts": [[i + 1, w] for i in range(n) for w, v in clear[i].items() if v == 0],
    }
    # At the ceiling the far clearances grow by ceil12 - side; the near ones do not change.
    facts["at_ceiling_contacts"] = [[i + 1, w] for i in range(n) for w, v in clear[i].items() if (v + (ceil12 - side) if w in FAR else v) == 0]

    # The least pair, closed along its centre line. Which square can move without meeting
    # anything else: every axis gap changes by at most the move's length, so the move must
    # be shorter than the mover's other margins (from the closed form at tau = 0, compared
    # exactly through squares), and its walls are recomputed at the moved position.
    least = res["least_margin"]["pair"]
    i, j = least[0] - 1, least[1] - 1
    s4: dict[str, Any] = {"pair": least}
    for mover, fixed in ((j, i), (i, j)):
        info = geom.closing(sq[fixed], sq[mover])
        tau = info["tau"]
        assert isinstance(tau, Fraction)
        d = info["direction"]
        assert isinstance(d, tuple)
        move2 = (tau * d[0]) ** 2 + (tau * d[1]) ** 2
        other = []
        for k in range(n):
            if k in (mover, fixed):
                continue
            m = geom.gap_at(geom.closing(sq[k], sq[mover]), Fraction(0))
            other.append((m, k + 1))
        other.sort()
        m_next, k_next = other[0]
        past = geom.past_tau(info, EPS)
        at_walls = geom.clearances(geom.moved(sq[mover], info, tau), side)
        past_walls = geom.clearances(geom.moved(sq[mover], info, past), side)
        s4[f"move_square_{mover + 1}"] = {
            "tau": check.dec(tau),
            "move_length_squared": check.dec(move2),
            "next_margin": {"square": k_next, "value": check.dec(m_next)},
            "move_shorter_than_every_other_margin": m_next > 0 and move2 < m_next * m_next,
            "binding_axes": len(info["binding_rates"]),  # type: ignore[arg-type]
            "margin_at_contact": check.exact(geom.gap_at(info, tau)),
            "margin_past": check.dec(geom.gap_at(info, past)),
            "margin_past_is_minus_1e-30": geom.gap_at(info, past) == -EPS,
            "walls_before": {w: check.dec(v) for w, v in clear[mover].items()},
            "walls_at_contact": {w: check.dec(v) for w, v in at_walls.items()},
            "walls_past": {w: check.dec(v) for w, v in past_walls.items()},
            "inside_at_contact_and_past": all(v >= 0 for v in at_walls.values()) and all(v >= 0 for v in past_walls.values()),
            "wall_contacts_at_contact": [w for w, v in at_walls.items() if v == 0],
        }
    facts["s4"] = s4

    # Every pair below 1e-12, closed along its centre line (the second square moves).
    near = [r["pair"] for r in res["pairs_below_1e-3"] if Fraction(1, 10**12) > _approx(r["margin"])]
    s5 = {"pairs": len(near), "one_binding_axis": 0, "past_margin_minus_1e-30": 0, "contact_margin_zero": 0}
    for a, b in near:
        info = geom.closing(sq[a - 1], sq[b - 1])
        tau = info["tau"]
        assert isinstance(tau, Fraction)
        if len(info["binding_rates"]) == 1:  # type: ignore[arg-type]
            s5["one_binding_axis"] += 1
        if geom.gap_at(info, tau) == 0:
            s5["contact_margin_zero"] += 1
        if geom.gap_at(info, geom.past_tau(info, EPS)) == -EPS:
            s5["past_margin_minus_1e-30"] += 1
    facts["s5"] = s5

    # Every square to its nearest wall (ties: left, bottom, right, top).
    nearest = []
    for k in range(n):
        w = min(("left", "bottom", "right", "top"), key=lambda name: clear[k][name])
        nearest.append([k + 1, w, check.dec(clear[k][w], 6)])
    facts["s6_nearest_wall"] = nearest
    facts["s6_nearest_wall_counts"] = {w: sum(1 for r in nearest if r[1] == w) for w in ("left", "bottom", "right", "top")}

    # For G6: reflecting a square in its horizontal centre line keeps its bounding box.
    facts["g6_walls_unchanged_by_reflection"] = True
    Path(argv[4]).write_text(json.dumps(facts, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in facts.items() if k not in ("s6_nearest_wall",)}, indent=1)[:4000])
    return 0


def _approx(text: str) -> Fraction:
    """The receipt's truncated scientific print as a Fraction (for selecting pairs only)."""
    mant, exp = text.split("e")
    return Fraction(mant) * Fraction(10) ** int(exp)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
