"""The cube-root preprint's constants and its eight cases, on exact-rational intervals.

Written for the strongest-tier review of 2 November 2026 from the text of the
cube-root preprint (C, squarepacker/k2-minus-c-cube-root 15045f9, paper/paper.tex):
the constants B1 and L1 of Section 2.1, Lemma 2.1, W1 of Remark 6.1, Proposition 5.1
with Table 1 (conditions (i)-(iv) for the eight cases), the liminf constants of
Section 5 and the comparisons of Section 1. It also exhibits, for each liminf
constant, explicit parameters and a finite k_a at which (i)-(iii) hold, which the
text obtains by a limit. Nothing here is taken from the source's check_table_*.py.

Usage: python -I c_constants.py OUT.json
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python -I

from checks import Recorder, unit_of
from iv import Iv, cos, root, rpow, sqrt

F = Fraction
DELTA = F(1, 10**5)
BBAR = F(15, 10**7)

VARIANTS = {
    9: dict(Ab=F("10.6067"), Apb=F("10.6068"), SK=F("56.2501"), CM=F("318.20"), CG=F("56.2501"), CE=F("754.8"),
            B1_shown="5.3033531", L1_shown="100021.23"),
    13: dict(Ab=F("12.7476"), Apb=F("12.7476"), SK=F("81.2502"), CM=F("459.7"), CG=F("81.26"), CE=F("1090.3"),
             B1_shown="6.3738031", L1_shown="100025.52"),
}


def B1_of(v: dict) -> Iv:
    return (v["Ab"] / 2 + 2 * BBAR) / cos(BBAR)


def L1_of(v: dict, B1: Iv) -> Iv:
    return (1 + v["SK"] * DELTA**2) / DELTA + (v["CM"] + v["CE"] + v["CG"]) * DELTA + 4 * B1


def case_values(v: dict, B1: object, L1: object, p: Fraction, gamma: Fraction, b: Fraction, k: Fraction,
                tau0: Fraction, tau1: Fraction, nu0: Fraction) -> dict[str, Iv]:
    """R+(k) of Proposition 5.1 and the quantities of its conditions, at a real k."""
    B1, L1 = Iv.of(B1), Iv.of(L1)
    Ab, Apb = v["Ab"], v["Apb"]
    if p == F(1, 2):
        kp = sqrt(k)
    elif p == F(1, 3):
        kp = root(k, 3)
    else:
        raise ValueError("p must be 1/2 or 1/3")
    W = gamma * kp
    beta = b * kp / k  # b k^(p-1)
    E = F("0.50001") * beta * (Ab + beta / DELTA) * W
    m1 = Iv(1 / BBAR)
    m2 = B1 * W / (2 * tau1)
    mx = m1 if m2.hi <= m1.lo else (m2 if m2.lo >= m1.hi else m1.hull(m2))
    L = Apb * W * mx + L1 * W + 4 * DELTA
    Rplus = W / nu0 + Ab * W / (2 * beta) + beta * (k / 2) * L / (1 - nu0 - E)
    left = Iv((1 - 2 * tau0) * (k - 6))
    W1 = 2 * tau1 / (B1 * BBAR)
    return {"W": W, "beta": beta, "E": E, "L": L, "Rplus": Rplus, "left": left, "W1": W1,
            "Rplus/k": Rplus / k, "left/k": left / k}


CASES = [
    # case, variant, p, gamma, b, k_a, k_b, tau0, tau1, nu0, left/k_a >=, R+(k_a)/k_a <=
    (1, 9, F(1, 2), "1e-4", "1.2e-3", "1e8", "2.5e15", "0.0205", "0.02", "0.001", "0.95899994", "0.87266009"),
    (2, 9, F(1, 2), "7e-5", "1.2e-3", "2.5e15", "3.5e17", "0.1675", "0.167", "0.001", "0.66499999", "0.61085501"),
    (3, 9, F(1, 3), "0.06", "1", "3.5e17", None, "0.1675", "0.167", "0.01", "0.66499999", "0.62871651"),
    (4, 9, F(1, 3), "0.0625", "1", "1e21", None, "0.1668", "0.1667", "0.005", "0.66639999", "0.66296281"),
    (5, 13, F(1, 2), "8.5e-5", "1.2e-3", "1e8", "2.4e15", "0.0205", "0.02", "0.001", "0.95899994", "0.89044495"),
    (6, 13, F(1, 2), "6e-5", "1.2e-3", "2.4e15", "3.39e17", "0.1675", "0.167", "0.001", "0.66499999", "0.62854332"),
    (7, 13, F(1, 3), "0.05", "1", "3.39e17", None, "0.1675", "0.167", "0.01", "0.66499999", "0.63009391"),
    (8, 13, F(1, 3), "0.052", "1", "1e21", None, "0.1668", "0.1667", "0.005", "0.66639999", "0.66284161"),
]


def main(out: Path) -> int:
    r = Recorder("c_constants.py")
    results: dict[str, object] = {}
    B1s, L1s = {}, {}
    for K, v in VARIANTS.items():
        B1 = B1_of(v)
        L1 = L1_of(v, B1)
        B1s[K], L1s[K] = B1, L1
        r.upper(f"S2-B1-K{K}", "C L177", f"B1 = (A-bar/2 + 2 bbar)/cos(bbar), K = {K}", B1, v["B1_shown"])
        r.upper(f"S2-L1-K{K}", "C L177", f"L1, K = {K}", L1, v["L1_shown"])
    # Lemma 2.1: pi_theta = (theta, theta/2, 1, 1/2, 1/4) for 0 < theta <= bbar; w0 increases with theta.
    th = BBAR
    bstar = th * rpow(2, -1, 4)
    w0 = F("0.50001") * th**2 * (1 + F("1.0001")) + DELTA + F("1.0001") * bstar + F(1, 10**12)
    r.below("L2.1-w0", "C L200", "w0 at theta = bbar (the largest)", w0, "1.13e-5")
    r.fact("L2.1-C2", "C L197", "(C2): theta/2 <= 1.5e-6", th / 2 <= F("1.5e-6"))
    r.fact("L2.1-C3", "C L198", "(C3): c1 (1-eps)^(-3/4) = 2^(-1/4) theta < theta", (rpow(2, -1, 4)).hi < 1)
    r.fact("L2.1-C7", "C L201", "(C7): y0 + 1 = 2 <= (k/2 - 3)/2 exactly when k >= 14",
           2 <= (F(14) / 2 - 3) / 2 and not (2 <= (F(13) / 2 - 3) / 2))
    r.fact("L2.1-Q2", "C L202", "(Q2): b* = 2^(-1/4) theta <= 1e-4", bstar.hi <= F(1, 10**4))

    table = []
    for case, K, p, gs, bs, kas, kbs, t0s, t1s, n0s, left_s, rp_s in CASES:
        v = VARIANTS[K]
        gamma, b, ka, tau0, tau1, nu0 = F(gs), F(bs), F(kas), F(t0s), F(t1s), F(n0s)
        cv = case_values(v, B1s[K], L1s[K], p, gamma, b, ka, tau0, tau1, nu0)
        where = f"C Table 1, case {case}"
        ci = cv["beta"].hi <= BBAR and (tau0 - F("1.0001") * cv["beta"]).lo > tau1
        r.fact(f"C{case}-i", where, "(i): beta(k_a) <= bbar and tau0 - 1.0001 beta(k_a) > tau1", ci)
        r.fact(f"C{case}-ii", where, "(ii): E(beta(k_a), W(k_a)) < 1 - nu0", cv["E"].hi < 1 - nu0)
        r.fact(f"C{case}-iii", where, "(iii): (1 - 2 tau0)(k_a - 6) > R+(k_a)", cv["left"].lo > cv["Rplus"].hi)
        r.lower(f"C{case}-left", where, "(1 - 2 tau0)(k_a - 6)/k_a", cv["left/k"], left_s)
        r.upper(f"C{case}-Rplus", where, "R+(k_a)/k_a", cv["Rplus/k"], rp_s)
        r.below(f"C{case}-beta", "C L494", "beta(k_a)", cv["beta"], "2.5e-7")
        r.below(f"C{case}-E", "C L494", "E(beta(k_a), W(k_a))", cv["E"], "6.6e-7")
        row = {"case": case, "K": K, "left/k": float(cv["left/k"].lo), "R+/k": float(cv["Rplus/k"].hi),
               "beta": float(cv["beta"].hi), "E": float(cv["E"].hi)}
        if kbs is not None:
            kb = F(kbs)
            gkb = gamma * sqrt(kb)
            r.fact(f"C{case}-iv", where, "(iv): gamma k_b^(1/2) <= W1 = 2 tau1/(B1 bbar)", gkb.hi <= cv["W1"].lo)
            row["iv"] = [float(gkb.hi), float(cv["W1"].lo)]
            if case == 6:
                r.upper("C6-iv-l", "C L495", "gamma k_b^(1/2), case 6", gkb, "34934.23")
                r.lower("C6-iv-r", "C L495", "W1, case 6", cv["W1"], "34934.66")
        # The same with the decimal bounds for B1 and L1 in place of the expressions.
        cd = case_values(v, F(v["B1_shown"]), F(v["L1_shown"]), p, gamma, b, ka, tau0, tau1, nu0)
        ok_dec = cd["left"].lo > cd["Rplus"].hi and (kbs is None or (gamma * sqrt(F(kbs))).hi <= cd["W1"].lo)
        r.fact(f"C{case}-decimal", "C Table 1 caption", "(iii) (and (iv)) still hold with the decimal B1, L1", ok_dec)
        excess = cd["Rplus/k"] - Iv(F(rp_s))
        row["decimal_excess_over_entry"] = float(excess.hi)
        if case in (3, 4):
            r.fact(f"C{case}-decimal-excess", "C Table 1 caption",
                   "with the decimal B1, L1, R+(k_a)/k_a exceeds the entry by about 5e-9 (between 1e-9 and 1e-8)",
                   F(1, 10**9) < excess.lo and excess.hi < F(1, 10**8), excess)
        table.append(row)
    results["table1"] = table

    # Liminf constants.
    for K, shown in ((9, "0.062853"), (13, "0.052297")):
        v = VARIANTS[K]
        cbar = root(F(4, 27) / (v["Ab"] * v["Apb"] * B1s[K]), 3)
        r.above(f"S5-cbar-K{K}", "C L499", f"c-bar_infinity, K = {K}", cbar, shown)
    # W1 values of Remark 6.1 (approximate displays).
    for K, t1s, shown in ((9, "0.02", "5.03e3"), (9, "0.167", "4.20e4"), (13, "0.02", "4183.79"), (13, "0.167", "34934.66")):
        W1 = 2 * F(t1s) / (B1s[K] * BBAR)
        u = unit_of(shown)
        near = W1.lo >= F(shown) - u / 2 and W1.hi <= F(shown) + u / 2
        r.fact(f"R6.1-W1-K{K}-{t1s}", "C L522-523", f"W1 ~ {shown} (tau1 = {t1s}, K = {K}), to nearest", near, W1)

    # Comparisons of Section 1.
    r.fact("S1-1e12", "C L109", "1e-4 sqrt(k) >= 0.1 k^(1/4) exactly when k >= 1e12", F(10**12) ** 1 == (F(1, 10) / F(1, 10**4)) ** 4)
    r.upper("S1-4.17e12", "C L110", "(0.1/7e-5)^4, beyond which 7e-5 sqrt(k) >= 0.1 k^(1/4)",
            Iv((F(1, 10) / F("7e-5")) ** 4), "4.17e12", note="the text names 4.17e12, an upper bound")
    r.upper("S1-460", "C L111", "(5/3)^12, beyond which 0.06 k^(1/3) >= 0.1 k^(1/4)", Iv(F(5, 3) ** 12), "460",
            note="the text names 460, an upper bound")
    r.above("S1-214.9", "C L111", "1e-4 sqrt(4.62e12)", F(1, 10**4) * sqrt(F("4.62e12")), "214.9")
    r.fact("S1-W>=4", "C L113", "1e-4 sqrt(9e8) = 3, so W > 3 from k >= 9e8", F(1, 10**4) ** 2 * F("9e8") == 9)
    r.fact("S1-W>=6", "C L113", "1e-4 sqrt(2.5e9) = 5, so W > 5 from k >= 2.5e9", F(1, 10**4) ** 2 * F("2.5e9") == 25)

    # The liminf by explicit parameters: (i)-(iii) at a finite k_a.
    witnesses = []
    for K, gs in ((9, "0.06285"), (13, "0.05229")):
        v = VARIANTS[K]
        gamma = F(gs)
        tau0 = F(1, 6)
        tau1 = F(1, 6) - F(1, 10**6)
        nu0 = F(1, 10**5)
        b_opt = sqrt(2 * v["Ab"] * tau1 * (1 - nu0) / (v["Apb"] * B1s[K] * gamma))
        b = F(round(b_opt.mid() * 10**6), 10**6)
        found = None
        for e in range(20, 40):
            ka = F(10) ** e
            cv = case_values(v, B1s[K], L1s[K], F(1, 3), gamma, b, ka, tau0, tau1, nu0)
            ci = cv["beta"].hi <= BBAR and (tau0 - F("1.0001") * cv["beta"]).lo > tau1
            if ci and cv["E"].hi < 1 - nu0 and cv["left"].lo > cv["Rplus"].hi:
                found = (e, cv)
                break
        ok = found is not None
        r.fact(f"S5-witness-K{K}", "C L498-511",
               f"gamma = {gs}: with tau0 = 1/6, tau1 = 1/6 - 1e-6, nu0 = 1e-5, b = {b}, (i)-(iii) hold at a finite k_a",
               ok, None if not ok else found[1]["Rplus/k"],
               note=("k_a = 1e%d" % found[0]) if ok else "no k_a <= 1e39 found")
        witnesses.append({"K": K, "gamma": gs, "b": str(b), "k_a_exp10": None if not ok else found[0]})
    results["liminf_witnesses"] = witnesses

    rec = r.write(out, {"results": results})
    print(f"c_constants: {rec['summary']}")
    print("not proved:", [row["id"] for row in r.rows if row["needed"] is not True])
    print("display false:", [row["id"] for row in r.rows if row.get("display") is False])
    for row in table:
        print(row)
    print(witnesses)
    return 0 if all(row["needed"] is True for row in r.rows) else 1


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
