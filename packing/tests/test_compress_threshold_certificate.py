"""Guards for the exp-161 Route S compression producer."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from devtools import compress_threshold_certificate as producer
from sqpack.fractional.threshold_coverage_encoding import FrozenCoverageEncoding


def test_source_revision_mismatch_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / producer.SOURCE_PATH
    source.parent.mkdir(parents=True)
    source.write_bytes(b"current\n")
    monkeypatch.setattr(producer, "REPOSITORY", tmp_path)
    monkeypatch.setattr(producer, "PACKING", tmp_path / "packing")
    monkeypatch.setattr(
        producer,
        "_git_content",
        lambda _revision, _path, *, label: b"reviewed\n" if label else b"",
    )

    with pytest.raises(producer.CompressionError, match="declared Git revision"):
        producer.authenticate_source(
            path=source,
            revision=producer.SOURCE_REVISION,
            expect_catalog_sha256=producer.FROZEN_CATALOG_SHA256,
        )
    assert producer.main(["--source", str(source), "--selftest"]) == 2


def test_wrong_expected_revision_is_refused_before_search() -> None:
    with pytest.raises(producer.CompressionError, match="expected frozen revision"):
        producer.build_receipt(expect_source_revision="0" * 40)
    assert producer.main(["--expect-source-revision", "0" * 40, "--selftest"]) == 2


def test_catalog_sha_mismatch_is_refused() -> None:
    with pytest.raises(producer.CompressionError, match="catalog SHA-256"):
        producer.build_receipt(expect_catalog_sha256="0" * 64)
    assert producer.main(["--expect-catalog-sha256", "0" * 64, "--selftest"]) == 2


def test_selftest_accepts_23_orbit_synthetic_and_rejects_24(tmp_path: Path) -> None:
    output = tmp_path / "selftest.json"

    assert producer.main(["--selftest", "--output", str(output)]) == 0

    receipt = json.loads(output.read_text(encoding="utf-8"))
    boundary = receipt["controls"]["policy_boundary"]
    synthetic = receipt["controls"]["synthetic_decompressor"]
    full = receipt["controls"]["full_manifest_roundtrip"]

    assert boundary["accepted_orbits"] == 23
    assert boundary["rejected_orbits"] == 24
    assert boundary["rejected_manifest_sha256"] == (
        "194f1f9f47fc94e7f945920c38a4efdb43476719eba025ea446a1d7b91fde27e"
    )
    assert boundary["rejected_before_decompression"] is True
    assert boundary["coverage_ran"] is False
    assert synthetic["selected_orbits"] == 23
    assert synthetic["compression_factor"] == "119/23"
    assert synthetic["satisfies_policy"] is True
    assert full["canonical_equivalent"] is True
    assert full["catalog_sha256"] == producer.FROZEN_CATALOG_SHA256
    assert full["orbits"] == 119
    assert full["atoms"] == 904
    assert receipt["controls"]["coverage_ran"] is False


def test_default_invocation_without_authorize_target_does_not_create_a_candidate(
    tmp_path: Path,
) -> None:
    output = tmp_path / "exp-161-route-s-threshold-compression.json"

    assert producer.main(["--output", str(output)]) == 0

    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["schema"] == producer.RECEIPT_SCHEMA
    assert receipt["source_revision"] == producer.SOURCE_REVISION
    assert receipt["catalog_sha256"] == producer.FROZEN_CATALOG_SHA256
    assert receipt["target_ran"] is False
    assert receipt["optimizer_ran"] is False
    assert receipt["candidate_created"] is False
    assert receipt["coverage_ran"] is False
    assert receipt["n_plus"] is None
    assert receipt["selected_orbits"] is None
    assert receipt["generating_account"] is None
    assert receipt["forbidden_control_manifests"] == [
        "53fbe28bd6dd022600515663ea1e3609ed2bd36a83e69e350b4bb3b45d7b7176",
        "007b394f48b0b11565ca87d09ad961258534c426bfd623a3e9bfc15aa6495e8a",
        "194f1f9f47fc94e7f945920c38a4efdb43476719eba025ea446a1d7b91fde27e",
    ]
    assert receipt["search_status"] == "not_run"
    assert receipt["authorization"] is None
    assert receipt["search"] is None
    assert receipt["controls"]["selftest_ran"] is True


def test_unauthorized_authorize_target_is_refused() -> None:
    for value in ("exp-160", "H-216", "H-217", "exp-162"):
        with pytest.raises(producer.CompressionError, match="not exp-161"):
            producer.build_receipt(authorize_target=value)
    assert producer.main(["--authorize-target", "H-216", "--selftest"]) == 2


def test_authorized_exp161_formulates_linear_coverage_without_a_candidate(
    tmp_path: Path,
) -> None:
    output = tmp_path / "authorized.json"

    assert producer.main(["--authorize-target", "exp-161", "--output", str(output)]) == 0

    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["authorization"] == "exp-161"
    assert receipt["target_ran"] is False
    assert receipt["optimizer_ran"] is False
    assert receipt["candidate_created"] is False
    assert receipt["coverage_ran"] is False
    assert receipt["n_plus"] is None
    assert receipt["search_status"] == "encoding_ready"
    search = receipt["search"]
    assert search["solver"] == "highs"
    assert search["includes_coverage"] is True
    assert search["coverage_linear"] is True
    assert search["coverage_enumerated"] is False
    assert search["optimizer_ran"] is False
    assert search["orbit_count"] == 119
    assert len(search["budget_coefficients"]) == 119
    assert "A w >= 1" in " ".join(search["constraints"])
    assert search["float_incumbent"] is None


def test_search_without_encode_coverage_is_refused() -> None:
    assert producer.main(["--authorize-target", "exp-161", "--search", "--selftest"]) == 2


def test_encode_coverage_without_authorization_is_refused() -> None:
    assert producer.main(["--encode-coverage", "--selftest"]) == 2


def test_authorized_encode_coverage_stub_still_emits_no_candidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:

    encoding = FrozenCoverageEncoding(
        orbit_count=119,
        direction_count=1,
        reachable_cells=1,
        direction_unique_rows=1,
        pareto_rows=np.array([[1] + [0] * 118], dtype=np.uint8),
        budget_coefficients=(1,) * 119,
        rows_sha256="ab" * 32,
    )
    monkeypatch.setattr(producer, "encode_frozen_coverage", lambda _inventory: encoding)
    output = tmp_path / "encoded.json"

    assert (
        producer.main(
            ["--authorize-target", "exp-161", "--encode-coverage", "--output", str(output)]
        )
        == 0
    )

    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["candidate_created"] is False
    assert receipt["coverage_ran"] is False
    assert receipt["n_plus"] is None
    assert receipt["search_status"] == "encoding_complete"
    assert receipt["search"]["coverage_enumerated"] is True
    assert receipt["search"]["encoding"]["pareto_row_count"] == 1
    assert receipt["forbidden_control_manifests"] == [
        "53fbe28bd6dd022600515663ea1e3609ed2bd36a83e69e350b4bb3b45d7b7176",
        "007b394f48b0b11565ca87d09ad961258534c426bfd623a3e9bfc15aa6495e8a",
        "194f1f9f47fc94e7f945920c38a4efdb43476719eba025ea446a1d7b91fde27e",
    ]


def test_authorized_search_after_stub_encoding_still_emits_no_candidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:

    encoding = FrozenCoverageEncoding(
        orbit_count=119,
        direction_count=1,
        reachable_cells=1,
        direction_unique_rows=1,
        pareto_rows=np.array([[1] + [0] * 118], dtype=np.uint8),
        budget_coefficients=(1,) * 119,
        rows_sha256="ab" * 32,
    )
    monkeypatch.setattr(producer, "encode_frozen_coverage", lambda _inventory: encoding)
    output = tmp_path / "searched.json"

    assert (
        producer.main(
            [
                "--authorize-target",
                "exp-161",
                "--encode-coverage",
                "--search",
                "--output",
                str(output),
            ]
        )
        == 0
    )

    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["candidate_created"] is False
    assert receipt["coverage_ran"] is False
    assert receipt["n_plus"] is None
    assert receipt["search"]["optimizer_ran"] is True
    assert receipt["search"]["float_incumbent"] is not None
    assert receipt["search"]["float_incumbent"]["n_plus"] is not None


def test_output_cannot_overwrite_the_bound_source() -> None:
    assert producer.main(["--output", str(producer.REPOSITORY / producer.SOURCE_PATH)]) == 2
