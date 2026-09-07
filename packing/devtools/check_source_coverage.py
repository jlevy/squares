#!/usr/bin/env python3
"""Reparse retained first-party result sources and reconcile the frontier.

This check deliberately uses stable local snapshots. Refreshing a source is a dated
research action; ordinary tests must not depend on network state.

Two reconciliations run here, against the same retained catalogue.

The first reads the *values*: what side length the source reports for each `n`, checked
against `reported_upper_bound.value` and the selected-source register.

The second reads the *exact forms*: the closed form, degree lock and minimal polynomial
the catalogue prints beside each value, checked against the record's `exact_form`,
`algebraic_degree`, `minimal_polynomial` and `catalogue_rigid`. That half exists because
for a long time it did not. The value reconciliation parsed only the printed decimal, so
a missed radical was invisible, and one was missed: `n = 54`, whose closed form the
catalogue renders in a multi-line block, was recorded as having none, and the miss
reached a published figure (`think-k5z2`). Nothing here compares strings -- forms are
evaluated to `EXACT_FORM_DIGITS` digits and polynomials are compared as polynomials --
because a transcription can be right and spelled differently, and wrong while spelled
almost the same.

Only a catalogue fact the record lacks or contradicts is a divergence. Where the record
holds *more* than the source -- a degree this repository derived, or the rational minimal
polynomial of a root the catalogue prints over a quadratic field -- that is not drift.
"""

from __future__ import annotations

import json
import math
import pathlib
import re
import shlex
import sys
from collections.abc import Mapping
from decimal import Decimal

from sqpack.kingbird_catalogue import (
    NOT_STATED,
    RIGIDITY_STATES,
    CatalogueEntry,
    CatalogueParseError,
    agrees_with_printed_decimal,
    completeness_bound_from_text,
    cross_check_html,
    evaluate_exact_form,
    index_entries,
    normalized_polynomial,
    parse_entries,
)
from sqpack.yamlio import safe_load

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRONTIER = ROOT / "frontier"
COVERAGE = FRONTIER / "source-coverage.yaml"
EVIDENCE = FRONTIER / "evidence.yaml"

#: Significant digits the exact-form reconciliation agrees to. The catalogue prints 14
#: places, and a wrong radical usually agrees to the printed precision, so comparing at
#: the printed precision would catch almost nothing worth catching.
EXACT_FORM_DIGITS = 40

#: A malformed exact form or polynomial must be reported, not raised: the run has to
#: name every divergence it found, not stop at the first. SymPy's `SympifyError` and its
#: tokenizer errors are all one of these.
_FORM_ERRORS = (ValueError, TypeError, SyntaxError, AttributeError)


def parse_case(path: pathlib.Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return safe_load(text.split("---\n")[1])["packing"]


def parse_kingbird(path: pathlib.Path, n_min: int, n_max: int) -> dict[int, str]:
    """Read the catalogue's visible boxes, then apply its stated grid fallback."""
    text = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.DOTALL)
    blocks = re.findall(
        r'<div class="box"><font size="\+3">(.*?)</div></div>', text, flags=re.DOTALL
    )
    values: dict[int, str] = {}
    for block in blocks:
        label = re.match(r"\s*([0-9][0-9, ]*)<br>", block)
        if label is None:
            continue
        ns = [int(value) for value in re.findall(r"\d+", label.group(1))]
        approximate = re.search(r"\\Nn\{([0-9]+(?:\.[0-9]+)?)\}", block)
        integer = re.search(r"\$s\s*=\s*([0-9]+(?:\.[0-9]+)?)\$", block)
        match = approximate or integer
        if match is None:
            raise ValueError(f"could not parse Kingbird value for labels {ns}")
        value = match.group(1)
        for n in ns:
            previous = values.setdefault(n, value)
            if previous != value:
                raise ValueError(f"conflicting Kingbird values for n={n}: {previous}, {value}")
    for n in range(n_min, n_max + 1):
        values.setdefault(n, str(math.isqrt(n - 1) + 1))
    return values


def source_by_id(coverage: dict, source_id: str) -> dict:
    matches = [source for source in coverage["sources"] if source["id"] == source_id]
    if len(matches) != 1:
        raise ValueError(f"source id {source_id!r} occurs {len(matches)} times")
    return matches[0]


def scope_contains(scope: dict, n: int) -> bool:
    """Return whether a source's declared scope includes one case."""
    if "n_values" in scope:
        return n in scope["n_values"]
    return scope["n_min"] <= n <= scope["n_max"]


def replay_input_errors(evidence: list[dict]) -> list[str]:
    """Require case-specific replays to name their retained source explicitly."""
    errors: list[str] = []
    module = "cases.kingbird29.verify_svg"
    for entry in evidence:
        replay = entry.get("replay")
        if not isinstance(replay, str) or module not in replay:
            continue
        tokens = shlex.split(replay)
        try:
            module_index = tokens.index(module)
        except ValueError:
            errors.append(f"{entry['id']}: malformed {module} replay command")
            continue
        arguments = tokens[module_index + 1 :]
        if not arguments or arguments[0].startswith("-"):
            errors.append(f"{entry['id']}: {module} replay omits its retained SVG input")
            continue
        source = ROOT / arguments[0]
        if not source.is_file():
            errors.append(f"{entry['id']}: replay input does not exist: {arguments[0]}")
    return errors


def _summarize_polynomial(coefficients: tuple[int, ...]) -> str:
    """Name a polynomial by degree and leading coefficients, not by its full text.

    Several of these run to thousands of digits; printing two of them in a failure
    message would bury the `n` and the field that failed.
    """
    head = ", ".join(str(value) for value in coefficients[:4])
    tail = "" if len(coefficients) <= 4 else ", ..."
    return f"degree {len(coefficients) - 1} [{head}{tail}]"


def exact_form_errors(n: int, bound: Mapping, entry: CatalogueEntry) -> list[str]:
    """Compare one record's `exact_form` with the closed form the catalogue prints.

    Semantically, in three ways: the two forms must agree to `EXACT_FORM_DIGITS`, and
    each must agree with the decimal the catalogue prints beside them. The third check
    is what a string comparison cannot do -- it catches a form that is well spelled and
    denotes the wrong number.
    """
    stated = entry.exact_form
    recorded = bound.get("exact_form")
    where = f"catalogue line {entry.source_line}"
    if stated is None:
        return []
    if recorded is None:
        return [f"n={n}: exact_form: record has null, {where} prints {stated!r}"]
    try:
        recorded_value = evaluate_exact_form(str(recorded), EXACT_FORM_DIGITS + 10)
        stated_value = evaluate_exact_form(stated, EXACT_FORM_DIGITS + 10)
    except _FORM_ERRORS as error:
        return [f"n={n}: exact_form: {recorded!r} or {stated!r} does not evaluate: {error}"]

    errors: list[str] = []
    tolerance = abs(stated_value) * Decimal(10) ** -EXACT_FORM_DIGITS
    if abs(recorded_value - stated_value) > tolerance:
        errors.append(
            f"n={n}: exact_form: record has {recorded!r} = {recorded_value}, "
            f"{where} prints {stated!r} = {stated_value}"
        )
    for owner, value in (("record", recorded_value), ("catalogue", stated_value)):
        if not agrees_with_printed_decimal(value, entry.side_decimal):
            errors.append(
                f"n={n}: exact_form: the {owner}'s form evaluates to {value}, which is "
                f"not the decimal {entry.side_decimal} printed at {where}"
            )
    return errors


def degree_errors(n: int, bound: Mapping, entry: CatalogueEntry) -> list[str]:
    """Compare one record's `algebraic_degree` with the catalogue's degree lock."""
    stated = entry.algebraic_degree
    recorded = bound.get("algebraic_degree")
    where = f"catalogue line {entry.source_line}"
    if stated is None:
        return []
    if recorded is None:
        return [f"n={n}: algebraic_degree: record has null, {where} locks degree {stated}"]
    if int(recorded) != stated:
        return [f"n={n}: algebraic_degree: record has {recorded}, {where} locks {stated}"]
    return []


def polynomial_errors(n: int, bound: Mapping, entry: CatalogueEntry) -> list[str]:
    """Compare one record's `minimal_polynomial` with the catalogue's, as polynomials.

    Both sides are reduced to primitive integer coefficients first, so a trailing `= 0`,
    a braced exponent, and any rational scale all wash out, and a polynomial the
    catalogue prints over a real quadratic field is compared through its norm over the
    rationals -- which is the spelling the frontier records for `n = 37`.
    """
    stated = entry.minimal_polynomial
    recorded = bound.get("minimal_polynomial")
    where = f"catalogue line {entry.source_line}"
    if stated is None:
        return []
    if recorded is None:
        return [f"n={n}: minimal_polynomial: record has null, {where} prints one"]
    try:
        recorded_coefficients = normalized_polynomial(str(recorded))
        stated_coefficients = normalized_polynomial(stated)
    except _FORM_ERRORS as error:
        return [f"n={n}: minimal_polynomial: does not read as a polynomial: {error}"]
    if recorded_coefficients != stated_coefficients:
        return [
            (
                f"n={n}: minimal_polynomial: record has "
                f"{_summarize_polynomial(recorded_coefficients)}, {where} prints "
                f"{_summarize_polynomial(stated_coefficients)}"
            )
        ]
    return []


def rigidity_errors(n: int, bound: Mapping, entry: CatalogueEntry | None) -> list[str]:
    """Compare one record's `catalogue_rigid` with the entry's own annotation.

    Checked for every `n`, including the two a newer release governs: the field records
    what the catalogue says, which does not depend on whose value the record reports.
    Silence is `not-stated`, never `false`; the catalogue never asserts that a packing
    can move.
    """
    recorded = bound.get("catalogue_rigid")
    expected = entry.catalogue_rigid if entry is not None else NOT_STATED
    where = (
        f"catalogue line {entry.source_line}"
        if entry is not None
        else "no catalogue block lists this n"
    )
    if recorded not in RIGIDITY_STATES:
        return [f"n={n}: catalogue_rigid is {recorded!r}, not one of {list(RIGIDITY_STATES)}"]
    if recorded != expected:
        return [f"n={n}: catalogue_rigid: record has {recorded!r}, {where} says {expected!r}"]
    return []


def trivial_packing_errors(n: int, bound: Mapping, completeness_bound: int) -> list[str]:
    """Check a case the catalogue settles by its completeness sentence rather than a block.

    The page states that for every `n` at or below its bound that it does not picture,
    the trivial untilted packing is the best known. That packing's side is the integer
    `ceil(sqrt(n))`, so the record's exact form here is neither optional nor a radical --
    the same claim the value reconciliation above already reads from that sentence.
    """
    if n > completeness_bound:
        return []
    side = math.isqrt(n - 1) + 1
    stated = (
        f"the catalogue's unpictured n <= {completeness_bound} take the trivial packing, "
        f"of side {side}"
    )
    recorded = bound.get("exact_form")
    if recorded is None:
        return [f"n={n}: exact_form: record has null, {stated}"]
    try:
        value = evaluate_exact_form(str(recorded), EXACT_FORM_DIGITS + 10)
    except _FORM_ERRORS as error:
        return [f"n={n}: exact_form: {recorded!r} does not evaluate: {error}"]
    if value != Decimal(side):
        return [f"n={n}: exact_form: record has {recorded!r} = {value}, but {stated}"]
    return []


def catalogue_transcription_errors(
    cases: Mapping[int, Mapping],
    catalogue: Mapping[int, CatalogueEntry],
    source_key: str,
    completeness_bound: int,
) -> tuple[list[str], int, int]:
    """Reconcile every hand-transcribed catalogue field, and count what was checked.

    Returns the divergences, the number of cases compared against a catalogue block, and
    the number of printed facts those comparisons covered. The count is part of the
    result: a parser that quietly stopped matching would otherwise agree with every
    record, which is the failure this check exists to prevent.
    """
    errors: list[str] = []
    compared = 0
    facts = 0
    for n in sorted(cases):
        bound = cases[n].get("reported_upper_bound")
        if not isinstance(bound, Mapping):
            errors.append(f"n={n}: reported_upper_bound is missing or malformed")
            continue
        entry = catalogue.get(n)
        errors.extend(rigidity_errors(n, bound, entry))
        facts += 1
        if entry is None:
            if bound.get("source_key") == source_key:
                errors.extend(trivial_packing_errors(n, bound, completeness_bound))
                facts += 1
            continue
        if bound.get("source_key") != source_key:
            # A newer first-party release reports this case, so the catalogue's block
            # describes a different packing; its exact form is not this record's to hold.
            continue
        compared += 1
        if Decimal(str(bound.get("value"))) != Decimal(entry.side_decimal):
            errors.append(
                f"n={n}: value: record has {bound.get('value')}, catalogue line "
                f"{entry.source_line} prints {entry.side_decimal}"
            )
        facts += sum(
            field is not None
            for field in (entry.exact_form, entry.algebraic_degree, entry.minimal_polynomial)
        )
        errors.extend(exact_form_errors(n, bound, entry))
        errors.extend(degree_errors(n, bound, entry))
        errors.extend(polynomial_errors(n, bound, entry))
    return errors, compared, facts


def main() -> int:
    coverage = safe_load(COVERAGE.read_text(encoding="utf-8"))
    n_min = coverage["case_corpus"]["n_min"]
    n_max = coverage["case_corpus"]["n_max"]
    errors: list[str] = []

    reader_view = ROOT / coverage["case_corpus"]["reader_view"]
    if not reader_view.is_file():
        errors.append(f"case reader view does not exist: {reader_view.relative_to(ROOT)}")
    if n_min > n_max:
        errors.append(f"case corpus range is reversed: {n_min}..{n_max}")

    source_ids = [source["id"] for source in coverage["sources"]]
    if len(source_ids) != len(set(source_ids)):
        errors.append("source ids are not unique")
    errors.extend(
        f"{source['id']}: local source does not exist: {source['local']}"
        for source in coverage["sources"]
        if not (ROOT / source["local"]).exists()
    )

    evidence_document = safe_load(EVIDENCE.read_text(encoding="utf-8"))
    evidence = evidence_document["evidence"]
    evidence_ids = [entry["id"] for entry in evidence]
    if len(evidence_ids) != len(set(evidence_ids)):
        errors.append("frontier evidence ids are not unique")
    errors.extend(replay_input_errors(evidence))
    evidence_id_set = set(evidence_ids)
    for source in coverage["sources"]:
        errors.extend(
            f"{source['id']}: unknown evidence id {evidence_id}"
            for evidence_id in source["evidence"]
            if evidence_id not in evidence_id_set
        )

    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1

    kingbird_source = source_by_id(coverage, "kingbird-current")
    kingbird = parse_kingbird(ROOT / kingbird_source["local"], n_min, n_max)
    overrides = {entry["n"]: entry for entry in coverage["selected_overrides"]}
    if len(overrides) != len(coverage["selected_overrides"]):
        errors.append("selected override n values are not unique")
    for entry in coverage["selected_overrides"]:
        n = entry["n"]
        if not n_min <= n <= n_max:
            errors.append(f"selected override n={n} lies outside the case corpus")
        if entry["source_id"] not in source_ids:
            errors.append(f"selected override n={n} names unknown source {entry['source_id']}")
            continue
        source = source_by_id(coverage, entry["source_id"])
        if not scope_contains(source["scope"], n):
            errors.append(f"selected override n={n} is outside {source['id']}'s scope")
        if entry["evidence"] not in source["evidence"]:
            errors.append(
                f"selected override n={n} uses evidence {entry['evidence']} "
                f"not declared by {source['id']}"
            )

    cases = {
        case["n"]: case
        for case in (parse_case(path) for path in sorted(FRONTIER.glob("n-[0-9][0-9][0-9].md")))
    }
    expected_ns = set(range(n_min, n_max + 1))
    if set(cases) != expected_ns:
        errors.append(f"case corpus is not exactly n={n_min}..{n_max}")
    for n in sorted(expected_ns & set(cases)):
        case = cases[n]
        bound = case["reported_upper_bound"]
        if n in overrides:
            expected = overrides[n]
            source = source_by_id(coverage, expected["source_id"])
            expected_value = expected["value"]
            expected_key = source["source_key"]
            if expected["evidence"] not in bound["evidence"]:
                errors.append(f"n={n}: selected evidence {expected['evidence']} is absent")
        else:
            expected_value = kingbird[n]
            expected_key = kingbird_source["source_key"]
        if Decimal(bound["value"]) != Decimal(expected_value):
            errors.append(
                f"n={n}: reported upper {bound['value']} != selected source {expected_value}"
            )
        if bound["source_key"] != expected_key:
            errors.append(
                f"n={n}: source {bound['source_key']!r} != selected source {expected_key!r}"
            )

    # The register names the retained HTML; the Markdown transcription beside it is what
    # carries the entry structure, and the two are cross-checked below on labels and
    # printed sides so a box lost in transcription cannot pass as source silence.
    catalogue_html = ROOT / kingbird_source["local"]
    entries: tuple[CatalogueEntry, ...] = ()
    compared = facts = 0
    try:
        transcription_text = catalogue_html.with_suffix(".md").read_text(encoding="utf-8")
        entries = parse_entries(transcription_text)
        errors.extend(cross_check_html(entries, catalogue_html.read_text(encoding="utf-8")))
        transcription, compared, facts = catalogue_transcription_errors(
            cases,
            index_entries(entries),
            kingbird_source["source_key"],
            completeness_bound_from_text(transcription_text),
        )
        errors.extend(transcription)
    except CatalogueParseError as error:
        errors.append(f"retained catalogue: {error}")

    unit_source = source_by_id(coverage, "unitsquare-release1")
    release = json.loads((ROOT / unit_source["local"]).read_text(encoding="utf-8"))
    release_values = {entry["n"]: entry["offered_side"] for entry in release["results"]}
    inventory = {entry["n"]: entry["value"] for entry in coverage["beyond_horizon_claims"]}
    if len(inventory) != len(coverage["beyond_horizon_claims"]):
        errors.append("beyond-horizon n values are not unique")
    for entry in coverage["beyond_horizon_claims"]:
        n = entry["n"]
        if n_min <= n <= n_max:
            errors.append(f"beyond-horizon claim n={n} lies inside the case corpus")
        if entry["source_id"] not in source_ids:
            errors.append(f"beyond-horizon n={n} names unknown source {entry['source_id']}")
            continue
        source = source_by_id(coverage, entry["source_id"])
        if not scope_contains(source["scope"], n):
            errors.append(f"beyond-horizon n={n} is outside {source['id']}'s scope")
    for n, expected in release_values.items():
        recorded = overrides.get(n, {}).get("value") if n <= n_max else inventory.get(n)
        if recorded != expected:
            errors.append(f"UnitSquare n={n}: source {expected} != inventory {recorded}")
    if set(release_values) != set(overrides) | set(inventory):
        errors.append("UnitSquare result set differs from in- and beyond-horizon inventory")

    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    print(
        f"  source coverage reconciled: {n_max - n_min + 1} cases, "
        f"{len(overrides)} newer in-horizon reports, {len(inventory)} tracked beyond horizon"
    )
    print(
        f"  catalogue transcription reconciled: {len(entries)} entries reparsed, "
        f"{compared} cases matched to a block, {facts} printed facts checked, "
        f"0 divergences"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
