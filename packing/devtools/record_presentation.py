"""One current-record tally across person tables, profiles and project cards."""

from __future__ import annotations

import html
from collections.abc import Iterable, Mapping
from functools import cache

from devtools.profile_records import RecordIndex, current_record_ids, load_record_index
from devtools.site_tallies import render_tally, tally_results


@cache
def record_index() -> RecordIndex:
    """Share the canonical classification across every surface in one build."""
    return load_record_index()


def record_tally(
    authored_ids: Iterable[str],
    measures: Mapping[str, tuple[int, str]],
    *,
    index: RecordIndex | None = None,
    total_href: str | None = None,
    pending_href: str | None = None,
    blank_zero: bool = False,
) -> str:
    """Supported totals never absorb unresolved comparisons or imply a false zero."""
    index = record_index() if index is None else index
    authored = set(authored_ids)
    current = current_record_ids(authored, index)
    pending = sorted(authored.intersection(index.unresolved).difference(index.current_results))
    rendered = (
        render_tally(
            tally_results(current, measures, (5, 4, 3, 2, 1)),
            noun="record",
            total_href=total_href if current else None,
        )
        if current or not (blank_zero or pending)
        else ""
    )
    if pending:
        reasons = "; ".join(
            f"{identifier}: {reason}"
            for identifier in pending
            for reason in index.unresolved[identifier]
        )
        label = "Review pending"
        if pending_href:
            label = f'<a href="{html.escape(pending_href, quote=True)}">{label}</a>'
        pending_note = (
            f'<span class="site-record-pending" title="{html.escape(reasons, quote=True)}">'
            f"{label}</span>"
        )
        rendered += (" · " if rendered else "") + pending_note
    return rendered
