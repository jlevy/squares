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
from collections.abc import Sequence
from functools import cache
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Any
from urllib.parse import urlsplit

from markdown_it import MarkdownIt

from devtools.overview_data import tex_bounds
from devtools.profile_links import link_prose, profile_names
from devtools.render_overview import PACKING, REPO, Page, PageMeta, static_content_page
from devtools.repo_links import repo_url
from devtools.site_icons import account_icon
from devtools.site_resources import Resource, resources_for_profile
from sqpack.contributor_occurrences import MANIFEST as OCCURRENCES_MANIFEST
from sqpack.contributors import (
    PEOPLE_DIR,
    PROFILES_DIR,
    Contributor,
    ContributorError,
    load_contributors,
    record_ids,
    record_metadata,
    record_names,
    validate_public_url,
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
        PACKING / "devtools/profile_links.py",
        PACKING / "devtools/site_icons.py",
        PACKING / "devtools/site_resources.py",
        PACKING / "devtools/render_changelog.py",
        PACKING / "site-changelog.yaml",
        PACKING / "site-changelog.schema.yaml",
        CONTRIBUTORS.parent,
        PACKING / "devtools/templates/site-contributor.css",
        *evidence_paths(),
    )


def _bio(markdown: str, *, current_profile: str | None = None) -> str:
    parser = MarkdownIt("commonmark", {"html": False}).disable("image")

    def checked_link(url: str) -> bool:
        validate_public_url(url)
        return True

    parser.validateLink = checked_link
    from devtools.profile_links import link_prose  # noqa: PLC0415

    return link_prose(parser.renderInline(markdown), current_profile=current_profile)


def _source_links(contributor: Contributor, ids: Sequence[str]) -> str:
    return ", ".join(
        f'<a href="#source-{html.escape(source_id)}">{html.escape(source_id)}</a>'
        for source_id in ids
        if any(source.id == source_id for source in contributor.sources)
    )


def _credit_target(occurrence: CreditOccurrence) -> tuple[str, str]:
    origin = occurrence.origin
    if match := re.fullmatch(r"packing/frontier/n-(\d{3})\.md", origin.path):
        n = int(match[1])
        return f"cases/{n}.html", f"n = {n}"
    if origin.path == "packing/frontier/results.yaml" and re.fullmatch(
        r"T-\d{3}", origin.record_key
    ):
        return f"result/{origin.record_key.lower()}.html", origin.record_key
    if origin.path == "packing/resources/bibliography.yaml":
        line = _bibliography_line(origin.record_key)
        fragment = f"?plain=1#L{line}" if line is not None else ""
        return repo_url(origin.path, fragment), origin.record_key
    return repo_url(origin.path), origin.record_key or origin.path


@cache
def _bibliography_line(record_key: str) -> int | None:
    for number, line in enumerate(
        (REPO / "packing/resources/bibliography.yaml").read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if (match := re.fullmatch(r"\s*- key: (.+)", line)) and load_yaml(
            match[1]
        ) == record_key:
            return number
    return None


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


def credited_work(
    identifier: str, occurrences: Sequence[CreditOccurrence]
) -> dict[tuple[str, str, str, str, str], str]:
    """The reviewed work entries shown on a profile, with their existing deduplication."""
    credited: dict[tuple[str, str, str, str, str], str] = {}
    for occurrence in occurrences:
        if occurrence.disposition == "resolved" and occurrence.contributor_id == identifier:
            target, label = _credit_target(occurrence)
            credited.setdefault(
                (
                    target,
                    occurrence.origin.path,
                    occurrence.origin.record_key,
                    occurrence.role,
                    occurrence.label,
                ),
                label,
            )
    return credited


def account_links(contributor: Contributor, *, compact: bool = False) -> str:
    """The same public account destinations and icons in profiles and directory rows."""
    if not contributor.links:
        return ""
    variant = " site-contributor-links-compact" if compact else ""
    pieces = [f'<ul class="site-contributor-links{variant}" aria-label="Public websites">']
    for link in contributor.links:
        label = link.handle or link.url.removeprefix("https://").removeprefix(
            "http://"
        ).removesuffix("/")
        if link.kind == "twitter" and link.handle:
            label = "@" + link.handle
        accessible = f"{_LINK_LABELS[link.kind]}: {label}"
        if compact:
            accessible += f" ({contributor.real_name or contributor.display_name})"
        visible = "" if compact else f"<span>{html.escape(label)}</span>"
        pieces.append(
            f'<li><a href="{html.escape(link.url)}" aria-label="{html.escape(accessible)}" '
            f'title="{html.escape(accessible)}">{account_icon(link.kind)}{visible}</a></li>'
        )
    pieces.append("</ul>")
    return "".join(pieces)


def resource_list(identifier: str, records: Sequence[Resource] | None = None) -> str:
    """Cited external work, preserving its original author and lineage relationship."""
    linked = resources_for_profile(identifier, records)
    if not linked:
        return ""
    items = []
    for resource in linked:
        context = link_prose(
            tex_bounds(resource.byline + ". " + resource.description),
            current_profile=identifier,
        )
        items.append(
            f'<li><a href="{html.escape(resource.url)}">{html.escape(resource.title)}</a>'
            f" — {context}</li>"
        )
    return (
        '<section id="resources"><h2>Resources</h2><ul class="site-contributor-resources">'
        + "".join(items)
        + "</ul></section>"
    )


def contributor_article(
    contributor: Contributor, occurrences: Sequence[CreditOccurrence]
) -> str:
    """The same complete article is served standalone and extracted by the popover."""
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
    if contributor.real_name and contributor.real_name != contributor.display_name:
        identity.append(f"<dt>Real name</dt><dd>{html.escape(contributor.real_name)}</dd>")
    if contributor.display_aliases:
        identity.append(
            "<dt>Also credited as</dt><dd>"
            + ", ".join(html.escape(alias) for alias in contributor.display_aliases)
            + "</dd>"
        )
    if identity:
        pieces.append('<dl class="site-contributor-identity">' + "".join(identity) + "</dl>")
    if contributor.bio:
        biography = _bio(contributor.bio, current_profile=contributor.id)
        pieces.append(f'<p class="site-contributor-bio">{biography}</p>')
    pieces.append(account_links(contributor))
    pieces.append(resource_list(contributor.id))
    credited = credited_work(contributor.id, occurrences)
    if credited:
        pieces.append("<section><h2>Credited work</h2>")
        if len(credited) > 12:
            pieces.append(f"<details open><summary>{len(credited)} reviewed credits</summary>")
        pieces.append('<ul class="site-contributor-credits">')
        for (target, _path, _key, role, original_label), label in credited.items():
            match = re.fullmatch(r"cases/(\d+)\.html", target)
            case = f' data-case="{match[1]}"' if match else ""
            pieces.append(
                f'<li><a href="{html.escape(target)}"{case}>{html.escape(label)}</a>: '
                f"{html.escape(role.replace('-', ' '))} — {html.escape(original_label)}</li>"
            )
        pieces.append("</ul>")
        if len(credited) > 12:
            pieces.append("</details>")
        pieces.append("</section>")
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
    field_names = {
        "id": "Profile identifier",
        "display_name": "Public name",
        "real_name": "Real name",
        "surname": "Family name",
        "aliases": "Credit spellings",
        "links": "Public websites",
        "sources": "Sources",
        "bio_sources": "Biography sources",
        "provenance": "Field evidence",
    }
    pieces.append('<p class="site-contributor-evidence">Identity evidence</p><ul>')
    for provenance in contributor.provenance:
        field = field_names.get(
            provenance.field.split("/")[1], provenance.field.replace("_", " ")
        )
        pieces.append(f"<li>{field}: {_source_links(contributor, provenance.sources)}</li>")
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


def _resource_count(person: Contributor, target: str, name: str) -> str:
    count = len(resources_for_profile(person.id))
    return (
        f'<a href="{target}#resources" aria-label="{count} resources for {name}">{count}</a>'
        if count
        else '<span class="site-profile-empty">0</span>'
    )


def profile_table(
    contributors: Sequence[Contributor], occurrences: Sequence[CreditOccurrence]
) -> str:
    """Full public names and the same reviewed-credit counts as each profile."""
    rows = []
    for person in contributors:
        name = html.escape(person.real_name or person.display_name)
        target = html.escape(person.profile_path)
        count = len(credited_work(person.id, occurrences))
        rows.append(
            f'<tr><td><a href="{target}">{name}</a></td>'
            f'<td class="num"><a href="{target}" tabindex="-1" '
            f'aria-label="{count} reviewed credits for {name}">{count}</a></td>'
            f'<td class="num">{_resource_count(person, target, name)}</td>'
            f'<td class="site-profile-links">{account_links(person, compact=True)}</td></tr>'
        )
    return (
        '<div class="site-table-wrap">'
        '<table class="kpress-table site-table site-profile-table" '
        'aria-label="Profiles"><thead><tr><th scope="col">Name</th>'
        '<th scope="col" class="num">Credits</th>'
        '<th scope="col" class="num">Resources</th><th scope="col">Links</th>'
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
        "and links to reviewed credits. Counts match the reviewed credits listed on each "
        "profile. Links open public accounts and websites; Resources lists the cited "
        "external work shown on the homepage.</p>"
        + profile_table(contributors, occurrences)
        + "</article>"
    )
    pages = [
        static_content_page(
            directory, meta=DIRECTORY_META, current="about", page_scripts=(DIRECTORY_SCRIPT,)
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
