"""Compare each certificate exactly with its case ceiling and the other reports at its count.

Written for the stage 4 review of 19 October 2026. It decides nothing. It reads, as data:

- each case record's verified upper bound (``packing/frontier/n-NNN.md``, its YAML front
  matter's ``verified_upper_bound.exact_form``, a rational ``p/q`` at these four counts);
- each packet's frozen claim record (``acquisition/claims.json``), which ``check-claims``
  rebuilt equal on this review's run: the certificate's exact side, the case's exact side
  as the import lane read it, and every other report pending at the count, exactly where
  its packet retains a side and by its print otherwise.

It holds the claim record's case side to the case record's ceiling, recomputes every
difference exactly, and prints, count by count, every side smallest first, rounded up at
sixteen places, with its difference from the smallest; and where a pending report is
known only by its print, it says so and compares the print (rounded up, so the exact side
is at most the print).

Usage, from ``packing/`` with the project interpreter::

    python -I adoption_1019.py --json OUT.json
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path

import yaml

ROOT = Path.cwd()
WEB = ROOT / "resources/web"
PACKETS = (
    ("T-197 (#669)", "evand-n155-explorer-2026-10-17"),
    ("T-198 (#674 opening)", "evand-n229-dilation-2026-10-17"),
    ("T-199 (#674 update)", "evand-n229-dilation-update-2026-10-18"),
    ("T-218 (#659, provisional number)", "evand-n236-2026-10-16"),
    ("T-219 (#664, provisional number)", "evand-n271-2026-10-17"),
)


def exact(text: str) -> Fraction:
    if "/" in text:
        p, q = text.split("/")
        return Fraction(int(p), int(q))
    return Fraction(text)


def up16(value: Fraction) -> str:
    scaled = -((-value.numerator * 10**16) // value.denominator)
    whole, rest = divmod(scaled, 10**16)
    return f"{whole}.{rest:016d}"


def sci(value: Fraction) -> str:
    return f"{float(value):.3e}"


def ceiling(n: int) -> Fraction:
    text = (ROOT / f"frontier/n-{n:03d}.md").read_text(encoding="utf-8")
    front = yaml.safe_load(text.split("---")[1])
    return exact(str(front["packing"]["verified_upper_bound"]["exact_form"]))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args(argv)
    counts: dict[int, list[dict[str, object]]] = {}
    problems: list[str] = []
    for label, packet in PACKETS:
        record = json.loads((WEB / packet / "acquisition/claims.json").read_text(encoding="utf-8"))
        (row,) = record["results"]
        n = row["n"]
        side = exact(row["exact_side"])
        case_side = exact(row["case"]["exact_side"])
        if case_side != ceiling(n):
            problems.append(f"n={n}: the claim record's case side is not the case record's ceiling")
        found = counts.setdefault(n, [])
        found.append({"report": label, "side": side, "kind": "exact"})
        if not any(item["report"].startswith("case") for item in found):
            found.append({"report": f"case ceiling, {row['case']['result']} ({row['case']['holders']})", "side": case_side, "kind": "exact"})
        for pending in row["pending"]:
            name = pending["report"]
            if any(name.split(" ")[0] in str(item["report"]) for item in found):
                continue
            if "exact_side" in pending:
                found.append({"report": f"{name} ({pending['holders']})", "side": exact(pending["exact_side"]), "kind": "exact"})
            else:
                found.append({"report": f"{name} ({pending['holders']}), print only", "side": exact(pending["printed"]), "kind": "print, rounded up"})
    out: dict[str, object] = {"problems": problems, "counts": {}}
    table = out["counts"]
    assert isinstance(table, dict)
    for n, found in sorted(counts.items()):
        found.sort(key=lambda item: item["side"])  # type: ignore[arg-type,return-value]
        least = found[0]["side"]
        assert isinstance(least, Fraction)
        rows = []
        print(f"n = {n}")
        for item in found:
            side = item["side"]
            assert isinstance(side, Fraction)
            rows.append({"report": item["report"], "kind": item["kind"], "side_up16": up16(side), "above_smallest": sci(side - least)})
            print(f"  {up16(side)}  +{sci(side - least)}  {item['report']} [{item['kind']}]")
        table[str(n)] = rows
    args.json.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print("problems:", problems or "none")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
