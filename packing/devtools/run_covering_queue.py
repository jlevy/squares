"""Walk a ranked covering-queue YAML through run_fractional_colgen.

The producer is already `devtools.run_fractional_colgen`. A one-core host still
needs a scheduler that skips a probe whose run JSON exists, refuses to start a
second generator, and halts only when a freeze mass is strictly below n — that
is the retain boundary, not a freeze that sits above n.

A shell waiter is not an entry point this repository keeps.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path

from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parent.parent
DEFAULT_STOP_AT = "2026-09-19T06:42:00Z"
EXIT_DONE = 0
EXIT_STOP = 2
EXIT_FREEZE_BELOW = 3


@dataclass(frozen=True, slots=True)
class Probe:
    """One named covering construction from a queue file."""

    id: str
    n: int
    side: str
    grid_counts: str
    seed_certificate: str | None
    seed_windows: int
    deadline_seconds: int


def parse_stop_at(text: str) -> datetime:
    """ISO-8601 instant; a trailing Z is UTC."""

    parsed = datetime.fromisoformat(text)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def remain_seconds(stop_at: datetime, now: datetime | None = None) -> int:
    clock = now if now is not None else datetime.now(UTC)
    return int((stop_at - clock).total_seconds())


def load_queue(path: Path) -> list[Probe]:
    """The `probes` list. Extra keys (bead, notes) are ignored."""

    payload = safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{path}: queue root must be a mapping")
    raw = payload.get("probes")
    if not isinstance(raw, list):
        raise TypeError(f"{path}: needs a nonempty probes list")
    if not raw:
        raise ValueError(f"{path}: needs a nonempty probes list")
    probes: list[Probe] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise TypeError(f"{path}: probes[{index}] must be a mapping")
        probes.append(_probe_from(item, path, index))
    return probes


def _require_str(item: Mapping[object, object], key: str, path: Path, index: int) -> str:
    value = item.get(key)
    if not isinstance(value, str):
        raise TypeError(f"{path}: probes[{index}].{key} must be a nonempty string")
    if not value:
        raise ValueError(f"{path}: probes[{index}].{key} must be a nonempty string")
    return value


def _require_int(item: Mapping[object, object], key: str, path: Path, index: int) -> int:
    value = item.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{path}: probes[{index}].{key} must be an int")
    return value


def _optional_str(
    item: Mapping[object, object], key: str, path: Path, index: int
) -> str | None:
    if key not in item or item[key] is None or item[key] == "":
        return None
    return _require_str(item, key, path, index)


def _probe_from(item: Mapping[object, object], path: Path, index: int) -> Probe:
    return Probe(
        id=_require_str(item, "id", path, index),
        n=_require_int(item, "n", path, index),
        side=_require_str(item, "side", path, index),
        grid_counts=_require_str(item, "grid_counts", path, index),
        seed_certificate=_optional_str(item, "seed_certificate", path, index),
        seed_windows=_require_int(item, "seed_windows", path, index),
        deadline_seconds=_require_int(item, "deadline_seconds", path, index),
    )


def prefix_for(queue_dir: Path, probe_id: str) -> Path:
    return queue_dir / probe_id


def run_json_path(prefix: Path) -> Path:
    return Path(f"{prefix}-run.json")


def freeze_path(prefix: Path) -> Path:
    return Path(f"{prefix}-certificate.json")


def freeze_mass_below_n(n: int, run_path: Path) -> bool:
    """Halt only when the freeze total is strictly below n."""

    payload = json.loads(run_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"{run_path}: run JSON must be a mapping")
    mass = payload.get("total_mass")
    if mass is None:
        return False
    if not isinstance(mass, str | int):
        raise TypeError(f"{run_path}: total_mass must be a string or int")
    return Fraction(mass) < n


def colgen_command(probe: Probe, prefix: Path) -> list[str]:
    command = [
        sys.executable,
        "-m",
        "devtools.run_fractional_colgen",
        "--n",
        str(probe.n),
        "--side",
        probe.side,
        "--shrink",
        "9977/10000",
        "--direction-steps",
        "181",
        "--grid-counts",
        probe.grid_counts,
        "--scale",
        "4000000",
        "--support-cap",
        "32",
        "--column-rounds",
        "1",
        "--max-rounds",
        "60",
        "--deadline-seconds",
        str(probe.deadline_seconds),
        "--seed-windows",
        str(probe.seed_windows),
        "--freeze",
        str(freeze_path(prefix)),
        "--freeze-family",
        f"{prefix}-family.json",
        "--json",
        str(run_json_path(prefix)),
        "--row-log",
        f"{prefix}-rows.jsonl",
        "--log",
        f"{prefix}.log",
    ]
    if probe.seed_certificate is not None:
        command.extend(["--seed-certificate", probe.seed_certificate, "--seed-map", "scale"])
    return command


def run_colgen(probe: Probe, prefix: Path) -> int:
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    env["OPENBLAS_NUM_THREADS"] = "1"
    env["MKL_NUM_THREADS"] = "1"
    completed = subprocess.run(
        colgen_command(probe, prefix),
        cwd=PACKING,
        env=env,
        check=False,
    )
    return completed.returncode


def stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def emit(log_path: Path, line: str) -> None:
    text = f"{stamp()} {line}"
    print(text, flush=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(text + "\n")


def walk_queue(
    probes: Sequence[Probe],
    queue_dir: Path,
    stop_at: datetime,
    log_path: Path,
    runner: Callable[[Probe, Path], int] = run_colgen,
) -> int:
    """Skip existing run JSON; halt on freeze mass < n or when the stop instant lands."""

    emit(log_path, f"waiter start; stop_at={stop_at.strftime('%Y-%m-%dT%H:%M:%SZ')}")
    for probe in probes:
        prefix = prefix_for(queue_dir, probe.id)
        if run_json_path(prefix).is_file():
            emit(log_path, f"SKIP {probe.id}: run JSON exists")
            continue
        remain = remain_seconds(stop_at)
        if remain < 60:
            emit(log_path, f"STOP before {probe.id}: remain={remain}s")
            return EXIT_STOP
        emit(
            log_path,
            f"START {probe.id} deadline={probe.deadline_seconds}s remain={remain}s",
        )
        rc = runner(probe, prefix)
        emit(log_path, f"EXIT {probe.id} rc={rc}")
        if rc != 0:
            return rc
        run_path = run_json_path(prefix)
        if freeze_path(prefix).is_file() and run_path.is_file():
            if freeze_mass_below_n(probe.n, run_path):
                emit(
                    log_path,
                    f"{probe.id}: freeze mass < {probe.n}; coordinator must decide_certificate",
                )
                return EXIT_FREEZE_BELOW
            emit(log_path, f"{probe.id}: freeze mass >= {probe.n}; site set refuted, continue")
            continue
        emit(log_path, f"{probe.id}: no freeze (unconverged or mass not rationalised)")
    emit(log_path, "waiter done")
    return EXIT_DONE


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--queue",
        type=Path,
        required=True,
        help="YAML with a probes list; run JSON and freezes land beside it",
    )
    parser.add_argument(
        "--stop-at",
        default=os.environ.get("STOP_AT", DEFAULT_STOP_AT),
        help="UTC instant after which no new probe starts (default STOP_AT or session-140)",
    )
    parser.add_argument(
        "--log",
        type=Path,
        default=None,
        help="append waiter lines here; default <queue-dir>/covering-queue.log",
    )
    args = parser.parse_args(argv)
    queue_path = args.queue.resolve()
    probes = load_queue(queue_path)
    log_path = (
        args.log.resolve() if args.log is not None else queue_path.parent / "covering-queue.log"
    )
    return walk_queue(probes, queue_path.parent, parse_stop_at(args.stop_at), log_path)


if __name__ == "__main__":
    sys.exit(main())
