#!/usr/bin/env python3
"""The retained files of T-046's 46 standing certificates, read in exact rationals.

Written for the stage 4 review of T-046 (bead think-buaj). Decides nothing about
coverage: it checks every premise of the certificate-to-bound argument that is not
coverage, and the internal consistency of the source's own records, for the 36 standing
certificates of the 28 September packet (39d8ecc), the 10 of the 27 September packet
(ad43d29) that T-046 still cites, and the two retained 28 September certificates outside
T-046 (rect_n21_L49875, rect_n77_L891), which are read but not counted.

For each certificate it checks:

- the stored file's digest, and the decompressed digest against the packet README's
  table and both packets' upstream tree manifests;
- the candidate's own n, L, B, rhs and threshold, as literal decimals, against the
  directory name and T-046's claim;
- every weight nonnegative and exact, every positive-weight rectangle nondegenerate and
  inside [0, L]^2, the positive orbit count against the README, the exact mass as the sum
  of the weight strings, its gap below n, and the densest expanded image;
- the scaling record: factor_exact equal to target / source, target equal to the mass;
- the embedded and separate metadata equal, with the standard net, core, epsilon and
  smoothing margin, and the metadata mass equal to the computed one;
- the accepting run's summary (status, 201 angle cases, target 10001/10000, checker
  digest, input digest) and its 201 per-angle rows (r = 0..200 once, each verified,
  node and leaf sums, least printed bound at least up(10001/10000));
- the packet's exact preflight receipt for the same certificate.

It also checks the net identities in exact arithmetic, L^2 >= 2 B^2 at every side, and
the two transfers by mass that T-046 claims (n = 77 from rect_n76_L892, n = 90 from
rect_n89_L955).

Usage, from packing/:
  .venv/bin/python3 -I PROGRAMS/certificates_t046.py --packing . --out OUT.json
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import re
import sys
from decimal import Decimal
from fractions import Fraction as Q
from pathlib import Path

WEB = "resources/web"
PACKETS = {
    "2026-09-27": "wand125-rectangle-certificates-2026-09-27",
    "2026-09-28": "wand125-rectangle-certificates-2026-09-28",
}
#: Tokoharu's verify.cpp, byte-identical in every certificate directory.
CHECKER = "a75140df1b484ad104a214d2e8de87afda9fca5929341ec40121afde0c1af602"
CORE = Q(9977, 10000)
STEP = Q(83, 40000)
DIRECTIONS = 201
EPSILON = Q(1, 20000)
THRESHOLD = Q(10001, 10000)
RHS = Q(1001, 1000)

#: T-046's claim as registered: s(n) >= value, one standing certificate per count, and
#: n = 77 and n = 90 by the mass of the n = 76 and n = 89 certificates.
CLAIM = {
    18: "939/200", 19: "963/200", 20: "979/200", 26: "553/100", 27: "28/5", 28: "143/25",
    29: "579/100", 30: "1173/200", 31: "1187/200", 37: "257/40", 38: "327/50",
    39: "663/100", 40: "1339/200", 41: "1351/200", 42: "679/100", 43: "1373/200",
    44: "1387/200", 51: "2977/400", 52: "1507/200", 53: "1519/200", 54: "3067/400",
    55: "771/100", 56: "777/100", 57: "1567/200", 58: "789/100", 59: "198/25",
    60: "397/50", 61: "199/25", 66: "67/8", 67: "1691/200", 68: "1699/200", 69: "343/40",
    70: "431/50", 71: "1737/200", 72: "437/50", 73: "439/50", 74: "221/25", 75: "889/100",
    76: "223/25", 77: "223/25", 78: "1791/200", 86: "1871/200", 88: "189/20",
    89: "191/20", 90: "191/20", 91: "1929/200", 94: "1959/200", 95: "49209/5000",
}
BY_MASS = {77: 76, 90: 89}

#: The standing certificate of each claimed count, and the packet that retains it.
STANDING = {
    "2026-09-27": [
        "rect_n18_L4695", "rect_n19_L4815", "rect_n20_L4895", "rect_n26_L553",
        "rect_n27_L56", "rect_n30_L5865", "rect_n40_L6695", "rect_n61_L796",
        "rect_n75_L889", "rect_n78_L8955",
    ],
    "2026-09-28": [
        "rect_n28_L572", "rect_n29_L579", "rect_n31_L5935", "rect_n37_L6425",
        "rect_n38_L654", "rect_n39_L663", "rect_n41_L6755", "rect_n42_L679",
        "rect_n43_L6865", "rect_n44_L6935", "rect_n51_L74425", "rect_n52_L7535",
        "rect_n53_L7595", "rect_n54_L76675", "rect_n55_L771", "rect_n56_L777",
        "rect_n57_L7835", "rect_n58_L789", "rect_n59_L792", "rect_n60_L794",
        "rect_n66_L8375", "rect_n67_L8455", "rect_n68_L8495", "rect_n69_L8575",
        "rect_n70_L862", "rect_n71_L8685", "rect_n72_L874", "rect_n73_L878",
        "rect_n74_L884", "rect_n76_L892", "rect_n86_L9355", "rect_n88_L945",
        "rect_n89_L955", "rect_n91_L9645", "rect_n94_L9795", "rect_n95_L98418",
    ],
}
#: Retained in the 28 September packet but not standing in T-046.
OUTSIDE = ["rect_n21_L49875", "rect_n77_L891"]


def write_report(path: Path, report: dict) -> None:
    """JSON with each row of a list of records on one line, so a receipt stays readable
    and under the 1,000 lines above which a retained data file is compressed."""
    items = sorted(report.items())
    lines = ["{"]
    for index, (key, value) in enumerate(items):
        if isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
            body = ",\n".join("  " + json.dumps(item, sort_keys=True) for item in value)
            text = f"  {json.dumps(key)}: [\n{body}\n  ]"
        else:
            text = f"  {json.dumps(key)}: {json.dumps(value, sort_keys=True)}"
        lines.append(text + ("," if index < len(items) - 1 else ""))
    lines.append("}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def literal(token: str) -> Q:
    return Q(Decimal(token))


def exact_json(data: bytes) -> dict:
    return json.loads(data, parse_float=literal, parse_int=lambda token: Q(int(token)))


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def up(value: Q) -> float:
    """The least binary64 at or above an exact rational."""
    f = float(value)
    return f if Q(f) >= value else math.nextafter(f, math.inf)


def side_of(name: str) -> Q:
    digits = name.rsplit("_L", 1)[1]
    return literal(digits[0] + "." + digits[1:])


def readme_rows(readme: str) -> dict[str, tuple[str, str, int]]:
    """`| n | `name` | `side` = ... | `mass` = ... | rectangles |` rows of a packet README."""
    rows: dict[str, tuple[str, str, int]] = {}
    pattern = re.compile(
        r"^\| (\d+) \| `(rect_n\d+_L\d+)` \| `([0-9/]+)` = [0-9.]+ \| `([0-9/]+)` = [0-9.]+ \| (\d+) \|"
    )
    for line in readme.splitlines():
        match = pattern.match(line)
        if match:
            rows[match[2]] = (match[3], match[4], int(match[5]))
    return rows


def readme_pins(readme: str) -> dict[str, str]:
    """Stored path -> decompressed SHA-256, from the README's compressed-files table."""
    pins: dict[str, str] = {}
    for line in readme.splitlines():
        cells = [cell.strip().strip("`") for cell in line.split("|")]
        if len(cells) >= 6 and cells[1].endswith(".gz") and re.fullmatch(r"[0-9a-f]{64}", cells[4]):
            pins[cells[1]] = cells[4]
    return pins


def manifest(path: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, name = line.split(None, 1)
        found[name.removeprefix("./")] = digest
    return found


def check(packing: Path, packet: str, name: str, context: dict) -> dict:
    root = packing / WEB / PACKETS[packet]
    folder = root / "wand125-rectangles/certificates" / name
    problems: list[str] = []
    stored = (folder / "certified_candidate.json.gz").read_bytes()
    plain = gzip.decompress(stored)
    pin_key = f"wand125-rectangles/certificates/{name}/certified_candidate.json.gz"
    if context["pins"][packet].get(pin_key) != sha256(plain):
        problems.append("decompressed candidate digest is not the README's pin")
    for label, tree in context["manifests"].items():
        if tree.get(f"certificates/{name}/certified_candidate.json") not in (None, sha256(plain)):
            problems.append(f"candidate digest differs from the {label} tree manifest")
    if context["manifests"]["2026-09-28"].get(f"certificates/{name}/certified_candidate.json") != sha256(plain):
        problems.append("candidate not pinned by the 39d8ecc tree manifest")
    raw = exact_json(plain)
    n = int(raw["n"])
    side = Q(raw["L"])
    if (n, side) != (int(name.split("_")[1][1:]), side_of(name)):
        problems.append("candidate n or L differs from the directory name")
    if Q(raw["B"]) != CORE or Q(raw["rhs"]) != RHS:
        problems.append("candidate B or rhs is not 9977/10000, 1001/1000")
    if Q(str(raw["coverage_lower_bound_exact"])) != THRESHOLD:
        problems.append("declared threshold is not 10001/10000")
    for key in ("points", "segments", "proof_net", "net", "schema"):
        if key in raw:
            problems.append(f"candidate has a {key} field")
    weights = [Q(str(w)) for w in raw["weights"]]
    if len(weights) != len(raw["rectangles"]):
        problems.append("weights and rectangles differ in length")
    if any(w < 0 for w in weights):
        problems.append("negative weight")
    positive = 0
    densest = Q(0)
    distinct: set[tuple[Q, Q, Q, Q]] = set()
    for row, weight in zip(raw["rectangles"], weights, strict=False):
        if weight == 0:
            continue
        positive += 1
        x1, y1, x2, y2 = (Q(value) for value in row)
        if not (0 <= x1 < x2 <= side and 0 <= y1 < y2 <= side):
            problems.append(f"rectangle {row} not inside [0, L]^2 or degenerate")
        densest = max(densest, weight / ((x2 - x1) * (y2 - y1)))
        for a1, a2 in ((x1, x2), (side - x2, side - x1)):
            for b1, b2 in ((y1, y2), (side - y2, side - y1)):
                distinct.add((a1, b1, a2, b2))
                distinct.add((b1, a1, b2, a2))
    mass = sum(weights, Q(0))
    gap = n - mass
    if not (0 < mass < n):
        problems.append("mass is not strictly between 0 and n")
    if Q(raw["mass"]) != mass:
        problems.append("the candidate's mass field is not the sum of its weights")
    scaling = raw.get("scaling_experiment") or {}
    factor = Q(scaling["factor_exact"])
    if Q(scaling["target_mass_exact"]) != mass:
        problems.append("scaling target is not the mass")
    if factor != Q(scaling["target_mass_exact"]) / Q(scaling["source_mass_exact"]) or factor <= 0:
        problems.append("factor_exact is not target / source, or not positive")
    embedded = raw["certificate"]
    metadata = json.loads((folder / "certificate_metadata.json").read_text(encoding="utf-8"))
    for key in ("L", "B", "D", "angle_count", "mass_exact", "epsilon", "safety_exact", "input_sha256"):
        if str(embedded.get(key)) != str(metadata.get(key)):
            problems.append(f"embedded and separate metadata differ in {key}")
    if (
        Q(metadata["L"]) != side
        or Q(metadata["B"]) != CORE
        or Q(metadata["D"]) != STEP
        or int(metadata["angle_count"]) != DIRECTIONS
        or Q(metadata["epsilon"]) != EPSILON
        or Q(metadata["safety_exact"]) != CORE * (1 + STEP) + 3 * EPSILON
        or Q(metadata["mass_exact"]) != mass
    ):
        problems.append("metadata is not the standard net, core and margin, or not this mass")
    summary = json.loads((folder / "verification_summary.json").read_text(encoding="utf-8"))
    rows = [
        json.loads(line)
        for line in (folder / "verified_angles.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    least = min(row["lower_bound"] for row in rows)
    if (
        summary["status"] != "VERIFIED"
        or summary["angle_cases"] != DIRECTIONS
        or Q(summary["target_lower_bound_exact"]) != THRESHOLD
        or summary["verifier_source_sha256"] != CHECKER
        or summary["input_sha256"] != metadata["input_sha256"]
    ):
        problems.append("summary is not VERIFIED at 201 directions, 10001/10000, this checker and input")
    if sorted(row["r"] for row in rows) != list(range(DIRECTIONS)):
        problems.append("per-angle rows are not r = 0..200 once each")
    if any(row["status"] != "verified" for row in rows):
        problems.append("a per-angle row is not verified")
    if sum(row["nodes"] for row in rows) != summary["nodes"] or sum(row["leaves"] for row in rows) != summary["leaves"]:
        problems.append("per-angle node or leaf sums differ from the summary")
    if least != summary["minimum_printed_leaf_lower_bound"] or least < up(THRESHOLD):
        problems.append("least printed bound differs from the summary or is below up(10001/10000)")
    preflight = context["preflight"].get(name)
    if (
        preflight is None
        or preflight["status"] != "PASS"
        or preflight["input_sha256"] != metadata["input_sha256"]
        or Q(preflight["mass_exact"]) != mass
        or Q(preflight["L"]) != side
        or preflight["positive_basis_rectangles"] != positive
        # The preflight counts the eight images with multiplicity, as the checker reads
        # them; the census counts distinct images after merging coincident ones.
        or preflight["expanded_rectangles"] != 8 * positive
        or preflight["upstream_nodes"] != summary["nodes"]
    ):
        problems.append("the packet's preflight receipt does not PASS this certificate as read here")
    table = context["tables"][packet].get(name) or context["tables"]["2026-09-28"].get(name)
    if table is None or (Q(table[0]), Q(table[1]), table[2]) != (side, mass, positive):
        problems.append("the packet README's claims row differs")
    return {
        "certificate": name,
        "packet": packet,
        "n": n,
        "L": str(side),
        "mass": str(mass),
        "mass_below_n": str(gap),
        "positive_orbits": positive,
        "listed_rows": len(weights),
        "distinct_images": len(distinct),
        "densest_image_density": float(densest),
        "densest_log2": round(math.log2(densest), 2),
        "scaling_factor": float(factor),
        "upstream_nodes": summary["nodes"],
        "least_printed_leaf_bound": least,
        "axis_vertices_upstream": preflight["axis_vertex_count"] if preflight else None,
        "input_sha256": metadata["input_sha256"],
        "candidate_gz_sha256": sha256(stored),
        "candidate_sha256": sha256(plain),
        "problems": problems,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--packing", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    packing = args.packing.resolve()
    context: dict = {"pins": {}, "manifests": {}, "tables": {}, "preflight": {}}
    for packet, folder in PACKETS.items():
        readme = (packing / WEB / folder / "README.md").read_text(encoding="utf-8")
        context["pins"][packet] = readme_pins(readme)
        context["tables"][packet] = readme_rows(readme)
        context["manifests"][packet] = manifest(packing / WEB / folder / "acquisition/upstream-tree.sha256")
    receipt = json.loads(gzip.decompress((packing / WEB / PACKETS["2026-09-28"] / "receipts/preflight/audit.json.gz").read_bytes()))
    context["preflight"] = {case["certificate"]: case for case in receipt["cases"]}
    results = [
        check(packing, packet, name, context)
        for packet, names in STANDING.items()
        for name in names
    ]
    outside = [check(packing, "2026-09-28", name, context) for name in OUTSIDE]
    by_count = {row["n"]: row for row in results}
    claim_problems: list[str] = []
    for n, value in CLAIM.items():
        row = by_count.get(BY_MASS.get(n, n))
        if row is None:
            claim_problems.append(f"n = {n}: no standing certificate")
            continue
        if Q(row["L"]) != Q(value):
            claim_problems.append(f"n = {n}: T-046 claims {value}, the certificate has {row['L']}")
        if not Q(row["mass"]) < n:
            claim_problems.append(f"n = {n}: the certificate's mass is not below {n}")
    if len(results) != 46 or set(by_count) != set(CLAIM) - set(BY_MASS):
        claim_problems.append("the 46 standing certificates are not one per directly claimed count")
    sides = [Q(row["L"]) for row in results]
    top = (DIRECTIONS - 1) * STEP
    net = {
        "B(1 + D)": str(CORE * (1 + STEP)),
        "B(1 + D) + 3 epsilon": str(CORE * (1 + STEP) + 3 * EPSILON),
        "t_max": str(top),
        "t_max^2 + 2 t_max - 1": str(top * top + 2 * top - 1),
        "all hold": CORE * (1 + STEP) < 1
        and CORE * (1 + STEP) + 3 * EPSILON < 1
        and top * top + 2 * top - 1 > 0
        and top <= Q(1, 2)
        and all(side * side >= 2 * CORE * CORE for side in sides),
    }
    gaps: dict[str, list[str]] = {}
    for row in results:
        gaps.setdefault(row["mass_below_n"], []).append(row["certificate"])
    report = {
        "kind": "t046-review-certificates/v1",
        "certificates": results,
        "outside_t046": outside,
        "claim_problems": claim_problems,
        "net": net,
        "mass_below_n": gaps,
        "densest_log2_max": max(row["densest_log2"] for row in results),
        "scaling_factor_range": [
            min(row["scaling_factor"] for row in results),
            max(row["scaling_factor"] for row in results),
        ],
        "least_printed_leaf_bound": min(row["least_printed_leaf_bound"] for row in results),
        "up_threshold": up(THRESHOLD),
        "positive_orbit_range": [
            min(row["positive_orbits"] for row in results),
            max(row["positive_orbits"] for row in results),
        ],
        "upstream_nodes_total": sum(row["upstream_nodes"] for row in results),
        "problems": sum(len(row["problems"]) for row in results + outside) + len(claim_problems),
        "status": "PASS"
        if not claim_problems and net["all hold"] and not any(row["problems"] for row in results + outside)
        else "FAIL",
    }
    write_report(args.out, report)
    print(f"{report['status']}: {len(results)} standing certificates, {len(outside)} outside T-046, "
          f"{report['problems']} problems; mass gaps {sorted(gaps)}; net {net['all hold']}")
    for row in results + outside:
        for problem in row["problems"]:
            print(f"  {row['certificate']}: {problem}")
    for problem in claim_problems:
        print(f"  {problem}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
