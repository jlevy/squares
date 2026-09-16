"""Validate that a generated HTML page needs no external resources.

Two layers, because neither is enough alone. This scan reads the markup, the CSS and the
script text for every construct that fetches: URL-bearing attributes (SVG's `href` and
`xlink:href` included), CSS `url(` and `@import` wherever they are written, and the script
APIs that make a request. It cannot parse JavaScript, so it recognises the call shapes and
nothing more. The published page therefore also carries a `default-src 'none'`
Content-Security-Policy (`build_site.CONTENT_SECURITY_POLICY`), under which the browser
itself refuses any request the scan could not see.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser

_CSS_RESOURCE = re.compile(
    r"@import\b|url\(\s*(?![\"']?(?:data:|#))",
    re.IGNORECASE,
)
#: A CSS `url(` written inside script text. Unlike in a stylesheet, it must not be the tail
#: of an identifier: `URL.createObjectURL(` makes a local blob and requests nothing.
_SCRIPT_CSS_URL = re.compile(r"(?<![\w$.])url\(\s*(?![\"'`]?(?:data:|#))", re.IGNORECASE)
#: Script calls that request a resource. Matched on the call shape, not parsed: a type
#: import in a JSDoc comment (`import("./api/pack-api.js")`) names a module for `tsc` and
#: is not matched, which is why a dynamic `import(` counts only with an absolute URL -- a
#: relative one is refused by the page's policy, which grants scripts no source at all.
_SCRIPT_REQUEST = re.compile(
    r"(?<![\w$.])fetch\s*\("
    r"|\bXMLHttpRequest\b"
    r"|\bnew\s+(?:Shared)?Worker\s*\("
    r"|\bnew\s+WebSocket\s*\("
    r"|\bnew\s+EventSource\s*\("
    r"|\bsendBeacon\s*\("
    r"|\bimportScripts\s*\("
    r"|(?<![\w$.])import\s*\(\s*[\"'`](?:[a-z][a-z0-9+.-]*:|//)",
    re.IGNORECASE,
)
#: A data island is data, not script: `<script type="application/json">`.
_DATA_TYPES = frozenset({"application/json", "application/ld+json"})
_FETCH_ATTRIBUTES = {
    "audio": ("src",),
    "embed": ("src",),
    "feimage": ("href", "xlink:href"),
    "iframe": ("src",),
    "image": ("href", "xlink:href"),
    "img": ("src", "srcset"),
    "object": ("data",),
    "source": ("src", "srcset"),
    "track": ("src",),
    "use": ("href", "xlink:href"),
    "video": ("poster", "src"),
}
#: References that stay inside the page: an in-document fragment and inline data.
_LOCAL_PREFIXES = ("data:", "#")


class _ResourceParser(HTMLParser):
    """Collect fetch-bearing markup, CSS and script calls."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.findings: list[str] = []
        self._style_depth = 0
        self._script_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name.casefold(): value for name, value in attrs}
        folded = tag.casefold()
        if folded == "style":
            self._style_depth += 1
        if folded == "script":
            if values.get("src") is not None:
                self.findings.append("script src")
            if (values.get("type") or "").strip().casefold() not in _DATA_TYPES:
                self._script_depth += 1
        if folded == "link" and values.get("href") is not None:
            relationships = set((values.get("rel") or "").casefold().split())
            if "canonical" not in relationships:
                self.findings.append("link href")
        for attribute in _FETCH_ATTRIBUTES.get(folded, ()):
            value = values.get(attribute)
            if value is not None and not value.lstrip().casefold().startswith(_LOCAL_PREFIXES):
                self.findings.append(f"{folded} {attribute}")
        inline_style = values.get("style")
        if inline_style is not None:
            self._check_css(inline_style)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.casefold() == "style":
            self._style_depth -= 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "style":
            self._style_depth = max(0, self._style_depth - 1)
        if tag.casefold() == "script":
            self._script_depth = max(0, self._script_depth - 1)

    def handle_data(self, data: str) -> None:
        if self._style_depth:
            self._check_css(data)
        if self._script_depth:
            # CSS assembled in script reaches the page as a `url(` the markup never shows.
            request = _SCRIPT_CSS_URL.search(data) or _SCRIPT_REQUEST.search(data)
            if request is not None:
                self.findings.append(f"script {request.group(0).strip()}")

    def _check_css(self, css: str) -> None:
        match = _CSS_RESOURCE.search(css)
        if match is not None:
            self.findings.append(match.group(0))


def external_resources(page: str) -> list[str]:
    """Return resource-bearing HTML/CSS constructs that reach outside the page."""
    parser = _ResourceParser()
    parser.feed(page)
    parser.close()
    return parser.findings


def assert_self_contained_html(page: str) -> None:
    """Raise when displaying ``page`` would fetch a resource outside itself."""
    findings = external_resources(page)
    if findings:
        raise ValueError(
            f"the page references {len(findings)} resource(s) outside itself: "
            + ", ".join(findings)
        )
