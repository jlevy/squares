"""Native header controls shared by cards and complete article popovers."""

import html
from urllib.parse import urlsplit

from devtools.site_icons import popover_icon


def popover_controls(
    target: str, *, destination: tuple[str, str] | None = None, sprite: bool = False
) -> str:
    """Keep the full-page link beside Close only when an overlay has a page to open."""
    expand = ""
    if destination:
        href, label = destination
        parsed = urlsplit(href)
        if (parsed.path or parsed.netloc) and parsed.scheme in {"", "http", "https"}:
            expand = (
                '<a class="site-popover-expand" '
                f'href="{html.escape(href, quote=True)}" '
                f'aria-label="{html.escape(label, quote=True)}" '
                f'title="{html.escape(label, quote=True)}">'
                + popover_icon("maximize-2", sprite=sprite)
                + "</a>"
            )
    return (
        '<div class="site-popover-controls">'
        + expand
        + '<button type="button" class="site-popover-close" '
        f'popovertarget="{html.escape(target, quote=True)}" '
        'popovertargetaction="hide" aria-label="Close">'
        + popover_icon("x", sprite=sprite)
        + "</button></div>"
    )
