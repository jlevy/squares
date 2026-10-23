"""Measure what the n = 204 certificate (T-231) shares with Evan Daniel's exact solver's output.

The project ran Evan Daniel's regularizer driver (``devtools.regularize_evand run``) on
T-229's witness on 22 October 2026, and this review ran it again on 23 October with the
same input digest. Its exact solve (``exactsolve.py``) writes a certificate,
``solve/witness.cert``, and records which squares it found free (rattlers) and which flat
variables it froze; its regularize step writes ``regularize.cert``, the display view at
the same side. This program compares the certificate under review with both, row by row
as text and as exact poses, and classifies every row that differs by what the solve says
about it. It also states the certificate's own structure: its pairs at contact scale by
the tilt of their squares, its rows that are exactly a half-integer times ``1 + 1e-20``,
and the clearance of each free square in the certificate, in T-229 and in the solve's
certificate; and it tabulates the near-axis tilts of the 204 family under the pairings
``identity_t231.py`` measured. It decides nothing.

Run with ``python3 -I``::

    lineage_t231.py --cert CERT --t229 N-204.CERT --solve-dir RERUN/solve \\
        --regularized RERUN/regularize.cert --identity OUTPUTS/identity.json \\
        --ref T-225=CERT --ref T-223=CERT --ref T-228=CERT --ref T-226=CERT --out LINEAGE.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import math
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

PROGRAM = Path(__file__).resolve()
sys.path.insert(0, str(PROGRAM.parent))
check = importlib.import_module("review_t231_check")
identity = importlib.import_module("identity_t231")

LAMBDA = 1 + Fraction(1, 10**20)


def text_rows(path: Path) -> tuple[list[str], str, list[str]]:
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    lines = data.decode("ascii").splitlines()
    comments = [line for line in lines if line.startswith("#")]
    body = [line for line in lines if line.strip() and not line.startswith("#")]
    return comments, body[0], body[1:]


def poses(rows: list[str]) -> list[tuple[Fraction, Fraction, Fraction]]:
    out = []
    for row in rows:
        x, y, t = (Fraction(value) for value in row.split())
        out.append((x, y, t))
    return out


def move(first: tuple[Fraction, ...], second: tuple[Fraction, ...]) -> float:
    return math.hypot(float(first[0] - second[0]), float(first[1] - second[1]))


def load_json(path: Path) -> Any:
    data = path.read_bytes()
    if path.suffix == ".gz":
        data = gzip.decompress(data)
    return json.loads(data)


def clearance_of(cert: Any, square: int) -> Fraction:
    all_poses = check.poses_z(cert)
    wall = min(Fraction(*value) for value in check.wall_clearances_z(all_poses[square], cert.side).values())
    gap = min(
        Fraction(*check.pair_gap_z(all_poses[min(square, j)], all_poses[max(square, j)])[0])
        for j in range(cert.n)
        if j != square
    )
    return min(wall, gap)


def main() -> int:  # noqa: C901, PLR0912, PLR0914, PLR0915
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--t229", type=Path, required=True)
    parser.add_argument("--solve-dir", type=Path, required=True)
    parser.add_argument("--regularized", type=Path, required=True)
    parser.add_argument("--identity", type=Path, required=True)
    parser.add_argument("--ref", action="append", default=[])
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    record: dict[str, Any] = {
        "program": PROGRAM.name,
        "program_sha256": hashlib.sha256(PROGRAM.read_bytes()).hexdigest(),
        "python": sys.version,
    }
    comments, header, rows = text_rows(args.cert)
    _, header_229, rows_229 = text_rows(args.t229)
    a = poses(rows)
    c229 = poses(rows_229)
    cert = check.read_certificate(args.cert.read_text(encoding="ascii"))
    cert229 = check.read_certificate(args.t229.read_text(encoding="ascii"))
    # 1. The certificate's own structure.
    zposes = check.poses_z(cert)

    def tilted(pose: Any) -> bool:
        return not (pose.a == 0 or pose.b == 0)

    contact_kinds: Counter[str] = Counter()
    for i in range(cert.n):
        for j in range(i + 1, cert.n):
            gap, _ = check.pair_gap_z(zposes[i], zposes[j])
            if gap[0] * 10**15 < gap[1]:
                kind = {(False, False): "aligned-aligned", (True, True): "tilted-tilted"}.get(
                    (tilted(zposes[i]), tilted(zposes[j])), "tilted-aligned"
                )
                contact_kinds[kind] += 1
    half_integer_dilated = 0
    for x, y, _ in a:
        for value in (x, y):
            k = value / LAMBDA * 2
            if k.denominator == 1:
                half_integer_dilated += 1
    record["structure"] = {
        "comment_line": comments,
        "pairs_within_1e-15": dict(contact_kinds),
        "pairs_within_1e-15_total": sum(contact_kinds.values()),
        "coordinates_equal_to_half_integer_times_1_plus_1e-20": half_integer_dilated,
        "tilted_rows": sum(1 for pose in zposes if tilted(pose)),
        "tilted_rows_by_magnitude": {
            "below_1e-10_degrees": sum(1 for _, _, t in a if t != 0 and abs(identity.angle_mod_90(t)) < 1e-10),
            "below_1_degree": sum(1 for _, _, t in a if t != 0 and abs(identity.angle_mod_90(t)) < 1),
            "from_1_degree": sum(1 for _, _, t in a if t != 0 and abs(identity.angle_mod_90(t)) >= 1),
            "least_from_1_degree": min(abs(identity.angle_mod_90(t)) for _, _, t in a if t != 0 and abs(identity.angle_mod_90(t)) >= 1),
            "largest": max(abs(identity.angle_mod_90(t)) for _, _, t in a if t != 0),
            "positive_from_1_degree": sum(1 for _, _, t in a if t != 0 and identity.angle_mod_90(t) >= 1),
            "negative_from_1_degree": sum(1 for _, _, t in a if t != 0 and identity.angle_mod_90(t) <= -1),
        },
        "tilt_angles_degrees": sorted({round(identity.angle_mod_90(t), 9) for _, _, t in a if t != 0}),
    }
    # 1b. T-229 against this certificate scaled about the origin by the ratio of the sides.
    ratio = Fraction(*cert229.side) / Fraction(*cert.side)
    residuals = [
        math.hypot(float(c229[k][0] - ratio * a[k][0]), float(c229[k][1] - ratio * a[k][1]))
        for k in range(204)
    ]
    moves_229 = [move(a[k], c229[k]) for k in range(204)]
    radii = [math.hypot(float(a[k][0]), float(a[k][1])) for k in range(204)]
    record["t229_as_a_dilation"] = {
        "side_ratio_minus_1": check.sci((ratio - 1).numerator, (ratio - 1).denominator, 13),
        "largest_residual_after_scaling": max(residuals),
        "residual_square": max(range(204), key=residuals.__getitem__),
        "largest_move_without_scaling": max(moves_229),
        "move_over_distance_from_origin": {
            "min": min(moves_229[k] / radii[k] for k in range(204)),
            "max": max(moves_229[k] / radii[k] for k in range(204)),
        },
        "tilts_equal_within_degrees": max(
            abs(identity.turn(identity.angle_mod_90(a[k][2]), identity.angle_mod_90(c229[k][2])))
            for k in range(204)
        ),
    }
    # 2. Against the solve's certificate and the regularized view.
    solve_comments, solve_header, solve_rows = text_rows(args.solve_dir / "witness.cert")
    solve = poses(solve_rows)
    witness = load_json(args.solve_dir / "witness.json")
    contacts_path = args.solve_dir / "witness.contacts.json"
    if not contacts_path.exists():
        contacts_path = args.solve_dir / "witness.contacts.json.gz"
    contacts = load_json(contacts_path)
    free = set(witness["free_squares"])
    frozen = contacts["frozen_vars"]
    frozen_squares = {v // 3 for v in frozen}
    identical = [k for k in range(204) if rows[k] == solve_rows[k]]
    differing = [k for k in range(204) if rows[k] != solve_rows[k]]
    free_rows = [k for k in differing if k in free]
    other_rows = [k for k in differing if k not in free]

    def spread(keys: list[int], first: list[Any], second: list[Any]) -> dict[str, float]:
        values = [move(first[k], second[k]) for k in keys]
        return {"max": max(values), "min": min(values)} if values else {}

    components: Counter[str] = Counter()
    for v in frozen:
        k = v // 3
        differ = tuple(i for i in range(3) if a[k][i] != solve[k][i])
        components[",".join("xyt"[i] for i in differ) or "none"] += 1
    reg_comments, reg_header, reg_rows = text_rows(args.regularized)
    regularized = poses(reg_rows)
    record["solver"] = {
        "solve_certificate_sha256": hashlib.sha256((args.solve_dir / "witness.cert").read_bytes()).hexdigest(),
        "comment_line_equal": solve_comments == comments,
        "header_equal": solve_header == header,
        "rows_identical_as_text": len(identical),
        "rows_differing": len(differing),
        "solve_free_squares": sorted(free),
        "differing_rows_that_are_free": len(free_rows),
        "every_free_square_differs": all(k in differing for k in free),
        "solve_frozen_variables": len(frozen),
        "frozen_variables_one_per_square": len(frozen_squares) == len(frozen),
        "differing_non_free_rows_are_the_frozen_squares": set(other_rows) == frozen_squares,
        "frozen_squares_components_that_differ": dict(components),
        "free_rows": {
            "t231_vs_solve": spread(free_rows, a, solve),
            "t231_vs_t229": spread(free_rows, a, c229),
            "solve_vs_t229": spread(free_rows, solve, c229),
            "tilt_differs_from_solve": sum(1 for k in free_rows if a[k][2] != solve[k][2]),
        },
        "frozen_rows": {
            "t231_vs_solve": spread(other_rows, a, solve),
            "t231_vs_t229": spread(other_rows, a, c229),
            "solve_vs_t229": spread(other_rows, solve, c229),
            "tilt_differs_from_solve": sum(1 for k in other_rows if a[k][2] != solve[k][2]),
        },
        "identical_rows_t231_vs_t229": spread(identical, a, c229),
        "frozen_coordinate_vs_dilated_t229": {
            "solve_max": float(max(abs(solve[v // 3][v % 3] - LAMBDA * c229[v // 3][v % 3]) for v in frozen)),
            "t231_max": float(max(abs(a[v // 3][v % 3] - LAMBDA * c229[v // 3][v % 3]) for v in frozen)),
        },
        "solve_reports": {
            key: witness.get(key)
            for key in (
                "S_exact",
                "S_cert",
                "load_bearing_squares",
                "free_clearance",
                "newton_converged",
                "cert_valid",
                "cert_min_wall",
                "cert_min_pair",
                "jam_residual",
            )
        },
        "second_order_status": (witness.get("second_order") or {}).get("status"),
        "regularized_view": {
            "header_equal": reg_header == header,
            "comment_line": reg_comments,
            "rows_identical_as_text": sum(1 for k in range(204) if rows[k] == reg_rows[k]),
            "largest_centre_difference": max(move(a[k], regularized[k]) for k in range(204)),
        },
    }
    solve_cert = check.read_certificate((args.solve_dir / "witness.cert").read_text(encoding="ascii"))
    record["free_square_clearance_by_square"] = {
        str(k): {
            "T-231": check.sci(*(lambda v: (v.numerator, v.denominator))(clearance_of(cert, k)), 12),
            "T-229": check.sci(*(lambda v: (v.numerator, v.denominator))(clearance_of(cert229, k)), 12),
            "solve": check.sci(*(lambda v: (v.numerator, v.denominator))(clearance_of(solve_cert, k)), 12),
            "solve_turn_degrees_from_t229": round(
                identity.turn(identity.angle_mod_90(solve[k][2]), identity.angle_mod_90(c229[k][2])), 6
            ),
        }
        for k in sorted(free)
    }
    record["free_square_clearance"] = {
        name: {
            "min": float(min(values)),
            "max": float(max(values)),
            "below_1e-15": sum(1 for value in values if value < Fraction(1, 10**15)),
        }
        for name, values in (
            ("T-231", [clearance_of(cert, k) for k in sorted(free)]),
            ("T-229", [clearance_of(cert229, k) for k in sorted(free)]),
            ("solve", [clearance_of(solve_cert, k) for k in sorted(free)]),
        )
    }
    # 3. Near-axis tilts and large turns across the family, under the measured pairings.
    measured = json.loads(args.identity.read_text(encoding="utf-8"))["references"]
    test = identity.read_text_certificate(args.cert)
    refs = {"T-229": args.t229}
    for item in args.ref:
        name, _, path = item.partition("=")
        refs[name] = Path(path)
    packings = {name: identity.read_text_certificate(path) for name, path in refs.items()}
    proper = {name: dict(identity.SYMMETRIES)[measured[name]["best"]["symmetry"]] for name in refs}
    assignment = {name: measured[name]["best"]["assignment"] for name in refs}

    def angle(name: str, square: int) -> float:
        value = packings[name].angles[assignment[name][square]]
        return value if proper[name] else -value

    table = []
    turned = []
    for k in range(204):
        values = {"T-231": test.angles[k], **{name: angle(name, k) for name in refs}}
        if any(0 < abs(value) < 0.5 for value in values.values()):
            table.append({"square": k, **{name: round(value, 6) for name, value in values.items()}})
        turns = {name: identity.turn(test.angles[k], angle(name, k)) for name in refs}
        if any(abs(value) > 1 for value in turns.values()):
            turned.append({"square": k, "T-231": round(test.angles[k], 4), **{name: round(angle(name, k), 4) for name in refs}})
    record["near_axis_tilts"] = table
    record["turned_beyond_1_degree_against_some_reference"] = turned
    args.out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    solver = record["solver"]
    summary = {
        "contact_scale_pairs": record["structure"]["pairs_within_1e-15"],
        "half_integer_dilated_coordinates": half_integer_dilated,
        "solve": {
            key: solver[key]
            for key in (
                "comment_line_equal",
                "header_equal",
                "rows_identical_as_text",
                "differing_rows_that_are_free",
                "differing_non_free_rows_are_the_frozen_squares",
                "frozen_squares_components_that_differ",
                "free_rows",
                "frozen_rows",
                "frozen_coordinate_vs_dilated_t229",
            )
        },
        "regularized_view": solver["regularized_view"],
        "free_square_clearance": record["free_square_clearance"],
        "near_axis_rows": len(table),
        "turned": turned,
    }
    sys.stdout.write(json.dumps(summary, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
