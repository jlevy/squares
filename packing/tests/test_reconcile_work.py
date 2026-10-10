"""Reconciliation queues preserve unfinished scope and disjoint review coverage."""

import json
import sys
from pathlib import Path

import pytest

from devtools.reconcile_work import inventory, main, review_coverage


def test_closed_children_are_not_confused_with_undecomposed_work(tmp_path: Path) -> None:
    report = inventory(
        [
            {"id": "think-a111", "status": "open", "kind": "epic"},
            {"id": "think-z111", "status": "open", "kind": "epic"},
            {"id": "think-c111", "status": "closed", "parentId": "think-a111"},
        ],
        tmp_path,
    )
    decomposed = report["lanes"]["a"]["beads"][0]
    undecomposed = report["lanes"]["b"]["beads"][0]
    assert decomposed["children_total"] == 1
    assert decomposed["children_nonclosed"] == 0
    assert "all_children_closed_read_scope" in decomposed["review_flags"]
    assert undecomposed["children_total"] == 0
    assert not undecomposed["review_flags"]


def test_queues_cover_nonclosed_beads_and_all_specs_once(tmp_path: Path) -> None:
    specs = tmp_path / "docs/project/specs/active"
    specs.mkdir(parents=True)
    (specs / "first.md").write_text("- [ ] Keep unfinished work\n", encoding="utf-8")
    (specs / "second.md").write_text("- [x] Finished\n", encoding="utf-8")
    report = inventory(
        [
            {"id": "think-0111", "status": "in_progress"},
            {"id": "think-i111", "status": "deferred"},
            {"id": "think-z111", "status": "closed"},
        ],
        tmp_path,
    )
    lanes = list(report["lanes"].values())
    ids = [b["id"] for lane in lanes for b in lane["beads"]]
    assert sorted(ids) == ["think-0111", "think-i111"]
    paths = [s["path"] for lane in lanes for s in lane["specs"]]
    assert len(paths) == len(set(paths)) == 2
    assert sum(s["unchecked"] for lane in lanes for s in lane["specs"]) == 1


def test_spec_mentions_resolve_nonclosed_and_missing_beads(tmp_path: Path) -> None:
    specs = tmp_path / "docs/project/specs/active"
    specs.mkdir(parents=True)
    (specs / "plan.md").write_text(
        "Tracks think-a111, think-b111, and think-missing.\n", encoding="utf-8"
    )
    report = inventory(
        [
            {"id": "think-a111", "status": "open"},
            {"id": "think-b111", "status": "closed"},
        ],
        tmp_path,
    )
    spec = report["lanes"]["a"]["specs"][0]
    assert spec["mentioned_beads"] == ["think-a111", "think-b111", "think-missing"]
    assert spec["mentioned_nonclosed"] == ["think-a111"]
    assert spec["mentioned_missing"] == ["think-missing"]


def test_missing_spec_reports_candidates_without_asserting_a_move(tmp_path: Path) -> None:
    for folder in ("active", "done"):
        directory = tmp_path / "docs/project/specs" / folder
        directory.mkdir(parents=True)
        (directory / "same.md").write_text("A plan.\n", encoding="utf-8")
    report = inventory(
        [{"id": "think-a111", "status": "open", "spec_path": "old/same.md"}],
        tmp_path,
    )
    bead = report["lanes"]["a"]["beads"][0]
    assert not bead["spec_exists"]
    assert bead["spec_same_filename"] == [
        "docs/project/specs/active/same.md",
        "docs/project/specs/done/same.md",
    ]
    assert bead["review_flags"] == ["missing_spec_path"]


def test_review_coverage_refuses_omissions_duplicates_and_unsupported_closures(
    tmp_path: Path,
) -> None:
    report = inventory(
        [{"id": "think-a111", "status": "open"}, {"id": "think-z111", "status": "open"}],
        tmp_path,
    )
    item = {
        "id": "think-a111",
        "action": "close",
        "reason": "All done",
        "updates": {
            "expected_version": 2,
            "expected_status": "open",
            "status": "closed",
        },
    }
    incomplete = review_coverage(report, [{"beads": [item, item]}])
    assert "missing beads: think-z111" in incomplete["problems"]
    assert "duplicate beads: think-a111" in incomplete["problems"]
    assert "disposition without evidence: think-a111" in incomplete["problems"]
    complete = review_coverage(
        report,
        [
            {
                "beads": [
                    {**item, "evidence": ["Verified completion receipt"]},
                    {
                        "id": "think-z111",
                        "action": "needs_evidence",
                        "reason": "No completion receipt",
                        "evidence": ["Fresh record has no completion note"],
                    },
                ]
            }
        ],
    )
    assert not complete["problems"]


def test_retained_scope_survives_a_spec_move() -> None:
    baseline = {"beads": ["think-a111"], "specs": ["docs/project/specs/active/plan.md"]}
    review = {
        "beads": [
            {
                "id": "think-a111",
                "action": "retain",
                "reason": "Work remains",
                "evidence": ["Current bead remains open"],
            }
        ],
        "specs": [
            {
                "path": "docs/project/specs/active/plan.md",
                "action": "move_draft",
                "reason": "Never launched",
                "evidence": ["The plan explicitly says Draft"],
            }
        ],
    }
    assert not review_coverage(baseline, [review])["problems"]


def test_review_coverage_requires_evidence_for_every_disposition() -> None:
    baseline = {"beads": ["think-a111"], "specs": ["plan.md"]}
    review = {
        "beads": [{"id": "think-a111", "action": "retain", "reason": "Work remains"}],
        "specs": [{"path": "plan.md", "action": "needs_evidence", "reason": "Unclear"}],
    }
    problems = review_coverage(baseline, [review])["problems"]
    assert "disposition without evidence: think-a111" in problems
    assert "disposition without evidence: plan.md" in problems


def test_review_coverage_requires_freshness_and_a_mutation_target() -> None:
    baseline = {"beads": ["think-a111"], "specs": []}
    base = {
        "id": "think-a111",
        "action": "update",
        "reason": "Repair stale metadata",
        "evidence": ["Fresh tracker record"],
    }
    missing_updates = review_coverage(baseline, [{"beads": [base]}])["problems"]
    assert "mutation without updates: think-a111" in missing_updates

    missing_freshness = review_coverage(
        baseline,
        [{"beads": [{**base, "updates": {"spec_path": "plan.md"}}]}],
    )["problems"]
    assert "mutation without expected_version: think-a111" in missing_freshness
    assert "mutation without expected_status: think-a111" in missing_freshness

    no_target = review_coverage(
        baseline,
        [
            {
                "beads": [
                    {
                        **base,
                        "updates": {"expected_version": 3, "expected_status": "open"},
                    }
                ]
            }
        ],
    )["problems"]
    assert "mutation without target: think-a111" in no_target

    valid = review_coverage(
        baseline,
        [
            {
                "beads": [
                    {
                        **base,
                        "updates": {
                            "expected_version": 3,
                            "expected_status": "open",
                            "spec_path": "docs/project/specs/active/plan.md",
                        },
                    }
                ]
            }
        ],
    )
    assert not valid["problems"]


def test_mutation_target_typo_is_rejected() -> None:
    baseline = {"beads": ["think-a111"], "specs": []}
    review = {
        "beads": [
            {
                "id": "think-a111",
                "action": "update",
                "reason": "Repair stale metadata",
                "evidence": ["Fresh tracker record"],
                "updates": {
                    "expected_version": 3,
                    "expected_status": "open",
                    "spec_paht": "docs/project/specs/active/plan.md",
                },
            }
        ]
    }
    problems = review_coverage(baseline, [review])["problems"]
    assert "unknown mutation fields: think-a111: spec_paht" in problems
    assert "mutation without target: think-a111" in problems


def test_close_requires_a_closed_status_target() -> None:
    baseline = {"beads": ["think-a111"], "specs": []}
    review = {
        "beads": [
            {
                "id": "think-a111",
                "action": "close",
                "reason": "Delivered",
                "evidence": ["Completion receipt"],
                "updates": {
                    "expected_version": 3,
                    "expected_status": "open",
                    "close_reason": "Delivered",
                },
            }
        ]
    }
    assert (
        "close without closed target: think-a111"
        in review_coverage(baseline, [review])["problems"]
    )


def test_review_coverage_rejects_unknown_spec_actions() -> None:
    baseline = {"beads": [], "specs": ["plan.md"]}
    review = {
        "specs": [
            {
                "path": "plan.md",
                "action": "move_dnoe",
                "reason": "Typo",
                "evidence": ["A receipt"],
            }
        ]
    }
    assert "unknown spec action: plan.md" in review_coverage(baseline, [review])["problems"]


def test_relocated_closed_beads_still_establish_spec_decomposition(tmp_path: Path) -> None:
    specs = tmp_path / "docs/project/specs/active"
    specs.mkdir(parents=True)
    (specs / "plan.md").write_text("- [ ] Remaining scope\n", encoding="utf-8")
    path = "docs/project/specs/active/plan.md"
    report = inventory(
        [{"id": "think-a111", "status": "closed", "spec_path": f"explorations/packing/{path}"}],
        tmp_path,
    )
    spec = report["lanes"]["a"]["specs"][0]
    assert spec["linked_total"] == 1
    assert not spec["linked_nonclosed"]
    assert spec["unchecked"] == 1
    assert report["exact_path_repairs"][0]["to"] == path


@pytest.mark.parametrize("option", [("--lane", "a"), ("--path-repairs",), ("--baseline",)])
def test_cli_rejects_inventory_only_modes_for_retained_baseline(
    option: tuple[str, ...],
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    baseline = tmp_path / "baseline.json"
    baseline.write_text(json.dumps({"beads": [], "specs": []}), encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["reconcile_work", str(baseline), *option])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert "require a full tbd list snapshot" in capsys.readouterr().err


def test_cli_rejects_conflicting_output_modes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text("[]\n", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["reconcile_work", str(snapshot), "--lane", "a", "--path-repairs"],
    )
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert "not allowed with argument" in capsys.readouterr().err
