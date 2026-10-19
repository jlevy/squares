"""Exact sides at each count the six entries reach, against the case ceilings on main.

Written for the 16 October review lane C. Reads each case record's verified ceiling
(``frontier/n-NNN.md``, ``verified_upper_bound.exact_form``) and each packet's exact side
through ``devtools.upper_bound_reports.import_side`` (the packet's custody admission and
its own adapter), compares them exactly, and prints each count's sides smallest first,
rounded up at sixteen places, with each side's margin below the case. It decides nothing
and writes only its JSON output. From ``packing/``::

    python -I resources/web/mishapolk-kkt-refinements-2026-10-14/review/review-2026-10-16/programs/adoption_table.py OUT.json
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

#: `packing/`, six levels up from this file in the packet's review directory.
PACKING = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(PACKING))

from devtools import upper_bound_reports as upper  # noqa: E402
from sqpack.yamlio import load_yaml  # noqa: E402

PACKETS = {
    "T-185": ("couzo-certificates-2026-10-11", (175,)),
    "T-186": (
        "mishapolk-kkt-refinements-2026-10-14",
        (129, 154, 156, 175, 176, 204, 232, 264, 271, 302, 303, 304),
    ),
    "T-187": ("evand-n146-2026-10-14", (146,)),
    "T-188": ("couzo-verified-bounds-2026-10-14", (211,)),
    "T-189": ("couzo-certificates-2026-10-14", (237,)),
    "T-190": ("couzo-n237-2026-10-15", (237,)),
}
# PR #574's rational certificates (T-174, held for the owner) at the counts it shares.
T174 = "pingyou-pr574-certificates-2026-10-13"


def up16(value: Fraction) -> str:
    scaled = -(-value.numerator * 10**16 // value.denominator)
    text = str(scaled)
    return f"{text[:-16]}.{text[-16:]}"


def case(n: int) -> tuple[Fraction, str]:
    text = (PACKING / f"frontier/n-{n:03d}.md").read_text(encoding="utf-8")
    front = load_yaml(text.split("---\n", 2)[1])["packing"]
    lane = front["verified_upper_bound"]
    return Fraction(str(lane["exact_form"])), ", ".join(lane["evidence"])


def main(out: str) -> int:
    counts = sorted({n for _packet, ns in PACKETS.values() for n in ns})
    t174 = upper.read_facts(upper.packet_path(T174))
    rows = []
    for n in counts:
        ceiling, evidence = case(n)
        sides = {
            entry: upper.import_side(packet, n)
            for entry, (packet, ns) in PACKETS.items()
            if n in ns
        }
        if n in t174:
            sides["T-174"] = t174[n].side
        ordered = sorted(sides.items(), key=lambda item: item[1])
        row = {
            "n": n,
            "case": up16(ceiling),
            "case_evidence": evidence,
            "sides": [
                {
                    "entry": entry,
                    "up16": up16(side),
                    "below_case": float(ceiling - side),
                    "exact": f"{side.numerator}/{side.denominator}",
                }
                for entry, side in ordered
            ],
            "gaps": [
                {"lower": a[0], "upper": b[0], "difference": float(b[1] - a[1])}
                for a, b in zip(ordered, ordered[1:], strict=False)
            ],
        }
        rows.append(row)
        print(n, row["case"], evidence)
        for item in row["sides"]:
            print(f"   {item['entry']} {item['up16']} below case by {item['below_case']:.3e}")
        for gap in row["gaps"]:
            print(f"   {gap['lower']} below {gap['upper']} by {gap['difference']:.3e}")
    Path(out).write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
