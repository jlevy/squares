"""The results register's rungs are earned: the derivation and its refusals.

`epistemics.md` owns the vocabulary; `devtools/check_results.py` is its
executable form. These tests pin the derivation ladder on synthetic atoms, the
live register's health, and the refusal directions a control also exercises:
a rung claimed past its atoms, and an understatement with no composition note.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import check_results
from devtools.check_results import derive_confirmation, derive_verification

MACHINE_ENTRY = {
    "method": "exact-algebraic",
    "certificate": "somewhere.py",
    "replay": "uv run --frozen python -m somewhere",
    "replay_status": "passed",
    "origin": "audited-here",
}


def test_the_live_register_is_healthy() -> None:
    assert check_results.main() == 0


def test_confirmation_ladder_on_synthetic_atoms() -> None:
    assert derive_confirmation([]) == "C0"
    read_only = {"external_review": {"state": "informally-verified"}, "origin": "external"}
    assert derive_confirmation([read_only]) == "C1"
    replayed = {"origin": "replayed-here", "replay_status": "passed", "method": "numerical-f64"}
    assert derive_confirmation([replayed]) == "C2"
    assert derive_confirmation([dict(MACHINE_ENTRY)]) == "C3"
    # Two machine proofs of the same method are still C3: independence is
    # between mechanisms.
    assert derive_confirmation([dict(MACHINE_ENTRY), dict(MACHINE_ENTRY)]) == "C3"
    interval = dict(MACHINE_ENTRY, method="interval-certified")
    assert derive_confirmation([dict(MACHINE_ENTRY), interval]) == "C4"
    # The world's machine proof raises V, never C.
    external_machine = dict(MACHINE_ENTRY, origin="external")
    assert derive_confirmation([external_machine]) == "C0"


def test_verification_ladder_on_synthetic_atoms() -> None:
    assert derive_verification([]) == "V0"
    numeric = {"method": "numerical-f64", "precision": {"rounding": "nearest"}}
    assert derive_verification([numeric]) == "V1"
    published = {"method": "published-proof", "proof": {"theorem": "T"}}
    assert derive_verification([published]) == "V3"
    assert derive_verification([dict(MACHINE_ENTRY, origin="external")]) == "V4"
    assert derive_verification([{"method": "proof-assistant-checked"}]) == "V5"


def _poisoned_register(tmp_path: Path, old: str, new: str) -> Path:
    text = check_results.RESULTS.read_text(encoding="utf-8")
    assert text.count(old) == 1
    target = tmp_path / "results.yaml"
    target.write_text(text.replace(old, new), encoding="utf-8")
    return target


def test_an_inflated_rung_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    poisoned = _poisoned_register(
        tmp_path,
        "    verification: V3\n    confirmation: C1\n    significance:\n"
        "      score: 3\n      rationale: >-\n        A published exact value",
        "    verification: V3\n    confirmation: C4\n    significance:\n"
        "      score: 3\n      rationale: >-\n        A published exact value",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-006: declares C4" in capsys.readouterr().out


def test_an_unexplained_understatement_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # T-004 sits at its derived C3; dropping it to C2 with no composition note
    # must fail in the sandbagging direction.
    poisoned = _poisoned_register(
        tmp_path,
        "    verification: V4\n    confirmation: C3\n    significance:\n"
        "      score: 3\n      rationale: >-\n"
        "        As far as the archived corpus shows, the first machine verification of",
        "    verification: V4\n    confirmation: C2\n    significance:\n"
        "      score: 3\n      rationale: >-\n"
        "        As far as the archived corpus shows, the first machine verification of",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-004: understates C3 as C2" in capsys.readouterr().out
