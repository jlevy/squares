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
    for name in ("build", "font-loading"):
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
        screen = [
            command
            for command in commands
            if "--print" not in command and "--alternate-certificate" not in command
        ]
        assert {option(command, "--width", "1280") for command in screen} >= {"1280", "390"}
        desktop = [
            command for command in screen if option(command, "--width", "1280") == "1280"
        ]
        assert any("--host-check" in command for command in desktop)
        if name == "build":
            assert any(
                "--host-check" in command and "--self-test" in command for command in desktop
            )
            assert any("--print" in command for command in commands)
            assert any("--alternate-certificate" in command for command in commands)
