"""Target-blind production entry point for the UnitSquare one-parent adapter."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import sys
import tempfile
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from fractions import Fraction
from pathlib import Path
from typing import BinaryIO

from cases.unitsquare_precision.production.adapter import (
    BoundedResponse,
    ProductionAdapterError,
    StructuralRefusalError,
    TransformRefusalError,
    bounded_parent_opener,
    parse_transform,
    production_model_factory,
    structural_scanner,
)
from cases.unitsquare_precision.production.verify import (
    ResultVerificationError,
    verify_result_bytes,
)
from cases.unitsquare_precision.refusal.run import (
    RunnerAuthorization,
    RunnerContract,
    RunnerGuardError,
    RunnerModelEvaluation,
    atomic_publish_new,
    canonical_runner_bytes,
    run_authorized_runner,
)

EXP054_RESULT_PATH = (
    "campaign/series/series-000-smoke-and-calibration/results/"
    "exp-054-h-058-n68-one-parent-production-serialization.json"
)
PARENT_URL = "https://kingbird.myphotos.cc/packing/square-68.svg"
PARENT_SHA256 = "558fbdddfeb0b2f8752b88e172d2776544beb4d2a7122189ef77c1e1c5ebdc6d"

_SYNTHETIC_URL = "https://example.invalid/synthetic-parent.svg"
_SYNTHETIC_SVG = b"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4 4">
<rect id="container" x="0" y="0" width="4" height="4"/>
<g transform="translate(1,1) scale(1)">
<polygon id="square-a"
 points="0.000000,0.000000 1.000000,0.000000 1.000000,1.000000 0.000000,1.000000"/>
</g></svg>"""


class ProductionGuardError(ValueError):
    """A bounded production-adapter admission failure."""


@dataclass(frozen=True, slots=True)
class ProductionDependencies:
    """Injected channels behind the literal CLI boundary."""

    contract: RunnerContract
    authorization: RunnerAuthorization
    opener: Callable[[str], BinaryIO]
    structural_scan: Callable[[memoryview], Sequence[Mapping[str, object]]]
    model_factory: Callable[[str], Callable[[memoryview, str], RunnerModelEvaluation]]
    output_root: Path
    publisher: Callable[[Path, bytes], None] = atomic_publish_new


def production_dependencies(
    *,
    contract: RunnerContract,
    authorization: RunnerAuthorization,
    output_root: Path,
) -> ProductionDependencies:
    """Bind a future authorized W6 contract to the complete parent-only adapter."""

    if contract.parent_url != PARENT_URL or contract.parent_sha256 != PARENT_SHA256:
        raise ProductionGuardError("production contract does not bind the frozen n=68 parent")
    return ProductionDependencies(
        contract,
        authorization,
        bounded_parent_opener(PARENT_URL),
        structural_scanner(expected_polygon_count=68),
        production_model_factory(expected_polygon_count=68, side=None),
        output_root,
    )


def verified_publisher(
    contract: RunnerContract,
    publisher: Callable[[Path, bytes], None] = atomic_publish_new,
) -> Callable[[Path, bytes], None]:
    """Independently replay complete bytes before invoking the atomic publisher."""

    def publish(path: Path, content: bytes) -> None:
        verify_result_bytes(content, contract)
        publisher(path, content)

    return publish


def literal_test_dependencies(root: Path) -> ProductionDependencies:
    source_sha256 = hashlib.sha256(_SYNTHETIC_SVG).hexdigest()
    authorization = RunnerAuthorization(
        "session-074", "2026-09-02T00:30:00Z", "2026-09-02T00:50:00Z"
    )
    contract = RunnerContract(
        "exp-054",
        "session-074",
        EXP054_RESULT_PATH,
        authorization,
        _SYNTHETIC_URL,
        source_sha256,
    )
    return ProductionDependencies(
        contract,
        authorization,
        lambda _url: io.BytesIO(_SYNTHETIC_SVG),
        structural_scanner(expected_polygon_count=1),
        production_model_factory(expected_polygon_count=1, side=Fraction(4)),
        root,
    )


def _expect_error(
    label: str,
    expected: type[BaseException] | tuple[type[BaseException], ...],
    action: Callable[[], object],
    mutations: list[str],
) -> None:
    try:
        action()
    except expected:
        mutations.append(label)
        return
    raise ProductionGuardError(f"mutation did not fire its named guard: {label}")


def _reseal_first_proof(document: dict[str, object]) -> None:
    models = document.get("models")
    if not isinstance(models, list) or not models or not isinstance(models[0], dict):
        raise ProductionGuardError("synthetic mutation fixture lacks its first model")
    envelope = models[0].get("proof")
    if not isinstance(envelope, dict) or not isinstance(envelope.get("proof"), dict):
        raise ProductionGuardError("synthetic mutation fixture lacks its proof")
    proof = envelope["proof"]
    envelope["proof_sha256"] = hashlib.sha256(
        json.dumps(proof, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _mutation_selftest(
    root: Path,
    dependencies: ProductionDependencies,
    retained: bytes,
) -> list[str]:
    mutations: list[str] = []
    opened: list[str] = []
    guarded = replace(
        dependencies,
        opener=lambda url: opened.append(url) or io.BytesIO(_SYNTHETIC_SVG),
    )
    _expect_error(
        "wrong-result-path-before-open",
        RunnerGuardError,
        lambda: run_literal(["--record", "wrong.json"], guarded),
        mutations,
    )
    if opened:
        raise ProductionGuardError("wrong result path reached the opener")
    wrong_authorization = replace(
        dependencies,
        authorization=RunnerAuthorization(
            "session-074",
            "2026-09-02T00:30:01Z",
            "2026-09-02T00:50:00Z",
        ),
    )
    _expect_error(
        "mismatched-runtime-authorization",
        RunnerGuardError,
        lambda: run_literal(["--record", EXP054_RESULT_PATH], wrong_authorization),
        mutations,
    )
    if opened:
        raise ProductionGuardError("mismatched authorization reached the opener")
    _expect_error(
        "existing-result-before-open",
        RunnerGuardError,
        lambda: run_literal(["--record", EXP054_RESULT_PATH], guarded),
        mutations,
    )
    if opened:
        raise ProductionGuardError("existing result reached the opener")

    digest_root = root / "digest-mutation"
    digest_target = digest_root / EXP054_RESULT_PATH
    digest_target.parent.mkdir(parents=True)
    scanned: list[bool] = []
    response = io.BytesIO(_SYNTHETIC_SVG + b"changed")
    digest_dependencies = replace(
        dependencies,
        opener=lambda _url: response,
        structural_scan=lambda _view: scanned.append(True) or (),
        output_root=digest_root,
    )
    _expect_error(
        "source-byte-before-parse",
        RunnerGuardError,
        lambda: run_literal(["--record", EXP054_RESULT_PATH], digest_dependencies),
        mutations,
    )
    if scanned or not response.closed or digest_target.exists():
        raise ProductionGuardError("digest mutation crossed parse, cleanup or publication")

    class UnclosableResponse(io.BytesIO):
        @property
        def closed(self) -> bool:
            return False

        def close(self) -> None:
            return None

    cleanup_root = root / "cleanup-mutation"
    cleanup_target = cleanup_root / EXP054_RESULT_PATH
    cleanup_target.parent.mkdir(parents=True)
    cleanup_dependencies = replace(
        dependencies,
        opener=lambda _url: UnclosableResponse(_SYNTHETIC_SVG),
        output_root=cleanup_root,
    )
    _expect_error(
        "failed-response-cleanup",
        RunnerGuardError,
        lambda: run_literal(["--record", EXP054_RESULT_PATH], cleanup_dependencies),
        mutations,
    )
    if cleanup_target.exists():
        raise ProductionGuardError("cleanup failure reached publication")

    duplicate = _SYNTHETIC_SVG.replace(
        b"</svg>",
        b'<polygon id="square-a" points="0,0 1,0 1,1 0,1"/></svg>',
    )
    _expect_error(
        "duplicate-stable-id",
        StructuralRefusalError,
        lambda: structural_scanner(expected_polygon_count=2)(memoryview(duplicate)),
        mutations,
    )
    _expect_error(
        "wrong-polygon-count",
        StructuralRefusalError,
        lambda: structural_scanner(expected_polygon_count=2)(memoryview(_SYNTHETIC_SVG)),
        mutations,
    )
    _expect_error(
        "singular-transform",
        TransformRefusalError,
        lambda: parse_transform("matrix(1 0 0 0 0 0)"),
        mutations,
    )
    _expect_error(
        "uncertified-decimal-rotation",
        TransformRefusalError,
        lambda: parse_transform("rotate(13.5)"),
        mutations,
    )
    forward = parse_transform("translate(1,2) scale(2,3)")
    reverse = parse_transform("scale(2,3) translate(1,2)")
    if forward == reverse or forward.apply("1", "1") != ("3", "5"):
        raise ProductionGuardError("noncommuting transform-order control failed")
    mutations.append("reversed-noncommuting-transform")

    expected_url = "https://example.invalid/bounded-parent.svg"

    class RedirectResponse(io.BytesIO):
        def geturl(self) -> str:
            return "https://example.invalid/redirected.svg"

    class RedirectTransport:
        def __init__(self) -> None:
            self.response = RedirectResponse(b"bounded")
            self.calls: list[tuple[str, int]] = []

        def open(self, url: str, *, timeout: int) -> BinaryIO:
            self.calls.append((url, timeout))
            return self.response

    redirect_transport = RedirectTransport()
    bounded_opener = bounded_parent_opener(
        expected_url,
        timeout_seconds=7,
        transport=redirect_transport,
    )
    _expect_error(
        "wrong-parent-url",
        ProductionAdapterError,
        lambda: bounded_opener("https://example.invalid/wrong.svg"),
        mutations,
    )
    if redirect_transport.calls:
        raise ProductionGuardError("wrong parent URL reached the transport")
    _expect_error(
        "redirected-parent",
        ProductionAdapterError,
        lambda: bounded_opener(expected_url),
        mutations,
    )
    if (
        redirect_transport.calls != [(expected_url, 7)]
        or not redirect_transport.response.closed
    ):
        raise ProductionGuardError("redirect timeout or cleanup control failed")

    oversized = BoundedResponse(io.BytesIO(b"12345"), byte_cap=4)
    _expect_error(
        "oversized-parent-stream",
        ProductionAdapterError,
        oversized.read,
        mutations,
    )
    oversized.close()
    if not oversized.closed:
        raise ProductionGuardError("oversized response cleanup failed")

    reordered = json.loads(retained)
    reordered["model_order"] = list(reversed(reordered["model_order"]))
    _expect_error(
        "model-order-mutation",
        ResultVerificationError,
        lambda: verify_result_bytes(
            canonical_runner_bytes(reordered) + b"\n", dependencies.contract
        ),
        mutations,
    )
    forged = json.loads(retained)
    forged["models"][0]["proof"]["proof"]["witness"]["rotation"]["c"] = "0"
    _reseal_first_proof(forged)
    _expect_error(
        "forged-half-angle-identity",
        ResultVerificationError,
        lambda: verify_result_bytes(
            canonical_runner_bytes(forged) + b"\n", dependencies.contract
        ),
        mutations,
    )
    missing_cover = json.loads(retained)
    del missing_cover["models"][0]["proof"]["proof"]["cover"]["corner_images"]
    _reseal_first_proof(missing_cover)
    _expect_error(
        "missing-cover-evidence",
        ResultVerificationError,
        lambda: verify_result_bytes(
            canonical_runner_bytes(missing_cover) + b"\n", dependencies.contract
        ),
        mutations,
    )
    wall = json.loads(retained)
    wall["models"][0]["proof"]["proof"]["wall_signs"]["decision"] = "negative"
    _reseal_first_proof(wall)
    _expect_error(
        "wall-sign-across-zero",
        ResultVerificationError,
        lambda: verify_result_bytes(
            canonical_runner_bytes(wall) + b"\n", dependencies.contract
        ),
        mutations,
    )
    pair = json.loads(retained)
    pair["models"][0]["proof"]["proof"]["pair_controls"][0]["signs"]["decision"] = "overlap"
    _reseal_first_proof(pair)
    _expect_error(
        "separated-pair-to-overlap",
        ResultVerificationError,
        lambda: verify_result_bytes(
            canonical_runner_bytes(pair) + b"\n", dependencies.contract
        ),
        mutations,
    )
    leaked = json.loads(retained)
    leaked["models"][0]["proof"]["proof"]["child"] = "forbidden"
    _reseal_first_proof(leaked)
    _expect_error(
        "forbidden-child-channel",
        ResultVerificationError,
        lambda: verify_result_bytes(
            canonical_runner_bytes(leaked) + b"\n", dependencies.contract
        ),
        mutations,
    )
    published: list[bytes] = []
    verifier_first = verified_publisher(
        dependencies.contract,
        lambda _path, content: published.append(content),
    )
    _expect_error(
        "whole-verifier-before-publisher",
        ResultVerificationError,
        lambda: verifier_first(root / "invalid.json", b"{}\n"),
        mutations,
    )
    if published:
        raise ProductionGuardError("invalid whole result reached the publisher")
    return mutations


def run_literal(argv: list[str], dependencies: ProductionDependencies) -> dict[str, object]:
    """Parse the exact production argv and run only through supplied dependencies."""

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--record", required=True)
    arguments = parser.parse_args(argv)
    return run_authorized_runner(
        contract=dependencies.contract,
        authorization=dependencies.authorization,
        record_path=arguments.record,
        output_root=dependencies.output_root,
        opener=dependencies.opener,
        structural_scan=dependencies.structural_scan,
        model_factory=dependencies.model_factory,
        publisher=verified_publisher(dependencies.contract, dependencies.publisher),
    )


def literal_selftest(record_path: str) -> dict[str, object]:
    """Exercise the exact production argv with in-memory SVG and temporary output."""

    if record_path != EXP054_RESULT_PATH:
        raise ProductionGuardError(f"result path must be exactly {EXP054_RESULT_PATH}")
    with tempfile.TemporaryDirectory(prefix="unitsquare-production-") as directory:
        root = Path(directory)
        target = root / record_path
        target.parent.mkdir(parents=True)
        dependencies = literal_test_dependencies(root)
        document = run_literal(["--record", record_path], dependencies)
        retained = target.read_bytes()
        expected = canonical_runner_bytes(document) + b"\n"
        if retained != expected:
            raise ProductionGuardError("literal command publication mismatch")
        verified = verify_result_bytes(retained, dependencies.contract)
        if verified != document:
            raise ProductionGuardError("whole-result verifier changed the result")
        if any(token in retained.lower() for token in (b"<svg", b"child", b"gain")):
            raise ProductionGuardError("literal command retained a forbidden channel")
        models = document.get("models")
        if not isinstance(models, list) or len(models) != 3:
            raise ProductionGuardError("literal command did not execute all three models")
        outcomes = [model.get("outcome") for model in models if isinstance(model, dict)]
        if len(outcomes) != 3 or "compatible" not in outcomes:
            raise ProductionGuardError("synthetic scene lacked a verified compatible model")
        mutations = _mutation_selftest(root, dependencies, retained)
        return {
            "format": "UnitSquareProductionLiteralSelftest/v2",
            "argv": ["--record", record_path],
            "result_sha256": hashlib.sha256(retained).hexdigest(),
            "models": document["model_order"],
            "outcomes": outcomes,
            "selection": document["selection"],
            "publication": "whole-result-verified-before-atomic-create",
            "mutations": mutations,
        }


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", required=True)
    arguments = parser.parse_args(argv)
    try:
        receipt = literal_selftest(arguments.record)
    except (
        ProductionAdapterError,
        ProductionGuardError,
        ResultVerificationError,
        RunnerGuardError,
    ) as error:
        print(f"production literal selftest failed: {error}", file=sys.stderr)
        return 2
    sys.stdout.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
