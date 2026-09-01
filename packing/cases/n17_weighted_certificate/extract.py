"""Hash-pinned, nonexecuting extraction of literal certificate assignments."""

from __future__ import annotations

import ast
import hashlib
from fractions import Fraction
from pathlib import Path
from typing import Any


class StaticExtractionError(ValueError):
    """The retained file cannot be reduced to the declared literal data boundary."""


def verified_source(path: Path, expected_sha256: str) -> str:
    raw = path.read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if actual != expected_sha256:
        raise StaticExtractionError(
            f"source hash mismatch for {path}: expected {expected_sha256}, got {actual}"
        )
    return raw.decode("utf-8")


def _safe_value(node: ast.AST, known: dict[str, Any]) -> Any:  # noqa: PLR0911
    if isinstance(node, ast.Constant) and isinstance(node.value, int | str):
        return node.value
    if isinstance(node, ast.Name) and node.id in known:
        return known[node.id]
    if isinstance(node, ast.Tuple):
        return tuple(_safe_value(item, known) for item in node.elts)
    if isinstance(node, ast.List):
        return [_safe_value(item, known) for item in node.elts]
    if isinstance(node, ast.Dict):
        result: dict[Any, Any] = {}
        for key, value in zip(node.keys, node.values, strict=True):
            if key is None:
                raise StaticExtractionError("dictionary unpacking is not static data")
            result[_safe_value(key, known)] = _safe_value(value, known)
        return result
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_safe_value(node.operand, known)
    if isinstance(node, ast.BinOp):
        left = _safe_value(node.left, known)
        right = _safe_value(node.right, known)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return Fraction(left, right)
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "Fraction"
        and not node.keywords
        and 1 <= len(node.args) <= 2
    ):
        args = [_safe_value(arg, known) for arg in node.args]
        return Fraction(*args)
    raise StaticExtractionError(f"unsupported static expression: {ast.dump(node)}")


def literal_assignments(path: Path, expected_sha256: str, names: set[str]) -> dict[str, Any]:
    """Read only declared top-level assignments; never compile or execute the source."""

    tree = ast.parse(verified_source(path, expected_sha256), filename=str(path))
    known: dict[str, Any] = {}
    selected: dict[str, Any] = {}
    for statement in tree.body:
        if not isinstance(statement, ast.Assign) or len(statement.targets) != 1:
            continue
        target = statement.targets[0]
        if not isinstance(target, ast.Name):
            continue
        try:
            value = _safe_value(statement.value, known)
        except StaticExtractionError:
            if target.id in names:
                raise
            continue
        known[target.id] = value
        if target.id in names:
            selected[target.id] = value
    missing = names - selected.keys()
    if missing:
        raise StaticExtractionError(f"missing static assignments: {sorted(missing)}")
    return selected
