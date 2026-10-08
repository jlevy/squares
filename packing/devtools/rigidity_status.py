"""One known-rigid flag for the displayed packing, with separate dated assessments.

The flag includes an explicit source assertion as well as a verified local-rigidity
argument. Their assurance stays distinct in metadata. A numerical screen with no
motion is never a positive assessment; a rigid alternative at the same side is never
evidence about the selected arrangement.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from functools import cache
from pathlib import Path
from typing import Any

from devtools.validate_schemas import check as check_schema
from sqpack.assurance import check_case_semantics
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO / "packing"
SOURCES = ROOT / "frontier/rigidity-sources.yaml"
MANIFEST = ROOT / "atlas/known-best/manifest.json"
EVIDENCE = ROOT / "frontier/evidence.yaml"


@dataclass(frozen=True)
class RigidityContext:
    audit: Mapping[str, Any]
    evidence: Mapping[str, Mapping[str, Any]]
    entries: Mapping[int, Mapping[str, Any]]


def date_precision(value: str | None) -> str:
    """Validate a real partial calendar date without inventing its missing precision."""
    if value is None:
        return "unknown"
    parts = value.split("-")
    precision = {1: "year", 2: "month", 3: "day"}.get(len(parts))
    if precision is None or len(parts[0]) != 4 or any(len(p) != 2 for p in parts[1:]):
        raise ValueError(f"invalid determination date: {value!r}")
    try:
        date.fromisoformat("-".join([*parts, *(["01"] * (3 - len(parts)))]))
    except ValueError as error:
        raise ValueError(f"invalid determination date: {value!r}") from error
    return precision


def _check_reference(reference: str | None) -> None:
    if reference is None:
        return
    path = REPO / reference.split("#", 1)[0]
    if not path.resolve().is_relative_to(REPO) or not path.is_file():
        raise ValueError(f"rigidity source reference does not resolve: {reference}")


@cache
def load_context() -> RigidityContext:
    errors = check_schema(SOURCES)
    if errors:
        raise ValueError("invalid rigidity source index: " + "; ".join(errors))
    audit = safe_load(SOURCES.read_text(encoding="utf-8"))["audit"]
    date.fromisoformat(audit["recorded_at"])
    for source in [
        *audit["evidence_dates"].values(),
        *audit["source_assertions"],
        *audit["alternatives"],
    ]:
        date_precision(source["determined_at"])
        _check_reference(source["reference"])
        _check_reference(source["date_reference"])
        if source["determined_at"] is not None and source["date_reference"] is None:
            raise ValueError("a rigidity determination date requires a cited date source")
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))["atlas"]["entries"]
    evidence = safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    return RigidityContext(
        audit=audit,
        evidence={entry["id"]: entry for entry in evidence},
        entries={entry["n"]: entry for entry in entries},
    )


def _dated_source(source: Mapping[str, Any], context: RigidityContext) -> dict[str, Any]:
    return {
        "reference": source["reference"],
        "determined_at": source["determined_at"],
        "determination_precision": date_precision(source["determined_at"]),
        "date_reference": source["date_reference"],
        "date_note": source["date_note"],
        "recorded_at": context.audit["recorded_at"],
        "recording_event": context.audit["recording_event"],
    }


def rigidity_metadata(
    n: int, packing: Mapping[str, Any], *, context: RigidityContext | None = None
) -> dict[str, Any]:
    """Derive the binary display decision without changing any proof's assurance."""
    context = load_context() if context is None else context
    entry = context.entries[n]
    reported = packing["reported_upper_bound"]
    if packing["n"] != n or reported["value"] != entry["reported_side"]:
        raise ValueError(f"n={n}: rigidity assessment and selected atlas construction differ")
    errors = [
        error
        for error in check_case_semantics(packing, context.evidence)
        if "rigidity:" in error
    ]
    if errors:
        raise ValueError("invalid rigidity assessment: " + "; ".join(errors))
    geometry = {
        "witness_id": entry["witness"]["id"],
        "witness_path": "packing/" + entry["witness"]["path"],
        "source_url": entry["source"].get("url"),
        "reported_side": entry["reported_side"],
    }
    assessments: list[dict[str, Any]] = []
    block = packing.get("rigidity")
    if block:
        sources = []
        for ref in block["evidence"]:
            source = context.audit["evidence_dates"].get(
                ref,
                {
                    "reference": f"packing/frontier/evidence.yaml#{ref}",
                    "determined_at": None,
                    "date_reference": None,
                    "date_note": (
                        "No determination date is recorded; "
                        "an evidence review does not supply one."
                    ),
                },
            )
            sources.append(
                {
                    **_dated_source(source, context),
                    "evidence_ref": ref,
                    "reviewed_at": context.evidence[ref].get("source_reviewed"),
                }
            )
        assessments.append(
            {
                "property": block["property"],
                "assurance": block["assurance"],
                "method": block["method"],
                "scope": block["scope"],
                "evidence_refs": list(block["evidence"]),
                "sources": sources,
            }
        )
    catalogue_matched = False
    for source in context.audit["source_assertions"]:
        if source["requires_catalogue_annotation"] and reported["catalogue_rigid"] != "rigid":
            continue
        matches = any(
            target["n"] == n
            and target["reported_side"] == geometry["reported_side"]
            and target["source_url"] == geometry["source_url"]
            for target in source["targets"]
        )
        if not matches:
            continue
        catalogue_matched |= source["requires_catalogue_annotation"]
        assessments.append(
            {
                "property": source["property"],
                "assurance": source["assurance"],
                "method": "source-assertion",
                "scope": (
                    "The cited source explicitly calls the selected construction rigid "
                    "at its fixed side."
                ),
                "evidence_refs": [],
                "sources": [
                    {
                        **_dated_source(source, context),
                        "source_id": source["id"],
                        "url": source["url"],
                    }
                ],
            }
        )
    if reported["catalogue_rigid"] == "rigid" and not catalogue_matched:
        raise ValueError(
            f"n={n}: catalogue rigidity has no source assertion matching the selected geometry"
        )
    known = any(
        assessment["property"] == "locally-rigid"
        and assessment["assurance"] in {"verified", "reported"}
        for assessment in assessments
    )
    if known and block and block["property"] in {"not-rigid", "semi-rigid"}:
        raise ValueError(
            f"n={n}: positive rigidity source conflicts with "
            "the selected packing's motion assessment"
        )
    return {"known_rigid": known, "assessed_geometry": geometry, "assessments": assessments}
