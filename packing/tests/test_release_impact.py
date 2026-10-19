"""The impact gate selects publication inputs and requires fresh owning dispositions."""

# These contracts exercise the validation command's internal step boundary.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
import shlex
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

import pytest
import yaml

from devtools import check_release_impact as gate
from sqpack import release
from sqpack.cli import validate

PAPER = "paper:n11-lower-bounds-explainer"
OTHER = "paper:n11-optimality-review"
PAPERS = tuple(
    component for component in release.COMPONENT_HISTORY_NAMES if component.startswith("paper:")
)


@pytest.mark.parametrize(
    ("environment", "on_main", "expected"),
    [
        ({}, False, ("--baseline-ref", "origin/main")),
        (
            {"PACKING_RELEASE_BASE_REF": "pinned-parent"},
            False,
            ("--baseline-ref", "pinned-parent"),
        ),
        (
            {"GITHUB_BASE_REF": "parent-branch"},
            False,
            ("--baseline-ref", "origin/parent-branch"),
        ),
        (
            {"GITHUB_BASE_REF": "parent-branch", "PACKING_RELEASE_BASE_REF": "local"},
            False,
            ("--baseline-ref", "local"),
        ),
        (
            {
                "GITHUB_BASE_REF": "main",
                "PACKING_RELEASE_BASE_REF": "a87de0cf735af2f84ce3ffaceb6d4d619bc64d80",
            },
            False,
            ("--baseline-ref", "a87de0cf735af2f84ce3ffaceb6d4d619bc64d80"),
        ),
        (
            {"GITHUB_BASE_REF": "main", "PACKING_RELEASE_BASE_REF": ""},
            False,
            ("--baseline-ref", "origin/main"),
        ),
        (
            {"GITHUB_BASE_REF": "parent-branch", "PACKING_RELEASE_BASE_REF": "local"},
            True,
            ("--base", "HEAD^1"),
        ),
    ],
)
def test_synopsis_selects_release_parent_without_moving_changelog_baseline(
    monkeypatch: pytest.MonkeyPatch,
    environment: dict[str, str],
    *,
    on_main: bool,
    expected: tuple[str, str],
) -> None:
    commands: list[Sequence[str]] = []

    def capture(_context: validate.Context, selected: Sequence[Sequence[str]]) -> str:
        commands.extend(selected)
        return "checked"

    monkeypatch.setattr(validate, "_commands", capture)
    monkeypatch.setattr(
        validate,
        "_git",
        lambda *args: "main" if on_main or args[-1] == "origin/main" else "feature",
    )
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=environment
    )
    assert validate._synopsis(context) == "checked"  # noqa: SLF001
    assert tuple(commands[-1]) == (
        sys.executable,
        "-m",
        "devtools.check_release_impact",
        *expected,
    )
    assert tuple(commands[-2]) == (
        sys.executable,
        "-m",
        "devtools.render_changelog",
        "--check",
        "--baseline-ref",
        "origin/main",
    )


def test_hosted_workflow_pins_release_base_to_pull_request_event_commit() -> None:
    workflow = yaml.safe_load(
        (validate.REPOSITORY_ROOT / ".github/workflows/packing-validation.yml").read_text(
            encoding="utf-8"
        )
    )
    assert workflow["env"]["PACKING_RELEASE_BASE_REF"] == (
        "${{ github.event_name == 'pull_request' && github.event.pull_request.base.sha || '' }}"
    )


def test_real_producer_helper_closure_covers_overview_content_without_workflow_tests() -> None:
    inputs = gate.producer_inputs()
    assert "packing/devtools/overview_sections.py" in inputs["site"]
    assert not any("packing/tests/test_changelog.py" in paths for paths in inputs.values())
    assert "packing/devtools/check_n11_optimality_d4.py" in inputs[OTHER]


def test_actual_overview_section_helper_delta_selects_site(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    live_inputs = gate.producer_inputs()
    repo = Repository(tmp_path, monkeypatch)
    monkeypatch.setattr(gate, "producer_inputs", lambda: live_inputs)
    helper = "packing/devtools/overview_sections.py"
    repo.write(helper, "PUBLIC_CONTENT = 'A changed Results legend'\n")
    report = repo.inspect()
    assert helper in report.candidate_paths["site"]
    assert any("site" in error for error in report.errors)


class Repository:
    def __init__(self, root: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)
        self.histories: dict[str, tuple[release.PublicationHistoryEntry, ...]] = {
            component: (
                release.PublicationHistoryEntry("v1.0.0", "October 1, 2026", "Baseline"),
            )
            for component in release.COMPONENT_HISTORY_NAMES
        }
        self.decisions: list[release.ReleaseImpactDecision] = []
        self.no_changes: list[release.ReleaseNoPublicChange] = []
        self.inputs: dict[str, tuple[str, ...]] = {
            component: (
                f"articles/{component.removeprefix('paper:')}.md",
                "shared.css",
                "packing/src/sqpack",
            )
            for component in PAPERS
        }
        self.inputs["site"] = (
            "about.md",
            "shared.css",
            "packing/src/sqpack",
            gate.CHANGELOG_PATH,
        )
        self.inputs["infographics"] = gate.component_outputs()["infographics"]
        monkeypatch.setattr(gate, "producer_inputs", lambda: self.inputs)
        monkeypatch.setattr(
            release, "component_history", lambda component: self.histories[component]
        )
        monkeypatch.setattr(
            release,
            "RELEASE_POLICY_BASELINES",
            dict.fromkeys(self.histories, "v1.0.0"),
        )
        monkeypatch.setattr(release, "RELEASE_IMPACTS", self.decisions)
        self.git("init", "-q")
        self.write_release()
        self.write("about.md", "About the project.\n")
        self.write("shared.css", "body { color: black; }\n")
        self.write(
            gate.CHANGELOG_PATH,
            yaml.safe_dump(
                {"entries": [{"id": "entry", "summary": "Contribution"}], "deliveries": []}
            ),
        )
        for component in PAPERS:
            self.write(self.inputs[component][0], "The original paper body.\n")
        self.write(
            "packing/src/sqpack/helper.py",
            '"""Old docstring."""\ndef helper():\n    return 1\n',
        )
        self.base = self.commit("fixture baseline")
        self.git("update-ref", "refs/remotes/origin/main", self.base)

    def git(self, *args: str) -> str:
        environment = {
            key: value for key, value in os.environ.items() if not key.startswith("GIT_")
        }
        environment.update(
            {
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_SYSTEM": os.devnull,
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_COUNT": "0",
            }
        )
        return subprocess.run(
            [
                "git",
                "-c",
                f"core.hooksPath={os.devnull}",
                "-c",
                "commit.gpgsign=false",
                "-c",
                "core.fsmonitor=false",
                *args,
            ],
            cwd=self.root,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()

    def write(self, path: str, text: str) -> None:
        output = self.root / path
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")

    def write_release(self, *, suffix: str = "") -> None:
        lines = [
            f"{release.COMPONENT_HISTORY_NAMES[component]} = {history!r}"
            for component, history in self.histories.items()
        ]
        lines += [
            f"RELEASE_IMPACTS: tuple = {tuple(self.decisions)!r}",
            f"RELEASE_NO_PUBLIC_CHANGES: tuple = {tuple(self.no_changes)!r}",
            "DATA_REVISION = 'old-pin'",
            "PUBLICATION_REVISION = 'old-publication-pin'",
            "raise RuntimeError('previous source must never execute')",
            suffix,
        ]
        self.write(gate.RELEASE_PATH, "\n".join(lines))

    def commit(self, message: str) -> str:
        self.git("add", ".")
        self.git(
            "-c",
            "user.name=Gate fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            message,
        )
        return self.git("rev-parse", "HEAD")

    def bump(self, component: str) -> None:
        previous = self.histories[component][0].version
        version = release.successor_version(previous, "patch")
        self.histories[component] = (
            release.PublicationHistoryEntry(version, "October 2, 2026", "Correction"),
            *self.histories[component],
        )
        self.decisions.append(
            release.ReleaseImpactDecision(
                component, previous, version, "patch", "A reader-visible correction"
            )
        )
        self.write_release()

    def exempt(
        self,
        components: tuple[str, ...],
        paths: tuple[str, ...],
        reason: str = "Reviewed public outputs remain unchanged",
    ) -> None:
        outputs = tuple(
            output for component in components for output in gate.component_outputs()[component]
        )
        self.no_changes.append(
            release.ReleaseNoPublicChange(components, paths, outputs, reason)
        )
        self.write_release()

    def inspect(self) -> gate.ImpactReport:
        return gate.inspect(repo=self.root)


def test_paper_body_requires_its_own_successor(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    paper_path = repo.inputs[PAPER][0]
    repo.write(paper_path, "A corrected public claim.\n")
    report = repo.inspect()
    assert report.candidate_paths == {PAPER: (paper_path,)}
    assert report.baseline_versions[PAPER] == "v1.0.0"
    assert any(PAPER in error for error in report.errors)
    repo.bump("site")
    assert any(PAPER in error for error in repo.inspect().errors)
    repo.bump(PAPER)
    assert repo.inspect().errors == ()


def test_shared_typography_selects_every_declared_owner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.write("shared.css", "body { color: blue; }\n")
    report = repo.inspect()
    assert set(report.candidate_paths) == {"site", *PAPERS}
    assert len(report.errors) == 1 + len(PAPERS)


def test_fresh_about_only_review_exempts_papers_on_broad_inputs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    helper = "packing/src/sqpack/helper.py"
    repo.write("about.md", "The About page gains a changelog.\n")
    repo.write(helper, "def helper():\n    return 2\n")
    repo.bump("site")
    repo.exempt(
        PAPERS,
        (helper,),
        "Compared all paper HTML, Markdown and PDF editions; the helper only changes About",
    )
    report = repo.inspect()
    assert set(report.exempt_components) == set(PAPERS)
    assert report.errors == ()


def test_old_and_incomplete_reviews_do_not_excuse_new_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    paper_path = repo.inputs[PAPER][0]
    repo.exempt((PAPER,), (paper_path,))
    baseline = repo.commit("prior no-public-change review")
    repo.git("update-ref", "refs/remotes/origin/main", baseline)
    repo.write(paper_path, "A new paper-body delta after the old review.\n")
    assert any(PAPER in error for error in repo.inspect().errors)
    repo.no_changes.clear()
    repo.exempt((PAPER,), (paper_path,), "Fresh review of this body's output")
    repo.write("shared.css", "body { color: blue; }\n")
    report = repo.inspect()
    assert PAPER not in report.exempt_components
    assert any(PAPER in error for error in report.errors)


def test_pins_comments_audit_metadata_and_tests_create_no_obligation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.write_release(
        suffix="# A pipeline comment.\nDATA_REVISION = 'new-pin'\n"
        "PUBLICATION_REVISION = 'new-pin'\n"
    )
    repo.write(
        "packing/src/sqpack/helper.py",
        '"""Reworded docstring."""\n# New comment\ndef helper():\n    return 1\n',
    )
    repo.write(
        gate.CHANGELOG_PATH,
        yaml.safe_dump(
            {
                "entries": [{"id": "entry", "summary": "Contribution"}],
                "deliveries": [{"number": 600}],
                "frozen_entries": [],
                "coverage": {"omissions": []},
            }
        ),
    )
    repo.write("packing/tests/test_new_gate.py", "def test_new():\n    assert 1 == 1\n")
    report = repo.inspect()
    assert report.candidate_paths == {}
    assert report.errors == ()


def test_deletions_renames_staged_and_relevant_untracked_paths_are_seen(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    old = repo.inputs[PAPER][0]
    new = "articles/renamed.md"
    repo.git("mv", old, new)
    repo.write("packing/src/sqpack/new_helper.py", "VALUE = 2\n")
    repo.write(repo.inputs[OTHER][0], "An unstaged paper change.\n")
    paths = gate.changed_paths(repo.root, repo.base)
    assert old in paths
    assert new in paths
    assert "packing/src/sqpack/new_helper.py" in paths
    report = repo.inspect()
    assert old in report.candidate_paths[PAPER]
    assert repo.inputs[OTHER][0] in report.candidate_paths[OTHER]
    assert "packing/src/sqpack/new_helper.py" in report.candidate_paths[PAPER]
    with pytest.raises(ValueError, match="git rev-parse failed"):
        gate.inspect(repo=repo.root, baseline_ref="missing-reference")


def test_merge_base_excludes_unrelated_upstream_changes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.git("checkout", "-qb", "fixture-feature")
    repo.write(repo.inputs[PAPER][0], "A committed feature paper change.\n")
    feature = repo.commit("feature change")
    repo.git("checkout", "--detach", repo.base)
    repo.write(repo.inputs[OTHER][0], "An upstream change absent from the feature branch.\n")
    upstream = repo.commit("upstream change")
    repo.git("update-ref", "refs/remotes/origin/main", upstream)
    repo.git("checkout", "--detach", feature)
    report = repo.inspect()
    assert report.baseline == repo.base
    assert set(report.candidate_paths) == {PAPER}


def test_dependent_base_requires_own_successor_and_keeps_uncovered_input_red(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.write("about.md", "A parent-layer public correction.\n")
    repo.bump("site")
    parent = repo.commit("parent site successor")
    repo.git("update-ref", "refs/remotes/origin/parent", parent)
    repo.write("about.md", "The parent correction and this layer's public correction.\n")
    repo.bump("site")
    repo.commit("own site successor")

    # Main sees two cuts; this layer must still own the immediate parent-to-child cut.
    assert any("site" in error for error in repo.inspect().errors)
    own = gate.inspect(repo=repo.root, baseline_ref="origin/parent")
    assert own.baseline == parent
    assert own.baseline_versions["site"] == "v1.0.1"
    assert own.errors == ()

    paper_path = repo.inputs[PAPER][0]
    repo.write(paper_path, "An uncovered public paper change in this layer.\n")
    uncovered = gate.inspect(repo=repo.root, baseline_ref="origin/parent")
    assert paper_path in uncovered.candidate_paths[PAPER]
    assert any(PAPER in error for error in uncovered.errors)


def test_atomic_delivery_accepts_complete_fresh_adjacent_cuts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.git("checkout", "-qb", "fixture-stack")
    for layer in ("first", "second"):
        repo.write("about.md", f"The {layer} layer's public correction.\n")
        repo.bump("site")
        repo.commit(f"{layer} layer")
    repo.git("checkout", "-qb", "fixture-main", repo.base)
    repo.git(
        "-c",
        "user.name=Gate fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "merge",
        "--no-ff",
        "-qm",
        "atomic stack delivery",
        "fixture-stack",
    )

    report = gate.inspect(repo=repo.root, base="HEAD^1")
    assert report.baseline == repo.base
    assert report.baseline_versions["site"] == "v1.0.0"
    assert report.errors == ()


@pytest.mark.parametrize(
    ("damage", "expected"),
    [
        ("missing-first", "site: candidate public inputs"),
        ("missing-last", "site: candidate public inputs"),
        ("arithmetic", "requires its minor successor v1.1.0"),
        ("backward", "requires its patch successor v1.0.2"),
        ("lost-baseline", "site: delivery baseline has no retained edition"),
        ("unchanged-edition", "site: candidate public inputs"),
    ],
)
def test_delivery_rejects_incomplete_or_invalid_retained_chains(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, damage: str, expected: str
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.write("about.md", "Two public corrections in one delivery.\n")
    repo.bump("site")
    repo.bump("site")
    if damage == "missing-first":
        repo.decisions.pop(0)
    elif damage == "missing-last":
        repo.decisions.pop()
    elif damage == "arithmetic":
        repo.decisions[-1] = repo.decisions[-1]._replace(impact="minor")
    elif damage == "backward":
        repo.histories["site"] = (
            repo.histories["site"][0]._replace(version="v0.9.0"),
            *repo.histories["site"][1:],
        )
        repo.decisions[-1] = repo.decisions[-1]._replace(version="v0.9.0")
    elif damage == "lost-baseline":
        repo.histories["site"] = repo.histories["site"][:-1]
    else:
        repo.histories["site"] = repo.histories["site"][-1:]
        repo.decisions.clear()
    repo.write_release()

    report = gate.inspect(repo=repo.root, base=repo.base)
    assert any(expected in error for error in report.errors)


def test_delivery_cannot_reuse_a_decision_already_present_at_its_baseline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.bump("site")
    repo.bump("site")
    repo.histories["site"] = repo.histories["site"][-1:]
    repo.write_release()
    baseline = repo.commit("predeclared decisions without their editions or changes")
    repo.decisions.clear()
    repo.write("about.md", "The later public corrections need fresh decisions.\n")
    repo.bump("site")
    repo.bump("site")

    report = gate.inspect(repo=repo.root, base=baseline)
    assert any("site: candidate public inputs" in error for error in report.errors)


def test_retained_composite_export_has_only_its_infographic_owner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    export = gate.component_outputs()["infographics"][0]
    repo.write(export, "An updated retained export.\n")
    report = repo.inspect()
    assert report.candidate_paths == {"infographics": (export,)}
    assert any("infographics" in error for error in report.errors)


def test_visible_release_dates_and_status_select_the_owning_component(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.write_release(suffix="EXPLAINER_REVISED = 'October 2, 2026'\n")
    report = repo.inspect()
    assert report.candidate_paths == {PAPER: (gate.RELEASE_PATH,)}
    assert any(PAPER in error for error in report.errors)
    repo.write_release(suffix="PUBLICATION_STATUS = 'Draft'\n")
    report = repo.inspect()
    assert report.candidate_paths == {"site": (gate.RELEASE_PATH,)}
    assert any("site" in error for error in report.errors)


def test_no_change_review_requires_outputs_owned_by_each_claimed_component(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    path = repo.inputs[PAPER][0]
    repo.write(path, "A candidate paper-body change.\n")
    repo.no_changes.append(
        release.ReleaseNoPublicChange(
            (PAPER,), (path,), ("about.html",), "Reviewed the wrong component's output"
        )
    )
    repo.write_release()
    report = repo.inspect()
    assert PAPER not in report.exempt_components
    assert any("recognized examined outputs" in error for error in report.errors)


@pytest.mark.parametrize(
    ("field", "owner"),
    [
        ("OPTIMALITY_PROOF_PUBLISHED", OTHER),
        ("THRESHOLD_PROOF_PUBLISHED", "paper:n11-threshold-bound-review"),
        ("PUBLICATION_EDITION", "site"),
        ("INFOGRAPHIC_EDITION", "infographics"),
    ],
)
def test_every_published_release_date_and_edition_expression_selects_its_owner(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    field: str,
    owner: str,
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.write_release(suffix=f"{field} = 'A changed published value'\n")
    report = repo.inspect()
    assert report.candidate_paths == {owner: (gate.RELEASE_PATH,)}
    assert any(owner in error for error in report.errors)


def test_release_edition_implementation_changes_select_every_owner_including_infographics(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = Repository(tmp_path, monkeypatch)
    repo.write_release(suffix='def edition_at(revision):\n    return "Edition " + revision\n')
    report = repo.inspect()
    assert set(report.candidate_paths) == {"site", "infographics", *PAPERS}
    assert all(paths == (gate.RELEASE_PATH,) for paths in report.candidate_paths.values())
    assert len(report.errors) == len(report.candidate_paths)


def test_disposable_git_fixtures_ignore_inherited_repository_and_hook_configuration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    sentinel = Repository(tmp_path / "sentinel", monkeypatch)
    sentinel.write("sentinel-only.txt", "Preserve this repository.\n")
    sentinel_head = sentinel.commit("sentinel state")
    marker = tmp_path / "inherited-hook-ran"
    hooks = tmp_path / "inherited-hooks"
    hooks.mkdir()
    hook = hooks / "pre-commit"
    hook.write_text("#!/bin/sh\nprintf ran > " + shlex.quote(str(marker)) + "\n")
    hook.chmod(0o755)
    configuration = tmp_path / "inherited-git-config"
    sentinel.git("config", "--file", str(configuration), "core.hooksPath", str(hooks))
    monkeypatch.setenv("GIT_DIR", str(sentinel.root / ".git"))
    monkeypatch.setenv("GIT_WORK_TREE", str(sentinel.root))
    monkeypatch.setenv("GIT_INDEX_FILE", str(sentinel.root / ".git/index"))
    monkeypatch.setenv("GIT_OBJECT_DIRECTORY", str(sentinel.root / ".git/objects"))
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(configuration))
    monkeypatch.setenv("GIT_CONFIG_SYSTEM", str(configuration))
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.hooksPath")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", str(hooks))
    monkeypatch.setenv("GIT_TEMPLATE_DIR", str(hooks))
    before = {
        path.relative_to(sentinel.root).as_posix(): path.read_bytes()
        for path in sentinel.root.rglob("*")
        if path.is_file()
    }
    isolated = Repository(tmp_path / "isolated", monkeypatch)
    assert (isolated.root / ".git").is_dir()
    assert isolated.git("rev-parse", "HEAD") == isolated.base
    assert sentinel.git("rev-parse", "HEAD") == sentinel_head
    assert not marker.exists()
    after = {
        path.relative_to(sentinel.root).as_posix(): path.read_bytes()
        for path in sentinel.root.rglob("*")
        if path.is_file()
    }
    assert after == before


#: A runbook with the News label rubric among its process text, as
#: `packing/campaign/result-import.md` carries it.
RUBRIC = (
    "# Runbook\n\nIntake process.\n\n### Label the PR and Prepare News\n\n"
    "| Label | Delivered contribution | Short | Examples |\n| --- | --- | --- | --- |\n"
    + "".join(
        f"| `S{n}` | Contribution {n} | Meaning {n} | Example {n} |\n" for n in range(1, 6)
    )
    + "\nScore conservatively.\n\n## The Next Stage\n\nMore process.\n"
)


def test_only_the_news_rubric_rows_of_the_intake_runbook_are_a_site_candidate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The site reads one thing from the intake runbook, each S label's `Short` meaning
    (`render_changelog.news_rubric_meanings`), so a process edit anywhere else in it,
    the rubric's other columns included, owes the site no release decision; an edit to a
    `Short` meaning does, and so does a rubric the site can no longer read."""
    repo = Repository(tmp_path, monkeypatch)
    repo.inputs["site"] = (*repo.inputs["site"], gate.NEWS_RUBRIC_PATH)
    repo.write(gate.NEWS_RUBRIC_PATH, RUBRIC)
    repo.base = repo.commit("rubric baseline")
    repo.git("update-ref", "refs/remotes/origin/main", repo.base)

    repo.write(
        gate.NEWS_RUBRIC_PATH,
        RUBRIC.replace("More process.", "Reworded process.")
        .replace("Contribution 3", "A reworded anchor")
        .replace("Score conservatively.", "Score every PR conservatively."),
    )
    report = repo.inspect()
    assert report.candidate_paths == {}
    assert report.errors == ()

    repo.write(gate.NEWS_RUBRIC_PATH, RUBRIC.replace("Meaning 4", "A new short meaning"))
    report = repo.inspect()
    assert set(report.candidate_paths["site"]) == {gate.NEWS_RUBRIC_PATH}
    assert any("site" in error for error in report.errors)

    without_short = "".join(
        line.replace(" Short |", "").replace(" --- | --- | --- | --- |", " --- | --- | --- |")
        for line in RUBRIC.splitlines(keepends=True)
        if not line.startswith("| `S")
    ) + "".join(f"| `S{n}` | Contribution {n} | Example {n} |\n" for n in range(1, 6))
    repo.write(gate.NEWS_RUBRIC_PATH, without_short)
    report = repo.inspect()
    assert set(report.candidate_paths["site"]) == {gate.NEWS_RUBRIC_PATH}


def test_a_second_unit_declaring_the_intake_runbook_compares_its_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The rubric comparison holds for the site alone. Once another unit declares the
    runbook too, nothing says what that unit reads of it, so a process edit outside the
    rubric is a candidate for every owner, the site included."""
    repo = Repository(tmp_path, monkeypatch)
    repo.inputs["site"] = (*repo.inputs["site"], gate.NEWS_RUBRIC_PATH)
    repo.inputs[PAPER] = (*repo.inputs[PAPER], gate.NEWS_RUBRIC_PATH)
    repo.write(gate.NEWS_RUBRIC_PATH, RUBRIC)
    repo.base = repo.commit("rubric baseline")
    repo.git("update-ref", "refs/remotes/origin/main", repo.base)
    repo.write(gate.NEWS_RUBRIC_PATH, RUBRIC.replace("More process.", "Reworded process."))
    report = repo.inspect()
    assert report.candidate_paths == {
        PAPER: (gate.NEWS_RUBRIC_PATH,),
        "site": (gate.NEWS_RUBRIC_PATH,),
    }
