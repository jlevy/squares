"""Change-scoped gate selection, and the two ways it must refuse to under-select.

`BC-084`. `D-355` measured a two-file edit to the rigidity assessor verified by a 979.79s
full gate whose two reachable steps run together in 12.06s. Selecting fewer steps is only
admissible when the unselected ones provably cannot fail on the change, so the design is
conservative on both sides and these assertions are where that is held:

- a changed path no step claims selects the **whole gate**, never the steps that happened
  to match, because a partial answer derived from an admittedly incomplete map is worse
  than no answer;
- a step that declares nothing is claimed by everything.

The one failure that costs coverage is a pattern set too narrow for its step, and nothing
but `test_every_step_is_reachable_from_a_declared_pattern` stands between a mistyped glob
and a check that silently stops running.
"""

from __future__ import annotations

from sqpack.cli.validate import STEPS, Step, select_for_paths

# One representative path per source region. Every step must be selected by at least one
# of these; a step selected by none has a pattern set that matches nothing real, which is
# indistinguishable from having been switched off.
PATTERN_PROBES = (
    "packing/src/sqpack/verify.py",
    "packing/src/sqpack/research/canonical.py",
    "packing/sqsearch/src/main.rs",
    "packing/cases/small_n/optimal_moduli.py",
    "packing/devtools/render_defects.py",
    "packing/devtools/assess_frontier_rigidity.py",
    "packing/devtools/build_n5_identity_pair.py",
    "packing/devtools/render_agenda_map.py",
    "packing/devtools/render_packing_svg.py",
    "packing/devtools/check_soundness_perimeter.py",
    "packing/devtools/render_research_tables.py",
    "packing/tests/test_verify.py",
    "packing/campaign/agendas/agenda-008-x.md",
    "packing/campaign/schemas/agenda.schema.yaml",
    "packing/campaign/series/series-000-smoke-and-calibration/results/bc-083-n5-identity-pair.json",
    "packing/frontier/STATUS.md",
    "packing/atlas/n-003-optimal-moduli.svg",
    "packing/defects.yaml",
    "packing/pyproject.toml",
    "AGENTS.md",
    "operating-rules.md",
    "defects.md",
    "SYNOPSIS.md",
    "Makefile",
    ".claude/skills/experiment-loop/SKILL.md",
    "packing/witnesses/known-best/n-011.yaml",
    "packing/golden/basin-maps.yaml",
    "packing/atlas/known-best/manifest.json",
    "packing/atlas/prospective/manifest.json",
    "packing/atlas/enumerated/contact-scaffolds-size5.json",
    "packing/cases/trump11/packing.py",
    "packing/cases/stromquist/printed_cover.py",
    "packing/resources/papers/kingbird-square-29-provenance.svg",
    "docs/project/research/research-2026-08-22-packing-11-unit-squares.md",
    ".tbd/config.yml",
)


def test_every_step_is_reachable_from_a_declared_pattern() -> None:
    """No step may be unreachable from every probe.

    An attributed step whose patterns match nothing that exists has been switched off
    without anyone deciding to switch it off, and the gate would keep reporting green.
    """
    unreachable = [
        step.name
        for step in STEPS
        if not any(step.reachable_from(path) for path in PATTERN_PROBES)
    ]
    assert unreachable == [], (
        f"these steps match no probe path and would never be selected: {unreachable}"
    )


def test_an_unclaimed_path_selects_the_whole_gate() -> None:
    """The escape hatch, which is the whole soundness argument.

    A path nobody attributed means the map is incomplete for this change. Returning the
    steps that happened to match would be an answer computed from a map known to be
    wrong, so the only safe answer is everything.
    """
    selection = select_for_paths(["packing/some/file/nobody/attributed.xyz"])
    assert selection.is_whole_gate
    assert selection.unattributed_paths == ("packing/some/file/nobody/attributed.xyz",)


def test_one_unclaimed_path_poisons_an_otherwise_narrow_selection() -> None:
    """Not "mostly attributed, so mostly narrow" -- one unknown path widens everything.

    This is the case a plausible implementation gets wrong: it is tempting to union the
    matched steps and treat the unknown path as contributing nothing.
    """
    narrow = select_for_paths(["packing/devtools/assess_frontier_rigidity.py"])
    assert not narrow.is_whole_gate

    poisoned = select_for_paths(
        ["packing/devtools/assess_frontier_rigidity.py", "some/unknown/thing.xyz"]
    )
    assert poisoned.is_whole_gate
    assert len(poisoned.steps) > len(narrow.steps)


def test_no_paths_is_not_nothing_changed() -> None:
    """An empty path list means "nothing was determined", not "nothing changed"."""
    assert select_for_paths([]).is_whole_gate


def test_an_unattributed_step_is_selected_by_everything() -> None:
    """The safe default: forgetting to attribute a step costs time, never coverage."""
    unattributed = Step("synthetic", lambda _c: "")
    claimed = Step("claimed", lambda _c: "", touches=("packing/frontier/*",))
    universe = (unattributed, claimed)

    selection = select_for_paths(["packing/frontier/STATUS.md"], universe)
    assert {step.name for step in selection.steps} == {"synthetic", "claimed"}


def test_a_narrow_change_does_not_select_the_whole_gate() -> None:
    """The point of the feature, stated as a measurement rather than a hope.

    `D-355`'s case: an edit to the rigidity assessor alone. It must reach the frontier
    steps and the Python floors, and must not reach steps that provably cannot see that
    file -- here the Rust ones, which read only `packing/sqsearch/`.

    It does still reach every unattributed step, and most steps are unattributed today.
    That is the safe direction and not a defect, but it does mean this test measures the
    mechanism rather than the saving; the saving grows as attribution does.
    """
    selection = select_for_paths(["packing/devtools/assess_frontier_rigidity.py"])
    assert not selection.is_whole_gate
    names = {step.name for step in selection.steps}
    assert "frontier rigidity assessed here" in names
    assert "lint floor (ruff)" in names
    # `frontier corpus` runs `cases.kingbird29.verify_svg`, not the assessor, so it is
    # correctly excluded -- attribution is per step's actual inputs, not per topic. It
    # first claimed `check_source_coverage.py`, which a different step runs; that was an
    # under-selection and is fixed.
    assert "frontier corpus" not in names
    assert "lint floor (rust)" not in names
    assert "search engine (sqsearch)" not in names


def test_a_markdown_only_change_skips_the_python_floors() -> None:
    """The cheapest real win, and the one that shows attribution is doing work.

    Editing only prose cannot change what `ruff` or `basedpyright` say, so neither should
    run. If this ever fails, either a floor gained a Markdown input or its patterns drifted.
    """
    selection = select_for_paths(["operating-rules.md", "AGENTS.md"])
    names = {step.name for step in selection.steps}
    assert "lint floor (ruff)" not in names
    assert "type floor (basedpyright)" not in names
    assert "AGENTS.md mirrors the operating rules" in names


def test_results_register_runs_for_its_open_ended_path_dependencies() -> None:
    for path in (
        "packing/cases/stromquist/repaired_cover.py",
        "packing/tests/test_falsify.py",
        "packing/witnesses/known-best/n-011.yaml",
        "packing/resources/papers/bentz-2010-optimal-packings-13-and-46.md",
        "docs/project/document-map.yaml",
    ):
        names = {step.name for step in select_for_paths([path]).steps}
        assert "results rungs are earned and the view agrees" in names


def test_the_five_under_selections_an_adversarial_review_found() -> None:
    """Each of these was a real hole: a file that changes a step's verdict, unclaimed.

    They matter more than they look, because `*.py` and `*.md` cross separators and so
    claim every Python and Markdown file in the repository. No change to either extension
    can reach the whole-gate escape, which leaves each narrow step's own patterns as the
    only thing standing between an edit and a check that does not run.
    """
    cases = {
        # check_svg_rendering pins examples in TUTORIAL.md and walks REPO.rglob("*.md").
        "TUTORIAL.md": "deterministic SVG rendering",
        # render_research_tables diffs the n=11 report cell by cell.
        "docs/project/research/research-2026-08-22-packing-11-unit-squares.md": (
            "generated tables in sync with frontier/"
        ),
        # assess_frontier_rigidity derives its verdict from this screen.
        "packing/atlas/known-best/translation-escape-screen.json": (
            "frontier rigidity assessed here"
        ),
        # _frontier_corpus runs cases.kingbird29.verify_svg.
        "packing/cases/kingbird29/verify_svg.py": "frontier corpus",
        # Both registry renderers parse through sqpack.yamlio.
        "packing/src/sqpack/yamlio.py": "defect log",
    }
    for path, step_name in cases.items():
        names = {step.name for step in select_for_paths([path]).steps}
        assert step_name in names, f"changing {path} must select {step_name!r}"


def test_a_narrowed_tier_reports_its_own_universe() -> None:
    """`--since` narrows whatever tier preceded it, so "everything" is that tier.

    Comparing against the full step list made a whole-tier selection report itself as a
    partial one, which is the wrong way round for a field a reader uses to decide whether
    anything was skipped.
    """
    fast = [step for step in STEPS if step.fast]
    selection = select_for_paths(["nobody/claims/this.xyz"], fast)
    assert selection.is_whole_gate
    assert len(selection.steps) == len(fast)


def test_an_explicitly_empty_universe_is_not_the_whole_gate() -> None:
    """An empty list passed on purpose meant "all steps", which reads backwards."""
    assert select_for_paths(["packing/frontier/STATUS.md"], []).steps == ()
