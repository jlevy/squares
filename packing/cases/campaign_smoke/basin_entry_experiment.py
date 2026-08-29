"""Perturb Trump's ``n = 11`` packing and measure return under three search arms.

The two local-quench arms test whether the configuration has an attracting
neighbourhood and whether return is effort-bound. The hot arm tests whether the
campaign annealer keeps the basin when handed it. The exact packing is converted to an
f64 seed before search; none of this command's output is exact-verification evidence.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from strif import atomic_output_file

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENGINE = PROJECT_ROOT / "sqsearch" / "target" / "release" / "sqsearch"
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / "campaign/series/series-000-smoke-and-calibration/results/exp-005-basin-entry.jsonl"
)


@dataclass(frozen=True)
class Arm:
    """One named basin-entry schedule."""

    name: str
    steps: int
    hot_temperature: float | None = None


ARMS = (
    Arm("quench-1x", 400_000),
    Arm("quench-10x", 4_000_000),
    Arm("hot", 400_000, 0.25),
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--engine", type=Path, default=DEFAULT_ENGINE)
    parser.add_argument("--eps", default="0,1e-5,1e-4,1e-3,1e-2,1e-1")
    parser.add_argument("--trials", type=int, default=40)
    parser.add_argument("--seed", type=int, default=1)
    return parser


def _export_seed(destination: Path) -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "cases.trump11.export_seed"],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    destination.write_text(completed.stdout, encoding="utf-8")


def _arm_command(
    engine: Path, seed_config: Path, arm: Arm, *, eps: str, trials: int, seed: int
) -> list[str | Path]:
    command: list[str | Path] = [
        engine,
        "--basin-entry",
        "--seed-config",
        seed_config,
        "--eps",
        eps,
        "--trials",
        str(trials),
        "--seed",
        str(seed),
        "--steps",
        str(arm.steps),
    ]
    if arm.hot_temperature is not None:
        command.extend(("--t-hot", str(arm.hot_temperature)))
    return command


def main(arguments: list[str] | None = None) -> int:
    """Run all basin-entry arms and return a process-compatible status code."""
    parser = _parser()
    options = parser.parse_args(arguments)
    if options.trials <= 0:
        parser.error("--trials must be positive")
    if options.seed < 0:
        parser.error("--seed must be non-negative")
    if not options.engine.is_file():
        parser.error(
            f"sqsearch executable not found at {options.engine}; "
            "run `cargo build --locked --release --manifest-path sqsearch/Cargo.toml`"
        )

    selftest = subprocess.run(
        [options.engine, "--selftest"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    if "SELFTEST PASSED" not in selftest.stdout:
        parser.error("sqsearch self-test did not report SELFTEST PASSED")

    record_count = 0
    with tempfile.TemporaryDirectory(prefix="packing-basin-entry-") as temporary_dir:
        seed_config = Path(temporary_dir) / "trump11-seed.json"
        _export_seed(seed_config)
        with (
            atomic_output_file(options.output, make_parents=True) as temporary_output,
            temporary_output.open("w", encoding="utf-8") as archive,
        ):
            for arm in ARMS:
                print(f"running {arm.name} ({arm.steps} steps)", file=sys.stderr)
                completed = subprocess.run(
                    _arm_command(
                        options.engine,
                        seed_config,
                        arm,
                        eps=options.eps,
                        trials=options.trials,
                        seed=options.seed,
                    ),
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                for line in completed.stdout.splitlines():
                    record = json.loads(line)
                    record["arm"] = arm.name
                    archive.write(json.dumps(record, separators=(",", ":")) + "\n")
                    record_count += 1

    print(f"wrote {record_count} records to {options.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
