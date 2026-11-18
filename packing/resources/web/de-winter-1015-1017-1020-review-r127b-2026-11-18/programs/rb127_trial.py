"""A priced trial of lane r127b-1118's programs on synthetic packings only.

Usage: ``python -I -B rb127_trial.py WORKDIR OUT.json``

It reads no certificate. It builds a synthetic packing of 127 squares, 117 upright and
10 turned by small rational angles, with scalars of 60 to 140 digits like the
certificates', writes it in de Winter's two layouts and in the house certificate's
layout (integer ids, a claim, source and certificate block after the squares), and an
issue response in the style of the three issues. It then runs the check, the controls
and the measurement on them, as the real runs will, and prices each run in CPU seconds.

Last, it runs the controls on a smaller synthetic packing under three broken copies of
the programs, each of which must make at least one control come out other than stated.
"""

from __future__ import annotations

import json
import random
import subprocess
import sys
import time
from fractions import Fraction as Fr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rb127_axes as A  # noqa: E402
import rb127_clip as B  # noqa: E402
import rb127_contract as K  # noqa: E402
import rb127_controls as CT  # noqa: E402
import rb127_decide as D  # noqa: E402
import rb127_fmt as F  # noqa: E402
import rb127_twin as T  # noqa: E402
import rb127_write as W  # noqa: E402

HERE = Path(__file__).resolve().parent


def pq(f: Fr) -> tuple[int, int]:
    return f.numerator, f.denominator


def synthetic(count: int, cols: int, gap: Fr, rng: random.Random, turned: int) -> tuple[list, tuple[int, int]]:
    rows = []
    cell = 1 + gap
    tilt_cells = set(rng.sample(range(count), turned))
    for k in range(count):
        i, j = k % cols, k // cols
        jitter_x = Fr(rng.randint(-10**30, 10**30), 10**34 * 7) * gap
        jitter_y = Fr(rng.randint(-10**30, 10**30), 10**34 * 3) * gap
        cx = Fr(1, 2) + gap + i * cell + jitter_x
        cy = Fr(1, 2) + gap + j * cell + jitter_y
        if k in tilt_cells:
            p = rng.randint(1, 10**30)
            q = 10**34 + rng.randint(1, 10**33)
            a, b, r = q * q - p * p, 2 * p * q, q * q + p * p
            row = (pq(cx), pq(cy), pq(Fr(a, r)), pq(Fr(b, r)))
        else:
            row = (pq(cx), pq(cy), (1, 1), (0, 1))
        rows.append(row)
    rows_ip = [A.to_ipose(*r) for r in rows]
    top = max(max(A.centre(p)[0] + A.half_extent(p), A.centre(p)[1] + A.half_extent(p)) for p in rows_ip)
    side = top + gap + Fr(1, 10**40) * 3
    return rows, pq(side)


def house_layout(n: int, side: tuple[int, int], corners: list) -> bytes:
    text = W.form_c(n, side, corners, id_style="integer").decode()
    head, _, squares = text.partition("  claim:\n")
    claim_block, _, rest = squares.partition("  squares:\n")
    tail = ("  claim:\n" + claim_block + "  source:\n    path: synthetic-pose.yaml\n  certificate:\n"
            "    kind: exact-rational-sat\n    center_dilation: '1'\n")
    return (head + "  squares:\n" + rest + tail).encode()


def issue_json(number: int, side: Fr, close_pairs: int, pin: str) -> dict:
    print12 = F.ceil_places(side, 12)
    body = (f"**Claim.** A packing of 127 unit squares in a square of side {print12} (rounded up at 12 places). "
            f"The case page lists 11.8017538904864874 (T-305, synthetic) on 17 November 2026. The gain is 0.00096.\n\n"
            f"**Certificate.** in the folder `n127` at commit {pin}.\n\n"
            f"It reports 127 squares and {close_pairs} close pairs.\n")
    return {"number": number, "title": f"Synthetic (side {print12})", "body": body, "created_at": "x", "updated_at": "x",
            "user": {"login": "synthetic"}, "comments": 0}


def run(cmd: list[str]) -> tuple[int, float, str]:
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, round(time.time() - t0, 1), (p.stdout + p.stderr).strip()[-400:]


def child_cpu() -> float:
    import resource
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime


def mutant_controls(work: Path, rng: random.Random) -> list[dict]:
    rows, side = synthetic(20, 5, Fr(1, 1000), rng, 4)
    jb = W.form_j(20, side, rows)
    cb = W.form_c(20, side, [T.corners_pq(r) for r in rows])
    claim = F.ceil_places(Fr(side[0], side[1]), 12)
    out = []

    def go(name: str, patch, undo) -> None:
        patch()
        try:
            res = CT.Runner("mutant", "pair", jb, cb, claim).run()
            bad = res["not_as_stated"]
        except Exception as exc:
            bad = [f"raised {type(exc).__name__}"]
        finally:
            undo()
        out.append({"mutant": name, "controls_not_as_stated": bad, "caught": bool(bad)})

    intact = CT.Runner("intact", "pair", jb, cb, claim).run()
    out.append({"mutant": "none (the intact programs)", "controls_not_as_stated": intact["not_as_stated"],
                "caught": False, "controls": intact["controls"]})
    orig_side = B._side
    go("method B clipping with open half-planes",
       lambda: setattr(B, "_side", lambda p, q, x: (lambda v: v if v != 0 else -1)(orig_side(p, q, x))),
       lambda: setattr(B, "_side", orig_side))
    saved = dict(D.A_PAIR)
    go("method A counting a zero margin as overlap", lambda: D.A_PAIR.__setitem__(0, "overlap"),
       lambda: (D.A_PAIR.clear(), D.A_PAIR.update(saved)))
    orig_contraction = K.contraction

    def broken(rows_, side_):
        res = orig_contraction(rows_, side_)
        res["_lam"] = res["_lam"] * (1 + Fr(1, 10**30))
        return res
    go("the contraction's first contact moved by a factor 1 + 1e-30", lambda: setattr(K, "contraction", broken),
       lambda: setattr(K, "contraction", orig_contraction))
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    work = Path(argv[1])
    work.mkdir(parents=True, exist_ok=True)
    rng = random.Random(1271118)
    t0 = time.process_time()
    rows, side = synthetic(127, 12, Fr(1, 1000), rng, 10)
    corners = [T.corners_pq(r) for r in rows]
    (work / "n127").mkdir(exist_ok=True)
    (work / "n127" / "n127_exact.json").write_bytes(W.form_j(127, side, rows))
    (work / "n127" / "n127_witness.yaml").write_bytes(W.form_c(127, side, corners))
    (work / "house.yaml").write_bytes(house_layout(127, side, corners))
    (work / "house-cb.yaml").write_text("not read\n")
    S = Fr(side[0], side[1])
    pts = [(Fr(*r[0]), Fr(*r[1])) for r in rows]
    close = sum(1 for i in range(127) for j in range(i + 1, 127)
                if (pts[j][0] - pts[i][0]) ** 2 + (pts[j][1] - pts[i][1]) ** 2 < 2)
    pin = "0" * 40
    (work / "issue.json").write_text(json.dumps(issue_json(9999, S, close, pin)))
    prepared = time.process_time() - t0
    py = [sys.executable, "-I", "-B"]
    jobs = []
    c0 = child_cpu()
    for name, cmd in (
        ("check pair", py + [str(HERE / "rb127_check.py"), "pair", "synthetic", pin, str(work / "n127/n127_exact.json"),
                             str(work / "n127/n127_witness.yaml"), str(work / "issue.json"), str(work / "check.json")]),
        ("check house", py + [str(HERE / "rb127_check.py"), "house", "synthetic-house", str(work / "house.yaml"),
                              str(work / "house-cb.yaml"), str(work / "check-house.json")]),
        ("controls pair", py + [str(HERE / "rb127_controls.py"), "pair", "synthetic", str(work / "n127/n127_exact.json"),
                                str(work / "n127/n127_witness.yaml"), str(HERE / "controls-plan.json"),
                                F.ceil_places(S, 12), str(work / "controls.json")]),
        ("controls house", py + [str(HERE / "rb127_controls.py"), "house", "synthetic-house", str(work / "house.yaml"),
                                 str(HERE / "controls-plan.json"), F.ceil_places(S, 12), str(work / "controls-house.json")]),
        ("measure", py + [str(HERE / "rb127_measure.py"), str(work / "house.yaml")] + [str(work / "n127/n127_exact.json")] * 3
         + [str(work / "issue.json")] * 3 + [str(work / "measure.json")]),
    ):
        code, wall, tail = run(cmd)
        c1 = child_cpu()
        jobs.append({"job": name, "exit": code, "wall_seconds": wall, "cpu_seconds": round(c1 - c0, 1), "tail": tail})
        c0 = c1
    mutants = mutant_controls(work, rng)
    out = {
        "program": "rb127_trial.py",
        "synthetic": {"squares": 127, "turned": 10, "side_sci": F.sci(S, 12),
                      "largest_scalar_digits": max(len(str(v[1])) for r in rows for v in r)},
        "prepare_cpu_seconds": round(prepared, 1),
        "jobs": jobs,
        "controls_under_broken_copies": mutants,
        "every_broken_copy_caught": all(m["caught"] for m in mutants[1:]) and not mutants[0]["controls_not_as_stated"],
        "cpu_seconds_total": round(time.process_time() - t0 + sum(j["cpu_seconds"] for j in jobs), 1),
    }
    Path(argv[2]).write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    for j in jobs:
        print(j["job"], "exit", j["exit"], "cpu", j["cpu_seconds"], "s;", j["tail"][-160:])
    print("broken copies caught:", out["every_broken_copy_caught"], [m["controls_not_as_stated"][:4] for m in mutants])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
