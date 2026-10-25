"""Exact sides of the #763 packings at 268 and 303 against their comparators.

Stage 4 review of 24 October 2026 (bead think-zjus). Reads each certificate's or
witness's stated side exactly (the header of a rational certificate, the `side` of a
Witness/v2 file) and compares it with the #763 side in exact rational arithmetic.
It decides no geometry: a side here is what its file states, and only the two #763
certificates are decided, by check_certificates.py.

Side-only Kaggle per-puzzle leaderboard values are constants below, each with the
file it was read from; they are numbers, not packings, and no report under the
runbook.

Added after the reviewer read the 23 October review at 303: the later counts. Since
s(n) <= s(m) for m > n, a side at n is new only if it is below every bound at every
later count; the program reads the case records at 269 to 288 and 304 to 320, and the
source's own certificate at 304.

Run from packing/:

    uv run --frozen --all-extras --group dev python -I \\
      resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/sides.py \\
      --evand PATH/TO/evand-square-packing-at-8a8879a \\
      --out resources/web/couzo-issue763-2026-10-23/review/review-2026-10-24/out/sides.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent.parent
PACKING = PACKET.parent.parent.parent

# The decimal renderings the record prints for the #763 sides (results.yaml, T-240's
# claim at #789's head), which must be truncations of the exact sides.
RECORD_DECIMALS = {268: "16.87436171587383", 303: "17.90697823379890"}

# Side-only leaderboard values, read from the source's public comparison.
BOARD = [
    (268, "Minal kharat123", "2026-10-22 18:54:00 UTC", "4218590428981673/250000000000000",
     "public_bounds.json at 964ee2b (retained, source/public_bounds.json.gz)"),
    (268, "panpanpanda", "2026-10-23 14:48:22 UTC", "16874361715872031/1000000000000000",
     "public_bounds.json at 43f666c (not retained; read from the watched clone)"),
    (303, "Lucas Boesen", "2026-10-22 22:51:05 UTC", "17908331255816149/1000000000000000",
     "public_bounds.json at 964ee2b (retained, source/public_bounds.json.gz)"),
    (303, "pjmathematician", "2026-10-23 11:56:49 UTC", "17906978233833611/1000000000000000",
     "public_bounds.json at 43f666c (not retained; read from the watched clone)"),
]

RATIONAL = re.compile(r"^[+-]?[0-9]+(/[0-9]+)?$")

# Later counts: s(n) <= s(m) for m > n (delete squares), so a side at n is new only if it
# is below every bound at every later count. The case records at #789's head are read for
# 269 to 288 and 304 to 320; 289 = 17^2 and 321 > 17.9^2 put every later bound above by
# area.
LATER = {268: range(269, 289), 303: range(304, 321)}


def header_side(path: Path) -> Fraction:
    for line in path.read_text(encoding="ascii").splitlines():
        if line.strip() and not line.startswith("#"):
            token = line.split()[1]
            if not RATIONAL.match(token):
                msg = f"{path}: side {token!r} is not rational"
                raise ValueError(msg)
            return Fraction(token)
    msg = f"{path}: no header"
    raise ValueError(msg)


def witness_side(path: Path) -> Fraction:
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("side:"):
            return Fraction(stripped.split(":", 1)[1].strip().strip("'\""))
    msg = f"{path}: no side"
    raise ValueError(msg)


def case_bounds(n: int) -> list[tuple[str, Fraction, str]]:
    """The reported and verified upper bounds of the case record at n."""
    import yaml  # noqa: PLC0415

    text = (PACKING / "frontier" / f"n-{n:03d}.md").read_text(encoding="utf-8")
    front = text.split("---", 2)[1]
    doc = yaml.load(front, Loader=yaml.CSafeLoader)["packing"]
    out = []
    for key in ("reported_upper_bound", "verified_upper_bound"):
        entry = doc.get(key) or {}
        exact = str(entry.get("exact_form", "")).strip()
        if RATIONAL.match(exact):
            out.append((key, Fraction(exact), "exact"))
        elif entry.get("value") is not None:
            out.append((key, Fraction(str(entry["value"])), "print"))
    return out


def ceil_print(x: Fraction, places: int = 12) -> str:
    scaled = x * 10**places
    up = -((-scaled.numerator) // scaled.denominator)
    whole, frac = divmod(up, 10**places)
    return f"{whole}.{frac:0{places}d}"


def truncated(x: Fraction, places: int) -> str:
    scaled = x * 10**places
    down = scaled.numerator // scaled.denominator
    whole, frac = divmod(down, 10**places)
    return f"{whole}.{frac:0{places}d}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--evand", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    src = PACKET / "source" / "certificates"
    ev = args.evand / "search" / "packer" / "candidates"
    ours = {268: header_side(src / "best" / "n268.cert"),
            303: header_side(src / "best" / "n303.cert")}
    others = [
        (268, "T-174, the house (W-known-best-n268)",
         witness_side(PACKING / "witnesses" / "known-best" / "n-268.yaml")),
        (268, "parent: Tymchishin's EDA+Seam LP v4 (parents/85dbd707...)",
         header_side(src / "parents" / "85dbd707746197d31f62dd52b4e580dfb90097498a4970c577f776ce7de2df46.cert")),
        (268, "evand 8a8879a s268_lightning.cert", header_side(ev / "s268_lightning.cert")),
        (303, "T-239, the house (W-known-best-n303)",
         witness_side(PACKING / "witnesses" / "known-best" / "n-303.yaml")),
        (303, "T-230 (s303_r303w0.cert)",
         header_side(PACKING / "resources" / "web" / "evand-n303-2026-10-22" / "source"
                     / "search" / "packer" / "candidates" / "s303_r303w0.cert")),
        (303, "parent: Couzo's Kaggle push (parents/22f07a7c...)",
         header_side(src / "parents" / "22f07a7c318328d257d1a7efd9c5acb05e3286650a94da751592b21014424244.cert")),
        (303, "evand 8a8879a s303_cdeotte.cert", header_side(ev / "s303_cdeotte.cert")),
    ]
    others += [(n, f"Kaggle board, side only: {team}, {when} ({where})", Fraction(v))
               for n, team, when, v, where in BOARD]
    rows = []
    for n, side in ours.items():
        print(f"#763 at {n}: {truncated(side, 30)}..., 12-place print {ceil_print(side)}; "
              f"record's decimal {RECORD_DECIMALS[n]}... is a truncation: "
              f"{truncated(side, len(RECORD_DECIMALS[n].split('.')[1])) == RECORD_DECIMALS[n]}")
        rows.append({"n": n, "who": "#763", "side": str(side),
                     "side_30": truncated(side, 30), "print_12_up": ceil_print(side),
                     "record_decimal_is_truncation": truncated(
                         side, len(RECORD_DECIMALS[n].split(".")[1])) == RECORD_DECIMALS[n]})
    for n, who, side in others:
        diff = side - ours[n]
        rel_word = "above" if diff > 0 else "below" if diff < 0 else "equal to"
        print(f"  {n}: {who}: {truncated(side, 18)}..., print {ceil_print(side)}; "
              f"{float(abs(diff)):.3e} {rel_word} #763")
        rows.append({"n": n, "who": who, "side": str(side), "side_30": truncated(side, 30),
                     "print_12_up": ceil_print(side), "minus_763": str(diff),
                     "minus_763_float": float(diff)})
    later_rows = []
    for n, counts in LATER.items():
        least: tuple[Fraction, int, str, str] | None = None
        for m in counts:
            for key, bound, kind in case_bounds(m):
                margin = bound - ours[n]
                later_rows.append({"n": n, "m": m, "bound": key, "kind": kind,
                                   "bound_minus_763": float(margin)})
                if least is None or margin < least[0]:
                    least = (margin, m, key, kind)
        assert least is not None
        print(f"  later counts {counts.start} to {counts.stop - 1}: every reported and "
              f"verified bound is above #763's {n} side: "
              f"{all(r['bound_minus_763'] > 0 for r in later_rows if r['n'] == n)}; least "
              f"margin {float(least[0]):.6e} at {least[1]} ({least[2]}, {least[3]})")
    n304 = header_side(src / "best" / "n304.cert")
    print(f"  the source's n304.cert (not claimed by #763): {truncated(n304, 18)}..., "
          f"{float(n304 - ours[303]):.6e} above #763's 303 side")
    later_rows.append({"n": 303, "m": 304, "bound": "source certificates/best/n304.cert",
                       "kind": "exact", "bound_minus_763": float(n304 - ours[303])})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"program": "sides.py", "python": sys.version.split()[0],
                                    "rows": rows, "later_counts": later_rows}, indent=1)
                        + "\n", encoding="utf-8")
    print(f"receipt {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
