"""Sharp and gross controls for the n = 204 certificate (T-231), on four deciders.

Each mutant is built from the certificate as this review's reader reads it and written
as certificate text with exact rational literals. Each is then decided by this review's
two routes (``review_t231_check.py``, routes Z and C) and by the repository's two
maintained routes, reached as ``devtools.upper_bound_reports certify``'s child reaches
them: the text through the ``evand-cert`` adapter, then ``sqpack.witness.exact_verify``
on the kernel's witness (``devtools.evand_arrangement_reports.to_witness``) and
``devtools.check_rational_witness_independent.check_squares`` on exact corners.

The mutants are the certificate taken to exact contact, which must be accepted, and
``1e-30`` past it, which must be refused, at the top-and-right walls (the side lowered),
the left wall and the bottom wall (every square moved), and at three pairs (one square
moved along the edge normal that gives the pair's separating gap): the least gap of the
certificate, between two squares tilted alike; the least gap between a tilted and an
axis-aligned square; and the least gap between two axis-aligned squares. Then the two
gross controls, a duplicated square and a square moved outside, and two reader mutants.
The verdicts are the deciders'; this program adds the mutants and the expectations, and
decides nothing of its own.

From ``packing/`` of the reference checkout, with the project interpreter::

    python -I sharp_controls_t231.py --packing . CERT --out CONTROLS.json
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

PROGRAM = Path(__file__).resolve()
sys.path.insert(0, str(PROGRAM.parent))
check = importlib.import_module("review_t231_check")

EPSILON = Fraction(1, 10**30)
WITNESS_PREFIX = "W-mishapolk-n204-n"
CLAIM_LIMITATIONS = "Sharp control of the stage 4 review lane; decides a mutant only."


def literal(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else str(value)


def as_fractions(cert: Any) -> tuple[Fraction, list[list[Fraction]]]:
    side = Fraction(*cert.side)
    rows = [[Fraction(*value) for value in row] for row in cert.rows]
    return side, rows


def text(side: Fraction, rows: list[list[Fraction]], comment: str, n: int | None = None) -> str:
    count = len(rows) if n is None else n
    lines = [f"# {comment}", f"{count} {literal(side)}"]
    lines += [" ".join(literal(value) for value in row) for row in rows]
    return "\n".join(lines) + "\n"


def normal_of(axis: int, first: Any, second: Any) -> tuple[Fraction, Fraction]:
    """The unit edge normal ``axis`` of the pair, oriented so that moving ``second`` along
    it closes the pair's separation on that normal."""
    owner = first if axis < 2 else second
    a, b, d = Fraction(owner.a), Fraction(owner.b), Fraction(owner.d)
    nx, ny = (a / d, b / d) if axis % 2 == 0 else (-b / d, a / d)
    dx = Fraction(second.xn, second.xd) - Fraction(first.xn, first.xd)
    dy = Fraction(second.yn, second.yd) - Fraction(first.yn, first.yd)
    projection = nx * dx + ny * dy
    return (-nx, -ny) if projection > 0 else (nx, ny)


def least_pair(poses: list[Any], kind: tuple[bool, bool] | None) -> tuple[int, int, Fraction, int]:
    def tilted(pose: Any) -> bool:
        return not (pose.a == 0 or pose.b == 0)

    best: tuple[int, int, Fraction, int] | None = None
    for i in range(len(poses)):
        for j in range(i + 1, len(poses)):
            if kind is not None and {tilted(poses[i]), tilted(poses[j])} != set(kind):
                continue
            gap_rat, axis = check.pair_gap_z(poses[i], poses[j])
            gap = Fraction(*gap_rat)
            if best is None or gap < best[2]:
                best = (i, j, gap, axis)
    if best is None:
        msg = "no pair of that kind"
        raise ValueError(msg)
    return best


def build_mutants(cert: Any) -> list[dict[str, Any]]:
    side, rows = as_fractions(cert)
    poses = check.poses_z(cert)
    walls = {
        wall: [Fraction(*check.wall_clearances_z(pose, cert.side)[wall]) for pose in poses]
        for wall in check.WALLS
    }
    top_right = min(min(walls["right"]), min(walls["top"]))
    left = min(walls["left"])
    bottom = min(walls["bottom"])
    mutants: list[dict[str, Any]] = []
    for label, past in (("F0", False), ("F1", True)):
        lowered = side - top_right - (EPSILON if past else 0)
        mutants.append(
            {
                "id": label,
                "what": "the side lowered by the least top-or-right clearance"
                + (" and 1e-30 more" if past else ""),
                "expected": not past,
                "text": text(lowered, rows, f"{label} control"),
            }
        )
    for label, past, wall, amount, coordinate in (
        ("N0", False, "left", left, 0),
        ("N1", True, "left", left, 0),
        ("B0", False, "bottom", bottom, 1),
        ("B1", True, "bottom", bottom, 1),
    ):
        step = amount + (EPSILON if past else 0)
        moved = [list(row) for row in rows]
        for row in moved:
            row[coordinate] -= step
        mutants.append(
            {
                "id": label,
                "what": f"every square moved toward the {wall} wall by its least clearance"
                + (" + 1e-30" if past else ""),
                "expected": not past,
                "text": text(side, moved, f"{label} control"),
            }
        )
    for prefix, kind, name in (
        ("P", None, "the least gap (two squares tilted alike)"),
        ("Q", (True, False), "the least gap between a tilted and an axis-aligned square"),
        ("A", (False, False), "the least gap between two axis-aligned squares"),
    ):
        i, j, gap, axis = least_pair(poses, kind)
        nx, ny = normal_of(axis, poses[i], poses[j])
        for past in (False, True):
            step = gap + (EPSILON if past else 0)
            moved = [list(row) for row in rows]
            moved[j][0] += step * nx
            moved[j][1] += step * ny
            label = f"{prefix}{int(past)}"
            mutants.append(
                {
                    "id": label,
                    "what": f"square {j} moved toward square {i} along edge normal {axis} by "
                    f"{name}" + (" + 1e-30" if past else ""),
                    "pair": [i, j],
                    "normal": axis,
                    "gap": literal(gap),
                    "expected": not past,
                    "text": text(side, moved, f"{label} control"),
                }
            )
    duplicated = [list(row) for row in rows]
    duplicated[1] = list(duplicated[0])
    mutants.append(
        {
            "id": "G1",
            "what": "square 1 replaced by a copy of square 0",
            "expected": False,
            "text": text(side, duplicated, "G1 control"),
        }
    )
    outside = [list(row) for row in rows]
    outside[0][0] += side + 2
    mutants.append(
        {
            "id": "G2",
            "what": "square 0 moved right by the side and 2",
            "expected": False,
            "text": text(side, outside, "G2 control"),
        }
    )
    mutants.append(
        {
            "id": "R1",
            "what": "the last row dropped, the header unchanged",
            "expected": False,
            "text": text(side, rows[:-1], "R1 control", n=cert.n),
        }
    )
    first_x = rows[0][0]
    decimal = str(first_x.numerator * 10**35 // first_x.denominator)
    decimal_text = decimal[:-35] + "." + decimal[-35:]
    if Fraction(decimal_text) != first_x:
        msg = "square 0's x is not a 35-place decimal"
        raise ValueError(msg)
    lines = text(side, rows, "R2 control").split("\n")
    fields = lines[2].split()
    fields[0] = decimal_text
    lines[2] = " ".join(fields)
    mutants.append(
        {
            "id": "R2",
            "what": "square 0's x written as its exact decimal (a reader difference)",
            "expected": None,
            "text": "\n".join(lines),
        }
    )
    return mutants


def decide_own(mutant_text: str) -> dict[str, Any]:
    try:
        cert = check.read_certificate(mutant_text)
    except check.CertificateError as error:
        return {"Z": {"refused_by_reader": str(error)}, "C": {"refused_by_reader": str(error)}}
    out: dict[str, Any] = {}
    for route, run in (("Z", check.route_z), ("C", check.route_c)):
        result = run(cert)
        least_wall = min(
            (Fraction(result["least_wall"][wall]["clearance"]) for wall in check.WALLS)
        )
        out[route] = {
            "accepted": result["accepted"],
            "least_wall": literal(least_wall),
            "least_gap": None if result["least_gap"] is None else result["least_gap"]["gap"],
            "wall_contacts": {wall: result["least_wall"][wall]["contacts"] for wall in check.WALLS},
            "wall_violations": {
                wall: result["least_wall"][wall]["violations"] for wall in check.WALLS
            },
        }
        if route == "Z":
            out[route]["touching_pairs"] = result["touching_pairs"]
            out[route]["overlapping_pairs"] = result["overlapping_pairs"]
        else:
            out[route]["positive_area_pairs"] = [
                [i, j] for i, j, _ in result["positive_area_pairs"]
            ]
            out[route]["nonempty_clip_pairs"] = result["nonempty_clip_pairs"]
    return out


def decide_maintained(mutant_text: str, reports: Any, kernel: Any, legacy: Any) -> dict[str, Any]:
    try:
        cert = reports.evand_cert(mutant_text.encode(), 204, {})
    except reports.ReportError as error:
        return {
            "exact_verify": {"refused_by_reader": str(error)},
            "independent": {"refused_by_reader": str(error)},
        }
    first, _report = legacy.exact_verify(
        kernel.to_witness(cert, witness_prefix=WITNESS_PREFIX, claim_limitations=CLAIM_LIMITATIONS)
    )
    second = legacy.independent.check_squares(legacy.corner_squares(cert), cert.side)
    return {
        route: {
            "accepted": bool(verdict["verification_passed"]),
            "least_wall": verdict["minimum_containment_clearance"],
            "least_gap": verdict["minimum_best_pair_gap"],
            "failures": [str(item)[:160] for item in verdict["failures"]][:6],
        }
        for route, verdict in (("exact_verify", first), ("independent", second))
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--packing", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--mutants-dir", type=Path)
    args = parser.parse_args()
    sys.path.insert(0, str(args.packing.resolve()))
    reports = importlib.import_module("devtools.upper_bound_reports")
    kernel = importlib.import_module("devtools.evand_arrangement_reports")
    legacy = importlib.import_module("devtools.evand_exact_certificates")
    raw = args.certificate.read_bytes()
    cert = check.read_certificate(raw.decode("ascii"))
    started = time.process_time()
    mutants = build_mutants(cert)
    results: list[dict[str, Any]] = []
    all_ok = True
    for mutant in mutants:
        body = mutant.pop("text")
        digest = hashlib.sha256(body.encode()).hexdigest()
        if args.mutants_dir is not None:
            args.mutants_dir.mkdir(parents=True, exist_ok=True)
            (args.mutants_dir / f"{mutant['id']}.cert").write_text(body, encoding="ascii")
        own = decide_own(body)
        maintained = decide_maintained(body, reports, kernel, legacy)
        verdicts = {
            "Z": own["Z"].get("accepted", False),
            "C": own["C"].get("accepted", False),
            "exact_verify": maintained["exact_verify"].get("accepted", False),
            "independent": maintained["independent"].get("accepted", False),
        }
        expected = mutant["expected"]
        ok = expected is None or all(value is expected for value in verdicts.values())
        all_ok = all_ok and ok
        results.append(
            {**mutant, "sha256": digest, "verdicts": verdicts, "as_expected": ok, "own": own, "maintained": maintained}
        )
        sys.stdout.write(
            json.dumps({"id": mutant["id"], "expected": expected, "verdicts": verdicts, "ok": ok}) + "\n"
        )
        sys.stdout.flush()
    record = {
        "program": PROGRAM.name,
        "program_sha256": hashlib.sha256(PROGRAM.read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(check.__file__).read_bytes()).hexdigest(),
        "python": sys.version,
        "certificate_sha256": hashlib.sha256(raw).hexdigest(),
        "epsilon": literal(EPSILON),
        "all_as_expected": all_ok,
        "mutants": results,
        "cpu_seconds": round(time.process_time() - started, 3),
    }
    args.out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    sys.stdout.write(json.dumps({"all_as_expected": all_ok, "cpu_seconds": record["cpu_seconds"]}) + "\n")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
