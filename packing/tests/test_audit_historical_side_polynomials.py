"""Independent algebra audit controls: false claims must fail on their mathematics."""

from __future__ import annotations

import copy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools.audit_historical_side_polynomials import (
    HistoricalAuditError,
    audit_document,
    verify_irreducibility,
    verify_root_interval,
    verify_source_equation,
)


def _document(tmp_path: Path) -> dict[str, Any]:
    (tmp_path / "source.txt").write_text("s^2-2=0\n", encoding="utf-8")
    return {
        "format": "kingbird-historical-side-polynomials-v2",
        "scope": {"unique_polynomial_side_pairs": 1, "decoded_source_rows": 1},
        "entries": [
            {
                "n": 2,
                "historical_side": "1.41421356",
                "degree": 2,
                "coefficients": [1, 0, -2],
                "validation": {
                    "checks": {
                        "irreducible": {"method": "modular-degree-patterns", "primes": [3]},
                        "root": {"interval": ["1.41421356237", "1.41421356238"]},
                    }
                },
                "occurrences": [
                    {
                        "source": {
                            "path": "source.txt",
                            "locator": {"line": 1, "line_end": 1, "section": "2"},
                        },
                        "printed_equation": "s^2-2=0",
                    }
                ],
            }
        ],
    }


def test_full_audit_accepts_an_exact_sqrt_two_witness(tmp_path: Path) -> None:
    assert audit_document(_document(tmp_path), repo=tmp_path) == {
        "pairs": 1,
        "source_equations": 1,
        "prime_replays": 1,
        "root_intervals": 1,
    }


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("coefficients", [1, 0, -3], "endpoint sign change"),
        ("coefficients", [2, 0, -4], "primitive"),
        ("degree", 3, "declared-degree"),
        ("historical_side", "1.41421359", "rounding/truncation"),
    ],
)
def test_audit_rejects_altered_claims(
    tmp_path: Path, field: str, value: Any, message: str
) -> None:
    document = _document(tmp_path)
    document["entries"][0][field] = value
    # Use Q factorization so the altered polynomial reaches the root check.
    document["entries"][0]["validation"]["checks"]["irreducible"] = {
        "method": "factorization",
        "primes": [],
    }
    with pytest.raises(HistoricalAuditError, match=message):
        audit_document(document, repo=tmp_path)


def test_reducible_polynomials_fail_both_certificate_routes() -> None:
    with pytest.raises(HistoricalAuditError, match="reducible over Q"):
        verify_irreducibility([1, -3, 2], {"method": "factorization", "primes": []})
    # (s^2-2)(s^2-3) stays squarefree modulo 5, but degree two remains possible.
    with pytest.raises(HistoricalAuditError, match="proper degrees"):
        verify_irreducibility(
            [1, 0, -5, 0, 6], {"method": "modular-degree-patterns", "primes": [5]}
        )


@pytest.mark.parametrize(
    ("coefficients", "prime", "message"),
    [
        ([1, 0, -2], 9, "nonprime"),
        ([2, 0, -3], 2, "degree drops"),
        ([1, 0, -2], 2, "squarefree"),
    ],
)
def test_bad_prime_witnesses_fail(coefficients: list[int], prime: int, message: str) -> None:
    with pytest.raises(HistoricalAuditError, match=message):
        verify_irreducibility(
            coefficients, {"method": "modular-degree-patterns", "primes": [prime]}
        )


@pytest.mark.parametrize(
    ("coefficients", "lo", "hi", "message"),
    [
        ([1, 0, 1], "0", "2", "endpoint sign change"),
        ([1, -3, 2], "0.5", "2.5", "endpoint sign change"),
        # Three simple roots give an endpoint sign change; Descartes must reject them.
        ([1, -6, 11, -6], "0.5", "3.5", "3 sign variations"),
    ],
)
def test_zero_two_or_three_roots_are_not_a_unique_root(
    coefficients: list[int], lo: str, hi: str, message: str
) -> None:
    with pytest.raises(HistoricalAuditError, match=message):
        verify_root_interval(coefficients, Fraction(lo), Fraction(hi))


def test_source_changes_cannot_borrow_an_algebraic_certificate(tmp_path: Path) -> None:
    document = _document(tmp_path)
    altered = copy.deepcopy(document)
    altered["entries"][0]["occurrences"][0]["printed_equation"] = "s^2-3=0"
    with pytest.raises(HistoricalAuditError, match="absent at source locator"):
        audit_document(altered, repo=tmp_path)
    (tmp_path / "source.txt").write_text("s^2-3=0\n", encoding="utf-8")
    with pytest.raises(HistoricalAuditError, match="disagrees with retained coefficients"):
        audit_document(altered, repo=tmp_path)
    with pytest.raises(HistoricalAuditError, match="not an integer polynomial"):
        verify_source_equation("s^2-__import__('os')=0", [1, 0, -2])
