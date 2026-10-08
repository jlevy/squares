"""Complete preflight and history-first interrupted Gupta adoption."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
from jsonschema_rs import Draft202012Validator

from devtools import build_bound_citations as citations
from devtools import build_known_best_atlas as atlas
from devtools import check_results
from devtools import check_source_coverage as coverage_check
from devtools import gupta_house_links as houses
from devtools import register_gupta_reports as register
from devtools import register_refinement_reports as registry
from devtools import run_negative_controls as controls
from devtools import ryxu_house_links as ryxu
from sqpack.yamlio import safe_load

SOURCE = houses.REPO


@pytest.fixture(scope="module")
def original_source() -> dict[int, dict[str, Any]]:
    """Complete source state preceding adoption, rather than later current-case text."""
    if register.HISTORY.exists():
        return {row["n"]: row for row in register.read_history()}
    return {
        n: {
            "n": n,
            "frontier": (SOURCE / "packing/frontier" / f"n-{n:03d}.md").read_text(),
            "house": houses.house_path(n).read_text(),
        }
        for n in houses.NUMBERS
    }


@pytest.fixture
def original_pair(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, original_source: dict[int, dict[str, Any]]
) -> dict[int, str]:
    repo = tmp_path / "private"
    packet = repo / houses.reports.PACKET.relative_to(SOURCE)
    original_packet = houses.reports.PACKET
    for relative in (
        "acquisition/case-inputs.json",
        "facts/complete-certificates-and-comparators.json.xz",
        "receipts/exact-certification.json.xz",
    ):
        path = packet / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((original_packet / relative).read_bytes())
    monkeypatch.setattr(houses.reports, "REPO", repo)
    monkeypatch.setattr(houses.reports, "PACKET", packet)
    monkeypatch.setattr(houses, "REPO", repo)
    monkeypatch.setattr(houses, "NUMBERS", (88, 130))
    monkeypatch.setattr(register, "REPO", repo)
    monkeypatch.setattr(register, "FRONTIER", repo / "packing/frontier")
    monkeypatch.setattr(
        register, "HISTORY", packet / "acquisition/frontier-prior-state.json.xz"
    )
    register.FRONTIER.mkdir(parents=True)
    for name in ("bibliography.yaml", "README.md"):
        metadata = repo / "packing/resources" / name
        metadata.parent.mkdir(parents=True, exist_ok=True)
        metadata.write_bytes((SOURCE / "packing/resources" / name).read_bytes())
    originals = {}
    for n in houses.NUMBERS:
        original = SOURCE / "packing/frontier" / f"n-{n:03d}.md"
        originals[n] = original_source[n]["frontier"]
        (register.FRONTIER / original.name).write_text(originals[n])
        house = houses.house_path(n)
        house.parent.mkdir(parents=True, exist_ok=True)
        house.write_text(original_source[n]["house"])
    return originals


def frontier_bytes() -> dict[int, bytes]:
    return {n: (register.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in houses.NUMBERS}


def test_all_fourteen_previous_exact_lanes_are_strictly_improved(
    original_source: dict[int, dict[str, Any]],
) -> None:
    facts = houses.reports.read_facts()
    for n in houses.NUMBERS:
        document = safe_load(original_source[n]["frontier"].split("---\n", 2)[1])["packing"]
        for lane in ("reported_upper_bound", "verified_upper_bound"):
            assert facts[n].side < Fraction(document[lane]["exact_form"])
        assert document["conjectured_optimum"] is None
    assert len(houses.NUMBERS) == 14


def test_late_nonimprovement_refuses_before_history_or_frontier_write(
    original_pair: dict[int, str],
) -> None:
    path = register.FRONTIER / "n-130.md"
    document = safe_load(original_pair[130].split("---\n", 2)[1])
    document["packing"]["verified_upper_bound"]["exact_form"] = "1"
    path.write_text(
        "---\n" + register.dump(document) + "---\n" + original_pair[130].split("---\n", 2)[2]
    )
    before = frontier_bytes()
    with pytest.raises(ValueError, match="not smaller than both lanes"):
        register.record_cases()
    assert frontier_bytes() == before
    assert not register.HISTORY.exists()


def test_complete_history_precedes_first_write_and_survives_interrupted_retry(
    original_pair: dict[int, str], monkeypatch: pytest.MonkeyPatch
) -> None:
    house_bytes = {n: houses.house_path(n).read_text() for n in houses.NUMBERS}

    def interrupt(path: Path, text: str) -> None:
        retained = register.read_history()
        assert {row["n"]: row["frontier"] for row in retained} == original_pair
        assert {row["n"]: row["house"] for row in retained} == house_bytes
        if path.name == "n-130.md":
            raise OSError("interrupted second atomic write")
        path.write_text(text)

    monkeypatch.setattr(register, "save", interrupt)
    with pytest.raises(OSError, match="interrupted second"):
        register.record_cases()
    original_boundary = register.HISTORY.read_bytes()
    assert (register.FRONTIER / "n-130.md").read_text() == original_pair[130]
    monkeypatch.setattr(register, "save", lambda path, text: path.write_text(text))
    register.record_cases()
    for n in houses.NUMBERS:
        before = safe_load(original_pair[n].split("---\n", 2)[1])["packing"]
        after = safe_load(
            (register.FRONTIER / f"n-{n:03d}.md").read_text().split("---\n", 2)[1]
        )["packing"]
        assert after["reported_upper_bound"] == register.reported_bound(n)
        for field in (
            "reported_lower_bound",
            "verified_lower_bound",
            "verified_upper_bound",
            "reported_status",
            "status",
        ):
            assert after[field] == before[field]
        assert after["blockers"] == register.pending_blockers(before)
        assert after["rigidity"] is None
    adopted = frontier_bytes()
    register.record_cases()
    assert frontier_bytes() == adopted
    assert register.HISTORY.read_bytes() == original_boundary


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "adopted-original"])
def test_existing_history_cannot_be_replaced_by_a_subset_or_adopted_original(
    original_pair: dict[int, str], mutation: str
) -> None:
    rows: list[dict[str, Any]] = [
        {"n": n, "frontier": text, "house": houses.house_path(n).read_text()}
        for n, text in original_pair.items()
    ]
    if mutation == "missing":
        rows.pop()
    elif mutation == "duplicate":
        rows[-1] = copy.deepcopy(rows[0])
    else:
        document = safe_load(rows[-1]["frontier"].split("---\n", 2)[1])
        document["packing"]["reported_upper_bound"] = register.reported_bound(rows[-1]["n"])
        rows[-1]["frontier"] = (
            "---\n"
            + register.dump(document)
            + "---\n"
            + original_pair[130].split("---\n", 2)[2]
        )
    houses.reports.save_xz(register.HISTORY, {"format": register.HISTORY_FORMAT, "cases": rows})
    before = frontier_bytes()
    boundary = register.HISTORY.read_bytes()
    with pytest.raises(ValueError, match=r"complete immutable|original pre-adoption"):
        register.record_cases()
    assert frontier_bytes() == before
    assert register.HISTORY.read_bytes() == boundary


def test_gupta_plan_binds_full_native_house_and_original_source_without_deciders(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args, **_kwargs):
        pytest.fail("drawing admission ran a geometric decider")

    monkeypatch.setattr(houses.reports.kernel, "run_case", forbidden)
    monkeypatch.setattr(houses.reports.legacy, "exact_verify", forbidden)
    monkeypatch.setattr(houses.reports.legacy.independent, "check_squares", forbidden)
    n = 88
    certificate = houses.reports.read_fact(n)
    shown = register.reported_bound(n)["value"]
    case = atlas.FrontierCase(
        n, shown, register.FRONTIER / "n-088.md", "", houses.reports.SOURCE_KEY
    )
    source = atlas._modern_packet_plan(case, houses.reports.SOURCE_KEY)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert source is not None
    assert source.path == houses.reports.fact_path()
    assert source.url.endswith(houses.reports.source_pins()[n]["certificate"])
    witness = atlas._build_witness(case, source)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    expected = houses.expected_house(certificate, houses.reports.check_certification()[n])
    assert witness == expected
    assert len(witness["squares"]) == n
    assert Fraction(witness["side"]) == certificate.side
    wrong = atlas.FrontierCase(n, shown + "1", case.path, "", case.reported_source_key)
    with pytest.raises(ValueError, match="Gupta side differs"):
        atlas._build_witness(wrong, source)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    withdrawn = atlas.FrontierCase(108, shown, case.path, "", case.reported_source_key)
    with pytest.raises(ValueError, match="improving roster"):
        atlas._modern_packet_plan(withdrawn, houses.reports.SOURCE_KEY)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


def test_all_four_complete_private_gupta_dependencies_are_in_production_copy_roster() -> None:
    assert len(houses.private_input_paths()) == 4
    assert set(houses.private_input_paths()) <= set(controls.COPY_SEPARATELY)
    assert set(houses.snapshot_house_links()) <= {
        controls.ROOT / path for path in controls.HOUSE_LINK_LEAVES
    }


HOUSE_MUTANTS = ("empty", "truncated", "n", "id", "source", "url", "side", "missing-pose")


def mutate_house(text: str, mutation: str) -> str:
    if mutation == "empty":
        return ""
    if mutation == "truncated":
        return text[: len(text) // 2]
    document = safe_load(text)
    witness = document["witness"]
    if mutation == "n":
        witness["n"] -= 1
    elif mutation == "id":
        witness["id"] = "W-known-best-n088"
    elif mutation == "source":
        witness["source"]["key"] = "[wrong source]"
    elif mutation == "url":
        witness["source"]["url"] = "https://example.invalid/wrong-source"
    elif mutation == "side":
        witness["side"] = str(Fraction(witness["side"]) + 1)
    else:
        assert mutation == "missing-pose"
        witness["squares"].pop()
    return register.dump(document)


@pytest.mark.parametrize("mutation", HOUSE_MUTANTS)
def test_late_invalid_house_refuses_before_history_or_frontier_write(
    original_pair: dict[int, str], mutation: str
) -> None:
    assert tuple(original_pair) == houses.NUMBERS
    path = houses.house_path(130)
    path.write_text(mutate_house(path.read_text(), mutation))
    before = frontier_bytes()
    with pytest.raises(ValueError, match="complete original prior house"):
        register.record_cases()
    assert frontier_bytes() == before
    assert not register.HISTORY.exists()


@pytest.mark.parametrize("mutation", HOUSE_MUTANTS)
def test_existing_history_requires_every_complete_original_house(
    original_pair: dict[int, str], mutation: str
) -> None:
    rows = [
        {"n": n, "frontier": text, "house": houses.house_path(n).read_text()}
        for n, text in original_pair.items()
    ]
    rows[-1]["house"] = mutate_house(rows[-1]["house"], mutation)
    houses.reports.save_xz(register.HISTORY, {"format": register.HISTORY_FORMAT, "cases": rows})
    before = frontier_bytes()
    boundary = register.HISTORY.read_bytes()
    with pytest.raises(ValueError, match="complete original prior house"):
        register.record_cases()
    assert frontier_bytes() == before
    assert register.HISTORY.read_bytes() == boundary


def test_linked_house_owner_follows_private_current_frontier(
    original_pair: dict[int, str], monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    second = houses.shared.confirmation
    original_paths = second.private_input_paths()
    repo = houses.REPO
    for original in original_paths:
        destination = repo / original.relative_to(SOURCE)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(original.read_bytes())
    monkeypatch.setattr(second, "REPO", repo)
    monkeypatch.setattr(second, "PACKET", repo / second.PACKET.relative_to(SOURCE))
    monkeypatch.setattr(second, "SCHEMA", repo / second.SCHEMA.relative_to(SOURCE))
    monkeypatch.setattr(second, "WITNESSES", repo / second.WITNESSES.relative_to(SOURCE))
    monkeypatch.setattr(check_results, "REPO", repo)

    def forbidden(*_args, **_kwargs):
        pytest.fail("source-owner admission ran a geometric decider")

    monkeypatch.setattr(second.original, "decide", forbidden)
    monkeypatch.setattr(houses.reports.kernel, "run_case", forbidden)
    path = houses.house_path(88)
    old = path.read_bytes()
    external = tmp_path / "linked-house.yaml"
    external.write_bytes(old)
    path.unlink()
    path.symlink_to(external)
    relative = path.relative_to(repo).as_posix()
    assert check_results.repository_file_problem(relative) is None

    frontier = register.FRONTIER / "n-088.md"
    document = safe_load(original_pair[88].split("---\n", 2)[1])
    document["packing"]["reported_upper_bound"] = register.reported_bound(88)
    frontier.write_text(
        "---\n" + register.dump(document) + "---\n" + original_pair[88].split("---\n", 2)[2]
    )
    assert check_results.repository_file_problem(relative)
    expected = houses.build_witness(88)
    external.write_text(second.witness_document(expected, schema="../witness.schema.yaml"))
    assert check_results.repository_file_problem(relative) is None
    frontier.write_text(original_pair[88])
    assert check_results.repository_file_problem(relative)
    frontier.unlink()
    assert check_results.repository_file_problem(relative)


def test_register_outputs_schema_valid_complete_selected_and_withdrawn_inventory(
    original_pair: dict[int, str],
    monkeypatch: pytest.MonkeyPatch,
    original_source: dict[int, dict[str, Any]],
) -> None:
    assert tuple(original_pair) == houses.NUMBERS
    monkeypatch.setattr(houses, "NUMBERS", houses.reports.SELECTED)
    monkeypatch.setattr(register, "record_cases", lambda: None)
    monkeypatch.setattr(registry.packets, "REPO", houses.REPO)
    for name in ("evidence", "results"):
        (register.FRONTIER / f"{name}.yaml").write_bytes(
            (SOURCE / f"packing/frontier/{name}.yaml").read_bytes()
        )
    result_path = register.FRONTIER / "results.yaml"
    original_result = next(
        row
        for row in safe_load(result_path.read_text())["results"]
        if row["id"] == register.RESULT
    )
    sentinel = register.PACKET_PATH + "/receipts/exact-certification.json.xz"
    register.replace_row(
        result_path,
        "results",
        {**original_result, "artifacts": [*original_result["artifacts"], sentinel]},
    )
    source_path = register.FRONTIER / "source-coverage.yaml"
    source_path.write_bytes((SOURCE / "packing/frontier/source-coverage.yaml").read_bytes())
    original = safe_load(source_path.read_text())
    if any(row["source_id"] == register.SOURCE_ID for row in original["selected_overrides"]):
        prior_selections = {}
        for n, row in original_source.items():
            prior = safe_load(row["frontier"].split("---\n", 2)[1])["packing"][
                "reported_upper_bound"
            ]
            source = next(
                item
                for item in original["sources"]
                if item["source_key"] == prior["source_key"]
            )
            prior_selections[n] = {
                "n": n,
                "source_id": source["id"],
                "value": prior["value"],
                "evidence": prior["evidence"][0],
                "reason": "Complete retained source before Gupta adoption.",
            }
        original["sources"] = [
            row for row in original["sources"] if row["id"] != register.SOURCE_ID
        ]
        original["selected_overrides"] = [
            prior_selections.get(row["n"], row) for row in original["selected_overrides"]
        ]
        original["superseded_reports"] = [
            row
            for row in original["superseded_reports"]
            if row["source_id"] != register.SOURCE_ID
            and not (
                row["n"] in prior_selections
                and row["source_id"] == prior_selections[row["n"]]["source_id"]
            )
        ]
        for row in original["superseded_reports"]:
            if row["n"] in prior_selections:
                row["superseded_by"] = prior_selections[row["n"]]["source_id"]
        source_path.write_text(register.dump(original))
    withdrawals = (108, 123, 129)
    original_selected = {
        row["n"]: row for row in original["selected_overrides"] if row["n"] in withdrawals
    }
    register.register()
    coverage = safe_load(source_path.read_text())
    monkeypatch.setattr(citations, "EVIDENCE", register.FRONTIER / "evidence.yaml")
    monkeypatch.setattr(citations, "RESULTS", result_path)
    monkeypatch.setattr(
        citations, "BIBLIOGRAPHY", register.REPO / "packing/resources/bibliography.yaml"
    )
    catalogue = citations.load_register()
    assert houses.reports.SOURCE_KEY in catalogue.sources
    bound = register.reported_bound(88)
    assert all(person in catalogue.names for person in bound["found_by"] + bound["improved_by"])
    for name in ("evidence", "results", "source-coverage"):
        validated = safe_load((register.FRONTIER / f"{name}.yaml").read_text())
        schema_path = SOURCE / "packing/frontier" / validated["softschema"]["schema"]
        schema = safe_load(schema_path.read_text())
        validated.pop("softschema")
        assert Draft202012Validator(schema).is_valid(validated), name
    claims = json.loads((houses.reports.PACKET / "acquisition/claims.json").read_text())
    offered = {row["n"]: row["offered_side"] for row in claims["results"]}
    n_min, n_max = (coverage["case_corpus"][key] for key in ("n_min", "n_max"))
    baseline_source = coverage_check.source_by_id(coverage, "kingbird-current")
    baseline = coverage_check.parse_kingbird(
        SOURCE / "packing" / baseline_source["local"], n_min, n_max
    )
    if pending := coverage.get("pending_catalogue_intake"):
        earlier = coverage_check.parse_kingbird(
            SOURCE / "packing" / coverage_check.INTAKE_CATALOGUE_HTML, n_min, n_max
        )
        baseline.update({row["n"]: earlier[row["n"]] for row in pending})
    assert (
        coverage_check.selection_errors(coverage, baseline, {register.SOURCE_ID: offered}) == []
    )
    selected = {
        row["n"]: row
        for row in coverage["selected_overrides"]
        if row["source_id"] == register.SOURCE_ID
    }
    withdrawn = {
        row["n"]: row
        for row in coverage["superseded_reports"]
        if row["source_id"] == register.SOURCE_ID
    }
    assert tuple(sorted(selected)) == houses.NUMBERS
    assert tuple(sorted(withdrawn)) == withdrawals
    for n in withdrawals:
        assert (
            next(row for row in coverage["selected_overrides"] if row["n"] == n)
            == original_selected[n]
        )
        assert withdrawn[n]["superseded_by"] == original_selected[n]["source_id"]
    result = next(
        row
        for row in safe_load(result_path.read_text())["results"]
        if row["id"] == register.RESULT
    )
    assert result["artifacts"] == [
        register.PACKET_PATH + "/README.md",
        register.PACKET_PATH + "/facts/complete-certificates-and-comparators.json.xz",
        "packing/devtools/gupta_refinement_reports.py",
        sentinel,
    ]
    assert (result["verification"], result["confirmation"]) == ("V0", "C0")
    result_bytes = result_path.read_bytes()
    first = source_path.read_bytes()
    register.register()
    assert source_path.read_bytes() == first
    assert result_path.read_bytes() == result_bytes


def test_unaffected_ryxu_link_keeps_its_complete_private_source_owner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = tmp_path / "ryxu-private"
    paths = ryxu.private_input_paths()
    for original in paths:
        path = repo / original.relative_to(SOURCE)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(original.read_bytes())
    monkeypatch.setattr(ryxu, "METADATA", repo / ryxu.METADATA.relative_to(SOURCE))
    monkeypatch.setattr(ryxu.reports, "PACKET", repo / ryxu.reports.PACKET.relative_to(SOURCE))
    monkeypatch.setattr(ryxu.reports, "REPO", repo)
    monkeypatch.setattr(ryxu, "REPO", repo)
    monkeypatch.setattr(check_results, "REPO", repo)
    frontier = repo / "packing/frontier/n-070.md"
    frontier.parent.mkdir(parents=True)
    frontier.write_bytes((SOURCE / frontier.relative_to(repo)).read_bytes())
    path = ryxu.house_path(70)
    path.parent.mkdir(parents=True)
    path.symlink_to(SOURCE / path.relative_to(repo))

    def forbidden(*_args, **_kwargs):
        pytest.fail("unaffected-source admission ran a geometric decider")

    monkeypatch.setattr(ryxu.reports.kernel, "run_case", forbidden)
    monkeypatch.setattr(ryxu.radical, "exact_verify", forbidden)
    assert check_results.repository_file_problem(path.relative_to(repo).as_posix()) is None


@pytest.mark.parametrize("indent", ["", "  "])
def test_registry_append_preserves_existing_list_indentation(
    indent: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(registry.packets, "REPO", tmp_path)
    path = tmp_path / "registry.yaml"
    text = f"# retained comment\nentries:\n{indent}- id: original\nother: unchanged\n"
    path.write_text(text)
    registry.append_rows(path, "entries", [{"id": "new", "value": "3/2"}], "id")
    value = safe_load(path.read_text())
    assert value == {
        "entries": [{"id": "original"}, {"id": "new", "value": "3/2"}],
        "other": "unchanged",
    }
    assert path.read_text().startswith(text.split("other:", maxsplit=1)[0])
    assert path.read_text().endswith("other: unchanged\n")
    first = path.read_bytes()
    registry.append_rows(path, "entries", [{"id": "new", "value": "9/2"}], "id")
    assert path.read_bytes() == first


def test_historical_prose_preserves_names_and_dates_the_compared_atlas_pose() -> None:
    earlier = (
        "Nate Chaoweeraprasit, using SQUISH, reports $s(88) \\le 9.9$.\n\n"
        "Square for square, its pose lies within `2.9e-4` of the binary64 pose "
        "the atlas pictures for this count.\n\n"
    )
    current = register.SECTION + "\n\nThe selected source is current.\n"
    rewritten = register.historical_prose(88, earlier + current)
    assert "Previously, Nate Chaoweeraprasit" in rewritten
    assert "`2.9e-4`" in rewritten
    assert "the atlas pictured at that intake for this count" in rewritten
    assert rewritten.endswith(current)
    assert register.historical_prose(88, rewritten) == rewritten


def test_pending_upper_blocker_survives_registration_resume_without_replacing_history(
    original_pair: dict[int, str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(registry.packets, "REPO", register.REPO)
    prior_cases = {
        n: safe_load(text.split("---\n", 2)[1])["packing"] for n, text in original_pair.items()
    }
    register.record_cases()
    boundary = register.HISTORY.read_bytes()
    for n, prior in prior_cases.items():
        case = safe_load(
            (register.FRONTIER / f"n-{n:03d}.md").read_text().split("---\n", 2)[1]
        )["packing"]
        assert case["blockers"][:-1] == prior["blockers"]
        assert case["blockers"][-1]["evidence"] == [register.REPORT]
        assert case["blockers"][-1]["kind"] == "source-evidence"
        for field in ("reported_lower_bound", "verified_lower_bound", "verified_upper_bound"):
            assert case[field] == prior[field]
    path = register.FRONTIER / "n-130.md"
    _, front, body = path.read_text().split("---\n", 2)
    document = safe_load(front)
    document["packing"]["blockers"].pop()
    path.write_text("---\n" + register.dump(document) + "---\n" + body)
    register.record_cases()
    assert register.HISTORY.read_bytes() == boundary
    restored = frontier_bytes()
    assert safe_load(restored[130].decode().split("---\n", 2)[1])["packing"]["blockers"][-1][
        "evidence"
    ] == [register.REPORT]
    register.record_cases()
    assert frontier_bytes() == restored
    assert register.HISTORY.read_bytes() == boundary


def test_pending_ceiling_disclosure_uses_current_report_and_retained_verified_lane() -> None:
    n = 88
    text = (register.FRONTIER / f"n-{n:03d}.md").read_text()
    _, front, body = text.split("---\n", 2)
    case = safe_load(front)["packing"]
    rewritten = register.ceiling_prose(n, case, body)
    assert register.ceiling_prose(n, case, rewritten) == rewritten
    section = rewritten.split("## The verified upper bound is a ceiling\n", 1)[1]
    section = section.split("\n## ", 1)[0]
    assert f"${case['reported_upper_bound']['value']}$" in section
    assert f"${case['verified_upper_bound']['value']}$" in section
    assert "not the value of $s(88)$" in section
    assert "actual private-worker admission" in section
    assert "pending" in section


def test_report_resume_preserves_equal_current_assessment_rendering() -> None:
    from devtools import assess_frontier_rigidity as assessment  # noqa: PLC0415

    n = 88
    text = (register.FRONTIER / f"n-{n:03d}.md").read_text()
    _, front, body = text.split("---\n", 2)
    document = safe_load(front)
    current = next(row for row in assessment.plan() if row[0] == n)
    assert current[2] == current[3], "source-bound assessment must match its owner's output"
    rewritten = register.render_selected_case(n, document, body, text)
    assert rewritten == text
    assert safe_load(rewritten.split("---\n", 2)[1]) == document
