"""Prepare the published site's mathematics once, with the pinned KaTeX renderer.

Kpress already supplies semantic MathML. This replaces its hidden TeX placeholder
with visual HTML using the same prose, sans and stock font metrics as the browser
adapter. Pages keep their semantic subtree and need no typesetting program.
"""

from __future__ import annotations

import html
import json
import shutil
import subprocess
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Literal, cast

Profile = Literal["prose", "sans", "katex"]
MathKey = tuple[str, bool, Profile, bool]
_DRIVER = Path(__file__).resolve().parent / "node" / "render-site-math.mjs"
_CACHE: dict[MathKey, str] = {}
_VOID = frozenset(
    [
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    ]
)
_SANS_CLASSES = frozenset(
    [
        "kpress-figcaption",
        "kpress-footnotes",
        "kpress-table",
        "sans-text",
        "description",
        "key-claims",
        "summary",
        "concepts",
        "claim",
        "para-caption",
        "tab-button",
        "kpress-tab-button",
        "site-table",
        "site-chip",
        "site-nav",
        "site-tabs",
    ]
)


@dataclass
class _Element:
    tag: str
    attrs: dict[str, str | None]
    start: int
    content: int
    profile: Profile


@dataclass(frozen=True)
class _Formula:
    start: int
    content: int
    end: int
    host_start: int | None
    host_content: int | None
    source: str
    display: bool
    profile: Profile


class _MathParser(HTMLParser):
    """Locate source placeholders without reading script/style text as markup."""

    def __init__(self, text: str) -> None:
        super().__init__(convert_charrefs=False)
        self.text = text
        self.lines = [0]
        self.lines.extend(index + 1 for index, char in enumerate(text) if char == "\n")
        self.stack: list[_Element] = []
        self.formulas: list[_Formula] = []

    def position(self) -> int:
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        inherited: Profile = self.stack[-1].profile if self.stack else "prose"
        classes = set((values.get("class") or "").split())
        if inherited == "katex" or any(
            values.get(name) in {"katex", "system"}
            for name in ("data-kpress-math-text", "data-kpress-fonts", "data-kpress-font-set")
        ):
            profile: Profile = "katex"
        elif values.get("data-math-face") == "serif":
            profile = "prose"
        elif (
            values.get("data-kpress-prose-font") == "sans"
            or classes & _SANS_CLASSES
            or tag in {"details", "figcaption", "th", "h1", "h2", "h3", "h4", "h5", "h6"}
        ):
            profile = "sans"
        else:
            profile = inherited
        start = self.position()
        content = start + len(self.get_starttag_text() or "")
        if "kpress-math" in classes and values.get("data-kpress-math-error") == "true":
            raise ValueError("unrenderable semantic mathematics in a published page")
        if tag not in _VOID:
            self.stack.append(_Element(tag, values, start, content, profile))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in _VOID:
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        matching = next(
            (i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i].tag == tag), None
        )
        if matching is None:
            return
        element = self.stack[matching]
        end = self.position()
        if "kpress-math-render" in (element.attrs.get("class") or "").split():
            host = next(
                (
                    node
                    for node in reversed(self.stack[:matching])
                    if "kpress-math" in (node.attrs.get("class") or "").split()
                ),
                None,
            )
            if host and host.attrs.get("data-kpress-math-rendered") != "true":
                source = html.unescape(self.text[element.content : end]).strip()
                display = host.attrs.get("data-kpress-math") == "display"
                opening, closing = (r"\[", r"\]") if display else (r"\(", r"\)")
                if not source.startswith(opening) or not source.endswith(closing):
                    raise ValueError("a published math placeholder has no TeX delimiters")
                self.formulas.append(
                    _Formula(
                        element.start,
                        element.content,
                        end,
                        host.start,
                        host.content,
                        source[2:-2],
                        display,
                        element.profile,
                    )
                )
        elif {"tex", "tex-d"} & set((element.attrs.get("class") or "").split()):
            if (
                element.attrs.get("data-kpress-math-prepared") != "true"
                and "katex-html" not in self.text[element.content : end]
            ):
                source = html.unescape(self.text[element.content : end]).strip()
                self.formulas.append(
                    _Formula(
                        element.start,
                        element.content,
                        end,
                        None,
                        None,
                        source,
                        "tex-d" in (element.attrs.get("class") or "").split(),
                        element.profile,
                    )
                )
        del self.stack[matching:]


def _render(keys: list[MathKey]) -> None:
    """One checked Node call for all previously unseen formulas in a page."""
    from devtools.render_n11_lower_bounds_explainer import kpress_static  # noqa: PLC0415

    node = shutil.which("node")
    if node is None:
        raise ValueError("Node.js is required to prepare the site's mathematics")
    static = kpress_static() / "katex"
    payload = {
        "bundle": str(static / "katex.min.js"),
        "metrics": str(static / "katex-text-metrics.js"),
        "formulas": [
            {"source": source, "display": display, "profile": profile, "semantic": semantic}
            for source, display, profile, semantic in keys
        ],
    }
    try:
        result = subprocess.run(
            [node, str(_DRIVER)],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            check=True,
            timeout=60,
        )
    except subprocess.CalledProcessError as error:
        raise ValueError(f"static mathematics failed: {error.stderr.strip()}") from error
    rendered = cast(list[str], json.loads(result.stdout))
    if len(rendered) != len(keys) or not all(
        isinstance(item, str) and "katex-html" in item for item in rendered
    ):
        raise ValueError("the static mathematics renderer returned incomplete output")
    _CACHE.update(zip(keys, rendered, strict=True))


def prepare(page: str) -> str:
    """Return visual and semantic mathematics ready to read before any script runs."""
    parser = _MathParser(page)
    parser.feed(page)
    parser.close()
    missing: list[MathKey] = list(
        dict.fromkeys(
            (formula.source, formula.display, formula.profile, formula.host_start is None)
            for formula in parser.formulas
            if (formula.source, formula.display, formula.profile, formula.host_start is None)
            not in _CACHE
        )
    )
    if missing:
        _render(missing)
    changes: list[tuple[int, int, str]] = []
    for formula in parser.formulas:
        visual = _CACHE[
            formula.source, formula.display, formula.profile, formula.host_start is None
        ]
        opening = page[formula.start : formula.content]
        opening = (
            opening[:-1]
            + f' data-kpress-math-face="{formula.profile}" data-kpress-math-prepared="true">'
        )
        changes.append((formula.start, formula.end, opening + visual))
        if formula.host_start is not None and formula.host_content is not None:
            host = page[formula.host_start : formula.host_content]
            host = host[:-1] + ' data-kpress-math-rendered="true">'
            changes.append((formula.host_start, formula.host_content, host))
    pieces: list[str] = []
    cursor = 0
    for start, end, replacement in sorted(changes):
        pieces.extend((page[cursor:start], replacement))
        cursor = end
    pieces.append(page[cursor:])
    return "".join(pieces)
