"""Independently verify the frozen synthetic n = 54 source-contract result.

This standard-library-only verifier treats both the synthetic fixture and the author
result as data.  It intentionally imports no author parser, runner, geometry module,
or production verifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

SCHEMA = "packing.squares:n54-source-contract/v1"
VERIFICATION_SCHEMA = "packing.squares:n54-source-contract-verification/v1"
SCOPE = "synthetic-structure-only"
FIXTURE_SHA256 = "92ef9c467564f651efc561d69005c3b0cb847d13f4766ce0e16f365bde791de3"
FIELD_RECEIPT_SHA256 = "3555f8910e0daced8022576bea238951654fface93f0d0b51109c0efd3678cf4"
WITNESS_SHA256 = "e4bcdefa3472e23ca7f4e403b26361efca17702c20570f6144b70c3a01a96ad7"
CLAIM_BOUNDARY = (
    "Prospective synthetic source-cell contract only; this establishes no source "
    "fidelity, actual row correspondence, precision cells, wall or pairwise geometry, "
    "feasibility, optimality or packing bound; H-055 remains instrument-unready."
)

MAX_INPUT_BYTES = 65_536
MAX_COMMENTS = 256
MAX_COMMENT_BYTES = 4_096
MAX_ASSIGNMENTS = 256
MAX_TOKENS = 256
MAX_DEPTH = 32
MAX_INTEGER_DIGITS = 18

LOCAL_LABELS = tuple(
    [f"stair/{index:02d}" for index in range(18)]
    + ["axis/00"]
    + [f"rot/{index:02d}" for index in range(4)]
    + ["block/00/0", "block/00/1", "block/01/0", "block/01/1"]
)
FULL_LABELS = tuple(f"{half}/{local}" for half in ("B", "T") for local in LOCAL_LABELS)
ASSIGNMENT_NAMES = tuple(label.replace("/", "_") for label in LOCAL_LABELS)


class VerificationError(RuntimeError):
    """The fixture or result disagrees with the frozen independent contract."""


type Q = tuple[Fraction, Fraction, Fraction, Fraction]
type Matrix = tuple[int, int, int, int]
type Element = tuple[int, int]
type Token = tuple[str, str]

ZERO: Q = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
ONE: Q = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
R: Matrix = (0, -1, 1, 0)
F: Matrix = (1, 0, 0, -1)
D4_ELEMENTS: tuple[Element, ...] = tuple(
    [(index, 0) for index in range(4)] + [(index, 1) for index in range(4)]
)


def _require(condition: object, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def _exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        left_mapping = cast(dict[object, object], left)
        right_mapping = cast(dict[object, object], right)
        return set(left_mapping) == set(right_mapping) and all(
            _exact_equal(left_mapping[key], right_mapping[key]) for key in left_mapping
        )
    if type(left) is list:
        left_items = cast(list[object], left)
        right_items = cast(list[object], right)
        return len(left_items) == len(right_items) and all(
            _exact_equal(a, b) for a, b in zip(left_items, right_items, strict=True)
        )
    return left == right


def canonical_bytes(value: object) -> bytes:
    """Return the one admitted canonical JSON encoding."""

    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    ).encode("ascii")


def _duplicate_guard(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_number(token: str) -> Any:
    raise VerificationError(f"non-integral JSON number: {token}")


def _reject_constant(token: str) -> Any:
    raise VerificationError(f"non-finite JSON number: {token}")


def load_result(path: Path) -> dict[str, Any]:
    """Load strict canonical JSON, rejecting duplicate keys and all float syntax."""

    raw = path.read_bytes()
    try:
        document = json.loads(
            raw,
            object_pairs_hook=_duplicate_guard,
            parse_float=_reject_number,
            parse_constant=_reject_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise VerificationError("result is not strict JSON") from error
    _require(type(document) is dict, "result is not an object")
    _require(canonical_bytes(document) == raw, "result is not canonical JSON")
    return cast(dict[str, Any], document)


def _q(value: int | Fraction = 0) -> Q:
    return (Fraction(value), Fraction(0), Fraction(0), Fraction(0))


def _q_add(left: Q, right: Q) -> Q:
    return cast(Q, tuple(a + b for a, b in zip(left, right, strict=True)))


def _q_neg(value: Q) -> Q:
    return cast(Q, tuple(-coefficient for coefficient in value))


def _q_sub(left: Q, right: Q) -> Q:
    return _q_add(left, _q_neg(right))


def _q_mul(left: Q, right: Q) -> Q:
    coefficients = [Fraction(0) for _ in range(7)]
    for left_degree, left_coefficient in enumerate(left):
        for right_degree, right_coefficient in enumerate(right):
            coefficients[left_degree + right_degree] += left_coefficient * right_coefficient
    # p^4 = 2p^2 + 1; descending reduction also handles p^5 and p^6.
    for degree in range(6, 3, -1):
        coefficient = coefficients[degree]
        coefficients[degree - 4] += coefficient
        coefficients[degree - 2] += 2 * coefficient
    return cast(Q, tuple(coefficients[:4]))


def _q_inverse(value: Q) -> Q:
    _require(value != ZERO, "zero denominator")
    columns = [
        _q_mul(value, cast(Q, tuple(Fraction(index == column) for index in range(4))))
        for column in range(4)
    ]
    matrix = [
        [columns[column][row] for column in range(4)] + [Fraction(row == 0)] for row in range(4)
    ]
    for column in range(4):
        pivot = next((row for row in range(column, 4) if matrix[row][column]), None)
        _require(pivot is not None, "nonzero field element has no inverse")
        if pivot is None:  # Keeps the type refinement independent of assertions and -O.
            raise VerificationError("nonzero field element has no inverse")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        divisor = matrix[column][column]
        matrix[column] = [entry / divisor for entry in matrix[column]]
        for row in range(4):
            if row == column:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[column], strict=True)
            ]
    inverse = cast(Q, tuple(matrix[row][4] for row in range(4)))
    _require(_q_mul(value, inverse) == ONE, "field inverse replay failed")
    return inverse


def _q_div(left: Q, right: Q) -> Q:
    return _q_mul(left, _q_inverse(right))


def _q_pow(value: Q, exponent: int) -> Q:
    result = ONE
    factor = value
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = _q_mul(result, factor)
        factor = _q_mul(factor, factor)
        remaining //= 2
    return result


def _minimal_polynomial(value: Q) -> tuple[Fraction, ...]:
    """Return the monic degree-four dependency among 1, value, ..., value^4."""

    columns = [_q_pow(value, exponent) for exponent in range(5)]
    matrix = [
        [columns[column][row] for column in range(4)] + [-columns[4][row]] for row in range(4)
    ]
    for column in range(4):
        pivot = next((row for row in range(column, 4) if matrix[row][column]), None)
        _require(pivot is not None, "field value has degree below frozen receipt")
        if pivot is None:  # Keeps the type refinement independent of assertions and -O.
            raise VerificationError("field value has degree below frozen receipt")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        divisor = matrix[column][column]
        matrix[column] = [entry / divisor for entry in matrix[column]]
        for row in range(4):
            if row == column:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[column], strict=True)
            ]
    return (*tuple(matrix[index][4] for index in range(4)), Fraction(1))


S_VALUE: Q = (Fraction(15, 2), Fraction(1), Fraction(-1, 2), Fraction(0))
SIN_VALUE: Q = (Fraction(1, 2), Fraction(-1), Fraction(0), Fraction(1, 2))
COS_VALUE: Q = (Fraction(1), Fraction(1, 2), Fraction(-1, 2), Fraction(0))
TAN_VALUE: Q = (
    Fraction(2, 7),
    Fraction(-6, 7),
    Fraction(1, 7),
    Fraction(4, 7),
)


def _verify_field_receipt() -> dict[str, Q]:
    p: Q = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    _require(
        _q_sub(_q_sub(_q_pow(p, 4), _q_mul(_q(2), _q_pow(p, 2))), ONE) == ZERO,
        "frozen quartic relation failed",
    )
    lower = Fraction(15_537, 10_000)
    upper = Fraction(7_769, 5_000)

    def polynomial(value: Fraction) -> Fraction:
        return value**4 - 2 * value**2 - 1

    _require(
        0 < lower < upper and polynomial(lower) < 0 < polynomial(upper),
        "positive embedding interval failed",
    )
    _require(_q_mul(TAN_VALUE, COS_VALUE) == SIN_VALUE, "tangent basis drift")
    _require(
        _q_add(_q_mul(SIN_VALUE, SIN_VALUE), _q_mul(COS_VALUE, COS_VALUE)) == ONE,
        "orientation unit identity failed",
    )
    side_polynomial = _q_add(
        _q_add(
            _q_add(_q_mul(_q(4), _q_pow(S_VALUE, 4)), _q_mul(_q(-112), _q_pow(S_VALUE, 3))),
            _q_mul(_q(1164), _q_pow(S_VALUE, 2)),
        ),
        _q_add(_q_mul(_q(-5304), S_VALUE), _q(8897)),
    )
    _require(side_polynomial == ZERO, "side minimal polynomial drift")
    expected_minimal_polynomials = {
        "s": (
            Fraction(8897, 4),
            Fraction(-1326),
            Fraction(291),
            Fraction(-28),
            Fraction(1),
        ),
        "Sin[a]": (
            Fraction(1, 8),
            Fraction(-1),
            Fraction(2),
            Fraction(-2),
            Fraction(1),
        ),
        "Cos[a]": (
            Fraction(-7, 8),
            Fraction(2),
            Fraction(0),
            Fraction(-2),
            Fraction(1),
        ),
        "Tan[a]": (
            Fraction(-1, 7),
            Fraction(-4, 7),
            Fraction(6, 7),
            Fraction(-12, 7),
            Fraction(1),
        ),
    }
    for name, value in {
        "s": S_VALUE,
        "Sin[a]": SIN_VALUE,
        "Cos[a]": COS_VALUE,
        "Tan[a]": TAN_VALUE,
    }.items():
        _require(
            _minimal_polynomial(value) == expected_minimal_polynomials[name],
            f"minimal polynomial drift: {name}",
        )
    sec = _q_inverse(COS_VALUE)
    return {
        "s": S_VALUE,
        "Sin[a]": SIN_VALUE,
        "Cos[a]": COS_VALUE,
        "Tan[a]": TAN_VALUE,
        "Sec[a]": sec,
    }


_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_UINT = re.compile(r"[0-9]+")
_BUILTINS = ("Sin[a]", "Cos[a]", "Tan[a]", "Sec[a]", "s")


def _tokenize(payload: str) -> list[Token]:
    tokens: list[Token] = []
    position = 0
    while position < len(payload):
        character = payload[position]
        if character in " \t\n":
            position += 1
            continue
        builtin = next((item for item in _BUILTINS if payload.startswith(item, position)), None)
        if builtin is not None:
            end = position + len(builtin)
            if end == len(payload) or not (payload[end].isalnum() or payload[end] == "_"):
                tokens.append(("BUILTIN", builtin))
                _require(len(tokens) <= MAX_TOKENS, "formula token cap exceeded")
                position = end
                continue
        identifier = _IDENTIFIER.match(payload, position)
        if identifier is not None:
            tokens.append(("IDENT", identifier.group()))
            position = identifier.end()
        else:
            integer = _UINT.match(payload, position)
            if integer is not None:
                text = integer.group()
                _require(
                    len(text) <= MAX_INTEGER_DIGITS,
                    "integer digit cap exceeded",
                )
                tokens.append(("UINT", text))
                position = integer.end()
            elif character in "=+-*/()":
                tokens.append((character, character))
                position += 1
            else:
                raise VerificationError(f"forbidden formula token: {character!r}")
        _require(len(tokens) <= MAX_TOKENS, "formula token cap exceeded")
    tokens.append(("EOF", ""))
    return tokens


class _FormulaParser:
    def __init__(
        self, tokens: list[Token], definitions: dict[str, Q], builtins: dict[str, Q]
    ) -> None:
        self._tokens = tokens
        self._position = 0
        self._definitions = definitions
        self._builtins = builtins

    def _peek(self) -> Token:
        return self._tokens[self._position]

    def _take(self, kind: str) -> str:
        actual, text = self._peek()
        _require(actual == kind, f"expected {kind}, got {actual}")
        self._position += 1
        return text

    def assignment(self) -> tuple[str, Q]:
        name = self._take("IDENT")
        _require(name not in self._definitions, f"duplicate assignment: {name}")
        self._take("=")
        value = self._sum(0)
        self._take("EOF")
        return name, value

    def _sum(self, depth: int) -> Q:
        _require(depth <= MAX_DEPTH, "formula depth cap exceeded")
        value = self._product(depth)
        while self._peek()[0] in ("+", "-"):
            operator = self._take(self._peek()[0])
            right = self._product(depth)
            value = _q_add(value, right) if operator == "+" else _q_sub(value, right)
        return value

    def _product(self, depth: int) -> Q:
        _require(depth <= MAX_DEPTH, "formula depth cap exceeded")
        value = self._unary(depth)
        while self._peek()[0] in ("*", "/"):
            operator = self._take(self._peek()[0])
            right = self._unary(depth)
            value = _q_mul(value, right) if operator == "*" else _q_div(value, right)
        return value

    def _unary(self, depth: int) -> Q:
        _require(depth <= MAX_DEPTH, "formula depth cap exceeded")
        if self._peek()[0] in ("+", "-"):
            operator = self._take(self._peek()[0])
            value = self._primary(depth + 1)
            return value if operator == "+" else _q_neg(value)
        return self._primary(depth)

    def _primary(self, depth: int) -> Q:
        _require(depth <= MAX_DEPTH, "formula depth cap exceeded")
        kind, text = self._peek()
        if kind == "UINT":
            self._position += 1
            return _q(int(text))
        if kind == "BUILTIN":
            self._position += 1
            return self._builtins[text]
        if kind == "IDENT":
            self._position += 1
            _require(text in self._definitions, f"unknown or forward symbol: {text}")
            return self._definitions[text]
        if kind == "(":
            self._position += 1
            value = self._sum(depth + 1)
            self._take(")")
            return value
        raise VerificationError(f"expected formula primary, got {kind}")


def parse_fixture(path: Path) -> list[tuple[str, Q]]:
    """Parse and evaluate only the closed marked-comment transport."""

    raw = path.read_bytes()
    _require(len(raw) <= MAX_INPUT_BYTES, "fixture byte cap exceeded")
    _require(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, "fixture SHA-256 drift")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as error:
        raise VerificationError("fixture is not UTF-8") from error
    _require(text.isascii(), "fixture contains non-ASCII contract text")
    _require("\x00" not in text, "fixture contains NUL")
    _require("\r" not in text, "fixture contains carriage return")
    lowered = text.lower()
    _require(
        "<!doctype" not in lowered and "<!entity" not in lowered and "&" not in text,
        "fixture contains DTD or entity syntax",
    )

    payloads: list[str] = []
    position = 0
    marker = "<!--@n54 "
    terminator = " -->"
    while position < len(text):
        while position < len(text) and text[position] in " \t\n":
            position += 1
        if position == len(text):
            break
        _require(text.startswith(marker, position), "unmarked fixture content")
        end = text.find(terminator, position + len(marker))
        _require(end >= 0, "unterminated marked comment")
        nested = text.find("<!--", position + len(marker), end)
        _require(nested < 0, "nested marked comment")
        payload = text[position + len(marker) : end]
        _require(
            len(payload.encode("ascii")) <= MAX_COMMENT_BYTES,
            "comment byte cap exceeded",
        )
        payloads.append(payload)
        _require(len(payloads) <= MAX_COMMENTS, "comment cap exceeded")
        position = end + len(terminator)

    _require(len(payloads) <= MAX_ASSIGNMENTS, "assignment cap exceeded")
    builtins = _verify_field_receipt()
    definitions: dict[str, Q] = {}
    assignments: list[tuple[str, Q]] = []
    for payload in payloads:
        name, value = _FormulaParser(_tokenize(payload), definitions, builtins).assignment()
        definitions[name] = value
        assignments.append((name, value))
    _require(
        tuple(name for name, _ in assignments) == ASSIGNMENT_NAMES,
        "synthetic assignment inventory changed",
    )
    return assignments


def _matrix_mul(left: Matrix, right: Matrix) -> Matrix:
    a, b, c, d = left
    e, f, g, h = right
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


def _matrix_power(matrix: Matrix, exponent: int) -> Matrix:
    result: Matrix = (1, 0, 0, 1)
    for _ in range(exponent):
        result = _matrix_mul(result, matrix)
    return result


def _matrix(element: Element) -> Matrix:
    rotation, reflected = element
    value = _matrix_power(R, rotation)
    return _matrix_mul(value, F) if reflected else value


def _compose(left: Element, right: Element) -> Element:
    rotation, reflected = left
    other_rotation, other_reflected = right
    return (
        (rotation + (-1 if reflected else 1) * other_rotation) % 4,
        reflected ^ other_reflected,
    )


def _apply(matrix: Matrix, vector: tuple[Q, Q]) -> tuple[Q, Q]:
    a, b, c, d = matrix
    x, y = vector
    return (
        _q_add(_q_mul(_q(a), x), _q_mul(_q(b), y)),
        _q_add(_q_mul(_q(c), x), _q_mul(_q(d), y)),
    )


def _normalize_orientation(vector: tuple[Q, Q]) -> tuple[Q, Q]:
    x, y = vector
    _require(x != ZERO or y != ZERO, "zero orientation")
    _require(
        _q_add(_q_mul(x, x), _q_mul(y, y)) == ONE,
        "orientation is not an exact unit vector",
    )
    candidates = []
    current = vector
    for _ in range(4):
        candidates.append(current)
        current = _apply(R, current)
    return min(candidates)


def _verify_d4() -> tuple[Q, Q]:
    identity: Element = (0, 0)
    _require(len(set(D4_ELEMENTS)) == 8 and D4_ELEMENTS[0] == identity, "D4 order drift")
    products = 0
    homomorphisms = 0
    probe = (_q(Fraction(4, 5)), _q(Fraction(3, 5)))
    for element in D4_ELEMENTS:
        matrix = _matrix(element)
        _require(
            matrix[0] * matrix[3] - matrix[1] * matrix[2] == (-1) ** element[1],
            "D4 determinant drift",
        )
        _require(
            any(
                _compose(element, candidate) == identity
                and _compose(candidate, element) == identity
                for candidate in D4_ELEMENTS
            ),
            "D4 inverse missing",
        )
        for other in D4_ELEMENTS:
            product = _compose(element, other)
            _require(product in D4_ELEMENTS, "D4 closure drift")
            _require(
                _matrix(product) == _matrix_mul(matrix, _matrix(other)),
                "D4 composition/action drift",
            )
            _require(
                _apply(matrix, _apply(_matrix(other), probe))
                == _apply(_matrix(product), probe),
                "active-left homomorphism drift",
            )
            products += 1
            homomorphisms += 1
            for third in D4_ELEMENTS:
                _require(
                    _compose(_compose(element, other), third)
                    == _compose(element, _compose(other, third)),
                    "D4 associativity drift",
                )
    _require(products == 64 and homomorphisms == 64, "D4 replay count drift")
    original = _normalize_orientation(probe)
    reflected = _normalize_orientation(_apply(F, probe))
    _require(original != reflected, "reflection sign was preserved")
    return _normalize_orientation(_apply(_matrix((2, 0)), probe))


def _tau(label: str) -> str:
    _require(label.startswith(("B/", "T/")), "invalid half-turn label")
    return ("T/" if label.startswith("B/") else "B/") + label[2:]


def _verify_labels() -> None:
    _require(
        len(LOCAL_LABELS) == 27 and len(set(LOCAL_LABELS)) == 27, "local label inventory drift"
    )
    _require(
        len(FULL_LABELS) == 54 and len(set(FULL_LABELS)) == 54, "full label inventory drift"
    )
    for label in FULL_LABELS:
        partner = _tau(label)
        _require(partner != label, "half-turn has a fixed point")
        _require(partner in FULL_LABELS, "half-turn left label inventory")
        _require(_tau(partner) == label, "half-turn is not involutive")


def _fraction_text(value: Fraction) -> str:
    return str(value)


_FRACTION_TEXT = re.compile(r"(?:0|-?[1-9][0-9]*)(?:/[1-9][0-9]*)?\Z")


def _parse_fraction(value: object) -> Fraction:
    _require(
        type(value) is str and _FRACTION_TEXT.fullmatch(value), "noncanonical fraction string"
    )
    try:
        fraction = Fraction(cast(str, value))
    except (ValueError, ZeroDivisionError) as error:
        raise VerificationError("invalid fraction string") from error
    _require(_fraction_text(fraction) == value, "non-normal fraction string")
    return fraction


def _encoded_q(value: Q) -> list[str]:
    return [_fraction_text(coefficient) for coefficient in value]


def _verify_assignments(value: object, expected: list[tuple[str, Q]]) -> None:
    _require(type(value) is list and len(value) == 27, "assignment result inventory changed")
    items = cast(list[Any], value)
    for item, (name, coefficients) in zip(items, expected, strict=True):
        _require(
            type(item) is dict and set(item) == {"name", "coefficients"},
            "assignment result fields changed",
        )
        entry = cast(dict[str, Any], item)
        _require(entry["name"] == name, f"assignment name changed: {name}")
        encoded = entry["coefficients"]
        _require(
            type(encoded) is list and len(encoded) == 4, f"coefficient shape changed: {name}"
        )
        parsed = cast(Q, tuple(_parse_fraction(part) for part in encoded))
        _require(parsed == coefficients, f"assignment value changed: {name}")


def _validate_correspondence(items: list[dict[str, Any]]) -> None:
    expected_labels = set(FULL_LABELS)
    actual_labels = {item.get("source_label") for item in items}
    if len(items) != 54 or actual_labels != expected_labels:
        raise VerificationError("missing or unexpected synthetic source endpoint")
    row_ids = [item.get("row_id") for item in items]
    _require(
        len(set(row_ids)) == 54 and set(row_ids) == {f"w{index:02d}" for index in range(54)},
        "duplicate or missing opaque row endpoint",
    )
    for item in items:
        row_id = item.get("row_id")
        _require(type(row_id) is str, "opaque row id is not a string")
        expected_tag = f"tag-{cast(str, row_id)[1:]}"
        if item.get("structural_tag") != expected_tag:
            raise VerificationError("synthetic structural-tag drift")


def _perfect_matching_count(graph: dict[str, tuple[str, ...]], row_ids: set[str]) -> int:
    """Count perfect matchings up to two, which is enough to refuse ambiguity."""

    _require(set(graph) == set(FULL_LABELS), "compatibility source inventory changed")
    count = 0

    def search(remaining: tuple[str, ...], used: set[str]) -> None:
        nonlocal count
        if count >= 2:
            return
        if not remaining:
            count += 1
            return
        source = min(
            remaining,
            key=lambda label: sum(row not in used for row in graph[label]),
        )
        tail = tuple(label for label in remaining if label != source)
        for row_id in graph[source]:
            if row_id not in row_ids or row_id in used:
                continue
            search(tail, used | {row_id})

    search(FULL_LABELS, set())
    return count


def _matching_receipts() -> dict[str, dict[str, object]]:
    base = [
        {
            "source_label": label,
            "row_id": f"w{index:02d}",
            "structural_tag": f"tag-{index:02d}",
        }
        for index, label in enumerate(FULL_LABELS)
    ]
    _validate_correspondence(base)
    matching_actions = []
    for action in D4_ELEMENTS:
        graph = {
            label: ((f"w{index:02d}",) if action == (2, 0) else ())
            for index, label in enumerate(FULL_LABELS)
        }
        matching_count = _perfect_matching_count(
            graph, {f"w{index:02d}" for index in range(54)}
        )
        _require(matching_count <= 1, "second within-action perfect matching")
        if matching_count == 1:
            matching_actions.append(action)
    _require(matching_actions == [(2, 0)], "global matching is not uniquely minimal r2")

    missing = [dict(item) for item in base[:-1]]
    try:
        _validate_correspondence(missing)
    except VerificationError as error:
        missing_reason = str(error)
    else:
        raise VerificationError("missing-inventory mutation passed")

    swapped = [dict(item) for item in base]
    swapped[0]["row_id"], swapped[1]["row_id"] = (
        swapped[1]["row_id"],
        swapped[0]["row_id"],
    )
    try:
        _validate_correspondence(swapped)
    except VerificationError as error:
        swap_reason = str(error)
    else:
        raise VerificationError("correspondence-swap mutation passed")
    return {
        "missing_structural_inventory": {
            "rejected": True,
            "reason": missing_reason,
        },
        "correspondence_swap": {"rejected": True, "reason": swap_reason},
    }


def _verify_correspondence(value: object, orientation: tuple[Q, Q]) -> None:
    _require(
        type(value) is list and len(value) == 54, "correspondence result inventory changed"
    )
    raw_items = cast(list[Any], value)
    items: list[dict[str, Any]] = []
    for index, raw_item in enumerate(raw_items):
        _require(
            type(raw_item) is dict
            and set(raw_item) == {"source_label", "row_id", "structural_tag", "orientation"},
            "correspondence fields changed",
        )
        item = cast(dict[str, Any], raw_item)
        _require(
            item["source_label"] == FULL_LABELS[index], "correspondence label order changed"
        )
        encoded_orientation = item["orientation"]
        _require(
            type(encoded_orientation) is dict and set(encoded_orientation) == {"x", "y"},
            "orientation fields changed",
        )
        orientation_object = cast(dict[str, Any], encoded_orientation)
        for axis, expected in zip(("x", "y"), orientation, strict=True):
            encoded_axis = orientation_object[axis]
            _require(
                type(encoded_axis) is list and len(encoded_axis) == 4,
                "orientation coefficient shape changed",
            )
            parsed = cast(Q, tuple(_parse_fraction(part) for part in encoded_axis))
            _require(parsed == expected, f"normalized orientation {axis} changed")
        items.append(item)
    _validate_correspondence(items)
    for index, item in enumerate(items):
        _require(item["row_id"] == f"w{index:02d}", "global r2 row binding changed")
        _require(
            item["structural_tag"] == f"tag-{index:02d}",
            "synthetic structural-tag drift",
        )


def verify_result(fixture: Path, result: Path) -> dict[str, Any]:
    """Independently replay and verify the complete frozen synthetic result."""

    assignments = parse_fixture(fixture)
    _verify_labels()
    orientation = _verify_d4()
    mutation_receipts = _matching_receipts()
    document = load_result(result)
    _require(
        set(document)
        == {
            "schema",
            "scope",
            "fixture_sha256",
            "field_receipt_sha256",
            "witness_sha256",
            "d4",
            "assignments",
            "correspondence",
            "mutations",
            "claim_boundary",
        },
        "result field inventory changed",
    )
    _require(document["schema"] == SCHEMA, "result schema changed")
    _require(document["scope"] == SCOPE, "result scope changed")
    _require(document["fixture_sha256"] == FIXTURE_SHA256, "fixture binding changed")
    _require(
        document["field_receipt_sha256"] == FIELD_RECEIPT_SHA256,
        "field receipt binding changed",
    )
    _require(document["witness_sha256"] == WITNESS_SHA256, "witness metadata binding changed")
    _require(document["claim_boundary"] == CLAIM_BOUNDARY, "claim boundary changed")
    _require(
        _exact_equal(
            document["d4"],
            {
                "action": "r2",
                "elements": 8,
                "products": 64,
                "associativity_checks": 512,
                "homomorphism_checks": 64,
            },
        ),
        "D4 receipt changed",
    )
    _verify_assignments(document["assignments"], assignments)
    _verify_correspondence(document["correspondence"], orientation)
    _require(
        _exact_equal(document["mutations"], mutation_receipts),
        "mutation receipts changed",
    )
    return {
        "schema": VERIFICATION_SCHEMA,
        "verified": True,
        "fixture_sha256": FIXTURE_SHA256,
        "result_sha256": hashlib.sha256(result.read_bytes()).hexdigest(),
        "field_receipt_sha256": FIELD_RECEIPT_SHA256,
        "action": "r2",
        "assignments": 27,
        "correspondences": 54,
        "mutations": mutation_receipts,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    parser.add_argument("result", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        receipt = verify_result(arguments.fixture, arguments.result)
    except (OSError, VerificationError) as error:
        _parser().exit(1, f"verification failed: {error}\n")
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
