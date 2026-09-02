from __future__ import annotations

import json
import subprocess
import sys

from devtools.audit_n54_source_formula import derive_receipt


def test_n54_source_formula_closes_in_one_quartic_field() -> None:
    receipt = derive_receipt()

    assert receipt["field"] == {
        "name": "Q(p)",
        "primitive": "p = sqrt(1 + sqrt(2))",
        "minimal_polynomial_coefficients": [1, 0, -2, 0, -1],
        "embedding": "positive real root p in (1.5537, 1.5538)",
    }
    assert receipt["minimal_polynomials"] == {
        "side": [4, -112, 1164, -5304, 8897],
        "tan_angle": [7, -12, 6, -4, -1],
        "sin_angle": [8, -16, 16, -8, 1],
        "cos_angle": [8, -16, 0, 16, -7],
    }


def test_n54_source_formula_cli_agrees_under_optimization() -> None:
    base = ["-m", "devtools.audit_n54_source_formula", "--check"]
    normal = subprocess.run(
        [sys.executable, *base],
        check=True,
        capture_output=True,
        text=True,
    )
    optimized = subprocess.run(
        [sys.executable, "-O", *base],
        check=True,
        capture_output=True,
        text=True,
    )

    assert json.loads(normal.stdout) == json.loads(optimized.stdout)
