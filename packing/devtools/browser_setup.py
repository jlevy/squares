"""Install locked browser tools with cached apt archives and bounded process groups.

The archive cache is only a download optimization: Playwright still resolves and
installs its required system packages on every invocation, including a warm cache.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from dataclasses import asdict, dataclass
from pathlib import Path

from devtools.supervise_posix import process_group_rss

SUDO = ("sudo", "-n")
CONTROL_TIMEOUT_SECONDS = 5
DEFAULT_INSTALL_SECONDS = 180
REPO = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Command:
    name: str
    argv: tuple[str, ...]
    cwd: Path


@dataclass(frozen=True)
class Result:
    name: str
    returncode: int | None
    elapsed_seconds: float
    timed_out: bool
    log: str
    error: str | None = None


def privileged(argv: Sequence[str], *, text: str | None = None) -> None:
    subprocess.run(
        [*SUDO, *argv],
        input=text,
        text=True,
        stdout=subprocess.DEVNULL,
        check=True,
        timeout=CONTROL_TIMEOUT_SECONDS,
    )


def normalize_ubuntu_mirror(
    mirror_list: Path = Path("/etc/apt/apt-mirrors.txt"),
) -> None:
    """Promote the runner's existing canonical archive alternative over slow Azure HTTP."""
    if not mirror_list.exists():
        print("apt mirror normalization: runner mirror list absent; unchanged", flush=True)
        return
    original = mirror_list.read_text()
    pattern = r"(?m)^([ \t]*)https?://azure\.archive\.ubuntu\.com/ubuntu(/?)(?=[ \t\r\n]|$)"
    updated, count = re.subn(
        pattern,
        r"\1https://archive.ubuntu.com/ubuntu\2",
        original,
    )
    if not count:
        print("apt mirror normalization: no known Azure archive entry; unchanged", flush=True)
        return
    # Only these fixed, public endpoints are logged; other mirror entries can
    # contain credentials. Preserve their bytes, priorities, and the security mirror.
    before_urls = [match.group(0).lstrip() for match in re.finditer(pattern, original)]
    print(f"apt mirror before: {', '.join(before_urls)}", flush=True)
    privileged(["tee", str(mirror_list)], text=updated)
    print("apt mirror after: https://archive.ubuntu.com/ubuntu", flush=True)


def configure_archives(
    archives: Path, *, config_directory: Path = Path("/etc/apt/apt.conf.d")
) -> None:
    archives.mkdir(parents=True, exist_ok=True)
    (archives / "partial").mkdir(exist_ok=True)
    privileged(
        ["tee", str(config_directory / "90-packing-archives")],
        text=f'Dir::Cache::Archives "{archives}/";\n',
    )
    # The hosted image's post-install hook otherwise deletes the files we cache.
    privileged(["rm", "-f", str(config_directory / "docker-clean")])


def clean_archives(archives: Path) -> None:
    privileged(["rm", "-rf", str(archives / "partial"), str(archives / "lock")])
    privileged(["chown", "-R", f"{os.getuid()}:{os.getgid()}", str(archives)])


def kill_install_group(pid: int) -> None:
    with suppress(ProcessLookupError, PermissionError):
        os.killpg(pid, signal.SIGKILL)
    # killpg can succeed for the unprivileged members while leaving root-owned
    # apt children alive. Reuse the existing group observer before escalating.
    if process_group_rss(pid):
        privileged(["kill", "-KILL", "--", f"-{pid}"])


def run_install(command: Command, *, max_seconds: float, artifacts: Path) -> Result:
    started = time.monotonic()
    log = artifacts / f"{command.name}.log"
    returncode = None
    timed_out = False
    error = None
    process: subprocess.Popen[bytes] | None = None
    try:
        with log.open("wb") as output:
            process = subprocess.Popen(
                command.argv,
                cwd=command.cwd,
                stdout=output,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )
            try:
                returncode = process.wait(timeout=max_seconds)
            except subprocess.TimeoutExpired:
                timed_out = True
    except (OSError, subprocess.SubprocessError) as failure:
        error = str(failure)
    finally:
        if process is not None:
            try:
                # A successful leader can leave children behind, including privileged
                # installers. Completion requires the whole owned group to be gone.
                kill_install_group(process.pid)
                returncode = process.wait(timeout=CONTROL_TIMEOUT_SECONDS)
                cleanup_deadline = time.monotonic() + CONTROL_TIMEOUT_SECONDS
                while process_group_rss(process.pid):
                    if time.monotonic() >= cleanup_deadline:
                        raise TimeoutError(f"process group {process.pid} survived cleanup")
                    time.sleep(0.01)
            except (OSError, subprocess.SubprocessError) as failure:
                error = f"{error or ''} process cleanup failed: {failure}".strip()
    return Result(
        command.name, returncode, time.monotonic() - started, timed_out, str(log), error
    )


def run_installs(
    commands: Sequence[Command], *, max_seconds: float, artifacts: Path
) -> list[Result]:
    if not commands or not math.isfinite(max_seconds) or max_seconds <= 0:
        raise ValueError(
            "at least one command and a finite positive install ceiling are required"
        )
    artifacts.mkdir(parents=True, exist_ok=True)
    # One future per independent installer; both results survive either install failing.
    with ThreadPoolExecutor(max_workers=len(commands)) as pool:
        futures = [
            pool.submit(run_install, command, max_seconds=max_seconds, artifacts=artifacts)
            for command in commands
        ]
        results = [future.result() for future in futures]
    for result in results:
        print(
            f"{result.name}: {result.elapsed_seconds:.2f}s, exit={result.returncode}, "
            f"timeout={result.timed_out}, error={result.error}",
            flush=True,
        )
        # Full logs remain in the uploaded artifact; bound the console tail.
        with Path(result.log).open("rb") as log:
            log.seek(max(0, log.seek(0, 2) - 16384))
            print(log.read().decode("utf-8", errors="replace"), flush=True)
    return results


def successful(results: Sequence[Result]) -> bool:
    return bool(results) and all(
        result.returncode == 0 and not result.timed_out and result.error is None
        for result in results
    )


def install_commands(*, include_npm: bool) -> list[Command]:
    commands = [
        Command(
            "playwright",
            (
                sys.executable,
                "-m",
                "playwright",
                "install",
                "--with-deps",
                "--only-shell",
                "chromium",
            ),
            REPO / "packing",
        )
    ]
    if include_npm:
        commands.append(Command("npm", ("npm", "ci", "--ignore-scripts"), REPO))
    return commands


def archive_sizes(archives: Path) -> dict[str, int]:
    sizes = [path.stat().st_size for path in archives.glob("*.deb")]
    return {"packages": len(sizes), "bytes": sum(sizes)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--npm", action="store_true", help="install npm concurrently with Playwright"
    )
    parser.add_argument("--max-seconds", type=float, default=DEFAULT_INSTALL_SECONDS)
    parser.add_argument("--artifacts", type=Path, required=True)
    args = parser.parse_args(argv)
    artifacts = args.artifacts.resolve() / "browser-setup"
    artifacts.mkdir(parents=True, exist_ok=True)
    archives = Path.home() / "apt-archives"
    results: list[Result] = []
    failure = None
    before = archive_sizes(archives)
    print(
        f"apt archive cache before setup: {before}; install ceiling={args.max_seconds}s",
        flush=True,
    )
    try:
        normalize_ubuntu_mirror()
        configure_archives(archives)
        results = run_installs(
            install_commands(include_npm=args.npm),
            max_seconds=args.max_seconds,
            artifacts=artifacts,
        )
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        failure = str(error)
    finally:
        try:
            clean_archives(archives)
        except (OSError, subprocess.SubprocessError) as error:
            failure = f"{failure or ''} archive cleanup failed: {error}".strip()
        receipt = {
            "image": (
                f"{os.environ.get('ImageOS', '')}-"  # noqa: SIM112 -- hosted runner names.
                f"{os.environ.get('ImageVersion', '')}"  # noqa: SIM112
            ),
            "archive_cache_before": before,
            "archive_cache_after": archive_sizes(archives),
            "max_seconds_per_install": args.max_seconds,
            "results": [asdict(result) for result in results],
            "failure": failure,
        }
        (artifacts / "setup.json").write_text(json.dumps(receipt, indent=2) + "\n")
    if failure:
        print(f"Browser setup failed: {failure}", file=sys.stderr)
    return 0 if failure is None and successful(results) else 1


if __name__ == "__main__":
    sys.exit(main())
