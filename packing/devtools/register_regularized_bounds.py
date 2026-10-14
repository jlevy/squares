#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes case-record prose, whose typography uses curly
# apostrophes, the double-struck Q and the less-or-equal sign, as the other layers do.
"""Register the regularized views whose exact side lies below a case's verified upper bound.

Row 3 of the regularization policy's decision table
(`docs/project/policies/regularization-policy.md`) holds back a view whose exact side
`s_V` lies below the case's verified upper bound `U`: such a view proves more than the
record holds, so it is registered as a result first and drawn after. The owner answered
the policy's question 3 on 12 October 2026, "regularize and correct always": every such
view is registered, in batches, each count with a `regularizations` item, and the case
record's verified upper bound moves to the exact side. This tool is that registration for
the views of the full run of 11 and 12 October 2026 (`devtools.regularize_evand run` over
`n = 1..324` on the register's known-best witnesses, and its re-runs).

**Which views.** `select` reads the run directories' reports, a later directory's report
replacing an earlier one's at the same count. A count is a candidate where either output,
the vendored generator's certificate at its own side (`solved`) or the same-side view at
the witness's side `s_W` (`same`), is decided at row 3. Three sets are left out
(`EXCLUDED`): `n = 17`, held by the owner (think-x4v4), the 42 counts jlevy/squares#518
re-houses, and the nine jlevy/squares#553 re-houses, whose witnesses those pull requests
replace; of the nine, only `n = 176` was a candidate. At each other candidate the view
with the least exact side is registered, so that once its side is the verified upper bound
no view of the count lies below it. A report is refused unless the witness it read is the
checkout's, by its id and exact side, and the bound it compared with is the case
record's; the identity measured against the checkout witness then shows any other drift.

At 33 counts the registered view is a `solved` certificate, and its side is exactly the
side of Evan Daniel's certificate of the same packing (T-101), which the record had
carried rounded up at the fourteen decimals the catalogue prints. At the other 26 it is a
`same` view, whose side is the witness's own, 6.6e-20 to 1.8e-19 below T-101's at 25 of
them; at `n = 29` it lies 5.4e-20 below the interval certificate's endpoint (T-009). The
packings are the catalogue's; only the ceiling's exact identity moves, by 5.4e-20 to
9.9e-15 at each count.

**What is retained.** Each registered view as the run wrote it, gzip-compressed, under
`cases/regularized_bounds/views/`, and `selection.json`, a row per count: the view's side
and display, the bound the record held before and the margin, the printed side and closed
form and the view's distance above each, whether the drawing would change, the identity
measured here on the retained view against the witness's exact frame
(`check_half_angle_area.arrangement_gap` under the box's eight symmetries, through
`regularize_evand.identity`), and the regularization in the register's terms.

**How each is decided.** `decide` decides every retained view over Q, pair by pair and
wall by wall, by `sqpack.witness.exact_verify` and by
`devtools.check_rational_witness_independent`, and writes `exact-decision.json`. The run
that made the views used the same two checkers, so this is a reproduction with the
producer's code, not a second implementation. `controls` makes three mutants of each view
and decides them on both routes (`negative-controls.json`): the tightest pair's second
square moved along the pair's best separating face axis by its gap plus one unit of the
side's denominator, doubled until the independent checker's own pair gap is negative,
which both must refuse; the box shrunk past its least top or right clearance by that unit,
which both must refuse; and the box shrunk by the unit alone, which both must accept
wherever the clearance exceeds it.

**What it writes.** Run with no command, it writes each case record's verified upper lane
onto the registered side (`apply_case`): the exact side as `exact_form` and this tool's
evidence, while `value` keeps the decimal the record printed before, which lies above the
exact side and so stays an upper display of it, as the record prints a rounded `value`
beside a rational `exact_form` at n = 70 and elsewhere (`printed_value`; were it below the
side, the smallest decimal at that precision at or above the side would be printed, and
the row says so). Agreement with the report at the printed precision is therefore what
it was. It also writes a `mathematics` blocker where the bound and the report disagree at
the declared precision, a dated paragraph and a section on the certificate, which state
the exact side, and the earlier certificate's sentences put in the past.
`devtools.generate_frontier_case` applies it last, after `devtools.apply_exact_ceilings`,
so that a regenerated draft reads as the record does; applied to its own output it
changes nothing. `--check` reports drift and writes nothing.

Usage, from `packing/`, each after `uv run --frozen --all-extras --group dev python -m
devtools.register_regularized_bounds`:

    select --run-dir RUN [RUN ...]
    decide
    controls
    table
    [--check]
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import re
import sys
import time
from collections.abc import Mapping, Sequence
from decimal import ROUND_CEILING, Decimal, localcontext
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import check_rational_witness_independent as independent
from devtools.migrate_math import markdown_math
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
FRONTIER = ROOT / "frontier"
PACKAGE = ROOT / "cases/regularized_bounds"
VIEWS = PACKAGE / "views"
SELECTION = PACKAGE / "selection.json"
DECISION = PACKAGE / "exact-decision.json"
CONTROLS = PACKAGE / "negative-controls.json"
PACKAGE_LINK = "../cases/regularized_bounds/README.md"

FORMAT = "regularized-bounds-receipt-v1"
TOOL = "python -m devtools.register_regularized_bounds"
POLICY = "docs/project/policies/regularization-policy.md"
RESULT = "T-155"
EVIDENCE = "E-regularized-bounds-2026-10-12-exact-decision"
SOURCE_KEY = "[Daniel regularizer 2026-10-11]"
REGISTERED = "2026-10-12"
DATE_WORDS = "12 October 2026"
#: The count the owner holds (think-x4v4), and the counts jlevy/squares#518 (42) and
#: jlevy/squares#553 (nine) re-house, whose witnesses those pull requests replace; nothing
#: here reads a view of them.
HELD = frozenset({17})
REHOUSED = frozenset(
    {70, 84, 86, 102, 103, 105, 108, 123, 126, 127, 129, 131, 132, 146, 153, 154, 155}
    | {156, 175, 180, 207, 209, 211, 228, 232, 236, 237, 258, 259, 261, 263, 267, 269}
    | {270, 292, 295, 302, 303, 305, 306, 307, 308}
)
#: #553 merged after the runs, re-housing 176 below the side its view would register.
REHOUSED_553 = frozenset({176, 181, 238, 239, 270, 271, 272, 304, 305})
EXCLUDED = HELD | REHOUSED | REHOUSED_553
#: The decimal places at which prose writes an exact side: the exact decimal where it
#: ends by then, else the side rounded up there.
DISPLAY_PLACES = 36
#: The register result whose packing each count's view redraws: Evan Daniel's exact
#: certificates of the catalogue's packings (T-101), and at n = 29 this project's interval
#: certificate of the catalogue's packing (T-009), the results that hold the packings the
#: views were made from.
PACKING_RESULT = {29: "T-009"}
DEFAULT_PACKING_RESULT = "T-101"
#: Headings and markers this layer writes.
DATED = "**Exact regularized certificate, 2026-10-12.**"
SECTION = "## The regularized exact certificate"
CEILING_HEADING = "## The verified upper bound is a ceiling"
T101_SECTION = "## The exact certificate"
T101_EARLIER = "## The earlier exact certificate"


class RegistrationError(ValueError):
    """A run, a view or a record this tool refuses."""


# --------------------------------------------------------------------------------------
# Small exact helpers
# --------------------------------------------------------------------------------------


def literal(value: Fraction) -> str:
    """The witness format's rational literal."""
    return str(value.numerator) if value.denominator == 1 else f"{value}"


def terminating_places(value: Fraction) -> int | None:
    """The decimal places at which `value` ends, or `None` where it never does."""
    denominator, twos, fives = value.denominator, 0, 0
    while denominator % 2 == 0:
        denominator //= 2
        twos += 1
    while denominator % 5 == 0:
        denominator //= 5
        fives += 1
    return max(twos, fives) if denominator == 1 else None


def ceiling_decimal(value: Fraction, places: int) -> Decimal:
    """`value` rounded up at `places` decimal places, exactly."""
    with localcontext() as context:
        context.prec = 400
        quotient = Decimal(value.numerator) / Decimal(value.denominator)
        result = quotient.quantize(Decimal(1).scaleb(-places), rounding=ROUND_CEILING)
    if Fraction(result) < value:
        raise RegistrationError("a ceiling underflowed its working precision")
    return result


def rounded_up(side: Fraction) -> bool:
    """Whether `side_text` writes the side rounded up rather than exactly: its decimal
    never ends, or ends past `DISPLAY_PLACES` places."""
    places = terminating_places(side)
    return places is None or places > DISPLAY_PLACES


def side_text(side: Fraction) -> str:
    """A side as prose writes it: its exact decimal where that ends within
    `DISPLAY_PLACES` places, else the side rounded up there, so it stays a ceiling."""
    places = terminating_places(side)
    if places is not None and places <= DISPLAY_PLACES:
        return format(ceiling_decimal(side, max(places, 1)), "f")
    return format(ceiling_decimal(side, DISPLAY_PLACES), "f")


#: What prose adds after a side it writes rounded up, so a decimal that is not the side is
#: never called the side exactly.
ROUNDED_WORDS = f"rounded up at {DISPLAY_PLACES} places"


def printed_value(earlier: str, side: Fraction) -> tuple[str, bool]:
    """The record's `value` for a bound whose exact form becomes `side`: the decimal it
    printed before where that is at or above `side`, as every registered count's is, else
    the smallest decimal at the same precision at or above `side`; and whether it had to
    be raised."""
    if Fraction(Decimal(earlier)) >= side:
        return earlier, False
    places = -int(Decimal(earlier).as_tuple().exponent)
    return format(ceiling_decimal(side, places), "f"), True


def decimal_text(value: Fraction, digits: int = 40) -> str:
    """`value` to `digits` significant digits, rounded up."""
    with localcontext() as context:
        context.prec = digits
        context.rounding = ROUND_CEILING
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def scientific(value: float) -> str:
    """A small positive number in two significant digits, `1.2e-15`."""
    return f"{value:.1e}".replace("e-0", "e-")


def round_up(value: float, digits: int = 2) -> float:
    """`value` rounded up at `digits` significant digits, so a bound stays one."""
    if value <= 0:
        return value
    exponent = math.floor(math.log10(value)) - digits + 1
    scale = 10.0**exponent
    return math.ceil(value / scale - 1e-9) * scale


def difference(larger: str, smaller: str) -> str:
    """`larger - smaller` at 28 digits, as the record's ceiling sections write a gap."""
    with localcontext() as context:
        context.prec = 28
        return str(Decimal(larger) - Decimal(smaller)).replace("E", "e")


def write_json(path: Path, value: object) -> None:
    """A receipt, one record per line where it is a list of rows."""
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(json.dumps(value, indent=1, ensure_ascii=False) + "\n")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def view_path(n: int) -> Path:
    return VIEWS / f"n-{n:03d}.yaml.gz"


def read_view(n: int) -> dict[str, Any]:
    """A retained view's Witness/v2 body."""
    document = load_yaml(gzip.decompress(view_path(n).read_bytes()).decode("utf-8"))
    return dict(document["witness"])


_VIEW_SIDE = re.compile(r"^  side: '?([0-9/.]+)'?$", re.MULTILINE)


def view_side(n: int) -> Fraction:
    """A retained view's stated side, read without parsing its squares."""
    match = _VIEW_SIDE.search(gzip.decompress(view_path(n).read_bytes()).decode("utf-8"))
    if match is None:
        raise RegistrationError(f"n={n}: the retained view states no side")
    return Fraction(match.group(1))


def case_front(n: int) -> dict[str, Any]:
    text = (FRONTIER / f"n-{n:03d}.md").read_text(encoding="utf-8")
    return dict(load_yaml(text.split("---\n", 2)[1])["packing"])


# --------------------------------------------------------------------------------------
# select
# --------------------------------------------------------------------------------------


def latest_reports(run_dirs: Sequence[Path]) -> dict[int, tuple[str, Path, dict[str, Any]]]:
    """Each count's report, a later run directory's replacing an earlier one's."""
    reports: dict[int, tuple[str, Path, dict[str, Any]]] = {}
    for run_dir in run_dirs:
        for directory in sorted(run_dir.glob("n-[0-9][0-9][0-9]")):
            path = directory / "report.json"
            if path.is_file():
                reports[int(directory.name[2:])] = (run_dir.name, directory, read_json(path))
    return reports


def row_three(report: Mapping[str, Any]) -> list[str]:
    """The outputs of one report decided at row 3."""
    decisions = report.get("decisions") or {}
    return [
        name
        for name in ("same", "solved")
        if (decisions.get(name) or {}).get("row") == 3
        and (report.get("outputs") or {}).get(name)
    ]


def least_output(report: Mapping[str, Any]) -> tuple[str, dict[str, str]]:
    """The report's row-3 output with the least exact side, and every row-3 output's side,
    which the row records so the choice can be checked without the run's report."""
    outputs = report["outputs"]
    sides = {name: literal(Fraction(outputs[name]["side_exact"])) for name in row_three(report)}
    if not sides:
        raise RegistrationError("no output of the report is decided at row 3")
    return min(sides, key=lambda name: Fraction(sides[name])), sides


def earlier_bound(n: int, case: Mapping[str, Any]) -> dict[str, Any]:
    """The verified upper bound the case held before this registration: the record's own,
    or, once the record carries this registration, the one the committed selection read
    from it then."""
    upper = case["verified_upper_bound"]
    if EVIDENCE in (upper.get("evidence") or []):
        if n not in committed():
            raise RegistrationError(f"n={n}: the record carries a registration no row holds")
        return dict(committed()[n]["earlier_verified"])
    return {
        "value": str(upper["value"]),
        "exact_form": upper.get("exact_form"),
        "evidence": list(upper.get("evidence") or []),
    }


def _closed_form_facts(
    reported: Mapping[str, Any], side: Fraction
) -> tuple[float | None, int | None]:
    """How far `side` lies above the catalogue's closed form, and the form's degree."""
    form = reported.get("exact_form")
    if not form:
        return None, None
    from devtools.apply_exact_ceilings import closed_form_degree  # noqa: PLC0415
    from sqpack.kingbird_catalogue import evaluate_exact_form  # noqa: PLC0415

    with localcontext() as context:
        context.prec = 90
        exact = evaluate_exact_form(str(form), 80)
        above = Decimal(side.numerator) / Decimal(side.denominator) - exact
    if above <= 0:
        raise RegistrationError(
            "a view's side is not above the catalogue's closed form, which would be a "
            "smaller packing than the catalogue's"
        )
    return float(f"{float(above):.4e}"), closed_form_degree(str(form))


def measure_identity(
    n: int, view: Mapping[str, Any], named: Sequence[int], source: Mapping[str, Any]
) -> dict[str, Any]:
    """The retained view against the checkout witness's exact frame, as the driver
    measures it. The run's report names the witness it read and that witness's exact side
    `s_W`; a checkout witness with another id or side is not the one the run read."""
    from devtools import regularize_evand as driver  # noqa: PLC0415
    from sqpack.witness import load_witness  # noqa: PLC0415

    witness = load_witness(driver.witness_path(n), fallback_schema=driver.WITNESS_SCHEMA)
    frame = driver.source_frame(witness)
    if frame.side is None:
        raise RegistrationError(f"n={n}: the witness has no rational frame")
    if witness.get("id") != source.get("id") or frame.side != Fraction(
        str(source.get("s_W_exact"))
    ):
        raise RegistrationError(f"n={n}: the run read another witness than the checkout's")
    side, placements, _corners = driver.view_geometry(view)
    measured = driver.identity(
        (side, placements), (frame.side, frame.placements), named, "view"
    )
    return {
        "one_to_one": bool(measured["one_to_one"]),
        "moved": measured.get("moved"),
        "moved_beyond": measured.get("moved_beyond"),
        "max_move": float(measured["max_move"]) if measured.get("max_move") else None,
        "max_turn_deg": float(measured["max_turn_deg"])
        if measured.get("max_turn_deg")
        else None,
        "turned": len(measured.get("turned") or []),
        "unnamed_turns": list(measured.get("unnamed_turns") or []),
        "symmetry": measured.get("symmetry"),
    }


def selection_row(
    n: int, run: str, directory: Path, report: Mapping[str, Any]
) -> dict[str, Any]:
    """One count's registered view, retained, with what the record needs about it."""
    from devtools.apply_exact_ceilings import bound_value  # noqa: PLC0415

    case = case_front(n)
    earlier = earlier_bound(n, case)
    upper = bound_value(earlier)
    outputs = report["outputs"]
    names = row_three(report)
    chosen, sides = least_output(report)
    block = outputs[chosen]
    side = Fraction(block["side_exact"])
    compared = bound_value(
        {
            "value": report["verified_upper_bound"],
            "exact_form": report["verified_upper_bound_exact_form"],
        }
    )
    if compared != upper:
        raise RegistrationError(f"n={n}: the run compared with another bound than the record's")
    if not side < upper:
        raise RegistrationError(f"n={n}: the view is not below the verified upper bound")
    if not all(block["routes"].get(route) for route in ("exact_verify", "independent")):
        raise RegistrationError(f"n={n}: a maintained route refused the view in the run")
    data = (directory / block["path"]).read_bytes()
    view = dict(load_yaml(data.decode("utf-8"))["witness"])
    if Fraction(str(view["side"])) != side:
        raise RegistrationError(f"n={n}: the view's side is not the report's")
    with atomic_output_file(view_path(n), make_parents=True) as temporary:
        temporary.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))
    reported = case["reported_upper_bound"]
    value, raised = printed_value(earlier["value"], side)
    verified = {"value": value, "exact_form": literal(side)}
    above_form, degree = _closed_form_facts(reported, side)
    regularized = report.get("regularize") or {}
    named = [int(square) for square in regularized.get("changed_angles") or []]
    record = report.get("regularization") or {}
    decision = report.get("decision") or {}
    after = decision.get("after_registration") or {}
    from devtools import apply_exact_ceilings as t101  # noqa: PLC0415

    t101_row = t101.committed().get(n)
    t101_side = Fraction(t101_row["certified_side"]) if t101_row else None
    return {
        "n": n,
        "run": run,
        "output": chosen,
        "outputs_at_row_3": names,
        "row_three_sides": sides,
        "side": literal(side),
        "side_decimal": decimal_text(side),
        "side_text": side_text(side),
        "value": value,
        "value_raised": raised,
        "earlier_verified": earlier,
        "below_earlier_by": float(f"{float(upper - side):.4e}"),
        "t101_side": literal(t101_side) if t101_side is not None else None,
        "below_t101_side_by": (
            float(f"{float(t101_side - side):.4e}") if t101_side is not None else None
        ),
        "witness_side": report["source"]["s_W_exact"],
        "witness_frame": report["source"]["frame"],
        "printed_side": str(reported["value"]),
        "printed_exact_form": reported.get("exact_form"),
        "printed_exact_form_degree": degree,
        "above_printed_side_by": float(
            f"{float(side - Fraction(Decimal(str(reported['value'])))):.4e}"
        ),
        "above_exact_side_by": above_form,
        "agrees_with_report": bounds_agree_at_declared_precision(reported, verified),
        "drawing": decision.get("decision"),
        "after_registration": {
            "decision": after.get("decision"),
            "index_record": after.get("index_record"),
            "reason": after.get("reason"),
        },
        "identity": measure_identity(n, view, named, report["source"]),
        "regularization": {
            "of": PACKING_RESULT.get(n, DEFAULT_PACKING_RESULT),
            "method": record.get("method"),
            "side": "same" if chosen == "same" else "solved",
            "changes": record.get("changes") or {},
        },
        "generator": report.get("generator"),
    }


def select(run_dirs: Sequence[Path]) -> dict[str, Any]:
    """Every row-3 count outside `EXCLUDED`, its least view retained and measured."""
    reports = latest_reports(run_dirs)
    candidates = sorted(
        n for n, (_run, _directory, report) in reports.items() if row_three(report)
    )
    rows = [selection_row(n, *reports[n]) for n in candidates if n not in EXCLUDED]
    receipts = []
    for run_dir in run_dirs:
        receipt = read_json(run_dir / "receipt.json")
        receipts.append(
            {
                "run": run_dir.name,
                "generator": receipt.get("generator"),
                "parameters": {
                    key: value
                    for key, value in (receipt.get("parameters") or {}).items()
                    if key != "counts"
                },
                "counts": len((receipt.get("parameters") or {}).get("counts") or []),
                "cost": receipt.get("cost"),
            }
        )
    return {
        "format": FORMAT,
        "tool": f"{TOOL} select",
        "policy": POLICY,
        "what": (
            "Every count where a view of the regularization runs is decided at row 3 of the "
            "policy's table, its side below the case's verified upper bound, apart from the "
            "held n = 17 and the counts jlevy/squares#518 and #553 re-house: the view with the "
            "least exact side, retained under views/, with the bound the record held before, "
            "the printed side and closed form, the drawing decision, and the identity "
            "measured on the retained view against the witness's exact frame."
        ),
        "runs": receipts,
        "candidates": candidates,
        "excluded": sorted(set(candidates) & EXCLUDED),
        "registered": [row["n"] for row in rows],
        "rows": rows,
    }


# --------------------------------------------------------------------------------------
# decide and controls
# --------------------------------------------------------------------------------------


def corners_of(
    view: Mapping[str, Any],
) -> tuple[Fraction, list[list[tuple[Fraction, Fraction]]]]:
    from devtools.regularize_evand import view_geometry  # noqa: PLC0415

    side, _placements, corners = view_geometry(view)
    return side, corners


def decide_view(view: Mapping[str, Any]) -> dict[str, Any]:
    """Both maintained exact routes on one view, with their least clearances."""
    from sqpack.witness import exact_verify  # noqa: PLC0415

    started = time.process_time()
    first, _report = exact_verify(dict(view))
    first_seconds = time.process_time() - started
    side, corners = corners_of(view)
    started = time.process_time()
    second = independent.check_squares(corners, side)
    second_seconds = time.process_time() - started
    return {
        "n": int(view["n"]),
        "side": literal(side),
        "exact_verify": {
            "passed": bool(first["verification_passed"]),
            "pairs_tested": first["pairs_tested"],
            "minimum_containment_clearance": float(
                Fraction(first["minimum_containment_clearance"])
            ),
            "minimum_best_pair_gap": float(Fraction(first["minimum_best_pair_gap"])),
            "failures": len(first["failures"]),
            "cpu_seconds": round(first_seconds, 2),
        },
        "independent": {
            "passed": bool(second["verification_passed"]),
            "pairs_tested": second["pairs_tested"],
            "minimum_containment_clearance": float(
                Fraction(second["minimum_containment_clearance"])
            ),
            "minimum_best_pair_gap": float(Fraction(second["minimum_best_pair_gap"])),
            "failures": len(second["failures"]),
            "cpu_seconds": round(second_seconds, 2),
        },
    }


def decide_all() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for n in committed():
        view = read_view(n)
        if Fraction(str(view["side"])) != Fraction(committed()[n]["side"]):
            raise RegistrationError(f"n={n}: the retained view's side is not the selection's")
        row = decide_view(view)
        rows.append(row)
        print(
            f"n={n}: exact_verify {row['exact_verify']['passed']}, independent "
            f"{row['independent']['passed']}",
            flush=True,
        )
    return {
        "format": FORMAT,
        "tool": f"{TOOL} decide",
        "what": (
            "Each retained view decided over Q, every pair and every wall, by "
            "sqpack.witness.exact_verify and devtools.check_rational_witness_independent, "
            "the two checkers the run that made the views decided them with."
        ),
        "decided": len(rows),
        "all_passed": all(
            row["exact_verify"]["passed"] and row["independent"]["passed"] for row in rows
        ),
        "pairs_tested": sum(row["exact_verify"]["pairs_tested"] for row in rows),
        "cpu_seconds": round(
            sum(
                row["exact_verify"]["cpu_seconds"] + row["independent"]["cpu_seconds"]
                for row in rows
            ),
            1,
        ),
        "least_wall_clearance": min(
            row["exact_verify"]["minimum_containment_clearance"] for row in rows
        ),
        "rows": rows,
    }


def _axes(square: Sequence[tuple[Fraction, Fraction]]) -> list[tuple[Fraction, Fraction]]:
    return [
        (-(square[1][1] - square[0][1]), square[1][0] - square[0][0]),
        (-(square[2][1] - square[1][1]), square[2][0] - square[1][0]),
    ]


def _extent(
    square: Sequence[tuple[Fraction, Fraction]], axis: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    values = [x * axis[0] + y * axis[1] for x, y in square]
    return min(values), max(values)


def tightest_pair(
    view: Mapping[str, Any],
) -> tuple[int, int, Fraction, tuple[Fraction, Fraction]]:
    """The pair with the least exact separating gap and the face normal that closes it,
    as `evand_exact_certificates.tightest_pair` finds it for a certificate."""
    _side, squares = corners_of(view)
    centres = [
        (sum(x for x, _y in square) / 4, sum(y for _x, y in square) / 4) for square in squares
    ]
    best: tuple[int, int, Fraction, tuple[Fraction, Fraction]] | None = None
    for left in range(len(squares)):
        for right in range(left + 1, len(squares)):
            dx = centres[left][0] - centres[right][0]
            dy = centres[left][1] - centres[right][1]
            if dx * dx + dy * dy > 2:
                continue
            gap: Fraction | None = None
            direction = (Fraction(0), Fraction(0))
            for axis in (*_axes(squares[left]), *_axes(squares[right])):
                left_lo, left_hi = _extent(squares[left], axis)
                right_lo, right_hi = _extent(squares[right], axis)
                for value, sign in ((right_lo - left_hi, -1), (left_lo - right_hi, 1)):
                    if gap is None or value > gap:
                        gap, direction = value, (sign * axis[0], sign * axis[1])
            if gap is not None and (best is None or gap < best[2]):
                best = (left, right, gap, direction)
    if best is None:
        raise RegistrationError("no pair lies close enough to touch")
    return best


def _moved(view: Mapping[str, Any], index: int, dx: Fraction, dy: Fraction) -> dict[str, Any]:
    document = dict(view)
    squares = [dict(square) for square in view["squares"]]
    x, y = (Fraction(str(value)) for value in squares[index]["center"])
    squares[index]["center"] = [literal(x + dx), literal(y + dy)]
    document["squares"] = squares
    return document


def _resized(view: Mapping[str, Any], side: Fraction) -> dict[str, Any]:
    document = dict(view)
    document["side"] = literal(side)
    return document


def control_views(view: Mapping[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """The three mutants of one view, each with what it must do."""
    side, corners = corners_of(view)
    unit = Fraction(1, side.denominator)
    left, right, gap, (nx, ny) = tightest_pair(view)
    overlap: dict[str, Any] | None = None
    excess = unit
    for _ in range(200):
        step = gap + excess
        moved = _moved(view, right, step * nx, step * ny)
        _side, moved_corners = corners_of(moved)
        if independent.pair_gap(moved_corners[left], moved_corners[right]) < 0:
            overlap = moved
            break
        excess *= 2
    if overlap is None:
        raise RegistrationError(f"n={view['n']}: no small move overlaps the tightest pair")
    clearance = min(
        side - coordinate for square in corners for point in square for coordinate in point
    )
    return [
        (
            overlap,
            {
                "control": "tightest-pair-overlapped",
                "squares": [left + 1, right + 1],
                "exact_gap": float(gap),
                "moved_by_gap_plus": float(excess),
                "expect": "refused",
            },
        ),
        (
            _resized(view, side - clearance - unit),
            {
                "control": "side-shrunk-past-clearance",
                "clearance": float(clearance),
                "unit": float(unit),
                "expect": "refused",
            },
        ),
        (
            _resized(view, side - unit),
            {
                "control": "side-shrunk-one-unit",
                "clearance": float(clearance),
                "unit": float(unit),
                "expect": "accepted" if clearance > unit else "refused",
            },
        ),
    ]


def control_rows(n: int) -> list[dict[str, Any]]:
    from sqpack.witness import exact_verify  # noqa: PLC0415

    rows: list[dict[str, Any]] = []
    for mutant, row in control_views(read_view(n)):
        first, _report = exact_verify(mutant)
        side, corners = corners_of(mutant)
        second = independent.check_squares(corners, side)
        verdicts = {
            "exact_verify": bool(first["verification_passed"]),
            "independent": bool(second["verification_passed"]),
        }
        accepted = row["expect"] == "accepted"
        rows.append(
            {
                "n": n,
                **row,
                **verdicts,
                "as_expected": all(v == accepted for v in verdicts.values()),
            }
        )
    return rows


def run_controls() -> dict[str, Any]:
    started = time.process_time()
    rows: list[dict[str, Any]] = []
    for n in committed():
        these = control_rows(n)
        rows.extend(these)
        print(
            f"n={n}: " + ", ".join(f"{row['control']} {row['as_expected']}" for row in these),
            flush=True,
        )
    return {
        "format": FORMAT,
        "tool": f"{TOOL} controls",
        "what": (
            "Three mutants of each retained view, decided by both maintained routes: the "
            "tightest pair pushed into overlap and the box shrunk past its least top or right "
            "clearance, which both must refuse, and the box shrunk by one unit of the side's "
            "denominator, which both must accept where the clearance exceeds that unit. The "
            "overlap is judged by the independent checker's own pair gap, so its refusal of "
            "that mutant is circular; the mutant is invalid regardless, since a negative gap "
            "on every face axis means, by the separating-axis theorem, that the interiors meet."
        ),
        "controls": len(rows),
        "all_as_expected": all(row["as_expected"] for row in rows),
        "cpu_seconds": round(time.process_time() - started, 1),
        "rows": rows,
    }


# --------------------------------------------------------------------------------------
# The committed receipts
# --------------------------------------------------------------------------------------


@cache
def committed() -> dict[int, dict[str, Any]]:
    """The committed selection's rows, by count; empty before `select` has run."""
    if not SELECTION.is_file():
        return {}
    return {int(row["n"]): row for row in read_json(SELECTION)["rows"]}


def counts() -> tuple[int, ...]:
    return tuple(sorted(committed()))


def problems() -> list[str]:
    """The committed receipts against the retained views and the case records."""
    found: list[str] = []
    rows = committed()
    if not rows:
        return ["no selection is committed"]
    if set(rows) & EXCLUDED:
        found.append(f"selection holds excluded counts {sorted(set(rows) & EXCLUDED)}")
    decision = {int(row["n"]): row for row in read_json(DECISION)["rows"]}
    controls: dict[int, list[dict[str, Any]]] = {}
    for row in read_json(CONTROLS)["rows"]:
        controls.setdefault(int(row["n"]), []).append(row)
    for n, row in rows.items():
        if not view_path(n).is_file():
            found.append(f"n={n}: the view is not retained")
            continue
        side = Fraction(row["side"])
        if view_side(n) != side:
            found.append(f"n={n}: the retained view's side is not the selection's")
        decided = decision.get(n)
        if decided is None or Fraction(decided["side"]) != side:
            found.append(f"n={n}: the decision receipt does not hold this view")
        elif not (decided["exact_verify"]["passed"] and decided["independent"]["passed"]):
            found.append(f"n={n}: a maintained route refused the view")
        kinds = {item["control"] for item in controls.get(n, []) if item["as_expected"]}
        if len(kinds) != 3:
            found.append(f"n={n}: the controls did not all reach their outcomes")
        if printed_value(row["earlier_verified"]["value"], side)[0] != row["value"]:
            found.append(f"n={n}: the printed value is not the rule's")
        if side_text(side) != row["side_text"]:
            found.append(f"n={n}: the side's decimal is not the rule's")
        case = case_front(n)
        if case["verified_upper_bound"] != verified_block(row):
            found.append(f"n={n}: the case record's verified upper bound is not the view's")
        if at_t101_side(row) and row["earlier_verified"]["evidence"] != list(t101_replays()):
            found.append(f"n={n}: the side is T-101's, but the record held another ceiling")
        found.extend(least_view_problems(n, row))
    return found


def least_view_problems(n: int, row: Mapping[str, Any]) -> list[str]:
    """Whether the row's view is the least of its count's row-3 outputs, as far as the
    row shows it: every output's side where `select` recorded them (`row_three_sides`),
    else the `same` output's side, which is the witness's own (`witness_side`). A row of
    the first selection whose `solved` view was not taken records no side for it."""
    side = Fraction(row["side"])
    recorded = row.get("row_three_sides")
    if recorded is not None:
        if sorted(recorded) != sorted(row["outputs_at_row_3"]):
            return [f"n={n}: the recorded sides are not the row-3 outputs'"]
        if side != min(Fraction(value) for value in recorded.values()):
            return [f"n={n}: the registered view is not the least row-3 output"]
        return []
    witness = Fraction(row["witness_side"])
    if row["output"] == "same" and side != witness:
        return [f"n={n}: the same-side view is not at the witness's side"]
    if "same" in row["outputs_at_row_3"] and side > witness:
        return [f"n={n}: the registered view lies above the same-side view"]
    return []


# --------------------------------------------------------------------------------------
# The case-record layer: front matter
# --------------------------------------------------------------------------------------


def t101_replays() -> tuple[str, str]:
    """T-101's two replays here of Evan Daniel's certificates, which prove each
    certificate's side exactly: the independent implementation and the source's own."""
    from devtools import apply_exact_ceilings as t101  # noqa: PLC0415

    return t101.EXACT_REPLAY, t101.SOURCE_REPLAY


def at_t101_side(row: Mapping[str, Any]) -> bool:
    """Whether the registered side is exactly the side of Evan Daniel's earlier certificate
    of the same packing (T-101), which T-101's replays already prove."""
    return row["t101_side"] is not None and Fraction(row["t101_side"]) == Fraction(row["side"])


def verified_block(row: Mapping[str, Any]) -> dict[str, Any]:
    """The verified upper lane on the registered side. Where that side is T-101's, T-101's
    replays prove the same bound, the independent one among them, and stay cited first."""
    evidence = [*t101_replays(), EVIDENCE] if at_t101_side(row) else [EVIDENCE]
    return {"value": row["value"], "exact_form": row["side"], "evidence": evidence}


def _set_block(front: str, name: str, value: object) -> str:
    """Replace one top-level `packing` key, laid out as the generator lays out a record:
    its YAML at a width of 98 columns, indentation included."""
    import yaml  # noqa: PLC0415

    pattern = re.compile(rf"^  {name}:.*\n(?:(?:    |  - ).*\n)*", re.MULTILINE)
    if not pattern.search(front):
        raise RegistrationError(f"no {name} in the front matter")
    dumped = yaml.safe_dump({name: value}, allow_unicode=True, sort_keys=False, width=96)
    block = "".join("  " + line + "\n" for line in dumped.splitlines())
    return pattern.sub(lambda _match: block, front, count=1)


def trailing_blocker(row: Mapping[str, Any], evidence: Sequence[str]) -> dict[str, Any]:
    """The `mathematics` blocker where the bound and the report disagree."""
    gap = difference(row["value"], row["printed_side"])
    whose = (
        f"the exact side {t101_replays()[0]} and {EVIDENCE} both prove"
        if at_t101_side(row)
        else f"{EVIDENCE}'s exact side"
    )
    shown = (
        f"the rational in exact_form ({row['side_text']} {ROUNDED_WORDS})"
        if rounded_up(Fraction(row["side"]))
        else row["side_text"]
    )
    exact = f"{whose}, {shown}, printed as {row['value']},"
    form = row["printed_exact_form"]
    if form:
        rational = row["printed_exact_form_degree"] == 1
        kind = (
            "a rational side, which this certificate does not reach"
            if rational
            else "an irrational side, which no rational certificate reaches"
        )
        remedy = (
            "an exact certificate of the packing at that side"
            if rational
            else "an exact algebraic certificate of the packing at its closed-form side"
        )
        detail = (
            f"verified_upper_bound is {exact} which trails the report "
            f"{row['printed_side']} by {gap}, and the report's exact form {form}, "
            f"{kind}: the certificate's side lies "
            f"{scientific(row['above_exact_side_by'])} above it. Closing the gap needs "
            f"{remedy}."
        )
    else:
        detail = (
            f"verified_upper_bound is {exact} which trails the report "
            f"{row['printed_side']} by {gap}, more than half a unit of the "
            "report's last declared place, so the two do not agree at declared precision "
            "and the printed side itself is not certified here. Closing the gap needs a "
            "certificate at or below the printed side."
        )
    return {"kind": "mathematics", "detail": detail, "evidence": list(evidence)}


def front_matter(n: int, front: str) -> str:
    """The front matter with the verified upper lane on the registered view's side."""
    row = committed()[n]
    payload = load_yaml(front)["packing"]
    front = _set_block(front, "verified_upper_bound", verified_block(row))
    evidence = [item for item in payload["evidence"] if item != EVIDENCE]
    front = _set_block(front, "evidence", [EVIDENCE, *evidence])
    reported = payload["reported_upper_bound"]
    gap = set(reported.get("evidence") or [])
    replacement = (
        None if row["agrees_with_report"] else trailing_blocker(row, reported["evidence"])
    )
    blockers: list[dict[str, Any]] = []
    for blocker in payload.get("blockers") or []:
        ours = blocker.get("kind") == "mathematics" and bool(
            gap & set(blocker.get("evidence") or [])
        )
        if not ours:
            blockers.append(blocker)
        elif replacement is not None:
            blockers.append(replacement)
            replacement = None
    if replacement is not None:
        blockers.insert(0, replacement)
    if blockers == list(payload.get("blockers") or []):
        # Rewritten only where they change, so the other blockers keep their layout.
        return front
    return _set_block(front, "blockers", blockers)


# --------------------------------------------------------------------------------------
# The case-record layer: body
# --------------------------------------------------------------------------------------


def _section_span(body: str, heading: str) -> tuple[int, int] | None:
    start = body.find(f"{heading}\n")
    if start < 0:
        return None
    end = body.find("\n## ", start + len(heading))
    end_comment = body.find("\n<!--", start + len(heading))
    candidates = [index for index in (end, end_comment) if index >= 0]
    return start, (min(candidates) + 1 if candidates else len(body))


def _remove_section(body: str, heading: str) -> tuple[str, int | None]:
    span = _section_span(body, heading)
    if span is None:
        return body, None
    return body[: span[0]] + body[span[1] :], span[0]


def _without_dated(body: str) -> str:
    start = body.find(DATED)
    if start < 0:
        return body
    end = body.find("\n\n", start)
    return body[:start] + body[end + 2 :]


def earlier_words(n: int, row: Mapping[str, Any]) -> str:
    earlier = row["earlier_verified"]
    if n in PACKING_RESULT:
        return (
            f"exactly `{earlier['value']}`, the upper endpoint of this project’s interval "
            f"certificate of the same packing ({PACKING_RESULT[n]})"
        )
    return (
        f"exactly `{earlier['value']}`, the side of Evan Daniel’s exact certificate of this "
        f"packing rounded up at the printed precision ({DEFAULT_PACKING_RESULT})"
    )


def _rounded(row: Mapping[str, Any], words: str) -> str:
    """`words` where prose writes the side rounded up, else nothing."""
    return words if rounded_up(Fraction(row["side"])) else ""


def dated_paragraph(n: int, row: Mapping[str, Any]) -> str:
    # Where nearest centres do not pair the view with the witness, its identity with the
    # credited packing is undecided, so the view is only made from the witness.
    made = "of this arrangement" if row["identity"]["one_to_one"] else "from that witness"
    proves = f"it proves `s({n}) ≤ {row['side_text']}`"
    if at_t101_side(row):
        bound = (
            f"{proves}, a bound Evan Daniel’s exact certificate of this packing already "
            f"proves at the same side ({DEFAULT_PACKING_RESULT}). The verified upper bound "
            "is now that side exactly, resting on both certificates "
            f"({DEFAULT_PACKING_RESULT}, {RESULT}), and the record still prints it as "
            f"`{row['value']}`. Until then the verified upper bound was "
            f"{earlier_words(n, row)}."
        )
    else:
        bound = (
            f"{proves}, the verified upper bound ({RESULT})"
            f"{_rounded(row, ' ' + ROUNDED_WORDS)}, which the record still prints as "
            f"`{row['value']}`. Until then the verified upper bound was "
            f"{earlier_words(n, row)}."
        )
    return (
        f"{DATED} This project’s regularization pass, Evan Daniel’s exact solver and "
        "regularizer run here on this register’s witness, produced an exact rational "
        f"packing {made}, decided here over `ℚ` by two exact checkers: {bound}\n\n"
    )


def _how_made(row: Mapping[str, Any]) -> str:
    if row["output"] == "same":
        return (
            "and this project’s same-side re-solve then fixed the result’s tight contacts "
            "over `ℚ` at the witness’s own side"
        )
    return (
        "which wrote its certificate at the side the solver reached, the solved point "
        "scaled by `1 + 10^-20` and the side rounded up"
    )


def _side_words(n: int, row: Mapping[str, Any]) -> str:
    below = scientific(float(row["below_earlier_by"]))
    if n in PACKING_RESULT:
        return f"`{below}` below the endpoint of the interval certificate"
    if row["output"] == "solved" and float(row["below_t101_side_by"] or 0) == 0:
        return (
            f"`{below}` below the verified upper bound the record held before, which was "
            "that same side rounded up at the printed precision: it is the side of Evan "
            f"Daniel’s certificate of this packing ({DEFAULT_PACKING_RESULT})"
        )
    t101 = scientific(float(row["below_t101_side_by"]))
    return (
        f"`{below}` below the verified upper bound the record held before, and `{t101}` "
        f"below the side of Evan Daniel’s certificate of this packing "
        f"({DEFAULT_PACKING_RESULT}): it is the witness’s own side"
    )


def _identity_words(row: Mapping[str, Any]) -> str:
    ident = row["identity"]
    if not ident["one_to_one"]:
        return (
            "Measured against the witness under the box’s eight symmetries, its squares do "
            "not pair one to one with the witness’s by nearest centres; Evan Daniel’s "
            "regularizer reports it as the same packing by its sampled path test, and "
            "whether it is drawn as this packing waits for the regularized layer’s review."
        )
    moved = int(ident.get("moved") or 0)
    if not moved:
        moves = "none moves by more than `1e-3`"
    else:
        largest = scientific(round_up(float(ident["max_move"])))
        moves = (
            f"{moved} {'moves' if moved == 1 else 'move'} by more than `1e-3`, the largest by "
            f"`{largest}`"
        )
    turn = float(ident.get("max_turn_deg") or 0)
    turns = (
        "and none turns by more than `1e-6` as a sine"
        if not ident.get("turned")
        else f"and the largest turn is `{turn:.3g}` degrees"
    )
    return (
        "Measured against the witness under the box’s eight symmetries, its squares pair "
        f"one to one with the witness’s; {moves}, {turns}."
    )


def _drawing_words(row: Mapping[str, Any]) -> str:
    if row["drawing"] == "no-change":
        return "It draws the same picture as the witness, so the atlas drawing does not change."
    return (
        "It redraws the packing visibly, and is drawn only once the regularized layer admits "
        "it under the regularization policy."
    )


def section(n: int, row: Mapping[str, Any]) -> str:
    """The section on the registered certificate."""
    first = (
        "This project’s regularization pass of 11 and 12 October 2026 ran Evan Daniel’s "
        "exact solver and regularizer ([`evand/square-packing`]"
        "(https://github.com/evand/square-packing), MIT, vendored here) on this register’s "
        "witness for this count, with the `conservative` angle policy and `coincide` "
        f"placement, {_how_made(row)}. The result is an exact rational packing of the same "
        f"{n} squares in a square of side `{row['side_text']}`"
        f"{_rounded(row, ' (' + ROUNDED_WORDS + ')')}, {_side_words(n, row)}. "
        f"{_identity_words(row)} {_drawing_words(row)}"
    )
    proves = f"That proves `s({n}) ≤ {row['side_text']}`"
    printed = (
        f"prints it as `{row['value']}`, the decimal it printed before and an upper display "
        "of it"
    )
    if at_t101_side(row):
        bound = (
            f"{proves}. Evan Daniel’s certificate of this packing already proves the same "
            f"bound at the same side ({DEFAULT_PACKING_RESULT}), and its replay here, by two "
            "checkers that share no code with each other or with the source, is independent "
            "of the code that made this view. That side is the exact form of the case’s "
            f"`verified_upper_bound`, which cites both certificates ({DEFAULT_PACKING_RESULT}, "
            f"{RESULT}) and {printed}."
        )
    elif rounded_up(Fraction(row["side"])):
        bound = (
            f"{proves}, the verified upper bound ({RESULT}) {ROUNDED_WORDS}. The exact side, "
            "a rational, is the exact form of the case’s `verified_upper_bound`, which "
            f"{printed}."
        )
    else:
        bound = (
            f"{proves}, the verified upper bound ({RESULT}), the exact form of the case’s "
            f"`verified_upper_bound`, which {printed}."
        )
    second = (
        "Each pair and each wall is decided over `ℚ` twice, by `sqpack`’s exact "
        "separating-axis test and by an independent checker that shares no code with it, "
        "and both accept it; both refuse it with its tightest pair pushed into overlap and "
        f"with its box shrunk past its least clearance ([certificate]({PACKAGE_LINK})). The "
        "same two checkers accepted it in the run that made it, so this is a reproduction "
        f"with the producer’s code. {bound} It says nothing about optimality, and the "
        "packing stays its finders’."
    )
    return f"{SECTION}\n\n{first}\n\n{second}\n\n"


def ceiling_section(n: int, row: Mapping[str, Any]) -> str:
    """The ceiling section of a count whose bound and report disagree."""
    value, printed = row["value"], row["printed_side"]
    side = (
        f"the rational in its `exact_form`, `{row['side_text']}` {ROUNDED_WORDS},"
        if rounded_up(Fraction(row["side"]))
        else f"`{row['side_text']}`, exactly,"
    )
    proved = (
        f"Evan Daniel’s exact certificate of this packing (`{t101_replays()[0]}`, "
        f"{DEFAULT_PACKING_RESULT}) and by the exact regularized certificate of it "
        f"(`{EVIDENCE}`, {RESULT})"
        if at_t101_side(row)
        else f"the exact regularized certificate of this packing (`{EVIDENCE}`, {RESULT})"
    )
    first = (
        f"`verified_upper_bound` for this case is {side} proved by {proved}, and the record "
        f"prints it as `{value}`. As printed it is **larger** than the best known "
        f"`{printed}` two fields above it, by `{difference(value, printed)}`."
    )
    form = row["printed_exact_form"]
    if form:
        closing = (
            "That side is rational, so an exact certificate of the packing at that side "
            "would reach it. "
            if row["printed_exact_form_degree"] == 1
            else "That side is irrational, so no rational certificate reaches it. "
        )
        second = (
            f"It is not the value of `s({n})` and not a different packing: it is the "
            "certificate’s own exact side. The catalogue gives the packing’s side exactly, "
            f"as `{form}`, and the certificate’s side lies "
            f"`{scientific(row['above_exact_side_by'])}` above that, so it bounds the exact "
            f"side from above and does not reach it. {closing}"
        )
    else:
        second = (
            f"It is not the value of `s({n})` and not a different packing: it is the "
            "certificate’s own exact side. It lies "
            f"`{scientific(float(row['above_printed_side_by']))}` above the side the "
            "catalogue prints, more than half a unit of the printed side’s last place, so "
            "the two disagree at the printed precision and the printed side itself is not "
            "certified here. "
        )
    second += (
        "The `mathematics` blocker in the frontmatter records the difference. Read "
        "`reported_upper_bound` for the best known side length."
    )
    history = ""
    if n in PACKING_RESULT:
        earlier = row["earlier_verified"]
        history = (
            f"\n\nUntil {DATE_WORDS} that printed decimal was the bound exactly, the upper "
            f"endpoint of this project’s interval certificate (`{earlier['evidence'][0]}`, "
            f"{PACKING_RESULT[n]}) at a declared relaxation of `1e-20`, which on 30 August "
            "2026 had replaced an exact rational replay at `5.93388579981302587863645209`."
        )
    return f"{CEILING_HEADING}\n\n{first}\n\n{second}{history}\n\n"


#: T-101's sentences that name its rounded-up side the verified upper bound; after this
#: layer that is history. Math form and code form, across the formatter's line breaks.
_BOUND = r"(?:\$s\(\d+\)\s+\\le\s+[^$]+\$|`s\(\d+\)\s+≤\s+[^`]+`)"
_T101_DATED = re.compile(rf"(proves\s+{_BOUND}),\s+the\s+verified\s+upper\s+bound\s+\(T-101\)")
_T101_SECTION = re.compile(rf"(That\s+proves\s+{_BOUND}),\s+the\s+verified\s+upper\s+bound:")
_T101_AGREES = re.compile(
    r"The\s+verified\s+upper\s+bound\s+and\s+the\s+printed\s+side\s+now\s+agree\s+to\s+one"
)
#: n = 29's hand-written sentences on the interval certificate, put in the past.
_N029_VERIFIES = re.compile(
    r"(own\s+interval\s+certificate)\s+verifies\s+"
    r"(\$s\(29\)\s+\\le\s+5\.93383346267692918974379895098\$)"
)
_N029_ABOVE = re.compile(
    r"(The\s+verified\s+upper\s+value\s+is\s+not\s+the\s+reported\s+one:\s+it\s+sits\s+"
    r"above\s+it\s+by\s+)`[0-9.Ee+-]+`"
)


def _words(text: str) -> str:
    """`text` as a pattern that matches it across the formatter's line breaks."""
    return r"\s+".join(re.escape(word) for word in text.split())


#: What each rewrite above leaves behind, so a record already in the past is recognized.
_T101_DATED_PAST = re.compile(
    _words(f"the verified upper bound from 6 to {DATE_WORDS} ({DEFAULT_PACKING_RESULT})")
)
_T101_SECTION_PAST = re.compile(_words(f"the verified upper bound until {DATE_WORDS}:"))
_T101_AGREES_PAST = re.compile(_words("Its rounded-up side and the printed side agree to one"))
_N029_VERIFIES_PAST = re.compile(_words("own interval certificate verified") + r"\s+\$s\(29\)")


def _rewrite(
    n: int, body: str, pattern: re.Pattern[str], replacement: Any, past: re.Pattern[str]
) -> str:
    """`body` with `pattern` rewritten into the past, refusing a record where the sentence
    is in neither tense: the earlier layer reworded it, and a sentence this layer no longer
    finds would go on calling a superseded ceiling the verified upper bound."""
    rewritten, count = pattern.subn(replacement, body)
    if not count and not past.search(rewritten):
        raise RegistrationError(
            f"n={n}: neither the earlier ceiling's sentence /{pattern.pattern}/ nor its past "
            "tense is in the record; reword the pattern to the earlier layer's prose"
        )
    return rewritten


def past_tense(n: int, body: str, row: Mapping[str, Any]) -> str:
    """The earlier ceiling's sentences put in the past. Each sentence the earlier layer
    wrote must be found, in the present tense or already in the past, or the record is
    refused (`_rewrite`)."""
    if n not in PACKING_RESULT:
        body = _rewrite(
            n,
            body,
            _T101_DATED,
            rf"\1, the verified upper bound from 6 to {DATE_WORDS} ({DEFAULT_PACKING_RESULT})",
            _T101_DATED_PAST,
        )
        body = _rewrite(
            n,
            body,
            _T101_SECTION,
            rf"\1, the verified upper bound until {DATE_WORDS}:",
            _T101_SECTION_PAST,
        )
        if row["agrees_with_report"]:
            # T-101 wrote this sentence only where its rounded-up side agreed with the report,
            # and the value it printed, which this layer keeps, agrees exactly where it did.
            body = _rewrite(
                n,
                body,
                _T101_AGREES,
                "Its rounded-up side and the printed side agree to one",
                _T101_AGREES_PAST,
            )
        if f"{T101_SECTION}\n" in body:
            body = body.replace(f"{T101_SECTION}\n", f"{T101_EARLIER}\n", 1)
        elif f"{T101_EARLIER}\n" not in body:
            raise RegistrationError(f"n={n}: no section on the earlier exact certificate")
    if n == 29:
        now = markdown_math(f"`s(29) ≤ {row['side_text']}`")
        body = _rewrite(
            n,
            body,
            _N029_VERIFIES,
            lambda match: (
                f"{match.group(1)} verified {match.group(2)} until {DATE_WORDS}, and its "
                f"exact regularized certificate now verifies {now}"
            ),
            _N029_VERIFIES_PAST,
        )
        gap = difference(row["value"], row["printed_side"]).replace("e", "E")
        # The gap is restated on every application, so the sentence is always present.
        body = _rewrite(
            n,
            body,
            _N029_ABOVE,
            lambda match: f"{match.group(1)}`{gap}`",
            re.compile(r"(?!)"),
        )
    return body


def body_text(n: int, body: str) -> str:
    row = committed()[n]
    body = _without_dated(body)
    title = re.search(r"^# .*\n\n", body, flags=re.MULTILINE)
    if title is None:
        raise RegistrationError(f"n={n}: no title")
    body = body[: title.end()] + markdown_math(dated_paragraph(n, row)) + body[title.end() :]
    body, own = _remove_section(body, SECTION)
    body, ceiling = _remove_section(body, CEILING_HEADING)
    places = [index for index in (own, ceiling) if index is not None]
    if not places:
        for heading in (T101_SECTION, T101_EARLIER, "## The packing"):
            span = _section_span(body, heading)
            if span is not None:
                places.append(span[0])
                break
    if not places:
        raise RegistrationError(f"n={n}: no section to place the certificate before")
    place = min(places)
    written = ("" if row["agrees_with_report"] else ceiling_section(n, row)) + section(n, row)
    body = body[:place] + markdown_math(written) + body[place:]
    return past_tense(n, body, row)


def apply_case(n: int, text: str) -> str:
    """One case record with its verified upper lane on the registered view; others
    unchanged."""
    if n not in committed():
        return text
    _, front, body = text.split("---\n", 2)
    return f"---\n{front_matter(n, front)}---\n{body_text(n, body)}"


# --------------------------------------------------------------------------------------
# The package README's table
# --------------------------------------------------------------------------------------


def _shown(value: str, digits: int = 22) -> str:
    """A long decimal cut after `digits` characters and marked, rounded up so a bound
    stays one; a short one whole."""
    if len(value) <= digits + 2:
        return value
    places = digits - value.index(".") - 1
    return format(ceiling_decimal(Fraction(Decimal(value)), places), "f") + "…"


def table() -> str:
    """One row per registered count, from the committed selection."""
    header = (
        "| n | View | Exact side | Printed as | Below the earlier bound by "
        "| Below T-101’s side by | Agrees | Drawing | Moved, largest |"
    )
    lines = [header, "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for n, row in sorted(committed().items()):
        ident = row["identity"]
        moved = (
            f"{ident['moved']}, `{scientific(round_up(float(ident['max_move'])))}`"
            if ident["one_to_one"] and ident.get("moved")
            else ("none" if ident["one_to_one"] else "not one to one")
        )
        t101 = row["below_t101_side_by"]
        after = row["after_registration"]["decision"] or row["drawing"]
        margin = "0" if t101 == 0 else f"`{scientific(float(t101 or 0))}`"
        lines.append(
            f"| {n} | `{row['output']}` | `{_shown(row['side_text'])}` "
            f"| `{row['value']}` "
            f"| `{scientific(float(row['below_earlier_by']))}` "
            f"| {'—' if t101 is None else margin} "
            f"| {'yes' if row['agrees_with_report'] else 'no'} "
            f"| {row['drawing']}, then {after} | {moved} |"
        )
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------------------


def _normalized(text: str) -> str:
    from devtools.apply_upper_bound_packets import normalized  # noqa: PLC0415

    return normalized(text)


def main(argv: Sequence[str] | None = None) -> int:
    from devtools import render_case_verifiers  # noqa: PLC0415

    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("command", nargs="?", choices=("select", "decide", "controls", "table"))
    parser.add_argument("--run-dir", type=Path, nargs="+", default=[])
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args(argv)
    if args.command == "select":
        if not args.run_dir:
            parser.error("select needs --run-dir")
        receipt = select([path.resolve() for path in args.run_dir])
        write_json(SELECTION, receipt)
        print(f"{len(receipt['registered'])} counts selected: {receipt['registered']}")
        return 0
    if args.command == "table":
        print(table(), end="")
        return 0
    if args.command == "decide":
        receipt = decide_all()
        write_json(DECISION, receipt)
        print(f"{receipt['decided']} views decided; all passed: {receipt['all_passed']}")
        return 0 if receipt["all_passed"] else 1
    if args.command == "controls":
        receipt = run_controls()
        write_json(CONTROLS, receipt)
        print(f"{receipt['controls']} controls; all as expected: {receipt['all_as_expected']}")
        return 0 if receipt["all_as_expected"] else 1
    drift: list[Path] = []
    for n in counts():
        path = FRONTIER / f"n-{n:03d}.md"
        text = path.read_text(encoding="utf-8")
        rendered = render_case_verifiers.refresh(apply_case(n, text))
        if _normalized(rendered) != _normalized(text):
            drift.append(path)
            if not args.check:
                with atomic_output_file(path) as temporary:
                    temporary.write_text(rendered, encoding="utf-8")
    found = problems() if args.check else []
    for problem in found:
        print(f"FAIL {problem}", file=sys.stderr)
    for path in drift:
        print(("drift: " if args.check else "wrote: ") + str(path.relative_to(ROOT)))
    if not drift and not found:
        print(f"the {len(counts())} records and the receipts are current")
    return 1 if found or (args.check and drift) else 0


if __name__ == "__main__":
    sys.exit(main())
