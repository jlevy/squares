"""Refuse incomplete or skipped native Darwin memory acceptance evidence."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED_CASES = (
    "test_live_memory_sample_is_positive",
    "test_released_allocation_does_not_leave_current_memory_above_guard",
    "test_darwin_current_memory_agrees_with_external_ps",
    "test_darwin_sdk_layout_and_signature",
)


def check_results(path: Path) -> None:
    """Require exactly the four named cases, successful both in totals and case records."""
    root = ET.parse(path).getroot()
    suites = list(root.iter("testsuite"))
    if not suites:
        raise ValueError("native Darwin report contains no test suites")
    totals = dict.fromkeys(("tests", "failures", "errors", "skipped"), 0)
    for suite in suites:
        for name in totals:
            value = int(suite.attrib[name])
            if value < 0:
                raise ValueError(f"native Darwin report has negative {name}")
            totals[name] += value
    if totals != {"tests": len(EXPECTED_CASES), "failures": 0, "errors": 0, "skipped": 0}:
        raise ValueError(f"native Darwin report requires four passes with zero skips: {totals}")
    cases = list(root.iter("testcase"))
    identities = [(case.get("classname"), case.get("name")) for case in cases]
    expected = {("tests.test_process_memory", name) for name in EXPECTED_CASES}
    if len(identities) != len(expected) or set(identities) != expected:
        raise ValueError(
            f"native Darwin report has missing, duplicate or unexpected cases: {identities}"
        )
    if any(
        case.find(name) is not None
        for case in cases
        for name in ("failure", "error", "skipped")
    ):
        raise ValueError("native Darwin report contains a failed, errored or skipped case")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args(argv)
    try:
        check_results(args.report)
    except (OSError, ET.ParseError, KeyError, ValueError) as error:
        print(f"Darwin memory acceptance failed: {error}", file=sys.stderr)
        return 1
    print(f"Darwin memory acceptance: {len(EXPECTED_CASES)} passed, zero skips")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
