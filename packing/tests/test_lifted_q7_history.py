"""Historical Q(sqrt7) geometry remains distinct from current exact ry-xu houses."""

from __future__ import annotations

import copy
from pathlib import Path

import pytest

from cases.lifted_q7 import packing
from devtools import register_ryxu_reports as register
from sqpack.witness import WitnessError, load_witness, witness_document
from sqpack.yamlio import safe_load


def test_complete_original86_and_live18_reader_preserve_their_full_inputs(
    tmp_path: Path,
) -> None:
    original = next(row for row in register.read_history() if row["n"] == 86)
    path = tmp_path / "original-86.yaml"
    path.write_text(original["house"])
    expected = load_witness(path, fallback_schema=packing.WITNESS_SCHEMA)
    current = packing.WITNESSES / "n-086.yaml"
    current_bytes = current.read_bytes()
    assert packing.source_witness(86) == expected
    assert len(expected["squares"]) == 86
    assert expected["representation"] == "center-angle"
    assert load_witness(current, fallback_schema=packing.WITNESS_SCHEMA) != expected
    assert current.read_bytes() == current_bytes
    assert packing.source_witness(18) == load_witness(
        packing.WITNESSES / "n-018.yaml", fallback_schema=packing.WITNESS_SCHEMA
    )


@pytest.mark.parametrize("mutation", ["missing-pose", "wrong-source", "wrong-count"])
def test_historical_reader_refuses_incomplete_or_misattributed_full_document(
    mutation: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    rows = copy.deepcopy(register.read_history())
    row = next(row for row in rows if row["n"] == 86)
    witness = safe_load(row["house"])["witness"]
    if mutation == "missing-pose":
        witness["squares"].pop()
    elif mutation == "wrong-source":
        witness["source"]["key"] = "A different construction"
    else:
        witness["n"] = 85
    row["house"] = witness_document(witness)
    monkeypatch.setattr(register, "read_history", lambda: rows)
    with pytest.raises((ValueError, WitnessError)):
        packing.source_witness(86)
