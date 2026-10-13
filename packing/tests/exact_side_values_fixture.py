"""One adopted native side for presentation controls, without running the corpus builder."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

_NUMERATOR = (
    "647621270347922806782680126627700398497757575308093167357830"
    "64762127034792280678268012662770039849775757530809316735783"
)
_DENOMINATOR = (
    "500000000000000000000000000000000000000000000000000000000000"
    "0000000000000000000000000000000000000000000000000000000000"
)
_EXACT_FORM = f"{_NUMERATOR}/{_DENOMINATOR}"
_PACKET = "packing/resources/web/dostashev-records-2026-10-11"

_ADOPTED = {
    "n": 155,
    "status": "open",
    "side": {"value": "12.9524254069584562", "relation": "upper-bound"},
    "lower": {"value": "12"},
    "state": "rational",
    "exact_form": _EXACT_FORM,
    "exact_form_latex": rf"\frac{{{_NUMERATOR}}}{{{_DENOMINATOR}}}",
    "algebraic_source": "derived-from-exact-form",
    "degree": 1,
    "polynomial": {
        "coefficients": [
            _DENOMINATOR,
            f"-{_NUMERATOR}",
        ],
        "text": "retained native linear identity",
        "latex": "retained native linear identity",
        "height_digits": 118,
    },
    "checks": {
        "catalogue": "derived-here",
        "decimal": "12.952425406958456135",
        "galois": None,
        "irreducible": {"method": "linear", "primes": []},
        "kkt_agreement_digits": None,
        "recorded_agreement_digits": 16,
        "root": {
            "contains_recorded_side": True,
            "interval": [
                _EXACT_FORM,
                _EXACT_FORM,
            ],
            "unique": True,
            "window": "exact",
        },
    },
    "kkt": None,
    "notes": [],
    "source_certificate": {
        "result": "T-149",
        "source_key": "[Ostashev records 2026-10-11]",
        "revision": "c3d17ab08bd5db65dc5ffe69e41f7b2ff0c2fc49",
        "facts": f"{_PACKET}/source/records/n0155.sqcert",
        "original_certificate": "records/n0155.sqcert",
        "receipt": f"{_PACKET}/receipts/exact-certification.json.xz",
        "verification": "V3",
        "confirmation": "C3",
        "algebraic_identity": "independently-checked",
        "geometry_replay": "native-replay-retained",
        "adoption": "adopted",
        "global_optimality": "not-established",
    },
    "source_occurrences": [
        {
            "path": f"{_PACKET}/source/records/n0155.sqcert",
            "url": "https://github.com/dostashev/square-packing/blob/c3d17ab08bd5db65dc5ffe69e41f7b2ff0c2fc49/records/n0155.sqcert",
            "kind": "derived-from-source-closed-form",
            "locator": {"line": 1, "section": "155"},
            "source_flags": ["source certificate; T-149"],
        }
    ],
    "attribution": {
        "date_mentions": ["2026-10-11"],
        "source_text": [
            "Daniil Ostashev retains finder and certificate credit.",
            "Literal [source](https://example.test/) <b>text</b> & $notation$.",
        ],
    },
    "source_statuses": [
        "adopted-current",
        "scoped-finite-feasibility-confirmed",
        "native-replay-retained",
    ],
}


def adopted_current() -> dict[str, Any]:
    """A fresh n155/T-149 row with all custody fields and adversarial literal source text."""
    return deepcopy(_ADOPTED)
