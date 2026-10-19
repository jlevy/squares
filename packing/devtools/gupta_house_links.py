"""Fourteen Gupta atlas leaves admitted against private complete native inputs.

Source facts and all fifty-one actual jobs remain privately copied. Full-house
admission executes no geometric predicate and assigns no result confirmation rung.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from devtools import gupta_refinement_reports as reports
from devtools import squish_second_update_house_links as shared
from sqpack.yamlio import safe_load

REPO = reports.REPO
NUMBERS = reports.SELECTED
HISTORY = reports.PACKET / "acquisition/frontier-prior-state.json.xz"


def house_path(n: int) -> Path:
    if type(n) is not int or n not in NUMBERS:
        raise reports.kernel.ReportError("count outside the fourteen Gupta atlas leaves")
    return REPO / "packing/witnesses/known-best" / f"n-{n:03d}.yaml"


def expected_house(
    certificate: reports.legacy.Certificate, positive: dict[str, Any]
) -> dict[str, Any]:
    """Preserve every exact source pose and full native result in a deterministic view."""
    house_path(certificate.n)
    reports.validate_job(positive, certificate, "positive")
    witness = reports.kernel.to_witness(
        certificate,
        witness_prefix=reports.WITNESS_PREFIX,
        claim_limitations=reports.CLAIM_LIMITATIONS,
    )
    identifier = f"W-known-best-n{certificate.n:03d}"
    witness["id"] = identifier
    witness["claim"]["coordinate_provenance"] = "verified"
    source = reports.source_pins()[certificate.n]["certificate"]
    witness["source"] = {
        "key": reports.SOURCE_KEY,
        "path": reports.fact_path().relative_to(REPO / "packing").as_posix(),
        "url": f"{reports.SOURCE}/blob/{reports.REVISION}/{source}",
        "revision": reports.REVISION,
        "retrieved": "2026-10-08",
    }
    native = copy.deepcopy(positive["exact_verify"])
    native["id"] = identifier
    witness["certificate"] = {
        "kind": "exact-rational-sat",
        "replay": (
            "uv run --frozen packing-witness verify "
            f"witnesses/known-best/n-{certificate.n:03d}.yaml"
        ),
        "result": native,
    }
    return witness


def build_witness(n: int) -> dict[str, Any]:
    """Reconstruct the full house from admitted executions without repeating a decision."""
    house_path(n)
    positives = reports.check_certification()
    return expected_house(reports.read_fact(n), positives[n])


def check_houses(numbers: list[int] | None = None) -> None:
    selected = list(NUMBERS) if numbers is None else numbers
    if not selected or len(set(selected)) != len(selected):
        raise reports.kernel.ReportError("unique explicit Gupta atlas roster required")
    for n in selected:
        house_path(n)
    positives = reports.check_certification()
    facts = reports.read_facts()
    for n in selected:
        path = house_path(n)
        if path.parent.is_symlink() or not path.parent.resolve().is_relative_to(REPO.resolve()):
            raise reports.kernel.ReportError("Gupta atlas parent escapes private checkout")
        if path.is_symlink() and (path.parent / path.readlink()).is_symlink():
            raise reports.kernel.ReportError("Gupta atlas leaf must be a direct read-only link")
        if shared.bounded_house(path) != expected_house(facts[n], positives[n]):
            raise reports.kernel.ReportError(
                "complete Gupta house geometry or metadata differs"
            )


def guard_house_outputs(numbers: list[int]) -> None:
    for n in NUMBERS:
        if n in numbers:
            shared.confirmation.guard_output(house_path(n))


def snapshot_house_links() -> tuple[Path, ...]:
    controls = safe_load((REPO / "packing/devtools/controls.yaml").read_text())
    private = {(REPO / "packing" / row["file"]).resolve() for row in controls["controls"]}
    return tuple(house_path(n) for n in NUMBERS if house_path(n) not in private)


def private_input_paths() -> tuple[Path, ...]:
    return (
        reports.PACKET / "acquisition/case-inputs.json",
        reports.fact_path(),
        reports.receipt_path(),
        HISTORY,
    )


def linked_house_problem(path: str, *, repository: Path) -> str | None:
    allowed = {house_path(n).relative_to(REPO).as_posix(): n for n in NUMBERS}
    if repository.resolve() != REPO.resolve() or path not in allowed:
        return "artifact escapes the repository checkout"
    if not house_path(allowed[path]).is_symlink():
        return "artifact is not an admitted Gupta leaf"
    try:
        check_houses([allowed[path]])
    except (ValueError, KeyError, TypeError, OSError) as error:
        return f"Gupta complete source/custody mismatch: {error}"
    return None
