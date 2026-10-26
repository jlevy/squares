"""GitHub issue and PR links derived from explicit retained evidence associations."""

from __future__ import annotations

import html
import re
from collections.abc import Collection, Iterable, Mapping
from functools import cache
from pathlib import Path
from typing import Any, Literal, NamedTuple
from urllib.parse import urlsplit, urlunsplit

from devtools.site_icons import github_reference_icon
from sqpack.yamlio import load_yaml

_THREAD_PATH = re.compile(
    r"/([A-Za-z0-9][A-Za-z0-9-]*)/([A-Za-z0-9_.-]+)/(issues|pull)/([1-9][0-9]*)/?"
)

#: Every result report received as a GitHub issue, joined to the register: the one
#: record of which issue reported which result (`devtools.check_requests`).
REQUESTS = Path(__file__).resolve().parent.parent / "campaign" / "result-requests.yaml"


def reporting_issues(requests: Mapping[str, Any]) -> dict[str, tuple[int, ...]]:
    """Each register id, with the issues whose reported results map to it.

    An issue reports a result when one of its `results` names that id in `register`.
    Evidence ids and replies are not reports of a result, so they are not followed.
    """
    found: dict[str, set[int]] = {}
    for issue in requests["issues"]:
        for result in issue.get("results") or ():
            for ident in result.get("register") or ():
                found.setdefault(str(ident), set()).add(int(issue["number"]))
    return {ident: tuple(sorted(numbers)) for ident, numbers in sorted(found.items())}


@cache
def result_reporting_issues() -> dict[str, tuple[int, ...]]:
    """`reporting_issues` of the committed request record, read once."""
    return reporting_issues(load_yaml(REQUESTS.read_text(encoding="utf-8")))


@cache
def issue_opened() -> dict[int, str]:
    """Each recorded issue's opening day (`opened`, ISO), from the committed record."""
    requests = load_yaml(REQUESTS.read_text(encoding="utf-8"))
    return {int(issue["number"]): str(issue["opened"]) for issue in requests["issues"]}


def issues_reporting(
    result_ids: Iterable[str],
    reporting: Mapping[str, Iterable[int]] | None = None,
    *,
    on_or_before: str | None = None,
    opened: Mapping[int, str] | None = None,
) -> tuple[int, ...]:
    """The issues that reported any of `result_ids`, in ascending order.

    With `on_or_before` (an ISO day), an issue opened after that day is left out: a
    review-tracking issue opened later for a result (#772 to #786, of 24 October 2026)
    did not report it, and a News entry dated before it cannot have come from it. An
    issue with no recorded opening day is kept."""
    table = result_reporting_issues() if reporting is None else reporting
    numbers = {number for ident in result_ids for number in table.get(ident, ())}
    if on_or_before is not None:
        days = issue_opened() if opened is None else opened
        numbers = {n for n in numbers if days.get(n, on_or_before) <= on_or_before}
    return tuple(sorted(numbers))


def issue_url(repository: str, number: int) -> str:
    """An issue's address in `repository`, a full GitHub URL or an `owner/name`."""
    base = repository.rstrip("/")
    if not base.startswith("https://"):
        base = f"https://github.com/{base}"
    return f"{base}/issues/{number}"


def cited_issues(repository: str, urls: Iterable[str]) -> tuple[int, ...]:
    """The numbers of the issues in `repository` that `urls` link, ignoring other repositories
    and pull requests; a link to one comment of an issue cites that issue."""
    name = repository.rstrip("/").removeprefix("https://github.com/").casefold()
    return tuple(
        sorted(
            {
                reference.number
                for reference in github_references(urls)
                if reference.kind == "issue" and reference.repository.casefold() == name
            }
        )
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
