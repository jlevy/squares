"""Independent whole-result verifier for the UnitSquare production adapter."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from cases.unitsquare_precision.refusal.run import RunnerContract
from cases.unitsquare_precision.refusal.verify import verify_proof

_DIGEST = re.compile(r"[0-9a-f]{64}\Z")
_MODELS = ("declared:svg-literal", "nearest-6", "truncate-6")
_REFUSALS = {
    "pose-compatibility-refusal",
    "serialization-refusal",
    "affine-transform-refusal",
    "unresolved",
}
_FORBIDDEN_KEYS = {
    "buffer",
    "child",
    "gain",
    "header",
    "headers",
    "palette",
    "path",
    "raw",
    "response",
    "temp",
    "temporary",
    "xml",
}


class ResultVerificationError(ValueError):
    """The complete sanitized runner result did not replay independently."""


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ResultVerificationError(f"{label} must be an object")
    return value


def _digest(value: object, label: str) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        raise ResultVerificationError(f"{label} is not a SHA-256 digest")
    return value


def _verify_sanitized(value: object) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ResultVerificationError("result contains a non-string key")
            tokens = set(re.findall(r"[a-z0-9]+", key.lower()))
            forbidden = tokens & _FORBIDDEN_KEYS
            if forbidden:
                raise ResultVerificationError(
                    f"result contains forbidden retained key: {sorted(forbidden)[0]}"
                )
            _verify_sanitized(item)
        return
    if isinstance(value, list):
        for item in value:
            _verify_sanitized(item)
        return
    if isinstance(value, str) and ("<svg" in value.lower() or "<?xml" in value.lower()):
        raise ResultVerificationError("result contains source markup")
    if value is not None and not isinstance(value, (str, int, bool)):
        raise ResultVerificationError("result contains a non-exact JSON scalar")


def _exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise ResultVerificationError(f"{label} fields are incomplete")


def _verify_cover_shape(value: object) -> None:
    node = _mapping(value, "cover node")
    kind = node.get("kind")
    if kind == "split":
        _exact_keys(
            node,
            {"kind", "region", "axis", "cut", "lower", "upper"},
            "cover split",
        )
        _verify_cover_shape(node.get("lower"))
        _verify_cover_shape(node.get("upper"))
        return
    if kind != "leaf":
        raise ResultVerificationError("cover node kind is invalid")
    expected = {"kind", "region", "status", "reason"}
    status = node.get("status")
    if status == "retained":
        expected.add("corner_images")
    elif status == "rejected":
        expected.add("rejection")
    else:
        raise ResultVerificationError("cover leaf status is invalid")
    _exact_keys(node, expected, "cover leaf")


def _verify_proof_shape(proof: dict[str, Any]) -> None:
    _exact_keys(
        proof,
        {"format", "binding", "witness", "cover", "wall_signs", "pair_controls"},
        "proof",
    )
    binding = _mapping(proof.get("binding"), "proof binding")
    _exact_keys(
        binding,
        {"model", "source_sha256", "polygon_sha256", "transform", "container"},
        "proof binding",
    )
    witness = _mapping(proof.get("witness"), "proof witness")
    _exact_keys(
        witness,
        {
            "format",
            "binding",
            "pose",
            "rotation",
            "correspondence",
            "corners",
            "source_cells",
            "source_cells_sha256",
        },
        "proof witness",
    )
    _exact_keys(_mapping(witness.get("pose"), "witness pose"), {"cx", "cy", "t"}, "pose")
    _exact_keys(_mapping(witness.get("rotation"), "witness rotation"), {"c", "s"}, "rotation")
    _verify_cover_shape(proof.get("cover"))
    wall = _mapping(proof.get("wall_signs"), "wall signs")
    _exact_keys(wall, {"walls", "minimum", "decision"}, "wall signs")
    controls = proof.get("pair_controls")
    if not isinstance(controls, list) or len(controls) != 3:
        raise ResultVerificationError("pair controls have invalid shape")
    for control in controls:
        item = _mapping(control, "pair control")
        _exact_keys(item, {"label", "signs"}, "pair control")
        signs = _mapping(item.get("signs"), "pair signs")
        _exact_keys(
            signs,
            {"first", "second", "axis_gaps", "maximum", "decision"},
            "pair signs",
        )


def _verify_model(
    value: object,
    *,
    expected_model: str,
    source_sha256: str,
    polygon_sha256: str,
) -> None:
    model = _mapping(value, "model result")
    if model.get("model") != expected_model:
        raise ResultVerificationError("model order is not frozen")
    outcome = model.get("outcome")
    if outcome == "refused":
        if set(model) != {"model", "outcome", "reason"} or model.get("reason") not in _REFUSALS:
            raise ResultVerificationError("refused model has invalid fields or reason")
        return
    if (
        outcome != "compatible"
        or model.get("reason") != "localized-compatible"
        or set(model) != {"model", "outcome", "reason", "proof"}
    ):
        raise ResultVerificationError("compatible model has invalid fields or reason")
    envelope = _mapping(model.get("proof"), "proof envelope")
    _exact_keys(envelope, {"proof", "proof_sha256"}, "proof envelope")
    proof = _mapping(envelope.get("proof"), "proof")
    _verify_proof_shape(proof)
    binding = _mapping(proof.get("binding"), "proof binding")
    if (
        binding.get("model") != expected_model
        or binding.get("source_sha256") != source_sha256
        or binding.get("polygon_sha256") != polygon_sha256
    ):
        raise ResultVerificationError("proof binding does not match the selected source")
    witness = _mapping(proof.get("witness"), "proof witness")
    cells_sha256 = _digest(witness.get("source_cells_sha256"), "source-cell digest")
    wall_signs = _mapping(proof.get("wall_signs"), "wall signs")
    if wall_signs.get("decision") != "nonnegative":
        raise ResultVerificationError("compatible proof lacks nonnegative wall containment")
    errors = verify_proof(envelope, binding, cells_sha256)
    if errors:
        raise ResultVerificationError("independent proof verification failed: " + errors[0])


def verify_result_bytes(content: bytes, contract: RunnerContract) -> dict[str, object]:
    """Replay a complete canonical result against independently supplied contract facts."""

    if not content.endswith(b"\n") or content.endswith(b"\n\n"):
        raise ResultVerificationError("result must have one trailing newline")
    try:
        document = json.loads(content)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ResultVerificationError("result is not UTF-8 canonical JSON") from error
    if not isinstance(document, dict):
        raise ResultVerificationError("result root must be an object")
    _verify_sanitized(document)
    try:
        canonical = (
            json.dumps(
                document,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=True,
                allow_nan=False,
            ).encode()
            + b"\n"
        )
    except (TypeError, ValueError) as error:
        raise ResultVerificationError("result contains a noncanonical JSON value") from error
    if content != canonical:
        raise ResultVerificationError("result bytes are not canonical")
    expected_keys = {
        "format",
        "experiment_id",
        "session_id",
        "authorization",
        "source",
        "selection",
        "model_order",
        "models",
        "retention",
        "blindness",
    }
    if set(document) != expected_keys:
        raise ResultVerificationError("result fields are incomplete")
    if (
        document.get("format") != "UnitSquareRefusalRunner/v1"
        or document.get("experiment_id") != contract.experiment_id
        or document.get("session_id") != contract.session_id
        or document.get("authorization") != contract.authorization.to_document()
        or document.get("retention") != "sanitized-provenance-and-proof-only"
        or document.get("blindness") != "parent-only-input-interface"
    ):
        raise ResultVerificationError("result contract binding is invalid")
    source = _mapping(document.get("source"), "source")
    if set(source) != {"url", "expected_sha256", "observed_sha256"}:
        raise ResultVerificationError("source fields are incomplete")
    if (
        source.get("url") != contract.parent_url
        or source.get("expected_sha256") != contract.parent_sha256
        or source.get("observed_sha256") != contract.parent_sha256
    ):
        raise ResultVerificationError("source binding does not match the frozen contract")
    selection = _mapping(document.get("selection"), "selection")
    if set(selection) != {"stable_id", "polygon_sha256"}:
        raise ResultVerificationError("selection fields are incomplete")
    stable_id = selection.get("stable_id")
    if not isinstance(stable_id, str) or not stable_id:
        raise ResultVerificationError("selected id is invalid")
    try:
        stable_id.encode("utf-8")
    except UnicodeEncodeError as error:
        raise ResultVerificationError("selected id is not valid UTF-8") from error
    polygon_sha256 = _digest(selection.get("polygon_sha256"), "selected polygon digest")
    if document.get("model_order") != list(_MODELS):
        raise ResultVerificationError("model inventory is not frozen")
    models = document.get("models")
    if not isinstance(models, list) or len(models) != 3:
        raise ResultVerificationError("result must contain exactly three model outcomes")
    for value, expected_model in zip(models, _MODELS, strict=True):
        _verify_model(
            value,
            expected_model=expected_model,
            source_sha256=contract.parent_sha256,
            polygon_sha256=polygon_sha256,
        )
    return document


def result_sha256(content: bytes, contract: RunnerContract) -> str:
    """Return a digest only after whole-result replay succeeds."""

    verify_result_bytes(content, contract)
    return hashlib.sha256(content).hexdigest()
