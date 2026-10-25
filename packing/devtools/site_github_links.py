"""Classify exact GitHub thread routes without rewriting link contents or addresses."""

from html.parser import HTMLParser

from devtools.github_references import parse_github_reference


class _GitHubLinks(HTMLParser):
    def __init__(self, markup: str) -> None:
        super().__init__(convert_charrefs=True)
        self.starts = [0, *(index + 1 for index, char in enumerate(markup) if char == "\n")]
        self.edits: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        attributes = dict(attrs)
        href = attributes.get("href")
        reference = parse_github_reference(href) if href else None
        if reference is None or "data-site-github-kind" in attributes:
            return
        raw = self.get_starttag_text()
        assert raw is not None
        line, column = self.getpos()
        end = len(raw) - (2 if raw.endswith("/>") else 1)
        self.edits.append(
            (self.starts[line - 1] + column + end, f' data-site-github-kind="{reference.kind}"')
        )


def decorate_github_links(markup: str) -> str:
    """Add only the thread-kind attribute; a second pass returns identical bytes."""
    parser = _GitHubLinks(markup)
    parser.feed(markup)
    parser.close()
    if not parser.edits:
        return markup
    parts = []
    cursor = 0
    for position, addition in parser.edits:
        parts.extend((markup[cursor:position], addition))
        cursor = position
    parts.append(markup[cursor:])
    return "".join(parts)
