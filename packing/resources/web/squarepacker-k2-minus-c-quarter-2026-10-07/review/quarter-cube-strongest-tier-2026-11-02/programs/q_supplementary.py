"""Q's supplementary optimization and sensitivity tables, executed.

Table 4 (tab:const-pairs, further thresholds c* k^(1/4) from k0), Table 5
(tab:const-k, lower bounds for W at single k) and the sensitivity record of
Section 12.6 (subsec:const-sens) of the quarter-power preprint (Q,
squarepacker/k2-minus-c-quarter abbedcf, paper/paper.tex lines 5264-5391), on the
exact-rational intervals of iv.py, with Q's quantities from qmodel.py. Every
parameter set is held to (C0)-(C7) at its k, and every threshold claim to
conditions (i)-(iii) of Proposition 11.2. Where the text names a largest value or a
crossing point, the program brackets it by bisection with each end decided on
intervals, and holds the displayed digits to the bracket.

Usage: python -I q_supplementary.py OUT.json
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python -I

from checks import Recorder
from iv import Iv, root
from qmodel import BARS, BW, PI_STAR, PI_STAR_13, Params, conditions, constraints, model

F = Fraction


def all_constraints(p: Params, k: Fraction) -> bool:
    cs = constraints(p, k)
    return all(cs[key] is True for key in ("C0", "C1", "C2", "C4", "C5", "C6", "C7"))


def bisect(pred, lo: Fraction, hi: Fraction, tol: Fraction, integer: bool = False) -> tuple[Fraction, Fraction]:
    """A bracket [a, b] with pred(a) True and pred(b) False, b - a <= tol (or b = a + 1
    for integers); pred must be decided (True/False) at every point it is called on."""
    a, b = lo, hi
    if pred(a) is not True or pred(b) is not False:
        raise ArithmeticError(f"bad initial bracket: {pred(a)}, {pred(b)}")
    while (b - a > 1) if integer else (b - a > tol):
        m = (a + b) // 2 if integer else (a + b) / 2
        v = pred(m)
        if v is None:
            raise ArithmeticError(f"undecided at {m}")
        if v:
            a = m
        else:
            b = m
    return a, b


def main(out: Path) -> int:
    r = Recorder("q_supplementary.py")
    results: dict[str, object] = {}

    # ---- Table 4: further thresholds, W >= c* k^(1/4) for all integers k >= k0.
    table4 = [
        (9, "0.12", "2.17e13", ("0.3674", "0.3009", "6e10", "5e-6", "1.5e-5"), "0.1200448", "0.0067036", "12.166", "0.0062733"),
        (9, "0.14", "2.01e14", ("0.4086", "0.3173", "7.422e10", "4.7e-6", "1.5e-5"), "0.1400019", "0.0041135", "13.024", "0.0077586"),
        (9, "0.15", "1.18e15", ("0.4243", "0.3234", "8.003e10", "4.6e-6", "1.4e-5"), "0.1500058", "0.0027026", "13.320", "0.0083679"),
        (9, "0.16", "2.77e16", ("0.4376", "0.3284", "8.5109e10", "4.5e-6", "1.4e-5"), "0.1600075", "0.0012500", "13.560", "0.0088999"),
        (13, "0.12", "3.78e14", ("0.4153", "0.3203", "7.667e10", "4.6e-6", "1.3e-5"), "0.1200086", "0.0029558", "10.959", "0.0066855"),
    ]
    t4 = []
    for K, cstar, k0s, ps, psi_r, d1, iii_l, iii_r in table4:
        p = Params.of(*ps)
        k0, cs = F(k0s), F(cstar)
        m = model(p, k0, *BARS[K], cstar=cs)
        cid = f"T4-K{K}-c{cstar}"
        where = f"Q Table 4, column K={K}, c*={cstar}"
        r.fact(f"{cid}-constraints", where, "(C0)-(C7) at k0", all_constraints(p, k0))
        ratio = m["Psi"] / root(k0, 4)
        r.lower(f"{cid}-ratio", where, "Psi-bar(k0)/k0^(1/4)", ratio, psi_r)
        r.fact(f"{cid}-i", where, "(i): Psi-bar(k0) >= c* k0^(1/4)", conditions(m)["i"])
        r.lower(f"{cid}-D1", where, "D1", m["D1"], d1)
        r.lower(f"{cid}-iii-l", where, "y1(k0)^(1/4) D1", m["iii_lhs"], iii_l)
        r.upper(f"{cid}-iii-r", where, "K_W/(2 B-bar)", m["iii_rhs"], iii_r)
        cond = conditions(m)
        r.fact(f"{cid}-ii", where, "(ii): D1 > 0", cond["ii"])
        r.fact(f"{cid}-iii", where, "(iii)", cond["iii"])
        t4.append({"K": K, "c*": cstar, "k0": k0s, "ratio": [float(ratio.lo), float(ratio.hi)],
                   "D1": float(m["D1"].lo), "iii": [float(m["iii_lhs"].lo), float(m["iii_rhs"].hi)]})
    results["table4"] = t4
    # The example after Table 4.
    r.fact("T4-2065", "Q L5299-5300", "(2065/0.16)^4 > 2.77e16 > (2064/0.16)^4",
           (F(2065) / F("0.16")) ** 4 > F("2.77e16") > (F(2064) / F("0.16")) ** 4)

    # ---- Table 5: lower bounds for W at given k (no monotonicity needed).
    table5 = [
        (9, "1e13", ("0.3421", "0.2903", "5.2015e10", "5.3e-6", "1.6e-5"), "36.52537", "196.77", 197),
        (9, "1e14", ("0.3993", "0.3136", "7.0863e10", "4.8e-6", "1.5e-5"), "33.80809", "426.16", 427),
        (9, "1e16", ("0.4345", "0.3273", "8.393e10", "4.5e-6", "1.4e-5"), "32.40967", "1575.76", 1576),
        (9, "1e20", ("0.4457", "0.3324", "2.458e11", "2.7e-6", "9.5e-6"), "31.91017", "16751.28", 16752),
        (9, "1e30", ("0.4472", "0.3343", "5.473e14", "5.7e-8", "5.3e-7"), "31.72495", "5363347.52", 5363348),
        (13, "1e13", ("0.3421", "0.2907", "5.2015e10", "5.3e-6", "1.4e-5"), "43.84613", "163.91", 164),
        (13, "1e14", ("0.3993", "0.314", "7.0863e10", "4.8e-6", "1.3e-5"), "40.58423", "355.01", 356),
        (13, "1e16", ("0.4345", "0.3276", "8.393e10", "4.5e-6", "1.3e-5"), "38.90551", "1312.66", 1313),
        (13, "1e20", ("0.4458", "0.3325", "1.928e11", "3e-6", "9.5e-6"), "38.33686", "13948.51", 13949),
        (13, "1e30", ("0.4472", "0.3343", "4.287e14", "6.4e-8", "5.3e-7"), "38.12805", "4462691.45", 4462692),
    ]
    t5 = []
    for K, ks, ps, bbar_s, psi_s, wmin in table5:
        p = Params.of(*ps)
        k = F(ks)
        m = model(p, k, *BARS[K])
        cid = f"T5-K{K}-k{ks}"
        where = f"Q Table 5, K={K}, k={ks}"
        r.fact(f"{cid}-constraints", where, "(C0)-(C7) at k", all_constraints(p, k))
        r.upper(f"{cid}-B", where, "B-bar", m["B"], bbar_s)
        r.lower(f"{cid}-Psi", where, "Psi-bar(k)", m["Psi"], psi_s)
        ce = math.ceil(m["Psi"].lo)
        r.fact(f"{cid}-W", where, f"W >= ceil(Psi-bar(k)) = {wmin}", ce == wmin and math.ceil(m["Psi"].hi) == wmin,
               note="W is an integer and W >= Psi-bar(k) (Lemma 11.1)")
        t5.append({"K": K, "k": ks, "B": float(m["B"].hi), "Psi": float(m["Psi"].lo), "W>=": ce})
    results["table5"] = t5

    # ---- Section 12.6: sensitivity of the threshold of Theorem A.
    k0 = F("4.62e12")
    Ab, Apb, CLb = BARS[9]
    m0 = model(PI_STAR, k0, Ab, Apb, CLb)
    bcrit = m0["numerator"] / m0["rhs_i"]
    r.lower("S-Bcrit", "Q L5334-5337", "B_crit at pi*, k0 = 4.62e12", bcrit, "38.510824")
    margin = (bcrit - m0["B"]) / m0["B"]
    r.trunc("S-margin", "Q L5338", "(B_crit - B-bar)/B-bar", margin, "1.0463e-4")
    r.below("S-margin<", "Q L5338", "(B_crit - B-bar)/B-bar", margin, "1.05e-4")

    def cond_i(A: Fraction, Ap: Fraction, CL: Fraction, bw: Fraction = BW, wf: Fraction = F(1),
               p: Params = PI_STAR, k: Fraction = k0) -> bool | None:
        return conditions(model(p, k, A, Ap, CL, bw=bw, wall_factor=wf))["i"]

    def all3(A: Fraction, Ap: Fraction, CL: Fraction, bw: Fraction = BW, wf: Fraction = F(1),
             p: Params = PI_STAR, k: Fraction = k0) -> bool:
        c = conditions(model(p, k, A, Ap, CL, bw=bw, wall_factor=wf))
        return c["i"] is True and c["ii"] is True and c["iii"] is True

    tol = F(1, 10**13)
    sens: dict[str, object] = {}
    cases = [
        ("a", "A' up to 10.60905 (A <= 10.6067)", "10.60905", "10.6090514",
         lambda x: cond_i(Ab, x, CLb), F("10.6"), F("10.62"), lambda x: all3(Ab, x, CLb)),
        ("b", "A up to 10.60891 (A' <= 10.6068)", "10.60891", "10.6089191",
         lambda x: cond_i(x, Apb, CLb), F("10.6"), F("10.62"), lambda x: all3(x, Apb, CLb)),
        ("c", "A <= 10.60781 with A' = A + 1e-4", "10.60781", "10.6078176",
         lambda x: cond_i(x, x + F(1, 10**4), CLb), F("10.6"), F("10.62"), lambda x: all3(x, x + F(1, 10**4), CLb)),
        ("d", "C_Lambda up to 1.0150", "1.0150", "1.0150101",
         lambda x: cond_i(Ab, Apb, x), F("1"), F("1.1"), lambda x: all3(Ab, Apb, x)),
        ("e", "b_W in Theorem 9.1 up to 53.09", "53.09", "53.0942",
         lambda x: cond_i(Ab, Apb, CLb, bw=x), F("2"), F("100"), lambda x: all3(Ab, Apb, CLb, bw=x)),
        ("f", "wall term up to 1.434 times its bound", "1.434", "1.43499",
         lambda x: cond_i(Ab, Apb, CLb, wf=x), F("1"), F("2"), lambda x: all3(Ab, Apb, CLb, wf=x)),
    ]
    for tag, what, shown, largest, pred, lo, hi, at_extreme in cases:
        a, b = bisect(pred, lo, hi, tol)
        sens[tag] = {"what": what, "bracket": [str(a), str(b)], "float": float(a)}
        where = f"Q L5343-5362, ({tag})"
        r.fact(f"S-{tag}-holds", where, f"(i)-(iii) hold at the extreme value {shown}", at_extreme(F(shown)))
        u = F(1, 10 ** (len(largest.split('.')[1])))
        trunc_ok = F(largest) <= a and b < F(largest) + u
        r.fact(f"S-{tag}-largest", where, f"the largest value for which (i) holds is {largest}...",
               trunc_ok, Iv(a, b))
        nxt = F(shown) + F(1, 10 ** (len(shown.split('.')[1])))
        r.fact(f"S-{tag}-rounded-down", where, f"{shown} is that value rounded down: (i) fails at {nxt}",
               pred(nxt) is False)
    results["sensitivity"] = sens

    # C_Lambda = 2.
    def phi_cl2(k: Fraction) -> bool | None:
        return cond_i(Ab, Apb, F(2), k=k)

    c2 = conditions(model(PI_STAR, k0, Ab, Apb, F(2)))
    r.fact("S-CL2-ii-iii", "Q L5364-5366", "with C_Lambda = 2, (ii) and (iii) hold at 4.62e12", c2["ii"] is True and c2["iii"] is True)
    r.fact("S-CL2-i-fails", "Q L5367", "with C_Lambda = 2, (i) fails at 4.62e12", c2["i"] is False)
    za, zb = bisect(lambda k: not phi_cl2(k) if phi_cl2(k) is not None else None, F("4.62e12"), F("5e12"), F(1), integer=False)
    # za: (i) fails, zb: (i) holds; the crossing lies in (za, zb].
    r.fact("S-CL2-zero", "Q L5367", "the crossing point is 4.8449...e12", F("4.8449e12") <= za and zb < F("4.8450e12"), Iv(za, zb))
    r.fact("S-CL2-4.845", "Q L5368", "at 4.845e12, (i)-(iii) and (C7) hold with C_Lambda = 2",
           all3(Ab, Apb, F(2), k=F("4.845e12")) and constraints(PI_STAR, F("4.845e12"))["C7"] is True)
    results["CL2_crossing"] = [str(za), str(zb)]

    # The least integer k with (C7), and conditions (ii), (iii) there.
    def kmin(p: Params) -> int:
        return math.ceil(2 * (p.y0 + 1) / (1 - p.eps) + 6)

    km = kmin(PI_STAR)
    r.fact("S-kmin", "Q L5374", "the least integer k with (C7) at pi* is 84216488464",
           km == 84216488464 and constraints(PI_STAR, F(km))["C7"] is True and constraints(PI_STAR, F(km - 1))["C7"] is False)
    cm = conditions(model(PI_STAR, F(km), Ab, Apb, CLb))
    r.fact("S-kmin-ii-iii", "Q L5374-5375", "(ii) and (iii) hold at that k", cm["ii"] is True and cm["iii"] is True)

    # k*: the least k at which (i) holds, between the two named integers.
    lo_k, hi_k = 4616673963026, 4616673963027
    i_lo = conditions(model(PI_STAR, F(lo_k), Ab, Apb, CLb))["i"]
    i_hi = conditions(model(PI_STAR, F(hi_k), Ab, Apb, CLb))["i"]
    r.fact("S-kstar", "Q L5376-5379", "(i) fails at 4616673963026 and holds at 4616673963027", i_lo is False and i_hi is True)
    ka, kb = bisect(lambda k: not cond_i(Ab, Apb, CLb, k=k) if cond_i(Ab, Apb, CLb, k=k) is not None else None,
                    F(lo_k), F(hi_k), F(1, 10**6))
    r.fact("S-kstar-trunc", "Q L5377", "k* = 4.616673...e12", F("4.616673e12") <= ka and kb < F("4.616674e12"), Iv(ka, kb))
    ratio = F("4.62e12") / Iv(ka, kb) - 1
    r.trunc("S-k0/k*", "Q L5381", "k0/k* - 1", ratio, "7.20e-4")
    r.below("S-k0/k*-intro", "Q L143", "4.62e12/k* - 1", ratio, "7.3e-4")
    # phi at the two integers, for the record.
    phis = {}
    for kk in (lo_k, hi_k):
        mm = model(PI_STAR, F(kk), Ab, Apb, CLb)
        phis[str(kk)] = [float((mm["Psi"] - mm["rhs_i"]).lo), float((mm["Psi"] - mm["rhs_i"]).hi)]
    results["kstar"] = {"bracket": [str(ka), str(kb)], "phi": phis}

    # Theorem A13.
    k013 = F("2.17e13")
    A13b, Ap13b, CL13b = BARS[13]
    m13 = model(PI_STAR_13, k013, A13b, Ap13b, CL13b)
    margin13 = (m13["numerator"] / m13["rhs_i"] - m13["B"]) / m13["B"]
    r.trunc("S13-margin", "Q L5383", "relative margin for Theorem A13", margin13, "1.7385e-5")
    km13 = kmin(PI_STAR_13)
    r.fact("S13-kmin", "Q L5385", "the least integer k with (C7) at pi*13 is 120000600012",
           km13 == 120000600012 and constraints(PI_STAR_13, F(km13 - 1))["C7"] is False)
    cm13 = conditions(model(PI_STAR_13, F(km13), A13b, Ap13b, CL13b))
    r.fact("S13-kmin-ii-iii", "Q L5385", "(ii) and (iii) hold at that k", cm13["ii"] is True and cm13["iii"] is True)
    lo13, hi13 = 21695977343082, 21695977343083
    j_lo = conditions(model(PI_STAR_13, F(lo13), A13b, Ap13b, CL13b))["i"]
    j_hi = conditions(model(PI_STAR_13, F(hi13), A13b, Ap13b, CL13b))["i"]
    r.fact("S13-kstar", "Q L5387-5389", "(i) fails at 21695977343082 and holds at 21695977343083", j_lo is False and j_hi is True)

    def c13(k: Fraction) -> bool | None:
        return cond_i(A13b, Ap13b, CL13b, p=PI_STAR_13, k=k)

    ka13, kb13 = bisect(lambda k: not c13(k) if c13(k) is not None else None, F(lo13), F(hi13), F(1, 10**6))
    r.fact("S13-kstar-trunc", "Q L5388", "k*13 = 2.169597...e13", F("2.169597e13") <= ka13 and kb13 < F("2.169598e13"), Iv(ka13, kb13))
    r.trunc("S13-k0/k*", "Q L5391", "2.17e13/k*13 - 1", F("2.17e13") / Iv(ka13, kb13) - 1, "1.85e-4")
    results["kstar13"] = [str(ka13), str(kb13)]

    rec = r.write(out, {"results": results})
    print(f"q_supplementary: {rec['summary']}")
    bad = [row["id"] for row in r.rows if row["needed"] is not True]
    print("not proved:", bad)
    print("display false:", [row["id"] for row in r.rows if row.get("display") is False])
    for tag, v in sens.items():
        print(tag, v["float"])
    print("CL2 crossing", float(za), "k*", float(ka), "k*13", float(ka13))
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
