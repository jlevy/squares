"""Hold this review's checker to the maintained routes at every number they share (T-231).

Reads the receipts the other programs wrote (``outputs/check-z.json``, ``check-c.json``,
``maintained-*.json``, ``sharp-controls.json``) and the certificate, and compares: the
side and all 204 poses as read by this review's reader and as the maintained adapter
handed them to the kernel (``checker_input``); the number of pairs; the least wall
clearance and the least pair gap of the positive on all four deciders; the kernel's
tightest pair and closing normal against this review's least-gap pair; the kernel's
``top_clearance`` against this review's least right and top clearances; the gross
controls' margins; and the kernel's own sharp controls against this review's mutants at
the same walls and pair. It also holds the T-229 reference that ``identity_t231.py``
measured against (the source's ``certificates/n-204.cert`` from this lane's clone) to the
T-229 packet's derived Witness/v2 fact, pose by pose. It compares and decides nothing.

Run with the project interpreter (PyYAML reads the fact)::

    python -I agree_t231.py --outputs OUTPUTS --cert CERT --t229 N-204.CERT --t229-fact FACT.yaml.gz
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import lzma
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

PROGRAM = Path(__file__).resolve()
sys.path.insert(0, str(PROGRAM.parent))
check = importlib.import_module("review_t231_check")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:  # noqa: PLR0914, PLR0915
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--outputs", type=Path, required=True)
    parser.add_argument("--cert", type=Path, required=True)
    parser.add_argument("--t229", type=Path, required=True)
    parser.add_argument("--t229-fact", type=Path, required=True)
    parser.add_argument(
        "--records-receipt",
        type=Path,
        help="the records lane's receipts/exact-certification.json.xz, compared when given",
    )
    args = parser.parse_args()
    out = args.outputs
    z = load(out / "check-z.json")
    c = load(out / "check-c.json")
    positive = load(out / "maintained-positive.json")
    duplicate = load(out / "maintained-duplicate-square-overlap.json")
    outside = load(out / "maintained-square-translated-outside-container.json")
    sharp = load(out / "maintained-sharp.json")
    controls = {row["id"]: row for row in load(out / "sharp-controls.json")["mutants"]}
    cert = check.read_certificate(args.cert.read_text(encoding="ascii"))
    checks: list[dict[str, Any]] = []

    def hold(name: str, ours: Any, theirs: Any) -> None:
        checks.append({"check": name, "equal": ours == theirs, "ours": str(ours)[:200], "theirs": str(theirs)[:200]})

    row = positive["row"]
    hold("side as read", check.text_of(cert.side), row["checker_input"]["side"])
    ours_poses = [[check.text_of(value) for value in pose] for pose in cert.rows]
    hold("all 204 poses as read, literal by literal", ours_poses, row["checker_input"]["poses"])
    for route in ("exact_verify", "independent"):
        verdict = row[route]
        hold(f"pairs tested ({route})", z["pairs_decided"], verdict["pairs_tested"])
        least_wall = min((Fraction(z["least_wall"][w]["clearance"]) for w in check.WALLS))
        hold(f"least wall clearance, route Z against {route}", least_wall, Fraction(verdict["minimum_containment_clearance"]))
        least_wall_c = min((Fraction(c["least_wall"][w]["clearance"]) for w in check.WALLS))
        hold(f"least wall clearance, route C against {route}", least_wall_c, Fraction(verdict["minimum_containment_clearance"]))
        hold(f"least pair gap, route Z against {route}", Fraction(z["least_gap"]["gap"]), Fraction(verdict["minimum_best_pair_gap"]))
        hold(f"least pair gap, route C against {route}", Fraction(c["least_gap"]["gap"]), Fraction(verdict["minimum_best_pair_gap"]))
    hold("pairs tested, route C", c["pairs_decided"], z["pairs_decided"])
    hold("least Euclidean pair (route C) against the least-gap pair (route Z)", c["least_distance_squared"]["pair"], z["least_gap"]["pair"])
    hold(
        "least squared Euclidean distance (route C) against the least gap squared (route Z)",
        Fraction(c["least_distance_squared"]["value"]),
        Fraction(z["least_gap"]["gap"]) ** 2,
    )
    tight = sharp["tightest_pair"]
    hold("kernel's tightest pair against the least-gap pair", z["least_gap"]["pair"], tight["pair_0_based"])
    hold("kernel's tightest gap against the least gap", Fraction(z["least_gap"]["gap"]), Fraction(tight["gap"]))
    p0 = controls["P0"]
    pair = p0["pair"]
    poses = check.poses_z(cert)
    axis = p0["normal"]
    owner = poses[pair[0]] if axis < 2 else poses[pair[1]]
    a, b, d = Fraction(owner.a), Fraction(owner.b), Fraction(owner.d)
    nx, ny = (a / d, b / d) if axis % 2 == 0 else (-b / d, a / d)
    dx = Fraction(poses[pair[1]].xn, poses[pair[1]].xd) - Fraction(poses[pair[0]].xn, poses[pair[0]].xd)
    dy = Fraction(poses[pair[1]].yn, poses[pair[1]].yd) - Fraction(poses[pair[0]].yn, poses[pair[0]].yd)
    if nx * dx + ny * dy > 0:
        nx, ny = -nx, -ny
    hold("kernel's closing normal against this review's P0 normal", [nx, ny], [Fraction(v) for v in tight["direction"]])
    top_right = min(Fraction(z["least_wall"]["right"]["clearance"]), Fraction(z["least_wall"]["top"]["clearance"]))
    hold("kernel's top_clearance against the least right-or-top clearance", top_right, Fraction(sharp["top_clearance"]))
    for route in ("exact_verify", "independent"):
        hold(
            f"outside control's least wall ({route}) against G2 on route Z",
            Fraction(controls["G2"]["own"]["Z"]["least_wall"]),
            Fraction(outside["row"][route]["minimum_containment_clearance"]),
        )
        hold(
            f"duplicate control's least gap ({route}) against G1 on route Z",
            Fraction(controls["G1"]["own"]["Z"]["least_gap"]),
            Fraction(duplicate["row"][route]["minimum_best_pair_gap"]),
        )
    for kernel_name, ours_id, field in (
        ("side-lowered-past-wall-contact (at contact)", "F0", "wall"),
        ("side-lowered-past-wall-contact", "F1", "wall"),
        ("tightest-pair-closed-past-contact (at contact)", "P0", "gap"),
        ("tightest-pair-closed-past-contact", "P1", "gap"),
    ):
        ours_field = "least_wall" if field == "wall" else "least_gap"
        for route in ("exact_verify", "independent"):
            hold(
                f"kernel's {kernel_name} {field} ({route}) against {ours_id} on route C",
                Fraction(controls[ours_id]["own"]["C"][ours_field]),
                Fraction(sharp["sharp"][kernel_name][route][field]),
            )
            hold(
                f"kernel's {kernel_name} verdict ({route}) against {ours_id}",
                controls[ours_id]["verdicts"]["C"],
                sharp["sharp"][kernel_name][route]["passed"],
            )
    # The T-229 reference: the clone's n-204.cert against the packet's derived fact.
    fact = yaml.safe_load(gzip.decompress(args.t229_fact.read_bytes()))["witness"]
    t229 = check.read_certificate(args.t229.read_text(encoding="ascii"))
    hold("T-229 side: clone's n-204.cert against the packet's fact", Fraction(*t229.side), Fraction(fact["side"]))
    same = 0
    for (x, y, t), square in zip(t229.rows, fact["squares"], strict=True):
        tt = Fraction(*t)
        basis = ((1 - tt * tt) / (1 + tt * tt), 2 * tt / (1 + tt * tt))
        centre = (Fraction(*x), Fraction(*y))
        if centre == tuple(Fraction(v) for v in square["center"]) and basis == tuple(
            Fraction(v) for v in square["basis"]
        ):
            same += 1
    hold("T-229 poses equal to the fact's, of 204", same, len(fact["squares"]))
    if args.records_receipt is not None:
        receipt = json.loads(lzma.decompress(args.records_receipt.read_bytes()))
        by_control = {case["control"]: case for case in receipt["cases"]}
        lane = by_control["positive"]
        hold("records lane's receipt: side", check.text_of(cert.side), lane["checker_input"]["side"])
        hold("records lane's receipt: all 204 poses", ours_poses, lane["checker_input"]["poses"])
        for route in ("exact_verify", "independent"):
            for field in ("minimum_containment_clearance", "minimum_best_pair_gap", "pairs_tested", "verification_passed"):
                hold(f"records lane's receipt against this lane's maintained run: {route} {field}", row[route][field], lane[route][field])
            for control, mine in (("duplicate-square-overlap", duplicate), ("square-translated-outside-container", outside)):
                for field in ("minimum_containment_clearance", "minimum_best_pair_gap", "verification_passed"):
                    hold(f"records lane's receipt against this lane's maintained run: {control} {route} {field}", mine["row"][route][field], by_control[control][route][field])
    record = {
        "program": PROGRAM.name,
        "program_sha256": hashlib.sha256(PROGRAM.read_bytes()).hexdigest(),
        "python": sys.version,
        "checks": checks,
        "all_equal": all(item["equal"] for item in checks),
        "count": len(checks),
    }
    (out / "agree.json").write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    for item in checks:
        sys.stdout.write(f"{'equal' if item['equal'] else 'DIFFER'}: {item['check']}\n")
    sys.stdout.write(f"{sum(item['equal'] for item in checks)} of {len(checks)} equal\n")
    return 0 if record["all_equal"] else 1


if __name__ == "__main__":
    sys.exit(main())
