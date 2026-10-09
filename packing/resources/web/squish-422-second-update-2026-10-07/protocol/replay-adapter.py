"""Acquire SQUISH #401 rational facts, certify them, and replay both exact checkers.

No producer executable is retained or run. Source JSON is bounded and untrusted;
only normalized geometric facts survive acquisition. Neither decimal display strings
nor upstream success logs decide feasibility. Run from packing/ with ``acquire
--release PATH --supplement PATH``, ``certify``, or ``check [--replay]``.
"""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import re
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import check_rational_witness_independent as independent
from devtools.import_half_angle_witness import (
    half_angle_corners,
    rational_literal,
    unique_json_object,
)
from sqpack.witness import exact_verify, load_witness, witness_document

REPO = Path(__file__).resolve().parents[2]
PACKET = REPO / "packing/resources/web/squish-401-2026-10-07"
WITNESSES = REPO / "packing/witnesses/squish-401-2026"
SCHEMA = REPO / "base/witness.schema.yaml"
NUMBERS = (108, 126, 129, 130, 153, 154, 155, 180, 209, 238, 303)
MAX_SOURCE_BYTES = 1_000_000
# The eleven exact input rosters occupy 1.58 MB as JSON; controls are separate.
# Source admission keeps its smaller ceiling, while receipts and corner YAML stay bounded.
MAX_RECEIPT_BYTES = 4_000_000
MAX_CHECKER_LITERAL_CHARS = 1024
CERTIFICATION_FORMAT = "squish-exact-certification-v2"
MAX_N = 324
REVISION = "07fe6dde1e5b67405a3076719b90e58e2882b677"
RETRIEVED = "2026-10-07"
AUTHOR = "Nate Chaoweeraprasit"
DECIMAL = re.compile(r"[0-9]+\.[0-9]{1,80}\Z")


def source_key(n: int) -> str:
    """Return the governed source key for the original release or supplement."""
    if n not in NUMBERS:
        raise PacketError("count absent from SQUISH submission")
    return "[SQUISH n153 2026-10-07]" if n == 153 else "[SQUISH ten packings 2026-10-07]"


def source_url(n: int) -> str:
    """Pin the geometric source at its actual upstream trust boundary."""
    source_key(n)
    if n == 153:
        return "https://github.com/user-attachments/files/33140088/n153.cert.json"
    return (
        f"https://github.com/itsnaka/squish-certs/blob/{REVISION}/"
        f"squish-submission-2026-10-06/n{n}/n{n}.cert.json"
    )


class PacketError(ValueError):
    """Untrusted input or retained evidence failed the packet contract."""


def parse_source(path: Path, expected_n: int) -> tuple[dict[str, Any], bytes]:
    """Read a bounded complete roster; never accept numeric JSON coordinates."""
    if type(expected_n) is not int or not 1 <= expected_n <= MAX_N:
        raise PacketError('expected n exceeds the bounded admission range')
    with path.open('rb') as stream:
        raw = stream.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES:
        raise PacketError('source exceeds byte ceiling')
    try:
        source = json.loads(raw, object_pairs_hook=unique_json_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PacketError('invalid source JSON') from error
    required = {'n', 's_exact', 's_decimal', 'note', 'squares'}
    if type(source) is not dict or not required <= set(source) <= required | {'phase', 'squeezed'}:
        raise PacketError('source has missing required or unknown fields')
    if 'phase' in source and (type(source['phase']) is not int or not 1 <= source['phase'] <= 100):
        raise PacketError('unsupported source phase metadata')
    if 'squeezed' in source and type(source['squeezed']) is not bool:
        raise PacketError('unsupported source squeezed metadata')
    if type(source['n']) is not int or source['n'] != expected_n:
        raise PacketError('source n differs from expected n')
    side = rational_literal(source['s_exact'], 'source side')
    printed = source['s_decimal']
    if side <= 0 or type(printed) is not str or DECIMAL.fullmatch(printed) is None:
        raise PacketError('positive exact side and bounded decimal display required')
    if type(source['note']) is not str or len(source['note']) > 1024:
        raise PacketError('source note must be bounded text')
    entries = source['squares']
    if type(entries) is not list or len(entries) != expected_n:
        raise PacketError('incomplete square roster')
    squares = []
    for index, entry in enumerate(entries, 1):
        if type(entry) is not list or len(entry) != 3:
            raise PacketError(f'square {index} must have three exact strings')
        squares.append({key: str(rational_literal(value, f'square {index} {key}')) for key, value in zip(('x', 'y', 't'), entry, strict=True)})
    return ({'n': expected_n, 'side': str(side), 'printed_side': printed, 'squares': squares}, raw)


def fact_path(n: int) -> Path:
    return PACKET / "facts" / f"n-{n:03d}.json.gz"


def certificate_path(n: int) -> Path:
    return WITNESSES / f"n-{n:03d}-rational.yaml.gz"


def _json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def read_json(path: Path) -> Any:
    ceiling = MAX_RECEIPT_BYTES if path.name == "certification.json" else MAX_SOURCE_BYTES
    with path.open("rb") as stream:
        data = stream.read(ceiling + 1)
    if len(data) > ceiling:
        raise PacketError("retained JSON exceeds byte ceiling")
    return json.loads(data, object_pairs_hook=unique_json_object)


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(data)


def acquire(release: Path, supplement: Path, *, release_url: str, supplement_url: str) -> None:
    """Acquire the complete declared release plus n153 without copying raw bytes."""
    parsed = []
    for n in NUMBERS:
        source = supplement if n == 153 else release / f"n{n}/n{n}.cert.json"
        fact, raw = parse_source(source, n)
        parsed.append((n, fact, raw, source))
    cases = []
    for n, fact, raw, source in parsed:
        derived = _json(fact)
        _write(fact_path(n), gzip.compress(derived, mtime=0))
        cases.append(
            {
                "n": n,
                "side": fact["printed_side"],
                "exact_side": fact["side"],
                "source_url": supplement_url
                if n == 153
                else release_url
                + f"/blob/{REVISION}/squish-submission-2026-10-06/n{n}/n{n}.cert.json",
                "source_file": source.name,
                "source_sha256": hashlib.sha256(raw).hexdigest(),
                "source_bytes": len(raw),
                "facts": fact_path(n).relative_to(REPO).as_posix(),
                "raw_asset_retained": False,
            }
        )
    _write(
        PACKET / "acquisition/sources.json",
        _json(
            {
                "format": "external-source-acquisition-v1",
                "retrieved": "2026-10-07",
                "source_commit": REVISION,
                "raw_asset_retained": False,
                "producer_checker_replayed": False,
                "cases": cases,
            }
        ),
    )
    for label, counts in (("release", set(NUMBERS) - {153}), ("supplement", {153})):
        _write(
            PACKET / f"acquisition/{label}-claims.json",
            _json(
                {
                    "results": [
                        {"n": row["n"], "offered_side": row["side"]}
                        for row in cases
                        if row["n"] in counts
                    ]
                }
            ),
        )


def read_fact(n: int) -> dict[str, Any]:
    """Revalidate retained normalized facts through the same strict source boundary."""
    if fact_path(n).stat().st_size > MAX_SOURCE_BYTES:
        raise PacketError("compressed facts exceed byte ceiling")
    with gzip.open(fact_path(n), "rb") as stream:
        data = stream.read(MAX_SOURCE_BYTES + 1)
    if len(data) > MAX_SOURCE_BYTES:
        raise PacketError("derived facts exceed byte ceiling")
    fact = json.loads(data, object_pairs_hook=unique_json_object)
    if type(fact) is not dict or set(fact) != {"n", "side", "printed_side", "squares"}:
        raise PacketError("invalid derived fact schema")
    entries = fact["squares"]
    if type(entries) is not list or any(
        type(entry) is not dict or set(entry) != {"x", "y", "t"} for entry in entries
    ):
        raise PacketError("invalid derived square schema")
    source = {
        "n": fact["n"],
        "s_exact": fact["side"],
        "s_decimal": fact["printed_side"],
        "note": "derived facts",
        "squares": [[entry[key] for key in ("x", "y", "t")] for entry in entries],
    }
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "facts.json"
        path.write_bytes(_json(source))
        normalized, _raw = parse_source(path, n)
    return normalized


def to_witness(fact: dict[str, Any]) -> dict[str, Any]:
    """Use rational half-angle identities; no rounding, dilation, or trigonometry."""
    n = fact["n"]
    return {
        "id": f"W-squish-401-n{n:03d}",
        "n": n,
        "side": fact["side"],
        "square_size": "1",
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": {
            "origin": "lower-left",
            "axes": "x-right-y-up",
            "angle_unit": "not-applicable",
        },
        "squares": [
            {
                "id": index,
                "corners": [
                    [str(x), str(y)]
                    for x, y in half_angle_corners(
                        *(Fraction(entry[key]) for key in ("x", "y", "t"))
                    )
                ],
            }
            for index, entry in enumerate(fact["squares"], 1)
        ],
        "claim": {
            "coordinate_provenance": "verified",
            "method": "exact-algebraic",
            "limitations": "Exact feasible upper bound only; no optimality claim.",
        },
        "source": {"path": fact_path(n).relative_to(REPO).as_posix()},
        "certificate": {
            "kind": "exact-rational-sat",
            "replay": "uv run --frozen python -m devtools.squish_upper_bound_packets "
            f"check --replay --n {n}",
        },
    }


def decide(witness: dict[str, Any]) -> dict[str, Any]:
    """Independently decide the serialized artifact with both complete exact routes."""
    witness = {**witness, **checker_input(witness)}
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "certificate.yaml"
        path.write_text(witness_document(witness, schema=SCHEMA.as_posix()))
        corner = independent.check(path)
        exact, _report = exact_verify(load_witness(path, fallback_schema=SCHEMA))
    result = {
        "independent": {
            key: corner[key]
            for key in (
                "verification_passed",
                "n",
                "pairs_tested",
                "minimum_containment_clearance",
                "failures",
            )
        },
        "exact_verify": {
            key: exact[key]
            for key in (
                "verification_passed",
                "n",
                "pairs_tested",
                "minimum_containment_clearance",
                "failures",
            )
        },
    }
    # The first-party report represents failures as tuples. Normalize them at the
    # receipt boundary so in-memory replay compares with JSON-loaded receipts.
    return json.loads(_json(result))


def _checker_fraction(value: Any) -> str:
    if (
        type(value) is not str
        or len(value) > MAX_CHECKER_LITERAL_CHARS
        or re.fullmatch(r"-?[0-9]+(?:/[0-9]+)?", value) is None
    ):
        raise PacketError("checker input needs bounded exact rational strings")
    try:
        return str(Fraction(value))
    except ZeroDivisionError as error:
        raise PacketError("checker input rational denominator must be nonzero") from error


def checker_input(witness: dict[str, Any], *, receipt: bool = False) -> dict[str, Any]:
    """The complete exact decision input, independent of witness prose and provenance.

    Compare these bounded values directly. Repository-owned facts and certificates are
    ordinary Git data; a file checksum must not decide whether an old verdict applies.
    The native verifier's method dispatch is enforced before extracting its geometry.
    """
    if type(witness) is not dict or (
        not receipt and witness.get("claim", {}).get("method") != "exact-algebraic"
    ):
        raise PacketError("checker input requires exact-algebraic dispatch")
    coordinates = {
        "origin": "lower-left",
        "axes": "x-right-y-up",
        "angle_unit": "not-applicable",
    }
    n = witness.get("n")
    if (
        type(n) is not int
        or not 1 <= n <= MAX_N
        or witness.get("representation") != "corners"
        or witness.get("scalar") != {"kind": "rational"}
        or witness.get("coordinates") != coordinates
    ):
        raise PacketError("checker input requires a bounded rational corner frame")
    side = _checker_fraction(witness.get("side"))
    unit = _checker_fraction(witness.get("square_size"))
    if Fraction(side) <= 0 or unit != "1":
        raise PacketError("checker input requires a positive side and unit squares")
    roster = witness.get("squares")
    if type(roster) is not list or len(roster) != n:
        raise PacketError("checker input requires the complete square roster")
    squares = []
    ids = set()
    for square in roster:
        if type(square) is not dict:
            raise PacketError("checker input square must be an object")
        identifier = square.get("id")
        if (
            type(identifier) not in (int, str)
            or (type(identifier) is int and not 1 <= identifier <= MAX_N)
            or (type(identifier) is str and not 1 <= len(identifier) <= 256)
            or identifier in ids
        ):
            raise PacketError("checker input square IDs must be bounded and unique")
        ids.add(identifier)
        corners = square.get("corners")
        if type(corners) is not list or len(corners) != 4:
            raise PacketError("checker input square must have four ordered corners")
        points = []
        for point in corners:
            if type(point) is not list or len(point) != 2:
                raise PacketError("checker input corner must have two coordinates")
            points.append([_checker_fraction(value) for value in point])
        squares.append({"id": identifier, "corners": points})
    return {
        "n": n,
        "side": side,
        "square_size": unit,
        "representation": "corners",
        "scalar": {"kind": "rational"},
        "coordinates": coordinates,
        "squares": squares,
    }


def verified_value(side: Fraction, printed: str) -> str:
    """A decimal ceiling derived with integer arithmetic, never nearest rounding."""
    digits = len(printed.split(".")[1])
    scale = 10**digits
    upper = -(-(side.numerator * scale) // side.denominator)
    integer, decimal = divmod(upper, scale)
    return f"{integer}.{decimal:0{digits}d}"


def certify_one(n: int) -> dict[str, Any]:
    fact = read_fact(n)
    witness = to_witness(fact)
    verdict = decide(witness)
    expected_pairs = n * (n - 1) // 2
    if any(
        not row["verification_passed"] or row["pairs_tested"] != expected_pairs
        for row in verdict.values()
    ):
        raise PacketError(f"n={n} failed complete dual exact verification: {verdict}")
    text = witness_document(witness, schema="../witness.schema.yaml").encode()
    _write(certificate_path(n), gzip.compress(text, mtime=0))
    value = verified_value(Fraction(fact["side"]), fact["printed_side"])
    return {
        "n": n,
        "printed_side": fact["printed_side"],
        "certified_side": fact["side"],
        "verified_value": value,
        "exact_form": fact["side"],
        "side_inflation": "0",
        "certificate": certificate_path(n).relative_to(REPO).as_posix(),
        "checker_input": checker_input(witness),
        **verdict,
    }


def control_witnesses() -> list[tuple[str, dict[str, Any]]]:
    witness = to_witness(read_fact(NUMBERS[0]))
    overlap = copy.deepcopy(witness)
    overlap["squares"][1]["corners"] = copy.deepcopy(overlap["squares"][0]["corners"])
    outside = copy.deepcopy(witness)
    for point in outside["squares"][0]["corners"]:
        point[0] = str(Fraction(point[0]) - 2 * Fraction(outside["side"]))
    return [
        ("duplicate-square-overlap", overlap),
        ("square-translated-outside-container", outside),
    ]


def negative_controls() -> dict[str, Any]:
    rows = [
        {"control": name, "checker_input": checker_input(control), **decide(control)}
        for name, control in control_witnesses()
    ]
    if any(
        row[checker]["verification_passed"]
        for row in rows
        for checker in ("independent", "exact_verify")
    ):
        raise PacketError("a deciding checker accepted a negative control")
    return {
        "n": NUMBERS[0],
        "expectation": "both deciding checkers refuse both controls",
        "controls": rows,
    }


def certify(numbers: list[int], workers: int) -> None:
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(certify_one, sorted(numbers, reverse=True)))
    path = PACKET / "receipts/certification.json"
    previous_receipt = read_json(path) if path.exists() else {}
    if previous_receipt and previous_receipt.get("format") != CERTIFICATION_FORMAT:
        if set(numbers) != set(NUMBERS):
            raise PacketError("old receipts require complete semantic recertification")
        previous_receipt = {}
    previous = previous_receipt.get("cases", [])
    merged = {row["n"]: row for row in previous + rows}
    _write(
        path,
        _json(
            {
                "format": CERTIFICATION_FORMAT,
                "producer_checker_replayed": False,
                "checkers": [
                    "devtools.check_rational_witness_independent",
                    "sqpack.witness.exact_verify",
                ],
                "cases": [merged[n] for n in sorted(merged)],
            }
        ),
    )
    if NUMBERS[0] in merged:
        _write(PACKET / "receipts/negative-controls.json", _json(negative_controls()))
    if set(merged) == set(NUMBERS):
        for label, value in normalized_claims([merged[n] for n in sorted(merged)]).items():
            _write(PACKET / f"acquisition/{label}-normalized-claims.json", _json(value))


def normalized_claims(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Source-coverage offers at safe display ceilings, preserving source exact sides."""
    return {
        label: {
            "basis": (
                "Safe decimal displays of the source exact rational bounds, rounded "
                "upward at the source display precision by the complete replay receipt. "
                "Original source finite displays remain in the acquisition and original "
                "claims records."
            ),
            "certificate_receipt": (PACKET / "receipts/certification.json")
            .relative_to(REPO)
            .as_posix(),
            "original_claims_record": (PACKET / f"acquisition/{label}-claims.json")
            .relative_to(REPO)
            .as_posix(),
            "results": [
                {
                    "n": row["n"],
                    "offered_side": row["verified_value"],
                    "exact_side": row["certified_side"],
                    "source_display": row["printed_side"],
                }
                for row in rows
                if (row["n"] == 153) == (label == "supplement")
            ],
        }
        for label in ("release", "supplement")
    }


def check(numbers: list[int], *, replay: bool) -> None:
    receipt = read_json(PACKET / "receipts/certification.json")
    if receipt.get("format") != CERTIFICATION_FORMAT:
        raise PacketError("old receipt format requires semantic recertification")
    if receipt["producer_checker_replayed"] is not False or receipt["checkers"] != [
        "devtools.check_rational_witness_independent",
        "sqpack.witness.exact_verify",
    ]:
        raise PacketError("certification checker provenance mismatch")
    rows = {row["n"]: row for row in receipt["cases"]}
    if len(receipt["cases"]) != len(NUMBERS) or set(rows) != set(NUMBERS):
        raise PacketError("certification roster is incomplete or has duplicate/extra counts")
    acquisition = read_json(PACKET / "acquisition/sources.json")
    if (
        acquisition["format"] != "external-source-acquisition-v1"
        or acquisition["source_commit"] != REVISION
        or acquisition["retrieved"] != RETRIEVED
        or acquisition["raw_asset_retained"] is not False
        or acquisition["producer_checker_replayed"] is not False
    ):
        raise PacketError("acquisition source provenance mismatch")
    acquired = {row["n"]: row for row in acquisition["cases"]}
    if len(acquisition["cases"]) != len(NUMBERS) or set(acquired) != set(NUMBERS):
        raise PacketError("acquisition roster mismatch")
    for n, entry in acquired.items():
        if (
            entry["source_url"] != source_url(n)
            or entry["facts"] != fact_path(n).relative_to(REPO).as_posix()
            or entry["source_file"] != f"n{n}.cert.json"
            or entry["raw_asset_retained"] is not False
            or type(entry["source_bytes"]) is not int
            or not 1 <= entry["source_bytes"] <= MAX_SOURCE_BYTES
            or type(entry["source_sha256"]) is not str
            or re.fullmatch(r"[0-9a-f]{64}", entry["source_sha256"]) is None
        ):
            raise PacketError(f"n={n} acquisition source metadata mismatch")
    for n in numbers:
        fact = read_fact(n)
        witness = to_witness(fact)
        expected = checker_input(witness)
        if certificate_path(n).stat().st_size > MAX_RECEIPT_BYTES:
            raise PacketError("compressed certificate exceeds byte ceiling")
        with gzip.open(certificate_path(n), "rb") as stream:
            actual = stream.read(MAX_RECEIPT_BYTES + 1)
        if len(actual) > MAX_RECEIPT_BYTES:
            raise PacketError("certificate exceeds byte ceiling")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.yaml"
            path.write_bytes(actual)
            certificate = load_witness(path, fallback_schema=SCHEMA)
        if (
            expected != checker_input(dict(certificate))
            or acquired[n]["exact_side"] != fact["side"]
            or acquired[n]["side"] != fact["printed_side"]
        ):
            raise PacketError(f"n={n} certificate/facts acquisition mismatch")
        row = rows[n]
        if expected != checker_input(row["checker_input"], receipt=True):
            raise PacketError(f"n={n} checker-input semantic mismatch")
        if (
            row["certificate"] != certificate_path(n).relative_to(REPO).as_posix()
            or row["printed_side"] != fact["printed_side"]
            or row["side_inflation"] != "0"
        ):
            raise PacketError(f"n={n} receipt source metadata mismatch")
        value = verified_value(Fraction(fact["side"]), fact["printed_side"])
        if (row["certified_side"], row["verified_value"], row["exact_form"]) != (
            fact["side"],
            value,
            fact["side"],
        ):
            raise PacketError(f"n={n} receipt bound mismatch")
        for name in ("independent", "exact_verify"):
            if (
                row[name]["verification_passed"] is not True
                or row[name]["n"] != n
                or row[name]["pairs_tested"] != n * (n - 1) // 2
                or row[name]["failures"] != []
                or Fraction(row[name]["minimum_containment_clearance"]) < 0
            ):
                raise PacketError(f"n={n} missing full checker coverage")
        if replay and decide(dict(certificate)) != {
            name: row[name] for name in ("independent", "exact_verify")
        }:
            raise PacketError(f"n={n} exact replay mismatch")
    controls = read_json(PACKET / "receipts/negative-controls.json")
    if (
        controls["n"] != NUMBERS[0]
        or {row["control"] for row in controls["controls"]}
        != {"duplicate-square-overlap", "square-translated-outside-container"}
        or len(controls["controls"]) != 2
    ) or any(
        row[name]["verification_passed"]
        for row in controls["controls"]
        for name in ("independent", "exact_verify")
    ):
        raise PacketError("invalid negative-control receipt")
    expected_controls = dict(control_witnesses())
    for row in controls["controls"]:
        if checker_input(row["checker_input"], receipt=True) != checker_input(
            expected_controls[row["control"]]
        ):
            raise PacketError("negative-control checker-input semantic mismatch")
        for name in ("independent", "exact_verify"):
            result = row[name]
            if (
                result["verification_passed"] is not False
                or result["n"] != NUMBERS[0]
                or result["pairs_tested"] != NUMBERS[0] * (NUMBERS[0] - 1) // 2
                or not result["failures"]
            ):
                raise PacketError("incomplete negative-control checker coverage")
        if row["control"] == "duplicate-square-overlap":
            if not any(
                "overlapping pairs" in failure for failure in row["independent"]["failures"]
            ):
                raise PacketError("overlap control lacks independent overlap refusal")
            if not any(failure[0] == "overlap" for failure in row["exact_verify"]["failures"]):
                raise PacketError("overlap control lacks exact overlap refusal")
        elif any(
            Fraction(row[name]["minimum_containment_clearance"]) >= 0
            for name in ("independent", "exact_verify")
        ):
            raise PacketError("container control lacks exact negative clearance")
    if replay and controls != negative_controls():
        raise PacketError("negative-control replay mismatch")
    for label, expected_claims in normalized_claims(receipt["cases"]).items():
        if read_json(PACKET / f"acquisition/{label}-normalized-claims.json") != expected_claims:
            raise PacketError(f"{label} normalized claims mismatch")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    sub = parser.add_subparsers(dest="command", required=True)
    acquisition = sub.add_parser("acquire", allow_abbrev=False)
    acquisition.add_argument("--release", type=Path, required=True)
    acquisition.add_argument("--supplement", type=Path, required=True)
    acquisition.add_argument("--release-url", required=True)
    acquisition.add_argument("--supplement-url", required=True)
    certification = sub.add_parser("certify", allow_abbrev=False)
    certification.add_argument("--workers", type=int, default=2, choices=range(1, 9))
    verification = sub.add_parser("check", allow_abbrev=False)
    verification.add_argument("--replay", action="store_true")
    for command in (certification, verification):
        command.add_argument("--n", type=int, nargs="+", choices=NUMBERS)
    args = parser.parse_args(argv)
    try:
        if args.command == "acquire":
            acquire(
                args.release,
                args.supplement,
                release_url=args.release_url,
                supplement_url=args.supplement_url,
            )
        elif args.command == "certify":
            certify(args.n or list(NUMBERS), args.workers)
        else:
            check(args.n or list(NUMBERS), replay=args.replay)
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f"REFUSED: {error}", file=sys.stderr)
        return 2
    print(f"SQUISH {args.command}: passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
