"""The homepage's newest S5 result announcements, shared with the News archive."""

from __future__ import annotations

from devtools import render_changelog

LIMIT = 3


def highlights(document: render_changelog.Document) -> tuple[render_changelog.Document, ...]:
    """Keep eligible result announcements in their frozen News date and ID order."""
    return tuple(
        entry
        for entry in render_changelog.news_entries(document)
        if entry.get("result_ids") and render_changelog.entry_significance(entry)["score"] == 5
    )[:LIMIT]


def render(document: render_changelog.Document) -> str:
    """Show the selected articles through the archive's complete card renderer."""
    return render_changelog.render_news(
        document, limit=LIMIT, entry_ids={entry["id"] for entry in highlights(document)}
    )
