"""Implement the frozen synthetic source contract and author result for BC-141.

The author-side surface comprises the closed assignment parser, exact quartic-field
binding, D4 and orientation action, synthetic structural correspondence, and canonical
``N54Result/v1`` serialization frozen in session-082. Result-file publication,
independent verification, source and target access, and packing geometry are absent. The
module never interprets XML or delegates expression parsing or evaluation to another
language.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from fractions import Fraction
from typing import Final, Literal, NoReturn, cast

from devtools.audit_n54_source_formula import derive_receipt

MAX_INPUT_BYTES: Final = 65_536
MAX_COMMENTS: Final = 256
MAX_COMMENT_BYTES: Final = 4_096
MAX_ASSIGNMENTS: Final = 256
MAX_TOKENS_PER_FORMULA: Final = 256
MAX_EXPRESSION_DEPTH: Final = 32
MAX_INTEGER_DIGITS: Final = 18

_MARKER: Final = b"<!--@n54 "
_COMMENT_END: Final = b"-->"
_ASCII_WHITESPACE: Final = frozenset(b" \t\n")
BUILTINS: Final = frozenset({"s", "Sin[a]", "Cos[a]", "Tan[a]", "Sec[a]"})

EXPECTED_FIELD_RECEIPT_SHA256: Final = (
    "3555f8910e0daced8022576bea238951654fface93f0d0b51109c0efd3678cf4"
)
FIELD_POLYNOMIAL: Final = (1, 0, -2, 0, -1)
FIELD_BASIS: Final = ("1", "p", "p^2", "p^3")
EXPECTED_BASIS_COEFFICIENTS: Final = {
    "sqrt_two": ["-1", "0", "1", "0"],
    "sqrt_1_plus_5sqrt2": ["0", "-3", "0", "2"],
    "side": ["15/2", "1", "-1/2", "0"],
    "tan_angle": ["2/7", "-6/7", "1/7", "4/7"],
    "sin_angle": ["1/2", "-1", "0", "1/2"],
    "cos_angle": ["1", "1/2", "-1/2", "0"],
}
EXPECTED_MINIMAL_POLYNOMIALS: Final = {
    "side": [4, -112, 1164, -5304, 8897],
    "tan_angle": [7, -12, 6, -4, -1],
    "sin_angle": [8, -16, 16, -8, 1],
    "cos_angle": [8, -16, 0, 16, -7],
}

LOCAL_LABELS: Final = (
    *(f"stair/{index:02d}" for index in range(18)),
    "axis/00",
    *(f"rot/{index:02d}" for index in range(4)),
    "block/00/0",
    "block/00/1",
    "block/01/0",
    "block/01/1",
)
FULL_LABELS: Final = (
    *(f"B/{label}" for label in LOCAL_LABELS),
    *(f"T/{label}" for label in LOCAL_LABELS),
)
WITNESS_ROW_IDS: Final = tuple(f"w{index:02d}" for index in range(54))
WITNESS_SHA256: Final = "e4bcdefa3472e23ca7f4e403b26361efca17702c20570f6144b70c3a01a96ad7"
RESULT_SCHEMA: Final = "packing.squares:n54-source-contract/v1"
RESULT_SCOPE: Final = "synthetic-structure-only"
EXPECTED_FIXTURE_SHA256: Final = (
    "92ef9c467564f651efc561d69005c3b0cb847d13f4766ce0e16f365bde791de3"
)
CLAIM_BOUNDARY: Final = (
    "Prospective synthetic source-cell contract only; this establishes no source "
    "fidelity, actual row correspondence, precision cells, wall or pairwise geometry, "
    "feasibility, optimality or packing bound; H-055 remains instrument-unready."
)

type JsonValue = bool | int | str | list[JsonValue] | dict[str, JsonValue] | None


class ContractError(ValueError):
    """The synthetic transport, formula, or frozen label contract was refused."""


@dataclass(frozen=True, slots=True)
class FieldElement:
    """One exact element of Q(p) in the frozen basis 1, p, p^2, p^3."""

    coefficients: tuple[Fraction, ...]

    def __post_init__(self) -> None:
        if len(self.coefficients) != 4:
            raise ContractError("quartic-field element must have exactly four coefficients")

    @classmethod
    def from_values(
        cls,
        c0: int | Fraction = 0,
        c1: int | Fraction = 0,
        c2: int | Fraction = 0,
        c3: int | Fraction = 0,
    ) -> FieldElement:
        return cls(tuple(Fraction(value) for value in (c0, c1, c2, c3)))

    def __add__(self, other: FieldElement) -> FieldElement:
        return FieldElement(
            tuple(
                left + right
                for left, right in zip(self.coefficients, other.coefficients, strict=True)
            )
        )

    def __sub__(self, other: FieldElement) -> FieldElement:
        return FieldElement(
            tuple(
                left - right
                for left, right in zip(self.coefficients, other.coefficients, strict=True)
            )
        )

    def __neg__(self) -> FieldElement:
        return FieldElement(tuple(-coefficient for coefficient in self.coefficients))

    def __mul__(self, other: FieldElement) -> FieldElement:
        product = [Fraction(0) for _ in range(7)]
        for left_degree, left in enumerate(self.coefficients):
            for right_degree, right in enumerate(other.coefficients):
                product[left_degree + right_degree] += left * right
        for degree in range(6, 3, -1):
            coefficient = product[degree]
            product[degree] = Fraction(0)
            product[degree - 4] += coefficient
            product[degree - 2] += 2 * coefficient
        return FieldElement(tuple(product[:4]))

    def __rmul__(self, scalar: int) -> FieldElement:
        return FieldElement(tuple(scalar * coefficient for coefficient in self.coefficients))

    def __truediv__(self, other: FieldElement) -> FieldElement:
        return self * other.inverse()

    def inverse(self) -> FieldElement:
        """Invert any nonzero field element by exact Gaussian elimination."""

        if self.is_zero:
            raise ContractError("cannot invert the zero quartic-field element")
        basis = tuple(
            FieldElement.from_values(*(1 if row == column else 0 for row in range(4)))
            for column in range(4)
        )
        columns = tuple(self * element for element in basis)
        matrix = [
            [columns[column].coefficients[row] for column in range(4)]
            + [Fraction(1 if row == 0 else 0)]
            for row in range(4)
        ]
        for column in range(4):
            pivot = next(
                (row for row in range(column, 4) if matrix[row][column] != 0),
                None,
            )
            if pivot is None:
                raise ContractError("nonzero quartic-field element has no exact inverse")
            matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
            divisor = matrix[column][column]
            matrix[column] = [value / divisor for value in matrix[column]]
            for row in range(4):
                if row == column:
                    continue
                multiplier = matrix[row][column]
                if multiplier != 0:
                    matrix[row] = [
                        value - multiplier * pivot_value
                        for value, pivot_value in zip(matrix[row], matrix[column], strict=True)
                    ]
        return FieldElement(tuple(matrix[row][4] for row in range(4)))

    @property
    def is_zero(self) -> bool:
        return all(coefficient == 0 for coefficient in self.coefficients)


FIELD_ZERO: Final = FieldElement.from_values()
FIELD_ONE: Final = FieldElement.from_values(1)
FIELD_P: Final = FieldElement.from_values(0, 1)


@dataclass(frozen=True, slots=True)
class FieldBinding:
    """The audited receipt digest and exact builtin values admitted by the contract."""

    receipt_sha256: str
    symbols: tuple[tuple[str, FieldElement], ...]

    def value(self, name: str) -> FieldElement:
        for symbol, value in self.symbols:
            if symbol == name:
                return value
        raise ContractError(f"unknown quartic-field symbol: {name}")


@dataclass(frozen=True, slots=True)
class EvaluatedAssignment:
    """One parsed assignment evaluated exactly in the frozen quartic field."""

    name: str
    value: FieldElement


@dataclass(frozen=True, slots=True)
class EvaluatedFixture:
    """The ordered exact values of every assignment in one parsed fixture."""

    field_receipt_sha256: str
    assignments: tuple[EvaluatedAssignment, ...]


@dataclass(frozen=True, slots=True)
class D4Element:
    """One frozen dihedral element r^k f^b under the active-left convention."""

    quarter_turns: int
    reflected: bool = dataclass_field(kw_only=True)

    def __post_init__(self) -> None:
        if (
            not isinstance(self.quarter_turns, int)
            or isinstance(self.quarter_turns, bool)
            or not 0 <= self.quarter_turns < 4
            or not isinstance(self.reflected, bool)
        ):
            raise ContractError("invalid frozen D4 element")

    @property
    def name(self) -> str:
        rotation = ("e", "r", "r2", "r3")[self.quarter_turns]
        if not self.reflected:
            return rotation
        return "f" if self.quarter_turns == 0 else f"{rotation}f"

    @property
    def matrix(self) -> tuple[int, int, int, int]:
        a, b, c, d = (
            (1, 0, 0, 1),
            (0, -1, 1, 0),
            (-1, 0, 0, -1),
            (0, 1, -1, 0),
        )[self.quarter_turns]
        return (a, -b, c, -d) if self.reflected else (a, b, c, d)

    @property
    def determinant(self) -> int:
        a, b, c, d = self.matrix
        return a * d - b * c

    def compose(self, other: D4Element) -> D4Element:
        sign = -1 if self.reflected else 1
        return D4Element(
            (self.quarter_turns + sign * other.quarter_turns) % 4,
            reflected=self.reflected ^ other.reflected,
        )

    def inverse(self) -> D4Element:
        for candidate in D4_ORDER:
            if (
                self.compose(candidate) == D4_IDENTITY
                and candidate.compose(self) == D4_IDENTITY
            ):
                return candidate
        raise ContractError("frozen D4 element has no inverse")

    def apply_vector(
        self, vector: tuple[FieldElement, FieldElement]
    ) -> tuple[FieldElement, FieldElement]:
        a, b, c, d = self.matrix
        x, y = vector
        return (a * x + b * y, c * x + d * y)


D4_IDENTITY: Final = D4Element(0, reflected=False)
D4_ORDER: Final = tuple(
    D4Element(quarter_turns, reflected=reflected)
    for reflected in (False, True)
    for quarter_turns in range(4)
)


@dataclass(frozen=True, slots=True)
class OrientationVector:
    """One exact nonzero unit edge vector in the audited quartic field."""

    x: FieldElement
    y: FieldElement

    def __post_init__(self) -> None:
        if self.x.is_zero and self.y.is_zero:
            raise ContractError("orientation vector is zero")
        if self.x * self.x + self.y * self.y != FIELD_ONE:
            raise ContractError("orientation vector is not exactly unit")

    def quarter_turn(self, turns: int) -> OrientationVector:
        turns %= 4
        x, y = self.x, self.y
        for _ in range(turns):
            x, y = -y, x
        return OrientationVector(x, y)


@dataclass(frozen=True, slots=True)
class OrientationClass:
    """A quarter-turn equivalence class with its least exact representative."""

    representative: OrientationVector

    @classmethod
    def from_vector(cls, vector: OrientationVector) -> OrientationClass:
        orbit = tuple(vector.quarter_turn(turns) for turns in range(4))
        representative = min(
            orbit,
            key=lambda item: item.x.coefficients + item.y.coefficients,
        )
        return cls(representative)


def act_on_orientation(action: D4Element, orientation: OrientationClass) -> OrientationClass:
    """Apply one global active-left D4 action to an orientation class."""

    x, y = action.apply_vector((orientation.representative.x, orientation.representative.y))
    return OrientationClass.from_vector(OrientationVector(x, y))


@dataclass(frozen=True, slots=True)
class D4Replay:
    """Counts from a complete replay of the frozen D4 group and action."""

    elements: int
    products: int
    associativity_checks: int
    homomorphism_checks: int


def replay_d4_contract() -> D4Replay:
    """Replay all frozen D4 products, laws, matrices, and active-left actions."""

    if (
        tuple(element.name for element in D4_ORDER)
        != (
            "e",
            "r",
            "r2",
            "r3",
            "f",
            "rf",
            "r2f",
            "r3f",
        )
        or len(set(D4_ORDER)) != 8
    ):
        raise ContractError("frozen D4 order changed")
    products = 0
    homomorphisms = 0
    test_vector = (
        FieldElement.from_values(Fraction(4, 5)),
        FieldElement.from_values(Fraction(3, 5)),
    )
    for left in D4_ORDER:
        if left.compose(D4_IDENTITY) != left or D4_IDENTITY.compose(left) != left:
            raise ContractError("D4 identity law failed")
        if left.compose(left.inverse()) != D4_IDENTITY:
            raise ContractError("D4 inverse law failed")
        if left.determinant != (-1 if left.reflected else 1):
            raise ContractError("D4 determinant law failed")
        for right in D4_ORDER:
            product = left.compose(right)
            if product not in D4_ORDER:
                raise ContractError("D4 product escaped the frozen group")
            if _multiply_matrices(left.matrix, right.matrix) != product.matrix:
                raise ContractError("D4 composition and matrix multiplication disagree")
            acted = left.apply_vector(right.apply_vector(test_vector))
            if acted != product.apply_vector(test_vector):
                raise ContractError("D4 active-left action homomorphism failed")
            products += 1
            homomorphisms += 1
    associativity = 0
    for first in D4_ORDER:
        for second in D4_ORDER:
            for third in D4_ORDER:
                if first.compose(second).compose(third) != first.compose(second.compose(third)):
                    raise ContractError("D4 associativity failed")
                associativity += 1
    return D4Replay(8, products, associativity, homomorphisms)


def _multiply_matrices(
    left: tuple[int, int, int, int], right: tuple[int, int, int, int]
) -> tuple[int, int, int, int]:
    a, b, c, d = left
    e, f, g, h = right
    return (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h)


@dataclass(frozen=True, slots=True)
class SyntheticEndpoint:
    """One source label or opaque witness-row id with a synthetic structural tag."""

    identifier: str
    structural_tag: str


@dataclass(frozen=True, slots=True)
class CompatibilityEdge:
    """One synthetic compatibility edge under a single global D4 action."""

    action: D4Element
    source_label: str
    row_id: str
    structural_tag: str
    orientation: OrientationVector


@dataclass(frozen=True, slots=True)
class CorrespondencePair:
    """One selected opaque correspondence and canonical orientation class."""

    source_label: str
    row_id: str
    structural_tag: str
    orientation: OrientationClass


@dataclass(frozen=True, slots=True)
class SyntheticCorrespondence:
    """The first uniquely matching global action over synthetic structure only."""

    action: D4Element
    witness_sha256: str
    pairs: tuple[CorrespondencePair, ...]


def _endpoint_map(
    endpoints: Sequence[SyntheticEndpoint],
    expected: tuple[str, ...],
    label: str,
) -> dict[str, SyntheticEndpoint]:
    identifiers = tuple(endpoint.identifier for endpoint in endpoints)
    if len(identifiers) != len(set(identifiers)):
        raise ContractError(f"duplicate synthetic {label} endpoint")
    if set(identifiers) != set(expected):
        raise ContractError(f"missing or unexpected synthetic {label} endpoint")
    mapped = {endpoint.identifier: endpoint for endpoint in endpoints}
    if any(not endpoint.structural_tag for endpoint in endpoints):
        raise ContractError(f"empty synthetic {label} structural tag")
    return mapped


def _perfect_matchings(
    candidates: Mapping[str, tuple[str, ...]],
) -> tuple[tuple[tuple[str, str], ...], ...]:
    solutions: list[tuple[tuple[str, str], ...]] = []

    def search(remaining: tuple[str, ...], used: frozenset[str], pairs: dict[str, str]) -> None:
        if len(solutions) >= 2:
            return
        if not remaining:
            solutions.append(tuple((label, pairs[label]) for label in FULL_LABELS))
            return
        source = min(
            remaining,
            key=lambda label: (
                len([row for row in candidates[label] if row not in used]),
                label,
            ),
        )
        choices = tuple(row for row in candidates[source] if row not in used)
        following = tuple(label for label in remaining if label != source)
        for row in choices:
            pairs[source] = row
            search(following, used | {row}, pairs)
            del pairs[source]
            if len(solutions) >= 2:
                return

    search(FULL_LABELS, frozenset(), {})
    return tuple(solutions)


def select_synthetic_correspondence(
    source_endpoints: Sequence[SyntheticEndpoint],
    row_endpoints: Sequence[SyntheticEndpoint],
    edges: Sequence[CompatibilityEdge],
    *,
    declared_action: D4Element | None = None,
) -> SyntheticCorrespondence:
    """Select the first unique synthetic matching without reading witness-row values."""

    sources = _endpoint_map(source_endpoints, FULL_LABELS, "source")
    rows = _endpoint_map(row_endpoints, WITNESS_ROW_IDS, "row")
    edge_keys: set[tuple[D4Element, str, str]] = set()
    for edge in edges:
        key = (edge.action, edge.source_label, edge.row_id)
        if key in edge_keys:
            raise ContractError("duplicate synthetic compatibility edge")
        edge_keys.add(key)
        if edge.source_label not in sources or edge.row_id not in rows:
            raise ContractError("compatibility edge has a missing endpoint")
        if (
            edge.structural_tag != sources[edge.source_label].structural_tag
            or edge.structural_tag != rows[edge.row_id].structural_tag
        ):
            raise ContractError("synthetic structural-tag drift")

    unique: list[tuple[D4Element, tuple[tuple[str, str], ...]]] = []
    for action in D4_ORDER:
        candidates = {
            label: tuple(
                edge.row_id
                for edge in edges
                if edge.action == action and edge.source_label == label
            )
            for label in FULL_LABELS
        }
        matchings = _perfect_matchings(candidates)
        if len(matchings) > 1:
            raise ContractError(f"second perfect matching for global action: {action.name}")
        if matchings:
            unique.append((action, matchings[0]))
    if not unique:
        raise ContractError("no synthetic perfect matching")
    action, matching = unique[0]
    if declared_action is not None and declared_action != action:
        raise ContractError("declared global action is not the first unique matching action")
    selected_edges = {(edge.action, edge.source_label, edge.row_id): edge for edge in edges}
    pairs = tuple(
        CorrespondencePair(
            source_label,
            row_id,
            sources[source_label].structural_tag,
            act_on_orientation(
                action,
                OrientationClass.from_vector(
                    selected_edges[(action, source_label, row_id)].orientation
                ),
            ),
        )
        for source_label, row_id in matching
    )
    return SyntheticCorrespondence(action, WITNESS_SHA256, pairs)


@dataclass(frozen=True, slots=True)
class Integer:
    """One unsigned integer literal, normalized to its numerical value."""

    value: int


@dataclass(frozen=True, slots=True)
class Symbol:
    """One builtin or previously defined, case-sensitive symbol."""

    name: str


@dataclass(frozen=True, slots=True)
class Negation:
    """One unary negation."""

    operand: Expression


type BinaryOperator = Literal["add", "subtract", "multiply", "divide"]


@dataclass(frozen=True, slots=True)
class Binary:
    """One closed binary arithmetic node."""

    operator: BinaryOperator
    left: Expression
    right: Expression


type Expression = Integer | Symbol | Negation | Binary
type CanonicalExpression = tuple[object, ...]


@dataclass(frozen=True, slots=True)
class Assignment:
    """One unique identifier and its closed expression AST."""

    name: str
    expression: Expression


@dataclass(frozen=True, slots=True)
class ParsedFixture:
    """The ordered assignments carried by one fully consumed synthetic fixture."""

    assignments: tuple[Assignment, ...]


@dataclass(frozen=True, slots=True)
class LabelInventory:
    """The frozen 27 local labels and their disjoint B/T half-turn orbits."""

    local: tuple[str, ...]
    full: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class _Token:
    kind: Literal["uint", "symbol", "operator", "eof"]
    text: str
    offset: int


def canonical_expression(expression: Expression) -> CanonicalExpression:
    """Return the unique prefix tuple for one immutable AST."""

    if isinstance(expression, Integer):
        return ("integer", str(expression.value))
    if isinstance(expression, Symbol):
        return ("symbol", expression.name)
    if isinstance(expression, Negation):
        return ("negation", canonical_expression(expression.operand))
    return (
        expression.operator,
        canonical_expression(expression.left),
        canonical_expression(expression.right),
    )


def _receipt_bytes(receipt: Mapping[str, object]) -> bytes:
    try:
        return (json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    except (TypeError, ValueError) as error:
        raise ContractError("quartic-field receipt is not exact JSON data") from error


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, dict):
        raise ContractError(f"quartic-field receipt {label} is not an object")
    return value


def _evaluate_polynomial(coefficients: list[int], value: FieldElement) -> FieldElement:
    result = FIELD_ZERO
    for coefficient in coefficients:
        result = result * value + FieldElement.from_values(coefficient)
    return result


def bind_field_receipt(
    receipt: Mapping[str, object] | None = None,
) -> FieldBinding:
    """Bind the readmitted audit receipt and construct the frozen exact builtins."""

    document = derive_receipt() if receipt is None else receipt
    expected_top_keys = {
        "field",
        "basis_order",
        "basis_coefficients",
        "minimal_polynomials",
        "decimal_check",
        "checks",
        "scope",
    }
    if set(document) != expected_top_keys:
        raise ContractError("quartic-field receipt inventory changed")
    field = _mapping(document.get("field"), "field")
    if set(field) != {
        "name",
        "primitive",
        "minimal_polynomial_coefficients",
        "embedding",
    }:
        raise ContractError("quartic-field receipt field inventory changed")
    if field.get("name") != "Q(p)":
        raise ContractError("quartic-field receipt field name changed")
    if field.get("primitive") != "p = sqrt(1 + sqrt(2))":
        raise ContractError("quartic-field receipt primitive changed")
    if field.get("minimal_polynomial_coefficients") != list(FIELD_POLYNOMIAL):
        raise ContractError("quartic-field receipt field polynomial changed")
    if field.get("embedding") != "positive real root p in (1.5537, 1.5538)":
        raise ContractError("quartic-field receipt positive embedding changed")
    if document.get("basis_order") != list(FIELD_BASIS):
        raise ContractError("quartic-field receipt basis order changed")
    if document.get("basis_coefficients") != EXPECTED_BASIS_COEFFICIENTS:
        raise ContractError("quartic-field receipt basis coefficients changed")
    if document.get("minimal_polynomials") != EXPECTED_MINIMAL_POLYNOMIALS:
        raise ContractError("quartic-field receipt minimal polynomials changed")

    digest = hashlib.sha256(_receipt_bytes(document)).hexdigest()
    if digest != EXPECTED_FIELD_RECEIPT_SHA256:
        raise ContractError("quartic-field receipt SHA-256 changed")

    side = FieldElement.from_values(Fraction(15, 2), 1, Fraction(-1, 2))
    tangent = FieldElement.from_values(
        Fraction(2, 7), Fraction(-6, 7), Fraction(1, 7), Fraction(4, 7)
    )
    sine = FieldElement.from_values(Fraction(1, 2), -1, 0, Fraction(1, 2))
    cosine = FieldElement.from_values(1, Fraction(1, 2), Fraction(-1, 2))
    secant = cosine.inverse()
    symbols = (
        ("s", side),
        ("Sin[a]", sine),
        ("Cos[a]", cosine),
        ("Tan[a]", tangent),
        ("Sec[a]", secant),
    )
    if FIELD_P * FIELD_P * FIELD_P * FIELD_P - 2 * FIELD_P * FIELD_P - FIELD_ONE != FIELD_ZERO:
        raise ContractError("quartic-field reduction does not satisfy its polynomial")
    field_values = {
        "side": side,
        "tan_angle": tangent,
        "sin_angle": sine,
        "cos_angle": cosine,
    }
    for name, polynomial in EXPECTED_MINIMAL_POLYNOMIALS.items():
        if not _evaluate_polynomial(polynomial, field_values[name]).is_zero:
            raise ContractError(f"quartic-field builtin fails its minimal polynomial: {name}")
    if sine / cosine != tangent:
        raise ContractError("quartic-field orientation ratio disagrees with tangent")
    if sine * sine + cosine * cosine != FIELD_ONE:
        raise ContractError("quartic-field orientation vector is not a unit vector")
    if secant * cosine != FIELD_ONE:
        raise ContractError("Sec[a] is not the exact inverse of Cos[a]")
    return FieldBinding(digest, symbols)


def _evaluate_expression(
    expression: Expression,
    binding: FieldBinding,
    definitions: Mapping[str, FieldElement],
) -> FieldElement:
    result: FieldElement
    if isinstance(expression, Integer):
        result = FieldElement.from_values(expression.value)
    elif isinstance(expression, Symbol):
        if expression.name in BUILTINS:
            result = binding.value(expression.name)
        else:
            try:
                result = definitions[expression.name]
            except KeyError as error:
                raise ContractError(
                    f"missing earlier quartic-field assignment: {expression.name}"
                ) from error
    elif isinstance(expression, Negation):
        result = -_evaluate_expression(expression.operand, binding, definitions)
    else:
        left = _evaluate_expression(expression.left, binding, definitions)
        right = _evaluate_expression(expression.right, binding, definitions)
        if expression.operator == "add":
            result = left + right
        elif expression.operator == "subtract":
            result = left - right
        elif expression.operator == "multiply":
            result = left * right
        else:
            if right.is_zero:
                raise ContractError("formula denominator is algebraically zero in Q(p)")
            result = left / right
    return result


def evaluate_fixture(
    parsed: ParsedFixture,
    receipt: Mapping[str, object] | None = None,
) -> EvaluatedFixture:
    """Evaluate every parsed formula exactly after binding the audited field receipt."""

    binding = bind_field_receipt(receipt)
    definitions: dict[str, FieldElement] = {}
    evaluated: list[EvaluatedAssignment] = []
    for assignment in parsed.assignments:
        value = _evaluate_expression(assignment.expression, binding, definitions)
        definitions[assignment.name] = value
        evaluated.append(EvaluatedAssignment(assignment.name, value))
    return EvaluatedFixture(binding.receipt_sha256, tuple(evaluated))


def half_turn_label(label: str) -> str:
    """Apply the fixed-point-free B/T involution to one frozen full label."""

    if label.startswith("B/") and label[2:] in LOCAL_LABELS:
        return f"T/{label[2:]}"
    if label.startswith("T/") and label[2:] in LOCAL_LABELS:
        return f"B/{label[2:]}"
    raise ContractError(f"unknown n = 54 source-cell label: {label}")


def label_inventory() -> LabelInventory:
    """Build and replay the frozen 27 plus 27 semantic label inventory."""

    if len(LOCAL_LABELS) != 27 or len(set(LOCAL_LABELS)) != 27:
        raise ContractError("local label inventory is not exactly 27 unique labels")
    if len(FULL_LABELS) != 54 or len(set(FULL_LABELS)) != 54:
        raise ContractError("full label inventory is not exactly 54 unique labels")
    images = tuple(half_turn_label(label) for label in FULL_LABELS)
    if len(set(images)) != 54:
        raise ContractError("half-turn label action is not injective")
    for label, image in zip(FULL_LABELS, images, strict=True):
        if image == label or half_turn_label(image) != label:
            raise ContractError("half-turn label action is not fixed-point-free and involutive")
    return LabelInventory(LOCAL_LABELS, FULL_LABELS)


def _tokenize(payload: str) -> tuple[_Token, ...]:
    tokens: list[_Token] = []
    cursor = 0
    while cursor < len(payload):
        character = payload[cursor]
        if character in " \t\n":
            cursor += 1
            continue
        start = cursor
        builtin = next(
            (
                candidate
                for candidate in ("Sin[a]", "Cos[a]", "Tan[a]", "Sec[a]")
                if payload.startswith(candidate, cursor)
            ),
            None,
        )
        if builtin is not None:
            tokens.append(_Token("symbol", builtin, start))
            cursor += len(builtin)
        elif character.isdigit():
            cursor += 1
            while cursor < len(payload) and payload[cursor].isdigit():
                cursor += 1
            text = payload[start:cursor]
            if len(text) > MAX_INTEGER_DIGITS:
                raise ContractError("integer literal exceeds the 18-digit bound")
            tokens.append(_Token("uint", text, start))
        elif character.isalpha() or character == "_":
            cursor += 1
            while cursor < len(payload) and (
                payload[cursor].isalnum() or payload[cursor] == "_"
            ):
                cursor += 1
            tokens.append(_Token("symbol", payload[start:cursor], start))
        elif character in "=+-*/()":
            tokens.append(_Token("operator", character, start))
            cursor += 1
        else:
            raise ContractError(f"unsupported formula character at byte {start}: {character!r}")
        if len(tokens) > MAX_TOKENS_PER_FORMULA:
            raise ContractError("formula exceeds the 256-token bound")
    tokens.append(_Token("eof", "", len(payload)))
    return tuple(tokens)


class _FormulaParser:
    def __init__(
        self,
        payload: str,
        definitions: dict[str, Expression],
    ) -> None:
        self._tokens = _tokenize(payload)
        self._cursor = 0
        self._definitions = definitions
        self._zero_cache: dict[Expression, bool] = {}

    def parse_assignment(self) -> Assignment:
        name_token = self._take_symbol("assignment identifier")
        name = name_token.text
        if name in BUILTINS:
            raise ContractError(f"builtin cannot be assigned: {name}")
        if name in self._definitions:
            raise ContractError(f"duplicate assignment identifier: {name}")
        self._take_operator("=")
        expression = self._parse_sum(0)
        token = self._peek()
        if token.kind != "eof":
            raise ContractError(
                f"trailing formula token at byte {token.offset}: {token.text!r}"
            )
        return Assignment(name, expression)

    def _parse_sum(self, depth: int) -> Expression:
        self._check_depth(depth)
        expression = self._parse_product(depth)
        while self._peek().text in {"+", "-"}:
            operator = self._advance().text
            right = self._parse_product(depth)
            expression = Binary("add" if operator == "+" else "subtract", expression, right)
        return expression

    def _parse_product(self, depth: int) -> Expression:
        self._check_depth(depth)
        expression = self._parse_unary(depth)
        while self._peek().text in {"*", "/"}:
            operator = self._advance().text
            right = self._parse_unary(depth)
            if operator == "/" and self._definitely_zero(right):
                raise ContractError("formula denominator is zero")
            expression = Binary("multiply" if operator == "*" else "divide", expression, right)
        return expression

    def _parse_unary(self, depth: int) -> Expression:
        self._check_depth(depth)
        token = self._peek()
        if token.text in {"+", "-"}:
            self._advance()
            primary = self._parse_primary(depth + 1)
            return primary if token.text == "+" else Negation(primary)
        return self._parse_primary(depth)

    def _parse_primary(self, depth: int) -> Expression:
        self._check_depth(depth)
        token = self._peek()
        if token.kind == "uint":
            self._advance()
            return Integer(int(token.text))
        if token.kind == "symbol":
            self._advance()
            if token.text not in BUILTINS and token.text not in self._definitions:
                raise ContractError(f"undefined or forward formula reference: {token.text}")
            return Symbol(token.text)
        if token.text == "(":
            self._advance()
            expression = self._parse_sum(depth + 1)
            self._take_operator(")")
            return expression
        raise ContractError(f"expected formula primary at byte {token.offset}")

    def _definitely_zero(self, expression: Expression) -> bool:
        cached = self._zero_cache.get(expression)
        if cached is not None:
            return cached

        result = False
        if isinstance(expression, Integer):
            result = expression.value == 0
        elif isinstance(expression, Symbol):
            definition = self._definitions.get(expression.name)
            result = definition is not None and self._definitely_zero(definition)
        elif isinstance(expression, Negation):
            result = self._definitely_zero(expression.operand)
        elif expression.operator == "subtract":
            result = canonical_expression(expression.left) == canonical_expression(
                expression.right
            )
        elif expression.operator == "multiply":
            result = self._definitely_zero(expression.left) or self._definitely_zero(
                expression.right
            )
        elif expression.operator == "add":
            if isinstance(expression.left, Negation):
                result = canonical_expression(expression.left.operand) == canonical_expression(
                    expression.right
                )
            elif isinstance(expression.right, Negation):
                result = canonical_expression(expression.left) == canonical_expression(
                    expression.right.operand
                )
        self._zero_cache[expression] = result
        return result

    def _check_depth(self, depth: int) -> None:
        if depth > MAX_EXPRESSION_DEPTH:
            raise ContractError("formula exceeds the expression-depth bound")

    def _peek(self) -> _Token:
        return self._tokens[self._cursor]

    def _advance(self) -> _Token:
        token = self._peek()
        self._cursor += 1
        return token

    def _take_symbol(self, label: str) -> _Token:
        token = self._peek()
        if token.kind != "symbol":
            raise ContractError(f"expected {label} at byte {token.offset}")
        return self._advance()

    def _take_operator(self, expected: str) -> None:
        token = self._peek()
        if token.kind != "operator" or token.text != expected:
            raise ContractError(f"expected {expected!r} at byte {token.offset}")
        self._advance()


def _validate_transport(content: bytes) -> None:
    if len(content) > MAX_INPUT_BYTES:
        raise ContractError("synthetic fixture exceeds the 65,536-byte bound")
    try:
        content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ContractError("synthetic fixture is not valid UTF-8") from error
    if not content.isascii():
        raise ContractError("synthetic fixture contains non-ASCII contract text")
    if b"\0" in content:
        raise ContractError("synthetic fixture contains NUL")
    if b"\r" in content:
        raise ContractError("synthetic fixture contains carriage return")
    folded = content.lower()
    if b"<!doctype" in folded or b"<!entity" in folded:
        raise ContractError("DTD and entity markers are forbidden")


def parse_fixture(content: bytes) -> ParsedFixture:
    """Fully consume ordered marked comments into unique closed assignments."""

    _validate_transport(content)
    cursor = 0
    assignments: list[Assignment] = []
    definitions: dict[str, Expression] = {}
    while cursor < len(content):
        while cursor < len(content) and content[cursor] in _ASCII_WHITESPACE:
            cursor += 1
        if cursor == len(content):
            break
        if not content.startswith(_MARKER, cursor):
            raise ContractError(f"unmarked transport content at byte {cursor}")
        if len(assignments) >= MAX_COMMENTS:
            raise ContractError("synthetic fixture exceeds the 256-comment bound")
        payload_start = cursor + len(_MARKER)
        payload_end = content.find(_COMMENT_END, payload_start)
        if payload_end < 0:
            raise ContractError("unterminated marked comment")
        payload_bytes = content[payload_start:payload_end]
        if b"<!--" in payload_bytes:
            raise ContractError("nested comments are forbidden")
        if len(payload_bytes) > MAX_COMMENT_BYTES:
            raise ContractError("marked comment exceeds the 4,096-byte bound")
        payload = payload_bytes.decode("ascii")
        assignment = _FormulaParser(payload, definitions).parse_assignment()
        definitions[assignment.name] = assignment.expression
        assignments.append(assignment)
        if len(assignments) > MAX_ASSIGNMENTS:
            raise ContractError("synthetic fixture exceeds the 256-assignment bound")
        cursor = payload_end + len(_COMMENT_END)
    if not assignments:
        raise ContractError("synthetic fixture contains no marked assignments")
    return ParsedFixture(tuple(assignments))


def _validate_json_value(value: object) -> None:
    if value is None or isinstance(value, (str, bool)):
        return
    if isinstance(value, int):
        return
    if isinstance(value, float):
        raise ContractError("floating JSON values are forbidden")
    if isinstance(value, list):
        for item in value:
            _validate_json_value(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ContractError("JSON object keys must be strings")
            _validate_json_value(item)
        return
    raise ContractError(f"unsupported canonical JSON value: {type(value).__name__}")


def canonical_json_bytes(value: object) -> bytes:
    """Encode one strict JSON value canonically with exactly one terminal newline."""

    _validate_json_value(value)
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
            allow_nan=False,
        )
        + "\n"
    ).encode("ascii")


def _strict_object(pairs: list[tuple[str, JsonValue]]) -> dict[str, JsonValue]:
    result: dict[str, JsonValue] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _reject_json_float(text: str) -> NoReturn:
    raise ContractError(f"floating or exponent JSON number is forbidden: {text}")


def _reject_json_constant(text: str) -> NoReturn:
    raise ContractError(f"non-finite JSON value is forbidden: {text}")


def load_canonical_json(content: bytes) -> JsonValue:
    """Load strict JSON and require byte-for-byte canonical representation."""

    try:
        value = cast(
            JsonValue,
            json.loads(
                content,
                object_pairs_hook=_strict_object,
                parse_float=_reject_json_float,
                parse_constant=_reject_json_constant,
            ),
        )
    except ContractError:
        raise
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ContractError("invalid canonical JSON") from error
    if canonical_json_bytes(value) != content:
        raise ContractError("JSON bytes are not canonical")
    return value


def _fraction_string(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def _field_coefficients(value: FieldElement) -> list[JsonValue]:
    return [_fraction_string(coefficient) for coefficient in value.coefficients]


def _record_refusal(
    operation: Callable[[], object], expected_reason: str
) -> dict[str, JsonValue]:
    try:
        operation()
    except ContractError as error:
        reason = str(error)
    else:
        raise ContractError("required synthetic mutation was not refused")
    if reason != expected_reason:
        raise ContractError(f"required synthetic mutation refusal drift: {reason!r}")
    return {"rejected": True, "reason": reason}


def build_n54_result(fixture_content: bytes) -> dict[str, JsonValue]:
    """Build the frozen synthetic ``N54Result/v1`` object from fixture bytes."""

    fixture_sha256 = hashlib.sha256(fixture_content).hexdigest()
    if fixture_sha256 != EXPECTED_FIXTURE_SHA256:
        raise ContractError("synthetic fixture SHA-256 drift")
    parsed = parse_fixture(fixture_content)
    evaluated = evaluate_fixture(parsed)
    replay = replay_d4_contract()

    action = D4Element(2, reflected=False)
    tags = tuple(f"tag-{index:02d}" for index in range(54))
    sources = tuple(
        SyntheticEndpoint(label, tags[index]) for index, label in enumerate(FULL_LABELS)
    )
    rows = tuple(
        SyntheticEndpoint(row_id, tags[index]) for index, row_id in enumerate(WITNESS_ROW_IDS)
    )
    orientation = OrientationVector(
        FieldElement.from_values(Fraction(4, 5)),
        FieldElement.from_values(Fraction(3, 5)),
    )
    edges = tuple(
        CompatibilityEdge(
            action,
            label,
            WITNESS_ROW_IDS[index],
            tags[index],
            orientation,
        )
        for index, label in enumerate(FULL_LABELS)
    )
    correspondence = select_synthetic_correspondence(
        sources,
        rows,
        edges,
        declared_action=action,
    )

    missing_reason = "missing or unexpected synthetic source endpoint"
    missing = _record_refusal(
        lambda: select_synthetic_correspondence(
            sources[:-1], rows, edges, declared_action=action
        ),
        missing_reason,
    )
    swapped_edges = (
        CompatibilityEdge(
            action,
            edges[0].source_label,
            edges[1].row_id,
            edges[0].structural_tag,
            edges[0].orientation,
        ),
        CompatibilityEdge(
            action,
            edges[1].source_label,
            edges[0].row_id,
            edges[1].structural_tag,
            edges[1].orientation,
        ),
        *edges[2:],
    )
    swap = _record_refusal(
        lambda: select_synthetic_correspondence(
            sources, rows, swapped_edges, declared_action=action
        ),
        "synthetic structural-tag drift",
    )

    assignments: list[JsonValue] = [
        {
            "name": assignment.name,
            "coefficients": _field_coefficients(assignment.value),
        }
        for assignment in evaluated.assignments
    ]
    pairs: list[JsonValue] = [
        {
            "source_label": pair.source_label,
            "row_id": pair.row_id,
            "structural_tag": pair.structural_tag,
            "orientation": {
                "x": _field_coefficients(pair.orientation.representative.x),
                "y": _field_coefficients(pair.orientation.representative.y),
            },
        }
        for pair in correspondence.pairs
    ]
    return {
        "schema": RESULT_SCHEMA,
        "scope": RESULT_SCOPE,
        "fixture_sha256": fixture_sha256,
        "field_receipt_sha256": evaluated.field_receipt_sha256,
        "witness_sha256": correspondence.witness_sha256,
        "d4": {
            "action": action.name,
            "elements": replay.elements,
            "products": replay.products,
            "associativity_checks": replay.associativity_checks,
            "homomorphism_checks": replay.homomorphism_checks,
        },
        "assignments": assignments,
        "correspondence": pairs,
        "mutations": {
            "missing_structural_inventory": missing,
            "correspondence_swap": swap,
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_n54_result_bytes(fixture_content: bytes) -> bytes:
    """Build canonical bytes for the frozen synthetic ``N54Result/v1`` object."""

    return canonical_json_bytes(build_n54_result(fixture_content))
