"""Check four reported source roots without admitting geometry or a frontier bound.

The complete catalogue is bound to its retained acquisition before selecting the four
new coefficient vectors. Exact arithmetic proves irreducibility and one real root in
both the source's declared interval and the independently isolated decimal cell. The
source's checker flags remain source assertions. Geometry, local minimality, Lean
replay and equality to a current finite witness are separate, unperformed obligations.

``collect()`` returns source-only records for the exact-values register. This command
writes no register: ``--check`` reports the outcome and ``--json`` emits the records.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from collections.abc import Sequence
from fractions import Fraction
from math import gcd
from typing import Any

from devtools import acquire_source
from devtools import evand_report_catalogue as reports
from devtools.retained_data import read_retained_bytes
from sqpack.exact_values import format_polynomial

REPO = reports.ROOT.parent
PACKET = reports.PACKET
UPSTREAM_PATH = "s12/search/exact/exact_forms.json"
SOURCE_FILE = PACKET / "source" / (UPSTREAM_PATH + ".gz")
SOURCE_URL = "https://github.com/evand/square-packing"
SOURCE_KEY = "[Daniel exact and local reports 2026]"
BEAD = "think-8sm2"
# These bounds contain the four retained degrees (8, 32, 40, 32), coefficient
# heights (13 to 52 digits) and 2e-25-wide positive intervals, without admitting
# an unbounded replacement problem to a routine register build.
MAX_INTEGER_DIGITS = 256
MAX_LITERAL_LENGTH = 512
MAX_INTERVAL_WIDTH = Fraction(1, 10**12)


class ReportedRootError(ValueError):
    """Source custody or a bounded exact algebraic obligation was not established."""


def read_source_rows() -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    """Freshly bind the consumed catalogue bytes, derived view and acquisition pin."""
    problems = acquire_source.check(PACKET, REPO)
    if problems:
        raise ReportedRootError("reported source custody: " + "; ".join(problems))
    record = json.loads(read_retained_bytes(PACKET / acquire_source.RECORD))
    source = record["sources"][0]
    if source["source_commit"] != reports.REVISION or source["source_url"] != SOURCE_URL:
        raise ReportedRootError("reported source acquisition names a different source pin")
    manifest = acquire_source.read_manifest(PACKET / acquire_source.MANIFEST)
    raw = read_retained_bytes(SOURCE_FILE)
    digest = hashlib.sha256(raw).hexdigest()
    if digest != manifest.get(UPSTREAM_PATH):
        raise ReportedRootError("consumed source catalogue bytes differ from acquisition")
    rows = json.loads(raw)
    view = reports.catalogue(rows)
    retained = json.loads(read_retained_bytes(PACKET / "reported-catalogue.json"))
    if retained != json.loads(json.dumps(view)):
        raise ReportedRootError("reported catalogue differs from the bound source rows")
    indexed = {row["n"]: row for row in rows if row["n"] in reports.NEW_DEGREES}
    lines: dict[int, int] = {}
    for number, line in enumerate(raw.decode("utf-8").splitlines(), 1):
        match = re.fullmatch(r'\s*"n": (\d+),?\s*', line)
        if match is not None and int(match[1]) in indexed:
            n = int(match[1])
            if n in lines:
                raise ReportedRootError("source catalogue has duplicate count locators")
            lines[n] = number
    if lines.keys() != indexed.keys():
        raise ReportedRootError("source catalogue lacks unambiguous count locators")
    return indexed, {"sha256": digest, "lines": lines}


def verify_source_root(
    row: dict[str, Any], *, prime_budget: int | None = None
) -> tuple[tuple[int, ...], dict[str, Any]]:
    """Check only algebra: callers must establish custody before attributing a row.

    Source verification flags are deliberately unused. The existing register's bounded
    rational root counter and irreducibility checker compute every verdict anew.
    """
    # The register consumes collect(); defer this import until its mathematics exists.
    from devtools import build_exact_values as exact  # noqa: PLC0415 -- register cycle

    n = row.get("n")
    raw = row.get("S_poly_ascending")
    degree = row.get("S_degree")
    if (
        type(n) is not int
        or n not in reports.NEW_DEGREES
        or type(degree) is not int
        or degree != reports.NEW_DEGREES[n]
        or not isinstance(raw, list)
        or len(raw) != degree + 1
        or any(type(c) is not int or len(str(abs(c))) > MAX_INTEGER_DIGITS for c in raw)
        or raw[-1] == 0
    ):
        raise ReportedRootError(f"n = {n}: invalid or over-budget source coefficients")
    literals = row.get("S_interval")
    side = row.get("S")
    if (
        not isinstance(literals, list)
        or len(literals) != 2
        or any(type(value) is not str or len(value) > MAX_LITERAL_LENGTH for value in literals)
        or type(side) is not str
        or len(side) > MAX_LITERAL_LENGTH
    ):
        raise ReportedRootError(f"n = {n}: invalid source side or root interval")
    try:
        lo, hi = map(Fraction, literals)
        decimal = Fraction(side)
    except (ValueError, ZeroDivisionError) as error:
        raise ReportedRootError(f"n = {n}: invalid rational source interval") from error
    if not 0 < lo < hi < 100 or hi - lo > MAX_INTERVAL_WIDTH or not 0 < decimal < 100:
        raise ReportedRootError(f"n = {n}: invalid or over-budget source root interval")
    budget = exact.PRIME_BUDGET if prime_budget is None else prime_budget
    if type(budget) is not int or not 0 < budget <= exact.PRIME_BUDGET:
        raise ReportedRootError(f"n = {n}: invalid irreducibility prime budget")
    divisor = gcd(*raw)
    if raw[-1] < 0:
        divisor = -divisor
    coefficients = tuple(c // divisor for c in reversed(raw))
    try:
        if not exact.unique_root_in(coefficients, lo, hi):
            raise ReportedRootError(
                f"n = {n}: declared source interval does not contain one root"
            )
        checks, root = exact.polynomial_checks(n, coefficients, side, None, budget)
        if not lo <= root.lo < root.hi <= hi:
            raise ReportedRootError(
                f"n = {n}: declared source interval does not contain "
                "the independently isolated root"
            )
    except exact.ExactValuesError as error:
        raise ReportedRootError(f"n = {n}: {error}") from error
    checks.update(catalogue="not-in-catalogue", galois=None)
    return coefficients, checks


def collect() -> list[dict[str, Any]]:
    """Four checked source identities; no current bound, status or geometry verdict."""
    from devtools import build_exact_values as exact  # noqa: PLC0415 -- register cycle

    rows, custody = read_source_rows()
    result = []
    for n in sorted(rows):
        row = rows[n]
        coefficients, checks = verify_source_root(row)
        source_row = copy.deepcopy(row)
        # JSON numbers cannot preserve these integers in browser consumers. The raw
        # pinned source remains untouched; its complete arrays retain exact strings here.
        for key in ("S_poly_ascending", "field_poly_ascending"):
            source_row[key] = [str(c) for c in row[key]]
        result.append(
            {
                "n": n,
                "side": row["S"],
                "degree": len(coefficients) - 1,
                "polynomial": {
                    "coefficients": [str(c) for c in coefficients],
                    "text": format_polynomial(coefficients),
                    "latex": exact.polynomial_latex(coefficients),
                    "height_digits": len(str(max(abs(c) for c in coefficients))),
                },
                "checks": checks,
                "sources": [
                    {
                        "path": SOURCE_FILE.relative_to(REPO).as_posix(),
                        "url": f"{SOURCE_URL}/blob/{reports.REVISION}/{UPSTREAM_PATH}",
                        "kind": "reported-exact-catalogue",
                        "locator": {"line": custody["lines"][n], "section": str(n)},
                        "source_flags": [
                            f"source-reported {key}={json.dumps(row[key])}"
                            for key in ("verify_exact", "lean_packs", "lean_local_min", "new")
                        ],
                    }
                ],
                "source_statuses": [
                    "reported-feasibility",
                    "geometry-not-retained",
                    "lean-not-replayed",
                ],
                "attribution": {
                    "date_mentions": ["2026-10-07"],
                    "source_text": [
                        f"Evan Daniel, {SOURCE_KEY}, issue #419; source row n = {n}.",
                        f"Source crosscheck: {row['crosscheck']}",
                    ],
                },
                "bead": BEAD,
                "reported_source": {
                    "revision": reports.REVISION,
                    "sha256": custody["sha256"],
                    "acquisition": (PACKET / acquire_source.RECORD)
                    .relative_to(REPO)
                    .as_posix(),
                    "manifest": (PACKET / acquire_source.MANIFEST).relative_to(REPO).as_posix(),
                    "row": source_row,
                    "interval_root_count": 1,
                    "isolated_root_contained": True,
                },
                "assurance": {
                    "verification": "V0",
                    "confirmation": "C0",
                    "algebraic_identity": "independently-checked",
                    "geometry_replay": "not-attempted",
                    "lean_replay": "not-attempted",
                    "current_pose_identity": "not-established",
                    "global_optimality": "not-established",
                },
            }
        )
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    output = parser.add_mutually_exclusive_group()
    output.add_argument("--check", action="store_true", help="check the four source roots")
    output.add_argument("--json", action="store_true", help="emit complete source-only records")
    args = parser.parse_args(argv)
    try:
        records = collect()
    except (ReportedRootError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"reported exact roots refused: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(records, indent=2, ensure_ascii=False))
    else:
        print(
            f"{len(records)} reported source roots independently checked; feasibility V0/C0; "
            "geometry and Lean not replayed"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
