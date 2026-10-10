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
from collections.abc import Callable, Mapping, Sequence
from datetime import date
from decimal import Decimal
from fractions import Fraction

from devtools.retained_data import read_retained_text, retained_exists
from sqpack.kingbird_catalogue import (
    INTAKE_CAPTURE_DATE,
    INTAKE_CATALOGUE_HTML,
    INTAKE_CATALOGUE_MARKDOWN,
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
#: The acquisition record `devtools.upper_bound_packets` writes into a packet.
ACQUISITION_FORMAT = "external-source-acquisition-v1"
#: The disposition of the source whose values every case reports unless overridden.
BASELINE_DISPOSITION = "baseline-current"

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


def _stated_form_agrees_with_its_decimal(stated: str, entry: CatalogueEntry) -> bool:
    """Whether the catalogue's own printed form denotes the decimal printed beside it.

    A form that does not evaluate at all is reported by the caller's later evaluation;
    here it counts as agreeing so that the ordinary comparison, and its error, run.
    """
    try:
        value = evaluate_exact_form(stated, EXACT_FORM_DIGITS + 10)
    except _FORM_ERRORS:
        return True
    return agrees_with_printed_decimal(value, entry.side_decimal)


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
    if not _stated_form_agrees_with_its_decimal(stated, entry):
        # The catalogue contradicts itself: the printed form does not denote the printed
        # decimal (n = 179 prints a superseded closed form beside a newer value). The
        # record must then carry no form at all; a generated record says why in a typed
        # `stale-source` conflict, and a form copied from such an entry is the error.
        if recorded is None:
            return []
        return [
            (
                f"n={n}: exact_form: record has {recorded!r}, but {where} prints "
                f"{stated!r}, which does not evaluate to the decimal {entry.side_decimal} "
                "printed beside it; the record may carry no form from a self-contradicting "
                "entry"
            )
        ]
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


#: What a record's `source-evidence` blocker names while its count is declared pending
#: catalogue intake. The record says so where a reader and `STATUS.md` see it, rather
#: than only in this register, which has no reader view.
PENDING_INTAKE_MARKER = "pending_catalogue_intake"


def pending_intake_blocker(case: Mapping) -> Mapping | None:
    """The record's blocker declaring a pending catalogue intake, if it carries one."""
    for blocker in case.get("blockers") or ():
        if blocker.get("kind") == "source-evidence" and PENDING_INTAKE_MARKER in str(
            blocker.get("detail", "")
        ):
            return blocker
    return None


#: A bead alias as the records name one.
BEAD_ALIAS = re.compile(r"think-[a-z0-9]{4}")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def deferral_errors(entry: Mapping, where: str) -> list[str]:
    """What a pending catalogue intake lacks to be owned: its bead and its date."""
    bead, recorded = str(entry.get("bead") or ""), str(entry.get("recorded") or "")
    errors: list[str] = []
    if not BEAD_ALIAS.fullmatch(bead):
        errors.append(
            f"{where} names no bead ({bead or 'none'}); a deferral names the open bead "
            "that owns the intake"
        )
    if not _DATE.fullmatch(recorded):
        errors.append(f"{where} records no date ({recorded or 'none'}) it was deferred on")
    return errors


def pending_intake_errors(
    pending: Sequence[Mapping],
    current: Mapping[int, str],
    earlier: Mapping[int, str],
    cases: Mapping[int, Mapping],
) -> list[str]:
    """Hold each declared pending catalogue intake to both captures and to its record.

    A declaration says: the current capture prints a side below the one this record
    reports, the record still transcribes the earlier capture, and moving it is an intake
    of its own -- a result by others that the register must hold first. So the current
    capture must print exactly the declared side, the earlier capture must print
    something else, the declared side must beat the record's, and the record must still
    report the side it declared, with a `source-evidence` blocker naming
    `PENDING_INTAKE_MARKER` and the newer side, so the record itself says it trails the
    source; no record may carry that blocker undeclared. Once the intake lands the record
    reports the current side, and the declaration then fails here until it is removed.

    A declaration is also a deferral, and a deferral is work: it names the bead that owns
    the intake and the day it was recorded. The three declared on 2026-09-30 named no
    bead, nothing listed them, and the record trailed the catalogue for five days until
    the owner noticed. Whether the bead is still open is not a fact of the tree, so
    `check_bead_tree` asks the bead store, and `devtools.intake_sweep` reports the age.
    """
    errors: list[str] = []
    seen: set[int] = set()
    for entry in pending:
        n = int(entry["n"])
        where = f"pending catalogue intake n={n}"
        if n in seen:
            errors.append(f"{where} is declared twice")
        seen.add(n)
        errors.extend(deferral_errors(entry, where))
        if entry["capture"] != INTAKE_CAPTURE_DATE:
            errors.append(
                f"{where} names capture {entry['capture']}; the one retained earlier "
                f"capture is {INTAKE_CAPTURE_DATE}"
            )
            continue
        printed = current.get(n)
        if printed is None or Decimal(printed) != Decimal(entry["catalogue_value"]):
            errors.append(
                f"{where}: the current capture prints {printed}, not the declared "
                f"{entry['catalogue_value']}"
            )
        before = earlier.get(n)
        if printed is not None and before is not None and Decimal(printed) == Decimal(before):
            errors.append(f"{where}: both captures print {printed}; nothing is pending")
        if Decimal(entry["catalogue_value"]) >= Decimal(entry["record_value"]):
            errors.append(f"{where}: {entry['catalogue_value']} does not beat the record")
        case = cases.get(n)
        reported = None if case is None else case["reported_upper_bound"]["value"]
        if reported is None or Decimal(str(reported)) != Decimal(entry["record_value"]):
            errors.append(
                f"{where}: the record reports {reported}, not the declared "
                f"{entry['record_value']}; remove the declaration once the intake lands"
            )
        blocker = None if case is None else pending_intake_blocker(case)
        if blocker is None or entry["catalogue_value"] not in str(blocker.get("detail")):
            errors.append(
                f"{where}: the record carries no source-evidence blocker naming "
                f"{PENDING_INTAKE_MARKER} and the side {entry['catalogue_value']}"
            )
    errors.extend(
        f"n={n}: the record declares a pending catalogue intake that "
        f"source-coverage.yaml does not list"
        for n in sorted(cases)
        if n not in seen and pending_intake_blocker(cases[n]) is not None
    )
    return errors


def record_catalogue(
    current: Mapping[int, CatalogueEntry], pending: Sequence[Mapping]
) -> dict[int, CatalogueEntry]:
    """The catalogue entry each record transcribes, by count.

    The current capture's, except at a count declared pending intake, whose record still
    transcribes the earlier capture and is reconciled against that capture's entry.
    """
    indexed = dict(current)
    if not pending:
        return indexed
    earlier_text = (ROOT / INTAKE_CATALOGUE_MARKDOWN).read_text(encoding="utf-8")
    earlier = index_entries(parse_entries(earlier_text))
    for entry in pending:
        n = int(entry["n"])
        if n in earlier:
            indexed[n] = earlier[n]
        else:
            indexed.pop(n, None)
    return indexed


def load_claims(path: pathlib.Path) -> dict[int, str]:
    """A source's upper-bound claims by `n`, reparsed from its own retained record.

    Three shapes are read: a UnitSquare results release, whose `results` carry
    `offered_side`; an acquisition record written by `devtools.upper_bound_packets`,
    whose one source's `cases` carry the `side` each retained packing file prints; and a
    directory of exact certificates `n-N.cert` in Evan Daniel's format, each claiming the
    side its header gives, written out in full (`devtools.evand_exact_certificates`).
    """
    if path.is_dir():
        from devtools import evand_exact_certificates as certificates  # noqa: PLC0415

        claims: dict[int, str] = {}
        for n in certificates.certificate_counts(path):
            text = certificates.certificate_path(path, n).read_text(encoding="utf-8")
            side = certificates.parse(text, expected_n=n).side
            written = certificates.terminating_decimal(side)
            if written is None:
                raise ValueError(f"n={n}: the certificate's side does not terminate in decimal")
            claims[n] = written
        return claims
    from devtools import ryxu_house_links as ryxu  # noqa: PLC0415

    if path == ryxu.reports.fact_path():
        return {
            n: ryxu.reports.legacy.ceiling_decimal(fact.side, 16)
            for n, fact in ryxu.reports.read_facts().items()
        }
    if path == ryxu.radical.fact_path():
        ryxu.radical.read_fact()
        return {51: ryxu.radical_display()}
    record = json.loads(read_retained_text(path))
    if isinstance(record.get("results"), list):
        return {int(entry["n"]): str(entry["offered_side"]) for entry in record["results"]}
    if record.get("format") == ACQUISITION_FORMAT:
        (entry,) = record["sources"]
        return {int(case["n"]): str(case["side"]) for case in entry["cases"]}
    raise ValueError(f"{path.name} is not a claims record this check can reparse")


def selection_errors(
    coverage: Mapping, kingbird: Mapping[int, str], claims: Mapping[str, Mapping[int, str]]
) -> list[str]:
    """Reconcile the selected overrides and superseded reports with their sources.

    An override may come from any retained source. It must lie in that source's scope,
    use evidence the source declares, report a side strictly below the catalogue
    baseline it replaces, and, where the source's claims are reparsed here, equal the
    side the source itself prints. A superseded report is a retained claim that a
    selected override at the same `n` beats: it must equal its own source's printed side
    and exceed the override's. Where no override is selected the report may instead name
    the catalogue baseline, which must then print a side below it -- what a later capture
    of the catalogue does when it overtakes a release (`n = 69`, 2026-10-05, T-088). Every
    reparsed claim is then accounted for exactly once, as a selected override, a
    superseded report, or a claim tracked beyond the corpus.
    """
    errors: list[str] = []
    n_min = coverage["case_corpus"]["n_min"]
    n_max = coverage["case_corpus"]["n_max"]
    sources = {source["id"]: source for source in coverage["sources"]}
    baselines = {
        source["id"]
        for source in coverage["sources"]
        if source.get("disposition") == BASELINE_DISPOSITION
    }
    overrides = {entry["n"]: entry for entry in coverage["selected_overrides"]}
    if len(overrides) != len(coverage["selected_overrides"]):
        errors.append("selected override n values are not unique")
    accounted: dict[str, set[int]] = {}
    for entry in coverage["selected_overrides"]:
        n, source_id = entry["n"], entry["source_id"]
        where = f"selected override n={n}"
        if not n_min <= n <= n_max:
            errors.append(f"{where} lies outside the case corpus")
        source = sources.get(source_id)
        if source is None:
            errors.append(f"{where} names unknown source {source_id}")
            continue
        if not scope_contains(source["scope"], n):
            errors.append(f"{where} is outside {source_id}'s scope")
        if entry["evidence"] not in source["evidence"]:
            errors.append(
                f"{where} uses evidence {entry['evidence']} not declared by {source_id}"
            )
        if n in kingbird and Decimal(entry["value"]) >= Decimal(kingbird[n]):
            errors.append(f"{where} does not beat the catalogue baseline {kingbird[n]}")
        errors.extend(_claim_errors(where, source_id, n, entry["value"], claims))
        accounted.setdefault(source_id, set()).add(n)
    for entry in coverage["superseded_reports"]:
        n, source_id = entry["n"], entry["source_id"]
        where = f"superseded report n={n} from {source_id}"
        source = sources.get(source_id)
        if source is None:
            errors.append(f"{where} names an unknown source")
            continue
        if not scope_contains(source["scope"], n):
            errors.append(f"{where} is outside that source's scope")
        if n in accounted.get(source_id, set()):
            errors.append(f"{where} is listed twice")
        accounted.setdefault(source_id, set()).add(n)
        errors.extend(_claim_errors(where, source_id, n, entry["value"], claims))
        selected = overrides.get(n)
        if selected is None and entry["superseded_by"] in baselines:
            # No override is selected, so the catalogue baseline is the case's report and
            # what beat this claim: a later capture printing a smaller side.
            printed = kingbird.get(n)
            if printed is None or Decimal(printed) >= Decimal(entry["value"]):
                errors.append(f"{where} is not beaten by the catalogue baseline {printed}")
        elif selected is None or selected["source_id"] != entry["superseded_by"]:
            errors.append(f"{where} names {entry['superseded_by']}, not the selected source")
        elif Decimal(selected["value"]) >= Decimal(entry["value"]):
            errors.append(f"{where} is not beaten by the selected {selected['value']}")
    beyond, inventory = beyond_horizon_errors(coverage, claims)
    errors.extend(beyond)
    for source_id, claimed in sorted(claims.items()):
        held = accounted.get(source_id, set()) | inventory.get(source_id, set())
        if set(claimed) != held:
            missing = sorted(set(claimed) - held)
            extra = sorted(held - set(claimed))
            errors.append(
                f"{source_id}: reparsed claims differ from the selected, superseded and "
                f"beyond-horizon inventory (unaccounted {missing}, not claimed {extra})"
            )
    return errors


def _claim_errors(
    where: str, source_id: str, n: int, value: str, claims: Mapping[str, Mapping[int, str]]
) -> list[str]:
    if source_id not in claims:
        return []
    printed = claims[source_id].get(n)
    if printed is None:
        return [f"{where}: {source_id}'s retained record makes no claim at n={n}"]
    if Decimal(printed) != Decimal(value):
        return [f"{where}: {source_id} prints {printed}, the inventory says {value}"]
    return []


#: The disposition of a beyond-horizon row a later report of the same claim beats.
SUPERSEDED = "superseded"

#: How a later report of each claim beats an earlier one, compared exactly. An exact
#: value has no direction: two that differ conflict, and neither improves the other.
_BEATS: dict[str, Callable[[Fraction, Fraction], bool]] = {
    "upper-bound": lambda later, earlier: later < earlier,
    "lower-bound": lambda later, earlier: later > earlier,
}


def beyond_horizon_errors(
    coverage: Mapping, claims: Mapping[str, Mapping[int, str]]
) -> tuple[list[str], dict[str, set[int]]]:
    """Hold every dated row beyond the case corpus, and say which claims they account for.

    Rows are keyed on `(n, source_id)`, so a count may carry several: at most one current
    row, and every earlier report a later one beats, kept as its source printed it, with
    `disposition: superseded` and `superseded_by` naming the successor's source. Couzo's
    2d32a6e reports at `n = 375` and `378` beat his ffd900d reports at the same counts,
    and a register with one row per count could hold only one of the two.

    Each row must lie outside the corpus and inside the scope of a source that declares
    a claims record, and read that record's reparsed claim byte for byte: a dated row
    keeps the facts it was recorded with. Each successor must be a row at the same
    count, of the same claim, from a source dated no earlier, and strictly better by
    exact rational comparison of the printed decimals. Strict improvement along every
    link makes a cycle impossible, since a cycle would make some value strictly better
    than itself, so every chain of successors ends at the count's current row and no
    separate cycle check is needed.
    Returns the errors and, by source, the counts whose claims the rows account for.
    """
    errors: list[str] = []
    n_min = coverage["case_corpus"]["n_min"]
    n_max = coverage["case_corpus"]["n_max"]
    sources = {source["id"]: source for source in coverage["sources"]}
    rows: dict[tuple[int, str], Mapping] = {}
    current: dict[int, list[str]] = {}
    inventory: dict[str, set[int]] = {}
    for entry in coverage["beyond_horizon_claims"]:
        n, source_id = entry["n"], entry["source_id"]
        where = f"beyond-horizon n={n} from {source_id}"
        if (n, source_id) in rows:
            errors.append(f"{where} is listed twice; a count has one row per source")
            continue
        rows[n, source_id] = entry
        if n_min <= n <= n_max:
            errors.append(f"beyond-horizon claim n={n} lies inside the case corpus")
        if entry.get("disposition") == SUPERSEDED:
            if not entry.get("superseded_by"):
                errors.append(f"{where} is superseded but names no successor")
        else:
            current.setdefault(n, []).append(source_id)
            if "superseded_by" in entry:
                errors.append(
                    f"{where} names successor {entry['superseded_by']} but is not superseded"
                )
        if source_id not in sources:
            errors.append(f"beyond-horizon n={n} names unknown source {source_id}")
            continue
        if not scope_contains(sources[source_id]["scope"], n):
            errors.append(f"beyond-horizon n={n} is outside {source_id}'s scope")
        if not sources[source_id].get("claims_record"):
            errors.append(
                f"{where}: {source_id} declares no claims record, so the row is compared "
                "with nothing its source prints"
            )
        errors.extend(_claim_errors(where, source_id, n, entry["value"], claims))
        printed = claims.get(source_id, {}).get(n)
        if (
            printed is not None
            and printed != entry["value"]
            and Decimal(printed) == Decimal(entry["value"])
        ):
            errors.append(
                f"{where} reads {entry['value']!r}, not {printed!r} as its source prints "
                "it; a dated row keeps its source's facts byte for byte"
            )
        inventory.setdefault(source_id, set()).add(n)
    errors.extend(
        f"beyond-horizon n={n} has {len(held)} current rows ({', '.join(held)}); a count "
        "has at most one, and each earlier report names the row that supersedes it"
        for n, held in sorted(current.items())
        if len(held) > 1
    )
    for entry in rows.values():
        if entry.get("disposition") == SUPERSEDED and entry.get("superseded_by"):
            errors.extend(_succession_errors(entry, rows, sources))
    return errors, inventory


def _succession_errors(
    entry: Mapping,
    rows: Mapping[tuple[int, str], Mapping],
    sources: Mapping[str, Mapping],
) -> list[str]:
    """What a superseded row's named successor fails to be."""
    n, source_id, successor_id = entry["n"], entry["source_id"], entry["superseded_by"]
    where = f"beyond-horizon n={n} from {source_id}"
    if successor_id == source_id:
        return [f"{where} names itself as its successor"]
    successor = rows.get((n, successor_id))
    if successor is None:
        elsewhere = sorted(count for count, owner in rows if owner == successor_id)
        held = f"; its rows are at n={elsewhere}" if elsewhere else ""
        return [f"{where} names successor {successor_id}, which has no row at n={n}{held}"]
    errors: list[str] = []
    if successor["claim"] != entry["claim"]:
        errors.append(
            f"{where} claims {entry['claim']}, and its successor from {successor_id} "
            f"claims {successor['claim']}"
        )
    elif entry["claim"] not in _BEATS:
        errors.append(
            f"{where}: an {entry['claim']} claim is never superseded; a later report that "
            "differs from it conflicts with it, and one that agrees adds nothing"
        )
    elif not _BEATS[entry["claim"]](Fraction(successor["value"]), Fraction(entry["value"])):
        errors.append(
            f"{where}: {entry['value']} is not strictly beaten by {successor['value']} "
            f"from {successor_id}, compared exactly"
        )
    owners = (source_id, successor_id)
    dates = [sources.get(owner, {}).get("source_date") for owner in owners]
    if None in dates:
        undated = [owner for owner, day in zip(owners, dates, strict=True) if day is None]
        errors.append(
            f"{where}: {', '.join(undated)} has no source_date, and a supersession orders "
            "dated reports"
        )
    elif date.fromisoformat(str(dates[1])) < date.fromisoformat(str(dates[0])):
        errors.append(
            f"{where} is dated {dates[0]}, after its successor from {successor_id}, dated "
            f"{dates[1]}"
        )
    return errors


def current_beyond_horizon(coverage: Mapping) -> dict[int, Mapping]:
    """Each count's current beyond-horizon row: the one no later report supersedes.

    Refuses a count with more than one current row rather than choosing between them;
    `beyond_horizon_errors` reports the same register as a failure.
    """
    current: dict[int, Mapping] = {}
    for entry in coverage["beyond_horizon_claims"]:
        if entry.get("disposition") == SUPERSEDED:
            continue
        n = entry["n"]
        if n in current:
            raise ValueError(
                f"beyond-horizon n={n} has more than one current row "
                f"({current[n]['source_id']}, {entry['source_id']})"
            )
        current[n] = entry
    return current


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
    errors.extend(
        f"{source['id']}: claims record does not exist: {source['claims_record']}"
        for source in coverage["sources"]
        if source.get("claims_record")
        and not (ROOT / source["claims_record"]).is_dir()
        and not retained_exists(ROOT / source["claims_record"])
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
    # A count declared pending intake is still read against the capture its record
    # transcribes; `pending_intake_errors` holds the declaration to both captures.
    pending = coverage.get("pending_catalogue_intake", [])
    earlier = parse_kingbird(ROOT / INTAKE_CATALOGUE_HTML, n_min, n_max) if pending else {}
    baseline = dict(kingbird)
    baseline.update({int(entry["n"]): earlier[int(entry["n"])] for entry in pending})
    overrides = {entry["n"]: entry for entry in coverage["selected_overrides"]}
    claims = {
        source["id"]: load_claims(ROOT / source["claims_record"])
        for source in coverage["sources"]
        if source.get("claims_record")
    }
    errors.extend(selection_errors(coverage, baseline, claims))

    cases = {
        case["n"]: case
        for case in (parse_case(path) for path in sorted(FRONTIER.glob("n-[0-9][0-9][0-9].md")))
    }
    errors.extend(pending_intake_errors(pending, kingbird, earlier, cases))
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
            expected_value = baseline[n]
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
            record_catalogue(index_entries(entries), pending),
            kingbird_source["source_key"],
            completeness_bound_from_text(transcription_text),
        )
        errors.extend(transcription)
    except CatalogueParseError as error:
        errors.append(f"retained catalogue: {error}")

    if errors:
        for error in errors:
            print(f"FAIL {error}", file=sys.stderr)
        return 1
    # Only after the reconciliation passed, which refuses a second current row.
    beyond = current_beyond_horizon(coverage)
    dated = len(coverage["beyond_horizon_claims"]) - len(beyond)
    print(
        f"  source coverage reconciled: {n_max - n_min + 1} cases, "
        f"{len(overrides)} newer in-horizon reports from {len(claims)} reparsed claim "
        f"records, {len(coverage['superseded_reports'])} superseded reports, "
        f"{len(beyond)} tracked beyond horizon with {dated} earlier dated "
        f"report{'' if dated == 1 else 's'} superseded there, "
        f"{len(pending)} catalogue count{'' if len(pending) == 1 else 's'} pending intake"
    )
    print(
        f"  catalogue transcription reconciled: {len(entries)} entries reparsed, "
        f"{compared} cases matched to a block, {facts} printed facts checked, "
        f"0 divergences"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
