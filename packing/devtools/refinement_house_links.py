"""Three atlas leaves with private complete facts and metadata admission.

Only generated, read-only leaves may link to the parent checkout. Registered mutation
targets remain copied and indexed; producers refuse a linked output before writing.
The complete witness is reconstructed from independently pinned private source facts.
"""

from __future__ import annotations

import copy
import lzma
from pathlib import Path
from typing import Any

from devtools import refinement_custody as custody
from devtools import refinement_packets as packets
from devtools import squish_second_update_house_links as house
from sqpack.yamlio import safe_load

NUMBERS = (68, 105, 292)
REPO = packets.REPO
METADATA = packets.COUZO.packet / "receipts/house-metadata.json.xz"
LIMITATIONS = (
    "Exact rational corners from the retained centered source, checked "
    "with exact predicates at the full rational side. Drawing feasibility "
    "does not assign the imported result's confirmation rung. No optimality, "
    "rigidity or human oversight claim."
)


def source(n: int) -> packets.Source:
    return next(item for item in packets.SOURCES.values() if n in item.numbers)


def house_path(n: int) -> Path:
    if type(n) is not int or n not in NUMBERS:
        raise ValueError("count outside the three refinement atlas leaves")
    return REPO / "packing/witnesses/known-best" / f"n-{n:03d}.yaml"


def expected_metadata(n: int, result: dict[str, Any]) -> dict[str, Any]:
    witness = packets.to_witness(source(n), n)
    witness["id"] = f"W-known-best-n{n:03d}"
    witness["claim"]["coordinate_provenance"] = "verified"
    witness["claim"]["limitations"] = LIMITATIONS
    witness["certificate"] = {
        "kind": "exact-rational-sat",
        "replay": f"uv run --frozen packing-witness verify witnesses/known-best/n-{n:03d}.yaml",
        "result": result,
    }
    return house.confirmation.metadata(witness)


def validate_metadata(n: int, value: dict[str, Any]) -> None:
    result = value["certificate"]["result"]
    house.shared.validate_verdict(result, n, passed=True)
    if (
        value != expected_metadata(n, result)
        or set(result)
        != {
            "operation",
            "id",
            "coordinate_provenance",
            "method",
            "verification_passed",
            "n",
            "side",
            "pairs_tested",
            "minimum_containment_clearance",
            "minimum_best_pair_gap",
            "field_certificate",
            "failures",
            "limitations",
        }
        or result["id"] != f"W-known-best-n{n:03d}"
        or result["operation"] != "verify"
        or result["coordinate_provenance"] != "verified"
        or result["method"] != "exact-algebraic"
        or result["side"] != packets.read_fact(source(n), n)["side"]
        or result["field_certificate"]
        != {"field": "Q", "preconditions": "degree-one rational field"}
        or result["limitations"]
        != "Verifies witness feasibility and its upper bound, not global optimality."
    ):
        raise ValueError("refinement house metadata differs from private facts")
    index = custody.read_index()
    if n in packets.COUZO.numbers:
        actual = next(
            row for row in index["couzo_jobs"] if row["n"] == n and row["name"] == "positive"
        )
        native = copy.deepcopy(actual["verdict"]["routes"]["exact_verify"])
        native["id"] = f"W-known-best-n{n:03d}"
        if result != native:
            raise ValueError("house native result differs from the actual complete replay")
    else:
        actual = index["n68_jobs"][0]["routes"][0]["result"]
        if (
            result["minimum_best_pair_gap"] != actual["minimum_pair_gap"]
            or result["minimum_containment_clearance"] != actual["minimum_wall_gap"]
        ):
            raise ValueError("house exact minima differ from both accepted source routes")


def retain_metadata() -> None:
    rows = []
    for n in NUMBERS:
        actual = house.bounded_house(house_path(n))
        metadata = house.confirmation.metadata(actual)
        validate_metadata(n, metadata)
        expected = packets.to_witness(source(n), n)
        expected.update(metadata)
        if actual != expected:
            raise ValueError("complete refinement house differs from pinned source")
        rows.append({"n": n, "metadata": metadata})
    packets.save(METADATA, lzma.compress(packets.json_bytes(rows)))


def check_houses(numbers: list[int] | None = None) -> None:
    selected = list(NUMBERS) if numbers is None else numbers
    if (
        not selected
        or len(set(selected)) != len(selected)
        or any(n not in NUMBERS for n in selected)
    ):
        raise ValueError("unique refinement leaf roster required")
    if not METADATA.resolve().is_relative_to(REPO.resolve()):
        raise ValueError("refinement metadata custody must remain private")
    rows = house.shared.roster(house.shared.read_xz_receipt(METADATA), NUMBERS)
    for n in selected:
        path = house_path(n)
        if path.parent.is_symlink() or not path.parent.resolve().is_relative_to(REPO.resolve()):
            raise ValueError("refinement house parent escapes the private checkout")
        if path.is_symlink() and (path.parent / path.readlink()).is_symlink():
            raise ValueError("refinement leaf must be a direct read-only link")
        metadata = rows[n]["metadata"]
        validate_metadata(n, metadata)
        expected = packets.to_witness(source(n), n)
        expected.update(copy.deepcopy(metadata))
        if house.bounded_house(path) != expected:
            raise ValueError("complete refinement geometry or private metadata differs")


def guard_house_outputs(numbers: list[int]) -> None:
    for n in NUMBERS:
        if n in numbers:
            house.confirmation.guard_output(house_path(n))


def snapshot_house_links() -> tuple[Path, ...]:
    controls = safe_load((REPO / "packing/devtools/controls.yaml").read_text())
    private = {(REPO / "packing" / row["file"]).resolve() for row in controls["controls"]}
    return tuple(house_path(n) for n in NUMBERS if house_path(n) not in private)


def private_input_paths() -> tuple[Path, ...]:
    """Minimal complete scientific custody copied before read-only atlas links."""
    return (
        METADATA,
        custody.INDEX,
        *(packets.fact_path(source(n), n) for n in NUMBERS),
    )


def linked_house_problem(path: str, *, repository: Path) -> str | None:
    allowed = {house_path(n).relative_to(REPO).as_posix(): n for n in NUMBERS}
    if repository.resolve() != REPO.resolve() or path not in allowed:
        return "artifact escapes the repository checkout"
    if not house_path(allowed[path]).is_symlink():
        return "artifact is not an admitted refinement leaf"
    try:
        check_houses([allowed[path]])
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as error:
        return f"refinement source/custody mismatch: {error}"
    return None
