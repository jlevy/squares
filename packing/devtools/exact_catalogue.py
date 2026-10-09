"""Export the exact-values register as small metadata and lazy coefficient payloads."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path
from typing import Any

DATA_DIRECTORY = "exact-side-values-data"
INDEX_PATH = Path(DATA_DIRECTORY) / "index.json"
SCHEMA_VERSION = 1
INTEGER = re.compile(r"[+-]?[0-9]+")
REPORTED_SOURCE_CLAIM = (
    "The source polynomial and isolated root were independently checked. "
    "Geometric feasibility and Lean replay await verification (V0/C0). "
    "This source root establishes no packing upper bound or global optimum."
)


class ExactCatalogueError(ValueError):
    """A register record cannot be exported without losing its exact identity."""


def publication_register(register: Mapping[str, Any]) -> dict[str, Any]:
    """Copy the register, omitting superseded history and its redundant current notes.

    The canonical register keeps these source facts. Publication retains every other
    record and field, including the assurance of unreconciled source roots.
    """
    published = deepcopy(dict(register))
    for key in ("entries", "historical_entries"):
        records = published.get(key, [])
        if not isinstance(records, list):
            raise ExactCatalogueError(f"register.{key} must be an array")
        for record in records:
            if not isinstance(record, dict):
                raise ExactCatalogueError(f"register.{key} records must be objects")
            if key == "entries" and isinstance(record.get("notes"), list):
                record["notes"] = [
                    note
                    for note in record["notes"]
                    if not isinstance(note, dict)
                    or note.get("kind") != "superseded-catalogue-polynomial"
                ]
        if key == "historical_entries" and key in published:
            published[key] = [
                record for record in records if record.get("kind") != "superseded"
            ]
    return published


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def source_certificate_claim(certificate: Mapping[str, Any]) -> str:
    level = f"{certificate['verification']}/{certificate['confirmation']}"
    adoption = "pending" if certificate["adoption"] == "pending" else "not selected"
    replay = (
        "Native geometry replay is retained."
        if certificate["geometry_replay"] == "native-replay-retained"
        else "Geometry has not been replayed for this source packet."
    )
    return (
        "Independently checked exact rational side. "
        f"Packing adoption is {adoption} ({level}). {replay} "
        "Global optimality remains open."
    )


def _claim(record: Mapping[str, Any], section: str) -> str:
    if section == "historical":
        certificate = record.get("source_certificate")
        if isinstance(certificate, dict):
            claim = source_certificate_claim(certificate)
        elif record.get("kind") == "unreconciled-source" and record.get("reported_source"):
            claim = REPORTED_SOURCE_CLAIM
        else:
            claim = {
                "source-invalid": (
                    "The algebraic checks do not furnish a valid packing upper bound: "
                    "the source marks this historical row invalid."
                ),
                "superseded": (
                    "This historical source side is superseded by the current recorded side."
                ),
                "outside-frontier": (
                    "This historical source side lies outside the current frontier."
                ),
                "unreconciled-source": (
                    "The relationship of this historical source to the frontier is unresolved."
                ),
            }.get(
                str(record.get("kind")), "Historical source fact; no current bound is claimed."
            )
        return claim
    side = record.get("side", {})
    relation = side.get("relation") if isinstance(side, dict) else None
    if relation == "equality" and record.get("status") == "proved":
        return "global optimum proved"
    if relation == "equality":
        return "reported equality; proof status open"
    if relation == "upper-bound":
        return "reported packing upper bound; optimum open"
    return f"{relation}; {record.get('status')}"


def _search(record: Mapping[str, Any], *, historical: bool) -> str:
    values = [
        record.get("n"),
        record.get("state"),
        record.get("status"),
        record.get("kind") if historical else record.get("algebraic_source"),
        record.get("side") if historical else record.get("side", {}).get("value"),
        *record.get("source_statuses", []),
    ]
    sources = record.get("sources" if historical else "source_occurrences", [])
    for source in sources:
        values.extend((source.get("kind"), source.get("path"), *source.get("source_flags", [])))
    for note in record.get("notes", []):
        values.extend((note.get("kind"), note.get("bead"), note.get("text")))
    values.append(record.get("bead"))
    return " ".join(str(value) for value in values if value is not None)


def _coefficient_strings(
    polynomial: Mapping[str, Any], *, degree: Any, context: str
) -> list[str]:
    values = polynomial.get("coefficients")
    if not isinstance(values, list) or not all(
        isinstance(value, str) and INTEGER.fullmatch(value) for value in values
    ):
        raise ExactCatalogueError(f"{context}: coefficients must be integer strings")
    if (
        not isinstance(degree, int)
        or isinstance(degree, bool)
        or degree < 0
        or len(values) != degree + 1
        or not values[0].lstrip("+-0")
    ):
        raise ExactCatalogueError(
            f"{context}: degree {degree} requires a complete nonzero lead"
        )
    return values


def output_files(register: Mapping[str, Any], *, papers: Path) -> dict[Path, str]:
    """Plan every output before publication; coefficient strings occur only in payloads.

    The publication subset omits superseded historical rows and current notes. Its
    fields survive except redundant polynomial text and LaTeX, whose complete
    representations remain in the archive. Retained nested note polynomials also get
    their own coefficient payload, so metadata never silently expands a large vector.
    """
    register = publication_register(register)
    files: dict[Path, str] = {}
    rows: list[dict[str, Any]] = []
    historical_counts: dict[int, int] = {}
    identities: set[str] = set()

    def add_record(record: Mapping[str, Any], *, section: str) -> None:
        n = record.get("n")
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            raise ExactCatalogueError(f"{section}: n must be a positive integer")
        historical = section == "historical"
        if historical:
            historical_counts[n] = historical_counts.get(n, 0) + 1
            ordinal = historical_counts[n]
            side_identity = str(record.get("side")).encode("utf-8").hex()
            identity = f"historical-n{n}-s{side_identity}"
            repeated_side = identity in identities
            if repeated_side:
                identity += f"-occurrence{ordinal}"
            component = f"H_{n},{ordinal}"
            title = f"Historical side for n = {n}: {record.get('side')}"
            certificate = record.get("source_certificate")
            if repeated_side and isinstance(certificate, Mapping):
                title += f" ({certificate['source_key']})"
        else:
            identity = f"current-n{n}"
            component = f"P_{n}" if record.get("polynomial") is not None else "recorded-side"
            title = f"Current recorded side for n = {n}"
        if identity in identities:
            raise ExactCatalogueError(f"duplicate catalogue identity: {identity}")
        identities.add(identity)

        def extract(value: Any, trail: tuple[str, ...], degree: Any = None) -> Any:
            if isinstance(value, list):
                return [extract(item, (*trail, str(index))) for index, item in enumerate(value)]
            if not isinstance(value, dict):
                return value
            if "coefficients" in value:
                coefficients = _coefficient_strings(value, degree=degree, context=identity)
                payload_id = (
                    identity if trail == ("polynomial",) else (identity + "-" + "-".join(trail))
                )
                if not re.fullmatch(r"[a-zA-Z0-9_-]+", payload_id):
                    raise ExactCatalogueError(
                        f"unsafe coefficient payload identity: {payload_id}"
                    )
                url = (Path(DATA_DIRECTORY) / "coefficients" / f"{payload_id}.json").as_posix()
                path = papers / url
                if path in files:
                    raise ExactCatalogueError(f"duplicate coefficient payload: {path}")
                files[path] = _json(
                    {
                        "schema_version": SCHEMA_VERSION,
                        "id": payload_id,
                        "order": "descending",
                        "coefficients": coefficients,
                    }
                )
                return {
                    **{
                        key: extract(item, (*trail, key))
                        for key, item in sorted(value.items())
                        if key not in {"coefficients", "text", "latex"}
                    },
                    "coefficients_url": url,
                    "order": "descending",
                }
            return {
                key: extract(item, (*trail, key), value.get("degree"))
                for key, item in sorted(value.items())
            }

        stripped = extract(dict(record), ())
        polynomial = stripped.get("polynomial")
        kind = "polynomial" if polynomial is not None else "numeric"
        coefficients_url = polynomial.get("coefficients_url") if polynomial else None
        metadata_url = (Path(DATA_DIRECTORY) / "metadata" / f"{identity}.json").as_posix()
        files[papers / metadata_url] = _json(
            {
                "schema_version": SCHEMA_VERSION,
                "id": identity,
                "section": section,
                "kind": kind,
                "claim": _claim(record, section),
                "record": stripped,
            }
        )
        rows.append(
            {
                "id": identity,
                "n": n,
                "section": section,
                "kind": kind,
                "component": component,
                "title": title,
                "status": record.get("kind") if historical else record.get("status"),
                "degree": record.get("degree"),
                "coefficient_digits": polynomial.get("height_digits") if polynomial else None,
                "metadata_url": metadata_url,
                "coefficients_url": coefficients_url,
                "legacy_anchor": None if historical else f"current-polynomial-for--{n}",
                "search_text": _search(record, historical=historical),
            }
        )

    for section, key in (("current", "entries"), ("historical", "historical_entries")):
        records = register.get(key, [])
        if not isinstance(records, list):
            raise ExactCatalogueError(f"register.{key} must be an array")
        for record in records:
            if not isinstance(record, dict):
                raise ExactCatalogueError(f"register.{key} records must be objects")
            add_record(record, section=section)
    files[papers / INDEX_PATH] = _json(
        {
            **{
                key: value
                for key, value in register.items()
                if key not in {"entries", "historical_entries"}
            },
            "schema_version": SCHEMA_VERSION,
            "entries": rows,
        }
    )
    return files
