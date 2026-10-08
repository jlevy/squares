"""Complete preflight and history-first interrupted Gupta adoption."""

from __future__ import annotations

import copy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import build_known_best_atlas as atlas
from devtools import gupta_house_links as houses
from devtools import register_gupta_reports as register
from devtools import run_negative_controls as controls
from sqpack.yamlio import safe_load

SOURCE = houses.REPO


@pytest.fixture
def original_pair(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[int, str]:
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
    originals = {}
    for n in houses.NUMBERS:
        original = SOURCE / "packing/frontier" / f"n-{n:03d}.md"
        originals[n] = original.read_text()
        (register.FRONTIER / original.name).write_text(originals[n])
        house = houses.house_path(n)
        house.parent.mkdir(parents=True, exist_ok=True)
        house.write_bytes((SOURCE / house.relative_to(repo)).read_bytes())
    return originals


def frontier_bytes() -> dict[int, bytes]:
    return {n: (register.FRONTIER / f"n-{n:03d}.md").read_bytes() for n in houses.NUMBERS}


def test_all_fourteen_current_exact_lanes_are_strictly_improved() -> None:
    facts = houses.reports.read_facts()
    for n in houses.NUMBERS:
        document = safe_load(
            (register.FRONTIER / f"n-{n:03d}.md").read_text().split("---\n", 2)[1]
        )["packing"]
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
            "blockers",
        ):
            assert after[field] == before[field]
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
