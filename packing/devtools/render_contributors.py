"""Publish evidenced contributor articles, their directory and reviewed credit links."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
from collections.abc import Sequence
from functools import cache
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING

from markdown_it import MarkdownIt

from devtools.render_overview import PACKING, REPO, Page, PageMeta, static_content_page
from devtools.repo_links import repo_url
from sqpack.contributors import (
    Contributor,
    ContributorError,
    load_contributors,
    validate_public_url,
)
from sqpack.yamlio import load_yaml

if TYPE_CHECKING:
    from sqpack.contributor_occurrences import CreditOccurrence

CONTRIBUTORS_DIR = "contributors"
CONTRIBUTORS = PACKING / CONTRIBUTORS_DIR
DIRECTORY_PATH = f"{CONTRIBUTORS_DIR}/index.html"
_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
_LINK_LABELS = {
    "github": "GitHub",
    "twitter": "Twitter / X",
    "substack": "Substack",
    "personal": "Personal website",
    "publication": "Publication website",
}


def page_paths() -> tuple[str, ...]:
    """Declare routes without reading archive bytes omitted by a sparse checkout."""
    paths = sorted(CONTRIBUTORS.glob("*.md"))
    if any(_ID.fullmatch(path.stem) is None for path in paths):
        raise ContributorError("contributor filenames must be stable lowercase ids")
    return (DIRECTORY_PATH, *(f"contributors/{path.stem}.html" for path in paths))


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
    manifest = CONTRIBUTORS / "occurrences.yaml"
    if manifest.is_file():
        from sqpack.contributor_occurrences import dependency_paths  # noqa: PLC0415

        paths.update(dependency_paths(manifest, repo=REPO))
    return tuple(sorted(paths))


def inputs() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        CONTRIBUTORS,
        PACKING / "devtools/templates/site-contributor.css",
        *evidence_paths(),
    )


def _bio(markdown: str) -> str:
    parser = MarkdownIt("commonmark", {"html": False}).disable("image")

    def checked_link(url: str) -> bool:
        validate_public_url(url)
        return True

    parser.validateLink = checked_link
    return parser.renderInline(markdown)


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


def contributor_article(
    contributor: Contributor, occurrences: Sequence[CreditOccurrence]
) -> str:
    """The same complete article is served standalone and extracted by the popover."""
    name = html.escape(contributor.display_name)
    pieces = [
        f'<article class="site-contributor" data-contributor-id="{contributor.id}">',
        (
            '<nav class="site-contributor-breadcrumb" aria-label="Breadcrumb">'
            '<a href="contributors/index.html">Contributors</a></nav>'
        ),
        f"<h1>{name}</h1>",
    ]
    identity = []
    if contributor.real_name and contributor.real_name != contributor.display_name:
        identity.append(f"<dt>Real name</dt><dd>{html.escape(contributor.real_name)}</dd>")
    if contributor.aliases:
        identity.append(
            "<dt>Also credited as</dt><dd>"
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
    credited = {}
    for occurrence in occurrences:
        if occurrence.disposition == "resolved" and occurrence.contributor_id == contributor.id:
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
    if credited:
        pieces.append("<section><h2>Credited work</h2>")
        if len(credited) > 12:
            pieces.append(f"<details><summary>{len(credited)} reviewed credits</summary>")
        pieces.append('<ul class="site-contributor-credits">')
        for (target, _path, _key, role, original_label), label in credited.items():
            match = re.fullmatch(r"cases/(\d+)\.html", target)
            case = f' data-case="{match[1]}"' if match else ""
            pieces.append(
                f'<li><a href="{html.escape(target)}"{case}>{html.escape(label)}</a>: '
                f"{html.escape(role)} — {html.escape(original_label)}</li>"
            )
        pieces.append("</ul>")
        if len(credited) > 12:
            pieces.append("</details>")
        pieces.append("</section>")
    pieces.append('<section class="site-contributor-sources"><h2>Sources</h2><ol>')
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
        "aliases": "Credit spellings",
        "links": "Public websites",
        "sources": "Sources",
        "bio_sources": "Biography sources",
        "provenance": "Field evidence",
    }
    pieces.append("<details><summary>Identity evidence</summary><ul>")
    for provenance in contributor.provenance:
        field = field_names.get(
            provenance.field.split("/")[1], provenance.field.replace("_", " ")
        )
        pieces.append(f"<li>{field}: {_source_links(contributor, provenance.sources)}</li>")
    pieces.append("</ul></details></section></article>")
    return "\n".join(pieces)


def contributor_pages() -> list[Page]:
    """Directory plus one canonical profile per validated person."""
    from sqpack.contributor_occurrences import load_occurrences  # noqa: PLC0415

    contributors = sorted(
        load_contributors(CONTRIBUTORS, repo=REPO).by_id.values(),
        key=lambda contributor: (contributor.display_name.casefold(), contributor.id),
    )
    occurrences = load_occurrences().occurrences
    directory = (
        '<article class="site-contributor-directory"><h1>Contributors</h1>'
        "<p>People credited in the square-packing record. Each profile records public "
        "identity evidence and links to reviewed credits.</p>"
        '<nav aria-label="Contributors"><ul>'
        + "".join(
            f'<li><a href="{contributor.profile_path}" data-contributor="{contributor.id}">'
            f"{html.escape(contributor.display_name)}</a></li>"
            for contributor in contributors
        )
        + "</ul></nav></article>"
    )
    pages = [
        static_content_page(
            directory,
            meta=PageMeta(
                "Contributors",
                "People credited in the square-packing record, with sourced public profiles "
                "and links to their work.",
                DIRECTORY_PATH,
            ),
            current="",
        )
    ]
    for contributor in contributors:
        description = (
            "Public profile, identity sources and credited square-packing work for "
            f"{contributor.display_name}."
        )
        if len(description) > 160:
            description = description[:159].rsplit(" ", 1)[0] + "."
        pages.append(
            static_content_page(
                contributor_article(contributor, occurrences),
                meta=PageMeta(contributor.display_name, description, contributor.profile_path),
                current="",
            )
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
