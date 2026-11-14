"""Lane L163 converter, after the freeze: a decimal centre-angle Witness/v2 file to the
`binary64-xyd` text that `devtools.measure_identity` reads (`n side`, then `x y degrees`).

Usage: l163_convert.py WITNESS.yaml[.gz] OUT.txt

Decides nothing. The centres and side are copied as the decimals the witness states;
an angle in radians is turned into degrees at 40 significant digits. The measure tool
then reads each number as binary64, which is what it is for: identity for credit.
"""

from __future__ import annotations

import gzip
import hashlib
import sys
from decimal import Decimal, getcontext

import yaml

getcontext().prec = 60
PI = Decimal("3.14159265358979323846264338327950288419716939937510582097494459")


def plain(x: Decimal) -> str:
    s = format(x, "f")
    return s if "." not in s else s.rstrip("0").rstrip(".") or "0"


def main() -> None:
    src, out = sys.argv[1:3]
    raw = open(src, "rb").read()
    if src.endswith(".gz"):
        raw = gzip.decompress(raw)
    doc = yaml.safe_load(raw)
    w = doc["witness"]
    if w["representation"] != "center-angle" or w["scalar"]["kind"] != "decimal":
        raise SystemExit("not a decimal centre-angle witness")
    unit = w["coordinates"]["angle_unit"]
    if w["coordinates"]["origin"] != "lower-left" or w["coordinates"]["axes"] != "x-right-y-up":
        raise SystemExit("unexpected frame")
    lines = [f"# from {src.split('/')[-1]}, SHA-256 {hashlib.sha256(raw).hexdigest()}, by l163_convert.py", f"{w['n']} {plain(Decimal(str(w['side'])))}"]
    for sq in w["squares"]:
        x, y = (Decimal(str(c)) for c in sq["center"])
        a = Decimal(str(sq["angle"]))
        if unit == "radians":
            a = a * 180 / PI
        elif unit != "degrees":
            raise SystemExit(f"angle unit {unit}")
        lines.append(f"{plain(x)} {plain(y)} {plain(a.quantize(Decimal(1).scaleb(-40)) if abs(a) > 0 else a)}")
    if len(lines) != w["n"] + 2:
        raise SystemExit("count")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(out, w["n"], unit)


if __name__ == "__main__":
    main()
