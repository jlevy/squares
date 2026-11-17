"""Lane L182: the controls plan's facts for #997's certificate, by L180's rules, the claim re-targeted.

Written for the addendum to lane L180's blind stage 4 review of issue #996, on the
replacement certificate of issue #997. It imports nothing from this repository or the
source. It runs ``l180_plan_facts.main``, unchanged, into SCRATCH; that program states
#996's claim (9.994038857546) and its 12-place floor (9.994038857545) as constants. This
program then replaces exactly the six S1 fields that depend on those two constants with
the same expressions evaluated at #997's printed claim (9.994038766610) and its floor
(9.994038766609), from the closed form of ``l180_geom`` (corner projections), the
formulation L180's program uses. It runs neither method. Every replaced field is kept
under ``l182_retargeted`` with L180's value beside it.

Usage: l182_plan_facts.py JSON TWIN CHECK_RECEIPT SCRATCH OUT
"""

from __future__ import annotations

import json
import os
import sys
import time
from fractions import Fraction as F
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
L180 = os.path.normpath(os.path.join(HERE, "..", "..", "programs"))
sys.path.insert(0, L180)

import l180_geom as G  # noqa: E402
import l180_plan_facts as PF  # noqa: E402
import l180_reader as R  # noqa: E402
from l180_decide import fstr, sci  # noqa: E402

CLAIM = F(9994038766610, 10**12)  # issue #997, as printed
FLOOR12 = F(9994038766609, 10**12)


def places(v: F, k: int, up: bool) -> F:
    q = v * 10**k
    n = -((-q.numerator) // q.denominator) if up else q.numerator // q.denominator
    return F(n, 10**k)


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    jpath, tpath, cpath, scratch, out = argv[1:]
    t0 = time.process_time()
    rc = PF.main(["l180_plan_facts.py", jpath, tpath, cpath, scratch])
    if rc != 0:
        return rc
    with open(scratch, encoding="utf-8") as fh:
        facts: dict[str, Any] = json.load(fh)
    r = R.read_json(jpath)
    side = r.side
    rt: dict[tuple[int, str], F] = {}
    for i, p in enumerate(r.poses, start=1):
        for w, c in G.clearances(p, side).items():
            if w in ("right", "top"):
                rt[(i, w)] = c
    new = {
        "claim": fstr(CLAIM),
        "claim_minus_side": sci(CLAIM - side),
        "claim_at_least_side": CLAIM >= side,
        "floor12": fstr(FLOOR12),
        "side_minus_floor12": sci(side - FLOOR12),
        "right_top_below_side_minus_floor12": sorted([[i, w] for (i, w), v in rt.items() if v < side - FLOOR12]),
    }
    s1 = facts["S1"]
    facts["l182_retargeted"] = {
        "why": "l180_plan_facts.py states #996's claim and floor as constants; #997 claims 9.994038766610",
        "claim_is_ceil_12_of_side": CLAIM == places(side, 12, True),
        "floor12_is_floor_12_of_side": FLOOR12 == places(side, 12, False),
        "S1": {k: {"l180": s1[k], "l182": v} for k, v in new.items()},
    }
    s1.update(new)
    facts["program"] = "l182_plan_facts.py (l180_plan_facts.py unchanged; S1's claim and floor re-targeted)"
    facts["lane"] = "L182"
    facts["cpu_seconds"] = round(time.process_time() - t0, 2)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(facts, fh, indent=1)
        fh.write("\n")
    rt_ = facts["l182_retargeted"]
    print(
        f"re-targeted S1: claim {new['claim']} (ceil 12 {rt_['claim_is_ceil_12_of_side']}), "
        f"floor {new['floor12']} (floor 12 {rt_['floor12_is_floor_12_of_side']}); "
        f"claim - side {new['claim_minus_side']}; side - floor {new['side_minus_floor12']}; "
        f"right/top below side - floor {len(new['right_top_below_side_minus_floor12'])}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
