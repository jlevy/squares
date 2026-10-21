"""Separate primary results, credited person/result associations, and activity evidence."""

from __future__ import annotations

import html
import re
from collections import Counter
from collections.abc import Collection, Iterable, Mapping, Sequence
from datetime import date
from typing import Any, Literal, NamedTuple

from devtools.result_credit import PROJECT_AUTHOR_ORIGIN, is_first_party
from sqpack.contributor_occurrences import CreditOccurrence, CreditOrigin

BIBLIOGRAPHY = "packing/resources/bibliography.yaml"
REGISTER = "packing/frontier/results.yaml"
_AUTHOR_FIELD = re.compile(r"/authors/[0-9]+")
_DIRECT_CREDIT_FIELD = re.compile(r"/builds_on/credit/[0-9]+")


class ResultTally(NamedTuple):
    """Distinct primary result ids and their significance counts."""

    results: tuple[str, ...]
    counts: tuple[tuple[int, int], ...]
    latest: str


class CreditTally(NamedTuple):
    """Distinct credited person/result pairs; several people may share one result."""

    associations: tuple[tuple[str, str], ...]
    counts: tuple[tuple[int, int], ...]
    latest: str


class CreditStats(NamedTuple):
    """Primary results and nonprimary credits are disjoint; raw spans are diagnostic."""

    results: tuple[str, ...]
    credited_results: tuple[str, ...]
    reviewed_spans: int


class _Assignments(NamedTuple):
    authors: dict[str, set[str]]
    source_credits: dict[str, set[str]]
    source_prerequisites: dict[str, set[str]]
    direct_credits: dict[str, set[str]]
    project_authors: set[str]


def _credit_key(item: CreditOccurrence) -> tuple[CreditOrigin, int, int, str, str | None]:
    return item.origin, item.start, item.end, item.role, item.contributor_id


def _source_author(item: CreditOccurrence) -> bool:
    return (
        item.origin.path == BIBLIOGRAPHY
        and item.role == "source-author"
        and _AUTHOR_FIELD.fullmatch(item.origin.field) is not None
    )


def _assignments(occurrences: Iterable[CreditOccurrence]) -> _Assignments:
    authors: dict[str, set[str]] = {}
    source_credits: dict[str, set[str]] = {}
    source_prerequisites: dict[str, set[str]] = {}
    direct_credits: dict[str, set[str]] = {}
    project_authors: set[str] = set()
    for item in occurrences:
        if item.disposition != "resolved" or item.contributor_id is None:
            continue
        origin, identifier = item.origin, item.contributor_id
        if origin == PROJECT_AUTHOR_ORIGIN and item.role == "project-author":
            project_authors.add(identifier)
        elif origin.path == BIBLIOGRAPHY:
            if _source_author(item):
                authors.setdefault(origin.record_key, set()).add(identifier)
            if origin.field == "/credit" or _AUTHOR_FIELD.fullmatch(origin.field):
                source_credits.setdefault(origin.record_key, set()).add(identifier)
            if origin.field == "/credit" and item.role == "prerequisite":
                source_prerequisites.setdefault(origin.record_key, set()).add(identifier)
        elif origin.path == REGISTER and _DIRECT_CREDIT_FIELD.fullmatch(origin.field):
            direct_credits.setdefault(origin.record_key, set()).add(identifier)
    return _Assignments(
        authors, source_credits, source_prerequisites, direct_credits, project_authors
    )


def _primary_authors(
    record: Mapping[str, Any],
    assignments: _Assignments,
    *,
    source_keys: Collection[str] | None = None,
) -> set[str]:
    if is_first_party(record):
        return assignments.project_authors if source_keys is None else set()
    keys = set(record["attribution"]["source_keys"])
    if source_keys is not None:
        keys.intersection_update(source_keys)
    return {
        identifier
        for key in keys
        for identifier in assignments.authors.get(key, set())
        - assignments.source_prerequisites.get(key, set())
    }


def _credited_people(
    record: Mapping[str, Any],
    assignments: _Assignments,
    *,
    source_keys: Collection[str] | None = None,
) -> set[str]:
    keys = set((record.get("attribution") or {}).get("source_keys", ()))
    if source_keys is not None:
        keys.intersection_update(source_keys)
    named = {
        identifier for key in keys for identifier in assignments.source_credits.get(key, ())
    }
    named.update(assignments.direct_credits.get(str(record["id"]), ()))
    return named - _primary_authors(record, assignments)


def person_credit_stats(
    identifier: str,
    occurrences: Iterable[CreditOccurrence],
    raw_records: Iterable[Mapping[str, Any]],
) -> CreditStats:
    """Count primary authorship separately from reviewed acknowledgments of prior work.

    Primary authors require reviewed source-author spans in the result's attribution
    sources, or the reviewed author constant for first-party work. Other reviewed
    source-credit and result-specific builds-on spans yield one Credit per result.
    Merely citing a basis source or sharing a case does not assign a personal credit.
    """
    reviewed = {
        _credit_key(item): item
        for item in occurrences
        if item.disposition == "resolved" and item.contributor_id == identifier
    }
    assignments = _assignments(reviewed.values())
    records = tuple(raw_records)
    results = dict.fromkeys(
        str(record["id"])
        for record in records
        if identifier in _primary_authors(record, assignments)
    )
    credited = dict.fromkeys(
        str(record["id"])
        for record in records
        if identifier in _credited_people(record, assignments)
    )
    return CreditStats(tuple(results), tuple(credited), len(reviewed))


def project_primary_results(
    identifiers: Collection[str],
    source_keys: Collection[str],
    occurrences: Iterable[CreditOccurrence],
    raw_records: Iterable[Mapping[str, Any]],
) -> tuple[str, ...]:
    """Primary results for identified project authors through its explicit sources."""
    assignments = _assignments(occurrences)
    people = frozenset(identifiers)
    return tuple(
        dict.fromkeys(
            str(record["id"])
            for record in raw_records
            if people.intersection(
                _primary_authors(record, assignments, source_keys=source_keys)
            )
        )
    )


def project_credit_associations(
    identifiers: Collection[str],
    source_keys: Collection[str],
    occurrences: Iterable[CreditOccurrence],
    raw_records: Iterable[Mapping[str, Any]],
) -> tuple[tuple[str, str], ...] | None:
    """Credits received by this project's named authors for its explicitly linked work.

    The citing result must name a project source in attribution or builds_on and must
    review a personal credit to its author. An author's credits for unrelated projects
    cannot enter this scope. None means the project lacks an identified author or
    source-key scope, so callers must omit the tally rather than imply an author total.
    """
    if not identifiers or not source_keys:
        return None
    assignments = _assignments(occurrences)
    people, sources = frozenset(identifiers), frozenset(source_keys)
    associations: dict[tuple[str, str], None] = {}
    for record in raw_records:
        cited = set((record.get("attribution") or {}).get("source_keys", ()))
        cited.update((record.get("builds_on") or {}).get("source_keys", ()))
        if not sources.intersection(cited):
            continue
        for identifier in sorted(people.intersection(_credited_people(record, assignments))):
            associations[identifier, str(record["id"])] = None
    return tuple(associations)


def _measures(
    ids: Sequence[str],
    measures: Mapping[str, tuple[int, str]],
    levels: Sequence[int],
) -> tuple[tuple[tuple[int, int], ...], str]:
    ordered_levels = sorted(set(levels), reverse=True)
    counts = Counter(measures[identifier][0] for identifier in ids)
    if counts.keys() - set(ordered_levels):
        raise ValueError("result significance is outside the supplied levels")
    return (
        tuple((level, counts[level]) for level in ordered_levels),
        max((measures[identifier][1] for identifier in ids), default=""),
    )


def tally_results(
    ids: Iterable[str],
    measures: Mapping[str, tuple[int, str]],
    levels: Sequence[int],
) -> ResultTally:
    """Count each primary result once at its own supplied significance level."""
    results = tuple(dict.fromkeys(ids))
    counts, latest = _measures(results, measures, levels)
    return ResultTally(results, counts, latest)


def tally_credits(
    associations: Iterable[tuple[str, str]],
    measures: Mapping[str, tuple[int, str]],
    levels: Sequence[int],
) -> CreditTally:
    """Count each person/result pair once, at the citing result's significance."""
    pairs = tuple(dict.fromkeys(associations))
    counts, latest = _measures(tuple(result for _, result in pairs), measures, levels)
    return CreditTally(pairs, counts, latest)


def _link(text: str, href: str | None) -> str:
    shown = html.escape(text)
    return shown if href is None else f'<a href="{html.escape(href, quote=True)}">{shown}</a>'


def render_tally(
    tally: ResultTally | CreditTally,
    *,
    noun: Literal["result", "credit", "record"] = "result",
    total_href: str | None = None,
    level_hrefs: Mapping[int, str] | None = None,
) -> str:
    """Inline result or credit totals and significance histograms with caller-supplied links."""
    total = len(tally.results if isinstance(tally, ResultTally) else tally.associations)
    label = noun if total == 1 else noun + "s"
    rendered = _link(f"{total} {label}", total_href)
    populated = [(level, count) for level, count in tally.counts if count]
    hrefs = level_hrefs if level_hrefs is not None else {}
    if len(populated) == 1:
        level = populated[0][0]
        rendered += (
            ' <span class="site-tally-levels">(at '
            + _link(f"S{level}", hrefs.get(level))
            + ")</span>"
        )
    elif populated:
        rendered += (
            ' <span class="site-tally-levels">('
            + ", ".join(
                _link(f"{count} at S{level}", hrefs.get(level)) for level, count in populated
            )
            + ")</span>"
        )
    return rendered


def _activity_year(dated: str) -> int:
    if re.fullmatch(r"[0-9]{4}(?:-[0-9]{2}){0,2}", dated) is None:
        raise ValueError(f"Invalid activity date: {dated!r}")
    # Omitted calendar parts are filled only to validate the recorded precision.
    return date.fromisoformat(dated + "-01" * (2 - dated.count("-"))).year


def person_activity_years(
    identifier: str,
    occurrences: Iterable[CreditOccurrence],
    bibliography_sources: Mapping[str, Mapping[str, Any]],
    cases: Mapping[str, Mapping[str, Any]],
    results: Iterable[Mapping[str, Any]],
) -> tuple[int, ...]:
    """Original authorship and explicit discovery/proof years, never later reuse or import.

    Bibliography sources are indexed by key and case payloads by repository-relative
    path. A case improver has no dedicated year field, so its discovery year cannot be
    borrowed. Undated originals and unreviewed identities remain unknown.
    """
    years: set[int] = set()
    project_author = False
    for item in occurrences:
        if item.disposition != "resolved" or item.contributor_id != identifier:
            continue
        origin = item.origin
        year = None
        if _source_author(item) or (
            origin.path == BIBLIOGRAPHY
            and item.role == "credited-contributor"
            and _AUTHOR_FIELD.fullmatch(origin.field) is not None
        ):
            # A reviewed author-list acknowledgment dates this person's own support
            # work; a later /credit citation does not date the cited person's activity.
            year = bibliography_sources.get(origin.record_key, {}).get("year")
        elif origin == PROJECT_AUTHOR_ORIGIN and item.role == "project-author":
            project_author = True
        elif origin.path in cases:
            case = cases[origin.path]
            if item.role == "construction-finder" and re.fullmatch(
                r"/reported_upper_bound/found_by/[0-9]+", origin.field
            ):
                year = (case.get("reported_upper_bound") or {}).get("found_year")
            elif item.role == "lower-bound-prover" and re.fullmatch(
                r"/reported_lower_bound/proved_by/[0-9]+", origin.field
            ):
                year = (case.get("reported_lower_bound") or {}).get("proved_year")
        if year is not None:
            years.add(_activity_year(str(year)))
    if project_author:
        years.update(
            _activity_year(str(record["established"]))
            for record in results
            if is_first_party(record) and record.get("established")
        )
    return tuple(sorted(years))


def years_active(years: Iterable[int]) -> str | None:
    """Format the range of evidenced activity years, leaving an unknown range blank."""
    selected = set(years)
    if not selected:
        return None
    earliest, latest = min(selected), max(selected)
    return str(earliest) if earliest == latest else f"{earliest}\u2013{latest}"
