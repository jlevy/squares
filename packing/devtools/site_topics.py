"""The shared topic vocabulary and chip labels for Results and News."""

from __future__ import annotations

import html
from typing import Literal

from devtools.check_results import KINDS, kind_label

# Precise result kinds keep their existing stable keys. News can also describe the
# project's capabilities, engineering and verification work.
TOPICS: dict[str, str] = {
    **{kind: kind_label(kind).capitalize() for kind in KINDS},
    "project": "Project",
    "engineering": "Engineering",
    "verification": "Verification",
}


def topic_label(topic: str) -> str:
    """One sentence-case label per stable topic key, on every reader surface."""
    if topic not in TOPICS:
        raise ValueError(f"unknown topic: {topic}")
    return TOPICS[topic]


def topic_chip(topic: str, *, attribute: Literal["data-kind", "data-news-topic"]) -> str:
    """Shared topic markup; consumers retain their existing filter attributes."""
    return (
        f'<span class="site-chip" {attribute}="{html.escape(topic, quote=True)}">'
        f"{html.escape(topic_label(topic))}</span>"
    )
