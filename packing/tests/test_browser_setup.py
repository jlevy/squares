"""Browser provisioning preserves cache inputs and refuses incomplete installs."""

from __future__ import annotations

import json
import os
import signal
import sys
from contextlib import suppress
from pathlib import Path

import pytest

from devtools import browser_setup as tool
from sqpack.yamlio import safe_load


def test_install_failures_keep_both_process_results_and_logs(tmp_path: Path) -> None:
    commands = [
        tool.Command(
            "npm", (sys.executable, "-c", "print('npm failed'); raise SystemExit(7)"), tmp_path
        ),
        tool.Command("playwright", (sys.executable, "-c", "print('browser ready')"), tmp_path),
    ]
    results = tool.run_installs(commands, max_seconds=5, artifacts=tmp_path)
    assert {result.name: result.returncode for result in results} == {"npm": 7, "playwright": 0}
    assert not tool.successful(results)
    assert "npm failed" in (tmp_path / "npm.log").read_text()
    assert "browser ready" in (tmp_path / "playwright.log").read_text()
    assert all(result.elapsed_seconds > 0 for result in results)
    assert not tool.successful([])


@pytest.mark.pool_heavy
@pytest.mark.skipif(os.name != "posix", reason="hosted browser setup requires POSIX groups")
def test_timeout_kills_a_term_ignoring_process_and_keeps_partial_log(tmp_path: Path) -> None:
    command = tool.Command(
        "playwright",
        (
            sys.executable,
            "-c",
            (
                "import signal,time; signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                "print('download started',flush=True); time.sleep(30)"
            ),
        ),
        tmp_path,
    )
    results = tool.run_installs([command], max_seconds=0.5, artifacts=tmp_path)
    assert not tool.successful(results)
    result = results[0]
    assert result.timed_out
    assert result.returncode == -signal.SIGKILL
    assert result.elapsed_seconds < 5
    assert "download started" in (tmp_path / "playwright.log").read_text()


@pytest.mark.parametrize("warm", [False, True])
def test_archive_configuration_preserves_downloads_and_cleans_transient_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, warm: bool
) -> None:
    # Run real tee/rm/chown against a private config tree, without privileges.
    monkeypatch.setattr(tool, "SUDO", ())
    config = tmp_path / "apt.conf.d"
    config.mkdir()
    (config / "docker-clean").write_text('DPkg::Post-Invoke { "delete archives"; };')
    archives = tmp_path / "apt-archives"
    if warm:
        archives.mkdir()
        (archives / "cached.deb").write_bytes(b"previously downloaded package")
    tool.configure_archives(archives, config_directory=config)
    assert (archives / "partial").is_dir()
    assert f'"{archives}/"' in (config / "90-packing-archives").read_text()
    assert not (config / "docker-clean").exists()
    (archives / "partial" / "unfinished").write_bytes(b"partial download")
    (archives / "lock").touch()
    tool.clean_archives(archives)
    assert not (archives / "partial").exists()
    assert not (archives / "lock").exists()
    assert (archives / "cached.deb").exists() is warm


def test_packing_uses_pages_archive_identity_without_skipping_installs() -> None:
    repo = Path(__file__).resolve().parents[2]
    pages = safe_load((repo / ".github/workflows/pages.yml").read_text())["jobs"]
    pages_cache = next(
        step["with"]
        for job in pages.values()
        for step in job.get("steps", [])
        if step.get("with", {}).get("path") == "~/apt-archives"
    )
    jobs = safe_load((repo / ".github/workflows/packing-validation.yml").read_text())["jobs"]
    for name in ("validate", "integration-suites", "frontend"):
        steps = jobs[name]["steps"]
        cache = next(
            step["with"]
            for step in steps
            if step.get("with", {}).get("path") == "~/apt-archives"
        )
        assert cache["key"] == pages_cache["key"].replace("${{ matrix.browser }}", "chromium")
        assert cache["restore-keys"] == pages_cache["restore-keys"].replace(
            "${{ matrix.browser }}", "chromium"
        )
        install = next(
            step for step in steps if "-m devtools.browser_setup" in step.get("run", "")
        )
        assert "cache-hit" not in install.get("if", "")
        assert 0 < install["timeout-minutes"] <= 4


@pytest.mark.pool_heavy
def test_installers_overlap_and_missing_tools_cannot_pass(tmp_path: Path) -> None:
    commands = [
        tool.Command(
            name,
            (
                sys.executable,
                "-c",
                (
                    "import pathlib,sys,time; mine,peer=map(pathlib.Path,sys.argv[1:]); "
                    "mine.touch(); deadline=time.monotonic()+2; "
                    "exec('while not peer.exists() and time.monotonic()<deadline: "
                    "time.sleep(.01)'); "
                    "raise SystemExit(0 if peer.exists() else 8)"
                ),
                str(tmp_path / name),
                str(tmp_path / peer),
            ),
            tmp_path,
        )
        for name, peer in (("npm", "playwright"), ("playwright", "npm"))
    ]
    assert tool.successful(tool.run_installs(commands, max_seconds=5, artifacts=tmp_path))
    missing = tool.run_installs(
        [tool.Command("missing", (str(tmp_path / "absent-command"),), tmp_path)],
        max_seconds=5,
        artifacts=tmp_path,
    )
    assert not tool.successful(missing)
    assert missing[0].error


def test_root_owned_timeout_children_are_signalled_even_if_killpg_succeeds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []
    monkeypatch.setattr(tool.os, "killpg", lambda _pid, _signal: None)
    monkeypatch.setattr(tool, "process_group_rss", lambda _pid: {456: 1024})
    monkeypatch.setattr(tool, "privileged", calls.append)
    tool.kill_install_group(123)
    assert calls == [["kill", "-KILL", "--", "-123"]]


def test_main_refuses_failed_install_and_retains_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(tool, "normalize_ubuntu_mirror", lambda: None)
    monkeypatch.setattr(tool, "configure_archives", lambda _archives: None)
    monkeypatch.setattr(tool, "clean_archives", lambda _archives: None)
    commands = [tool.Command("npm", (sys.executable, "-c", "raise SystemExit(9)"), tmp_path)]
    monkeypatch.setattr(tool, "install_commands", lambda **_kwargs: commands)
    assert tool.main(["--npm", "--artifacts", str(tmp_path)]) == 1
    receipt = json.loads((tmp_path / "browser-setup/setup.json").read_text())
    assert receipt["results"][0]["returncode"] == 9
    assert (tmp_path / "browser-setup/npm.log").is_file()


@pytest.mark.pool_heavy
@pytest.mark.skipif(os.name != "posix", reason="hosted browser setup requires POSIX groups")
def test_successful_leader_exit_cleans_its_surviving_child(tmp_path: Path) -> None:
    command = tool.Command(
        "playwright",
        (
            sys.executable,
            "-c",
            (
                "import os,subprocess,sys; "
                "subprocess.Popen([sys.executable,'-c','import time; time.sleep(30)']); "
                "print(os.getpid(),flush=True)"
            ),
        ),
        tmp_path,
    )
    result = tool.run_install(command, max_seconds=5, artifacts=tmp_path)
    group = int((tmp_path / "playwright.log").read_text().strip())
    try:
        assert tool.successful([result])
        assert tool.process_group_rss(group) == {}
    finally:
        # A failing regression must not leave the deliberately orphaned child running.
        with suppress(ProcessLookupError):
            os.killpg(group, signal.SIGKILL)


def test_mirror_normalization_changes_only_known_azure_archive_urls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(tool, "SUDO", ())
    mirror_list = tmp_path / "apt-mirrors.txt"
    original = (
        "# runner mirror priority list\n"
        "  http://azure.archive.ubuntu.com/ubuntu/\tpriority:1\n"
        "https://archive.ubuntu.com/ubuntu/\tpriority:2\n"
        "https://security.ubuntu.com/ubuntu/\tpriority:3\n"
        "https://azure.archive.ubuntu.com/ubuntu priority:4\n"
        "https://user:secret@private.example/ubuntu/ priority:5\n"
        "http://azure.archive.ubuntu.com/other/ priority:6\n"
        "http://azure.archive.ubuntu.com.attacker.example/ubuntu/ priority:7\n"
    )
    mirror_list.write_text(original)
    tool.normalize_ubuntu_mirror(mirror_list)
    expected = original.replace(
        "http://azure.archive.ubuntu.com/ubuntu/\tpriority:1",
        "https://archive.ubuntu.com/ubuntu/\tpriority:1",
    ).replace(
        "https://azure.archive.ubuntu.com/ubuntu priority:4",
        "https://archive.ubuntu.com/ubuntu priority:4",
    )
    assert mirror_list.read_text() == expected
    output = capsys.readouterr().out
    assert "apt mirror before:" in output
    assert "apt mirror after: https://archive.ubuntu.com/ubuntu" in output
    assert "secret" not in output
    tool.normalize_ubuntu_mirror(mirror_list)
    assert mirror_list.read_text() == expected
    absent = tmp_path / "absent-list"
    tool.normalize_ubuntu_mirror(absent)
    assert not absent.exists()
