"""The houses on main decided by the frozen checker, and their exact scale slack (lane L64).

Usage: python -I -B l64_houses.py STATEMENTS.json HOUSE_DIR SIDES.json OUT.json

For each count it reads the house witness `n-NNN.yaml` with `l64_house.py`, writes its
squares as exact corners, and decides them at the house side with `l64_check.decide`
(both methods, every wall and pair). It then measures the house's scale slack exactly:
how far the side can fall when every centre is scaled about the lower-left corner by a
factor k <= 1, orientations kept.

With half-widths h_i(a) = (|u_i.a| + |w_i.a|)/2 along a unit edge direction a, a pair
stays apart while k |(c_j - c_i).a| >= h_i(a) + h_j(a) for one of its four axes, so it
needs k >= min over its axes of (h_i + h_j)/|(c_j - c_i).a|; the left and bottom walls
need k >= h_i(e)/c_i.e. The least feasible k* is the largest of these, and the scaled
packing needs the side max over squares of k* c_i.e + h_i(e) over e = x, y. The slack is
the house side less that. A gap above the slack cannot come from rescaling the house.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from l64_check import CHECKER, decide  # noqa: E402
from l64_house import as_int_corners, exact_corners, read_house  # noqa: E402
from l64_util import Clock, environment, frac_str, program_digests, sci, write_receipt  # noqa: E402

HERE = Path(__file__).resolve().parent


def frame(pts: list[tuple[F, F]]) -> tuple[tuple[F, F], tuple[F, F], tuple[F, F]]:
    (x0, y0), _, (x2, y2), _ = pts
    u = (pts[1][0] - x0, pts[1][1] - y0)
    w = (-u[1], u[0])
    return ((x0 + x2) / 2, (y0 + y2) / 2), u, w


def half(u: tuple[F, F], w: tuple[F, F], a: tuple[F, F]) -> F:
    return (abs(u[0] * a[0] + u[1] * a[1]) + abs(w[0] * a[0] + w[1] * a[1])) / 2


def scale_slack(squares: list[list[tuple[F, F]]], side: F) -> dict:
    frames = [frame(p) for p in squares]
    kstar = F(0)
    binding = None
    ex, ey = (F(1), F(0)), (F(0), F(1))
    for idx, (c, u, w) in enumerate(frames):
        for e, ce in ((ex, c[0]), (ey, c[1])):
            k = half(u, w, e) / ce
            if k > kstar:
                kstar, binding = k, ("wall", idx)
    n = len(frames)
    for i in range(n):
        ci, ui, wi = frames[i]
        for j in range(i + 1, n):
            cj, uj, wj = frames[j]
            dx, dy = cj[0] - ci[0], cj[1] - ci[1]
            need = None
            for a in (ui, wi, uj, wj):
                delta = abs(dx * a[0] + dy * a[1])
                if delta == 0:
                    continue
                k = (half(ui, wi, a) + half(uj, wj, a)) / delta
                if need is None or k < need:
                    need = k
            if need is not None and need > kstar:
                kstar, binding = need, ("pair", i, j)
    new_side = max(
        max(kstar * c[0] + half(u, w, ex), kstar * c[1] + half(u, w, ey)) for c, u, w in frames
    )
    return {
        "k_star": frac_str(kstar),
        "one_minus_k_star": sci(1 - kstar, 6),
        "binding": binding,
        "scaled_side": frac_str(new_side),
        "slack": frac_str(side - new_side),
        "slack_sci": sci(side - new_side, 6) if side != new_side else "0",
    }


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__)
        return 2
    statements = json.loads(Path(argv[1]).read_text())["counts"]
    house_dir, sides, out = Path(argv[2]), json.loads(Path(argv[3]).read_text())["counts"], argv[4]
    clock = Clock()
    rows = {}
    for n_text in statements:
        n = int(n_text)
        h = read_house(house_dir / f"n-{n:03d}.yaml", expected_n=n)
        side = F(*h["side"])
        corners = [exact_corners(sq) for sq in h["squares"]]
        res = decide([{"id": sq["id"], "corners": as_int_corners(p)} for sq, p in zip(h["squares"], corners, strict=True)], side, nearest=5)
        slack = scale_slack(corners, side)
        gap = F(sides[n_text]["gap"])
        rows[n_text] = {
            "house": h["path"],
            "house_sha256": h["sha256"],
            "representation": h["representation"],
            "side": frac_str(side),
            "verdict": res["verdict"],
            "pairs": res["pairs"]["decided_by_both"],
            "classes": res["pairs"]["classes"],
            "least_margin_sci": res["pairs"]["least_margin_sci"],
            "least_clearance_sci": res["walls"]["least_clearance_sci"],
            "wall_contacts": res["walls"]["contacts_by_wall"],
            "disagreements_A_B": len(res["disagreements_A_B"]),
            "scale_slack": slack,
            "gap": sci(gap, 6),
            "gap_over_slack": "unbounded (no slack)" if F(slack["slack"]) == 0 else sci(gap / F(slack["slack"]), 3),
        }
        print(n_text, res["verdict"], rows[n_text]["classes"], "least margin", rows[n_text]["least_margin_sci"], "walls", rows[n_text]["wall_contacts"], "slack", slack["slack_sci"], "gap/slack", rows[n_text]["gap_over_slack"])
    receipt = {
        "program": "l64_houses.py",
        "programs_sha256": program_digests([HERE / f for f in [*CHECKER, "l64_house.py", "l64_houses.py"]]),
        "environment": environment(),
        "counts": rows,
        "clock": clock.report(),
    }
    write_receipt(out, receipt)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
