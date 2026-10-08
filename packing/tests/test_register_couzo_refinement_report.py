"""Source-only #451 registration preserves current selection and complete evidence."""

from __future__ import annotations

from pathlib import Path

import pytest

from devtools import register_couzo_refinement_report as register
from sqpack.yamlio import safe_load


def test_complete_source_only_plan_is_schema_valid_and_preserves_current_cases() -> None:
    frontiers = register.REPO / "packing/frontier"
    cases = {p: p.read_bytes() for p in frontiers.glob("n-[0-9][0-9][0-9].md")}
    deciding = {
        p: p.read_bytes()
        for p in (register.reports.fact_path(), register.reports.receipt_path())
    }
    proposed = register.plan()
    assert len(proposed) == 6
    evidence, result, source, request = register.rows()
    expected = {
        "evidence.yaml": ("evidence", evidence),
        "results.yaml": ("results", result),
        "source-coverage.yaml": ("sources", source),
        "result-requests.yaml": ("issues", request),
    }
    for path, text in proposed:
        if path.name not in expected:
            continue
        field, row = expected[path.name]
        old = safe_load(path.read_text())
        new = safe_load(text)
        identity = "number" if field == "issues" else "id"
        if any(item[identity] == row[identity] for item in old[field]):
            assert new[field] == old[field]
        else:
            assert new[field][:-1] == old[field]
            assert new[field][-1] == row
        assert {key: value for key, value in new.items() if key != field} == {
            key: value for key, value in old.items() if key != field
        }
    assert len(cases) == 324
    assert all(path.read_bytes() == raw for path, raw in {**cases, **deciding}.items())
    assert result["verification"] == "V0"
    assert result["confirmation"] == "C0"
    assert "overlaps that source checker" in result["notes"]
    assert "second maintained rational-geometry" in result["notes"]
    assert "claims_record" not in source


def test_late_registry_contract_failure_writes_nothing(monkeypatch: pytest.MonkeyPatch) -> None:
    checked = []
    written = []
    real = register.validate

    def late(path: Path, text: str) -> None:
        checked.append(path.name)
        if path.name == "bibliography.yaml":
            raise ValueError("late registry contract")
        real(path, text)

    monkeypatch.setattr(register, "validate", late)
    monkeypatch.setattr(register, "save", lambda path, text: written.append((path, text)))
    with pytest.raises(ValueError, match="late registry contract"):
        register.register()
    assert checked == [
        "evidence.yaml",
        "results.yaml",
        "source-coverage.yaml",
        "result-requests.yaml",
        "bibliography.yaml",
    ]
    assert written == []


@pytest.mark.parametrize("indent", ["", "  "])
def test_registration_preserves_prior_layout_comments_and_repeated_confirmed_row(
    indent: str,
) -> None:
    before = (
        f"sources:\n{indent}- id: old\n{indent}  scope: {{n_values: [1]}}\n"
        "# separator\nother: retained\n"
    )
    row = {"id": "new", "scope": {"n_values": [105]}, "extra": "retained"}
    after = register.append(before, "sources", row, "id")
    assert after.startswith(before.split("# separator", maxsplit=1)[0])
    assert after.endswith("# separator\nother: retained\n")
    assert (
        register.append(after, "sources", {**row, "extra": "fresh reported candidate"}, "id")
        == after
    )
    with pytest.raises(ValueError, match="scope differs"):
        register.append(after, "sources", {**row, "scope": {"n_values": [108]}}, "id")
