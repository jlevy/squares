"""Hold the author's referee report's values to this review's own evaluator.

Usage: dm_compare.py CERTIFICATE.json.gz HOSONO.json.gz GRADE.json OUT.json

Written after this review's findings were committed, when `second-checker/GRADE.md` and
`GRADE.json` were first read; it reads GRADE.json as data and runs none of its code:

1. its least observed capture: dmlib's exact capture at its centre and direction must
   lie in the interval it states, at a centre in the per-bin domain;
2. its masses x 0.998 mutant: 0.998 times that capture against its stated floor;
3. its heaviest-orbit-removed mutant (r = 0) and its L = 9.975 mutant with B held at
   19884161/19900000 on the same net (r = 144): a binary64 search on each mutant at
   that direction (dm_sample.search), then an exact capture at the lowest pose found,
   which must lie below 1 and at or below the referee's witness value or near it.
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
import dm_mutants  # noqa: E402
import dm_sample  # noqa: E402
import dmlib  # noqa: E402


def searched_witness(data: dict, index: int) -> dict:
    cert = dmlib.certificate(data)
    fm = dmlib.FloatMeasure.of(cert, dmlib.expand(cert))
    _, high = dmlib.domain(cert, index)
    lo = float(cert.side / 2)
    if Fraction(lo) < cert.side / 2:
        lo = math.nextafter(lo, math.inf)
    hi = float(high)
    if Fraction(hi) > high:
        hi = math.nextafter(hi, -math.inf)
    value, x, y = dm_sample.search(fm, index, lo, hi)["refined"][0]
    return dm_mutants.coverage_witness(data, index, (x, y))


def main() -> None:
    cert_path, hosono_path, grade_path, out_path = (Path(a) for a in sys.argv[1:5])
    started = time.process_time()
    data = dmlib.read_gzip_json(cert_path).data
    base = dmlib.read_gzip_json(hosono_path).data
    grade = json.loads(grade_path.read_text())
    failures: list[str] = []
    cert = dmlib.certificate(data)
    exact = dmlib.ExactMeasure.of(cert, dmlib.expand(cert))

    # 1. the least observed capture
    index = int(grade["min_capture_direction"])
    cx, cy = (Fraction(v) for v in grade["min_capture_centre"])
    cap = dmlib.fraction_of(dmlib.capture_exact(exact, index, dmlib.q(cx), dmlib.q(cy))[0])
    low_s, high_s = (Fraction(v) for v in grade["min_capture_found_interval"])
    low, high = dmlib.domain(cert, index)
    least = {
        "r": index,
        "centre": [str(cx), str(cy)],
        "centre_float": [float(cx), float(cy)],
        "mine": str(cap),
        "mine_float": dmlib.short(cap, 17),
        "in_their_interval": low_s <= cap < high_s,
        "in_domain": low <= cx <= high and low <= cy <= high,
    }
    if not least["in_their_interval"]:
        failures.append("their least capture does not reproduce")

    # 2. masses x 0.998 at that centre
    floor = Fraction(grade["mutants"]["masses_times_0.998"]["capture_decimal_floor"])
    scaled = Fraction(998, 1000) * cap
    mass = {"mine": dmlib.short(scaled, 17), "their_floor": str(floor), "agrees": floor <= scaled < floor + Fraction(1, 10**15), "below_1": scaled < 1}
    if not mass["agrees"]:
        failures.append("their 0.998 mutant does not reproduce")

    # 3a. heaviest orbit removed, at r = 0
    heavy = copy.deepcopy(data)
    masses = [dmlib.rational(row["mass"]) for row in heavy["rectangles"]]
    drop = max(range(len(masses)), key=masses.__getitem__)
    del heavy["rectangles"][drop]
    heavy["total_mass"] = str(sum(masses) - masses[drop])
    w3a = searched_witness(heavy, 0)
    their = Fraction(grade["mutants"]["heaviest_orbit_removed"]["capture_decimal_floor"])
    w3a.update({"dropped_row": drop, "dropped_mass": str(masses[drop]), "their_floor": str(their), "at_or_below_theirs": Fraction(w3a["exact_capture"]) < their + Fraction(1, 10**15)})
    if not w3a["below_1"]:
        failures.append("heaviest-orbit mutant not refused here")

    # 3b. L = 9.975 with B held, on the same net, at r = 144
    wide = copy.deepcopy(base)
    lam = Fraction(399, 40) / dmlib.rational(base["L"])
    wide["L"] = "399/40"
    wide["B"] = data["B"]
    wide["proof_net"] = dict(data["proof_net"])
    for row in wide["rectangles"]:
        row["rectangle"] = [str(dmlib.rational(v) * lam) for v in row["rectangle"]]
    wide.pop("scaling_factor", None)
    wide.pop("scaling_source_digest", None)
    w3b = searched_witness(wide, 144)
    their = Fraction(grade["mutants"]["L_9.975_fixed_B"]["capture_decimal_floor"])
    w3b.update({"lambda": str(lam), "their_floor": str(their), "at_or_below_theirs": Fraction(w3b["exact_capture"]) < their + Fraction(1, 10**15)})
    if not w3b["below_1"]:
        failures.append("L = 9.975 mutant not refused here")

    report = {
        "program": "dm_compare.py",
        "program_sha256": dmlib.sha256_file(Path(__file__)),
        "dmlib_sha256": dmlib.sha256_file(Path(dmlib.__file__)),
        "dm_sample_sha256": dmlib.sha256_file(Path(dm_sample.__file__)),
        "dm_mutants_sha256": dmlib.sha256_file(Path(dm_mutants.__file__)),
        "grade_json_sha256": dmlib.sha256_file(grade_path),
        "their_least_capture": least,
        "their_masses_0.998": mass,
        "their_heaviest_orbit_removed": w3a,
        "their_L_9.975_fixed_B": w3b,
        "failures": failures,
        "status": "REFEREE_VALUES_HOLD" if not failures else "REFEREE_VALUES_DIFFER",
        "cpu_seconds": round(time.process_time() - started, 1),
    }
    out_path.write_text(dmlib.dumps(report) + "\n")
    print(dmlib.dumps({k: report[k] for k in ("status", "failures", "their_least_capture", "their_masses_0.998", "cpu_seconds")}))


if __name__ == "__main__":
    main()
