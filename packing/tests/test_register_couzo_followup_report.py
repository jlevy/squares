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
    assert result["verification"] == "V0"
    assert result["confirmation"] == "C0"
    assert "confirmed" not in result["claim"] + result["next_rung"]
    assert result["scope"] == evidence["scope"] == source["scope"]
    assert request["register"] == [register.RESULT]
    assert request["source"].endswith("#issuecomment-6070798890")
    credit = register.bibliography_row()
    assert credit["lineage"] == "builds-on-project"
    assert credit["credit"] == "Couzo after Xu, Daniel, Ellsworth, Levy"


def test_plan_leaves_registered_rows_and_every_case_unchanged() -> None:
    """An existing row is never rewritten, so later review or adoption survives a re-run."""
    frontiers = register.REPO / "packing/frontier"
    cases = {p: p.read_bytes() for p in frontiers.glob("n-[0-9][0-9][0-9].md")}
    proposed = register.plan()
    evidence, result, source, _ = register.rows()
    expected = {
        "evidence.yaml": ("evidence", "id", evidence),
        "results.yaml": ("results", "id", result),
        "source-coverage.yaml": ("sources", "id", source),
        "bibliography.yaml": ("sources", "key", register.bibliography_row()),
    }
    for path, text in proposed:
        if path.name not in expected:
            continue
        field, identity, row = expected[path.name]
        old = safe_load(path.read_text())
        new = safe_load(text)
        if any(item[identity] == row[identity] for item in old[field]):
            assert new[field] == old[field], path
        else:
            assert new[field][:-1] == old[field], path
            assert new[field][-1] == row, path
    assert len(cases) == 324
    assert not {path for path, _ in proposed} & set(cases)
    assert all(path.read_bytes() == raw for path, raw in cases.items())


@pytest.mark.parametrize("n", register.reports.NUMBERS)
def test_each_side_is_below_its_frozen_ceiling(n: int) -> None:
    certificate = register.reports.read_facts()[n]
    prior = register.reports.prior_houses()[n]
    assert certificate.side < Fraction(prior["verified_exact"])
    assert certificate.side < Fraction(prior["selected_exact"])


def test_quoted_replay_figures_are_the_receipts() -> None:
    reports = register.reports
    cases = reports.kernel.read_xz(reports.receipt_path())["cases"]
    figures = (
        f"{sum(sum(row['cpu_seconds'].values()) for row in cases):.2f} route CPU seconds",
        f"{sum(row['wall_seconds'] for row in cases):.2f} ",
        f"{max(row['wall_seconds'] for row in cases):.2f} seconds",
    )
    pairs = sum(row[route]["pairs_tested"] for row in cases for route in reports.ROUTES)
    readme = " ".join((reports.PACKET / "README.md").read_text().split())
    assert f"{pairs} pair decisions" in register.REPLAY
    assert f"{pairs:,} pair decisions" in readme
    for figure in figures:
        assert figure in register.REPLAY
        assert figure in readme


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


def test_watch_edit_never_moves_a_later_read_back() -> None:
    later = WATCH.replace(
        "    read_through: ffd900dfff6d2674ad995359208c2f0714915c82\n"
        "    read_on: '2026-10-09'\n",
        "    read_through: " + "c" * 40 + "\n    read_on: '2026-10-12'\n",
    )
    assert later != WATCH
    assert register.watch_text(later) == later
    same_day = later.replace("'2026-10-12'", "'2026-10-09'")
    assert register.watch_text(same_day) == same_day


@pytest.mark.parametrize(
    ("read_through", "read_on"),
    [
        ("74f7e8b3f8df9cd5c2277b54d3cd7fe00769a998", "2026-10-09"),
        ("b10ad360f80ee82580e75330417e0171d1a9fb81", "2026-10-08"),
        ("c" * 40, "2026-10-08"),
    ],
)
def test_watch_edit_refuses_a_read_behind_the_parent(read_through: str, read_on: str) -> None:
    behind = WATCH.replace(
        "    read_through: ffd900dfff6d2674ad995359208c2f0714915c82\n"
        "    read_on: '2026-10-09'\n",
        f"    read_through: {read_through}\n    read_on: '{read_on}'\n",
    )
    assert behind != WATCH
    with pytest.raises(ValueError, match="behind the parent"):
        register.watch_text(behind)


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
