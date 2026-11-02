"""An independent check of the 108 predicates of cases/asymptotic/quarter_cube_constants.py.

The maintained checker (written for the 8 October review) decides 108 predicates
about the quarter-power (Q) and cube-root (C) preprints with mpmath intervals. This
program reads that file as data, without importing or running it. It parses its input
rows (QUARTER_ROWS, CUBE_ROWS, GEOMETRIC) with `ast`, holds them to this review's own
transcription of the primaries, and decides every one of the 108 predicates again with
the exact-rational intervals of iv.py and the formulas of qmodel.py and c_constants.py,
written from the primaries before the maintained file was opened. Each predicate keeps
the maintained checker's name, so the two lists can be compared line by line.

Usage: python -I qcc_predicates.py MAINTAINED_PY OUT.json
"""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python -I

from c_constants import CASES, VARIANTS, B1_of, L1_of, case_values
from iv import PI, Iv, cos, root, rpow, sqrt
from qmodel import BARS, BBAR, DELTA, PI_STAR, PI_STAR_13, A_exact, Ap_exact, Params, c_inf, model

F = Fraction


def literal(node: ast.AST) -> object:
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
        base, exp = literal(node.left), literal(node.right)
        if isinstance(base, int) and isinstance(exp, int):
            return base**exp
    raise ValueError(f"not a literal: {ast.dump(node)}")


def parse_inputs(path: Path) -> tuple[list[list[object]], list[list[object]], dict[int, tuple[str, ...]]]:
    tree = ast.parse(path.read_text())
    quarter: list[list[object]] = []
    cube: list[list[object]] = []
    geometric: dict[int, tuple[str, ...]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id == "QuarterRow":
                quarter.append([literal(a) for a in node.args])
            elif node.func.id == "CubeRow":
                cube.append([literal(a) for a in node.args])
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "GEOMETRIC" for t in node.targets):
            assert isinstance(node.value, ast.Dict)
            for k, v in zip(node.value.keys, node.value.values, strict=True):
                assert k is not None and isinstance(v, ast.Tuple)
                geometric[int(literal(k))] = tuple(str(literal(e)) for e in v.elts)  # type: ignore[arg-type]
    return quarter, cube, geometric


def tri(ok_lo: bool, ok_hi_false: bool) -> bool | None:
    return True if ok_lo else (False if ok_hi_false else None)


def lt(a: Iv, b: Iv) -> bool | None:
    return tri(a.hi < b.lo, a.lo >= b.hi)


def main(maintained: Path, out: Path) -> int:
    quarter, cube, geometric = parse_inputs(maintained)
    rows: list[dict[str, object]] = []

    def rec(name: str, verdict: bool | None, value: Iv | None = None, note: str = "") -> None:
        row: dict[str, object] = {"predicate": name, "verdict": verdict}
        if value is not None:
            row["enclosure"] = [float(value.lo), float(value.hi)]
        if note:
            row["note"] = note
        rows.append(row)

    # The inputs, held to this review's own transcription of the primaries.
    mine_q = [(9, PI_STAR, F("4.62e12")), (13, PI_STAR_13, F("2.17e13"))]
    inputs_q = len(quarter) == 2 and all(
        int(q[0]) == K and F(str(q[1])) == p.c0 and F(str(q[2])) == p.c1 and F(int(q[3])) == p.y0  # type: ignore[arg-type]
        and F(str(q[4])) == p.eps and F(str(q[5])) == p.om0 and F(int(q[6])) == k0  # type: ignore[arg-type]
        for q, (K, p, k0) in zip(quarter, mine_q, strict=False)
    )
    inputs_c = len(cube) == 8 and all(
        int(c[0]) == case and int(c[1]) == K and F(1, int(c[2])) == pp and F(str(c[3])) == F(gs) and F(str(c[4])) == F(bs)  # type: ignore[arg-type]
        and int(c[5]) == F(kas) and (c[6] is None if kbs is None else int(c[6]) == F(kbs))  # type: ignore[arg-type]
        and F(str(c[7])) == F(t0) and F(str(c[8])) == F(t1) and F(str(c[9])) == F(n0)
        and str(c[10]) == ls and str(c[11]) == rs
        for c, (case, K, pp, gs, bs, kas, kbs, t0, t1, n0, ls, rs) in zip(cube, CASES, strict=False)
    )
    inputs_g = all(tuple(F(x) for x in geometric[K]) == (v["Ab"], v["Apb"], v["SK"], v["CM"], v["CG"], v["CE"])
                   for K, v in VARIANTS.items())

    # 1-2: rosters.
    rec("quarter roster", inputs_q and [int(q[0]) for q in quarter] == [9, 13])  # type: ignore[arg-type]
    rec("cube roster", inputs_c)

    # 3-26: two quarter rows of 12.
    for K, p, k0 in mine_q:
        Ab, Apb, CLb = BARS[K]
        m = model(p, k0, Ab, Apb, CLb)
        alpha = p.c0 / sqrt(p.y0)
        beta = p.c1 / rpow(p.y0, 3, 4)
        bstar = p.c1 / rpow((1 - p.eps) * p.y0, 3, 4)
        pre = f"quarter K{K} "
        rec(pre + "alpha cap", lt(alpha, Iv(BBAR)), alpha)
        rec(pre + "beta cap", lt(beta, Iv(BBAR)), beta)
        rec(pre + "alpha small-angle domain", lt(alpha, Iv(F(1, 10**3))), alpha)
        rec(pre + "beta star small-angle domain", lt(bstar, Iv(F(1, 10**4))), bstar)
        rec(pre + "C3", lt(p.c1 / rpow(1 - p.eps, 3, 4), p.c0 * root(p.y0, 4)), m["C3_lhs"])
        rec(pre + "positive height", lt(Iv(0), m["h0"]), m["h0"])
        rec(pre + "inclination geometry", lt(Iv(DELTA), cos(2 * alpha) / 2), cos(2 * alpha) / 2)
        y1 = k0 / 2 - 3
        rec(pre + "scale window", lt(Iv(p.y0 + 1), Iv((1 - p.eps) * y1)), Iv((1 - p.eps) * y1))
        rec(pre + "inverse factor", (lt(Iv(0), m["invF"]) is True) and (lt(m["invF"], Iv(1)) is True), m["invF"])
        rec(pre + "threshold margin", lt(m["rhs_i"], m["Psi"]), m["Psi"] - m["rhs_i"])
        rec(pre + "positive derivative", lt(Iv(0), m["D1"]), m["D1"])
        rec(pre + "derivative loss", lt(m["iii_rhs"], m["iii_lhs"]), m["iii_lhs"] - m["iii_rhs"])

    # 27-90: eight cube cases of 8.
    for case, K, pp, gs, bs, kas, kbs, t0s, t1s, n0s, ls, rs in CASES:
        v = VARIANTS[K]
        B1 = B1_of(v)
        L1 = L1_of(v, B1)
        gamma, b, ka, tau0, tau1, nu0 = F(gs), F(bs), F(kas), F(t0s), F(t1s), F(n0s)
        cv = case_values(v, B1, L1, pp, gamma, b, ka, tau0, tau1, nu0)
        pre = f"cube case{case} "
        rec(pre + "tau ordering", DELTA < tau1 < tau0 < F(1, 2))
        rec(pre + "beta cap", lt(cv["beta"], Iv(BBAR)), cv["beta"])
        rec(pre + "height room", lt(Iv(tau1), tau0 - F("1.0001") * cv["beta"]), tau0 - F("1.0001") * cv["beta"])
        height = 1 - nu0 - cv["E"]
        rec(pre + "positive denominator", lt(Iv(0), height), height)
        rec(pre + "main margin", lt(cv["Rplus/k"], cv["left/k"]), cv["left/k"] - cv["Rplus/k"])
        rec(pre + "printed lower bound", lt(Iv(F(ls)), cv["left/k"]), cv["left/k"])
        rec(pre + "printed upper bound", lt(cv["Rplus/k"], Iv(F(rs))), cv["Rplus/k"])
        if pp == F(1, 2):
            assert kbs is not None
            gkb = gamma * sqrt(F(kbs))
            rec(pre + "finite linear branch", lt(gkb, cv["W1"]), gkb)
        else:
            rec(pre + "nonincreasing normalized exponents", 2 * pp - 1 <= 0 and 3 * pp - 1 <= 0,
                note="a property of p = 1/3, used by Proposition 5.1's monotonicity")

    # 91-108: the geometric ceilings and the asymptotic floors, per overlap.
    for K, qfloor, cfloor in ((9, "0.1696524", "0.062853"), (13, "0.1411593", "0.052297")):
        v = VARIANTS[K]
        A, Ap = A_exact(K), Ap_exact(K)
        S = (1 + F(1, 10**11)) * 4 * K / (F("0.32") * (2 - F(3, 10**6)))
        CL = 1 + (F("1185.6") if K == 9 else F("1712.6")) * DELTA**2
        geo = (
            ("A", A, v["Ab"]),
            ("A prime", Ap, v["Apb"]),
            ("C Lambda", Iv(CL), F("1.0000002")),
            ("S", Iv(S), v["SK"]),
            ("CM", 4 * Iv(S) / cos(PI / 4 + BBAR), v["CM"]),
            ("CG", Iv(S) / cos(BBAR), v["CG"]),
            ("CE", Iv(2 * K * F("41.933")), v["CE"]),
        )
        for name, value, ceiling in geo:
            rec(f"K{K} geometric {name} ceiling", lt(value, Iv(ceiling)), value)
        rec(f"quarter K{K} asymptotic floor", lt(Iv(F(qfloor)), c_inf(A, Ap)), c_inf(A, Ap))
        cbar = root(F(4, 27) / (v["Ab"] * v["Apb"] * B1_of(v)), 3)
        rec(f"cube K{K} asymptotic floor", lt(Iv(F(cfloor)), cbar), cbar)

    receipt = {
        "program": "qcc_predicates.py",
        "program_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in sorted(Path(__file__).resolve().parent.glob("*.py"))},
        "maintained_file": str(maintained.name),
        "maintained_sha256": hashlib.sha256(maintained.read_bytes()).hexdigest(),
        "inputs_match_primaries": {"quarter": inputs_q, "cube": inputs_c, "geometric": inputs_g},
        "summary": {"predicates": len(rows), "true": sum(1 for r in rows if r["verdict"] is True),
                    "false": sum(1 for r in rows if r["verdict"] is False),
                    "undecided": sum(1 for r in rows if r["verdict"] is None)},
        "predicates": rows,
    }
    out.write_text(json.dumps(receipt, indent=1) + "\n")
    print(receipt["summary"], receipt["inputs_match_primaries"])
    for r in rows:
        if r["verdict"] is not True:
            print("NOT TRUE:", r)
    return 0 if receipt["summary"]["true"] == 108 and all(receipt["inputs_match_primaries"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
