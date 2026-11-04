"""Mutants of the certificate that this review must refuse, each for the reason it names.

Usage: dm_mutants.py CERTIFICATE.json.gz HOSONO.json.gz SAMPLE.json OUT.json

Each mutant is built in memory from the certificate's parsed JSON and decided with this
review's own code (dm_premises.decide, dmlib's exact capture, dm_sample's search):

1. `hosono-net`: the dilated certificate on Hosono's net (step 83/40000, last 200), the
   naive dilation. Lemma N0 (b) must refuse it: B(1 + D) > 1.
2. `short-net`: the declared net one direction short (last 598). N0 (c) must refuse it,
   and the half-angle tangents (t_598 + D/2, tan(pi/8)] are then in no bin.
3. `core-not-dilated`: the container and the measure dilated but the core left at
   Hosono's 9977/10000, on Hosono's net, so that (b) holds. Every premise but coverage
   holds, so it must be refused on coverage: a binary64 search at three of Hosono's
   directions, then an exact capture below 1 at a pose in the per-bin domain.
4. `mass-99/100` and `mass-tight`: every mass scaled by 99/100, and by the largest
   factor of the form k/10^9 below 1/F*, where F* is the least exact capture
   `dm_sample.py` found (SAMPLE.json). Premises hold; each must be refused by an exact
   capture below 1 at that pose, found by this review's search, not by the crate.
"""

from __future__ import annotations

import copy
import json
import math
import sys
import time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dm_premises  # noqa: E402
import dm_sample  # noqa: E402
import dmlib  # noqa: E402


def scaled(data: dict, factor: Fraction) -> dict:
    out = copy.deepcopy(data)
    total = Fraction(0)
    for row in out["rectangles"]:
        mass = dmlib.rational(row["mass"]) * factor
        row["mass"] = str(mass)
        total += mass
    out["total_mass"] = str(total)
    return out


def coverage_witness(data: dict, index: int, pose: tuple[float, float]) -> dict:
    cert = dmlib.certificate(data)
    exact = dmlib.ExactMeasure.of(cert, dmlib.expand(cert))
    x, y = pose
    cap = dmlib.fraction_of(dmlib.capture_exact(exact, index, dmlib.exact_of_float(x), dmlib.exact_of_float(y))[0])
    low, high = dmlib.domain(cert, index)
    inside = all(low <= Fraction(v) <= high for v in (x, y))
    return {"r": index, "pose": [x, y], "exact_capture": str(cap), "exact_capture_float": float(cap), "below_1": cap < 1, "in_domain": inside}


def main() -> None:
    cert_path, hosono_path, sample_path, out_path = (Path(a) for a in sys.argv[1:5])
    started = time.process_time()
    data = dmlib.read_gzip_json(cert_path).data
    base = dmlib.read_gzip_json(hosono_path).data
    sample = json.loads(sample_path.read_text())
    results = {}
    failures: list[str] = []

    original = dm_premises.decide(data, base)
    results["original"] = {"status": original["status"]}

    # 1. the naive dilation on Hosono's net
    m1 = copy.deepcopy(data)
    m1["proof_net"] = {"step": "83/40000", "last": 200}
    d1 = dm_premises.decide(m1, base)
    results["hosono-net"] = {"status": d1["status"], "problems": d1["problems"], "B(1 + D)": d1["premises"]["(b) B(1 + D)"]}
    if not any("(b)" in p for p in d1["problems"]):
        failures.append("hosono-net not refused by (b)")

    # 2. one direction short
    m2 = copy.deepcopy(data)
    m2["proof_net"] = {"step": data["proof_net"]["step"], "last": 598}
    d2 = dm_premises.decide(m2, base)
    step = dmlib.rational(data["proof_net"]["step"])
    gap_low = step * 598 + step / 2
    results["short-net"] = {
        "status": d2["status"],
        "problems": d2["problems"],
        "reach t^2 + 2t - 1": d2["premises"]["(c) t_max^2 + 2 t_max - 1"],
        "uncovered_tangents": [str(gap_low), "sqrt(2) - 1"],
        "uncovered_width": float(Fraction(math.sqrt(2) - 1) - gap_low),
    }
    if not any("(c)" in p for p in d2["problems"]):
        failures.append("short-net not refused by (c)")

    # 3. the core left undilated, on Hosono's net
    m3 = copy.deepcopy(data)
    m3["B"] = base["B"]
    m3["proof_net"] = {"step": "83/40000", "last": 200}
    d3 = dm_premises.decide(m3, base)
    cert3 = dmlib.certificate(m3)
    images3 = dmlib.expand(cert3)
    fm3 = dmlib.FloatMeasure.of(cert3, images3)
    best = None
    for k in (0, 92, 99):
        _, high = dmlib.domain(cert3, k)
        lo = math.nextafter(float(cert3.side / 2), math.inf)
        hi = float(high)
        if Fraction(hi) > high:
            hi = math.nextafter(hi, -math.inf)
        found = dm_sample.search(fm3, k, lo, hi)["refined"][0]
        if best is None or found[0] < best[0]:
            best = (found[0], k, found[1], found[2])
    w3 = coverage_witness(m3, best[1], (best[2], best[3]))
    results["core-not-dilated"] = {"premises": d3["status"], "problems": d3["problems"], "witness": w3}
    if d3["status"] != "PREMISES_HOLD" or not (w3["below_1"] and w3["in_domain"]):
        failures.append("core-not-dilated not refused on coverage")

    # 4. masses scaled, at the least capture this review's search found
    lowest = sample["B_lowest_exact_capture_found"]
    f_star = Fraction(lowest["exact"])
    pose = (lowest["pose"][0], lowest["pose"][1])
    tight = Fraction(math.floor(Fraction(10**9) / f_star), 10**9)
    for name, factor in (("mass-99/100", Fraction(99, 100)), ("mass-tight", tight)):
        mutant = scaled(data, factor)
        decided = dm_premises.decide(mutant, base)
        witness = coverage_witness(mutant, int(lowest["r"]), pose)
        results[name] = {"factor": str(factor), "premises": decided["status"], "mass": decided["file"]["mass"], "witness": witness}
        if decided["status"] != "PREMISES_HOLD" or not (witness["below_1"] and witness["in_domain"]):
            failures.append(f"{name} not refused on coverage")
    results["least_capture_found_F*"] = {"r": lowest["r"], "pose": list(pose), "value": float(f_star)}

    report = {
        "program": "dm_mutants.py",
        "program_sha256": dmlib.sha256_file(Path(__file__)),
        "dmlib_sha256": dmlib.sha256_file(Path(dmlib.__file__)),
        "dm_premises_sha256": dmlib.sha256_file(Path(dm_premises.__file__)),
        "dm_sample_sha256": dmlib.sha256_file(Path(dm_sample.__file__)),
        "sample_receipt_sha256": dmlib.sha256_file(sample_path),
        "mutants": results,
        "failures": failures,
        "status": "EVERY_MUTANT_REFUSED" if not failures else "A_MUTANT_PASSED",
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    out_path.write_text(dmlib.dumps(report) + "\n")
    print(json.dumps({"status": report["status"], "failures": failures, "cpu_seconds": report["cpu_seconds"]}, indent=1))


if __name__ == "__main__":
    main()
