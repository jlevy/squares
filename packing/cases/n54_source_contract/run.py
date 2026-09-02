"""Emit the frozen synthetic ``N54Result/v1`` self-test receipt to stdout only."""

from __future__ import annotations

import sys
from pathlib import Path

from cases.n54_source_contract.contract import build_n54_result_bytes


def main() -> int:
    """Run the closed author self-test and emit no files."""

    if sys.argv[1:] != ["--selftest"]:
        raise SystemExit("usage: python -m cases.n54_source_contract.run --selftest")
    fixture = Path(__file__).with_name("synthetic_fixture.n54").read_bytes()
    sys.stdout.buffer.write(build_n54_result_bytes(fixture))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
