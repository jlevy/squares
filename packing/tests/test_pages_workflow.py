"""Page checks must run when their own implementations change."""

from __future__ import annotations

import re
import shlex
import shutil
import subprocess
from collections.abc import Mapping
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any

from devtools.pages_scope import BUILDER_INPUTS, declared_inputs, pull_request_jobs
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
REGISTER = REPO / "packing/devtools/gate-budgets.yaml"

#: The jobs a pull request never runs: the deploy path, which only a push to `main`
#: starts, and the dispatch-only timing experiment.
DEPLOY_PATH = {"deploy", "verify-deployment"}

# These jobs can provision Python and their browser without the rendered page. They
# start beside `prepare`, then join its exact artifact before the first page consumer.
OVERLAPPED_PREPARED_PAGE_JOBS = {
    "pdf",
    "print-layout",
    "typography",
    "screen",
    "geometry",
    "font-loading",
    "browser-geometry",
}

#: The step right before every download by artifact id, reading the same id expression.
#: With `merge-multiple`, an empty `artifact-ids` downloads every artifact in the run.
ARTIFACT_ID_GUARD = "Require the prepared page's artifact id"
ARTIFACT_ID_CHECK = (
    '[[ "$ARTIFACT_ID" =~ ^[1-9][0-9]*$ ]] '
    '|| { echo "::error::the prepared page has no artifact id to download"; exit 1; }'
)


def load() -> dict[str, Any]:
    return safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))


def needs_of(job: Mapping[str, Any]) -> list[str]:
    needs = job.get("needs", [])
    return [needs] if isinstance(needs, str) else list(needs)


def upstream(jobs: Mapping[str, Mapping[str, Any]], name: str) -> set[str]:
    """Every job `name` waits for, transitively."""
    found: set[str] = set()
    pending = needs_of(jobs[name])
    while pending:
        need = pending.pop()
        if need not in found:
            found.add(need)
            pending.extend(needs_of(jobs[need]))
    return found


def browser_check_jobs(jobs: Mapping[str, Mapping[str, Any]]) -> list[str]:
    """Jobs that launch a browser against the prepared page, as opposed to producing it."""
    return [
        name
        for name, job in jobs.items()
        if name not in {"prepare", *DEPLOY_PATH}
        and any("playwright install" in step.get("run", "") for step in job.get("steps", []))
    ]


def page_probe_inputs() -> dict[str, list[str]]:
    """Probe inputs the page builders or their own workflow checks actually consume."""
    sources: dict[str, list[str]] = {}
    for inputs in declared_inputs().values():
        for path in inputs:
            relative = path.relative_to(REPO)
            if "probes" not in relative.parts:
                continue
            files = (
                [
                    item.relative_to(REPO).as_posix()
                    for item in path.rglob("*")
                    if item.is_file()
                ]
                if path.is_dir()
                else [relative.as_posix()]
            )
            sources[relative.as_posix()] = sorted(files)
    return dict(sorted(sources.items()))


def missing_page_probe_inputs(patterns: list[str]) -> dict[str, list[str]]:
    """Declared probe inputs whose files no Pages push pattern covers."""
    return {
        root: missing
        for root, files in page_probe_inputs().items()
        if (
            missing := [
                path
                for path in files
                if not any(fnmatchcase(path, pattern) for pattern in patterns)
            ]
        )
    }


def test_the_push_filter_covers_the_developer_tools_its_jobs_run() -> None:
    """A checker omitted from the deploy filter can change on `main` without running.

    Pull requests have no filter: `devtools.pages_scope` decides per page from the same
    commands, and `test_pages_scope` holds it to them.
    """
    workflow = load()
    modules = {
        module
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
        for module in re.findall(r"\bpython\s+-m\s+(devtools\.[\w.]+)", step.get("run", ""))
    }
    assert modules, "the page workflow runs no developer tools"
    scripts = {f"packing/{module.replace('.', '/')}.py" for module in modules}
    assert all((REPO / script).is_file() for script in scripts)
    patterns = workflow["on"]["push"]["paths"]
    missing = sorted(
        script for script in scripts if not any(fnmatchcase(script, p) for p in patterns)
    )
    assert not missing, f"push: page tools outside the workflow path filter: {missing}"
    assert workflow["on"]["pull_request"] is None, "pull requests are scoped by the scope job"


def test_every_pull_request_job_is_scoped_to_its_page_or_says_why() -> None:
    """No browser work runs on a pull request that changed neither page, and none silently.

    Every job that builds a page or launches a browser waits on the scope job's verdict
    for its page; each page has one job that runs only when that page is skipped and
    fails without a reason; and the scope runs the tool on the pull request's merge
    commit against its first parent, which a checkout of depth one could not diff.
    """
    workflow = load()
    jobs = workflow["jobs"]
    scope = jobs["scope"]
    halves = ("explainer", "workbench")
    assert set(scope["outputs"]) == {
        name for half in halves for name in (half, f"{half}_reason")
    }
    for name, value in scope["outputs"].items():
        assert value == f"${{{{ steps.scope.outputs.{name} }}}}"
    checkout = next(
        step for step in scope["steps"] if "actions/checkout@" in step.get("uses", "")
    )
    assert checkout["with"]["fetch-depth"] == 2
    decide = next(step for step in scope["steps"] if step.get("id") == "scope")
    assert "python -m devtools.pages_scope --diff HEAD^1 HEAD" in decide["run"]
    assert '[ "$EVENT" = pull_request ]' in decide["run"]

    gated = {
        half: {
            name
            for name, job in jobs.items()
            if job.get("if") == f"needs.scope.outputs.{half} == 'true'"
        }
        for half in halves
    }
    assert gated == {
        "explainer": {"prepare", *OVERLAPPED_PREPARED_PAGE_JOBS},
        "workbench": {"workbench"},
    }
    for half, roots in gated.items():
        assert all(needs_of(jobs[root]) == ["scope"] for root in roots)
        notices = [
            name
            for name, job in jobs.items()
            if job.get("if") == f"needs.scope.outputs.{half} != 'true'"
        ]
        assert notices == [f"{half}-unchanged"], half
        notice = jobs[notices[0]]
        assert needs_of(notice) == ["scope"]
        (step,) = notice["steps"]
        assert step["env"]["REASON"] == f"${{{{ needs.scope.outputs.{half}_reason }}}}"
        assert step["run"].splitlines()[0] == 'test -n "$REASON"'
        assert half in step["run"]
        assert "not built" in step["run"]

    for name, job in jobs.items():
        commands = "\n".join(step.get("run", "") for step in job.get("steps", []))
        works = "playwright install" in commands or re.search(
            r"python -m (devtools\.render_explainer|workbench_tools\.build_site)\b", commands
        )
        if works and name not in DEPLOY_PATH:
            directly_scoped = job.get("if") in {
                "needs.scope.outputs.explainer == 'true'",
                "needs.scope.outputs.workbench == 'true'",
            }
            assert upstream(jobs, name) & {"prepare", "workbench"} or directly_scoped, (
                f"{name} does page work on a pull request without waiting for the scope"
            )


def test_the_required_aggregate_passes_a_justified_skip_and_nothing_else() -> None:
    """`pages-required` is the one context a branch rule would name.

    It waits for every job a pull request runs, so a skip caused by an upstream failure
    is always accompanied by that failure; and it requires the scope's outputs to be
    decisions, so a scope that wrote nothing cannot read as a decision to skip.
    """
    jobs = load()["jobs"]
    aggregate = jobs["pages-required"]
    assert aggregate["if"] == "always()"
    assert set(needs_of(aggregate)) == set(jobs) - {"pages-required", *DEPLOY_PATH}
    step = next(
        item
        for item in aggregate["steps"]
        if item.get("name") == "Require every page this run builds to pass"
    )
    assert step["env"]["NEEDS"] == "${{ toJSON(needs) }}"
    program = step["run"]
    assert '.scope.result == "success"' in program
    decisions = "[.scope.outputs.explainer, .scope.outputs.workbench]"
    assert f'{decisions} | all(. == "true" or . == "false")' in program
    assert '[.[].result] | all(. == "success" or . == "skipped")' in program
    assert "jq -e" in program
    assert set(needs_of(jobs["deploy"])) == {"publish", "pages-required"}


def conjuncts(condition: str) -> list[str] | None:
    """The whole clauses an `if:` joins with `&&`, or None if it is not only a conjunction.

    Under `||` no clause is necessary, so finding one in the text proves nothing about
    what the condition requires. The same holds inside a group: `!(a && b)` or
    `(a && b) == false` splits into clauses that read as required and are not. So a clause
    whose parentheses do not balance, or that negates a group, refuses the whole condition.
    """
    text = condition.strip()
    if text.startswith("${{") and text.endswith("}}"):
        text = text[3:-2]
    if "||" in text:
        return None
    clauses = [" ".join(clause.split()) for clause in text.split("&&")]
    for clause in clauses:
        depth = 0
        for character in clause:
            depth += {"(": 1, ")": -1}.get(character, 0)
            if depth < 0:
                return None
        if depth or clause.replace(" ", "").startswith("!("):
            return None
    return clauses


def implicit_success_gaps(jobs: Mapping[str, Mapping[str, Any]], name: str) -> list[str]:
    """The clauses `name`'s `if:` does not require when an ancestor can skip on a push.

    Without a status function GitHub applies `success()` over every ancestor, so one
    skipped ancestor skips the job however its direct `needs:` ended. Each clause must be
    a whole conjunct of the condition, and a condition with `||` requires none of them.
    """
    if not any(jobs[ancestor].get("if") for ancestor in upstream(jobs, name)):
        return []
    clauses = conjuncts(str(jobs[name].get("if", "")))
    required = [
        "!cancelled()",
        *(f"needs.{need}.result == 'success'" for need in needs_of(jobs[name])),
    ]
    return [clause for clause in required if clauses is None or clause not in clauses]


def test_the_deploy_path_does_not_inherit_skips_from_its_ancestors() -> None:
    """From #183 to this fix every push to `main` skipped `deploy`.

    The dispatch-only timing job and one job of each `*-unchanged` pair skip on a push, and
    `deploy` carried no status function, so its implicit `success()` saw those skips. The
    conditions are pinned whole, so the fix cannot also drop the push-to-`main` gate.
    """
    jobs = load()["jobs"]
    assert jobs["deploy"]["if"] == (
        "${{ !cancelled() && github.ref == 'refs/heads/main' "
        "&& github.event_name != 'pull_request' "
        "&& needs.publish.result == 'success' && needs.pages-required.result == 'success' }}"
    )
    assert jobs["verify-deployment"]["if"] == (
        "${{ !cancelled() && needs.deploy.result == 'success' }}"
    )
    for name in sorted(DEPLOY_PATH):
        assert not implicit_success_gaps(jobs, name), (name, implicit_success_gaps(jobs, name))

    def deploying_if(condition: str) -> dict[str, Any]:
        return {**jobs, "deploy": {**jobs["deploy"], "if": condition}}

    required = [
        "!cancelled()",
        "needs.publish.result == 'success'",
        "needs.pages-required.result == 'success'",
    ]
    before = "github.ref == 'refs/heads/main' && github.event_name != 'pull_request'"
    assert implicit_success_gaps(deploying_if(before), "deploy") == required
    # Every clause is in the text of each of these, which a substring match accepted.
    fixed = str(jobs["deploy"]["if"])
    for weakened in (
        fixed.replace("!cancelled()", "always() || !cancelled()"),
        fixed.replace("&& needs.publish.result", "|| needs.publish.result"),
    ):
        assert all(clause in weakened for clause in required), weakened
        assert implicit_success_gaps(deploying_if(weakened), "deploy") == required, weakened
    # Each required clause is a whole `&&` split of these, which a plain split accepted, but
    # inside a negated group none of them is required.
    body = fixed.strip()[3:-2].strip()
    ref = "github.ref == 'refs/heads/main'"
    for negated in (
        f"${{{{ !({ref} && {body} && {ref}) }}}}",
        f"${{{{ ({ref} && {body} && {ref}) == false }}}}",
    ):
        split = {" ".join(clause.split()) for clause in negated[3:-2].split("&&")}
        assert set(required) <= split, negated
        assert conjuncts(negated) is None, negated
        assert implicit_success_gaps(deploying_if(negated), "deploy") == required, negated
    # A whole clause in harmless parentheses is still a conjunct.
    grouped = f"${{{{ {body} && ({ref}) }}}}"
    whole = conjuncts(fixed)
    assert whole is not None
    assert conjuncts(grouped) == [*whole, f"({ref})"]
    assert implicit_success_gaps(deploying_if(grouped), "deploy") == []


def test_every_download_by_artifact_id_extracts_into_its_path() -> None:
    """`download-artifact` v4 puts an id download under `<path>/<artifact name>/`.

    Only a download by `name` or with `merge-multiple` extracts into `path` itself. Run
    35175474665 downloaded the prepared page to `packing/site/prepared-page/`, and every
    browser check then failed to find `site/index.html`.
    """
    downloads = [
        (name, step["with"])
        for name, job in load()["jobs"].items()
        for step in job.get("steps", [])
        if step.get("uses", "").startswith("actions/download-artifact@")
        and "artifact-ids" in step.get("with", {})
    ]
    assert len(downloads) >= 9
    for name, arguments in downloads:
        assert arguments.get("merge-multiple") is True, name


def unguarded_downloads_by_id(jobs: Mapping[str, Mapping[str, Any]]) -> list[str]:
    """Downloads by artifact id that an empty id would not stop.

    Each must follow, immediately, the guard step reading its own id expression, and
    neither step may be skippable or allowed to fail.
    """
    unguarded: list[str] = []
    for name, job in jobs.items():
        steps = job.get("steps", [])
        for index, step in enumerate(steps):
            if not (
                step.get("uses", "").startswith("actions/download-artifact@")
                and "artifact-ids" in step.get("with", {})
            ):
                continue
            guard = {
                "name": ARTIFACT_ID_GUARD,
                "env": {"ARTIFACT_ID": step["with"]["artifact-ids"]},
                "run": ARTIFACT_ID_CHECK,
            }
            preceding = steps[index - 1] if index else None
            if preceding != guard or "if" in step or "continue-on-error" in step:
                unguarded.append(f"{name}: step {index}")
    return unguarded


def test_every_download_by_artifact_id_is_refused_without_an_id() -> None:
    """`artifact-ids: ''` with `merge-multiple` is not an error; it downloads everything.

    Every artifact in the run would land in `packing/site`, the workbench's `index.html`
    over the explainer's, and the checks after it would read the wrong page. Skipping the
    download would leave them reading no page, so the step before it fails the job instead.
    """
    jobs = load()["jobs"]
    assert not unguarded_downloads_by_id(jobs)
    guarded = [
        (name, index)
        for name, job in jobs.items()
        for index, step in enumerate(job.get("steps", []))
        if step.get("name") == ARTIFACT_ID_GUARD
    ]
    downloads = [
        name
        for name, job in jobs.items()
        for step in job.get("steps", [])
        if "artifact-ids" in step.get("with", {})
    ]
    assert len(guarded) == len(downloads) >= 9
    bash = shutil.which("bash")
    assert bash
    for value, status in (("", 1), (" ", 1), ("0", 1), ("12abc", 1), ("35175474665", 0)):
        result = subprocess.run(
            (bash, "-e", "-c", ARTIFACT_ID_CHECK),
            env={"ARTIFACT_ID": value},
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == status, (value, result)

    for name, index in guarded:
        steps = jobs[name]["steps"]
        guard, download = steps[index], steps[index + 1]
        mutations = {
            "no guard": [*steps[:index], *steps[index + 1 :]],
            "another id": [
                *steps[:index],
                {**guard, "env": {"ARTIFACT_ID": "${{ steps.other.outputs.artifact_id }}"}},
                *steps[index + 1 :],
            ],
            "skippable guard": [
                *steps[:index],
                {**guard, "if": "always()"},
                *steps[index + 1 :],
            ],
            "skippable download": [
                *steps[: index + 1],
                {**download, "if": "steps.prepared.outputs.artifact_id != ''"},
                *steps[index + 2 :],
            ],
            "guard allowed to fail": [
                *steps[:index],
                {**guard, "continue-on-error": True},
                *steps[index + 1 :],
            ],
            "download allowed to fail": [
                *steps[: index + 1],
                {**download, "continue-on-error": True},
                *steps[index + 2 :],
            ],
        }
        for mutation, mutated in mutations.items():
            changed = {**jobs, name: {**jobs[name], "steps": mutated}}
            assert unguarded_downloads_by_id(changed), (name, mutation)


def test_pages_filters_cover_the_probes_its_tools_and_controls_load() -> None:
    """The page's tools and its PDF controls hand the browser JavaScript from probe files, and
    the render inlines some of them; an edit to one is an edit to the tool that loads it.

    Pull requests are covered by the builder-owned inputs in `pages_scope`; the push
    filter remains the one outer trigger that must be checked directly.
    """
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
    patterns = workflow["on"]["push"]["paths"]
    trees = page_probe_inputs()
    assert trees
    assert not missing_page_probe_inputs(patterns), (
        "push: declared page probe inputs outside the workflow path filter: "
        f"{missing_page_probe_inputs(patterns)}"
    )


def test_pages_filter_contract_rejects_each_omitted_declared_probe_input() -> None:
    """The coverage check must fail when an actual page probe input loses its trigger."""
    patterns = load()["on"]["push"]["paths"]
    trees = page_probe_inputs()
    for root, files in trees.items():
        covering = {
            pattern for pattern in patterns if any(fnmatchcase(path, pattern) for path in files)
        }
        assert covering, f"test setup: {root} has no covering push pattern"
        without_tree = [pattern for pattern in patterns if pattern not in covering]
        missing = missing_page_probe_inputs(without_tree)
        assert root in missing, f"test setup: removing {covering} did not expose {root}"


def test_deployment_waits_for_the_cross_browser_loading_checks() -> None:
    jobs = load()["jobs"]
    for name in ("font-loading", "browser-geometry"):
        assert set(jobs[name]["strategy"]["matrix"]["browser"]) == {"firefox", "webkit"}
        assert name in upstream(jobs, "deploy")
    assert any(
        "devtools.check_math_loading" in step.get("run", "")
        for step in jobs["font-loading"]["steps"]
    )


def test_page_check_setup_overlaps_prepare_then_joins_its_exact_artifact() -> None:
    """Independent provisioning starts early; no page consumer can outrun prepare."""
    jobs = load()["jobs"]
    for name in OVERLAPPED_PREPARED_PAGE_JOBS:
        job = jobs[name]
        assert needs_of(job) == ["scope"]
        assert job["if"] == "needs.scope.outputs.explainer == 'true'"
        assert job["permissions"] == {"contents": "read", "actions": "read"}
        steps = job["steps"]
        install_index = max(
            index
            for index, step in enumerate(steps)
            if "playwright install" in step.get("run", "")
        )
        wait = next(step for step in steps if step.get("name") == "Wait for the prepared page")
        guard = next(step for step in steps if step.get("name") == ARTIFACT_ID_GUARD)
        download = next(step for step in steps if step.get("name") == "Use the prepared page")
        assert (
            install_index < steps.index(wait) < steps.index(guard) == steps.index(download) - 1
        )
        assert guard["env"] == {"ARTIFACT_ID": "${{ steps.prepared.outputs.artifact_id }}"}
        assert wait["id"] == "prepared"
        assert wait["env"]["GH_TOKEN"] == "${{ github.token }}"
        command = wait["run"]
        assert "python -m devtools.wait_for_run_artifact" in command
        assert '--repository "$GITHUB_REPOSITORY"' in command
        assert '--run-id "$GITHUB_RUN_ID"' in command
        assert '--run-attempt "$GITHUB_RUN_ATTEMPT"' in command
        assert "--name prepared-page" in command
        assert "--producer prepare" in command
        assert '--github-output "$GITHUB_OUTPUT"' in command
        assert "--timeout 600" in command
        assert download["with"] == {
            "artifact-ids": "${{ steps.prepared.outputs.artifact_id }}",
            "path": "packing/site",
            "merge-multiple": True,
        }


def test_saved_font_geometry_runs_as_two_bounded_pairs() -> None:
    """Remove the serial WebKit tail without launching four browsers at once."""
    steps = load()["jobs"]["font-loading"]["steps"]
    command = next(
        step["run"]
        for step in steps
        if step.get("name") == "Check saved font settings retain geometry at 1280 px"
    )
    lines = command.splitlines()
    launches = [line for line in lines if "devtools.prepare_explainer_math" in line]
    waits = [line for line in lines if line.strip().startswith("wait ")]
    assert len(launches) == 4
    assert all(line.endswith(" &") for line in launches)
    assert len(waits) == 4
    assert lines.index(waits[1]) < lines.index(launches[2])


def test_print_layout_runs_the_overflow_self_check_beside_the_page() -> None:
    """Two Chromium launches, one page each; serializing them was 66 s of this job."""
    steps = load()["jobs"]["print-layout"]["steps"]
    command = next(
        step["run"]
        for step in steps
        if step.get("name") == "Check the print layout and its overflow self-check"
    )
    lines = command.splitlines()
    launches = [line for line in lines if "python -m devtools.check_print_layout" in line]
    waits = [line for line in lines if line.strip().startswith("wait ")]
    assert len(launches) == 2
    assert all(line.rstrip().endswith(" &") for line in launches)
    assert sum("--self-check" in line for line in launches) == 1
    assert len(waits) == 2
    assert 'wait "$layout_pid"' in command
    assert 'wait "$self_pid"' in command
    assert 'test "$layout_status" -eq 0' in command
    assert 'test "$self_status" -eq 0' in command
    last_launch = max(lines.index(line) for line in launches)
    first_wait = min(lines.index(line) for line in waits)
    assert last_launch < first_wait


def test_every_browser_check_waits_for_deployment() -> None:
    """Splitting one queue into jobs must not let a check fall off the deploy's `needs`."""
    jobs = load()["jobs"]
    checks = browser_check_jobs(jobs)
    assert len(checks) >= 6
    assert set(checks) <= upstream(jobs, "deploy")
    assert {"workbench", "publish", "prepare"} <= upstream(jobs, "deploy")


def test_the_firefox_and_webkit_system_packages_are_cached_and_installed_the_same_way() -> None:
    """The archive cache must not change which packages the browsers run against.

    Playwright's own `install --with-deps` still decides the package list and apt still
    resolves it against this runner image's lists; the cache only keeps apt from
    downloading archives it already holds, and the key names the image and the lock.
    """
    jobs = load()["jobs"]
    for name in ("font-loading", "browser-geometry"):
        steps = jobs[name]["steps"]
        image = next(step for step in steps if step.get("id") == "image")
        assert image["run"] == 'echo "image=${ImageOS}-${ImageVersion}" >> "$GITHUB_OUTPUT"'
        cache = next(
            step for step in steps if step.get("name") == "Cache the browser's system packages"
        )
        assert cache["with"]["path"] == "~/apt-archives"
        assert cache["with"]["key"] == (
            "apt-${{ matrix.browser }}-${{ steps.image.outputs.image }}-"
            "${{ hashFiles('packing/uv.lock') }}"
        )
        install = next(
            step for step in steps if "playwright install --with-deps" in step.get("run", "")
        )
        lines = install["run"].splitlines()
        playwright = "uv run --frozen --group dev python -m playwright"
        assert f"{playwright} install --with-deps ${{{{ matrix.browser }}}}" in lines
        assert any('Dir::Cache::Archives \\"$HOME/apt-archives/\\"' in line for line in lines)
        assert steps.index(image) < steps.index(cache) < steps.index(install)


def test_live_verification_waits_for_the_exact_deployed_revision() -> None:
    """The source gate cannot prove that Pages serves the artifact it accepted."""
    workflow = load()
    deploy = workflow["jobs"]["deploy"]
    verify = workflow["jobs"]["verify-deployment"]
    assert deploy["outputs"]["page-url"] == "${{ steps.deployment.outputs.page_url }}"
    assert verify["needs"] == "deploy"
    commands = "\n".join(step.get("run", "") for step in verify["steps"])
    assert "python -m devtools.check_published_site" in commands
    assert '--site "${{ needs.deploy.outputs.page-url }}"' in commands
    assert '--commit "${{ github.sha }}"' in commands
    assert "--no-browser" not in commands


def test_publication_assembles_the_three_checked_products_and_only_main_uploads_it() -> None:
    """What `build` uploaded from one directory is now three artifacts put back together.

    The prepared page at the root, the checked PDF beside it, the workbench under
    `/workbench/`: the same tree, and the only upload to Pages is a push to `main`.
    """
    jobs = load()["jobs"]
    publish = jobs["publish"]
    assert set(needs_of(publish)) == {"prepare", "pdf", "workbench"}
    steps = publish["steps"]
    assert steps[0]["name"] == ARTIFACT_ID_GUARD
    assert steps[0]["env"] == {
        "ARTIFACT_ID": "${{ needs.prepare.outputs.prepared_artifact_id }}"
    }
    downloads = [
        step["with"]
        for step in steps
        if step.get("uses", "").startswith("actions/download-artifact@")
    ]
    assert downloads == [
        {
            "artifact-ids": "${{ needs.prepare.outputs.prepared_artifact_id }}",
            "path": "packing/site",
            "merge-multiple": True,
        },
        {"name": "explainer-pdf", "path": "packing/site"},
        {"name": "workbench-page", "path": "packing/site/workbench"},
    ]
    prepare = jobs["prepare"]
    assert prepare["outputs"] == {
        "prepared_artifact_id": "${{ steps.prepared-page-upload.outputs.artifact-id }}"
    }
    prepared_upload = next(
        step for step in prepare["steps"] if step.get("with", {}).get("name") == "prepared-page"
    )
    assert prepared_upload["id"] == "prepared-page-upload"
    produced = {
        step["with"]["name"]: (name, step["with"]["path"])
        for name, job in jobs.items()
        for step in job.get("steps", [])
        if step.get("uses", "").startswith("actions/upload-artifact@")
    }
    assert produced["prepared-page"] == ("prepare", "packing/site")
    assert produced["explainer-pdf"] == ("pdf", "packing/site/t-018-explainer.pdf")
    assert produced["workbench-page"] == ("workbench", "packing/site/workbench")
    (upload,) = [
        step
        for step in steps
        if step.get("uses", "").startswith("actions/upload-pages-artifact@")
    ]
    assert (
        upload["if"] == "github.ref == 'refs/heads/main' && github.event_name != 'pull_request'"
    )
    assert upload["with"] == {"path": "packing/site"}
    uploads_elsewhere = [
        name
        for name, job in jobs.items()
        for step in job.get("steps", [])
        if step.get("uses", "").startswith("actions/upload-pages-artifact@")
        and name != "publish"
    ]
    assert uploads_elsewhere == []
    workbench = jobs["workbench"]["steps"]
    build = next(
        i for i, s in enumerate(workbench) if "workbench_tools.build_site" in s.get("run", "")
    )
    share = next(
        i for i, s in enumerate(workbench) if s.get("with", {}).get("name") == "workbench-page"
    )
    assert build < share
    assert "--check" in shlex.split(workbench[build]["run"])


def test_every_page_job_a_pull_request_runs_is_budgeted() -> None:
    """A page job with no recorded cost is a job that can double without anything objecting.

    That is what happened to this workflow: the register budgets the validation tiers and
    said nothing about Pages, which reached 472 s on a pull request with every check green
    (`think-xfqk`). The tiers' own rule, asked of these jobs: every job a pull request runs
    has an entry, every entry names a job that exists, every entry carries a cost measured
    on named runs, and every ceiling is inside the register's `max_headroom` of that cost.
    A matrix job is one entry per cell, because that is what a runner runs.

    Enforcement against a live run belongs to the pull-request wall tool; this is the
    declaration check, and like `check_gate_budgets` it needs no clock.
    """
    register = safe_load(REGISTER.read_text("utf-8"))
    pages = register["pages"]
    workflow = load()
    jobs = workflow["jobs"]
    expected: set[str] = set()
    for name in pull_request_jobs(workflow):
        matrix = jobs[name].get("strategy", {}).get("matrix", {}).get("browser")
        expected |= {f"{name} ({cell})" for cell in matrix} if matrix else {name}
    assert {entry["id"] for entry in pages["jobs"]} == expected
    assert pages["reference"] == {"runner": "ubuntu-latest", "cpus": 4, "caches": "warm"}
    headroom = register["policy"]["max_headroom"]
    for entry in pages["jobs"]:
        where = entry["id"]
        assert entry["measured_seconds"] > 0, where
        assert entry["measured_on"], where
        assert re.search(r"run \d{8,}", entry["measured_where"]), where
        assert entry["ceiling_seconds"] >= entry["measured_seconds"], where
        assert entry["ceiling_seconds"] <= headroom * entry["measured_seconds"], where
        assert entry["argument"].strip(), where
    wall = pages["wall"]
    wall_budget = next(
        workflow
        for workflow in register["pull_request_walls"]["workflows"]
        if workflow["id"] == "certificate-page"
    )["budget_seconds"]
    assert wall["measured_seconds"] > 0
    assert wall["measured_on"]
    assert re.search(r"run \d{8,}", wall["measured_where"])
    assert wall["ceiling_seconds"] == wall_budget == 180.0
    assert wall["argument"].strip()
    assert pages["wall"]["measured_seconds"] >= max(
        entry["measured_seconds"] for entry in pages["jobs"]
    ), "the wall is at least the longest job"


def test_pages_runs_real_math_failure_controls_on_the_pdf_it_draws() -> None:
    """The real-browser controls must run, rather than silently taking their default skip.

    They run after the publication draw, because the normal-math control reads that PDF
    rather than drawing its own, and before the artifact check, so a refused control
    fails the job before the fresh comparison draw is spent.
    """
    workflow = load()
    job = workflow["jobs"]["pdf"]
    steps = job["steps"]
    test_path = "tests/test_pdf_math_browser.py"
    controls = [
        (index, step) for index, step in enumerate(steps) if test_path in step.get("run", "")
    ]
    assert len(controls) == 1
    index, step = controls[0]
    assert job["defaults"]["run"]["working-directory"] == "packing"
    assert step["env"]["SQPACK_PDF_MATH_BROWSER"] == "1"
    assert shlex.split(step["run"]) == [
        "uv",
        "run",
        "--frozen",
        "--group",
        "dev",
        "pytest",
        "-q",
        test_path,
    ]
    assert not step.get("if")
    assert not step.get("continue-on-error")
    downloads = [
        before
        for before, candidate in enumerate(steps)
        if candidate.get("uses", "").startswith("actions/download-artifact@")
        and candidate.get("name") == "Use the prepared page"
    ]
    installs = [
        before
        for before, candidate in enumerate(steps)
        if "playwright install --only-shell chromium" in candidate.get("run", "")
    ]
    draws = [
        before
        for before, candidate in enumerate(steps)
        if "devtools.render_explainer_pdf --update" in candidate.get("run", "")
    ]
    checks = [
        after
        for after, candidate in enumerate(steps)
        if "devtools.render_explainer_pdf --check-artifact" in candidate.get("run", "")
    ]
    assert downloads
    assert installs
    assert len(draws) == 1
    assert len(checks) == 1
    assert max(downloads + installs) < draws[0] < index < checks[0]
    assert (REPO / "packing" / test_path).is_file()
    assert any(
        fnmatchcase(f"packing/{test_path}", pattern)
        for pattern in workflow["on"]["push"]["paths"]
    ), "push: editing the browser controls must run them"


def test_the_normal_math_control_does_not_draw_the_pdf_again() -> None:
    """One production draw of the unfaulted page per run, and it is the published one."""
    source = (REPO / "packing/tests/test_pdf_math_browser.py").read_text("utf-8")
    control = source.split("def test_production_pdf_accepts_typeset_math", 1)[1]
    control = control.split("\ndef ", 1)[0]
    assert "render_pdf_bytes" not in control
    assert "pdf.OUTPUT.read_bytes()" in control
    assert "sqpack-source-html-sha256" in control


def test_pages_checks_the_pdf_it_uploads_and_retains_mismatch_evidence() -> None:
    """A later pair of fresh draws must not stand in for the artifact being published."""
    workflow = load()
    steps = workflow["jobs"]["pdf"]["steps"]
    module = "devtools.render_explainer_pdf"
    commands = [
        (index, shlex.split(line))
        for index, step in enumerate(steps)
        for line in step.get("run", "").splitlines()
        if f"python -m {module} " in line and "--trace-math" not in shlex.split(line)
    ]
    assert len(commands) == 2, (
        "the PDF must be drawn once and then checked without rewriting it"
    )
    (draw_index, draw), (check_index, check) = commands
    assert draw[draw.index(module) + 1 :] == ["--update"]
    assert check[check.index(module) + 1 :] == [
        "--check-artifact",
        "--diagnostics-dir",
        "/tmp/explainer-pdf-check",
    ]
    assert not steps[check_index].get("if"), "the artifact check must run on every build"
    assert not steps[check_index].get("continue-on-error")
    uploads = [
        index
        for index, step in enumerate(steps)
        if step.get("uses", "").startswith("actions/upload-artifact@")
        and step["with"]["name"] == "explainer-pdf"
    ]
    assert len(uploads) == 1
    assert draw_index < check_index < uploads[0]
    assert steps[uploads[0]]["with"]["path"] == "packing/site/t-018-explainer.pdf"
    assert not steps[uploads[0]].get("if"), "the published PDF is the one this job checked"
    diagnostics = [
        (index, step)
        for index, step in enumerate(steps)
        if step.get("with", {}).get("path") == "/tmp/explainer-pdf-check"
    ]
    assert len(diagnostics) == 1
    index, diagnostic_step = diagnostics[0]
    assert check_index < index < uploads[0]
    assert diagnostic_step["if"] == "failure()"
    assert re.fullmatch(r"actions/upload-artifact@[0-9a-f]{40}", diagnostic_step["uses"])
    assert diagnostic_step["with"] == {
        "name": "explainer-pdf-check",
        "path": "/tmp/explainer-pdf-check",
        "if-no-files-found": "ignore",
        "retention-days": 7,
    }


def test_pdf_tracing_is_manual_and_preserves_the_uninstrumented_artifact_gate() -> None:
    workflow = load()
    option = workflow["on"]["workflow_dispatch"]["inputs"]["trace_pdf"]
    assert option["type"] == "boolean"
    assert option["default"] is False
    steps = workflow["jobs"]["pdf"]["steps"]
    traces = [
        step
        for step in steps
        if "--trace-math" in step.get("run", "")
        and "--rebuild-prepared-text" not in step.get("run", "")
    ]
    assert len(traces) == 1
    trace = traces[0]
    assert trace["if"] == (
        "${{ !cancelled() && github.event_name == 'workflow_dispatch' && inputs.trace_pdf }}"
    )
    assert not trace.get("continue-on-error")
    args = shlex.split(trace["run"])
    assert args[args.index("devtools.render_explainer_pdf") + 1 :] == [
        "--check",
        "--renders",
        "20",
        "--trace-math",
        "--diagnostics-dir",
        "/tmp/explainer-pdf-trace",
    ]
    capture = next(
        step for step in steps if step.get("with", {}).get("name") == "explainer-pdf-trace"
    )
    assert capture["if"] == (
        "${{ always() && github.event_name == 'workflow_dispatch' && inputs.trace_pdf }}"
    )
    assert capture["with"]["path"] == "/tmp/explainer-pdf-trace"
    assert capture["with"]["if-no-files-found"] == "error"
    assert capture["with"]["retention-days"] == 7
    assert re.fullmatch(r"actions/upload-artifact@[0-9a-f]{40}", capture["uses"])
    gate = next(step for step in steps if "--check-artifact" in step.get("run", ""))
    publish = next(
        step for step in steps if step.get("with", {}).get("name") == "explainer-pdf"
    )
    assert steps.index(gate) < steps.index(trace) < steps.index(capture) < steps.index(publish)


def test_pdf_reconstruction_is_a_separate_optional_diagnostic_arm() -> None:
    workflow = load()
    option = workflow["on"]["workflow_dispatch"]["inputs"]["rebuild_pdf_math_text"]
    assert option["type"] == "boolean"
    assert option["default"] is False
    steps = workflow["jobs"]["pdf"]["steps"]
    treatments = [step for step in steps if "--rebuild-prepared-text" in step.get("run", "")]
    assert len(treatments) == 1
    treatment = treatments[0]
    assert treatment["if"] == (
        "${{ !cancelled() && github.event_name == 'workflow_dispatch' "
        "&& inputs.trace_pdf && inputs.rebuild_pdf_math_text }}"
    )
    assert not treatment.get("continue-on-error")
    args = shlex.split(treatment["run"])
    assert args[args.index("devtools.render_explainer_pdf") + 1 :] == [
        "--check",
        "--renders",
        "20",
        "--trace-math",
        "--rebuild-prepared-text",
        "--diagnostics-dir",
        "/tmp/explainer-pdf-rebuild",
    ]
    capture = next(
        step for step in steps if step.get("with", {}).get("name") == "explainer-pdf-rebuild"
    )
    assert capture["if"] == (
        "${{ always() && github.event_name == 'workflow_dispatch' "
        "&& inputs.trace_pdf && inputs.rebuild_pdf_math_text }}"
    )
    assert capture["with"]["path"] == "/tmp/explainer-pdf-rebuild"
    assert capture["with"]["if-no-files-found"] == "error"
    assert capture["with"]["retention-days"] == 7
    assert re.fullmatch(r"actions/upload-artifact@[0-9a-f]{40}", capture["uses"])
    control = next(
        step
        for step in steps
        if "--trace-math" in step.get("run", "")
        and "--rebuild-prepared-text" not in step.get("run", "")
    )
    assert steps.index(control) < steps.index(treatment) < steps.index(capture)


def test_every_browser_checks_the_same_prepared_publication() -> None:
    """A raw re-render in one job would leave the actual published boxes untested.

    One job renders. It renders twice, at once, into two directories and requires every
    file to agree; only the render into `site/` is shared, and every job that launches a
    browser against the page downloads that one artifact.
    """
    workflow = load()
    jobs = workflow["jobs"]
    renders = [
        (name, index, line)
        for name, job in jobs.items()
        for index, step in enumerate(job.get("steps", []))
        for line in step.get("run", "").splitlines()
        if "python -m devtools.render_explainer " in line
        or line.endswith("python -m devtools.render_explainer")
    ]
    assert renders, "publication never renders its HTML"
    assert all("--prepare-math" in line for _, _, line in renders)
    producers = {name for name, _, _ in renders}
    assert producers == {"prepare"}, "browser checks must share one prepared artifact"
    steps = jobs["prepare"]["steps"]
    (render_index,) = {index for _, index, _ in renders}
    render = steps[render_index]["run"].splitlines()
    lines = [line for line in render if "python -m devtools.render_explainer" in line]
    assert len(lines) == 2, "two independent renders"
    twin, published = lines
    assert twin.endswith('--output "$twin/index.html" &'), "the twin renders outside site/"
    assert "--output" not in published, "the shared render writes site/"
    assert render.index('wait "$twin_pid"') > render.index(published)
    assert 'diff --recursive site "$twin"' in render
    assert render.index('diff --recursive site "$twin"') > render.index('wait "$twin_pid"')
    installs = [
        index
        for index, step in enumerate(steps)
        if "playwright install" in step.get("run", "") and "chromium" in step["run"]
    ]
    assert installs
    assert min(installs) < render_index
    uploads = [
        step["with"]
        for step in steps
        if step.get("uses", "").startswith("actions/upload-artifact@")
    ]
    assert len(uploads) == 1
    assert uploads[0]["path"] == "packing/site"
    checks = browser_check_jobs(jobs)
    assert {
        "pdf",
        "print-layout",
        "typography",
        "screen",
        "geometry",
        "font-loading",
        "browser-geometry",
        "startup-timing",
    } <= set(checks)
    for name in checks:
        if name in OVERLAPPED_PREPARED_PAGE_JOBS:
            assert needs_of(jobs[name]) == ["scope"], name
            artifact_id = "${{ steps.prepared.outputs.artifact_id }}"
        else:
            assert needs_of(jobs[name]) == ["prepare"], name
            artifact_id = "${{ needs.prepare.outputs.prepared_artifact_id }}"
        downloads = [
            step["with"]
            for step in jobs[name]["steps"]
            if step.get("uses", "").startswith("actions/download-artifact@")
        ]
        assert downloads == [
            {"artifact-ids": artifact_id, "path": "packing/site", "merge-multiple": True}
        ], name

    assert not any(
        step.get("with", {}).get("name") == "prepared-page"
        for job in jobs.values()
        for step in job.get("steps", [])
        if step.get("uses", "").startswith("actions/download-artifact@")
    )


def test_the_partial_checkouts_keep_the_directories_the_render_links() -> None:
    """Leaving out the literature archive and the campaign must not change the page.

    The renderer writes the archive's link as a `tree/` URL because `packing/resources`
    is a directory; a checkout without that directory would publish a `blob/` URL with
    every check green. So the sparse patterns exclude the two trees' subdirectories and
    keep their top-level files. The workbench stamps the checkout's cleanliness into its
    page, but Git's sparse checkout keeps omitted tracked files at `skip-worktree`: a clean
    sparse checkout is still clean, and downloading 504 MB of unrelated archive and
    campaign data cannot make that answer more honest.
    """
    jobs = load()["jobs"]
    patterns = "/*\n!/packing/resources/*/\n!/packing/campaign/*/\n"
    sparse = []
    for name, job in jobs.items():
        for step in job.get("steps", []):
            if "actions/checkout@" not in step.get("uses", ""):
                continue
            settings = step["with"]
            if "sparse-checkout" in settings:
                if step.get("name") == "Check out the wall budget and its register":
                    assert settings["sparse-checkout"] == (
                        "packing/devtools/check_pr_wall.py\n"
                        "packing/devtools/gate-budgets.yaml\n"
                    )
                    assert settings["sparse-checkout-cone-mode"] is False, name
                    assert settings["filter"] == "blob:none", name
                    continue
                assert settings["sparse-checkout"] == patterns, name
                assert settings["sparse-checkout-cone-mode"] is False, name
                assert settings["filter"] == "blob:none", name
                sparse.append(name)
    assert {"scope", "prepare", "workbench", *browser_check_jobs(jobs)} <= set(sparse)
    omitted_roots = (REPO / "packing/resources", REPO / "packing/campaign")
    for half, builder in BUILDER_INPUTS.items():
        omitted = []
        for declared in builder():
            for root in omitted_roots:
                if declared.is_relative_to(root):
                    relative = declared.relative_to(root)
                    if relative.parts and (root / relative.parts[0]).is_dir():
                        omitted.append(declared.relative_to(REPO).as_posix())
        assert omitted == [], f"{half}: render inputs omitted by sparse checkout: {omitted}"
    assert (REPO / "packing/resources/README.md").is_file()
    assert (REPO / "packing/campaign/README.md").is_file()


def test_prepared_geometry_checks_cover_each_browser_and_their_controls() -> None:
    """Downloading the page alone does not validate the geometry being published.

    The configurations are split across jobs so no browser waits on all of them; the
    coverage is asserted per browser over every job that measures it, so a setting
    dropped in the split fails here as it would have in one job.
    """
    jobs = load()["jobs"]
    module = "devtools.prepare_explainer_math"

    def option(command: list[str], flag: str, default: str) -> str:
        return command[command.index(flag) + 1] if flag in command else default

    settings = {
        (font_set, prose_font)
        for font_set in ("custom", "system")
        for prose_font in ("serif", "sans")
    }

    def context(command: list[str]) -> tuple[str, str]:
        return (
            option(command, "--font-set", "custom"),
            option(command, "--prose-font", "serif"),
        )

    measuring = {
        name: [
            shlex.split(line.replace("${{ matrix.browser }}", "matrix-browser"))
            for step in job.get("steps", [])
            for line in step.get("run", "").splitlines()
            if f"python -m {module} " in line
        ]
        for name, job in jobs.items()
        if name != "prepare"
    }
    measuring = {name: commands for name, commands in measuring.items() if commands}
    browsers = {
        "chromium": [name for name in measuring if "strategy" not in jobs[name]],
        "matrix-browser": [name for name in measuring if "strategy" in jobs[name]],
    }
    assert set(browsers["chromium"]) == {"geometry", "typography", "pdf"}
    assert set(browsers["matrix-browser"]) == {"font-loading", "browser-geometry"}
    for name in browsers["matrix-browser"]:
        assert set(jobs[name]["strategy"]["matrix"]["browser"]) == {"firefox", "webkit"}

    artifact_names: set[str] = set()
    for expected_browser, names in browsers.items():
        commands = [command for name in names for command in measuring[name]]
        assert all(
            command[command.index(module) + 1] == "site/index.html" for command in commands
        )
        assert all(
            option(command, "--browser", "chromium") == expected_browser for command in commands
        )
        outputs = [option(command, "--output", "") for command in commands]
        assert len(set(outputs)) == len(commands), (
            "geometry reports must not overwrite each other"
        )
        for command, output in zip(commands, outputs, strict=True):
            medium = "print" if "--print" in command else "screen"
            suffix = "-controls" if "--self-test" in command else ""
            if "--alternate-certificate" in command:
                suffix += "-alternate-certificate"
            assert output == (
                f"/tmp/math-geometry/{expected_browser}-{option(command, '--width', '1280')}-"
                f"{'-'.join(context(command))}-{medium}{suffix}.json"
            )
            width = option(command, "--width", "1280")
            if expected_browser == "matrix-browser" and width == "1280":
                assert command[-1] == "&"
            else:
                assert command[-2:] == ["||", "geometry_status=1"]
        for name in names:
            geometry_steps = [
                step
                for step in jobs[name]["steps"]
                if f"python -m {module} " in step.get("run", "")
            ]
            for step in geometry_steps:
                lines = step["run"].strip().splitlines()
                assert lines[0] == "trap 'exit 130' INT TERM", (
                    f"{name}: a cancelled run must stop measuring"
                )
                assert "mkdir -p /tmp/math-geometry" in lines
                assert "geometry_status=0" in lines
                assert lines[-1] == 'exit "$geometry_status"'
            uploads = [
                step
                for step in jobs[name]["steps"]
                if step.get("uses", "").startswith("actions/upload-artifact@")
                and step["with"]["name"].startswith("math-geometry-")
            ]
            assert len(uploads) == 1, name
            assert uploads[0]["if"] == "always()"
            assert uploads[0]["with"]["path"] == "/tmp/math-geometry"
            assert uploads[0]["with"]["if-no-files-found"] == "error"
            assert uploads[0]["with"]["retention-days"] == 7
            artifact_names.add(uploads[0]["with"]["name"])
        screen = [
            command
            for command in commands
            if "--print" not in command and "--alternate-certificate" not in command
        ]
        observed = {
            (*context(command), option(command, "--width", "1280")) for command in screen
        }
        expected = {(*setting, width) for setting in settings for width in ("1280", "390")}
        assert observed >= expected, (
            f"{expected_browser}: saved-setting geometry omitted {expected - observed}"
        )
        desktop = [
            command for command in screen if option(command, "--width", "1280") == "1280"
        ]
        assert any("--host-check" in command for command in desktop)
        if expected_browser == "chromium":
            assert any(
                "--host-check" in command and "--self-test" in command for command in desktop
            )
            assert {
                context(command) for command in commands if "--print" in command
            } >= settings
            assert any("--alternate-certificate" in command for command in commands)
    assert len(artifact_names) == 5, "each job's observations are retained under its own name"


def test_reload_guard_covers_both_viewports_on_the_published_artifact() -> None:
    jobs = load()["jobs"]
    for name in ("screen", "browser-geometry"):
        steps = jobs[name]["steps"]
        commands = [
            line
            for step in steps
            for line in step.get("run", "").splitlines()
            if "python -m devtools.check_scroll_restoration " in line
        ]
        assert len(commands) == 2
        assert all(" site/index.html " in command for command in commands)
        assert any("--self-test" in command for command in commands)
        assert any("--width 390" in command for command in commands)
        if name == "browser-geometry":
            assert all("--browser ${{ matrix.browser }}" in command for command in commands)
        uploads = [
            step
            for step in steps
            if step.get("with", {}).get("path") == "/tmp/scroll-restoration"
        ]
        assert len(uploads) == 1
        assert uploads[0]["if"] == "always()"


def test_dispatch_timing_uses_frozen_pairs_and_retains_failed_measurements() -> None:
    """Timing must use the published artifact on a separate runner, with no speed gate."""
    workflow = load()
    jobs = workflow["jobs"]
    job = jobs["startup-timing"]
    assert job["if"] == "github.event_name == 'workflow_dispatch'"
    assert job["needs"] == "prepare"
    assert job["runs-on"] == jobs["prepare"]["runs-on"]
    assert "strategy" not in job, "both widths must run sequentially on one fresh runner"
    assert not job.get("continue-on-error")
    assert job["defaults"]["run"]["working-directory"] == "packing"
    steps = job["steps"]
    for step in steps:
        if "uses" in step:
            assert re.fullmatch(r"[\w/-]+@[0-9a-f]{40}", step["uses"])
    setups = [step for step in steps if step.get("uses", "").startswith("astral-sh/setup-uv@")]
    assert len(setups) == 1
    reference = next(
        step
        for step in jobs["prepare"]["steps"]
        if step.get("uses", "").startswith("astral-sh/setup-uv@")
    )
    assert setups[0]["uses"] == reference["uses"]
    assert setups[0]["with"] == reference["with"]

    module = "devtools.check_math_startup"

    def commands(job_name: str) -> list[tuple[dict[str, object], list[str]]]:
        return [
            (step, shlex.split(line))
            for step in jobs[job_name]["steps"]
            for line in step.get("run", "").splitlines()
            if f"python -m {module} " in line
        ]

    def option(command: list[str], flag: str) -> str | None:
        return command[command.index(flag) + 1] if flag in command else None

    timing = commands("startup-timing")
    assert timing
    assert all(option(command, "--mode") == "parameters" for _, command in timing)
    controls = [(step, command) for step, command in timing if "--self-test" in command]
    assert len(controls) == 1
    assert controls[0][0]["id"] == "timing-controls"
    assert option(controls[0][1], "--output") == "/tmp/math-startup-timing/controls.json"
    assert any(
        "--self-test" in command and option(command, "--mode") == "parameters"
        for _, command in commands("typography")
    ), "the low-overhead observer's controls must also run on ordinary pull requests"

    pairs = [(step, command) for step, command in timing if "--self-test" not in command]
    assert [option(command, "--width") for _, command in pairs] == ["1280", "390"]
    for step, command in pairs:
        assert command[:6] == ["uv", "run", "--frozen", "--group", "dev", "python"]
        assert option(command, "--runs") == "12"
        assert option(command, "--browser") == "chromium"
        assert option(command, "--candidate") == "site/index.html"
        assert option(command, "--control") == "/tmp/math-startup-timing/control-33cd4760.html"
        assert option(command, "--output") == (
            f"/tmp/math-startup-timing/startup-{option(command, '--width')}.json"
        )
        assert not step.get("continue-on-error"), "invalid measurements must fail the job"
    assert (
        pairs[1][0]["if"] == "${{ !cancelled() && steps.timing-controls.outcome == 'success' }}"
    )
    shell = "\n".join(step.get("run", "") for step in steps)
    assert "python -m playwright install --only-shell chromium" in shell
    assert (
        "gzip --decompress --stdout benchmarks/math-startup/fixtures/control-33cd4760.html.gz"
        " > /tmp/math-startup-timing/control-33cd4760.html"
    ) in shell
    assert "cp site/index.html /tmp/math-startup-timing/candidate.html" in shell
    uploads = [
        step for step in steps if step.get("uses", "").startswith("actions/upload-artifact@")
    ]
    assert len(uploads) == 1
    assert uploads[0]["if"] == "always()"
    assert uploads[0]["with"]["path"] == "/tmp/math-startup-timing"
    assert uploads[0]["with"]["if-no-files-found"] == "error"
