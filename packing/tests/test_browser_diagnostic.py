"""Manual browser observations have fixed scope, external evidence and a hard deadline."""

from __future__ import annotations

import json
import os
import subprocess
from collections.abc import Sequence
from pathlib import Path

import pytest

from devtools import browser_diagnostic
from sqpack.cli import validate


@pytest.mark.parametrize(
    ("mode", "target", "seconds"),
    [
        ("forwarder-node", browser_diagnostic.FORWARDER_NODE, 120),
        ("forwarder-module", browser_diagnostic.FORWARDER_MODULE, 180),
    ],
)
def test_presets_cannot_inherit_broader_selection_or_optional_chromium(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mode: str,
    target: str,
    seconds: int,
) -> None:
    seen: list[tuple[validate.Context, Sequence[str], object]] = []

    def capture(context: validate.Context, command: Sequence[str], **options: object) -> str:
        seen.append((context, command, options["pytest_progress"]))
        return "passed"

    monkeypatch.setattr(browser_diagnostic, "_begin_artifacts", lambda *_args: None)
    monkeypatch.setattr(browser_diagnostic, "_run", capture)
    monkeypatch.setenv("PYTEST_ADDOPTS", "-n 9 -k absent --collect-only")
    monkeypatch.setenv("SQPACK_SITE_PREVIEW_URL", "https://unrelated.example")
    monkeypatch.setenv("PACKING_REACHABLE_TEST_ARTIFACT_STEM", "/old/command")
    monkeypatch.delenv(validate.REQUIRE_CHROMIUM, raising=False)
    assert browser_diagnostic.main(["--mode", mode, "--artifacts", str(tmp_path)]) == 0
    ((context, command, progress),) = seen
    assert command[-1] == target
    assert command[command.index("-n") + 1] == "0"
    assert {"-s", "-vv", "-x", "faulthandler_timeout=45"} <= set(command)
    assert "--collect-only" not in context.environment["PYTEST_ADDOPTS"]
    assert "SQPACK_SITE_PREVIEW_URL" not in context.environment
    assert "PACKING_REACHABLE_TEST_ARTIFACT_STEM" not in context.environment
    assert context.environment[validate.REQUIRE_CHROMIUM] == "1"
    assert context.environment["DEBUGP"] == context.environment["PYTHONUNBUFFERED"] == "1"
    assert context.environment["PACK_JOBS"] == "1"
    assert context.timeout_seconds == seconds
    assert context.timeout_is_explicit
    assert progress == ("browser-diagnostic", "all tests outside the fixed preset")


@pytest.mark.parametrize("mode", ["font", "tests", "forwarder-node; echo unsafe"])
def test_unknown_modes_are_refused_before_any_child_or_artifact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mode: str
) -> None:
    def unexpected(*_args: object) -> None:
        pytest.fail("invalid mode reached artifact creation")

    monkeypatch.setattr(browser_diagnostic, "_begin_artifacts", unexpected)
    artifacts = tmp_path / "artifacts"
    with pytest.raises(SystemExit) as refused:
        browser_diagnostic.main(["--mode", mode, "--artifacts", str(artifacts)])
    assert refused.value.code == 2
    assert not artifacts.exists()


def test_source_and_symlinked_artifact_paths_are_refused_before_writing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source"
    source.mkdir()
    alias = tmp_path / "alias"
    alias.symlink_to(source, target_is_directory=True)
    monkeypatch.setattr(validate, "REPOSITORY_ROOT", source)
    for requested in ("relative", str(source / "new"), str(alias / "new")):
        with pytest.raises(SystemExit) as refused:
            browser_diagnostic.main(["--mode", "forwarder-node", "--artifacts", requested])
        assert refused.value.code == 2
    assert not list(source.iterdir())


@pytest.mark.pool_heavy
def test_timeout_keeps_raw_output_and_unfinished_phase_bound_to_actual_head(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # A real child exercises deadline cleanup without starting Chromium or waiting for
    # the operational 120s cap. Only this test replaces the fixed diagnostic preset.
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import time\ndef test_wait():\n"
        "    print('raw transport evidence', flush=True)\n    time.sleep(30)\n"
    )
    monkeypatch.setattr(browser_diagnostic, "PRESETS", {"forwarder-node": (str(test_file), 2)})
    monkeypatch.setenv("GITHUB_SHA", "f" * 40)
    monkeypatch.setenv("GIT_DIR", "/not-the-source-repository")
    monkeypatch.setenv("PYTEST_ADDOPTS", "--collect-only")
    artifacts = tmp_path / "artifacts"
    assert (
        browser_diagnostic.main(["--mode", "forwarder-node", "--artifacts", str(artifacts)])
        == 1
    )
    assert "raw transport evidence" in next(artifacts.glob("*.log")).read_text()
    end = json.loads(next(artifacts.glob("*.end.json")).read_text())
    assert end["status"] == "timed_out"
    assert end["timeout_seconds"] == 2
    assert not list(artifacts.glob("*.junit.xml"))
    rows = [
        json.loads(line)
        for line in next(artifacts.glob("*.progress-main.jsonl")).read_text().splitlines()
    ]
    assert rows[-1]["phase"] == "setup"
    assert rows[-1]["nodeid"].endswith("::test_wait")
    head = subprocess.check_output(
        ("git", "rev-parse", "HEAD"),
        cwd=validate.REPOSITORY_ROOT,
        env={key: value for key, value in os.environ.items() if not key.startswith("GIT_")},
        text=True,
    ).strip()
    assert {row["source_commit"] for row in rows} == {head}
    assert {row["xdist_workers"] for row in rows} == {1}
    run = json.loads(next(artifacts.glob("run-*.json")).read_text())
    assert run["commit"] == head
