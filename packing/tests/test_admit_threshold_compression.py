"""Admission controls for the target-blind Route S compression surface."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools import admit_threshold_compression as admission
from sqpack.cli import validate


def _record() -> dict[str, object]:
    return json.loads(admission.ADMISSION.read_text(encoding="utf-8"))


def _write(path: Path, record: object) -> Path:
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def test_retained_admission_replays_without_running_a_target() -> None:
    receipt = admission.build_receipt()

    assert receipt["status"] == "blocked"
    assert receipt["admission_blockers"] == [
        "pin all T-025/T-026 digests outside the mutable admission record",
        "bind both the 720-step and 1440-step T-026 provenance sentinels",
        "admit a canonical selection-manifest parser and serializer",
        "exercise every mutation refusal declared by X-032",
    ]
    assert receipt["control"]["orbits"] == 119
    assert receipt["control"]["atoms"] == 904
    assert receipt["control"]["decompressor_roundtrip"] == {
        "role": "full authenticated T-025 decompressor control",
        "canonical_equivalent": True,
        "catalog_sha256": receipt["control"]["catalog_sha256"],
        "orbits": 119,
        "atoms": 904,
        "total_budget": "685457679/62500000",
    }
    assert receipt["sentinel"]["reproduced"] is True
    assert receipt["quantization_control"] == {
        "denominator": 30_000,
        "rounded_budget": "82373/7500",
        "budget_below_n": True,
        "support_changed": False,
        "research_success": False,
    }
    assert receipt["synthetic_decompressor"]["selected_orbits"] == 23
    assert receipt["synthetic_decompressor"]["compression_factor"] == "119/23"
    assert receipt["synthetic_decompressor"]["satisfies_policy"] is True
    for field in (
        "target_ran",
        "optimizer_ran",
        "coverage_ran",
        "candidate_created",
        "experiment_created",
    ):
        assert receipt[field] is False


def test_output_is_byte_identical_to_the_retained_receipt(tmp_path: Path) -> None:
    output = tmp_path / "receipt.json"

    assert admission.main(["--output", str(output)]) == 0
    assert output.read_bytes() == admission.RECEIPT.read_bytes()
    assert admission.main(["--check"]) == 0


@pytest.mark.parametrize(
    ("section", "field", "value"),
    [
        ("control", "path", "../certificate.json"),
        ("control", "sha256", "0" * 64),
        ("control", "catalog_sha256", "a" * 64),
        ("sentinel", "source_path", "/tmp/certificate.json"),
        ("sentinel", "source_sha256", "f" * 64),
        ("family", "max_orbits", 24),
        ("execution_boundary", "target_ran", True),
        ("quantization_control", "denominator", 29_999),
    ],
)
def test_contract_mutations_are_refused(
    tmp_path: Path, section: str, field: str, value: object
) -> None:
    record = _record()
    nested = record[section]
    assert isinstance(nested, dict)
    nested[field] = value

    with pytest.raises(admission.AdmissionError):
        admission.build_receipt(_write(tmp_path / "mutated.json", record))


def test_duplicate_keys_and_floating_numbers_are_refused(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"schema":"one","schema":"two"}\n', encoding="utf-8")
    floating = tmp_path / "floating.json"
    floating.write_text('{"max_orbits":23.0}\n', encoding="utf-8")

    with pytest.raises(admission.AdmissionError, match="duplicate"):
        admission.load_json(duplicate, label="control")
    with pytest.raises(admission.AdmissionError, match="floating"):
        admission.load_json(floating, label="control")


def test_byte_and_depth_limits_are_enforced_before_contract_parsing(tmp_path: Path) -> None:
    too_large = tmp_path / "large.json"
    too_large.write_text('{"x":"' + "x" * 64 + '"}\n', encoding="utf-8")
    too_deep = tmp_path / "deep.json"
    too_deep.write_text("[" * 17 + "0" + "]" * 17, encoding="utf-8")

    with pytest.raises(admission.AdmissionError, match="byte"):
        admission.load_json(too_large, label="control", limit=32)
    with pytest.raises(admission.AdmissionError, match="depth"):
        admission.load_json(too_deep, label="control")


def test_output_cannot_overwrite_a_bound_input() -> None:
    assert admission.main(["--output", str(admission.ADMISSION)]) == 2


def test_validation_step_runs_the_retained_check(monkeypatch: pytest.MonkeyPatch) -> None:
    observed: tuple[str, ...] | None = None

    def capture(_context: validate.Context, module: str, *arguments: str) -> str:
        nonlocal observed
        observed = (module, *arguments)
        return "Route S compression checkpoint check passed"

    monkeypatch.setattr(validate, "_module", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={},
    )

    assert "check passed" in validate._threshold_compression_admission(context)  # noqa: SLF001
    assert observed == ("devtools.admit_threshold_compression", "--check")
    step = next(
        step
        for step in validate.STEPS
        if step.name == "Route S compression admission checkpoint is consistent"
    )
    assert step.fast
    assert step.records
    assert not step.broad
