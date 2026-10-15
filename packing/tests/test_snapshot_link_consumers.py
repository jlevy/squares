"""A pruned file returns to a worker only for a reader a registered control runs there.

The copy-back follows the links a registered control resolves inside a worker -- the
campaign record's, `README.md`'s and `SYNOPSIS.md`'s -- and the paths the record declares
structurally: the results register's evidence and each defect's `recorded_in`. Every
other document's links are prose for a reader outside the worker (think-b6ir).
"""

import re
import subprocess
from pathlib import Path

import pytest

from cases.kingbird29 import layout as kingbird_layout
from devtools import check_gate_budgets, check_readme, check_results, check_synopsis
from devtools import run_negative_controls as controls
from devtools.check_pr_wall import load_walls
from sqpack.campaign import ledger
from sqpack.yamlio import safe_load
from tests.test_negative_controls import index_fixture_source


def test_fragment_links_rescue_their_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`[proof](review.md#section)` needs `review.md` as much as a bare link does."""
    repo = tmp_path / "source"
    packing = repo / "packing"
    archive = packing / "resources"
    review = archive / "original_review/review.md"
    review.parent.mkdir(parents=True)
    review.write_text("# Seven rows close the support\n")
    bundle = archive / "bundle"
    bundle.mkdir()
    (bundle / "certificate.json").write_bytes(b"deciding scientific input")
    campaign = packing / "campaign/X-001-cover.md"
    campaign.parent.mkdir()
    campaign.write_text(
        "[support proof](../resources/original_review/review.md#seven-rows-close-the-support)\n"
        "[bundle](../resources/bundle#readme)\n"
        "[this document](#cover)\n"
    )
    register = packing / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text("results: []\n")
    monkeypatch.setattr(controls, "REPO", repo)
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset({archive}))
    monkeypatch.setattr(controls, "DESCEND", frozenset())
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (archive,))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", ())
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())
    monkeypatch.setattr(controls, "root_files", lambda: ())

    assert controls.INLINE_LINK.findall(campaign.read_text()) == [
        "../resources/original_review/review.md",
        "../resources/bundle",
    ]
    assert controls.snapshot_pruned_targets() == [review]
    assert controls.linked_pruned_directories() == [bundle]
    index_fixture_source(repo)
    tree = tmp_path / "worker"
    controls.clone_tree(tree)
    assert (tree / review.relative_to(repo)).read_bytes() == review.read_bytes()
    assert (tree / bundle.relative_to(repo)).is_dir()


@pytest.mark.parametrize(
    ("checked", "pattern"),
    [
        ("campaign", ledger.LINK_TARGET),
        ("README.md", check_synopsis.LINK_TARGET),
        ("SYNOPSIS.md", check_synopsis.LINK_TARGET),
    ],
)
def test_every_pruned_target_a_link_checker_resolves_reaches_a_worker(
    checked: str, pattern: re.Pattern[str]
) -> None:
    """The copier reads each checked document's links the way its checker does.

    `ledger check` resolves campaign links and `check_links` resolves README's and
    SYNOPSIS's, each by the path before any `#`, and each with its own pattern, imported
    here rather than copied. A target under a pruned root that the copier misses is a
    dead link in every worker, and the controls that drive the checker (35 for the
    ledger, 12 for `check_synopsis`, 4 for `check_readme`) would report it in place of
    the refusal each rehearses. The original n11 review was that case, linked from
    campaign Markdown only with fragments (think-wzmf).
    """
    documents = (
        sorted((controls.ROOT / "campaign").rglob("*.md"))
        if checked == "campaign"
        else [controls.REPO / checked]
    )
    roots = frozenset(controls.LINKED_PRUNE_ROOTS)
    files = set(controls.snapshot_pruned_targets())
    directories = set(controls.linked_pruned_directories())
    missing = []
    reached = 0
    for document in documents:
        for target in pattern.findall(document.read_text(encoding="utf-8")):
            path = target.partition("#")[0]
            if not path or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (document.parent / path).resolve()
            if not resolved.exists() or not controls.in_pruned_roots(resolved, roots):
                continue
            reached += 1
            if resolved not in (files if resolved.is_file() else directories):
                missing.append(f"{document.relative_to(controls.REPO)} -> {target}")
    assert not missing
    if checked != "README.md":
        # The campaign and SYNOPSIS reach into pruned roots hundreds of times; a parse
        # that found none would make this test vacuous.
        assert reached


def test_the_link_checked_documents_are_the_ones_registered_controls_check() -> None:
    """The rule's documents are the checkers' own, and registered controls run them."""
    checked = {
        (controls.REPO / document).resolve() for document in controls.LINK_CHECKED_DOCUMENTS
    }
    assert checked == {check_readme.README.resolve(), check_synopsis.SYNOPSIS.resolve()}
    assert ledger.ROOT.resolve() == (controls.ROOT / "campaign").resolve()
    spec = safe_load((controls.ROOT / "devtools/controls.yaml").read_text(encoding="utf-8"))
    commands = {control["run"] for control in spec["controls"]}
    for checker in (
        "devtools.check_readme",
        "devtools.check_synopsis",
        "campaign.ledger check",
    ):
        assert any(checker in command for command in commands), checker


def test_the_wall_workflows_are_declared_worker_inputs() -> None:
    """`check_gate_budgets` reads each wall's workflow; no review's link brings it now."""
    read = {
        check_gate_budgets.PULL_REQUEST_WORKFLOW,
        *(
            controls.REPO / wall.file
            for wall in load_walls(check_gate_budgets.REGISTER).workflows
        ),
    }
    assert read <= set(controls.COPY_SEPARATELY)
    assert set(controls.wall_workflows()) == read


#: The verifier-registry paths a review's link used to bring into every worker: the ones
#: `validate_schemas` found missing there once the copy-back stopped following reviews.
REVIEW_LINKED_VERIFIER_PATHS = (
    "packing/resources/web/n11-optimality-2026-09-29/source/VERIFY.py",
    (
        "packing/resources/web/queuingtheorydotcom-n11-lean-2026-10-06/receipts/lean/"
        "AuditN11Statement.lean"
    ),
    "packing/resources/web/wand125-closed-form-2026-10-14/review/README.md",
)


def test_the_readers_the_baselines_found_are_declared_worker_inputs() -> None:
    """Each explicit input names a reader that still reads it, or the entry is stale."""
    carried = set(controls.COPY_SEPARATELY)
    assert controls.ROOT / kingbird_layout.DEFAULT_SOURCE in carried
    registry = safe_load(
        (controls.ROOT / "frontier/verifiers.yaml").read_text(encoding="utf-8")
    )
    # The fields `verifier_registry.problems` requires to exist.
    named = {
        path
        for record in registry["verifiers"]
        for path in (
            *record.get("source", []),
            *(version["path"] for version in record.get("versions", []) if "path" in version),
            *([record["independence_record"]] if "independence_record" in record else []),
        )
    }
    for path in REVIEW_LINKED_VERIFIER_PATHS:
        assert path in named, path
        assert controls.REPO / path in carried, path


def test_every_file_the_results_checker_stats_reaches_a_worker(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Each path `check_results` requires to exist is declared, and comes back if pruned.

    Two controls run the checker in a worker. Its reads are traced rather than listed:
    every path it hands `repository_file_problem` for a review, a regularization or a
    regularized drawing, with every artifact and control, must be one `result_paths`
    declares. #612 registered T-185 and T-186 with `identity.measured_in` under
    `resources/web`, which nothing declared, and only the slow unmutated run of the
    checker in a worker found the 13 missing files (think-tddb).
    """
    register = safe_load(check_results.RESULTS.read_text(encoding="utf-8"))
    document_map = safe_load(check_results.DOCUMENT_MAP.read_text(encoding="utf-8"))
    results = register["results"]
    scopes = {record["id"]: check_results.scope_values(record["scope"]) for record in results}
    dated = {record["id"]: check_results.result_date(record) for record in results}
    stated = [
        path
        for record in results
        for field in ("artifacts", "controls")
        for path in record.get(field) or []
    ]
    real = check_results.repository_file_problem

    def traced(path: str) -> str | None:
        stated.append(path)
        return real(path)

    monkeypatch.setattr(check_results, "repository_file_problem", traced)
    for record in results:
        check_results.review_problems(record, document_map)
        check_results.regularizations_problems(record, dated, scopes)
    check_results.regularized_drawings_problems(register, scopes, drift=False)
    measured = {
        item["identity"]["measured_in"]
        for record in results
        for item in record.get("regularizations") or []
        if (item.get("identity") or {}).get("measured_in")
    }
    # The trace saw the field this guards, or the test would pass over nothing.
    assert measured
    assert measured <= set(stated)
    undeclared = sorted(set(stated) - set(controls.result_paths(register)))
    assert not undeclared

    roots = frozenset(controls.LINKED_PRUNE_ROOTS)
    reached = set(controls.result_pruned_targets())
    missing = sorted(
        path
        for path in set(stated)
        if (resolved := (controls.REPO / path).resolve()).is_file()
        and controls.in_pruned_roots(resolved, roots)
        and resolved not in reached
    )
    assert not missing


def test_only_the_links_a_control_checks_are_rescued(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A review's or a guide's links leave the worker; checked links and declarations stay."""
    repo = tmp_path / "source"
    packing = repo / "packing"
    runs = packing / "benchmarks/math-startup/runs"
    output = runs / "historical/reference.pdf"
    output.parent.mkdir(parents=True)
    output.write_bytes(b"retained browser observation")
    archive = packing / "resources"
    scientific_input = archive / "certificate.json"
    archive.mkdir()
    scientific_input.write_bytes(b"deciding scientific input")
    paper = archive / "paper.md"
    paper.write_text("# A paper\n")
    review = repo / "docs/review.md"
    review.parent.mkdir()
    review.write_text(
        "[observation](../packing/benchmarks/math-startup/runs/historical/reference.pdf)\n"
        "[scientific input](../packing/resources/certificate.json)\n"
    )
    guide = repo / "development.md"
    guide.write_text("[paper](packing/resources/paper.md#a-paper)\n")
    readme, synopsis = repo / "README.md", repo / "SYNOPSIS.md"
    readme.write_text("[review](docs/review.md)\n")
    synopsis.write_text("Synopsis\n")
    campaign = packing / "campaign/record.md"
    campaign.parent.mkdir()
    campaign.write_text("Campaign\n")
    register = packing / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text("results: []\n")
    defects = packing / "defects.yaml"
    defects.write_text("defects: []\n")
    monkeypatch.setattr(controls, "REPO", repo)
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset({runs, archive}))
    monkeypatch.setattr(
        controls,
        "DESCEND",
        frozenset({packing / "benchmarks", packing / "benchmarks/math-startup"}),
    )
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (runs, archive))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (readme, synopsis, guide, review.parent))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())

    # A checked link to the review checks that document, not its outgoing links, and no
    # control link-checks the guide: both documents reach the worker, their targets not.
    assert controls.snapshot_pruned_targets() == []
    index_fixture_source(repo)
    tree = tmp_path / "worker"
    controls.clone_tree(tree)
    assert (tree / review.relative_to(repo)).read_bytes() == review.read_bytes()
    assert (tree / guide.relative_to(repo)).read_bytes() == guide.read_bytes()
    for omitted in (output, scientific_input, paper):
        assert not (tree / omitted.relative_to(repo)).exists()
    git_tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    assert controls.snapshot_git_source_bytes(git_tree) == controls.snapshot_source_bytes()

    # The same targets linked from a document a control checks return, fragment or not.
    for document, relative in (
        (readme, "packing/resources/certificate.json"),
        (synopsis, "packing/resources/certificate.json#digest"),
        (campaign, "../resources/certificate.json#digest"),
    ):
        original = document.read_text()
        document.write_text(original + f"[deciding input]({relative})\n")
        assert controls.snapshot_pruned_targets() == [scientific_input]
        document.write_text(original)

    # Structural declarations are independent of prose: the results register's evidence,
    # which `check_results` requires to exist, and the defect log's `recorded_in`, which
    # `validate_schemas` does.
    measured = "{identity: {measured_in: packing/resources/certificate.json}}"
    for declaration in (
        "results:\n- artifacts: [packing/resources/certificate.json]\n",
        "results:\n- controls: [packing/resources/certificate.json]\n",
        "results:\n- reviews: [{path: packing/resources/certificate.json}]\n",
        f"results:\n- regularizations: [{measured}]\n",
        f"results: []\nregularized_drawings:\n  items: [{measured}]\n",
    ):
        register.write_text(declaration)
        assert controls.snapshot_pruned_targets() == [scientific_input]
    register.write_text("results: []\n")
    defects.write_text("defects:\n- recorded_in: packing/resources/paper.md\n")
    assert controls.snapshot_pruned_targets() == [paper]
    index_fixture_source(repo)
    git_tree = subprocess.run(
        ["git", "-C", str(repo), "write-tree"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    ).stdout.strip()
    assert controls.snapshot_git_source_bytes(git_tree) == controls.snapshot_source_bytes()
    defects.write_text("defects: []\n")
    monkeypatch.setattr(controls, "COPY_SEPARATELY", (output,))
    assert output in controls.snapshot_copy_targets()
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())

    # Rescued evidence remains a private mutable copy, never a link into custody.
    readme.write_text(
        "[observed input](packing/benchmarks/math-startup/runs/historical/reference.pdf)\n"
    )
    index_fixture_source(repo)
    rescued_tree = tmp_path / "rescued-worker"
    controls.clone_tree(rescued_tree)
    copied = rescued_tree / output.relative_to(repo)
    assert not copied.is_symlink()
    assert copied.read_bytes() == output.read_bytes()
    copied.write_bytes(b"corrupted observation")
    assert output.read_bytes() == b"retained browser observation"


def test_linked_directories_follow_the_same_checked_consumer_rule(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A linked pruned directory is recreated empty only for a link a worker checks."""
    repo = tmp_path / "source"
    packing = repo / "packing"
    runs = packing / "benchmarks/math-startup/runs"
    observations = runs / "historical"
    observations.mkdir(parents=True)
    (observations / "reference.pdf").write_bytes(b"retained browser observation")
    archive = packing / "resources"
    bundle = archive / "bundle"
    bundle.mkdir(parents=True)
    (bundle / "certificate.json").write_bytes(b"deciding scientific input")
    review = repo / "docs/review.md"
    review.parent.mkdir()
    review.write_text(
        "[observations](../packing/benchmarks/math-startup/runs/historical)\n"
        "[bundle](../packing/resources/bundle)\n"
    )
    readme, synopsis = repo / "README.md", repo / "SYNOPSIS.md"
    readme.write_text("[review](docs/review.md)\n")
    synopsis.write_text("Synopsis\n")
    campaign = packing / "campaign/record.md"
    campaign.parent.mkdir()
    campaign.write_text("Campaign\n")
    register = packing / "frontier/results.yaml"
    register.parent.mkdir()
    register.write_text("results: []\n")
    monkeypatch.setattr(controls, "REPO", repo)
    monkeypatch.setattr(controls, "ROOT", packing)
    monkeypatch.setattr(controls, "HERE", Path("packing"))
    monkeypatch.setattr(controls, "PRUNE", frozenset({runs, archive}))
    monkeypatch.setattr(
        controls,
        "DESCEND",
        frozenset({packing / "benchmarks", packing / "benchmarks/math-startup"}),
    )
    monkeypatch.setattr(controls, "LINKED_PRUNE_ROOTS", (runs, archive))
    monkeypatch.setattr(controls, "ROOT_DOCUMENTS", (readme, synopsis, review.parent))
    monkeypatch.setattr(controls, "COPY_SEPARATELY", ())
    monkeypatch.setattr(controls, "LINK_BACK", ())

    # Neither of the review's directory links is followed in a worker.
    assert controls.linked_pruned_directories() == []
    index_fixture_source(repo)
    tree = tmp_path / "worker"
    controls.clone_tree(tree)
    assert not (tree / observations.relative_to(repo)).exists()
    assert not (tree / bundle.relative_to(repo)).exists()

    for document, prefix in ((readme, "packing/"), (synopsis, "packing/"), (campaign, "../")):
        original = document.read_text()
        document.write_text(
            original
            + f"[observations]({prefix}benchmarks/math-startup/runs/historical)\n"
            + f"[bundle]({prefix}resources/bundle#certificate)\n"
        )
        assert controls.linked_pruned_directories() == [observations, bundle]
        document.write_text(original)
    readme.write_text("[bundle](packing/resources/bundle)\n")
    index_fixture_source(repo)
    linked_tree = tmp_path / "linked-worker"
    controls.clone_tree(linked_tree)
    landed = linked_tree / bundle.relative_to(repo)
    assert landed.is_dir()
    assert not any(landed.iterdir())
