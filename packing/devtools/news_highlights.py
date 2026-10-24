"""The home page's News box: the newest News articles at the significance a reader picks.

The box shows `LIMIT` articles, newest first, drawn with the News archive's own card
renderer and its significance filter in the compact form (`render_changelog.news_filters`),
small and at the right above the cards. Which levels it opens on is decided at render time
from the archive (`default_levels`): S5 alone where News holds at least `LIMIT` S5
articles, so the box is full of them, and otherwise S4 and S5, the levels the archive
itself opens on (`render_changelog.NEWS_LEVELS`). That is the owner's rule of 22 October
2026 (think-s38d): "preselected to S5 when there are enough S5 items for the box, else
S4+S5". It reads no date, so a render is the same bytes on any day and the opening moves
only as articles arrive. An earlier reading that also required the three to fall within 30
days was a coordinator's answer to #736's review A (finding A4), never the owner's, and
review B (finding B1) retired it.

A reader widens or narrows the choice, and `news-filters.js` then shows the newest
`LIMIT` that match and says how many in a visually hidden live count; the box carries,
for that, the newest `LIMIT` articles at each level News has (`carried`), the ones
outside the opening choice hidden. Without scripts the box shows the opening choice and
no filter. The choice is not kept in the home page's address; its "All News" link
carries it to the archive as `news-s` (`data-news-carry`) when the reader has changed it.
With no article to show, the box says "No news yet." and draws no filter.
"""

from __future__ import annotations

from devtools import render_changelog

#: How many articles the box shows at once.
LIMIT = 3


def _score(entry: render_changelog.Document) -> int:
    return render_changelog.entry_significance(entry)["score"]


def default_levels(document: render_changelog.Document) -> tuple[int, ...]:
    """The levels the box opens on: S5 alone where News holds at least `LIMIT` S5
    articles, and otherwise the archive's own opening levels, S4 and S5."""
    fives = sum(1 for entry in render_changelog.news_entries(document) if _score(entry) == 5)
    return (5,) if fives >= LIMIT else render_changelog.NEWS_LEVELS


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


def highlights(document: render_changelog.Document) -> tuple[render_changelog.Document, ...]:
    """The articles the box shows first, newest first: the newest `LIMIT` at the levels
    it opens on (`default_levels`), in their frozen News date and ID order."""
    levels = default_levels(document)
    return tuple(entry for entry in carried(document) if _score(entry) in levels)[:LIMIT]


def render(document: render_changelog.Document) -> str:
    """The box: every carried article through the archive's complete card renderer,
    under the compact significance filter preselected to the opening levels."""
    return render_changelog.render_news(
        document,
        limit=LIMIT,
        entry_ids={entry["id"] for entry in carried(document)},
        selected=default_levels(document),
    )
