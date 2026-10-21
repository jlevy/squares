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
from dataclasses import fields, is_dataclass
from functools import cache
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any

from devtools.overview_data import RESULTS
from devtools.render_overview import (
    PACKING,
    REPO,
    RESULTS_PAGE,
    Page,
    PageMeta,
    static_content_page,
)
from devtools.repo_links import repo_url
from devtools.result_credit import PROJECT_AUTHOR_ORIGIN, credit_sources, is_first_party
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
        CONTRIBUTORS.parent,
        PACKING / "devtools/templates/site-contributor.css",
        # Which results a source's credit reaches, and what each is (`_credited_work`).
        RESULTS,
        *evidence_paths(),
    )


def _bio(markdown: str) -> str:
    """The bio as inline HTML, by the one rule the loader already checked it with."""
    return render_bio(markdown)


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
    cited = "; ".join(sources)
    cited = f", in {html.escape(cited)}" if cited else ""
    identifier = str(record["id"])
    kind = html.escape(str(record["kind"]).replace("-", " "))
    return (
        f'<li><a href="result/{html.escape(identifier.lower())}.html">'
        f"{html.escape(identifier)}</a> ({kind}, {html.escape(_cases_text(record))}): "
        f"{credit}{cited}</li>"
    )


def _plural(count: int, one: str) -> str:
    return f"{count} {one}" + ("" if count == 1 else "s")


def _credited_work(
    identifier: str,
    occurrences: Sequence[CreditOccurrence],
    results: Sequence[Mapping[str, Any]],
) -> list[str]:
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
    lines = [
        _result_line(by_id[result_id], *credited[result_id])
        # In register order: `T-` and a zero-padded number, which may grow a digit.
        for result_id in sorted(credited, key=lambda result_id: (len(result_id), result_id))
    ]
    counts = {"result": len(credited), "case": 0, "source": 0, "other record": 0}
    for (target, path, _key, role, original_label), label in sorted(
        rows.items(), key=lambda row: not row[0][0].startswith("cases/")
    ):
        match = re.fullmatch(r"cases/(\d+)\.html", target)
        case = f' data-case="{match[1]}"' if match else ""
        counts["case" if match else "source" if path == BIBLIOGRAPHY else "other record"] += 1
        lines.append(
            f'<li><a href="{html.escape(target)}"{case}>{html.escape(label)}</a>: '
            f"{_role(role)} — {html.escape(original_label)}</li>"
        )
    if not (lines or authored):
        return []
    pieces = ["<section><h2>Credited work</h2>"]
    first_party = sum(1 for record in results if is_first_party(record))
    pieces.extend(
        '<ul class="site-contributor-credits">'
        f'<li><a href="{RESULTS_PAGE}">The register\u2019s '
        f"{html.escape(_plural(first_party, 'first-party result'))}</a>: "
        f"{_role(occurrence.role)} — {html.escape(occurrence.label)}</li></ul>"
        for occurrence in dict.fromkeys(authored)
    )
    if lines:
        fold = len(lines) > _FOLD
        if fold:
            summary = ", ".join(_plural(count, noun) for noun, count in counts.items() if count)
            pieces.append(f"<details><summary>Reviewed credits: {summary}</summary>")
        pieces.extend(('<ul class="site-contributor-credits">', *lines, "</ul>"))
        if fold:
            pieces.append("</details>")
    pieces.append("</section>")
    return pieces


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


def contributor_article(
    contributor: Contributor,
    occurrences: Sequence[CreditOccurrence],
    *,
    results: Sequence[Mapping[str, Any]] | None = None,
) -> str:
    """The same complete article is served standalone and extracted by the popover.
    `results` are the register's (`frontier/results.yaml`) unless a test gives others."""
    name = html.escape(contributor.display_name)
    pieces = [
        f'<article class="site-contributor" data-contributor-id="{contributor.id}">',
        (
            '<nav class="site-contributor-breadcrumb" aria-label="Breadcrumb">'
            f'<a href="{DIRECTORY_PATH}">Profiles</a></nav>'
        ),
        f"<h1>{name}</h1>",
    ]
    identity = []
    if contributor.real_name and contributor.real_name != contributor.display_name:
        identity.append(f"<dt>Real name</dt><dd>{html.escape(contributor.real_name)}</dd>")
    if contributor.aliases:
        identity.append(
            f"<dt>{_FIELD_NAMES['aliases']}</dt><dd>"
            + ", ".join(html.escape(alias) for alias in contributor.aliases)
            + "</dd>"
        )
    if identity:
        pieces.append('<dl class="site-contributor-identity">' + "".join(identity) + "</dl>")
    if contributor.bio:
        pieces.append(f'<p class="site-contributor-bio">{_bio(contributor.bio)}</p>')
        pieces.append(
            '<p class="site-contributor-evidence">Biography sources: '
            + _source_links(contributor, contributor.bio_sources)
            + "</p>"
        )
    if contributor.links:
        pieces.append('<ul class="site-contributor-links" aria-label="Public websites">')
        for link in contributor.links:
            label = _LINK_LABELS[link.kind]
            if link.handle:
                label += ": " + link.handle
            pieces.append(
                f'<li><a href="{html.escape(link.url)}">{html.escape(label)}</a></li>'
            )
        pieces.append("</ul>")
    pieces.extend(
        _credited_work(
            contributor.id,
            occurrences,
            _register_results() if results is None else results,
        )
    )
    pieces.append('<section class="site-contributor-sources"><h2>Sources</h2><ol>')
    for source in contributor.sources:
        target = source.url or repo_url(source.archive_path or "")
        pieces.append(
            f'<li id="source-{html.escape(source.id)}"><a href="{html.escape(target)}">'
            f"{html.escape(source.id)}</a>: {html.escape(source.locator)}</li>"
        )
    pieces.append("</ol>")
    pieces.append("<details><summary>Identity evidence</summary><ul>")
    pieces.extend(_evidence_item(contributor, item) for item in contributor.provenance)
    pieces.append("</ul></details></section></article>")
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
    """Every validated person, in public-name order."""
    return sorted(
        load_contributors(CONTRIBUTORS, repo=REPO).by_id.values(),
        key=lambda contributor: (contributor.display_name.casefold(), contributor.id),
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
        '<article class="site-contributor-directory"><h1>Profiles</h1>'
        "<p>People whose work the square-packing record cites or credits, paper authors "
        "and project contributors alike. Each profile records public identity evidence "
        "and links to reviewed credits.</p>"
        # The directory's names navigate; they never open the profile popover.
        '<nav aria-label="Profiles" data-contributor-plain><ul>'
        + "".join(
            f'<li><a href="{contributor.profile_path}">'
            f"{html.escape(contributor.display_name)}</a></li>"
            for contributor in contributors
        )
        + "</ul></nav></article>"
    )
    pages = [static_content_page(directory, meta=DIRECTORY_META, current="")]
    pages.extend(
        static_content_page(
            contributor_article(contributor, occurrences),
            meta=profile_meta(contributor),
            current="",
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
