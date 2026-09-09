"""Controls for bounded pricing from one immutable solved-support receipt."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import price_solved_support_candidates as candidate
from sqpack.fractional import colgen
from sqpack.fractional.ceiling import CeilingCertificate
from sqpack.fractional.colgen import site_set_from_points
from sqpack.fractional.cutting import SupportEntry, symmetric_placements

BLOBS: dict[tuple[str, str], bytes] = {}
OLD_HEAD = "1" * 40
NEW_HEAD = "2" * 40


@pytest.fixture(autouse=True)
def stable_source_binding(monkeypatch: pytest.MonkeyPatch) -> None:
    BLOBS.clear()
    monkeypatch.setattr(
        candidate,
        "source_binding",
        lambda path: {
            "path": path.name,
            "git_commit": NEW_HEAD,
            "source_in_worktree": True,
            "source_tracked": True,
            "source_dirty": False,
        },
    )
    monkeypatch.setattr(candidate, "_git_blob", lambda commit, path: BLOBS[(commit, path)])


def _inputs(
    tmp_path: Path,
    *,
    control_total: Fraction = Fraction(1),
    held_point: tuple[Fraction, Fraction] = (Fraction(0), Fraction(0)),
) -> tuple[Path, Path, Path]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    state_path = tmp_path / "state.json"
    solved_path = tmp_path / "solved.json"
    output_path = tmp_path / "screened.json"
    entries = (
        *(
            SupportEntry(0, Fraction(0), Fraction(3, 2), Fraction(3, 2), control_total / 32)
            for _ in range(32)
        ),
        SupportEntry(0, Fraction(0), Fraction(3, 2), Fraction(3, 2), Fraction(1, 2)),
    )
    family = CeilingCertificate(
        11,
        Fraction(3),
        Fraction(1),
        (Fraction(0), Fraction(1, 3)),
        symmetric_placements(entries, Fraction(3), Fraction(1)),
    )
    exact_rows = [[0, "3/2", "3/2"] for _ in entries]
    sites = site_set_from_points(Fraction(3), {held_point})
    state = {
        "outer_side": "3",
        "square_side": "1",
        "half_tangents": ["0", "1/3"],
        "sites": [[str(value) for value in held_point]],
        "rows": exact_rows,
        "best_family": family.to_record(),
    }
    support = {
        "schema": "paired-cutting-dual-support-v1",
        "stage": "solved_support",
        "source": {
            "path": state_path.name,
            "git_commit": OLD_HEAD,
            "source_in_worktree": True,
            "source_tracked": True,
            "source_dirty": False,
        },
        "source_transport": None,
        "settings": {"control_cap": 32, "weight_denominator": 10**9},
        "lp": {"rows": len(entries), "sites": sites.size},
        "positive_support": [
            {
                "row_index": index,
                "row": exact_rows[index],
                "half_tangent": "0",
                "raw_dual_hex": float(entry.weight).hex(),
                "rational_weight": str(entry.weight),
            }
            for index, entry in enumerate(entries)
        ],
        "full_family": family.to_record(),
    }
    state_path.write_text(json.dumps(state) + "\n")
    solved_path.write_text(json.dumps(support) + "\n")
    BLOBS[(OLD_HEAD, state_path.name)] = state_path.read_bytes()
    return state_path, solved_path, output_path


def _screen(
    state: Path,
    solved: Path,
    output: Path,
    *,
    max_line_pairs: int = 100,
    max_unique_points: int = 32,
) -> dict[str, Any]:
    return candidate.screen_candidates(
        state,
        solved,
        output,
        tail_line_limit=4,
        max_line_pairs=max_line_pairs,
        max_unique_points=max_unique_points,
    )


def test_exact_tail_intersection_witness_reuses_all_solved_support(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state, solved, output = _inputs(tmp_path)

    def forbidden_lp(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("a solved-support screen must not solve an LP")

    monkeypatch.setattr(colgen, "solve_lp", forbidden_lp)
    result = _screen(state, solved, output)

    assert result["classification"] == "paired_32_row_miss"
    assert result["evidence_of_paired_32_row_miss"] is True
    assert result["support_rows"] == 33
    assert result["source_state"]["recorded"]["git_commit"] == OLD_HEAD
    assert result["source_state"]["observed"]["git_commit"] == NEW_HEAD
    witness = result["witness"]
    assert isinstance(witness, dict)
    assert witness["orbit_absent_from_state"] is True
    assert witness["paired32"]["depth"] == "1"
    assert witness["full"]["depth"] == "3/2"
    assert len(witness["paired32"]["placement_indices"]) == 32 * 8
    assert len(witness["full"]["placement_indices"]) == 33 * 8
    assert len(witness["source_lines"]) == 2


def test_line_pair_guard_is_preflight_and_unresolved(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state, solved, output = _inputs(tmp_path)

    def forbidden(*_args: object) -> None:
        raise AssertionError("guarded sampling must not intersect lines")

    monkeypatch.setattr(candidate, "exact_intersection", forbidden)
    result = _screen(state, solved, output, max_line_pairs=21)

    assert result["classification"] == "unresolved"
    assert result["stop_reason"] == "line_pair_guard"
    assert result["sampling"]["line_pairs_examined"] == 0


def test_zero_unique_point_guard_is_preflight_and_unresolved(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state, solved, output = _inputs(tmp_path)

    def forbidden(*_args: object) -> None:
        raise AssertionError("a zero-point sample must not intersect lines")

    monkeypatch.setattr(candidate, "exact_intersection", forbidden)
    result = _screen(state, solved, output, max_unique_points=0)

    assert result["classification"] == "unresolved"
    assert result["stop_reason"] == "unique_point_guard"
    assert result["sampling"]["unique_points_examined"] == 0


def test_bounded_and_exhausted_samples_never_claim_negative_evidence(tmp_path: Path) -> None:
    state, solved, output = _inputs(tmp_path)
    bounded = _screen(state, solved, output, max_unique_points=1)
    assert bounded["classification"] == "unresolved"
    assert bounded["stop_reason"] == "unique_point_guard"
    assert bounded["sampling"]["unique_points_examined"] == 1

    state, solved, output = _inputs(tmp_path / "exhausted", control_total=Fraction(2))
    exhausted = _screen(state, solved, output)
    assert exhausted["classification"] == "unresolved"
    assert exhausted["stop_reason"] == "selected_sample_exhausted"
    assert exhausted["evidence_of_paired_32_row_miss"] is False


def test_held_orbit_cannot_be_positive(tmp_path: Path) -> None:
    state, solved, output = _inputs(tmp_path, held_point=(Fraction(1), Fraction(1)))
    result = _screen(state, solved, output)

    assert result["classification"] == "unresolved"
    assert result["stop_reason"] == "selected_sample_exhausted"
    assert result["sampling"]["held_orbit_points"] > 0


@pytest.mark.parametrize("damage", ["binding", "grouping"])
def test_input_binding_and_support_grouping_fail_closed(tmp_path: Path, damage: str) -> None:
    state, solved, output = _inputs(tmp_path)
    receipt = json.loads(solved.read_text())
    if damage == "binding":
        receipt["source"] = {"path": "another-state.json"}
    else:
        receipt["full_family"]["placements"].pop()
    solved.write_text(json.dumps(receipt) + "\n")

    with pytest.raises(ValueError, match=r"binding|full_family"):
        _screen(state, solved, output)
    assert not output.exists()


def test_tampered_state_bytes_fail_the_retained_blob_check(tmp_path: Path) -> None:
    state, solved, output = _inputs(tmp_path)
    state.write_text(state.read_text() + " ")
    with pytest.raises(ValueError, match="bytes differ"):
        _screen(state, solved, output)
    assert not output.exists()


def test_option_like_commit_is_refused_before_git_lookup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state, solved, output = _inputs(tmp_path)
    receipt = json.loads(solved.read_text())
    receipt["source"]["git_commit"] = "--help"
    solved.write_text(json.dumps(receipt) + "\n")

    def forbidden(*_args: object) -> bytes:
        raise AssertionError("an invalid revision must not reach git")

    monkeypatch.setattr(candidate, "_git_blob", forbidden)
    with pytest.raises(ValueError, match="full 40-character hexadecimal"):
        _screen(state, solved, output)
    assert not output.exists()


def test_sparse_incident_pairs_skip_every_unselected_pair() -> None:
    pairs = list(candidate.incident_pairs(10, {2, 8}))
    assert pairs == sorted(set(pairs))
    assert len(pairs) == 2 * 10 - 2 * 3 // 2
    assert (3, 4) not in pairs


def test_existing_output_refuses_before_reading_inputs(tmp_path: Path) -> None:
    output = tmp_path / "screened.json"
    output.write_text("old\n")
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        _screen(tmp_path / "missing-state", tmp_path / "missing-solved", output)
    assert output.read_text() == "old\n"
