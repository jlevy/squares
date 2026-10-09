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
    bibliography = next(text for path, text in proposed if path.name == "bibliography.yaml")
    credit = next(
        row
        for row in safe_load(bibliography)["sources"]
        if row["key"] == register.reports.SOURCE_KEY
    )
    assert credit["lineage"] == "builds-on-project"
    assert credit["credit"] == "Couzo after Xu, Chaoweeraprasit, Gupta, Ellsworth, Daniel, Levy"
    assert "Squares Project (Levy) verification code" in credit["note"]
    assert len(cases) == 324
    assert all(path.read_bytes() == raw for path, raw in {**cases, **deciding}.items())
    assert result["verification"] == "V0"
    assert result["confirmation"] == "C0"
    assert "overlaps that source checker" in result["notes"]
    assert "second maintained rational-geometry" in result["notes"]
    assert "claims_record" not in source


def test_missing_bibliography_row_inherits_full_credit_and_project_lineage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    bibliography = register.REPO / "packing/resources/bibliography.yaml"
    original_bytes = bibliography.read_bytes()
    original = safe_load(bibliography.read_text())
    retained = {
        **original,
        "sources": [
            row for row in original["sources"] if row["key"] != register.reports.SOURCE_KEY
        ],
    }
    assert len(retained["sources"]) == len(original["sources"]) - 1
    real_read = Path.read_text

    def read(path: Path, *args, **kwargs) -> str:
        if path == bibliography:
            return register.dump(retained)
        return real_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", read)
    proposed = register.plan()
    inserted = safe_load(next(text for path, text in proposed if path == bibliography))
    assert inserted["sources"][:-1] == retained["sources"]
    credit = inserted["sources"][-1]
    assert credit["key"] == register.reports.SOURCE_KEY
    assert credit["credit"] == "Couzo after Xu, Chaoweeraprasit, Gupta, Ellsworth, Daniel, Levy"
    assert credit["short_credit"] == "Couzo after Xu et al."
    assert credit["lineage"] == "builds-on-project"
    assert "Squares Project (Levy) verification code" in credit["note"]
    assert "this project lineage is not independent" in credit["note"]
    assert {key: value for key, value in inserted.items() if key != "sources"} == {
        key: value for key, value in retained.items() if key != "sources"
    }
    assert bibliography.read_bytes() == original_bytes


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
