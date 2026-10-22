"""Publish evidenced person profiles, their directory and reviewed credit links.

The site serves them under `profiles/` (`sqpack.contributors.PROFILES_DIR`), since the
directory includes cited paper authors as well as the project's contributors; each
earlier `contributors/` address forwards there (`render_overview.MOVED_PAGES`). Module,
record and attribute names keep the contributor vocabulary of the records.
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, fields, is_dataclass
from functools import cache
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any
from urllib.parse import urlsplit

from markdown_it import MarkdownIt

from devtools.github_references import credit_reference_urls, render_github_references
from devtools.overview_data import RESULTS
from devtools.profile_links import link_prose, profile_names, public_names
from devtools.profile_records import current_record_ids, record_input_paths
from devtools.record_presentation import record_index, record_tally
from devtools.render_overview import (
    PACKING,
    REPO,
    RESULTS_PAGE,
    TABLE_SCRIPT,
    Page,
    PageMeta,
    static_content_page,
)
from devtools.repo_links import repo_url
from devtools.result_credit import PROJECT_AUTHOR_ORIGIN, credit_sources, is_first_party
from devtools.site_icons import account_icon
from devtools.site_resources import Resource, profile_resources
from devtools.site_resources import resources as resource_records
from devtools.site_tallies import (
    person_activity_years,
    person_credit_stats,
    render_tally,
    tally_credits,
    tally_results,
    years_active,
)
from sqpack.contributor_occurrences import MANIFEST as OCCURRENCES_MANIFEST
from sqpack.contributors import (
    PEOPLE_DIR,
    PROFILES_DIR,
    Contributor,
    ContributorError,
    ContributorLink,
    ContributorSource,
    FieldProvenance,
    load_contributors,
    record_ids,
    record_metadata,
    record_names,
    render_bio,
)
from sqpack.yamlio import load_yaml

if TYPE_CHECKING:
    from sqpack.contributor_occurrences import CreditOccurrence

#: The person records' directory under `packing/` (`sqpack.contributors.PEOPLE_DIR`), not
#: a published address; the occurrence manifest and the schemas sit beside it.
CONTRIBUTORS = PACKING / PEOPLE_DIR
MANIFEST = PACKING / OCCURRENCES_MANIFEST
DIRECTORY_PATH = f"{PROFILES_DIR}/index.html"
DIRECTORY_SCRIPT = PACKING / "devtools/overview/profile-directory.js"
_LINK_LABELS = {
    "github": "GitHub",
    "twitter": "Twitter / X",
    "substack": "Substack",
    "personal": "Personal website",
    "publication": "Publication website",
}


def page_paths() -> tuple[str, ...]:
    """Declare routes without reading archive bytes omitted by a sparse checkout."""
    return (
        DIRECTORY_PATH,
        *(f"{PROFILES_DIR}/{identifier}.html" for identifier in record_ids(CONTRIBUTORS)),
    )


def evidence_paths() -> tuple[Path, ...]:
    """Exact archive dependencies, discoverable before sparse evidence is restored."""
    paths: set[Path] = set()
    for document in sorted(CONTRIBUTORS.glob("*.md")):
        record = load_yaml(document.read_text(encoding="utf-8").split("---\n")[1])
        for source in record["contributor"]["sources"]:
            if raw := source.get("archive_path"):
                path = PurePosixPath(raw)
                if (
                    path.is_absolute()
                    or "\\" in raw
                    or any(part in {"", ".", ".."} for part in raw.split("/"))
                    or not (REPO / raw).resolve().is_relative_to(REPO.resolve())
                ):
                    raise ContributorError(f"invalid contributor archive path: {raw}")
                paths.add(REPO / raw)
    manifest = MANIFEST
    if manifest.is_file():
        from sqpack.contributor_occurrences import dependency_paths  # noqa: PLC0415

        paths.update(dependency_paths(manifest, repo=REPO))
    return tuple(sorted(paths))


def inputs() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        DIRECTORY_SCRIPT,
        TABLE_SCRIPT,
        PACKING / "devtools/profile_links.py",
        PACKING / "devtools/site_icons.py",
        PACKING / "devtools/site_resources.py",
        PACKING / "devtools/site_tallies.py",
        PACKING / "devtools/record_presentation.py",
        *record_input_paths(),
        PACKING / "devtools/github_references.py",
        PACKING / "devtools/overview_sections.py",
        PACKING / "frontier/source-coverage.yaml",
        REPO / "epistemics.md",
        PACKING / "devtools/render_changelog.py",
        PACKING / "site-changelog.yaml",
        PACKING / "site-changelog.schema.yaml",
        CONTRIBUTORS.parent,
        PACKING / "devtools/templates/site-contributor.css",
        RESULTS,
        *evidence_paths(),
    )


def _bio(markdown: str, *, current_profile: str | None = None) -> str:
    """Render with the loader's checked Markdown contract, then link authored names."""
    return link_prose(render_bio(markdown), current_profile=current_profile)


def _source_links(contributor: Contributor, ids: Sequence[str]) -> str:
    return ", ".join(
        f'<a href="#source-{html.escape(source_id)}">{html.escape(source_id)}</a>'
        for source_id in ids
        if any(source.id == source_id for source in contributor.sources)
    )


#: Where a source's reviewed credit spans sit, and the register, as the manifest names them.
BIBLIOGRAPHY = "packing/resources/bibliography.yaml"
REGISTER = "packing/frontier/results.yaml"
#: More credited records than this fold under a disclosure.
_FOLD = 12
#: How an identity evidence item names the record field it supports, by its root key.
_FIELD_NAMES = {
    "id": "Profile identifier",
    "display_name": "Public name",
    "real_name": "Real name",
    "surname": "Family name",
    "display_aliases": "Selected alternate names",
    # Aliases are credit spellings, X display names and former handles alike.
    "aliases": "Also known as",
    "links": "Public websites",
    "sources": "Sources",
    "bio_sources": "Biography sources",
    "provenance": "Field evidence",
}
#: The same, for an item that names one entry of a list field (`/links/0`).
_ITEM_NAMES = {
    "links": "Public website",
    "sources": "Source",
    "bio_sources": "Biography source",
}


def _credit_target(occurrence: CreditOccurrence) -> tuple[str, str]:
    origin = occurrence.origin
    if match := re.fullmatch(r"packing/frontier/n-(\d{3})\.md", origin.path):
        n = int(match[1])
        return f"cases/{n}.html", f"n = {n}"
    if origin.path == REGISTER and re.fullmatch(r"T-\d{3}", origin.record_key):
        return f"result/{origin.record_key.lower()}.html", origin.record_key
    if origin.path == BIBLIOGRAPHY:
        line = _bibliography_line(origin.record_key)
        fragment = f"?plain=1#L{line}" if line is not None else ""
        return repo_url(origin.path, fragment), origin.record_key
    return repo_url(origin.path), origin.record_key or origin.path


@cache
def _bibliography_line(record_key: str) -> int | None:
    for number, line in enumerate(
        (REPO / BIBLIOGRAPHY).read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if (match := re.fullmatch(r"\s*- key: (.+)", line)) and load_yaml(
            match[1]
        ) == record_key:
            return number
    return None


@cache
def _register_results() -> tuple[Mapping[str, Any], ...]:
    """The register's results, in its order."""
    return tuple(load_yaml(RESULTS.read_text(encoding="utf-8"))["results"])


def _cases_text(record: Mapping[str, Any]) -> str:
    """A result's cases in plain text, by the rule its page's head states them with
    (`result_overview.where`): `n = 11`, a few named, or a count and a range."""
    from devtools.result_overview import CASES_NAMED  # noqa: PLC0415

    scope = record["scope"]
    cases = (
        sorted(scope["n_values"])
        if "n_values" in scope
        else list(range(scope["n_min"], scope["n_max"] + 1))
    )
    if len(cases) == 1:
        return f"n = {cases[0]}"
    if len(cases) <= CASES_NAMED:
        return "n = " + ", ".join(map(str, cases))
    return f"{len(cases)} cases, n = {cases[0]} to {cases[-1]}"


def _role(role: str) -> str:
    return html.escape(role.replace("-", " "))


def _result_line(
    record: Mapping[str, Any], roles: Mapping[str, Mapping[str, None]], sources: Iterable[str]
) -> str:
    """One credited result: its ID linked to its page, its kind and cases, each role the
    reviewed spans give with the spellings they credit, and the sources they sit in."""
    by_labels: dict[tuple[str, ...], list[str]] = {}
    for role, labels in roles.items():
        by_labels.setdefault(tuple(labels), []).append(role)
    credit = "; ".join(
        ", ".join(_role(role) for role in group)
        + " — "
        + ", ".join(html.escape(label) for label in labels)
        for labels, group in by_labels.items()
    )
    sources = tuple(sources)
    cited = "; ".join(sources)
    cited = f", in {html.escape(cited)}" if cited else ""
    identifier = str(record["id"])
    kind = html.escape(str(record["kind"]).replace("-", " "))
    return (
        f'<li><a href="result/{html.escape(identifier.lower())}.html">'
        f"{html.escape(identifier)}</a> ({kind}, {html.escape(_cases_text(record))}): "
        f"{credit}{cited}{contribution_references(sources, (identifier,))}</li>"
    )


def _plural(count: int, one: str) -> str:
    return f"{count} {one}" + ("" if count == 1 else "s")


@dataclass(frozen=True)
class CreditedWork:
    parts: tuple[str, ...]
    count: int


def _credited_work(
    identifier: str,
    occurrences: Sequence[CreditOccurrence],
    results: Sequence[Mapping[str, Any]],
) -> CreditedWork:
    """The profile's credited work, read from the reviewed manifest.

    A span in a source's credit or authors credits the person in every result whose
    attribution names that source, the results its credit line is printed for
    (`result_credit.credit_sources`), so it is listed under those results: one line a
    result, each role once, with the source keys as secondary text. A span in a
    result's own entry lists under that result too. The project author's one generator
    constant becomes one line for the first-party results, not a line naming the
    constant. Case spans keep their case links, and a source no result names keeps its
    bibliography line."""
    by_id = {str(record["id"]): record for record in results}
    reached: dict[str, list[str]] = {}
    for record in results:
        for key in credit_sources(record):
            reached.setdefault(key, []).append(str(record["id"]))
    credited: dict[str, tuple[dict[str, dict[str, None]], dict[str, None]]] = {}
    rows: dict[tuple[str, str, str, str, str], str] = {}
    authored: list[CreditOccurrence] = []
    for occurrence in occurrences:
        if occurrence.disposition != "resolved" or occurrence.contributor_id != identifier:
            continue
        origin = occurrence.origin
        if origin == PROJECT_AUTHOR_ORIGIN:
            authored.append(occurrence)
            continue
        if origin.path == BIBLIOGRAPHY and origin.record_key in reached:
            ids, source = reached[origin.record_key], origin.record_key
        elif origin.path == REGISTER and origin.record_key in by_id:
            ids, source = [origin.record_key], None
        else:
            target, label = _credit_target(occurrence)
            rows.setdefault(
                (target, origin.path, origin.record_key, occurrence.role, occurrence.label),
                label,
            )
            continue
        for result_id in ids:
            roles, sources = credited.setdefault(result_id, ({}, {}))
            roles.setdefault(occurrence.role, {})[occurrence.label] = None
            if source is not None:
                sources[source] = None
    stats = person_credit_stats(identifier, occurrences, results)
    primary_ids, credit_ids = set(stats.results), set(stats.credited_results)
    ordered = sorted(credited, key=lambda result_id: (len(result_id), result_id))
    primary_lines = [
        _result_line(by_id[result_id], *credited[result_id])
        for result_id in ordered
        if result_id in primary_ids and not (authored and is_first_party(by_id[result_id]))
    ]
    credit_lines = [
        _result_line(by_id[result_id], *credited[result_id])
        for result_id in ordered
        if result_id in credit_ids
    ]
    other_lines = [
        _result_line(by_id[result_id], *credited[result_id])
        for result_id in ordered
        if result_id not in primary_ids | credit_ids
    ]
    for (target, path, key, role, original_label), label in sorted(
        rows.items(), key=lambda row: not row[0][0].startswith("cases/")
    ):
        match = re.fullmatch(r"cases/(\d+)\.html", target)
        case = f' data-case="{match[1]}"' if match else ""
        references = contribution_references((key,), ()) if path == BIBLIOGRAPHY else ""
        other_lines.append(
            f'<li><a href="{html.escape(target)}"{case}>{html.escape(label)}</a>: '
            f"{_role(role)} — {html.escape(original_label)}{references}</li>"
        )
    authored = list(dict.fromkeys(authored))
    if not (primary_lines or credit_lines or other_lines or authored):
        return CreditedWork((), 0)
    pieces = []
    current_ids = current_record_ids(primary_ids, record_index())
    pending = sorted(primary_ids.intersection(record_index().unresolved))
    if current_ids or pending:
        pieces.append('<section id="records"><h2>Records</h2>')
        pieces.append(
            "<p>Current registered contributions in their recorded family "
            "and scope. A result counts once when any of its facets remains current.</p>"
        )
        fallback = ({item.role: {item.label: None} for item in authored}, {})
        pieces.extend(
            _work_listing(
                [
                    _result_line(by_id[result_id], *credited.get(result_id, fallback))
                    for result_id in current_ids
                ],
                "Records",
            )
        )
        if pending:
            pieces.append(
                '<p>Facet comparisons awaiting review:</p><ul class="site-contributor-credits">'
            )
            for result_id in pending:
                reasons = "; ".join(record_index().unresolved[result_id])
                pieces.append(
                    f'<li><a href="result/{html.escape(result_id.lower())}.html">'
                    f"{html.escape(result_id)}</a>: {html.escape(reasons)}</li>"
                )
            pieces.append("</ul>")
        pieces.append("</section>")
    if primary_lines or authored:
        pieces.append('<section id="results"><h2>Results</h2>')
        first_party_ids = tuple(
            str(record["id"]) for record in results if is_first_party(record)
        )
        pieces.extend(
            '<ul class="site-contributor-credits">'
            f'<li><a href="{RESULTS_PAGE}">The register\u2019s '
            f"{html.escape(_plural(len(first_party_ids), 'first-party result'))}</a>: "
            f"{_role(occurrence.role)} — {html.escape(occurrence.label)}"
            f"{contribution_references((), first_party_ids)}</li></ul>"
            for occurrence in authored
        )
        pieces.extend(_work_listing(primary_lines, "Results"))
        pieces.append("</section>")
    if credit_lines:
        pieces.append('<section id="credited-work"><h2>Credited work</h2>')
        pieces.extend(_work_listing(credit_lines, "Credits"))
        pieces.append("</section>")
    if other_lines:
        pieces.append('<section id="other-reviewed-records"><h2>Other reviewed records</h2>')
        pieces.extend(_work_listing(other_lines, "Reviewed records"))
        pieces.append("</section>")
    return CreditedWork(
        tuple(pieces), len(primary_lines) + len(credit_lines) + len(other_lines) + len(authored)
    )


def _work_listing(lines: Sequence[str], label: str) -> list[str]:
    if not lines:
        return []
    parts = []
    if len(lines) > _FOLD:
        parts.append(f"<details open><summary>{label}: {len(lines)}</summary>")
    parts.extend(('<ul class="site-contributor-credits">', *lines, "</ul>"))
    if len(lines) > _FOLD:
        parts.append("</details>")
    return parts


#: What the identity evidence prints for a record value that is not plain text.
_PRINTED_FIELDS: dict[type, str] = {
    ContributorLink: "url",
    ContributorSource: "id",
    FieldProvenance: "field",
}


def _printed(value: object) -> str | None:
    """A record value as the identity evidence prints the claim it supports."""
    if isinstance(value, tuple):
        printed = [text for item in value if (text := _printed(item))]
        return ", ".join(printed) or None
    if (name := _PRINTED_FIELDS.get(type(value))) is not None:
        value = getattr(value, name)
    return None if value is None else str(value)


def _claimed(contributor: Contributor, pointer: str) -> str | None:
    """The value a provenance JSON pointer names in the record, if it names one."""
    value: object = contributor
    for raw in pointer.split("/")[1:]:
        part = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(value, tuple):
            if not part.isdigit() or int(part) >= len(value):
                return None
            value = value[int(part)]
        elif is_dataclass(value) and part in {field.name for field in fields(value)}:
            value = getattr(value, part)
        else:
            return None
    return _printed(value)


def _evidence_item(contributor: Contributor, provenance: FieldProvenance) -> str:
    """One identity evidence item: the field, the value it claims, and its sources."""
    parts = provenance.field.split("/")
    names = _ITEM_NAMES if len(parts) > 2 and parts[2].isdigit() else {}
    field = (
        names.get(parts[1])
        or _FIELD_NAMES.get(parts[1])
        or html.escape(provenance.field.replace("_", " "))
    )
    sources = _source_links(contributor, provenance.sources)
    value = _claimed(contributor, provenance.field)
    if value is None:
        return f"<li>{field}: {sources}</li>"
    return f"<li>{field}: {html.escape(value)} ({sources})</li>"


def news_by_profile(entries: Sequence[dict[str, Any]]) -> dict[str, list[tuple[str, str, str]]]:
    """Derive related articles only from explicit profile-record links in News prose."""
    from devtools.render_changelog import entry_anchor, inline_html  # noqa: PLC0415

    linked: dict[str, list[tuple[str, str, str]]] = {}
    parser = MarkdownIt("commonmark", {"html": False})
    for entry in entries:
        identifiers = set()
        prose = entry["summary"] + "\n\n" + entry.get("details", "")
        for token in parser.parse(prose):
            for child in token.children or ():
                if child.type != "link_open":
                    continue
                path = urlsplit(str(child.attrGet("href") or "")).path
                if match := re.fullmatch(r"packing/contributors/people/([a-z0-9-]+)\.md", path):
                    identifiers.add(match[1])
        for identifier in sorted(identifiers):
            linked.setdefault(identifier, []).append(
                (
                    entry_anchor(entry["id"]),
                    inline_html(entry["title"], allow_links=False),
                    entry["date"],
                )
            )
    return linked


@cache
def _related_news() -> dict[str, list[tuple[str, str, str]]]:
    from devtools.render_changelog import load, news_entries  # noqa: PLC0415

    return news_by_profile(news_entries(load()))


@dataclass(frozen=True)
class _PublicLink:
    kind: str
    url: str
    label: str
    description: str


def account_links(contributor: Contributor, *, compact: bool = False) -> str:
    """Public provider accounts; personal/publication websites belong to Resources."""
    links = []
    for link in contributor.links:
        if link.kind in {"personal", "publication"}:
            continue
        label = link.handle or urlsplit(link.url).netloc
        if link.kind == "twitter" and link.handle:
            label = "@" + link.handle
        links.append(
            _PublicLink(link.kind, link.url, label, f"{_LINK_LABELS[link.kind]}: {label}")
        )
    return _public_links(contributor, links, compact=compact, label="Public accounts")


def _public_links(
    contributor: Contributor, links: Sequence[_PublicLink], *, compact: bool, label: str
) -> str:
    """Shared named external-link icons for public accounts and resource addresses."""
    if not links:
        return ""
    variant = " site-contributor-links-compact" if compact else ""
    pieces = [f'<ul class="site-contributor-links{variant}" aria-label="{label}">']
    for link in links:
        accessible = link.description
        if compact:
            accessible += f" ({contributor.real_name or contributor.display_name})"
        visible = f"<span>{html.escape(link.label)}</span>"
        pieces.append(
            f'<li><a href="{html.escape(link.url)}" aria-label="{html.escape(accessible)}" '
            f'title="{html.escape(accessible)}">{account_icon(link.kind)}{visible}</a></li>'
        )
    pieces.append("</ul>")
    return "".join(pieces)


def resource_list(identifier: str, records: Sequence[Resource] | None = None) -> str:
    """Reuse homepage resource cards, preserving their sources, attribution and tally."""
    from devtools.overview_sections import resource_cards  # noqa: PLC0415

    linked = profile_resources(identifier, records)
    if not linked:
        return ""
    return (
        '<section id="resources"><h2>Resources</h2>'
        + resource_cards(linked, current_profile=identifier)
        + "</section>"
    )


def resource_links(person: Contributor) -> str:
    """Visible exact resource addresses, using the same external-link component."""
    links = tuple(
        _PublicLink(
            "github" if urlsplit(record.url).hostname == "github.com" else "personal",
            record.url,
            (
                "/".join(urlsplit(record.url).path.strip("/").split("/")[:2])
                if urlsplit(record.url).hostname == "github.com"
                else urlsplit(record.url).netloc
            ),
            f"Resource: {record.title} ({record.url})",
        )
        for record in profile_resources(person.id)
    )
    return _public_links(person, links, compact=True, label="Resources")


def _profile_measures(records: Sequence[Mapping[str, Any]]) -> dict[str, tuple[int, str]]:
    return {
        str(record["id"]): (
            int(record["significance"]["score"]),
            str(
                (record.get("attribution") or {}).get("published")
                or record.get("established")
                or ""
            ),
        )
        for record in records
    }


@cache
def _activity_documents() -> tuple[dict[str, Mapping[str, Any]], dict[str, Mapping[str, Any]]]:
    bibliography = load_yaml((REPO / BIBLIOGRAPHY).read_text())["sources"]
    sources = {str(source["key"]): source for source in bibliography}
    cases = {
        path.relative_to(REPO).as_posix(): load_yaml(path.read_text().split("---\n")[1])[
            "packing"
        ]
        for path in (PACKING / "frontier").glob("n-*.md")
    }
    return sources, cases


def profile_years(
    identifier: str,
    occurrences: Sequence[CreditOccurrence],
    records: Sequence[Mapping[str, Any]],
) -> str | None:
    sources, cases = _activity_documents()
    return years_active(person_activity_years(identifier, occurrences, sources, cases, records))


def profile_summary(
    contributors: Sequence[Contributor],
    occurrences: Sequence[CreditOccurrence],
    *,
    results: Sequence[Mapping[str, Any]] | None = None,
    resources: Sequence[Resource] | None = None,
) -> str:
    """Union result and resource identities across the published people; never sum overlaps."""
    records = _register_results() if results is None else results
    stats = {
        person.id: person_credit_stats(person.id, occurrences, records)
        for person in contributors
    }
    result_ids = {identifier for item in stats.values() for identifier in item.results}
    credit_pairs = {
        (identifier, result_id)
        for identifier, item in stats.items()
        for result_id in item.credited_results
    }
    identifiers = {person.id for person in contributors}
    resources = resource_records() if resources is None else resources
    resource_urls = {
        record.url for record in resources if identifiers.intersection(record.profile_ids)
    }
    resource_urls.update(
        link.url
        for person in contributors
        for link in person.links
        if link.kind in {"personal", "publication"}
    )
    people = f"{len(contributors)} " + ("person" if len(contributors) == 1 else "people")
    return (
        '<p class="site-profile-summary">'
        + " · ".join(
            (
                people,
                _plural(len(current_record_ids(result_ids, record_index())), "record"),
                _plural(len(result_ids), "result"),
                _plural(len(credit_pairs), "credit"),
                _plural(len(resource_urls), "resource"),
            )
        )
        + "</p>"
    )


@cache
def _reference_documents() -> tuple[dict[str, Any], dict[str, Any]]:
    from devtools.render_changelog import load  # noqa: PLC0415

    return load_yaml((PACKING / "frontier/source-coverage.yaml").read_text()), load()


def contribution_references(source_keys: Sequence[str], result_ids: Sequence[str]) -> str:
    """Threads attached to this credited entry; registration is not PR authorship."""
    coverage, changelog = _reference_documents()
    references = credit_reference_urls(
        source_keys, result_ids, coverage=coverage, changelog=changelog
    )
    groups = [
        f"{label}: {rendered}"
        for label, urls in (
            ("Source", references.sources),
            ("Registered in", references.registrations),
            ("Supporting", references.supporting),
        )
        if (rendered := render_github_references(urls))
    ]
    return (
        ' <span class="site-contributor-references">(' + "; ".join(groups) + ")</span>"
        if groups
        else ""
    )


def profile_table(
    contributors: Sequence[Contributor],
    occurrences: Sequence[CreditOccurrence],
    *,
    results: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """Full public names with separate primary-result and nonprimary-credit tallies."""
    records = _register_results() if results is None else results
    names = public_names()
    rows = []
    for person in contributors:
        name = html.escape(person.real_name or person.display_name)
        label = name
        target = html.escape(person.profile_path)
        years = profile_years(person.id, occurrences, records)
        stats = person_credit_stats(person.id, occurrences, records)
        tally = (
            '<span class="site-credit-tally">'
            + render_tally(
                tally_results(stats.results, _profile_measures(records), (5, 4, 3, 2, 1)),
                total_href=person.profile_path + "#results",
            )
            + "</span>"
            if stats.results
            else ""
        )
        credit_cell_markup = (
            '<span class="site-credit-tally">'
            + render_tally(
                tally_credits(
                    ((person.id, result_id) for result_id in stats.credited_results),
                    _profile_measures(records),
                    (5, 4, 3, 2, 1),
                ),
                noun="credit",
                total_href=person.profile_path + "#credited-work",
            )
            + "</span>"
            if stats.credited_results
            else ""
        )
        record_cell = record_tally(
            stats.results,
            _profile_measures(records),
            total_href=person.profile_path + "#records",
            pending_href=person.profile_path + "#records",
            blank_zero=True,
        )
        if record_cell:
            record_cell = '<span class="site-credit-tally">' + record_cell + "</span>"
        sort_name = html.escape(" | ".join(names[person.id].sort_key), quote=True)
        record_count = len(current_record_ids(stats.results, record_index()))
        rows.append(
            f'<tr><td data-value="{sort_name}"><a href="{target}">{label}</a></td>'
            f'<td class="site-profile-records" data-value="{record_count}">{record_cell}</td>'
            f'<td class="site-profile-stats" data-value="{len(stats.results)}">{tally}</td>'
            f'<td class="site-profile-credits" data-value="{len(stats.credited_results)}">'
            f"{credit_cell_markup}</td>"
            f'<td class="site-profile-years" data-value="{years[:4] if years else ""}">'
            f"{html.escape(years) if years else ''}</td>"
            f'<td class="site-profile-resources">{resource_links(person)}</td>'
            f'<td class="site-profile-links">{account_links(person, compact=True)}</td></tr>'
        )
    return (
        '<div class="site-table-wrap site-wide">'
        '<table class="kpress-table site-table site-profile-table" data-contributor-plain '
        'aria-label="Profiles"><thead><tr>'
        '<th scope="col" data-sort="text" aria-sort="ascending">Name</th>'
        '<th scope="col" data-sort="num">Records</th>'
        '<th scope="col" data-sort="num">Results</th>'
        '<th scope="col" data-sort="num">Credits</th>'
        '<th scope="col" data-sort="num" data-sort-empty="last" '
        'title="Sort by the first recorded activity year">Years active</th>'
        '<th scope="col" data-sort="text" data-sort-empty="last">Resources</th>'
        '<th scope="col" data-sort="text" data-sort-empty="last">Accounts</th>'
        "</tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
    )


def profile_preview() -> str:
    """The same metadata-free Profiles invitation on Home and About."""
    from devtools.overview_sections import arrow_icon  # noqa: PLC0415

    return (
        '<h1 id="profiles" class="site-title">Profiles</h1>\n\n'
        "We track contributors and the authors cited in the square-packing record. "
        "Browse their profiles and credited work.\n\n"
        '<p class="site-action-row site-more">'
        '<a class="site-action" href="profiles/index.html">All Profiles'
        + arrow_icon()
        + "</a></p>"
    )


def credited_work(
    identifier: str,
    occurrences: Sequence[CreditOccurrence],
    *,
    results: Sequence[Mapping[str, Any]] | None = None,
) -> CreditedWork:
    """The grouped reviewed entries and exact count displayed on a profile."""
    return _credited_work(
        identifier, occurrences, _register_results() if results is None else results
    )


def _visible_handles(contributor: Contributor) -> tuple[str, ...]:
    """Only curated additional handles, without repeating accounts or obvious names."""
    accounts = {
        link.handle.casefold().removeprefix("@") for link in contributor.links if link.handle
    }
    names = {
        re.sub(r"[\W_]+", "", name.casefold())
        for name in (contributor.display_name, contributor.real_name, contributor.surname)
        if name
    }
    return tuple(
        alias
        for alias in contributor.display_aliases
        if alias.casefold().removeprefix("@") not in accounts
        and re.sub(r"[\W_]+", "", alias.casefold()) not in names
    )


def profile_tally(
    identifier: str,
    occurrences: Sequence[CreditOccurrence],
    *,
    target: str = "",
    results: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """Current Records, primary Results and nonprimary Credits with shared formatting."""
    records = _register_results() if results is None else results
    stats = person_credit_stats(identifier, occurrences, records)
    measures = _profile_measures(records)
    authored = tally_results(stats.results, measures, (5, 4, 3, 2, 1))
    credited = tally_credits(
        ((identifier, result_id) for result_id in stats.credited_results),
        measures,
        (5, 4, 3, 2, 1),
    )
    return (
        '<span class="site-credit-tally">'
        + record_tally(
            stats.results,
            measures,
            total_href=target + "#records",
            pending_href=target + "#records",
        )
        + " · "
        + render_tally(authored, total_href=target + "#results" if authored.results else None)
        + " · "
        + render_tally(
            credited,
            noun="credit",
            total_href=target + "#credited-work" if credited.associations else None,
        )
        + "</span>"
    )


def contributor_article(
    contributor: Contributor,
    occurrences: Sequence[CreditOccurrence],
    *,
    results: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """The same complete article is served standalone and extracted by the popover."""
    records = _register_results() if results is None else results
    name = html.escape(contributor.display_name)
    pieces = [
        f'<article class="site-contributor" data-contributor-id="{contributor.id}">',
        (
            '<nav class="site-contributor-breadcrumb" aria-label="Breadcrumb">'
            '<a href="about.html#profiles">About</a> / '
            f'<a href="{DIRECTORY_PATH}">Profiles</a></nav>'
        ),
        f"<h1>{name}</h1>",
    ]
    identity = []
    if years := profile_years(contributor.id, occurrences, records):
        identity.append(f"<dt>Years active</dt><dd>{html.escape(years)}</dd>")
    if contributor.real_name and contributor.real_name != contributor.display_name:
        identity.append(f"<dt>Real name</dt><dd>{html.escape(contributor.real_name)}</dd>")
    if handles := _visible_handles(contributor):
        identity.append(
            "<dt>Handles</dt><dd>"
            + ", ".join(html.escape(alias) for alias in handles)
            + "</dd>"
        )
    if contributor.bio:
        biography = _bio(contributor.bio, current_profile=contributor.id)
        pieces.append(f'<p class="site-contributor-bio">{biography}</p>')
    pieces.append(account_links(contributor))
    if identity:
        pieces.append('<dl class="site-contributor-identity">' + "".join(identity) + "</dl>")
    pieces.append(resource_list(contributor.id))
    pieces.append("<p>" + profile_tally(contributor.id, occurrences, results=results) + "</p>")
    work = credited_work(contributor.id, occurrences, results=records).parts
    pieces.extend(work)
    if news := _related_news().get(contributor.id):
        pieces.append('<section><h2>Related News</h2><ul class="site-contributor-news">')
        for anchor, title, day in news:
            pieces.append(
                f'<li><a href="news.html#{anchor}">{title}</a> '
                f'<time datetime="{day}">{day}</time></li>'
            )
        pieces.append("</ul></section>")
    pieces.append('<details class="site-contributor-sources"><summary>Sources</summary>')
    if contributor.bio:
        pieces.append(
            '<p class="site-contributor-evidence">Biography sources: '
            + _source_links(contributor, contributor.bio_sources)
            + "</p>"
        )
    pieces.append("<ol>")
    for source in contributor.sources:
        target = source.url or repo_url(source.archive_path or "")
        pieces.append(
            f'<li id="source-{html.escape(source.id)}"><a href="{html.escape(target)}">'
            f"{html.escape(source.id)}</a>: {html.escape(source.locator)}</li>"
        )
    pieces.append("</ol>")
    pieces.append('<p class="site-contributor-evidence">Identity evidence</p><ul>')
    pieces.extend(_evidence_item(contributor, item) for item in contributor.provenance)
    pieces.append("</ul></details></article>")
    return "\n".join(pieces)


#: The directory's head record. Profiles include cited paper authors, so the directory
#: says whose work the record names rather than calling everyone a contributor.
DIRECTORY_META = PageMeta(
    "Profiles",
    "People whose work the square-packing record cites or credits, with sourced public "
    "profiles and links to their work.",
    DIRECTORY_PATH,
)


def _contributors() -> list[Contributor]:
    """Every validated person, in evidenced family-name order."""
    names = profile_names(record_metadata(CONTRIBUTORS))
    return sorted(
        load_contributors(CONTRIBUTORS, repo=REPO).by_id.values(),
        key=lambda contributor: names[contributor.id].sort_key,
    )


def _profile_meta(identifier: str, display_name: str) -> PageMeta:
    description = (
        f"Public profile, identity sources and credited square-packing work for {display_name}."
    )
    if len(description) > 160:
        description = description[:159].rsplit(" ", 1)[0] + "."
    return PageMeta(display_name, description, f"{PROFILES_DIR}/{identifier}.html")


def profile_meta(contributor: Contributor) -> PageMeta:
    """A profile's head record: the evidenced public name and its own description."""
    return _profile_meta(contributor.id, contributor.display_name)


def page_metas() -> dict[str, PageMeta]:
    """The directory's and each profile's head record, by path. A forwarder at an
    earlier `contributors/` address previews the page it leads to from these
    (`render_overview.forwarded_metas`), in every build that checks forwarders, a
    paper's partial one included, so they are read from the records' names alone
    (`record_names`) and need none of the archive evidence a profile page cites."""
    return {
        DIRECTORY_PATH: DIRECTORY_META,
        **{
            f"{PROFILES_DIR}/{identifier}.html": _profile_meta(identifier, name)
            for identifier, name in record_names(CONTRIBUTORS).items()
        },
    }


def contributor_pages() -> list[Page]:
    """Directory plus one canonical profile per validated person."""
    from sqpack.contributor_occurrences import load_occurrences  # noqa: PLC0415

    contributors = _contributors()
    occurrences = load_occurrences().occurrences
    directory = (
        '<article class="site-contributor-directory">'
        '<nav class="site-contributor-breadcrumb" aria-label="Breadcrumb">'
        '<a href="about.html#profiles">About</a></nav><h1>Profiles</h1>'
        "<p>People whose work the square-packing record cites or credits, paper authors "
        "and project contributors alike. Each profile records public identity evidence "
        "and links to reviewed credits. Results count distinct registered results by their "
        "reviewed primary authors. Records are current registered contributions "
        "in their recorded family and scope. Review pending marks comparisons that remain "
        "unclassified, including alongside a supported positive count. "
        "Credits count distinct results that credit a person\u2019s prior work, excluding "
        "their authored results. Years active covers dated original work and explicit "
        "discovery or proof records, excluding later reuse and import dates. "
        "Accounts open public account profiles; Resources lists personal and publication "
        "websites and the cited "
        "external work shown on the homepage.</p>"
        + profile_summary(contributors, occurrences)
        + profile_table(contributors, occurrences)
        + "</article>"
    )
    pages = [
        static_content_page(
            directory,
            meta=DIRECTORY_META,
            current="about",
            page_scripts=(TABLE_SCRIPT, DIRECTORY_SCRIPT),
        )
    ]
    pages.extend(
        static_content_page(
            contributor_article(contributor, occurrences),
            meta=profile_meta(contributor),
            current="about",
        )
        for contributor in contributors
    )
    return pages


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--checkout-evidence",
        action="store_true",
        help="restore exact contributor archive dependencies in a sparse checkout",
    )
    args = parser.parse_args(argv)
    if not args.checkout_evidence:
        parser.error("use devtools.render_overview to publish pages")
    sparse = subprocess.run(
        ["git", "config", "--bool", "core.sparseCheckout"],
        cwd=REPO,
        check=False,
        capture_output=True,
        text=True,
    )
    if sparse.stdout.strip() == "true":
        cone = subprocess.run(
            ["git", "config", "--bool", "core.sparseCheckoutCone"],
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
        )
        if cone.stdout.strip() == "true":
            raise ContributorError(
                "exact evidence restoration requires non-cone sparse checkout"
            )
        paths = ["/" + path.relative_to(REPO).as_posix() for path in evidence_paths()]
        if paths:
            subprocess.run(["git", "sparse-checkout", "add", *paths], cwd=REPO, check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
