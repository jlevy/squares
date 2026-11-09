"""Controls for lane L64, decided by the frozen checker against controls-plan.json.

Usage: python -I -B l64_controls.py PLAN.json CERT.yaml N CHECK.json SCRATCH_DIR OUT.json

The plan states every control and its expected outcome; it was written and hashed
before this program existed. Each control is built here from the certificate's exact
corners and decided by `l64_check.decide` (both methods, the whole file) unless the plan
says pair-level or square-level, where both methods decide the pair or the square.
Exact contacts use the contact parameter of the Minkowski difference along a direction
(`l64_selftest.contact_lambda`, which the self-test validated on 3,000 random pairs)
and the exact contact factor of an enlargement, derived below.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import l64_clip as B  # noqa: E402
import l64_sat as A  # noqa: E402
from l64_check import CHECKER, decide  # noqa: E402
from l64_reader import ReadError, read_witness  # noqa: E402
from l64_selftest import contact_lambda  # noqa: E402
from l64_util import (  # noqa: E402
    Clock,
    ceil_places,
    environment,
    floor_places,
    frac_str,
    program_digests,
    sci,
    sha256_file,
    write_receipt,
)

HERE = Path(__file__).resolve().parent
EPS = F(1, 10**30)
NEAR = F(1, 10**12)


def pts_of(sq: dict) -> list[tuple[F, F]]:
    return [(F(c[0], c[1]), F(c[2], c[3])) for c in sq["corners"]]


def entry(sid: int, pts: list[tuple[F, F]]) -> dict:
    return {"id": sid, "corners": [(x.numerator, x.denominator, y.numerator, y.denominator) for x, y in pts]}


def moved(pts: list[tuple[F, F]], dx: F, dy: F) -> list[tuple[F, F]]:
    return [(x + dx, y + dy) for x, y in pts]


def centre(pts: list[tuple[F, F]]) -> tuple[F, F]:
    return (pts[0][0] + pts[2][0]) / 2, (pts[0][1] + pts[2][1]) / 2


def scaled(pts: list[tuple[F, F]], k: F) -> list[tuple[F, F]]:
    cx, cy = centre(pts)
    return [(cx + k * (x - cx), cy + k * (y - cy)) for x, y in pts]


def summary(res: dict) -> dict:
    return {
        "verdict": res["verdict"],
        "shape_refusals": [r["square"] for r in res["shape_refusals"]],
        "not_squares": res["not_squares"],
        "outside": [o["square"] for o in res["walls"]["outside"]],
        "overlapping_pairs": len(res["pairs"]["overlapping"]),
        "overlapping_first": res["pairs"]["overlapping"][:3],
        "classes": res["pairs"]["classes"],
        "disagreements_A_B": len(res["disagreements_A_B"]),
    }


def pair_both(p: list[tuple[F, F]], q: list[tuple[F, F]], unit: bool = True) -> tuple[str, F, str, str]:
    a1, a2 = A.SquareA(1, entry(1, p)["corners"], unit), A.SquareA(2, entry(2, q)["corners"], unit)
    m, _ = A.pair_margin(a1, a2)
    b1, b2 = B.SquareB(1, entry(1, p)["corners"], unit), B.SquareB(2, entry(2, q)["corners"], unit)
    cb, area = B.pair_class(b1, b2)
    return A.classify(m), m, cb, str(area)


def axis_from_to(pi: list[tuple[F, F]], pj: list[tuple[F, F]]) -> tuple[F, tuple[F, F]]:
    """The pair's margin and its separating axis, oriented from square i toward square j."""
    ai, aj = A.SquareA(1, entry(1, pi)["corners"]), A.SquareA(2, entry(2, pj)["corners"])
    m, k = A.pair_margin(ai, aj)
    d = (ai.u, ai.w, aj.u, aj.w)[k]
    ci, cj = centre(pi), centre(pj)
    if (cj[0] - ci[0]) * d[0] + (cj[1] - ci[1]) * d[1] < 0:
        d = (-d[0], -d[1])
    return m, d


def closing(pi: list[tuple[F, F]], pj: list[tuple[F, F]], extra: F) -> tuple[list[tuple[F, F]], F]:
    """Square j moved toward i along their separating axis to contact, plus `extra`."""
    _, d = axis_from_to(pi, pj)
    lam = contact_lambda(pi, pj, d) + extra
    return moved(pj, -lam * d[0], -lam * d[1]), lam


def enlargement_factor(pi: list[tuple[F, F]], pj: list[tuple[F, F]]) -> F:
    """The exact factor k* about j's centre at which square j first touches square i.

    For each of the eight edge directions a of the two squares, j scaled by k keeps its
    axes, so its gap to i along a is (a.c_j - k r_a) - M_a, with r_a = a.c_j - min a.y over
    j and M_a = max a.x over i. The pair is apart while some gap is positive, so it first
    touches at k* = max over a of (a.c_j - M_a) / r_a.
    """
    cj = centre(pj)
    axes = []
    for pts in (pi, pj):
        ux, uy = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        axes += [(ux, uy), (-uy, ux), (-ux, -uy), (uy, -ux)]
    best: F | None = None
    for ax in axes:
        acj = ax[0] * cj[0] + ax[1] * cj[1]
        r = acj - min(ax[0] * x + ax[1] * y for x, y in pj)
        mi = max(ax[0] * x + ax[1] * y for x, y in pi)
        k = (acj - mi) / r
        if best is None or k > best:
            best = k
    assert best is not None
    return best


def main(argv: list[str]) -> int:  # noqa: C901, PLR0915 - one control after another
    if len(argv) != 7:
        print(__doc__)
        return 2
    plan_path, cert, n_text, check_path, scratch, out = argv[1:]
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
    far = [ids[k] for k in range(n) if max(x for x, _ in pts[k]) == side or max(y for _, y in pts[k]) == side]
    left = [ids[k] for k in range(n) if min(x for x, _ in pts[k]) == 0]
    bottom = [ids[k] for k in range(n) if min(y for _, y in pts[k]) == 0]
    results: list[dict] = []

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

    def full(cid: str, squares: list[dict], at_side: F, ok_detail) -> None:  # noqa: ANN001
        res = decide(squares, at_side, nearest=3)
        s = summary(res)
        record(cid, res["verdict"], bool(ok_detail(s)) and s["disagreements_A_B"] == 0, decision=s)

    def with_square(k: int, new_pts: list[tuple[F, F]]) -> list[dict]:
        out_sqs = list(sqs)
        out_sqs[k] = entry(ids[k], new_pts)
        return out_sqs

    # G1: the last square replaced by a copy of the first.
    g1 = list(sqs)
    g1[-1] = {"id": ids[-1], "corners": sqs[0]["corners"]}
    full("G1", g1, side, lambda s: any(o["pair"] == [ids[0], ids[-1]] and o["margin_A"] == "-1" and o["area_B"] == "1" for o in s["overlapping_first"]))
    # G2: square 1 translated by (S, 0).
    full("G2", with_square(0, moved(pts[0], side, F(0))), side, lambda s: ids[0] in s["outside"])
    # G3 and G4: the reader on edited files.
    text = Path(cert).read_text(encoding="ascii")
    last_marker = f"\n  - id: {ids[-1]}\n"
    claim_marker = "\n  claim:\n"
    a, b = text.rindex(last_marker), text.index(claim_marker)
    for cid, edited in (
        ("G3", text[:a] + text[b:]),
        ("G4", text[:a] + "\n  - id: 1\n" + text[a + len(last_marker) :]),
    ):
        path = Path(scratch) / f"{cid}-n{n}.yaml"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(edited, encoding="ascii")
        try:
            read_witness(path, expected_n=n)
            record(cid, "READ_ACCEPTED", False)
        except ReadError as exc:
            record(cid, "READ_REFUSED", True, reason=str(exc)[:120], edited_sha256=sha256_file(path))
        path.unlink()
    # G5: square 1's third corner moved by 1e-30 in x.
    p5 = list(pts[0])
    p5[2] = (p5[2][0] + EPS, p5[2][1])
    full("G5", with_square(0, p5), side, lambda s: ids[0] in s["not_squares"])
    # G6: every square reflected in the horizontal line through its centre.
    g6 = []
    for k in range(n):
        cy = centre(pts[k])[1]
        g6.append(entry(ids[k], [(x, 2 * cy - y) for x, y in pts[k]]))
    full("G6", g6, side, lambda s: s["overlapping_pairs"] >= 1)
    # S1: the side.
    unit_last = F(1, side.denominator)
    full("S1a", sqs, side - unit_last, lambda s: s["outside"] == far)
    full("S1b", sqs, side - EPS, lambda s: s["outside"] == far)
    full("S1c", sqs, floor_places(side, 12), lambda s: set(far) <= set(s["outside"]))
    full("S1d", sqs, ceil_places(side, 12), lambda s: not s["outside"])
    # S3: the near walls.
    full("S3a", [entry(ids[k], moved(pts[k], -EPS, F(0))) for k in range(n)], side, lambda s: s["outside"] == left)
    full("S3b", [entry(ids[k], moved(pts[k], F(0), -EPS)) for k in range(n)], side, lambda s: s["outside"] == bottom)
    # S4: the least-margin pair closed along its separating axis.
    for cid, extra, want in (("S4c", F(0), "touching"), ("S4p", EPS, "overlapping")):
        pj2, lam = closing(pts[i], pts[j], extra)
        ca, m, cb, area = pair_both(pts[i], pj2)
        res = decide(with_square(j, pj2), side, nearest=3)
        s = summary(res)
        record(
            cid,
            res["verdict"],
            ca == want and cb == want and (m == 0 if want == "touching" else m < 0) and s["disagreements_A_B"] == 0,
            pair=[i_id, j_id],
            moved_by=sci(lam, 12),
            pair_A=ca,
            pair_margin_A=sci(m, 6) if m else "0",
            pair_B=cb,
            pair_area_B=area if len(area) < 80 else sci(F(area), 6),
            decision=s,
        )
    # S5: every pair below 1e-12, each alone, closed the same way.
    near: list[tuple[int, int]] = []
    sa = [A.SquareA(ids[k], sqs[k]["corners"]) for k in range(n)]
    for a_ in range(n):
        for b_ in range(a_ + 1, n):
            if A.pair_margin(sa[a_], sa[b_])[0] < NEAR:
                near.append((a_, b_))
    misses5 = []
    for a_, b_ in near:
        for extra, want in ((F(0), "touching"), (EPS, "overlapping")):
            pj2, _ = closing(pts[a_], pts[b_], extra)
            ca, m, cb, _ = pair_both(pts[a_], pj2)
            if not (ca == want and cb == want and (m == 0 if want == "touching" else m < 0)):
                misses5.append({"pair": [ids[a_], ids[b_]], "extra": str(extra), "A": ca, "B": cb})
    record("S5", "ALL_AS_STATED" if not misses5 else "MISSES", not misses5, pairs=len(near), misses=misses5[:10])
    # S6: every square alone moved toward its nearest wall by its least clearance.
    misses6 = []
    side_q = B.mpq(side.numerator, side.denominator)
    for k in range(n):
        cl = A.wall_clearances(sa[k], side)
        wall = min(cl, key=lambda key: cl[key])
        v = cl[wall]
        step = {"left": (-1, 0), "bottom": (0, -1), "right": (1, 0), "top": (0, 1)}[wall]
        for extra, inside in ((F(0), True), (EPS, False)):
            t = v + extra
            p6 = moved(pts[k], t * step[0], t * step[1])
            a6 = A.SquareA(ids[k], entry(ids[k], p6)["corners"])
            m6 = min(A.wall_clearances(a6, side).values())
            ok_b, _ = B.contained(B.SquareB(ids[k], entry(ids[k], p6)["corners"]), side_q)
            good = (m6 == 0 and ok_b) if inside else (m6 < 0 and not ok_b)
            if not good:
                misses6.append({"square": ids[k], "wall": wall, "extra": str(extra)})
    record("S6", "ALL_AS_STATED" if not misses6 else "MISSES", not misses6, squares=n, misses=misses6[:10])
    # S7: square j enlarged to touch i, then past.
    kstar = enlargement_factor(pts[i], pts[j])
    for cid, extra, want in (("S7c", F(0), "touching"), ("S7p", EPS, "overlapping")):
        pj2 = scaled(pts[j], kstar + extra)
        ca, m, cb, _ = pair_both(pts[i], pj2, unit=False)
        res = decide(with_square(j, pj2), side, nearest=3)
        s = summary(res)
        record(
            cid,
            res["verdict"],
            ca == want and cb == want and j_id in s["shape_refusals"] and s["disagreements_A_B"] == 0,
            pair=[i_id, j_id],
            factor_minus_one=sci(kstar + extra - 1, 12),
            pair_A=ca,
            pair_B=cb,
            decision=s,
        )
    # S8: the far-wall square enlarged by 1 + 1e-30.
    kf = ids.index(far[0])
    full("S8", with_square(kf, scaled(pts[kf], 1 + EPS)), side, lambda s: far[0] in s["shape_refusals"] and far[0] in s["outside"])

    misses = [r["id"] for r in results if not r["as_expected"]]
    receipt = {
        "program": "l64_controls.py",
        "programs_sha256": program_digests([HERE / f for f in [*CHECKER, "l64_selftest.py", "l64_controls.py"]]),
        "plan_sha256": sha256_file(plan_path),
        "environment": environment(),
        "certificate": cert,
        "certificate_sha256": w["sha256"],
        "n": n,
        "side": frac_str(side),
        "least_margin_pair": [i_id, j_id],
        "far_wall_square": far,
        "left_wall_square": left,
        "bottom_wall_square": bottom,
        "controls": results,
        "verdict": "EVERY_CONTROL_AS_EXPECTED" if not misses else "MISSES",
        "misses": misses,
        "clock": clock.report(),
    }
    write_receipt(out, receipt)
    print(f"n={n}: {receipt['verdict']} {misses}; cpu {receipt['clock']['cpu_seconds']} s")
    for r in results:
        print(f"  {r['id']:4s} expect {r['expect']:14s} observed {r['observed']:14s} {'ok' if r['as_expected'] else 'MISS'}")
    return 0 if not misses else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
