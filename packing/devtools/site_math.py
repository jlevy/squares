"""Prepare the published site's mathematics once, with the pinned KaTeX renderer.

Kpress already supplies semantic MathML. This replaces its hidden TeX placeholder
with visual HTML using the same prose, sans and stock font metrics as the browser
adapter. Pages keep their semantic subtree and need no typesetting program.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Literal, cast

Profile = Literal["prose", "sans", "katex"]
Choice = Literal["prose", "sans", "serif", "katex"]
MathKey = tuple[str, bool, Profile, bool]
_DRIVER = Path(__file__).resolve().parent / "node" / "render-site-math.mjs"
_CACHE: dict[MathKey, str] = {}
_RENDERER_VERSION: str | None = None
_STYLES: dict[str, tuple[str, str, str]] = {}
_CSS = Path(__file__).resolve().parent / "templates" / "site-math.css"
_PROFILES: tuple[Profile, ...] = ("prose", "sans", "katex")
_TAG = re.compile(r"(<[^>]+>)")
_STYLE = re.compile(r' style="([^"]*)"')
_STYLE_CLASS = re.compile(r"\bsm[0-9a-f]{10}\b")
_SANS_SELECTOR = (
    ':is([data-site-math="sans"], [data-kpress-prose-font="sans"] [data-site-math="prose"])'
)
_STOCK_SELECTOR = (
    ':is([data-site-math="katex"], '
    '[data-kpress-font-set="system"] [data-site-math], '
    '.kpress[data-kpress-fonts="system"] [data-site-math])'
)
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
        "site-title",
        "subtitle",
        "site-colophon",
        "site-card-foot",
        "site-popover",
        "site-popover-close",
        "site-popover-action",
        "site-action",
        "site-action-row",
        "site-card-label",
        "site-card-value",
        "site-popover-value",
        "site-card-note",
        "site-card-url",
        "site-table-tools",
        "site-detail",
        "site-records",
        "site-significance",
        "site-atlas-note",
        "site-rung-legend",
        "site-cell-quiet",
        "site-corrects",
        "site-approx",
        "site-frontier-same",
        "site-ladders",
        "site-atlas-legend",
        "site-atlas-n",
        "site-case-head",
        "site-case-summary-facts",
        "site-case-bound",
        "site-case-note",
        "site-case-data",
        "site-case-heading",
        "site-case-index",
        "site-film-note",
        "site-result",
    ]
)


@dataclass
class _Element:
    tag: str
    attrs: dict[str, str | None]
    start: int
    content: int
    profile: Choice


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
    choice: Choice


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
        inherited: Choice = self.stack[-1].profile if self.stack else "prose"
        classes = set((values.get("class") or "").split())
        if inherited == "katex" or any(
            values.get(name) in {"katex", "system"}
            for name in ("data-kpress-math-text", "data-kpress-fonts", "data-kpress-font-set")
        ):
            profile: Choice = "katex"
        elif values.get("data-math-face") == "serif":
            profile = "serif"
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
                        "prose" if element.profile == "serif" else element.profile,
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
                        "prose" if element.profile == "serif" else element.profile,
                        element.profile,
                    )
                )
        del self.stack[matching:]


def _render(keys: list[MathKey]) -> None:
    """One checked Node call for all previously unseen formulas in a page."""
    from devtools.render_n11_lower_bounds_explainer import kpress_static  # noqa: PLC0415

    global _RENDERER_VERSION  # noqa: PLW0603
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
    output = cast(dict[str, object], json.loads(result.stdout))
    expected = (static / "VERSION").read_text(encoding="utf-8").split()[-1]
    if not isinstance(output, dict) or output.get("version") != expected:
        raise ValueError("the static mathematics renderer does not match its pinned version")
    rendered = output.get("rendered")
    if (
        not isinstance(rendered, list)
        or len(rendered) != len(keys)
        or not all(isinstance(item, str) and "katex-html" in item for item in rendered)
    ):
        raise ValueError("the static mathematics renderer returned incomplete output")
    _RENDERER_VERSION = expected
    _CACHE.update(zip(keys, cast(list[str], rendered), strict=True))


def _style_class(styles: tuple[str, str, str]) -> str:
    """Stable classes share metric declarations without copying their visual tree."""
    name = "sm" + hashlib.sha256("\0".join(styles).encode()).hexdigest()[:10]
    previous = _STYLES.setdefault(name, styles)
    if previous != styles:
        raise ValueError("static mathematics style-class collision")
    return name


def _styled_tag(tag: str, styles: tuple[str, str, str]) -> str:
    if not any(styles):
        return tag
    name = _style_class(styles)
    tag = _STYLE.sub("", tag)
    if ' class="' in tag:
        return tag.replace(' class="', f' class="{name} ', 1)
    return tag.replace(">", f' class="{name}">', 1)


def _compact_visual(visual: str) -> str:
    """Move repeated inline KaTeX styles into the page's static stylesheet."""
    return _TAG.sub(
        lambda match: _styled_tag(
            match[0],
            (style[1], style[1], style[1])
            if (style := _STYLE.search(match[0]))
            else ("", "", ""),
        ),
        visual,
    )


def _tag_styles(parts: tuple[str, ...]) -> tuple[str, str, str] | None:
    declarations = []
    for part in parts:
        style = _STYLE.search(part)
        declarations.append(
            {
                item.partition(":")[0]: item.partition(":")[2]
                for item in style[1].split(";")
                if item
            }
            if style
            else {}
        )
    properties = set().union(*(value.keys() for value in declarations))
    for part, values in zip(parts, declarations, strict=True):
        for missing in properties - values.keys():
            # KaTeX's strut is an inline-block with the CSS initial baseline when
            # stock glyphs need no explicit vertical correction. Spell that value
            # out so each profile has an exact delta on the shared strut.
            if missing == "vertical-align" and 'class="strut"' in part:
                values[missing] = "baseline"
            elif missing == "margin-right" and "mathnormal" in part:
                # A zero italic correction is omitted from stock output. Math
                # glyphs have no stylesheet margin, so 0 is the identical value.
                values[missing] = "0em"
            else:
                return None
    return cast(
        tuple[str, str, str],
        tuple(
            "".join(f"{name}:{value};" for name, value in items.items())
            for items in declarations
        ),
    )


def merge_profiles(variants: tuple[str, str, str]) -> str:
    """Share identical DOM topology; retain exact copies when topology differs."""
    tokens = [_TAG.split(visual) for visual in variants]
    skeletons = [[_STYLE.sub("", token) for token in parts] for parts in tokens]
    styles = (
        [_tag_styles(parts) for parts in zip(*tokens, strict=True)]
        if len({len(parts) for parts in tokens}) == 1
        else []
    )
    if skeletons[0] == skeletons[1] == skeletons[2] and all(
        style is not None for style in styles
    ):
        shared = []
        for parts, declarations in zip(zip(*tokens, strict=True), styles, strict=True):
            tag = parts[0]
            if tag.startswith("<"):
                assert declarations is not None
                tag = _styled_tag(tag, declarations)
            shared.append(tag)
        return "".join(shared)
    # Identical fallback versions still share one subtree, selected by either profile.
    groups: dict[str, list[str]] = {}
    for profile, visual in zip(_PROFILES, variants, strict=True):
        groups.setdefault(visual, []).append(profile)
    return "".join(
        f'<span class="site-math-variant" data-site-math-profile="{" ".join(profiles)}">'
        f"{_compact_visual(visual)}</span>"
        for visual, profiles in groups.items()
    )


def _profile_keys(formula: _Formula) -> tuple[MathKey, ...]:
    profiles: tuple[Profile, ...] = (
        ("katex",)
        if formula.choice == "katex"
        else (formula.profile, "katex")
        if formula.choice in {"sans", "serif"}
        else _PROFILES
    )
    visual: tuple[MathKey, ...] = tuple(
        (formula.source, formula.display, profile, False) for profile in profiles
    )
    if formula.host_start is None:
        return (*visual, (formula.source, formula.display, formula.profile, True))
    return visual


def _visual(formula: _Formula) -> str:
    needed = {key[2] for key in _profile_keys(formula) if not key[3]}
    variants = tuple(
        _CACHE[
            formula.source,
            formula.display,
            profile if profile in needed else formula.profile,
            False,
        ]
        for profile in _PROFILES
    )
    visual = merge_profiles(cast(tuple[str, str, str], variants))
    if formula.host_start is None:
        semantic = _CACHE[formula.source, formula.display, formula.profile, True]
        match = re.search(r'<span class="katex-mathml">.*?</math></span>', semantic, re.DOTALL)
        if match is None:
            raise ValueError("standalone mathematics has no semantic MathML")
        visual = match[0] + visual
    return visual


def _stylesheet(page: str) -> str:
    """Select metric deltas using the same prepaint reader state as the glyph faces."""
    rules: list[str] = [_CSS.read_text(encoding="utf-8")]
    names = sorted(set(_STYLE_CLASS.findall(page)) & _STYLES.keys())
    for index, prefix in enumerate(("[data-site-math]", _SANS_SELECTOR, _STOCK_SELECTOR)):
        for name in names:
            styles = _STYLES[name]
            if index and styles[0] == styles[1] == styles[2]:
                continue
            # Specificity preserves the precedence that KaTeX's inline styles had.
            selector = f"{prefix} .{name}.{name}.{name}.{name}"
            rules.append(f"{selector}{{{html.unescape(styles[index])}}}")
    return "\n".join(rules)


def formula_sources(page: str) -> tuple[_Formula, ...]:
    """Unprepared source locations and inherited reader contexts for diagnostics."""
    parser = _MathParser(page)
    parser.feed(page)
    parser.close()
    return tuple(parser.formulas)


def native_math(keys: list[MathKey]) -> dict[MathKey, str]:
    """Pinned native output, before geometry sharing, for independent comparisons."""
    missing = list(dict.fromkeys(key for key in keys if key not in _CACHE))
    if missing:
        missing.sort(key=lambda key: (key[2], key[3]))
        _render(missing)
    return {key: _CACHE[key] for key in keys}


def clear_cache() -> None:
    """Discard process-local rendered formulas; output remains deterministic."""
    global _RENDERER_VERSION  # noqa: PLW0603
    _CACHE.clear()
    _STYLES.clear()
    _RENDERER_VERSION = None


def _attach_styles(page: str, page_path: str) -> str:
    if "</head>" not in page:
        return f"<style>{_stylesheet(page)}</style>" + page
    head = page.split("</head>", 1)[0]
    if re.search(r"<(?:link|style)\b[^>]*\bdata-site-math-styles\b", head):
        return page
    from devtools import site_assets  # noqa: PLC0415

    ref = site_assets.shared().assets.stylesheet("site-math.css", _stylesheet(page))
    style = site_assets.stylesheet_tag(ref, page_path).replace(
        "<link ", "<link data-site-math-styles ", 1
    )
    if _RENDERER_VERSION is None:
        raise ValueError("prepared mathematics has no checked renderer provenance")
    provenance = f'<meta name="site-math-katex" content="{_RENDERER_VERSION}">'
    return page.replace("</head>", f"{provenance}\n{style}\n</head>", 1)


def prepare(page: str, *, page_path: str = "index.html") -> str:
    """Prepare all reader font choices without post-load math or duplicate semantics."""
    formulas = formula_sources(page)
    if not formulas:
        if "</head>" in page and 'data-site-math="' in page:
            return _attach_styles(page, page_path)
        return page
    missing = list(
        dict.fromkeys(
            key for formula in formulas for key in _profile_keys(formula) if key not in _CACHE
        )
    )
    if missing:
        # Install each metric table once per batch rather than once per adjacent formula.
        missing.sort(key=lambda key: (key[2], key[3]))
        _render(missing)
    changes: list[tuple[int, int, str]] = []
    for formula in formulas:
        visual = _visual(formula)
        opening = page[formula.start : formula.content]
        opening = (
            opening[:-1]
            + f' data-kpress-math-face="{formula.profile}" data-kpress-math-prepared="true"'
            + f' data-site-math="{formula.choice}">'
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
    prepared = "".join(pieces)
    return _attach_styles(prepared, page_path)
