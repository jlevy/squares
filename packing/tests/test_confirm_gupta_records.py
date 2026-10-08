"""Finite confirmation proposal with private complete inputs and atomic preflight.

Fixtures copy scientific inputs and metadata only, never a whole native worker.
The separately measured production snapshot is tested at its unchanged cap boundary;
no geometric decider may execute during receipt admission or record composition.
"""

from __future__ import annotations

import copy
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from jsonschema_rs import Draft202012Validator

from devtools import confirm_gupta_records as confirmation
from devtools import gupta_house_links as houses
from devtools import register_gupta_reports as register
from devtools import register_refinement_reports as registry
from sqpack.yamlio import safe_load

SOURCE = register.REPO
PACKET = houses.reports.PACKET
FRONTIER = register.FRONTIER
REGISTRIES = ("verifiers", "evidence", "results", "source-coverage")


def case(text: str) -> dict[str, Any]:
    return safe_load(text.split("---\n", 2)[1])["packing"]


@pytest.fixture
def private_proposal(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo = tmp_path / "metadata-and-scientific-inputs"
    inputs = (
        *houses.private_input_paths(),
        *(FRONTIER / f"{name}.yaml" for name in REGISTRIES),
        *FRONTIER.glob("n-*.md"),
        *(houses.house_path(n) for n in houses.NUMBERS),
        SOURCE / register.REVIEW,
        *FRONTIER.glob("*.schema.yaml"),
    )
    for original in inputs:
        path = repo / original.relative_to(SOURCE)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(original.read_bytes())
    packet = repo / PACKET.relative_to(SOURCE)
    history = repo / register.HISTORY.relative_to(SOURCE)
    monkeypatch.setattr(houses.reports, "REPO", repo)
    monkeypatch.setattr(houses.reports, "PACKET", packet)
    monkeypatch.setattr(houses, "REPO", repo)
    monkeypatch.setattr(houses, "HISTORY", history)
    monkeypatch.setattr(register, "REPO", repo)
    monkeypatch.setattr(register, "FRONTIER", repo / "packing/frontier")
    monkeypatch.setattr(register, "HISTORY", history)
    monkeypatch.setattr(registry.packets, "REPO", repo)
    # Construct the reported stage explicitly even after the live record is
    # confirmed. Its old verified ceiling comes from validated immutable history;
    # every deciding input and complete current source house remains untouched.
    history_rows = {row["n"]: row for row in register.read_history()}
    for n in houses.NUMBERS:
        path = register.FRONTIER / f"n-{n:03d}.md"
        text = path.read_text()
        document = safe_load(text.split("---\n", 2)[1])
        current = document["packing"]
        previous = case(history_rows[n]["frontier"])
        current["verified_upper_bound"] = copy.deepcopy(previous["verified_upper_bound"])
        current["evidence"] = [
            item for item in current["evidence"] if item != confirmation.EXACT
        ]
        current["blockers"] = register.pending_blockers(current)
        body = re.sub(
            rf"\n{register.SECTION}\n.*?(?=\n## |\n<!-- This document follows)",
            lambda _match, n=n: register.section(n, confirmed=False),
            text.split("---\n", 2)[2],
            flags=re.DOTALL,
        )
        body = register.ceiling_prose(n, current, body)
        path.write_text("---\n" + register.dump(document) + "---\n" + body)
    for name, identifier in (
        ("evidence", confirmation.EXACT),
        ("verifiers", confirmation.CUSTODY),
    ):
        path = register.FRONTIER / f"{name}.yaml"
        document = safe_load(path.read_text())
        document[name] = [row for row in document[name] if row["id"] != identifier]
        path.write_text(register.dump(document))
    path = register.FRONTIER / "results.yaml"
    document = safe_load(path.read_text())
    result = next(row for row in document["results"] if row["id"] == register.RESULT)
    result["verification"], result["confirmation"] = "V0", "C0"
    result["evidence"] = [item for item in result["evidence"] if item != confirmation.EXACT]
    path.write_text(register.dump(document))
    path = register.FRONTIER / "source-coverage.yaml"
    document = safe_load(path.read_text())
    source = next(row for row in document["sources"] if row["id"] == register.SOURCE_ID)
    source["evidence"] = [item for item in source["evidence"] if item != confirmation.EXACT]
    path.write_text(register.dump(document))
    # No production clone/count claim: actual custody and footprint have separate
    # retained reviews. Exercise the same unchanged cap comparison in this fixture.
    monkeypatch.setattr(
        confirmation.controls,
        "snapshot_source_bytes",
        lambda: confirmation.controls.SNAPSHOT_MAX_BYTES,
    )

    def forbidden(*_args, **_kwargs):
        pytest.fail("confirmation admission invoked a geometric decider")

    monkeypatch.setattr(houses.reports.kernel, "run_case", forbidden)
    monkeypatch.setattr(houses.reports, "run_child", forbidden)
    monkeypatch.setattr(houses.reports.legacy, "exact_verify", forbidden)
    monkeypatch.setattr(houses.reports.legacy.independent, "check_squares", forbidden)
    return repo


def snapshot(repo: Path) -> dict[str, bytes]:
    return {
        p.relative_to(repo).as_posix(): p.read_bytes() for p in repo.rglob("*") if p.is_file()
    }


@pytest.mark.parametrize("boundary", ["native-review", "custody-review", "capacity"])
def test_unclosed_prerequisite_refuses_before_any_record_write(
    private_proposal: Path, monkeypatch: pytest.MonkeyPatch, boundary: str
) -> None:
    if boundary == "capacity":
        monkeypatch.setattr(
            confirmation.controls,
            "snapshot_source_bytes",
            lambda: confirmation.controls.SNAPSHOT_MAX_BYTES + 1,
        )
    else:
        path = private_proposal / register.REVIEW
        marker = "**G1, closed:" if boundary == "native-review" else "**G2, closed:"
        path.write_text(path.read_text().replace(marker, "**Prerequisite still open:"))
    before = snapshot(private_proposal)
    with pytest.raises(ValueError, match=r"mapped native|unchanged private snapshot cap"):
        confirmation.confirm()
    assert snapshot(private_proposal) == before


@pytest.mark.parametrize(
    "boundary",
    ["reported-lane", "verified-lane", "result-scope", "coverage-schema", "case-evidence"],
)
def test_late_case_or_registry_refuses_the_entire_write_plan(
    private_proposal: Path, boundary: str
) -> None:
    if boundary == "result-scope":
        path = register.FRONTIER / "results.yaml"
        document = safe_load(path.read_text())
        result = next(r for r in document["results"] if r["id"] == register.RESULT)
        result["scope"]["n_values"].pop()
        path.write_text(register.dump(document))
    elif boundary == "coverage-schema":
        path = register.FRONTIER / "source-coverage.yaml"
        document = safe_load(path.read_text())
        document["selected_overrides"][0].pop("reason")
        path.write_text(register.dump(document))
    else:
        path = register.FRONTIER / "n-239.md"
        text = path.read_text()
        document = safe_load(text.split("---\n", 2)[1])
        lane = "reported_upper_bound" if boundary == "reported-lane" else "verified_upper_bound"
        if boundary == "case-evidence":
            document["packing"]["evidence"].append("E-made-up")
        else:
            document["packing"][lane]["exact_form"] = "1"
        path.write_text("---\n" + register.dump(document) + "---\n" + text.split("---\n", 2)[2])
    before = snapshot(private_proposal)
    with pytest.raises(
        ValueError,
        match=(
            r"selected.*upper lane|seventeen-case result scope|"
            r"schema contract|case semantics"
        ),
    ):
        confirmation.confirm()
    assert snapshot(private_proposal) == before


@pytest.mark.parametrize("boundary", ["native-result", "original-comparator"])
def test_changed_complete_deciding_input_refuses_then_restores_positive_admission(
    private_proposal: Path, boundary: str
) -> None:
    path = (
        houses.reports.receipt_path()
        if boundary == "native-result"
        else houses.reports.fact_path()
    )
    raw = path.read_bytes()
    value = houses.reports.kernel.read_xz(path)
    if boundary == "native-result":
        value["cases"][-3]["exact_verify"]["verification_passed"] = False
    else:
        value["cases"][-1]["source_comparator"] += " "
    houses.reports.save_xz(path, value)
    before = snapshot(private_proposal)
    with pytest.raises(ValueError, match=r"native exact route result|acquired source"):
        confirmation.confirm()
    assert snapshot(private_proposal) == before
    path.write_bytes(raw)
    assert tuple(confirmation.admit_confirmation()) == houses.reports.NUMBERS
    assert path.read_bytes() == raw


@pytest.mark.slow
def test_complete_proposal_preserves_all_lower_history_withdrawals_and_unowned_rows(
    private_proposal: Path,
) -> None:
    before = snapshot(private_proposal)
    old_cases = {
        n: case((register.FRONTIER / f"n-{n:03d}.md").read_text()) for n in houses.NUMBERS
    }
    old_records = {
        name: safe_load((register.FRONTIER / f"{name}.yaml").read_text()) for name in REGISTRIES
    }
    facts = houses.reports.read_facts()
    confirmation.confirm()
    after = snapshot(private_proposal)
    allowed = {f"packing/frontier/n-{n:03d}.md" for n in houses.NUMBERS} | {
        f"packing/frontier/{name}.yaml" for name in REGISTRIES
    }
    assert {path for path in before if before[path] != after[path]} == allowed
    for n, previous in old_cases.items():
        text = (register.FRONTIER / f"n-{n:03d}.md").read_text()
        current = case(text)
        expected = copy.deepcopy(previous)
        expected["verified_upper_bound"] = {
            "value": houses.reports.legacy.ceiling_decimal(facts[n].side, 16),
            "exact_form": str(facts[n].side),
            "evidence": [confirmation.EXACT],
        }
        expected["evidence"].append(confirmation.EXACT)
        expected["blockers"] = [
            b for b in previous["blockers"] if b["evidence"] != [register.REPORT]
        ]
        assert current == expected
        assert Fraction(current["reported_upper_bound"]["exact_form"]) == facts[n].side
        assert "V3/C3 using independently" in text
        assert "## The verified upper bound is a ceiling" not in text
        assert (
            "actual private-worker admission and confirming record review remain pending."
            not in " ".join(text.split())
        )
        assert register.pending_blockers(current) == current["blockers"]
    # Only the explicit 14-case/4-registry roster changes. The other 310 records,
    # three withdrawals, complete houses and four deciding inputs stay exact.
    for name, original in old_records.items():
        path = register.FRONTIER / f"{name}.yaml"
        document = safe_load(path.read_text())
        schema_path = SOURCE / "packing/frontier" / document["softschema"]["schema"]
        validated = copy.deepcopy(document)
        validated.pop("softschema")
        assert Draft202012Validator(safe_load(schema_path.read_text())).is_valid(validated), (
            name
        )
        field = "sources" if name == "source-coverage" else name
        owned = {
            "results": register.RESULT,
            "evidence": confirmation.EXACT,
            "verifiers": confirmation.CUSTODY,
            "source-coverage": register.SOURCE_ID,
        }[name]
        assert [r for r in document[field] if r["id"] != owned] == [
            r for r in original[field] if r["id"] != owned
        ]
        if name == "source-coverage":
            for key in original.keys() - {"sources"}:
                assert document[key] == original[key]
    result = next(
        r
        for r in safe_load((register.FRONTIER / "results.yaml").read_text())["results"]
        if r["id"] == register.RESULT
    )
    assert (result["verification"], result["confirmation"]) == ("V3", "C3")
    assert result["scope"] == {"n_values": list(houses.reports.NUMBERS)}
    assert register.REPORT in result["evidence"]
    assert confirmation.EXACT in result["evidence"]
    assert "human" in result["next_rung"]
    assert "optimum" in result["claim"]
    assert confirmation.custody_verifier()["role"] == "premises"
    evidence = confirmation.confirming_evidence()
    assert evidence["independence_record"] == register.REVIEW
    assert evidence["relationship_to_generator"] == "independent-implementation"
    assert "share" in evidence["limitations"]
    assert "SAT" in evidence["limitations"]
    assert "forbids geometric deciders" in evidence["limitations"]
    assert len(evidence["scope"]["n_values"]) == 17
    confirmation.confirm()
    assert snapshot(private_proposal) == after
    register.record_cases()
    assert snapshot(private_proposal) == after


@pytest.mark.parametrize("indent", ["", "  "])
def test_owned_row_replacement_preserves_layout_adjacent_fields_and_extra_artifacts(
    indent: str,
) -> None:
    text = (
        f"entries:\n{indent}- id: first\n{indent}  value: original\n"
        f"{indent}- id: owned\n{indent}  artifacts: [kept]\n"
        "# next section\nnext: unchanged\n"
    )
    row = {"id": "owned", "artifacts": ["kept", "new"]}
    updated = confirmation.update_row(text, "entries", row)
    assert safe_load(updated)["entries"] == [{"id": "first", "value": "original"}, row]
    assert updated.startswith(f"entries:\n{indent}- id: first\n{indent}  value: original\n")
    assert updated.endswith("# next section\nnext: unchanged\n")
    assert confirmation.update_row(updated, "entries", row) == updated


@pytest.mark.slow
def test_interrupted_atomic_write_resumes_from_the_unchanged_complete_history(
    private_proposal: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = snapshot(private_proposal)
    actual_save = confirmation.save

    def interrupt(path: Path, text: str) -> None:
        if path.name == "n-130.md":
            raise OSError("second frontier atomic write interrupted")
        actual_save(path, text)

    monkeypatch.setattr(confirmation, "save", interrupt)
    with pytest.raises(OSError, match="second frontier atomic write"):
        confirmation.confirm()
    partial = snapshot(private_proposal)
    assert partial["packing/frontier/n-088.md"] != original["packing/frontier/n-088.md"]
    assert partial["packing/frontier/n-130.md"] == original["packing/frontier/n-130.md"]
    retained = register.HISTORY.relative_to(private_proposal).as_posix()
    assert partial[retained] == original[retained]
    monkeypatch.setattr(confirmation, "save", actual_save)
    confirmation.confirm()
    completed = snapshot(private_proposal)
    confirmation.confirm()
    assert snapshot(private_proposal) == completed
    assert completed[retained] == original[retained]
