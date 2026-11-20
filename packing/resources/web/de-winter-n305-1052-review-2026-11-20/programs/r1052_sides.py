"""Lane r1052, after the findings' freeze: the sides at 305 and their differences, exactly.
It decides nothing.

Usage: r1052_sides.py J_FILE OUT_JSON LABEL=VALUE [LABEL=VALUE ...]

Reads the certificate's side from form J through the reader, and each VALUE as an exact
decimal or ``p/q`` (as the source prints it), and writes each value, the certificate's
side less it, exactly and in scientific notation, and the differences between
consecutive values, sorted from the largest.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import r1052_check as check  # noqa: E402
import r1052_reader as reader  # noqa: E402


def main(argv: list[str]) -> int:
    j_path, out_path = argv[1:3]
    side = reader.read_form_j(Path(j_path).read_bytes())["side"]
    rows = [("the certificate", side, "form J's side")]
    for item in argv[3:]:
        label, _, text = item.partition("=")
        rows.append((label, F(text), text))
    rows.sort(key=lambda r: -r[1])
    out = []
    for k, (label, value, text) in enumerate(rows):
        entry = {
            "label": label,
            "as_given": text if len(text) < 120 else text[:117] + "...",
            "decimal_30": check.decimal(value, 30),
            "certificate_less_it": str(side - value),
            "certificate_less_it_sci": check.sci(side - value, 9),
        }
        if k + 1 < len(rows):
            entry["less_the_next"] = check.sci(value - rows[k + 1][1], 9)
        out.append(entry)
    Path(out_path).write_text(json.dumps({"program": "r1052_sides.py", "rows": out}, indent=1) + "\n")
    for e in out:
        print(f"{e['label']}: {e['decimal_30']}  certificate less it {e['certificate_less_it_sci']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
