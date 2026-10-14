"""Read an upper-bound packet's exact replay receipt and its claims record, as data.

    python3 -I -B receipt_summary.py PACKET_DIR

``PACKET_DIR`` holds ``acquisition/report.json`` (the import declaration),
``acquisition/claims.json``, ``receipts/exact-certification.json.xz`` and ``source/``.
The program prints, from the receipt: the jobs, their summed pair decisions, route CPU
seconds and wall seconds, the longest job; for each positive, that its deciding input
is the retained certificate (count, side and every pose, parsed here), that both routes
passed with every pair tested and the same least wall clearance and least pair gap; for
each control, that both routes refused it and on what. From the claims record: that
each certificate's exact side rounds up at 15 places to the side the source prints and
at 16 to the ceiling the record states, the gap to the grid, and each pending report's
relation and difference recomputed from the exact side and the report's printed value.

It decides no geometry; it reads two records this repository wrote and the retained
certificates. Exit status 0 when every statement it checks holds. Written for the
review of 14 October 2026; see ../README.md.
"""

from __future__ import annotations

import argparse
import json
import lzma
import sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from squares_exact import parse_certificate

JOBS = ("positive", "duplicate-square-overlap", "square-translated-outside-container")


def say(line: str) -> None:
    sys.stdout.write(line + "\n")


def round_up(value: Fraction, places: int) -> Decimal:
    scale = 10**places
    return Decimal(-((-value.numerator * scale) // value.denominator)) / Decimal(scale)


def check_receipt(packet: Path, problems: list[str]) -> None:
    declaration = json.loads((packet / "acquisition/report.json").read_text(encoding="utf-8"))
    paths = {row["n"]: row["path"] for row in declaration["certificates"]}
    with lzma.open(packet / "receipts/exact-certification.json.xz") as stream:
        receipt = json.load(stream)
    cases = receipt["cases"]
    say(f"receipt {receipt['format']}: routes {receipt['routes']}, {len(cases)} jobs")
    expected = [(n, job) for n in declaration["replayed"] for job in JOBS]
    if [(case["n"], case["control"]) for case in cases] != expected:
        problems.append("the receipt's jobs are not the replayed roster's, in order")
    pairs = cpu = wall = 0
    longest = (0.0, "")
    for case in cases:
        n, control = case["n"], case["control"]
        cert = parse_certificate((packet / "source" / paths[n]).read_text(encoding="utf-8"))
        poses = [[str(x), str(y), str(t)] for x, y, t in cert.squares]
        if control == "duplicate-square-overlap":
            poses[1] = poses[0]
        elif control == "square-translated-outside-container":
            x, y, t = cert.squares[0]
            poses[0] = [str(x + cert.width + 2), str(y), str(t)]
        given = case["checker_input"]
        if (
            given["n"] != cert.n
            or Fraction(given["side"]) != cert.width
            or given["poses"] != poses
        ):
            problems.append(
                f"{n} {control}: the deciding input is not the retained certificate"
            )
        routes = {route: case[route] for route in receipt["routes"]}
        cpu += sum(case["cpu_seconds"].values())
        wall += case["wall_seconds"]
        if case["wall_seconds"] > longest[0]:
            longest = (case["wall_seconds"], f"{n} {control}")
        for route, verdict in routes.items():
            pairs += verdict["pairs_tested"]
            if verdict["pairs_tested"] != n * (n - 1) // 2:
                problems.append(f"{n} {control} {route}: not every pair tested")
            if Fraction(verdict["side"]) != cert.width:
                problems.append(f"{n} {control} {route}: side differs from the certificate")
            if verdict["verification_passed"] != (control == "positive"):
                problems.append(
                    f"{n} {control} {route}: verdict {verdict['verification_passed']}"
                )
            if bool(verdict["failures"]) == (control == "positive"):
                problems.append(f"{n} {control} {route}: failures {verdict['failures']}")
        gaps = {Fraction(v["minimum_best_pair_gap"]) for v in routes.values()}
        walls = {Fraction(v["minimum_containment_clearance"]) for v in routes.values()}
        if len(gaps) != 1 or len(walls) != 1:
            problems.append(f"{n} {control}: the routes disagree on the least margins")
        gap, clearance = gaps.pop(), walls.pop()
        if control == "positive":
            if gap <= 0 or clearance <= 0:
                problems.append(f"{n}: a positive with a non-positive margin")
            say(
                f"  {n} positive: side {cert.width} as retained; both routes pass; least "
                f"wall clearance {float(clearance):.6e}, least pair gap {float(gap):.6e}"
            )
        else:
            reasons = {route: verdict["failures"][0] for route, verdict in routes.items()}
            bad = gap >= 0 if control == "duplicate-square-overlap" else clearance >= 0
            if bad:
                problems.append(f"{n} {control}: the margins do not show the mutation")
            say(f"  {n} {control}: refused by both routes: {reasons}")
    say(
        f"  sums: {pairs:,} pair decisions over both routes, {cpu:.1f} route CPU s, "
        f"{wall:.1f} job wall s; longest job {longest[0]:.1f} s ({longest[1]})"
    )


def check_claims(packet: Path, problems: list[str]) -> None:
    claims = json.loads((packet / "acquisition/claims.json").read_text(encoding="utf-8"))
    read_at = claims["read_at_main"][:9]
    say(f"claims {claims['format']}: read at main {read_at}, horizon {claims['horizon']}")
    for row in claims["results"]:
        n = row["n"]
        exact = Fraction(row["exact_side"])
        cert = parse_certificate(
            (packet / "source" / row["certificate"]).read_text(encoding="utf-8")
        )
        if cert.width != exact or cert.n != n:
            problems.append(f"{n}: claims.json's exact side is not the certificate's")
        offered = Decimal(row["offered_side"])
        places = -offered.as_tuple().exponent
        if round_up(exact, places) != offered:
            problems.append(f"{n}: exact side does not round up to the offered {offered}")
        if round_up(exact, 16) != Decimal(row["ceiling"]):
            problems.append(f"{n}: ceiling {row['ceiling']} is not the 16-place round-up")
        grid = Fraction(row["grid_side"])
        say(
            f"  {n}: exact side rounds up to {offered} at {places} places; below the grid "
            f"{grid} by {float(grid - exact):.3e}; case {row.get('case')}; "
            f"smallest {row.get('smallest')}"
        )
        others = list(row.get("pending", []))
        if row.get("case"):
            others.append({**row["case"], "report": f"case {row['case']['result']}"})
        for other in others:
            # A report is compared by the decimals it prints, or by its retained exact
            # side where the record holds one.
            if "printed" in other:
                value, shown = Fraction(other["printed"]), f"prints {other['printed']}"
            else:
                value = Fraction(other["exact_side"])
                shown = f"holds the exact side {float(value):.15f}"
            relation = "below" if exact < value else "above" if exact > value else "equal"
            if relation != other["relation"] or Fraction(other["difference"]) != value - exact:
                problems.append(f"{n}: {other['report']} relation or difference")
            say(
                f"    {other['report']} ({other['holders']}) {shown}: "
                f"this certificate is {relation} it by {float(abs(value - exact)):.3e}"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    parser.add_argument("packet", type=Path)
    args = parser.parse_args(argv)
    problems: list[str] = []
    check_receipt(args.packet, problems)
    check_claims(args.packet, problems)
    for problem in problems:
        say("PROBLEM " + problem)
    say("RECEIPT_SUMMARY_HOLDS" if not problems else "RECEIPT_SUMMARY_FAILS")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
