"""Evidence-backed contributor records, independent of credit and site renderers.

Ids identify people; names and handles are evidence-backed display spellings. Name
lookup returns candidates, never an identity, even when one spelling has one match. Bios
remain reader prose: the loader checks their paragraph shape and evidence references;
the five-sentence limit is an editorial check, not a punctuation-splitting heuristic.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from functools import cache
from ipaddress import ip_address
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, cast
from urllib.parse import urlsplit

import yaml
from jsonschema_rs import Draft202012Validator

from sqpack.project import require_project_root
from sqpack.yamlio import load_yaml

CONTRACT = "packing.squares:Contributor/v1"
SCHEMA_NAME = "contributor.schema.yaml"
FOOTER = (
    "<!-- This document follows common-doc-guidelines.md.\n"
    "See github.com/jlevy/practical-prose and review guidelines before editing.\n-->"
)
_META = {
    "contract": CONTRACT,
    "schema": SCHEMA_NAME,
    "envelope": "contributor",
    "status": "enforced",
}
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)(.*)\Z", re.DOTALL)
_BLOCK = re.compile(
    r"^(?: {4}|\t| {0,3}(?:#{1,6}(?:\s|$)|>|[-+*]\s|\d+[.)]\s|`{3}|~{3}|<|"
    r"(?:[-*_]\s*){3,}$|=+\s*$|-+\s*$))",
    re.MULTILINE,
)


class ContributorError(ValueError):
    """A contributor record or its evidence references violates the contract."""


@dataclass(frozen=True, slots=True)
class ContributorSource:
    id: str
    locator: str
    archive_path: str | None = None
    url: str | None = None


@dataclass(frozen=True, slots=True)
class ContributorLink:
    kind: str
    url: str
    handle: str | None = None


@dataclass(frozen=True, slots=True)
class FieldProvenance:
    field: str
    sources: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Contributor:
    id: str
    display_name: str
    real_name: str | None
    aliases: tuple[str, ...]
    links: tuple[ContributorLink, ...]
    sources: tuple[ContributorSource, ...]
    provenance: tuple[FieldProvenance, ...]
    bio: str | None
    bio_sources: tuple[str, ...]

    @property
    def profile_path(self) -> str:
        """Planned canonical path; this module publishes no page."""
        return f"contributors/{self.id}.html"


@dataclass(frozen=True, slots=True)
class ContributorRegistry:
    by_id: Mapping[str, Contributor]
    by_name: Mapping[str, tuple[Contributor, ...]]

    def candidates(self, name: str) -> tuple[Contributor, ...]:
        """Find spelling candidates; only an explicit id establishes an identity join."""
        return self.by_name.get(name.casefold(), ())


@cache
def _validator(schema: Path) -> Draft202012Validator:
    return Draft202012Validator(load_yaml(schema.read_text(encoding="utf-8")))


def _safe_url(value: str) -> None:
    try:
        parsed = urlsplit(value)
        host = parsed.hostname
        port = parsed.port
    except ValueError as error:
        raise ContributorError(f"invalid HTTP URL: {value}") from error
    if (
        parsed.scheme not in {"http", "https"}
        or not host
        or parsed.username is not None
        or parsed.password is not None
        or re.search(r"[\s\\\x00-\x1f\x7f]", value)
        or port == 0
    ):
        raise ContributorError(f"unsafe HTTP URL: {value}")
    try:
        ip_address(host)
    except ValueError:
        if len(host) > 253 or any(
            not re.fullmatch(r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?", label)
            for label in host.split(".")
        ):
            raise ContributorError(f"unsafe HTTP URL host: {value}") from None


def _account_link(link: Mapping[str, Any]) -> None:
    _safe_url(link["url"])
    parsed = urlsplit(link["url"])
    host = parsed.hostname
    path = parsed.path.removeprefix("/").removesuffix("/")
    handle = link.get("handle")
    kind = link["kind"]
    if handle is not None and kind not in {"github", "twitter", "substack"}:
        raise ContributorError(f"{kind} links cannot declare an account handle")
    account = None
    if kind == "github":
        if host != "github.com" or not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9-]{0,38}", path):
            raise ContributorError("github links must name a github.com account")
        account = path
    elif kind == "twitter":
        if host not in {"x.com", "twitter.com"} or not re.fullmatch(
            r"[a-zA-Z0-9_]{1,15}", path
        ):
            raise ContributorError("twitter links must name an x.com or twitter.com account")
        account = path
    elif kind == "substack":
        if host == "substack.com" and re.fullmatch(r"@[a-zA-Z0-9_-]+", path):
            account = path[1:]
        elif host and re.fullmatch(r"[a-zA-Z0-9-]+\.substack\.com", host) and not path:
            account = host.removesuffix(".substack.com")
        else:
            raise ContributorError("substack links must name a Substack account or publication")
    if account is not None and (
        parsed.query
        or parsed.fragment
        or parsed.port is not None
        or (handle is not None and handle.casefold() != account.casefold())
    ):
        raise ContributorError("account handle must match its unambiguous account URL")


def _archive(path: str, repo: Path) -> None:
    parts = path.split("/")
    if (
        "\\" in path
        or any(part in {"", ".", ".."} for part in parts)
        or PurePosixPath(path).is_absolute()
        or not (repo / path).resolve().is_relative_to(repo.resolve())
        or not (repo / path).is_file()
    ):
        raise ContributorError(f"archive_path must name a file inside the repository: {path}")


def _pointer(payload: dict[str, Any], pointer: str) -> Any:
    value: Any = payload
    for encoded in pointer.removeprefix("/").split("/"):
        if re.search(r"~(?![01])", encoded):
            raise ContributorError(f"invalid provenance JSON Pointer: {pointer}")
        part = encoded.replace("~1", "/").replace("~0", "~")
        if isinstance(value, dict) and part in value:
            value = value[part]
        elif (
            isinstance(value, list)
            and re.fullmatch(r"0|[1-9]\d*", part)
            and int(part) < len(value)
        ):
            value = value[int(part)]
        else:
            raise ContributorError(f"provenance field does not exist: {pointer}")
    return value


def _bio(body: str) -> str | None:
    body = body.strip("\r\n")
    if not body.endswith(FOOTER) or body.count(FOOTER) != 1:
        raise ContributorError("record must end with exactly one unchanged guideline footer")
    bio = body.removesuffix(FOOTER).strip("\r\n")
    if not bio.strip():
        return None
    if (
        re.search(r"\n[ \t]*\n", bio)
        or _BLOCK.search(bio)
        or re.search(r"^\s*\|?\s*:?-+:?\s*\|[ |:\-]*$", bio, re.MULTILINE)
    ):
        raise ContributorError("bio must be one Markdown paragraph without block content")
    return bio.strip()


def _semantics(payload: dict[str, Any], bio: str | None, repo: Path) -> None:
    sources = payload["sources"]
    source_ids = {source["id"] for source in sources}
    if len(source_ids) != len(sources):
        raise ContributorError("source ids must be unique within the record")
    for source in sources:
        if "archive_path" in source:
            _archive(source["archive_path"], repo)
        if "url" in source:
            _safe_url(source["url"])
    for link in payload.get("links", []):
        _account_link(link)
    pointers = set()
    for evidence in payload["provenance"]:
        pointer = evidence["field"]
        _pointer(payload, pointer)
        if pointer in pointers:
            raise ContributorError(f"duplicate provenance field: {pointer}")
        pointers.add(pointer)
        if unknown := set(evidence["sources"]) - source_ids:
            raise ContributorError(f"unknown provenance sources: {sorted(unknown)}")
    claims = ["/display_name"]
    if "real_name" in payload:
        claims.append("/real_name")
    claims.extend(f"/aliases/{index}" for index in range(len(payload.get("aliases", []))))
    for index, link in enumerate(payload.get("links", [])):
        claims.extend(f"/links/{index}/{key}" for key in link)
    for claim in claims:
        if not any(claim == pointer or claim.startswith(pointer + "/") for pointer in pointers):
            raise ContributorError(f"identity field requires provenance: {claim}")
    bio_sources = payload.get("bio_sources", [])
    if bool(bio) != bool(bio_sources):
        raise ContributorError("bio_sources must be present exactly when the record has a bio")
    if unknown := set(bio_sources) - source_ids:
        raise ContributorError(f"unknown bio sources: {sorted(unknown)}")


def load_contributor(path: Path, *, repo: Path | None = None) -> Contributor:
    """Load a self-describing record and validate identity, evidence and bio shape."""
    match = _FRONTMATTER.fullmatch(path.read_text(encoding="utf-8"))
    if match is None:
        raise ContributorError("record requires YAML frontmatter")
    try:
        document = load_yaml(match[1])
    except yaml.YAMLError as error:
        raise ContributorError(f"invalid or ambiguous YAML: {error}") from error
    if not isinstance(document, dict) or set(document) != {"softschema", "contributor"}:
        raise ContributorError("record requires only softschema and contributor root fields")
    if document["softschema"] != _META:
        raise ContributorError(
            "softschema metadata must bind the enforced Contributor/v1 contract"
        )
    payload = cast(dict[str, Any], document["contributor"])
    errors = list(_validator(path.parent / SCHEMA_NAME).iter_errors(payload))
    if errors:
        raise ContributorError("; ".join(str(error) for error in errors))
    if path.stem != payload["id"]:
        raise ContributorError("contributor id must equal its filename stem")
    bio = _bio(match[2])
    _semantics(payload, bio, repo if repo is not None else require_project_root().parent)
    return Contributor(
        id=payload["id"],
        display_name=payload["display_name"],
        real_name=payload.get("real_name"),
        aliases=tuple(payload.get("aliases", [])),
        links=tuple(ContributorLink(**link) for link in payload.get("links", [])),
        sources=tuple(ContributorSource(**source) for source in payload["sources"]),
        provenance=tuple(
            FieldProvenance(evidence["field"], tuple(evidence["sources"]))
            for evidence in payload["provenance"]
        ),
        bio=bio,
        bio_sources=tuple(payload.get("bio_sources", [])),
    )


def load_contributors(
    directory: Path | None = None, *, repo: Path | None = None
) -> ContributorRegistry:
    """Load records deterministically; ids are unique and names are candidate keys."""
    directory = directory if directory is not None else require_project_root() / "contributors"
    records: dict[str, Contributor] = {}
    names: dict[str, list[Contributor]] = {}
    for path in sorted(directory.glob("*.md")):
        contributor = load_contributor(path, repo=repo)
        if contributor.id in records:
            raise ContributorError(f"duplicate contributor id: {contributor.id}")
        records[contributor.id] = contributor
        spellings = {contributor.display_name, *contributor.aliases}
        if contributor.real_name:
            spellings.add(contributor.real_name)
        for name in sorted({spelling.casefold() for spelling in spellings}):
            names.setdefault(name, []).append(contributor)
    if not records:
        raise ContributorError(f"no contributor records found in {directory}")
    return ContributorRegistry(
        MappingProxyType(records),
        MappingProxyType({name: tuple(matches) for name, matches in names.items()}),
    )
