"""The results register's rungs are earned: the derivation and its refusals.

`epistemics.md` owns the vocabulary; `devtools/check_results.py` is its
executable form. These tests pin the derivation ladder on synthetic atoms, the
live register's health, and the refusal directions a control also exercises:
a rung claimed past its atoms, and an understatement with no composition note.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from devtools import check_results, render_results
from devtools.check_results import (
    derive_confirmation,
    derive_verification,
    repository_file_problem,
    verification_relation,
)
from sqpack.yamlio import safe_load

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
    read_only = {
        "external_review": {
            "state": "informally-verified",
            "date": "2026-08-31",
            "reviewed_by": "reviewer",
            "note": "Read the argument; did not rederive its case split.",
        },
        "origin": "external",
    }
    assert derive_confirmation([read_only]) == "C1"
    assert derive_confirmation([{**read_only, "origin": "independently-external"}]) == "C1"
    assert derive_confirmation([{**read_only, "origin": "replayed-here"}]) == "C0"
    assert (
        derive_confirmation(
            [{**read_only, "external_review": {"state": "informally-verified"}}]
        )
        == "C0"
    )
    replayed = {
        "origin": "replayed-here",
        "replay": "uv run replay",
        "replay_status": "passed",
        "method": "numerical-f64",
    }
    assert derive_confirmation([replayed]) == "C2"
    assert derive_confirmation([{**replayed, "replay": None}]) == "C0"
    assert derive_confirmation([dict(MACHINE_ENTRY)]) == "C3"
    # Two machine proofs of the same method are still C3: independence is
    # between mechanisms.
    assert derive_confirmation([dict(MACHINE_ENTRY), dict(MACHINE_ENTRY)]) == "C3"
    interval = dict(MACHINE_ENTRY, method="interval-certified")
    assert derive_confirmation([dict(MACHINE_ENTRY), interval]) == "C4"
    assert derive_confirmation([dict(MACHINE_ENTRY)], review_ready=True) == "C5"
    assert derive_confirmation([replayed], review_ready=True) == "C2"
    # The world's machine proof raises V, never C.
    external_machine = dict(MACHINE_ENTRY, origin="external")
    assert derive_confirmation([external_machine]) == "C0"


def test_verification_ladder_on_synthetic_atoms() -> None:
    assert derive_verification([]) == "V0"
    numeric = {"method": "numerical-f64", "precision": {"rounding": "nearest"}}
    assert derive_verification([numeric]) == "V1"
    published = {"method": "published-proof", "proof": {"theorem": "T"}}
    assert derive_verification([published]) == "V3"
    audited = {"method": "proof-audited", "proof": {"theorem": "T"}}
    assert derive_verification([audited]) == "V3"
    assert derive_verification([dict(MACHINE_ENTRY, origin="external")]) == "V4"
    assert derive_verification([{"method": "proof-assistant-checked"}]) == "V5"


def test_v2_bridges_only_an_unavailable_proof() -> None:
    assert verification_relation("V2", "V0") == "supported"
    assert verification_relation("V2", "V1") == "supported"
    assert verification_relation("V2", "V3") == "understated"
    assert verification_relation("V2", "V4") == "understated"


def test_result_paths_must_name_repository_files() -> None:
    assert repository_file_problem("epistemics.md") is None
    assert repository_file_problem("packing") == "does not name a file"
    assert repository_file_problem("/etc/passwd") == (
        "must be a normalized repository-relative path"
    )
    assert repository_file_problem("../outside") == (
        "must be a normalized repository-relative path"
    )


def test_a_reversed_scope_range_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    poisoned = _changed_result(tmp_path, "T-007", scope={"n_min": 100, "n_max": 4})
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-007: scope range is reversed: 100 > 4" in capsys.readouterr().out


def test_results_renderer_escapes_a_pipe_in_a_claim(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    register = _poisoned_register(
        tmp_path,
        "      Sixteen points make [0, 4426213/1000000]^2 unavoidable",
        "      Sixteen points | make [0, 4426213/1000000]^2 unavoidable",
    )
    monkeypatch.setattr(render_results, "RESULTS", register)
    row = next(
        line for line in render_results.render().splitlines() if line.startswith("| T-001 ")
    )
    assert r"Sixteen points \| make" in row
    assert len(re.findall(r"(?<!\\)\|", row)) == 8


def _poisoned_register(tmp_path: Path, old: str, new: str) -> Path:
    text = check_results.RESULTS.read_text(encoding="utf-8")
    assert text.count(old) == 1
    target = tmp_path / "results.yaml"
    target.write_text(text.replace(old, new), encoding="utf-8")
    return target


def _changed_result(tmp_path: Path, result_id: str, **changes: object) -> Path:
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    record = next(result for result in register["results"] if result["id"] == result_id)
    record.update(changes)
    target = tmp_path / "results.yaml"
    target.write_text(
        yaml.safe_dump(register, sort_keys=False, allow_unicode=True, width=96),
        encoding="utf-8",
    )
    return target


def test_c5_is_earned_by_a_mapped_review_artifact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    promoted = _changed_result(
        tmp_path,
        "T-004",
        confirmation="C5",
        review_artifact=(
            "docs/project/reviews/"
            "review-2026-08-31-overnight-run-verification-determinations.md"
        ),
    )
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 0


def test_c5_refuses_a_mapped_document_that_is_not_a_review(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    promoted = _changed_result(
        tmp_path,
        "T-004",
        confirmation="C5",
        review_artifact="epistemics.md",
    )
    monkeypatch.setattr(check_results, "RESULTS", promoted)
    assert check_results.main() == 1
    assert "not a non-superseded review" in capsys.readouterr().out


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


def test_v0_cannot_hide_machine_verification_behind_notes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    poisoned = _changed_result(
        tmp_path,
        "T-004",
        verification="V0",
        notes="Deliberately poisoned declaration for the regression.",
    )
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert "T-004: understates V4 as V0" in capsys.readouterr().out


@pytest.mark.parametrize(
    ("kind", "value"),
    [
        ("hypothesis", "H-999"),
        ("agenda_cell", "BC-999"),
        ("session", "session-999"),
        ("experiment", "exp-999"),
    ],
)
def test_a_dangling_produced_by_id_is_refused(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    kind: str,
    value: str,
) -> None:
    """The join from a result back to the campaign is a reference, so it can dangle.

    Before `produced_by` existed the join ran through prose -- a `by:` line, cell ids
    in `next_rung` -- and nothing could resolve it. A field that resolves to nothing
    would be the same prose with a colon in front of it.
    """
    poisoned = _changed_result(tmp_path, "T-017", produced_by={kind: value})
    monkeypatch.setattr(check_results, "RESULTS", poisoned)
    assert check_results.main() == 1
    assert f"T-017: produced_by.{kind} names {value}, which is not a recorded" in (
        capsys.readouterr().out
    )


def test_produced_by_resolves_every_kind_of_campaign_record(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    known = check_results.campaign_ids()
    assert {"H-060", "H-061"} <= known["hypothesis"]
    assert {"BC-150", "BC-152", "BC-161"} <= known["agenda_cell"]
    assert {"session-083", "session-085"} <= known["session"]
    assert {"exp-058", "exp-059"} <= known["experiment"]
    linked = _changed_result(
        tmp_path,
        "T-017",
        produced_by={
            "hypothesis": "H-061",
            "agenda_cell": "BC-161",
            "session": "session-085",
            "experiment": "exp-058",
        },
    )
    monkeypatch.setattr(check_results, "RESULTS", linked)
    assert check_results.main() == 0
