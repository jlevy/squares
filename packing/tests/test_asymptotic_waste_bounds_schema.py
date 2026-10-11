"""The waste register's two kinds of upper bound: on W(x) for all x, and on c*(k) only."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator

FRONTIER = Path(__file__).resolve().parents[1] / "frontier"


@pytest.fixture(scope="module")
def register() -> dict[str, Any]:
    document = yaml.safe_load(
        (FRONTIER / "asymptotic-waste-bounds.yaml").read_text(encoding="utf-8")
    )
    document.pop("softschema")
    return document


@pytest.fixture(scope="module")
def validator() -> Draft202012Validator:
    schema = yaml.safe_load(
        (FRONTIER / "asymptotic-waste-bounds.schema.yaml").read_text(encoding="utf-8")
    )
    return Draft202012Validator(schema)


def _errors(validator: Draft202012Validator, document: dict[str, Any]) -> list[str]:
    return [error.message for error in validator.iter_errors(document)]


def test_the_register_holds_both_kinds(
    register: dict[str, Any], validator: Draft202012Validator
) -> None:
    assert _errors(validator, register) == []
    exponents = [row.get("exponent") for row in register["deficiency_upper_bounds"]]
    assert exponents == [0.5, 0.4, 0.375, 0.375]
    assert all(
        row["bound"].startswith("REPORTED:") for row in register["deficiency_upper_bounds"]
    )


def test_an_exponent_below_one_half_is_refused_for_w_at_every_x(
    register: dict[str, Any], validator: Draft202012Validator
) -> None:
    document = copy.deepcopy(register)
    document["upper_bounds"][0]["exponent"] = 0.375
    assert any("0.5" in message for message in _errors(validator, document))


def test_a_deficiency_bound_must_state_its_side_condition(
    register: dict[str, Any], validator: Draft202012Validator
) -> None:
    document = copy.deepcopy(register)
    del document["deficiency_upper_bounds"][0]["side_condition"]
    assert any("side_condition" in message for message in _errors(validator, document))
