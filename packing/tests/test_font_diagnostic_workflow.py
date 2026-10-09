"""The manual font-delivery diagnostic qualifies nothing and stays out of every gate.

`.github/workflows/font-diagnostic.yml` observes the n11 threshold paper's first screen
while its web fonts are held. It used to be a dispatch mode of `pages.yml`, where a
dispatch was a Certificate page run: it joined `certificate-page-<ref>`, so on `main` it
could replace a pending push run and lose that push's deploy, and
`devtools.rerun_starved` counted it as a newer run superseding a starved pull-request
run at the same commit (review B's B2, review A's A2 on PR 468). These tests hold the
separation, and the bounds of the one job.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from devtools import check_site_rendering, rerun_starved
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
WORKFLOWS = REPO / ".github" / "workflows"
DIAGNOSTIC = WORKFLOWS / "font-diagnostic.yml"
JOB = "font-diagnostic"
#: The immutable #449 inputs the diagnostic renders the paper from.
PINNED_INPUTS = "4963448e33c39002a48593ef79999940b153f2c0"


def workflow(path: Path) -> dict[str, Any]:
    document = safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    # YAML 1.1 reads an unquoted `on:` as `True`; every reader here looks up `"on"`.
    assert "on" in document, f"{path.name} must quote its `on:` key"
    return document


def diagnostic_job() -> dict[str, Any]:
    return workflow(DIAGNOSTIC)["jobs"][JOB]


def checkouts(job: dict[str, Any]) -> list[dict[str, Any]]:
    return [step for step in job["steps"] if "checkout@" in step.get("uses", "")]


def test_the_diagnostic_is_dispatch_only_with_no_inputs_and_one_read_only_job() -> None:
    document = workflow(DIAGNOSTIC)
    # No input at all: nothing a dispatcher types reaches a condition or a shell.
    assert document["on"] == {"workflow_dispatch": None}
    assert document["permissions"] == {"contents": "read"}
    assert list(document["jobs"]) == [JOB]
    job = document["jobs"][JOB]
    assert "if" not in job
    assert "needs" not in job
    assert job["permissions"] == {"contents": "read"}


def test_a_dispatch_shares_no_concurrency_group_with_any_other_workflow() -> None:
    """On `main`, `certificate-page-<ref>` holds the push run whose deploy must not be lost."""
    group = workflow(DIAGNOSTIC)["concurrency"]["group"]
    assert group == "font-diagnostic-${{ github.ref }}"
    assert workflow(DIAGNOSTIC)["concurrency"]["cancel-in-progress"] is False
    prefix = group.split("${{")[0]
    for path in sorted(WORKFLOWS.glob("*.yml")):
        if path == DIAGNOSTIC:
            continue
        document = workflow(path)
        groups = [document.get("concurrency")] + [
            job.get("concurrency") for job in document["jobs"].values()
        ]
        for other in groups:
            if other is None:
                continue
            name = other if isinstance(other, str) else other["group"]
            assert not name.startswith(prefix), (path.name, name)
            static = name.split("${{")[0]
            assert not static or not prefix.startswith(static), (path.name, name)


def test_the_re_run_listener_never_reads_a_diagnostic_as_a_superseding_run() -> None:
    document = workflow(DIAGNOSTIC)
    listener = workflow(WORKFLOWS / "rerun-starved.yml")
    assert document["name"] not in rerun_starved.WORKFLOWS
    assert document["name"] not in listener["on"]["workflow_run"]["workflows"]
    starved = {
        "id": 1,
        "name": "Certificate page",
        "path": ".github/workflows/pages.yml",
        "event": "pull_request",
        "created_at": "2026-10-09T10:00:00Z",
        "head_branch": "codex/intake-font-diagnostic-449",
        "head_sha": "3a2ab4ff0d03a41463d2f43d3e773064d0abd02b",
    }
    dispatch = {
        **starved,
        "id": 2,
        "name": document["name"],
        "path": ".github/workflows/font-diagnostic.yml",
        "event": "workflow_dispatch",
        "created_at": "2026-10-09T10:05:00Z",
    }
    # The same commit and branch: inside `pages.yml` this dispatch suppressed the re-run.
    assert rerun_starved.newer_runs(starved, [starved, dispatch]) == ()


def test_the_certificate_page_workflow_carries_no_diagnostic_mode() -> None:
    pages = workflow(WORKFLOWS / "pages.yml")
    assert "font_diagnostic" not in pages["on"]["workflow_dispatch"]["inputs"]
    assert JOB not in pages["jobs"]
    assert "font_diagnostic" not in (WORKFLOWS / "pages.yml").read_text(encoding="utf-8")


def test_the_diagnostic_is_one_bounded_paper_only_observation() -> None:
    job = diagnostic_job()
    pages_job = workflow(WORKFLOWS / "pages.yml")["jobs"]["n11-threshold-bound-review"]
    assert job["runs-on"] == pages_job["runs-on"]
    assert job["timeout-minutes"] == 5
    steps = job["steps"]
    current, pinned = checkouts(job)
    original_checkout = checkouts(pages_job)[0]
    assert current["uses"] == pinned["uses"] == original_checkout["uses"]
    assert current["with"]["sparse-checkout"] == original_checkout["with"]["sparse-checkout"]
    assert current["with"]["persist-credentials"] is False
    assert pinned["with"]["ref"] == PINNED_INPUTS
    assert pinned["with"]["sparse-checkout"] == original_checkout["with"]["sparse-checkout"]
    assert pinned["with"]["submodules"] is True
    commands = [step["run"] for step in steps if "run" in step]
    bounded = [command for command in commands if command.startswith("timeout ")]
    assert len(bounded) == 2
    assert all(command.startswith("timeout --kill-after=5s 60s ") for command in bounded)
    assert "-m devtools.render_n11_threshold_bound_review --site diagnostics/site" in bounded[0]
    assert f"--revision {PINNED_INPUTS}" in bounded[0]
    assert "--pdf" not in bounded[0]
    assert (
        "--font-diagnostic diagnostics/font-delivery.json --font-scenario 390-light"
        in bounded[1]
    )
    assert "--page papers/n11-threshold-bound-review.html" in bounded[1]
    assert "python diagnostics/tool/check_site_rendering.py diagnostics/site" in bounded[1]
    # The retained protocol says what each row is: every rendered text node below the
    # declared node, as the tool records it (review B3), not a container's own read.
    protocol = next(step["run"] for step in steps if "protocol.txt" in step.get("run", ""))
    assert "every rendered text node below it" in protocol
    assert "every rendered text node below it" in check_site_rendering.FONT_DIAGNOSTIC_PROTOCOL
    assert "Hero aggregates" not in protocol
    probe_step = next(
        step
        for step in steps
        if step.get("name") == "Observe controlled font delivery at 390px light"
    )
    assert probe_step["env"]["PYTHONPATH"] == (
        "${{ github.workspace }}/packing/src:${{ github.workspace }}/packing"
    )
    for step in steps:
        if "uses" in step:
            assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", step["uses"]), step["uses"]
    upload = next(step for step in steps if "upload-artifact@" in step.get("uses", ""))
    assert upload["if"] == "always()"
    assert upload["with"]["path"] == "packing/diagnostics"
    assert upload["with"]["if-no-files-found"] == "error"


def test_transported_font_diagnostic_cli_keeps_its_declared_probe_root(tmp_path: Path) -> None:
    source = REPO / "packing"
    tool = tmp_path / "tool"
    tool.mkdir()
    shutil.copy2(source / "devtools/check_site_rendering.py", tool)
    shutil.copytree(
        source / "devtools/probes/check_site_rendering",
        tool / "probes/check_site_rendering",
    )
    environment = dict(os.environ, PYTHONPATH=f"{source / 'src'}:{source}")
    result = subprocess.run(
        [sys.executable, str(tool / "check_site_rendering.py"), "--help"],
        cwd=source,
        env=environment,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "--font-diagnostic" in result.stdout
    assert "--font-scenario" in result.stdout
