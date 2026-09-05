"""The explainer renders, and what it renders fetches nothing.

`devtools.render_certificate_page` was exercised only by the Pages workflow, on the pull
requests whose paths its filters name; nothing in the suite rendered the page. A full
render is under a second, so it runs here, and the two properties the workflow used to
grep for are asserted on the string the renderer returns: no placeholder survived
substitution, and nothing in the page is a reference outside it.
"""

from __future__ import annotations

import re

import pytest

from devtools.render_certificate_page import WALKTHROUGH, assert_self_contained, render
from devtools.render_certificate_page import load_certificate as load


@pytest.fixture(scope="module")
def page() -> str:
    return render(WALKTHROUGH)


def test_the_page_renders_every_walkthrough_certificate(page: str) -> None:
    """Each certificate's slug is in the page: its switch button and its figure copies."""

    for path in WALKTHROUGH:
        certificate, _ = load(path)
        fragment = f"{certificate.outer_side.numerator}-{certificate.outer_side.denominator}"
        assert f'data-cert="{fragment}"' in page, fragment


def test_no_placeholder_survives_substitution(page: str) -> None:
    assert re.findall(r"\{\{[A-Z_]+\}\}", page) == []


def test_the_page_is_self_contained(page: str) -> None:
    """The renderer's own check passes on its own output; the workflow relies on this."""

    assert_self_contained(page)
    assert "<link" not in page
    assert re.search(r"<script[^>]*\ssrc=", page) is None


@pytest.mark.parametrize(
    "fragment",
    [
        '<script src="https://cdn.example/x.js"></script>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=X">',
        "<style>@import url(https://example.org/a.css);</style>",
        "<style>body { background: url(https://example.org/a.png) }</style>",
        "<style>body { background: url('//example.org/a.png') }</style>",
    ],
)
def test_an_external_reference_is_refused(fragment: str) -> None:
    with pytest.raises(SystemExit, match="not self-contained"):
        assert_self_contained(f"<html><body>{fragment}</body></html>")


@pytest.mark.parametrize(
    "fragment",
    [
        "<style>@font-face { src: url(data:font/woff2;base64,AAAA) }</style>",
        "<style>.a { fill: url(#gradient) }</style>",
        '<style>.b { background: url("data:image/svg+xml,%3Csvg%3E") }</style>',
    ],
)
def test_a_data_uri_or_fragment_is_not_a_fetch(fragment: str) -> None:
    assert_self_contained(f"<html><body>{fragment}</body></html>")
