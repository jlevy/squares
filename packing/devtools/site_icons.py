"""Shared account icons; brand marks and the KPress external-link glyph."""

import html

# GitHub Octicons mark-github, MIT; the same path used by project resource cards.
# https://github.com/primer/octicons/blob/main/icons/mark-github-16.svg
_GITHUB_PATH = (
    "M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27."
    "01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59"
    "-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0"
    "-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1."
    "28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33"
    "-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.3"
    "1 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 "
    "3.58-8 8-8Z"
)

# Simple Icons X, CC0: https://github.com/simple-icons/simple-icons/blob/develop/icons/x.svg
_X_PATH = (
    "M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2."
    "33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8"
    ".532.929 1.329 7.754 11.09h-3.182z"
)


def account_icon(kind: str, *, class_name: str = "site-account-icon") -> str:
    """A decorative brand or web icon; the enclosing link supplies its account label."""
    if kind in {"github", "twitter"}:
        size = 16 if kind == "github" else 24
        path = _GITHUB_PATH if kind == "github" else _X_PATH
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


# GitHub Octicons issue-opened-16 and git-pull-request-16, MIT; canonical paths:
# https://github.com/primer/octicons/blob/main/icons/issue-opened-16.svg
# https://github.com/primer/octicons/blob/main/icons/git-pull-request-16.svg
_ISSUE_PATHS = (
    "M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z",
    "M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z",
)
_PULL_REQUEST_PATHS = (
    (
        "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 "
        "0 0 1 1.5 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 "
        "5v5.628a2.251 2.251 0 1 1-1.5 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7."
        "177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm0 "
        "9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0 0 "
        "0-1.5 0Z"
    ),
)


def github_reference_icon(kind: str, *, class_name: str = "site-account-icon") -> str:
    """Decorative GitHub issue or PR glyph; its link supplies type and repository context."""
    if kind not in {"issue", "pull-request"}:
        raise ValueError(f"unknown GitHub reference kind: {kind}")
    paths = _ISSUE_PATHS if kind == "issue" else _PULL_REQUEST_PATHS
    return (
        f'<svg class="{html.escape(class_name, quote=True)}" viewBox="0 0 16 16" '
        'fill="currentColor" stroke="none" aria-hidden="true" focusable="false">'
        + "".join(f'<path d="{path}"/>' for path in paths)
        + "</svg>"
    )
