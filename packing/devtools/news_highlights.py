"""The home page's News box: the newest News articles at the significance a reader picks.

The box shows `LIMIT` articles, newest first, drawn with the News archive's own card
renderer and its significance filter in the compact form (`render_changelog.news_filters`),
small and at the right above the cards. Which levels it opens on is decided at render time
(`default_levels`; the owner, 22 October 2026, and #736's review A, finding A4): S5 alone
where the `LIMIT` newest S5 articles all fall within `FRESH_DAYS` of the build's
reference day, so the box is full of current S5 news, and otherwise S4 and S5, the levels
the archive itself opens on (`render_changelog.NEWS_LEVELS`). The reference day is the
newest day the build's records say anything reached `main`
(`overview_sections.record_reference`), never the clock, so a render is the same bytes on
any day and the rule moves on its own as articles arrive and age.

A reader widens or narrows the choice, and `news-filters.js` then shows the newest
`LIMIT` that match and says how many in a visually hidden live count; the box carries,
for that, the newest `LIMIT` articles at each level News has (`carried`), the ones
outside the opening choice hidden. Without scripts the box shows the opening choice and
no filter. The choice is not kept in the home page's address; its "View All News" link
carries it to the archive as `news-s` (`data-news-carry`) when the reader has changed it.
With no article to show, the box says "No news yet." and draws no filter.
"""

from __future__ import annotations

from datetime import date, timedelta

from devtools import render_changelog

#: How many articles the box shows at once.
LIMIT = 3
#: How recent, in days before the reference day, each of the `LIMIT` newest S5 articles
#: must be for the box to open on S5 alone (#736's review A, finding A4).
FRESH_DAYS = 30


def _score(entry: render_changelog.Document) -> int:
    return render_changelog.entry_significance(entry)["score"]


def _reference(reference: date | None) -> date:
    """The given reference day, or the build's own (`record_reference`)."""
    if reference is not None:
        return reference
    from devtools.overview_sections import record_reference  # noqa: PLC0415

    return record_reference()


def default_levels(
    document: render_changelog.Document, reference: date | None = None
) -> tuple[int, ...]:
    """The levels the box opens on: S5 alone where the `LIMIT` newest S5 articles all
    fall within `FRESH_DAYS` of `reference`, the build's reference day unless given, and
    otherwise the archive's own opening levels, S4 and S5."""
    cutoff = _reference(reference) - timedelta(days=FRESH_DAYS)
    fives = [entry for entry in render_changelog.news_entries(document) if _score(entry) == 5]
    newest = fives[:LIMIT]
    fresh = len(newest) == LIMIT and all(
        date.fromisoformat(str(entry["date"])) >= cutoff for entry in newest
    )
    return (5,) if fresh else render_changelog.NEWS_LEVELS


def carried(document: render_changelog.Document) -> tuple[render_changelog.Document, ...]:
    """Every article the box carries, in News order: the newest `LIMIT` at each level
    News has, so any choice of levels finds its newest `LIMIT`."""
    taken: dict[int, int] = {}
    kept = []
    for entry in render_changelog.news_entries(document):
        level = _score(entry)
        if taken.get(level, 0) < LIMIT:
            taken[level] = taken.get(level, 0) + 1
            kept.append(entry)
    return tuple(kept)


def highlights(
    document: render_changelog.Document, reference: date | None = None
) -> tuple[render_changelog.Document, ...]:
    """The articles the box shows first, newest first: the newest `LIMIT` at the levels
    it opens on (`default_levels`), in their frozen News date and ID order."""
    levels = default_levels(document, reference)
    return tuple(entry for entry in carried(document) if _score(entry) in levels)[:LIMIT]


def render(document: render_changelog.Document, reference: date | None = None) -> str:
    """The box: every carried article through the archive's complete card renderer,
    under the compact significance filter preselected to the opening levels."""
    return render_changelog.render_news(
        document,
        limit=LIMIT,
        entry_ids={entry["id"] for entry in carried(document)},
        selected=default_levels(document, reference),
    )
