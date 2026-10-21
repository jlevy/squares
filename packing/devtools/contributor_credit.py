"""HTML credit adapter: only explicit reviewed source spans become person links."""

from __future__ import annotations

import html
from functools import cache

from sqpack.contributor_occurrences import (
    CreditOrigin,
    OccurrenceError,
    OccurrenceRegistry,
    load_occurrences,
)
from sqpack.contributors import PROFILES_DIR


@cache
def occurrence_registry() -> OccurrenceRegistry:
    return load_occurrences()


def render_credit(
    origin: CreditOrigin,
    text: str,
    *,
    prefix: str = "",
    registry: OccurrenceRegistry | None = None,
) -> str:
    """Escape the original line and link its reviewed labels without choosing aliases."""
    registry = registry if registry is not None else occurrence_registry()
    pieces = []
    offset = 0
    for item in registry.by_origin.get(origin, ()):
        if item.expected_text != text:
            raise OccurrenceError(
                f"reviewed source text differs from rendered source text: {origin}"
            )
        pieces.append(html.escape(text[offset : item.start]))
        label = html.escape(item.label)
        if item.disposition == "resolved":
            identifier = html.escape(item.contributor_id or "", quote=True)
            href = html.escape(f"{prefix}{PROFILES_DIR}/{identifier}.html", quote=True)
            label = f'<a href="{href}">{label}</a>'
        pieces.append(label)
        offset = item.end
    pieces.append(html.escape(text[offset:]))
    return "".join(pieces)


def case_credit(
    n: int, field: str, names: list[str] | tuple[str, ...] | None, *, prefix: str = ""
) -> str:
    return ", ".join(
        render_credit(
            CreditOrigin(f"packing/frontier/n-{n:03d}.md", str(n), f"{field}/{index}"),
            name,
            prefix=prefix,
        )
        for index, name in enumerate(names or [])
    )
