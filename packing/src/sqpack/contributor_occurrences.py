"""Reviewed person joins address exact source fields, never a global name lookup."""

from __future__ import annotations

import ast
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Any, cast

import yaml
from jsonschema_rs import Draft202012Validator

from sqpack.contributors import PEOPLE_DIR, ContributorRegistry, load_contributors
from sqpack.project import require_project_root
from sqpack.yamlio import load_yaml

CONTRACT = "packing.squares:ContributorOccurrences/v1"
SCHEMA_NAME = "occurrences.schema.yaml"
#: The manifest's schema, as the manifest declares it: in `schemas/` beside it, with the
#: person records' (`sqpack.contributors.SCHEMA_PATH`).
SCHEMA_PATH = f"schemas/{SCHEMA_NAME}"
#: The manifest, under the project root, beside the `people/` records it joins.
MANIFEST = "contributors/occurrences.yaml"
#: The credit roles a span may carry, which profile pages publish beside each credit. The
#: schema's `role` enum repeats them, and the loader checks both.
ROLES = frozenset(
    {
        "collective-abbreviation",
        "construction-finder",
        "construction-improver",
        "credited-contributor",
        "lower-bound-prover",
        "prerequisite",
        "project-author",
        "source-author",
    }
)
_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---(?:\n|\Z)", re.DOTALL)


class OccurrenceError(ValueError):
    """A reviewed join no longer matches its source, span, identity or evidence."""


class MissingSourceError(OccurrenceError):
    """The addressed file, record or field is gone, rather than changed or unreadable."""


@dataclass(frozen=True, slots=True, order=True)
class CreditOrigin:
    path: str
    record_key: str
    field: str


@dataclass(frozen=True, slots=True)
class CreditOccurrence:
    origin: CreditOrigin
    expected_text: str
    start: int
    end: int
    label: str
    role: str
    disposition: str
    contributor_id: str | None = None
    evidence: tuple[str, ...] = ()
    note: str = ""


@dataclass(frozen=True, slots=True)
class InspectionReceipt:
    path: str
    status: str
    scope: str
    locators: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class OccurrenceRegistry:
    occurrences: tuple[CreditOccurrence, ...]
    by_origin: Mapping[CreditOrigin, tuple[CreditOccurrence, ...]]
    inspections: tuple[InspectionReceipt, ...]


def source_path(path: str, repo: Path, *, must_exist: bool = True) -> Path:
    """Require a retained file with one repository-relative, symlink-safe meaning."""
    if (
        "\\" in path
        or PurePosixPath(path).is_absolute()
        or any(part in {"", ".", ".."} for part in path.split("/"))
        or not (repo / path).resolve().is_relative_to(repo.resolve())
    ):
        raise OccurrenceError(f"source path must name a file inside the repository: {path}")
    if must_exist and not (repo / path).is_file():
        raise MissingSourceError(f"credit source file does not exist: {path}")
    return repo / path


def source_document(path: Path) -> Any:
    """Parse a credit source: YAML, a Markdown file's frontmatter, or a module's constants.

    A source that does not parse, a merge-conflicted one included, is an `OccurrenceError`
    naming it, so a census lists it among the changed sources instead of stopping."""
    try:
        text = path.read_text(encoding="utf-8")
        if path.suffix == ".py":
            # Read the reviewed generator constant without importing or executing its module.
            constants = {}
            for statement in ast.parse(text).body:
                if isinstance(statement, ast.Assign) and isinstance(
                    statement.value, ast.Constant
                ):
                    for target in statement.targets:
                        if isinstance(target, ast.Name):
                            constants[target.id] = statement.value.value
            return {"constants": constants}
        if path.suffix == ".md":
            match = _FRONTMATTER.match(text)
            if match is None:
                raise OccurrenceError(f"source has no structured frontmatter: {path}")
            text = match[1]
        return load_yaml(text)
    except (SyntaxError, UnicodeDecodeError, yaml.YAMLError) as error:
        raise OccurrenceError(
            f"credit source does not parse ({type(error).__name__}): {path}"
        ) from error


def _record(document: Any, key: str, path: str) -> Mapping[str, Any]:
    if not isinstance(document, dict):
        raise OccurrenceError(f"credit source must be a structured mapping: {path}")
    softschema = document.get("softschema") or {}
    if not isinstance(softschema, dict):
        raise OccurrenceError(f"credit source softschema must be a mapping: {path}")
    if envelope := softschema.get("envelope"):
        if not isinstance(envelope, str) or not isinstance(document.get(envelope), dict):
            raise OccurrenceError(f"credit source envelope must name a mapping: {path}")
        document = document[envelope]
    if any(field in document and str(document[field]) == key for field in ("id", "key", "n")):
        return document
    matches = [
        row
        for rows in document.values()
        if isinstance(rows, list)
        for row in rows
        if isinstance(row, dict)
        and any(field in row and str(row[field]) == key for field in ("id", "key", "n"))
    ]
    if key in document and isinstance(document[key], dict):
        matches.append(document[key])
    if key == "$":
        return document
    if not matches:
        raise MissingSourceError(f"credit source record does not exist: {key}: {path}")
    if len(matches) != 1:
        raise OccurrenceError(f"credit source record must resolve uniquely: {key}: {path}")
    return matches[0]


def source_text(
    origin: CreditOrigin, *, repo: Path | None = None, documents: dict[str, Any] | None = None
) -> str:
    """Retrieve the addressed scalar, so stored text is an assertion about live evidence.

    `MissingSourceError` says the file, record or field is gone; any other
    `OccurrenceError` says it is there but changed shape or does not parse."""
    repo = repo if repo is not None else require_project_root().parent
    path = source_path(origin.path, repo)
    documents = documents if documents is not None else {}
    if origin.path not in documents:
        try:
            documents[origin.path] = source_document(path)
        except OccurrenceError as error:
            # Every span in a broken source reports it without parsing it again.
            documents[origin.path] = error
    if isinstance(cached := documents[origin.path], OccurrenceError):
        raise OccurrenceError(str(cached)) from cached
    value: Any = _record(cached, origin.record_key, origin.path)
    if not origin.field.startswith("/"):
        raise OccurrenceError(f"credit field must be a JSON Pointer: {origin.field}")
    for encoded in origin.field[1:].split("/"):
        if re.search(r"~(?![01])", encoded):
            raise OccurrenceError(f"invalid credit field pointer: {origin.field}")
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
            raise MissingSourceError(f"credit field does not exist: {origin}")
    if not isinstance(value, str):
        raise OccurrenceError(f"credit field must address a text scalar: {origin}")
    return value


def load_occurrences(
    path: Path | None = None,
    *,
    repo: Path | None = None,
    profiles: ContributorRegistry | None = None,
) -> OccurrenceRegistry:
    """Validate every retained join, including unresolved and non-person dispositions."""
    repo = repo if repo is not None else require_project_root().parent
    path = path if path is not None else repo / "packing" / MANIFEST
    document = load_yaml(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or document.get("softschema") != {
        "contract": CONTRACT,
        "schema": SCHEMA_PATH,
        "status": "enforced",
    }:
        raise OccurrenceError(
            "occurrences must bind the enforced ContributorOccurrences/v1 contract"
        )
    payload = {key: value for key, value in document.items() if key != "softschema"}
    errors = list(
        Draft202012Validator(
            load_yaml((path.parent / SCHEMA_PATH).read_text(encoding="utf-8"))
        ).iter_errors(payload)
    )
    if errors:
        raise OccurrenceError("; ".join(str(error) for error in errors))
    profiles = (
        profiles
        if profiles is not None
        else load_contributors(repo / "packing" / PEOPLE_DIR, repo=repo)
    )
    documents: dict[str, Any] = {}
    by_origin: dict[CreditOrigin, list[CreditOccurrence]] = {}
    occurrences = []
    for row in cast(list[dict[str, Any]], payload["occurrences"]):
        origin = CreditOrigin(**row["origin"])
        item = CreditOccurrence(
            **{key: value for key, value in row.items() if key not in {"origin", "evidence"}},
            origin=origin,
            evidence=tuple(row["evidence"]),
        )
        if item.role not in ROLES:
            raise OccurrenceError(f"unknown credit role {item.role!r}: {origin}")
        if source_text(origin, repo=repo, documents=documents) != item.expected_text:
            raise OccurrenceError(f"reviewed source text changed: {origin}")
        if (
            item.end <= item.start
            or item.end > len(item.expected_text)
            or item.expected_text[item.start : item.end] != item.label
        ):
            raise OccurrenceError(f"reviewed label span does not match source text: {origin}")
        if item.disposition == "resolved":
            profile = profiles.by_id.get(item.contributor_id or "")
            if profile is None:
                raise OccurrenceError(f"unknown contributor id: {item.contributor_id}")
            if not item.evidence or set(item.evidence) - {
                source.id for source in profile.sources
            }:
                raise OccurrenceError(f"unknown or missing contributor evidence: {origin}")
        elif item.contributor_id is not None or item.evidence:
            raise OccurrenceError(
                f"unresolved or non-person occurrence cannot assert identity: {origin}"
            )
        previous = by_origin.setdefault(origin, [])
        if any(item.start < other.end and other.start < item.end for other in previous):
            raise OccurrenceError(f"overlapping credit spans: {origin}")
        previous.append(item)
        occurrences.append(item)
    receipts = []
    seen_receipts = set()
    for row in payload["inspections"]:
        source_path(row["path"], repo, must_exist=row["status"] == "inspected")
        receipt = InspectionReceipt(**{**row, "locators": tuple(row["locators"])})
        key = (receipt.path, receipt.scope)
        if key in seen_receipts:
            raise OccurrenceError(f"duplicate inspection receipt: {key}")
        seen_receipts.add(key)
        if (receipt.status == "inspected") != bool(receipt.locators):
            raise OccurrenceError(f"inspection locators required exactly when inspected: {key}")
        receipts.append(receipt)
    return OccurrenceRegistry(
        tuple(occurrences),
        MappingProxyType(
            {
                origin: tuple(sorted(items, key=lambda item: item.start))
                for origin, items in by_origin.items()
            }
        ),
        tuple(receipts),
    )


def dependency_paths(path: Path, *, repo: Path) -> tuple[Path, ...]:
    """Discover exact retained inputs before sparse checkout or full semantic validation."""
    document = load_yaml(path.read_text(encoding="utf-8"))
    paths = {row["origin"]["path"] for row in document["occurrences"]}
    paths.update(row["path"] for row in document["inspections"] if row["status"] == "inspected")
    return tuple(source_path(value, repo, must_exist=False) for value in sorted(paths))
