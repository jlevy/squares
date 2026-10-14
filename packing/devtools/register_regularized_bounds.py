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

**The second batch.** Under the policy's section 9, question 16 (the owner, 13 October
2026), an exactly verified side below `U` is registered as a result however it was made.
It is a new upper bound only where no larger count's verified upper bound is at or below
it; otherwise the result says that its bound follows by monotonicity and names the
result that proves it (**A bound already implied**, below). A view of
`devtools.regularize_grid_slack`, this project's port of Evan Daniel's coincidence
placement, decided at row 3 is registered so, as a batch of its own, T-156 the first
(`GRID`): `select --batch grid-slack` reads the named counts' reports in the named runs,
decides each view by the policy's table against the case record's bound
(`regularize_grid_slack.decided`), and takes at each count the row-3 view with the least
exact side, the first run named among equals. A view is refused unless it was derived
from the checkout's witness and its side is that witness's own `s_W`, which every row-3
grid-slack view's is: the generator's other side is the bound itself. The row records
`s_W` as read from the witness, and `--check` reads the witness again. Its receipts and
view lie under `cases/regularized_bounds/grid-slack-2026-10-13/`, laid out as the first
batch's are, and the case-record layer below writes each count in the words of its
batch's generator kind (`Batch.kind`), so a later grid-slack batch is written as this
one is. The batches are disjoint.

**A bound already implied.** `s(n) ≤ s(n + 1)`, since deleting a square from a packing
leaves a packing in the same square, so a ceiling at the next count at or below a view's
side already proves the view's bound. A grid-slack row records a ceiling at the view's
side, its evidence and the results that hold it (`implied_by`), and the case record says
the bound was not new: T-155's certificate at `n = 291`, at exactly the side T-156
registers, proved `s(290)`'s bound from 12 October 2026, and T-156 is kept as the
certificate of 290's own packing at that side (the owner's decision of 13 October 2026,
on jlevy/squares#587). `select` refuses a view whose side lies above the next count's
ceiling, since the record would then carry a weaker ceiling than the register proves; such
a count's bound is registered by monotonicity instead. The next count suffices, since
`test_verified_upper_bound_contract` holds every ceiling at or below the next count's.

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
    select --batch grid-slack --run-dir RUN [RUN ...] --n N [N ...]
    decide [--batch grid-slack]
    controls [--batch grid-slack]
    table [--batch grid-slack]
    [--check]

`decide`, `controls` and `table` act on the first batch unless `--batch` names another;
with no command, the case records of every batch are written, or checked with `--check`.
`--run-dir` and `--n` are refused on any other command, and `--n` on a batch of Evan
Daniel's regularizer, whose `select` takes every row-3 count of its runs. `select` writes
the views and the selection only once every refusal has run.
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
from dataclasses import dataclass
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
#: Headings this layer writes; each batch's dated marker is `Batch.dated`.
SECTION = "## The regularized exact certificate"
CEILING_HEADING = "## The verified upper bound is a ceiling"
T101_SECTION = "## The exact certificate"
T101_EARLIER = "## The earlier exact certificate"


#: The generator kinds a batch's views come from: Evan Daniel's regularizer through the
#: vendored driver (`devtools.regularize_evand`), whose runs keep a receipt and report two
#: outputs a count, and this project's grid-slack port of his coincidence placement
#: (`devtools.regularize_grid_slack`), whose runs report one view a count. What a batch
#: selects, and how its records are worded, follow its kind, never its identity.
EVAND_KIND = "evand"
GRID_KIND = "grid-slack"


@dataclass(frozen=True)
class Batch:
    """One registration: a register result over the views of one generator kind's runs,
    with its receipts and views under `package`. The batches are disjoint, and each count's
    record is written in the words of the kind of the batch that holds it."""

    name: str
    kind: str
    result: str
    evidence: str
    registered: str
    date_words: str
    package: Path
    #: The counts the batch never registers.
    excluded: frozenset[int] = HELD
    #: The days its runs ran, in words, where they are not the day it was registered.
    run_dates: str = ""
    #: The package README's section on this batch, where the batch is not its subject.
    anchor: str = ""

    @property
    def ran(self) -> str:
        """The days the batch's runs ran, in words."""
        return self.run_dates or self.date_words

    @property
    def views(self) -> Path:
        return self.package / "views"

    @property
    def selection(self) -> Path:
        return self.package / "selection.json"

    @property
    def decision(self) -> Path:
        return self.package / "exact-decision.json"

    @property
    def controls(self) -> Path:
        return self.package / "negative-controls.json"

    @property
    def dated(self) -> str:
        """The marker of the dated paragraph this batch writes on a case record."""
        return f"**Exact regularized certificate, {self.registered}.**"

    @property
    def link(self) -> str:
        """The package README, or its section on this batch, as a case record links it."""
        return PACKAGE_LINK + (f"#{self.anchor}" if self.anchor else "")

    def command(self, verb: str) -> str:
        """This tool's command line for `verb` on this batch."""
        return f"{TOOL} {verb}" + ("" if self.name == FIRST_NAME else f" --batch {self.name}")


FIRST_NAME = "evand"
#: The views of Evan Daniel's regularizer from the full run of 11 and 12 October 2026 and
#: its re-runs (T-155).
FIRST = Batch(
    FIRST_NAME,
    EVAND_KIND,
    RESULT,
    EVIDENCE,
    REGISTERED,
    DATE_WORDS,
    PACKAGE,
    excluded=EXCLUDED,
    run_dates="11 and 12 October 2026",
)
#: The views of this project's grid-slack regularizer, its port of Evan Daniel's
#: coincidence placement, from the runs of 13 October 2026 (T-156).
GRID = Batch(
    "grid-slack",
    GRID_KIND,
    "T-156",
    "E-regularized-bounds-2026-10-13-grid-slack-exact-decision",
    "2026-10-13",
    "13 October 2026",
    PACKAGE / "grid-slack-2026-10-13",
    anchor="the-grid-slack-batch",
)
BATCHES = (FIRST, GRID)
BATCH_NAMES = {batch.name: batch for batch in BATCHES}


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


def view_path(n: int, batch: Batch = FIRST) -> Path:
    return batch.views / f"n-{n:03d}.yaml.gz"


def read_view(n: int, batch: Batch = FIRST) -> dict[str, Any]:
    """A retained view's Witness/v2 body."""
    document = load_yaml(gzip.decompress(view_path(n, batch).read_bytes()).decode("utf-8"))
    return dict(document["witness"])


_VIEW_SIDE = re.compile(r"^  side: '?([0-9/.]+)'?$", re.MULTILINE)


def view_side(n: int, batch: Batch = FIRST) -> Fraction:
    """A retained view's stated side, read without parsing its squares."""
    match = _VIEW_SIDE.search(gzip.decompress(view_path(n, batch).read_bytes()).decode("utf-8"))
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


def earlier_bound(n: int, case: Mapping[str, Any], batch: Batch = FIRST) -> dict[str, Any]:
    """The verified upper bound the case held before `batch` registered it: the record's
    own, or, once the record carries the registration, the one the committed selection
    read from it then."""
    upper = case["verified_upper_bound"]
    if batch.evidence in (upper.get("evidence") or []):
        if n not in committed(batch):
            raise RegistrationError(f"n={n}: the record carries a registration no row holds")
        return dict(committed(batch)[n]["earlier_verified"])
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
    if witness.get("id") != source.get("id"):
        raise RegistrationError(
            f"n={n}: the run read witness {source.get('id')}, not the checkout's "
            f"{witness.get('id')}"
        )
    if frame.side != Fraction(str(source.get("s_W_exact"))):
        raise RegistrationError(
            f"n={n}: the run read its witness at another side than the checkout witness's "
            "own s_W"
        )
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


#: A view's bytes as its run wrote them, by count: what `retain` writes under a batch's
#: `views/` once every row of its selection has passed.
Views = dict[int, bytes]


def retain(batch: Batch, views: Mapping[int, bytes]) -> None:
    """Write a selection's views, gzip-compressed, after every refusal has run."""
    for n, data in sorted(views.items()):
        with atomic_output_file(view_path(n, batch), make_parents=True) as temporary:
            temporary.write_bytes(gzip.compress(data, compresslevel=9, mtime=0))


def selection_row(
    n: int, run: str, directory: Path, report: Mapping[str, Any], batch: Batch = FIRST
) -> tuple[dict[str, Any], bytes]:
    """One count's registered view, with what the record needs about it, and the view's
    bytes, which `retain` writes once the whole selection has passed."""
    from devtools.apply_exact_ceilings import bound_value  # noqa: PLC0415

    case = case_front(n)
    earlier = earlier_bound(n, case, batch)
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
    row = {
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
    return row, data


def select(run_dirs: Sequence[Path], batch: Batch = FIRST) -> tuple[dict[str, Any], Views]:
    """Every row-3 count outside the batch's `excluded`, its least view measured: the
    receipt, and the views `retain` writes. Nothing is written here, so a refused
    selection leaves the package as it was."""
    reports = latest_reports(run_dirs)
    candidates = sorted(
        n for n, (_run, _directory, report) in reports.items() if row_three(report)
    )
    built = [
        selection_row(n, *reports[n], batch) for n in candidates if n not in batch.excluded
    ]
    rows = [row for row, _data in built]
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
    receipt = {
        "format": FORMAT,
        "tool": batch.command("select"),
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
        "excluded": sorted(set(candidates) & batch.excluded),
        "registered": [row["n"] for row in rows],
        "rows": rows,
    }
    return receipt, {row["n"]: data for row, data in built}


# --------------------------------------------------------------------------------------
# select, the grid-slack batch
# --------------------------------------------------------------------------------------


def grid_reports(
    run_dirs: Sequence[Path], numbers: Sequence[int]
) -> dict[int, list[tuple[str, Path, dict[str, Any]]]]:
    """Each named count's grid-slack reports, in the order the runs are named."""
    names = [run_dir.name for run_dir in run_dirs]
    if len(set(names)) != len(names):
        raise RegistrationError(f"two runs share a name: {names}")
    reports: dict[int, list[tuple[str, Path, dict[str, Any]]]] = {}
    for run_dir in run_dirs:
        for n in numbers:
            directory = run_dir / f"n-{n:03d}"
            if (directory / "report.json").is_file():
                reports.setdefault(n, []).append(
                    (run_dir.name, directory, read_json(directory / "report.json"))
                )
    return reports


def next_count_ceiling(n: int) -> dict[str, Any] | None:
    """The next count's verified upper bound, as a rational, and its evidence: the exact
    form where that is a rational, else the decimal, an upper display of the bound, so a
    comparison with it never overstates what the bound proves."""
    path = FRONTIER / f"n-{n + 1:03d}.md"
    if not path.is_file():
        return None
    upper = case_front(n + 1)["verified_upper_bound"]
    try:
        bound = Fraction(str(upper.get("exact_form")))
    except ValueError:
        bound = Fraction(Decimal(str(upper["value"])))
    return {"bound": bound, "evidence": list(upper.get("evidence") or [])}


def results_holding(n: int, evidence: Sequence[str]) -> list[str]:
    """The register's upper-bound results at `n` that cite any of `evidence`."""
    register = load_yaml((FRONTIER / "results.yaml").read_text(encoding="utf-8"))
    return [
        str(result["id"])
        for result in register["results"]
        if result["kind"] in {"upper-bound", "optimality"}
        and n in (result.get("scope") or {}).get("n_values", [])
        and set(evidence) & set(result.get("evidence") or [])
    ]


def implied_by(n: int, side: Fraction) -> dict[str, Any] | None:
    """The next count's verified upper bound where it is at or below `side`, which already
    proves `s(n) ≤ side`: `s(n) ≤ s(n + 1)`, since deleting a square from a packing leaves
    a packing in the same square. Its exact bound, its evidence and the results that hold
    it, as the record stood when the view was selected; `None` where it lies above `side`.
    A larger count's lower ceiling would be the next count's own gap first, which
    `test_verified_upper_bound_contract` holds the register against."""
    found = next_count_ceiling(n)
    if found is None or found["bound"] > side:
        return None
    results = results_holding(n + 1, found["evidence"])
    if not results:
        raise RegistrationError(f"n={n + 1}: no registered result holds the verified bound")
    return {
        "n": n + 1,
        "side": literal(found["bound"]),
        "evidence": found["evidence"],
        "results": results,
    }


def grid_selection_row(
    n: int, found: Sequence[tuple[str, Path, Mapping[str, Any]]], batch: Batch = GRID
) -> tuple[dict[str, Any], bytes]:
    """One count's least row-3 grid-slack view among the runs, with what the record needs
    about it, in the terms `selection_row` gives a view of the first batch, and the view's
    bytes, which `retain` writes once the whole selection has passed. The view's sides are
    keyed by run (`run_sides`), as the first batch's are by output."""
    from devtools import apply_exact_ceilings as t101  # noqa: PLC0415
    from devtools import regularize_evand as driver  # noqa: PLC0415
    from devtools import regularize_grid_slack as grid  # noqa: PLC0415
    from devtools.regularized_drawings import grid_written_method  # noqa: PLC0415

    case = case_front(n)
    earlier = earlier_bound(n, case, batch)
    upper = t101.bound_value(earlier)
    witness = grid.load_source(n)
    frame = driver.source_frame(witness)
    held: list[tuple[str, Path, Mapping[str, Any], driver.Decision]] = []
    for run, directory, report in found:
        if report.get("generator") != grid.GENERATOR:
            raise RegistrationError(
                f"n={n}: {run} holds a view of {report.get('generator')}, not of "
                f"{grid.GENERATOR}"
            )
        decision = grid.decided(report, witness, upper=upper)
        if decision.row == 3:
            held.append((run, directory, report, decision))
    if not held:
        raise RegistrationError(f"n={n}: no named run's view is decided at row 3")
    sides = {
        run: literal(Fraction(str(report["attempts"][-1]["exact"]["side"])))
        for run, _directory, report, _decision in held
    }
    # The least side; among equal sides, the first run named.
    run, directory, report, decision = min(held, key=lambda item: Fraction(sides[item[0]]))
    exact = report["attempts"][-1]["exact"]
    side = Fraction(sides[run])
    if not side < upper:
        raise RegistrationError(f"n={n}: the view is not below the verified upper bound")
    if not all(exact["verdicts"][route]["passed"] for route in ("exact_verify", "independent")):
        raise RegistrationError(f"n={n}: a maintained route refused the view in the run")
    data = gzip.decompress((directory / "view.yaml.gz").read_bytes())
    view = dict(load_yaml(data.decode("utf-8"))["witness"])
    if Fraction(str(view["side"])) != side:
        raise RegistrationError(f"n={n}: the view's side is not the report's")
    derived = (view.get("certificate") or {}).get("derived_from")
    if derived != witness.get("id"):
        raise RegistrationError(
            f"n={n}: the view was derived from {derived}, not the checkout's witness "
            f"{witness.get('id')}"
        )
    # The generator's other side is the bound itself, never below it, so a row-3 view is
    # the same-side view, at the witness's own exact side `s_W`.
    if exact.get("relation") != "same":
        raise RegistrationError(
            f"n={n}: the run labels its row-3 view {exact.get('relation')!r}, not the "
            "same-side view"
        )
    if frame.side is None or side != frame.side:
        raise RegistrationError(f"n={n}: the view's side is not the checkout witness's own s_W")
    # A larger count's ceiling below the side proves more than the view does: the record
    # would carry a weaker ceiling than the register proves (review C4).
    implied = implied_by(n, side)
    if implied is not None and Fraction(implied["side"]) < side:
        raise RegistrationError(
            f"n={n}: the record already proves s({n}) ≤ "
            f"{side_text(Fraction(implied['side']))} by monotonicity from "
            f"{', '.join(implied['results'])}; register the count by monotonicity"
        )
    straightened = [int(row["square"]) for row in report.get("straightened") or []]
    identity = measure_identity(
        n,
        view,
        [square - 1 for square in straightened],
        {"id": witness.get("id"), "s_W_exact": literal(frame.side)},
    )
    t101_row = t101.committed().get(n)
    if t101_row is None and n not in PACKING_RESULT:
        raise RegistrationError(f"n={n}: no registered result named for the packing")
    t101_side = Fraction(t101_row["certified_side"]) if t101_row else None
    reported = case["reported_upper_bound"]
    value, raised = printed_value(earlier["value"], side)
    verified = {"value": value, "exact_form": literal(side)}
    above_form, degree = _closed_form_facts(reported, side)
    after = grid.decided(report, witness, upper=side)
    row = {
        "n": n,
        "run": run,
        "output": "same",
        "runs_at_row_3": [item[0] for item in held],
        "run_sides": sides,
        "side": literal(side),
        "side_decimal": decimal_text(side),
        "side_text": side_text(side),
        "value": value,
        "value_raised": raised,
        "earlier_verified": earlier,
        "below_earlier_by": float(f"{float(upper - side):.4e}"),
        "implied_by": implied,
        "t101_side": literal(t101_side) if t101_side is not None else None,
        "below_t101_side_by": (
            float(f"{float(t101_side - side):.4e}") if t101_side is not None else None
        ),
        "witness_side": literal(frame.side),
        "witness_frame": frame.derivation,
        "printed_side": str(reported["value"]),
        "printed_exact_form": reported.get("exact_form"),
        "printed_exact_form_degree": degree,
        "above_printed_side_by": float(
            f"{float(side - Fraction(Decimal(str(reported['value'])))):.4e}"
        ),
        "above_exact_side_by": above_form,
        "agrees_with_report": bounds_agree_at_declared_precision(reported, verified),
        "drawing": decision.decision,
        "decided": {"row": decision.row, "reason": decision.reason},
        "after_registration": {
            "decision": after.decision,
            "index_record": after.index_record,
            "reason": after.reason,
        },
        "identity": identity,
        "regularization": {
            "of": PACKING_RESULT.get(n, DEFAULT_PACKING_RESULT),
            "method": grid_written_method(grid.METHOD),
            "side": "same",
            "changes": {},
        },
        "straightened": straightened,
        "generator": {"name": report.get("generator"), "settings": report.get("settings")},
    }
    return row, data


def select_grid(
    run_dirs: Sequence[Path], numbers: Sequence[int], batch: Batch = GRID
) -> tuple[dict[str, Any], Views]:
    """The named counts' least row-3 grid-slack views among the named runs, measured: a
    grid-slack batch's receipt (T-156's the first), and the views `retain` writes. Nothing
    is written here, so a refused selection leaves the package as it was."""
    wanted = sorted(set(numbers))
    excluded = sorted(set(wanted) & batch.excluded)
    if excluded:
        raise RegistrationError(f"counts {excluded} are held, and {batch.result} excludes them")
    for other in BATCHES:
        taken = sorted(set(wanted) & set(committed(other))) if other.name != batch.name else []
        if taken:
            raise RegistrationError(f"counts {taken} are registered by {other.result}")
    reports = grid_reports(run_dirs, wanted)
    missing = sorted(set(wanted) - set(reports))
    if missing:
        raise RegistrationError(f"no named run reports counts {missing}")
    built = [grid_selection_row(n, reports[n], batch) for n in wanted]
    rows = [row for row, _data in built]
    runs = []
    for run_dir in run_dirs:
        these = [
            report for n in wanted for run, _d, report in reports[n] if run == run_dir.name
        ]
        settings = [dict(report.get("settings") or {}) for report in these]
        if any(setting != settings[0] for setting in settings):
            raise RegistrationError(f"{run_dir.name}: its reports differ in their settings")
        runs.append(
            {
                "run": run_dir.name,
                "generator": sorted({str(report.get("generator")) for report in these}),
                "parameters": settings[0] if settings else {},
                "counts": [int(report["n"]) for report in these],
                "cost": {
                    "cpu_seconds": round(
                        sum(float(report.get("seconds") or 0) for report in these), 2
                    ),
                    "note": (
                        "the seconds these counts' reports record, summed; a grid-slack run "
                        "keeps no receipt of its own"
                    ),
                },
            }
        )
    receipt = {
        "format": FORMAT,
        "tool": batch.command("select"),
        "policy": POLICY,
        "what": (
            "Each named count's view of this project's grid-slack regularizer "
            "(devtools.regularize_grid_slack, its port of Evan Daniel's coincidence "
            "placement) decided at row 3 of the policy's table, its side below the case's "
            "verified upper bound: the view with the least exact side among the named runs, "
            "the first run named among equals, retained under views/, with every run's side "
            "at row 3 keyed by run (run_sides, runs_at_row_3, where the first batch keys its "
            "outputs), the bound the record held before, the next count's ceiling where it "
            "already implies the bound (implied_by), the witness's own side as read from it, "
            "the printed side and closed form, the drawing decision before and after "
            "registration, and the identity measured on the retained view against the "
            "witness's exact frame."
        ),
        "runs": runs,
        "candidates": wanted,
        "excluded": [],
        "registered": [row["n"] for row in rows],
        "rows": rows,
    }
    return receipt, {row["n"]: data for row, data in built}


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


def decide_all(batch: Batch = FIRST) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for n in committed(batch):
        view = read_view(n, batch)
        if Fraction(str(view["side"])) != Fraction(committed(batch)[n]["side"]):
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
        "tool": batch.command("decide"),
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


def control_rows(n: int, batch: Batch = FIRST) -> list[dict[str, Any]]:
    from sqpack.witness import exact_verify  # noqa: PLC0415

    rows: list[dict[str, Any]] = []
    for mutant, row in control_views(read_view(n, batch)):
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


def run_controls(batch: Batch = FIRST) -> dict[str, Any]:
    started = time.process_time()
    rows: list[dict[str, Any]] = []
    for n in committed(batch):
        these = control_rows(n, batch)
        rows.extend(these)
        print(
            f"n={n}: " + ", ".join(f"{row['control']} {row['as_expected']}" for row in these),
            flush=True,
        )
    return {
        "format": FORMAT,
        "tool": batch.command("controls"),
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
def committed(batch: Batch = FIRST) -> dict[int, dict[str, Any]]:
    """A batch's committed selection rows, by count; empty before `select` has run."""
    if not batch.selection.is_file():
        return {}
    return {int(row["n"]): row for row in read_json(batch.selection)["rows"]}


def counts(batch: Batch = FIRST) -> tuple[int, ...]:
    return tuple(sorted(committed(batch)))


def batch_of(n: int) -> Batch | None:
    """The batch whose committed selection holds `n`, if any; the batches are disjoint."""
    return next((batch for batch in BATCHES if n in committed(batch)), None)


def holder(n: int) -> tuple[Batch, dict[str, Any]]:
    """The batch that registers `n`, and its row."""
    batch = batch_of(n)
    if batch is None:
        raise RegistrationError(f"n={n}: no batch registers this count")
    return batch, committed(batch)[n]


def problems(batch: Batch = FIRST) -> list[str]:
    """A batch's committed receipts against its retained views and the case records."""
    found: list[str] = []
    rows = committed(batch)
    if not rows:
        return [f"no selection of {batch.result} is committed"]
    if set(rows) & batch.excluded:
        found.append(f"selection holds excluded counts {sorted(set(rows) & batch.excluded)}")
    # Each pair of batches once: a batch is held against the batches before it.
    earlier = BATCHES[: BATCHES.index(batch)] if batch in BATCHES else BATCHES
    found.extend(
        f"{batch.result} and {other.result} both register {shared}"
        for other in earlier
        if (shared := sorted(set(rows) & set(committed(other))))
    )
    decision = {int(row["n"]): row for row in read_json(batch.decision)["rows"]}
    controls: dict[int, list[dict[str, Any]]] = {}
    for row in read_json(batch.controls)["rows"]:
        controls.setdefault(int(row["n"]), []).append(row)
    for n, row in rows.items():
        if not view_path(n, batch).is_file():
            found.append(f"n={n}: the view is not retained")
            continue
        side = Fraction(row["side"])
        if view_side(n, batch) != side:
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
        if case["verified_upper_bound"] != verified_block(row, batch):
            found.append(f"n={n}: the case record's verified upper bound is not the view's")
        if at_t101_side(row) and row["earlier_verified"]["evidence"] != list(t101_replays()):
            found.append(f"n={n}: the side is T-101's, but the record held another ceiling")
        found.extend(least_view_problems(n, row))
        if batch.kind == GRID_KIND:
            found.extend(witness_problems(n, row, batch))
        implied = row.get("implied_by")
        if implied is not None and not (
            int(implied["n"]) > n and Fraction(implied["side"]) <= side
        ):
            found.append(f"n={n}: the ceiling the row says implies the bound does not")
        elif implied is not None and Fraction(implied["side"]) < side:
            found.append(
                f"n={n}: the ceiling at n = {implied['n']} lies below the side, so the "
                "record would carry a weaker ceiling than the register proves"
            )
    return found


def checkout_witness(n: int) -> tuple[str, Fraction | None]:
    """The checkout witness's id and exact side `s_W`, as the driver reads its frame."""
    from devtools import regularize_evand as driver  # noqa: PLC0415
    from sqpack.witness import load_witness  # noqa: PLC0415

    witness = load_witness(driver.witness_path(n), fallback_schema=driver.WITNESS_SCHEMA)
    return str(witness.get("id")), driver.source_frame(witness).side


def witness_problems(n: int, row: Mapping[str, Any], batch: Batch) -> list[str]:
    """A grid-slack row against the checkout witness, read again: the retained view was
    derived from it, the side the row records as its own `s_W` is its exact side, and the
    same-side view is at that side. A re-housed or corrected witness fails here rather
    than leaving the record calling the view the witness's packing."""
    identity, side = checkout_witness(n)
    found: list[str] = []
    derived = (read_view(n, batch).get("certificate") or {}).get("derived_from")
    if derived != identity:
        found.append(
            f"n={n}: the view was derived from {derived}, not the checkout's {identity}"
        )
    if side is None or Fraction(row["witness_side"]) != side:
        found.append(f"n={n}: the side the row records is not the checkout witness's own s_W")
    if row["output"] == "same" and Fraction(row["side"]) != Fraction(row["witness_side"]):
        found.append(f"n={n}: the same-side view is not at the witness's side")
    return found


def least_view_problems(n: int, row: Mapping[str, Any]) -> list[str]:
    """Whether the row's view is the least of its count's row-3 views, as far as the row
    shows it: every row-3 side where `select` recorded them, by output in a first-batch row
    (`row_three_sides`, `outputs_at_row_3`) and by run in a grid-slack row (`run_sides`,
    `runs_at_row_3`), else the `same` output's side, which is the witness's own
    (`witness_side`). A row of the first selection whose `solved` view was not taken
    records no side for it."""
    side = Fraction(row["side"])
    recorded, among = (
        (row["run_sides"], row["runs_at_row_3"])
        if "run_sides" in row
        else (row.get("row_three_sides"), row["outputs_at_row_3"])
    )
    if recorded is not None:
        if sorted(recorded) != sorted(among):
            return [f"n={n}: the recorded sides are not the row-3 views'"]
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


def verified_block(row: Mapping[str, Any], batch: Batch = FIRST) -> dict[str, Any]:
    """The verified upper lane on the registered side. Where that side is T-101's, T-101's
    replays prove the same bound, the independent one among them, and stay cited first."""
    own = batch.evidence
    evidence = [*t101_replays(), own] if at_t101_side(row) else [own]
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


def trailing_blocker(
    row: Mapping[str, Any], evidence: Sequence[str], batch: Batch = FIRST
) -> dict[str, Any]:
    """The `mathematics` blocker where the bound and the report disagree."""
    gap = difference(row["value"], row["printed_side"])
    whose = (
        f"the exact side {t101_replays()[0]} and {batch.evidence} both prove"
        if at_t101_side(row)
        else f"{batch.evidence}'s exact side"
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
    batch, row = holder(n)
    payload = load_yaml(front)["packing"]
    front = _set_block(front, "verified_upper_bound", verified_block(row, batch))
    evidence = [item for item in payload["evidence"] if item != batch.evidence]
    front = _set_block(front, "evidence", [batch.evidence, *evidence])
    reported = payload["reported_upper_bound"]
    gap = set(reported.get("evidence") or [])
    replacement = (
        None
        if row["agrees_with_report"]
        else trailing_blocker(row, reported["evidence"], batch)
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


def _without_dated(body: str, marker: str) -> str:
    start = body.find(marker)
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


#: How a batch's dated paragraph names the pass that made its views, by generator kind.
PASS_WORDS = {
    EVAND_KIND: (
        "This project’s regularization pass, Evan Daniel’s exact solver and regularizer run "
        "here on this register’s witness,"
    ),
    GRID_KIND: (
        "This project’s grid-slack regularizer, its port of Evan Daniel’s coincidence "
        "placement, run here on this register’s witness,"
    ),
}


def _implied(n: int, row: Mapping[str, Any]) -> tuple[str, str]:
    """Where the next count's ceiling already proved the bound when the view was selected
    (`implied_by`), what the dated paragraph and the section add to say so; else nothing.
    `s(n) ≤ s(n + 1)`: deleting a square from a packing leaves a packing in the same
    square."""
    implied = row.get("implied_by")
    if not implied:
        return "", ""
    later, results = int(implied["n"]), ", ".join(implied["results"])
    # `select` refuses a view above a larger count's ceiling, and `problems` a row that
    # records one, so the ceiling is at the view's own side (review C4).
    step = (
        f"`s({n}) ≤ s({later})`, since deleting a square from a packing of {later} leaves a "
        f"packing of {n} in the same square"
    )
    dated = (
        f" The bound was not new: the certificate registered at `n = {later}` ({results}), "
        "at the same side, already proved it by monotonicity; this one certifies this "
        "count’s own packing."
    )
    section = (
        f" The bound was not new when it was registered. The exact certificate registered at "
        f"`n = {later}` ({results}) is at the same side, and {step}, so that certificate "
        "already proved the bound. This one is a certificate of this count’s own packing, the "
        "one the record credits."
    )
    return dated, section


def dated_paragraph(n: int, row: Mapping[str, Any], batch: Batch = FIRST) -> str:
    # Where nearest centres do not pair the view with the witness, its identity with the
    # credited packing is undecided, so the view is only made from the witness.
    made = "of this arrangement" if row["identity"]["one_to_one"] else "from that witness"
    proves = f"it proves `s({n}) ≤ {row['side_text']}`"
    if at_t101_side(row):
        bound = (
            f"{proves}, a bound Evan Daniel’s exact certificate of this packing already "
            f"proves at the same side ({DEFAULT_PACKING_RESULT}). The verified upper bound "
            "is now that side exactly, resting on both certificates "
            f"({DEFAULT_PACKING_RESULT}, {batch.result}), and the record still prints it as "
            f"`{row['value']}`.{_implied(n, row)[0]} Until then the verified upper bound was "
            f"{earlier_words(n, row)}."
        )
    else:
        bound = (
            f"{proves}, the verified upper bound ({batch.result})"
            f"{_rounded(row, ' ' + ROUNDED_WORDS)}, which the record still prints as "
            f"`{row['value']}`.{_implied(n, row)[0]} Until then the verified upper bound was "
            f"{earlier_words(n, row)}."
        )
    return (
        f"{batch.dated} {PASS_WORDS[batch.kind]} produced an exact rational packing "
        f"{made}, decided here over `ℚ` by two exact checkers: {bound}\n\n"
    )


def _how_made(row: Mapping[str, Any], batch: Batch = FIRST) -> str:
    if batch.kind == GRID_KIND:
        return "and then fixed the result’s tight contacts over `ℚ` at the witness’s own side"
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


def _identity_words(row: Mapping[str, Any], batch: Batch = FIRST) -> str:
    ident = row["identity"]
    if not ident["one_to_one"]:
        claim = (
            "Evan Daniel’s regularizer reports it as the same packing by its sampled path "
            "test, and "
            if batch.kind == EVAND_KIND
            else ""
        )
        return (
            "Measured against the witness under the box’s eight symmetries, its squares do "
            f"not pair one to one with the witness’s by nearest centres; {claim}whether it "
            "is drawn as this packing waits for the regularized layer’s review."
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


def _straightened_words(row: Mapping[str, Any]) -> str:
    """What a grid-slack view did to the witness's rotations, as a clause."""
    count = len(row.get("straightened") or [])
    degrees = (row["generator"].get("settings") or {}).get("near_axis_degrees")
    if not count:
        return (
            "kept every rotation the witness’s own, since no tilted square lies within "
            f"{degrees:g} degrees of the axes"
        )
    squares = "square" if count == 1 else "squares"
    return (
        f"turned {count} tilted {squares} lying within {degrees:g} degrees of the axes to them"
    )


def _pass_sentence(row: Mapping[str, Any], batch: Batch) -> str:
    """The section's first sentence: which pass made the view, and how."""
    if batch.kind == GRID_KIND:
        return (
            f"This project’s grid-slack regularizer (`devtools.regularize_grid_slack`), its "
            "port of Evan Daniel’s coincidence placement ([`evand/square-packing`]"
            "(https://github.com/evand/square-packing), MIT), ran on this register’s witness "
            f"for this count on {batch.ran}. Starting from the witness’s exact frame, "
            f"it {_straightened_words(row)}, closed what free slack it could while keeping "
            f"every contact the witness has, {_how_made(row, batch)}."
        )
    return (
        f"This project’s regularization pass of {batch.ran} ran Evan Daniel’s "
        "exact solver and regularizer ([`evand/square-packing`]"
        "(https://github.com/evand/square-packing), MIT, vendored here) on this register’s "
        "witness for this count, with the `conservative` angle policy and `coincide` "
        f"placement, {_how_made(row, batch)}."
    )


def section(n: int, row: Mapping[str, Any], batch: Batch = FIRST) -> str:
    """The section on the registered certificate."""
    first = (
        f"{_pass_sentence(row, batch)} The result is an exact rational packing of the same "
        f"{n} squares in a square of side `{row['side_text']}`"
        f"{_rounded(row, ' (' + ROUNDED_WORDS + ')')}, {_side_words(n, row)}. "
        f"{_identity_words(row, batch)} {_drawing_words(row)}"
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
            f"{batch.result}) and {printed}."
        )
    elif rounded_up(Fraction(row["side"])):
        bound = (
            f"{proves}, the verified upper bound ({batch.result}) {ROUNDED_WORDS}. The exact "
            "side, a rational, is the exact form of the case’s `verified_upper_bound`, which "
            f"{printed}."
        )
    else:
        bound = (
            f"{proves}, the verified upper bound ({batch.result}), the exact form of the "
            f"case’s `verified_upper_bound`, which {printed}."
        )
    second = (
        "Each pair and each wall is decided over `ℚ` twice, by `sqpack`’s exact "
        "separating-axis test and by an independent checker that shares no code with it, "
        "and both accept it; both refuse it with its tightest pair pushed into overlap and "
        f"with its box shrunk past its least clearance ([certificate]({batch.link})). The "
        "same two checkers accepted it in the run that made it, so this is a reproduction "
        f"with the producer’s code. {bound}{_implied(n, row)[1]} It says nothing about "
        "optimality, and the packing stays its finders’."
    )
    return f"{SECTION}\n\n{first}\n\n{second}\n\n"


def ceiling_section(n: int, row: Mapping[str, Any], batch: Batch = FIRST) -> str:
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
        f"(`{batch.evidence}`, {batch.result})"
        if at_t101_side(row)
        else (
            f"the exact regularized certificate of this packing (`{batch.evidence}`, "
            f"{batch.result})"
        )
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
            f"\n\nUntil {batch.date_words} that printed decimal was the bound exactly, the "
            "upper endpoint of this project’s interval certificate "
            f"(`{earlier['evidence'][0]}`, {PACKING_RESULT[n]}) at a declared relaxation of "
            "`1e-20`, which on 30 August 2026 had replaced an exact rational replay at "
            "`5.93388579981302587863645209`."
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


#: What each rewrite above leaves behind, so a record already in the past is recognized;
#: the date is the registering batch's.
def _t101_dated_past(batch: Batch) -> re.Pattern[str]:
    return re.compile(
        _words(
            f"the verified upper bound from 6 to {batch.date_words} ({DEFAULT_PACKING_RESULT})"
        )
    )


def _t101_section_past(batch: Batch) -> re.Pattern[str]:
    return re.compile(_words(f"the verified upper bound until {batch.date_words}:"))


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


def past_tense(n: int, body: str, row: Mapping[str, Any], batch: Batch = FIRST) -> str:
    """The earlier ceiling's sentences put in the past. Each sentence the earlier layer
    wrote must be found, in the present tense or already in the past, or the record is
    refused (`_rewrite`)."""
    if n not in PACKING_RESULT:
        body = _rewrite(
            n,
            body,
            _T101_DATED,
            rf"\1, the verified upper bound from 6 to {batch.date_words} "
            f"({DEFAULT_PACKING_RESULT})",
            _t101_dated_past(batch),
        )
        body = _rewrite(
            n,
            body,
            _T101_SECTION,
            rf"\1, the verified upper bound until {batch.date_words}:",
            _t101_section_past(batch),
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
                f"{match.group(1)} verified {match.group(2)} until {batch.date_words}, and its "
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
    batch, row = holder(n)
    body = _without_dated(body, batch.dated)
    title = re.search(r"^# .*\n\n", body, flags=re.MULTILINE)
    if title is None:
        raise RegistrationError(f"n={n}: no title")
    body = (
        body[: title.end()]
        + markdown_math(dated_paragraph(n, row, batch))
        + body[title.end() :]
    )
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
    written = ("" if row["agrees_with_report"] else ceiling_section(n, row, batch)) + section(
        n, row, batch
    )
    body = body[:place] + markdown_math(written) + body[place:]
    return past_tense(n, body, row, batch)


def apply_case(n: int, text: str) -> str:
    """One case record with its verified upper lane on the registered view of the batch
    that holds it; others unchanged."""
    if batch_of(n) is None:
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


def table(batch: Batch = FIRST) -> str:
    """One row per registered count, from a batch's committed selection."""
    header = (
        "| n | View | Exact side | Printed as | Below the earlier bound by "
        "| Below T-101’s side by | Agrees | Drawing | Moved, largest |"
    )
    lines = [header, "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for n, row in sorted(committed(batch).items()):
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
    parser.add_argument(
        "--batch",
        choices=tuple(BATCH_NAMES),
        default=FIRST_NAME,
        help="the batch a command acts on (default: the first, T-155)",
    )
    parser.add_argument(
        "--n",
        type=int,
        nargs="+",
        default=[],
        help="the counts a grid-slack batch's select takes (select --batch grid-slack only)",
    )
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args(argv)
    batch = BATCH_NAMES[args.batch]
    if args.command != "select" and (args.run_dir or args.n):
        parser.error("--run-dir and --n are select's alone")
    if args.command == "select":
        if not args.run_dir:
            parser.error("select needs --run-dir")
        run_dirs = [path.resolve() for path in args.run_dir]
        if batch.kind == EVAND_KIND:
            if args.n:
                parser.error(
                    f"select --batch {batch.name} takes every row-3 count of its runs and no "
                    "--n; --n names the counts of a grid-slack batch (--batch grid-slack)"
                )
            receipt, views = select(run_dirs, batch)
        elif not args.n:
            parser.error(f"select --batch {batch.name} needs --n")
        else:
            receipt, views = select_grid(run_dirs, args.n, batch)
        retain(batch, views)
        write_json(batch.selection, receipt)
        print(f"{len(receipt['registered'])} counts selected: {receipt['registered']}")
        return 0
    if args.command == "table":
        print(table(batch), end="")
        return 0
    if args.command == "decide":
        receipt = decide_all(batch)
        write_json(batch.decision, receipt)
        print(f"{receipt['decided']} views decided; all passed: {receipt['all_passed']}")
        return 0 if receipt["all_passed"] else 1
    if args.command == "controls":
        receipt = run_controls(batch)
        write_json(batch.controls, receipt)
        print(f"{receipt['controls']} controls; all as expected: {receipt['all_as_expected']}")
        return 0 if receipt["all_as_expected"] else 1
    drift: list[Path] = []
    every = sorted(n for each in BATCHES for n in counts(each))
    for n in every:
        path = FRONTIER / f"n-{n:03d}.md"
        text = path.read_text(encoding="utf-8")
        rendered = render_case_verifiers.refresh(apply_case(n, text))
        if _normalized(rendered) != _normalized(text):
            drift.append(path)
            if not args.check:
                with atomic_output_file(path) as temporary:
                    temporary.write_text(rendered, encoding="utf-8")
    found = [problem for each in BATCHES for problem in problems(each)] if args.check else []
    for problem in found:
        print(f"FAIL {problem}", file=sys.stderr)
    for path in drift:
        print(("drift: " if args.check else "wrote: ") + str(path.relative_to(ROOT)))
    if not drift and not found:
        print(f"the {len(every)} records and the receipts are current")
    return 1 if found or (args.check and drift) else 0


if __name__ == "__main__":
    sys.exit(main())
