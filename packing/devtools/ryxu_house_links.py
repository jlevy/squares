"""Current ry-xu atlas leaves reconstructed from private complete native inputs.

Generated leaves may be read-only links; facts, all actual jobs and metadata remain
private. No geometric predicate runs during admission, and drawing provenance never
assigns a result's confirmation rung.
"""

from __future__ import annotations

import copy
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import ryxu_arrangement_reports as reports
from devtools import ryxu_radical_n51 as radical
from devtools import squish_second_update_house_links as shared
from sqpack.yamlio import safe_load

NUMBERS = (51, 70, 84, 86, 102, 103, 105, 108, 123, 126, 127, 129, 131, 146, 175, 261, 267, 295)
SOURCE_KEY = "[ry-xu square packing 2026]"
SOURCE_ID = reports.SOURCE_KEY
RADICAL_SOURCE_ID = "ry-xu-undilated-n51-2026"
REPO = reports.REPO
RETRIEVED = "2026-10-08"
RADICAL_EXACT = "(16+5*sqrt(2))/3"
METADATA = reports.PACKET / "receipts/house-atlas-metadata.json.xz"
LIMITATIONS = (
    "Complete source geometry and native finite-feasibility outcomes retained privately. "
    "Only display coordinates are projected. No optimality, local minimum, rigidity, "
    "novelty, human oversight or unconfirmed contact-count claim. Drawing admission "
    "does not assign the imported result's confirmation rung."
)


def house_path(n: int) -> Path:
    if type(n) is not int or n not in NUMBERS:
        raise ValueError("count outside the selected ry-xu atlas roster")
    return REPO / "packing/witnesses/known-best" / f"n-{n:03d}.yaml"


def radical_display(digits: int = 16) -> str:
    """An upward decimal bound proved by exact Q(sqrt2) order, not its approximation."""
    if type(digits) is not int or not 1 <= digits <= 80:
        raise ValueError("bounded positive display precision required")
    side, _poses = radical.inputs("positive")
    scale = 10**digits
    with localcontext() as context:
        context.prec = digits + 20
        estimate = Decimal(16) / 3 + Decimal(5) / 3 * Decimal(2).sqrt()
        numerator = int(estimate * scale)
    while (radical.Q2(Fraction(numerator, scale)) - side).sign() < 0:
        numerator += 1
    while (radical.Q2(Fraction(numerator - 1, scale)) - side).sign() >= 0:
        numerator -= 1
    whole, fraction = divmod(numerator, scale)
    return f"{whole}.{fraction:0{digits}d}"


def source_url(n: int) -> str:
    reports.source_path(n)
    path = "square_packing_records.json" if n == 51 else reports.source_path(n)
    return f"{reports.SOURCE}/blob/{reports.REVISION}/{path}"


def bound(n: int) -> dict[str, Any]:
    house_path(n)
    if n == 51:
        radical.check_certification()
        return {
            "value": radical_display(),
            "exact_form": RADICAL_EXACT,
            "evidence": ["E-ryxu-432-radical-n51-feasibility"],
        }
    return reports.confirmed_bound(n)


def expected_witness(
    n: int,
    *,
    facts: dict[int, Any] | None = None,
    positives: dict[int, Any] | None = None,
    radical_rows: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """The complete house is a deterministic view of admitted source and actual results."""
    house_path(n)
    if n == 51:
        rows = radical.check_certification() if radical_rows is None else radical_rows
        witness = copy.deepcopy(rows["positive"]["native_input"])
        if witness["square_size"] != ["1", "0"]:
            raise ValueError("radical native unit-square literal differs")
        # Witness/v2 requires the unit literal "1"; the recorded field coefficient
        # pair is exactly that unit. Keep every source pose, side and field unchanged.
        witness["square_size"] = "1"
        result = copy.deepcopy(rows["positive"]["exact_verify"])
        fact = radical.fact_path()
    else:
        admitted = reports.check_certification() if positives is None else positives
        source_facts = reports.read_facts() if facts is None else facts
        witness = reports.to_witness(source_facts[n])
        result = copy.deepcopy(admitted[n]["exact_verify"])
        fact = reports.fact_path()
    identifier = f"W-known-best-n{n:03d}"
    witness["id"] = identifier
    witness["claim"]["coordinate_provenance"] = "verified"
    witness["claim"]["limitations"] = LIMITATIONS
    witness["source"] = {
        "key": SOURCE_KEY,
        "path": fact.relative_to(REPO / "packing").as_posix(),
        "url": source_url(n),
        "retrieved": RETRIEVED,
        "revision": reports.REVISION,
    }
    # The native geometry, field and diagnostics remain exactly the recorded outcome.
    # Only the public atlas identity changes; positive native provenance is verified.
    result["id"] = identifier
    witness["certificate"] = {
        "kind": "exact-number-field-sat" if n == 51 else "exact-rational-sat",
        "replay": f"uv run --frozen packing-witness verify witnesses/known-best/n-{n:03d}.yaml",
        "result": result,
    }
    return witness


def metadata(witness: dict[str, Any]) -> dict[str, Any]:
    """Complete non-geometric metadata, independent of the scalar representation."""
    return copy.deepcopy(
        {key: witness[key] for key in ("id", "claim", "source", "certificate")}
    )


def retain_metadata() -> None:
    facts = reports.read_facts()
    positives = reports.check_certification()
    radical_rows = radical.check_certification()
    rows = []
    for n in NUMBERS:
        expected = expected_witness(
            n, facts=facts, positives=positives, radical_rows=radical_rows
        )
        if shared.bounded_house(house_path(n)) != expected:
            raise ValueError(
                "complete ry-xu house differs from admitted source and native outcome"
            )
        rows.append({"n": n, "metadata": metadata(expected)})
    reports.save(METADATA, {"format": "ryxu-432-private-house-metadata-v1", "cases": rows})


def check_houses(numbers: list[int] | None = None) -> dict[int, Any]:
    selected = list(NUMBERS) if numbers is None else numbers
    if not selected or len(set(selected)) != len(selected):
        raise ValueError("unique selected ry-xu house roster required")
    for n in selected:
        house_path(n)
    if not METADATA.resolve().is_relative_to(REPO.resolve()):
        raise ValueError("ry-xu house metadata must remain private")
    record = reports.kernel.read_xz(METADATA)
    if (
        type(record) is not dict
        or set(record) != {"format", "cases"}
        or record["format"] != "ryxu-432-private-house-metadata-v1"
    ):
        raise ValueError("ry-xu private house metadata namespace mismatch")
    rows = shared.shared.roster(record["cases"], NUMBERS)
    facts = reports.read_facts()
    positives = reports.check_certification()
    radical_rows = radical.check_certification()
    result = {}
    for n in selected:
        path = house_path(n)
        if path.parent.is_symlink() or not path.parent.resolve().is_relative_to(REPO.resolve()):
            raise ValueError("ry-xu house parent escapes the private checkout")
        if path.is_symlink() and (path.parent / path.readlink()).is_symlink():
            raise ValueError("ry-xu house leaf must be a direct read-only link")
        expected = expected_witness(
            n, facts=facts, positives=positives, radical_rows=radical_rows
        )
        if rows[n]["metadata"] != metadata(expected):
            raise ValueError("ry-xu complete private house metadata or native result differs")
        actual = shared.bounded_house(path)
        if actual != expected:
            raise ValueError("ry-xu complete house geometry or metadata differs")
        result[n] = actual
    return result


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
        reports.fact_path(),
        reports.receipt_path(),
        radical.fact_path(),
        METADATA,
        reports.PACKET / "acquisition/frontier-prior-state.json.xz",
        *(
            reports.PACKET / f"receipts/n051-radical-{control}.json.xz"
            for control in reports.JOBS
        ),
    )


def linked_house_problem(path: str, *, repository: Path) -> str | None:
    allowed = {house_path(n).relative_to(REPO).as_posix(): n for n in NUMBERS}
    if repository.resolve() != REPO.resolve() or path not in allowed:
        return "artifact escapes the repository checkout"
    if not house_path(allowed[path]).is_symlink():
        return "artifact is not an admitted ry-xu leaf"
    try:
        check_houses([allowed[path]])
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as error:
        return f"ry-xu complete source/custody mismatch: {error}"
    return None
