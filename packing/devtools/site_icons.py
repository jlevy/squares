"""Shared account glyphs, sized and colored by their text role."""


def account_icon(kind: str) -> str:
    """A decorative GitHub, X or web glyph; the enclosing link names the account."""
    if kind == "github":
        drawing = (
            '<path fill="currentColor" d="M12 .8a11.2 11.2 0 0 0-3.54 21.83c.56.1.77-.24.77'
            "-.54v-2.1c-3.13.68-3.79-1.33-3.79-1.33-.51-1.3-1.25-1.65-1.25-1.65-1.02-.7.08-"
            ".69.08-.69 1.13.08 1.72 1.16 1.72 1.16 1 1.71 2.62 1.22 3.26.94.1-.73.39-1.22."
            "71-1.5-2.5-.28-5.13-1.25-5.13-5.56 0-1.23.44-2.23 1.16-3.02-.12-.28-.5-1.43.11"
            "-2.97 0 0 .95-.3 3.08 1.16a10.7 10.7 0 0 1 5.62 0c2.13-1.46 3.08-1.16 3.08-1.1"
            "6.61 1.54.23 2.69.11 2.97.72.79 1.16 1.79 1.16 3.02 0 4.32-2.64 5.28-5.15 5.56"
            '.4.35.76 1.03.76 2.08v3.09c0 .3.2.65.78.54A11.2 11.2 0 0 0 12 .8Z"/>'
        )
    elif kind == "twitter":
        drawing = '<path d="m4 3 16 18M20 3 4 21M4 3h4l12 18h-4Z"/>'
    else:
        drawing = (
            '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/>'
            '<path d="M3 12h18"/>'
        )
    return (
        '<svg class="site-account-icon" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
        f'aria-hidden="true" focusable="false">{drawing}</svg>'
    )
