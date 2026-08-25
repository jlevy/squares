"""Contracts for the temporary macOS deep-golden expected-failure check."""

from __future__ import annotations

import pytest

from devtools.check_known_macos_golden_drift import (
    ProbeMismatchError,
    validate_probe_result,
)

KNOWN_DRIFT = """\
GOLDEN DRIFT — the map changed. Review the diff before accepting:
  n= 4   2 endpoint rows from  4 proposals (3 converged)
  -    converged: 4
  -    distinct_basins: 1
  +    converged: 3
  +    distinct_basins: 2
ORACLE FAILURES:
  the rebuilt map differs from the committed golden
GOLDEN BASIN CHECKS FAILED
"""


def test_known_portability_drift_is_the_only_accepted_probe_failure() -> None:
    validate_probe_result(1, KNOWN_DRIFT)

    with pytest.raises(ProbeMismatchError, match="unexpectedly passed"):
        validate_probe_result(0, "ALL CHECKS PASSED")

    with pytest.raises(ProbeMismatchError, match="unexpected failure"):
        validate_probe_result(1, "segmentation fault")
