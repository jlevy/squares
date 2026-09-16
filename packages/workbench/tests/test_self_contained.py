"""The workbench self-containment check reads markup and CSS, not JavaScript text."""

from pathlib import Path

import pytest

from workbench_tools.build_site import (
    CONTENT_SECURITY_POLICY,
    POLICY_META,
    dirty_metadata,
    with_policy,
)
from workbench_tools.self_contained import assert_self_contained_html


def test_dirty_metadata_is_explicit() -> None:
    assert dirty_metadata(dirty=True) == (
        '<meta name="squares-workbench-dirty" content="true">'
    )
    assert dirty_metadata(dirty=False) == (
        '<meta name="squares-workbench-dirty" content="false">'
    )


@pytest.mark.parametrize(
    "fragment",
    [
        '<script src="https://example.test/app.js"></script>',
        '<link rel="stylesheet" href="https://example.test/app.css">',
        "<style>@import 'https://example.test/app.css';</style>",
        "<style>.mark { background: url(https://example.test/mark.svg); }</style>",
        '<div style="background: url(../mark.svg)"></div>',
        '<img src="https://example.test/mark.svg">',
        # SVG's own fetch-bearing references (#125 F21).
        '<svg><image href="https://example.test/mark.png"></image></svg>',
        '<svg><image xlink:href="https://example.test/mark.png"/></svg>',
        '<svg><use href="https://example.test/sprite.svg#mark"></use></svg>',
        '<svg><filter><feImage href="https://example.test/mark.png"/></filter></svg>',
    ],
)
def test_external_resource_is_refused(fragment: str) -> None:
    with pytest.raises(ValueError, match="outside itself"):
        assert_self_contained_html(f"<html><body>{fragment}</body></html>")


@pytest.mark.parametrize(
    "fragment",
    [
        '<script>URL.createObjectURL(new Blob(["ok"]));</script>',
        '<link rel="canonical" href="https://example.test/workbench/">',
        '<a href="https://example.test/explainer/">explainer</a>',
        "<style>.font { src: url(data:font/woff2;base64,AAAA); }</style>",
        "<style>.mark { fill: url(#gradient); }</style>",
        '<img src="data:image/svg+xml;base64,AAAA">',
        '<svg><use href="#mark"></use><image href="data:image/png;base64,AAAA"/></svg>',
        '<script id="data" type="application/json">{"note": "no requests here"}</script>',
    ],
)
def test_local_or_nonfetch_reference_is_allowed(fragment: str) -> None:
    assert_self_contained_html(f"<html><body>{fragment}</body></html>")


#: Pages whose scripts request or assemble a resource the markup never shows (#160 R22), and
#: scripts that only look like it. Kept as files because a script body written as a Python
#: string is exactly what the repository's no-JavaScript-in-Python rule forbids.
FIXTURES = Path(__file__).with_name("fixtures") / "self-contained"


@pytest.mark.parametrize(
    "fixture", sorted((FIXTURES / "refused").glob("*.html")), ids=lambda path: path.stem
)
def test_a_resource_requested_by_script_is_refused(fixture: Path) -> None:
    page = fixture.read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="outside itself"):
        assert_self_contained_html(f"<html><body>{page}</body></html>")


@pytest.mark.parametrize(
    "fixture", sorted((FIXTURES / "allowed").glob("*.html")), ids=lambda path: path.stem
)
def test_a_script_that_requests_nothing_is_allowed(fixture: Path) -> None:
    assert_self_contained_html(
        f"<html><body>{fixture.read_text(encoding='utf-8')}</body></html>"
    )


def test_the_script_fixtures_are_present() -> None:
    assert len(list((FIXTURES / "refused").glob("*.html"))) == 8
    assert len(list((FIXTURES / "allowed").glob("*.html"))) == 2


def test_the_published_page_carries_a_policy_that_grants_no_network_source() -> None:
    """The second layer (#125 F21): whatever the scan misses, the browser refuses."""
    page = with_policy('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">')
    head = page.index("<head>") + len("<head>")
    assert page[head:].lstrip().startswith(POLICY_META), "the policy must precede everything"
    directives = {
        part.split()[0]: part.split()[1:]
        for part in CONTENT_SECURITY_POLICY.split(";")
        if part.strip()
    }
    assert directives["default-src"] == ["'none'"]
    granted = [source for sources in directives.values() for source in sources]
    assert set(granted) <= {"'none'", "'unsafe-inline'", "data:", "blob:"}
    assert "'unsafe-eval'" not in granted, "the public page is not loosened for test tooling"
    assert "connect-src" not in directives, "requests fall to default-src 'none'"
    assert page.count("Content-Security-Policy") == 1


def test_a_page_without_a_head_cannot_carry_the_policy() -> None:
    with pytest.raises(ValueError, match="head"):
        with_policy("<html><body></body></html>")
