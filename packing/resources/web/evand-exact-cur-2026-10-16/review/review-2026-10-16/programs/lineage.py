"""Which packing each T-193 exact form is, pose by pose: a credit measurement that decides nothing.

For each of T-193's sixteen counts, the exact form's configuration (as
``claims_and_credit.poses`` evaluates it) is paired with each candidate packing the record
credits at the count, with ``devtools.check_half_angle_area``'s ``arrangement_gap`` and
``unmoved``: the case's house and the entries its ledger chain names (T-174, T-186 and
their sources), each read by that route's own reader (``CREDITED_READERS``) or, for
T-174 and T-186, from the derived facts their packets keep.

Run from ``packing/`` with the project interpreter, ``python -I``; prints JSON lines.
"""

import gzip
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from claims_and_credit import FACTS, PACKET, poses  # noqa: E402
from devtools import check_half_angle_area as area  # noqa: E402

CANDIDATES = {
    88: ("T-127", "T-174", "T-146"),
    102: ("T-146", "T-174", "T-125"),
    123: ("T-146", "T-174", "T-125"),
    126: ("T-139", "T-174", "T-125"),
    175: ("T-158", "T-186", "T-174"),
    199: ("T-127", "T-174", "T-146"),
    204: ("T-162", "T-186", "T-174"),
    232: ("T-158", "T-186", "T-174"),
    258: ("T-146", "T-174", "T-115"),
    259: ("T-136", "T-174"),
    266: ("T-119", "T-174"),
    267: ("T-134", "T-174"),
    292: ("T-146", "T-174"),
    295: ("T-146", "T-174", "T-125"),
    301: ("T-098", "T-174"),
    302: ("T-181", "T-186", "T-164"),
}


def load(tid, n):
    if tid in FACTS:
        text = gzip.decompress((FACTS[tid] / f"n-{n:03d}.yaml.gz").read_bytes()).decode("utf-8")
        try:
            return area.read_fact(text, n)
        except area.AreaRouteError:
            return area.read_fact(text, n, labelled=True)
    return area.CREDITED_READERS[tid](n)


def main():
    pinned = Path(sys.argv[1])
    counts = [int(a) for a in sys.argv[2:]] or list(CANDIDATES)
    for n in counts:
        path = PACKET / f"n-{n}.minpoly.json.gz"
        if not path.is_file():
            path = pinned / f"n-{n}.minpoly.json.gz"
        data = json.loads(gzip.decompress(path.read_bytes()).decode("utf-8"))
        mine = poses(data)
        for tid in CANDIDATES[n]:
            row = {"n": n, "against": tid}
            try:
                other = load(tid, n)
            except Exception as exc:  # a reader without this count
                row["unreadable"] = f"{type(exc).__name__}: {str(exc)[:120]}"
                print(json.dumps(row), flush=True)
                continue
            kept = area.unmoved(mine, other)
            row["unmoved"] = {"symmetry": kept["symmetry"], "within": kept["within"], "one_to_one": kept["one_to_one"]}
            try:
                gap = area.arrangement_gap(mine, other)
                row["gap"] = {
                    "symmetry": gap["symmetry"],
                    "largest_displacement": str(gap["largest_displacement"])[:12],
                    "largest_orientation_sine": gap["largest_orientation_sine"],
                    "moved_beyond": gap["moved_beyond"],
                    "turned_beyond_1e-6": gap["turned_beyond_1e-6"],
                }
            except area.AreaRouteError as exc:
                row["gap"] = {"none": str(exc)}
            print(json.dumps(row), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
