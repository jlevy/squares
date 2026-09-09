"""Scale a retained ceiling family or state without changing its depth or weights.

Run from packing/ with the project interpreter, passing exp-070's retained family::

    python -m devtools.transport_ceiling_family \
        SOURCE.json \
        --scale 10000/9977 --side 96/25 --verify --out /tmp/n11-unit-control.json

The optional larger container recentres the scaled geometry. A state records its
exact net at the top level; a legacy state must carry that net in best_family.
--net reads a JSON list of rational half-tangents and remaps rows by tangent
identity. It refuses lost angles instead of reinterpreting direction indices.
The output replaces the named file atomically after all requested checks pass.
Scaling is a source transport, not a new search or a proof that eleven fit.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack.cover import write_text_atomic
from sqpack.fractional.ceiling import CeilingCertificate, Placement, verify_ceiling

REPO = Path(__file__).resolve().parents[2]


def transport(
    record: dict[str, Any],
    factor: Fraction,
    *,
    side: Fraction | None = None,
    half_tangents: tuple[Fraction, ...] | None = None,
) -> dict[str, Any]:
    """Transport all geometry exactly; persist the source and destination nets."""
    if factor <= 0:
        raise ValueError("the scale factor must be positive")
    is_state = "best_family" in record
    source = CeilingCertificate.from_record(record["best_family"] if is_state else record)
    if "half_tangents" in record:
        declared = tuple(Fraction(t) for t in record["half_tangents"])
        if declared != source.half_tangents:
            raise ValueError("state and best_family disagree about the source direction net")
    net = source.half_tangents if half_tangents is None else half_tangents
    positions = {t: i for i, t in enumerate(net)}
    if any(t not in positions for t in source.half_tangents):
        raise ValueError("the destination net omits a source direction")
    scaled_side = source.outer_side * factor
    target_side = scaled_side if side is None else side
    if target_side < scaled_side:
        raise ValueError("the destination container is smaller than the scaled source")
    shift = (target_side - scaled_side) / 2
    family = CeilingCertificate(
        source.n,
        target_side,
        source.square_side * factor,
        net,
        tuple(
            Placement(
                p.half_tangent,
                p.centre_x * factor + shift,
                p.centre_y * factor + shift,
                p.weight,
                p.side * factor,
            )
            for p in source.placements
        ),
    )
    if any(
        not (0 <= x <= target_side and 0 <= y <= target_side)
        for placement in family.placements
        for x, y in placement.corners()
    ):
        raise ValueError("a transported placement is outside the container")
    output = family.to_record()
    if is_state:
        if Fraction(record["outer_side"]) != source.outer_side:
            raise ValueError("state and best_family disagree about the source container")
        if Fraction(record["square_side"]) != source.square_side:
            raise ValueError("state and best_family disagree about the source square side")
        rows = []
        for direction, x, y in record["rows"]:
            if type(direction) is not int or not 0 <= direction < len(source.half_tangents):
                raise ValueError("state row has an invalid source direction index")
            rows.append(
                [
                    positions[source.half_tangents[direction]],
                    str(Fraction(x) * factor + shift),
                    str(Fraction(y) * factor + shift),
                ]
            )
        output = {
            "outer_side": str(target_side),
            "square_side": str(family.square_side),
            "half_tangents": [str(t) for t in net],
            "sites": [
                [str(Fraction(x) * factor + shift), str(Fraction(y) * factor + shift)]
                for x, y in record["sites"]
            ],
            "rows": rows,
            "best_family": family.to_record(),
            "best_scaled_total": str(family.total_weight),
            "iterations": [],
            "stopped": "exact geometric transport; no search iterations",
        }
    output["transport"] = {
        "factor": str(factor),
        "source_outer_side": str(source.outer_side),
        "scaled_outer_side": str(scaled_side),
        "translation": [str(shift), str(shift)],
        "source_half_tangents": [str(t) for t in source.half_tangents],
        "destination_half_tangents": [str(t) for t in net],
        "depth_check": "not run; exact affine transport preserves the source depth",
    }
    return output


def source_binding(path: Path) -> dict[str, Any]:
    """Record Git/path identity without a separate checksum manifest."""
    resolved = path.resolve()
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()
    if not resolved.is_relative_to(REPO):
        return {"path": str(resolved), "git_commit": commit, "source_in_worktree": False}
    relative = resolved.relative_to(REPO).as_posix()
    tracked = (
        subprocess.run(
            ["git", "ls-files", "--error-unmatch", "--", relative],
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
        ).returncode
        == 0
    )
    status = subprocess.run(
        ["git", "status", "--porcelain", "--", relative],
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return {
        "path": relative,
        "git_commit": commit,
        "source_in_worktree": True,
        "source_tracked": tracked,
        "source_dirty": bool(status) if tracked else None,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--scale", type=Fraction, required=True)
    parser.add_argument("--side", type=Fraction)
    parser.add_argument("--net", type=Path, help="JSON list of exact destination half-tangents")
    parser.add_argument("--verify", action="store_true", help="replay the transported depth")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.out.resolve() == args.source.resolve():
        parser.error("the source must be preserved; choose a separate output path")
    net = None
    if args.net is not None:
        net = tuple(Fraction(t) for t in json.loads(args.net.read_text()))
    output = transport(
        json.loads(args.source.read_text()), args.scale, side=args.side, half_tangents=net
    )
    output["transport"]["source"] = source_binding(args.source)
    if args.verify:
        family = CeilingCertificate.from_record(output.get("best_family", output))
        verdict = verify_ceiling(family)
        checked = {
            "proved": verdict.proved,
            "failures": list(verdict.failures),
            "max_depth": str(verdict.max_depth),
            "vertices": verdict.vertices,
            "decided_exactly": verdict.decided_exactly,
            "total_weight": str(verdict.total_weight),
            "regime": verdict.regime,
        }
        print(json.dumps(checked), flush=True)
        if any(f != "K3 total weight at least n" for f in verdict.failures):
            return 1
        output["transport"]["depth_check"] = "replayed by verify_ceiling"
        output.get("best_family", output)["provenance"] = {"verify_ceiling": checked}
    write_text_atomic(args.out, json.dumps(output, indent=1) + "\n")
    print(json.dumps({"output": str(args.out), "transport": output["transport"]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
