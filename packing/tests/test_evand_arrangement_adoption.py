"""Complete new-pose adoption, preserved history and exact private atlas custody."""

from __future__ import annotations

import copy
import json
import lzma
import shutil
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from devtools import build_known_best_atlas as atlas
from devtools import evand_arrangement_houses as houses
from devtools import evand_arrangement_reports as reports
from devtools import register_evand_arrangements as adoption
from devtools import run_negative_controls as controls
from sqpack.witness import witness_document
from sqpack.yamlio import safe_load

SOURCE = reports.REPO


@pytest.fixture
def private(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    tree = tmp_path / "private"
    packet = tree / reports.PACKET.relative_to(SOURCE)
    for path in houses.private_input_paths():
        target = tree / path.relative_to(SOURCE)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for n in reports.NUMBERS:
        target = tree / houses.house_path(n).relative_to(SOURCE)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(houses.house_path(n))
    monkeypatch.setattr(reports, "REPO", tree)
    monkeypatch.setattr(reports, "PACKET", packet)
    monkeypatch.setattr(houses, "REPO", tree)
    return tree


@pytest.mark.parametrize("n", reports.NUMBERS)
def test_exact_new_pose_adoption_preserves_historical_case_and_is_idempotent(n: int) -> None:
    prior = reports.read_xz(reports.PACKET / "acquisition/prior-state.json.xz")
    original = next(row["complete_case"] for row in prior if row["n"] == n)
    adopted = adoption.adopt_case(n, original)
    case = safe_load(adopted.split("---\n", 2)[1])["packing"]
    old = safe_load(original.split("---\n", 2)[1])["packing"]
    assert Decimal(case["verified_upper_bound"]["value"]) < Decimal(
        old["verified_upper_bound"]["value"]
    )
    assert case["reported_upper_bound"]["exact_form"] == reports.legacy.literal(
        reports.read_fact(n).side
    )
    assert case["reported_lower_bound"] == old["reported_lower_bound"]
    assert case["verified_lower_bound"] == old["verified_lower_bound"]
    assert case["rigidity"] is None
    assert case["conjectured_optimum"] is None
    assert set(old["evidence"]) <= set(case["evidence"])
    assert all(resource in case["resources"] for resource in old["resources"])
    assert old["reported_upper_bound"]["value"] in str(case["priority_notes"])
    assert adoption.adopt_case(n, adopted) == adopted
    assert "earlier #375" in adopted


def test_generator_preserves_new_geometry_and_adopts_ordinary_lower_lane() -> None:
    n = 266
    existing = (SOURCE / "packing/frontier/n-266.md").read_text()
    document = safe_load(existing.split("---\n", 2)[1])
    document["packing"]["verified_lower_bound"] = {
        "value": "16",
        "exact_form": "16",
        "evidence": ["E-area-lower"],
    }
    generated = (
        "---\n" + adoption.registry.dump(document) + "---\n" + existing.split("---\n", 2)[2]
    )
    result = adoption.adopt_case(n, existing, generated)
    case = safe_load(result.split("---\n", 2)[1])["packing"]
    assert case["verified_lower_bound"]["value"] == "16"
    assert case["reported_upper_bound"]["exact_form"] == reports.legacy.literal(
        reports.read_fact(n).side
    )
    assert case["verified_upper_bound"] == reports.confirmed_bound(n)


def test_actual_houses_bind_every_complete_input_and_native_field(private: Path) -> None:
    assert private == reports.REPO
    houses.check_houses()
    row = reports.check_certification()[266]
    expected = houses.expected_house(reports.read_fact(266), row)
    assert len(expected["squares"]) == 266
    assert expected["certificate"]["result"]["pairs_tested"] == 35245
    assert expected["source"]["path"].startswith("packing/")
    assert (
        houses.linked_house_problem(
            "packing/witnesses/known-best/n-266.yaml", repository=private
        )
        is None
    )
    assert (
        houses.linked_house_problem(
            "packing/witnesses/known-best/n-267.yaml", repository=private
        )
        is not None
    )


@pytest.mark.parametrize(
    "change", ["last-pose", "side", "source", "claim", "native-minimum", "native-limitations"]
)
def test_individual_linked_leaf_mutation_is_refused(
    private: Path, tmp_path: Path, change: str
) -> None:
    assert private == reports.REPO
    witness = houses.house.bounded_house(houses.house_path(266))
    if change == "last-pose":
        witness["squares"][-1]["corners"][0][0] = "0"
    elif change == "side":
        witness["side"] = "17"
    elif change == "source":
        witness["source"]["key"] = "[wrong]"
    elif change == "claim":
        witness["claim"]["limitations"] = "Globally optimal."
    elif change == "native-minimum":
        witness["certificate"]["result"]["minimum_best_pair_gap"] = "1"
    else:
        witness["certificate"]["result"]["limitations"] = "Globally optimal."
    changed = tmp_path / "changed.yaml"
    changed.write_text(witness_document(witness, schema="../witness.schema.yaml"))
    houses.house_path(266).unlink()
    houses.house_path(266).symlink_to(changed)
    houses.check_houses([270])
    with pytest.raises(reports.ReportError, match="geometry or metadata"):
        houses.check_houses([266])


def test_each_standalone_call_rereads_private_receipt_and_full_facts(private: Path) -> None:
    assert private == reports.REPO
    houses.check_houses([266])
    record = reports.read_xz(reports.receipt_path())
    changed = copy.deepcopy(record)
    changed["cases"][-1]["checker_input"]["poses"][-1][2] = "1"
    reports.save_xz(reports.receipt_path(), changed)
    with pytest.raises(reports.ReportError):
        houses.check_houses([266])
    reports.save_xz(reports.receipt_path(), record)
    houses.check_houses([266])
    facts = reports.read_xz(reports.fact_path())
    facts["cases"][-1]["source_certificate"] += "\n1 1 0\n"
    reports.save_xz(reports.fact_path(), facts)
    with pytest.raises(reports.ReportError):
        houses.check_houses([266])


def test_all_house_producers_refuse_before_writing(private: Path) -> None:
    assert private == reports.REPO
    before = houses.house_path(266).read_bytes()
    for producer in (
        lambda: houses.guard_house_outputs([266]),
        lambda: atlas.update_selected([266]),
        atlas.update,
    ):
        with pytest.raises(ValueError, match="escapes"):
            producer()
        assert houses.house_path(266).read_bytes() == before


def test_production_clone_copies_every_scientific_input_and_admits_exact_links(
    tmp_path: Path,
) -> None:
    assert set(houses.private_input_paths()) <= set(controls.COPY_SEPARATELY)
    assert controls.snapshot_source_bytes() <= controls.SNAPSHOT_MAX_BYTES
    tree = tmp_path / "worker"
    controls.clone_tree(tree)
    for path in houses.private_input_paths():
        copied = tree / path.relative_to(SOURCE)
        assert copied.is_file()
        assert not copied.is_symlink()
        assert copied.read_bytes() == path.read_bytes()
    env = controls.control_environment(tree, tmp_path / "pycache")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from devtools.evand_arrangement_houses import check_houses; check_houses()",
        ],
        cwd=tree / controls.HERE,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    leaf = tree / houses.house_path(266).relative_to(SOURCE)
    before = leaf.read_bytes()
    refused = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "from devtools.evand_arrangement_houses import guard_house_outputs; "
                "guard_house_outputs([266])"
            ),
        ],
        cwd=tree / controls.HERE,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert refused.returncode != 0
    assert "escapes" in refused.stderr
    assert leaf.read_bytes() == before
    child_receipt = tree / reports.receipt_path().relative_to(SOURCE)
    record: Any = reports.read_xz(child_receipt)
    record["cases"][0]["exact_verify"]["pairs_tested"] -= 1
    child_receipt.write_bytes(lzma.compress(json.dumps(record).encode()))
    rejected = subprocess.run(
        [
            sys.executable,
            "-c",
            "from devtools.evand_arrangement_houses import check_houses; check_houses()",
        ],
        cwd=tree / controls.HERE,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=45,
    )
    assert rejected.returncode != 0
    assert "native exact route" in rejected.stderr
