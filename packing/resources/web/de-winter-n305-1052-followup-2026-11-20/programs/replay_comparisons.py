"""Replay #1052 follow-up identities; do not decide variant feasibility or motion bounds.

Use the project's exact readers, pose margins and contraction implementation. The
contraction factor comes from the accepted original receipt; it is not recomputed here.
No contributor program is loaded. See the packet README for the replay command.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_write_text

from devtools import contraction_margin, evand_exact_certificates, retained_data
from devtools.upper_bound_reports import parse_certificate


def require(condition: object, message: str) -> None:
    """Refuse mismatched evidence even when Python assertions are disabled."""
    if not condition:
        raise ValueError(message)


def custody(repo: Path, packet: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    manifest = json.loads((packet / "acquisition/manifest.json").read_bytes())
    declared = {
        name: digest
        for digest, name in (
            line.split(None, 1)
            for line in (packet / "acquisition/upstream-members.sha256")
            .read_text()
            .splitlines()
        )
    }
    require(len(declared) == len(manifest["members"]), "Manifest member count differs")
    data: dict[str, bytes] = {}
    for row in manifest["members"]:
        name = row["member"]
        require(declared[name] == row["sha256"], f"Source manifest digest differs: {name}")
        if "retained_as" in row:
            raw = (packet / row["retained_as"]).read_bytes()
            if row["storage"] == "gzip":
                raw = gzip.decompress(raw)
        elif "identical_to" in row:
            raw = retained_data.read_retained_bytes(repo / row["identical_to"])
        else:
            continue
        require(len(raw) == row["bytes"], f"Source size differs: {name}")
        require(
            hashlib.sha256(raw).hexdigest() == row["sha256"], f"Source digest differs: {name}"
        )
        data[name] = raw
    license_row = manifest["license"]
    license_bytes = (repo / license_row["identical_to"]).read_bytes()
    require(
        hashlib.sha256(license_bytes).hexdigest() == license_row["sha256"], "Licence differs"
    )
    return manifest, data


def variants(original: dict[str, Any], data: dict[str, bytes], reader: Any) -> dict[str, Any]:
    result = {}
    for name, expected_changes, expected_moved, expected_aligned in (
        ("n305_31_quarter_turns.json", 31, [], 207),
        ("n305_37_aligned.json", 37, [108, 140, 141, 142, 143, 150, 153, 164, 175], 213),
    ):
        variant = reader.read_form_j(data[name])
        require(variant["n"] == original["n"] == 305, "Variant count differs")
        require(variant["side"] == original["side"], "Variant side differs")
        pairs = list(zip(original["poses"], variant["poses"], strict=True))
        moved = [i for i, (a, b) in enumerate(pairs, 1) if a[:2] != b[:2]]
        turns = [i for i, (a, b) in enumerate(pairs, 1) if a[2:] != b[2:]]
        aligned = sum(c * s == 0 for _, _, c, s in variant["poses"])
        require(moved == expected_moved, f"Moved center roster differs: {name}")
        require(len(turns) == expected_changes, f"Changed direction count differs: {name}")
        require(aligned == expected_aligned, f"Axis-aligned count differs: {name}")
        largest = max(abs(b[j] - a[j]) for a, b in pairs for j in (0, 1))
        require(largest <= Fraction(2, 10**11), f"Coordinate movement exceeds limit: {name}")
        result[name] = {
            "same_exact_side": True,
            "moved_center_ids": moved,
            "changed_direction_ids": turns,
            "axis_aligned_count": aligned,
            "maximum_coordinate_displacement": str(largest),
            "whole_packing_feasibility": "pending",
        }
    return result


def corrected_witness(
    repo: Path,
    manifest: dict[str, Any],
    original: dict[str, Any],
    data: dict[str, bytes],
    reader: Any,
) -> dict[str, Any]:
    corrected = data["n305_witness.yaml"]
    lines = corrected.splitlines(keepends=True)
    restored = b"".join(lines[:2] + lines[5:17] + lines[21:])
    original_yaml = (repo / manifest["prior_evidence"]["original_yaml"]).read_bytes()
    require(restored == original_yaml, "Metadata removal does not restore original YAML")
    witness = reader.read_form_c(corrected)
    require(
        witness["side"] == original["side"] and witness["n"] == 305, "Witness header differs"
    )
    for (x, y, c, s), corners in zip(original["poses"], witness["corners"], strict=True):
        expected = {
            (x + (i * c - j * s) / 2, y + (i * s + j * c) / 2) for i in (-1, 1) for j in (-1, 1)
        }
        require(expected == set(corners), "Corrected witness corner differs")
    return {"original_bytes_restored": True, "added_metadata_lines": 7, "equal_corners": 1220}


def reconstruction(original: dict[str, Any], certificate: Any) -> dict[str, Any]:
    q = 10**82
    factor = 1 + Fraction(3, q)
    poses = original["poses"]
    require(
        all((coordinate / factor * q).denominator == 1 for p in poses for coordinate in p[:2]),
        "A center is off the reconstructed grid",
    )
    require(
        all((s * q / (1 + c)).denominator == 1 for _, _, c, s in poses),
        "A half-angle tangent is off the reconstructed grid",
    )
    h = max(max(x, y) / factor + (abs(c) + abs(s)) / 2 for x, y, c, s in poses)
    require(h == original["side"] - Fraction(54, q), "Pre-expansion extent differs")
    require(Fraction(math.ceil(q * factor * h), q) == original["side"], "Side rounding differs")
    reboxed = contraction_margin.contract(certificate, Fraction(1))
    return {
        "center_coordinates_on_grid": 610,
        "half_angle_tangents_on_grid": 305,
        "grid_denominator": str(q),
        "center_expansion": str(factor),
        "h_equals_side_minus_54_over_q": True,
        "ceiling_identity": True,
        "translation_and_trim_gain": str(certificate.side - reboxed.side),
        "historical_export_settings": "not established",
    }


def forced_turns(original: dict[str, Any], geometry: Any) -> dict[str, Any]:
    poses = original["poses"]
    near = {
        i
        for i, (_, _, c, s) in enumerate(poses, 1)
        if 0 < min(abs(c), abs(s)) < Fraction(1, 10**9)
    }
    require(
        len(near) == 36 and not near.intersection({54, 140, 143}), "Near-axis roster differs"
    )
    rows = []
    for kept, snapped in ((54, 108), (140, 150), (143, 153), (153, 164), (164, 175)):
        require(snapped in near, "Forced turn is outside near-axis roster")
        x, y, c, s = poses[snapped - 1]
        turned = (
            (x, y, Fraction(1 if c > 0 else -1), Fraction(0))
            if abs(c) > abs(s)
            else (x, y, Fraction(0), Fraction(1 if s > 0 else -1))
        )
        margin = geometry.margin(
            geometry.integer_pose(*poses[kept - 1]), geometry.integer_pose(*turned)
        )
        require(margin < 0, "Claimed forced pair does not overlap")
        rows.append({"kept": kept, "snapped": snapped, "margin": str(margin)})
    return {
        "near_axis_ids": sorted(near),
        "forced_original_turns": [108, 150, 153, 164, 175],
        "exact_conflicts": rows,
        "maximum_snaps_upper_bound": 31,
        "scope": (
            "Original centers and side; each near-axis direction kept or snapped; others fixed."
        ),
        "feasible_31_snap_lower_bound": "pending",
        "minimum_nine_moved_centers": (
            "pending: 34 geometric solver checks and hitting-set proof"
        ),
    }


def precision(
    repo: Path, manifest: dict[str, Any], certificate: Any, data: dict[str, bytes]
) -> dict[str, Any]:
    receipt = json.loads(
        (repo / manifest["prior_evidence"]["contraction_receipt"]).read_bytes()
    )
    require(
        receipt["certificate"]["sha256"] == hashlib.sha256(data["n305_exact.json"]).hexdigest(),
        "Prior contraction receipt names different source bytes",
    )
    require(receipt["routes_accept"] is True, "Prior contraction receipt is not accepted")
    contracted = contraction_margin.contract(certificate, Fraction(receipt["lambda_star"]))
    candidate = json.loads(gzip.decompress(data["precision/n305-candidate.json.gz"]))
    require(candidate["n"] == certificate.n == 305, "Precision candidate count differs")
    require(
        Fraction(candidate["side"]) == Fraction(receipt["contracted_side"]) == contracted.side,
        "Precision candidate side differs from accepted contraction",
    )
    poses = tuple(
        evand_exact_certificates.Pose(*map(Fraction, row)) for row in candidate["squares"]
    )
    require(
        poses == contracted.poses, "Precision candidate poses differ from accepted contraction"
    )
    return {
        "equal_poses": len(poses),
        "exact_side_difference_from_accepted_contraction": "0",
        "side_ceiling_12": evand_exact_certificates.ceiling_decimal(contracted.side, 12),
        "gain_over_original": str(certificate.side - contracted.side),
        "option_d": "restatement: equal to predecessor contracted to first contact",
        "dependency": manifest["prior_evidence"]["contraction_receipt"],
        "factor_or_pair_replay_performed": False,
    }


def replay(repo: Path, packet: Path) -> dict[str, Any]:
    manifest, data = custody(repo, packet)
    review = repo / "packing/resources/web/de-winter-n305-1052-review-2026-11-20/programs"
    sys.path.insert(0, str(review))
    reader = importlib.import_module("r1052_reader")
    geometry = importlib.import_module("r1052_poses")
    original = reader.read_form_j(data["n305_exact.json"])
    certificate = parse_certificate(data["n305_exact.json"], 305, "center-direction-json")
    return {
        "format": "n305-followup-comparisons-v1",
        "scope": "Exact custody, artifact and pose identities; five local conflicts only.",
        "source_programs_executed": False,
        "retained_or_preexisting_member_digests_checked": len(data),
        "corrected_witness": corrected_witness(repo, manifest, original, data, reader),
        "variants": variants(original, data, reader),
        "export_reconstruction": reconstruction(original, certificate),
        "restricted_alignment": forced_turns(original, geometry),
        "precision_enclosure": precision(repo, manifest, certificate, data),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--packet", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = replay(args.repo.resolve(), args.packet.resolve())
    if args.check:
        require(
            result == json.loads(args.check.read_bytes()), "Saved comparison receipt differs"
        )
    text = json.dumps(result, indent=2) + "\n"
    if args.out:
        atomic_write_text(args.out, text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
