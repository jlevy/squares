"""Synthetic scalar identities and bounded fresh checks; no packing theorem control."""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import check_n17_global_contact_budget as tool


def document(*, stars: bool = True) -> dict[str, Any]:
    return {
        "schema": tool.DESCRIPTOR_SCHEMA,
        "constants": copy.deepcopy(tool.CONSTANTS),
        "include_star_packet": stars,
    }


def deadline() -> float:
    return time.monotonic() + 10


def test_exact_four_scalar_comparisons_and_scope() -> None:
    result = tool.generate(document(), deadline=deadline())
    assert all(row["holds"] for row in result["scalar_checks"].values())
    assert result["scalar_checks"]["disk_separation_squared"] == {
        "left": "15/16",
        "relation": ">",
        "right": "225/256",
        "holds": True,
    }
    assert result["scalar_checks"]["rank_count_subtraction"]["left"] == "19"
    assert result["hand_implications_not_independently_verified"]
    assert all(result[name] is False for name in tool.no_claims())


def test_exact_star_packet_and_optional_omission() -> None:
    stars = tool.star_packet()
    assert stars["identities"]["triple_angle_polynomial_at_three_quarters"]["left"] == "-1/16"
    assert stars["identities"]["five_angle_reduced_coefficient"]["left"] == "-1/4"
    assert stars["identities"]["five_angle_cosine_squared"]["left"] == "7/128"
    assert all(row["holds"] for group in stars.values() for row in group.values())
    assert (
        tool.generate(document(stars=False), deadline=deadline())["optional_star_arithmetic"]
        is None
    )


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("outer_U", "5"),
        ("wall_strip_width", "1/3"),
        ("tangential_separation", "1"),
        ("wall_capacity", 3),
        ("walls", 5),
        ("squares", 18),
        ("variables", 34),
    ],
)
def test_changed_scientific_constants_refused(key: str, value: Any) -> None:
    doc = document()
    doc["constants"][key] = value
    with pytest.raises(ValueError, match="frozen constants"):
        tool.generate(doc, deadline=deadline())


@pytest.mark.parametrize(
    ("args", "key"),
    [
        ((tool.Q(5), tool.Q(1, 4), tool.Q(15, 16), 4, 17), "five_wall_centres_span"),
        ((tool.Q(4), tool.Q(1, 2), tool.Q(15, 16), 4, 17), "disk_separation_squared"),
        ((tool.Q(1169, 250), tool.Q(1, 4), tool.Q(15, 16), 3, 17), "rank_count_subtraction"),
    ],
)
def test_wrong_inequality_and_capacity_controls(
    args: tuple[tool.Q, tool.Q, tool.Q, int, int], key: str
) -> None:
    assert tool.scalar_packet(*args)[key]["holds"] is False


@pytest.mark.parametrize(
    "value", ["1e999999999", "0.25", "\u0661", "+1", "01", "1/0", "2/4", "-0"]
)
def test_canonical_grammar_before_fraction(value: str, monkeypatch: pytest.MonkeyPatch) -> None:
    if value != "2/4":

        def refuse_fraction(_value: str) -> tool.Q:
            pytest.fail("invalid grammar reached Fraction")

        monkeypatch.setattr(tool, "Q", refuse_fraction)
    with pytest.raises(ValueError, match="rational"):
        tool.rational(value)


def test_used_rational_bit_ceiling_and_ascii_boundary() -> None:
    with pytest.raises(tool.IncompleteError, match="bit ceiling"):
        tool.rational(str(1 << 4096))
    assert tool.rational(str((1 << 4096) - 1)).numerator.bit_length() == 4096
    with pytest.raises(tool.IncompleteError, match="string ceiling"):
        tool.rational("9" * 2601)


@pytest.mark.parametrize("tamper", ["scalar", "star", "theorem", "extra"])
def test_fresh_full_payload_tamper_refused(tamper: str) -> None:
    doc = document()
    certificate = tool.generate(doc, deadline=deadline())
    if tamper == "scalar":
        certificate["scalar_checks"]["rank_count_subtraction"]["holds"] = False
    elif tamper == "star":
        certificate["optional_star_arithmetic"]["identities"]["five_angle_reduced_coefficient"][
            "left"
        ] = "1"
    elif tamper == "theorem":
        certificate["hand_global_theorem_verified"] = True
    else:
        certificate["invented_proof"] = True
    with pytest.raises(ValueError, match="fresh arithmetic payload"):
        tool.check(doc, certificate, deadline=deadline())


def test_expired_check_never_reports_scalar_acceptance() -> None:
    with pytest.raises(tool.IncompleteError, match="wall ceiling"):
        tool.generate(document(), deadline=time.monotonic() - 1)


@pytest.mark.parametrize("raw", ['{"x":1,"x":2}', '{"x":NaN}', '{"x":1.2}'])
def test_bounded_json_duplicate_and_float_refusal(tmp_path: Path, raw: str) -> None:
    path = tmp_path / "input.json"
    path.write_text(raw)
    with pytest.raises(ValueError, match="JSON"):
        tool.read_json(path, deadline())


def test_bounded_json_byte_refusal(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    path = tmp_path / "input.json"
    path.write_text("{} ")
    monkeypatch.setattr(tool, "BYTE_LIMIT", 2)
    with pytest.raises(tool.IncompleteError, match="JSON byte ceiling"):
        tool.read_json(path, deadline())


def test_two_clean_processes_reconstruct_and_preserve_no_claims(tmp_path: Path) -> None:
    descriptor, certificate, replay = (
        tmp_path / name for name in ("descriptor.json", "certificate.json", "replay.json")
    )
    descriptor.write_text(json.dumps(document()))
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(tool.__file__).resolve().parents[1])
    env.pop("PACKING_PROJECT_ROOT", None)
    command = [
        sys.executable,
        "-m",
        "devtools.check_n17_global_contact_budget",
        "--descriptor",
        str(descriptor),
    ]
    first = subprocess.run(
        [*command, "--output", str(certificate)],
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    second = subprocess.run(
        [*command, "--certificate", str(certificate), "--output", str(replay)],
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert first.returncode == second.returncode == 0, (first.stderr, second.stderr)
    left, right = (json.loads(path.read_text()) for path in (certificate, replay))
    assert left["process_id"] != right["process_id"]
    assert right["verification_passed"] is True
    assert tool.payload(left) == tool.payload(right)
    assert all(right[name] is False for name in tool.no_claims())
    again = subprocess.run(
        [*command, "--output", str(certificate)],
        env=env,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert again.returncode == 1
    assert "already exists" in again.stderr


def test_partial_failure_receipt_clears_proof_flags(tmp_path: Path) -> None:
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "output.json"
    descriptor.write_text("[]")
    assert tool.main(["--descriptor", str(descriptor), "--output", str(output)]) == 1
    result = json.loads(output.read_text())
    assert result["status"] == "refused"
    assert not result["arithmetic_packet_verified"]
    assert all(result[name] is False for name in tool.no_claims())


def test_changed_input_bytes_refused_before_acceptance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    descriptor, output = tmp_path / "descriptor.json", tmp_path / "output.json"
    descriptor.write_text(json.dumps(document()))
    original = tool.generate

    def mutate(doc: Any, *, deadline: float) -> dict[str, Any]:
        result = original(doc, deadline=deadline)
        descriptor.write_text(descriptor.read_text() + " ")
        return result

    monkeypatch.setattr(tool, "generate", mutate)
    assert tool.main(["--descriptor", str(descriptor), "--output", str(output)]) == 1
    assert json.loads(output.read_text())["error"] == "retained input bytes changed"


def test_saved_descriptor_byte_identity_tamper_refuses(tmp_path: Path) -> None:
    descriptor, certificate, replay = (
        tmp_path / name for name in ("descriptor.json", "certificate.json", "replay.json")
    )
    descriptor.write_text(json.dumps(document()))
    assert tool.main(["--descriptor", str(descriptor), "--output", str(certificate)]) == 0
    result = json.loads(certificate.read_text())
    result["descriptor_sha256"] = "0" * 64
    certificate.write_text(json.dumps(result))
    assert (
        tool.main(
            [
                "--descriptor",
                str(descriptor),
                "--certificate",
                str(certificate),
                "--output",
                str(replay),
            ]
        )
        == 1
    )
    refused = json.loads(replay.read_text())
    assert refused["status"] == "refused"
    assert refused["arithmetic_packet_verified"] is False
    assert refused["error"] == "certificate descriptor byte identity differs"
