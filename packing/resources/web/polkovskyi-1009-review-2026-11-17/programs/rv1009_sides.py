"""The sides against the record: gains, prints, L steps, monotonicity. Decides nothing.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Written after the checker
and the controls plan were frozen and run only after the findings were frozen.

    python -I -B rv1009_sides.py FRONTIER_DIR ISSUE.json OUT.json CHECK.json...

Reads the front matter of every case record ``n-NNN.md`` in FRONTIER_DIR and the check
receipts of this review. For each of the review's counts it gives the record's two upper
lanes exactly, the gain of the certificate's side on them, the 12-place prints, and the
issue's own "standing" and "gain" columns beside what the record gives. For every count
of the record it then asks what else the new sides imply: a certificate at n bounds every
smaller count (delete squares), and with an L-shaped border of width k it bounds a larger
count at its side plus k.

A side the record writes as a fraction is compared exactly. A side it writes as a closed
form is evaluated by sympy to 60 digits and compared with the certificate's side there;
the comparison is exact in sign whenever the two differ before the sixtieth digit, and
the receipt says which sides were closed forms.
"""

from __future__ import annotations

import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import sympy
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rv1009_issue as issue  # noqa: E402

F = Fraction
FRACTION = re.compile(r"-?\d+(/\d+)?")
DIGITS = 60


def exact(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}" if value.denominator != 1 else str(value.numerator)


def sci(value: Fraction, digits: int = 12) -> str:
    return f"{float(value):.{digits - 1}e}"


def fixed(value: Fraction, places: int = 30) -> str:
    scaled = value.numerator * 10**places // value.denominator
    text = str(scaled).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def ceiling_12(value: Fraction) -> str:
    k = -((-value.numerator * 10**12) // value.denominator)
    return f"{k // 10**12}.{k % 10**12:012d}"


def closed_form(text: str) -> sympy.Expr:
    """A closed form as the record writes it, with its implied products made explicit."""
    work = text.replace("^", "**")
    work = re.sub(r"\)\s*(?=[\w(])", ")*", work)
    work = re.sub(r"(\d)\s*(?=sqrt|\()", r"\1*", work)
    work = re.sub(r"(\d+)/(\d+)", r"Rational(\1,\2)", work)
    return sympy.sympify(work, rational=True)


def side_of(lane: dict | None) -> dict | None:
    """A lane's side: exact when a fraction, else a 60-digit rational enclosure's centre."""
    if not lane or lane.get("value") in (None, "null"):
        return None
    form = lane.get("exact_form")
    out = {"value": str(lane["value"]), "exact_form": None if form is None else str(form)[:120]}
    if form is not None and FRACTION.fullmatch(str(form)):
        out["kind"] = "fraction"
        out["side"] = F(str(form))
    elif form is not None:
        expr = closed_form(str(form))
        digits = sympy.N(expr, DIGITS)
        out["kind"] = "closed form"
        out["side"] = F(str(digits))
        out["closed_form_60_digits"] = str(digits)
    else:
        out["kind"] = "decimal"
        out["side"] = F(str(lane["value"]))
    return out


def read_records(frontier: Path) -> dict[int, dict]:
    records = {}
    for path in sorted(frontier.glob("n-*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        front = yaml.safe_load(text.split("\n---\n", 1)[0][4:])
        packing = front.get("packing") or {}
        n = packing.get("n")
        if not isinstance(n, int):
            continue
        rep = packing.get("reported_upper_bound") or {}
        ver = packing.get("verified_upper_bound") or {}
        records[n] = {
            "reported": side_of(rep),
            "verified": side_of(ver),
            "found_by": rep.get("found_by"),
            "improved_by": rep.get("improved_by"),
            "source_key": rep.get("source_key"),
            "source_date": str(rep.get("source_date")),
            "witnesses": rep.get("witnesses"),
            "evidence_reported": rep.get("evidence"),
            "evidence_verified": ver.get("evidence"),
            "status": packing.get("status"),
        }
    return records


def lane_json(side: dict | None) -> dict | None:
    if side is None:
        return None
    out = {k: v for k, v in side.items() if k != "side"}
    out["side_30_places"] = fixed(side["side"])
    out["ceiling_12"] = ceiling_12(side["side"])
    return out


def least_upper(record: dict) -> tuple[Fraction, str] | None:
    """The smaller of the record's two upper lanes."""
    best = None
    for name in ("reported", "verified"):
        lane = record[name]
        if lane is not None and (best is None or lane["side"] < best[0]):
            best = (lane["side"], name)
    return best


def main(argv: list[str]) -> int:
    frontier, issue_path, out_path = Path(argv[1]), argv[2], argv[3]
    stated = issue.read_issue(issue_path)
    records = read_records(frontier)
    sides = {}
    for receipt_path in argv[4:]:
        receipt = json.loads(Path(receipt_path).read_text(encoding="ascii"))
        sides[receipt["n"]] = F(receipt["side"]["exact"])
    counts = {}
    for n, side in sorted(sides.items()):
        record = records[n]
        claim = stated["claims"][n]
        entry: dict = {
            "side_30_places": fixed(side),
            "ceiling_12": ceiling_12(side),
            "record": {
                "reported": lane_json(record["reported"]),
                "verified": lane_json(record["verified"]),
                "found_by": record["found_by"],
                "improved_by": record["improved_by"],
                "source_key": record["source_key"],
                "source_date": record["source_date"],
                "witnesses": record["witnesses"],
                "evidence_verified": record["evidence_verified"],
            },
            "issue": claim,
        }
        for name in ("reported", "verified"):
            lane = record[name]
            if lane is None:
                continue
            gain = lane["side"] - side
            entry[f"gain_on_{name}"] = {
                "exact": exact(gain) if lane["kind"] == "fraction" else None,
                "sci": sci(gain),
                "positive": gain > 0,
                "relative": sci(gain / lane["side"], 4),
                "house_kind": lane["kind"],
                "print_units_lowered": int((F(ceiling_12(lane["side"])) - F(ceiling_12(side))) * 10**12),
            }
        best = least_upper(record)
        assert best is not None
        gain = best[0] - side
        stand = F(claim["standing"])
        entry["issue_standing_is_record_ceiling_12"] = claim["standing"] == ceiling_12(best[0])
        entry["issue_standing_less_record_sci"] = sci(stand - best[0])
        entry["issue_gain"] = claim["gain"]
        entry["issue_gain_as_side_less_record"] = f"{float(-gain):.6e}"
        entry["issue_gain_as_claim_less_standing"] = f"{float(F(claim['claim']) - stand):.6e}"
        counts[n] = entry

    # what else the new sides imply
    deletions = []
    for n, side in sorted(sides.items()):
        for m in sorted(records):
            if m >= n:
                break
            best = least_upper(records[m])
            if best is not None and best[0] > side:
                deletions.append(
                    {
                        "from": n,
                        "to": m,
                        "record_ceiling_12": ceiling_12(best[0]),
                        "new_side_ceiling_12": ceiling_12(side),
                        "gain_sci": sci(best[0] - side),
                        "also_a_count_of_this_issue": m in sides,
                    }
                )
    above = []
    for n, side in sorted(sides.items()):
        for m in sorted(records):
            if m <= n:
                continue
            best = least_upper(records[m])
            if best is not None and best[0] < side:
                above.append({"count": n, "larger_count_below_it": m, "by_sci": sci(side - best[0])})
    lsteps = []
    for n, side in sorted(sides.items()):
        m = n
        for k in range(1, 9):
            m += 2 * int(side + k - 1) + 1
            new = side + k
            row = {"from": n, "width": k, "to": m, "side_ceiling_12": ceiling_12(new)}
            if m in records and least_upper(records[m]) is not None:
                best = least_upper(records[m])
                assert best is not None
                row["record_ceiling_12"] = ceiling_12(best[0])
                row["record_less_step_sci"] = sci(best[0] - new)
                row["improves_the_record"] = new < best[0]
                row["also_a_count_of_this_issue"] = m in sides
            else:
                row["record_ceiling_12"] = None
                row["improves_the_record"] = None
            lsteps.append(row)
    receipt = {
        "program": "rv1009_sides.py",
        "lane": "c-review-1009-1117",
        "decides": "nothing",
        "case_records_read": len(records),
        "counts": counts,
        "deletion_bounds_that_improve_the_record": deletions,
        "larger_counts_below_a_new_side": above,
        "l_steps": lsteps,
        "l_steps_that_improve_the_record": [r for r in lsteps if r["improves_the_record"]],
    }
    Path(out_path).write_text(json.dumps(receipt, indent=1) + "\n", encoding="ascii")
    for n, entry in counts.items():
        g = entry.get("gain_on_verified") or entry.get("gain_on_reported")
        sys.stdout.write(
            f"n={n} gain={g['sci']} units={g['print_units_lowered']} house={g['house_kind']} "
            f"standing_ok={entry['issue_standing_is_record_ceiling_12']}\n"
        )
    sys.stdout.write(
        f"deletions={len(deletions)} l_steps_improving={len(receipt['l_steps_that_improve_the_record'])} "
        f"larger_below={len(above)}\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
