#!/usr/bin/env python3
"""Public command family for square-packing witness interchange."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from strif import atomic_output_file

from sqpack.project import ProjectLayoutError, require_project_root
from sqpack.witness import (
    WitnessError,
    exact_verify,
    inspect_witness,
    load_witness,
    numerical_check,
    promote_rational,
    render_svg,
    result_json,
    witness_document,
)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description="Inspect, numerically check, formally verify, or promote a Witness/v1 file."
    )
    subcommands = command.add_subparsers(dest="operation", required=True)

    inspect = subcommands.add_parser(
        "inspect", help="summarize or render; makes no assurance claim"
    )
    inspect.add_argument("witness", type=Path)
    inspect.add_argument("--svg", type=Path)
    inspect.add_argument("--json", action="store_true")

    check = subcommands.add_parser("check", help="finite-precision numerical feasibility check")
    check.add_argument("witness", type=Path)
    check.add_argument(
        "--method",
        choices=("numerical-f64", "numerical-multiprecision"),
        required=True,
    )
    check.add_argument("--precision", type=int, required=True)
    check.add_argument("--tolerance", required=True)
    check.add_argument("--json", action="store_true")

    verify = subcommands.add_parser("verify", help="replay exact or interval formal evidence")
    verify.add_argument("witness", type=Path)
    verify.add_argument("--json", action="store_true")

    promote = subcommands.add_parser(
        "promote",
        help="attempt a formal certificate; failure does not alter the source witness",
    )
    promote.add_argument("witness", type=Path)
    promote.add_argument(
        "--strategy", choices=("robust-rational", "interval-existence"), required=True
    )
    promote.add_argument("--rational-digits", type=int, default=36)
    promote.add_argument("--max-side-increase", required=True)
    promote.add_argument("--output-witness", type=Path, required=True)
    promote.add_argument("--json", action="store_true")
    return command


def _print(result: dict, success: str, *, machine: bool) -> None:
    if machine:
        print(result_json(result))
        return
    print(success)
    for key in ("id", "n", "side", "declared_side", "method", "tolerance", "pairs_tested"):
        if key in result:
            print(f"  {key.replace('_', ' ')}: {result[key]}")
    print(f"  limits: {result['limitations']}")


def _interval_not_built() -> None:
    raise WitnessError(
        "checker-not-built",
        "interval existence certification is a buildable path for suitable contact "
        "systems, but this repository does not yet have a generic checker",
    )


def _run(args: argparse.Namespace) -> int:
    project_root = require_project_root()
    witness = load_witness(
        args.witness,
        fallback_schema=project_root / "witnesses" / "witness.schema.yaml",
    )
    if args.operation == "inspect":
        result = inspect_witness(witness)
        if args.svg:
            render_svg(witness, args.svg)
            result["svg"] = str(args.svg)
        _print(result, "INSPECTED — no assurance claim", machine=args.json)
        return 0
    if args.operation == "check":
        result, report = numerical_check(
            witness,
            method=args.method,
            precision=args.precision,
            tolerance=args.tolerance,
        )
        _print(
            result,
            (
                "NUMERIC CHECK PASSED — not verification"
                if report.valid
                else "NUMERIC CHECK FAILED"
            ),
            machine=args.json,
        )
        return 0 if report.valid else 1
    if args.operation == "verify":
        result, report = exact_verify(witness)
        _print(
            result,
            "VERIFIED" if report.valid else "VERIFICATION FAILED",
            machine=args.json,
        )
        return 0 if report.valid else 1
    if args.strategy == "interval-existence":
        _interval_not_built()
    result, promoted = promote_rational(
        witness,
        rational_digits=args.rational_digits,
        max_side_increase=args.max_side_increase,
        source_path=str(args.witness),
        replay_path=str(args.output_witness),
    )
    with atomic_output_file(args.output_witness) as temporary:
        temporary.write_text(witness_document(promoted), encoding="utf-8")
    result["output_witness"] = str(args.output_witness)
    _print(result, "PROMOTED — exact rational certificate produced", machine=args.json)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return _run(args)
    except (ProjectLayoutError, WitnessError) as error:
        kind = error.kind if isinstance(error, WitnessError) else "project-layout"
        failure = {
            "operation": args.operation,
            "status": "failed",
            "blocker": {"kind": kind, "detail": str(error)},
        }
        if getattr(args, "json", False):
            print(json.dumps(failure, indent=2, sort_keys=True), file=sys.stderr)
        else:
            print(f"FAILED [{kind}]: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
