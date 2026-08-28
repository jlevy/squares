#!/usr/bin/env python3
"""Network-free controls for the metadata-only Kingbird live-audit workflow."""

from __future__ import annotations

from typing import cast

from devtools.audit_kingbird_catalogue import audit_catalogue, source_groups, source_quirks


def _synthetic_source(source_n: int) -> bytes:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        f'<defs><rect id="outer" width="{source_n}" height="{source_n}" '
        'fill="none"/></defs>'
        f'<rect width="{source_n}" height="1"/>'
        "</svg>"
    ).encode()


def test_live_audit_covers_all_groups_without_emitting_geometry() -> None:
    groups = source_groups()
    expected = {group.source_path: group.source_n for group in groups}

    audit = audit_catalogue(
        fetch=lambda source_path: _synthetic_source(expected[source_path]),
        checked_at="2026-08-26T06:00:00+00:00",
        jobs=4,
    )

    assert len(groups) == 114
    assert audit["summary"] == {
        "adapter_failed": 0,
        "adapter_passed": 114,
        "source_groups": 114,
        "svg_responses": 114,
    }
    sources = cast(list[dict[str, object]], audit["sources"])
    assert all(record["adapter_status"] == "passed" for record in sources)
    assert "poses" not in str(audit)
    assert "coordinates" not in str(audit)
    assert "sha256" not in str(audit)


def test_live_audit_describes_bounded_source_recovery_quirks() -> None:
    text = (
        '<svg xmlns="http://www.w3.org/2000/svg">'
        '<rect id="one"/><g id="two"><rect id="one"/></g>'
        '<g id="corner"/><use href="corner"/>'
        "</svg>"
    )

    assert source_quirks(text) == [
        {"kind": "duplicate-id-first-in-tree-order", "identifiers": ["one"]},
        {
            "kind": "bare-local-use-ignored-after-count-reconciliation",
            "identifiers": ["corner"],
        },
    ]
