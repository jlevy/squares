"""One site hierarchy for global navigation and both breadcrumb presentations."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlsplit

from devtools.site_icons import account_icon


@dataclass(frozen=True)
class NavigationItem:
    """A destination and its direct children; record families stay on collection pages."""

    key: str
    label: str
    path: str
    children: tuple[NavigationItem, ...] = ()


NAVIGATION = (
    NavigationItem("overview", "Overview", "./"),
    NavigationItem("news", "News", "news.html"),
    NavigationItem(
        "results",
        "Results",
        "",
        (
            NavigationItem("recent-results", "Recent Results", "recent-results.html"),
            NavigationItem("all-results", "Results Archive", "results.html"),
            NavigationItem("atlas", "Visual Atlas", "atlas.html"),
            NavigationItem("verification", "Verification and Ratings", "epistemics.html"),
        ),
    ),
    NavigationItem(
        "learn",
        "Learn",
        "",
        (
            NavigationItem("papers", "Papers", "papers.html"),
            NavigationItem("tutorials", "Tutorials", "tutorials.html"),
            NavigationItem("film", "Videos", "visualize.html"),
            NavigationItem("workbench", "Workbench", "workbench/"),
            NavigationItem("downloads", "Downloads", "downloads.html"),
            NavigationItem("resources", "Resources", "resources.html"),
        ),
    ),
    NavigationItem(
        "about",
        "About",
        "",
        (
            NavigationItem("project", "The Squares Project", "about.html"),
            NavigationItem("profiles", "Contributor Profiles", "profiles/"),
            NavigationItem("documentation", "Project Documentation", "documentation.html"),
            NavigationItem("report", "Report a Result", "report.html"),
        ),
    ),
)
_PAGE_TITLES = {
    item.path: item.label
    for group in NAVIGATION
    for item in (group, *group.children)
    if item.path
}
_LEGACY_PATHS = {
    "overview": "./",
    "news": "news.html",
    "results": "results.html",
    "recent-results": "recent-results.html",
    "atlas": "atlas.html",
    "papers": "papers.html",
    "explanations": "papers.html",
    "learn": "papers.html",
    "visualize": "visualize.html",
    "film": "visualize.html",
    "about": "about.html",
    "github": "readme.html",
    "workbench": "workbench/",
    "profiles": "profiles/",
    "resources": "resources.html",
}
# The same parent declarations drive the group indication and visible/structured trails.
_PARENTS = {
    "about.html": ("about",),
    "recent-results.html": ("results",),
    "results.html": ("results",),
    "atlas.html": ("results",),
    "epistemics.html": ("results",),
    "papers.html": ("learn",),
    "tutorials.html": ("learn",),
    "downloads.html": ("learn",),
    "tutorial.html": ("learn", "tutorials"),
    "tutorial-advanced.html": ("learn", "tutorials"),
    "visualize.html": ("learn",),
    "workbench/": ("learn",),
    "resources.html": ("learn",),
    "profiles/": ("about",),
    "documentation.html": ("about",),
    "report.html": ("about",),
    "readme.html": ("about",),
    "synopsis.html": ("about",),
    "conventions.html": ("about",),
    "development.html": ("about",),
}
_COLLECTIONS = {
    "cases/": ("results", "atlas"),
    "result/": ("results", "all-results"),
    "papers/": ("learn", "papers"),
    "profiles/": ("about", "profiles"),
    "synopsis/": ("about", "synopsis"),
}
_ANCESTORS = {
    **{item.key: (item.label, item.path) for item in NAVIGATION},
    **{child.key: (child.label, child.path) for item in NAVIGATION for child in item.children},
    "synopsis": ("Research Synopsis", "synopsis.html"),
}
_CHEVRON = (
    '<svg class="site-nav-icon" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true" focusable="false">'
    '<path d="m9 6 6 6-6 6"/></svg>'
)


def _path(value: str) -> str:
    path = urlsplit(_LEGACY_PATHS.get(value, value)).path.removeprefix("/")
    while path.startswith("./"):
        path = path[2:]
    if path in {"", "index.html"}:
        return "./"
    if path.endswith("/index.html"):
        return path.removesuffix("index.html")
    return path


def navigation_title(path: str, fallback: str = "") -> str:
    """Return a menu destination's canonical title, leaving detail titles to the caller."""
    return _PAGE_TITLES.get(_path(path), fallback)


def _parents(path: str) -> tuple[str, ...]:
    if path in _PARENTS:
        return _PARENTS[path]
    for prefix, ancestors in _COLLECTIONS.items():
        if path.startswith(prefix) and path != prefix:
            return ancestors
    return ()


def _link(item: NavigationItem, path: str, ancestors: tuple[str, ...], root: str) -> str:
    current = ""
    # Fragment destinations are not the current page unless a reader follows that
    # location explicitly; never mark both Atlas and its Bounds section as current.
    if "#" not in item.path and _path(item.path) == path:
        current = ' aria-current="page"'
    elif item.key in ancestors:
        current = ' aria-current="true"'
    return (
        f'<a data-page="{item.key}" href="{html.escape(root + item.path, quote=True)}"'
        f"{current}>{html.escape(item.label)}</a>"
    )


def navigation_links(current: str, root: str = "") -> str:
    """Render the full shared navigation shell from a legacy key or canonical path."""
    path = _path(current) if current else ""
    ancestors = _parents(path)
    links = []
    for item in NAVIGATION:
        contents = _link(item, path, ancestors, root)
        if item.children:
            target = f"site-nav-{item.key}"
            active = item.key in ancestors or bool(item.path and _path(item.path) == path)
            current = ' aria-current="true"' if active else ""
            fallback = (
                contents.replace("<a ", '<a class="site-nav-fallback" ', 1).replace(
                    'aria-current="page"', 'aria-current="true"'
                )
                if item.path
                else (
                    f'<span class="site-nav-fallback" data-page="{item.key}"{current}>'
                    f"{item.label}</span>"
                )
            )
            contents = (
                fallback + '<button type="button" class="site-nav-disclosure" '
                f'data-page="{item.key}" aria-expanded="false" aria-controls="{target}"'
                f"{current}>{html.escape(item.label)}{_CHEVRON}</button>"
                f'<ul id="{target}" class="site-nav-submenu">'
                + "".join(
                    f"<li>{_link(child, path, ancestors, root)}</li>" for child in item.children
                )
                + "</ul>"
            )
        links.append(f"<li>{contents}</li>")
    return (
        Path(__file__)
        .with_name("templates")
        .joinpath("site-nav.html")
        .read_text(encoding="utf-8")
        .replace("{{ROOT}}", html.escape(root, quote=True))
        .replace("{{NAVIGATION_LINKS}}", "".join(links))
        .replace("{{GITHUB_ICON}}", account_icon("github", class_name="site-nav-icon"))
    )


def _trail(path: str, title: str) -> tuple[tuple[str, str], ...]:
    path = _path(path)
    parents = _parents(path)
    current = navigation_title(path, title)
    return (*(_ANCESTORS[key] for key in parents), (current, path))


def breadcrumbs_html(path: str, title: str, root: str = "") -> str:
    """Show every page's ancestry, ending in its own plain current-page label."""
    trail = _trail(path, title)
    if not trail:
        return ""
    items = "".join(
        "<li>"
        + (
            f'<span aria-current="page">{html.escape(label)}</span>'
            if index == len(trail) - 1
            else (
                f'<a href="{html.escape(root + target, quote=True)}">{html.escape(label)}</a>'
                if target
                else f"<span>{html.escape(label)}</span>"
            )
        )
        + "</li>"
        for index, (label, target) in enumerate(trail)
    )
    return f'<nav class="site-breadcrumbs" aria-label="Breadcrumb"><ol>{items}</ol></nav>'


def breadcrumb_data(path: str, title: str, site_url: str) -> dict[str, Any] | None:
    """Use the visible trail's parents and titles for search-engine breadcrumb data."""
    trail = _trail(path, title)
    if not trail:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": label,
                **({"item": urljoin(site_url.rstrip("/") + "/", target)} if target else {}),
            }
            for index, (label, target) in enumerate(trail, start=1)
        ],
    }
