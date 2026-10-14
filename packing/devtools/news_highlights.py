"""The homepage's newest three S5 results, from the existing result register."""

from __future__ import annotations

from devtools import overview_sections, render_changelog
from devtools.check_results import KINDS
from devtools.overview_data import Overview, Result, prose_html, tex_bounds

LIMIT = 3

# Result highlights retain the precise registered kind from the shared vocabulary.
TOPIC_BY_KIND = {kind: kind for kind in KINDS}


def highlights(overview: Overview) -> tuple[Result, ...]:
    """Keep the register's displayed-date and ID order, without an age cutoff."""
    return tuple(
        result
        for result in overview_sections.recent_results(overview)
        if overview_sections.significance(result) == 5
    )[:LIMIT]


def _article(result: Result) -> str:
    claim = prose_html(result.record["claim"], between="</p><p>")
    rationale = prose_html(result.record["significance"]["rationale"], between="</p><p>")
    kind = result.record["kind"]
    topic = TOPIC_BY_KIND.get(kind)
    qualifier = (
        '<p class="site-result-meta">Reported result: this project has not verified '
        "the complete claim.</p>"
        if result.record["verification"] == "V0"
        else ""
    )
    header = render_changelog.news_article_header(
        tex_bounds(result.summary),
        overview_sections.first_day(result.dated[1]),
        [topic] if topic else [],
        {
            "score": overview_sections.significance(result),
            "rationale": result.record["significance"]["rationale"],
        },
    )
    return (
        f'<article class="site-news-item" data-news-entry="{result.id}">'
        f"{header}"
        '<p class="site-result-status">'
        f"{overview_sections.ladder_chips(result)} "
        f"{overview_sections.kind_and_status(result)}</p>"
        f'<p class="site-result-meta">{overview_sections.credit_cell(result.credit)}</p>'
        f"{qualifier}<p>{claim}</p><p>{rationale}</p>"
        f'<p><a href="result/{result.id.lower()}.html">Full result '
        f"{result.id}</a></p></article>"
    )


def render(overview: Overview) -> str:
    """Give each selected result its own card, keeping every headline in the preview."""
    cards = (
        render_changelog.news_card(
            f"news-result-{result.id.lower()}",
            overview_sections.first_day(result.dated[1]),
            _article(result),
        )
        for result in highlights(overview)
    )
    return '<div class="site-news sans-text" data-news>' + "\n".join(cards) + "</div>"
