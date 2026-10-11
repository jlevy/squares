"""Names, roles and evidenced chronology for the shared atlas print credits.

The curated input retains citations and case/source associations separately from
visible names. This parser does not decide proof acceptance or change case facts.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from typing import Any

CreditDate = date | int | str | None


def _date_interval(value: CreditDate) -> tuple[str, str] | None:
    if value is None:
        return None
    text = value.isoformat() if isinstance(value, date) else str(value)
    if re.fullmatch(r"\d{4}", text):
        return f"{text}-01-01T00:00:00", f"{text}-12-31T23:59:59.999999"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        date.fromisoformat(text)
        return f"{text}T00:00:00", f"{text}T23:59:59.999999"
    instant = datetime.fromisoformat(text)
    if instant.tzinfo is None:
        raise ValueError("a timed credit date must include its timezone")
    stamp = instant.astimezone(UTC).replace(tzinfo=None).isoformat()
    return stamp, stamp


def chronological_names(dates: Mapping[str, CreditDate]) -> tuple[str, ...]:
    """Oldest first, without inventing month/day priority for a year-only date.

    Non-overlapping date intervals establish order. Names whose evidenced precision
    leaves them incomparable use alphabetical ties; undated names follow last.
    """
    intervals = {name: _date_interval(value) for name, value in dates.items()}
    remaining = {name: interval for name, interval in intervals.items() if interval is not None}
    ordered: list[str] = []
    while remaining:
        eligible = [
            name
            for name, interval in remaining.items()
            if not any(other[1] < interval[0] for other in remaining.values())
        ]
        name = min(eligible, key=str.casefold)
        ordered.append(name)
        del remaining[name]
    ordered.extend(
        sorted(
            (name for name, interval in intervals.items() if interval is None), key=str.casefold
        )
    )
    return tuple(ordered)


@dataclass(frozen=True, slots=True)
class CreditClause:
    prefix: str
    names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class CreditParagraph:
    key: str
    clauses: tuple[CreditClause, ...]

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(name for clause in self.clauses for name in clause.names)

    @property
    def atoms(self) -> tuple[str, ...]:
        """Keep each name intact at a line break, including a role clause's prefix."""
        atoms = []
        for clause_index, clause in enumerate(self.clauses):
            for index, name in enumerate(clause.names):
                suffix = (
                    ","
                    if index < len(clause.names) - 1
                    else ";"
                    if clause_index < len(self.clauses) - 1
                    else ""
                )
                atoms.append((f"{clause.prefix} " if index == 0 else "") + name + suffix)
        return tuple(atoms)


@dataclass(frozen=True, slots=True)
class CreditAttributions:
    aliases: Mapping[str, str]
    paragraphs: tuple[CreditParagraph, ...]
    metadata: str

    def normalize_name(self, name: str) -> str:
        return self.aliases.get(name.casefold(), name)


def parse(document: Mapping[str, Any]) -> CreditAttributions:
    """Parse the curated versioned input, preserving its complete source metadata."""
    if document["format_version"] != 1:
        raise ValueError("unsupported atlas credit attribution format")
    aliases = {
        str(alias).casefold(): str(name) for alias, name in document["name_aliases"].items()
    }
    paragraphs = []
    for section_key, paragraph_key, clauses in (
        (
            "lower_bounds",
            "lower-bound",
            (("Lower bounds due to", {"current-bound-source-author"}),),
        ),
        (
            "optimality",
            "optimality",
            (
                (
                    "Optimality proofs due to",
                    {"theorem-author", "direct-prerequisite-proof-author"},
                ),
                ("formalization contributions by", {"formalization-proof-contributor"}),
                (
                    "verification infrastructure and execution by",
                    {"verification-infrastructure-or-execution"},
                ),
            ),
        ),
    ):
        contributors = document[section_key]["contributors"]
        names = [entry["name"] for entry in contributors]
        if len(names) != len(set(names)):
            raise ValueError("atlas attribution contributor names must be unique")
        parsed_clauses = []
        for prefix, roles in clauses:
            dates = {
                str(entry["name"]): entry["first_date"]
                for entry in contributors
                if roles.intersection(entry["roles"])
            }
            parsed_clauses.append(CreditClause(prefix, chronological_names(dates)))
        paragraph = CreditParagraph(paragraph_key, tuple(parsed_clauses))
        if len(paragraph.names) != len(set(paragraph.names)):
            raise ValueError("print roles must not repeat a contributor within a paragraph")
        paragraphs.append(paragraph)
    return CreditAttributions(
        aliases,
        tuple(paragraphs),
        json.dumps(document, ensure_ascii=False, separators=(",", ":")),
    )
