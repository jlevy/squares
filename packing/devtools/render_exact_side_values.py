#!/usr/bin/env python3
"""Render the exact-side-values register as HTML, Markdown, and optionally PDF.

The register is the paper's only mathematical source.  The article template supplies
exposition; every count, expression, polynomial, check, route, and bead is generated
from ``frontier/exact-values.json``.  Given the site's root with ``--site``, this module
writes a compact browser, lazy JSON payloads, a complete HTML archive, and Markdown.
``--pdf`` prints the complete archive through the shared KPress publication layer;
``--check`` refuses missing, stale, or unexpected browser and archive outputs.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections.abc import Mapping, Sequence
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Any

from kpress.format.pdf import _await_print_fonts  # pyright: ignore[reportPrivateUsage]
from kpress.output import write_bytes_atomic
from strif import atomic_output_file

from devtools import exact_catalogue, paper_front, render_n11_lower_bounds_explainer
from devtools.render_n11_lower_bounds_explainer_pdf import dated
from devtools.render_overview import (
    EMBED_SCRIPT,
    EXACT_SIDE_VALUES,
    MATH_SCRIPT,
    PAPER_TYPE_CSS,
    PAPERS_ROOT,
    SITE_NAV,
    SITE_NAV_CSS,
    SITE_URL,
    THEME_SCRIPT,
    PageMeta,
    colophon_lines,
    favicon_html,
    head_tags,
    nav_html,
    paper_path,
)
from sqpack.probes import probe
from sqpack.release import (
    EXACT_SIDE_VALUES_EDITION,
    EXACT_SIDE_VALUES_FIRST_PUBLISHED,
    EXACT_SIDE_VALUES_REVISED,
)

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent
TEMPLATES = Path(__file__).with_name("templates")
ARTICLE = TEMPLATES / "exact-side-values-article.md"
STYLE = TEMPLATES / "exact-side-values.css"
# The shared review shell has every publication and site layer this paper needs.  The
# renderer changes only its article class; the paper has no diagrams or private script.
SHELL = TEMPLATES / "exact-side-values-shell.html"
BROWSER_SHELL = TEMPLATES / "exact-side-values-browser-shell.html"
BROWSER_STYLE = TEMPLATES / "exact-side-values-browser.css"
BROWSER_SCRIPT = PACKING / "devtools/overview/exact-side-values.js"
BROWSER_SCRIPT_NAME = "exact-side-values-browser.js"
REGISTER = PACKING / "frontier/exact-values.json"
SITE = PACKING / "site"
SLUG = EXACT_SIDE_VALUES
SITE_PATH = paper_path(SLUG)
COMPLETE_PATH = paper_path(f"{SLUG}-complete")
SITE_ROOT = PAPERS_ROOT
TITLE = "Exact Side Values for Packing Unit Squares"
DESCRIPTION = (
    "Exact side expressions and certified polynomials for 1 through 324 unit-square "
    "packings, with historical source polynomials and open exact-value routes."
)
ARCHIVE_DESCRIPTION = (
    "Complete exact-side archive with every polynomial coefficient, current and historical "
    "source records, certificates and open derivation routes."
)
EDITION = EXACT_SIDE_VALUES_EDITION
FIRST_PUBLISHED = EXACT_SIDE_VALUES_FIRST_PUBLISHED
REVISED = EXACT_SIDE_VALUES_REVISED
FRONT = paper_front.check(
    paper_front.PaperFront(
        slug=SLUG,
        title=TITLE,
        oversight=(paper_front.Person("Joshua Levy", "https://x.com/ojoshe"),),
        agents=("GPT-5.6 Sol", "GPT-6 Astra"),
        version=EDITION,
        dates=(
            paper_front.Dated("First published", FIRST_PUBLISHED),
            paper_front.Dated(paper_front.REVISED, REVISED),
        ),
    )
)
MATH_WAIT_MS = 15_000
TYPESET_ALL = probe(
    render_n11_lower_bounds_explainer.PROBES,
    "render_n11_optimality_review/typeset_all",
)
ABSOLUTE_LINKS = probe(
    render_n11_lower_bounds_explainer.PROBES,
    "render_n11_lower_bounds_explainer_pdf/absolute_links",
)
LEFTOVER_SLOT = re.compile(r"\{\{[A-Z][A-Z_]*\}\}")
RELATIVE_LINK = re.compile(r"(?P<start>\]\()(?P<url>\.\.?/[^\s)]+)(?P<end>\))")
RELATIVE_REFERENCE = re.compile(r"(?m)^(?P<start>\[[^\]\n]+\]:[ \t]*)(?P<url>\.\.?/[^\s]+)")
RELATIVE_ANCHOR = re.compile(r'(?P<start><a\b[^>]*\bhref=")(?P<url>\.\.?/[^"]+)(?P<end>")')
CONTRACT = "packing.squares:ExactValues/v1"
POLYNOMIAL_STATES = frozenset(("integer", "rational", "closed-form", "minimal-polynomial"))
COEFFICIENT_TABLE_DEGREE = 64
COEFFICIENT_TABLE_DIGITS = 48
TERMS_PER_DISPLAY = 4
# The complete archive prints at the shared 12pt face and Letter reading measure.
# Long numeric terms need shorter displays; a wide single term uses its full table.
DISPLAY_CHARACTER_BUDGET = 56
PRINT_PROBES = PACKING / "devtools/probes"
PRINT_CONTENT_WIDTH = probe(PRINT_PROBES, "render_exact_side_values/print_content_width")
PRINT_MATH_FIT = probe(PRINT_PROBES, "render_exact_side_values/print_math_fit")

RENDER_INPUTS = (
    Path(__file__),
    ARTICLE,
    STYLE,
    SHELL,
    BROWSER_SHELL,
    BROWSER_STYLE,
    BROWSER_SCRIPT,
    Path(exact_catalogue.__file__),
    PRINT_PROBES / "render_exact_side_values/print_content_width.js",
    PRINT_PROBES / "render_exact_side_values/print_math_fit.js",
    REGISTER,
    PACKING / "devtools/paper_front.py",
    PACKING / "devtools/render_overview.py",
    PACKING / "src/sqpack/release.py",
    PAPER_TYPE_CSS,
    SITE_NAV,
    SITE_NAV_CSS,
    THEME_SCRIPT,
    EMBED_SCRIPT,
    MATH_SCRIPT,
    render_n11_lower_bounds_explainer.PUBLICATION_STYLE,
    render_n11_lower_bounds_explainer.INLINE_SCRIPT_ASSETS["NATIVE_MATH_METRICS"],
    render_n11_lower_bounds_explainer.PROBES
    / "render_n11_lower_bounds_explainer"
    / "host_math_init.js",
    render_n11_lower_bounds_explainer.PROBES
    / "render_n11_optimality_review"
    / "typeset_all.js",
    REPO / "vendor/kpress",
)


class ExactSideValuesPaperError(ValueError):
    """The register cannot support a complete and accurate paper."""


def _as_mapping(value: object, context: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ExactSideValuesPaperError(f"{context} must be an object")
    return value


def _as_sequence(value: object, context: str) -> Sequence[Any]:
    if not isinstance(value, list):
        raise ExactSideValuesPaperError(f"{context} must be an array")
    return value


def load_register(path: Path | None = None) -> Mapping[str, Any]:
    """Load and structurally check the exact-values register used by the paper."""
    source = path or REGISTER
    try:
        document = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ExactSideValuesPaperError(f"cannot read {source}: {error}") from error
    root = _as_mapping(document, source.name)
    softschema = _as_mapping(root.get("softschema"), "softschema")
    if softschema.get("contract") != CONTRACT:
        raise ExactSideValuesPaperError(
            f"{source.name}: expected {CONTRACT}, found {softschema.get('contract')!r}"
        )
    register = _as_mapping(root.get("register"), "register")
    entries = _as_sequence(register.get("entries"), "register.entries")
    numbers = [entry.get("n") for entry in (_as_mapping(row, "entry") for row in entries)]
    if numbers != list(range(1, len(entries) + 1)):
        raise ExactSideValuesPaperError("register.entries must be consecutive from n = 1")
    return register


def entries(register: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    return tuple(
        _as_mapping(row, f"entry {index}")
        for index, row in enumerate(_as_sequence(register.get("entries"), "entries"), 1)
    )


def historical_entries(register: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
    """Return the separately recorded historical polynomial-side pairs."""
    raw = register.get("historical_entries")
    if raw is None:
        return ()
    return tuple(
        _as_mapping(row, f"historical entry {index}")
        for index, row in enumerate(_as_sequence(raw, "register.historical_entries"), 1)
    )


def _table_text(value: object) -> str:
    """Plain register text safe in one Markdown table cell."""
    if value is None:
        return "—"
    return escape(str(value), quote=False).replace("|", "\\|").replace("\n", " ")


def _math(value: object) -> str:
    return "—" if value is None else f"${value}$"


def _claim(entry: Mapping[str, Any]) -> str:
    side = _as_mapping(entry.get("side"), f"n={entry.get('n')} side")
    relation = side.get("relation")
    status = entry.get("status")
    if relation == "equality" and status == "proved":
        return "global optimum proved"
    if relation == "equality":
        return "reported equality; proof status open"
    if relation == "upper-bound":
        return "reported packing upper bound; optimum open"
    return f"{_table_text(relation)}; {_table_text(status)}"


def summary_markdown(register: Mapping[str, Any]) -> str:
    totals = _as_mapping(register.get("totals"), "register.totals")
    rows = entries(register)
    polynomial_count = sum(row.get("polynomial") is not None for row in rows)
    historical = historical_entries(register)
    historical_count = (
        len(historical) if "historical_entries" in register else len(superseded_notes(register))
    )
    return (
        f"The register covers **{len(rows)}** values, from $n=1$ through $n={len(rows)}$. "
        f"It records **{polynomial_count}** current polynomials: "
        f"{totals.get('integer', 0)} integer, {totals.get('rational', 0)} rational, "
        f"{totals.get('closed-form', 0)} nonrational closed-form, and "
        f"{totals.get('minimal-polynomial', 0)} polynomial-only values. "
        f"There are **{totals.get('degree-only', 0)}** degree-only and "
        f"**{totals.get('numeric-only', 0)}** numeric-only current values. "
        f"Separately, it retains **{historical_count}** historical polynomial-side "
        "pairs from the compared primary sources. These rows do not change the current "
        "totals above.\n"
    )


def sources_markdown(register: Mapping[str, Any]) -> str:
    """Print every source identity carried by the register, including nested KKT data."""
    sources = _as_mapping(register.get("sources"), "register.sources")
    rows: list[tuple[str, object]] = []

    def flatten(prefix: str, value: object) -> None:
        if isinstance(value, dict):
            for key, nested in value.items():
                flatten(f"{prefix}.{key}" if prefix else str(key), nested)
            return
        rows.append((prefix, value))

    flatten("", sources)
    lines = [
        "| Register source field | Recorded identity |",
        "| --- | --- |",
    ]
    lines.extend(f"| `{name}` | `{_table_text(value)}` |" for name, value in rows)
    return "\n".join(lines) + "\n"


def exact_forms_markdown(register: Mapping[str, Any]) -> str:
    lines = [
        "| $n$ | Register state | Exact side of the recorded packing | Degree | Claim |",
        "| ---: | --- | --- | ---: | --- |",
    ]
    for entry in entries(register):
        exact = entry.get("exact_form_latex")
        if exact is None:
            continue
        lines.append(
            "| "
            + " | ".join(
                (
                    str(entry["n"]),
                    _table_text(entry.get("state")),
                    _math(exact),
                    _table_text(entry.get("degree")),
                    _claim(entry),
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def closed_form_families_markdown(register: Mapping[str, Any]) -> str:
    """Group every nonrational closed form by the radical field visible in the register."""
    families: dict[str, list[int]] = {
        r"Quadratic forms in $\mathbb{Q}(\sqrt{2})$": [],
        r"Nested quartic forms over $\mathbb{Q}(\sqrt{2})$": [],
        r"Quadratic forms in $\mathbb{Q}(\sqrt{7})$": [],
    }
    for entry in entries(register):
        if entry.get("state") != "closed-form":
            continue
        expression = str(entry.get("exact_form"))
        if "sqrt(1 + sqrt(2))" in expression:
            family = r"Nested quartic forms over $\mathbb{Q}(\sqrt{2})$"
        elif "sqrt(2)" in expression:
            family = r"Quadratic forms in $\mathbb{Q}(\sqrt{2})$"
        elif "sqrt(7)" in expression:
            family = r"Quadratic forms in $\mathbb{Q}(\sqrt{7})$"
        else:
            family = "Other recorded closed forms"
            families.setdefault(family, [])
        families[family].append(int(entry["n"]))
    lines = [
        "| Family | Count | Values of $n$ |",
        "| --- | ---: | --- |",
    ]
    lines.extend(
        f"| {family} | {len(numbers)} | {', '.join(map(str, numbers)) or '—'} |"
        for family, numbers in families.items()
        if numbers
    )
    return "\n".join(lines) + "\n"


def _irreducibility(checks: Mapping[str, Any]) -> str:
    certificate = checks.get("irreducible")
    if certificate is None:
        return "—"
    record = _as_mapping(certificate, "irreducibility certificate")
    method = str(record.get("method", "unknown"))
    primes = _as_sequence(record.get("primes", []), "irreducibility primes")
    if primes:
        method += " (primes " + ", ".join(map(str, primes)) + ")"
    return _table_text(method)


def _root_check(checks: Mapping[str, Any]) -> str:
    root = checks.get("root")
    if root is None:
        return "—"
    record = _as_mapping(root, "root check")
    interval = _as_sequence(record.get("interval"), "root interval")
    if len(interval) != 2:
        raise ExactSideValuesPaperError("a root interval must have two endpoints")
    verdicts = []
    if record.get("unique") is True:
        verdicts.append("one real root")
    if record.get("contains_recorded_side") is True:
        verdicts.append("contains recorded side")
    source_index = record.get("source_index")
    if source_index is not None:
        index = _as_mapping(source_index, "source Root index")
        stated = _table_text(index.get("stated"))
        counted = index.get("counted")
        if counted is None:
            verdicts.append(f"source Root index {stated}, not independently counted")
        else:
            verdicts.append(
                f"source Root index {stated}, independently counted as {_table_text(counted)}"
            )
    return _table_text(", ".join(verdicts) + f" in [{interval[0]}, {interval[1]}]")


def checks_markdown(register: Mapping[str, Any]) -> str:
    lines = [
        (
            "| $n$ | Side / lower bound | State / degree / height | "
            "Source / exact decimal | Galois data | Irreducibility | Isolated root | "
            "Record / KKT agreement | Notes | Claim |"
        ),
        "| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in entries(register):
        polynomial = entry.get("polynomial")
        if polynomial is None:
            continue
        poly = _as_mapping(polynomial, f"n={entry['n']} polynomial")
        checks = _as_mapping(entry.get("checks"), f"n={entry['n']} checks")
        side = _as_mapping(entry.get("side"), f"n={entry['n']} side")
        lower = _as_mapping(entry.get("lower"), f"n={entry['n']} lower")
        kkt = entry.get("kkt")
        if kkt is None:
            kkt_text = "no independent KKT value"
        else:
            kkt_record = _as_mapping(kkt, f"n={entry['n']} kkt")
            kkt_text = (
                f"KKT {_table_text(kkt_record.get('value'))} "
                f"({_table_text(kkt_record.get('status'))})"
            )
        agreement = (
            f"{_table_text(checks.get('recorded_agreement_digits'))} / "
            f"{_table_text(checks.get('kkt_agreement_digits'))} digits; {kkt_text}"
        )
        galois = checks.get("galois")
        if isinstance(galois, dict):
            galois_text = (
                f"{galois.get('group')}, order {galois.get('order')}, "
                f"solvable {str(galois.get('solvable')).lower()}"
            )
        else:
            galois_text = "—"
        notes = (
            "; ".join(
                _table_text(note.get("text"))
                for note in (
                    _as_mapping(raw, f"n={entry['n']} note")
                    for raw in _as_sequence(entry.get("notes"), f"n={entry['n']} notes")
                )
            )
            or "—"
        )
        occurrence_labels = "<br>".join(
            _source_label(_as_mapping(raw, f"n={entry['n']} source occurrence"))
            for raw in _as_sequence(
                entry.get("source_occurrences", []),
                f"n={entry['n']} source occurrences",
            )
        )
        source_identity = (
            f"{_table_text(entry.get('algebraic_source'))}; "
            f"{_table_text(checks.get('catalogue'))}; "
            f"{_table_text(checks.get('decimal'))}"
        )
        if occurrence_labels:
            source_identity += f"<br>{occurrence_labels}"
        lines.append(
            "| "
            + " | ".join(
                (
                    str(entry["n"]),
                    f"{_table_text(side.get('value'))} / {_table_text(lower.get('value'))}",
                    (
                        f"{_table_text(entry.get('state'))} / "
                        f"{_table_text(entry.get('degree'))} / "
                        f"{_table_text(poly.get('height_digits'))} digits"
                    ),
                    source_identity,
                    _table_text(galois_text),
                    _irreducibility(checks),
                    _root_check(checks),
                    agreement,
                    notes,
                    _claim(entry),
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def missing_values_markdown(register: Mapping[str, Any]) -> str:
    lines = [
        "| $n$ | State | Recorded side | Independent KKT value | Route | Bead |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for entry in entries(register):
        if entry.get("state") not in {"degree-only", "numeric-only"}:
            continue
        notes = tuple(
            _as_mapping(note, f"n={entry['n']} note")
            for note in _as_sequence(entry.get("notes"), f"n={entry['n']} notes")
        )
        routes = [
            note
            for note in notes
            if note.get("kind")
            in {"route", "missing-polynomial-text", "relation-search-negative"}
        ]
        if not routes:
            routes = [{"text": "No route is recorded.", "bead": None}]
        side = _as_mapping(entry.get("side"), f"n={entry['n']} side")
        kkt_value = "—"
        if entry.get("kkt") is not None:
            kkt = _as_mapping(entry["kkt"], f"n={entry['n']} kkt")
            kkt_value = f"{_table_text(kkt.get('value'))} ({_table_text(kkt.get('status'))})"
        for index, route in enumerate(routes):
            lines.append(
                "| "
                + " | ".join(
                    (
                        str(entry["n"]) if index == 0 else "",
                        _table_text(entry.get("state")) if index == 0 else "",
                        _table_text(side.get("value")) if index == 0 else "",
                        kkt_value if index == 0 else "",
                        _table_text(route.get("text")),
                        _table_text(route.get("bead")),
                    )
                )
                + " |"
            )
    return "\n".join(lines) + "\n"


def superseded_notes(
    register: Mapping[str, Any],
) -> tuple[tuple[Mapping[str, Any], Mapping[str, Any]], ...]:
    found = []
    for entry in entries(register):
        for raw_note in _as_sequence(entry.get("notes"), f"n={entry['n']} notes"):
            note = _as_mapping(raw_note, f"n={entry['n']} note")
            if note.get("kind") == "superseded-catalogue-polynomial":
                found.append((entry, note))
    return tuple(found)


def superseded_summary_markdown(register: Mapping[str, Any]) -> str:
    lines = [
        "| $n$ | Superseded degree | Historical side | Current side | Exact checks |",
        "| ---: | ---: | --- | --- | --- |",
    ]
    for entry, note in superseded_notes(register):
        side = note.get("side")
        historical = (
            _table_text(side.get("value")) if isinstance(side, dict) else _table_text(side)
        )
        current = _as_mapping(entry.get("side"), f"n={entry['n']} side")
        checks = note.get("checks")
        if isinstance(checks, dict):
            check_text = "; ".join(
                (
                    f"source identity: {checks.get('catalogue')}",
                    f"exact decimal: {checks.get('decimal')}",
                    f"irreducible: {_irreducibility(checks).replace('\\|', '|')}",
                    f"root: {_root_check(checks).replace('\\|', '|')}",
                    f"record agreement: {checks.get('recorded_agreement_digits')} digits",
                )
            )
        else:
            check_text = _table_text(note.get("text"))
        lines.append(
            "| "
            + " | ".join(
                (
                    str(entry["n"]),
                    _table_text(note.get("degree")),
                    historical,
                    _table_text(current.get("value")),
                    _table_text(check_text),
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def _source_label(source: Mapping[str, Any]) -> str:
    locator = _as_mapping(source.get("locator"), "historical source locator")
    location = str(source.get("path"))
    if locator.get("line") is not None:
        location += f":{locator['line']}"
        if locator.get("line_end") not in {None, locator.get("line")}:
            location += f"-{locator['line_end']}"
    kind = _table_text(source.get("kind"))
    url = source.get("url")
    if url is None:
        return f"`{_table_text(location)}` ({kind})"
    return f"[{kind}]({url}); `{_table_text(location)}`"


def _historical_checks(entry: Mapping[str, Any]) -> str:
    record = _as_mapping(entry.get("checks"), "historical checks")
    details = [
        f"source identity {_table_text(record.get('catalogue'))}",
        f"decimal {_table_text(record.get('decimal'))}",
        f"irreducibility {_irreducibility(record).replace('\\|', '|')}",
        f"root {_root_check(record).replace('\\|', '|')}",
        (
            "printed-side agreement "
            f"{_table_text(record.get('recorded_agreement_digits'))} digits"
        ),
    ]
    return "; ".join(details)


def historical_summary_markdown(register: Mapping[str, Any]) -> str:
    """Summarize historical pairs without comparing them with current KKT values."""
    historical = historical_entries(register)
    if "historical_entries" not in register:
        return superseded_summary_markdown(register)
    lines = [
        (
            "| $n$ | Historical side | Degree | Kind / current side | Source status | "
            "Retained source occurrences | Exact checks |"
        ),
        "| ---: | --- | ---: | --- | --- | --- | --- |",
    ]
    for entry in historical:
        n = int(entry["n"])
        relation = _table_text(entry.get("kind"))
        if entry.get("current_side") is not None:
            relation += f"; current side {_table_text(entry.get('current_side'))}"
        statuses = _as_sequence(
            entry.get("source_statuses"), f"historical n={n} source statuses"
        )
        sources = tuple(
            _as_mapping(item, f"historical n={n} source")
            for item in _as_sequence(entry.get("sources"), f"historical n={n} sources")
        )
        labels = "<br>".join(_source_label(item) for item in sources)
        lines.append(
            "| "
            + " | ".join(
                (
                    str(n),
                    _table_text(entry.get("side")),
                    _table_text(entry.get("degree")),
                    relation,
                    ", ".join(_table_text(value) for value in statuses) or "—",
                    labels or "—",
                    _table_text(_historical_checks(entry)),
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def _coefficients(
    polynomial: Mapping[str, Any], *, degree: int, context: str
) -> tuple[int, ...]:
    raw = _as_sequence(polynomial.get("coefficients"), f"{context} coefficients")
    try:
        coefficients = tuple(int(value) for value in raw)
    except (TypeError, ValueError) as error:
        raise ExactSideValuesPaperError(f"{context}: coefficients must be integers") from error
    if len(coefficients) != degree + 1 or not coefficients or coefficients[0] == 0:
        raise ExactSideValuesPaperError(
            f"{context}: degree {degree} requires {degree + 1} coefficients and a nonzero lead"
        )
    return coefficients


def _term(coefficient: int, power: int, *, first: bool) -> str:
    sign = "-" if coefficient < 0 else ("" if first else "+")
    magnitude = abs(coefficient)
    factor = "" if magnitude == 1 and power else str(magnitude)
    if power == 0:
        variable = ""
    elif power == 1:
        variable = "s"
    else:
        variable = f"s^{{{power}}}"
    return f"{sign} {factor}{variable}".strip()


def _term_chunks(coefficients: Sequence[int]) -> tuple[str, ...]:
    degree = len(coefficients) - 1
    terms = [
        _term(coefficient, degree - index, first=False)
        for index, coefficient in enumerate(coefficients)
        if coefficient
    ]
    if not terms:
        return ("0",)
    terms[0] = terms[0].removeprefix("+ ")
    chunks: list[str] = []
    current: list[str] = []
    for term in terms:
        if current and (
            len(current) >= TERMS_PER_DISPLAY
            or len(" ".join((*current, term))) > DISPLAY_CHARACTER_BUDGET
        ):
            chunks.append(" ".join(current))
            current = []
        current.append(term)
    if current:
        chunks.append(" ".join(current))
    return tuple(chunks)


def _expanded_polynomial(name: str, coefficients: Sequence[int]) -> str:
    chunks = _term_chunks(coefficients)
    displays = []
    for index, chunk in enumerate(chunks):
        prefix = f"{name}(s) ={{}}" if index == 0 else rf"\phantom{{{name}(s) ={{}}}}"
        suffix = " = 0" if index == len(chunks) - 1 else ""
        displays.append(f"$$\n{prefix} {chunk}{suffix}\n$$")
    return "\n\n".join(displays)


def _coefficient_table(name: str, coefficients: Sequence[int]) -> str:
    degree = len(coefficients) - 1
    lines = [
        "The polynomial is",
        "",
        f"$$\n{name}(s)=\\sum_{{k=0}}^{{{degree}}} a_k s^k=0.\n$$",
        "",
        (
            "The complete coefficient vector follows from the leading coefficient to the "
            "constant term."
        ),
        "",
        "| Power $k$ | Coefficient $a_k$ |",
        "| ---: | --- |",
    ]
    lines.extend(
        f"| {degree - index} | <code>{coefficient}</code> |"
        for index, coefficient in enumerate(coefficients)
    )
    return "\n".join(lines)


def polynomial_markdown(
    name: str, polynomial: Mapping[str, Any], *, degree: int, context: str
) -> str:
    coefficients = _coefficients(polynomial, degree=degree, context=context)
    widest = max(len(str(abs(value))) for value in coefficients)
    if degree >= COEFFICIENT_TABLE_DEGREE or widest >= COEFFICIENT_TABLE_DIGITS:
        return _coefficient_table(name, coefficients)
    return _expanded_polynomial(name, coefficients)


def current_polynomials_markdown(register: Mapping[str, Any]) -> str:
    sections = []
    for entry in entries(register):
        polynomial = entry.get("polynomial")
        if polynomial is None:
            continue
        n = int(entry["n"])
        degree = int(entry["degree"])
        poly = _as_mapping(polynomial, f"n={n} polynomial")
        checks = _as_mapping(entry.get("checks"), f"n={n} checks")
        occurrence_labels = tuple(
            _source_label(_as_mapping(raw, f"n={n} source occurrence"))
            for raw in _as_sequence(
                entry.get("source_occurrences", []), f"n={n} source occurrences"
            )
        )
        source_line = (
            " Retained source occurrences: " + "; ".join(occurrence_labels) + "."
            if occurrence_labels
            else ""
        )
        sections.append(
            "\n".join(
                (
                    f"### Current polynomial for $n={n}$",
                    "",
                    (
                        f"Degree {degree}; source "
                        f"`{_table_text(entry.get('algebraic_source'))}`; irreducibility "
                        f"`{_irreducibility(checks).replace('\\|', '|')}`; {_claim(entry)}."
                        f"{source_line}"
                    ),
                    "",
                    polynomial_markdown(f"P_{{{n}}}", poly, degree=degree, context=f"n={n}"),
                )
            )
        )
    return "\n\n".join(sections) + "\n"


def superseded_polynomials_markdown(register: Mapping[str, Any]) -> str:
    sections = []
    for entry, note in superseded_notes(register):
        n = int(entry["n"])
        degree = int(note["degree"])
        if note.get("polynomial") is None:
            sections.append(
                f"### Superseded polynomial for $n={n}$\n\n"
                "The register identifies this historical polynomial but does not retain its "
                "coefficients in this revision."
            )
            continue
        polynomial = _as_mapping(note["polynomial"], f"n={n} superseded polynomial")
        sections.append(
            "\n".join(
                (
                    f"### Superseded polynomial for $n={n}$",
                    "",
                    _table_text(note.get("text")),
                    "",
                    polynomial_markdown(
                        f"Q_{{{n}}}",
                        polynomial,
                        degree=degree,
                        context=f"n={n} superseded",
                    ),
                )
            )
        )
    return "\n\n".join(sections) + "\n"


def _historical_kind_claim(entry: Mapping[str, Any]) -> str:
    kind = entry.get("kind")
    if kind == "superseded":
        return "This source side is superseded by the current recorded side."
    if kind == "outside-frontier":
        return r"This source fact lies outside the current $n=1\ldots324$ frontier."
    if kind == "source-invalid":
        return (
            "The equation may pass its algebraic checks, but the source row does not "
            "furnish a valid packing upper bound."
        )
    if kind == "unreconciled-source":
        return (
            "The source fact is retained, but its relationship to the frontier is unresolved."
        )
    raise ExactSideValuesPaperError(f"unknown historical kind: {kind!r}")


def historical_attribution_markdown(entry: Mapping[str, Any], *, n: int) -> str:
    attribution = _as_mapping(entry.get("attribution"), f"historical n={n} attribution")
    dates = _as_sequence(
        attribution.get("date_mentions"), f"historical n={n} attribution dates"
    )
    source_text = _as_sequence(
        attribution.get("source_text"), f"historical n={n} attribution text"
    )
    lines = [
        "Attribution date mentions: "
        + (", ".join(f"`{_table_text(value)}`" for value in dates) or "none."),
        "",
        "Source attribution text:",
        "",
    ]
    if not source_text:
        lines.append(
            '<blockquote class="source-quote"><p><code>'
            "No attribution text was retained."
            "</code></p></blockquote>"
        )
    for text in source_text:
        cleaned = escape(str(text), quote=False).replace("\n", " ")
        lines.append(
            f'<blockquote class="source-quote"><p><code>{cleaned}</code></p></blockquote>'
        )
    return "\n".join(lines)


def historical_polynomials_markdown(register: Mapping[str, Any]) -> str:
    """Print every historical coefficient with attribution and source identity."""
    historical = historical_entries(register)
    if "historical_entries" not in register:
        return superseded_polynomials_markdown(register)
    if not historical:
        return "No historical polynomial-side pairs are recorded.\n"
    sections: list[str] = []
    seen: dict[int, int] = {}
    for entry in historical:
        n = int(entry["n"])
        seen[n] = seen.get(n, 0) + 1
        degree = int(entry["degree"])
        side = _table_text(entry.get("side"))
        polynomial = _as_mapping(entry.get("polynomial"), f"historical n={n} polynomial")
        sources = tuple(
            _as_mapping(raw, f"historical n={n} source")
            for raw in _as_sequence(entry.get("sources"), f"historical n={n} sources")
        )
        source_lines = []
        for source in sources:
            flags = _as_sequence(
                source.get("source_flags", []), f"historical n={n} source flags"
            )
            flag_text = ", ".join(_table_text(flag) for flag in flags) or "none"
            source_lines.append(f"- {_source_label(source)}; source flags: {flag_text}.")
        statuses = _as_sequence(
            entry.get("source_statuses"), f"historical n={n} source statuses"
        )
        current_side = entry.get("current_side")
        current_text = (
            "No current-frontier side applies."
            if current_side is None
            else f"The current register side is `{_table_text(current_side)}`."
        )
        identity_lines = []
        for field, label in (
            ("algebraic_source", "Polynomial origin"),
            ("exact_form", "Retained source expression"),
        ):
            value = entry.get(field)
            if value is not None:
                literal = escape(str(value), quote=False)
                identity_lines.append(f"{label}: <code>{literal}</code>.")
        bead = entry.get("bead")
        bead_text = "none" if bead is None else f"`{_table_text(bead)}`"
        name = f"H_{{{n},{seen[n]}}}"
        sections.append(
            "\n".join(
                (
                    f"### Historical polynomial for $n={n}$ at side `{side}`",
                    "",
                    (
                        f"Kind: `{_table_text(entry.get('kind'))}`. "
                        f"{_historical_kind_claim(entry)} {current_text}"
                    ),
                    "",
                    (
                        "Source statuses: "
                        + (", ".join(f"`{_table_text(value)}`" for value in statuses) or "none")
                        + f". Route bead: {bead_text}."
                    ),
                    "",
                    *identity_lines,
                    "",
                    f"Exact checks: {_historical_checks(entry)}.",
                    "",
                    "Retained source occurrences:",
                    "",
                    *(source_lines or ["- No retained source occurrence."]),
                    "",
                    historical_attribution_markdown(entry, n=n),
                    "",
                    polynomial_markdown(
                        name,
                        polynomial,
                        degree=degree,
                        context=f"historical n={n} side={side}",
                    ),
                )
            )
        )
    return "\n\n".join(sections) + "\n"


def generated_sections(register: Mapping[str, Any]) -> dict[str, str]:
    return {
        "REGISTER_SUMMARY": summary_markdown(register),
        "REGISTER_SOURCES": sources_markdown(register),
        "CLOSED_FORM_FAMILIES": closed_form_families_markdown(register),
        "EXACT_FORMS": exact_forms_markdown(register),
        "CHECK_SUMMARIES": checks_markdown(register),
        "MISSING_VALUES": missing_values_markdown(register),
        "HISTORICAL_SUMMARY": historical_summary_markdown(register),
        "HISTORICAL_POLYNOMIALS": historical_polynomials_markdown(register),
        "CURRENT_POLYNOMIALS": current_polynomials_markdown(register),
    }


def render_all_figures() -> dict[str, str]:
    """The catalogue is entirely textual and has no retained figure slots."""
    return {}


def render_all_facts() -> dict[str, str]:
    """All generated facts come directly from the register passed to ``render``."""
    return {}


def _fill(
    template: str,
    values: Mapping[str, str],
    *,
    source: Path,
    strict: bool = False,
) -> str:
    if strict:
        unused = [key for key in values if "{{" + key + "}}" not in template]
        if unused:
            raise ExactSideValuesPaperError(
                f"{source.name}: values with no placeholder: {sorted(unused)}"
            )
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    remaining = LEFTOVER_SLOT.findall(rendered)
    if remaining:
        raise ExactSideValuesPaperError(
            f"{source.name}: unresolved placeholders: {sorted(set(remaining))}"
        )
    return rendered


def _repository_links(markdown: str, *, source: Path, revision: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ExactSideValuesPaperError(
            "repository-link revision must be a full lowercase Git commit ID"
        )

    def pin(url: str) -> str:
        path_text, mark, fragment = url.partition("#")
        target = (source.parent / path_text).resolve()
        if not target.is_relative_to(REPO):
            raise ExactSideValuesPaperError(
                f"{source.name}: link escapes repository: {path_text}"
            )
        if not target.is_file():
            raise ExactSideValuesPaperError(
                f"{source.name}: linked source does not exist: {path_text}"
            )
        path = target.relative_to(REPO).as_posix()
        result = f"https://github.com/jlevy/squares/blob/{revision}/{path}"
        return result + ("#" + fragment if mark else "")

    markdown = RELATIVE_LINK.sub(
        lambda match: match.group("start") + pin(match.group("url")) + match.group("end"),
        markdown,
    )
    markdown = RELATIVE_REFERENCE.sub(
        lambda match: match.group("start") + pin(match.group("url")), markdown
    )
    return RELATIVE_ANCHOR.sub(
        lambda match: (
            match.group("start")
            + escape(pin(match.group("url")), quote=True)
            + match.group("end")
        ),
        markdown,
    )


def link_revision() -> str:
    found = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    revision = found.stdout.strip()
    if found.returncode != 0 or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise SystemExit("git names no HEAD here: give --revision, a full commit ID")
    return revision


def expanded_markdown(
    source: str,
    *,
    register: Mapping[str, Any],
    revision: str,
    article: Path = ARTICLE,
) -> str:
    source = paper_front.fill(source, FRONT)
    source = _fill(source, generated_sections(register), source=article, strict=True)
    return _repository_links(source, source=article, revision=revision)


def page_meta(*, complete: bool = False) -> PageMeta:
    return PageMeta(
        name=TITLE,
        description=ARCHIVE_DESCRIPTION if complete else DESCRIPTION,
        path=COMPLETE_PATH if complete else SITE_PATH,
        kind="article",
        published=paper_front.iso_date(FIRST_PUBLISHED),
        modified=paper_front.iso_date(paper_front.revised(FRONT)),
    )


def _script(text: str, *, name: str) -> str:
    if "</script" in text.lower():
        raise ExactSideValuesPaperError(f"{name} closes its inline script")
    return text


def math_scripts(static: Path) -> dict[str, str]:
    return {
        "KATEX_JS": _script(
            render_n11_lower_bounds_explainer.katex_js(static), name="the math pipeline"
        ),
        "SITE_MATH": _script(MATH_SCRIPT.read_text(encoding="utf-8"), name=MATH_SCRIPT.name),
    }


def render(
    source: str,
    *,
    register: Mapping[str, Any] | None = None,
    revision: str,
    article: Path = ARTICLE,
    figures: Mapping[str, str] | None = None,
    facts: Mapping[str, str] | None = None,
) -> tuple[str, str]:
    """Return the self-contained HTML and published Markdown editions."""
    from kpress.format.markdown import parse_markdown  # noqa: PLC0415

    if figures or facts:
        raise ExactSideValuesPaperError("the exact-values paper has no figure or fact slots")
    register = register or load_register()
    expanded = expanded_markdown(source, register=register, revision=revision, article=article)
    document = parse_markdown(expanded, title=TITLE, trust_mode="trusted", math="auto")
    errors = [item.message for item in document.diagnostics if item.severity == "error"]
    if errors:
        raise ExactSideValuesPaperError(
            f"{article.name}: KPress refused the article: {'; '.join(errors)}"
        )
    static = render_n11_lower_bounds_explainer.kpress_static()
    values = {
        "PAGE_HEAD": head_tags(page_meta(complete=True)),
        "KPRESS_CSS": render_n11_lower_bounds_explainer.kpress_css(static),
        "KATEX_CSS": render_n11_lower_bounds_explainer.katex_css(static)
        if document.has_math
        else "",
        "RELATION_CSS": render_n11_lower_bounds_explainer.relation_face_css(static),
        "PAPER_TYPE_CSS": PAPER_TYPE_CSS.read_text(encoding="utf-8"),
        **render_n11_lower_bounds_explainer.publication_layer(),
        "PAPER_CSS": STYLE.read_text(encoding="utf-8"),
        "SITE_FAVICON": favicon_html(inline=True),
        "SITE_NAV_CSS": SITE_NAV_CSS.read_text(encoding="utf-8"),
        "SITE_NAV": nav_html("papers", root=SITE_ROOT),
        "COLOPHON": colophon_lines(edition=""),
        "SITE_EMBED": EMBED_SCRIPT.read_text(encoding="utf-8"),
        "SITE_THEME": THEME_SCRIPT.read_text(encoding="utf-8"),
        "THEME_BOOTSTRAP": render_n11_lower_bounds_explainer.theme_bootstrap(static),
        "BODY_HTML": document.html,
        **(math_scripts(static) if document.has_math else {"KATEX_JS": "", "SITE_MATH": ""}),
        "DIAGRAM_LABEL_SCRIPT": "",
    }
    shell = SHELL.read_text(encoding="utf-8")
    page = _fill(shell, values, source=SHELL, strict=True)
    render_n11_lower_bounds_explainer.assert_self_contained(page)
    return page, paper_front.published(expanded, FRONT)


def render_browser(*, revision: str | None = None) -> str:
    """The browser shell ships no mathematical payload or embedded font distribution."""
    static = render_n11_lower_bounds_explainer.kpress_static()
    values = {
        "PAGE_HEAD": head_tags(page_meta()),
        "SITE_FAVICON": favicon_html(root=SITE_ROOT),
        "SITE_NAV_CSS": SITE_NAV_CSS.read_text(encoding="utf-8"),
        "SITE_NAV": nav_html("papers", root=SITE_ROOT),
        "SITE_THEME": THEME_SCRIPT.read_text(encoding="utf-8"),
        "THEME_BOOTSTRAP": render_n11_lower_bounds_explainer.theme_bootstrap(static),
        "COLOPHON": colophon_lines(edition=""),
        "BROWSER_VERSION": escape(FRONT.version),
        "REGISTER_SOURCE_URL": (
            f"https://github.com/jlevy/squares/blob/{revision or link_revision()}/"
            "packing/frontier/exact-values.json"
        ),
        "BROWSER_STYLE": BROWSER_STYLE.read_text(encoding="utf-8"),
        "BROWSER_INDEX_URL": escape(exact_catalogue.INDEX_PATH.as_posix(), quote=True),
        "BROWSER_SCRIPT_URL": escape(BROWSER_SCRIPT_NAME, quote=True),
        "COMPLETE_HTML_URL": escape(Path(COMPLETE_PATH).name, quote=True),
        "COMPLETE_MARKDOWN_URL": escape(Path(paper_path(SLUG, ".md")).name, quote=True),
        "COMPLETE_PDF_URL": escape(Path(paper_path(SLUG, ".pdf")).name, quote=True),
    }
    return _fill(
        BROWSER_SHELL.read_text(encoding="utf-8"), values, source=BROWSER_SHELL, strict=True
    )


def output_files(
    site: Path,
    html: str,
    markdown: str,
    *,
    register: Mapping[str, Any],
    revision: str | None = None,
) -> dict[Path, str]:
    """Plan the entire deterministic export, publishing the browser after its dependencies."""
    return {
        site / COMPLETE_PATH: html,
        site / paper_path(SLUG, ".md"): markdown,
        site / Path(SITE_PATH).parent / BROWSER_SCRIPT_NAME: BROWSER_SCRIPT.read_text(
            encoding="utf-8"
        ),
        **exact_catalogue.output_files(register, papers=site / Path(SITE_PATH).parent),
        site / SITE_PATH: render_browser(revision=revision),
    }


def _payload_files(site: Path) -> tuple[Path, ...]:
    """The generated data directory is owned by this exporter; never follow links."""
    root = site / Path(SITE_PATH).parent / exact_catalogue.DATA_DIRECTORY
    if root.is_symlink():
        raise ExactSideValuesPaperError(f"generated payload directory is a symlink: {root}")
    if not root.exists():
        return ()
    if not root.is_dir():
        raise ExactSideValuesPaperError(
            f"generated payload directory is not a directory: {root}"
        )

    def failed(error: OSError) -> None:
        raise error

    files: list[Path] = []
    for directory, directories, names in root.walk(on_error=failed, follow_symlinks=False):
        for name in (*directories, *names):
            path = directory / name
            if path.is_symlink():
                raise ExactSideValuesPaperError(f"generated payload path is a symlink: {path}")
        files.extend(directory / name for name in names)
    return tuple(sorted(files))


def _publication_day() -> datetime:
    return datetime.strptime(paper_front.revised(FRONT), "%B %d, %Y")  # noqa: DTZ007


def _print_pdf(html_path: Path, pdf_path: Path) -> None:
    from playwright.sync_api import expect, sync_playwright  # noqa: PLC0415

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = None
        try:
            page = browser.new_page()
            page.goto(html_path.as_uri(), wait_until="networkidle")
            page.evaluate(ABSOLUTE_LINKS, SITE_URL + COMPLETE_PATH)
            page.emulate_media(media="print")
            content_width = page.evaluate(PRINT_CONTENT_WIDTH)
            if not isinstance(content_width, int | float) or not 0 < content_width <= 816:
                raise ExactSideValuesPaperError("invalid Letter print content width")
            # A print-media viewport excludes @page margins, just as the physical page
            # content box does. Preflight at that width before Chromium paginates.
            page.set_viewport_size({"width": int(content_width), "height": 1056})
            hosts = page.locator(".kpress-math")
            if hosts.count() == 0:
                raise ExactSideValuesPaperError("the paper has no typeset math")
            page.evaluate(TYPESET_ALL)
            try:
                expect(page.locator(".kpress-math:not(:has(.katex))")).to_have_count(
                    0, timeout=MATH_WAIT_MS
                )
            except AssertionError as error:
                raise ExactSideValuesPaperError("the paper has unrendered math") from error
            if page.locator(".katex-error, math merror").count():
                raise ExactSideValuesPaperError("the paper contains a math rendering error")
            _await_print_fonts(page)  # pyright: ignore[reportArgumentType]
            fit = page.evaluate(PRINT_MATH_FIT)
            if fit["checked"] != page.locator(".kpress-math-display").count():
                raise ExactSideValuesPaperError("print math fit check missed a display")
            if fit["overflows"]:
                raise ExactSideValuesPaperError(
                    "paper math exceeds its print column: " + json.dumps(fit["overflows"][:5])
                )
            drawn = page.pdf(format="Letter", prefer_css_page_size=True, print_background=True)
            write_bytes_atomic(pdf_path, dated(drawn, _publication_day().date()))
        finally:
            if page is not None:
                page.close()
            browser.close()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--site",
        type=Path,
        default=SITE,
        help="the site's root; the paper is written under papers/ in it",
    )
    parser.add_argument("--revision", default=None, help="full Git commit for source links")
    parser.add_argument(
        "--pdf", action="store_true", help="also print the complete HTML archive with KPress"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare browser, complete archive, and every lazy payload",
    )
    args = parser.parse_args(argv)
    register = load_register()
    revision = args.revision or link_revision()
    html, markdown = render(
        ARTICLE.read_text(encoding="utf-8"), register=register, revision=revision
    )
    site = args.site.resolve()
    outputs = output_files(site, html, markdown, register=register, revision=revision)
    extra = [path for path in _payload_files(site) if path not in outputs]
    if args.check:
        if args.pdf:
            parser.error("--check compares browser/archive outputs; use --pdf for a fresh PDF")
        stale = [
            path
            for path, content in outputs.items()
            if not path.is_file() or path.read_text(encoding="utf-8") != content
        ]
        stale.extend(extra)
        if stale:
            raise SystemExit(f"stale {SLUG} output: " + ", ".join(map(str, stale)))
        return 0
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary: Path | None = None
        try:
            with atomic_output_file(path) as temporary:
                temporary.write_text(content, encoding="utf-8")
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
    for path in extra:
        path.unlink()
    if args.pdf:
        _print_pdf(site / COMPLETE_PATH, site / paper_path(SLUG, ".pdf"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
