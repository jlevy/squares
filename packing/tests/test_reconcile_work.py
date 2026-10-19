"""Reconciliation queues preserve unfinished scope and disjoint review coverage."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from devtools.reconcile_work import (
    annotate_prior,
    branch_only_paths,
    cited_commits,
    duplicate_candidates,
    inventory,
    main,
    open_needs_evidence,
    review_coverage,
    split_lanes,
    status_line,
    verify_applied,
)


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
            "close_reason": "All done",
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


def test_close_resolution_is_known_and_a_duplicate_names_its_target() -> None:
    baseline = {"beads": ["think-a111", "think-b111", "think-c111"], "specs": []}

    def close(bead_id: str, **targets: str) -> dict[str, object]:
        return {
            "id": bead_id,
            "action": "close",
            "reason": "Superseded",
            "evidence": ["Owner decision"],
            "updates": {
                "expected_version": 2,
                "expected_status": "open",
                "status": "closed",
                "close_reason": "Superseded",
                **targets,
            },
        }

    review = {
        "beads": [
            close("think-a111", resolution="duplicate", duplicate_of="think-z111"),
            close("think-b111", resolution="duplicate"),
            close("think-c111", resolution="abandoned"),
        ]
    }
    problems = review_coverage(baseline, [review])["problems"]
    assert problems == [
        "duplicate close needs exactly one target: think-b111",
        "unknown close resolution: think-c111",
    ]


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


def test_status_line_keeps_the_whole_claim() -> None:
    assert status_line("# Plan\n\n**Status:** Active (4 of 10 items landed)\n") == (
        "Active (4 of 10 items landed)"
    )
    assert status_line("---\ntitle: x\nstatus: implemented\n---\n") == "implemented"
    assert status_line("# Plan\n\nNo lifecycle claim here.\n") == ""


def test_split_keeps_each_spec_with_the_beads_it_governs(tmp_path: Path) -> None:
    specs = tmp_path / "docs/project/specs/active"
    specs.mkdir(parents=True)
    for name in ("big", "small"):
        (specs / f"{name}.md").write_text("A plan.\n", encoding="utf-8")
    big = "docs/project/specs/active/big.md"
    small = "docs/project/specs/active/small.md"
    beads = [{"id": f"think-b{i}", "status": "open", "spec_path": big} for i in range(4)]
    beads += [
        {"id": "think-s1", "status": "open", "spec_path": f"explorations/packing/{small}"},
        {"id": "think-free", "status": "in_progress"},
    ]
    report = split_lanes(inventory(beads, tmp_path), 3, tmp_path)
    assert list(report["lanes"]) == ["1", "2", "3"]
    for lane in report["lanes"].values():
        governed = {current for b in lane["beads"] if (current := b.get("spec_path"))}
        held = {s["path"] for s in lane["specs"]}
        assert all(path.removeprefix("explorations/packing/") in held for path in governed)
    ids = sorted(b["id"] for lane in report["lanes"].values() for b in lane["beads"])
    assert ids == sorted(b["id"] for b in beads)
    assert report["counts"]["lane_1_beads"] == 4
    assert "lane_a_beads" not in report["counts"]
    again = split_lanes(inventory(beads, tmp_path), 3, tmp_path)
    assert again["lanes"] == report["lanes"]


def test_prior_dispositions_follow_a_moved_spec(tmp_path: Path) -> None:
    done = tmp_path / "docs/project/specs/done"
    done.mkdir(parents=True)
    (done / "plan.md").write_text("A plan.\n", encoding="utf-8")
    report = annotate_prior(
        inventory([{"id": "think-a111", "status": "open"}], tmp_path),
        [
            {
                "beads": [{"id": "think-a111", "action": "retain", "reason": "Live"}],
                "specs": [
                    {
                        "path": "docs/project/specs/active/plan.md",
                        "action": "move_done",
                        "reason": "Finished",
                    }
                ],
            }
        ],
    )
    lane = report["lanes"]["a"]
    assert lane["beads"][0]["prior"] == {"action": "retain", "reason": "Live"}
    assert lane["specs"][0]["prior"]["action"] == "move_done"


def test_cli_prints_one_split_lane_and_refuses_an_unknown_one(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text(
        json.dumps(
            [{"id": "think-a111", "status": "open"}, {"id": "think-b111", "status": "open"}]
        ),
        encoding="utf-8",
    )
    argv = ["reconcile_work", str(snapshot), "--repo", str(tmp_path), "--split", "2"]
    monkeypatch.setattr(sys, "argv", [*argv, "--lane", "2"])
    main()
    assert [b["id"] for b in json.loads(capsys.readouterr().out)["beads"]] == ["think-b111"]
    monkeypatch.setattr(sys, "argv", [*argv, "--lane", "a"])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert "no lane 'a'" in capsys.readouterr().err


def test_verify_applied_finds_unapplied_closes_moves_and_stale_paths(tmp_path: Path) -> None:
    done = tmp_path / "docs/project/specs/done"
    done.mkdir(parents=True)
    (done / "moved.md").write_text("A plan.\n", encoding="utf-8")
    (tmp_path / "docs/project/specs/active").mkdir(parents=True)
    (tmp_path / "docs/project/specs/active/stuck.md").write_text("A plan.\n", encoding="utf-8")
    old = "docs/project/specs/active/moved.md"
    review = {
        "beads": [
            {"id": "think-a111", "action": "close", "updates": {"status": "closed"}},
            {"id": "think-b111", "action": "close", "updates": {"status": "closed"}},
            {"id": "think-c111", "action": "update", "updates": {"spec_path": old}},
            {"id": "think-d111", "action": "update", "updates": {"hold": "paused"}},
            {"id": "think-e111", "action": "retain"},
        ],
        "specs": [
            {"path": old, "action": "move_done"},
            {"path": "docs/project/specs/active/stuck.md", "action": "move_paused"},
            {"path": "docs/project/specs/active/kept.md", "action": "retain"},
        ],
    }
    snapshot = [
        {"id": "think-a111", "status": "closed"},
        {"id": "think-b111", "status": "open"},
        {"id": "think-c111", "status": "open", "spec_path": "docs/project/specs/done/moved.md"},
        {"id": "think-d111", "status": "open"},
        {"id": "think-e111", "status": "open", "spec_path": old},
    ]
    result = verify_applied(snapshot, [review], tmp_path)
    assert result["checked"] == 5
    assert result["unchecked_fields"] == {"hold": 1, "resolution": 2}
    assert result["problems"] == [
        "moved spec missing from docs/project/specs/paused/stuck.md",
        "moved spec still at docs/project/specs/active/stuck.md",
        "not closed: think-b111 is open",
        "bead still names a moved spec's old path: think-e111",
    ]


def test_cited_commits_must_be_on_the_base(tmp_path: Path) -> None:
    def git(*arguments: str) -> str:
        return subprocess.run(
            ["git", "-C", str(tmp_path), *arguments],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.org")
    git("config", "user.name", "t")
    git("commit", "-q", "--allow-empty", "-m", "on main")
    on_main = git("rev-parse", "HEAD")
    git("checkout", "-q", "-b", "side")
    git("commit", "-q", "--allow-empty", "-m", "off main")
    off_main = git("rev-parse", "HEAD")
    review = {
        "beads": [
            {"id": "think-a111", "action": "close", "evidence": [f"landed in {on_main}"]},
            {"id": "think-b111", "action": "close", "evidence": [f"landed in {off_main}"]},
            {
                "id": "think-c111",
                "action": "close",
                "evidence": ["comment 6106560733, deadbeefcafe"],
            },
            {"id": "think-d111", "action": "retain", "evidence": [off_main]},
        ]
    }
    result = cited_commits([review], tmp_path, base="main")
    assert result["closes"] == 3
    assert result["citing_commits"] == 3
    assert result["off_base"] == [f"think-b111: {off_main} is not on main"]
    assert result["unresolved"] == ["think-c111: deadbeefcafe"]


def test_duplicate_candidates_pair_open_beads_with_open_or_finished_twins() -> None:
    beads = [
        {
            "id": "think-a111",
            "status": "open",
            "title": "Fix the atlas legend swatch alignment",
        },
        {
            "id": "think-b111",
            "status": "in_progress",
            "title": "Atlas legend swatch alignment fix",
        },
        {
            "id": "think-c111",
            "status": "closed",
            "title": "Fix the atlas legend swatch alignment",
        },
        {"id": "think-d111", "status": "closed", "title": "Atlas legend swatch alignment"},
        {"id": "think-e111", "status": "open", "title": "Measure the verifier cohort"},
    ]
    pairs = duplicate_candidates(beads)
    assert [pair["ids"] for pair in pairs] == [
        ["think-a111", "think-b111"],
        ["think-a111", "think-c111"],
        ["think-b111", "think-c111"],
        ["think-a111", "think-d111"],
        ["think-b111", "think-d111"],
    ]
    assert pairs[0]["score"] == 1.0
    assert all("think-e111" not in pair["ids"] for pair in pairs)
    assert duplicate_candidates(beads, threshold=0.9)[-1]["ids"] == ["think-b111", "think-c111"]


def test_needs_evidence_lists_only_what_is_still_open_and_undecided(tmp_path: Path) -> None:
    (tmp_path / "plan.md").write_text("A plan.\n", encoding="utf-8")
    older = {
        "beads": [
            {"id": "think-a111", "action": "needs_evidence", "reason": "Owner decides"},
            {"id": "think-b111", "action": "needs_evidence", "reason": "Missing receipt"},
            {"id": "think-c111", "action": "needs_evidence", "reason": "Gone"},
        ],
        "specs": [
            {"path": "plan.md", "action": "needs_evidence", "reason": "Status?"},
            {"path": "moved.md", "action": "needs_evidence", "reason": "Moved"},
        ],
    }
    newer = {"beads": [{"id": "think-b111", "action": "retain", "reason": "Decided"}]}
    snapshot = [
        {"id": "think-a111", "status": "open"},
        {"id": "think-b111", "status": "open"},
        {"id": "think-c111", "status": "closed"},
    ]
    result = open_needs_evidence(snapshot, [older, newer], tmp_path)
    assert result["open"] == 2
    assert [item["id"] for item in result["items"]] == ["think-a111", "plan.md"]


def test_branch_only_paths_finds_beads_that_dangle_on_the_base(tmp_path: Path) -> None:
    def git(*arguments: str) -> None:
        subprocess.run(
            ["git", "-C", str(tmp_path), *arguments], check=True, capture_output=True
        )

    git("init", "-q", "-b", "main")
    git("config", "user.email", "t@example.org")
    git("config", "user.name", "t")
    (tmp_path / "on-main.md").write_text("A plan.\n", encoding="utf-8")
    git("add", "on-main.md")
    git("commit", "-q", "-m", "base")
    git("checkout", "-q", "-b", "side")
    (tmp_path / "moved.md").write_text("A plan.\n", encoding="utf-8")
    beads = [
        {"id": "think-a111", "status": "closed", "spec_path": "moved.md"},
        {"id": "think-b111", "status": "open", "spec_path": "moved.md"},
        {"id": "think-c111", "status": "open", "spec_path": "on-main.md"},
        {"id": "think-d111", "status": "open", "spec_path": "gone.md"},
    ]
    result = branch_only_paths(beads, tmp_path, "main")
    assert (result["beads"], result["nonclosed"]) == (2, 1)
    assert result["by_path"] == {"moved.md": 2}


@pytest.mark.parametrize(
    "option",
    [
        ("--lane", "a"),
        ("--path-repairs",),
        ("--baseline",),
        ("--split", "2"),
        ("--verify", "review.json"),
        ("--duplicates",),
        ("--needs-evidence", "review.json"),
        ("--branch-only-paths",),
    ],
)
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


def round_one_receipt() -> dict[str, object]:
    """The 10 October applied receipt's shape: past-tense actions, targets at the top."""
    return {
        "beads": [
            {"id": "think-a111", "action": "closed", "previous_version": 5},
            {
                "id": "think-b111",
                "action": "closed_duplicate",
                "duplicate_of": "think-z111",
            },
            {"id": "think-c111", "action": "updated", "hold": "paused", "previous_version": 3},
            {"id": "think-d111", "action": "notes_updated"},
        ],
        "path_repairs": [
            {
                "id": "think-e111",
                "from": "explorations/packing/docs/project/specs/active/plan.md",
                "to": "docs/project/specs/active/plan.md",
                "previous_version": 2,
            }
        ],
    }


def test_verify_reads_the_round_one_receipt_and_fails_what_was_not_applied(
    tmp_path: Path,
) -> None:
    snapshot = [
        {"id": "think-a111", "status": "open"},
        {"id": "think-b111", "status": "in_progress"},
        {"id": "think-c111", "status": "open"},
        {"id": "think-d111", "status": "open"},
        {"id": "think-e111", "status": "open", "spec_path": "explorations/packing/x.md"},
    ]
    result = verify_applied(snapshot, [round_one_receipt()], tmp_path)
    assert result["problems"] == [
        "not closed: think-a111 is open",
        "not closed: think-b111 is in_progress",
        "spec_path not applied: think-e111 has explorations/packing/x.md",
    ]
    assert result["checked"] == 3
    assert result["unchecked_fields"] == {
        "close_reason": 2,
        "duplicate_of": 1,
        "hold": 1,
        "notes": 1,
        "resolution": 2,
        "version": 3,
    }


def test_verify_passes_the_round_one_receipt_once_it_holds(tmp_path: Path) -> None:
    snapshot = [
        {"id": "think-a111", "internalId": "is-a", "status": "closed"},
        {"id": "think-b111", "internalId": "is-b", "status": "closed"},
        {"id": "think-c111", "internalId": "is-c", "status": "open"},
        {"id": "think-d111", "internalId": "is-d", "status": "open"},
        {
            "id": "think-e111",
            "internalId": "is-e",
            "status": "open",
            "spec_path": "docs/project/specs/active/plan.md",
        },
        {"id": "think-z111", "internalId": "is-z", "status": "open"},
    ]
    shown = {
        "think-a111": {"status": "closed", "version": 6},
        "think-b111": {"status": "closed", "resolution": "duplicate", "duplicate_of": "is-z"},
        "think-c111": {"status": "open", "hold": "paused", "version": 4},
        "think-d111": {"status": "open", "version": 2},
        "think-e111": {
            "status": "open",
            "version": 3,
            "spec_path": "docs/project/specs/active/plan.md",
        },
    }
    result = verify_applied(snapshot, [round_one_receipt()], tmp_path, shown)
    assert result["problems"] == []
    assert result["unchecked_fields"] == {"close_reason": 2, "notes": 1}


def test_verify_fails_an_unknown_action_and_a_record_it_cannot_read(tmp_path: Path) -> None:
    typo = {"beads": [{"id": "think-a111", "action": "Close", "updates": {"status": "closed"}}]}
    result = verify_applied([{"id": "think-a111", "status": "open"}], [typo], tmp_path)
    assert result["problems"] == [
        "unknown bead action: think-a111: Close",
        "nothing verified: no recognized close, update, move or path repair",
    ]
    moved = {"specs": [{"path": "docs/project/specs/active/x.md", "action": "move_dnoe"}]}
    assert (
        "unknown spec action: docs/project/specs/active/x.md: move_dnoe"
        in (verify_applied([], [moved], tmp_path)["problems"])
    )


def test_cli_verify_exits_nonzero_when_nothing_is_recognized(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text(json.dumps([{"id": "think-a111", "status": "open"}]), encoding="utf-8")
    receipt = tmp_path / "receipt.json"
    receipt.write_text(
        json.dumps({"beads": [{"id": "think-a111", "action": "retain"}]}), encoding="utf-8"
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "reconcile_work",
            str(snapshot),
            "--repo",
            str(tmp_path),
            "--verify",
            str(receipt),
            "--snapshot-only",
        ],
    )
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 1
    assert "nothing verified" in capsys.readouterr().out


def duplicate_close() -> dict[str, object]:
    return {
        "beads": [
            {
                "id": "think-a111",
                "action": "close",
                "updates": {
                    "expected_version": 3,
                    "expected_status": "open",
                    "status": "closed",
                    "resolution": "duplicate",
                    "duplicate_of": "think-z111",
                    "close_reason": "Same as think-z111",
                },
            }
        ]
    }


def test_verify_checks_resolution_duplicate_and_reason_from_tbd_show(tmp_path: Path) -> None:
    snapshot = [
        {"id": "think-a111", "internalId": "is-a", "status": "closed"},
        {"id": "think-z111", "internalId": "is-z", "status": "open"},
    ]
    applied_as_plain = {
        "think-a111": {"status": "closed", "version": 4, "close_reason": "Done"}
    }
    result = verify_applied(snapshot, [duplicate_close()], tmp_path, applied_as_plain)
    assert result["problems"] == [
        "close_reason not applied: think-a111 has 'Done'",
        "duplicate_of not applied: think-a111 has None",
        "resolution not applied: think-a111 has completed",
    ]
    held = {
        "think-a111": {
            "status": "closed",
            "version": 3,
            "resolution": "duplicate",
            "duplicate_of": "is-z",
            "close_reason": "Same as think-z111",
        }
    }
    assert verify_applied(snapshot, [duplicate_close()], tmp_path, held)["problems"] == [
        "version not advanced: think-a111 is at 3, recorded as applied at 3"
    ]


def test_verify_counts_what_a_list_snapshot_cannot_show(tmp_path: Path) -> None:
    result = verify_applied(
        [{"id": "think-a111", "status": "closed"}], [duplicate_close()], tmp_path
    )
    assert result["problems"] == []
    assert result["checked"] == 1
    assert result["unchecked_fields"] == {
        "close_reason": 1,
        "duplicate_of": 1,
        "resolution": 1,
        "version": 1,
    }


def test_verify_follows_a_spec_moved_twice_and_a_later_repair(tmp_path: Path) -> None:
    archive = tmp_path / "docs/project/specs/archive"
    archive.mkdir(parents=True)
    (archive / "x.md").write_text("A plan.\n", encoding="utf-8")
    (tmp_path / "docs/project/specs/done").mkdir(parents=True)
    (tmp_path / "docs/project/specs/done/y.md").write_text("A plan.\n", encoding="utf-8")
    first = {
        "specs": [
            {"path": "docs/project/specs/active/x.md", "action": "move_done"},
            {"path": "docs/project/specs/active/y.md", "action": "move_done"},
        ],
        "beads": [
            {
                "id": "think-a111",
                "action": "update",
                "updates": {"spec_path": "docs/project/specs/draft/old.md"},
            },
            {
                "id": "think-b111",
                "action": "update",
                "updates": {"spec_path": "docs/project/specs/active/x.md"},
            },
        ],
    }
    second = {
        "specs": [
            {
                "path": "docs/project/specs/done/x.md",
                "action": "move_archive",
                "new_status": "Archived.",
            },
            {"path": "docs/project/specs/done/y.md", "action": "move_done"},
        ],
        "beads": [
            {
                "id": "think-a111",
                "action": "update",
                "updates": {"spec_path": "docs/project/specs/archive/x.md"},
            }
        ],
    }
    snapshot = [
        {"id": "think-a111", "status": "open", "spec_path": "docs/project/specs/archive/x.md"},
        {"id": "think-b111", "status": "open", "spec_path": "docs/project/specs/archive/x.md"},
    ]
    result = verify_applied(snapshot, [first, second], tmp_path)
    assert result["problems"] == []
    assert result["checked"] == 4
    assert result["unchecked_fields"] == {"new_status": 1}
    stale = [
        *snapshot,
        {"id": "think-c111", "status": "open", "spec_path": "docs/project/specs/done/x.md"},
    ]
    assert verify_applied(stale, [first, second], tmp_path)["problems"] == [
        "bead still names a moved spec's old path: think-c111"
    ]


def test_cited_commits_checks_its_base_and_can_fail_on_unresolved_tokens(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    subprocess.run(["git", "init", "-q", "-b", "main", str(tmp_path)], check=True)
    review = {"beads": [{"id": "think-a111", "action": "close", "evidence": ["deadbeefcafe"]}]}
    missing = cited_commits([review], tmp_path, base="origin/main")
    assert missing["problems"] == ["base does not resolve to a commit: origin/main"]
    receipt = tmp_path / "receipt.json"
    receipt.write_text(json.dumps(review), encoding="utf-8")
    argv = ["reconcile_work", "--repo", str(tmp_path), "--check-commits", str(receipt)]
    for extra, code in (([], 1), (["--base", "HEAD"], 1)):
        monkeypatch.setattr(sys, "argv", [*argv, *extra])
        with pytest.raises(SystemExit) as error:
            main()
        assert error.value.code == code
    capsys.readouterr()
    git = ["git", "-C", str(tmp_path), "-c", "user.email=t@example.org", "-c", "user.name=t"]
    subprocess.run([*git, "commit", "-q", "--allow-empty", "-m", "base"], check=True)
    for extra, code in (([], 0), (["--strict"], 1)):
        monkeypatch.setattr(sys, "argv", [*argv, "--base", "main", *extra])
        with pytest.raises(SystemExit) as error:
            main()
        assert error.value.code == code
    out = json.loads(capsys.readouterr().out.split("\n}\n")[0] + "\n}")
    assert out["unresolved"] == ["think-a111: deadbeefcafe"]
    assert "not fetched here" in out["note"]


def test_review_coverage_requires_a_close_reason_and_no_updates_on_a_retain() -> None:
    baseline = {"beads": ["think-a111", "think-b111", "think-c111"], "specs": []}
    updates = {"expected_version": 2, "expected_status": "open", "status": "closed"}
    review = {
        "beads": [
            {
                "id": "think-a111",
                "action": "close",
                "reason": "Done",
                "evidence": ["Receipt"],
                "updates": updates,
            },
            {
                "id": "think-b111",
                "action": "retain",
                "reason": "Live",
                "evidence": ["Open"],
                "updates": {"expected_version": 2, "expected_status": "open", "hold": "paused"},
            },
            {
                "id": "think-c111",
                "action": "close",
                "reason": "Same",
                "evidence": ["Twin"],
                "updates": {
                    **updates,
                    "close_reason": "Same",
                    "resolution": "duplicate",
                    "duplicate_of": "think-c111",
                },
            },
        ]
    }
    assert review_coverage(baseline, [review])["problems"] == [
        "close without close_reason: think-a111",
        "updates on a disposition that changes nothing: think-b111",
        "duplicate of itself: think-c111",
    ]


def test_prior_dispositions_do_not_cross_folders_that_share_a_filename(tmp_path: Path) -> None:
    for folder in ("active", "done"):
        directory = tmp_path / "docs/project/specs" / folder
        directory.mkdir(parents=True)
        (directory / "same.md").write_text("A plan.\n", encoding="utf-8")
    report = annotate_prior(
        inventory([], tmp_path),
        [
            {
                "specs": [
                    {
                        "path": "docs/project/specs/active/same.md",
                        "action": "retain",
                        "reason": "Live",
                    }
                ]
            }
        ],
    )
    priors = {
        spec["path"]: spec.get("prior")
        for lane in report["lanes"].values()
        for spec in lane["specs"]
    }
    assert priors == {
        "docs/project/specs/active/same.md": {"action": "retain", "reason": "Live"},
        "docs/project/specs/done/same.md": None,
    }


def test_verify_checks_a_receipt_s_path_repoints(tmp_path: Path) -> None:
    review = {
        "beads": [],
        "receipt": {
            "path_repoints": [
                {"id": "think-a111", "from": "old/a.md", "to": "new/a.md", "status": "open"},
                {"id": "think-b111", "from": "old/b.md", "to": "new/b.md", "status": "open"},
            ]
        },
    }
    later = {"receipt": {"path_repoints": [{"id": "think-a111", "to": "newer/a.md"}]}}
    snapshot = [
        {"id": "think-a111", "status": "open", "spec_path": "newer/a.md"},
        {"id": "think-b111", "status": "open", "spec_path": "wrong/b.md"},
    ]
    result = verify_applied(snapshot, [review, later], tmp_path)
    assert result["checked"] == 2
    assert result["problems"] == ["spec_path not applied: think-b111 has wrong/b.md"]


def test_verify_holds_a_close_to_its_closed_status_and_names_an_empty_receipt_item(
    tmp_path: Path,
) -> None:
    close = {
        "beads": [
            {
                "id": "think-a111",
                "action": "close",
                "updates": {"expected_version": 1, "expected_status": "open"},
            }
        ]
    }
    shown = {"think-a111": {"status": "open", "version": 2}}
    snapshot = [{"id": "think-a111", "status": "open"}]
    assert verify_applied(snapshot, [close], tmp_path, shown)["problems"] == [
        "not closed: think-a111 is open"
    ]
    empty = {"beads": [{"id": "think-a111", "action": "updated", "previous_version": 1}]}
    assert verify_applied(snapshot, [empty], tmp_path)["problems"][0] == (
        "receipt item with no recorded target: think-a111: updated"
    )
