"""Page checks must run when their own implementations change."""

from __future__ import annotations

import re
import shlex
from fnmatch import fnmatchcase
from pathlib import Path

from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]


def test_pages_filters_cover_the_developer_tools_its_jobs_run() -> None:
    """A checker omitted from the filter can change without ever checking its result."""
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
    modules = {
        module
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
        for module in re.findall(r"\bpython\s+-m\s+(devtools\.[\w.]+)", step.get("run", ""))
    }
    assert modules, "the page workflow runs no developer tools"
    scripts = {f"packing/{module.replace('.', '/')}.py" for module in modules}
    assert all((REPO / script).is_file() for script in scripts)
    for event in ("push", "pull_request"):
        patterns = workflow["on"][event]["paths"]
        missing = sorted(
            script for script in scripts if not any(fnmatchcase(script, p) for p in patterns)
        )
        assert not missing, f"{event}: page tools outside the workflow path filter: {missing}"


def test_deployment_waits_for_the_cross_browser_loading_checks() -> None:
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
    checks = workflow["jobs"]["font-loading"]
    assert set(checks["strategy"]["matrix"]["browser"]) == {"firefox", "webkit"}
    assert "font-loading" in workflow["jobs"]["deploy"]["needs"]
    assert any("devtools.check_math_loading" in step.get("run", "") for step in checks["steps"])


def test_pages_runs_real_math_failure_controls_before_drawing_the_pdf() -> None:
    """The real-browser controls must run, rather than silently taking their default skip."""
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
    job = workflow["jobs"]["build"]
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
        and candidate["with"] == {"name": "prepared-page", "path": "packing/site"}
    ]
    installs = [
        before
        for before, candidate in enumerate(steps)
        if "playwright install --only-shell chromium" in candidate.get("run", "")
    ]
    draws = [
        after
        for after, candidate in enumerate(steps)
        if "devtools.render_explainer_pdf --update" in candidate.get("run", "")
    ]
    assert downloads
    assert installs
    assert draws
    assert max(downloads + installs) < index < min(draws)
    assert (REPO / "packing" / test_path).is_file()
    for event in ("push", "pull_request"):
        assert any(
            fnmatchcase(f"packing/{test_path}", pattern)
            for pattern in workflow["on"][event]["paths"]
        ), f"{event}: editing the browser controls must run them"


def test_pages_checks_the_pdf_it_uploads_and_retains_mismatch_evidence() -> None:
    """A later pair of fresh draws must not stand in for the artifact being published."""
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
    steps = workflow["jobs"]["build"]["steps"]
    module = "devtools.render_explainer_pdf"
    commands = [
        (index, shlex.split(line))
        for index, step in enumerate(steps)
        for line in step.get("run", "").splitlines()
        if f"python -m {module} " in line
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
        if step.get("uses", "").startswith("actions/upload-pages-artifact@")
    ]
    assert len(uploads) == 1
    assert draw_index < check_index < uploads[0]
    assert steps[uploads[0]]["with"]["path"] == "packing/site"
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


def test_every_browser_checks_the_same_prepared_publication() -> None:
    """A raw re-render in one job would leave the actual published boxes untested."""
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
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
    assert any("--check" in line for _, _, line in renders)
    producers = {name for name, _, _ in renders}
    assert len(producers) == 1, "browser checks must share one prepared artifact"
    producer = next(iter(producers))
    steps = jobs[producer]["steps"]
    installs = [
        index
        for index, step in enumerate(steps)
        if "playwright install" in step.get("run", "") and "chromium" in step["run"]
    ]
    assert installs
    assert min(installs) < min(index for _, index, _ in renders)
    uploads = [
        step["with"]
        for step in steps
        if step.get("uses", "").startswith("actions/upload-artifact@")
    ]
    assert len(uploads) == 1
    assert uploads[0]["path"] == "packing/site"
    for name in ("build", "font-loading", "startup-timing"):
        needs = jobs[name]["needs"]
        assert producer in ([needs] if isinstance(needs, str) else needs)
        downloads = [
            step["with"]
            for step in jobs[name]["steps"]
            if step.get("uses", "").startswith("actions/download-artifact@")
        ]
        assert downloads == [{"name": uploads[0]["name"], "path": "packing/site"}]


def test_prepared_geometry_checks_cover_each_browser_and_their_controls() -> None:
    """Downloading the page alone does not validate the geometry being published."""
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
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

    for name in ("build", "font-loading"):
        commands = [
            shlex.split(line.replace("${{ matrix.browser }}", "matrix-browser"))
            for step in workflow["jobs"][name]["steps"]
            for line in step.get("run", "").splitlines()
            if f"python -m {module} " in line
        ]
        assert commands, f"{name}: prepared geometry is never checked"
        assert all(
            command[command.index(module) + 1] == "site/index.html" for command in commands
        )
        expected_browser = "chromium" if name == "build" else "matrix-browser"
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
            assert command[-2:] == ["||", "geometry_status=1"]
        geometry_steps = [
            step
            for step in workflow["jobs"][name]["steps"]
            if f"python -m {module} " in step.get("run", "")
        ]
        for step in geometry_steps:
            assert "mkdir -p /tmp/math-geometry" in step["run"]
            assert "geometry_status=0" in step["run"]
            assert step["run"].strip().endswith('exit "$geometry_status"')
        uploads = [
            step
            for step in workflow["jobs"][name]["steps"]
            if step.get("uses", "").startswith("actions/upload-artifact@")
            and step["with"]["name"].startswith("math-geometry-")
        ]
        assert len(uploads) == 1
        assert uploads[0]["if"] == "always()"
        assert uploads[0]["with"] == {
            "name": "math-geometry-chromium"
            if name == "build"
            else "math-geometry-${{ matrix.browser }}",
            "path": "/tmp/math-geometry",
            "if-no-files-found": "error",
            "retention-days": 7,
        }
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
            f"{name}: saved-setting geometry omitted {expected - observed}"
        )
        desktop = [
            command for command in screen if option(command, "--width", "1280") == "1280"
        ]
        assert any("--host-check" in command for command in desktop)
        if name == "build":
            assert any(
                "--host-check" in command and "--self-test" in command for command in desktop
            )
            assert {
                context(command) for command in commands if "--print" in command
            } >= settings
            assert any("--alternate-certificate" in command for command in commands)


def test_reload_guard_covers_both_viewports_on_the_published_artifact() -> None:
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
    for name in ("build", "font-loading"):
        steps = workflow["jobs"][name]["steps"]
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
        if name == "font-loading":
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
    workflow = safe_load((REPO / ".github/workflows/pages.yml").read_text("utf-8"))
    jobs = workflow["jobs"]
    job = jobs["startup-timing"]
    assert job["if"] == "github.event_name == 'workflow_dispatch'"
    assert job["needs"] == "prepare"
    assert job["runs-on"] == jobs["build"]["runs-on"]
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
        for _, command in commands("build")
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
