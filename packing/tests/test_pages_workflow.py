"""Page checks must run when their own implementations change."""

from __future__ import annotations

import re
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
