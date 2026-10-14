"""A site version bump is one command: it names the edition, redraws, checks, and stops.

The bump is when the large generated assets are rebuilt (the owner, 2026-10-01). What is
pinned here is the one edit the command makes by hand -- a new edition at the front of
`release.py`'s site history, written as the formatter leaves one, with no paper's own
history or version moved -- its refusals, that it changes nothing until the tree is clean
and the pin is current, and that what it leaves to the owner ends at the deployment
check, with no tag and no GitHub release. The redraw and the checks it then runs are
other modules' commands, with tests of their own.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from devtools import build_known_best_atlas, cut_release, release_pin
from sqpack import release

PACKING = Path(__file__).resolve().parents[1]
SOURCE = release_pin.RELEASE.read_text(encoding="utf-8")
LONG = (
    "The atlas edition: the posters state the data they were drawn from, the site's "
    "pages carry one footer, and $s(11) = 3.8770835…$ is recorded as proved optimal."
)


def _module(text: str) -> dict[str, object]:
    namespace: dict[str, object] = {"__name__": "scratch_release"}
    exec(compile(text, "release.py", "exec"), namespace)
    return namespace


def _next() -> str:
    return release.successor_version(release.PUBLICATION_VERSION, "patch")


@pytest.mark.parametrize("scope", [LONG, "A short edition."])
def test_a_bump_adds_the_edition_at_the_front_and_moves_nothing_else(scope: str) -> None:
    """One entry more, newest first; the claim documents' revision; the data pin untouched."""
    version = _next()
    bumped = cut_release.with_edition(
        SOURCE,
        version=version,
        first_published="October 2, 2026",
        scope=scope,
        revision="0123abcd",
    )
    module = _module(bumped)
    history = module["PUBLICATION_HISTORY"]
    assert isinstance(history, tuple)
    assert len(history) == len(release.PUBLICATION_HISTORY) + 1
    assert tuple(history[0]) == (version, "October 2, 2026", scope)
    assert [tuple(entry) for entry in history[1:]] == [
        tuple(entry) for entry in release.PUBLICATION_HISTORY
    ]
    assert module["PUBLICATION_VERSION"] == version
    assert module["PUBLICATION_DATE"] == "October 2, 2026"
    assert module["FIRST_PUBLISHED"] == release.FIRST_PUBLISHED
    assert module["PUBLICATION_REVISION"] == "0123abcd"
    assert module["DATA_REVISION"] == release.DATA_REVISION
    assert module["PUBLICATION_EDITION"] == (
        f"{version}-{release.DATA_REVISION[: release.DATA_REVISION_LENGTH]}"
    )
    # A site bump moves no paper: each paper's own history and version stay as they are.
    assert module["EXPLAINER_HISTORY"] == release.EXPLAINER_HISTORY
    assert module["EXPLAINER_VERSION"] == release.EXPLAINER_VERSION
    assert module["OPTIMALITY_REVIEW_EDITION"] == release.OPTIMALITY_REVIEW_EDITION
    assert module["INFOGRAPHIC_HISTORY"] == release.INFOGRAPHIC_HISTORY
    assert module["INFOGRAPHIC_VERSION"] == release.INFOGRAPHIC_VERSION
    assert module["THRESHOLD_REVIEW_HISTORY"] == release.THRESHOLD_REVIEW_HISTORY
    assert module["PACKING_METHODS_HISTORY"] == release.PACKING_METHODS_HISTORY
    validate = module["validate_release_impacts"]
    assert callable(validate)
    validate(externally_changed=["site"])

    # The lint floor formats every tracked Python file, so the edit has to be written
    # the way the formatter writes it, or a bump would fail the gate on its own output.
    formatted = subprocess.run(
        (sys.executable, "-m", "ruff", "format", "--check", "--stdin-filename", "release.py"),
        input=bumped,
        capture_output=True,
        text=True,
        cwd=PACKING,
        check=False,
    )
    assert formatted.returncode == 0, formatted.stdout + formatted.stderr


@pytest.mark.parametrize(
    ("change", "refusal"),
    [
        ({"version": release.PUBLICATION_VERSION}, "is not after the current edition"),
        ({"version": "v0.1.0"}, "is not after the current edition"),
        ({"version": "0.5.0"}, "is not a version"),
        ({"version": "v0.5"}, "is not a version"),
        ({"first_published": "2026-10-02"}, "does not match format"),
        ({"scope": "No full stop"}, "one trimmed sentence"),
        ({"scope": " Padded. "}, "one trimmed sentence"),
        ({"scope": "Two\nlines."}, "one trimmed sentence"),
        ({"revision": "HEAD"}, "is not a commit"),
    ],
)
def test_a_bump_that_is_not_one_is_refused(change: dict[str, str], refusal: str) -> None:
    arguments = {
        "version": _next(),
        "first_published": "October 2, 2026",
        "scope": "A short edition.",
        "revision": "0123abcd",
    } | change
    with pytest.raises(ValueError, match=refusal):
        cut_release.with_edition(
            SOURCE,
            version=arguments["version"],
            first_published=arguments["first_published"],
            scope=arguments["scope"],
            revision=arguments["revision"],
        )


def test_component_steps_generate_only_owned_outputs() -> None:
    site_plan = cut_release.steps("v9.9.9")
    assert [command[0] for _what, command in site_plan] == [
        "devtools.render_verifiable_claim",
        "pytest",
    ]
    plan = cut_release.steps("v9.9.9", "infographics")
    atlas_steps = [command for _what, command in plan if command[0].endswith("atlas")]
    assert [command[1:] for command in atlas_steps] == [
        ("--update-composites",),
        ("--check-composites",),
    ]
    for command in atlas_steps:
        build_known_best_atlas.parser().parse_args(list(command[1:]))
    assert all((PACKING / test).is_file() for test in cut_release.TESTS)
    paper_plan = cut_release.steps("v0.1.8", "paper:n11-optimality-review")
    assert paper_plan[0][1] == ("devtools.render_n11_optimality_review", "--pdf")


def test_a_dry_run_prints_the_plan_and_changes_nothing(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The whole plan, and what is left for the owner, without touching the tree."""
    answers = {("rev-parse", "--short=8", "HEAD"): "0123abcd", ("status", "--porcelain"): ""}
    monkeypatch.setattr(cut_release, "_git", lambda *arguments: answers[arguments])
    monkeypatch.setattr(release_pin, "check", lambda _repo, _source: 0)
    version = _next()
    status = cut_release.main(
        [
            version,
            "--impact",
            "patch",
            "--scope",
            "A short edition.",
            "--date",
            "October 2, 2026",
            "--dry-run",
        ]
    )
    printed = capsys.readouterr().out
    assert status == 0
    assert f"{release.PUBLICATION_VERSION} -> {version}, first published October 2, 2026" in (
        printed
    )
    assert "python -m devtools.build_known_best_atlas --update-composites" not in printed
    assert "dry run: nothing was changed" in printed
    # A site bump ends at the deployment check. No tag and no GitHub release are
    # routine (the owner, 2026-10-01: releases matter only for the generated assets
    # that need a download address, the films), and no paper's version moves.
    assert f"The site version {version} is complete when that passes" in printed
    assert "git tag" not in printed
    assert "gh release create" not in printed
    assert "A release is cut only to host generated" in printed
    assert "render_overview.FILM_RELEASE" in printed
    assert "Other components keep their own editions" in printed
    assert release_pin.RELEASE.read_text(encoding="utf-8") == SOURCE


@pytest.mark.parametrize(
    ("dirty", "pin", "refusal"),
    [
        (" M packing/frontier/n-017.md", 0, "the working tree is not clean"),
        ("", 1, "the pinned data revision is stale"),
    ],
)
def test_a_bump_starts_only_from_a_clean_tree_and_a_current_pin(
    dirty: str,
    pin: int,
    refusal: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A poster drawn over uncommitted data, or under a stale pin, would be stamped wrong."""
    answers = {("rev-parse", "--short=8", "HEAD"): "0123abcd", ("status", "--porcelain"): dirty}
    monkeypatch.setattr(cut_release, "_git", lambda *arguments: answers[arguments])
    monkeypatch.setattr(release_pin, "check", lambda _repo, _source: pin)
    assert cut_release.main([_next(), "--impact", "patch", "--scope", "A short edition."]) == 1
    assert refusal in capsys.readouterr().err
    assert release_pin.RELEASE.read_text(encoding="utf-8") == SOURCE


@pytest.mark.parametrize(
    ("component", "impact"),
    [("infographics", "patch"), ("paper:n11-optimality-review", "minor")],
)
def test_component_cut_preserves_all_other_histories_and_records_its_impact(
    component: str,
    impact: release.ReleaseImpact,
) -> None:
    version = release.successor_version(release.component_version(component), impact)
    bumped = cut_release.with_edition(
        SOURCE,
        version=version,
        first_published="October 13, 2026",
        scope="Change the delivered component.",
        revision="0123abcd",
        component=component,
        impact=impact,
    )
    module = _module(bumped)
    for owner, name in release.COMPONENT_HISTORY_NAMES.items():
        history = module[name]
        assert isinstance(history, tuple)
        if owner == component:
            assert history[0].version == version
            assert tuple(history[1:]) == release.component_history(owner)
        else:
            assert history == release.component_history(owner)
    assert module["PUBLICATION_REVISION"] == release.PUBLICATION_REVISION
    assert module["OPTIMALITY_REVIEW_STATUS"] == "Draft"
    assert module["THRESHOLD_REVIEW_STATUS"] == "Draft"
    validate = module["validate_release_impacts"]
    assert callable(validate)
    validate(externally_changed=[component])


@pytest.mark.parametrize(
    ("version", "impact"),
    [
        (release.successor_version(release.INFOGRAPHIC_VERSION, "patch"), "minor"),
        (release.successor_version(release.INFOGRAPHIC_VERSION, "minor"), "patch"),
        (
            release.successor_version(
                release.successor_version(release.INFOGRAPHIC_VERSION, "minor"), "minor"
            ),
            "minor",
        ),
    ],
)
def test_a_cut_refuses_skipped_or_wrong_impact_successors(
    version: str, impact: release.ReleaseImpact
) -> None:
    with pytest.raises(ValueError, match="requires successor"):
        cut_release.with_edition(
            SOURCE,
            version=version,
            first_published="October 13, 2026",
            scope="Change the delivered component.",
            revision="0123abcd",
            impact=impact,
            component="infographics",
        )
