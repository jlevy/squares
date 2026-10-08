"""Cheap semantic custody and link/output refusal controls; never rerun a decider."""

from __future__ import annotations

import copy
import gzip
import json
import lzma
import shutil
from pathlib import Path

import pytest

from devtools import squish_second_update_confirmation as confirmation
from devtools import squish_second_update_house_links as house

SOURCE = confirmation.REPO
PACKET_RELATIVE = confirmation.PACKET.relative_to(SOURCE)
PROOFS_RELATIVE = confirmation.WITNESSES.relative_to(SOURCE)


@pytest.fixture
def private(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo = tmp_path / "private"
    shutil.copytree(SOURCE / PACKET_RELATIVE, repo / PACKET_RELATIVE)
    shutil.copytree(SOURCE / PROOFS_RELATIVE, repo / PROOFS_RELATIVE)
    schema = repo / "packing/witnesses/witness.schema.yaml"
    shutil.copyfile(SOURCE / "packing/witnesses/witness.schema.yaml", schema)
    monkeypatch.setattr(confirmation, "REPO", repo)
    monkeypatch.setattr(
        confirmation,
        "PACKET",
        repo / PACKET_RELATIVE,
    )
    monkeypatch.setattr(
        confirmation, "WITNESSES", repo / "packing/witnesses/squish-422-second-update-2026"
    )
    monkeypatch.setattr(confirmation, "SCHEMA", repo / "packing/witnesses/witness.schema.yaml")

    def forbidden(*_args, **_kwargs):
        pytest.fail("cheap admission called a decider")

    monkeypatch.setattr(confirmation.original, "decide", forbidden)
    monkeypatch.setattr(confirmation, "decide", forbidden)
    return repo


@pytest.fixture
def case(private: Path) -> tuple[dict, dict, dict]:
    assert private == confirmation.REPO
    value = confirmation.shared.read_xz_receipt(confirmation.case_path(88))
    admitted = confirmation.acquisition()
    protocol = confirmation.shared.read_review_json(
        confirmation.PACKET / "receipts/replay-protocol.json"
    )
    return value, admitted, protocol


def test_complete_canonical_scope_and_historical_equality(private: Path) -> None:
    rows = confirmation.check_certification()
    assert tuple(rows) == confirmation.NUMBERS
    assert sum(rows) == 1762
    assert sum(n * (n - 1) // 2 for n in rows) == 190303
    for n, row in rows.items():
        witness = confirmation.read_certificate(n)
        assert witness["id"] == f"W-squish-422-n{n:03d}"
        assert (
            witness["source"]["path"]
            == confirmation.fact_path(n).relative_to(private).as_posix()
        )
        case = row["case"]
        assert len(case["historical_actual_receipts"]) == 3
        for actual, transform in zip(
            case["historical_actual_receipts"], case["canonicalization"], strict=True
        ):
            assert transform["historical_metadata"] != transform["canonical_metadata"]
            assert (
                actual["source_custody_anchor"]
                == "/workspace/squares-422-import-preparation/source-pin.json"
            )
    assert confirmation.shared.NUMBERS == (
        123,
        126,
        129,
        153,
        154,
        155,
        179,
        208,
        237,
        238,
        239,
        258,
        263,
    )
    assert confirmation.shared.REVISION == "5e32bbd7028b6e3b869979278079cd37ed6770aa"


@pytest.fixture
def linked_proofs(private: Path) -> Path:
    store = private.parent / "proof-store"
    confirmation.WITNESSES.rename(store)
    confirmation.WITNESSES.symlink_to(store, target_is_directory=True)
    return private


@pytest.mark.slow
def test_linked_proof_batch_matches_all_fresh_standalone_checks(linked_proofs: Path) -> None:
    paths = [
        confirmation.certificate_path(n).relative_to(linked_proofs).as_posix()
        for n in confirmation.NUMBERS
    ]
    paths += [
        "packing/witnesses/squish-422-second-update-2026/n-089-rational.yaml.gz",
        "../outside.yaml",
        "/outside.yaml",
    ]
    batched = confirmation.linked_certificate_problems(paths, repository=linked_proofs)
    assert batched == {
        path: confirmation.linked_certificate_problem(path, repository=linked_proofs)
        for path in paths
    }
    assert all(batched[path] is None for path in paths[:9])
    assert all(batched[path] for path in paths[9:])
    assert all(confirmation.linked_certificate_problems(paths, repository=SOURCE).values())


@pytest.mark.parametrize("mutation", ["misbound", "malformed"])
def test_linked_proof_batch_rechecks_mutations_between_invocations(
    linked_proofs: Path, mutation: str
) -> None:
    paths = [
        confirmation.certificate_path(n).relative_to(linked_proofs).as_posix()
        for n in (88, 108)
    ]
    assert confirmation.linked_certificate_problems(
        paths, repository=linked_proofs
    ) == dict.fromkeys(paths)
    target = confirmation.certificate_path(88)
    replacement = (
        confirmation.certificate_path(108).read_bytes()
        if mutation == "misbound"
        else gzip.compress(b"not a witness")
    )
    target.write_bytes(replacement)
    batched = confirmation.linked_certificate_problems(paths, repository=linked_proofs)
    assert batched[paths[0]]
    assert batched[paths[1]] is None
    assert batched == {
        path: confirmation.linked_certificate_problem(path, repository=linked_proofs)
        for path in paths
    }


@pytest.mark.parametrize(
    "mutation",
    [
        "source",
        "id",
        "replay",
        "claim",
        "lastcorner",
        "reviewcorner",
        "bindingwitness",
        "count_bool",
        "verdict_bool",
        "drop_control",
        "drop_review",
        "canonical_metadata",
        "timing",
    ],
)
def test_complete_case_tamper_refused(case: tuple[dict, dict, dict], mutation: str) -> None:
    value, admitted, protocol = copy.deepcopy(case)
    actual = value["historical_actual_receipts"][0]
    if mutation == "source":
        actual["witness"]["source"]["path"] = "wrong-source.json"
    elif mutation == "id":
        actual["witness_id"] = "W-wrong"
    elif mutation == "replay":
        actual["witness"]["certificate"]["replay"] = "wrong-command"
    elif mutation == "claim":
        actual["witness"]["claim"]["limitations"] = "wrong-assurance"
    elif mutation == "lastcorner":
        actual["checker_input"]["squares"][-1]["corners"][-1][0] = "1/3"
    elif mutation == "reviewcorner":
        value["independent_review_inputs"]["math"][0]["checker_input"]["squares"][-1][
            "corners"
        ][-1][0] = "1/3"
    elif mutation == "bindingwitness":
        value["independent_review_inputs"]["binding"][0]["witness"]["source"]["path"] = (
            "wrong.json"
        )
    elif mutation == "count_bool":
        actual["exact_verify"]["pairs_tested"] = True
    elif mutation == "verdict_bool":
        actual["independent"]["verification_passed"] = 1
    elif mutation == "drop_control":
        value["historical_actual_receipts"].pop()
    elif mutation == "drop_review":
        value["independent_review_inputs"].pop("math")
    elif mutation == "canonical_metadata":
        value["canonicalization"][0]["canonical_metadata"]["source"]["path"] = "wrong.json"
    else:
        actual["wall_seconds"] += 1
    with pytest.raises(confirmation.original.PacketError):
        confirmation.validate_case(value, 88, admitted, protocol)


@pytest.mark.parametrize(
    "mutation", ["runtime", "schema", "summary_scope", "timing", "seed", "print_relation"]
)
def test_historical_protocol_tamper_refused(
    case: tuple[dict, dict, dict], mutation: str
) -> None:
    _, admitted, protocol = copy.deepcopy(case)
    if mutation == "runtime":
        protocol["historical_runtime"]["independent_module"] = "/tmp/fake.py"
    elif mutation == "schema":
        protocol["historical_runtime"]["schema_selected"] = "/tmp/witness.schema.yaml"
    elif mutation == "summary_scope":
        protocol["historical_execution_summary"]["jobs"].pop()
    elif mutation == "timing":
        protocol["historical_execution_summary"]["sum_dual_route_decision_wall_seconds"] += 1
    elif mutation == "seed":
        protocol["source_custody"]["cases"][0]["reported_seed"] = "wrong-credit"
    else:
        protocol["source_custody"]["cases"][0]["sourceprint_below_exact"] = True
    with pytest.raises(confirmation.original.PacketError):
        confirmation.validate_protocol(protocol, admitted)


def test_restore_refuses_linked_output_before_any_write(private: Path, tmp_path: Path) -> None:
    assert private == confirmation.REPO
    root = confirmation.WITNESSES
    original = {p.name: p.read_bytes() for p in root.iterdir()}
    shutil.rmtree(root)
    external = tmp_path / "external"
    external.mkdir()
    root.symlink_to(external, target_is_directory=True)
    with pytest.raises(confirmation.original.PacketError):
        confirmation.restore_witnesses()
    assert not list(external.iterdir())
    root.unlink()
    root.mkdir()
    confirmation.restore_witnesses()
    assert {p.name: p.read_bytes() for p in root.iterdir()} == original


def test_private_receipt_symlink_refused(private: Path, tmp_path: Path) -> None:
    assert private == confirmation.REPO
    path = confirmation.case_path(88)
    external = tmp_path / "case.json.xz"
    external.write_bytes(path.read_bytes())
    path.unlink()
    path.symlink_to(external)
    with pytest.raises(confirmation.original.PacketError):
        confirmation.admit_certification()


def test_xz_trailing_and_schema_contract_refused(private: Path) -> None:
    assert private == confirmation.REPO
    receipt = confirmation.case_path(88)
    receipt.write_bytes(receipt.read_bytes() + b"trailing")
    with pytest.raises(confirmation.original.PacketError):
        confirmation.admit_certification()
    certificate = confirmation.certificate_path(88)
    data = gzip.decompress(certificate.read_bytes()).replace(
        b"packing.squares:Witness/v2", b"wrong-contract"
    )
    certificate.write_bytes(gzip.compress(data))
    with pytest.raises(confirmation.original.PacketError):
        confirmation.read_certificate(88)


def add_house_files(private: Path) -> None:
    for n in confirmation.NUMBERS:
        path = house.house_path(n)
        path.parent.mkdir(parents=True, exist_ok=True)
        source = SOURCE / path.relative_to(private)
        if n in house.LINK_NUMBERS:
            path.symlink_to(source)
        else:
            shutil.copyfile(source, path)


def test_exact_house_link_reads_and_private_n263(private: Path) -> None:
    add_house_files(private)
    reviewed = house.check_houses()
    for n in confirmation.NUMBERS:
        actual = reviewed[n]
        assert len(actual["squares"]) == n
        assert house.house_path(n).is_symlink() is (n != 263)
    path = house.house_path(88).relative_to(private).as_posix()
    assert house.linked_house_problem(path, repository=private) is None
    assert house.linked_house_problem(
        "packing/witnesses/known-best/n-089.yaml", repository=private
    )
    assert house.linked_house_problem(path, repository=SOURCE)
    with pytest.raises(confirmation.original.PacketError):
        house.guard_house_outputs([88])
    house.guard_house_outputs([263])


def test_house_valid_geometry_wrong_metadata_refused(private: Path, tmp_path: Path) -> None:
    add_house_files(private)
    path = house.house_path(88)
    document = confirmation.safe_load(path.read_text())
    document["witness"]["source"]["revision"] = "wrong-source"
    external = tmp_path / "wrong.yaml"
    external.write_text(
        confirmation.witness_document(document["witness"], schema="../witness.schema.yaml")
    )
    path.unlink()
    path.symlink_to(external)
    assert house.linked_house_problem(path.relative_to(private).as_posix(), repository=private)


def test_house_metadata_and_link_chain_refused(private: Path, tmp_path: Path) -> None:
    add_house_files(private)
    path = house.house_path(88)
    intermediate = tmp_path / "intermediate.yaml"
    intermediate.symlink_to(path.readlink())
    path.unlink()
    path.symlink_to(intermediate)
    with pytest.raises(confirmation.original.PacketError):
        house.check_house(88)
    value = confirmation.shared.read_xz_receipt(house.metadata_path())
    value["cases"][0]["metadata"]["claim"]["limitations"] = "wrong-assurance"
    house.metadata_path().write_bytes(lzma.compress(json.dumps(value).encode()))
    with pytest.raises(confirmation.original.PacketError):
        house.check_house(263)


def test_registered_mutation_consumer_is_copied_before_linking(private: Path) -> None:
    controls = private / "packing/devtools/controls.yaml"
    controls.parent.mkdir(parents=True, exist_ok=True)
    controls.write_text(
        "controls:\n- file: witnesses/known-best/n-088.yaml\n- file: unrelated.yaml\n"
    )
    links = house.snapshot_house_links()
    assert house.house_path(88) not in links
    assert house.house_path(263) not in links
    assert set(links) == {house.house_path(n) for n in house.LINK_NUMBERS if n != 88}


def test_schema_custody_link_refused_even_with_identical_bytes(
    private: Path, tmp_path: Path
) -> None:
    assert private == confirmation.REPO
    schema = confirmation.SCHEMA
    external = tmp_path / "external-schema.yaml"
    external.write_bytes(schema.read_bytes())
    schema.unlink()
    schema.symlink_to(external)
    with pytest.raises(confirmation.original.PacketError, match="private confirmation input"):
        confirmation.admit_certification()


def test_house_diagnostic_exponent_refused(
    private: Path, case: tuple[dict, dict, dict]
) -> None:
    assert private == confirmation.REPO
    value = confirmation.shared.read_xz_receipt(house.metadata_path())
    metadata = value["cases"][0]["metadata"]
    metadata["certificate"]["result"]["minimum_best_pair_gap"] = "1e3"
    with pytest.raises(confirmation.original.PacketError, match="invalid exact"):
        house.validate_metadata(
            88, metadata, case[0]["historical_actual_receipts"][0]["exact_verify"]
        )


def test_confirmed_case_adoption_preserves_lower_and_refutes_older_conjecture(
    private: Path,
) -> None:
    assert private == confirmation.REPO
    current = (SOURCE / "packing/frontier/n-088.md").read_text()
    adapted = confirmation.adopt_verified(88, current)
    marker, end = "  rigidity:\n", "  conjectured_optimum:"
    assert (
        adapted.split(marker, 1)[1].split(end, 1)[0]
        == (current.split(marker, 1)[1].split(end, 1)[0])
    )
    assert confirmation.shared.json_bytes(
        confirmation.safe_load(adapted.split("---\n", 2)[1])["packing"]["rigidity"]
    ) == confirmation.shared.json_bytes(
        confirmation.safe_load(current.split("---\n", 2)[1])["packing"]["rigidity"]
    )
    case = confirmation.safe_load(adapted.split("---\n", 2)[1])["packing"]
    prior = confirmation.reported.prior_lanes()[88]
    for field, value in prior["hand_authored_lower"].items():
        assert case[field] == value
    assert case["verified_lower_bound"]["exact_form"] == "481/50"
    assert case["verified_upper_bound"]["evidence"] == [confirmation.EXACT_EVIDENCE]
    assert case["conjectured_optimum"] is None
    assert any(
        "is refuted by the confirmed feasible upper bound" in note["claim"]
        for note in case["priority_notes"]
    )
    assert all("pending confirmation" not in note["claim"] for note in case["priority_notes"])
    assert "E-evand-exact-ceilings-2026-10-05-exact-replay" in case["evidence"]
    assert confirmation.adopt_verified(88, adapted) == adapted


def test_confirmed_case_cannot_relabel_an_unreviewed_bound(private: Path) -> None:
    assert private == confirmation.REPO
    current = (SOURCE / "packing/frontier/n-088.md").read_text()
    _, front, body = current.split("---\n", 2)
    document = confirmation.safe_load(front)
    document["packing"]["verified_upper_bound"]["exact_form"] = "10"
    forged = "---\n" + confirmation.yaml.safe_dump(document) + "---\n" + body
    with pytest.raises(
        confirmation.original.PacketError, match="differs from admitted evidence"
    ):
        confirmation.adopt_verified(88, forged)
