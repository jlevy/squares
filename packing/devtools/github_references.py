"""GitHub issue and PR links derived from explicit retained evidence associations."""

from __future__ import annotations

import html
import re
from collections.abc import Collection, Iterable, Mapping
from typing import Any, Literal, NamedTuple
from urllib.parse import urlsplit, urlunsplit

from devtools.site_icons import github_reference_icon

_THREAD_PATH = re.compile(
    r"/([A-Za-z0-9][A-Za-z0-9-]*)/([A-Za-z0-9_.-]+)/(issues|pull)/([1-9][0-9]*)/?"
)


class GitHubReference(NamedTuple):
    """One exact issue or PR URL; a fragment may retain a specific evidence comment."""

    repository: str
    kind: Literal["issue", "pull-request"]
    number: int
    url: str


class CreditReferences(NamedTuple):
    """Source threads, registering PRs and supporting records have different meanings."""

    sources: tuple[str, ...]
    registrations: tuple[str, ...]
    supporting: tuple[str, ...]


def parse_github_reference(url: str) -> GitHubReference | None:
    """Recognize HTTPS GitHub thread routes, refusing host and path ambiguities."""
    if any(
        char.isspace() or ord(char) < 32 or ord(char) == 127 or char == "\\" for char in url
    ):
        return None
    try:
        parts = urlsplit(url)
    except ValueError:
        return None
    if parts.scheme != "https" or parts.netloc.casefold() != "github.com":
        return None
    match = _THREAD_PATH.fullmatch(parts.path)
    if match is None or match[2] in {".", ".."}:
        return None
    try:
        number = int(match[4])
    except ValueError:
        return None
    kind: Literal["issue", "pull-request"] = "issue" if match[3] == "issues" else "pull-request"
    return GitHubReference(
        f"{match[1]}/{match[2]}",
        kind,
        number,
        urlunsplit(("https", "github.com", parts.path, parts.query, parts.fragment)),
    )


def github_references(urls: Iterable[str]) -> tuple[GitHubReference, ...]:
    """Keep one link per repository, type and number, retaining the first evidence URL."""
    unique: dict[tuple[str, str, int], GitHubReference] = {}
    for url in urls:
        if (reference := parse_github_reference(url)) is not None:
            unique.setdefault(
                (reference.repository.casefold(), reference.kind, reference.number), reference
            )
    return tuple(unique.values())


def render_github_references(
    urls: Iterable[str], *, class_name: str = "site-github-ref"
) -> str:
    """Inline issue/PR icons and numbers; accessible labels also name their repositories."""
    links = []
    for reference in github_references(urls):
        kind = "issue" if reference.kind == "issue" else "pull request"
        label = f"GitHub {kind} {reference.repository}#{reference.number}"
        links.append(
            f'<a class="{html.escape(class_name, quote=True)}" '
            f'href="{html.escape(reference.url, quote=True)}" '
            f'aria-label="{html.escape(label, quote=True)}">'
            f"{github_reference_icon(reference.kind)} #{reference.number}</a>"
        )
    return " · ".join(links)


def credit_reference_urls(
    source_keys: Collection[str],
    result_ids: Collection[str],
    *,
    coverage: Mapping[str, Any],
    changelog: Mapping[str, Any],
) -> CreditReferences:
    """Follow source keys and result ids in loaded records, without mining prose.

    Registration PRs describe where a result entered this project, not who authored
    its construction. Supporting references remain separate from its source evidence.
    """
    sources, results = frozenset(source_keys), frozenset(result_ids)
    source_urls = [
        str(source["url"])
        for source in coverage["sources"]
        if source.get("source_key") in sources
    ]
    registrations: list[str] = []
    supporting: list[str] = []
    repository = str(changelog["repository"]).rstrip("/")
    for entry in changelog["entries"]:
        if not results.intersection(entry.get("result_ids", ())):
            continue
        registrations.extend(f"{repository}/pull/{number}" for number in entry["pull_requests"])
        supporting.extend(str(item["target"]) for item in entry.get("references", ()))
    return CreditReferences(
        tuple(reference.url for reference in github_references(source_urls)),
        tuple(reference.url for reference in github_references(registrations)),
        tuple(reference.url for reference in github_references(supporting)),
    )
