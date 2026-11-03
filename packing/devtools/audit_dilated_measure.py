"""Audit a format M certificate made by dilating a retained one onto a declared net.

Doğa Özden's `s(94) >= 1993/200` (jlevy/squares#890) is Hiroaki Hosono's
`mixed_n94_L995` measure dilated about the origin by `λ = 1993/1990`, with a finer net
declared (`proof_net`) so that the dilated core still fits a unit square. Its bound
rests on a complete coverage decision by `sqverify-fast`, which
`devtools.sqverify_fast_census` runs and keeps; this tool is the first-party premise
check of its import, and the comparison of that decision with the producer's receipts.
It decides no coverage. `DILATIONS` names each certificate it reads, by its packet.

- ``audit`` recomputes, from the packet's retained files and the base packet's, in exact
  rationals and apart from the crate:

  - the file: format M, rectangles only (each row exactly four coordinates and a mass),
    `scaling_factor` absent or 1, a `proof_net`
    with exactly `step` and `last` (and `count = last + 1` if given), no top-level
    `net`, and eight times the densest row's density at most `2^32` (item 1 of the
    records-lane checklist of the 6 October declared-net soundness review);
  - the measure: every mass nonnegative, every rectangle nondegenerate and inside the
    container, the masses totalling exactly the stated `total_mass`, `n - 1/100000`,
    below `n`;
  - lemma N0's (a) to (e) on the declared net (`sqverify_fast/SOUNDNESS.md`);
  - the dilation: `L = λ L₀` and `B = λ B₀`, the same row count, each rectangle `λ`
    times the base's row by row, and each mass equal;
  - the regeneration: the base rewritten as the source's `tools/rescale.py` says,
    serialized as Python's `json.dump` writes it, is byte for byte the retained file's
    decompressed text. The receipt records each text's SHA-256 beside the one the
    source states, as data: Git holds the retained bytes (OR-16), and the stage 2
    custody check compared them once;
  - and, as observations its status requires nothing of, what the dilation does not
    carry: `λ B₀ (1 + D₀)` on the base's own net (its declared step, else the standard
    one), the direction-0 centre domain's growth `ρ₀ (1 - 1/λ)` in the base's
    coordinates on an unchanged net, and the route's ceiling `L₀ / B₀`.

- ``compare`` reads the census capture (`census-mixed/PACKET/NAME.jsonl.gz`) and each
  receipt of the producer's own `sqverify-fast` runs, and compares them direction by
  direction on every field but the two timings (`cpu_seconds`, `seconds`), and their
  summaries on status, nodes, refused directions and premises. It also reads the
  producer's second checker's replay (`second-checker/full.jsonl`) for its verdicts and
  least bound, as a reading of the producer's output that decides nothing.

``--check`` recomputes either receipt and fails unless it equals the retained one and
passes (`PREMISES_HOLD`, `EVERY_DIRECTION_AGREES`). A capture or receipt with a line
that is neither a direction row nor the summary, a direction twice, or no summary or a
second one, is refused.

From ``packing/``::

    .venv/bin/python3 -m devtools.audit_dilated_measure audit \\
        ozden-s94-lower-bound-2026-11-03 --write
    .venv/bin/python3 -m devtools.audit_dilated_measure compare \\
        ozden-s94-lower-bound-2026-11-03 --write
    .venv/bin/python3 -m devtools.audit_dilated_measure audit \\
        ozden-s94-lower-bound-2026-11-03 --check
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from sqpack import retained_json

PROJECT = Path(__file__).resolve().parents[1]
WEB = PROJECT / "resources/web"
CENSUS = PROJECT / "benchmarks/measure-verifier/census-mixed"

#: The keys a format M certificate may carry, beside the ones this audit reads.
FORMAT_M_KEYS = frozenset(
    {"n", "L", "B", "total_mass", "points", "rectangles", "proof_net", "derived_from"}
)
#: Lemma N0 (a)'s cap on a declared net's direction count.
MAX_DIRECTIONS = 2**16
#: Item 1's cap on eight times the densest row's density.
MAX_DENSITY = 2**32
#: The standard net's step, on which the base certificate stands.
STANDARD_STEP = Fraction(83, 40000)
#: The two timings a direction's row records, which no two runs share.
TIMINGS = frozenset({"cpu_seconds", "seconds"})


@dataclass(frozen=True)
class Dilation:
    """One dilated certificate and the retained one it dilates."""

    #: The census name of the certificate (`sqverify_fast_census.MIXED_FILES`).
    name: str
    n: int
    side: Fraction
    #: The certificate, relative to its packet.
    candidate: str
    #: The base candidate, relative to `resources/web/`.
    base: str
    #: The SHA-256 the source states for the base's JSON text.
    base_sha256: str
    #: The SHA-256 the source states for the certificate's JSON text.
    text_sha256: str
    #: The producer's `sqverify-fast` receipts, relative to the packet.
    receipts: tuple[str, ...]
    #: The producer's second checker's replay, relative to the packet.
    second_checker: str


DILATIONS: dict[str, Dilation] = {
    "ozden-s94-lower-bound-2026-11-03": Dilation(
        name="mixed_n94_L9965",
        n=94,
        side=Fraction(1993, 200),
        candidate="source/certificate/n94_L9965.json.gz",
        base=(
            "wand125-mixed-bounds-evening-2026-10-04/square-packing-bounds/certificates/"
            "mixed_n94_L995/candidate.json.gz"
        ),
        base_sha256="64d819536a9994172b1f7a7b2095e7b40e420a09efa7441d459e73191a20667a",
        text_sha256="b8b03ee83fd2738f723759e8a54442adb55e607a211dd57d28873a62db9c749c",
        receipts=(
            "source/receipts/sqverify-fast-rustc1.98-full.jsonl",
            "source/receipts/sqverify-fast-rustc1.93-full.jsonl",
        ),
        second_checker="source/second-checker/full.jsonl",
    ),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def text_of(path: Path) -> bytes:
    """A retained file's JSON text: decompressed when it is gzip."""
    raw = path.read_bytes()
    return gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw


def as_text(value: Fraction) -> str:
    return str(value)


def rectangles(data: dict[str, Any]) -> list[tuple[list[Fraction], Fraction]]:
    return [
        ([Fraction(v) for v in row["rectangle"]], Fraction(row["mass"]))
        for row in data["rectangles"]
    ]


def file_checks(data: dict[str, Any], dilation: Dilation) -> dict[str, Any]:
    """Item 1 of the records-lane checklist, and the measure's own premises."""
    side = Fraction(data["L"])
    net = data.get("proof_net")
    net_keys = sorted(net) if isinstance(net, dict) else None
    # Each row is exactly a rectangle of four coordinates and a mass; the geometry is
    # read only when every row has that shape.
    shaped = all(
        isinstance(row, dict)
        and set(row) == {"rectangle", "mass"}
        and isinstance(row["rectangle"], list)
        and len(row["rectangle"]) == 4
        for row in data["rectangles"]
    )
    rows = rectangles(data) if shaped else []
    masses = [mass for _, mass in rows]
    densities = [
        mass / ((box[2] - box[0]) * (box[3] - box[1]))
        for box, mass in rows
        if box[2] > box[0] and box[3] > box[1]
    ] or [Fraction(0)]
    total = sum(masses, Fraction(0))
    stated = Fraction(data["total_mass"])
    return {
        "n_matches": int(data["n"]) == dilation.n,
        "side_matches": side == dilation.side,
        "format_m": data.get("points") == [] and "segments" not in data,
        "keys_known": sorted(set(data) - FORMAT_M_KEYS) == [],
        "every_row_a_rectangle_of_four_and_a_mass": shaped,
        "scaling_factor": data.get("scaling_factor"),
        "scaling_factor_absent_or_one": Fraction(str(data.get("scaling_factor", 1))) == 1,
        "proof_net_keys": net_keys,
        "proof_net_exact_keys": net_keys in (["last", "step"], ["count", "last", "step"]),
        "count_is_last_plus_one": (
            isinstance(net, dict)
            and int(net.get("count", int(net["last"]) + 1)) == int(net["last"]) + 1
        ),
        "no_top_level_net": "net" not in data,
        "no_certificate_metadata": "certificate" not in data,
        "rows": len(data["rectangles"]),
        "every_mass_nonnegative": shaped and all(mass >= 0 for mass in masses),
        "every_rectangle_nondegenerate": shaped
        and all(box[2] > box[0] and box[3] > box[1] for box, _ in rows),
        "every_rectangle_inside": shaped
        and all(
            box[0] >= 0 and box[2] <= side and box[1] >= 0 and box[3] <= side for box, _ in rows
        ),
        "total_mass": as_text(total),
        "total_mass_equals_stated": total == stated,
        "mass_gap": as_text(dilation.n - total),
        "mass_is_n_minus_1_100000": total == dilation.n - Fraction(1, 100000),
        "mass_below_n": total < dilation.n,
        "densest_row": as_text(max(densities)),
        "densest_row_approx": float(max(densities)),
        "eight_densest_within_2_32": 8 * max(densities) <= MAX_DENSITY,
    }


def lemma_n0(data: dict[str, Any]) -> dict[str, Any]:
    """Lemma N0's (a) to (e) on the file's declared net, in exact rationals."""
    core = Fraction(data["B"])
    step = Fraction(data["proof_net"]["step"])
    last = int(data["proof_net"]["last"])
    count = last + 1
    tangent = last * step
    shrink = core * (1 + step)
    endpoint = tangent**2 + 2 * tangent - 1
    tangent_form = core * (1 + step / (1 - step**2 / 4))
    return {
        "B": as_text(core),
        "D": as_text(step),
        "angle_count": count,
        "net_last_tangent": as_text(tangent),
        "a_step_positive_and_count_in_range": step > 0 and 2 <= count <= MAX_DIRECTIONS,
        "b_shrink": as_text(shrink),
        "b_shrink_below_one": shrink < 1,
        "c_endpoint": as_text(endpoint),
        "c_endpoint_positive": endpoint > 0,
        "d_last_tangent_at_most_half": tangent <= Fraction(1, 2),
        "e_tangent_form": as_text(tangent_form),
        "e_tangent_form_below_one": tangent_form < 1,
    }


def rescaled_text(base_text: bytes, side: Fraction, step: Fraction, last: int) -> bytes:
    """The base rewritten as the source's `tools/rescale.py` says, as `json.dump` writes it.

    Its rule, read from the retained script: keep the base's keys in order, set `L` and
    `B`, append `proof_net`, scale every rectangle coordinate by `λ` and keep each mass as
    its text, write `n` as an integer, drop `scaling_source_digest` and `scaling_factor`,
    and append `derived_from`. Every number is read as its text, so nothing is rounded.
    """
    data = json.loads(base_text, parse_float=str, parse_int=str)
    scale = side / Fraction(data["L"])
    out = dict(data)
    out["L"] = str(side)
    out["B"] = str(Fraction(data["B"]) * scale)
    out["proof_net"] = {"step": str(step), "last": last}
    out["rectangles"] = [
        {"rectangle": [str(Fraction(v) * scale) for v in row["rectangle"]], "mass": row["mass"]}
        for row in data["rectangles"]
    ]
    out["n"] = int(data["n"])
    out.pop("scaling_source_digest", None)
    out.pop("scaling_factor", None)
    out["derived_from"] = f"published certificate at L={data['L']} scaled by lambda={scale}"
    return json.dumps(out).encode()


def base_step(base: dict[str, Any]) -> Fraction:
    """The step of the base's own net: the one it declares, else the standard one."""
    net = base.get("proof_net")
    return Fraction(net["step"]) if isinstance(net, dict) else STANDARD_STEP


def dilation_checks(data: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """That the certificate is the base dilated, row by row, in exact rationals. Every
    boolean here is a condition the audit's status requires."""
    side, base_side = Fraction(data["L"]), Fraction(base["L"])
    scale = side / base_side
    rows, base_rows = rectangles(data), rectangles(base)
    paired = list(zip(rows, base_rows, strict=False))
    base_core = Fraction(base["B"])
    return {
        "lambda": as_text(scale),
        "core_is_lambda_times_base": Fraction(data["B"]) == scale * base_core,
        "same_row_count": len(rows) == len(base_rows),
        "every_rectangle_lambda_times_base": len(rows) == len(base_rows)
        and all(box == [scale * v for v in base_box] for (box, _), (base_box, _) in paired),
        "every_mass_equal": len(rows) == len(base_rows)
        and all(mass == base_mass for (_, mass), (_, base_mass) in paired),
        "total_mass_equal": Fraction(data["total_mass"]) == Fraction(base["total_mass"]),
    }


def dilation_observations(data: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """What the dilation does not carry, reported and required of nothing: the dilated
    core on the base's own net, the axis domain's growth in the base's coordinates on an
    unchanged net, and the route's ceiling as the step goes to zero."""
    side, base_side = Fraction(data["L"]), Fraction(base["L"])
    scale = side / base_side
    base_core = Fraction(base["B"])
    step = base_step(base)
    base_shrink = scale * base_core * (1 + step)
    return {
        "base_net": base.get("proof_net", "standard"),
        "base_step": as_text(step),
        "dilated_core_on_base_net": as_text(base_shrink),
        "base_net_admits_dilated_core": base_shrink < 1,
        "axis_domain_growth_in_base_coordinates": as_text(Fraction(1, 2) * (1 - 1 / scale)),
        "route_ceiling": as_text(base_side / base_core),
        "side_below_ceiling": side < base_side / base_core,
    }


def audit(packet: str) -> dict[str, Any]:
    """The `audit` receipt of one packet's dilated certificate."""
    dilation = DILATIONS[packet]
    path = WEB / packet / dilation.candidate
    base_path = WEB / dilation.base
    text = text_of(path)
    base_text = text_of(base_path)
    data = json.loads(text, parse_float=str)
    base = json.loads(base_text, parse_float=str)
    step = Fraction(data["proof_net"]["step"])
    last = int(data["proof_net"]["last"])
    regenerated = rescaled_text(base_text, dilation.side, step, last)
    file = file_checks(data, dilation)
    net = lemma_n0(data)
    if not file["every_row_a_rectangle_of_four_and_a_mass"]:
        message = f"{path}: a row is not a rectangle of four coordinates and a mass"
        raise SystemExit(message)
    scaled = dilation_checks(data, base)
    # The digests are recorded beside the source's stated ones, for a reader and the
    # test; Git holds the retained bytes (OR-16), so the gate is the byte comparison.
    digests = {
        "candidate": str(path.relative_to(PROJECT.parent)),
        "candidate_sha256": sha256(path.read_bytes()),
        "text_sha256": sha256(text),
        "text_sha256_stated": dilation.text_sha256,
        "base": str(base_path.relative_to(PROJECT.parent)),
        "base_text_sha256": sha256(base_text),
        "base_text_sha256_stated": dilation.base_sha256,
        "regenerated_text_sha256": sha256(regenerated),
    }
    scaled["regenerated_text_is_the_certificate"] = regenerated == text
    passes = (
        all(value is True for value in file.values() if isinstance(value, bool))
        and all(value is True for value in net.values() if isinstance(value, bool))
        and all(value is True for value in scaled.values() if isinstance(value, bool))
    )
    return {
        "kind": "dilated-measure-audit/v1",
        "packet": packet,
        "certificate": dilation.name,
        "n": dilation.n,
        "L": as_text(dilation.side),
        "digests": digests,
        "file": file,
        "lemma_n0": net,
        "dilation": scaled,
        "observations": dilation_observations(data, base),
        "status": "PREMISES_HOLD" if passes else "PREMISES_FAIL",
        "decides": (
            "no coverage: the premises, the dilation and the regeneration only; the"
            " observations are reported and required of nothing"
        ),
    }


def read_rows(path: Path) -> tuple[dict[int, dict[str, Any]], dict[str, Any]]:
    """A `sqverify-fast` capture's direction rows by index, and its summary."""
    rows: dict[int, dict[str, Any]] = {}
    summary: dict[str, Any] | None = None
    for number, line in enumerate(text_of(path).decode().splitlines(), start=1):
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("kind") == "sqverify-fast-summary/v1":
            if summary is not None:
                message = f"{path}:{number}: a second summary"
                raise SystemExit(message)
            summary = record
        elif "r" in record:
            index = int(record["r"])
            if index in rows:
                message = f"{path}:{number}: direction {index} twice"
                raise SystemExit(message)
            rows[index] = record
        else:
            message = f"{path}:{number}: neither a direction row nor the summary"
            raise SystemExit(message)
    if summary is None:
        message = f"{path}: no summary"
        raise SystemExit(message)
    return rows, summary


def untimed(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key not in TIMINGS}


def compare_receipt(
    ours: dict[int, dict[str, Any]], summary: dict[str, Any], path: Path
) -> dict[str, Any]:
    """One producer receipt against the census capture, direction by direction."""
    theirs, their_summary = read_rows(path)
    differing = {
        str(index): sorted(
            key
            for key in set(untimed(ours.get(index, {}))) | set(untimed(theirs.get(index, {})))
            if untimed(ours.get(index, {})).get(key) != untimed(theirs.get(index, {})).get(key)
        )
        for index in sorted(set(ours) | set(theirs))
        if untimed(ours.get(index, {})) != untimed(theirs.get(index, {}))
    }
    fields = ("status", "nodes", "refused_directions", "directions", "premises", "threshold")
    return {
        "receipt": str(path.relative_to(PROJECT.parent)),
        "receipt_sha256": sha256(path.read_bytes()),
        "directions": len(theirs),
        "same_directions": sorted(theirs) == sorted(ours),
        "identical_directions": sum(
            1
            for index in ours
            if index in theirs and untimed(ours[index]) == untimed(theirs[index])
        ),
        "differing": differing,
        "summary_equal": {
            field: summary.get(field) == their_summary.get(field) for field in fields
        },
        "their_build": their_summary.get("build"),
        "their_threads": their_summary.get("threads"),
        "their_direction_cpu_seconds": their_summary.get("direction_cpu_seconds"),
        "their_status": their_summary.get("status"),
    }


def second_checker(path: Path, directions: int) -> dict[str, Any]:
    """The producer's second checker's verdicts and least bound, read and not run."""
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    indices = sorted(int(row["r"]) for row in rows)
    verdicts = sorted({str(row.get("verdict")) for row in rows})
    # Its rows state each direction's least certified bound in fixed-point units of
    # `scale` (2^42), as `min_bound_units`.
    bounds = [
        (Fraction(int(row["min_bound_units"]), int(row["scale"])), int(row["r"]))
        for row in rows
        if "min_bound_units" in row and "scale" in row
    ]
    least = min(bounds) if bounds else None
    return {
        "replay": str(path.relative_to(PROJECT.parent)),
        "replay_sha256": sha256(path.read_bytes()),
        "rows": len(rows),
        "every_direction_once": indices == list(range(directions)),
        "verdicts": verdicts,
        "nodes": sum(int(row.get("nodes") or 0) for row in rows),
        "least_bound": as_text(least[0]) if least else None,
        "least_bound_approx": float(least[0]) if least else None,
        "least_bound_direction": least[1] if least else None,
        "decides": "nothing here: the producer's output, read; the checker was not run",
    }


def compare(packet: str) -> dict[str, Any]:
    """The `compare` receipt: the census capture against the producer's receipts."""
    dilation = DILATIONS[packet]
    capture = CENSUS / packet / f"{dilation.name}.jsonl.gz"
    ours, summary = read_rows(capture)
    receipts = [
        compare_receipt(ours, summary, WEB / packet / path) for path in dilation.receipts
    ]
    count = int((summary.get("premises") or {}).get("angle_count") or 0)
    agree = all(
        item["same_directions"]
        and item["identical_directions"] == count
        and all(item["summary_equal"].values())
        for item in receipts
    )
    least = min(
        (row["min_certified_lower_bound"] for row in ours.values()),
        default=None,
    )
    return {
        "kind": "dilated-measure-replay-comparison/v1",
        "packet": packet,
        "certificate": dilation.name,
        "capture": str(capture.relative_to(PROJECT.parent)),
        "capture_sha256": sha256(capture.read_bytes()),
        "directions": count,
        "status": summary.get("status"),
        "nodes": summary.get("nodes"),
        "least_certified_bound": least,
        "build": summary.get("build"),
        "threads": summary.get("threads"),
        "direction_cpu_seconds": summary.get("direction_cpu_seconds"),
        "cpu_ratio_to_receipts": [
            round(
                float(summary["direction_cpu_seconds"])
                / float(item["their_direction_cpu_seconds"]),
                3,
            )
            if summary.get("direction_cpu_seconds") and item["their_direction_cpu_seconds"]
            else None
            for item in receipts
        ],
        "receipts": receipts,
        "second_checker": second_checker(WEB / packet / dilation.second_checker, count),
        "verdict": "EVERY_DIRECTION_AGREES" if agree else "DIRECTIONS_DIFFER",
        "compared": "every field of every direction row but cpu_seconds and seconds",
    }


def receipt_path(packet: str, command: str) -> Path:
    name = "dilation-audit.json" if command == "audit" else "replay-comparison.json"
    return WEB / packet / "receipts" / name


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("command", choices=("audit", "compare"))
    parser.add_argument("packet", choices=sorted(DILATIONS))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--write", action="store_true", help="write the packet's receipt")
    group.add_argument("--check", action="store_true", help="fail unless it is unchanged")
    args = parser.parse_args(argv)
    receipt = audit(args.packet) if args.command == "audit" else compare(args.packet)
    path = receipt_path(args.packet, args.command)
    text = retained_json.dumps(receipt)
    passed = (
        receipt["status"] == "PREMISES_HOLD"
        if args.command == "audit"
        else (receipt["verdict"] == "EVERY_DIRECTION_AGREES")
    )
    if args.check:
        stored = json.loads(path.read_text(encoding="utf-8"))
        if stored != json.loads(text):
            sys.stderr.write(f"{path}: differs from the recomputed receipt\n")
            return 1
        if not passed:
            sys.stderr.write(f"{path}: unchanged, and it does not pass\n")
            return 1
        sys.stdout.write(f"{path.relative_to(PROJECT)}: unchanged, and it passes\n")
        return 0
    if args.write:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
