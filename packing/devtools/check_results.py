#!/usr/bin/env python3
"""Validate structural support for the results register's declared rungs.

`epistemics.md` owns the policy. This checker derives V1 and V3 through V5,
derives C0 through C5, requires explanations for declared-only V0 and V2, and
refuses unsupported promotion or unexplained understatement. It also resolves
evidence, repository-file and `produced_by` references -- the campaign records a
result came out of, which must exist -- requires retained controls at C3 and
above, restricts C5 to mapped review artifacts, and rejects unknown result ids
in the reader tier. Human review owns evidence relevance, claim coverage,
composition, significance, and novelty.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_results
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path, PurePosixPath

from sqpack.assurance import EXTERNAL_ORIGINS, PROOF_METHODS
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"
EVIDENCE = ROOT / "frontier" / "evidence.yaml"
READER_TIER = (REPO / "README.md", REPO / "SYNOPSIS.md")
DOCUMENT_MAP = REPO / "docs" / "project" / "document-map.yaml"
CAMPAIGN = ROOT / "campaign"
# What each `produced_by` key names, for the refusal message.
PRODUCED_BY_NOUNS = {
    "hypothesis": "hypothesis",
    "agenda_cell": "agenda commitment",
    "session": "agent session",
    "experiment": "experiment round",
}

MACHINE_METHODS = {"exact-algebraic", "interval-certified"}
OURS_ORIGINS = {"audited-here", "replayed-here"}
DECLARED_ONLY_V = {"V0", "V2"}


def _rank(rung: str) -> int:
    return int(rung[1])


def _machine_proof_shaped(entry: dict) -> bool:
    return (
        entry.get("method") in MACHINE_METHODS
        and bool(entry.get("certificate"))
        and bool(entry.get("replay"))
        and entry.get("replay_status") == "passed"
    )


def derive_confirmation(entries: list[dict], *, review_ready: bool = False) -> str:
    ours = [entry for entry in entries if entry.get("origin") in OURS_ORIGINS]
    machine = [entry for entry in ours if _machine_proof_shaped(entry)]
    if machine and review_ready:
        return "C5"
    if len({entry.get("method") for entry in machine}) >= 2:
        return "C4"
    if machine:
        return "C3"
    if any(entry.get("replay") and entry.get("replay_status") == "passed" for entry in ours):
        return "C2"
    if any(
        entry.get("origin") in EXTERNAL_ORIGINS
        and _qualifying_read(entry.get("external_review") or {})
        for entry in entries
    ):
        return "C1"
    return "C0"


def _qualifying_read(review: dict) -> bool:
    return (
        review.get("state") in {"informally-verified", "defect-found"}
        and bool(review.get("date"))
        and bool(review.get("reviewed_by"))
        and bool(review.get("note"))
    )


def _document_map_entry(path: str, document_map: dict) -> dict | None:
    for document in document_map["documents"]:
        if path == document["path"]:
            return document
    pure = PurePosixPath(path)
    return next(
        (
            collection
            for collection in document_map["collections"]
            if pure.match(collection["pattern"])
        ),
        None,
    )


def repository_file_problem(path: str) -> str | None:
    pure = PurePosixPath(path)
    if pure.is_absolute() or pure.as_posix() != path or ".." in pure.parts:
        return "must be a normalized repository-relative path"
    target = (REPO / pure).resolve()
    try:
        target.relative_to(REPO.resolve())
    except ValueError:
        return "resolves outside the repository"
    if not target.is_file():
        return "does not name a file"
    return None


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    return safe_load(text[4 : text.index("\n---", 4)]) or {}


def campaign_ids() -> dict[str, set[str]]:
    """The ids a `produced_by` entry may name, read from the campaign record.

    Hypotheses, sessions and rounds carry their id as the filename prefix, which is the
    naming rule `packing-ledger check` enforces, so the prefix is read rather than every
    frontmatter parsed. Agenda commitments live inside their agenda's frontmatter and
    are read from there.
    """

    def prefixes(paths: Iterable[Path], pattern: str) -> set[str]:
        return {match.group() for path in paths if (match := re.match(pattern, path.name))}

    cells: set[str] = set()
    for path in sorted((CAMPAIGN / "agendas").glob("agenda-*.md")):
        agenda = _frontmatter(path).get("agenda") or {}
        cells.update(item["id"] for item in agenda.get("items") or [])
    return {
        "hypothesis": prefixes((CAMPAIGN / "hypotheses").glob("H-*.md"), r"H-\d{3}"),
        "agenda_cell": cells,
        "session": prefixes(
            (CAMPAIGN / "agent-sessions").glob("session-*.md"), r"session-\d{3}"
        ),
        "experiment": prefixes(CAMPAIGN.glob("series/*/experiments/exp-*.md"), r"exp-\d{3}"),
    }


def derive_verification(entries: list[dict]) -> str:
    if any(entry.get("method") == "proof-assistant-checked" for entry in entries):
        return "V5"
    if any(_machine_proof_shaped(entry) for entry in entries):
        return "V4"
    if any(entry.get("method") in PROOF_METHODS and entry.get("proof") for entry in entries):
        return "V3"
    if any(
        str(entry.get("method", "")).startswith("numerical") and entry.get("precision")
        for entry in entries
    ):
        return "V1"
    return "V0"


def verification_relation(declared: str, derived: str) -> str:
    if declared == "V2" and _rank(derived) <= 1:
        return "supported"
    if _rank(declared) > _rank(derived):
        return "inflated"
    if _rank(declared) < _rank(derived):
        return "understated"
    return "supported"


def main() -> int:
    problems: list[str] = []
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    document_map = safe_load(DOCUMENT_MAP.read_text(encoding="utf-8"))
    evidence_index = {
        entry["id"]: entry
        for entry in safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }
    results = register["results"]
    known_ids = campaign_ids()

    expected_ids = [f"T-{index:03d}" for index in range(1, len(results) + 1)]
    actual_ids = [record["id"] for record in results]
    if actual_ids != expected_ids:
        problems.append(f"register ids are not contiguous T-001..: {actual_ids}")

    for record in results:
        rid = record["id"]
        scope = record["scope"]
        if "n_min" in scope and scope["n_min"] > scope["n_max"]:
            problems.append(
                f"{rid}: scope range is reversed: {scope['n_min']} > {scope['n_max']}"
            )
        cited: list[dict] = []
        for ref in record["evidence"]:
            entry = evidence_index.get(ref)
            if entry is None:
                problems.append(f"{rid}: cites unknown evidence {ref}")
                continue
            cited.append(entry)

        for field in ("artifacts", "controls"):
            problems.extend(
                f"{rid}: {field} path {problem}: {path}"
                for path in record.get(field) or []
                if (problem := repository_file_problem(path))
            )

        for kind, value in (record.get("produced_by") or {}).items():
            if value not in known_ids.get(kind, set()):
                problems.append(
                    f"{rid}: produced_by.{kind} names {value}, which is not a recorded "
                    f"{PRODUCED_BY_NOUNS.get(kind, kind)}"
                )

        declared_c = record["confirmation"]
        review = record.get("review_artifact")
        review_path_problem = repository_file_problem(review) if review else None
        review_exists = bool(review and review_path_problem is None)
        review_entry = _document_map_entry(review, document_map) if review else None
        review_mapped = bool(
            review_entry
            and review_entry.get("role") == "review"
            and review_entry.get("lifecycle") != "superseded"
        )
        derived_c = derive_confirmation(cited, review_ready=review_exists and review_mapped)
        has_composition = bool(record.get("composition"))
        if _rank(declared_c) > _rank(derived_c):
            problems.append(
                f"{rid}: declares {declared_c} but the cited atoms support only {derived_c}"
            )
        elif _rank(declared_c) < _rank(derived_c) and not has_composition:
            problems.append(
                f"{rid}: understates {derived_c} as {declared_c} with no "
                "composition note claiming the minimum over parts"
            )

        declared_v = record["verification"]
        if declared_v in DECLARED_ONLY_V and not record.get("notes"):
            problems.append(
                f"{rid}: {declared_v} is declared-only and needs a notes field saying why"
            )
        derived_v = derive_verification(cited)
        relation = verification_relation(declared_v, derived_v)
        if relation == "inflated":
            problems.append(
                f"{rid}: declares {declared_v} but the cited atoms support only {derived_v}"
            )
        elif relation == "understated" and not has_composition:
            problems.append(
                f"{rid}: understates {derived_v} as {declared_v} with no "
                "composition note claiming the minimum over parts"
            )

        if _rank(declared_c) >= 3 and not record.get("controls"):
            problems.append(f"{rid}: a {declared_c} rung names at least one control file")
        if declared_c == "C5":
            if not review:
                problems.append(f"{rid}: C5 requires review_artifact")
            elif not review_exists:
                problems.append(f"{rid}: review_artifact path {review_path_problem}: {review}")
            elif not review_mapped:
                problems.append(
                    f"{rid}: review_artifact is not a non-superseded review in the "
                    f"document map: {review}"
                )

    known = set(actual_ids)
    for path in READER_TIER:
        text = path.read_text(encoding="utf-8")
        problems.extend(
            f"{path.name}: mentions unknown result {mention}"
            for mention in sorted(set(re.findall(r"\bT-\d{3}\b", text)))
            if mention not in known
        )

    if problems:
        print(f"{len(problems)} results-register problems:")
        for line in problems:
            print(f"  {line}")
        return 1

    print(
        f"{len(results)} registered results: every declared rung passes its "
        "structural checks, every path and produced_by id resolves, every reader-tier "
        "mention exists"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
