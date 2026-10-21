"""Shared counts for distinct registered results and reviewed attribution spans."""

from __future__ import annotations

import html
import re
from collections import Counter
from collections.abc import Collection, Iterable, Mapping, Sequence
from datetime import date
from typing import Any, NamedTuple

from devtools.result_credit import PROJECT_AUTHOR_ORIGIN, credit_sources, is_first_party
from sqpack.contributor_occurrences import CreditOccurrence, CreditOrigin

BIBLIOGRAPHY = "packing/resources/bibliography.yaml"
REGISTER = "packing/frontier/results.yaml"


class ResultTally(NamedTuple):
    """Distinct result ids, counts at each significance level, and latest recorded date."""

    results: tuple[str, ...]
    counts: tuple[tuple[int, int], ...]
    latest: str


class CreditStats(NamedTuple):
    """A person's registered results and separately counted reviewed credit spans."""

    results: tuple[str, ...]
    credits: int


def _credit_key(item: CreditOccurrence) -> tuple[CreditOrigin, int, int, str, str | None]:
    return item.origin, item.start, item.end, item.role, item.contributor_id


def person_credit_stats(
    identifier: str,
    occurrences: Iterable[CreditOccurrence],
    raw_records: Iterable[Mapping[str, Any]],
) -> CreditStats:
    """Join reviewed source credits to results without inferring work from case mentions.

    Bibliography joins follow the sources whose credit each result prints. Direct
    register joins reach that result alone; the reviewed project-author constant
    reaches all first-party results. Every other reviewed span counts as a credit only.
    """
    reviewed = {
        _credit_key(item): item
        for item in occurrences
        if item.disposition == "resolved" and item.contributor_id == identifier
    }
    sources = {
        item.origin.record_key for item in reviewed.values() if item.origin.path == BIBLIOGRAPHY
    }
    direct = {
        item.origin.record_key for item in reviewed.values() if item.origin.path == REGISTER
    }
    author = any(item.origin == PROJECT_AUTHOR_ORIGIN for item in reviewed.values())
    results = dict.fromkeys(
        str(record["id"])
        for record in raw_records
        if str(record["id"]) in direct
        or (author and is_first_party(record))
        or sources.intersection(credit_sources(record))
    )
    return CreditStats(tuple(results), len(reviewed))


def project_credit_count(
    source_keys: Collection[str],
    result_ids: Collection[str],
    occurrences: Iterable[CreditOccurrence],
) -> int:
    """Count reviewed spans within a project's explicit sources and registered results.

    A project's author may have credits elsewhere; those do not enter this scope.
    """
    sources, results = frozenset(source_keys), frozenset(result_ids)
    return len(
        {
            _credit_key(item)
            for item in occurrences
            if item.disposition == "resolved"
            and (
                (item.origin.path == BIBLIOGRAPHY and item.origin.record_key in sources)
                or (item.origin.path == REGISTER and item.origin.record_key in results)
            )
        }
    )


def tally_results(
    ids: Iterable[str],
    measures: Mapping[str, tuple[int, str]],
    levels: Sequence[int],
) -> ResultTally:
    """Count each id once, retaining its supplied significance and date without inference."""
    results = tuple(dict.fromkeys(ids))
    ordered_levels = sorted(set(levels), reverse=True)
    counts = Counter(measures[identifier][0] for identifier in results)
    if counts.keys() - set(ordered_levels):
        raise ValueError("result significance is outside the supplied levels")
    return ResultTally(
        results,
        tuple((level, counts[level]) for level in ordered_levels),
        max((measures[identifier][1] for identifier in results), default=""),
    )


def _link(text: str, href: str | None) -> str:
    shown = html.escape(text)
    return shown if href is None else f'<a href="{html.escape(href, quote=True)}">{shown}</a>'


def render_tally(
    tally: ResultTally,
    *,
    total_href: str | None = None,
    level_hrefs: Mapping[int, str] | None = None,
    credit_count: int | None = None,
) -> str:
    """Inline HTML shared by profile and project counts; callers supply their own links."""
    total = len(tally.results)
    noun = "result" if total == 1 else "results"
    rendered = _link(f"{total} {noun}", total_href)
    populated = [(level, count) for level, count in tally.counts if count]
    hrefs = level_hrefs if level_hrefs is not None else {}
    if len(populated) == 1:
        level = populated[0][0]
        rendered += " at " + _link(f"S{level}", hrefs.get(level))
    elif populated:
        rendered += (
            " ("
            + ", ".join(
                _link(f"{count} at S{level}", hrefs.get(level)) for level, count in populated
            )
            + ")"
        )
    if credit_count is not None:
        noun = "credit" if credit_count == 1 else "credits"
        rendered += ", " + html.escape(f"{credit_count} {noun}")
    return rendered


def _result_year(dated: str) -> int:
    if re.fullmatch(r"[0-9]{4}(?:-[0-9]{2}){0,2}", dated) is None:
        raise ValueError(f"Invalid result date: {dated!r}")
    # Omitted calendar parts are filled only to validate the recorded precision.
    return date.fromisoformat(dated + "-01" * (2 - dated.count("-"))).year


def years_active(ids: Iterable[str], measures: Mapping[str, tuple[int, str]]) -> str | None:
    """Years covered by dated reviewed results, using the tally's supplied date policy."""
    years = {
        _result_year(measures[identifier][1])
        for identifier in set(ids)
        if measures[identifier][1]
    }
    if not years:
        return None
    earliest, latest = min(years), max(years)
    return str(earliest) if earliest == latest else f"{earliest}\u2013{latest}"
