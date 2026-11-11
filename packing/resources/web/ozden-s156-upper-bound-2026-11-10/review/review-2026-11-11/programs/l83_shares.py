"""Each gain against its house certificate's uniform-contraction margin, exactly (review L83).

Usage: python -I -B l83_shares.py OUT_DIR OUT.json
"""

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l83_check as C  # noqa: E402


def main(argv):
    d, out = Path(argv[1]), Path(argv[2])
    sides = json.loads((d / "sides.json").read_text())["counts"]
    res = {}
    for n in (156, 180, 268, 269):
        h = json.loads((d / f"houses-n{n}.json").read_text())
        side = F(sides[str(n)]["side"])
        gain = F(h["house_side"]) - side
        margin = F(h["margin"])
        res[str(n)] = {
            "house": sides[str(n)]["house"],
            "gain": float(gain),
            "margin": float(margin),
            "margin_is_zero": margin == 0,
            "gain_over_margin": None if margin == 0 else float(gain / margin),
            "margin_share_of_gain": float(margin / gain),
            "gain_inside_margin": gain <= margin,
            "rv3_reaches": gain <= margin,
        }
        print(n, res[str(n)])
    doc = {"verdict": "NO_GAIN_INSIDE_ITS_HOUSE_MARGIN" if not any(r["gain_inside_margin"] for r in res.values()) else "SOME_GAIN_INSIDE_MARGIN", "counts": res, "programs": C.program_digests()}
    out.write_text(json.dumps(doc, indent=1) + "\n")
    print(doc["verdict"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
