"""Three exact #399 atlas leaves, reconstructed from private complete scientific inputs."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as reports
from devtools import squish_second_update_house_links as house
from sqpack.yamlio import safe_load

REPO = reports.REPO
NUMBERS = reports.NUMBERS


def house_path(n: int) -> Path:
    if type(n) is not int or n not in NUMBERS:
        raise reports.ReportError("count outside the three #399 atlas leaves")
    return REPO / "packing/witnesses/known-best" / f"n-{n:03d}.yaml"


def expected_house(
    certificate: reports.legacy.Certificate, positive: dict[str, Any]
) -> dict[str, Any]:
    """Bind the entire native result and metadata to the complete admitted source pose."""
    reports.validate_job(positive, certificate, "positive")
    witness = reports.to_witness(certificate)
    witness["representation"] = "corners"
    witness["squares"] = [
        {
            "id": index,
            "corners": [
                [reports.legacy.literal(x), reports.legacy.literal(y)] for x, y in square
            ],
        }
        for index, square in enumerate(reports.legacy.corner_squares(certificate), 1)
    ]
    identifier = f"W-known-best-n{certificate.n:03d}"
    witness["id"] = identifier
    witness["claim"]["coordinate_provenance"] = "verified"
    witness["source"] = {
        "key": reports.SOURCE_KEY,
        "path": reports.fact_path().relative_to(REPO).as_posix(),
        "url": f"{reports.SOURCE}/blob/{reports.REVISION}/{reports.source_path(certificate.n)}",
        "revision": reports.REVISION,
        "retrieved": "2026-10-07",
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
    """A selected producer repeats the exact decision and compares its full native result."""
    house_path(n)
    rows = reports.check_certification()
    witness = expected_house(reports.read_fact(n), rows[n])
    native, verification = reports.legacy.exact_verify(witness)
    if not verification.valid or native != witness["certificate"]["result"]:
        raise reports.ReportError("atlas decision differs from the complete actual replay")
    return witness


class VerifiedInputs:
    """Complete source and nine-job custody admitted within one caller invocation."""

    def __init__(self) -> None:
        self.rows = reports.check_certification()
        self.facts = reports.read_facts()


def check_houses(
    numbers: list[int] | None = None, *, verified_inputs: VerifiedInputs | None = None
) -> None:
    selected = list(NUMBERS) if numbers is None else numbers
    if (
        not selected
        or len(set(selected)) != len(selected)
        or any(type(n) is not int or n not in NUMBERS for n in selected)
    ):
        raise reports.ReportError("unique explicit #399 atlas roster required")
    if verified_inputs is not None and type(verified_inputs) is not VerifiedInputs:
        raise reports.ReportError("house inputs require complete validated #399 custody")
    inputs = VerifiedInputs() if verified_inputs is None else verified_inputs
    rows, facts = inputs.rows, inputs.facts
    for n in selected:
        path = house_path(n)
        if path.parent.is_symlink() or not path.parent.resolve().is_relative_to(REPO.resolve()):
            raise reports.ReportError("#399 atlas parent escapes private checkout")
        if path.is_symlink() and (path.parent / path.readlink()).is_symlink():
            raise reports.ReportError("#399 atlas leaf must be a direct read-only link")
        if house.bounded_house(path) != expected_house(facts[n], rows[n]):
            raise reports.ReportError("complete #399 atlas geometry or metadata differs")


def guard_house_outputs(numbers: list[int]) -> None:
    for n in NUMBERS:
        if n in numbers and not house_path(n).resolve().is_relative_to(REPO.resolve()):
            raise ValueError("#399 atlas producer output escapes the private checkout")


def snapshot_house_links() -> tuple[Path, ...]:
    controls = safe_load((REPO / "packing/devtools/controls.yaml").read_text())
    private = {(REPO / "packing" / row["file"]).resolve() for row in controls["controls"]}
    return tuple(house_path(n) for n in NUMBERS if house_path(n).resolve() not in private)


def private_input_paths() -> tuple[Path, ...]:
    """Both complete inputs and all nine complete native verdicts stay independently mutable."""
    return reports.fact_path(), reports.receipt_path()


def linked_house_problem(path: str, *, repository: Path) -> str | None:
    allowed = {house_path(n).relative_to(REPO).as_posix(): n for n in NUMBERS}
    if repository.resolve() != REPO.resolve() or path not in allowed:
        return "artifact escapes the repository checkout"
    if not house_path(allowed[path]).is_symlink():
        return "artifact is not an admitted #399 atlas leaf"
    try:
        check_houses([allowed[path]])
    except (ValueError, KeyError, TypeError, OSError) as error:
        return f"#399 source/custody mismatch: {error}"
    return None
