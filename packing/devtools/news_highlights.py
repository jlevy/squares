"""The homepage's newest three S5 results, from the existing result register."""

from __future__ import annotations

import re
from collections.abc import Mapping
from functools import partial

from devtools import overview_sections, render_changelog
from devtools.check_results import KINDS
from devtools.overview_data import BIBLIOGRAPHY, Overview, Result
from devtools.register_prose import paragraphs
from devtools.site_topics import NEWS_TOPICS
from sqpack.yamlio import safe_load

LIMIT = 3

# Result kinds stay precise; only the subset offered by News gets a topic chip.
TOPIC_BY_KIND = {kind: kind for kind in KINDS if kind in NEWS_TOPICS}


def highlights(overview: Overview) -> tuple[Result, ...]:
    """Keep the register's displayed-date and ID order, without an age cutoff."""
    return tuple(
        result
        for result in overview_sections.recent_results(overview)
        if overview_sections.significance(result) == 5
    )[:LIMIT]


def surname_text(text: str, names: Mapping[str, str]) -> str:
    """Shorten known names only for News, retaining full names when surnames collide."""
    people: dict[str, set[str]] = {}
    for full, surname in names.items():
        people.setdefault(surname, set()).add(full.partition(" (")[0])
    short: dict[str, str] = {}
    for full, surname in names.items():
        if full != surname and len(people[surname]) == 1:
            _, separator, handle = full.partition(" (")
            short[full] = surname + separator + handle
    if not short:
        return text
    pattern = re.compile(
        r"(?<!\w)(?:"
        + "|".join(re.escape(full) for full in sorted(short, key=len, reverse=True))
        + r")(?!\w)"
    )
    return pattern.sub(lambda match: short[match[0]], text)


def _article(result: Result, names: Mapping[str, str]) -> str:
    shorten = partial(surname_text, names=names)
    claim = render_changelog.inline_html(
        paragraphs(result.record["claim"])[0], transform_text=shorten
    )
    kind = result.record["kind"]
    topic = TOPIC_BY_KIND.get(kind)
    qualifier = (
        '<p class="site-result-meta">Reported result: this project has not verified '
        "the complete claim.</p>"
        if result.record["verification"] == "V0"
        else ""
    )
    header = render_changelog.news_article_header(
        render_changelog.inline_html(result.summary, allow_links=False, transform_text=shorten),
        overview_sections.first_day(result.dated[1]),
        [topic] if topic else [],
        {
            "score": overview_sections.significance(result),
            "rationale": surname_text(result.record["significance"]["rationale"], names),
        },
    )
    return (
        f'<article class="site-news-item" data-news-entry="{result.id}">'
        f"{header}"
        '<p class="site-result-status">'
        f"{overview_sections.ladder_chips(result)} "
        f"{overview_sections.status_marks(result)}</p>"
        f'<p class="site-result-meta">{overview_sections.credit_cell(result.credit)}</p>'
        f"{qualifier}<p>{claim}</p>"
        f'<p><a href="result/{result.id.lower()}.html">Full result '
        f"{result.id}</a></p></article>"
    )


def render(overview: Overview) -> str:
    """Give each selected result its own card, keeping every headline in the preview."""
    names = safe_load(BIBLIOGRAPHY.read_text(encoding="utf-8"))["credited_names"]
    cards = (
        render_changelog.news_card(
            f"news-result-{result.id.lower()}",
            overview_sections.first_day(result.dated[1]),
            _article(result, names),
        )
        for result in highlights(overview)
    )
    return '<div class="site-news sans-text" data-news>' + "\n".join(cards) + "</div>"
