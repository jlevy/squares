"""Q's constants and thresholds, recomputed on exact-rational intervals.

Every value of the quarter-power preprint (Q, squarepacker/k2-minus-c-quarter abbedcf,
paper/paper.tex) that its theorems use, each in the direction the proof needs and,
separately, in its displayed rounding direction (Section 12.1): Sections 1-8, 10-11,
Table 2 (const-fixed) and Table 3 (const-main). The supplementary Tables 4 and 5 and
the sensitivity record of Section 12.6 are q_supplementary.py.

Usage: python -I q_constants.py OUT.json
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # run with python -I

from checks import Recorder
from iv import PI, Iv, ceil_int, cos, log, root, rpow, sin, sqrt, tan
from qmodel import (
    BARS,
    BBAR,
    DELTA,
    F050001,
    LAMBDA,
    PI_STAR,
    PI_STAR_13,
    A_exact,
    Ap_exact,
    CL_exact,
    Params,
    c0_opt,
    c_inf,
    constraints,
    derived,
    model,
)

F = Fraction


def main(out: Path) -> int:
    r = Recorder("q_constants.py")
    A9, A13 = A_exact(9), A_exact(13)
    Ap9, Ap13 = Ap_exact(9), Ap_exact(13)

    # Section 1 and 2: the constants of Theorems A and A13 and of [R].
    r.trunc("intro-cinf", "Q L131-137", "c_inf with exact A, A'", c_inf(A9, Ap9), "0.1696524")
    r.trunc("intro-cinf13", "Q L151-158", "c_inf^(13) with exact A13, A'13", c_inf(A13, Ap13), "0.1411593")
    k0, k013 = F("4.62e12"), F("2.17e13")
    r.fact("intro-147", "Q L129, L4926", "ceil(0.1 k0^(1/4)) = 147 at k0 = 4.62e12",
           ceil_int(F(1, 10) * root(k0, 4)) == 147, F(1, 10) * root(k0, 4))
    r.fact("intro-216", "Q L149, L5062", "ceil(0.1 k0^(1/4)) = 216 at k0 = 2.17e13",
           ceil_int(F(1, 10) * root(k013, 4)) == 216, F(1, 10) * root(k013, 4))
    r.below("intro-log", "Q L191", "log(4.62e12)", log(k0), "29.17")
    r.upper("intro-R-slope", "Q L191, [R] Remark 7.4", "30.418/1.99954", Iv(F("30.418") / F("1.99954")), "15.22")
    r.upper("intro-R-const", "Q L191, [R] Remark 7.4", "13.06675", Iv(F("13.06675")), "13.07")
    r.below("imp-A", "Q L479, L594", "A = 4 sqrt(9/0.32)/(2-3e-6)", A9, "10.6067")
    r.trunc("imp-A-trunc", "Q L594", "A", A9, "10.60661762")
    r.below("imp-A13", "Q L591", "A13", A13, "12.7476")
    r.trunc("imp-A13-trunc", "Q L594", "A13", A13, "12.74756790")
    r.below("imp-sec", "Q L512", "1/(2 - 1e-6), the coefficient of sec x - 1 <= x^2/(2-x^2)", Iv(1 / (2 - F(1, 10**6))),
            "0.5000003")

    # Section 3: constraints and the parameter vectors (Lemmas 3.3, 3.4).
    r.above("L3.3a", "Q L709", "(1 - (3e-6)^2/2)/2", Iv((1 - F(9, 10**12) / 2) / 2), "0.49")
    r.fact("L3.3b", "Q L713", "0.0037^3 = 5.0653e-8 > 5.0625e-8 = 0.015^4",
           F("0.0037") ** 3 == F("5.0653e-8") and F("0.015") ** 4 == F("5.0625e-8") and F("0.0037") ** 3 > F("0.015") ** 4)
    r.fact("L3.3b-2", "Q L713", "1.5e-6/0.015 = 1e-4", F("1.5e-6") / F("0.015") == F("1e-4"))
    for name, p, kk in (("pi*", PI_STAR, k0), ("pi*13", PI_STAR_13, k013)):
        cs = constraints(p, kk)
        for key in ("C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "Q1", "Q2"):
            r.fact(f"L3.4-{name}-{key}", "Q L726-751, Table 3", f"{name} satisfies ({key}) at k0 = {kk}", cs[key])
        # (C7) holds for every larger k (Lemma 3.3(e)); the least integer k is in q_supplementary.
    r.equal("L3.4-c0/bbar", "Q L727, L736", "c0/bbar at pi*", PI_STAR.c0 / BBAR, "205200")
    r.equal("L3.4-(c0/bbar)^2", "Q L727", "(c0/bbar)^2 at pi*", (PI_STAR.c0 / BBAR) ** 2, "42107040000")
    r.equal("L3.4-c0^2", "Q L735", "c0^2 at pi*", PI_STAR.c0**2, "0.09474084")
    r.equal("L3.4-bbar^2y0", "Q L735", "bbar^2 y0 at pi*", BBAR**2 * PI_STAR.y0, "0.094743")
    d = derived(PI_STAR)
    r.below("L3.4-bstar", "Q L727", "b* at pi*", d["bstar"], "1e-8")
    r.below("L3.4-betahat", "Q L737", "betahat(y0) at pi*", d["betahat_y0"], "1e-8")
    r.above("L3.4-w0-lo", "Q L727, L741", "w0 at pi*", d["w0"], "0.0473813")
    r.below("L3.4-w0-hi", "Q L727, L742", "w0 at pi*", d["w0"], "0.0473814")
    r.above("L3.4-h0-lo", "Q L728", "h0 at pi*", d["h0"], "0.9052372")
    r.below("L3.4-h0-hi", "Q L728", "h0 at pi*", d["h0"], "0.9052374")
    r.equal("L3.4-0.50001c0^2", "Q L739", "0.50001 c0^2 at pi*", F050001 * PI_STAR.c0**2, "0.0473713674084")
    r.below("L3.4-C3a", "Q L738", "c1 (1-eps)^(-3/4) at pi*", PI_STAR.c1 / rpow(1 - PI_STAR.eps, 3, 4), "0.2755")
    r.above("L3.4-C3b", "Q L738", "c0 y0^(1/4) at pi*", PI_STAR.c0 * root(PI_STAR.y0, 4), "97")
    r.above("L3.4-C7", "Q L746", "(1-eps)(k0/2-3) at pi*, k0 = 4.62e12", Iv((1 - PI_STAR.eps) * (k0 / 2 - 3)), "2e12")
    d13 = derived(PI_STAR_13)
    r.fact("L3.4-13-c0^2", "Q L748", "c0^2 = 0.13498276 <= 0.135 = 2.25e-12 * 6e10 at pi*13",
           PI_STAR_13.c0**2 == F("0.13498276") and F("2.25e-12") * F("6e10") == F("0.135")
           and PI_STAR_13.c0**2 <= F("0.135"))
    r.below("L3.4-13-bstar", "Q L749", "b* at pi*13", d13["bstar"], "1.1e-8")
    r.below("L3.4-13-betahat", "Q L749", "betahat(y0) at pi*13", d13["betahat_y0"], "1.1e-8")
    r.below("L3.4-13-C3a", "Q L749", "c1 (1-eps)^(-3/4) at pi*13", PI_STAR_13.c1 / rpow(1 - PI_STAR_13.eps, 3, 4), "0.302")
    r.above("L3.4-13-C3b", "Q L749", "c0 y0^(1/4) at pi*13", PI_STAR_13.c0 * root(PI_STAR_13.y0, 4), "97")
    r.below("L3.4-13-w0", "Q L750", "w0 at pi*13", d13["w0"], "0.0676")
    r.above("L3.4-13-C7", "Q L751", "(1-eps)(k0/2-3) at pi*13, k0 = 2.17e13", Iv((1 - PI_STAR_13.eps) * (k013 / 2 - 3)), "1e13")
    CL9, CL13 = CL_exact(9), CL_exact(13)
    r.below("D3.6-A", "Q L806", "A", A9, "10.6067")
    r.below("D3.6-A'", "Q L806", "A'", Ap9, "10.6068")
    r.below("D3.6-CL", "Q L806", "C_Lambda", Iv(CL9), "1.0000002")
    r.below("D3.6-A13", "Q L806", "A13", A13, "12.7476")
    r.below("D3.6-A'13", "Q L806", "A'13", Ap13, "12.7476")
    r.below("D3.6-CL13", "Q L806", "C_Lambda^(13)", Iv(CL13), "1.0000002")

    # Section 4: the auxiliary inequality (Lemma 4.6).
    def h(t: Fraction) -> Iv:
        return sin(t) + 1 - cos(t) - F("1.0001") * t

    t1, t2 = F("2.000133e-4"), F("2.000134e-4")
    r.below("L4.6-h(t1)", "Q L1898", "h(t1) = f(t1) - 1.0001 t1 < 0", h(t1), "0")
    r.above("L4.6-h(t2)", "Q L1898", "h(t2) > 0", h(t2), "0")
    rhs1 = Iv(t1 / 2 - t1**2 / 6 + t1**4 / 120 - F(1, 10**4))
    lhs2 = Iv(t2 / 2 - t2**2 / 6 - t2**3 / 24 - F(1, 10**4))
    r.below("L4.6-rhs(t1)", "Q L1898", "t1/2 - t1^2/6 + t1^4/120 - 1e-4", rhs1, "-1.7e-11")
    r.above("L4.6-lhs(t2)", "Q L1898", "t2/2 - t2^2/6 - t2^3/24 - 1e-4", lhs2, "3.2e-11")

    # Section 5: end collisions (Proposition 5.10).
    q4 = PI / 4
    ratio1 = 40 / (q4 * (2 - q4))
    r.trunc("P5.10-ratio1", "Q L2333", "40/((pi/4)(2-pi/4))", ratio1, "41.93109")
    am = F("1.5e-6")
    ratio2 = 40 * tan(q4 + am) / ((q4 - am) * (2 - q4 + am))
    r.upper("P5.10-ratio2", "Q L2338", "40 tan(pi/4+amax)/((pi/4-amax)(2-pi/4+amax))", ratio2, "41.9313")
    r.trunc("P5.10-ratio2t", "Q L2339", "the same", ratio2, "41.93124")
    r.below("P5.10-cE", "Q L2341", "both ratios <= c_E = 41.933", ratio1.hull(ratio2), "41.933")
    r.equal("P5.10-754", "Q L2360", "18 * 41.933", 18 * F("41.933"), "754.794")
    r.equal("P5.10-1090", "Q L2360", "26 * 41.933", 26 * F("41.933"), "1090.258")
    r.fact("P5.10-round", "Q L2321", "754.794 <= 754.8 and 1090.258 <= 1090.3",
           F("754.794") <= F("754.8") and F("1090.258") <= F("1090.3"))

    # Section 7: deaths, merges, gap overlap (Theorem 7.1, Lemmas 7.6, 7.8).
    S9 = (1 + F(1, 10**11)) * 4 * 9 / (F("0.32") * (2 - F(3, 10**6)))
    S13 = (1 + F(1, 10**11)) * 4 * 13 / (F("0.32") * (2 - F(3, 10**6)))
    r.upper("T7.1-S9", "Q L2952, L3142", "S_9", Iv(S9), "56.2501")
    r.upper("T7.1-S13", "Q L2952, L3142", "S_13", Iv(S13), "81.2502")
    r.trunc("L7.8-56", "Q L3142", "4*9/(0.32(2-3e-6))", Iv(F(36) / (F("0.32") * (2 - F(3, 10**6)))), "56.2500843")
    r.trunc("L7.8-81", "Q L3142", "4*13/(0.32(2-3e-6))", Iv(F(52) / (F("0.32") * (2 - F(3, 10**6)))), "81.2501218")
    r.upper("L7.8-cos2", "Q L3141", "1/cos^2(3e-6)", 1 / cos(F(3, 10**6)) ** 2, "1.00000000001",
            note="the text writes <= 1 + 1e-11")
    r.upper("L7.6-disc-r", "Q L3104", "1e-4 + sqrt(2)/2", F(1, 10**4) + sqrt(F(2)) / 2, "0.70721")
    r.below("L7.6-disc", "Q L3104", "4 pi 0.70721^2", 4 * PI * F("0.70721") ** 2, "6.29")
    th = F(3, 10**6)
    we = DELTA * tan(th) / cos(th)
    r.below("T7.1M-we", "Q L3206", "w_e = delta tan(theta)/cos(theta) at theta = 3e-6, in units of delta",
            we / DELTA, "3.1e-6")
    r.below("T7.1M-dist", "Q L3206", "(w_e^2 + delta^2)^(1/2)/delta", sqrt(we * we + DELTA**2) / DELTA, "1.01")
    r.below("T7.1M-dist2", "Q L3206", "(tan^2(3e-6) + 1)^(1/2)", sqrt(tan(th) ** 2 + 1), "1.01")
    m4 = 4 / cos(q4 + am)
    r.trunc("T7.1M-5.65", "Q L3217", "4/cos(pi/4 + 1.5e-6)", m4, "5.65686273")
    r.upper("T7.1M-5.65u", "Q L3217", "4/cos(pi/4 + 1.5e-6)", m4, "5.656863")
    r.trunc("T7.1M-318", "Q L3217", "5.656863 * 56.2501", Iv(F("5.656863") * F("56.2501")), "318.1991")
    r.trunc("T7.1M-459", "Q L3217", "5.656863 * 81.2502", Iv(F("5.656863") * F("81.2502")), "459.6212")
    r.below("T7.1M-CM9", "Q L2964", "4 S_9/cos(pi/4+amax) <= C_M = 318.20", 4 * Iv(S9) / cos(q4 + am), "318.20")
    r.below("T7.1M-CM13", "Q L2964", "4 S_13/cos(pi/4+amax) <= 459.7", 4 * Iv(S13) / cos(q4 + am), "459.7")
    r.below("T7.1G-9", "Q L3250", "S_9/cos(1.5e-6)", Iv(S9) / cos(am), "56.2501")
    r.below("T7.1G-13", "Q L3250", "S_13/cos(1.5e-6)", Iv(S13) / cos(am), "81.2502")
    r.equal("C7.2-sum9", "Q L3264", "56.2501 + 318.20 + 754.8 + 56.2501", F("56.2501") + F("318.20") + F("754.8") + F("56.2501"),
            "1185.5002")
    r.equal("C7.2-sum13", "Q L3266", "81.26 + 459.7 + 1090.3 + 81.26", F("81.26") + F("459.7") + F("1090.3") + F("81.26"),
            "1712.52")
    r.fact("C7.2-cap", "Q L3264-3266", "1185.5002 <= 1185.6, 1712.52 <= 1712.6, 1712.6e-10 < 2e-7",
           F("1185.5002") <= F("1185.6") and F("1712.52") <= F("1712.6") and F("1712.6") * DELTA**2 < F("2e-7"))
    r.fact("C7.2-S13-in-CD", "Q L2964", "S_13 <= 81.26 (C_D and C_G for K = 13)", S13 <= F("81.26"))
    r.above("R7.3-C6", "Q L2976", "cos(3e-6)/2", cos(F(3, 10**6)) / 2, "0.4999999")

    # Section 8: the path version of [R, Lemma 4.14] (Theorem 8.3, Lemma 8.9).
    r.below("P6-kappa", "Q L3490", "tan(pi/4 + bbar)", tan(q4 + BBAR), "1.00001")
    chi = cos(BBAR) - F("1.00001") * BBAR
    r.above("L8.9-chi", "Q L3589, L3612", "cos(1.5e-6) - 1.00001 * 1.5e-6", chi, "0.99999849")
    r.below("L8.9-1/chi", "Q L3613", "1/0.99999849", Iv(1 / F("0.99999849")), "1.0000016")
    r.below("T8.3-56.26", "Q L3884", "36/(0.32(2 - 1.5e-6))", Iv(F(36) / (F("0.32") * (2 - BBAR))), "56.26")
    r.below("T8.3-err9", "Q L3887", "1.0000016e-5 * 1.5e-6 * 56.26", Iv(F("1.0000016e-5") * BBAR * F("56.26")), "8.5e-10")
    r.below("T8.3-1/cos", "Q L3891", "1/cos(bbar) - 1", 1 / cos(BBAR) - 1, "1.2e-12")
    r.below("T8.3-A'", "Q L3892", "10.6067 (1 + 1.2e-12) + 1e-8", Iv(F("10.6067") * (1 + F("1.2e-12")) + F(1, 10**8)), "10.60671")
    r.below("T8.3-A'2", "Q L3421", "A/cos(bbar) + 8.5e-10 <= A'", A9 / cos(BBAR) + F("8.5e-10") - Ap9, "0")
    r.below("T8.3-81.26", "Q L3896", "52/(0.32(2 - 1.5e-6))", Iv(F(52) / (F("0.32") * (2 - BBAR))), "81.26")
    r.below("T8.3-err13", "Q L3897", "1.0000016e-5 * 1.5e-6 * 81.26", Iv(F("1.0000016e-5") * BBAR * F("81.26")), "1.22e-9")
    r.below("T8.3-A13", "Q L3899", "A13", A13, "12.74757")
    r.below("T8.3-A'13", "Q L3900", "12.74757 (1 + 1.2e-12) + 1e-8", Iv(F("12.74757") * (1 + F("1.2e-12")) + F(1, 10**8)), "12.7476")
    r.below("T8.3-A'13b", "Q L3426", "A13/cos(bbar) + 1.22e-9 <= A'13", A13 / cos(BBAR) + F("1.22e-9") - Ap13, "0")
    r.above("L8.12-a", "Q L3799", "1e-5 (2 - 1e-5)/40", Iv(F(1, 10**5) * (2 - F(1, 10**5)) / 40), "4.99e-7")
    r.equal("L8.12-b", "Q L3800", "0.32 * 1.5e-6 * 2/4", F("0.32") * BBAR * 2 / 4, "2.4e-7")

    # Sections 9-11.
    r.trunc("R9.3", "Q L4128", "1.0001 * pi/4", F("1.0001") * PI / 4, "0.7854767")
    r.upper("T10.3-tan", "Q L4777", "tan(1.5e-6)/1.5e-6", tan(BBAR) / BBAR, "1.000001",
            note="rounded-up display not claimed; the proof needs tan(bbar) <= 1.000001 bbar")
    co = c0_opt()
    r.below("P11.5-c0opt2", "Q L4976", "(c0_opt)^2", co * co, "0.2")
    r.below("P11.5-w0lim", "Q L4975", "0.50001 c0_opt^2 + delta + 1e-12", F050001 * co * co + DELTA + F(1, 10**12), "0.10002")
    r.fact("C-cor-146", "Q L5090", "10^4 * 146^4 + 1 = 4543718560001 < 4.62e12",
           10**4 * 146**4 + 1 == 4543718560001 and 4543718560001 < F("4.62e12"))
    r.fact("C-cor-215", "Q L5095", "10^4 * 215^4 + 1 = 21367506250001 < 2.17e13",
           10**4 * 215**4 + 1 == 21367506250001 and 21367506250001 < F("2.17e13"))
    r.fact("C-cor-147", "Q L5100", "10^4 * 147^4 + 1 = 4669488810001 > 4.62e12",
           10**4 * 147**4 + 1 == 4669488810001 and 4669488810001 > F("4.62e12"))
    r.fact("C-cor-216", "Q L5102", "10^4 * 216^4 + 1 = 21767823360001 > 2.17e13",
           10**4 * 216**4 + 1 == 21767823360001 and 21767823360001 > F("2.17e13"))

    # Section 12: Table 2 (const-fixed).
    r.equal("T2-lambda", "Q L5136", "lambda = 2 delta + 2e-12", LAMBDA, "2.0000002e-5")
    r.trunc("T2-c0opt", "Q L5138", "c0_opt", co, "0.4472046513")
    r.trunc("T2-A", "Q Table 2", "A", A9, "10.6066176277")
    r.trunc("T2-A'", "Q Table 2", "A'", Ap9, "10.6066176377")
    r.trunc("T2-A13", "Q Table 2", "A13", A13, "12.7475679053")
    r.trunc("T2-A'13", "Q Table 2", "A'13", Ap13, "12.7475679153")
    r.equal("T2-CL", "Q Table 2", "C_Lambda", CL9, "1.00000011856")
    r.equal("T2-CL13", "Q Table 2", "C_Lambda^(13)", CL13, "1.00000017126")
    r.trunc("T2-cinf", "Q Table 2", "c_inf, exact A, A'", c_inf(A9, Ap9), "0.1696524112")
    r.trunc("T2-cinf13", "Q Table 2", "c_inf^(13), exact", c_inf(A13, Ap13), "0.1411593387")
    Ab, Apb, CLb = BARS[9]
    Ab13, Apb13, CLb13 = BARS[13]
    r.trunc("T2-cinf+", "Q Table 2", "c_inf^+ with 10.6067, 10.6068", c_inf(Ab, Apb), "0.1696502940")
    r.trunc("T2-cinf13+", "Q Table 2", "c_inf^+(13) with 12.7476, 12.7476", c_inf(Ab13, Apb13), "0.1411589833")
    r.fact("T2-bars", "Q Table 2, L4850", "A < 10.6067, A' < 10.6068, C_L < 1.0000002 (and the K=13 analogues)",
           A9.hi < Ab and Ap9.hi < Apb and CL9 < CLb and A13.hi < Ab13 and Ap13.hi < Apb13 and CL13 < CLb13)
    r.below("T2-A'13cs", "Q L5170", "4 sqrt(13/Q*)/((2-bbar)cos bbar) + 1e-8 <= A'13 bound",
            4 * sqrt(F(13) / F("0.32")) / ((2 - BBAR) * cos(BBAR)) + F(1, 10**8), "12.7476")

    # Table 3 (const-main), both columns, with the bars of Section 11.1.
    rows = [
        ("A", PI_STAR, k0, BARS[9],
         dict(alpha_y0="1.4999830e-6", betahat_y0="2.9628e-9", C3_lhs="0.27541", C3_rhs="139.43", w0="0.04738138",
              C7_lhs="2.3099866e12", bstar="2.9628e-9", h0="0.9052372592", eps_y0="244226.4", invF="0.99998818",
              t1="0.00063282", t2="19.256900", t3="19.249235", Gamma="2.8472e-5", B="38.506796",
              Cwall="3.5789897", KW="0.3390769", Omega_bound="0.37941519", wall="1.3579231",
              lH_bound="5647.4855", Psi="146.62429", rhs_i="146.60896", D1="0.0086429", iii_lhs="10.655",
              iii_rhs="0.0044029", Psi_inf="0.1581428")),
        ("A13", PI_STAR_13, k013, BARS[13],
         dict(alpha_y0="1.4999043e-6", betahat_y0="2.4846e-9", C3_lhs="0.30121", C3_rhs="181.83", w0="0.06750274",
              C7_lhs="1.0849945e13", bstar="2.4846e-9", h0="0.8649945353", eps_y0="300000", invF="0.99999020",
              t1="0.00058920", t2="21.161355", t3="21.147482", Gamma="3.1351e-5", B="42.309457",
              Cwall="3.2792918", KW="0.4426483", Omega_bound="0.70158383", wall="2.3006981",
              lH_bound="9134.3029", Psi="215.83530", rhs_i="215.83156", D1="0.0055790", iii_lhs="10.125",
              iii_rhs="0.0052311", Psi_inf="0.1375313")),
    ]
    up = {"alpha_y0", "betahat_y0", "C3_lhs", "w0", "bstar", "t1", "t2", "t3", "Gamma", "B", "Cwall", "KW",
          "Omega_bound", "wall", "rhs_i", "iii_rhs"}
    lo = {"C3_rhs", "C7_lhs", "h0", "invF", "lH_bound", "Psi", "D1", "iii_lhs"}
    table3: dict[str, object] = {}
    for col, p, kk, bars, shown in rows:
        m = model(p, kk, *bars)
        conds = {"i": m["Psi"].lo >= m["rhs_i"].hi, "ii": m["D1"].lo > 0, "iii": m["iii_lhs"].lo >= m["iii_rhs"].hi}
        table3[col] = {key: [float(v.lo), float(v.hi)] for key, v in m.items()}
        for key, v in shown.items():
            where = f"Q Table 3, column Theorem {col}"
            if key == "eps_y0":
                r.equal(f"T3-{col}-{key}", where, key, m[key].lo, v)
            elif key == "Psi_inf":
                r.trunc(f"T3-{col}-{key}", where, "Psi_inf(pi) with B-bar", m[key], v)
            elif key in up:
                r.upper(f"T3-{col}-{key}", where, key, m[key], v)
            elif key in lo:
                r.lower(f"T3-{col}-{key}", where, key, m[key], v)
        for c, ok in conds.items():
            r.fact(f"T3-{col}-cond-{c}", f"Q Prop 11.2, L4923-4924 / L5058-5059", f"condition ({c}) at k0, Theorem {col}", ok)
        disp_sum = sum(Fraction(shown[x]) for x in ("t1", "t2", "t3", "Gamma"))
        r.fact(f"T3-{col}-dispsum", "Q L5237-5238", "the four displayed terms, each rounded up, add up to more "
               "than the displayed bound for B-bar", disp_sum > Fraction(shown["B"]), Iv(disp_sum))

    extra = {"table3_enclosures": table3}
    rec = r.write(out, extra)
    s = rec["summary"]
    print(f"q_constants: {s}")
    bad = [row["id"] for row in r.rows if row["needed"] is not True]
    disp_bad = [row["id"] for row in r.rows if row.get("display") is False]
    print("needed not proved:", bad)
    print("display convention false:", disp_bad)
    return 0 if not bad else 1


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
