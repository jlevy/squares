"""Whether the 295 certificate is the 262 certificate in an L border. Decides nothing.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Written after the checker
and the controls plan were frozen and before the findings were; it is not in the frozen
checker list.

    python -I -B rv1009_lstep.py CERT_262 CERT_295 OUT.json

An L-shaped border of width 1 about a box of side S holds 2*floor(S) + 1 unit squares,
so a packing of 262 squares at a side between 16 and 17 gives one of 295 at that side
plus 1. This program asks whether the 295 certificate is such a packing: for each of the
four corners the inner box can sit in, it pairs every square of the 262 certificate,
moved by that offset, with the nearest square of the 295 certificate, and reports how
far the pairs lie apart, whether the pairing is one to one, and what the 33 squares left
over are. Centres are compared exactly; the nearest square is found in binary64.
"""

from __future__ import annotations

import json
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1009_reader as reader  # noqa: E402

F = Fraction


def sci(value: Fraction, digits: int = 9) -> str:
    return f"{float(value):.{digits - 1}e}"


def main(argv: list[str]) -> int:
    small_path, large_path, out_path = argv[1:4]
    started = time.process_time()
    small = reader.read_cert(Path(small_path).read_bytes())
    large = reader.read_cert(Path(large_path).read_bytes())
    a = [tuple(F(*v) for v in row) for row in small["poses"]]
    b = [tuple(F(*v) for v in row) for row in large["poses"]]
    sa, sb = F(*small["side"]), F(*large["side"])
    bf = [(float(x), float(y)) for x, y, _t in b]
    offsets = {
        "inner box at the lower left": (F(0), F(0)),
        "inner box at the lower right": (sb - sa, F(0)),
        "inner box at the upper left": (F(0), sb - sa),
        "inner box at the upper right": (sb - sa, sb - sa),
    }
    results = {}
    best_name = None
    best_worst = None
    for name, (dx, dy) in offsets.items():
        pairs = []
        for x, y, t in a:
            fx, fy = float(x + dx), float(y + dy)
            k = min(range(len(b)), key=lambda m: (bf[m][0] - fx) ** 2 + (bf[m][1] - fy) ** 2)
            ddx, ddy = b[k][0] - x - dx, b[k][1] - y - dy
            pairs.append((k, ddx, ddy, b[k][2] - t))
        used = [k for k, _dx, _dy, _dt in pairs]
        one_to_one = len(set(used)) == len(used)
        d2 = [ddx * ddx + ddy * ddy for _k, ddx, ddy, _dt in pairs]
        worst = max(d2)
        shifts_x = sorted({ddx for _k, ddx, _dy, _dt in pairs})
        shifts_y = sorted({ddy for _k, _dx, ddy, _dt in pairs})
        rest = sorted(set(range(len(b))) - set(used))
        results[name] = {
            "offset": [sci(dx, 12), sci(dy, 12)],
            "one_to_one": one_to_one,
            "largest_centre_distance_squared": sci(worst),
            "squares_moved_beyond_1e-18": sum(1 for v in d2 if v > F(1, 10**36)),
            "squares_moved_beyond_1e-9": sum(1 for v in d2 if v > F(1, 10**18)),
            "squares_moved_beyond_1e-3": sum(1 for v in d2 if v > F(1, 10**6)),
            "distinct_x_shifts": len(shifts_x),
            "distinct_y_shifts": len(shifts_y),
            "x_shift_range": [sci(shifts_x[0], 12), sci(shifts_x[-1], 12)],
            "y_shift_range": [sci(shifts_y[0], 12), sci(shifts_y[-1], 12)],
            "tangents_equal": sum(1 for _k, _dx, _dy, dt in pairs if dt == 0),
            "largest_tangent_difference": sci(max(abs(dt) for _k, _dx, _dy, dt in pairs)),
            "left_over": len(rest),
            "left_over_upright": sum(1 for k in rest if b[k][2] in (0, 1, -1)),
            "left_over_squares": [k + 1 for k in rest],
            "left_over_centres": [[round(float(b[k][0]), 6), round(float(b[k][1]), 6)] for k in rest],
        }
        if one_to_one and (best_worst is None or worst < best_worst):
            best_worst, best_name = worst, name
    receipt = {
        "program": "rv1009_lstep.py",
        "lane": "c-review-1009-1117",
        "decides": "nothing",
        "small": {"n": small["n"], "side": f"{small['side'][0]}/{small['side'][1]}"},
        "large": {"n": large["n"], "side": f"{large['side'][0]}/{large['side'][1]}"},
        "large_side_less_small_side_less_one": f"{(sb - sa - 1).numerator}/{(sb - sa - 1).denominator}",
        "large_side_less_small_side_less_one_sci": sci(sb - sa - 1, 12),
        "squares_an_l_border_holds": 2 * int(sa) + 1,
        "best_one_to_one_offset": best_name,
        "offsets": results,
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n", encoding="ascii")
    sys.stdout.write(f"best={best_name} cpu={receipt['cpu_seconds']}s\n")
    for name, r in results.items():
        sys.stdout.write(
            f"  {name}: one_to_one={r['one_to_one']} worst_d2={r['largest_centre_distance_squared']} "
            f"moved>1e-9={r['squares_moved_beyond_1e-9']} tangents_equal={r['tangents_equal']} "
            f"left_over_upright={r['left_over_upright']}/{r['left_over']}\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
