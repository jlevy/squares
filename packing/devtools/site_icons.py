"""Shared account icons; brand marks and the KPress external-link glyph."""

import base64
import html
import re
from functools import cache
from pathlib import Path

# Simple Icons X, CC0: https://github.com/simple-icons/simple-icons/blob/develop/icons/x.svg
_X_PATH = (
    "M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2."
    "33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8"
    ".532.929 1.329 7.754 11.09h-3.182z"
)


def account_icon(kind: str, *, class_name: str = "site-account-icon") -> str:
    """A decorative brand or web icon; the enclosing link supplies its account label."""
    if kind == "github":
        return _github_icon("github", class_name)
    if kind == "twitter":
        size = 24
        path = _X_PATH
        return (
            f'<svg class="{html.escape(class_name)}" viewBox="0 0 {size} {size}" '
            'fill="currentColor" stroke="none" aria-hidden="true" focusable="false">'
            f'<path d="{path}"/></svg>'
        )
    # Inline the canonical KPress Lucide glyph: standalone pages have no icon sprite.
    return (
        f'<svg class="{html.escape(class_name)}" viewBox="0 0 24 24" '
        'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true" focusable="false">'
        '<path d="M15 3h6v6"/><path d="M10 14 21 3"/>'
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h6"/></svg>'
    )


# The retained GitHub brand mark (Octicons, MIT) and Lucide 1.17.0 thread glyphs
# (ISC) are shared by inline references and CSS link decoration.
_ICON_ROOT = Path(__file__).with_name("overview") / "icons"
_GITHUB_ICONS = {"github": "github", "issue": "circle-dot", "pull-request": "git-pull-request"}
GITHUB_LINK_CSS = Path(__file__).with_name("templates") / "github-links.css"
GITHUB_ICON_INPUTS = (
    Path(__file__),
    Path(__file__).with_name("site_github_links.py"),
    Path(__file__).with_name("github_references.py"),
    GITHUB_LINK_CSS,
    *(_ICON_ROOT / f"{name}.svg" for name in _GITHUB_ICONS.values()),
)


@cache
def _github_svg(kind: str) -> str:
    return (_ICON_ROOT / f"{_GITHUB_ICONS[kind]}.svg").read_text(encoding="utf-8").strip()


def _github_icon(kind: str, class_name: str) -> str:
    attributes = (
        f'<svg class="{html.escape(class_name, quote=True)}" '
        'aria-hidden="true" focusable="false" '
    )
    return re.sub(r"<svg\s+", lambda _: attributes, _github_svg(kind), count=1)


def github_reference_icon(kind: str, *, class_name: str = "site-account-icon") -> str:
    """A decorative Lucide issue or PR glyph; the link supplies its accessible name."""
    if kind not in {"issue", "pull-request"}:
        raise ValueError(f"unknown GitHub reference kind: {kind}")
    return _github_icon(kind, class_name)


def github_link_css() -> str:
    """One CSS-only link treatment, including inert content loaded into popovers."""
    css = GITHUB_LINK_CSS.read_text(encoding="utf-8")
    for kind in _GITHUB_ICONS:
        url = (
            "data:image/svg+xml;base64," + base64.b64encode(_github_svg(kind).encode()).decode()
        )
        css = css.replace(f"__SITE_GITHUB_{kind.upper().replace('-', '_')}__", url)
    return css


# Canonical Lucide maximize and x paths from KPress's retained icons/icons.svg.
# Inline like account_icon's web glyph: lightweight standalone shells have no sprite.
_POPOVER_PATHS = {
    "maximize": (
        "M8 3H5a2 2 0 0 0-2 2v3",
        "M21 8V5a2 2 0 0 0-2-2h-3",
        "M3 16v3a2 2 0 0 0 2 2h3",
        "M16 21h3a2 2 0 0 0 2-2v-3",
    ),
    "x": ("M18 6 6 18", "m6 6 12 12"),
}


def popover_icon(name: str, *, sprite: bool = False) -> str:
    """One retained Lucide glyph; the enclosing header control owns its accessible name."""
    paths = _POPOVER_PATHS[name]
    if sprite:
        return (
            '<svg aria-hidden="true" focusable="false">'
            f'<use href="#kpress-icon-{name}"></use></svg>'
        )
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
        + "".join(f'<path d="{path}"/>' for path in paths)
        + "</svg>"
    )
