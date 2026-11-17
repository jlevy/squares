"""The addendum's controls for lane L64: pairs closed along their centre lines.

Usage: python -I -B l64_controls_centre.py ADDENDUM.json CERT.yaml N CHECK.json OUT.json

controls-plan-addendum.json states these controls and their expected outcomes; it was
written and hashed after the first controls run at 232 and before this program existed.
That run's S5 closed near pairs along their separating axes, and some stayed separated
by both methods, because a line along one edge normal can pass beside the other square.
Here each pair is closed along its centre line c_j - c_i, which meets the pair (at
parameter 1 the centres coincide), and the S5 misses are diagnosed: a pair's
separating-axis line meets the pair exactly when the parameters of overlap along it,
max over edge directions a with a.d > 0 of -H(a)/(a.d) up to min over a.d < 0 of the
same, form a non-empty interval and every direction with a.d = 0 has H(a) > 0, where
H(a) is the support of square i along a less the least projection of square j on it.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l64_sat as A  # noqa: E402
from l64_check import CHECKER, decide  # noqa: E402
from l64_controls import axis_from_to, centre, closing, entry, moved, pair_both, pts_of, summary  # noqa: E402
from l64_reader import read_witness  # noqa: E402
from l64_selftest import contact_lambda  # noqa: E402
from l64_util import Clock, environment, frac_str, program_digests, sci, sha256_file, write_receipt  # noqa: E402

HERE = Path(__file__).resolve().parent
EPS = F(1, 10**30)
NEAR = F(1, 10**12)


def centre_closing(pi: list, pj: list, extra: F) -> tuple[list, F]:
    ci, cj = centre(pi), centre(pj)
    v = (cj[0] - ci[0], cj[1] - ci[1])
    lam = contact_lambda(pi, pj, v) + extra
    return moved(pj, -lam * v[0], -lam * v[1]), lam


def axis_line_meets(pi: list, pj: list) -> bool:
    _, d = axis_from_to(pi, pj)
    axes = []
    for pts in (pi, pj):
        ux, uy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        axes += [(ux, uy), (-uy, ux), (-ux, -uy), (uy, -ux)]
    low: F | None = None
    high: F | None = None
    for ax in axes:
        k = ax[0] * d[0] + ax[1] * d[1]
        h = max(ax[0] * x + ax[1] * y for x, y in pi) - min(ax[0] * x + ax[1] * y for x, y in pj)
        if k > 0:
            low = -h / k if low is None else max(low, -h / k)
        elif k < 0:
            high = -h / k if high is None else min(high, -h / k)
        elif h <= 0:
            return False
    return low is not None and high is not None and low < high


def main(argv: list[str]) -> int:
    if len(argv) != 6:
        print(__doc__)
        return 2
    plan_path, cert, n_text, check_path, out = argv[1:]
    clock = Clock()
    plan = {c["id"]: c for c in json.loads(Path(plan_path).read_text())["controls"]}
    n = int(n_text)
    w = read_witness(cert, expected_n=n)
    side = F(*w["side"])
    sqs = w["squares"]
    ids = [s["id"] for s in sqs]
    pts = [pts_of(s) for s in sqs]
    check = json.loads(Path(check_path).read_text())
    i_id, j_id = check["decision"]["pairs"]["least_margin_pair"]
    i, j = ids.index(i_id), ids.index(j_id)
    results = []

    def record(cid: str, observed: str, ok: bool, **detail: object) -> None:
        results.append(
            {
                "id": cid,
                "what": plan[cid]["what"],
                "expect": plan[cid]["expect"],
                "expect_detail": plan[cid]["detail"],
                "observed": observed,
                "as_expected": ok and observed == plan[cid]["expect"],
                **detail,
            }
        )

    for cid, extra, want in (("S4'c", F(0), "touching"), ("S4'p", EPS, "overlapping")):
        pj2, lam = centre_closing(pts[i], pts[j], extra)
        ca, m, cb, area = pair_both(pts[i], pj2)
        new = list(sqs)
        new[j] = entry(ids[j], pj2)
        res = decide(new, side, nearest=3)
        s = summary(res)
        record(
            cid,
            res["verdict"],
            ca == want and cb == want and (m == 0 if want == "touching" else m < 0) and s["disagreements_A_B"] == 0,
            pair=[i_id, j_id],
            parameter=sci(lam, 12),
            pair_A=ca,
            pair_margin_A=sci(m, 6) if m else "0",
            pair_B=cb,
            pair_area_B=area if len(area) < 80 else sci(F(area), 6),
            decision=s,
        )
    sa = [A.SquareA(ids[k], sqs[k]["corners"]) for k in range(n)]
    near = [(a, b) for a in range(n) for b in range(a + 1, n) if A.pair_margin(sa[a], sa[b])[0] < NEAR]
    misses = []
    axis_touch = 0
    meets = 0
    unexplained = []
    for a, b in near:
        for extra, want in ((F(0), "touching"), (EPS, "overlapping")):
            q, _ = centre_closing(pts[a], pts[b], extra)
            ca, m, cb, _ = pair_both(pts[a], q)
            if not (ca == want and cb == want and (m == 0 if want == "touching" else m < 0)):
                misses.append({"pair": [ids[a], ids[b]], "extra": str(extra), "A": ca, "B": cb})
        q0, _ = closing(pts[a], pts[b], F(0))
        q1, _ = closing(pts[a], pts[b], EPS)
        c0 = pair_both(pts[a], q0)
        c1 = pair_both(pts[a], q1)
        touched = c0[0] == c0[2] == "touching" and c1[0] == c1[2] == "overlapping"
        line = axis_line_meets(pts[a], pts[b])
        axis_touch += touched
        meets += line
        if touched != line:
            unexplained.append({"pair": [ids[a], ids[b]], "axis_closing_touched": touched, "axis_line_meets": line})
    record("S5'", "ALL_AS_STATED" if not misses else "MISSES", not misses, pairs=len(near), misses=misses[:10])
    record(
        "S5-diagnosis",
        "MISSES_EXPLAINED" if not unexplained else "UNEXPLAINED",
        not unexplained,
        pairs=len(near),
        axis_closing_reached_contact=axis_touch,
        axis_line_meets_pair=meets,
        axis_line_misses_pair=len(near) - meets,
        unexplained=unexplained[:10],
    )
    bad = [r["id"] for r in results if not r["as_expected"]]
    receipt = {
        "program": "l64_controls_centre.py",
        "programs_sha256": program_digests(
            [HERE / f for f in [*CHECKER, "l64_selftest.py", "l64_controls.py", "l64_controls_centre.py"]]
        ),
        "plan_sha256": sha256_file(plan_path),
        "environment": environment(),
        "certificate": cert,
        "certificate_sha256": w["sha256"],
        "n": n,
        "side": frac_str(side),
        "least_margin_pair": [i_id, j_id],
        "controls": results,
        "verdict": "EVERY_CONTROL_AS_EXPECTED" if not bad else "MISSES",
        "misses": bad,
        "clock": clock.report(),
    }
    write_receipt(out, receipt)
    print(f"n={n}: {receipt['verdict']} {bad}; cpu {receipt['clock']['cpu_seconds']} s")
    for r in results:
        extra = {k: r[k] for k in ("pairs", "axis_line_misses_pair") if k in r}
        print(f"  {r['id']:12s} expect {r['expect']:16s} observed {r['observed']:16s} {'ok' if r['as_expected'] else 'MISS'} {extra}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
