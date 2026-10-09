"""Bounded structural sizes of an accepted parent, without coupling predicates."""

from __future__ import annotations

import argparse
import copy
import math
import sys
import time
from pathlib import Path
from typing import Any, cast

from devtools import check_n17_partner_pose_coupling as parent
from devtools.provenance import provenance
from sqpack import retained_json

finite, cases = parent.finite, parent.cases
require, tick = parent.require, parent.tick
IncompleteError = parent.IncompleteError
SCHEMA = "n17-parent-geometry-structure/v1"
DESCRIPTOR_SCHEMA = "n17-parent-geometry-structure-context/v1"
OUTPUT_LIMIT = 64 << 20
SCAN_VERTEX_LIMIT = 1048576
COORDINATE_CHAR_LIMIT = 131072


def scalar_bits(token: Any, deadline: float | None = None) -> int:
    require(type(token) is str and token.isascii(), "ASCII exact coordinate required")
    if len(token) > COORDINATE_CHAR_LIMIT:
        raise IncompleteError("parent structural audit coordinate string ceiling")
    finite.rational_grammar(token)
    numerator, separator, denominator = token.partition("/")

    def integer(part: str) -> int:
        negative = part.startswith("-")
        digits = part[1:] if negative else part
        value = 0
        for start in range(0, len(digits), 1000):
            if deadline is not None:
                tick(deadline)
            chunk = digits[start : start + 1000]
            value = value * 10 ** len(chunk) + int(chunk)
        return -value if negative else value

    n, d = integer(numerator), integer(denominator) if separator else 1
    bits = max(abs(n).bit_length(), d.bit_length())
    require(
        token != "-0" and (not separator or d > 1) and math.gcd(n, d) == 1,
        "noncanonical coordinate rational",
    )
    return bits


def inspect(
    cells: dict[str, Any],
    roles: dict[str, int],
    *,
    deadline: float,
    reference_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    require(
        set(roles) == set(map(str, range(1, 18)))
        and roles["1"] == 0
        and roles["6"] == 12
        and len(set(roles.values())) == 17
        and all(type(owner) is int and 0 <= owner < 24 for owner in roles.values())
        and set(cells) == set(map(str, roles.values())),
        "complete label/owner roster differs",
    )
    owners = {}
    total_vertices, total_pieces, empty_pieces, max_bits = 0, 0, 0, 0
    largest_row = None
    largest_piece = None
    for owner in sorted(roles.values()):
        raw = cells[str(owner)]
        parent.closed_rows(raw, owner, 32 if owner == 12 else 64, reference_context)
        rows = []
        for index, row in enumerate(raw):
            tick(deadline)
            count = len(row["residual_polygons"])
            total_pieces += count
            summary = {
                "owner": owner,
                "row_index": index,
                "pieces": count,
                "reference": copy.deepcopy(row["reference"]),
            }
            if largest_row is None or count > largest_row["pieces"]:
                largest_row = summary.copy()
            vertices, row_bits, piece_sizes = 0, 0, []
            for piece_index, polygon in enumerate(row["residual_polygons"]):
                finite.opaque_polygon(polygon)
                size = len(polygon)
                empty_pieces += not size
                total_vertices += size
                if total_vertices > SCAN_VERTEX_LIMIT:
                    raise IncompleteError("parent structural audit total vertex ceiling")
                vertices += size
                bits = 0
                for point in polygon:
                    tick(deadline)
                    for token in point:
                        bits = max(bits, scalar_bits(token, deadline))
                piece_sizes.append(
                    {
                        "piece_index": piece_index,
                        "vertices": size,
                        "largest_coordinate_bits": bits,
                    }
                )
                row_bits = max(row_bits, bits)
                max_bits = max(max_bits, bits)
                if largest_piece is None or size > largest_piece["vertices"]:
                    largest_piece = {"owner": owner, "row_index": index, **piece_sizes[-1]}
            rows.append(
                {
                    **summary,
                    "vertices": vertices,
                    "largest_coordinate_bits": row_bits,
                    "piece_sizes": piece_sizes,
                }
            )
        owners[str(owner)] = {
            "rows": rows,
            "row_count": len(rows),
            "pieces": sum(r["pieces"] for r in rows),
            "vertices": sum(r["vertices"] for r in rows),
        }
    tick(deadline)
    return {
        "status": "complete",
        "all_rows_checked": sum(o["row_count"] for o in owners.values()),
        "foreign_rows_checked": sum(
            o["row_count"] for owner, o in owners.items() if owner != "0"
        ),
        "total_residual_pieces": total_pieces,
        "empty_residual_pieces": empty_pieces,
        "total_residual_vertices": total_vertices,
        "largest_coordinate_bits": max_bits,
        "largest_row_by_piece_count": largest_row,
        "largest_piece_by_vertex_count": largest_piece,
        "owners": owners,
        "numeric_scope": (
            "all original residual-polygon coordinates only; no wall clipping, "
            "ownership or collision predicates"
        ),
        "row_piece_limit_applied": False,
        "prospective_mathematical_comparisons": {
            "all_rows_within64_pieces": largest_row is None or largest_row["pieces"] <= 64,
            "all_rows_within4096_pieces": largest_row is None or largest_row["pieces"] <= 4096,
            "all_coordinates_within4096_bits": max_bits <= 4096,
            "raw_vertices_within262144": total_vertices <= 262144,
            "all_raw_pieces_within256_vertices": largest_piece is None
            or largest_piece["vertices"] <= 256,
        },
    }


def scope() -> dict[str, bool]:
    return {**parent.scope(), "coupling_predicates_evaluated": False, "criterion_met": False}


def generate(document: dict[str, Any], *, deadline: float) -> dict[str, Any]:
    require(document["schema"] == DESCRIPTOR_SCHEMA, "parent audit descriptor schema differs")
    frozen = finite.canonical(document)
    held: dict[Path, tuple[str, int]] = {}
    final, custody, _roster, _centre = parent.intake(
        copy.deepcopy(document) | {"schema": parent.DESCRIPTOR_SCHEMA}, held, deadline
    )
    gate = finite.read_json(
        finite.retained_path(document["parent_descriptor"]), parent.JSON_LIMIT
    )[1]
    result = inspect(
        final["cells"],
        gate["label_to_owner"],
        deadline=deadline,
        reference_context=custody["typed_reference_context"],
    )
    for path, (expected, ceiling) in held.items():
        require(
            finite.digest(path, ceiling, deadline) == expected, "parent audit inputs changed"
        )
    require(finite.canonical(document) == frozen, "parent audit descriptor changed")
    tick(deadline)
    return {
        "schema": SCHEMA,
        "accepted_inputs": copy.deepcopy(document),
        "parent_custody": {
            k: copy.deepcopy(custody[k])
            for k in (
                "h290_receipt",
                "h290_receipt_sha256",
                "seed_sha256",
                "node_sha256",
                "compressed_sha256",
                "steps",
                "typed_reference_context",
            )
        },
        "accepted_matched_pose_premise_freshly_checked": True,
        "constants": {
            "cumulative_scanned_raw_vertices": SCAN_VERTEX_LIMIT,
            "coordinate_ascii_characters": COORDINATE_CHAR_LIMIT,
            "json_bytes_each": parent.JSON_LIMIT,
            "output_bytes": OUTPUT_LIMIT,
            "seed_bytes": finite.SEED_LIMIT,
            "compressed_node_bytes": finite.NODE_LIMIT,
            "decoded_node_bytes": finite.DECODED_LIMIT,
            "final_slice_bytes": finite.SLICE_LIMIT,
        },
        **scope(),
        **result,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--max-seconds", type=float, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if not math.isfinite(args.max_seconds) or args.max_seconds <= 0:
        parser.error("max-seconds must be finite and positive")
    deadline = time.monotonic() + args.max_seconds
    try:
        require(
            not any(
                name == prefix or name.startswith(prefix + ".")
                for name in sys.modules
                for prefix in (*finite.FORBIDDEN, "devtools.produce_n17_conditional_owned_hull")
            ),
            "producer/kernel/root import in parent audit",
        )
        raw, document = finite.read_json(args.descriptor, parent.JSON_LIMIT)
        result = generate(document, deadline=deadline)
        require(
            finite.read_json(args.descriptor, parent.JSON_LIMIT)[0] == raw,
            "parent audit descriptor bytes changed",
        )
    except IncompleteError as exc:
        result = {"schema": SCHEMA, "status": "incomplete", "error": str(exc), **scope()}
    except (
        ValueError,
        KeyError,
        TypeError,
        OSError,
        EOFError,
        parent.standing.VerificationError,
    ) as exc:
        result = {"schema": SCHEMA, "status": "refused", "error": str(exc), **scope()}
    result.update(
        provenance=provenance(
            Path(__file__), Path(parent.__file__), Path(cast(str, finite.__file__))
        ),
        invocation={
            "argv": argv if argv is not None else sys.argv[1:],
            "executable": sys.executable,
        },
    )
    text = retained_json.dumps(result, sort_keys=True)
    if len(text.encode()) > OUTPUT_LIMIT or time.monotonic() >= deadline:
        result = {
            "schema": SCHEMA,
            "status": "incomplete",
            "error": "parent audit output or wall ceiling",
            **scope(),
        }
        text = retained_json.dumps(result, sort_keys=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
