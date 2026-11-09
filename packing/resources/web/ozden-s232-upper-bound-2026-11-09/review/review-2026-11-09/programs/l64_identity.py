"""How each certificate pairs with its house and with the view it started from (lane L64).

Usage: python -I -B l64_identity.py STATEMENTS.json N CERT.yaml HOUSE.yaml VIEW.yaml.gz OUT.json

Decides nothing about any bound. Poses are taken exactly from each file (centre and edge
direction) and measured in binary64: the centre (p0 + p2)/2 and the angle of the edge
p1 - p0 for a corner file, the centre and basis for a centre-basis file, with angles
reduced modulo 90 degrees into [-45, 45).

Each reference packing (the house witness on main, and the regularized view the issues
say the search started from) is mapped by each of the eight symmetries of its own box,
[0, S_ref]^2, and compared with the certificate by nearest centres (one to one or not)
and by the optimal assignment of least summed squared move (SciPy's
linear_sum_assignment). Under the best symmetry it reports the moves beyond 1e-9 to
0.1, the largest move, the turns beyond 1e-6 radian and beyond 1 degree, the largest
turn, the squares tilted beyond 1 degree in each packing, and how many squares keep
their id. It then holds the issue's own lineage statement to those numbers.
"""

from __future__ import annotations

import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np  # noqa: E402
from scipy.optimize import linear_sum_assignment  # noqa: E402

from l64_house import read_house  # noqa: E402
from l64_reader import read_witness  # noqa: E402
from l64_util import Clock, environment, program_digests, write_receipt  # noqa: E402

HERE = Path(__file__).resolve().parent
MOVES = [("1e-9", 1e-9), ("1e-6", 1e-6), ("1e-3", 1e-3), ("1e-2", 1e-2), ("0.05", 0.05), ("0.1", 0.1)]


def wrap90(deg: float) -> float:
    """An angle in degrees reduced modulo 90 into [-45, 45)."""
    return (deg + 45.0) % 90.0 - 45.0


def poses(w: dict) -> tuple[list[int], np.ndarray, np.ndarray, F]:
    ids, cs, th = [], [], []
    for sq in w["squares"]:
        ids.append(sq["id"])
        if "corners" in sq:
            c = sq["corners"]
            x0, y0 = F(c[0][0], c[0][1]), F(c[0][2], c[0][3])
            x1, y1 = F(c[1][0], c[1][1]), F(c[1][2], c[1][3])
            x2, y2 = F(c[2][0], c[2][1]), F(c[2][2], c[2][3])
            cx, cy = (x0 + x2) / 2, (y0 + y2) / 2
            ux, uy = x1 - x0, y1 - y0
        else:
            cx, cy = F(sq["center"][0], sq["center"][1]), F(sq["center"][2], sq["center"][3])
            ux, uy = F(sq["basis"][0], sq["basis"][1]), F(sq["basis"][2], sq["basis"][3])
        cs.append((float(cx), float(cy)))
        th.append(wrap90(math.degrees(math.atan2(float(uy), float(ux)))))
    return ids, np.array(cs), np.array(th), F(*w["side"])


SYMS = {
    "identity": (lambda x, y, s: (x, y), 1),
    "quarter turn": (lambda x, y, s: (s - y, x), 1),
    "half turn": (lambda x, y, s: (s - x, s - y), 1),
    "three-quarter turn": (lambda x, y, s: (y, s - x), 1),
    "mirror x": (lambda x, y, s: (s - x, y), -1),
    "mirror y": (lambda x, y, s: (x, s - y), -1),
    "transpose": (lambda x, y, s: (y, x), -1),
    "anti-transpose": (lambda x, y, s: (s - y, s - x), -1),
}


def compare(cand: tuple, ref: tuple) -> dict:
    c_ids, c_c, c_t, _ = cand
    r_ids, r_c, r_t, r_s = ref
    s = float(r_s)
    n = len(c_ids)
    per_sym = {}
    best = None
    for name, (fn, sense) in SYMS.items():
        mx, my = fn(r_c[:, 0], r_c[:, 1], s)
        mapped = np.stack([mx, my], axis=1)
        d2 = ((c_c[:, None, :] - mapped[None, :, :]) ** 2).sum(axis=2)
        nearest = d2.argmin(axis=1)
        rows, cols = linear_sum_assignment(d2)
        cost = float(d2[rows, cols].sum())
        per_sym[name] = {
            "distinct_nearest": len(set(nearest.tolist())),
            "nearest_one_to_one": len(set(nearest.tolist())) == n,
            "assignment_cost": cost,
        }
        if best is None or cost < best[1]:
            best = (name, cost, mapped, sense, cols, nearest)
    assert best is not None
    name, cost, mapped, sense, cols, nearest = best
    moves = np.sqrt(((c_c - mapped[cols]) ** 2).sum(axis=1))
    ref_t = np.array([wrap90(sense * t) for t in r_t])[cols]
    turns = np.array([abs(wrap90(a - b)) for a, b in zip(c_t, ref_t, strict=True)])
    order = np.argsort(-moves)
    big = [
        {
            "id": c_ids[k],
            "ref_id": r_ids[cols[k]],
            "move": round(float(moves[k]), 6),
            "shift": [round(float(c_c[k, 0] - mapped[cols[k], 0]), 6), round(float(c_c[k, 1] - mapped[cols[k], 1]), 6)],
            "centre": [round(float(c_c[k, 0]), 4), round(float(c_c[k, 1]), 4)],
            "angle_ref": round(float(ref_t[k]), 3),
            "angle_new": round(float(c_t[k]), 3),
        }
        for k in order
        if moves[k] > 0.05
    ]
    retilt = [
        {
            "id": c_ids[k],
            "ref_id": r_ids[cols[k]],
            "turn_deg": round(float(turns[k]), 3),
            "turn_deg_full": float(turns[k]),
            "centre": [round(float(c_c[k, 0]), 4), round(float(c_c[k, 1]), 4)],
            "angle_ref": round(float(ref_t[k]), 3),
            "angle_new": round(float(c_t[k]), 3),
            "move": round(float(moves[k]), 6),
        }
        for k in np.argsort(-turns)
        if turns[k] > 1.0
    ]
    return {
        "per_symmetry": per_sym,
        "best_symmetry": name,
        "nearest_one_to_one_under_best": len(set(nearest.tolist())) == n,
        "assignment_is_nearest": bool((cols == nearest).all()),
        "moved_beyond": {label: int((moves > v).sum()) for label, v in MOVES},
        "within_0.05": int((moves <= 0.05).sum()),
        "largest_move": round(float(moves.max()), 6),
        "largest_move_id": c_ids[int(moves.argmax())],
        "turned_beyond_1e-6_rad": int((turns > math.degrees(1e-6)).sum()),
        "turned_beyond_1_deg": int((turns > 1.0).sum()),
        "largest_turn_deg": round(float(turns.max()), 3),
        "largest_turn_deg_full": float(turns.max()),
        "tilted_beyond_1_deg_new": int((np.abs(c_t) > 1.0).sum()),
        "tilted_beyond_1_deg_ref": int((np.abs(r_t) > 1.0).sum()),
        "tilted_by_threshold_deg": {
            str(thr): [int((np.abs(c_t) > thr).sum()), int((np.abs(r_t) > thr).sum())]
            for thr in (math.degrees(1e-9), math.degrees(1e-6), 0.01, 0.1, 0.5, 1.0, 2.0, 5.0)
        },
        "same_id": int(sum(1 for k in range(n) if c_ids[k] == r_ids[cols[k]])),
        "moved_beyond_0.05": big,
        "retilted_beyond_1_deg": retilt,
    }


def main(argv: list[str]) -> int:
    if len(argv) != 7:
        print(__doc__)
        return 2
    statements = json.loads(Path(argv[1]).read_text())["counts"]
    n = int(argv[2])
    cert, house_path, view_path, out = argv[3], argv[4], argv[5], argv[6]
    clock = Clock()
    cand = poses(read_witness(cert, expected_n=n))
    house_w = read_house(house_path, expected_n=n)
    view_w = read_house(view_path, expected_n=n)
    house, view = poses(house_w), poses(view_w)
    against_house = compare(cand, house)
    against_view = compare(cand, view)
    view_vs_house = compare(view, house)
    said = statements[str(n)]["lineage"]
    held = {}
    for label, cmp in (("house", against_house), ("view", against_view)):
        held[label] = {
            "moved_1e-3": [said["moved_1e-3"], cmp["moved_beyond"]["1e-3"]],
            "moved_0.05": [said["moved_0.05"], cmp["moved_beyond"]["0.05"]],
            "largest_move": [said["largest_move"], cmp["largest_move"]],
            "retilted_1deg": [said["retilted_1deg"], cmp["turned_beyond_1_deg"]],
            "largest_retilt_deg": [said["largest_retilt_deg"], cmp["largest_turn_deg"]],
            "tilted_new": [said["tilted_new"], cmp["tilted_beyond_1_deg_new"]],
            "tilted_house": [said["tilted_house"], cmp["tilted_beyond_1_deg_ref"]],
        }
    receipt = {
        "program": "l64_identity.py",
        "programs_sha256": program_digests(
            [HERE / f for f in ("l64_identity.py", "l64_house.py", "l64_reader.py", "l64_util.py")]
        ),
        "environment": environment(),
        "numpy": np.__version__,
        "n": n,
        "certificate_sha256": read_witness(cert, expected_n=n)["sha256"],
        "house": {"path": house_path, "sha256": house_w["sha256"], "id": house_w["id"], "representation": house_w["representation"]},
        "view": {"path": view_path, "sha256": view_w["sha256"], "id": view_w["id"], "representation": view_w["representation"]},
        "against_house": against_house,
        "against_view": against_view,
        "view_against_house": view_vs_house,
        "issue_statement_against_measured": held,
        "clock": clock.report(),
    }
    write_receipt(out, receipt)
    for label, cmp in (("house", against_house), ("view", against_view), ("view-vs-house", view_vs_house)):
        print(
            f"n={n} {label:13s} best {cmp['best_symmetry']:18s} 1:1 {cmp['nearest_one_to_one_under_best']} "
            f"moved {cmp['moved_beyond']} largest {cmp['largest_move']} turned>1deg {cmp['turned_beyond_1_deg']} "
            f"max turn {cmp['largest_turn_deg']} tilted {cmp['tilted_beyond_1_deg_new']}/{cmp['tilted_beyond_1_deg_ref']} same id {cmp['same_id']}"
        )
    print("  issue vs measured (house, view):", {k: (held["house"][k], held["view"][k][1]) for k in held["house"]})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
