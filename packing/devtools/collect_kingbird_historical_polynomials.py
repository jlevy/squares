#!/usr/bin/env python3
"""Collect printed side polynomials from retained Kingbird history pages.

The comparison pages are the bounded corpus: their current captures cover the three
published ranges and preserve older, alternative, invalid, and current comparison rows.
Twelve locators in the thematic exact-solution pages add independent occurrences and
the one later count absent from those comparison pages.  The collector reads retained
text only; it never fetches SVG or HTML bytes.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from devtools.build_exact_values import ExactValuesError, polynomial_checks
from devtools.retained_data import read_retained_text
from sqpack import retained_json

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
REGISTER = ROOT / "frontier/exact-values.json"
DEFAULT_OUTPUT = (
    ROOT / "resources/web/kingbird-exact-side-facts-2026-10-07/facts/"
    "historical-polynomials.json"
)
SOURCE_SCOPE_KEYS = (
    "comparison_equation_rows",
    "supplemental_locator_rows",
    "decoded_source_rows",
    "unique_polynomial_side_pairs",
    "unparsed_source_rows",
    "coefficient_order",
    "deduplication_key",
)
SOURCE_ENTRY_KEYS = (
    "n",
    "historical_side",
    "degree",
    "coefficients",
    "source_statuses",
    "attribution",
    "occurrences",
)


class HistoricalPolynomialError(ValueError):
    """A retained row cannot be translated without guessing."""


@dataclass(frozen=True)
class Source:
    path: str
    url: str
    kind: str

    @property
    def absolute(self) -> Path:
        return REPO / self.path


@dataclass(frozen=True)
class SupplementalLocator:
    n: int
    source: Source
    polynomial_line: int
    side_line: int | None = None


@dataclass(frozen=True)
class ComparisonCell:
    n: int
    start_line: int
    end_line: int
    text: str


COMPARISON_SOURCES = (
    Source(
        "packing/resources/web/kingbird-squares-in-squares-compared.md",
        "https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html",
        "comparison-catalogue",
    ),
    Source(
        "packing/resources/web/kingbird-squares-in-squares-compared2.md",
        "https://kingbird.myphotos.cc/packing/squares_in_squares__compared2.html",
        "comparison-catalogue",
    ),
    Source(
        "packing/resources/web/kingbird-squares-in-squares-compared3.md",
        "https://kingbird.myphotos.cc/packing/squares_in_squares__compared3.html",
        "comparison-catalogue",
    ),
)
N2_SOURCE = Source(
    "packing/resources/web/kingbird-squares-in-squares-n2-n-1.md",
    "https://kingbird.myphotos.cc/packing/squares_in_squares__n%5E2-n-1.html",
    "thematic-exact-solution",
)
GOBEL_SQUARES_SOURCE = Source(
    "packing/resources/web/kingbird-squares-in-squares-gobel-squares.md",
    "https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_squares.html",
    "thematic-exact-solution",
)
GOBEL_STRIPS_SOURCE = Source(
    "packing/resources/web/kingbird-squares-in-squares-gobel-strips.md",
    "https://kingbird.myphotos.cc/packing/squares_in_squares__G%C3%B6bel_strips.html",
    "thematic-exact-solution",
)

# These are locators, not transcribed equations.  Every coefficient and decimal is read
# again from the retained article.  Eleven rows independently duplicate comparison-page
# mathematics; n=2135 extends the comparison pages' published range.
SUPPLEMENTAL_LOCATORS = (
    SupplementalLocator(19, N2_SOURCE, 60),
    SupplementalLocator(41, N2_SOURCE, 89),
    SupplementalLocator(71, N2_SOURCE, 141),
    SupplementalLocator(71, N2_SOURCE, 143),
    SupplementalLocator(109, N2_SOURCE, 177),
    SupplementalLocator(155, N2_SOURCE, 219),
    SupplementalLocator(209, N2_SOURCE, 265),
    SupplementalLocator(271, N2_SOURCE, 319),
    SupplementalLocator(202, GOBEL_STRIPS_SOURCE, 941, 938),
    SupplementalLocator(1765, GOBEL_SQUARES_SOURCE, 556, 555),
    SupplementalLocator(2043, GOBEL_STRIPS_SOURCE, 2390, 2389),
    SupplementalLocator(2135, GOBEL_STRIPS_SOURCE, 2428, 2427),
)

SECTION = re.compile(r"^([0-9]+)\.  $")
MATH = re.compile(r"(?<!\\)\$([^$]+)\$")
SIDE = re.compile(r"\\Nn\{([0-9]+(?:\.[0-9]+)?)\}")
DEGREE = re.compile(r"\{\}\^\{?\s*([0-9]+)\s*\}?")
POWER_TERM = re.compile(r"([+-]?)([0-9]*)s(?:\^(?:\{([0-9]+)\}|([0-9]+)))?")
INTEGER_TERM = re.compile(r"[+-]?[0-9]+")
CELL_SEPARATOR = re.compile(r"\s*\|\s*\|\s*")
EQUATION_END = re.compile(r"=\s*0\s*$")
MONTH = (
    r"January|February|March|April|May|June|July|August|September|October|"
    r"November|December"
)
DATE = re.compile(
    rf"(?:(?:early|late|mid)\s+)?(?:{MONTH})\s+(?:19|20)[0-9]{{2}}|"
    r"\b(?:19|20)[0-9]{2}\b"
)


def read_latex_integer_polynomial(expression: str) -> tuple[int, ...]:
    """Translate one printed integer polynomial in ``s`` to descending coefficients."""
    text = expression.strip().replace(" ", "")
    if not text.endswith("=0"):
        raise HistoricalPolynomialError("equation does not end in =0")
    text = text[:-2]
    if "\\" in text or "(" in text or ")" in text:
        raise HistoricalPolynomialError("coefficient is not a printed integer")
    if not text:
        raise HistoricalPolynomialError("empty polynomial")
    if text[0] not in "+-":
        text = "+" + text
    terms = re.findall(r"[+-][^+-]+", text)
    if "".join(terms) != text:
        raise HistoricalPolynomialError("unreadable term boundary")
    by_power: dict[int, int] = {}
    for term in terms:
        match = POWER_TERM.fullmatch(term)
        if match is not None:
            sign, magnitude, braced_power, plain_power = match.groups()
            coefficient = int(magnitude or "1") * (-1 if sign == "-" else 1)
            power = int(braced_power or plain_power or "1")
        elif INTEGER_TERM.fullmatch(term):
            coefficient = int(term)
            power = 0
        else:
            raise HistoricalPolynomialError(f"unreadable term: {term}")
        if power in by_power:
            raise HistoricalPolynomialError(f"power {power} is repeated")
        by_power[power] = coefficient
    degree = max(by_power, default=-1)
    if degree < 1:
        raise HistoricalPolynomialError("polynomial has no positive-degree term")
    coefficients = tuple(by_power.get(power, 0) for power in range(degree, -1, -1))
    if coefficients[0] == 0:
        raise HistoricalPolynomialError("leading coefficient is zero")
    return coefficients


def _integer_polynomials(line: str) -> list[tuple[str, tuple[int, ...]]]:
    found: list[tuple[str, tuple[int, ...]]] = []
    for expression in MATH.findall(line):
        if EQUATION_END.search(expression) is None or "s" not in expression:
            continue
        try:
            coefficients = read_latex_integer_polynomial(expression)
        except HistoricalPolynomialError:
            continue
        found.append((expression, coefficients))
    return found


def _source_metadata(source: Source, lines: list[str]) -> dict[str, Any]:
    header = " ".join(lines[:8])
    archived = re.search(r"\*\*Archived:\*\*\s*([^;]+)", header)
    digest = re.search(r"SHA-256 `([0-9a-f]{64})`", header)
    if digest is None:
        digest = re.search(r"`([0-9a-f]{64})`", header)
    return {
        "path": source.path,
        "url": source.url,
        "kind": source.kind,
        "archived": None if archived is None else archived.group(1).strip(),
        "retained_html_sha256": None if digest is None else digest.group(1),
    }


def _context(lines: list[str], index: int) -> str:
    selected = lines[max(0, index - 2) : min(len(lines), index + 4)]
    return _clean_context(selected)


def _clean_context(selected: list[str]) -> str:
    cleaned: list[str] = []
    for raw_line in selected:
        cleaned_line = re.sub(
            r"\$[^$]*=\s*0\$",
            "[printed polynomial]",
            raw_line,
        )
        cleaned_line = re.sub(r"\s+", " ", cleaned_line).strip()
        if cleaned_line and not cleaned_line.startswith("---|"):
            cleaned.append(cleaned_line)
    return " ".join(cleaned)


def _comparison_cells(lines: list[str]) -> list[ComparisonCell]:
    """Split a Pandoc-extracted comparison table into its actual source cells."""
    n: int | None = None
    parts: list[tuple[int, str]] = []
    cells: list[ComparisonCell] = []

    def finish() -> None:
        nonlocal parts
        if n is not None and any(text.strip() for _, text in parts):
            cells.append(
                ComparisonCell(
                    n=n,
                    start_line=parts[0][0],
                    end_line=parts[-1][0],
                    text="\n".join(text for _, text in parts),
                )
            )
        parts = []

    for line_number, line in enumerate(lines, start=1):
        section = SECTION.fullmatch(line)
        if section is not None:
            finish()
            n = int(section.group(1))
            continue
        if line.startswith("---|") or line.strip() == "* * *":
            finish()
            continue
        segments = CELL_SEPARATOR.split(line)
        parts.append((line_number, segments[0]))
        for segment in segments[1:]:
            finish()
            parts.append((line_number, segment))
    finish()
    return cells


def _flags(source_text: str) -> list[str]:
    lowered = source_text.lower()
    cues = {
        "invalid": "invalid",
        "fixed": "fixed",
        "did-not-set-record": "didn't set a record",
        "not-optimal": "not optimal",
        "alternative": "alternative",
        "rearrangement": "rearrangement",
        "best-known": "best known",
    }
    found = [label for label, phrase in cues.items() if phrase in lowered]
    if "set a record" in lowered and "didn't set a record" not in lowered:
        found.append("record-setting")
    return found


def _row(
    *,
    n: int,
    side: str,
    expression: str,
    coefficients: tuple[int, ...],
    source: Source,
    line: int,
    line_end: int | None,
    context: str,
    status_text: str,
) -> dict[str, Any]:
    degree_markers = [int(value) for value in DEGREE.findall(status_text)]
    degree = len(coefficients) - 1
    marker_matches = not degree_markers or degree in degree_markers
    if "\\sqrt" in status_text:
        marker_matches = marker_matches or any(degree == 2 * value for value in degree_markers)
    return {
        "n": n,
        "historical_side": side,
        "degree": degree,
        "coefficients": list(coefficients),
        "printed_equation": expression,
        "source": {
            "path": source.path,
            "url": source.url,
            "kind": source.kind,
            "locator": {
                "line": line,
                "line_end": line if line_end is None else line_end,
                "section": str(n),
            },
        },
        "attribution": {
            "source_text": context,
            "date_mentions": list(dict.fromkeys(DATE.findall(context))),
        },
        "source_flags": _flags(status_text),
        "degree_marker_matches": marker_matches,
    }


def _parse_comparison(source: Source) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    lines = source.absolute.read_text(encoding="utf-8").splitlines()
    rows: list[dict[str, Any]] = []
    unparsed: list[dict[str, Any]] = []
    for cell in _comparison_cells(lines):
        equations = [
            expression
            for expression in MATH.findall(cell.text)
            if EQUATION_END.search(expression) is not None
        ]
        if not equations:
            continue
        side_matches = SIDE.findall(cell.text)
        polynomials = _integer_polynomials(cell.text)
        if not side_matches or len(polynomials) != 1:
            unparsed.append(
                {
                    "source": source.path,
                    "line": cell.start_line,
                    "line_end": cell.end_line,
                    "section": cell.n,
                    "reason": (
                        f"sides={len(side_matches)}, integer_polynomials={len(polynomials)}"
                    ),
                    "source_text": _clean_context(cell.text.splitlines()),
                }
            )
            continue
        expression, coefficients = polynomials[0]
        expression_line = next(
            (
                line_number
                for line_number in range(cell.start_line, cell.end_line + 1)
                if expression in lines[line_number - 1]
            ),
            cell.start_line,
        )
        context = _clean_context(cell.text.splitlines())
        rows.append(
            _row(
                n=cell.n,
                side=side_matches[-1],
                expression=expression,
                coefficients=coefficients,
                source=source,
                line=expression_line,
                line_end=cell.end_line,
                context=context,
                status_text=cell.text,
            )
        )
    return rows, unparsed


def _supplemental_cell(locator: SupplementalLocator, lines: list[str]) -> tuple[str, int]:
    """The attribution-bearing source cell, excluding every neighboring equation."""
    if locator.source == N2_SOURCE:
        expression = lines[locator.polynomial_line - 1]
        matches = [
            cell
            for cell in _comparison_cells(lines)
            if cell.n == locator.n
            and cell.start_line <= locator.polynomial_line <= cell.end_line
            and any(equation in cell.text for equation, _ in _integer_polynomials(expression))
        ]
        if len(matches) != 1:
            raise HistoricalPolynomialError(f"n={locator.n}: ambiguous thematic source cell")
        return matches[0].text, matches[0].end_line
    text = "\n".join(lines)
    offset = sum(len(line) + 1 for line in lines[: locator.polynomial_line - 1])
    start = text.rfind("<td", 0, offset)
    end = text.find("</td>", offset)
    if start < 0 or end < 0 or "</td>" in text[start:offset]:
        raise HistoricalPolynomialError(
            f"n={locator.n}: polynomial has no enclosing table cell"
        )
    return text[start : end + len("</td>")], text.count("\n", 0, end) + 1


def _parse_supplemental(locator: SupplementalLocator) -> dict[str, Any]:
    lines = locator.source.absolute.read_text(encoding="utf-8").splitlines()
    index = locator.polynomial_line - 1
    line = lines[index]
    polynomials = _integer_polynomials(line)
    if len(polynomials) != 1:
        raise HistoricalPolynomialError(
            f"{locator.source.path}:{locator.polynomial_line}: expected one integer polynomial"
        )
    side_index = index if locator.side_line is None else locator.side_line - 1
    side_matches = SIDE.findall(lines[side_index])
    if len(side_matches) != 1:
        raise HistoricalPolynomialError(
            f"{locator.source.path}:{side_index + 1}: expected one side decimal"
        )
    expression, coefficients = polynomials[0]
    context, end_line = _supplemental_cell(locator, lines)
    return _row(
        n=locator.n,
        side=side_matches[0],
        expression=expression,
        coefficients=coefficients,
        source=locator.source,
        line=locator.polynomial_line,
        line_end=end_line,
        context=_clean_context(context.splitlines()),
        status_text=context,
    )


def _current_entries(path: Path = REGISTER) -> dict[int, dict[str, Any]]:
    document = json.loads(read_retained_text(path))
    return {int(entry["n"]): entry for entry in document["register"]["entries"]}


def _relationship(row: dict[str, Any], current: dict[int, dict[str, Any]]) -> dict[str, Any]:
    record = current.get(row["n"])
    if record is None:
        return {"status": "outside-current-register", "current_side": None}
    current_side = str(record["side"]["value"])
    polynomial = record.get("polynomial")
    current_coefficients = None
    if isinstance(polynomial, dict):
        current_coefficients = [int(value) for value in polynomial["coefficients"]]
    same_side = Decimal(row["historical_side"]) == Decimal(current_side)
    if same_side and row["coefficients"] == current_coefficients:
        status = "current"
    elif same_side:
        status = "alternative-polynomial-at-current-side"
    elif Decimal(row["historical_side"]) > Decimal(current_side):
        status = "superseded-or-weaker"
    else:
        status = "stronger-than-current-register"
    return {"status": status, "current_side": current_side}


def _key(row: dict[str, Any]) -> tuple[int, str, tuple[int, ...]]:
    return row["n"], row["historical_side"], tuple(row["coefficients"])


def collect_source() -> dict[str, Any]:
    """Read, translate, reconcile, and deduplicate the bounded retained corpus."""
    rows: list[dict[str, Any]] = []
    unparsed: list[dict[str, Any]] = []
    source_metadata: list[dict[str, Any]] = []
    comparison_equation_rows = 0
    for source in COMPARISON_SOURCES:
        lines = source.absolute.read_text(encoding="utf-8").splitlines()
        source_metadata.append(_source_metadata(source, lines))
        decoded, refused = _parse_comparison(source)
        comparison_equation_rows += len(decoded) + len(refused)
        rows.extend(decoded)
        unparsed.extend(refused)
    for source in (N2_SOURCE, GOBEL_SQUARES_SOURCE, GOBEL_STRIPS_SOURCE):
        lines = source.absolute.read_text(encoding="utf-8").splitlines()
        source_metadata.append(_source_metadata(source, lines))
    rows.extend(_parse_supplemental(locator) for locator in SUPPLEMENTAL_LOCATORS)

    current = _current_entries()
    grouped: dict[tuple[int, str, tuple[int, ...]], list[dict[str, Any]]] = {}
    for row in rows:
        grouped.setdefault(_key(row), []).append(row)
    entries: list[dict[str, Any]] = []
    for key in sorted(grouped, key=lambda item: (item[0], Decimal(item[1]), item[2])):
        occurrences = grouped[key]
        exemplar = occurrences[0]
        relationships = [_relationship(item, current) for item in occurrences]
        entries.append(
            {
                "n": exemplar["n"],
                "historical_side": exemplar["historical_side"],
                "degree": exemplar["degree"],
                "coefficients": exemplar["coefficients"],
                "relationship_to_current": relationships[0],
                "source_statuses": sorted(
                    {flag for item in occurrences for flag in item["source_flags"]}
                ),
                "attribution": {
                    "date_mentions": list(
                        dict.fromkeys(
                            date
                            for item in occurrences
                            for date in item["attribution"]["date_mentions"]
                        )
                    ),
                    "source_text": list(
                        dict.fromkeys(
                            item["attribution"]["source_text"] for item in occurrences
                        )
                    ),
                },
                "occurrences": [
                    {
                        "source": item["source"],
                        "printed_equation": item["printed_equation"],
                        "source_flags": item["source_flags"],
                        "degree_marker_matches": item["degree_marker_matches"],
                    }
                    for item in occurrences
                ],
                "validation": {
                    "status": "source-transcribed-unverified",
                    "reason": "exact polynomial check not run",
                },
            }
        )
    return {
        "format": "kingbird-historical-side-polynomials-v2",
        "scope": {
            "description": (
                "All rows with a printed '=0' equation in the three current retained "
                "Kingbird comparison catalogues, plus 12 thematic exact-solution locators."
            ),
            "comparison_equation_rows": comparison_equation_rows,
            "supplemental_locator_rows": len(SUPPLEMENTAL_LOCATORS),
            "decoded_source_rows": len(rows),
            "unique_polynomial_side_pairs": len(entries),
            "unparsed_source_rows": len(unparsed),
            "coefficient_order": "highest degree first",
            "deduplication_key": ["n", "historical_side", "coefficients"],
            "translation_notes": [
                "Only integer univariate polynomials in s are translated to coefficients.",
                "Extension-field equations remain in the retained primary source text.",
                (
                    "Geometry validity flags are source descriptions and are separate "
                    "from algebraic validation."
                ),
                (
                    "Comparison attribution, dates, and status flags are scoped to the "
                    "Pandoc table cell containing the equation."
                ),
                (
                    "Current and superseded relationships are evaluated against "
                    "exact-values.json at generation time."
                ),
            ],
        },
        "sources": source_metadata,
        "entries": entries,
        "unparsed_rows": unparsed,
    }


def _source_identity(document: dict[str, Any]) -> dict[str, Any]:
    """Project a corpus document onto fields determined by retained sources alone."""
    scope = document.get("scope", {})
    entries = document.get("entries", [])
    return {
        "format": document.get("format"),
        "scope": {key: scope.get(key) for key in SOURCE_SCOPE_KEYS},
        "sources": document.get("sources"),
        "entries": [{key: entry.get(key) for key in SOURCE_ENTRY_KEYS} for entry in entries],
        "unparsed_rows": document.get("unparsed_rows"),
    }


def verify_source_identity(document: dict[str, Any]) -> None:
    """Refuse a saved corpus whose source-bound facts drift from retained articles."""
    expected = _source_identity(collect_source())
    actual = _source_identity(document)
    if actual != expected:
        raise HistoricalPolynomialError(
            "historical polynomial source identity differs from retained sources"
        )


def validate(document: dict[str, Any], degree_max: int | None) -> None:
    """Run the exact builder check where the declared degree ceiling permits it."""
    for entry in document["entries"]:
        degree = int(entry["degree"])
        if degree_max is not None and degree > degree_max:
            entry["validation"] = {
                "status": "source-transcribed-unverified",
                "reason": f"degree {degree} exceeds the bounded degree-{degree_max} pass",
            }
            continue
        try:
            checks, _ = polynomial_checks(
                int(entry["n"]),
                tuple(int(value) for value in entry["coefficients"]),
                str(entry["historical_side"]),
                None,
            )
        except ExactValuesError as error:
            entry["validation"] = {
                "status": "refused",
                "method": "devtools.build_exact_values.polynomial_checks",
                "reason": str(error),
            }
        else:
            entry["validation"] = {
                "status": "verified",
                "method": "devtools.build_exact_values.polynomial_checks",
                "checks": checks,
            }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--verify-degree-max",
        type=int,
        default=-1,
        help="run exact builder checks through this degree; -1 checks every degree",
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    document = collect_source()
    validate(document, None if args.verify_degree_max < 0 else args.verify_degree_max)
    rendered = retained_json.dumps(document, ensure_ascii=False)
    if args.check:
        return 0 if read_retained_text(args.out) == rendered else 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(rendered, encoding="utf-8")
    print(
        f"wrote {len(document['entries'])} unique pairs from "
        f"{document['scope']['decoded_source_rows']} decoded rows to {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
