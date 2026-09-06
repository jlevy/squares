"""Run the independent reviewer's verifier on one certificate path.

`independent_verify.py` is retained verbatim as evidence: its style is the
reviewer's and its point is that it shares nothing with `sqpack.fractional`.
Its command-line tail is the reviewer's too -- it reads its first argument as a
mode name (``both``, ``19-5``, ``77-20``) and resolves the certificates under
the reviewer's own absolute checkout path -- so the replay the evidence register
recorded, which passes a certificate path, selected no mode, verified nothing
and exited 0, and the mode form cannot run on any other machine (think-d7yx).

This wrapper is the executable replay. It loads the reviewer's module without
editing it, hands `verify` the certificate at the path given, and exits 0 only
on the reviewer's own ``CERTIFICATE VALID``. Nothing here decides anything the
reviewer's code does not.

Usage, from ``packing/``::

    uv run --frozen --all-extras python \\
        cases/n12_fractional_certificate/replay_independent.py \\
        cases/n12_fractional_certificate/certificate-77-20.json
"""

from __future__ import annotations

import argparse
import runpy
import sys
from pathlib import Path

REVIEWER_VERIFIER = Path(__file__).resolve().with_name("independent_verify.py")


def reviewer_module() -> dict[str, object]:
    """The reviewer's functions, loaded from the retained file as-is."""

    return runpy.run_path(str(REVIEWER_VERIFIER), run_name="independent_verify")


def replay(
    certificate: Path, *, directions: list[int] | None = None, brute_check: int = 0
) -> bool:
    """Whether the reviewer's `verify` accepts the certificate at ``certificate``."""

    module = reviewer_module()
    load = module["load"]
    verify = module["verify"]
    assert callable(load)
    assert callable(verify)
    result = verify(
        load(str(certificate)), ks=directions, label=certificate.name, brute_check=brute_check
    )
    # The reviewer's `verify` returns ``(accepted, report)``; only the verdict is read.
    assert isinstance(result, tuple)
    return bool(result[0])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="replay the reviewer's verifier on one file")
    parser.add_argument("certificate", type=Path)
    parser.add_argument(
        "--directions",
        default="all",
        help="comma-separated net direction indices to decide, or all (the default)",
    )
    parser.add_argument("--brute-check", type=int, default=0)
    args = parser.parse_args(argv)
    if not args.certificate.is_file():
        print(f"REFUSED: {args.certificate} is not a file")
        return 1
    directions = (
        None
        if args.directions == "all"
        else [int(part) for part in args.directions.split(",") if part]
    )
    accepted = replay(args.certificate, directions=directions, brute_check=args.brute_check)
    return 0 if accepted else 1


if __name__ == "__main__":
    sys.exit(main())
