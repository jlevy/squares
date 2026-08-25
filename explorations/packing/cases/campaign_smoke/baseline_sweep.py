"""Run the stock-engine calibration sweep and atomically retain every JSONL record.

The default cells preserve the original campaign design: proved ``n = 10`` is the
positive control, ``n = 11`` is the target, and open ``n = 12`` is calibration. A
sub-four result at ``n = 12`` is therefore a discovery candidate, not a control breach.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from strif import atomic_output_file

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_ENGINE = PROJECT_ROOT / "sqsearch" / "target" / "release" / "sqsearch"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="new JSONL archive to write atomically")
    parser.add_argument(
        "--engine", type=Path, default=DEFAULT_ENGINE, help="sqsearch executable"
    )
    parser.add_argument("--instances", type=int, nargs="+", default=[10, 11, 12], metavar="N")
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    parser.add_argument("--chains", type=int, default=8)
    parser.add_argument("--budget-moves", type=int, default=100_000_000)
    return parser


def _positive(parser: argparse.ArgumentParser, name: str, value: int) -> None:
    if value <= 0:
        parser.error(f"{name} must be positive")


def main(arguments: list[str] | None = None) -> int:
    """Run the declared sweep and return a process-compatible status code."""
    parser = _parser()
    options = parser.parse_args(arguments)
    _positive(parser, "--chains", options.chains)
    _positive(parser, "--budget-moves", options.budget_moves)
    for instance in options.instances:
        _positive(parser, "each instance", instance)
    for seed in options.seeds:
        _positive(parser, "each seed", seed)
    if not options.engine.is_file():
        parser.error(
            f"sqsearch executable not found at {options.engine}; "
            "run `cargo build --locked --release --manifest-path sqsearch/Cargo.toml`"
        )

    subprocess.run([options.engine, "--selftest"], cwd=PROJECT_ROOT, check=True)
    line_count = 0
    with (
        atomic_output_file(options.output, make_parents=True) as temporary,
        temporary.open("w", encoding="utf-8") as archive,
    ):
        for instance in options.instances:
            for seed in options.seeds:
                completed = subprocess.run(
                    [
                        options.engine,
                        "--n",
                        str(instance),
                        "--seed",
                        str(seed),
                        "--chains",
                        str(options.chains),
                        "--budget-moves",
                        str(options.budget_moves),
                    ],
                    cwd=PROJECT_ROOT,
                    stdout=subprocess.PIPE,
                    text=True,
                    check=True,
                )
                archive.write(completed.stdout)
                line_count += len(completed.stdout.splitlines())

    print(f"baseline complete: wrote {line_count} records to {options.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
