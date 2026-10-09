"""Source-only registration of Couzo's 2d32a6e five preserves selection and history."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest

from devtools import register_couzo_followup_report as register
from sqpack.yamlio import safe_load

REQUESTS = """# header comment
softschema:
  status: enforced
repository: jlevy/squares
issues:
  - number: 451
    title: example
    results:
    - key: eight-rational-refinements
      claim: earlier claim
      source: body
      register:
      - T-128
    asks:
    - what: credit
      state: done
    beads:
    - think-edo8
    answer_bead: think-edo8
    replies: []
  - number: 425
    title: other
    results:
    - key: other
      claim: other claim
      source: body
      register:
      - T-117
    beads:
    - think-f3dl
    replies: []
"""

WATCH = """# header
repositories:
  - url: https://github.com/example/before
    read_through: aaaa
    read_on: '2026-10-08'
    note: >-
      Before.

  - url: https://github.com/franciscouzo/square-packing
    read_through: ffd900dfff6d2674ad995359208c2f0714915c82
    read_on: '2026-10-09'
    bead: think-1545
    note: >-
      Older note.

  - url: https://github.com/example/after
    read_through: bbbb
    read_on: '2026-10-08'
    note: >-
      After.
"""


def test_registered_record_is_complete_and_the_plan_is_idempotent() -> None:
    proposed = register.plan()
    assert [path.name for path, _ in proposed] == [
        "evidence.yaml",
        "results.yaml",
        "source-coverage.yaml",
        "bibliography.yaml",
        "result-requests.yaml",
        "intake-watch.yaml",
        "README.md",
    ]
    for path, text in proposed:
        assert path.read_text() == text, path
    evidence, result, source, request = register.rows()
    results = safe_load((register.REPO / "packing/frontier/results.yaml").read_text())
    assert [row for row in results["results"] if row["id"] == register.RESULT] == [result]
    assert result["verification"] == "V0"
    assert result["confirmation"] == "C0"
    assert "confirmed" not in result["claim"] + result["next_rung"]
    assert result["scope"] == evidence["scope"] == source["scope"]
    assert request["register"] == [register.RESULT]
    assert request["source"].endswith("#issuecomment-6070798890")
    credit = register.bibliography_row()
    assert credit["lineage"] == "builds-on-project"
    assert credit["credit"] == "Couzo after Xu, Daniel, Ellsworth, Levy"


@pytest.mark.parametrize(
    ("n", "source_key"),
    [
        (84, "[ry-xu square packing 2026]"),
        (86, "[ry-xu square packing 2026]"),
        (105, "[ry-xu square packing 2026]"),
        (175, "[ry-xu square packing 2026]"),
        (270, "[Daniel new arrangements 2026-10-07]"),
    ],
)
def test_selected_cases_keep_their_current_sources(n: int, source_key: str) -> None:
    packing = register.reports.legacy.case_record(n)
    assert packing["reported_upper_bound"]["source_key"] == source_key
    certificate = register.reports.read_facts()[n]
    assert certificate.side < Fraction(packing["verified_upper_bound"]["exact_form"])


def test_request_edit_adds_one_result_and_the_import_bead_only() -> None:
    _, _, _, request = register.rows()
    updated = register.request_text(REQUESTS, request)
    assert updated.startswith("# header comment\n")
    before, after = safe_load(REQUESTS), safe_load(updated)
    entry = after["issues"][0]
    assert entry["results"] == [*before["issues"][0]["results"], request]
    assert entry["beads"] == ["think-edo8", register.BEAD]
    assert entry["asks"] == before["issues"][0]["asks"]
    assert after["issues"][1] == before["issues"][1]
    assert register.request_text(updated, request) == updated


def test_watch_edit_moves_only_the_franciscouzo_read() -> None:
    updated = register.watch_text(WATCH)
    before, after = safe_load(WATCH), safe_load(updated)
    assert after["repositories"][0] == before["repositories"][0]
    assert after["repositories"][2] == before["repositories"][2]
    read = after["repositories"][1]
    assert read["read_through"] == register.reports.REVISION
    assert read["bead"] == "think-1545"
    assert "think-1545" in read["note"]
    assert "Earlier reads" in read["note"]
    assert register.watch_text(updated) == updated


def test_review_date_never_moves_backwards() -> None:
    assert register.reviewed_text("last_reviewed: '2026-10-08'\n") == (
        "last_reviewed: '2026-10-09'\n"
    )
    assert register.reviewed_text("last_reviewed: '2026-10-10'\n") == (
        "last_reviewed: '2026-10-10'\n"
    )
    with pytest.raises(ValueError, match="review date"):
        register.reviewed_text("results: []\n")


def test_late_registry_contract_failure_writes_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    checked: list[str] = []
    written: list[Path] = []
    real = register.validate

    def late(path: Path, text: str) -> None:
        checked.append(path.name)
        if path.name == "intake-watch.yaml":
            raise ValueError("late registry contract")
        real(path, text)

    monkeypatch.setattr(register, "validate", late)
    monkeypatch.setattr(register, "save", lambda path, _text: written.append(path))
    with pytest.raises(ValueError, match="late registry contract"):
        register.register()
    assert checked == [
        "evidence.yaml",
        "results.yaml",
        "source-coverage.yaml",
        "bibliography.yaml",
        "result-requests.yaml",
        "intake-watch.yaml",
    ]
    assert written == []
