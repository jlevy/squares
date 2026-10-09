#!/usr/bin/env python3
# ruff: noqa: RUF001 -- this module writes register prose, whose typography uses curly
# apostrophes and the corpus's other non-ASCII marks.
"""Carry Evan Daniel's exact certificates to the verified upper lanes they lower.

``evand/square-packing`` at ``13ee36e`` (5 October 2026) certifies the register's known-best
packing exactly at 321 counts. At 48 the certified side ``S'`` lies below the printed side;
those are T-098, which ``devtools.apply_exact_optima`` writes. At the others ``S'`` lies
1e-20 to 1e-14 above the printed side, and the source offers them as a replay of the
existing bounds, asking for nothing to be registered. The owner decided on 6 October 2026
to act on them where they lower a verified ceiling (think-70bh).

**Which counts.** A certificate of a printed side carries the verified upper lane at the
larger of the printed side and its own side rounded up at the printed precision, with that
decimal's fraction as the exact form (`devtools.upper_bound_packets.verified_value`, the
rule T-056, T-088 and T-089 follow). ``survey`` computes that value at every count the
receipts decide, apart from the 48 and the held ``n = 17``, and selects the counts where it
lies strictly below the verified upper bound the record held before this import: 77 of
them, the integer grid at 74 and the exact certificates of the catalogue's pictures at
``n = 69, 83, 87`` (T-088, T-089). It writes ``receipts/ceiling-survey.json``, which also
lists the one count whose ceiling trailed its report and does not move, ``n = 29``, where
the interval-certified bound ``E-n029-interval-certified-upper`` already lies below ``S'``.
It refuses a certificate whose side is not above the catalogue's closed form, which would
be a smaller packing than the catalogue's and no ceiling.

**What it writes**, registered as T-101. At each of the 77 counts the
verified upper lane becomes that value, citing the exact replay here and the source's
checkers run here; the earlier upper-gap blocker goes, and where the report has a closed
form, which the certificate's side lies just above, a blocker saying by how much the ceiling
still trails it takes its place: no rational certificate reaches an irrational form, and
the six rational ones would be reached by an exact certificate at that side. The body gains a
dated paragraph and a section on the certificate where the ceiling section stood, and keeps
a rewritten ceiling section where it still trails. At ``n = 69, 83, 87`` the earlier
certificate's sentences go into the past. The reported lane is unchanged: the packing, its
side and its credit are the catalogue's.

It is a layer over the tools that wrote these records, as ``devtools.apply_exact_optima``
is: ``devtools.generate_frontier_case`` applies it last to its drafts, so that its
``--check`` still reads the record as written. Applied to its own output it changes nothing.

Usage, from ``packing/``:
    uv run --frozen --all-extras --group dev python -m devtools.apply_exact_ceilings survey
    uv run --frozen --all-extras --group dev python -m devtools.apply_exact_ceilings
    uv run --frozen --all-extras --group dev python -m devtools.apply_exact_ceilings --check

The count ``n = 17`` is held by the owner (think-x4v4): nothing here reads its certificate.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections.abc import Mapping, Sequence
from decimal import Decimal, localcontext
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import evand_exact_certificates as certificates
from devtools.apply_exact_optima import AI_SENTENCE
from devtools.migrate_math import markdown_math
from devtools.retained_data import read_retained_text
from devtools.upper_bound_packets import places, verified_value
from sqpack.assurance import bounds_agree_at_declared_precision
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"

RESULT = "T-101"
INTAKE = "2026-10-06"
AUTHOR = "Evan Daniel"
SOURCE_KEY = "[evand exact optima 2026-10-05]"
REPORT = "E-evand-exact-ceilings-2026-10-05-report"
EXACT_REPLAY = "E-evand-exact-ceilings-2026-10-05-exact-replay"
SOURCE_REPLAY = "E-evand-exact-ceilings-2026-10-05-source-replay"
EVIDENCE = (REPORT, EXACT_REPLAY, SOURCE_REPLAY)
GRID = "E-basic-grid-upper"
PACKET_LINK = "../resources/web/evand-square-packing-2026-10-05/README.md"
RESOURCE = {
    "key": SOURCE_KEY,
    "role": "formal-certificate",
    "local": "web/evand-square-packing-2026-10-05",
    "url": "https://github.com/evand/square-packing",
    "retrieved": True,
}
SURVEY_RECEIPT = certificates.RECEIPTS / "ceiling-survey.json"
COVERAGE = FRONTIER / "source-coverage.yaml"
COVERAGE_ID = "evand-square-packing-2026-10-05"
#: The catalogue baseline, whose printed side stays each count's report.
BASELINE = "kingbird-current"
CEILING_HEADING = "## The verified upper bound is a ceiling"
SECTION = "## The exact certificate"
DATED = "**Exact certificate, 2026-10-06.**"
#: The source's report of a certificate solved from the register's witness as it stands.
WITNESS_INPUT = "register witness"
#: Digits enough to order a rational candidate against an irrational ceiling.
DIGITS = 60
_PLACES = {14: "fourteen", 15: "fifteen", 16: "sixteen", 20: "twenty"}


# --------------------------------------------------------------------------------------
# The survey
# --------------------------------------------------------------------------------------


def _catalogue_certificates() -> Any:
    from devtools import catalogue_upper_bounds  # noqa: PLC0415 -- heavy import

    return catalogue_upper_bounds


def earlier_ceiling(n: int) -> dict[str, Any]:
    """The verified upper bound count ``n`` held before this import, from its sources.

    At the catalogue's ``n = 69, 83, 87`` it is their exact certificates' rounded-up side
    (T-088, T-089), from that tool's committed receipt; at every other count this import
    moves it is the integer grid, ``ceil(sqrt(n))``. Read from the sources rather than
    the case records, which this import changes.
    """
    catalogue = _catalogue_certificates()
    if n in catalogue.RESULTS:
        row = catalogue.certification()[n]
        return {
            "value": str(row["verified_value"]),
            "exact_form": str(row["exact_form"]),
            "evidence": [catalogue.REPLAY_EVIDENCE[n]],
        }
    side = str(math.isqrt(n - 1) + 1)
    return {"value": side, "exact_form": side, "evidence": [GRID]}


def bound_value(bound: Mapping[str, Any]) -> Fraction:
    """A verified bound as a rational: its exact form where that is one, a closed form
    evaluated to `DIGITS` digits, or else its decimal."""
    from sqpack.kingbird_catalogue import evaluate_exact_form  # noqa: PLC0415

    exact = bound.get("exact_form")
    try:
        return Fraction(str(exact))
    except ValueError:
        pass
    try:
        return Fraction(evaluate_exact_form(str(exact), DIGITS))
    except Exception:  # noqa: BLE001 -- any form the evaluator cannot read falls back
        return Fraction(Decimal(str(bound["value"])))


def _scientific(value: float) -> str:
    return f"{value:.1e}".replace("e-0", "e-")


def _closed_form_gap(exact_form: str | None, side: Fraction) -> float | None:
    """How far a certificate's side lies above a closed-form side, or `None` without one."""
    if not exact_form:
        return None
    from sqpack.kingbird_catalogue import evaluate_exact_form  # noqa: PLC0415

    with localcontext() as context:
        context.prec = DIGITS + 10
        exact = evaluate_exact_form(exact_form, DIGITS)
        above = Decimal(side.numerator) / Decimal(side.denominator) - exact
    return float(f"{float(above):.4e}")


def closed_form_degree(exact_form: str | None) -> int | None:
    """The degree over Q of a closed-form side, from SymPy's exact minimal polynomial, or
    `None` without one: 1 is a rational side, which a contact-exact rational certificate
    can reach, and above 1 an irrational one, which no rational certificate reaches."""
    if not exact_form:
        return None
    import sympy as sp  # noqa: PLC0415 - optional dependency, imported where it is used
    from sympy.parsing.sympy_parser import (  # noqa: PLC0415
        implicit_multiplication_application,
        parse_expr,
        standard_transformations,
    )

    transformations = (*standard_transformations, implicit_multiplication_application)
    value = parse_expr(exact_form, transformations=transformations)
    variable = sp.Symbol("x")
    return int(sp.minimal_polynomial(value, variable, polys=True).degree())


def survey_row(
    n: int,
    case: Mapping[str, Any],
    *,
    earlier: Mapping[str, Any],
    first: Mapping[str, Any],
    pose: Mapping[str, Any],
    report: Mapping[str, Any],
) -> dict[str, Any]:
    """One moved count: the bounds before and after, the certificate's side, and what the
    source's own report says the certificate was solved from and is."""
    reported = case["reported_upper_bound"]
    side = Fraction(first["side"])
    value = verified_value(str(reported["value"]), side)
    after = {"value": value, "exact_form": certificates.literal(Fraction(value))}
    return {
        "n": n,
        "printed_side": str(reported["value"]),
        "printed_exact_form": reported.get("exact_form"),
        "finders": list(reported.get("found_by") or []),
        "earlier_verified": dict(earlier),
        "certified_side": first["side"],
        "certified_side_decimal": certificates.terminating_decimal(side),
        "certified_above_printed_side_by": float(
            f"{float(side - Fraction(Decimal(str(reported['value'])))):.4e}"
        ),
        "certified_above_exact_side_by": _closed_form_gap(reported.get("exact_form"), side),
        "printed_exact_form_degree": closed_form_degree(reported.get("exact_form")),
        "verified_value": value,
        "exact_form": after["exact_form"],
        "agrees_with_report": bounds_agree_at_declared_precision(reported, after),
        "least_wall_clearance": first["exact_verify"]["minimum_containment_clearance"],
        "source_input": str(report.get("input")),
        "source_status": str(report.get("status")),
        "pose": dict(pose),
    }


def _first_party() -> dict[int, dict[str, Any]]:
    receipt = json.loads(read_retained_text(certificates.FIRST_PARTY_RECEIPT))
    return {int(row["n"]): row for row in receipt["rows"]}


def survey(directory: Path = certificates.CERTS) -> dict[str, Any]:
    """Every count the receipts decide, against the verified ceiling it held before.

    A count moves where its certificate's verified value lies strictly below that ceiling.
    Its pose is matched to the register's known-best witness from the certificate in
    ``directory``.
    """
    first = _first_party()
    free = certificates.reported_free()
    reports = {
        int(row["n"]): row for row in json.loads(read_retained_text(certificates.RESULTS_JSON))
    }
    rows: list[dict[str, Any]] = []
    unmoved: list[dict[str, Any]] = []
    considered = 0
    for n in sorted(first):
        if n in certificates.HELD or n in certificates.IMPROVING:
            continue
        considered += 1
        case = certificates.case_record(n)
        reported = case["reported_upper_bound"]
        current = case["verified_upper_bound"]
        applied = EXACT_REPLAY in (current.get("evidence") or [])
        earlier = earlier_ceiling(n) if applied else dict(current)
        side = Fraction(first[n]["side"])
        candidate = verified_value(str(reported["value"]), side)
        if Fraction(Decimal(candidate)) < bound_value(earlier):
            if not applied and earlier != earlier_ceiling(n):
                raise ValueError(f"n={n}: the record's ceiling is not the one its sources give")
            certificate = certificates.parse(
                certificates.certificate_path(directory, n).read_text(encoding="utf-8"),
                expected_n=n,
            )
            if not certificates.is_decided(certificates.certificate_path(directory, n), n):
                raise ValueError(f"n={n}: the certificate read is not the one decided")
            gap = _closed_form_gap(reported.get("exact_form"), side)
            if gap is not None and gap <= 0:
                raise ValueError(
                    f"n={n}: the certificate's side is not above the catalogue's closed form, "
                    "which would be a smaller packing than the catalogue's, not a ceiling"
                )
            pose = certificates.pose_match(certificate, free.get(n))
            rows.append(
                survey_row(
                    n, case, earlier=earlier, first=first[n], pose=pose, report=reports[n]
                )
            )
        elif not bounds_agree_at_declared_precision(reported, earlier):
            unmoved.append(
                {
                    "n": n,
                    "printed_side": str(reported["value"]),
                    "verified": dict(earlier),
                    "candidate_verified_value": candidate,
                    "certified_side": first[n]["side"],
                    "certified_above_verified_by": float(
                        f"{float(side - bound_value(earlier)):.4e}"
                    ),
                }
            )
    poses = [row["pose"] for row in rows]
    return {
        "format": certificates.FORMAT,
        "tool": "python -m devtools.apply_exact_ceilings survey",
        "what": (
            "At every count the replay receipts decide, apart from the 48 that improve the "
            "printed side (T-098) and the held n = 17: the verified value a certificate of a "
            "printed side carries, the larger of the printed side and the certified side "
            "rounded up at the printed precision, against the verified upper bound the "
            "record held before this import. Each count where it lies strictly below that "
            "ceiling is a row, with its certificate's pose matched to the register's "
            "known-best witness; a count whose ceiling trailed its report and does not move "
            "is listed as unmoved."
        ),
        "considered": considered,
        "moved": [row["n"] for row in rows],
        "agreeing_after": [row["n"] for row in rows if row["agrees_with_report"]],
        "trailing_after": [row["n"] for row in rows if not row["agrees_with_report"]],
        "all_matched_one_to_one": all(pose["matched_one_to_one"] for pose in poses),
        "largest_centre_displacement": max(
            pose["largest_centre_displacement"] for pose in poses
        ),
        "nonfree_moved_largest_centre_displacement": max(
            pose["nonfree_moved_largest_centre_displacement"] for pose in poses
        ),
        "unmoved_largest_centre_displacement": max(
            pose["unmoved_largest_centre_displacement"] for pose in poses
        ),
        "unmoved": unmoved,
        "rows": rows,
    }


@cache
def committed() -> dict[int, dict[str, Any]]:
    """The committed survey's rows, by count."""
    receipt = json.loads(read_retained_text(SURVEY_RECEIPT))
    return {int(row["n"]): row for row in receipt["rows"]}


# --------------------------------------------------------------------------------------
# Front matter
# --------------------------------------------------------------------------------------


def _set_block(front: str, name: str, value: object) -> str:
    from devtools.apply_upper_bound_packets import set_block  # noqa: PLC0415

    return set_block(front, name, value)


def _difference(larger: str, smaller: str) -> str:
    from devtools.apply_upper_bound_packets import difference  # noqa: PLC0415

    return difference(larger, smaller)


def verified_block(row: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "value": row["verified_value"],
        "exact_form": row["exact_form"],
        "evidence": [EXACT_REPLAY, SOURCE_REPLAY],
    }


def trailing_blocker(row: Mapping[str, Any], evidence: Sequence[str]) -> dict[str, Any]:
    """The ``mathematics`` blocker of a count whose report is a closed form: irrational,
    which no rational certificate reaches, or rational, which an exact certificate at that
    side would reach (the review's EC-1 and its fix check's FC-1)."""
    rational = row["printed_exact_form_degree"] == 1
    form = (
        "a rational side, which this certificate, rounded outward, does not reach"
        if rational
        else "an irrational side, which no rational certificate reaches"
    )
    remedy = (
        "an exact certificate of the packing at that side, rational where its exact point "
        "is rational"
        if rational
        else "an exact algebraic certificate of the packing at its closed-form side"
    )
    return {
        "kind": "mathematics",
        "detail": (
            f"verified_upper_bound is {EXACT_REPLAY}'s certified side rounded up, "
            f"{row['verified_value']}, which trails the report {row['printed_side']} by "
            f"{_difference(row['verified_value'], row['printed_side'])}, and the report's "
            f"exact form {row['printed_exact_form']}, {form}: the certificate's own side "
            f"lies {_scientific(row['certified_above_exact_side_by'])} above it. Closing "
            f"the gap needs {remedy}."
        ),
        "evidence": list(evidence),
    }


def front_matter(n: int, front: str) -> str:
    """The front matter with the verified upper lane on the certificate."""
    row = committed()[n]
    payload = safe_load(front)["packing"]
    reviewed = max(str(payload.get("source_reviewed") or ""), INTAKE)
    front = re.sub(
        r"^  source_reviewed: .*$",
        f"  source_reviewed: '{reviewed}'",
        front,
        count=1,
        flags=re.MULTILINE,
    )
    front = _set_block(front, "verified_upper_bound", verified_block(row))
    evidence = list(payload["evidence"])
    front = _set_block(
        front, "evidence", [item for item in EVIDENCE if item not in evidence] + evidence
    )
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
        blockers.append(replacement)
    front = _set_block(front, "blockers", blockers)
    kept = [RESOURCE if item["key"] == SOURCE_KEY else item for item in payload["resources"]]
    if all(item["key"] != SOURCE_KEY for item in kept):
        kept.insert(0, RESOURCE)
    return _set_block(front, "resources", kept)


# --------------------------------------------------------------------------------------
# Body
# --------------------------------------------------------------------------------------


def _section_span(body: str, heading: str) -> tuple[int, int] | None:
    start = body.find(f"{heading}\n")
    if start < 0:
        return None
    end = body.find("\n## ", start + len(heading))
    return start, (len(body) if end < 0 else end + 1)


def _places_word(printed: str) -> str:
    digits = places(printed)
    return _PLACES.get(digits, str(digits))


def _shown(row: Mapping[str, Any]) -> str:
    from devtools.generate_frontier_case import display_first_party_upper  # noqa: PLC0415

    return display_first_party_upper(str(row["certified_side_decimal"]))


def earlier_words(n: int, row: Mapping[str, Any]) -> str:
    """The verified upper bound before this import, as the dated paragraph names it."""
    earlier = row["earlier_verified"]
    if earlier["evidence"] == [GRID]:
        side = earlier["value"]
        return f"the trivial grid bound `{side}`"
    result = "T-088" if n == 69 else "T-089"
    return (
        f"`{earlier['value']}`, the rounded-up side of an exact certificate of a binary64 "
        f"parse of the catalogue’s picture ({result})"
    )


def dated_paragraph(n: int, row: Mapping[str, Any]) -> str:
    return (
        f"{DATED} {AUTHOR}’s [`square-packing`]({PACKET_LINK}) published on 5 October 2026 "
        "an exact rational certificate of this packing, decided here over `ℚ` by two exact "
        "checkers that share no code with each other or with the source, and by the "
        f"source’s own two run here: it proves `s({n}) ≤ {row['verified_value']}`, the "
        f"verified upper bound ({RESULT}). Until then the verified upper bound was "
        f"{earlier_words(n, row)}.\n\n"
    )


def _bound(value: float) -> str:
    """An upper bound in two significant digits, rounded up so that it stays one."""
    return _scientific(certificates.round_up(float(value), 2))


def motion(pose: Mapping[str, Any]) -> str:
    """How far the certificate's squares lie from the witness the atlas pictures."""
    largest = float(pose["largest_centre_displacement"])
    text = (
        f"Square for square, its pose lies within `{_bound(largest)}` of the binary64 pose "
        "the atlas pictures for this count."
        if largest > 0
        else "Rounded to binary64, square for square, its pose is the one the atlas "
        "pictures for this count."
    )
    count, free = int(pose["moved_count"]), int(pose["moved_listed_free"])
    if not count:
        return text
    others = count - free
    nonfree = _bound(pose["nonfree_moved_largest_centre_displacement"])
    if not others:
        parts = (
            "one the source lists as carrying no force"
            if count == 1
            else "all of them squares the source lists as carrying no force"
        )
    elif not free:
        parts = (
            f"one the source does not list as free, by at most `{nonfree}`"
            if count == 1
            else f"none of them listed by the source as free, each by at most `{nonfree}`"
        )
    else:
        parts = (
            f"{free} of them squares the source lists as carrying no force and the "
            f"other {others} by at most `{nonfree}`"
        )
    still = float(pose["unmoved_largest_centre_displacement"])
    rest = (
        f"every other square moves by at most `{_bound(still)}`"
        if still > 0
        else "every other square’s centre rounds to the witness’s"
    )
    return text + (
        f" {count} {'square moves' if count == 1 else 'squares move'} by more than "
        f"`1e-8`, {parts}; {rest}."
    )


def section(n: int, row: Mapping[str, Any]) -> str:
    """The section on the certificate, where the ceiling section stood."""
    printed = row["printed_side"]
    above = _scientific(row["certified_above_printed_side_by"])
    first = (
        f"{AUTHOR}’s [`square-packing`]({PACKET_LINK}) published on 5 October 2026 exact "
        "rational certificates of the packings this register lists as best known, solved "
        "from its own witnesses, and offered those that do not lower a printed side as a "
        "replay of the existing bounds, asking for nothing to be registered from them. The "
        f"certificate for this count holds the same {n} squares, each a rational centre and a "
        "rational "
        f"`t = tan(θ/2)`, in a square of side `{_shown(row)}`, `{above}` above the side "
        f"the Kingbird catalogue prints, `{printed}`. {motion(row['pose'])} "
        f"{AUTHOR}’s solver moves the binary64 pose to a nearby exact KKT point of the "
        "problem of minimizing the side under non-overlap, computed at 80 digits, and "
        "rounds it outward to rationals."
        + (
            ""
            if row["source_input"] == WITNESS_INPUT
            else " At this count it started from the witness after the source’s own local "
            "squeeze, which it has not published; that bears on reproducing the solve and "
            "not on checking the certificate."
        )
    )
    second = (
        "This repository decides the certificate exactly. Converted without rounding, "
        "every pair and every wall is decided over `ℚ` twice, by `sqpack`’s exact "
        "separating-axis test and by an independent checker that shares no code with it, "
        "and the source’s own two checkers, run here as retained, accept it as well "
        f"([receipts]({PACKET_LINK}#replayed-here)). That proves "
        f"`s({n}) ≤ {row['verified_value']}`, the verified upper bound: the certificate’s "
        f"side rounded up at the {_places_word(printed)} decimals the catalogue prints, as "
        "the record writes any certificate of a printed side. It says nothing about "
        f"optimality. {AI_SENTENCE}"
    )
    if row["agrees_with_report"]:
        third = (
            "\n\nThe verified upper bound and the printed side now agree to one unit of the "
            "printed side’s last place, the precision at which the record compares them. "
            "The printed side itself is not certified here: the certificate’s side lies "
            "above it."
        )
    else:
        third = ""
    return f"{SECTION}\n\n{first}\n\n{second}{third}\n\n"


def ceiling_section(n: int, row: Mapping[str, Any]) -> str:
    """The ceiling section of a count whose report is a closed form."""
    printed, value = row["printed_side"], row["verified_value"]
    first = (
        f"`verified_upper_bound` for this case is `{value}`, proved by {AUTHOR}’s exact "
        f"rational certificate of this packing (`{EXACT_REPLAY}`, {RESULT}). It is "
        f"**larger** than the best known `{printed}` two fields above it, by "
        f"`{_difference(value, printed)}`."
    )
    second = (
        f"It is not the value of `s({n})` and not a different packing: it is the "
        f"certificate’s own side, `{_shown(row)}`, rounded up at the "
        f"{_places_word(printed)} decimals the catalogue prints. The catalogue gives the "
        f"packing’s side exactly, as `{row['printed_exact_form']}`, and the certificate’s "
        f"side lies `{_scientific(row['certified_above_exact_side_by'])}` above that: its "
        "squares are rational and each is kept clear of its neighbours and the walls, so "
        "it bounds the exact side from above and does not reach it. "
        + (
            "That side is rational, so an exact certificate of the packing at that side "
            "would reach it, a rational one where the packing’s exact point is rational. "
            if row["printed_exact_form_degree"] == 1
            else "That side is irrational, so no rational certificate reaches it. "
        )
        + "The `mathematics` blocker in the frontmatter records the difference. Read "
        "`reported_upper_bound` for the best known side length."
    )
    return f"{CEILING_HEADING}\n\n{first}\n\n{second}\n\n"


#: The earlier certificate's sentences at n = 69, 83 and 87 name it the verified upper
#: bound; after this import that is history. Math form and code form.
_BOUND = r"(?:\$s\(\d+\)\s+\\le\s+[^$]+\$|`s\(\d+\)\s+≤\s+[^`]+`)"
_EARLIER_DATED = re.compile(rf"(proves\s+{_BOUND}),\s+the\s+verified\s+upper\s+bound,\s+")
_EARLIER_VERIFIED = re.compile(
    rf"(That\s+proves\s+{_BOUND}),\s+the\s+verified\s+upper\s+bound;"
)
_EARLIER_REMEDY = re.compile(
    r"The\s+printed\s+side\s+is\s+not\s+certified:\s+that\s+needs\s+the\s+SVG’s\s+own\s+"
    r"pose,\s+or\s+this\s+one\s+refined\s+on\s+its\s+active\s+contacts\."
)


def past_tense(body: str) -> str:
    """The catalogue certificate's sentences put in the past, at n = 69, 83 and 87."""
    body = _EARLIER_DATED.sub(r"\1, the verified upper bound until 6 October 2026, ", body)
    body = _EARLIER_VERIFIED.sub(
        rf"\1, which was the verified upper bound until {AUTHOR}’s exact certificate "
        "replaced it;",
        body,
    )
    return _EARLIER_REMEDY.sub(
        f"The printed side is not certified: {AUTHOR}’s exact certificate of the same "
        f"packing ({RESULT}) lies above it as well.",
        body,
    )


def _without_dated(body: str) -> str:
    start = body.find(DATED)
    if start < 0:
        return body
    end = body.find("\n\n", start)
    return body[:start] + body[end + 2 :]


def body_text(n: int, body: str) -> str:
    row = committed()[n]
    body = _without_dated(body)
    title = re.search(r"^# .*\n\n", body, flags=re.MULTILINE)
    if title is None:
        raise ValueError(f"n={n}: no title")
    body = body[: title.end()] + markdown_math(dated_paragraph(n, row)) + body[title.end() :]
    place = None
    for heading in (CEILING_HEADING, SECTION):
        span = _section_span(body, heading)
        if span is not None:
            place = span[0] if place is None else min(place, span[0])
            body = body[: span[0]] + body[span[1] :]
    if place is None:
        raise ValueError(f"n={n}: neither a ceiling section nor a certificate section")
    written = ("" if row["agrees_with_report"] else ceiling_section(n, row)) + section(n, row)
    body = body[:place] + markdown_math(written) + body[place:]
    if n in _catalogue_certificates().RESULTS:
        body = past_tense(body)
    return body


def apply_case(n: int, text: str) -> str:
    """One case record with its verified upper lane on the certificate; others unchanged."""
    if n not in certificates.CEILINGS:
        return text
    from devtools.source_supersession import preserve_selected_case  # noqa: PLC0415

    if preserve_selected_case(n, text, {COVERAGE_ID}):
        return text
    _, front, body = text.split("---\n", 2)
    return f"---\n{front_matter(n, front)}---\n{body_text(n, body)}"


# --------------------------------------------------------------------------------------
# Source coverage
# --------------------------------------------------------------------------------------


def coverage_text(text: str) -> str:
    """The coverage record with the source's claim at each count listed as superseded.

    Each certificate claims a side above the one the catalogue prints, so the
    catalogue's report stays selected and the certificate's side is a superseded
    report; the case record carries it, rounded up, as the verified upper bound.
    """
    from devtools.apply_exact_optima import coverage_entries  # noqa: PLC0415

    coverage = safe_load(text)
    from devtools.source_supersession import (  # noqa: PLC0415
        preserve_other_coverage,
        replace_coverage_list,
        superseded_counts,
    )

    counts = set(certificates.CEILINGS) - superseded_counts(coverage, {COVERAGE_ID})
    superseded = [
        entry
        for entry in coverage.get("superseded_reports") or []
        if not (entry["n"] in counts and entry["source_id"] == COVERAGE_ID)
    ]
    for n in sorted(counts):
        row = committed()[n]
        above = _scientific(row["certified_above_printed_side_by"])
        superseded.append(
            {
                "n": n,
                "source_id": COVERAGE_ID,
                "value": row["certified_side_decimal"],
                "superseded_by": BASELINE,
                "reason": (
                    f"Certifies the catalogue's packing at a side {above} above the one it "
                    "prints, which stays the report; since "
                    f"{INTAKE} it is the verified upper bound, rounded up at the printed "
                    f"precision ({RESULT})."
                ),
            }
        )
    superseded.sort(key=lambda entry: (entry["n"], entry["source_id"]))
    rendered = replace_coverage_list(
        text, "superseded_reports", coverage_entries("superseded_reports", superseded)
    )
    return preserve_other_coverage(text, rendered, counts)


# --------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------


def _normalized(text: str) -> str:
    from devtools.apply_upper_bound_packets import normalized  # noqa: PLC0415

    return normalized(text)


def survey_problems() -> list[str]:
    """The committed survey against the packet, the list it derives and the live records.

    Its moved counts must be `certificates.CEILINGS`; each row's side and digest must be
    its retained certificate's and the first-party receipt's, and its verified value the
    rule's; and at every other count the receipts decide, the rule must not lower the
    record's verified ceiling now.
    """
    problems: list[str] = []
    receipt = json.loads(read_retained_text(SURVEY_RECEIPT))
    if tuple(receipt["moved"]) != certificates.CEILINGS:
        problems.append("survey: the moved counts are not certificates.CEILINGS")
    first = _first_party()
    for n, row in committed().items():
        path = certificates.certificate_path(certificates.CERTS, n)
        if not path.is_file():
            problems.append(f"survey n={n}: the certificate is not retained")
            continue
        side = certificates.parse(path.read_text(encoding="utf-8"), expected_n=n).side
        if certificates.literal(side) != row["certified_side"] or (
            row["certified_side"] != first[n]["side"]
        ):
            problems.append(f"survey n={n}: the side is not the certificate's")
        if not certificates.is_decided(path, n):
            problems.append(f"survey n={n}: the retained certificate is not the one decided")
        if verified_value(row["printed_side"], side) != row["verified_value"]:
            problems.append(f"survey n={n}: the verified value is not the rule's")
    for n in sorted(first):
        if n in certificates.HELD or n in certificates.IMPROVING or n in committed():
            continue
        case = certificates.case_record(n)
        candidate = verified_value(
            str(case["reported_upper_bound"]["value"]), Fraction(first[n]["side"])
        )
        if Fraction(Decimal(candidate)) < bound_value(case["verified_upper_bound"]):
            problems.append(f"n={n}: the certificate would lower the ceiling and is not listed")
    return problems


def table() -> str:
    """The packet README's table of the 77 counts, from the committed survey."""
    header = (
        "| n | Printed side | Closed form | Earlier ceiling | Certified side `S'` "
        "| Above printed by | Verified upper bound | Agrees |"
    )
    lines = [header, "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for n, row in sorted(committed().items()):
        earlier = row["earlier_verified"]
        held = "grid" if earlier["evidence"] == [GRID] else ("T-088" if n == 69 else "T-089")
        form = row["printed_exact_form"]
        lines.append(
            f"| {n} | `{row['printed_side']}` | {f'`{form}`' if form else '—'} "
            f"| `{earlier['value']}` ({held}) | `{_shown(row)}` "
            f"| `{row['certified_above_printed_side_by']:.2e}` | `{row['verified_value']}` "
            f"| {'yes' if row['agrees_with_report'] else 'no'} |"
        )
    return "\n".join(lines) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    from devtools import render_case_verifiers  # noqa: PLC0415

    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("command", nargs="?", choices=("survey", "table"))
    parser.add_argument("--certs", type=Path, default=certificates.CERTS)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args(argv)
    if args.command == "survey":
        receipt = survey(args.certs)
        certificates.write_receipt(SURVEY_RECEIPT, receipt)
        print(
            f"{receipt['considered']} counts considered; {len(receipt['moved'])} move, "
            f"{len(receipt['agreeing_after'])} of them to agree with the report; unmoved "
            f"trailing: {[row['n'] for row in receipt['unmoved']]}"
        )
        return 0
    if args.command == "table":
        print(table(), end="")
        return 0
    problems = survey_problems()
    drift: list[Path] = []
    for n in certificates.CEILINGS:
        path = FRONTIER / f"n-{n:03d}.md"
        text = path.read_text(encoding="utf-8")
        rendered = render_case_verifiers.refresh(apply_case(n, text))
        if _normalized(rendered) != _normalized(text):
            drift.append(path)
            if not args.check:
                atomic_write_text(path, rendered)
    text = COVERAGE.read_text(encoding="utf-8")
    updated = coverage_text(text)
    if updated != text:
        drift.append(COVERAGE)
        if not args.check:
            atomic_write_text(COVERAGE, updated)
    for problem in problems:
        print(f"FAIL {problem}", file=sys.stderr)
    for path in drift:
        print(("drift: " if args.check else "wrote: ") + str(path.relative_to(ROOT)))
    if not drift and not problems:
        print(
            f"the {len(certificates.CEILINGS)} records, the coverage record and the survey "
            "are current"
        )
    return 1 if problems or (args.check and drift) else 0


if __name__ == "__main__":
    sys.exit(main())
