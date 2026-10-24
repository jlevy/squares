"""Exact margins of the n = 204 certificate (T-231) against every report at 204 in the record.

Reads the certificate's header side with this review's reader, and each earlier report's
side from the file the record retains for it (an Evan Daniel text certificate, Daniil
Ostashev's ``sqcert`` or a Witness/v2 fact), or from the record's print where no exact
side is retained. Prints the side rounded up at 12, 16 and 30 places and its decimal
expansion; checks the side against Evan Daniel's exact solver's side for T-229's witness
as the project's run of 22 October 2026 reports it (``S_cert`` and ``S_exact``); and
compares the side with the verified and reported upper bound at every count from 205 to
224 (at 225 and beyond every bound is at least sqrt(225) = 15 by area). It decides no
geometry.

From ``packing/`` of the reference checkout, with the project interpreter (PyYAML is
used to read the case records' front matter)::

    python -I margins_t231.py --packing . --cert CERT --t229 N-204.CERT --t186 N204-70A033F.CERT \\
        --run-report RUN/n-204/report.json --out MARGINS.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

PROGRAM = Path(__file__).resolve()
sys.path.insert(0, str(PROGRAM.parent))
check = importlib.import_module("review_t231_check")


def ceil_places(value: Fraction, places: int) -> str:
    scaled = math.ceil(value * 10**places)
    text = str(scaled).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def floor_places(value: Fraction, places: int) -> str:
    scaled = math.floor(value * 10**places)
    text = str(scaled).rjust(places + 1, "0")
    return f"{text[:-places]}.{text[-places:]}"


def read_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    return gzip.decompress(data) if path.suffix == ".gz" else data


def evand_side(path: Path) -> Fraction:
    for line in read_bytes(path).decode("ascii").splitlines():
        if line.strip() and not line.startswith("#"):
            return Fraction(line.split()[1])
    msg = f"{path}: no header"
    raise ValueError(msg)


def sqcert_side(path: Path) -> Fraction:
    for line in read_bytes(path).decode("ascii").splitlines():
        if line.startswith("s "):
            return Fraction(line.split()[1])
    msg = f"{path}: no side line"
    raise ValueError(msg)


def witness_side(path: Path) -> Fraction:
    text = read_bytes(path).decode("utf-8")
    match = re.search(r"^  side: '?([0-9/]+)'?$", text, re.MULTILINE)
    if match is None:
        msg = f"{path}: no witness side"
        raise ValueError(msg)
    return Fraction(match.group(1))


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---")[1])["packing"]


def gap_text(value: Fraction) -> str:
    return check.sci(value.numerator, value.denominator, 13)


def main() -> int:  # noqa: PLR0914, PLR0915
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--packing", type=Path, required=True)
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--t229", type=Path, required=True)
    parser.add_argument("--t186", type=Path, required=True)
    parser.add_argument("--run-report", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packing = args.packing.resolve()
    web = packing / "resources/web"
    cert = check.read_certificate(args.cert.read_text(encoding="ascii"))
    side = Fraction(*cert.side)
    record: dict[str, Any] = {
        "program": PROGRAM.name,
        "program_sha256": hashlib.sha256(PROGRAM.read_bytes()).hexdigest(),
        "python": sys.version,
        "certificate_sha256": hashlib.sha256(args.cert.read_bytes()).hexdigest(),
        "side": str(side),
        "side_decimal_40": floor_places(side, 40),
        "side_terminates_at_places": len(str(side.denominator)) - 1
        if 10 ** (len(str(side.denominator)) - 1) == side.denominator
        else None,
        "prints": {f"up_{k}": ceil_places(side, k) for k in (12, 16, 18, 30)},
    }
    # The project's runs of Evan Daniel's exact solver on T-229's witness.
    header_token = next(
        line for line in args.cert.read_text(encoding="ascii").splitlines() if not line.startswith("#")
    ).split()[1]
    factor = 1 + Fraction(1, 10**20)
    solver_rows = []
    for path in args.run_report:
        run = json.loads(read_bytes(path))
        s_cert = Fraction(run["solve"]["S_cert"])
        s_exact_print = run["solve"]["S_exact"]
        s_exact_low = Fraction(s_exact_print)
        places = len(s_exact_print.split(".")[1])
        s_exact_high = s_exact_low + Fraction(1, 10**places)
        solver_rows.append(
            {
                "report": str(path),
                "report_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "input_sha256": run["input"]["sha256"],
                "source_witness_sha256": run["source"]["sha256"],
                "S_cert": run["solve"]["S_cert"],
                "S_cert_equals_side": s_cert == side,
                "S_cert_string_equals_header": run["solve"]["S_cert"] == header_token,
                "S_exact_print": s_exact_print,
                "S_exact_print_places": places,
                "ceil30_of_dilated_S_exact_low": ceil_places(factor * s_exact_low, 30),
                "ceil30_of_dilated_S_exact_high": ceil_places(factor * s_exact_high, 30),
                "side_equals_ceil30_of_dilated_S_exact": ceil_places(factor * s_exact_low, 30)
                == ceil_places(side, 30)
                == ceil_places(factor * s_exact_high, 30)
                and side * 10**30 == math.ceil(side * 10**30),
                "side_minus_S_exact": gap_text(side - s_exact_low),
                "dilation_excess": gap_text((factor - 1) * s_exact_low),
                "solved_view_git_blob": run["outputs"]["solved"]["git_blob"],
                "same_view_git_blob": run["outputs"]["same"]["git_blob"],
            }
        )
    record["solver"] = solver_rows
    # Every report at 204 that the record holds, in report order.
    t186 = evand_side(args.t186)
    t186_fact = witness_side(web / "mishapolk-kkt-refinements-2026-10-14/facts/n-204.yaml.gz")
    t229 = evand_side(args.t229)
    t229_fact = witness_side(web / "mishapolk-issue719-2026-10-22/facts/n-204.yaml.gz")
    reports: list[tuple[str, str, str, Fraction | None, str | None]] = [
        ("Kingbird, David Ellsworth's catalogue (print, 14 places)", "before 2026-09-30", "print", None, "14.82287565553229"),
        ("T-101, Daniel's exact certificate of the catalogue packing", "2026-10-05", "exact", evand_side(web / "evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-204.cert"), None),
        ("T-155, the project's regularized certificate of it", "2026-10-12", "exact", Fraction("14.822875655532295295399036633375"), None),
        ("T-162, Ostashev's #562", "2026-10-12", "exact", sqcert_side(web / "dostashev-compositions-2026-10-12/source/records/n0204.sqcert"), None),
        ("T-174, PingYou Ltd's PR #574", "2026-10-13", "exact", witness_side(web / "pingyou-pr574-certificates-2026-10-13/facts/n-204.yaml.gz"), None),
        ("Polkovskyi's #593 (8bb41af)", "2026-10-13", "exact", witness_side(web / "mishapolk-records-2026-10-14/facts/n-204.yaml.gz"), None),
        ("T-186, Polkovskyi's KKT refinements (70a033f)", "2026-10-14", "exact", t186, None),
        ("T-226, Couzo's #670", "2026-10-17", "exact", evand_side(web / "couzo-issue670-2026-10-17/source/certificates/n204.cert"), None),
        ("T-228, Couzo's #675", "2026-10-18", "exact", evand_side(web / "couzo-issue675-2026-10-18/source/certificates/best/n204.cert"), None),
        ("T-223, Couzo's #678", "2026-10-18", "exact", evand_side(web / "couzo-issue678-2026-10-18/source/certificates/best/n204.cert"), None),
        ("T-225, Daniel's regularized lists", "2026-10-20", "exact", evand_side(web / "evand-regularized-2026-10-20/source/search/regularize/lists/certs/n-204.cert.gz"), None),
        ("T-229, Polkovskyi's #719 n-204.cert, the house", "2026-10-22 (1851c2c, the same commit)", "exact", t229, None),
    ]
    rows = []
    for label, date, kind, exact, printed in reports:
        if exact is not None:
            margin = exact - side
            rows.append(
                {
                    "report": label,
                    "reported": date,
                    "side": str(exact),
                    "side_up_16": ceil_places(exact, 16),
                    "side_below_by": str(margin),
                    "side_below_by_approx": gap_text(margin),
                    "below": margin > 0,
                }
            )
        else:
            low = Fraction(printed) - Fraction(1, 10**14)
            rows.append(
                {
                    "report": label,
                    "reported": date,
                    "print": printed,
                    "side_below_by_at_least": gap_text(low - side),
                    "below": low > side,
                    "kind": kind,
                }
            )
    # T-193's algebraic side: the record states it lies 1.48e-99 below T-186's exact side,
    # and the replay receipt prints the root's interval at 12 places.
    receipt = json.loads(
        (web / "evand-exact-cur-2026-10-16/receipts/replay-verify-exact.json").read_text(encoding="utf-8")
    )
    line = next(row for row in receipt["rows"] if row["n"] == 204)["positive"]["last_line"]
    low_text, high_text = re.search(r"in \[([0-9.]+), ([0-9.]+)\]", line).groups()
    t193_low = Fraction(low_text) - Fraction(1, 10**12)
    rows.insert(
        7,
        {
            "report": "T-193, Daniel's exact algebraic side (#639)",
            "reported": "2026-10-16",
            "print": f"root of a degree-35 polynomial in [{low_text}, {high_text}] (12 places)",
            "side_below_by_at_least": gap_text(t193_low - side),
            "below": t193_low > side,
            "record_states": "1.48e-99 below T-186's exact side",
            "side_below_by_approx_from_t186": gap_text(t186 - side),
        },
    )
    record["reports_at_204"] = rows
    record["custody"] = {
        "t186_clone_equals_packet_fact_side": t186 == t186_fact,
        "t229_clone_equals_packet_fact_side": t229 == t229_fact,
    }
    record["below_every_report"] = all(row["below"] for row in rows)
    # Later counts: s(204) <= s(m) for m > 204, so the side is new only below every bound there.
    later = []
    for m in range(205, 225):
        case = frontmatter(packing / f"frontier/n-{m:03d}.md")
        for lane in ("verified_upper_bound", "reported_upper_bound"):
            bound = case.get(lane) or {}
            exact_form = bound.get("exact_form")
            value = Fraction(str(bound["value"]))
            try:
                exact = Fraction(str(exact_form)) if exact_form is not None else None
            except ValueError:
                exact = None
            if exact is not None:
                margin = exact - side
                basis = "exact"
            else:
                places_m = len(str(bound["value"]).split(".")[1]) if "." in str(bound["value"]) else 0
                margin = value - Fraction(1, 10**places_m) - side
                basis = f"print {bound['value']} less one unit in its last place"
            later.append({"n": m, "lane": lane, "basis": basis, "above_side_by": gap_text(margin), "above": margin > 0})
    least = min(later, key=lambda row: float(row["above_side_by"]))
    record["later_counts"] = {
        "rows": later,
        "all_above": all(row["above"] for row in later),
        "least": least,
        "beyond_224": "every bound at m >= 225 is at least sqrt(m) >= 15 by area",
    }
    args.out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    summary = {
        "side": record["side"],
        "prints": record["prints"],
        "solver": [
            {k: row[k] for k in ("S_cert_equals_side", "S_cert_string_equals_header", "side_equals_ceil30_of_dilated_S_exact", "input_sha256", "solved_view_git_blob")}
            for row in record["solver"]
        ],
        "below_every_report": record["below_every_report"],
        "custody": record["custody"],
        "later_all_above": record["later_counts"]["all_above"],
        "later_least": least,
    }
    sys.stdout.write(json.dumps(summary, indent=1) + "\n")
    for row in rows:
        sys.stdout.write(
            f"  {row['report']:<60} {row['reported']:<38} "
            f"{row.get('side_below_by_approx') or ('>= ' + row['side_below_by_at_least'])}\n"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
