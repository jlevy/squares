"""Hold the import lane's receipts to this review's, after the findings were frozen (L64).

Usage: python -I -B l64_compare_lane.py REPO_WORKTREE BRANCH OUT_DIR OUT.json

Written after the freeze of 2026-11-09T08:07:30Z. It reads lane L63's packets from the
branch with `git show` (read-only), as data, and compares, at each count:

- each maintained route's least pair gap and least containment clearance on the positive
  case of `receipts/exact-certification.json.xz` with this review's exact least margin
  and least clearance in `check-nNNN.json`, as exact fractions;
- `measure/identity.json`'s counts against the house with `identity-nNNN.json`;
- the README's print of the side.

It decides nothing about any certificate.
"""

from __future__ import annotations

import json
import lzma
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from l64_util import fixed, program_digests, write_receipt  # noqa: E402

HERE = Path(__file__).resolve().parent
COUNTS = (232, 268, 299, 303, 307)


def show(repo: str, ref: str, path: str) -> bytes:
    return subprocess.run(  # noqa: S603 - read-only git plumbing, no shell
        ["git", "-C", repo, "show", f"{ref}:{path}"],  # noqa: S607
        check=True,
        capture_output=True,
    ).stdout


def main(argv: list[str]) -> int:
    if len(argv) != 5:
        print(__doc__)
        return 2
    repo, ref, out_dir, out = argv[1], argv[2], Path(argv[3]), argv[4]
    rows = {}
    for n in COUNTS:
        packet = f"packing/resources/web/ozden-s{n}-upper-bound-2026-11-09"
        cert = json.loads(lzma.decompress(show(repo, ref, f"{packet}/receipts/exact-certification.json.xz")))
        positive = [c for c in cert["cases"] if c["control"] == "positive"]
        mine = json.loads((out_dir / f"check-n{n}.json").read_text())["decision"]
        my_gap = F(mine["pairs"]["least_margin"])
        my_clear = F(mine["walls"]["least_clearance"])
        routes = {}
        for case in positive:
            for route in ("exact_verify", "independent"):
                r = case[route]
                routes[route] = {
                    "passed": r["verification_passed"],
                    "pairs_tested": r["pairs_tested"],
                    "least_gap_equals_mine": F(r["minimum_best_pair_gap"]) == my_gap,
                    "least_clearance_equals_mine": F(r["minimum_containment_clearance"]) == my_clear,
                    "side_equals_mine": F(r["side"]) == F(mine["side"]),
                }
        ident = json.loads(show(repo, ref, f"{packet}/measure/identity.json"))
        my_id = json.loads((out_dir / f"identity-n{n}.json").read_text())["against_house"]
        lane_pairs = {p["against"]: p for p in ident["pairs"]}
        house_key = next((k for k in lane_pairs if k.startswith("T-")), None)
        lane = lane_pairs[house_key]["assignment"] if house_key else {}
        lane_nn = lane_pairs[house_key]["nearest_centre"] if house_key else {}
        ident_cmp = {
            "against": house_key,
            "lane_nearest_one_to_one": lane_nn.get("one_to_one"),
            "mine_nearest_one_to_one": my_id["nearest_one_to_one_under_best"],
            "moved_beyond_lane": lane.get("moved_beyond"),
            "moved_beyond_mine": {k: my_id["moved_beyond"][k] for k in ("1e-9", "1e-6", "1e-3", "1e-2", "0.1")},
            "largest_move_lane": lane.get("largest_move"),
            "largest_move_mine": my_id["largest_move"],
            "largest_turn_lane": lane.get("largest_turn_degrees"),
            "largest_turn_mine": round(my_id["largest_turn_deg_full"], 2),
            "turned_beyond_1e-6_lane": lane.get("turned_beyond_1e-6"),
            "turned_beyond_1e-6_rad_mine": my_id["turned_beyond_1e-6_rad"],
        }
        lm, mm = ident_cmp["moved_beyond_lane"] or {}, ident_cmp["moved_beyond_mine"]
        ident_cmp["counts_equal"] = (
            lm.get("1e-9") == mm["1e-9"]
            and lm.get("1e-6") == mm["1e-6"]
            and lm.get("1e-3") == mm["1e-3"]
            and lm.get("1e-2") == mm["1e-2"]
            and lm.get("1e-1") == mm["0.1"]
            and ident_cmp["turned_beyond_1e-6_lane"] == ident_cmp["turned_beyond_1e-6_rad_mine"]
            and ident_cmp["lane_nearest_one_to_one"] == ident_cmp["mine_nearest_one_to_one"]
        )
        readme = show(repo, ref, f"{packet}/README.md").decode("utf-8")
        m = re.search(r"states s\(\d+\) ≤ ([0-9.]+)(…?) rounded up at 16 places", readme)
        side = F(mine["side"])
        rows[str(n)] = {
            "routes_on_positive": routes,
            "identity_against_house": ident_cmp,
            "readme_side_print": (m.group(1) + m.group(2)) if m else None,
            "readme_print_is_ceil_16": bool(m) and m.group(1) == fixed(side, 16, "ceil"),
            "readme_print_has_ellipsis": bool(m) and m.group(2) == "…",
            "side_floor_17": fixed(side, 17, "floor"),
        }
    ok = all(
        all(v["passed"] and v["least_gap_equals_mine"] and v["least_clearance_equals_mine"] and v["side_equals_mine"] for v in r["routes_on_positive"].values())
        and r["identity_against_house"]["counts_equal"]
        for r in rows.values()
    )
    receipt = {
        "program": "l64_compare_lane.py",
        "programs_sha256": program_digests([HERE / "l64_compare_lane.py", HERE / "l64_util.py"]),
        "branch": ref,
        "head": subprocess.run(["git", "-C", repo, "rev-parse", ref], check=True, capture_output=True, text=True).stdout.strip(),  # noqa: S603, S607
        "counts": rows,
        "verdict": "LANE_EQUALS_REVIEW" if ok else "DIFFERENCES",
    }
    write_receipt(out, receipt)
    print(receipt["verdict"], receipt["head"][:12])
    for n, r in rows.items():
        print(n, {k: (v["least_gap_equals_mine"], v["least_clearance_equals_mine"]) for k, v in r["routes_on_positive"].items()}, "identity equal", r["identity_against_house"]["counts_equal"], "readme", r["readme_side_print"], "ceil16", r["readme_print_is_ceil_16"], "floor17", r["side_floor_17"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
