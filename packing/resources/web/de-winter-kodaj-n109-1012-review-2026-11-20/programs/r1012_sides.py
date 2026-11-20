"""Lane r1012: the sides at 109 and their differences, exactly. Arithmetic only.

Usage: r1012_sides.py CERTIFICATE KODAJ_CSV SAMANYU_EXACT.json CONTRACTION_1012.json
       CONTRACTION_SAMANYU.json CONTRACTION_T101.json IMPORT_SAMANYU_CONTRACTION.json OUT.json

Written after the findings' freeze. The certificate's side is read through
r1012_reader; the contracted sides from this repository's devtools.contraction_margin
receipts; Samanyu-dev's exact extent from r1012_binary64_rows.py's receipt; the import
lane's contraction receipt of Samanyu-dev's 109 for comparison; and the binary64 extent
of Kodaj's rows from the source CSV, with binary64 cosines and sines, for display. The
other values are the decimals their sources print, named in VALUES. It decides nothing.
"""

import csv
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.set_int_max_str_digits(0)

import r1012_reader  # noqa: E402

getcontext().prec = 60

VALUES = [
    ("the claim, issue 1012's comment of 18 November", "10.949289580944"),
    ("the issue's first figure, rounded to nearest", "10.949289580943"),
    ("T-101, the house: Evan Daniel's exact certificate (n-109.md verified_upper_bound)",
     "5474873734152916335457704004709/500000000000000000000000000000"),
    ("Samanyu-dev's 109 as #958's record prints its binary64 extent", "10.94928958094538"),
    ("Fonseca's pinwheel of 6 November, as the comment prints it", "10.949392392"),
    ("Navneet Prabhat's compilation, 'about', as the source README prints it", "10.94928958094337"),
]


def dec(x, places=30):
    x = F(x)
    return f"{Decimal(x.numerator) / Decimal(x.denominator):.{places}f}"


def sci(x):
    x = F(x)
    if x == 0:
        return "0"
    return f"{Decimal(x.numerator) / Decimal(x.denominator):.9e}"


def float_extent(path):
    xs, ys = [], []
    with open(path, encoding="utf-8") as handle:
        for r in csv.DictReader(handle):
            if int(r["n"]) != 109:
                continue
            x, y, a = float(r["x"]), float(r["y"]), float(r["angle"])
            c, s = math.cos(a), math.sin(a)
            for sx in (-0.5, 0.5):
                for sy in (-0.5, 0.5):
                    xs.append(x + sx * c - sy * s)
                    ys.append(y + sx * s + sy * c)
    return max(xs) - min(xs), max(ys) - min(ys)


def main(argv):
    (cert, kodaj_csv, samanyu_json, c1012, csam, ct101, cimport, out) = argv[1:9]
    side = r1012_reader.read_path(cert)["side"]
    rows = []

    def add(label, value, exact=True):
        rows.append({"side": label, "value": dec(value, 30), "exact": exact,
                     "certificate_less_it": sci(side - F(value)),
                     "certificate_less_it_exact": None if not exact else
                     f"{(side - F(value)).numerator}/{(side - F(value)).denominator}"})

    add("the certificate", side)
    for label, text in VALUES:
        add(label, F(text))
    closed = Decimal(6) + Decimal(7) / Decimal(2) * Decimal(2).sqrt()
    rows.append({"side": "6 + (7/2)sqrt(2), the catalogue's closed form at 109 (60 digits)",
                 "value": f"{closed:.30f}", "exact": False,
                 "certificate_less_it": f"{(Decimal(side.numerator) / Decimal(side.denominator) - closed):.9e}"})
    with open(samanyu_json, encoding="utf-8") as handle:
        add("Samanyu-dev's 109 read exactly here (r1012_binary64_rows.py), its extent",
            F(json.load(handle)["side_exact"]))
    for label, path in (("the certificate shrunk to first contact", c1012),
                        ("Samanyu-dev's 109 shrunk to first contact (this lane's reading)", csam),
                        ("T-101 shrunk to first contact", ct101),
                        ("Samanyu-dev's 109 shrunk to first contact (the import lane's receipt)", cimport)):
        with open(path, encoding="utf-8") as handle:
            d = json.load(handle)
        add(label, F(d["contracted_side"]))
        if "import" in label:
            add("Samanyu-dev's 109 as the import lane read it, its side", F(d["side"]))
    w, h = float_extent(kodaj_csv)
    rows.append({"side": "Kodaj's rows in binary64 (cos, sin), the larger of width and height",
                 "value": repr(max(w, h)), "exact": False, "width": repr(w), "height": repr(h),
                 "certificate_less_it": sci(side - F(max(w, h)))})
    with open(out, "w", encoding="utf-8") as handle:
        json.dump({"program": "r1012_sides.py", "rows": rows}, handle, indent=1)
        handle.write("\n")
    for r in rows:
        print(f"{r['certificate_less_it']:>18}  {r['value'][:34]:34}  {r['side']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
