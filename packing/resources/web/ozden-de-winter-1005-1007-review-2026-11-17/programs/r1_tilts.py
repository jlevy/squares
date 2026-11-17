"""List a certificate's tilts.  It decides nothing.

Lane R1, stage 4 review of #1005, #1006 and #1007.  Clean-room.

    python -I -B r1_tilts.py FILE FORM OUT.json

Written after the checker and the controls plan were frozen and before the findings
were frozen, to say how far the squares the issues call axis-aligned are from
upright; it is not in the checker's digest list.  A square's tilt is its turn from
upright in (-45, 45] degrees, printed from the binary64 arctangent of its exact
direction; "exactly upright" is decided on the exact rationals.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_describe  # noqa: E402
import r1_fmt  # noqa: E402
import r1_frame  # noqa: E402
import r1_read  # noqa: E402


def main(argv):
    if len(argv) != 4:
        raise SystemExit(__doc__)
    path, form, out_path = argv[1:]
    packing, _ = r1_read.read_file(path, form)
    frames = r1_frame.of_packing(packing)
    rows = []
    for k, f in enumerate(frames):
        if r1_describe.exactly_upright(f.u):
            rows.append((0.0, k + 1, True))
        else:
            rows.append((r1_describe.tilt_degrees(f.u), k + 1, False))
    small = sorted((abs(t), k) for t, k, exact in rows if not exact and abs(t) < 1.0)
    large = sorted((t, k) for t, k, exact in rows if abs(t) >= 1.0)
    decades = {}
    for t, _ in small:
        exponent = -30
        while 10.0 ** (exponent + 1) <= t:
            exponent += 1
        key = f"1e{exponent} to 1e{exponent + 1}"
        decades[key] = decades.get(key, 0) + 1
    receipt = {
        "program": "r1_tilts.py",
        "lane": "R1 (c-review-1005-1117)",
        "decides": "nothing",
        "file": os.path.basename(path),
        "n": packing.n,
        "exactly_upright": sum(1 for _, _, exact in rows if exact),
        "turned_below_1_degree": {
            "count": len(small),
            "least_degrees": f"{small[0][0]:.6e}" if small else None,
            "greatest_degrees": f"{small[-1][0]:.6e}" if small else None,
            "greatest_at_square": small[-1][1] if small else None,
            "median_degrees": f"{small[len(small) // 2][0]:.6e}" if small else None,
            "by_decade_of_degrees": decades,
            "ten_greatest": [[k, f"{t:.6e}"] for t, k in small[-10:]],
        },
        "turned_beyond_1_degree": {
            "count": len(large),
            "positive": sum(1 for t, _ in large if t > 0),
            "negative": sum(1 for t, _ in large if t < 0),
            "least_degrees": round(min(abs(t) for t, _ in large), 6) if large else None,
            "greatest_degrees": round(max(abs(t) for t, _ in large), 6) if large else None,
            "tilts": [[k, round(t, 6)] for t, k in large],
        },
    }
    r1_fmt.write_json(out_path, receipt)
    print("TILTS", receipt["file"], receipt["exactly_upright"], receipt["turned_below_1_degree"]["count"],
          receipt["turned_below_1_degree"]["greatest_degrees"], receipt["turned_beyond_1_degree"]["count"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
